from sqlalchemy import desc
from sqlalchemy.orm import aliased

from app_router.models.database import db
from app_router.models.models import AuthUser, AuthGroup, AuthApi
from enums.enums import UserGroupEnum, MenuEnum, MenuHiddenEnum


def get_user_by_name(username):
    """
    根据用户名查询是否有这条数据
    :param username: 用户名
    :return:
    """
    return AuthUser.query.filter_by(username=username).first()


def get_user_by_id(user_id):
    """
    根据 business_id 查询用户
    :param user_id: 用户id
    :return:
    """
    return AuthUser.query.filter_by(business_id=user_id).first()


def add_user(data):
    """
    添加用户信息
    :param data:
    :return:
    """
    try:
        user_obj = AuthUser(**data)
        db.session.add(user_obj)
        db.session.commit()
        db.session.flush()
        return user_obj
    except:
        db.session.rollback()
        # TODO 添加自定义错误
        raise Exception


def get_group_name_by_user_id(user_id):
    """
    通过用户id获取对应的组名，例如99管理员组
    :param user_id: 用户id
    :return: group_name
    """
    A = aliased(AuthUser)
    B = aliased(AuthGroup)
    result_tuple_list = db.session.query(A, B).join(B, A.group_id == B.business_id).filter(
        A.business_id == user_id).first()
    return result_tuple_list[-1].group_name


def get_group_by_name(group_name):
    """
    根据组名查询组的 business_id
    :param group_name: 组名
    :return:
    """
    return AuthGroup.query.filter_by(group_name=group_name).first()


def add_group(data):
    """
    添加用户信息
    :param data:
    :return:
    """
    try:
        group_obj = AuthGroup(**data)
        # group_obj.fill(data)
        db.session.add(group_obj)
        db.session.commit()
        db.session.flush()
        return group_obj.business_id
    except:
        db.session.rollback()
        # TODO 添加自定义错误
        raise Exception


def add_menu(data):
    """
    添加一条菜单（api）
    :param data:
    :return:
    """
    try:
        menu_obj = AuthApi(**data)
        # group_obj.fill(data)
        db.session.add(menu_obj)
        db.session.commit()
        db.session.flush()
        return menu_obj.title
    except:
        db.session.rollback()
        # TODO 添加自定义错误
        raise Exception


def update_menu(data):
    """
    更新一条菜单（api）
    :param data:
    :return:
    """
    business_id = data.get('business_id')
    try:
        # 根据业务id查询这条数据
        api_obj = get_auth_api_by_id(business_id=business_id)
        if api_obj:
            # 执行更新操作
            api_obj.query.filter_by(business_id=business_id).update(data)
            db.session.commit()
    except:
        db.session.rollback()
        # TODO 添加自定义错误
        raise Exception


def get_all_permission():
    """
    获取所有的api权限
    :return:
    """
    all_group_list = AuthGroup.query.all()
    group_names = []
    for group_obj in all_group_list:
        group_name = group_obj.group_name
        group_dict = group_obj.as_dict()
        # group_dict['label'] 用作前端显示的
        group_dict['label'] = UserGroupEnum(group_name).name
        group_names.append(group_dict)

    return group_names


def get_parent_menu():
    """
    获取非最后一级的菜单
    :return:
    """
    return AuthApi.query.filter(AuthApi.menu_type == 0).order_by(desc('update_time')).all()


def get_auth_api_by_id(business_id):
    """
    通过 auth_api的business_id 查找这条数据
    :param business_id: 这条数据的业务id
    :return:
    """
    return AuthApi.query.filter_by(business_id=business_id).first()


def get_menu(page, limit):
    """
    获取菜单列表
    :param page:
    :param limit:
    :return:
    """
    result_list = AuthApi.query.order_by(desc('update_time')).offset(page).limit(limit).all()
    auth_api_list = []
    for auth_api_obj in result_list:
        menu_type = auth_api_obj.menu_type
        hidden = auth_api_obj.hidden
        permission = auth_api_obj.permission
        auth_api_dict = auth_api_obj.as_dict()

        # 用作前端显示的展示
        # 菜单等级
        auth_api_dict['menu_type_label'] = MenuEnum(menu_type).name
        # 父级菜单
        parent_id = auth_api_obj.api_parent_id
        if parent_id:
            this_auth_obj = get_auth_api_by_id(parent_id)
            auth_api_dict['api_parent_id_label'] = this_auth_obj.title
        # 菜单是否隐藏
        auth_api_dict['hidden_label'] = MenuHiddenEnum(hidden).name
        # 展示菜单的权限
        if ":" in permission:
            permissions = permission.split(":")
            auth_api_dict['permission'] = [int(x) for x in permissions]
            permissions_label = [UserGroupEnum(int(x)).name for x in permissions]
        else:
            auth_api_dict['permission'] = [int(permission)]
            permissions_label = [UserGroupEnum(int(permission)).name]
        auth_api_dict['permission_label'] = permissions_label

        auth_api_list.append(auth_api_dict)

    return {
        "data": auth_api_list,
        "count": AuthApi.query.count()
    }


def delete_menu_by_id(business_id):
    """
    通过业务id删除菜单
    :param business_id:
    :return:
    """
    try:
        AuthApi.query.filter_by(business_id=business_id).delete()
        db.session.commit()
    except:
        db.session.rollback()
        raise Exception
