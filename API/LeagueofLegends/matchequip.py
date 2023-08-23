import pymysql
import pandas as pd

def equip(proname,connection):
    proname='Canna'
    sql_query = f"SELECT * FROM equip WHERE Player='{proname}';"

    df = pd.read_sql(sql_query, connection)

    # 데이터프레임 출력
    return df

