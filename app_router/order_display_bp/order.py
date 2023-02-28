import json

from flask import Blueprint, request
from gkestor_common_logger import Logger

from app_router.models import order_crud, crud
from app_router.order_display_bp.order_lib import order_stock_data_list, search_stock_product
from messages.messages import *
from utils import restful
from utils.date_utils import time_to_timestamp

order_bp = Blueprint("order_display", __name__, url_prefix="/order")
logger = Logger()


@order_bp.route("/get_transaction_list", methods=["GET"])
def get_transaction_list():
    """
    获取交易信息列表（前10的经销商数据）
    :return:
    """
    data = {
      'total': 20,
      'items': [{
        'order_no': 'fuck hash',
        'timestamp': '202020200',
        'username': 'admin',
        'price': '1920000',
        'status': 0
      }]
    }
    return restful.ok(message="获取交易信息成功！", data=data)


@order_bp.route("/get_outbound_stock_all_data", methods=["GET"])
def get_outbound_stock_all_data():
    """
    获取出库数据信息-用于下载
    :return:
    """
    # 名称搜索
    product_name = request.args.get("title")

    params_dict = {'product_name': product_name}
    logger.info("/get_outbound_stock_all_data 前端的入参参数：\n{}".format(
        json.dumps(params_dict, indent=4, ensure_ascii=False))
    )

    # 获取出库库存数据
    outbound_stock_obj_list = order_crud.cal_outbound_stock_list()
    outbound_stock_obj_list = [_.get("product_obj") for _ in outbound_stock_obj_list]
    # 搜索
    data_list = search_stock_product(outbound_stock_obj_list, product_name)
    # 按数量排序
    data_list = order_stock_data_list(data_list)

    return_data = {
        "Success": True,
        "code": 2000,
        "msg": "",
        "count": len(data_list),
        "data": data_list
    }
    return restful.ok(message="返回产品列表数据", data=return_data)


@order_bp.route("/get_purchase_stock_all_data", methods=["GET"])
def get_purchase_stock_all_data():
    """
    获取入库数据信息-用于下载
    :return:
    """
    # 名称搜索
    product_name = request.args.get("title")

    params_dict = {"product_name": product_name}
    logger.info("/get_purchase_stock_all_data 前端的入参参数：\n{}".format(
        json.dumps(params_dict, indent=4, ensure_ascii=False))
    )

    # 获取入库库存数据
    purchase_stock_obj_list = order_crud.cal_purchase_stock_list()
    purchase_stock_obj_list = [_.get("product_obj") for _ in purchase_stock_obj_list]
    # 搜索
    data_list = search_stock_product(purchase_stock_obj_list, product_name)
    # 按数量排序
    data_list = order_stock_data_list(data_list)

    return_data = {
        "Success": True,
        "code": 2000,
        "msg": "",
        "count": len(data_list),
        "data": data_list
    }
    return restful.ok(message="返回产品列表数据", data=return_data)


@order_bp.route("/get_stock_all_data", methods=["GET"])
def get_stock_all_data():
    """
    获取总库存数据信息-用于下载
    :return:
    """
    # 名称搜索
    product_name = request.args.get("title")

    params_dict = {"product_name": product_name}
    logger.info("/get_stock_all_data 前端的入参参数：\n{}".format(json.dumps(params_dict, indent=4, ensure_ascii=False)))

    # 获取所有的库存数据
    stock_obj_list = order_crud.cal_stock_list()
    # 搜索
    data_list = search_stock_product(stock_obj_list, product_name)
    # 按数量排序
    data_list = order_stock_data_list(data_list)

    return_data = {
        "Success": True,
        "code": 2000,
        "msg": "",
        "count": len(data_list),
        "data": data_list
    }
    return restful.ok(message="返回产品列表数据", data=return_data)


@order_bp.route("/get_purchase_stock_data_list", methods=["GET"])
def get_purchase_stock_data_list():
    """
    获取入库数据信息
    :return:
    """
    page = int(request.args.get("page"))
    limit = int(request.args.get("limit"))
    # 名称搜索
    product_name = request.args.get("title")

    params_dict = {"page": page, "limit": limit, 'product_name': product_name}
    logger.info("/get_purchase_stock_data_list 前端的入参参数：\n{}".format(
        json.dumps(params_dict, indent=4, ensure_ascii=False))
    )

    # 获取入库库存数据
    purchase_stock_obj_list = order_crud.cal_purchase_stock_list()
    purchase_stock_obj_list = [_.get("product_obj") for _ in purchase_stock_obj_list]
    # 搜索
    data_list = search_stock_product(purchase_stock_obj_list, product_name)
    # 按数量排序
    data_list = order_stock_data_list(data_list)

    # 利用page、limit、order_by 做分页和排序
    # 前端page从1开始
    page -= 1
    page = page * limit
    paginate_list = data_list[page: page + limit]
    return_data = {
        "Success": True,
        "code": 2000,
        "msg": "",
        "count": len(data_list),
        "data": paginate_list
    }
    return restful.ok(message="返回产品列表数据", data=return_data)


@order_bp.route("/get_outbound_stock_data_list", methods=["GET"])
def get_outbound_stock_data_list():
    """
    获取出库数据信息
    :return:
    """
    page = int(request.args.get("page"))
    limit = int(request.args.get("limit"))
    # 名称搜索
    product_name = request.args.get("title")

    params_dict = {"page": page, "limit": limit, 'product_name': product_name}
    logger.info("/get_outbound_stock_data_list 前端的入参参数：\n{}".format(
        json.dumps(params_dict, indent=4, ensure_ascii=False))
    )

    # 获取出库库存数据
    outbound_stock_obj_list = order_crud.cal_outbound_stock_list()
    outbound_stock_obj_list = [_.get("product_obj") for _ in outbound_stock_obj_list]

    # 搜索
    data_list = search_stock_product(outbound_stock_obj_list, product_name)
    # 按数量排序
    data_list = order_stock_data_list(data_list)

    # 利用page、limit、order_by 做分页和排序
    # 前端page从1开始
    page -= 1
    page = page * limit
    paginate_list = data_list[page: page + limit]
    return_data = {
        "Success": True,
        "code": 2000,
        "msg": "",
        "count": len(data_list),
        "data": paginate_list
    }
    return restful.ok(message="返回产品列表数据", data=return_data)


@order_bp.route("/get_stock_data_list", methods=["GET"])
def get_stock_data_list():
    """
    获取总库存数据信息
    :return:
    """
    page = int(request.args.get("page"))
    limit = int(request.args.get("limit"))
    # 名称搜索
    product_name = request.args.get("title")

    params_dict = {"page": page, "limit": limit, "product_name": product_name}
    logger.info("/get_stock_data_list 前端的入参参数：\n{}".format(json.dumps(params_dict, indent=4, ensure_ascii=False)))

    # 获取所有的库存数据
    stock_obj_list = order_crud.cal_stock_list()

    # 搜索
    data_list = search_stock_product(stock_obj_list, product_name)
    # 按数量排序
    data_list = order_stock_data_list(data_list)

    # 利用page、limit、order_by 做分页和排序
    # 前端page从1开始
    page -= 1
    page = page * limit
    paginate_list = data_list[page: page + limit]
    return_data = {
        "Success": True,
        "code": 2000,
        "msg": "",
        "count": len(data_list),
        "data": paginate_list
    }
    return restful.ok(message="返回产品列表数据", data=return_data)


@order_bp.route("/get_outbound_pie_statistics", methods=["GET"])
def get_outbound_pie_statistics():
    """
    获取各个经销商的出库单的金额统计饼图信息
    :return:
    """
    result_data = order_crud.get_outbound_pie_statistic()

    dealer_names = []
    return_data = []
    for outbound_obj in result_data:
        _dict = {
            # 经销商名称
            "name": outbound_obj[0],
            # 经销商的销售金额
            "value": outbound_obj[1]
        }
        # 加入经销商的列表
        dealer_names.append(outbound_obj[0])
        return_data.append(_dict)

    return restful.ok(
        message="获取各个经销商出库金额统计信息成功！",
        data={"dealer_names": dealer_names, "data_dict": return_data}
    )


@order_bp.route("/get_outbound_bar_statistics", methods=["GET"])
def get_outbound_bar_statistics():
    """
    获取各个经销商的出库单的金额统计 柱状图 信息
    :return:
    """
    result_data = order_crud.get_outbound_bar_statistic()
    return restful.ok(message="获取各个经销商出库金额统计信息成功！", data=result_data)


@order_bp.route("/get_purchase_price_statistics", methods=["GET"])
def get_purchase_price_statistics():
    """
    获取入库单的金额统计信息
    :return:
    """
    result_data = order_crud.get_purchase_statistic()
    data_list = []
    for _ in result_data:
        _dict = _.as_dict()
        data_list.append(_dict)

    # 统计图的横坐标
    x = []
    # 统计图的纵坐标
    y = []
    for purchase_obj in data_list:
        x.append(purchase_obj.get('create_time'))
        y.append(purchase_obj.get("total_price"))

    data = {
        "x": x,
        "y": y
    }
    return restful.ok(message="获取入库单金额统计信息成功！", data=data)


@order_bp.route("/get_purchase_piece_statistics", methods=["GET"])
def get_purchase_piece_statistics():
    """
    获取入库单的数量统计信息
    :return:
    """
    result_data = order_crud.get_purchase_statistic()
    data_list = []
    for _ in result_data:
        _dict = _.as_dict()
        data_list.append(_dict)

    # 统计图的横坐标
    x = []
    # 统计图的纵坐标
    y = []
    for purchase_obj in data_list:
        x.append(purchase_obj.get('create_time'))
        y.append(purchase_obj.get("total_piece"))

    data = {
        "x": x,
        "y": y
    }
    return restful.ok(message="获取入库单数量统计信息成功！", data=data)


@order_bp.route("/get_outbound_price_statistics", methods=["GET"])
def get_outbound_price_statistics():
    """
    获取出库单的金额统计信息
    :return:
    """
    result_data = order_crud.get_outbound_statistic()
    data_list = []
    for _ in result_data:
        _dict = _.as_dict()
        data_list.append(_dict)

    # 统计图的横坐标
    x = []
    # 统计图的纵坐标
    y = []
    for outbound_obj in data_list:
        x.append(outbound_obj.get('create_time'))
        y.append(outbound_obj.get("total_price"))

    data = {
        "x": x,
        "y": y
    }
    return restful.ok(message="获取出库单金额统计信息成功！", data=data)


@order_bp.route("/get_outbound_piece_statistics", methods=["GET"])
def get_outbound_piece_statistics():
    """
    获取出库单的数量统计信息
    :return:
    """
    result_data = order_crud.get_outbound_statistic()
    data_list = []
    for _ in result_data:
        _dict = _.as_dict()
        data_list.append(_dict)

    # 统计图的横坐标
    x = []
    # 统计图的纵坐标
    y = []
    for outbound_obj in data_list:
        # 用创建时间（这样更改了订单内容也不会改变该条数据的排序）
        x.append(outbound_obj.get('create_time'))
        y.append(outbound_obj.get("total_piece"))

    data = {
        "x": x,
        "y": y
    }
    return restful.ok(message="获取出库单数量统计信息成功！", data=data)


@order_bp.route("/get_total_purchase_price_and_piece", methods=["GET"])
def get_total_purchase_price_and_piece():
    """
    获取入库单的总金额和总数量
    :return:
    """
    order_total_price = order_crud.get_total_purchase_price()
    order_total_piece = order_crud.get_total_purchase_piece()
    data = {
        "total_price": order_total_price,
        "total_piece": order_total_piece
    }
    return restful.ok(message="获取入库单总金额成功！", data=data)


@order_bp.route("/get_total_outbound_price_and_piece", methods=["GET"])
def get_total_outbound_price_and_piece():
    """
    获取出库单的总金额和总数量
    :return:
    """
    order_total_price = order_crud.get_total_outbound_price()
    order_total_piece = order_crud.get_total_outbound_piece()
    data = {
        "total_price": order_total_price,
        "total_piece": int(order_total_piece)
    }
    return restful.ok(message="获取出库单总金额成功！", data=data)


@order_bp.route("/get_purchase_order", methods=["GET"])
def get_purchase_order():
    """
    获取入库单列表
    :return:
    """
    page = int(request.args.get("page"))
    limit = int(request.args.get("limit"))

    params_dict = {"page": page, "limit": limit}
    logger.info("/get_purchase_order 前端的入参参数：\n{}".format(json.dumps(params_dict, indent=4, ensure_ascii=False)))

    # 前端page从1开始
    page -= 1
    page = page * limit
    result = order_crud.get_purchase_order_limit(page=page, limit=limit)
    result_data = result.get("data")
    data_list = []
    for _ in result_data:
        _dict = _.as_dict()
        data_list.append(_dict)

    # 增加一个产品采购单的种类
    for purchase_result_obj in data_list:
        purchase_business_id = purchase_result_obj['business_id']
        purchase_list_result = order_crud.get_products_by_purchase_order_id(data_id=purchase_business_id)
        purchase_result_obj['type'] = purchase_list_result.get("count")

    # 统一转换成时间戳的形式
    data_list = time_to_timestamp(data_list)

    return_data = {
        "Success": True,
        "code": 2000,
        "msg": "",
        "count": result.get('count'),
        "data": data_list
    }
    return restful.ok(message="返回进货单列表数据", data=return_data)


@order_bp.route("/get_purchase_product_details", methods=["GET"])
def get_purchase_product_details():
    """
    获取入库单的产品列表详情信息
    :return:
    """
    # 订单ID
    purchase_order_id = request.args.get("purchase_order_id")

    params_dict = {"purchase_order_id": purchase_order_id}
    logger.info("/get_purchase_product_details 前端的入参参数：\n{}".format(
        json.dumps(params_dict, indent=4, ensure_ascii=False))
    )

    data_list = []
    result = order_crud.get_products_by_purchase_order_id(data_id=purchase_order_id)
    result_data = result.get("data")
    for data_obj in result_data:
        purchase_product_id = data_obj.get('product_id')
        product_obj = crud.get_product_by_business_id(business_id=purchase_product_id)

        _dict = {
            'product_name': product_obj.product_name,
            'scent_type': product_obj.scent_type,
            "specifications": product_obj.specifications,
            "specification_of_piece": product_obj.specification_of_piece,
            "unit_price": product_obj.unit_price,
            "img_url": product_obj.img_url,
            "thumb_img_url": product_obj.thumb_img_url,
            "quantity": data_obj.get('quantity'),
            "subtotal_price": data_obj.get('subtotal_price'),
            "remarks": data_obj.get('remarks')
        }
        data_list.append(_dict)

    return_data = {
        "Success": True,
        "code": 2000,
        "msg": "",
        "count": result.get('count'),
        "data": data_list
    }
    return restful.ok(message="返回产品列表数据", data=return_data)


@order_bp.route("/add_purchase_order", methods=["POST"])
def add_purchase_order():
    """
    新增一条入库单
    :return:
    """
    data = request.get_data(as_text=True)
    params_dict = json.loads(data)
    logger.info(
        "/add_purchase_order 前端传入的参数为：\n{}".format(json.dumps(params_dict, indent=4, ensure_ascii=False))
    )

    title = params_dict.get("title")
    domains = params_dict.get("domains")
    total_price = params_dict.get("total_price")
    total_piece = params_dict.get("total_piece")
    remarks = params_dict.get("remarks")

    if domains:
        purchase_order_dict = {
            "title": title,
            "total_price": total_price,
            "total_piece": total_piece,
            "remarks": remarks
        }
        # 新增一条入库单数据，并返回入库单的 业务id
        purchase_order_obj = order_crud.add_purchase_order(data=purchase_order_dict)

        if purchase_order_obj:
            for single_product_obj in domains:
                # 单条产品列表
                single_product_dict = {
                    "purchase_order_id": purchase_order_obj.business_id,
                    "product_id": single_product_obj.get('business_id'),
                    "quantity": single_product_obj.get("quantity"),
                    "subtotal_price": single_product_obj.get("subtotal_price"),
                    "remarks": single_product_obj.get("remarks")
                }
                # 添加本条产品记录到 purchase_order_list 表里面
                order_crud.add_purchase_product(data=single_product_dict)

        else:
            return restful.server_error(message=add_purchase_order_failed)

        return restful.ok(message=add_purchase_order_success)
    return restful.server_error(message=add_purchase_order_not_zero)


@order_bp.route("/del_purchase_order", methods=["POST"])
def del_purchase_order():
    """
    根据 订单ID 删除一条入库单
    :return:
    """
    data = request.get_data(as_text=True)
    params_dict = json.loads(data)
    logger.info("/del_purchase_order 前端传入的参数为：\n{}".format(json.dumps(params_dict, indent=4, ensure_ascii=False)))

    business_id = params_dict.get("purchase_order_id")
    try:
        order_crud.del_purchase_order_by_id(data_id=business_id)
    except:
        return restful.server_error(message=del_purchase_order_failed)

    return restful.ok(message=del_purchase_order_success)


@order_bp.route("/get_outbound_order", methods=["GET"])
def get_outbound_order():
    """
    获取出库单列表
    :return:
    """
    page = int(request.args.get("page"))
    limit = int(request.args.get("limit"))
    dealer_name = request.args.get('dealer_name')

    params_dict = {"page": page, "limit": limit, 'dealer_name': dealer_name}
    logger.info("/get_outbound_order 前端的入参参数：\n{}".format(json.dumps(params_dict, indent=4, ensure_ascii=False)))

    # 前端page从1开始
    page -= 1
    page = page * limit
    result = order_crud.get_outbound_order_limit(page=page, limit=limit, dealer_name=dealer_name)
    result_data = result.get("data")
    data_list = []
    for _ in result_data:
        _dict = _.as_dict()
        data_list.append(_dict)

    # 增加一个产品出库的种类
    for outbound_result_obj in data_list:
        outbound_business_id = outbound_result_obj['business_id']
        outbound_list_result = order_crud.get_products_by_outbound_order_id(data_id=outbound_business_id)
        outbound_result_obj['type'] = outbound_list_result.get("count")

    # 统一转换成时间戳的形式
    data_list = time_to_timestamp(data_list)

    return_data = {
        "Success": True,
        "code": 2000,
        "msg": "",
        "count": result.get('count'),
        "data": data_list
    }

    return restful.ok(message="返回出库单列表数据", data=return_data)


@order_bp.route("/get_outbound_product_details", methods=["GET"])
def get_outbound_product_details():
    """
    获取出库单的产品列表详情信息
    :return:
    """
    # 出库单ID
    outbound_order_id = request.args.get("outbound_order_id")

    params_dict = {"outbound_order_id": outbound_order_id}
    logger.info("/get_outbound_product_details 前端的入参参数：\n{}".format(
        json.dumps(params_dict, indent=4, ensure_ascii=False))
    )

    result = order_crud.get_products_by_outbound_order_id(data_id=outbound_order_id)
    data_list = result.get("data")

    for data_obj in data_list:
        dealer_product_id = data_obj.get('dealer_product_id')
        dealer_product_obj = order_crud.get_products_by_dealer_product_id(dealer_product_id=dealer_product_id)
        _dict = dealer_product_obj.as_dict()
        product_obj = crud.get_product_by_business_id(business_id=dealer_product_obj.product_id)

        data_obj['product_name'] = product_obj.product_name
        data_obj['specifications'] = product_obj.specifications
        data_obj['scent_type'] = product_obj.scent_type
        data_obj['specification_of_piece'] = product_obj.specification_of_piece
        data_obj['thumb_img_url'] = product_obj.thumb_img_url
        data_obj['img_url'] = product_obj.img_url

        data_obj['belong_to'] = _dict.get('belong_to')
        data_obj['unit_price'] = _dict.get('unit_price')

    return_data = {
        "Success": True,
        "code": 2000,
        "msg": "",
        "count": result.get('count'),
        "data": data_list
    }
    return restful.ok(message="返回出库单列表数据", data=return_data)


@order_bp.route("/add_outbound_order", methods=["POST"])
def add_outbound_order():
    """
    新增一条出库单
    :return:
    """
    data = request.get_data(as_text=True)
    params_dict = json.loads(data)
    logger.info("/add_outbound_order 前端传入的参数为：\n{}".format(json.dumps(params_dict, indent=4, ensure_ascii=False)))

    title = params_dict.get("title")
    belong_to = params_dict.get("belong_to")
    domains = params_dict.get("domains")
    total_price = params_dict.get("total_price")
    total_piece = params_dict.get("total_piece")
    remarks = params_dict.get("remarks")
    phone = params_dict.get("phone")
    address = params_dict.get("address")
    logistics_company = params_dict.get("logistics_company")
    logistics_num = params_dict.get("logistics_num")

    if domains:
        outbound_order_dict = {
            "title": title,
            "belong_to": belong_to,
            "total_price": total_price,
            "total_piece": total_piece,
            "phone": phone,
            "address": address,
            "logistics_company": logistics_company,
            "logistics_num": logistics_num,
            "remarks": remarks
        }
        # 新增一条出库单数据，并返回出库单的 业务id
        outbound_order_obj = order_crud.add_outbound_order(data=outbound_order_dict)

        if domains and outbound_order_obj:
            for single_product_obj in domains:
                # 单条产品列表
                single_product_dict = {
                    "outbound_order_id": outbound_order_obj.business_id,
                    "dealer_product_id": single_product_obj.get("business_id"),
                    "quantity": single_product_obj.get("quantity"),
                    "subtotal_price": single_product_obj.get("subtotal_price"),
                    # 这个remark 不是 product表的remark，而是添加出库订单产品的remark，单独的
                    "remarks": single_product_obj.get("product_remarks")
                }
                # 添加本条产品记录到 outbound_order_list 表里面
                order_crud.add_outbound_product(data=single_product_dict)

        else:
            return restful.server_error(message=add_outbound_order_failed)

        return restful.ok(message=add_outbound_order_success)
    else:
        return restful.server_error(message=add_outbound_order_not_zero)


@order_bp.route("/del_outbound_order", methods=["POST"])
def del_outbound_order():
    """
    根据 订单ID 删除一条出库单
    :return:
    """
    data = request.get_data(as_text=True)
    params_dict = json.loads(data)
    logger.info("/del_outbound_order 前端传入的参数为：\n{}".format(json.dumps(params_dict, indent=4, ensure_ascii=False)))

    business_id = params_dict.get("outbound_order_id")
    try:
        order_crud.del_outbound_order_by_id(data_id=business_id)
    except:
        return restful.server_error(message=del_outbound_order_failed)

    return restful.ok(message=del_outbound_order_success)
