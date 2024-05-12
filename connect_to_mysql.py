from flask import Flask, request
import mysql.connector
from flask_sqlalchemy import SQLAlchemy
import pymysql
from datetime import datetime
app = Flask(__name__)

# 配置数据库连接
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'admin'
app.config['MYSQL_DB'] = 'notebook'


# 创建数据库连接
def get_db_connection():
    db = mysql.connector.connect(
        host=app.config['MYSQL_HOST'],
        user=app.config['MYSQL_USER'],
        password=app.config['MYSQL_PASSWORD'],
        database=app.config['MYSQL_DB']
    )
    return db


# 使用数据库连接
@app.route('/')
def index():
    db = get_db_connection()
    cursor = db.cursor()
    cursor.execute('SELECT * FROM notes')
    results = cursor.fetchall()

    cursor.close()
    db.close()
    return str(results)

@app.route('/insert', methods=['POST'])
def insert_data():
    title = request.form['title']
    content = request.form['content']
    category = request.form['category']

    from datetime import datetime

    # 获取当前时间
    now = datetime.now()

    # 设置指定的年月日时分秒
    specified_time = datetime(2025, 5, 12, 22, 0, 0)

    # 格式化时间戳
    formatted_time = now.strftime('%Y-%m-%d %H:%M:%S')

    print(formatted_time)
    db = get_db_connection()
    cursor = db.cursor()
    # cursor.execute("INSERT INTO notes (title, content, category, created_time) VALUES (%s, %s, %s, %s)", ("John", "john@example.com", "默认", "2024-05-12"))
    cursor.execute("INSERT INTO notes (title, content, category, created_time) VALUES (%s, %s, %s, %s)", (title, content, category, formatted_time))
    db.commit()
    return 'Data inserted successfully!'


if __name__ == '__main__':
    # app.run()
    # db.create_all()
    app.run(port=8888, debug=True, host='127.0.0.1')  # 启动服务