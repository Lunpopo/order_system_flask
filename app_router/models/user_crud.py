from app_router.models.database import db
from app_router.models.models import AuthUser, AuthGroup


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
