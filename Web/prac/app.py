# app.py

# app.py
from urllib import parse
from flask import Flask, request, jsonify
import requests
from dotenv import load_dotenv
import os
from flask import render_template
from PIL import Image
from io import BytesIO

load_dotenv()

app = Flask(__name__)

# RIOT_API_KEY = os.getenv('RIOT_API_KEY')

with open('C:\\Users\\066\\Desktop\\FlyAI_Project\\API\\LeagueofLegends\\APIkey.txt', 'r', encoding='utf-8') as file:
    RIOT_API_KEY =file.readline()
        
@app.route('/')
def index():
    print(f"API KEY = {RIOT_API_KEY}")
    return 'Riot Games API Example'

@app.route('/summoner', methods=['GET'])
def get_summoner_info():
    username = request.args.get('summoner_name')
    if not username:
        return jsonify({'error': 'Summoner name is required'}), 400
    print(username)
    id = parse.quote(username)
    url = f'https://kr.api.riotgames.com/lol/summoner/v4/summoners/by-name/{id}?api_key={RIOT_API_KEY}'

    response = requests.get(url)

    if response.status_code == 200:
        summoner_data = response.json()
        profile=summoner_data['profileIconId']
        url=f'https://ddragon.leagueoflegends.com/cdn/13.16.1/img/profileicon/{profile}.png'
        # response = requests.get(url)
        # request_get_img = Image.open(BytesIO(response.content))
        return render_template('index.html',profile_url=url)
    elif response.status_code == 404:
        return jsonify({'error': 'Summoner not found'}), 404
    else:
        return jsonify({'error': 'An error occurred'}), 500

if __name__ == '__main__':
    app.run(debug=True)
