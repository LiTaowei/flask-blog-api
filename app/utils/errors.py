"""全局异常处理：404/500 等错误统一返回友好 JSON，不暴露原始报错"""
from werkzeug.exceptions import HTTPException

from app.utils.response import error


def register_error_handlers(app):
    @app.errorhandler(404)
    def not_found(e):
        return error(message="资源不存在", code=404, http_status=404)

    @app.errorhandler(405)
    def method_not_allowed(e):
        return error(message="请求方法不允许", code=405, http_status=405)

    @app.errorhandler(500)
    def internal_error(e):
        return error(message="服务器内部错误", code=500, http_status=500)

    @app.errorhandler(Exception)
    def handle_exception(e):
        # HTTP 异常按自身状态码返回，其余一律 500
        if isinstance(e, HTTPException):
            return error(message=e.description, code=e.code, http_status=e.code)
        return error(message="服务器内部错误", code=500, http_status=500)


def register_jwt_handlers(jwt):
    """JWT 相关错误统一返回 401"""
    @jwt.unauthorized_loader
    def missing_token(reason):
        return error(message="缺少访问令牌，请先登录", code=401, http_status=401)

    @jwt.expired_token_loader
    def expired_token(jwt_header, jwt_payload):
        return error(message="令牌已过期，请重新登录", code=401, http_status=401)

    @jwt.invalid_token_loader
    def invalid_token(reason):
        return error(message="令牌非法，请重新登录", code=401, http_status=401)
