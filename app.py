from flask import Flask, render_template

from Variable_artifects.artifact import PLOT_DIR, COMBINE_PLOT
from components.model_prediction import Prediction
from Support_module_dir.support_function import combine_plot_function
import os


def app_mode():
    try:
        saved_model_path = "Saved_Model_dir/2023-12-23_00_42_22/SARIMAX_FORCAST_MODEL.joblib"
        prediction = Prediction(saved_model_path).model_prediction()  # called class Prediction
        return prediction

    except Exception as e:
        raise e


# Declaring the dataframe as predictions_instance for prediction and dataframe_instance for csv Dataset
predictions_instance, dataframe_instance = app_mode()

# Reset the index and move it into a new column
dataframe_instance = dataframe_instance[-7:].reset_index()

# Assuming predictions_instance is your DataFrame
predictions_instance['Mean_Price'] = (predictions_instance['Lower_Bound'] + predictions_instance['Upper_Bound']) / 2

# calling plot function
combine_plot_function(dataframe_instance, predictions_instance)

app = Flask(__name__)


@app.route('/', methods=['GET'])
def Home():
    return render_template("about.html")


@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Setting directory and path for plot Images
        plot_path = os.path.join(PLOT_DIR,
                                 COMBINE_PLOT)  # Save the plot to a static directory called form artifact module

        return render_template('index.html', predictions=predictions_instance.to_dict(orient="records"),
                               dataframe=dataframe_instance.to_dict(orient="records"),
                               combine_plot=plot_path)
    except Exception as e:
        return render_template('error.html', error_message=str(e))


if __name__ == '__main__':
    app.run()
