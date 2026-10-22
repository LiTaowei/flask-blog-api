"""博客文章模块：CRUD + 分页 + 作者权限控制"""
from flask import Blueprint, current_app, request
from flask_jwt_extended import get_jwt_identity, jwt_required

from app import db
from app.models import Article
from app.utils.response import error, success

article_bp = Blueprint("articles", __name__)


def _get_pagination_args():
    """解析分页参数，限制最大每页数量"""
    try:
        page = int(request.args.get("page", current_app.config["DEFAULT_PAGE"]))
        size = int(request.args.get("size", current_app.config["DEFAULT_PAGE_SIZE"]))
    except (TypeError, ValueError):
        page, size = 1, current_app.config["DEFAULT_PAGE_SIZE"]
    page = max(page, 1)
    size = min(max(size, 1), current_app.config["MAX_PAGE_SIZE"])
    return page, size


@article_bp.get("")
def list_articles():
    """获取文章列表（游客可访问，强制分页）"""
    page, size = _get_pagination_args()
    pagination = Article.query.order_by(Article.created_at.desc()).paginate(
        page=page, per_page=size, error_out=False
    )
    return success(
        data={
            "items": [a.to_dict() for a in pagination.items],
            "total": pagination.total,
            "page": pagination.page,
            "size": pagination.per_page,
            "pages": pagination.pages,
        }
    )


@article_bp.get("/<int:article_id>")
def get_article(article_id):
    """获取单篇文章详情（游客可访问）"""
    article = db.session.get(Article, article_id)
    if not article:
        return error(message="文章不存在", code=404, http_status=404)
    return success(data=article.to_dict())


@article_bp.post("")
@jwt_required()
def create_article():
    """发布新文章（需登录，自动绑定当前用户为作者）"""
    data = request.get_json(silent=True) or {}
    title = (data.get("title") or "").strip()
    content = (data.get("content") or "").strip()

    if not title or not content:
        return error(message="标题和内容不能为空", code=400, http_status=400)

    current_user_id = int(get_jwt_identity())
    article = Article(title=title, content=content, user_id=current_user_id)
    db.session.add(article)
    db.session.commit()

    return success(
        data=article.to_dict(), message="发布成功", code=201, http_status=201
    )


@article_bp.patch("/<int:article_id>")
@jwt_required()
def update_article(article_id):
    """修改文章（需登录 + 仅作者本人，支持部分字段更新）"""
    article = db.session.get(Article, article_id)
    if not article:
        return error(message="文章不存在", code=404, http_status=404)

    # 防越权：只有作者可以修改
    current_user_id = int(get_jwt_identity())
    if article.user_id != current_user_id:
        return error(message="无权操作他人的文章", code=403, http_status=403)

    data = request.get_json(silent=True) or {}
    title = data.get("title")
    content = data.get("content")

    # 部分更新：传了才校验、才更新
    if title is not None:
        title = title.strip()
        if not title:
            return error(message="标题不能为空", code=400, http_status=400)
        article.title = title
    if content is not None:
        content = content.strip()
        if not content:
            return error(message="内容不能为空", code=400, http_status=400)
        article.content = content

    db.session.commit()
    return success(data=article.to_dict(), message="修改成功")


@article_bp.delete("/<int:article_id>")
@jwt_required()
def delete_article(article_id):
    """删除文章（需登录 + 仅作者本人）"""
    article = db.session.get(Article, article_id)
    if not article:
        return error(message="文章不存在", code=404, http_status=404)

    current_user_id = int(get_jwt_identity())
    if article.user_id != current_user_id:
        return error(message="无权操作他人的文章", code=403, http_status=403)

    db.session.delete(article)
    db.session.commit()
    return success(message="删除成功", code=204, http_status=200)
