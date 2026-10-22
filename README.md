# 个人博客 API（flask-blog-api）

基于 Flask 的纯后端 **RESTful 博客 API**，提供用户注册登录（JWT 认证）与文章的增删改查，支持分页、作者权限隔离。项目无前端页面，可使用 Postman / Apifox 进行接口调试。

## 功能特性



* **用户认证**：注册、登录，密码使用 bcrypt 加盐哈希存储，登录签发 JWT（有效期 7 天）

* **文章管理**：文章的发布、查询、修改、删除（CRUD）

* **权限控制**：仅作者本人可修改 / 删除自己的文章，防止越权

* **分页查询**：文章列表强制分页，支持自定义页码与每页条数（上限 100）

* **统一响应**：所有接口返回统一的 `{code, message, data}` JSON 格式

* **安全设计**：SQLAlchemy ORM 防 SQL 注入、全局异常处理不暴露堆栈、敏感配置走环境变量

## 技术栈



| 分类     | 技术                            |
| ------ | ----------------------------- |
| 语言     | Python 3.12                   |
| Web 框架 | Flask 3.1                     |
| ORM    | Flask-SQLAlchemy + SQLAlchemy |
| 认证     | Flask-JWT-Extended（JWT）       |
| 跨域     | Flask-CORS                    |
| 密码加密   | bcrypt                        |
| 数据库    | MySQL 8.0（PyMySQL 驱动）         |
| 配置     | python-dotenv（环境变量）           |

## 项目结构



```
flask\_project\_1/

├── app/

│   ├── \_\_init\_\_.py          # 应用工厂：初始化扩展、注册蓝图、自动建表

│   ├── models.py            # 数据模型：User、Article

│   ├── routes/

│   │   ├── auth.py          # 认证蓝图：注册、登录

│   │   └── articles.py      # 文章蓝图：CRUD + 分页 + 权限控制

│   └── utils/

│       ├── response.py      # 统一 JSON 响应格式

│       └── errors.py        # 全局异常处理

├── config.py                # 配置（从环境变量读取）

├── run.py                   # 启动入口

├── requirements.txt         # 依赖清单

├── .env.example             # 环境变量模板

└── LICENSE                  # MIT 许可证
```

## 快速开始

### 1. 环境要求



* Python 3.12+

* MySQL 8.0+

### 2. 克隆项目



```
git clone https://github.com/LiTaowei/flask-blog-api.git

cd flask-blog-api
```

### 3. 创建虚拟环境并安装依赖



```
python -m venv .venv

.\\.venv\Scripts\Activate.ps1

pip install -r requirements.txt
```

### 4. 配置环境变量

复制 `.env.example` 为 `.env`，并填入你自己的数据库密码与密钥：



```
Copy-Item .env.example .env
```

`.env` 示例：



```
SECRET\_KEY=替换为随机字符串

FLASK\_DEBUG=1

DATABASE\_URL=mysql+pymysql://root:你的密码@localhost:3306/blog\_db?charset=utf8mb4

JWT\_SECRET\_KEY=替换为随机字符串
```

> 密钥可用 
>
> `python -c "import secrets;print(secrets.token_hex(32))"`
>
>  生成。

### 5. 创建数据库

应用会自动建表，但需先手动创建数据库（字符集 utf8mb4）：



```
CREATE DATABASE blog\_db CHARACTER SET utf8mb4 COLLATE utf8mb4\_unicode\_ci;
```

### 6. 启动服务



```
python run.py
```

启动后访问 `http://localhost:5000`，看到服务响应即运行成功。

## 接口文档

统一前缀：`/api/v1`，统一响应格式：



```
{

&#x20; "code": 200,

&#x20; "message": "success",

&#x20; "data": {}

}
```

### 用户模块



| 功能   | 方法   | URL                     | 权限 | 请求体                                      |
| ---- | ---- | ----------------------- | -- | ---------------------------------------- |
| 用户注册 | POST | `/api/v1/auth/register` | 公开 | `{"username": "...", "password": "..."}` |
| 用户登录 | POST | `/api/v1/auth/login`    | 公开 | `{"username": "...", "password": "..."}` |

### 文章模块



| 功能   | 方法     | URL                               | 权限  |
| ---- | ------ | --------------------------------- | --- |
| 文章列表 | GET    | `/api/v1/articles?page=1&size=10` | 公开  |
| 文章详情 | GET    | `/api/v1/articles/{id}`           | 公开  |
| 发布文章 | POST   | `/api/v1/articles`                | 需登录 |
| 修改文章 | PATCH  | `/api/v1/articles/{id}`           | 仅作者 |
| 删除文章 | DELETE | `/api/v1/articles/{id}`           | 仅作者 |

### 认证方式

受保护接口需在请求头携带 JWT：



```
Authorization: Bearer <登录时返回的 token>
```

### 使用示例

注册：



```
curl -X POST http://localhost:5000/api/v1/auth/register \\

&#x20; -H "Content-Type: application/json" \\

&#x20; -d '{"username":"zhangsan","password":"123456"}'
```

登录：



```
curl -X POST http://localhost:5000/api/v1/auth/login \\

&#x20; -H "Content-Type: application/json" \\

&#x20; -d '{"username":"zhangsan","password":"123456"}'
```

## 错误码说明



| HTTP 状态码 | 含义    | 触发场景                    |
| -------- | ----- | ----------------------- |
| 400      | 参数错误  | 用户名 / 密码为空、内容为空、用户名重复   |
| 401      | 未认证   | 密码错误、Token 缺失 / 过期 / 非法 |
| 403      | 无权限   | 操作他人文章                  |
| 404      | 不存在   | 资源 / 路由不存在              |
| 405      | 方法不允许 | 使用了错误的 HTTP 方法          |
| 500      | 服务器错误 | 服务端未预期异常                |

## 许可证

本项目基于 [MIT License](LICENSE) 开源。