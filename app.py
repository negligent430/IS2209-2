import os
import random
from cmath import log

from dotenv import load_dotenv
from flask import Flask, render_template, url_for, redirect, session
import requests

load_dotenv()

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY")
api_key = os.getenv("DOG_API")

def sort_breed_data(data):
    return {
        "id": data.get("id"),
        "name": data.get("name"),
        "life_span": data.get("life_span"),
        "temperament": data.get("temperament"),
        "origin": data.get("origin"),
        "country_code": data.get("country_code"),
        "description": data.get("description"),
        "history": data.get("history"),
        "weight": data.get("weight", {}).get("metric"),
        "height": data.get("height", {}).get("metric"),
        "image_url": data.get("image", {}).get("url"),
    }



def api_breed_search(breed):
    response = requests.get(
        "https://api.thedogapi.com/v1/breeds/search",
        headers={"x-api-key": api_key},
        params={"q": breed}
    )

    if response.status_code != 200:
        log("API connection error when searching for: " + breed)
        return None, "Connection Error"

    data = response.json()
    if not data:
        log("API returned no data for: " + breed)
        return None, "Data Not Found"

    return sort_breed_data(data[0]), None

@app.route('/',)
def index():
    session["session_id"] = random.randint(10000, 99999)
    return redirect(url_for('home'))


@app.route('/result')
def result():
    return 'Hello World!'

@app.route('/health')
def health():
    return 'Hello World!'

@app.route('/status')
def status():
    return 'Hello World!'

@app.route('/logs')
def logs():
    return 'Hello World!'


if __name__ == '__main__':
    app.run()
