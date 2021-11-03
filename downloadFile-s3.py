import boto3
import botocore.exceptions
from botocore import UNSIGNED
from botocore.client import Config
from urllib.parse import urlparse
import argparse
import logging

"""
    Param:
        bucket => name of bucket
        file_name => path of file in bucket
        local_path => directory to save the file
"""
def downloadFile_s3(bucket, file_name, local_path, access_key=None, secret_key=None):
    if access_key == None and secret_key == None:
        s3 = boto3.client('s3', config=Config(signature_version=UNSIGNED))
        s3.download_file(bucket, file_name, local_path)
    else:
        s3 = boto3.client('s3', access_key, secret_key)
        s3.download_file(bucket, file_name, local_path)

logger = logging.getLogger('downloadFile-s3')

parser = argparse.ArgumentParser(description='This is the function to download file from aws s3')
parser.add_argument('-u','--ur',action='store',dest='url',default=None,help='<Required> URL link',required=True)
parser.add_argument('-l',action='store',dest='local_path',default=None,help='<Required> Local directory for save file',required=True)
parser.add_argument('-a','--ak',action='store',dest='access_key',default=None,help='Credential for s3 bucket (access key)')
parser.add_argument('-s','--sk',action='store',dest='secret_key',default=None,help='Credential for s3 bucket (secret key)')
results = parser.parse_args()
url = results.url
local_path = results.local_path
access_key = results.access_key
secret_key = results.secret_key
    
try:
    url = urlparse(url)
    bucket = url.netloc
    file_bucket = url.path
    file_bucket = file_bucket[1:]
    file_name = url.path.split('/')
    file_name = file_name[len(file_name) - 1]

    if(local_path[:1] == '/'):
        local_path = local_path + file_name
    elif(local_path == './'):
        local_path = local_path + file_name
    elif(local_path[:1] != '/'):
        local_path = local_path + '/' + file_name
    
    downloadFile_s3(bucket, file_bucket, local_path, access_key, secret_key)
except botocore.exceptions.ParamValidationError as error:
    logger.error("Error downloading file" + error)
