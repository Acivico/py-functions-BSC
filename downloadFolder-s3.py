import boto3
from botocore.handlers import disable_signing
import os

def downloadDirectoryFroms3(bucketName, remoteDirectoryName):
    s3_resource = boto3.resource('s3')
    s3_resource.meta.client.meta.events.register('choose-signer.s3.*', disable_signing)
    bucket = s3_resource.Bucket(bucketName) 
    for obj in bucket.objects.filter(Prefix = remoteDirectoryName):
        if not os.path.exists(os.path.dirname(obj.key)):
            os.makedirs(os.path.dirname(obj.key))
        bucket.download_file(obj.key, obj.key) # save to same path


url = "s3://giab/changelog_details/"

url = url.split('s3://')
url = url[1]

bucket = url[:url.index("/")]
directory = url[url.index("/"):]
directory = directory[1:]

downloadDirectoryFroms3(bucket,directory)