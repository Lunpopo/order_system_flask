import requests

from app_router.models.models import AuthUser
from utils.authentication import verify_password


def check_user(username, password):
    """
    检查用户名和密码
    :param username:
    :param password:
    :return:
    """
    user = AuthUser.query.filter_by(username=username).first()
    if not user:
        return False
    if not verify_password(password, user.password):
        return False
    return user


def get_current_ip():
    """
    获取当前ip
    :return:
    """
    res = requests.get('http://myip.ipip.net', timeout=5)
    return res.text.split("：")[1].split(" ")[0]
