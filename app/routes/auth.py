"""用户认证模块：注册、登录（JWT）"""
from flask import Blueprint, request
from flask_jwt_extended import create_access_token

from app import db
from app.models import User
from app.utils.response import error, success

auth_bp = Blueprint("auth", __name__)


@auth_bp.post("/register")
def register():
    """用户注册：用户名唯一，密码 bcrypt 加密存储"""
    data = request.get_json(silent=True) or {}
    username = (data.get("username") or "").strip()
    password = data.get("password") or ""

    # 参数校验
    if not username or not password:
        return error(message="用户名和密码不能为空", code=400, http_status=400)

    # 用户名唯一性校验
    if User.query.filter_by(username=username).first():
        return error(message="用户名已存在", code=400, http_status=400)

    user = User(username=username)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()

    return success(
        data=user.to_dict(), message="注册成功", code=201, http_status=201
    )


@auth_bp.post("/login")
def login():
    """用户登录：校验通过返回 JWT Token（有效期 7 天）"""
    data = request.get_json(silent=True) or {}
    username = (data.get("username") or "").strip()
    password = data.get("password") or ""

    if not username or not password:
        return error(message="用户名和密码不能为空", code=400, http_status=400)

    user = User.query.filter_by(username=username).first()
    if not user or not user.check_password(password):
        return error(message="用户名或密码错误", code=401, http_status=401)

    # identity 使用字符串，兼容 JWT 规范
    token = create_access_token(identity=str(user.id))
    return success(
        data={"token": token, "user": user.to_dict()},
        message="登录成功",
        code=200,
        http_status=200,
    )
