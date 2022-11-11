from sensor.constant.prediction_pipeline import SCHEMA_FILE_PATH
from sensor.constant.training_pipeline import ARTIFACT_DIR, DATA_INGESTION_DIR_NAME, DATA_INGESTION_INGESTED_DIR, TRAIN_FILE_NAME, TARGET_COLUMN
from sensor.exception import SensorException
from sensor.logger import logging
from sensor.utils.main_utils import read_yaml_file,write_yaml_file
from sensor.utils.s3_utils import sync_artifact_dir_from_s3
from sensor.entity.config_entity import PredictionPipelineConfig

from scipy.stats import ks_2samp
from distutils import dir_util
import pandas as pd
import os,sys

class PredictionDataValidation:

    def __init__(self, input_df, prediction_pipeline_config: PredictionPipelineConfig):
        try:
            self.prediction_pipeline_config = prediction_pipeline_config
            self._schema_config = read_yaml_file(SCHEMA_FILE_PATH)
            self.input_df = input_df
        except Exception as e:
            raise  SensorException(e,sys)
    
    def validate_number_of_columns(self,dataframe:pd.DataFrame)->bool:
        try:
            number_of_columns = len(self._schema_config["columns"]) - 1 # subtract target feature column in prediction pipeline
            logging.info(f"Required number of columns: {number_of_columns}")
            logging.info(f"Data frame has columns: {len(dataframe.columns)}")
            if len(dataframe.columns)==number_of_columns:
                return True
            return False
        except Exception as e:
            raise SensorException(e,sys)

    def is_numerical_column_exist(self,dataframe:pd.DataFrame)->bool:
        try:
            numerical_columns = self._schema_config["numerical_columns"]
            dataframe_columns = dataframe.columns

            numerical_column_present = True
            missing_numerical_columns = []
            for num_column in numerical_columns:
                if num_column not in dataframe_columns:
                    numerical_column_present=False
                    missing_numerical_columns.append(num_column)
            
            logging.info(f"Missing numerical columns: [{missing_numerical_columns}]")
            return numerical_column_present
        except Exception as e:
            raise SensorException(e,sys)      

    def detect_dataset_drift(self,base_df,current_df,threshold=0.05)->bool:
        logging.info("Checking for data drift")
        try:
            status=False
            report = {}
            data_drift_columns = []
            base_data_columns = list(base_df.columns)
            base_data_columns.remove(TARGET_COLUMN)
            for column in base_data_columns:
                d1 = base_df[column]
                d2  = current_df[column]
                is_same_dist = ks_2samp(d1,d2)
                if threshold<=is_same_dist.pvalue:
                    is_found=False
                else:
                    is_found = True 
                    data_drift_columns.append(column)
                    status=True
                report.update({column:{
                    "p_value":float(is_same_dist.pvalue),
                    "drift_status":is_found                    
                    }})
            
            drift_report_file_path = self.prediction_pipeline_config.drift_report_file_path
            
            #Create directory
            dir_path = os.path.dirname(drift_report_file_path)
            os.makedirs(dir_path,exist_ok=True)
            write_yaml_file(file_path=drift_report_file_path,content=report,)

            logging.info(f"Data drift: {status}, Data drift columns: {data_drift_columns}. Report generated at {drift_report_file_path}")
            return status
        except Exception as e:
            raise SensorException(e,sys)

    def get_base_dataframe(self):
        artifact_list = os.listdir(rf"{ARTIFACT_DIR}/")
        artifact_list.sort(reverse=True)
        latest_artifact_dir = artifact_list[0]
        latest_artifact_dir_path = os.path.join(ARTIFACT_DIR, latest_artifact_dir)
        train_file = os.path.join(latest_artifact_dir_path, DATA_INGESTION_DIR_NAME, DATA_INGESTION_INGESTED_DIR, TRAIN_FILE_NAME)
        return pd.read_csv(train_file)

   

    def initiate_data_validation(self):
        try:
            error_message = ""
            
            # Validate number of columns
            logging.info("Validate no. of columns for input dataframe")
            status = self.validate_number_of_columns(dataframe=self.input_df)
            if not status:
                error_message=f"{error_message}Input dataframe does not contain all columns.\n"
            
            # Validate numerical columns
            logging.info("Validate if numerical columns are missing for input dataframe")
            status = self.is_numerical_column_exist(dataframe=self.input_df)
            if not status:
                error_message=f"{error_message}Input dataframe does not contain all numerical columns.\n"
            
            if len(error_message)>0:
                raise SensorException(error_message)
            # Check data drift
            status = self.detect_dataset_drift(base_df=self.get_base_dataframe(),current_df=self.input_df)                       
            return status
        except Exception as e:
            raise SensorException(e,sys)