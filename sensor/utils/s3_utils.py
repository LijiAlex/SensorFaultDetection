import sys

from sensor.exception import SensorException
from sensor.logger import logging
from sensor.constant.training_pipeline import SAVED_MODEL_DIR, ARTIFACT_DIR
from sensor.constant.s3_bucket import TRAINING_BUCKET_NAME, PREDICTION_BUCKET_NAME
from sensor.constant.prediction_pipeline import PREDICTION_OUTPUT_FOLDER
from sensor.cloud_storage.s3_syncer import *

# Training Pipeline
def sync_artifact_dir_to_s3(artifact_dir, time_stamp):
        try:
            aws_bucket_url = f"s3://{TRAINING_BUCKET_NAME}/{ARTIFACT_DIR}/{time_stamp}"
            sync_folder_to_s3(folder = artifact_dir,aws_bucket_url=aws_bucket_url)
        except Exception as e:
            raise SensorException(e,sys)
            
def sync_saved_model_dir_to_s3():
    try:
        aws_bucket_url = f"s3://{TRAINING_BUCKET_NAME}/{SAVED_MODEL_DIR}"
        sync_folder_to_s3(folder = SAVED_MODEL_DIR,aws_bucket_url=aws_bucket_url)
    except Exception as e:
        raise SensorException(e,sys)

# Prediction Pipeline
def sync_saved_model_dir_from_s3():
        try:
            aws_bucket_url = f"s3://{TRAINING_BUCKET_NAME}/{SAVED_MODEL_DIR}"
            sync_folder_from_s3(folder = SAVED_MODEL_DIR,aws_bucket_url=aws_bucket_url)
        except Exception as e:
            raise SensorException(e,sys)

def sync_artifact_dir_from_s3():
        try:
            aws_bucket_url = f"s3://{TRAINING_BUCKET_NAME}/{ARTIFACT_DIR}"
            sync_folder_from_s3(folder = SAVED_MODEL_DIR,aws_bucket_url=aws_bucket_url)
        except Exception as e:
            raise SensorException(e,sys)

def sync_prediction_artifact_dir_to_s3(prediction_artifact_dir, time_stamp):
        try:
            aws_bucket_url = f"s3://{PREDICTION_BUCKET_NAME}/{ARTIFACT_DIR}/{time_stamp}"
            sync_folder_to_s3(folder = prediction_artifact_dir, aws_bucket_url=aws_bucket_url)
        except Exception as e:
            raise SensorException(e,sys)

def get_predicted_s3_filepath(time_stamp, file_name):
    try:
            aws_bucket_url = f"s3://{PREDICTION_BUCKET_NAME}/{ARTIFACT_DIR}/{time_stamp}/{PREDICTION_OUTPUT_FOLDER}/{file_name}"
            return aws_bucket_url
    except Exception as e:
        raise SensorException(e,sys)
