import pandas as pd
import requests
from urllib import parse

col_list=[]
username=''
with open('APIcols.txt', 'r', encoding='utf-8') as file:
    for line in file:
        col_list.append(line.strip()) 

def preprocessing(df,r_timeline,col_list=col_list):
    df['timePlayed']=df['timePlayed']/60
    df1=df[df['summonerName']==username]
    df1['Player']=username
    df1['KDA 0.5']=(df1['kills']+df1['assists'])/(df1['deaths']+0.5)

    df1['CSM']=df1['totalMinionsKilled']/df1['timePlayed']

    df1['GPM']=df1['goldEarned']/df1['timePlayed']

    df1['VSPM']=df1['visionScore']/df1['timePlayed']
    df1['WPM']=df1['wardsPlaced']/df1['timePlayed']
    df1['VWPM']=df1['detectorWardsPlaced']/df1['timePlayed']
    df1['WCPM']=df1['wardsKilled']/df1['timePlayed']

    df1['DPM']=df1['totalDamageDealtToChampions']/df1['timePlayed']

    df1['K+A Per Minute']=(df1['kills']+df1['assists'])/df1['timePlayed']

    #이건 생략
    #  df1['Shutdown bounty collected']
    #  df1['Shutdown bounty lost']
    #  df1['Solo kills']=

    #timeline지표들
    usernum=str(df1['participantId'].iloc[0])
    oppnum=str((int(usernum)+4)%10+1)
    df1['GD@15']=r_timeline['info']['frames'][15]['participantFrames'][usernum]['totalGold']

    df1['CSD@15']=r_timeline['info']['frames'][15]['participantFrames'][usernum]['minionsKilled']

    df1['XPD']=r_timeline['info']['frames'][15]['participantFrames'][usernum]['xp']

    df1['LVLD@15']=r_timeline['info']['frames'][15]['participantFrames'][usernum]['level']-r_timeline['info']['frames'][15]['participantFrames'][oppnum]['level']#,'minionsKilled','xp']

    # %지표들

    df1['GOLD ratio']=df1['goldEarned']/df[df['teamId']==int(df1['teamId'])]['goldEarned'].sum(axis=0)*100
    df1['VS ratio']=df1['visionScore']/df[df['teamId']==int(df1['teamId'])]['visionScore'].sum(axis=0)*100
    df1['DMG ratio']=df1['totalDamageDealtToChampions']/df[df['teamId']==int(df1['teamId'])]['totalDamageDealtToChampions'].sum(axis=0)*100
    df1['KP']=(df1['kills']+df1['assists'])/df[df['teamId']==int(df1['teamId'])]['kills'].sum(axis=0)*100

    return df1[col_list]

def getAPI(name,Line):

    if(Line == 'MID'):
        Line = 'MIDDLE'
    if(Line == 'ADC'):
        Line = 'BOTTOM'
    if(Line == 'SUPPORT'):
        Line = 'UTILITY'
    

    N=10
    global username
    username=name
    with open('APIkey.txt', 'r', encoding='utf-8') as file:
        apiKey=file.readline()
    #username = '장연석'

    id = parse.quote(username) # 아이디를 URL 인코딩

    url = 'https://kr.api.riotgames.com/lol/summoner/v4/summoners/by-name/' + id +'?api_key=' + apiKey #puuid값을 가져오기 위한 주소
    r = requests.get(url)
    r = r.json()

    puuid = r['puuid'] # puuid값을 가져옴
    iconnum=r['profileIconId']
    tierUrl=f"https://kr.api.riotgames.com/lol/league/v4/entries/by-summoner/{r['id']}?api_key="+apiKey
    tier_data = requests.get(tierUrl)
    # print('-------------------------------------------')
    # print(tier_data.json())
    # print('-------------------------------------------')
    tier_data = [item for item in tier_data.json() if item['queueType'] == 'RANKED_SOLO_5x5']
    tier_data = tier_data[0]
    # print('-------------------------------------------')
    # print(tier_data)
    # print('-------------------------------------------')
    tier = tier_data['tier']
    rank = tier_data['rank']
    

    n = str(N)
    rankUrl = 'https://asia.api.riotgames.com/lol/match/v5/matches/by-puuid/' + puuid + '/ids?queue=420&type=ranked&start=0&count='+n+'&api_key='+ apiKey
    r = requests.get(rankUrl)
    r = r.json()
    
    rankId = r

    df_final=pd.DataFrame()
    for i in rankId:
        url = 'https://asia.api.riotgames.com/lol/match/v5/matches/' + i + '?api_key=' + apiKey
        r = requests.get(url)
        r = r.json()
        info = r['info']  # 전체 데이터에서 info를 추출
        part = info['participants'] # info 데이터에서 유저들의 정보 추출
        df= pd.DataFrame(part)
        url_timeline = f'https://asia.api.riotgames.com/lol/match/v5/matches/{i}/timeline?api_key={apiKey}'
        r_timeline=requests.get(url_timeline)
        r_timeline=r_timeline.json()
        if df['timePlayed'].iloc[0]<900:
            continue
        df_final=pd.concat([df_final,preprocessing(df,r_timeline)])
        df_final = df_final.reset_index(drop=True)
    
    df_line = df_final[df_final['teamPosition'] == Line]
    print('-------------------------------------------')
    print(f'TeamPosition : {df_final["teamPosition"]}, Line : {Line}')
    print(df_line['championName'].value_counts())
    print('-------------------------------------------')
    char = df_line['championName'].value_counts().idxmax()
    df_line = df_line[df_line['win'] == True]
    
    averages = df_line[['GPM', 'VSPM', 'DPM', 'KP', 'XPD']].mean()
    GPM = averages['GPM']
    VSPM = averages['VSPM']
    DPM = averages['DPM']
    KP = averages['KP']
    XPD = averages['XPD']
    return char, GPM, VSPM, DPM, KP, XPD, tier, rank, iconnum
