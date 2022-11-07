import sys

from sensor.entity.config_entity import *
from sensor.entity.artifact_entity import *
from sensor.component.data_validation import DataValidation
from sensor.component.data_ingestion import DataIngestion
from sensor.component.data_transformation import DataTransformation
from sensor.component.model_trainer import ModelTrainer
from sensor.component.model_evaluation import ModelEvaluation
from sensor.component.model_pusher import ModelPusher
from sensor.exception import SensorException
from sensor.logger import logging


class TrainPipeline:
    def __init__(self):
        self.training_pipeline_config = TrainingPipelineConfig()

    def start_data_ingestion(self)->DataIngestionArtifact:
        try:
            self.data_ingestion_config = DataIngestionConfig(training_pipeline_config=self.training_pipeline_config)
            logging.info(f"\nData ingestion started with config:{self.data_ingestion_config.__dict__}")
            data_ingestion = DataIngestion(data_ingestion_config=self.data_ingestion_config)
            data_ingestion_artifact = data_ingestion.initiate_data_ingestion()
            logging.info(f"Data ingestion completed and artifact: {data_ingestion_artifact}\n")
            return data_ingestion_artifact
        except  Exception as e:
            raise  SensorException(e,sys)

    def start_data_validaton(self,data_ingestion_artifact:DataIngestionArtifact)->DataValidationArtifact:
        try:
            data_validation_config = DataValidationConfig(training_pipeline_config=self.training_pipeline_config)
            logging.info(f"\nData validation started with config:{data_validation_config.__dict__}")
            data_validation = DataValidation(data_ingestion_artifact=data_ingestion_artifact,
            data_validation_config = data_validation_config)
            data_validation_artifact = data_validation.initiate_data_validation()
            logging.info(f"Data validation completed and artifact: {data_validation_artifact}\n")
            return data_validation_artifact
        except  Exception as e:
            raise  SensorException(e,sys)

    def start_data_transformation(self,data_validation_artifact:DataValidationArtifact)->DataTransformationArtifact:
        try:
            data_transformation_config = DataTransformationConfig(training_pipeline_config=self.training_pipeline_config)
            logging.info(f"\nData transformation started with config:{data_transformation_config.__dict__}")
            data_transformation = DataTransformation(data_validation_artifact=data_validation_artifact,
            data_transformation_config=data_transformation_config)
            data_transformation_artifact =  data_transformation.initiate_data_transformation()
            logging.info(f"Data transformation completed and artifact: {data_transformation_artifact}\n")
            return data_transformation_artifact
        except  Exception as e:
            raise  SensorException(e,sys)

    def start_model_trainer(self,data_transformation_artifact:DataTransformationArtifact)->ModelTrainerArtifact: 
        try:
            model_trainer_config = ModelTrainerConfig(training_pipeline_config=self.training_pipeline_config)
            logging.info(f"\nModel Training started with config:{model_trainer_config.__dict__}")
            model_trainer = ModelTrainer(model_trainer_config, data_transformation_artifact)
            model_trainer_artifact = model_trainer.initiate_model_trainer()
            logging.info(f"Model Training completed and artifact: {model_trainer_artifact}\n")
            return model_trainer_artifact
        except  Exception as e:
            raise  SensorException(e,sys)

    def start_model_evaluation(self,data_validation_artifact:DataValidationArtifact, model_trainer_artifact:ModelTrainerArtifact) -> ModelEvaluationArtifact:
        try:
            model_eval_config = ModelEvaluationConfig(self.training_pipeline_config)
            logging.info(f"\nModel evaluation started with config:{model_eval_config.__dict__}")
            model_eval = ModelEvaluation(model_eval_config, data_validation_artifact, model_trainer_artifact)
            model_eval_artifact = model_eval.initiate_model_evaluation()
            logging.info(f"Model evaluation completed and artifact: {model_eval_artifact}\n")
            return model_eval_artifact
        except  Exception as e:
            raise  SensorException(e,sys)

    def start_model_pusher(self,model_eval_artifact:ModelEvaluationArtifact):
        try:
            model_pusher_config = ModelPusherConfig(training_pipeline_config=self.training_pipeline_config)
            logging.info(f"\nModel pusher started with config:{model_pusher_config.__dict__}")
            model_pusher = ModelPusher(model_pusher_config, model_eval_artifact)
            model_pusher_artifact = model_pusher.initiate_model_pusher()
            logging.info(f"Model pusher completed and artifact: {model_pusher_artifact}\n")
            return model_pusher_artifact
        except  Exception as e:
            raise  SensorException(e,sys)

    def run_pipeline(self):
        try:
            data_ingestion_artifact:DataIngestionArtifact = self.start_data_ingestion()
            data_validation_artifact:DataValidationArtifact=self.start_data_validaton(data_ingestion_artifact=data_ingestion_artifact)
            data_transformation_artifact = self.start_data_transformation(data_validation_artifact=data_validation_artifact)
            model_trainer_artifact = self.start_model_trainer(data_transformation_artifact)
            model_eval_artifact = self.start_model_evaluation(data_validation_artifact, model_trainer_artifact)
            model_pusher_artifact = self.start_model_pusher(model_eval_artifact)
        except  Exception as e:
            raise  SensorException(e,sys)

