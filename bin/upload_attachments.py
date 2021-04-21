#!/usr/bin/env python
import base64, os, csv, argparse, sys, datetime, configparser
from simple_salesforce import Salesforce
import logging as log
from simple_salesforce.exceptions import SalesforceMalformedRequest

def create_attachment_request_body(attachment, base64_body, user_mapping, parent_mapping):
   attachment_request_body={'Body': base64_body, 'ContentType': attachment['ContentType'], 'Description': attachment['Description'], 'CreatedDate': attachment['CreatedDate'], 'IsPrivate': attachment['IsPrivate'].replace('False', 'false').replace('True', 'true'), 'LastModifiedDate': attachment['LastModifiedDate'], 'Name': attachment['Name']}

   if attachment['ParentId'] not in parent_mapping:
      log.info('Skipping upload of attachment with Id: ' + attachment['Id'] + ' due to missing parent (' + attachment['ParentId']  +')')
      return None

   attachment_request_body['ParentId'] = parent_mapping[attachment['ParentId']]
   if attachment['OwnerId'] in user_mapping:
       attachment_request_body['OwnerId'] = user_mapping[attachment['OwnerId']]
   if attachment['CreatedById'] in user_mapping:
       attachment_request_body['OwnerId'] = user_mapping[attachment['CreatedById']]
   if attachment['LastModifiedById'] in user_mapping:
       attachment_request_body['LastModifiedById'] = user_mapping[attachment['LastModifiedById']]
 
   return attachment_request_body

def load_mapping(mapping_file, key_field_name, value_field_name):
   mapping = {}
   for row in csv.DictReader(mapping_file):
      mapping[row[key_field_name]] = row[value_field_name]
   return mapping

def print_row_as_csv(row, csv_file = sys.stdout, write_header = True):
    writer = csv.DictWriter(csv_file, row.keys(), quoting=csv.QUOTE_ALL)
    if write_header == True:
       writer.writeheader()
    writer.writerow(row)

def main():
   parser = argparse.ArgumentParser(description='Script which loads attachments to Salesforce:\n' +
                                                'Example:\n' +
                                                '\t' + os.path.basename(__file__),
						formatter_class=argparse.RawTextHelpFormatter)

   parser.add_argument(
        "-i", "--input-file", dest="input_file",
        help="Input CSV file with Attachment info", required=True)

   parser.add_argument(
        "-s", "--salesforce-config-file", dest="salesforce_config_file",
        help="Salesforce config file with login info", required=True)

   parser.add_argument(
        "-f", "--input-folder", dest="input_folder",
        help="Input folder with binary data - file referenced by original attachment ID", required=True)

   parser.add_argument(
        "-u", "--user-mapping", dest="user_mapping",
        help="User ID mapping in CSV format", required=True)

   parser.add_argument(
        "-p", "--parent-mapping", dest="parent_mapping",
        help="Parent ID mapping in CSV format", required=True)

   parser.add_argument(
        "-v", "--verbose", dest="verbose", action='store_true',
        help="Verbose")

   args = parser.parse_args()

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

   # Output
   log.info('Upload Attachments (Files) from Salesforce')
   log.info('Username: ' + username)
   log.info('Signing in at: https://'+ domain + '.salesforce.com')

   if args.verbose:
      log.basicConfig(format="%(levelname)s: %(message)s", level=log.DEBUG)
   else:
      log.basicConfig(format="%(levelname)s: %(message)s", level=log.INFO)

   if(args.input_file is not None and args.input_folder is not None):
      sf = Salesforce(username = username,  password = password, security_token = token, domain = domain)

      user_mappping = {}
      parent_mapping = {}
      with open(args.parent_mapping, mode='r') as parent_mapping_csv_file:
         parent_mapping = load_mapping(parent_mapping_csv_file, 'OriginalId', 'NewId')
      with open(args.user_mapping, mode='r') as user_mapping_csv_file:
         user_mapping = load_mapping(user_mapping_csv_file, 'OriginalId', 'NewId')

      with open(args.input_file, mode='r') as input_csv_file:
          for attachment in csv.DictReader(input_csv_file):
            error = ''
            result = ''
            attachment_id = attachment['Id']
            log.info('Uploading file {body} with Id = \'{id}\''.format(body = attachment['Body'], id = attachment_id))
            
            body = os.path.join(args.input_folder, attachment_id)
            with open(body, 'rb') as attachment_binary_file:
               binary_file_body = attachment_binary_file.read()
               base64_encoded_body = base64.b64encode(binary_file_body)
               base64_body = base64_encoded_body.decode('utf-8')
               attachment_request_body = create_attachment_request_body(attachment, base64_body, user_mapping, parent_mapping)
               if attachment_request_body:
                  try:
                     result = sf.Attachment.create(attachment_request_body)
                  except Exception as ex:
                     error = ex
                  # add error key-value pair
                  if error is not None and hasattr(error, 'content'):
                     attachment_request_body['error'] = error.content[0]['message']
                  elif error is not None:
                     attachment_request_body['error'] = error
                  else:
                     attachment_request_body['error'] = ''

                  # replace base64 string by file path
                  attachment_request_body['Body'] = body
                  result_row = ', '.join("{!s}={!r}".format(key, val) for (key, val) in attachment_request_body.items())

                  #print_row_as_csv(attachment_request_body, write_header = False)
                  print(result_row)

if __name__ == "__main__":
   main()
