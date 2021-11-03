# py-functions-BSC
Functions to download content from aws s3

Installation:

    python3 -m venv .p
    source .p/bin/activate
    pip install --upgrade pip wheel
    pip install -r requirements.txt


Use downloadFile-s3.py

    python3 downloadFile-s3.py -u ["URL"] -l ["LOCAL_DIR"]
    Example:
        python downloadFile-s3.py -u "s3://giab/data/NA12878/NIST_NA12878_HG001_HiSeq_300x/140407_D00360_0017_BH947YADXX/Project_RM8398/Sample_U5c/U5c_CCGTCC_L001_R2_001.fastq.gz" -l .

Use downloadFolder-s3.py

    python3 downloadFolder-s3.py -u["URL"]
    Example:
        python downloadFolder-s3.py -u s3://giab/changelog_details/
