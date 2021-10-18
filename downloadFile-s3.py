import requests


# url = '/giab/data/NA12878/NIST_NA12878_HG001_HiSeq_300x/140407_D00360_0017_BH947YADXX/Project_RM8398/Sample_U5c/U5c_CCGTCC_L001_R2_001.fastq.gz'
url = 's3://giab/data/NA12878/NIST_NA12878_HG001_HiSeq_300x/140407_D00360_0017_BH947YADXX/Project_RM8398/Sample_U5c/U5c_CCGTCC_L001_R2_001.fastq.gz'

def downloadFile_s3(url, local_dir):

    aws = 'https://s3.amazonaws.com/'
    url = url.split('s3://')

    url = aws + url[1]

    myFile = requests.get(url)
    open(local_dir,'wb').write(myFile.content)


downloadFile_s3(url, "/home/adrian/Desktop/pruebas")