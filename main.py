from flask import Flask, request, jsonify
import mysql.connector
import logging

app = Flask(__name__)

# 配置数据库连接
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'admin'
app.config['MYSQL_DB'] = 'notebook'

# 配置日志
app.logger.setLevel(logging.DEBUG)  # 设置日志级别


# 定义一个装饰器来检查参数是否必须携带
def validate(**kwargs):
    def decorator(f):
        def decorated_function(*args, **kwargs):
            # 遍历参数字典，检查每个参数是否在请求中存在
            for param_name, required in kwargs.items():
                if required and param_name not in request.args:
                    return jsonify({"error": f"{param_name} is missing"}), 400
            return f(*args, **kwargs)

        return decorated_function

    return decorator


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
@app.route('/all_notes')
def index():
    db = get_db_connection()
    cursor = db.cursor()
    cursor.execute('SELECT title, category FROM notes')
    results = cursor.fetchall()

    cursor.close()
    db.close()

    return jsonify({"message": 'Query notes successfully!', "content": f'{results}'}), 200


# 使用数据库连接
@app.route('/all_cate')
def all_cate():
    db = get_db_connection()
    cursor = db.cursor()
    cursor.execute('SELECT DISTINCT  category FROM notes')
    results = cursor.fetchall()

    cursor.close()
    db.close()

    return jsonify({"message": 'Query categories successfully!', "categories": f'{results}'}), 200


# 使用数据库连接
@app.route('/note_content/<title>')
def index2(title):
    db = get_db_connection()
    cursor = db.cursor()
    cursor.execute('SELECT content FROM notes where title = %s', (title,))
    results = cursor.fetchall()

    cursor.close()
    db.close()
    data = str(results[0][0]) if results.__len__() > 0 else ""
    if results.__len__() > 0:
        return jsonify({"message": 'Query content successfully!', "content": f'{data}'}), 200
    else:
        return jsonify({"message": 'No note are found!', "content": f'{data}'}), 200


@app.route('/insert', methods=['POST'])
def insert_data():
    try:
        title = request.form['title']
    except KeyError:
        return jsonify({"error": "Param {title} is missing"}), 400

    try:
        content = request.form['content']
    except KeyError:
        return jsonify({"error": "Param {content} is missing"}), 400
    if request.form.get('category'):
        category = request.form['category']
    else:
        category = "默认分类"

    from datetime import datetime

    # 获取当前时间
    now = datetime.now()

    # 设置指定的年月日时分秒
    specified_time = datetime(2025, 5, 12, 22, 0, 0)

    # 格式化时间戳
    formatted_time = now.strftime('%Y-%m-%d %H:%M:%S')

    db = get_db_connection()
    cursor = db.cursor()
    # cursor.execute("INSERT INTO notes (title, content, category, created_time) VALUES (%s, %s, %s, %s)", ("John",
    # "john@example.com", "默认", "2024-05-12"))
    cursor.execute("INSERT INTO notes (title, content, category, created_time) VALUES (%s, %s, %s, %s)",
                   (title, content, category, formatted_time))
    db.commit()
    # return 'Data inserted successfully!'
    return jsonify({"message": 'Data inserted successfully!'}), 200


if __name__ == '__main__':
    # app.run()
    # db.create_all()
    app.run(port=8888, debug=True, host='127.0.0.1')  # 启动服务
