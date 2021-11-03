import boto3
import botocore.exceptions
from botocore.handlers import disable_signing
from urllib.parse import urlparse
import os
import logging
import argparse

logger = logging.getLogger('downloadFolder-s3')

def downloadDirectoryFroms3(bucketName, remoteDirectoryName, local_dir, access_key=None, secret_key=None):
    if access_key == None and secret_key == None:
        s3_resource = boto3.resource('s3')
        s3_resource.meta.client.meta.events.register('choose-signer.s3.*', disable_signing)
        bucket = s3_resource.Bucket(bucketName) 
        for obj in bucket.objects.filter(Prefix = remoteDirectoryName):
            if not os.path.exists(os.path.dirname(obj.key)):
                os.makedirs(os.path.dirname(obj.key))
            bucket.download_file(obj.key, obj.key) # save to same path
    else:
        try:
            s3_resource = boto3.resource('s3', access_key, secret_key)
            bucket = s3_resource.Bucket(bucketName) 
            for obj in bucket.objects.filter(Prefix = remoteDirectoryName):
                if not os.path.exists(os.path.dirname(obj.key)):
                    os.makedirs(os.path.dirname(obj.key))
                bucket.download_file(obj.key, obj.key) # save to same path
        except Exception as e:
            logger.warn("ERROR when downloading the folder" + e)

try:
    parser = argparse.ArgumentParser(description='This is the function to download folder from aws s3')
    parser.add_argument('-u',action='store',dest='url',default=None,help='<Required> URL link',required=True)
    parser.add_argument('-l',action='store',dest='local_path',default=None,help='<Required> Local directory for save file',required=True)
    parser.add_argument('-a','--ak',action='store',dest='access_key',default=None,help='Credential for s3 bucket (access key)')
    parser.add_argument('-s','--sk',action='store',dest='secret_key',default=None,help='Credential for s3 bucket (secret key)')
    results = parser.parse_args()
    url = results.url
    local_dir = results.local_path
    access_key = results.access_key
    secret_key = results.secret_key

    url = urlparse(url)
    bucket = url.netloc
    directory = url.path
    directory = directory[1:]

    downloadDirectoryFroms3(bucket,directory, access_key, secret_key)
except botocore.exceptions.ParameterError as error:
    logger.error("Error downloading file" + error)

