"""应用工厂：创建并配置 Flask 应用实例"""
from flask import Flask, jsonify
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_sqlalchemy import SQLAlchemy

from config import Config

db = SQLAlchemy()
jwt = JWTManager()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # 初始化扩展
    db.init_app(app)
    jwt.init_app(app)
    CORS(app)  # 允许跨域，便于前端/Postman 调试

    @app.get("/health")
    def health_check():
        return jsonify(code=200, message="success", data={"status": "ok"})

    # 注册蓝图
    from app.routes.auth import auth_bp
    from app.routes.articles import article_bp

    app.register_blueprint(auth_bp, url_prefix="/api/v1/auth")
    app.register_blueprint(article_bp, url_prefix="/api/v1/articles")

    # 注册全局错误处理
    from app.utils.errors import register_error_handlers

    register_error_handlers(app)

    # 注册 JWT 错误处理（Token 缺失/过期/非法统一返回 401）
    from app.utils.errors import register_jwt_handlers

    register_jwt_handlers(jwt)

    # 首次启动自动建表
    with app.app_context():
        db.create_all()

    return app
