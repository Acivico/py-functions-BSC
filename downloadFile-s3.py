import boto3
from botocore import UNSIGNED
from botocore.client import Config
from urllib.parse import urlparse

def downloadFile_s3(url):
    url = urlparse(url)

    bucket = url.netloc.split(".s3")
    bucket = bucket[0]

    file_name = url.path
    file_name = file_name[1:]

    s3.download_file(bucket,file_name, file_name)  

def downloadFolder_s3(url):
    url = urlparse(url)

    bucket = url.netloc.split(".s3")
    bucket = bucket[0]


s3 = boto3.client('s3', config=Config(signature_version=UNSIGNED))

url_file = 'https://xavitristancho.s3-eu-west-1.amazonaws.com/IMG_2619.JPG'
url_folder = ''

downloadFile_s3(url_file)
# downloadFolder_s3(url_folder)