import numpy as np
import pandas as pd

def which_feature_similar(data, similar_player, min_count=2):
    return_texts = []
    

    dictionary = {
        "GPM": "성장",
        "VSPM": "시야",
        "DPM": "데미지",
        "KP": "영향력",
        "XPD": "라인전"
    }
    # 프로 선수와 유저와 수치 차이의 절대값
    np_user = np.array(data['User'])
    np_pro = np.array(data[similar_player])

    np_diff = np.abs(np_user - np_pro).round(2)
    
    # 차이값이 가장 작은 2개의 특성의 인덱스를 가져옵니다.
    min_indices = np.argsort(np_diff)[:min_count]
    
    # 먼저 2개의 특성을 결과에 추가합니다.
    for idx in min_indices:
        return_texts.append([dictionary[data['Feature'][idx]]])

    return return_texts
# [['영향력', 0.33], ['시야', 0.42]] 결과가 리턴됨 





def min_max_feature(data):
    np_user = np.array(data['User'])
    dictionary = {
        "GPM": "성장",
        "VSPM": "시야",
        "DPM": "데미지",
        "KP": "영향력",
        "XPD": "라인전"
    }
    strength = dictionary[data['Feature'][np.argmax(np_user)]]
    weakness = dictionary[data['Feature'][np.argmin(np_user)]]
    return strength, weakness



#[['데미지', 1.11], ['영향력', 0.86]]