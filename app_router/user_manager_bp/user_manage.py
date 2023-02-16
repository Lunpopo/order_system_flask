import json
from datetime import timedelta

from flask import Blueprint, request
from gkestor_common_logger import Logger

from app_router.models import user_crud
from app_router.user_manager_bp.user_lib import check_user
from configs.contents import ACCESS_TOKEN_EXPIRE_MINUTES
from utils import restful
from utils.authentication import create_access_token, decode_token

user_bp = Blueprint("user_manage", __name__, url_prefix="/user")
logger = Logger()

users = {
    'admin': {
        'roles': ['admin'],
        'introduction': 'I am a super administrator',
        'avatar': 'https://wpimg.wallstcn.com/f778738c-e4f8-4870-b634-56703b4acafe.gif',
        'name': 'Super Admin'
    },
    'editor': {
        'roles': ['editor'],
        'introduction': 'I am an editor',
        'avatar': 'https://wpimg.wallstcn.com/f778738c-e4f8-4870-b634-56703b4acafe.gif',
        'name': 'Normal Editor'
    }
}


@user_bp.route("/login", methods=["POST"])
def login():
    """
    登录页面
    :return:
    """
    data = request.get_data(as_text=True)
    params_dict = json.loads(data)
    username = params_dict.get("username")
    password = params_dict.get('password')
    logger.info("/login 前端的入参参数：\n{}".format(json.dumps(params_dict, indent=4, ensure_ascii=False)))

    user = check_user(username, password)
    if not user:
        return restful.server_error(message="用户名或密码错误！")

    # 过期时间（分钟）
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    data = {
        "token": "Bearer:{}".format(create_access_token(user.business_id, expires_delta=access_token_expires))
    }
    return restful.ok(message='登录成功！', data=data)


@user_bp.route("/info", methods=["GET"])
def user_info():
    """
    获取用户信息 api
    :return:
    """
    user_token = request.args.get("token")
    user_token = user_token.split("Bearer:")[-1]
    decode_token_dict = decode_token(user_token)
    user_id = decode_token_dict.get("sub")
    user_obj = user_crud.get_user_by_id(user_id=user_id)
    username = user_obj.username

    return restful.ok(message="获取用户信息成功！", data=users[username])
