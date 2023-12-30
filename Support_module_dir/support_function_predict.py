import time
import warnings
import pandas as pd


def predict_function(trained_model, dataset, forecast_days):
    """
    Function created for prediction

    Parameters
    ---------
    trained_model : SARIMAX model-A trained SARIMAX model path
    dataset : pandas DataFrame containing the historical time series data.
    param forecast_days: how many days want to forecast

    Returns
    -------
    predict_frame : pandas Dataframe  with predicted values and corresponding dates.
    execution_time : float
        Execution time for making predictions.
    """
    try:
        # Specify the number of steps to forecast
        FORECAST_STEPS = forecast_days
        PERIODS = FORECAST_STEPS + 1

        # Suppress ValueWarning and FutureWarning
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", category=UserWarning)
            warnings.simplefilter("ignore", category=FutureWarning)

            # Measure execution time
            start_time = time.time()

            # making prediction:
            forecast = trained_model.get_forecast(FORECAST_STEPS, dynamic=True)

            # Measure execution time
            execution_time = time.time() - start_time

            # Access the confidence interval directly using 'conf_int'
            confidence_interval = forecast.conf_int()

            # Get the last date in the DataFrame
            last_date = dataset.index[-2]

            # Generate a new DataFrame with the dates for the next x number of steps
            new_dates = pd.date_range(
                start=last_date,
                periods=PERIODS,
                freq='B')[1:]  # 'B' stands for business day), [1:] Exclude the last_date

            # Print or use the confidence interval
            predict_frame = pd.DataFrame({"Date": new_dates, "Lower_Bound": confidence_interval.iloc[:, 0],
                                          "Upper_Bound": confidence_interval.iloc[:, 1]})
            return predict_frame, execution_time

    except Exception as e:
        raise e
