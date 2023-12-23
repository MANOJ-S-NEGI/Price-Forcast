import os
import cassandra
import csv
from dotenv import load_dotenv
from Variable_artifects.artifact import CSV_FILE
from Variable_artifects.artifact import CSV_DIR
from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider
from Variable_artifects.artifact import BUNDLE_NAME
from Variable_artifects.artifact import ROOT_PATH
from Log_Connection.log_file import logging

# Load variables from .env file
load_dotenv()


class ConnectionDatabase:
    def __init__(self):
        self.bundle_file = BUNDLE_NAME
        self.client_id = os.getenv("CLIENT_ID")
        self.secret_id = os.getenv("SECRET_ID")
        self.token_id = os.getenv('TOKEN_ID')

    @staticmethod
    def cloud_config_bundle_path():
        try:
            return ROOT_PATH if os.path.exists(ROOT_PATH) else BUNDLE_NAME  # setting path of Bundle.zip
        
        except FileNotFoundError as e:
            logging.info(f"Error with bundle file/path: {e}")

    def database_cassandra_connection(self):
        try:
            # configuring the connection with database
            cloud_config = {'secure_connect_bundle': ConnectionDatabase.cloud_config_bundle_path()}
            auth_provider = PlainTextAuthProvider(self.client_id, self.secret_id)
            cluster = Cluster(cloud=cloud_config, auth_provider=auth_provider)
            session = cluster.connect()

            # checking database connection:
            row = session.execute("select release_version from system.local").one()
            if row:
                logging.info(f"Cassandra connection established {row[0]}, Cassandra version: {cassandra.__version__}")
            else:
                logging.info(f"Cassandra connection : An error occurred.")
            return cluster
        
        except Exception as e:
            logging.info(f"Cassandra connection error: {e}")

    def fetch_database(self):
        try:
            """
            function description :  retrieving data from cassandra data base and saving it to the .csv file
            """
            cluster = self.database_cassandra_connection()
            session = cluster.connect()
            logging.info(f"Cassandra query initializing fetching data from database\n ")
            row = session.execute("SELECT * FROM brentoil.berentprice").all()
            logging.info(f"Cassandra query executed successfully \n ")

            # Creating csv dir and writing file as csv
            os.makedirs(CSV_DIR, exist_ok=True)
            CSV_PATH = os.path.join(CSV_DIR, CSV_FILE)  # called from artifact module

            # writing data into file as .csv
            with open(CSV_PATH, 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(['Date', 'Price'])  # writing header for file [date, price]
                for i in row:
                    writer.writerow(i)  # writing data into csv file
            row_count = session.execute("select count(*) from brentoil.berentprice")  # Executing another query for
            logging.info(f"Total number of rows: {row_count} \n ")

        except Exception as e:
            logging.info(f"fetching_database failed {e}")
