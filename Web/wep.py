from flask import Flask, request, jsonify
from flask_mysqldb import MySQL

app = Flask(__name__)

# MySQL 설정
app.config['MYSQL_HOST'] = 'your_mysql_host'
app.config['MYSQL_USER'] = 'your_mysql_user'
app.config['MYSQL_PASSWORD'] = 'your_mysql_password'
app.config['MYSQL_DB'] = 'your_database_name'

mysql = MySQL(app)

@app.route('/get_meaning', methods=['POST'])
def get_meaning():
    word = request.json.get('word')

    if word:
        cur = mysql.connection.cursor()
        query = f"SELECT meaning FROM words WHERE word = %s"
        cur.execute(query, (word,))
        meaning = cur.fetchone()

        if meaning:
            return jsonify({"word": word, "meaning": meaning[0]})
        else:
            return jsonify({"error": "Word not found"}), 404
    else:
        return jsonify({"error": "Word parameter is missing"}), 400

if __name__ == '__main__':
    app.run(debug=True)