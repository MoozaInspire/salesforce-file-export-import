#!/usr/bin/env python
import base64, os, csv, argparse, sys, datetime, configparser
from simple_salesforce import Salesforce
import logging as log
from simple_salesforce.exceptions import SalesforceMalformedRequest

def create_content_version_request_body(content_version, base64_version_data):
   content_version_request_body={'Title':content_version['Title'], 'Description':content_version['Description'], 'PathOnClient':content_version['PathOnClient'], 'VersionData':base64_version_data, 'CreatedDate':content_version['CreatedDate'], 'LastModifiedDate':content_version['LastModifiedDate'], 'ContentUrl':content_version['ContentUrl'], 'ReasonForChange':content_version['ReasonForChange'], 'SharingOption':content_version['SharingOption'], 'SharingPrivacy':content_version['SharingPrivacy'], 'Origin':content_version['Origin'], 'ContentLocation':content_version['ContentLocation'], 'ExternalDocumentInfo1':content_version['ExternalDocumentInfo1'], 'ExternalDocumentInfo2':content_version['ExternalDocumentInfo2'], 'IsMajorVersion':content_version['IsMajorVersion'].replace('1', 'true').replace('0', 'false').replace('False', 'false').replace('True', 'true')}
   return content_version_request_body

def main():
   parser = argparse.ArgumentParser(description='Script which loads content versions to Salesforce:\n' +
                                                'Example:\n' +
                                                '\t' + os.path.basename(__file__),
						formatter_class=argparse.RawTextHelpFormatter)

   parser.add_argument(
        "-i", "--input-file", dest="input_file",
        help="Input CSV file with ContentVersion info", required=True)

   parser.add_argument(
        "-f", "--input-folder", dest="input_folder",
        help="Input folder with binary data - file referenced by original content version ID", required=True)

   parser.add_argument(
        "-r", "--result-file", dest="result_file",
        help="Result CSV file with ContentVersion info", required=False)

   parser.add_argument(
        "-v", "--verbose", dest="verbose", action='store_true',
        help="Verbose")

   parser.add_argument(
        "-s", "--salesforce-config-file", dest="salesforce_config_file",
        help="Salesforce config file with login info", required=True)

   parser.add_argument(
        "-u", "--upsert-key", dest="upsert_key",
        help="Upsert key", required=True)

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

   if args.verbose:
      log.basicConfig(format="%(levelname)s: %(message)s", level=log.DEBUG)
   else:
      log.basicConfig(format="%(levelname)s: %(message)s")

   if(args.input_file is not None and args.input_folder is not None):
      sf = Salesforce(username = username,  password = password, security_token = token, domain = domain)
      # contact = sf.Contact.get('0037R00002TNL6eQAH')
      with open(args.input_file, mode='r') as input_csv_file:
          for content_version in csv.DictReader(input_csv_file):
            error = ''
            result = ''
            content_version_id=content_version['Id']
            print('Uploading file {path_on_client} with Id = \'{id}\''.format(path_on_client=content_version['PathOnClient'],id=content_version_id))
            #if int(content_version['ContentSize']) > 0:
            if True:
               version_data = os.path.join(args.input_folder, content_version_id)
               with open(version_data, 'rb') as content_version_binary_file:
                  binary_file_version_data = content_version_binary_file.read()
                  base64_encoded_version_data = base64.b64encode(binary_file_version_data)
                  base64_version_data = base64_encoded_version_data.decode('utf-8')
                  content_version_request_body = create_content_version_request_body(content_version, base64_version_data)
                  # set the Content-Disposition header otherwise the limit for the file upload will be 37,5 MB
                  sf.headers['Content-Type'] = 'multipart/form-data; boundary="boundary_string"'
                  try:
                     result=sf.ContentVersion.upsert(args.upsert_key + '/' + content_version_id, content_version_request_body)
                  except Exception as ex:
                     error=ex

                  if error is not None and hasattr(error, 'content'):
                     content_version_request_body['error'] = error.content[0]['message']
                  elif error is not None:
                     content_version_request_body['error'] = error
                  else:
                     content_version_request_body['error'] = ''
                  # replace base64 string by file path
                  content_version_request_body['VersionData'] = version_data
                  result_row = ', '.join("{!s}={!r}".format(key,val) for (key,val) in content_version_request_body.items())

                  print(result_row)
            else:
                print('No file for Id: ', content_version['Id'])
                print(result)

if __name__ == "__main__":
   main()
