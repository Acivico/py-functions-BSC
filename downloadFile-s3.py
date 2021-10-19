import requests
from urllib.parse import urlparse
import argparse

def downloadFile_s3(url, local_path):

    aws = 'https://s3.amazonaws.com/'
    
    url = urlparse(url)
    
    url = aws + url.netloc + url.path

    myFile = requests.get(url)
    
    with open(local_path,'w') as fp:
        pass
    
    open(local_path,'wb').write(myFile.content)

parser = argparse.ArgumentParser(description='This is the function to download file from aws s3')
parser.add_argument('-u','--ur',action='store',dest='url',default=None,help='<Required> URL link',required=True)
parser.add_argument('-l',action='store',dest='local_path',default=None,help='<Required> Local directory for save file',required=True)
results = parser.parse_args()
url = results.url
local_path = results.local_path

downloadFile_s3(url, local_path)