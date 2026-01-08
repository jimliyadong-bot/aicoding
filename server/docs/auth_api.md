# 管理端认证接口 - 运行指南

## 📋 生成的文件清单

### 新增文件(9 个)

| 文件路径 | 说明 | 核心功能 |
|---|---|---|
| `app/utils/password.py` | 密码哈希工具 | bcrypt 加密和验证 |
| `app/utils/jwt.py` | JWT 工具类 | 生成和验证 Access/Refresh Token |
| `app/models/user.py` | 用户模型 | AdminUser 模型定义 |
| `app/schemas/auth.py` | 认证 Schema | 登录、刷新、用户信息等 Schema |
| `app/services/auth_service.py` | 认证服务 | 登录、刷新、登出业务逻辑 |
| `app/core/dependencies.py` | 认证依赖 | 获取当前用户依赖 |
| `app/api/v1/admin/auth.py` | 认证路由 | 4 个认证接口 |
| `app/api/v1/admin/__init__.py` | 包初始化 | admin 包 |
| `scripts/seed_admin.py` | 初始化脚本 | 创建管理员账号 |

### 修改文件(1 个)

| 文件路径 | 修改内容 |
|---|---|
| `app/main.py` | 注册管理端认证路由 |

---

## 🚀 快速开始

### 步骤 1: 初始化管理员账号

**方式 1: 使用 Seed 脚本(推荐)**

```bash
# 进入 server 目录
cd d:\Projects\ai-develop\workspace\antigravity\yiya_ai_reader\server

# 运行初始化脚本
set ADMIN_USERNAME=admin
set ADMIN_PASSWORD=your-strong-password
python scripts\seed_admin.py
```

**命令用途**: 使用 `ADMIN_USERNAME` / `ADMIN_PASSWORD` 环境变量创建管理员账号,如果已存在则跳过。

**预期输出**:
```
开始初始化管理员账号...
管理员账号创建成功!
   用户名: admin
   ID: 1
   请妥善保管管理员凭据
```

**方式 2: 手动插入数据库**

```sql
-- 使用 bcrypt 哈希后的密码(示例)
INSERT INTO admin_user (username, password_hash, real_name, status) VALUES
('<ADMIN_USERNAME>', '<BCRYPT_PASSWORD_HASH>', '超级管理员', 1);
```

### 步骤 2: 启动服务

```bash
# 确保 MySQL 和 Redis 已启动

# 启动 FastAPI 服务
python -m app.main

# 或使用 uvicorn
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**命令用途**: 启动 FastAPI 开发服务器。

---

## ✅ API 测试

### 1. 登录接口

**请求**:
```bash
curl -X POST http://localhost:8000/api/v1/admin/auth/login \
  -H "Content-Type: application/json" \
  -d "{\"username\":\"<ADMIN_USERNAME>\",\"password\":\"<ADMIN_PASSWORD>\"}"
```

**预期响应**:
```json
{
  "code": 200,
  "message": "登录成功",
  "data": {
    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxIiwidXNlcm5hbWUiOiJhZG1pbiIsImV4cCI6MTcwNDYyMTYwMCwiaWF0IjoxNzA0NjE0NDAwLCJ0eXBlIjoiYWNjZXNzIn0.xxx",
    "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxIiwidXNlcm5hbWUiOiJhZG1pbiIsImV4cCI6MTcwNTIxOTIwMCwiaWF0IjoxNzA0NjE0NDAwLCJ0eXBlIjoicmVmcmVzaCJ9.xxx",
    "token_type": "Bearer",
    "expires_in": 7200
  },
  "trace_id": "550e8400-e29b-41d4-a716-446655440000"
}
```

**保存 Token**:
```bash
# 保存 access_token 和 refresh_token 供后续使用
export ACCESS_TOKEN="<access_token>"
export REFRESH_TOKEN="<refresh_token>"
```

### 2. 获取当前用户信息

**请求**:
```bash
curl -X GET http://localhost:8000/api/v1/admin/auth/me \
  -H "Authorization: Bearer $ACCESS_TOKEN"
```

**预期响应**:
```json
{
  "code": 200,
  "message": "获取用户信息成功",
  "data": {
    "id": 1,
    "username": "admin",
    "real_name": "超级管理员",
    "email": null,
    "phone": null,
    "avatar": null,
    "status": 1,
    "created_at": "2026-01-07T10:00:00"
  },
  "trace_id": "550e8400-e29b-41d4-a716-446655440000"
}
```

### 3. 刷新 Access Token

**请求**:
```bash
curl -X POST http://localhost:8000/api/v1/admin/auth/refresh \
  -H "Content-Type: application/json" \
  -d "{\"refresh_token\":\"$REFRESH_TOKEN\"}"
```

**预期响应**:
```json
{
  "code": 200,
  "message": "Token 刷新成功",
  "data": {
    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.xxx",
    "token_type": "Bearer",
    "expires_in": 7200
  },
  "trace_id": "550e8400-e29b-41d4-a716-446655440000"
}
```

### 4. 登出

**请求**:
```bash
curl -X POST http://localhost:8000/api/v1/admin/auth/logout \
  -H "Authorization: Bearer $ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d "{\"refresh_token\":\"$REFRESH_TOKEN\"}"
```

**预期响应**:
```json
{
  "code": 200,
  "message": "登出成功",
  "data": null,
  "trace_id": "550e8400-e29b-41d4-a716-446655440000"
}
```

---

## 🔍 验证步骤

### 1. 访问 API 文档

打开浏览器访问:
```
http://localhost:8000/docs
```

在 Swagger UI 中可以看到新增的认证接口:
- `POST /api/v1/admin/auth/login`
- `POST /api/v1/admin/auth/refresh`
- `GET /api/v1/admin/auth/me`
- `POST /api/v1/admin/auth/logout`

### 2. 测试登录流程

1. 调用登录接口,获取 Token
2. 使用 Access Token 调用 `/me` 接口
3. 验证返回的用户信息正确

### 3. 测试 Token 刷新

1. 使用 Refresh Token 调用刷新接口
2. 获取新的 Access Token
3. 使用新 Token 访问受保护接口

### 4. 测试登出功能

1. 调用登出接口
2. 尝试使用已登出的 Refresh Token 刷新
3. 应该返回 401 错误

### 5. 测试错误场景

**错误的用户名或密码**:
```bash
curl -X POST http://localhost:8000/api/v1/admin/auth/login \
  -H "Content-Type: application/json" \
  -d "{\"username\":\"admin\",\"password\":\"wrong\"}"
```

**预期响应**:
```json
{
  "code": 401,
  "message": "用户名或密码错误",
  "data": null,
  "trace_id": "xxx"
}
```

**无效的 Token**:
```bash
curl -X GET http://localhost:8000/api/v1/admin/auth/me \
  -H "Authorization: Bearer invalid_token"
```

**预期响应**:
```json
{
  "code": 401,
  "message": "Token 无效或已过期",
  "data": null,
  "trace_id": "xxx"
}
```

---

## 🔧 Redis 验证

### 查看 Refresh Token

```bash
# 连接 Redis
redis-cli

# 查看所有 refresh_token
KEYS refresh_token:*

# 查看特定用户的 token
GET refresh_token:1:<refresh_token>
```

### 查看黑名单

```bash
# 查看所有黑名单 token
KEYS token:blacklist:*

# 查看特定 token 是否在黑名单
GET token:blacklist:<refresh_token>
```

---

## 🔄 回滚方案

### 删除新增文件

```bash
cd server

# 删除新增的文件
rm app/utils/password.py
rm app/utils/jwt.py
rm app/models/user.py
rm app/schemas/auth.py
rm app/services/auth_service.py
rm app/core/dependencies.py
rm -r app/api/v1/admin
rm scripts/seed_admin.py
```

### 恢复修改文件

```bash
# 恢复 main.py
git checkout HEAD -- app/main.py
```

### 删除数据库数据

```sql
DELETE FROM admin_user WHERE username = 'admin';
```

### 清理 Redis

```bash
redis-cli FLUSHDB
```

---

## 📊 技术要点

### 1. 密码安全

- 使用 bcrypt 哈希算法
- 自动加盐,防止彩虹表攻击
- 计算成本可调(rounds=12)

### 2. JWT 双 Token 机制

| Token 类型 | 有效期 | 用途 | 存储位置 |
|---|---|---|---|
| Access Token | 2 小时 | API 访问鉴权 | 客户端 |
| Refresh Token | 7 天 | 刷新 Access Token | 客户端 + Redis |

### 3. Token 黑名单

- 登出时将 Refresh Token 加入黑名单
- 使用 Redis 存储,自动过期
- 刷新 Token 时检查黑名单

### 4. 认证流程

```
登录 → 生成 Token → 访问 API → Token 过期 → 刷新 Token → 继续访问
```

---

## ⚠️ 注意事项

1. **密码安全**: 生产环境必须使用强密码
2. **SECRET_KEY**: 生产环境必须使用强随机密钥
3. **HTTPS**: 生产环境必须使用 HTTPS
4. **Token 过期**: 根据实际需求调整过期时间
5. **限流**: 登录接口需要添加限流防止暴力破解
6. **审计日志**: 建议记录所有登录/登出操作

---

## 🎯 下一步

1. ✅ 测试所有认证接口
2. ✅ 实现角色权限管理
3. ✅ 添加登录限流
4. ✅ 添加审计日志
5. ✅ 实现前端登录页面
