from flask import Flask
import mysql.connector

app = Flask(__name__)

# 配置数据库连接
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'admin'
app.config['MYSQL_DB'] = 'how2java'


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
    cursor.execute('SELECT * FROM category_')
    results = cursor.fetchall()
    cursor.close()
    db.close()
    return str(results)


if __name__ == '__main__':
    app.run()