# calling libraries
import pandas as pd
import logging
from datetime import datetime


class Ingestion:
    def __init__(self, file_path):
        self.path = file_path
        self.data = pd.read_csv(self.path)

    def data_ingestion(self):
        """
        Function created for Data Ingestion
            Returns : Transformed Pandas Dataframe

        """
        try:
            counter = 0
            logging.info(f"Initializing the Ingestion Module")
            logging.info(f"Ingestion Module : iterating over data price column")
            for index, row in self.data.iterrows():  # iterating over data via rows sequence
                if pd.notnull(row["Price"]):  # Check if 'Date' is not null
                    row["Price"] = float(row["Price"])  # converting Price column data into float
                else:
                    counter = counter + 1
            logging.info(f"Ingestion Module : iterating over data Null value detected {counter}")
            logging.info(f"Ingestion Module : Column Price datatype converted to float type")

            # converting the Date string format to date type:
            timesteps = []
            for i in self.data.Date:
                i = str(i)
                datetime_obj = datetime.strptime(i, "%Y-%m-%d")
                date_only = datetime_obj.date()
                timesteps.append(date_only)
            logging.info(f"Ingestion Module : Column Date datatype converted to Date type")

            # List copied to original date column:
            self.data.Date = timesteps.copy()
            logging.info(f"Ingestion Module : data formatted into date type")
            self.data.sort_values('Date', inplace=True)  # Sorting dates accordance to calender
            self.data.set_index('Date', inplace=True)  # setting date columns as index
            logging.info(f"Ingestion Module : Sorting dates accordance to calender and setting date col as index")
            logging.info(f"Ingestion Module : Data Ingestion completed.")
            return self.data  # returning processed data

        except Exception as e:
            logging.info(f"Ingestion Module: data ingestion failed {e}")
