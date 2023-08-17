from flask import Flask, render_template, request, redirect, url_for
import pymysql

app = Flask(__name__)

def get_connection():
    return pymysql.connect(
        host='azure 주소',
        user='minseok',
        password='비밀번호',
        db='데이터베이스 이름',
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor,
        ssl={'ca': "인증키"},
        ssl_disabled=False
    )

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        name = request.form['name']
        mbti = request.form['mbti']

        connection = get_connection()
        try:
            with connection.cursor() as cursor:
                sql = "INSERT INTO `new_table` (`Name`, `Mbti`) VALUES (%s, %s)"
                cursor.execute(sql, (name, mbti))
            connection.commit()
        finally:
            connection.close()
        return redirect(url_for('thank_you'))
    return render_template('index.html')

@app.route('/thank_you')
def thank_you():
    return 'Thank you for submitting your information!'

if __name__ == '__main__':
    app.run(debug=True)
