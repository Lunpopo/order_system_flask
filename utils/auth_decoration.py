#!/usr/bin/env python
# encoding: utf8
# @Author  ：xie.yx
# @Date    ：2022/3/25 14:55
import traceback
from functools import wraps

from jose import jwt, ExpiredSignatureError
from utils import restful

templates = Jinja2Templates(directory=TEMPLATE_DIRECTORY)

login_template_path = "user_manager/login.html"


def auth_assign(api, group_assign: list, is_page: bool = False):
    """
    给 api 增加权限的装饰器
    传入auth权限列表，例如：[0, 1, 2, 99]

    example：@auth_assign(api='/get_base_data', group_assign=[0, 2, 99])  # 组名，普通默认组：0；用户管理组：1；数据管理组：2；超级管理员组：99
    :param api: api名字，例如：/
    :param group_assign: 组名，普通默认组：0；用户管理组：1；数据管理组：2；超级管理员组：99
    :param is_page: 是否为页面，如果是页面的话，没有权限会重定向到 401.html 页面，如果是请求的话那就是返回 restful json，默认为False
    :return:
    """

    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            db = kwargs.get("db")
            authorization = kwargs.get("Authorization")
            request = kwargs.get('request')

            # 登录过期检测
            if authorization:
                try:
                    payload = jwt.decode(token=authorization, key=SECRET_KEY, algorithms=[ALGORITHM])
                    user_data_id, expire = payload.get("sub"), payload.get("exp")

                    user_result = crud.get_user_by_id(db=db, data_id=user_data_id)
                    if not user_result:
                        # TODO 用户信息不存在，用户未注册
                        return templates.TemplateResponse(login_template_path, context={"request": request})
                except ExpiredSignatureError:
                    print('认证已过期，请重新登录')
                    return templates.TemplateResponse(login_template_path,
                                                      context={"request": request, "msg": "认证已过期，请重新登录"})
                except:
                    print('检测用户是否登录过程出错：')
                    print(traceback.format_exc())
                    return templates.TemplateResponse(login_template_path, context={"request": request})
            else:
                return templates.TemplateResponse(login_template_path, context={"request": request})

            # 从前端请求获取用户名
            username = user_result.username

            # 新增api权限和组到数据库
            # --------snip--------
            # 先写 api表 和 组表
            # 写 api 表
            api_result = crud.get_api_by_name(db=db, api_name=api)
            if api_result:
                auth_api_id = api_result.id
            else:
                # 没有就添加进数据库
                data = {
                    "api_name": api
                }
                auth_api_id = crud.add_from_model(db=db, data=data, model=AuthApi)

            # 写用户组表
            for group_name in group_assign:
                group_data = {
                    "group_name": group_name
                }

                get_group_by_name = crud.get_group_by_name(db=db, group_name=group_name)
                if get_group_by_name:
                    auth_group_id = get_group_by_name.id
                else:
                    auth_group_id = crud.add_from_model(db=db, data=group_data, model=AuthGroup)

                # 如果关联表中没有就进行添加
                relation_result = crud.get_relation_from_groupid_apiid(db=db, group_id=auth_group_id,
                                                                       api_id=auth_api_id)
                if not relation_result:
                    relation_data = {
                        "group_id": auth_group_id,
                        "auth_api_id": auth_api_id
                    }
                    crud.add_from_model(db=db, data=relation_data, model=AuthGroupApiRelation)
            # --------新增api权限和组到数据库 END--------

            # 验证权限
            user_result = crud.get_user_by_username(db=db, username=username)

            if user_result and user_result.is_delete == 0:
                # 查询当前用户属于什么用户组，再查看用户组的权限，跟这个api进行对比，如果不一致那么将拒绝此次请求
                current_group_id = user_result.group_id
                if not current_group_id:
                    # 如果当前用户没有组信息，那么就默认是 0 组，即默认组权限
                    # 去用户组 和 api 关联表中查询
                    # 查找 group_name 为 0 的那条数据的id
                    group_info = crud.get_group_by_name(db=db, group_name=0)
                    all_group_api = crud.get_api_group_relation_by_group_id(db=db, group_id=group_info.id)
                else:
                    all_group_api = crud.get_api_group_relation_by_group_id(db=db, group_id=current_group_id)

                # 过滤掉过期的权限
                if auth_api_id not in [_.auth_api_id for _ in all_group_api if _.is_delete == 0]:
                    # 权限认证不通过
                    # 抛出异常
                    if is_page:
                        return templates.TemplateResponse("page/401.html", context={"request": request})
                    else:
                        return restful.unauth(message="权限认证不通过，您没有此功能的权限")
            else:
                return restful.unauth(message="用户不存在")
            return await func(*args, **kwargs)

        return wrapper

    return decorator


def auth_check():
    """
    检测用户是否登录过期
    :return:
    """

    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            db = kwargs.get("db")
            authorization = kwargs.get("Authorization")
            request = kwargs.get('request')

            if authorization:
                try:
                    payload = jwt.decode(token=authorization, key=SECRET_KEY, algorithms=[ALGORITHM])
                    user_data_id, expire = payload.get("sub"), payload.get("exp")

                    user_result = crud.get_user_by_id(db=db, data_id=user_data_id)
                    if not user_result:
                        # TODO 用户信息不存在，用户未注册
                        return templates.TemplateResponse(login_template_path, context={"request": request})

                except ExpiredSignatureError:
                    print('认证已过期，请重新登录')
                    return templates.TemplateResponse(login_template_path,
                                                      context={"request": request, "msg": "认证已过期，请重新登录"})
                except:
                    print('检测用户是否登录过程出错：')
                    print(traceback.format_exc())
                    return templates.TemplateResponse(login_template_path, context={"request": request})
            else:
                return templates.TemplateResponse(login_template_path, context={"request": request})
            return await func(*args, **kwargs)

        return wrapper

    return decorator


def get_current_user(authorization, db):
    # 拉取nacos上的配置文件
    payload = jwt.decode(token=authorization, key=SECRET_KEY, algorithms=[ALGORITHM])
    user_data_id, expire = payload.get("sub"), payload.get("exp")

    user_result = crud.get_user_by_id(db=db, data_id=user_data_id)
    return user_result
