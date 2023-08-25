import numpy as np 
import pandas as pd 
import matplotlib.pyplot as plt
from io import BytesIO
import base64

def plot(df,similar_player):
    labels = np.array(df['Feature'])
    stats_user = df['User'].values
    stats_player = df[similar_player].values

    angles = np.linspace(0, 2 * np.pi, len(labels), endpoint=False)
    stats_user = np.concatenate((stats_user, [stats_user[0]]))
    stats_player = np.concatenate((stats_player, [stats_player[0]]))
    angles = np.concatenate((angles, [angles[0]]))

    fig, ax = plt.subplots(figsize=(8, 6), subplot_kw=dict(polar=True))
    ax.plot(angles, stats_user, color='b', linewidth=2, label='User')
    ax.fill(angles, stats_user, color='b', alpha=0.25)
    ax.plot(angles, stats_player, color='r', linewidth=2, label=similar_player)
    ax.fill(angles, stats_player, color='r', alpha=0.25)
    ax.set_yticklabels([])
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(labels)
    ax.legend()

    img = BytesIO()
    plt.savefig(img, format='png')
    plt.close()
    img.seek(0)
    chart_url = base64.b64encode(img.getvalue()).decode('utf8')
    return chart_url