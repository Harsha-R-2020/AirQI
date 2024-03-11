import flask
from flask_restful import Resource, Api
import re
import requests
from bs4 import BeautifulSoup, Comment
import pandas as pd
import numpy as np
from flask import  request, jsonify,send_file
import plotly.graph_objects as go
from concurrent.futures import ThreadPoolExecutor
import matplotlib.pyplot as plt
import plotly.io as pio
import seaborn as sns              # statistical data visualization
sns.set_theme()
import joblib
import xgboost  
from tensorflow.keras.models import load_model
import pickle
from copy import deepcopy


file = open('trdf.pkl', 'rb')
pickled_data = file.read()
train_df = pickle.loads(pickled_data)
file.close()
file = open('vldf.pkl', 'rb')
pickled_data = file.read()
val_df = pickle.loads(pickled_data)
file.close()
file = open('tsdf.pkl', 'rb')
pickled_data = file.read()
test_df = pickle.loads(pickled_data)
file.close()
file = open('trmean.pkl', 'rb')
pickled_data = file.read()
train_mean = pickle.loads(pickled_data)
file.close()
file = open('trstd.pkl', 'rb')
pickled_data = file.read()
train_std = pickle.loads(pickled_data)
file.close()
class WindowGenerator():
    def __init__(self, input_width, label_width, label_columns, offset, train_df=train_df, val_df=val_df, test_df=test_df):
        '''
        Initializes a WindowGenerator object (based on the Tensorflow tutorial on Time series forecasting).

        Parameters
        ----------
            input_width (int): The input size of the hostory used for a prediction.
            label_width (int): How many steps into the future to predict.
            label_columns (list: int): The features to be used as prediction targets.
            train_df (DataFrame): The training DataFrame.
            val_df (DataFrame): The validation DataFrame.
            test_df (DataFrame): The test DataFrame.
        '''

        # Store the raw data.
        self.train_df = train_df[label_columns + DATETIME_FEATURES]
        self.val_df = val_df[label_columns + DATETIME_FEATURES]
        self.test_df = test_df[label_columns + DATETIME_FEATURES]

        # Work out the label column indices.
        self.column_indices = {name: i for i, name in enumerate(self.train_df.columns)}
        self.label_columns = label_columns
        self.label_columns_indices = [self.column_indices[feature] for feature in self.label_columns]

        # Work out the window parameters.
        self.input_width = input_width
        self.label_width = label_width
        self.offset = offset
        self.window_size = self.input_width + self.offset

        # Work out input and label indices.
        self.input_slice = slice(0, input_width)
        self.input_indices = np.arange(self.window_size)[self.input_slice]

        self.label_start = self.window_size - self.label_width
        self.label_slice = slice(self.label_start, None)
        self.label_indices = np.arange(self.window_size)[self.label_slice]

        # Initialize the splitted train, val, and test datasets for easy use.
        self._initialize_sets()

    def _initialize_sets(self):
        self._train = self.split_window(self.train_df)
        self._val = self.split_window(self.val_df)
        self._test = self.split_window(self.test_df)

    def __repr__(self):
        return '\n'.join([f'Total window size: {self.window_size}',
                          f'Input indices: {self.input_indices}',
                          f'Label indices: {self.label_indices}',
                          f'Target features: {self.label_columns}'])
@property
def train(self):
    return self._train

@property
def val(self):
    return self._val

@property
def test(self):
    return self._test

WindowGenerator.train = train
WindowGenerator.val = val
WindowGenerator.test = test

app = flask.Flask(__name__)
api = Api(app)

@app.route('/api', methods = ['GET'])
def returnascii():
    d = {}
    inputchr = str(request.args['query'])
    if(inputchr=="Chennai"):
        city_url="https://air-quality.com/place//204c2788?lang=en&standard=naqi_in"
        city_response = requests.get(city_url)
        city_soup = BeautifulSoup(city_response.content, "html.parser")
        aqi_comment = city_soup.find(text=lambda text: isinstance(text, Comment) and "indexValue" in text)
        aqi_value = re.search(r"\d+", aqi_comment).group() if aqi_comment else np.NaN
        d['message'] = aqi_value
    elif(inputchr=="Delhi"):
        city_url="https://air-quality.com/place/india/delhi/fb9ff33b?lang=en&standard=naqi_in"
        city_response = requests.get(city_url)
        city_soup = BeautifulSoup(city_response.content, "html.parser")
        aqi_comment = city_soup.find(text=lambda text: isinstance(text, Comment) and "indexValue" in text)
        aqi_value = re.search(r"\d+", aqi_comment).group() if aqi_comment else np.NaN
        d['message'] = aqi_value
    elif(inputchr=="Banglore"):
        city_url="https://air-quality.com/place/india/bengaluru/f8edf853?lang=en&standard=naqi_in"
        city_response = requests.get(city_url)
        city_soup = BeautifulSoup(city_response.content, "html.parser")
        aqi_comment = city_soup.find(text=lambda text: isinstance(text, Comment) and "indexValue" in text)
        aqi_value = re.search(r"\d+", aqi_comment).group() if aqi_comment else np.NaN
        d['message'] = aqi_value
    elif(inputchr=="Mumbai"):
        city_url="https://air-quality.com/place/india/mumbai/6bf15df3?lang=en&standard=naqi_in"
        city_response = requests.get(city_url)
        city_soup = BeautifulSoup(city_response.content, "html.parser")
        aqi_comment = city_soup.find(text=lambda text: isinstance(text, Comment) and "indexValue" in text)
        aqi_value = re.search(r"\d+", aqi_comment).group() if aqi_comment else np.NaN
        d['message'] = aqi_value
    else:
        d['message']= "0"
    return d


@app.route('/futureprediction', methods = ['GET'])
def futurepredictionplot():
    X_test=pd.read_csv('x_test.csv')
    future_df=pd.read_csv('future_data.csv')
    X_test['datetime'] =  pd.to_datetime(X_test['datetime'])
    X_test = X_test.set_index('datetime')
    future_df['datetime'] =  pd.to_datetime(future_df['datetime'])
    future_df = future_df.set_index('datetime')
    test_predictions = X_test.copy()
    future_predictions = future_df.copy()
    loaded_model = joblib.load("AQI_model.pkl")
    test_predictions['predict_XGBoost'] = loaded_model.predict(X_test)
    future_predictions['predict_XGBoost'] = loaded_model.predict(future_df)
    y_test = pd.read_csv('y_test.csv')
    y_test['datetime'] =  pd.to_datetime(y_test['datetime'])
    y_test = y_test.set_index('datetime')
    fig, ax = plt.subplots(figsize=(12, 6))
    # Plot the data using the Axes object
    start_index = -len(future_df)
    sns.lineplot(data=y_test[start_index:], label="Actual Data", ax=ax)
    sns.lineplot(data=test_predictions['predict_XGBoost'][start_index:], label="Testing Prediction", ax=ax)
    sns.lineplot(data=future_predictions['predict_XGBoost'], label="Future Prediction", ax=ax)
    separator_date = future_df.index[0]  # Change this to the actual date separating testing and future predictions
    ax.axvline(x=separator_date, color='red', linestyle='--', label='Future Predictions Start')
    # Customize the plot further if needed
    ax.set_xlabel("XGBoost - Predictions", fontsize=14)  # Replace with your actual X-axis label
    ax.set_ylabel("PM2.5(ug)\m3", fontsize=14)  # Replace with your actual Y-axis label
    ax.set_title("Delhi PM2.5 Forecasting", fontsize=16)  # Replace with your actual plot title
    ax.legend(fontsize=12)
    # Show the plot
    plt.tight_layout()
    plt.savefig('prediction.jpg', dpi=300, bbox_inches='tight') 
    return send_file('prediction.jpg', mimetype='image/jpeg')

@app.route('/futurepredictionlstm', methods = ['GET'])
def futurepredictionlstmplot():
    def get_sin_cos_timestamp(timestamp):
        '''
        Takes as input a timestamp and returns an array of sine and cosine transforms of the timestamp.
        '''

        date_time = pd.to_datetime(timestamp, format='%d.%m.%Y %H:%M:%S')
        timestamp = pd.Timestamp.timestamp(date_time)
        day = 24*60*60
        year = (365.2425)*day

        return [np.sin(timestamp * (2 * np.pi / day)),
                np.cos(timestamp * (2 * np.pi / day)),
                np.sin(timestamp * (2 * np.pi / year)),
                np.cos(timestamp * (2 * np.pi / year))]
    def auto_predict(model, window, date_range):
        '''
        Autoregressively predicts future values.

        Parameters
        ----------
            model (Sequential): The model to use for future predictions.
            window (WindowGenerator): The window to be used for predictions.
            date_range (date_range): The range of future dates for predictions.

        Return
        ------
            predictions (array): An array of future predictions.
        '''

        X_future = deepcopy(window.test[0][-1:])
        y_future = []

        index = 0

        for target_date in date_range:
            # Make new prediction
            prediction = model.predict(X_future[-1:], verbose=None)
            y_future.append(prediction)

            # Create new input
            input = X_future[-1][1:]
            num_features = window.train[1].shape[-1]
            timestamp_sin_cos = get_sin_cos_timestamp(target_date)
            timestamp_sin_cos = (timestamp_sin_cos - train_mean[window.train_df.columns][num_features:]) / train_std[window.train_df.columns][num_features:]

            observation = np.concatenate((prediction[0], timestamp_sin_cos), axis=0)
            observation = np.expand_dims(observation, axis=0)

            input = np.concatenate((input, observation), axis=0)
            input = np.expand_dims(input, axis=0)

            X_future = np.concatenate((X_future, input), axis=0)

            print(f"{index+1}/{len(date_range)}", end='\r', flush=True)

            index += 1

        return np.array(y_future)
    # Load future dates from pickled file
    file = open('future_dates.pkl', 'rb')
    pickled_data = file.read()
    future_dates = pickle.loads(pickled_data)
    file.close()
    model_path = 'single_step_lstm.keras'
    # Load the model
    loaded_hyper_model = load_model(model_path)
    filew = open('window.pkl', 'rb')
    pickled_data_w = filew.read()
    window = pickle.loads(pickled_data_w)
    filew.close()
    predictions = auto_predict(loaded_hyper_model, window, future_dates)
    future_df = pd.DataFrame(predictions[:,0,0], index = future_dates, columns =['Future Prediction'])
    # Get test set predictions.
    test_predictions = loaded_hyper_model.predict(window.test[0])
    test_predictions = pd.DataFrame(test_predictions, index=window.test_df.index[window.input_width:-1], columns=window.label_columns)
    # Set figure properties.
    fig = plt.figure(figsize=(12, 5))
    ax = fig.add_subplot(111)
    ax.set_title("Hypermodel LSTM - Predictions")
    # Show the same amount of testing timesteps as future timesteps.
    start_index = -len(future_df)
    sns.lineplot(data=window.test_df[start_index:], x=window.test_df.index[start_index:], y=window.label_columns[0], label="Test Data")
    sns.lineplot(data=test_predictions[start_index:], x=test_predictions.index[start_index:], y=window.label_columns[0], label="Test Prediction")
    sns.lineplot(data=future_df, x=future_df.index, y=future_df['Future Prediction'], label="Future Prediction")
    separator_date = future_df.index[0]  # Change this to the actual date separating testing and future predictions
    ax.axvline(x=separator_date, color='red', linestyle='--', label='Future Predictions Start')
    ax.set(xlabel=None)
    #plt.show()
    plt.tight_layout()
    plt.savefig('predictionlstm.jpg', dpi=300, bbox_inches='tight') 
    return send_file('predictionlstm.jpg', mimetype='image/jpeg')



@app.route('/specificcleanplot', methods = ['GET'])
def returnspecificcleanplot():
    d = {}
    inputchr = str(request.args['query'])
    if(inputchr=="Chennai"):
        url = "https://air-quality.com/place//204c2788?lang=en&standard=naqi_in"
        response = requests.get(url)
        soup = BeautifulSoup(response.content, "html.parser")
        site_items = soup.find_all("a", class_="site-item")
        data = []
        def process_city_href(city_href):
            city_response = requests.get(city_href)
            city_soup = BeautifulSoup(city_response.content, "html.parser")

            # city name and state name
            city_name = city_soup.find("h2").text.strip()
            state_name = city_soup.find("p").text.strip().split(", ")[1]
            time = city_soup.find("div", class_="update-time").text.strip()
            aqi_comment = city_soup.find(string=lambda text: isinstance(text, Comment) and "indexValue" in text)
            aqi_value = float(re.search(r"\d+", aqi_comment).group()) if aqi_comment else np.NaN
            pollutants = city_soup.find_all("div", class_="pollutant-item")

            pollutant_data = {}
            for pollutant in pollutants:
                name = pollutant.find("div", class_="name").text.strip()
                value = pollutant.find("div", class_="value").text.strip()
                pollutant_data[name] = float(value) if value else np.NaN

            temperature = float(city_soup.find("div", class_="temperature").text.strip().replace("℃", "")) or np.NaN
            humidity = float(city_soup.find("div", class_="humidity").text.strip().replace("%", "")) or np.NaN
            wind_speed = float(city_soup.find("div", class_="wind").text.strip().replace("kph", "")) or np.NaN
            type = city_soup.find("div", class_="level").text.strip()
            type=type.replace("Moderately polluted", "Moderate")
            data.append([time,state_name, city_name,pollutant_data.get("PM2.5"), pollutant_data.get("PM10"), pollutant_data.get("O3"),pollutant_data.get("SO2"), pollutant_data.get("CO"),wind_speed, humidity, temperature, aqi_value,type])


        with ThreadPoolExecutor(max_workers=200) as executor:
            for site_item in site_items:
                state_href = site_item["href"]
                state_response = requests.get(state_href)
                state_soup = BeautifulSoup(state_response.content, "html.parser")
                all_city_hrefs = state_soup.find_all("a", class_="site-item")
                for city_href in all_city_hrefs:
                    city_href = city_href["href"]
                    if "https://air-quality.com/place/india" in city_href:
                        executor.submit(process_city_href, city_href)

        # Create a DataFrame from the collected data
        df = pd.DataFrame(data, columns=["Time","State", "City", "PM2.5", "PM10", "O3", "SO2", "CO", "Wind Speed", "Humidity", "Temp", "AQI","AQI Type"])
        # Remove duplicate cities
        df_unique = df.drop_duplicates(subset='City')

        df_sorted = df_unique.sort_values('AQI', ascending=False)

        top_cleansed_cities = df_sorted.tail(10)[::-1]

        fig = go.Figure(data=[go.Bar(x=top_cleansed_cities['City'], y=top_cleansed_cities['AQI'],marker=dict(color='green'),text=top_cleansed_cities['AQI'],textposition='auto')])
        fig.update_layout(
            title='Top 10 Cleansed Cities',
            xaxis=dict(title='City'),
            yaxis=dict(title='AQI'),
        )
        pio.write_image(fig, 'good_plot.jpg', format="jpeg")
        return send_file('good_plot.jpg', mimetype='image/jpeg')
    elif(inputchr=="Delhi"):
        url = "https://air-quality.com/place/india/delhi/fb9ff33b?lang=en&standard=naqi_in"
        response = requests.get(url)
        soup = BeautifulSoup(response.content, "html.parser")
        site_items = soup.find_all("a", class_="site-item")
        data = []
        def process_city_href(city_href):
            city_response = requests.get(city_href)
            city_soup = BeautifulSoup(city_response.content, "html.parser")

            # city name and state name
            city_name = city_soup.find("h2").text.strip()
            state_name = city_soup.find("p").text.strip().split(", ")[1]
            time = city_soup.find("div", class_="update-time").text.strip()
            aqi_comment = city_soup.find(string=lambda text: isinstance(text, Comment) and "indexValue" in text)
            aqi_value = float(re.search(r"\d+", aqi_comment).group()) if aqi_comment else np.NaN
            pollutants = city_soup.find_all("div", class_="pollutant-item")

            pollutant_data = {}
            for pollutant in pollutants:
                name = pollutant.find("div", class_="name").text.strip()
                value = pollutant.find("div", class_="value").text.strip()
                pollutant_data[name] = float(value) if value else np.NaN

            temperature = float(city_soup.find("div", class_="temperature").text.strip().replace("℃", "")) or np.NaN
            humidity = float(city_soup.find("div", class_="humidity").text.strip().replace("%", "")) or np.NaN
            wind_speed = float(city_soup.find("div", class_="wind").text.strip().replace("kph", "")) or np.NaN
            type = city_soup.find("div", class_="level").text.strip()
            type=type.replace("Moderately polluted", "Moderate")
            data.append([time,state_name, city_name,pollutant_data.get("PM2.5"), pollutant_data.get("PM10"), pollutant_data.get("O3"),pollutant_data.get("SO2"), pollutant_data.get("CO"),wind_speed, humidity, temperature, aqi_value,type])


        with ThreadPoolExecutor(max_workers=200) as executor:
            for site_item in site_items:
                state_href = site_item["href"]
                state_response = requests.get(state_href)
                state_soup = BeautifulSoup(state_response.content, "html.parser")
                all_city_hrefs = state_soup.find_all("a", class_="site-item")
                for city_href in all_city_hrefs:
                    city_href = city_href["href"]
                    if "https://air-quality.com/place/india" in city_href:
                        executor.submit(process_city_href, city_href)

        # Create a DataFrame from the collected data
        df = pd.DataFrame(data, columns=["Time","State", "City", "PM2.5", "PM10", "O3", "SO2", "CO", "Wind Speed", "Humidity", "Temp", "AQI","AQI Type"])
        # Remove duplicate cities
        df_unique = df.drop_duplicates(subset='City')

        df_sorted = df_unique.sort_values('AQI', ascending=False)

        top_cleansed_cities = df_sorted.tail(10)[::-1]

        fig = go.Figure(data=[go.Bar(x=top_cleansed_cities['City'], y=top_cleansed_cities['AQI'],marker=dict(color='green'),text=top_cleansed_cities['AQI'],textposition='auto')])
        fig.update_layout(
            title='Top 10 Cleansed Cities',
            xaxis=dict(title='City'),
            yaxis=dict(title='AQI'),
        )
        pio.write_image(fig, 'good_plot.jpg', format="jpeg")
        return send_file('good_plot.jpg', mimetype='image/jpeg')
    elif(inputchr=="Banglore"):
        url = "https://air-quality.com/place/india/bengaluru/f8edf853?lang=en&standard=naqi_in"
        response = requests.get(url)
        soup = BeautifulSoup(response.content, "html.parser")
        site_items = soup.find_all("a", class_="site-item")
        data = []
        def process_city_href(city_href):
            city_response = requests.get(city_href)
            city_soup = BeautifulSoup(city_response.content, "html.parser")

            # city name and state name
            city_name = city_soup.find("h2").text.strip()
            state_name = city_soup.find("p").text.strip().split(", ")[1]
            time = city_soup.find("div", class_="update-time").text.strip()
            aqi_comment = city_soup.find(string=lambda text: isinstance(text, Comment) and "indexValue" in text)
            aqi_value = float(re.search(r"\d+", aqi_comment).group()) if aqi_comment else np.NaN
            pollutants = city_soup.find_all("div", class_="pollutant-item")

            pollutant_data = {}
            for pollutant in pollutants:
                name = pollutant.find("div", class_="name").text.strip()
                value = pollutant.find("div", class_="value").text.strip()
                pollutant_data[name] = float(value) if value else np.NaN

            temperature = float(city_soup.find("div", class_="temperature").text.strip().replace("℃", "")) or np.NaN
            humidity = float(city_soup.find("div", class_="humidity").text.strip().replace("%", "")) or np.NaN
            wind_speed = float(city_soup.find("div", class_="wind").text.strip().replace("kph", "")) or np.NaN
            type = city_soup.find("div", class_="level").text.strip()
            type=type.replace("Moderately polluted", "Moderate")
            data.append([time,state_name, city_name,pollutant_data.get("PM2.5"), pollutant_data.get("PM10"), pollutant_data.get("O3"),pollutant_data.get("SO2"), pollutant_data.get("CO"),wind_speed, humidity, temperature, aqi_value,type])


        with ThreadPoolExecutor(max_workers=200) as executor:
            for site_item in site_items:
                state_href = site_item["href"]
                state_response = requests.get(state_href)
                state_soup = BeautifulSoup(state_response.content, "html.parser")
                all_city_hrefs = state_soup.find_all("a", class_="site-item")
                for city_href in all_city_hrefs:
                    city_href = city_href["href"]
                    if "https://air-quality.com/place/india" in city_href:
                        executor.submit(process_city_href, city_href)

        # Create a DataFrame from the collected data
        df = pd.DataFrame(data, columns=["Time","State", "City", "PM2.5", "PM10", "O3", "SO2", "CO", "Wind Speed", "Humidity", "Temp", "AQI","AQI Type"])
        # Remove duplicate cities
        df_unique = df.drop_duplicates(subset='City')

        df_sorted = df_unique.sort_values('AQI', ascending=False)

        top_cleansed_cities = df_sorted.tail(10)[::-1]

        fig = go.Figure(data=[go.Bar(x=top_cleansed_cities['City'], y=top_cleansed_cities['AQI'],marker=dict(color='green'),text=top_cleansed_cities['AQI'],textposition='auto')])
        fig.update_layout(
            title='Top 10 Cleansed Cities',
            xaxis=dict(title='City'),
            yaxis=dict(title='AQI'),
        )
        pio.write_image(fig, 'good_plot.jpg', format="jpeg")
        return send_file('good_plot.jpg', mimetype='image/jpeg')
    elif(inputchr=="Mumbai"):
        url = "https://air-quality.com/place/india/mumbai/6bf15df3?lang=en&standard=naqi_in"
        response = requests.get(url)
        soup = BeautifulSoup(response.content, "html.parser")
        site_items = soup.find_all("a", class_="site-item")
        data = []
        def process_city_href(city_href):
            city_response = requests.get(city_href)
            city_soup = BeautifulSoup(city_response.content, "html.parser")

            # city name and state name
            city_name = city_soup.find("h2").text.strip()
            state_name = city_soup.find("p").text.strip().split(", ")[1]
            time = city_soup.find("div", class_="update-time").text.strip()
            aqi_comment = city_soup.find(string=lambda text: isinstance(text, Comment) and "indexValue" in text)
            aqi_value = float(re.search(r"\d+", aqi_comment).group()) if aqi_comment else np.NaN
            pollutants = city_soup.find_all("div", class_="pollutant-item")

            pollutant_data = {}
            for pollutant in pollutants:
                name = pollutant.find("div", class_="name").text.strip()
                value = pollutant.find("div", class_="value").text.strip()
                pollutant_data[name] = float(value) if value else np.NaN

            temperature = float(city_soup.find("div", class_="temperature").text.strip().replace("℃", "")) or np.NaN
            humidity = float(city_soup.find("div", class_="humidity").text.strip().replace("%", "")) or np.NaN
            wind_speed = float(city_soup.find("div", class_="wind").text.strip().replace("kph", "")) or np.NaN
            type = city_soup.find("div", class_="level").text.strip()
            type=type.replace("Moderately polluted", "Moderate")
            data.append([time,state_name, city_name,pollutant_data.get("PM2.5"), pollutant_data.get("PM10"), pollutant_data.get("O3"),pollutant_data.get("SO2"), pollutant_data.get("CO"),wind_speed, humidity, temperature, aqi_value,type])


        with ThreadPoolExecutor(max_workers=200) as executor:
            for site_item in site_items:
                state_href = site_item["href"]
                state_response = requests.get(state_href)
                state_soup = BeautifulSoup(state_response.content, "html.parser")
                all_city_hrefs = state_soup.find_all("a", class_="site-item")
                for city_href in all_city_hrefs:
                    city_href = city_href["href"]
                    if "https://air-quality.com/place/india" in city_href:
                        executor.submit(process_city_href, city_href)

        # Create a DataFrame from the collected data
        df = pd.DataFrame(data, columns=["Time","State", "City", "PM2.5", "PM10", "O3", "SO2", "CO", "Wind Speed", "Humidity", "Temp", "AQI","AQI Type"])
        # Remove duplicate cities
        df_unique = df.drop_duplicates(subset='City')

        df_sorted = df_unique.sort_values('AQI', ascending=False)

        top_cleansed_cities = df_sorted.tail(10)[::-1]

        fig = go.Figure(data=[go.Bar(x=top_cleansed_cities['City'], y=top_cleansed_cities['AQI'],marker=dict(color='green'),text=top_cleansed_cities['AQI'],textposition='auto')])
        fig.update_layout(
            title='Top 10 Cleansed Cities',
            xaxis=dict(title='City'),
            yaxis=dict(title='AQI'),
        )
        pio.write_image(fig, 'good_plot.jpg', format="jpeg")
        return send_file('good_plot.jpg', mimetype='image/jpeg')



@app.route('/specificpollutedplot', methods = ['GET'])
def returnspecificpollutedplot():
    d = {}
    inputchr = str(request.args['query'])
    if(inputchr=="Chennai"):
        url = "https://air-quality.com/place//204c2788?lang=en&standard=naqi_in"
        response = requests.get(url)
        soup = BeautifulSoup(response.content, "html.parser")
        site_items = soup.find_all("a", class_="site-item")
        data = []
        def process_city_href(city_href):
            city_response = requests.get(city_href)
            city_soup = BeautifulSoup(city_response.content, "html.parser")

            # city name and state name
            city_name = city_soup.find("h2").text.strip()
            state_name = city_soup.find("p").text.strip().split(", ")[1]
            time = city_soup.find("div", class_="update-time").text.strip()
            aqi_comment = city_soup.find(string=lambda text: isinstance(text, Comment) and "indexValue" in text)
            aqi_value = float(re.search(r"\d+", aqi_comment).group()) if aqi_comment else np.NaN
            pollutants = city_soup.find_all("div", class_="pollutant-item")

            pollutant_data = {}
            for pollutant in pollutants:
                name = pollutant.find("div", class_="name").text.strip()
                value = pollutant.find("div", class_="value").text.strip()
                pollutant_data[name] = float(value) if value else np.NaN

            temperature = float(city_soup.find("div", class_="temperature").text.strip().replace("℃", "")) or np.NaN
            humidity = float(city_soup.find("div", class_="humidity").text.strip().replace("%", "")) or np.NaN
            wind_speed = float(city_soup.find("div", class_="wind").text.strip().replace("kph", "")) or np.NaN
            type = city_soup.find("div", class_="level").text.strip()
            type=type.replace("Moderately polluted", "Moderate")
            data.append([time,state_name, city_name,pollutant_data.get("PM2.5"), pollutant_data.get("PM10"), pollutant_data.get("O3"),pollutant_data.get("SO2"), pollutant_data.get("CO"),wind_speed, humidity, temperature, aqi_value,type])


        with ThreadPoolExecutor(max_workers=200) as executor:
            for site_item in site_items:
                state_href = site_item["href"]
                state_response = requests.get(state_href)
                state_soup = BeautifulSoup(state_response.content, "html.parser")
                all_city_hrefs = state_soup.find_all("a", class_="site-item")
                for city_href in all_city_hrefs:
                    city_href = city_href["href"]
                    if "https://air-quality.com/place/india" in city_href:
                        executor.submit(process_city_href, city_href)

        # Create a DataFrame from the collected data
        df = pd.DataFrame(data, columns=["Time","State", "City", "PM2.5", "PM10", "O3", "SO2", "CO", "Wind Speed", "Humidity", "Temp", "AQI","AQI Type"])
        # Remove duplicate cities
        df_unique = df.drop_duplicates(subset='City')

        df_sorted = df_unique.sort_values('AQI', ascending=False)

        top_polluted_cities = df_sorted.head(10)

        fig = go.Figure(data=[go.Bar(x=top_polluted_cities['City'], y=top_polluted_cities['AQI'],marker=dict(color='red'),text=top_polluted_cities['AQI'],textposition='auto')])
        fig.update_layout(
            title='Top 10 Polluted Cities',
            xaxis=dict(title='City'),
            yaxis=dict(title='AQI'),
        )
        pio.write_image(fig, 'sample_plot.jpg', format="jpeg")
        return send_file('sample_plot.jpg', mimetype='image/jpeg')
    elif(inputchr=="Delhi"):
        url = "https://air-quality.com/place/india/delhi/fb9ff33b?lang=en&standard=naqi_in"
        response = requests.get(url)
        soup = BeautifulSoup(response.content, "html.parser")
        site_items = soup.find_all("a", class_="site-item")
        data = []
        def process_city_href(city_href):
            city_response = requests.get(city_href)
            city_soup = BeautifulSoup(city_response.content, "html.parser")

            # city name and state name
            city_name = city_soup.find("h2").text.strip()
            state_name = city_soup.find("p").text.strip().split(", ")[1]
            time = city_soup.find("div", class_="update-time").text.strip()
            aqi_comment = city_soup.find(string=lambda text: isinstance(text, Comment) and "indexValue" in text)
            aqi_value = float(re.search(r"\d+", aqi_comment).group()) if aqi_comment else np.NaN
            pollutants = city_soup.find_all("div", class_="pollutant-item")

            pollutant_data = {}
            for pollutant in pollutants:
                name = pollutant.find("div", class_="name").text.strip()
                value = pollutant.find("div", class_="value").text.strip()
                pollutant_data[name] = float(value) if value else np.NaN

            temperature = float(city_soup.find("div", class_="temperature").text.strip().replace("℃", "")) or np.NaN
            humidity = float(city_soup.find("div", class_="humidity").text.strip().replace("%", "")) or np.NaN
            wind_speed = float(city_soup.find("div", class_="wind").text.strip().replace("kph", "")) or np.NaN
            type = city_soup.find("div", class_="level").text.strip()
            type=type.replace("Moderately polluted", "Moderate")
            data.append([time,state_name, city_name,pollutant_data.get("PM2.5"), pollutant_data.get("PM10"), pollutant_data.get("O3"),pollutant_data.get("SO2"), pollutant_data.get("CO"),wind_speed, humidity, temperature, aqi_value,type])


        with ThreadPoolExecutor(max_workers=200) as executor:
            for site_item in site_items:
                state_href = site_item["href"]
                state_response = requests.get(state_href)
                state_soup = BeautifulSoup(state_response.content, "html.parser")
                all_city_hrefs = state_soup.find_all("a", class_="site-item")
                for city_href in all_city_hrefs:
                    city_href = city_href["href"]
                    if "https://air-quality.com/place/india" in city_href:
                        executor.submit(process_city_href, city_href)

        # Create a DataFrame from the collected data
        df = pd.DataFrame(data, columns=["Time","State", "City", "PM2.5", "PM10", "O3", "SO2", "CO", "Wind Speed", "Humidity", "Temp", "AQI","AQI Type"])
        # Remove duplicate cities
        df_unique = df.drop_duplicates(subset='City')

        df_sorted = df_unique.sort_values('AQI', ascending=False)

        top_polluted_cities = df_sorted.head(10)

        fig = go.Figure(data=[go.Bar(x=top_polluted_cities['City'], y=top_polluted_cities['AQI'],marker=dict(color='red'),text=top_polluted_cities['AQI'],textposition='auto')])
        fig.update_layout(
            title='Top 10 Polluted Cities',
            xaxis=dict(title='City'),
            yaxis=dict(title='AQI'),
        )
        pio.write_image(fig, 'sample_plot.jpg', format="jpeg")
        return send_file('sample_plot.jpg', mimetype='image/jpeg')
    elif(inputchr=="Banglore"):
        url = "https://air-quality.com/place/india/bengaluru/f8edf853?lang=en&standard=naqi_in"
        response = requests.get(url)
        soup = BeautifulSoup(response.content, "html.parser")
        site_items = soup.find_all("a", class_="site-item")
        data = []
        def process_city_href(city_href):
            city_response = requests.get(city_href)
            city_soup = BeautifulSoup(city_response.content, "html.parser")

            # city name and state name
            city_name = city_soup.find("h2").text.strip()
            state_name = city_soup.find("p").text.strip().split(", ")[1]
            time = city_soup.find("div", class_="update-time").text.strip()
            aqi_comment = city_soup.find(string=lambda text: isinstance(text, Comment) and "indexValue" in text)
            aqi_value = float(re.search(r"\d+", aqi_comment).group()) if aqi_comment else np.NaN
            pollutants = city_soup.find_all("div", class_="pollutant-item")

            pollutant_data = {}
            for pollutant in pollutants:
                name = pollutant.find("div", class_="name").text.strip()
                value = pollutant.find("div", class_="value").text.strip()
                pollutant_data[name] = float(value) if value else np.NaN

            temperature = float(city_soup.find("div", class_="temperature").text.strip().replace("℃", "")) or np.NaN
            humidity = float(city_soup.find("div", class_="humidity").text.strip().replace("%", "")) or np.NaN
            wind_speed = float(city_soup.find("div", class_="wind").text.strip().replace("kph", "")) or np.NaN
            type = city_soup.find("div", class_="level").text.strip()
            type=type.replace("Moderately polluted", "Moderate")
            data.append([time,state_name, city_name,pollutant_data.get("PM2.5"), pollutant_data.get("PM10"), pollutant_data.get("O3"),pollutant_data.get("SO2"), pollutant_data.get("CO"),wind_speed, humidity, temperature, aqi_value,type])


        with ThreadPoolExecutor(max_workers=200) as executor:
            for site_item in site_items:
                state_href = site_item["href"]
                state_response = requests.get(state_href)
                state_soup = BeautifulSoup(state_response.content, "html.parser")
                all_city_hrefs = state_soup.find_all("a", class_="site-item")
                for city_href in all_city_hrefs:
                    city_href = city_href["href"]
                    if "https://air-quality.com/place/india" in city_href:
                        executor.submit(process_city_href, city_href)

        # Create a DataFrame from the collected data
        df = pd.DataFrame(data, columns=["Time","State", "City", "PM2.5", "PM10", "O3", "SO2", "CO", "Wind Speed", "Humidity", "Temp", "AQI","AQI Type"])
        # Remove duplicate cities
        df_unique = df.drop_duplicates(subset='City')

        df_sorted = df_unique.sort_values('AQI', ascending=False)

        top_polluted_cities = df_sorted.head(10)

        fig = go.Figure(data=[go.Bar(x=top_polluted_cities['City'], y=top_polluted_cities['AQI'],marker=dict(color='red'),text=top_polluted_cities['AQI'],textposition='auto')])
        fig.update_layout(
            title='Top 10 Polluted Cities',
            xaxis=dict(title='City'),
            yaxis=dict(title='AQI'),
        )
        pio.write_image(fig, 'sample_plot.jpg', format="jpeg")
        return send_file('sample_plot.jpg', mimetype='image/jpeg')
    elif(inputchr=="Mumbai"):
        url = "https://air-quality.com/place/india/mumbai/6bf15df3?lang=en&standard=naqi_in"
        response = requests.get(url)
        soup = BeautifulSoup(response.content, "html.parser")
        site_items = soup.find_all("a", class_="site-item")
        data = []
        def process_city_href(city_href):
            city_response = requests.get(city_href)
            city_soup = BeautifulSoup(city_response.content, "html.parser")

            # city name and state name
            city_name = city_soup.find("h2").text.strip()
            state_name = city_soup.find("p").text.strip().split(", ")[1]
            time = city_soup.find("div", class_="update-time").text.strip()
            aqi_comment = city_soup.find(string=lambda text: isinstance(text, Comment) and "indexValue" in text)
            aqi_value = float(re.search(r"\d+", aqi_comment).group()) if aqi_comment else np.NaN
            pollutants = city_soup.find_all("div", class_="pollutant-item")

            pollutant_data = {}
            for pollutant in pollutants:
                name = pollutant.find("div", class_="name").text.strip()
                value = pollutant.find("div", class_="value").text.strip()
                pollutant_data[name] = float(value) if value else np.NaN

            temperature = float(city_soup.find("div", class_="temperature").text.strip().replace("℃", "")) or np.NaN
            humidity = float(city_soup.find("div", class_="humidity").text.strip().replace("%", "")) or np.NaN
            wind_speed = float(city_soup.find("div", class_="wind").text.strip().replace("kph", "")) or np.NaN
            type = city_soup.find("div", class_="level").text.strip()
            type=type.replace("Moderately polluted", "Moderate")
            data.append([time,state_name, city_name,pollutant_data.get("PM2.5"), pollutant_data.get("PM10"), pollutant_data.get("O3"),pollutant_data.get("SO2"), pollutant_data.get("CO"),wind_speed, humidity, temperature, aqi_value,type])


        with ThreadPoolExecutor(max_workers=200) as executor:
            for site_item in site_items:
                state_href = site_item["href"]
                state_response = requests.get(state_href)
                state_soup = BeautifulSoup(state_response.content, "html.parser")
                all_city_hrefs = state_soup.find_all("a", class_="site-item")
                for city_href in all_city_hrefs:
                    city_href = city_href["href"]
                    if "https://air-quality.com/place/india" in city_href:
                        executor.submit(process_city_href, city_href)

        # Create a DataFrame from the collected data
        df = pd.DataFrame(data, columns=["Time","State", "City", "PM2.5", "PM10", "O3", "SO2", "CO", "Wind Speed", "Humidity", "Temp", "AQI","AQI Type"])
        # Remove duplicate cities
        df_unique = df.drop_duplicates(subset='City')

        df_sorted = df_unique.sort_values('AQI', ascending=False)

        top_polluted_cities = df_sorted.head(10)

        fig = go.Figure(data=[go.Bar(x=top_polluted_cities['City'], y=top_polluted_cities['AQI'],marker=dict(color='red'),text=top_polluted_cities['AQI'],textposition='auto')])
        fig.update_layout(
            title='Top 10 Polluted Cities',
            xaxis=dict(title='City'),
            yaxis=dict(title='AQI'),
        )
        pio.write_image(fig, 'sample_plot.jpg', format="jpeg")
        return send_file('sample_plot.jpg', mimetype='image/jpeg')




@app.route('/plot', methods = ['GET'])
def returnplot():
    d = {}
    inputchr = str(request.args['query'])
    url = "https://air-quality.com/place/india/tamil-nadu/96b5533c?lang=en&standard=naqi_in"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    site_items = soup.find_all("a", class_="site-item")
    data = []
    def process_city_href(city_href):
        city_response = requests.get(city_href)
        city_soup = BeautifulSoup(city_response.content, "html.parser")

        # city name and state name
        city_name = city_soup.find("h2").text.strip()
        state_name = city_soup.find("p").text.strip().split(", ")[1]
        time = city_soup.find("div", class_="update-time").text.strip()
        aqi_comment = city_soup.find(string=lambda text: isinstance(text, Comment) and "indexValue" in text)
        aqi_value = float(re.search(r"\d+", aqi_comment).group()) if aqi_comment else np.NaN
        pollutants = city_soup.find_all("div", class_="pollutant-item")

        pollutant_data = {}
        for pollutant in pollutants:
            name = pollutant.find("div", class_="name").text.strip()
            value = pollutant.find("div", class_="value").text.strip()
            pollutant_data[name] = float(value) if value else np.NaN

        temperature = float(city_soup.find("div", class_="temperature").text.strip().replace("℃", "")) or np.NaN
        humidity = float(city_soup.find("div", class_="humidity").text.strip().replace("%", "")) or np.NaN
        wind_speed = float(city_soup.find("div", class_="wind").text.strip().replace("kph", "")) or np.NaN
        type = city_soup.find("div", class_="level").text.strip()
        type=type.replace("Moderately polluted", "Moderate")
        data.append([time,state_name, city_name,pollutant_data.get("PM2.5"), pollutant_data.get("PM10"), pollutant_data.get("O3"),pollutant_data.get("SO2"), pollutant_data.get("CO"),wind_speed, humidity, temperature, aqi_value,type])


    with ThreadPoolExecutor(max_workers=200) as executor:
        for site_item in site_items:
            state_href = site_item["href"]
            state_response = requests.get(state_href)
            state_soup = BeautifulSoup(state_response.content, "html.parser")
            all_city_hrefs = state_soup.find_all("a", class_="site-item")
            for city_href in all_city_hrefs:
                city_href = city_href["href"]
                if "https://air-quality.com/place/india" in city_href:
                    executor.submit(process_city_href, city_href)

    # Create a DataFrame from the collected data
    df = pd.DataFrame(data, columns=["Time","State", "City", "PM2.5", "PM10", "O3", "SO2", "CO", "Wind Speed", "Humidity", "Temp", "AQI","AQI Type"])
    # Remove duplicate cities
    df_unique = df.drop_duplicates(subset='City')

    df_sorted = df_unique.sort_values('AQI', ascending=False)

    top_polluted_cities = df_sorted.head(10)

    fig = go.Figure(data=[go.Bar(x=top_polluted_cities['City'], y=top_polluted_cities['AQI'],marker=dict(color='red'),text=top_polluted_cities['AQI'],textposition='auto')])
    fig.update_layout(
        title='Top 10 Polluted Cities',
        xaxis=dict(title='City'),
        yaxis=dict(title='AQI'),
    )
    pio.write_image(fig, 'sample_plot.jpg', format="jpeg")
    return send_file('sample_plot.jpg', mimetype='image/jpeg')

@app.route('/getcities', methods = ['GET'])
def returncities():
    d = {}
    inputchr = str(request.args['query'])
    url = "https://air-quality.com/place//204c2788?lang=en&standard=naqi_in"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    site_items = soup.find_all("a", class_="site-item")
    data = []
    def process_city_href(city_href):
        city_response = requests.get(city_href)
        city_soup = BeautifulSoup(city_response.content, "html.parser")

        # city name and state name
        city_name = city_soup.find("h2").text.strip()
        state_name = city_soup.find("p").text.strip().split(", ")[1]
        time = city_soup.find("div", class_="update-time").text.strip()
        aqi_comment = city_soup.find(string=lambda text: isinstance(text, Comment) and "indexValue" in text)
        aqi_value = float(re.search(r"\d+", aqi_comment).group()) if aqi_comment else np.NaN
        pollutants = city_soup.find_all("div", class_="pollutant-item")

        pollutant_data = {}
        for pollutant in pollutants:
            name = pollutant.find("div", class_="name").text.strip()
            value = pollutant.find("div", class_="value").text.strip()
            pollutant_data[name] = float(value) if value else np.NaN

        temperature = float(city_soup.find("div", class_="temperature").text.strip().replace("℃", "")) or np.NaN
        humidity = float(city_soup.find("div", class_="humidity").text.strip().replace("%", "")) or np.NaN
        wind_speed = float(city_soup.find("div", class_="wind").text.strip().replace("kph", "")) or np.NaN
        type = city_soup.find("div", class_="level").text.strip()
        type=type.replace("Moderately polluted", "Moderate")
        data.append([time,state_name, city_name,pollutant_data.get("PM2.5"), pollutant_data.get("PM10"), pollutant_data.get("O3"),pollutant_data.get("SO2"), pollutant_data.get("CO"),wind_speed, humidity, temperature, aqi_value,type])


    with ThreadPoolExecutor(max_workers=200) as executor:
        for site_item in site_items:
            state_href = site_item["href"]
            state_response = requests.get(state_href)
            state_soup = BeautifulSoup(state_response.content, "html.parser")
            all_city_hrefs = state_soup.find_all("a", class_="site-item")
            for city_href in all_city_hrefs:
                city_href = city_href["href"]
                if "https://air-quality.com/place/india" in city_href:
                    executor.submit(process_city_href, city_href)

    # Create a DataFrame from the collected data
    df = pd.DataFrame(data, columns=["Time","State", "City", "PM2.5", "PM10", "O3", "SO2", "CO", "Wind Speed", "Humidity", "Temp", "AQI","AQI Type"])
    # Remove duplicate cities
    df_unique = df.drop_duplicates(subset='City')

    df_sorted = df_unique.sort_values('AQI', ascending=False)

    top_polluted_cities = df_sorted.head(10)

    d['message'] = list(top_polluted_cities['City'])
    return d

@app.route('/goodplot', methods = ['GET'])
def returngoodplot():
    d = {}
    inputchr = str(request.args['query'])
    url = "https://air-quality.com/place/india/tamil-nadu/96b5533c?lang=en&standard=naqi_in"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    site_items = soup.find_all("a", class_="site-item")
    data = []
    def process_city_href(city_href):
        city_response = requests.get(city_href)
        city_soup = BeautifulSoup(city_response.content, "html.parser")

        # city name and state name
        city_name = city_soup.find("h2").text.strip()
        state_name = city_soup.find("p").text.strip().split(", ")[1]
        time = city_soup.find("div", class_="update-time").text.strip()
        aqi_comment = city_soup.find(string=lambda text: isinstance(text, Comment) and "indexValue" in text)
        aqi_value = float(re.search(r"\d+", aqi_comment).group()) if aqi_comment else np.NaN
        pollutants = city_soup.find_all("div", class_="pollutant-item")

        pollutant_data = {}
        for pollutant in pollutants:
            name = pollutant.find("div", class_="name").text.strip()
            value = pollutant.find("div", class_="value").text.strip()
            pollutant_data[name] = float(value) if value else np.NaN

        temperature = float(city_soup.find("div", class_="temperature").text.strip().replace("℃", "")) or np.NaN
        humidity = float(city_soup.find("div", class_="humidity").text.strip().replace("%", "")) or np.NaN
        wind_speed = float(city_soup.find("div", class_="wind").text.strip().replace("kph", "")) or np.NaN
        type = city_soup.find("div", class_="level").text.strip()
        type=type.replace("Moderately polluted", "Moderate")
        data.append([time,state_name, city_name,pollutant_data.get("PM2.5"), pollutant_data.get("PM10"), pollutant_data.get("O3"),pollutant_data.get("SO2"), pollutant_data.get("CO"),wind_speed, humidity, temperature, aqi_value,type])


    with ThreadPoolExecutor(max_workers=200) as executor:
        for site_item in site_items:
            state_href = site_item["href"]
            state_response = requests.get(state_href)
            state_soup = BeautifulSoup(state_response.content, "html.parser")
            all_city_hrefs = state_soup.find_all("a", class_="site-item")
            for city_href in all_city_hrefs:
                city_href = city_href["href"]
                if "https://air-quality.com/place/india" in city_href:
                    executor.submit(process_city_href, city_href)

    # Create a DataFrame from the collected data
    df = pd.DataFrame(data, columns=["Time","State", "City", "PM2.5", "PM10", "O3", "SO2", "CO", "Wind Speed", "Humidity", "Temp", "AQI","AQI Type"])
    # Remove duplicate cities
    df_unique = df.drop_duplicates(subset='City')

    df_sorted = df_unique.sort_values('AQI', ascending=False)

    top_cleansed_cities = df_sorted.tail(10)[::-1]

    fig = go.Figure(data=[go.Bar(x=top_cleansed_cities['City'], y=top_cleansed_cities['AQI'],marker=dict(color='green'),text=top_cleansed_cities['AQI'],textposition='auto')])
    fig.update_layout(
        title='Top 10 Cleansed Cities',
        xaxis=dict(title='City'),
        yaxis=dict(title='AQI'),
    )
    pio.write_image(fig, 'good_plot.jpg', format="jpeg")
    return send_file('good_plot.jpg', mimetype='image/jpeg')
# class HelloWorld(Resource):
#     def get(self):
#         d = {}
#         city_url="https://air-quality.com/place//204c2788?lang=en&standard=naqi_in"
#         city_response = requests.get(city_url)
#         city_soup = BeautifulSoup(city_response.content, "html.parser")
#         aqi_comment = city_soup.find(text=lambda text: isinstance(text, Comment) and "indexValue" in text)
#         aqi_value = re.search(r"\d+", aqi_comment).group() if aqi_comment else np.NaN
#         d['message'] = aqi_value
#         return d


# api.add_resource(HelloWorld, '/')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)
