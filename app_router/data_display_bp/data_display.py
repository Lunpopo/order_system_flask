import json
import time
import traceback

from flask import Blueprint, request
from gkestor_common_logger import Logger

from app_router.data_display_bp.data_display_lib import upload_image_thumb, format_dealer_product
from app_router.models import crud
from messages.messages import add_product_success, add_product_failed, delete_product_failed, delete_product_success, \
    multiply_delete_product_success, multiply_delete_product_failed
from utils import restful
from utils.date_utils import time_to_timestamp

data_bp = Blueprint("data_display", __name__, url_prefix="/data")
logger = Logger()


@data_bp.route("/get_product_data", methods=["GET"])
def get_product_data():
    """
    获取产品列表数据-自己的
    :return:
    """
    page = int(request.args.get("page"))
    limit = int(request.args.get("limit"))
    order_by = request.args.get("order_by")

    params_dict = {"page": page, "limit": limit, "order_by": order_by}
    logger.info("/get_product_data 前端的入参参数：\n{}".format(json.dumps(params_dict, indent=4, ensure_ascii=False)))

    # 前端page从1开始
    page -= 1
    page = page * limit
    # 以时间排序获取的产品数据
    if order_by:
        result = crud.get_product_list_limit(page=page, limit=limit, order_by=order_by)
    else:
        result = crud.get_product_list_limit(page=page, limit=limit)
    result_data = result.get("data")
    data_list = []
    for _ in result_data:
        _dict = _.as_dict()
        for key, value in _dict.items():
            if key == "img_url" and value:
                _dict['img_url'] = "{}?{}".format(value, int(time.time()))
            elif key == "thumb_img_url" and value:
                _dict['thumb_img_url'] = "{}?{}".format(value, int(time.time()))
        data_list.append(_dict)

    # 统一转换成时间戳的形式
    data_list = time_to_timestamp(data_list)

    return_data = {
        "Success": True,
        "code": 2000,
        "msg": "",
        "count": result.get('count'),
        "data": data_list
    }
    return restful.ok(message="返回产品列表数据", data=return_data)


@data_bp.route("/get_all_product_data", methods=["GET"])
def get_all_product_data():
    """
    获取所有的产品列表数据——用于下载
    :return:
    """
    order_by = request.args.get("order_by")

    params_dict = {"order_by": order_by}
    logger.info("/get_all_product_data 前端的入参参数：\n{}".format(json.dumps(params_dict, indent=4, ensure_ascii=False)))

    # 前端page从1开始
    if order_by:
        result = crud.get_all_product(order_by=order_by)
    else:
        result = crud.get_all_product()

    result_data = result.get("data")

    # json格式化
    data_list = [_.as_dict() for _ in result_data]
    # 统一转换成时间戳的形式
    data_list = time_to_timestamp(data_list)

    return_data = {
        "Success": True,
        "code": 2000,
        "msg": "",
        "count": result.get('count'),
        "data": data_list
    }
    return restful.ok(message="返回产品列表数据", data=return_data)


@data_bp.route("/search_product", methods=["GET"])
def search_product():
    """
    搜索产品数据
    :return:
    """
    product_name = request.args.get("title")
    page = int(request.args.get("page"))
    limit = int(request.args.get("limit"))
    order_by = request.args.get("order_by")

    params_dict = {"product_name": product_name, "page": page, "limit": limit, "order_by": order_by}
    logger.info("/search_product 前端的入参参数：\n{}".format(json.dumps(params_dict, indent=4, ensure_ascii=False)))

    # 前端page从1开始
    page -= 1
    page = page * limit
    if order_by:
        if product_name:
            result = crud.search_product(product_name=product_name, page=page, limit=limit, order_by=order_by)
        else:
            result = crud.get_product_list_limit(page=page, limit=limit, order_by=order_by)
    else:
        if product_name:
            result = crud.search_product(product_name=product_name, page=page, limit=limit)
        else:
            result = crud.get_product_list_limit(page=page, limit=limit)

    result_data = result.get("data")
    # json格式化
    data_list = [_.as_dict() for _ in result_data]
    # 统一转换成时间戳的形式
    data_list = time_to_timestamp(data_list)

    return_data = {
        "Success": True,
        "code": 2000,
        "msg": "",
        "count": result.get('count'),
        "data": data_list
    }
    return restful.ok(message="返回产品列表数据", data=return_data)


@data_bp.route("/add_product", methods=["POST"])
def add_product():
    """
    新增产品——ajax
    :return:
    """
    # 从前端获取参数
    product_name = request.args.get("product_name")
    specifications = request.args.get("specifications")
    scent_type = request.args.get("scent_type")
    specification_of_piece = request.args.get("specification_of_piece")
    unit_price = request.args.get("unit_price")
    price_of_piece = request.args.get("price_of_piece")
    scanning_price = request.args.get('scanning_price')
    remarks = request.args.get("remarks")
    params_dict = {
        "product_name": product_name,
        "specifications": specifications,
        "scent_type": scent_type,
        "specification_of_piece": specification_of_piece,
        "unit_price": unit_price,
        "price_of_piece": price_of_piece,
        "scanning_price": scanning_price,
        "remarks": remarks
    }
    logger.info("/add_product 前端传入的参数为：\n{}".format(json.dumps(params_dict, indent=4, ensure_ascii=False)))

    # 查询产品是否已存在在数据库中
    result = crud.get_product_by_name_and_scent(
        product_name=product_name, scent_type=scent_type, specifications=specifications
    )
    if result:
        logger.info("新增产品 {} 出错，产品已存在！".format(product_name))
        return restful.server_error(
            message="新增产品出错，产品已存在！",
            data={"traceback": "新增产品 {} 出错，产品已存在！".format(product_name)}
        )

    # 上传图片和缩略图
    # 获取 上传文件的 参数，并将文件下载到本地
    file_obj = request.files.get("pictureFile")
    if file_obj:
        try:
            _return_dict = upload_image_thumb(file_obj=file_obj, product_name=product_name)
            params_dict['img_url'] = "{}?{}".format(_return_dict.get("img_url"), int(time.time()))
            params_dict['thumb_img_url'] = "{}?{}".format(_return_dict.get("thumb_img_url"), int(time.time()))
        except:
            logger.info("新增产品 {} 出错，图片文件不存在！".format(product_name))
            logger.info("详细的出错信息为：{}".format(traceback.format_exc()))
            return restful.server_error(
                message="新增产品出错，图片文件不存在！", data={"traceback": traceback.format_exc()}
            )

    try:
        # 增加数据
        result = crud.add_product(data=params_dict)
        logger.info("新增的 result 为：{}".format(result))
    except:
        logger.info("新增 产品 出错，详细的出错信息为：{}".format(traceback.format_exc()))
        return restful.server_error(message=add_product_failed, data={"traceback": traceback.format_exc()})
    return restful.ok(message=add_product_success)


@data_bp.route("/update_product", methods=["POST"])
def update_product():
    """
    更新产品信息-自己的货单
    :return:
    """
    # 从前端获取参数
    product_name = request.args.get("product_name")
    specifications = request.args.get("specifications")
    scent_type = request.args.get("scent_type")
    specification_of_piece = request.args.get("specification_of_piece")
    unit_price = request.args.get("unit_price")
    price_of_piece = request.args.get("price_of_piece")
    scanning_price = request.args.get('scanning_price')
    remarks = request.args.get("remarks")
    business_id = request.args.get("business_id")

    params_dict = {
        "product_name": product_name,
        "specifications": specifications,
        "scent_type": scent_type,
        "specification_of_piece": specification_of_piece,
        "unit_price": unit_price,
        "price_of_piece": price_of_piece,
        "scanning_price": scanning_price,
        "remarks": remarks
    }
    logger.info("/update_product 前端传入的参数为：\n{}".format(json.dumps(params_dict, indent=4, ensure_ascii=False)))

    # 获取 上传文件的 参数，并将文件下载到本地
    file_obj = request.files.get("pictureFile")
    if file_obj:
        try:
            _return_dict = upload_image_thumb(file_obj=file_obj, product_name=product_name)
            params_dict['img_url'] = "{}?{}".format(_return_dict.get("img_url"), int(time.time()))
            params_dict['thumb_img_url'] = "{}?{}".format(_return_dict.get("thumb_img_url"), int(time.time()))
        except:
            logger.info("更新产品 {} 出错，图片文件不存在！".format(product_name))
            logger.info("详细的出错信息为：{}".format(traceback.format_exc()))
            return restful.server_error(
                message="更新产品出错，图片文件不存在！", data={"traceback": traceback.format_exc()}
            )

    # # 下载原图
    # logger.info("开始下载原始png图像")
    # minio_handler.fget(img_bucket_name, img_object_name, file_path=img_file_path)
    # logger.info("下载原始png图像完成！")

    try:
        # 更新数据
        crud.update_product_by_business_id(data_id=business_id, data=params_dict)
        logger.info("更新 {} 产品数据完成！".format(params_dict.get("product_name")))
    except:
        logger.info("更新 {} 产品 出错，详细的出错信息为：{}".format(
            params_dict.get("product_name"), traceback.format_exc())
        )
        return restful.server_error(message=add_product_failed, data={"traceback": traceback.format_exc()})
    return restful.ok(message=add_product_success)


@data_bp.route("/delete_product", methods=["POST"])
def delete_product():
    """
    根据前端传入的 业务id 删除这条产品数据
    :return:
    """
    data = request.get_data(as_text=True)
    params_dict = json.loads(data)
    logger.info("/delete_product 前端传入的参数为：\n{}".format(json.dumps(params_dict, indent=4, ensure_ascii=False)))
    product_name = params_dict.get("product_name")
    product_id = params_dict.get("business_id")

    try:
        # 根据产品的业务id删除数据
        crud.delete_product_by_business_id(data_id=product_id)
        logger.info("删除 {} 成功！".format(product_name))
    except:
        logger.info("删除 产品{} 出错，详细的出错信息为：{}".format(product_id, traceback.format_exc()))
        return restful.server_error(message=delete_product_failed, data={"traceback": traceback.format_exc()})
    return restful.ok(message=delete_product_success)


@data_bp.route("/product_multi_delete", methods=["POST"])
def product_multi_delete():
    """
    删除多条产品数据
    :return:
    """
    try:
        data = request.get_data(as_text=True)
        # 业务id的集合
        business_ids = json.loads(data)
        logger.info(
            "/product_multi_delete 前端传入的参数为：\n{}".format(json.dumps(business_ids, indent=4, ensure_ascii=False)))

        if business_ids:
            # TODO 这个批量删除可以优化
            for product_business_id in business_ids:

                # 先查一下数据库看有没有这个数据
                product_data = crud.get_product_by_business_id(business_id=product_business_id)
                if product_data:  # 如果有这条数据
                    # 执行删除
                    try:
                        crud.delete_product_by_business_id(data_id=product_business_id)
                    except:
                        logger.error(
                            "删除 产品{} 出错，详细的出错信息为：{}".format(product_business_id, traceback.format_exc())
                        )
                        return restful.server_error(
                            message=multiply_delete_product_failed, data={"traceback": traceback.format_exc()}
                        )

        return restful.ok(message=multiply_delete_product_success)
    except:
        return restful.server_error(
            message=multiply_delete_product_failed, data={"traceback": traceback.format_exc()}
        )


# TODO 要改
@data_bp.route("/get_all_dealer_product_data", methods=["GET"])
def get_all_dealer_product_data():
    """
    获取所有的经销商产品列表数据——用于下载
    :return:
    """
    product_name = request.args.get("title")
    dealer_name = request.args.get("dealer_name")
    order_by = request.args.get("order_by")

    params_dict = {'product_name': product_name, "dealer_name": dealer_name, "order_by": order_by}
    logger.info(
        "/get_all_dealer_product_data 前端的入参参数：\n{}".format(json.dumps(params_dict, indent=4, ensure_ascii=False))
    )

    # 前端page从1开始
    if order_by:
        result = crud.get_all_dealer_product(product_name=product_name, dealer_name=dealer_name, order_by=order_by)
    else:
        result = crud.get_all_dealer_product(product_name=product_name, dealer_name=dealer_name)

    result_data = result.get("data")
    # json格式化
    data_list = [_.as_dict() for _ in result_data]
    # 统一转换成时间戳的形式
    data_list = time_to_timestamp(data_list)

    return_data = {
        "Success": True,
        "code": 2000,
        "msg": "",
        "count": result.get('count'),
        "data": data_list
    }
    return restful.ok(message="返回产品列表数据", data=return_data)


@data_bp.route("/get_dealer_list", methods=["GET"])
def get_dealer_list():
    """
    获取经销商名单列表
    :return:
    """
    result = crud.get_dealer_list()
    result_data = result.get("data")
    # json格式化
    data_list = [_.as_dict() for _ in result_data]
    # 统一转换成时间戳的形式
    data_list = time_to_timestamp(data_list)

    return_data = {
        "Success": True,
        "code": 2000,
        "msg": "",
        "data": data_list
    }
    return restful.ok(message="返回经销商名单列表", data=return_data)


@data_bp.route("/search_dealer_product", methods=["GET"])
def search_dealer_product():
    """
    搜索经销商产品数据
    :return:
    """
    title = request.args.get("title")
    dealer_name = request.args.get("dealer_name")
    page = int(request.args.get("page"))
    limit = int(request.args.get("limit"))
    order_by = request.args.get('order_by')

    params_dict = {
        "title": title, 'dealer_name': dealer_name, "page": page, "limit": limit, 'order_by': order_by
    }
    logger.info(
        "/search_dealer_product 前端的入参参数：\n{}".format(json.dumps(params_dict, indent=4, ensure_ascii=False))
    )

    # 前端page从1开始
    page -= 1
    page = page * limit
    result = crud.search_dealer_product(
        title=title, dealer_name=dealer_name, page=page, limit=limit, order_by=order_by
    )
    result_data = result.get('data')
    data_list = format_dealer_product(result_data)

    return_data = {
        "Success": True,
        "code": 2000,
        "msg": "",
        "count": result.get('count'),
        "data": data_list
    }
    return restful.ok(message="返回产品列表数据", data=return_data)


@data_bp.route("/add_dealer_product", methods=["POST"])
def add_dealer_product():
    """
    新增经销商产品
    :return:
    """
    product_id = request.args.get("product_id")
    product_name = request.args.get("product_name")
    belong_to = request.args.get("belong_to")
    # 出厂价
    unit_price = request.args.get("unit_price")
    # 每件价格
    price_of_piece = request.args.get("price_of_piece")
    # 批发价
    wholesale_price = request.args.get("wholesale_price")
    suggested_retail_price = request.args.get("suggested_retail_price")
    scanning_price = request.args.get("scanning_price")
    remarks = request.args.get("remarks")

    params_dict = {
        "product_id": product_id,
        "belong_to": belong_to,
        "unit_price": unit_price,
        "price_of_piece": price_of_piece,
        "wholesale_price": wholesale_price,
        "suggested_retail_price": suggested_retail_price,
        "scanning_price": scanning_price,
        "remarks": remarks
    }

    logger.info(
        "/add_dealer_product 前端传入的参数为：\n{}".format(json.dumps(params_dict, indent=4, ensure_ascii=False))
    )

    # 查询产品是否已存在在数据库中（香型、规格、产品名、经销商名可以唯一确定一个产品）
    result = crud.dealer_product_is_exist(product_id=product_id, belong_to=belong_to)
    if result:
        logger.info("新增产品 {} 出错，产品已存在！".format(product_name))
        return restful.server_error(
            message="新增产品出错，产品已存在！",
            data={"traceback": "新增产品 {} 出错，产品已存在！".format(product_name)}
        )

    try:
        # 增加数据
        crud.add_dealer_product(data=params_dict)
    except:
        logger.info("新增 经销商产品 出错，详细的出错信息为：{}".format(traceback.format_exc()))
        return restful.server_error(message=add_product_failed, data={"traceback": traceback.format_exc()})
    return restful.ok(message=add_product_success)


@data_bp.route("/update_dealer_product", methods=["POST"])
def update_dealer_product():
    """
    更新经销商产品数据
    :return:
    """
    product_id = request.args.get("product_id")
    product_name = request.args.get("product_name")
    belong_to = request.args.get("belong_to")
    # 出厂价
    unit_price = request.args.get("unit_price")
    # 每件价格
    price_of_piece = request.args.get("price_of_piece")
    # 批发价
    wholesale_price = request.args.get("wholesale_price")
    suggested_retail_price = request.args.get("suggested_retail_price")
    scanning_price = request.args.get("scanning_price")
    business_id = request.args.get("business_id")
    remarks = request.args.get("remarks")

    params_dict = {
        "product_id": product_id,
        "belong_to": belong_to,
        "unit_price": unit_price,
        "price_of_piece": price_of_piece,
        "wholesale_price": wholesale_price,
        "suggested_retail_price": suggested_retail_price,
        "scanning_price": scanning_price,
        "remarks": remarks
    }
    logger.info(
        "/update_dealer_product 前端传入的参数为：\n{}".format(json.dumps(params_dict, indent=4, ensure_ascii=False))
    )

    try:
        # 更新数据
        crud.update_dealer_product_by_business_id(data_id=business_id, data=params_dict)
        logger.info("更新 {} 经销商产品数据完成！".format(params_dict.get("product_name")))
    except:
        logger.info(
            "更新 {} 经销商产品出错，详细的出错信息为：{}".format(params_dict.get("product_name"), traceback.format_exc())
        )
        return restful.server_error(message=add_product_failed, data={"traceback": traceback.format_exc()})
    return restful.ok(message=add_product_success)


@data_bp.route("/delete_dealer_product", methods=["POST"])
def dealer_delete_product():
    """
    根据前端传入的 业务id 删除这条经销商产品数据
    :return:
    """
    data = request.get_data(as_text=True)
    params_dict = json.loads(data)
    logger.info(
        "/delete_dealer_product 前端传入的参数为：\n{}".format(json.dumps(params_dict, indent=4, ensure_ascii=False))
    )
    product_name = params_dict.get("product_name")
    product_id = params_dict.get("business_id")

    try:
        # 根据产品的业务id删除数据
        crud.delete_dealer_product_by_business_id(data_id=product_id)
        logger.info("删除经销商产品 {} 成功！".format(product_name))
    except:
        logger.info("删除经销商产品 {} 出错，详细的出错信息为：{}".format(product_id, traceback.format_exc()))
        return restful.server_error(message=delete_product_failed, data={"traceback": traceback.format_exc()})
    return restful.ok(message=delete_product_success)


@data_bp.route("/dealer_product_multi_delete", methods=["POST"])
def dealer_product_multi_delete():
    """
    删除多条经销商产品数据
    :return:
    """
    try:
        data = request.get_data(as_text=True)
        # 业务id的集合
        business_ids = json.loads(data)
        logger.info(
            "/dealer_product_multi_delete 前端传入的参数为：\n{}".format(
                json.dumps(business_ids, indent=4, ensure_ascii=False)
            )
        )

        if business_ids:
            # TODO 这个批量删除可以优化
            for product_business_id in business_ids:

                # 先查一下数据库看有没有这个数据
                product_data = crud.get_dealer_product_by_business_id(business_id=product_business_id)
                if product_data:  # 如果有这条数据
                    # 执行删除
                    try:
                        crud.delete_dealer_product_by_business_id(data_id=product_business_id)
                    except:
                        logger.error(
                            "删除 经销商产品{} 出错，详细的出错信息为：{}".format(
                                product_business_id, traceback.format_exc()
                            )
                        )
                        return restful.server_error(
                            message=multiply_delete_product_failed, data={"traceback": traceback.format_exc()}
                        )

        return restful.ok(message=multiply_delete_product_success)
    except:
        return restful.server_error(
            message=multiply_delete_product_failed, data={"traceback": traceback.format_exc()}
        )
