from fastapi import FastAPI
from uvicorn import run as app_run
from fastapi.responses import Response
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import RedirectResponse

from sensor.pipeline.training_pipeline import TrainPipeline
from sensor.pipeline.prediction_pipeline import PredictionPipeline
from sensor.logger import logging
from sensor.constant.application import *


app = FastAPI()
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/", tags=["authentication"])
async def index():
    return RedirectResponse(url="/docs")

@app.get("/train")
async def train_route():
    try:

        train_pipeline = TrainPipeline()
        if train_pipeline.is_pipeline_running:
            return Response("Training pipeline is already running.")
        train_pipeline.run_pipeline()
        return Response("Training successful !!")
    except Exception as e:
        return Response(f"Error Occurred! {e}")

@app.get("/predict/{path:path}")
async def predict_route(path):
    try:
        prediction_pipeline = PredictionPipeline(path)
        msg = prediction_pipeline.run_pipeline()
        return Response(msg)
    except Exception as e:
        return Response(f"Error Occurred! {e}")

def main():
    try:
        path:str = r"https://raw.githubusercontent.com/LijiAlex/Datasets/main/sensor5898273.csv"
        prediction_pipeline = PredictionPipeline(path)
        msg = prediction_pipeline.run_pipeline()
        print(msg)
    except Exception as e:
        print(e)


if __name__=="__main__":
    main()
    # set_env_variable(env_file_path)
    # app_run(app, host=APP_HOST, port=APP_PORT)
