import api, preprocessing, similar, gear, graph
import pymysql
from datetime import datetime
import pandas as pd 
import numpy as np

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


Line = 'TOP'
username = '장연석'


conn = get_db_connection()
cursor = conn.cursor()


char_user, GPM, VSPM, DPM, KP, XPD, tier, rank = api.getAPI(username,Line)
# 확인함
# print(char_user, GPM, VSPM, DPM, KP, XPD, tier, rank)

cursor.execute("SELECT GPM, VSPM, DPM, KP, XPD FROM usermeandata WHERE TIER = %s AND teamPosition = %s", (tier,Line,))
average_tier = cursor.fetchall()
GPM_user, VSPM_user, DPM_user, KP_user, XPD_user = preprocessing.normarization(average_tier, GPM, VSPM, DPM, KP, XPD)
#확인함
#print(GPM_user, VSPM_user, DPM_user, KP_user, XPD_user)

cursor.execute("SELECT * FROM pro_game_data WHERE Role = %s", (Line,))
players = cursor.fetchall()
similar_player, char_pro, GPM_pro, VSPM_pro, DPM_pro, KP_pro, XPD_pro = similar.pro_player(players, GPM, VSPM, DPM, KP, XPD)

#확인함
#print(similar_player, char_pro, GPM_pro, VSPM_pro, DPM_pro, KP_pro, XPD_pro)

data = {
    'Feature': ['GPM', 'VSPM', 'DPM', 'KP', 'XPD'],
    'User': [GPM_user, VSPM_user, DPM_user, KP_user, XPD_user],
    similar_player: [GPM_pro, VSPM_pro, DPM_pro, KP_pro, XPD_pro]
    }
plot_df = pd.DataFrame(data)
url = graph.plot(plot_df,similar_player)

#장비 가져오기 
cursor.execute("SELECT Mouse, Keyboard FROM gaming_gear WHERE Player = %s", (similar_player,))
gear_data = cursor.fetchone()

mouse = gear_data['Mouse']
keyboard = gear_data['Keyboard']

print(mouse, keyboard) 