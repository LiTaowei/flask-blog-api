"""数据库模型：User（用户）与 Article（文章），一对多关系"""
from datetime import datetime

import bcrypt

from app import db


class User(db.Model):
    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(50), unique=True, nullable=False, comment="用户名，全局唯一")
    password_hash = db.Column(db.String(128), nullable=False, comment="密码哈希值")
    created_at = db.Column(db.DateTime, default=datetime.now, comment="注册时间")

    # 一对多：一个用户可以有多篇文章
    articles = db.relationship("Article", backref="author", lazy=True)

    def set_password(self, password: str):
        """bcrypt 加盐哈希后存储"""
        self.password_hash = bcrypt.hashpw(
            password.encode("utf-8"), bcrypt.gensalt()
        ).decode("utf-8")

    def check_password(self, password: str) -> bool:
        """校验密码是否匹配"""
        return bcrypt.checkpw(
            password.encode("utf-8"), self.password_hash.encode("utf-8")
        )

    def to_dict(self):
        return {
            "id": self.id,
            "username": self.username,
            "created_at": self.created_at.strftime("%Y-%m-%d %H:%M:%S"),
        }


class Article(db.Model):
    __tablename__ = "article"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(100), nullable=False, comment="文章标题")
    content = db.Column(db.Text, nullable=False, comment="文章内容")
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False, comment="作者 ID")
    created_at = db.Column(db.DateTime, default=datetime.now, comment="发布时间")
    updated_at = db.Column(
        db.DateTime, default=datetime.now, onupdate=datetime.now, comment="最后修改时间"
    )

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "content": self.content,
            "author": self.author.username if self.author else None,
            "user_id": self.user_id,
            "created_at": self.created_at.strftime("%Y-%m-%d %H:%M:%S"),
            "updated_at": self.updated_at.strftime("%Y-%m-%d %H:%M:%S"),
        }
