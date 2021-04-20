#!/usr/bin/env python
import concurrent.futures
from simple_salesforce import Salesforce
import requests
import os
import csv
import re
import logging
import sys

SCRIPT_FOLDER_PATH = os.path.dirname(os.path.realpath(__file__))
DEFAULT_EXPORT_CONTENT_VERSION_CONFIG = SCRIPT_FOLDER_PATH + '/../etc/export_content_version.ini'

def split_into_batches(items, batch_size):
    full_list = list(items)
    for i in range(0, len(full_list), batch_size):
        yield full_list[i:i + batch_size]

def get_content_document_ids(content_document_links):
    content_document_ids = set()

    for content_document_link in content_document_links:
       content_document_ids.add(content_document_link["ContentDocumentId"])

    return content_document_ids

def download_file(args):
    record, output_directory, sf = args
    filename = os.path.join(output_directory, record['Id'])
    url = "https://%s%s" % (sf.sf_instance, record["VersionData"])

    logging.debug("Downloading from " + url)
    response = requests.get(url, headers={"Authorization": "OAuth " + sf.session_id,
                                          "Content-Type": "application/octet-stream"})

    if response.ok:
        # Save File
        if not os.path.isdir(output_directory):
           os.mkdir(output_directory)

        with open(filename, "wb") as output_file:
            output_file.write(response.content)
        return "Saved file to %s" % filename
    else:
        return "Couldn't download %s" % url

def fetch_content_versions(sf, query_string, output_file_name, output_directory, valid_content_document_ids=None, batch_size=100):
    # Divide the full list of files into batches of 100 ids
    batches = list(split_into_batches(valid_content_document_ids, batch_size))

    i = 0
    for batch in batches:
        i = i + 1
        logging.info("Processing batch {0}/{1}".format(i, len(batches)))
        batch_query = query_string + ' AND ContentDocumentId in (' + ",".join("'" + item + "'" for item in batch) + ')'
        query_response = sf.query(batch_query)
        records_to_process = get_records_from_response(query_response)
        if records_to_process:
           if(i == 1):
              with open(output_file_name, 'w') as output_file:
                 print_as_csv(records_to_process, output_file)
           else:
              with open(output_file_name, 'a') as output_file:
                 print_as_csv(records_to_process, output_file, write_header = False)

           records_to_process = len(get_records_from_response(query_response))
           logging.debug("Content Version Query found {0} results".format(records_to_process))

           while query_response:
              with concurrent.futures.ProcessPoolExecutor() as executor:
                 args = ((record, output_directory, sf) for record in query_response["records"])
                 for result in executor.map(download_file, args):
                    logging.debug(result)
              break

        logging.debug('All files in batch {0} downloaded'.format(i))
    logging.debug('All batches complete')


def print_as_csv(list_of_dicts, csv_file = sys.stdout, write_header = True):
    writer = csv.DictWriter(csv_file, list_of_dicts[0].keys(), quoting=csv.QUOTE_ALL)
    if write_header == True:
       writer.writeheader()
    writer.writerows(list_of_dicts)

def get_records_from_response(result):
    if 'totalSize' in result and result['totalSize'] > 0 and 'records' in result:
        # remove 'attributes' so that we can convert dictionary to CSV
        records = remove_key_from_dict_array(result['records'], 'attributes')
        return records
    else:
        return None

def remove_key_from_dict_array(dict_array, key):
    for record in dict_array:
        record.pop(key, None)
    return dict_array

def main():
    import argparse
    import configparser

    parser = argparse.ArgumentParser(description='Export ContentDocumentLink and ContentVersion (Files) related to parent records (e.g. Account) from Salesforce\n' +
                                                 'Example:\n' +
                                                 '\t' + os.path.basename(__file__) + ' -q "SELECT Id FROM Account" -s ~/Workspace/salesforce-file-export-import/etc/sf_credentials_myproject_uat.ini -o content_version_account_dev --include-notes True',
                                                 formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('-q', '--query', metavar='query', required=True,
                        help='SOQL to limit the valid ContentDocumentIds. Must return the Ids of parent objects.')

    parser.add_argument(
        "-o", "--output-folder", dest="output_folder",
        help="Output folder", required=True)

    parser.add_argument(
        "-s", "--salesforce-config-file", dest="salesforce_config_file",
        help="Salesforce config file with login info", required=True)

    parser.add_argument(
        "-c", "--basic-config-file", dest="basic_config_file",
        help="Optional parameter to override default basic configuration of the script", required=False)

    parser.add_argument(
        "--include-notes", dest="include_notes", default=False,
        help="By default notes are included in the export - set this flag to False if you want to exclude them", required=False)

    args = parser.parse_args()

    if not os.path.isdir(args.output_folder):
       os.mkdir(args.output_folder)

    # Get SF credentials from config file
    salesforce_config = configparser.ConfigParser(allow_no_value=True)
    salesforce_config.read(args.salesforce_config_file)

    username = salesforce_config['salesforce']['username']
    password = salesforce_config['salesforce']['password']
    token = salesforce_config['salesforce']['security_token']
    is_sandbox = salesforce_config['salesforce']['connect_to_sandbox']

    if is_sandbox == 'True':
       domain = 'test'
    else:
       domain = 'login'

    export_content_version_config = configparser.ConfigParser(allow_no_value=True)
    if args.basic_config_file:
       export_content_version_config.read(args.basic_config_file)
    else:
       export_content_version_config.read(DEFAULT_EXPORT_CONTENT_VERSION_CONFIG)

    content_document_link_output_file = os.path.join(args.output_folder, export_content_version_config['export_content_version']['content_document_link_output_file'])
    content_document_link_query_fields = export_content_version_config['export_content_version']['content_document_link_query_fields']
    content_version_output_file = os.path.join(args.output_folder, export_content_version_config['export_content_version']['content_version_output_file'])
    content_version_query_fields = export_content_version_config['export_content_version']['content_version_query_fields']

    batch_size = int(export_content_version_config['export_content_version']['batch_size'])
    loglevel = logging.getLevelName(export_content_version_config['export_content_version']['loglevel'])
    logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s', level=loglevel)

    content_document_link_query = 'SELECT ' + content_document_link_query_fields + ' ' \
                             'FROM ContentDocumentLink ' \
                             'WHERE LinkedEntityId in ({0})'.format(args.query)
    content_version_output = export_content_version_config['export_content_version']['content_version_output_dir']
    content_version_query = "SELECT " + content_version_query_fields + " FROM ContentVersion " \
            "WHERE IsLatest = True"
    if not args.include_notes:
       content_version_query = content_version_query + " AND FileExtension != 'snote'"

    # Output
    logging.info('Export ContentVersion (Files) from Salesforce')
    logging.info('Username: ' + username)
    logging.info('Signing in at: https://'+ domain + '.salesforce.com')
    logging.info('Output directory: ' + content_version_output)

    # Connect
    sf = Salesforce(username=username, password=password, security_token=token, domain=domain)
    logging.debug("Connected successfully to {0}".format(sf.sf_instance))

    # Get Content Document Ids
    logging.debug("Querying to get Content Document Ids...")
    
    valid_content_document_ids = None
    if content_document_link_query:
       content_document_link_response = sf.query_all(content_document_link_query)
       if(content_document_link_response):
          content_document_links = get_records_from_response(content_document_link_response)
          valid_content_document_ids = get_content_document_ids(content_document_links)
          
          with open(content_document_link_output_file, 'w') as output_file:
                  print_as_csv(content_document_links, output_file)

    logging.info("Found {0} total files".format(len(valid_content_document_ids)))

    # Begin Downloads
    fetch_content_versions(sf=sf, query_string=content_version_query, valid_content_document_ids=valid_content_document_ids, output_file_name=content_version_output_file , output_directory=os.path.join(args.output_folder, content_version_output), batch_size=batch_size)
   
if __name__ == "__main__":
    main()
