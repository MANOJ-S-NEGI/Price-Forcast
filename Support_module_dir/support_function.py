"""
Note: Support function  for the prediction , Folder timestamps, plotting required graphs
"""
import time
import warnings
from datetime import datetime
import pandas as pd
import matplotlib.pyplot as plt
from Variable_artifects.artifact import PLOT_DIR, COMBINE_PLOT
from Variable_artifects.artifact import FORECAST_DAY
import os


def predict_function(trained_model, dataset):
    """
    Function created for prediction

    Parameters
    ---------
    trained_model : SARIMAX model
        A trained SARIMAX model.
    dataset : pandas DataFrame
        A DataFrame containing the historical time series data.

    Returns
    -------
    predict_frame : pandas Dataframe         with predicted values and corresponding dates.
    execution_time : float
        Execution time for making predictions.
    """
    try:
        # Specify the number of steps to forecast
        FORECAST_STEPS = FORECAST_DAY
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
            new_dates = pd.date_range(start=last_date, periods=PERIODS, freq='B')[1:]  # 'B' stands for business day), [1:] Exclude the last_date

            # Print or use the confidence interval
            predict_frame = pd.DataFrame({"Date": new_dates, "Lower_Bound": confidence_interval.iloc[:, 0],
                                          "Upper_Bound": confidence_interval.iloc[:, 1]})
            return predict_frame, execution_time

    except Exception as e:
        raise e


# function for plot prediction and rolling window(previous price)
def combine_plot_function(dataframe_instance, predictions_instance):  # plot function for prediction data
    try:
        plt.figure(figsize=(13, 4))

        # Plotting the existing DataFrame
        plt.plot(dataframe_instance['Date'],
                 dataframe_instance['Price'],
                 marker='o',
                 label='Previous Rolling Window Prices')

        # Adding a vertical dashed line at the end of the existing DataFrame
        plt.axvline(x=dataframe_instance['Date'].max(),
                    color='black',
                    linestyle='--',
                    label=None)

        # Plotting the prediction DataFrame after the dashed line
        plt.plot(predictions_instance['Date'],
                 predictions_instance['Lower_Bound'],
                 marker='o',
                 label='Predicted Lower Bound',
                 color='red')

        plt.plot(predictions_instance['Date'],
                 predictions_instance['Upper_Bound'],
                 marker='o',
                 label='Predicted Upper Bound',
                 color='green')

        plt.plot(predictions_instance['Date'],
                 predictions_instance['Mean_Price'],
                 marker='o',
                 label='Mean Price',
                 color='blue')

        # Shading the region between Lower Bound and Mean Price in red
        plt.fill_between(predictions_instance['Date'],
                         predictions_instance['Lower_Bound'],
                         predictions_instance['Mean_Price'],
                         color='red', alpha=0.3)

        # Shading the region between Mean Price and Upper Bound in green
        plt.fill_between(predictions_instance['Date'],
                         predictions_instance['Mean_Price'],
                         predictions_instance['Upper_Bound'],
                         color='green', alpha=0.3)

        # Connecting the last point of df_existing to the first point of df_new
        plt.plot([dataframe_instance['Date'].max(), predictions_instance['Date'].min()],
                 [dataframe_instance['Price'].iloc[-1], predictions_instance['Lower_Bound'].iloc[0]],
                 linestyle='--', color='red')

        plt.plot([dataframe_instance['Date'].max(), predictions_instance['Date'].min()],
                 [dataframe_instance['Price'].iloc[-1], predictions_instance['Upper_Bound'].iloc[0]],
                 linestyle='--', color='green')  # Separate line for Upper Bound

        plt.plot([dataframe_instance['Date'].max(), predictions_instance['Date'].min()],
                 [dataframe_instance['Price'].iloc[-1], predictions_instance['Mean_Price'].iloc[0]],
                 linestyle='--', color='blue')  # Separate line for Mean Price

        # Setting directory and path for plot Images
        os.makedirs(PLOT_DIR, exist_ok=True)
        plot_path = os.path.join(PLOT_DIR,
                                 COMBINE_PLOT)    # Save the plot to a static directory called form artifact module
        plt.legend()
        plt.xticks(rotation=45)
        plt.savefig(plot_path)
        plt.close()

    except Exception as e:
        raise e


# Creating a function to plot time series data
def plot_time_series(timesteps, price, format='.', start=0, end=None, label=None):
    """
    Plots a timesteps (a series of points in time) against values (a series of values across timesteps).

    Parameters
    ---------
    timesteps :  timesteps
    price :  values across time
    format : style of plot, default "-"
    start : where to start the plot (setting a value will index from start of timesteps & values)
    end : where to end the plot (setting a value will index from end of timesteps & values)
    label : label to show on plot of values
    """
    try:
        # Plot the series with a solid line
        plt.plot(timesteps[start:end],
                 price[start:end],
                 linestyle='-',
                 marker=format,
                 label=label)
        plt.xlabel("Time")
        plt.ylabel("Brent Oil Price Movement")
        if label:
            plt.legend(fontsize=12)  # make label bigger
        plt.grid(True)
    except Exception as e:
        raise e


# class function 3: For date and time
class DateTimeFunctionClass:
    def __init__(self):
        self.curr_date_time = datetime.now()
        self.curr_date = self.curr_date_time.date()
        self.curr_time = self.curr_date_time.strftime("%H_%M_%S")

    def current_date(self):
        return self.curr_date

    def current_time(self):
        return self.curr_time

