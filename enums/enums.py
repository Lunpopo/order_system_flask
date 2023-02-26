from enum import Enum


class ProductScentEnum(Enum):
    """
    产品香型枚举
    """
    老白干香型 = 0
    浓香型 = 1
    清香型 = 2
    其他香型 = 99


class OrderNameEnum(Enum):
    """
    排序的产品列名枚举
    """
    product_name = 'product_name'
    specifications = 'specifications'
    specification_of_piece = 'specification_of_piece'
    unit_price = "unit_price"
    price_of_piece = "price_of_piece"
    suggested_retail_price = "suggested_retail_price"
    scanning_price = "scanning_price"
    create_time = "create_time"


# class UserGroupEnum(Enum):
#     """
#     用户和用户组枚举，数字对应的角色名：
#     普通用户组：0
#     用户管理组：1
#     数据管理组：2
#     管理员：99
#     """
#     editor = 0
#     user = 1
#     data = 2
#     admin = 99


class MenuEnum(Enum):
    """
    菜单显示的枚举
    """
    一级菜单 = 0
    二级菜单 = 1


class MenuHiddenEnum(Enum):
    """
    菜单是否隐藏显示枚举
    """
    是 = True
    否 = False


# class UserRoleEnum(Enum):
#     """
#     用户角色枚举
#     普通用户组：0
#     用户管理组：1
#     数据管理组：2
#     管理员：99
#     """
#     # editor = 0
#     # user = 1
#     # data = 2
#     # admin = 99
#     admin = {
#         'roles': ['admin'],
#         'introduction': 'I am a super administrator',
#         'avatar': 'https://wpimg.wallstcn.com/f778738c-e4f8-4870-b634-56703b4acafe.gif',
#         'name': 'Super Admin'
#     }
#     editor = {
#         'roles': ['editor'],
#         'introduction': 'I am an editor',
#         'avatar': 'https://wpimg.wallstcn.com/f778738c-e4f8-4870-b634-56703b4acafe.gif',
#         'name': 'Normal Editor'
#     }
#     user = {
#         'roles': ['user'],
#         'introduction': 'I am an user manager',
#         'avatar': 'https://wpimg.wallstcn.com/f778738c-e4f8-4870-b634-56703b4acafe.gif',
#         'name': '用户管理组'
#     }
#     data = {
#         'roles': ['data'],
#         'introduction': 'I am an data manager',
#         'avatar': 'https://wpimg.wallstcn.com/f778738c-e4f8-4870-b634-56703b4acafe.gif',
#         'name': '数据管理组'
#     }
