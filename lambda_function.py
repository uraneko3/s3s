import re
import subprocess
import boto3

## User info
S3_BUCKET = "<input your S3 bucket name>"
S3_DIR = "<input your S3 directory name>"


## boto3
s3 = boto3.resource('s3')
bucket = s3.Bucket(S3_BUCKET)

##
CONFIG_PATH = "/tmp/config.txt"
S3_PATH = S3_DIR + "/config.txt"


## Upload config.txt to S3
def upload_config_2s3():
    bucket.upload_file(CONFIG_PATH,S3_PATH)
    print(CONFIG_PATH + " is uploaded to S3 bucket...")

## Download config.txt from S3
def download_config_froms3():
    bucket.download_file(S3_PATH,CONFIG_PATH)
    print(CONFIG_PATH + " is downbloaded from S3 bucket...")

def main(event, context):
    download_config_froms3()

### executing s3s
    result = subprocess.run(["./s3s.py",  "-r"], encoding="utf-8", stdout=subprocess.PIPE)
    formatted_result = re.sub(r"^s3s .+\nChecking if there are previously-unuploaded battles/jobs...\n", "",
                              result.stdout).strip()
    print(formatted_result)


### Upload config.txt from /tmp/config.txt to s3
    upload_config_2s3()


if __name__ == "__main__":
    main("", "")
