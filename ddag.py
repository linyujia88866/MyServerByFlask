from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)


# 【1】注释以下两行后可能会报错： RuntimeError: Either 'SQLALCHEMY_DATABASE_URI' or 'SQLALCHEMY_BINDS' must be set.
app_ctx = app.app_context()
app_ctx.push()

class BaseConfig():
    DEBUG = True
    # 获取项目目录
    APP_PATH = os.path.dirname(__file__)
    # sqlite数据库url
    SQLALCHEMY_DATABASE_URI = f'sqlite:///{APP_PATH}/database'


app.config.from_object(BaseConfig)

# 创建数据库连接，管理项目
db = SQLAlchemy(app)


class User(db.Model):  # 模型类继承db.Model
    """创建User表"""
    #  SQLAlchemy 需要手动执行主键列，第一个参数是 字段类型，第二个参数是约束条件


    id = db.Column(db.INTEGER, primary_key=True)
    username = db.Column(db.String(50))
    password = db.Column(db.String(40))
# 【2】若想增加一个字段，run之后并没有加入表中，可以先删除表，再run,然后刷新即可加入（因为该表已存在，不会重新创建表了）
# desc = db.Column(db.String(40))

if __name__ == '__main__':
    # 【3】删除所有表，注意这条是危险命令，会将模型类对应数据库中的表物理删除。在实际生产环境下勿用。
    # db.drop_all()
    db.create_all()  # 创建所有的表
