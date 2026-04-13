import os
import random
from dotenv import load_dotenv
from flask import Flask, render_template, url_for, redirect, session, request, flash
from supabase import create_client, Client
import requests

load_dotenv()

# Grab keys from .env and Sets up connection to Supabase
url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_KEY")
supabase: Client = create_client(url, key)

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
def api_random():
    response = requests.get(
        "https://api.thedogapi.com/v1/breeds/",
        headers={"x-api-key": api_key}
    )

    if response.status_code != 200:
        return None, "Connection Error"

    data = response.json()
    if not data:
        return None, "Data Not Found"

    return sort_breed_data(random.choice(data)), None


def api_breed_search(breed):
    response = requests.get(
        "https://api.thedogapi.com/v1/breeds/search",
        headers={"x-api-key": api_key},
        params={"q": breed}
    )

    if response.status_code != 200:
        return None, "Connection Error"

    data = response.json()
    if not data:
        return None, "Data Not Found"

    return sort_breed_data(data[0]), None

def send_to_supabase(breed_data):
    response = (
        supabase.table("dog_breeds")
        .upsert(breed_data)
        .execute()
    )
    return response.data[0]

@app.route('/',)
def index():
    session["session_id"] = random.randint(10000, 99999)
    return redirect(url_for('home'))

@app.route('/home', methods=['GET', 'POST'])
def home():
    if not session.get("session_id"):
        return redirect(url_for('index'))
    if request.method == 'POST':
        breed = request.form['breed'].lower()
        response = (
            supabase.table("dog_breeds")
            .select("*")
            .ilike("name", f"%{breed}%")
            .execute()
        )
        if not response.data:
            data, error = api_breed_search(breed)
            if data:
                send_to_supabase(data)
                return redirect(url_for('breed', breed_id=data['id']))
            if not data:
                flash("Breed not found, please try again.")

    return render_template("index.html")

@app.route('/random', methods=['GET', 'POST'])
def random_breed():
    if not session.get("session_id"):
        return redirect(url_for('index'))
    data, error = api_random()
    if data:
        send_to_supabase(data)
        return redirect(url_for('breed', breed_id=data['id']))
    else:
        return None

app.route("/breed/<int:breed_id>")
def breed(breed_id):
    if not session.get("session_id"):
        return redirect(url_for('index'))
    response = supabase.table("dog_breeds").select("*").eq("id", breed_id).execute()
    if not response.data:
        log("Breed not found in Supabase for id: " + str(breed_id))
        return redirect(url_for('home'))
    data = response.data[0]
    log("User viewed breed: " + str(data.get('name')), session.get('session_id'))
    return render_template("result.html", breed=data)




@app.route('/health')
def health():
    try:
        supabase.table("dog_breeds").select("id").limit(1).execute()
        supabase_health = True
    except Exception:
        supabase_health = False

    try:
        response = requests.get(
            "https://api.thedogapi.com/v1/breeds?limit=1",
            headers={"x-api-key": api_key},
            timeout=3
        )
        api_health = response.status_code == 200
    except Exception:
        api_health = False

    overall = "working" if supabase_health and api_health else "degraded"

    return {"status": overall, "supabase": supabase_health, "dog_api": api_health}


@app.route('/status')
def status():
    if not session.get("session_id"):
        return redirect(url_for('index'))
    try:
        supabase.table("dog_breeds").select("*").limit(1).execute()
        supabase_status = "Working"
    except Exception:
        supabase_status = "Degraded"

    try:
        response = requests.get(
            "https://api.thedogapi.com/v1/breeds?limit=1",
            headers={"x-api-key": api_key},
            timeout=3
        )
        response.raise_for_status()
        api_status = "Working"
    except Exception:
        api_status = "Degraded"

    health = {
        "Supabase": supabase_status,
        "DogAPI": api_status
    }
    return render_template("health.html", health=health)


@app.route('/logs')
def logs():
    return 'Hello World!'

if __name__ == '__main__':
    app.run()
