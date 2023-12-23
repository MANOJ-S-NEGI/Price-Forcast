from flask import Flask
from flask import render_template
from components.model_prediction import Prediction
from Support_module_dir.support_function_plot import combine_plot_function
import io
import base64


# Function to load the model and make predictions
def load_and_predict_model():
    try:
        saved_model_path = "Saved_Model_dir/2023-12-24_01_07_38/SARIMAX_FORCAST_MODEL.joblib"
        prediction = Prediction(saved_model_path).model_prediction()  # called class Prediction
        return prediction
    except FileNotFoundError as file_error:
        raise FileNotFoundError(f"Error loading model: {file_error}")
    except Exception as e:
        raise e


# Call the function to load and predict
predictions_instance, dataframe_instance = load_and_predict_model()

# Reset the index and move it into a new column
dataframe_instance = dataframe_instance[-7:].reset_index()

# Assuming predictions_instance is your DataFrame
predictions_instance['Mean_Price'] = (predictions_instance['Lower_Bound'] + predictions_instance['Upper_Bound']) / 2

# Create an in-memory buffer
buffer = io.BytesIO()

# calling plot function
combine_plot_function(dataframe_instance, predictions_instance, buffer)

plot_img_str = base64.b64encode(buffer.getvalue()).decode()

# Initialize Flask app
app = Flask(__name__)


# Route for the home page
@app.route('/', methods=['GET'])
def home():
    return render_template("about.html")


# Route for the prediction page
@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Setting directory and path for plot Images
        # plot_path = os.path.join(PLOT_DIR, COMBINE_PLOT)

        return render_template('index.html', predictions=predictions_instance.to_dict(orient="records"),
                               dataframe=dataframe_instance.to_dict(orient="records"),
                               plot_img_str=plot_img_str)
    except Exception as e:
        return render_template('error.html', error_message=str(e))


# Run the app
if __name__ == '__main__':
    app.run()
