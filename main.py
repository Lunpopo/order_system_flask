"""
flask启动文件
"""
from gevent import monkey
monkey.patch_all()  # 替换标准socket模块的函数和类，改成异步非阻塞

# 将python标准的io方法，都替换成gevent中同名的方法，遇到io阻塞gevent自动进行协程切换
from app_router import create_app


# 原始的注册方式
# if __name__ == '__main__':
#     CORS(app, supports_credentials=True)
#     app.config.from_object(flask_config)
#     # 注册蓝图
#     app.register_blueprint(data_bp)
#     app.register_blueprint(user_bp)
#     app.register_blueprint(order_bp)
#
#     db.init_app(app=app)
#     migrate.init_app(app=app, db=db)
#     # # 删除表
#     # db.drop_all(app=app)
#     # # 创建表
#     # db.create_all(app=app)
#
#     manager = Manager(app, db)
#     manager.add_command("db", MigrateCommand)
#
#     # # 初始化 db
#     # with app.app_context():
#     #     init_db_data()
#
#     # python main.py runserver --host=0.0.0.0
#     manager.run()
#
#     WSGIServer(("127.0.0.1", 5000), app).serve_forever()


app = create_app()
# 然后这里可以写 manager
# from flask_migrate import MigrateCommand
# from flask_script import Manager
# manager = Manager(app)
# manager.add_command("db", MigrateCommand)

if __name__ == '__main__':
    # manager.run()
    # app.run()
    # # 不能用自带的服务器
    from gevent.pywsgi import WSGIServer
    WSGIServer(("0.0.0.0", 5000), app).serve_forever()
