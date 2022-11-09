
import os, sys

from sensor.exception import SensorException


class S3Sync:

    # sync the contents of folder to s3
    def sync_folder_to_s3(self,folder,aws_bucket_url):
        try:
            command = f"aws s3 sync {folder} {aws_bucket_url}"
            os.system(command)
        except Exception as e:
            raise SensorException(e,sys)

    def sync_folder_from_s3(self,folder,aws_bucket_url):
        try:
            command = f"aws s3 sync {aws_bucket_url} {folder}"
            os.system(command)
        except Exception as e:
            raise SensorException(e,sys)



