import requests
from decouple import config

API_URL = config("API_URL")
TOKEN = config("TOKEN")
headers = {"Authorization": f"Bearer {TOKEN}"}

def query(filename):
    with open(filename, "rb") as f:
        data = f.read()
    response = requests.post(API_URL, headers=headers, data=data)
    return response.json()
