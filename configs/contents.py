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
ACCESS_TOKEN_EXPIRE_MINUTES = 1

# 路由表
ROUTES = [{
    "path": '/permission',
    # 'component': 'layout/Layout',
    # 'redirect': '/permission/index',
    # 'alwaysShow': True,
    # 是否在前端隐藏
    'hidden': False,
    'meta': {
        'title': 'Permission',
        'icon': 'lock',
        'roles': ['editor']
    },
    'children': [{
        'path': 'page',
        'component': 'views/permission/page',
        'name': 'PagePermission',
        'meta': {
            'title': 'Page Permission',
            'roles': ['admin']
        }
    }, {
        'path': 'directive',
        'component': 'views/permission/directive',
        'name': 'DirectivePermission',
        'meta': {
            'title': 'Directive Permission'
        }
    }, {
        'path': 'role',
        'component': 'views/permission/role',
        'name': 'RolePermission',
        'meta': {
            'title': 'Role Permission',
            'roles': ['admin']
        }
    }]
}, {
    'path': '/product',
    'component': 'layout/Layout',
    'meta': {
        'title': '货单表格',
        'icon': 'table',
        'roles': ['admin']
    },
    'children': [{
        'path': 'complex-table',
        'component': 'views/product/myself-price-list',
        'name': 'Icons',
        'meta': {'title': '自己的货单表格', 'icon': 'tab'}
    }, {
      'path': 'inline-edit-table',
      'component': 'views/product/dealer-price-list',
      'name': 'InlineEditTable',
      'meta': {'title': '经销商产品价格表', 'icon': 'tab'}
    }]
}, {
    'path': '/order',
    'component': 'layout/Layout',
    'redirect': 'noRedirect',
    'meta': {
        'title': '入库出库单',
        'icon': 'table',
        'roles': ['admin']
    },
    'children': [{
        'path': 'stock-order',
        'component': 'views/order/stock-order',
        'name': 'StockOrder',
        'meta': { 'title': '总体库存', 'icon': 'list' }
    },
    {
        'path': 'purchase-order',
        'component': 'views/order/purchase-order',
        'name': 'PurchaseOrder',
        'meta': {'title': '入库单', 'icon': 'form'}
    },
    {
        'path': 'outbound-order',
        'component': 'views/order/outbound-order',
        'name': 'OutboundOrder',
        'meta': {'title': '出货单', 'icon': 'money'}
    }]
}]

# 角色表
ROLES = [{
    "key": 'admin',
    "name": 'admin',
    "description": 'Super Administrator. Have access to view all pages.',
    "routes": ROUTES
  },
  {
    "key": 'editor',
    "name": 'editor',
    "description": 'Normal Editor. Can see all pages except permission page',
    "routes": "routes.filter(i => i.path !== '/permission')// just a mock"
  },
  {
    "key": 'visitor',
    "name": 'visitor',
    "description": 'Just a visitor. Can only see the home page and the document page',
    "routes": [{
      "path": '/',
      "redirect": 'dashboard',
      "children": [
        {
          "path": 'dashboard',
          "name": 'Dashboard',
          "meta": {"title": 'dashboard', "icon": 'dashboard'}
        }
      ]
    }]
  }]
