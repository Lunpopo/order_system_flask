import json
from datetime import timedelta

from flask import Blueprint, request
from gkestor_common_logger import Logger

from app_router.models import user_crud
from app_router.user_manager_bp.user_lib import check_user
from configs.contents import ACCESS_TOKEN_EXPIRE_MINUTES, ROUTES, ROLES
from enums.enums import UserGroupEnum, UserRoleEnum
from messages.messages import add_menu_success, add_menu_failed, delete_menu_success, delete_menu_failed, \
    update_menu_success, update_menu_failed
from utils import restful
from utils.authentication import create_access_token, decode_token
from utils.date_utils import time_to_timestamp

user_bp = Blueprint("user_manage", __name__, url_prefix="/user")
logger = Logger()


@user_bp.route("/login", methods=["POST"])
def login():
    """
    登录api
    :return:
    """
    data = request.get_data(as_text=True)
    params_dict = json.loads(data)
    username = params_dict.get("username")
    password = params_dict.get('password')
    # logger.info("/login 前端的入参参数：\n{}".format(json.dumps(params_dict, indent=4, ensure_ascii=False)))

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
    group_name = user_crud.get_group_name_by_user_id(user_id=user_id)

    group_name = UserGroupEnum(group_name).name
    return_user = UserRoleEnum[group_name].value
    print(return_user)
    return restful.ok(message="获取用户信息成功！", data=return_user)


@user_bp.route("roles", methods=["GET"])
def get_roles():
    """
    获取权限信息表
    :return:
    """
    return restful.ok(message="获取权限信息成功！", data=ROLES)


@user_bp.route("routes", methods=["GET"])
def get_routes():
    """
    获取路由表
    :return:
    """
    return restful.ok(message="获取权限信息成功！", data=ROUTES)


@user_bp.route("get_all_permission", methods=["GET"])
def get_all_permission():
    """
    获取所有的api权限
    :return:
    """
    group_names = user_crud.get_all_permission()
    return_data = {
        "Success": True,
        "code": 2000,
        "msg": "",
        "data": group_names
    }
    return restful.ok(message="返回所有的api权限", data=return_data)


@user_bp.route("get_parent_menu", methods=["GET"])
def get_parent_menu():
    """
    获取父级菜单
    :return:
    """
    result = user_crud.get_parent_menu()
    # json格式化
    data_list = [_.as_dict() for _ in result]
    # 统一转换成时间戳的形式
    data_list = time_to_timestamp(data_list)

    return_data = {
        "Success": True,
        "code": 2000,
        "msg": "",
        "data": data_list
    }
    return restful.ok(message="返回所有的父级菜单列表数据", data=return_data)


@user_bp.route("get_menu", methods=["GET"])
def get_menu():
    """
    获取菜单列表
    :return:
    """
    page = int(request.args.get("page"))
    limit = int(request.args.get("limit"))

    params_dict = {"page": page, "limit": limit}
    logger.info("/user/get_menu 前端的入参参数：\n{}".format(json.dumps(params_dict, indent=4, ensure_ascii=False)))

    # 前端page从1开始
    page -= 1
    page = page * limit
    result = user_crud.get_menu(page, limit)

    result_data = result.get("data")
    # # json格式化
    # data_list = [_.as_dict() for _ in result_data]
    # 统一转换成时间戳的形式
    data_list = time_to_timestamp(result_data)

    return_data = {
        "Success": True,
        "code": 2000,
        "msg": "",
        "count": result.get('count'),
        "data": data_list
    }
    return restful.ok(message="返回菜单列表数据", data=return_data)


@user_bp.route("delete_menu", methods=["POST"])
def delete_menu():
    """
    删除菜单
    :return:
    """
    data = request.get_data(as_text=True)
    params_dict = json.loads(data)
    logger.info(
        "/user/delete_menu 前端传入的参数为：\n{}".format(json.dumps(params_dict, indent=4, ensure_ascii=False))
    )
    menu_id = params_dict.get("business_id")
    try:
        if menu_id:
            user_crud.delete_menu_by_id(menu_id)
    except:
        return restful.server_error(message=delete_menu_failed)
    return restful.ok(message=delete_menu_success)


@user_bp.route("add_menu", methods=["POST"])
def add_menu():
    """
    新增菜单
    :return:
    """
    data = request.get_data(as_text=True)
    params_dict = json.loads(data)
    logger.info(
        "/user/add_menu 前端传入的参数为：\n{}".format(json.dumps(params_dict, indent=4, ensure_ascii=False))
    )
    api_parent_id = params_dict.get("api_parent_id")
    title = params_dict.get("title")
    description = params_dict.get("description")
    icon = params_dict.get("icon")
    menu_type = params_dict.get("menu_type")
    hidden = params_dict.get("hidden")
    permission_list = params_dict.get("permission")
    # permission传过来是个数组，需要变换成字符串
    permission_list = [str(x) for x in permission_list]
    permission = ":".join(permission_list)
    router_path = params_dict.get("router_path")
    component_path = params_dict.get("component_path")

    try:
        if title:
            add_menu_dict = {
                "api_parent_id": api_parent_id,
                "title": title,
                "description": description,
                "icon": icon,
                "menu_type": menu_type,
                "hidden": hidden,
                "permission": permission,
                "router_path": router_path,
                "component_path": component_path,
            }
            # 新增一条菜单
            menu_title = user_crud.add_menu(data=add_menu_dict)

            if menu_title:
                return restful.ok(message=add_menu_success, data=menu_title)
            else:
                return restful.server_error(message=add_menu_failed)
    except:
        return restful.server_error(message=add_menu_failed)


@user_bp.route("update_menu", methods=["POST"])
def update_menu():
    """
    新增菜单
    :return:
    """
    data = request.get_data(as_text=True)
    params_dict = json.loads(data)
    logger.info(
        "/user/update_menu 前端传入的参数为：\n{}".format(json.dumps(params_dict, indent=4, ensure_ascii=False))
    )
    api_parent_id = params_dict.get("api_parent_id")
    title = params_dict.get("title")
    description = params_dict.get("description")
    icon = params_dict.get("icon")
    menu_type = params_dict.get("menu_type")
    hidden = params_dict.get("hidden")
    permission_list = params_dict.get("permission")
    # permission传过来是个数组，需要变换成字符串
    permission_list = [str(x) for x in permission_list]
    permission = ":".join(permission_list)
    router_path = params_dict.get("router_path")
    component_path = params_dict.get("component_path")
    business_id = params_dict.get('business_id')

    try:
        if title:
            update_menu_dict = {
                "api_parent_id": api_parent_id,
                "title": title,
                "description": description,
                "icon": icon,
                "menu_type": menu_type,
                "hidden": hidden,
                "permission": permission,
                "router_path": router_path,
                "component_path": component_path,
                "business_id": business_id
            }
            # 更新一条菜单
            user_crud.update_menu(data=update_menu_dict)
            return restful.ok(message=update_menu_success)
    except:
        return restful.server_error(message=update_menu_failed)
