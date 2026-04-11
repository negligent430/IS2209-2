import os
from dotenv import load_dotenv
from flask import Flask, render_template
import requests

load_dotenv()

app = Flask(__name__)

api_key = os.getenv("DOG_API")
url = "https://api.thedogapi.com/v1/images/search"


@app.route('/')
def hello_world():
    response = requests.get(url, headers={"x-api-key": api_key})
    if response.status_code == 200:
        data = response.json()
        print(data)


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
