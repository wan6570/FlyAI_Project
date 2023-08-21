# app.py

# app.py

from flask import Flask, request, jsonify
import requests
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)

RIOT_API_KEY = os.getenv('RIOT_API_KEY')

@app.route('/')
def index():
    print(f"API KEY = {RIOT_API_KEY}")
    return 'Riot Games API Example'

@app.route('/summoner', methods=['GET'])
def get_summoner_info():
    summoner_name = request.args.get('summoner_name')
    if not summoner_name:
        return jsonify({'error': 'Summoner name is required'}), 400

    url = f'https://na1.api.riotgames.com/lol/summoner/v4/summoners/by-name/{summoner_name}'
    headers = {'X-Riot-Token': RIOT_API_KEY}

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        summoner_data = response.json()
        return jsonify(summoner_data)
    elif response.status_code == 404:
        return jsonify({'error': 'Summoner not found'}), 404
    else:
        return jsonify({'error': 'An error occurred'}), 500

if __name__ == '__main__':
    app.run(debug=True)
