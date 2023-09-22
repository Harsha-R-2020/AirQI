import flask
from flask_restful import Resource, Api
import re
import requests
from bs4 import BeautifulSoup, Comment
import pandas as pd
import numpy as np
from flask import  request, jsonify

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
