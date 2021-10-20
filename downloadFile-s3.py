import boto3
import botocore
from botocore import UNSIGNED
from botocore.client import Config
from urllib.parse import urlparse
import argparse
import logging

"""
    Param:
        bucket => name of bucket
        file_name => path of file in bucket
        local_path => directory in which to save the file
"""
def downloadFile_s3(bucket, file_name, local_path):
    s3.download_file(bucket, file_name, local_path)

logger = logging.getLogger('downloadFile-s3')

parser = argparse.ArgumentParser(description='This is the function to download file from aws s3')
parser.add_argument('-u','--ur',action='store',dest='url',default=None,help='<Required> URL link',required=True)
parser.add_argument('-l',action='store',dest='local_path',default=None,help='<Required> Local directory for save file',required=True)
results = parser.parse_args()
url = results.url
local_path = results.local_path

try:
    s3 = boto3.client('s3', config=Config(signature_version=UNSIGNED))
except botocore.exceptions.ClientError as error:
    logger.error("Anon conection failed" + error)
    
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
    
    downloadFile_s3(bucket, file_bucket, local_path)
except botocore.exceptions.ParamValidationError as error:
    logger.error("Error downloading file" + error)