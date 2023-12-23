from Database.Database_connection import ConnectionDatabase
from components.ingestion import Ingestion
from components.training_model import Training
import logging


class Pipeline:
    def __init__(self):
        self.cassandra_connection = ConnectionDatabase()  # calling database module
        self.training = Training()  # calling training module

    def pipline_seq(self, data_file):
        try:
            """
            Function created for connecting simple module 

            Parameters
            ---------
            data_file : dataset - pandas DataFrame
                    A DataFrame containing the previous Price movement data.

            Returns: ingest_data from ingestion module and prediction values 
            """
            self.cassandra_connection.fetch_database()
            ingest_data = Ingestion(file_path=data_file).data_ingestion()  # calling Ingestion module
            prediction = self.training.training_data(dataset=ingest_data)
            return ingest_data, prediction

        except Exception as e:
            logging.info(f"pipeline Module: data pipeline failed: {e}")
