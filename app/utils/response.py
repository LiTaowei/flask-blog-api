"""统一 JSON 响应格式：{code, message, data}"""
from flask import jsonify


def success(data=None, message="success", code=200, http_status=200):
    """成功响应"""
    return jsonify({"code": code, "message": message, "data": data}), http_status


def error(message="error", code=400, http_status=400, data=None):
    """失败响应"""
    return jsonify({"code": code, "message": message, "data": data}), http_status
