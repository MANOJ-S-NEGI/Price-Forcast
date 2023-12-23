# calling libraries
from Support_module_dir.support_function import predict_function
from Support_module_dir.support_function import DateTimeFunctionClass
from Variable_artifects.artifact import ORDER
from Variable_artifects.artifact import MAIN_MODEL_DIR
from Variable_artifects.artifact import MODEL_FILENAME
from Variable_artifects.artifact import SEASONAL_ORDER
import logging
import statsmodels.api as sm
import warnings
import joblib
import os


class Training:
    def __init__(self):
        self.date_time = DateTimeFunctionClass()

    def training_data(self, dataset):
        """
        Function created for Training of dataset
        Parameters:
        ---------
        dataset : pandas DataFrame -A DataFrame containing the historical time series data.
                      function saves the model and return nothing
        """

        # Both function called from support_function.py
        current_time = self.date_time.current_time()
        current_date = self.date_time.current_date()
        try:
            logging.info("Training module: Initializing")
            with warnings.catch_warnings():
                warnings.simplefilter("ignore",
                                      category=UserWarning)
                warnings.simplefilter("ignore",
                                      category=FutureWarning)
                logging.info("Training Module: Initializing model SARIMAX")
                model_params = dict(order=ORDER,
                                    seasonal_order=SEASONAL_ORDER)
                model = sm.tsa.statespace.SARIMAX(dataset,
                                                  **model_params)
                logging.info("Training Module: Model SARIMAX - data fitting initialize")
                result = model.fit()
                summary = result.summary()
                result.plot_diagnostics()
                logging.info(f"Training Module: Summary: {summary}")
                predictions, execution_time = predict_function(result,
                                                               dataset)
                logging.info(f"Training Module: Predictions: {predictions}\n"
                             f"Training Module: Execution time: {execution_time}\n"
                             f" The aic and bic attributes of model Akaike Information Criterion and Bayesian Information Criterion, respectively\t:"
                             f" aic_value = {result.aic}  \n bic_value = {result.bic}")

                # Save the trained model using joblib
                timestamp = f"{current_date}_{current_time}"
                os.makedirs(MAIN_MODEL_DIR, exist_ok=True)
                sub_model_dir = os.path.join(MAIN_MODEL_DIR, timestamp)
                os.makedirs(sub_model_dir, exist_ok=True)
                model_filename = os.path.join(sub_model_dir, MODEL_FILENAME)
                joblib.dump(result, model_filename)
                logging.info("Training Module: Model saved successfully")

        except Exception as e:
            logging.info(f"Training_module Failed: {e}")
