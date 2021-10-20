import boto3
from botocore.handlers import disable_signing
from urllib.parse import urlparse
import os
import logging
import argparse

logger = logging.getLogger('downloadFolder-s3')

def downloadDirectoryFroms3(bucketName, remoteDirectoryName):
    s3_resource = boto3.resource('s3')
    s3_resource.meta.client.meta.events.register('choose-signer.s3.*', disable_signing)
    bucket = s3_resource.Bucket(bucketName) 
    for obj in bucket.objects.filter(Prefix = remoteDirectoryName):
        if not os.path.exists(os.path.dirname(obj.key)):
            os.makedirs(os.path.dirname(obj.key))
        bucket.download_file(obj.key, obj.key) # save to same path
try:
    parser = argparse.ArgumentParser(description='This is the function to download folder from aws s3')
    parser.add_argument('-u',action='store',dest='url',default=None,help='<Required> URL link',required=True)
    results = parser.parse_args()
    url = results.url

    url = urlparse(url)
    bucket = url.netloc
    directory = url.path
    directory = directory[1:]

    downloadDirectoryFroms3(bucket,directory)
except botocore.exceptions.ParameterError as error:
    logger.error("Error downloading file" + error)

