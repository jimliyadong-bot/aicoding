# FastAPI 项目骨架 - 运行指南

## 📋 生成的文件清单

### 新增文件(8 个)

| 文件路径 | 说明 | 行数 |
|---|---|---|
| [`server/app/schemas/response.py`](file:///d:/Projects/ai-develop/workspace/antigravity/yiya_ai_reader/server/app/schemas/response.py) | 统一响应模型 | ~90 行 |
| [`server/app/core/exceptions.py`](file:///d:/Projects/ai-develop/workspace/antigravity/yiya_ai_reader/server/app/core/exceptions.py) | 全局异常处理 | ~170 行 |
| [`server/app/middleware/trace_id.py`](file:///d:/Projects/ai-develop/workspace/antigravity/yiya_ai_reader/server/app/middleware/trace_id.py) | Trace ID 中间件 | ~45 行 |
| [`server/app/api/v1/health.py`](file:///d:/Projects/ai-develop/workspace/antigravity/yiya_ai_reader/server/app/api/v1/health.py) | 健康检查路由 | ~50 行 |
| [`server/app/models/base.py`](file:///d:/Projects/ai-develop/workspace/antigravity/yiya_ai_reader/server/app/models/base.py) | 数据库模型基类 | ~60 行 |
| [`server/alembic.ini`](file:///d:/Projects/ai-develop/workspace/antigravity/yiya_ai_reader/server/alembic.ini) | Alembic 配置文件 | ~120 行 |
| [`server/alembic/env.py`](file:///d:/Projects/ai-develop/workspace/antigravity/yiya_ai_reader/server/alembic/env.py) | Alembic 环境配置 | ~90 行 |
| [`server/alembic/script.py.mako`](file:///d:/Projects/ai-develop/workspace/antigravity/yiya_ai_reader/server/alembic/script.py.mako) | 迁移脚本模板 | ~25 行 |
| [`docker-compose.yml`](file:///d:/Projects/ai-develop/workspace/antigravity/yiya_ai_reader/docker-compose.yml) | Docker Compose 配置 | ~110 行 |

### 修改文件(3 个)

| 文件路径 | 修改内容 |
|---|---|
| [`server/.env.example`](file:///d:/Projects/ai-develop/workspace/antigravity/yiya_ai_reader/server/.env.example) | 添加 Trace ID、连接池配置和详细注释 |
| [`server/requirements.txt`](file:///d:/Projects/ai-develop/workspace/antigravity/yiya_ai_reader/server/requirements.txt) | 添加 httpx,重新组织依赖分类 |
| [`server/app/main.py`](file:///d:/Projects/ai-develop/workspace/antigravity/yiya_ai_reader/server/app/main.py) | 注册异常处理器、中间件和健康检查路由 |

---

## 🚀 本地运行

### 方式 1: 直接运行(推荐用于开发)

#### 步骤 1: 安装依赖

```bash
# 进入 server 目录
cd d:\Projects\ai-develop\workspace\antigravity\yiya_ai_reader\server

# 创建虚拟环境(可选但推荐)
python -m venv venv

# 激活虚拟环境
# Windows PowerShell:
.\venv\Scripts\Activate.ps1
# Windows CMD:
.\venv\Scripts\activate.bat

# 安装依赖
pip install -r requirements.txt
```

**命令用途**: 安装 FastAPI 及所有依赖包,包括 SQLAlchemy、Redis、Alembic 等。

#### 步骤 2: 配置环境变量

```bash
# 复制环境变量模板
copy .env.example .env

# 编辑 .env 文件,修改数据库和 Redis 连接信息
# 注意: 确保 MySQL 和 Redis 服务已启动
```

**命令用途**: 创建本地环境配置文件,需要根据实际环境修改数据库连接信息。

#### 步骤 3: 初始化数据库

```bash
# 确保 MySQL 服务已启动,并执行建表 SQL
mysql -u root -p < ../docs/database/schema_v2.sql
```

**命令用途**: 执行数据库初始化脚本,创建所有表和初始化数据。

#### 步骤 4: 启动服务

```bash
# 启动 FastAPI 服务
python -m app.main

# 或使用 uvicorn 直接启动(支持热重载)
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**命令用途**: 启动 FastAPI 开发服务器,`--reload` 参数会在代码修改时自动重启。

---

### 方式 2: Docker Compose 运行(推荐用于生产)

#### 步骤 1: 启动所有服务

```bash
# 回到项目根目录
cd d:\Projects\ai-develop\workspace\antigravity\yiya_ai_reader

# 启动所有服务(MySQL + Redis + FastAPI)
docker-compose up -d
```

**命令用途**: 
- 启动 3 个 Docker 容器:MySQL 8.0、Redis 7.0 和 FastAPI 应用
- `-d` 参数表示后台运行
- 首次运行会自动构建镜像和初始化数据库

#### 步骤 2: 查看日志

```bash
# 查看所有服务日志
docker-compose logs -f

# 只查看 FastAPI 服务日志
docker-compose logs -f server
```

**命令用途**: 实时查看服务运行日志,`-f` 参数表示持续输出。

#### 步骤 3: 停止服务

```bash
# 停止所有服务
docker-compose down

# 停止并删除数据卷(慎用,会删除数据库数据)
docker-compose down -v
```

**命令用途**: 停止并删除容器,`-v` 参数会同时删除数据卷。

---

## ✅ 验证步骤

### 1. 访问 API 文档

打开浏览器访问:

```
http://localhost:8000/docs
```

**预期结果**: 看到 Swagger UI 文档界面,包含健康检查接口。

![API 文档示例](https://via.placeholder.com/800x400?text=Swagger+UI+Documentation)

### 2. 测试健康检查接口

#### 使用浏览器

访问: `http://localhost:8000/api/v1/health`

#### 使用 curl

```bash
curl http://localhost:8000/api/v1/health
```

**预期响应**:

```json
{
  "code": 200,
  "message": "success",
  "data": {
    "status": "healthy",
    "database": "connected",
    "redis": "connected"
  },
  "trace_id": "550e8400-e29b-41d4-a716-446655440000"
}
```

### 3. 验证 Trace ID

查看响应头,应该包含 `X-Trace-ID`:

```bash
curl -I http://localhost:8000/api/v1/health
```

**预期响应头**:

```
HTTP/1.1 200 OK
content-type: application/json
x-trace-id: 550e8400-e29b-41d4-a716-446655440000
```

### 4. 测试异常处理

访问一个不存在的路由:

```bash
curl http://localhost:8000/api/v1/not-found
```

**预期响应**:

```json
{
  "code": 404,
  "message": "Not Found",
  "data": null,
  "trace_id": "550e8400-e29b-41d4-a716-446655440000"
}
```

### 5. 测试参数验证

创建一个测试接口(可选):

```python
# 在 health.py 中添加测试接口
@router.get("/test")
async def test_validation(age: int):
    return {"age": age}
```

访问并传入错误参数:

```bash
curl "http://localhost:8000/api/v1/test?age=abc"
```

**预期响应**:

```json
{
  "code": 400,
  "message": "参数验证失败",
  "data": {
    "errors": [
      {
        "field": "query.age",
        "message": "value is not a valid integer",
        "type": "type_error.integer"
      }
    ]
  },
  "trace_id": "550e8400-e29b-41d4-a716-446655440000"
}
```

---

## 🔧 Alembic 数据库迁移

### 初始化迁移(已完成)

Alembic 配置已经生成,无需再次初始化。

### 创建迁移脚本

```bash
cd server

# 自动生成迁移脚本
alembic revision --autogenerate -m "Initial migration"
```

**命令用途**: 根据模型自动生成数据库迁移脚本。

### 执行迁移

```bash
# 升级到最新版本
alembic upgrade head

# 回滚一个版本
alembic downgrade -1

# 查看迁移历史
alembic history
```

**命令用途**: 执行数据库迁移,升级或回滚数据库结构。

---

## 🔄 回滚方案

### 方案 1: Git 回滚(推荐)

```bash
# 查看修改的文件
git status

# 回滚所有修改
git checkout HEAD -- server/ docker-compose.yml

# 或回滚到特定提交
git reset --hard <commit-hash>
```

### 方案 2: 手动删除新增文件

```bash
# 删除新增的文件
rm server/app/schemas/response.py
rm server/app/core/exceptions.py
rm server/app/middleware/trace_id.py
rm server/app/api/v1/health.py
rm server/app/models/base.py
rm server/alembic.ini
rm -rf server/alembic
rm docker-compose.yml

# 恢复修改的文件(需要有备份)
```

### 方案 3: Docker Compose 清理

```bash
# 停止并删除所有容器和数据卷
docker-compose down -v

# 删除镜像
docker rmi yiya_ai_reader-server
```

---

## 📊 项目结构(更新后)

```
server/
├── alembic/                    # Alembic 迁移目录(新增)
│   ├── env.py                 # 迁移环境配置
│   ├── script.py.mako         # 迁移脚本模板
│   └── versions/              # 迁移版本目录
├── app/
│   ├── api/
│   │   └── v1/
│   │       └── health.py      # 健康检查路由(新增)
│   ├── core/
│   │   ├── config.py          # 配置管理
│   │   └── exceptions.py      # 全局异常处理(新增)
│   ├── db/
│   │   ├── session.py         # 数据库会话
│   │   └── redis.py           # Redis 客户端
│   ├── middleware/
│   │   └── trace_id.py        # Trace ID 中间件(新增)
│   ├── models/
│   │   └── base.py            # 数据库模型基类(新增)
│   ├── schemas/
│   │   └── response.py        # 统一响应模型(新增)
│   └── main.py                # 应用入口(已更新)
├── alembic.ini                # Alembic 配置(新增)
├── .env.example               # 环境变量模板(已更新)
├── requirements.txt           # 依赖列表(已更新)
└── README.md

docker-compose.yml             # Docker Compose 配置(新增)
```

---

## 🎯 核心功能说明

### 1. 统一响应格式

所有 API 响应都遵循统一格式:

```python
{
    "code": 200,           # 状态码
    "message": "success",  # 响应消息
    "data": {...},         # 响应数据
    "trace_id": "xxx"      # 请求追踪ID
}
```

### 2. 全局异常处理

自动捕获并处理以下异常:
- `APIException` - 自定义 API 异常
- `HTTPException` - HTTP 异常
- `RequestValidationError` - 参数验证异常
- `Exception` - 其他所有异常

### 3. Trace ID 追踪

每个请求自动生成唯一 trace_id:
- 从请求头 `X-Trace-ID` 获取或自动生成
- 存储在 `request.state.trace_id`
- 在响应头和响应体中返回

### 4. 健康检查

`GET /api/v1/health` 接口检查:
- 服务状态
- 数据库连接
- Redis 连接

---

## ⚠️ 注意事项

1. **环境变量**: 生产环境必须修改 `SECRET_KEY` 为强随机字符串
2. **数据库连接**: 确保 MySQL 和 Redis 服务已启动
3. **端口冲突**: 确保 3306、6379、8000 端口未被占用
4. **Docker 网络**: Docker Compose 中服务使用服务名作为主机名
5. **Alembic 迁移**: 修改模型后需要生成并执行迁移脚本

---

## 📞 问题排查

### 问题 1: 无法连接数据库

**错误**: `Can't connect to MySQL server`

**解决**:
1. 检查 MySQL 服务是否启动
2. 检查 `.env` 中的数据库连接信息
3. 检查防火墙设置

### 问题 2: Redis 连接失败

**错误**: `Error connecting to Redis`

**解决**:
1. 检查 Redis 服务是否启动
2. 检查 `.env` 中的 Redis 配置
3. 使用 `redis-cli ping` 测试连接

### 问题 3: 依赖安装失败

**错误**: `ERROR: Could not find a version that satisfies the requirement`

**解决**:
```bash
# 升级 pip
pip install --upgrade pip

# 使用国内镜像源
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
```

### 问题 4: Docker 构建失败

**错误**: `failed to solve with frontend dockerfile.v0`

**解决**:
```bash
# 清理 Docker 缓存
docker system prune -a

# 重新构建
docker-compose build --no-cache
```

---

## 🎉 下一步

1. ✅ 访问 `http://localhost:8000/docs` 查看 API 文档
2. ✅ 测试健康检查接口
3. ✅ 开始开发业务功能(用户、角色、权限等)
4. ✅ 使用 Alembic 管理数据库迁移
5. ✅ 编写单元测试和集成测试
