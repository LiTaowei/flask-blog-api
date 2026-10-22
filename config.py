"""项目配置文件

数据库、JWT、密钥等敏感配置均通过环境变量读取。可在项目根目录创建 .env 文件
（参考 .env.example）进行本地配置。注意：.env 含真实密码，切勿提交到 Git。
"""
import os
from datetime import timedelta

from dotenv import load_dotenv

# 加载项目根目录下的 .env（若存在）
load_dotenv()


class Config:
    # Flask
    SECRET_KEY = os.environ.get("SECRET_KEY", "change-me")
    DEBUG = os.environ.get("FLASK_DEBUG", "0") == "1"

    # 数据库：通过环境变量 DATABASE_URL 配置
    # 示例（MySQL）：mysql+pymysql://用户名:密码@主机:端口/数据库名
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL",
        "mysql+pymysql://user:password@localhost:3306/blog_db?charset=utf8mb4",
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {"pool_pre_ping": True}

    # JWT
    JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY", "change-me")
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(days=7)  # Token 有效期 7 天

    # 分页默认值
    DEFAULT_PAGE = 1
    DEFAULT_PAGE_SIZE = 10
    MAX_PAGE_SIZE = 100
