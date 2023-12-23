from Pipeline.pipeline_module import Pipeline
from Variable_artifects.artifact import CSV_FILE
from Variable_artifects.artifact import CSV_DIR
import logging
import os


def final_function():
    try:
        CSV_PATH = os.path.join(CSV_DIR, CSV_FILE)
        ingest_data, prediction = Pipeline().pipline_seq(CSV_PATH)
        # Writing the new data to the CSV file, overwriting its contents
        ingest_data.to_csv(CSV_PATH)

    except Exception as e:
        logging.info(f"Main module : final function An error occurred: {e}")


final_function()
