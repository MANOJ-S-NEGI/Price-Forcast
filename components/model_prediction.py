from Support_module_dir.support_function_predict import predict_function
from Variable_artifects.artifact import CSV_FILE
from Variable_artifects.artifact import CSV_DIR
from datetime import datetime
import pandas as pd
import logging
import joblib
import os


class Prediction:
    def __init__(self, saved_model_path):
        self.saved_model_path = saved_model_path

    @staticmethod
    def convert_timestamp(timestamp):
        """
        Function return timestamps

        during prediction date column print into datestamps into millisecond started from 1970 till date.
        to convert that back to today's time function is required
        """
        try:
            if isinstance(timestamp, pd.Timestamp):
                timestamp = timestamp.value // 10 ** 6  # Convert nanoseconds to milliseconds
            return datetime.utcfromtimestamp(timestamp / 1000).strftime('%Y-%m-%d')

        except Exception as e:
            raise e

    def model_prediction(self):
        """
        Function created for Data Ingestion

        Returns: Pandas processed Dataframe and predicted values
        """
        try:
            CSV_PATH = os.path.join(CSV_DIR, CSV_FILE)  # called from artifact module
            logging.info(f"Model Prediction Module : Initiating module prediction")
            dataset_frame = pd.read_csv(CSV_PATH)
            dataset_frame.set_index('Date', inplace=True)  # setting date columns as index
            logging.info(f"Model Prediction Module : Loading model")
            model = joblib.load(self.saved_model_path)  # Load the trained model

            # prediction function called from support_function material
            logging.info(f"Model Prediction Module : prediction function called")
            predictions, execution_time = predict_function(trained_model=model,
                                                           dataset=dataset_frame.Price)

            # Convert timestamps to a more readable date format
            predictions['Date'] = predictions['Date'].apply(Prediction.convert_timestamp)
            logging.info(f"Model Prediction Module : Exiting module  STATUS OK")
            return predictions, dataset_frame

        except Exception as e:
            logging.info(f"Model Prediction module: model prediction failed {e}")
