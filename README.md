# YiYa AI Reader

智能阅读管理平台 - 三层架构(管理后台 + 后端 API + 微信小程序)

## 📋 项目结构

```
yiya_ai_reader/
├── server/              # 后端 API (FastAPI)
├── admin-web/           # 管理后台 (Vue3)
├── miniprogram/         # 微信小程序
├── docs/                # 文档
└── deploy/              # 部署配置
```

## 🚀 快速开始

### 环境要求

- **Python**: 3.13+
- **MySQL**: 8.0+
- **Redis**: 6.0+
- **Node.js**: 18+

### 本地启动123

#### 1. 克隆项目

```bash
git clone https://github.com/your-repo/yiya_ai_reader.git
cd yiya_ai_reader
```

#### 2. 启动后端

```bash
# 进入后端目录
cd server

# 创建虚拟环境
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 安装依赖
pip install -r requirements.txt

# 配置环境变量
cp .env.example .env
# 编辑 .env 文件,填写数据库、Redis 等配置

# 运行数据库迁移
alembic upgrade head

# 初始化数据
python scripts/seed_admin.py
python scripts/seed_permissions.py
python scripts/seed_menus.py

# 启动服务
python -m app.main
```

**访问**: http://localhost:8000/docs

#### 3. 启动管理后台

```bash
# 进入管理后台目录
cd admin-web

# 安装依赖
npm install

# 启动开发服务器
npm run dev
```

**访问**: http://localhost:5173

**管理员账号**: 通过环境变量运行 `python scripts/seed_admin.py` 创建

#### 4. 启动小程序

1. 打开微信开发者工具
2. 导入 `miniprogram` 目录
3. 填写 AppID
4. 修改 `app.js` 中的 `apiBaseUrl`
5. 编译运行

## 📊 初始化数据

### 1. 创建管理员

```bash
cd server
export ADMIN_USERNAME=admin
export ADMIN_PASSWORD=your-strong-password
python scripts/seed_admin.py
```

**管理员账号**:
- 用户名: $ADMIN_USERNAME
- 密码: $ADMIN_PASSWORD

### 2. 初始化权限

```bash
python scripts/seed_permissions.py
```

**权限列表**:
- 系统管理权限
- 用户管理权限
- 角色管理权限
- 权限管理权限
- 菜单管理权限

### 3. 初始化菜单

```bash
python scripts/seed_menus.py
```

**菜单列表**:
- 仪表盘
- 系统管理
  - 用户管理
  - 角色管理
  - 权限管理
  - 菜单管理

## 🔧 配置说明

### 后端配置 (.env)

```env
# 数据库配置
DATABASE_URL=mysql+aiomysql://root:<db_password>@localhost:3306/yiya_ai_reader

# Redis 配置
REDIS_URL=redis://localhost:6379/0

# JWT 配置
SECRET_KEY=your-strong-secret-key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=120
REFRESH_TOKEN_EXPIRE_DAYS=7

# CORS 配置
CORS_ORIGINS=["http://localhost:5173"]

# 微信小程序配置
WECHAT_APPID=your_appid
WECHAT_SECRET=your_secret
```

### 前端配置 (.env.development)

```env
VITE_API_BASE_URL=http://localhost:8000
```

## ⚠️ 常见问题

### 1. 数据库连接失败

**错误**: `Can't connect to MySQL server`

**解决**:
1. 检查 MySQL 服务是否启动
2. 检查 `.env` 中的数据库配置
3. 确认数据库已创建: `CREATE DATABASE yiya_ai_reader;`

### 2. Redis 连接失败

**错误**: `Error connecting to Redis`

**解决**:
1. 检查 Redis 服务是否启动
2. 检查 `.env` 中的 Redis 配置
3. 测试连接: `redis-cli ping`

### 3. 端口被占用

**错误**: `Address already in use`

**解决**:
```bash
# 查找占用端口的进程
lsof -i :8000  # macOS/Linux
netstat -ano | findstr :8000  # Windows

# 杀死进程
kill -9 <PID>  # macOS/Linux
taskkill /PID <PID> /F  # Windows
```

### 4. 前端无法连接后端

**错误**: `Network Error`

**解决**:
1. 检查后端服务是否启动
2. 检查 `.env.development` 中的 API 地址
3. 检查浏览器控制台的网络请求

### 5. 小程序登录失败

**错误**: `登录失败`

**解决**:
1. 检查微信 AppID 和 AppSecret 配置
2. 检查后端服务是否启动
3. 查看微信开发者工具控制台错误

## 📚 技术栈

### 后端
- **框架**: FastAPI 0.109
- **数据库**: MySQL 8.0 + SQLAlchemy 2.0
- **缓存**: Redis 6.0
- **认证**: JWT
- **迁移**: Alembic

### 管理后台
- **框架**: Vue 3.4 + Vite 5.0
- **UI 库**: Element Plus 2.5
- **状态管理**: Pinia 2.1
- **路由**: Vue Router 4.2
- **HTTP**: Axios 1.6

### 微信小程序
- **框架**: 微信小程序原生
- **API**: 微信开放接口

## 📖 文档

- [后端 API 文档](server/README.md)
- [认证接口文档](server/docs/auth_api.md)
- [RBAC 权限文档](server/docs/rbac_guide.md)
- [菜单管理文档](server/docs/menu_guide.md)
- [管理后台文档](admin-web/README.md)
- [小程序文档](miniprogram/README.md)

## 🔐 安全特性

- ✅ JWT 认证
- ✅ RBAC 权限控制
- ✅ 审计日志
- ✅ 登录限流
- ✅ 密码加密(bcrypt)
- ✅ SQL 注入防护
- ✅ XSS 防护

## 🚢 部署

### Docker 部署

```bash
# 构建镜像
docker-compose build

# 启动服务
docker-compose up -d
```

### 生产环境

详见 [部署文档](docs/deployment.md)

## 📝 License

MIT License

## 👥 贡献

欢迎提交 Issue 和 Pull Request!
