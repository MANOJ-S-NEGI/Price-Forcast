# artifact for log file
LOG_ENTRY_DIR = "Log_entry"

# artifact for connection
BUNDLE_NAME = "secure-connect-oil.zip"
ROOT_PATH = "D:/msn/pycharm_projects/Brentprice/secure-connect-oil.zip"

# artifact for csv file:)
CSV_FILE = "Brent_oil.csv"
CSV_DIR = "Csv"

# app file artifact
PLOT_DIR = "static"
COMBINE_PLOT = "combined_price_plot.jpg"

# Trained model directory:
MODEL_FILENAME = "SARIMAX_FORCAST_MODEL.joblib"
MAIN_MODEL_DIR = "Saved_Model_dir"

# SARIMAX Model initialization
ORDER = (1, 1, 1)
SEASONAL_ORDER = (1, 1, 1, 7)

# support module artifact
FORECAST_DAY = 7  # give 7 days prediction customize time frame

"""
    Note: ORDER = (p, d, q) SEASONAL_ORDER = (P, D, Q, s)
    #  P = 1   P: Autoregressive order at the seasonal frequency.
    #  D = 1   D: Order of seasonal differencing.
    #  Q = 1   Q: Moving average order at the seasonal frequency.
    #  s = 7   s: Window size. (keep it small)
    #  p = 1   p:(AutoRegressive order) if p=2, the model uses the two most recent observations to predict the current one.
    #  d = 1   d:(Integrated order)
    #  q = 1   q: the model includes the most recent forecast error in the prediction.
"""
