import boto3
from botocore import UNSIGNED
from botocore.client import Config
import botocore.exceptions
from urllib.parse import urlparse
import os
import logging
import argparse

"""
    Download files from s3
    :param bucket: the name of the bucket to download from
    :param prefix: the s3 directory to download
    :param local_path: the local directory to download the files to
"""
def downloadFile_s3(bucket, prefix, local_path):
    try:
        s3.download_file(bucket, prefix, local_path)
    
    except botocore.exceptions.ParamValidationError as error:
        logger.warn("Error downloading file" + error)

"""
    Download content from a s3 folder
    :param bucket: the name of the bucket to download from
    :param prefix: the s3 directory to download
    :param local_path: the local directory to download the files to
"""
def downloadFolder_s3(bucket, prefix, local_path):
    try:

        if not prefix.endswith('/'):
            prefix += '/'

        paginator = s3.get_paginator('list_objects_v2')
        for result in paginator.paginate(Bucket=bucket, Prefix=prefix):
            for key in result['Contents']:
                rel_path = key['Key'][len(prefix):]
                if not key['Key'].endswith('/'):
                    local_file_path = os.path.join(local_path, rel_path)
                    local_file_dir = os.path.dirname(local_file_path)
                    if not os.path.exists(local_file_dir):
                        os.makedirs(local_file_dir)
                    s3.download_file(bucket, key['Key'],local_file_path)

    except botocore.exceptions.ParamValidationError as error:
        logger.warn("Error downloading file " + error)


logger = logging.getLogger('s3')

parser = argparse.ArgumentParser(description="This is to download content from aws s3")
parser.add_argument('-u', action='store', dest="url", help="<Required> URL link", required=True)
parser.add_argument('-l', action='store', dest="local_path", help="<Required> Local path to save the content", required=True)
parser.add_argument('-a',action='store',dest='access_key',default=None,help='Credential for s3 bucket (access key)')
parser.add_argument('-s',action='store',dest='secret_key',default=None,help='Credential for s3 bucket (secret key)')
results = parser.parse_args()
url = results.url
local_path = results.local_path
access_key = results.access_key
secret_key = results.secret_key

urlParse = urlparse(url)
bucket = urlParse.netloc
prefix = urlParse.path
prefix = prefix[1:]

try:
    if access_key == None and secret_key == None:
            s3 = boto3.client('s3', config=Config(signature_version=UNSIGNED))
            response = s3.list_objects_v2(Bucket=bucket,Prefix=prefix)

    else:
            s3 = boto3.client('s3',access_key,secret_key)
            response = s3.list_objects_v2(Bucket=bucket, Prefix=prefix)
except botocore.exceptions.ClientError as error:
    logger.warn('Error in the connection with s3 ' + error)

if response["KeyCount"] == 1:
    file_name = urlParse.path.split('/')
    file_name = file_name[len(file_name) - 1]

    if(local_path[:1] == '/'):
        local_path = local_path + file_name
    elif(local_path == './'):
        local_path = local_path + file_name
    elif(local_path[:1] != '/'):
        local_path = local_path + '/' + file_name
    
    downloadFile_s3(bucket, prefix, local_path)

elif response["KeyCount"] > 1:
    downloadFolder_s3(bucket, prefix, local_path)