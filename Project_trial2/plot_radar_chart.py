import numpy as np
import matplotlib.pyplot as plt
import matplotlib
import io 
from io import BytesIO

def plot_radar_chart(player_name, scaled_input_data, scaled_df, attributes):
    plt.clf()  # 그래프 출력 버퍼 지우기
    
    # 데이터 추출
    player_values = scaled_df.loc[player_name].tolist()
    input_values = scaled_input_data.tolist()

    # 데이터가 원을 이루도록 처리
    player_values += player_values[:1]
    input_values += input_values[:1]

    # 변수 및 라벨 설정
    num_vars = len(attributes)
    
    # 각도 계산
    angles = np.linspace(0, 2 * np.pi, num_vars, endpoint=False).tolist()
    angles += angles[:1]

    # 그래프 그리기
    fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(polar=True))
    ax.plot(angles, input_values, color='blue', linewidth=2, label="Input Data")
    ax.fill(angles, input_values, color='blue', alpha=0.25)
    ax.plot(angles, player_values, color='red', linewidth=2, label=player_name)
    ax.fill(angles, player_values, color='red', alpha=0.25)

    # 그래프 형식 설정
    ax.set_yticklabels([])  # y 축 레이블 제거
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(attributes)
    ax.set_title(f"Radar Chart Comparison: Input Data vs. {player_name}")
    ax.legend(loc="upper right", bbox_to_anchor=(1.1, 1.1))
    
    img = BytesIO()
    plt.savefig(img, format='png')
    plt.close()
    
    img.seek(0)
    return img
