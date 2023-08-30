# !!!
import api, preprocessing, similar, gear, graph, text
from flask import Flask, render_template, request, redirect, url_for
import pymysql
from datetime import datetime
import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt
import io 
from io import BytesIO
import base64
import traceback


app = Flask(__name__)

def get_db_connection():
    return pymysql.connect(
        host='minseok.mysql.database.azure.com',
        user='minseok',
        password='seok9745@@',
        db='project',
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor,
        ssl={'ca': "./DigiCertGlobalRootCA.crt.pem"},
        ssl_disabled=False
    )


#첫 화면
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        Line = request.form.get('Line')
        username = request.form.get('username')
        conn = get_db_connection()
        cursor = conn.cursor()

        if username == 'hide on bush':
            username = 'Hide on bush'

        try:
            #user의 플레이 정보 불러오기
            char_user, GPM, VSPM, DPM, KP, XPD, tier, rank, iconnum = api.getAPI(username,Line)

            icon_url = "https://ddragon.leagueoflegends.com/cdn/13.16.1/img/profileicon/{}.png".format(iconnum)

            #입력 데이터 전처리 
            cursor.execute("SELECT GPM, VSPM, DPM, KP, XPD FROM usermeandata WHERE TIER = %s AND teamPosition = %s", (tier,Line,))
            average_tier = cursor.fetchall()
            print('-------------------------------------------')
            print(f'GPM: {GPM}, VSPM: {VSPM}, DPM: {DPM}, KP: {KP}, XPD: {XPD}')
            GPM_user, VSPM_user, DPM_user, KP_user, XPD_user = preprocessing.normarization(average_tier, GPM, VSPM, DPM, KP, XPD)
            print(f'GPM_user : {GPM_user}, VSPM_user : {VSPM_user}, DPM_user : {DPM_user}, KP_user : {KP_user}, XPD_user : {XPD_user}')
            print('-------------------------------------------')
            #프로 선수 데이터 DB에서 가져오기
            DB_Line = Line

            cursor.execute("SELECT * FROM pro_game_data WHERE Role = %s", (DB_Line,))
            players = cursor.fetchall()
            similar_player, char_pro, GPM_pro, VSPM_pro, DPM_pro, KP_pro, XPD_pro = similar.pro_player(players, GPM_user, VSPM_user, DPM_user, KP_user, XPD_user)

            print('-------------------------------------------')
            print(f'similar_player : {similar_player}, char_pro : {char_pro}, GPM_pro : {GPM_pro}, VSPM_pro : {VSPM_pro}, DPM_pro : {DPM_pro}, KP_pro : {KP_pro}, XPD_pro : {XPD_pro}')
            print('-------------------------------------------')

            # 프로 선수 이미지 불러오기 
            cursor.execute("SELECT image_data FROM playerimages WHERE filename = %s", (similar_player,))
            result_pro = cursor.fetchone()

            image_data = result_pro['image_data']
            pro_image_data = base64.b64encode(image_data).decode('utf-8')

            #그래프 그리기 
            data = {
            'Feature': ['GPM', 'VSPM', 'DPM', 'KP', 'XPD'],
            'Feature1':['Growth','Vision','Damage','Influence','LineBattle'],
            'User': [GPM_user, VSPM_user, DPM_user, KP_user, XPD_user],
            similar_player: [GPM_pro, VSPM_pro, DPM_pro, KP_pro, XPD_pro]
            }
            plot_df = pd.DataFrame(data)
            url = graph.plot(plot_df,similar_player)

            #텍스트 가져오기 
            # 1. 비슷한 두 특성 가져오기 
            similar_template = "당신의 플레이 스타일은 {} 선수와 {} 지표와 {} 지표에서 유사한 수준으로 나왔습니다."
            similar_feature = text.which_feature_similar(data ,similar_player, min_count=2)
            similar_feature_text = similar_template.format(similar_player, similar_feature[0], similar_feature[1])

            # 2. 강점, 약점 가져오기 
            strength_template = "{}티어 {} 포지션 사람들의 평균과 당신의 플레이를 비교했을 때, 당신은 ['{}'] 지표에서 강점을 보이고 있습니다."
            weakness_template = "{}티어 {} 포지션 사람들의 평균과 당신의 플레이를 비교했을 때, 당신은 ['{}'] 지표에서 약점을 보이고 있습니다."
            strength, weakness = text.min_max_feature(data)
            strength_text = strength_template.format(tier, Line, strength)
            weakness_text = weakness_template.format(tier, Line, weakness)

            #장비 가져오기 
            cursor.execute("SELECT Mouse, Keyboard FROM gaming_gear WHERE Player = %s", (similar_player,))
            gear_data = cursor.fetchone()

            mouse = gear_data['Mouse']
            keyboard = gear_data['Keyboard']


            #장비 이미지 가져오기 
            cursor.execute("SELECT image_data FROM gaming_gear_images WHERE filename = %s", (mouse,))
            result_mouse = cursor.fetchone()
            image_data_mouse = result_mouse['image_data']
            mouse_image_data = base64.b64encode(image_data_mouse).decode('utf-8')

            cursor.execute("SELECT image_data FROM gaming_gear_images WHERE filename = %s", (keyboard,))
            result_keyboard = cursor.fetchone()
            image_data_keyboard = result_keyboard['image_data']
            keyboard_image_data = base64.b64encode(image_data_keyboard).decode('utf-8')


            #DB 저장 
            query = """INSERT INTO table3 (username, Line, char_user, similar_player, time) VALUES (%s, %s, %s, %s, %s)"""
            cursor.execute(query, (username, Line, char_user, similar_player,datetime.now()))

            conn.commit()
            cursor.close()
            conn.close()

            return render_template("result.html",
                            Line=Line,
                            username=username,
                            char_user=char_user,
                            char_pro = char_pro,
                            similar_player= similar_player,
                            url = url, mouse = mouse, keyboard = keyboard, 
                            tier = tier, rank = rank, icon_url = icon_url,
                            similar_feature_text = similar_feature_text,
                            strength_text = strength_text, weakness_text = weakness_text,
                            pro_image_data = pro_image_data,mouse_image_data= mouse_image_data,
                            keyboard_image_data = keyboard_image_data)
        except Exception as e:
            error_message = traceback.format_exc()
            query = 'INSERT INTO errors (player_name, error_message) VALUES (%s, %s)'
            cursor.execute(query, (username, error_message))
            conn.commit()
            cursor.close()
            conn.close()

            if isinstance(e, KeyError) and 'puuid' in str(e):
                return "API key is expired. Please change your API key." 
            
            return f'Bad Request occured. Please check your input.'

    return render_template('index.html')




@app.route("/result", methods=["POST"])
def result():
    Line = request.args.get('Line', default="", type=str)
    username = request.args.get('username', default="", type=str)
    char_user = request.args.get('char_user', default="", type=str)
    char_pro = request.args.get('char_pro', default="", type=str)
    similar_player = request.args.get('similar_player', default="", type=str)
    mouse = request.args.get('mouse', default="", type=str)
    keyboard = request.args.get('keyboard', default="", type=str)
    url = request.args.get('url', default="", type=str)
    tier = request.args.get('tier', default="", type=str)
    rank = request.args.get('rank', default="", type=str)
    icon_url = request.args.get('icon_url', default="", type=str)
    similar_feature_text = request.args.get('similar_feature_text', default="", type=str)
    strength_text = request.args.get('strength_text', default="", type=str)
    weakness_text = request.args.get('weakness_text', default="", type=str)
    pro_image_data = request.args.get('pro_image_data', default="", type=str)
    keyboard_image_data = request.args.get('keyboard_image_data ', default="", type=str)
    mouse_image_data= request.args.get('mouse_image_data', default="", type=str)
    


    return render_template("result.html", Line=Line,
                        username=username,
                        char_user=char_user,
                        char_pro = char_pro,
                        similar_player= similar_player,
                        url = url, mouse = mouse, keyboard = keyboard,
                        tier = tier, rank = rank, icon_url = icon_url,
                        similar_feature_text=similar_feature_text,
                        strength_text = strength_text, weakness_text = weakness_text,
                        pro_image_data = pro_image_data,keyboard_image_data = keyboard_image_data,
                        mouse_image_data = mouse_image_data)


if __name__ == "__main__":
    app.run(debug=True)


