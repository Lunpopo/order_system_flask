#!/usr/bin/env python
# encoding: utf8
# @Author  ：xie.yx
# @Date    ：2022/3/23 13:42
# encoding: utf8
import time

from flask import Response, json


class HttpCode(object):
    ok = 200
    paramserror = 400
    unauth = 401
    methoderror = 405
    servererror = 500


def result(status=HttpCode.ok, code=20000, message="", data=None, succ=True, kwargs=None):
    json_dict = {"code": code, "msg": message, "data": data, "succ": succ, "ts": int(time.time() * 1000)}

    if kwargs and isinstance(kwargs, dict) and kwargs.keys():
        json_dict.update(kwargs)

    # return Response(status_code=code, content=json_dict)
    return Response(json.dumps(json_dict), content_type='application/json', status=status)


# 正常返回
def ok(message='', data=None):
    return result(code=20000, message=message, data=data)


# 参数错误
def params_error(message="", data=None):
    return result(code=HttpCode.paramserror, message=message, data=data, succ=False)


# 未授权错误
def unauth(message="", data=None):
    return result(code=HttpCode.unauth, message=message, data=data, succ=False)


# 方法错误
def method_error(message="", data=None):
    return result(code=HttpCode.methoderror, message=message, data=data, succ=False)


# 服务器错误
def server_error(message="", data=None):
    return result(code=HttpCode.servererror, message=message, data=data, succ=False)
