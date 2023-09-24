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
import plotly.io as pio

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
