from datetime import datetime
from Log_Connection.log_file import logging
import matplotlib.pyplot as plt


# function for plot prediction and rolling window(previous price)
def combine_plot_function(dataframe_instance, predictions_instance, buffer):
    try:
        plt.figure(figsize=(13, 4))

        # Scatter plot for the existing DataFrame
        plt.plot(dataframe_instance['Date'],
                 dataframe_instance['Price'],
                 marker='o',
                 label='Previous Rolling Window Prices')

        # Adding a vertical dashed line at the end of the existing DataFrame
        plt.axvline(x=dataframe_instance['Date'].max(),
                    color='black',
                    linestyle='--',
                    label=None)

        # Scatter plots for the prediction DataFrame after the dashed line
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

        # Setting grid
        plt.grid(True)
        plt.legend()
        plt.xticks(rotation=45)

        # storing in buffer rather saving it
        plt.savefig(buffer, format='png', bbox_inches='tight')
        plt.close()

    except Exception as e:
        logging.info(f"Error in combine_plot_function: {e}")


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
