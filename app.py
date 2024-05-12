from flask import Flask, jsonify, request

app = Flask(__name__)


@app.route('/')
def index():
    return "服务运行中..."


@app.route('/api/greet', methods=['GET'])
def greet():
    name = request.args.get('name')
    return jsonify(message=f"Hello, {name}!")


if __name__ == '__main__':
    app.run(debug=True)