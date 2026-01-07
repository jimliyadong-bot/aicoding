# YiYa AI Reader - 三端项目部署文档

## 环境要求

### 开发环境
- **Node.js**: >= 18.0.0
- **Python**: 3.13
- **MySQL**: 8.0
- **Redis**: 7.0

### 生产环境
- **Docker**: >= 20.10
- **Docker Compose**: >= 2.0

---

## 本地开发部署

### 1. 数据库初始化

```bash
# 登录 MySQL
mysql -u root -p

# 执行初始化脚本
source docs/database/schema.sql
```

### 2. 后端启动

```bash
# 进入后端目录
cd server

# 创建虚拟环境
python -m venv venv

# 激活虚拟环境 (Windows)
.\venv\Scripts\activate

# 激活虚拟环境 (Linux/Mac)
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt

# 复制环境变量
cp .env.example .env

# 修改 .env 文件中的数据库连接信息

# 启动服务
python -m app.main
# 或使用 uvicorn
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

后端服务将运行在: http://localhost:8000

### 3. 管理端启动

```bash
# 进入前端目录
cd admin-web

# 安装依赖
npm install

# 启动开发服务器
npm run dev
```

管理端将运行在: http://localhost:5173

默认管理员账号:
- 用户名: `admin`
- 密码: `admin123`

---

## Docker 部署

### 1. 一键启动所有服务

```bash
# 在项目根目录执行
cd deploy
docker-compose up -d
```

服务访问地址:
- 管理端: http://localhost
- 后端 API: http://localhost:8000
- MySQL: localhost:3306
- Redis: localhost:6379

### 2. 查看服务状态

```bash
docker-compose ps
```

### 3. 查看日志

```bash
# 查看所有服务日志
docker-compose logs -f

# 查看特定服务日志
docker-compose logs -f server
docker-compose logs -f admin
```

### 4. 停止服务

```bash
docker-compose down
```

### 5. 重启服务

```bash
docker-compose restart
```

---

## 验证步骤

### 1. 后端健康检查

```bash
# 访问健康检查接口
curl http://localhost:8000/health

# 预期响应
{"status": "healthy"}
```

### 2. 数据库连接验证

```bash
# 登录 MySQL
mysql -h localhost -u root -p

# 查看数据库
SHOW DATABASES;

# 使用数据库
USE yiya_ai_reader;

# 查看表
SHOW TABLES;

# 查看默认管理员
SELECT * FROM sys_user;
```

### 3. Redis 连接验证

```bash
# 连接 Redis
redis-cli

# 测试连接
PING

# 预期响应: PONG
```

### 4. 前端访问验证

1. 打开浏览器访问: http://localhost:5173 (开发) 或 http://localhost (Docker)
2. 使用默认账号登录: `admin` / `admin123`
3. 验证菜单是否正确显示
4. 验证用户管理等功能是否正常

---

## 回滚方案

### Docker 部署回滚

```bash
# 1. 停止当前服务
docker-compose down

# 2. 恢复数据库备份
mysql -u root -p yiya_ai_reader < backup.sql

# 3. 切换到上一个版本的代码
git checkout <previous-commit>

# 4. 重新构建并启动
docker-compose up -d --build
```

### 本地部署回滚

```bash
# 1. 停止服务 (Ctrl+C)

# 2. 恢复数据库
mysql -u root -p yiya_ai_reader < backup.sql

# 3. 切换代码版本
git checkout <previous-commit>

# 4. 重新安装依赖并启动
# 后端
cd server
pip install -r requirements.txt
python -m app.main

# 前端
cd admin-web
npm install
npm run dev
```

---

## 常见问题

### 1. 后端启动失败

**问题**: `ModuleNotFoundError: No module named 'xxx'`

**解决**: 
```bash
pip install -r requirements.txt
```

### 2. 数据库连接失败

**问题**: `Can't connect to MySQL server`

**解决**:
- 检查 MySQL 服务是否启动
- 检查 `.env` 文件中的数据库配置
- 检查防火墙设置

### 3. Redis 连接失败

**问题**: `Error connecting to Redis`

**解决**:
- 检查 Redis 服务是否启动
- 检查 `.env` 文件中的 Redis 配置

### 4. 前端无法访问后端

**问题**: `Network Error` 或 `CORS Error`

**解决**:
- 检查后端服务是否启动
- 检查 `vite.config.ts` 中的代理配置
- 检查后端 CORS 配置

---

## 生产环境注意事项

1. **修改默认密码**: 修改数据库 root 密码和默认管理员密码
2. **修改 SECRET_KEY**: 在 `.env` 中设置强随机密钥
3. **启用 HTTPS**: 配置 SSL 证书
4. **配置防火墙**: 只开放必要端口
5. **定期备份**: 设置数据库自动备份
6. **日志管理**: 配置日志轮转和监控
7. **性能优化**: 根据实际负载调整连接池大小

---

## 监控和维护

### 数据库备份

```bash
# 备份数据库
mysqldump -u root -p yiya_ai_reader > backup_$(date +%Y%m%d).sql

# 恢复数据库
mysql -u root -p yiya_ai_reader < backup_20260106.sql
```

### 日志查看

```bash
# 后端日志 (Docker)
docker-compose logs -f server

# Nginx 日志
docker exec yiya-admin tail -f /var/log/nginx/access.log
docker exec yiya-admin tail -f /var/log/nginx/error.log
```

---

## 技术支持

如有问题,请联系技术团队或查看项目文档。
