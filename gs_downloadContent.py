from google.cloud import storage
from urllib.parse import urlparse
import argparse
import logging
import os

def downloadContent(url, local_path, credentials=None):
        total_bobs = 0

        url = urlparse(url)
        bucket = url.netloc
        prefix = url.path[1:]
        
        try:
            if credentials == None:
                gs = storage.Client.create_anonymous_client()
            else:
                path_service_account_json = credentials            
                gs = storage.Client.from_service_account_json(path_service_account_json)         
        except Exception as e:
            logging.warn("Autentication error: " + e)

        bucket = gs.bucket(bucket)
        blob = bucket.blob(prefix)
        blobs = bucket.list_blobs(prefix=prefix)
        listBlobs = bucket.list_blobs(prefix=prefix)

        for blob in blobs:
            total_bobs+=1

        if total_bobs == 1:
            if(local_path[-1] == '/'): 
                path = local_path + os.path.basename(prefix)
            elif(local_path == './'):
                path = local_path + os.path.basename(prefix)
            elif(local_path[-1] != '/'):
                path = local_path + '/' + os.path.basename(prefix)

            try:
                blob.download_to_filename(path)
            except Exception as e:
                logging.warn("Error downloading file " + e)

        elif total_bobs > 1:
            try:
                for blob in listBlobs:
                    if blob.name.endswith("/"):
                        continue
                    file = blob.name.split("/")            
                    file = os.path.join("/".join(file[1:-1]),' '.join(map(str, file[2:])))

                    if(local_path[-1] == '/'):
                        path = local_path + file
                    elif(local_path == './'):
                        path = local_path + file
                    elif(local_path[-1] != '/'):
                        path = local_path + '/' + file

                    if not os.path.exists(os.path.dirname(path)):
                        os.makedirs(os.path.dirname(path))
                    blob.download_to_filename(path)
            except Exception as e:
                logging.warn("Error downloading files " + e)


logger = logging.getLogger(__name__)

parser = argparse.ArgumentParser(description="This is to download content from gs")
parser.add_argument('-u', action='store', dest="url", help="<Required> URL link", required=True)
parser.add_argument('-l', action='store', dest="local_path", help="<Required> Local path to save the content", required=True)
parser.add_argument('-c', action='store', dest="credentials", help="Credentials to download content from private project")
results = parser.parse_args()

url = results.url
local_path = results.local_path
credentials = results.credentials

if not credentials:
    downloadContent(url,local_path)
else:
    downloadContent(url,local_path, credentials)