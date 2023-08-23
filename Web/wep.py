from flask import Flask, request, jsonify
from flask_mysqldb import MySQL

app = Flask(__name__)

# MySQL 설정
app.config['MYSQL_HOST'] = 'cdymysql.mysql.database.azure.com'
app.config['MYSQL_USER'] = 'minseok'
app.config['MYSQL_PASSWORD'] = '1234!@#$'
app.config['MYSQL_DB'] = 'testdb'

mysql = MySQL(app)

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM account WHERE username = %s", (username,))
        account = cursor.fetchone()
        cursor.close()

        if account and account['password'] == password:
            session['logged_in'] = True
            session['username'] = username
            return redirect(url_for('dashboard'))
        else:
            return 'Invalid login credentials'

    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if 'logged_in' in session:
        return f'Hello, {session["username"]}! Welcome to the dashboard.'
    else:
        return redirect(url_for('login'))

if __name__ == '__main__':
    app.run()

if __name__ == '__main__':
    app.run(debug=True)