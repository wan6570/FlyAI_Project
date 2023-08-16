from flask import Flask, render_template, request
from distance import find_closest_player, scaler, scaled_df
from plot_radar_chart import plot_radar_chart
import numpy as np
from io import BytesIO
import base64

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    chart_url = None
    player_name = None

    if request.method == "POST":
        input_data = [
            float(request.form.get("GOLD%")),
            float(request.form.get("VS%")),
            float(request.form.get("DMG%")),
            float(request.form.get("KP%")),
            float(request.form.get("XPD@15"))
        ]
        
        scaled_input_data = scaler.transform([input_data])[0]
        player_name = find_closest_player(scaled_df, scaled_input_data[0], scaled_input_data[1], 
                              scaled_input_data[2], scaled_input_data[3], scaled_input_data[4])
        img = BytesIO()
        attributes = list(scaled_df.columns)
        
        image_data = plot_radar_chart(player_name, scaled_input_data, scaled_df, attributes)
        chart_url = base64.b64encode(image_data.getvalue()).decode('utf8')

    return render_template("index.html", chart_url=chart_url, player_name=player_name)

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=8080)
