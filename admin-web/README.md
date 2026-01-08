# Vue3 管理后台项目 - 使用指南

## 📋 项目文件清单

### 配置文件
- `package.json` - 项目依赖
- `vite.config.js` - Vite 配置
- `.env.development` - 开发环境变量
- `.env.production` - 生产环境变量

### 核心功能
- `src/utils/request.js` - axios 封装
- `src/utils/auth.js` - 认证工具
- `src/stores/auth.js` - Pinia auth store
- `src/router/index.js` - 路由配置
- `src/directives/permission.js` - 权限指令

### API 接口
- `src/api/auth.js` - 认证接口
- `src/api/menu.js` - 菜单接口

### 页面组件
- `src/views/login/index.vue` - 登录页
- `src/components/Layout/index.vue` - Layout 布局
- `src/views/dashboard/index.vue` - 仪表盘
- `src/views/404.vue` - 404 页面

---

## 🚀 启动命令

### 1. 安装依赖

```bash
cd admin-web
npm install
```

**说明**: 安装所有项目依赖,包括 Vue3、Element Plus、Pinia、Vue Router、Axios 等。

### 2. 启动开发服务器

```bash
npm run dev
```

**说明**: 启动 Vite 开发服务器,默认端口 5173。

**访问**: http://localhost:5173

### 3. 生产构建

```bash
npm run build
```

**说明**: 构建生产版本,输出到 `dist` 目录。

### 4. 预览构建结果

```bash
npm run preview
```

**说明**: 预览生产构建结果。

---

## ✅ 联调步骤

### 步骤 1: 启动后端服务

```bash
# 进入后端目录
cd server

# 确保已初始化数据
python scripts/seed_admin.py
python scripts/seed_permissions.py
python scripts/seed_menus.py

# 启动后端
python -m app.main
```

**验证**: 访问 http://localhost:8000/docs 查看 API 文档

### 步骤 2: 启动前端服务

```bash
# 进入前端目录
cd admin-web

# 安装依赖(首次)
npm install

# 启动开发服务器
npm run dev
```

**访问**: http://localhost:5173

### 步骤 3: 登录测试

1. 打开浏览器访问 http://localhost:5173
2. 输入用户名: `admin`
3. 输入密码: `ADMIN_PASSWORD`
4. 点击登录

**预期结果**: 
- 登录成功,跳转到仪表盘
- 左侧显示菜单导航
- 顶部显示用户信息

### 步骤 4: 功能测试

#### 4.1 动态路由测试

- 登录后查看左侧菜单
- 超级管理员应该看到所有菜单
- 点击菜单项,路由正常跳转

#### 4.2 权限指令测试

- 在仪表盘页面查看权限测试按钮
- 超级管理员应该看到所有按钮
- 普通用户只能看到有权限的按钮

#### 4.3 暗黑模式测试

- 点击顶部的暗黑模式开关
- 页面切换到暗黑主题
- 刷新页面,主题保持

#### 4.4 Token 刷新测试

- 等待 Access Token 过期(2小时)
- 或手动修改 token 为无效值
- 发起请求,应该自动刷新 token 并重试

#### 4.5 登出测试

- 点击顶部用户头像
- 选择"退出登录"
- 确认登出
- 跳转到登录页

---

## 🔍 验证清单

- [ ] 项目成功启动
- [ ] 登录功能正常
- [ ] 菜单正确显示
- [ ] 动态路由加载成功
- [ ] 权限指令工作正常
- [ ] 暗黑模式切换正常
- [ ] 401 自动刷新 token
- [ ] 登出功能正常
- [ ] 页面样式美观

---

## 🎯 核心功能说明

### 1. axios 封装

**自动添加 Token**:
```javascript
config.headers.Authorization = `Bearer ${token}`
```

**401 自动刷新**:
```javascript
if (response?.status === 401 && !config._retry) {
  const newToken = await authStore.refreshToken()
  if (newToken) {
    config.headers.Authorization = `Bearer ${newToken}`
    return request(config)
  }
}
```

**统一错误提示**:
```javascript
ElMessage.error(response?.data?.message || '请求失败')
```

### 2. Pinia auth store

**状态管理**:
- `token` - Access Token
- `refreshTokenValue` - Refresh Token
- `user` - 用户信息
- `permissions` - 权限列表
- `menus` - 菜单列表

**核心方法**:
- `login()` - 登录
- `logout()` - 登出
- `refreshToken()` - 刷新 token
- `getUserInfo()` - 获取用户信息
- `getMenus()` - 获取菜单
- `hasPermission()` - 检查权限

### 3. 动态路由

**流程**:
```
登录成功 → 获取菜单 → 转换为路由 → router.addRoute() → 跳转
```

**菜单转路由**:
```javascript
function menuToRoutes(menus) {
  return menus.map(menu => ({
    path: menu.path,
    name: menu.name,
    component: loadView(menu.component),
    meta: menu.meta,
    children: menu.children?.map(menuToRoutes)
  }))
}
```

### 4. 权限指令

**使用方式**:
```vue
<el-button v-perm="'sys:user:create'">创建用户</el-button>
<el-button v-perm="['sys:user:update', 'sys:user:delete']">编辑</el-button>
```

**实现原理**:
```javascript
if (!authStore.hasPermission(value)) {
  el.parentNode?.removeChild(el)
}
```

---

## 🔧 常见问题

### 问题 1: 无法连接后端

**错误**: Network Error

**解决**:
1. 检查后端服务是否启动
2. 检查 `.env.development` 中的 API 地址
3. 检查浏览器控制台的网络请求

### 问题 2: 登录后没有菜单

**原因**: 后端未初始化菜单数据

**解决**:
```bash
cd server
python scripts/seed_menus.py
```

### 问题 3: 权限按钮都不显示

**原因**: 权限数据未正确加载

**解决**:
1. 检查后端权限接口
2. 查看浏览器控制台错误
3. 确认 auth store 中的 permissions 数据

### 问题 4: 暗黑模式不生效

**原因**: Element Plus 暗黑主题 CSS 未加载

**解决**:
确认 `main.js` 中已导入:
```javascript
import 'element-plus/theme-chalk/dark/css-vars.css'
```

---

## 📚 技术栈

- **Vue 3.4** - 渐进式 JavaScript 框架
- **Vite 5.0** - 下一代前端构建工具
- **Element Plus 2.5** - Vue 3 组件库
- **Pinia 2.1** - Vue 状态管理
- **Vue Router 4.2** - Vue 路由
- **Axios 1.6** - HTTP 客户端
- **SCSS** - CSS 预处理器

---

## 🎨 页面展示

### 登录页
- 现代简洁设计
- 左侧品牌展示
- 右侧登录表单
- 渐变背景

### Layout
- 侧边栏菜单导航
- 顶栏用户信息
- 暗黑模式切换
- 响应式布局

### 仪表盘
- 统计数据展示
- 权限测试按钮
- 欢迎信息

---

## 🔄 下一步

1. ✅ 开发更多业务页面
2. ✅ 实现用户管理
3. ✅ 实现角色管理
4. ✅ 实现权限管理
5. ✅ 实现菜单管理
6. ✅ 优化用户体验
7. ✅ 添加单元测试
