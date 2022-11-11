import pandas as pd
import os, sys
from six.moves import urllib
import numpy as np

from sensor.entity.config_entity import PredictionPipelineConfig
from sensor.component.prediction_data_validation import PredictionDataValidation
from sensor.ml.model.estimator import SensorModel, ModelResolver, TargetValueMapping
from sensor.exception import SensorException
from sensor.logger import logging
from sensor.constant import prediction_pipeline
from sensor.utils.s3_utils import sync_saved_model_dir_from_s3, sync_prediction_artifact_dir_to_s3, get_predicted_s3_filepath
from sensor.utils.main_utils import load_object
from sensor.utils.main_utils import read_yaml_file

class PredictionPipeline:
    def __init__(self, remote_input_file_path):
        self.prediction_pipeline_config = PredictionPipelineConfig()
        self.download_url = remote_input_file_path
        self._schema_config = read_yaml_file(prediction_pipeline.SCHEMA_FILE_PATH)

    def load_input_data(self)->pd.DataFrame:
        """
        Read data from the specified file path
        """
        try:
            # folder location to download file
            input_dir = self.prediction_pipeline_config.input_dir
            # create folder
            os.makedirs(input_dir, exist_ok=True)
            # get the file name
            self.data_file_name = os.path.basename(self.download_url)
            # complete path to download
            self.input_file_path = os.path.join(input_dir, self.data_file_name)            
            logging.info(f"Downloading file [{self.download_url}]")
            # get file from url
            urllib.request.urlretrieve(self.download_url, self.input_file_path)
            logging.info(f"Download completed. Input file at [{self.input_file_path}]") 
            dataframe = pd.read_csv(self.input_file_path, index_col=False, na_values = "na", keep_default_na=True)
            logging.info(f"Drop unnecessary columns") 
            dataframe = dataframe.drop(self._schema_config["drop_columns"],axis=1) 
            dataframe = dataframe
          
            return dataframe
        except Exception as e:
            raise SensorException(e,sys)

    def load_model(self)->SensorModel:
        try:
            logging.info("Syncing saved model from S3 bucket")
            sync_saved_model_dir_from_s3()
            model_resolver = ModelResolver(model_dir=prediction_pipeline.SAVED_MODEL_DIR)
            if not model_resolver.is_model_exists():
                logging.info("Model not available")
                raise Exception("Model not available")       
            best_model_path = model_resolver.get_latest_model_path()
            model:SensorModel = load_object(file_path=best_model_path)
            logging.info("Best model loaded")
            return model
        except Exception as e:
            raise SensorException(e,sys)

    def predict_the_output(self, input_dataframe, bestmodel):
        try:
            y_pred = bestmodel.predict(input_dataframe)
            logging.info("Prediction Complete")
            input_dataframe['predicted_column'] = y_pred
            input_dataframe['predicted_column'].replace(TargetValueMapping().reverse_mapping(),inplace=True)
            logging.info("Output dataframe prepared")
            return input_dataframe
        except Exception as e:
            raise SensorException(e,sys)

    def save_result(self, output_df:pd.DataFrame):
        try:
            # folder location to download file
            output_dir = self.prediction_pipeline_config.output_dir
            # create folder
            os.makedirs(output_dir, exist_ok=True)
            # complete path to download
            self.output_file_path = os.path.join(output_dir, self.data_file_name)   
            output_df.to_csv(self.output_file_path, index=False)  
            logging.info(f"Output written to {self.output_file_path}")                      
        except Exception as e:
            raise SensorException(e,sys)

    def run_pipeline(self):
        try:
            logging.info(f"Prediction pipeline started with config {self.prediction_pipeline_config.__dict__}")
            input_df:pd.DataFrame = self.load_input_data()
            status = PredictionDataValidation(input_df,self.prediction_pipeline_config).initiate_data_validation()
            model:SensorModel = self.load_model()
            output_df:pd.DataFrame = self.predict_the_output(input_df, model)
            self.save_result(output_df)
            sync_prediction_artifact_dir_to_s3(prediction_artifact_dir = self.prediction_pipeline_config.prediction_artifact_dir, 
            time_stamp = self.prediction_pipeline_config.timestamp)
            s3_output_file = get_predicted_s3_filepath(time_stamp = self.prediction_pipeline_config.timestamp, 
            file_name = self.data_file_name)
            if not status:
                return f"Prediction successful. Output at {s3_output_file}. Datadrift detected. Retrain model for better results"
            else:
                return f"Prediction successful. Output at {s3_output_file}"
        except Exception as e:
            raise SensorException(e,sys)


