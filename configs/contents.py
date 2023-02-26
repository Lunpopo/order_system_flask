import os

# 模板配置
ROOT_DIR = os.path.abspath(os.path.dirname('.'))

STATIC_DIRECTORY = os.path.join(ROOT_DIR, "static")
TEMPLATE_DIRECTORY = os.path.join(ROOT_DIR, "templates/order_system")

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
TEMP_DIR = os.path.join(BASE_DIR, "../tmp")

MINIO_HOSTS = "127.0.0.1:9001"
ACCESS_KEY = "minioadmin"
SECRET_KEY = "minioadmin"

AUTH_SECRET_KEY = "9d7caa1575015bbbb5bfbd0bb82984a5e856dbc23050da4b4eecbf8e0de0d06a"
ALGORITHM = "HS256"
# 过期时间（分钟）
ACCESS_TOKEN_EXPIRE_MINUTES = 60

# # 角色表
# ROLES = [
#     {
#         "key": 'admin',
#         "name": 'admin',
#         "description": 'Super Administrator. Have access to view all pages.',
#         "routes": ROUTES
#     },
#     {
#         "key": 'editor',
#         "name": 'editor',
#         "description": 'Normal Editor. Can see all pages except permission page',
#         "routes": "routes.filter(i => i.path !== '/permission')// just a mock"
#     },
#     {
#         "key": 'visitor',
#         "name": 'visitor',
#         "description": 'Just a visitor. Can only see the home page and the document page',
#         "routes": [{
#             "path": '/',
#             "redirect": 'dashboard',
#             "children": [
#                 {
#                     "path": 'dashboard',
#                     "name": 'Dashboard',
#                     "meta": {"title": 'dashboard', "icon": 'dashboard'}
#                 }
#             ]
#         }]
#     }]
