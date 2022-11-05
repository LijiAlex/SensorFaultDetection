from sensor.pipeline.training_pipeline import TrainPipeline
from sensor.logger import logging


if __name__ == '__main__':
    logging.info(f"{'#'*10} Training Pipeline Started{'#'*10}\n")
    training_pipeline = TrainPipeline()
    training_pipeline.run_pipeline()
    logging.info(f"{'#'*10} Training Pipeline Ended{'#'*10}\n")