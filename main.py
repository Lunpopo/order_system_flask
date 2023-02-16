from flask import Flask
from flask_cors import CORS
from flask_migrate import MigrateCommand
from flask_script import Manager

from app_router.data_display_bp.data_display import data_bp
from app_router.models import user_crud
from app_router.models.database import db, migrate
from app_router.models.models import DealerList
from app_router.order_display_bp.order import order_bp
from app_router.user_manager_bp.user_lib import get_current_ip
from app_router.user_manager_bp.user_manage import user_bp
from configs import config
from utils.authentication import pwd_context

app = Flask(__name__, static_url_path='/static', template_folder='templates/order_system')
CORS(app, supports_credentials=True)


def init_db_data():
    """
    初始化数据库数据
    """
    from app_router.models import crud
    # 初始化数据库的数据，例如香型表，需要提前添加
    dealer_name_list = [
        "安仁刘总",
        "王总",
        "刘巧蝶",
        "谢湘萍",

        "同事朋友",
        "餐饮酒店",

        "长沙周艳艳",
        "餐饮李卫国",
        "线上平台",
        "李玉国",
        "叶帅"
    ]

    for dealer_name in dealer_name_list:
        if not crud.get_dealer_list_by_name(name=dealer_name):
            st1 = DealerList(dealer_name=dealer_name)
            db.session.add(st1)
            db.session.commit()

    # 添加管理员用户组
    group_name_list = [
        # 普通用户组
        0,
        # 用户管理组
        1,
        # 数据管理组
        2,
        # 管理员
        99
    ]
    for group_name in group_name_list:
        group_data = {
            "group_name": group_name
        }
        if not user_crud.get_group_by_name(group_name):
            user_crud.add_group(data=group_data)

    # 注册管理员用户
    user_data = {
        "username": "admin",
        "password": pwd_context.hash("111111"),
        "group_id": user_crud.get_group_by_name(group_name=99).business_id,
        "register_ip": get_current_ip(),
        "status": 0
    }
    if not user_crud.get_user_by_name(username='admin'):
        user_crud.add_user(data=user_data)


if __name__ == '__main__':
    app.config.from_object(config)
    # 注册蓝图
    app.register_blueprint(data_bp)
    app.register_blueprint(user_bp)
    app.register_blueprint(order_bp)

    db.init_app(app=app)
    migrate.init_app(app=app, db=db)
    # # 删除表
    # db.drop_all(app=app)
    # # 创建表
    # db.create_all(app=app)

    manager = Manager(app, db)
    manager.add_command("db", MigrateCommand)

    # # 初始化 db
    # with app.app_context():
    #     init_db_data()

    # python main.py runserver --host=0.0.0.0
    manager.run()
