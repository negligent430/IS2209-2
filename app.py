import os
from dotenv import load_dotenv
from flask import Flask, render_template
from supabase import create_client, Client
import requests

load_dotenv()

# Grab keys from .env and Sets up connection to Supabase
url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_KEY")
supabase: Client = create_client(url, key)

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
