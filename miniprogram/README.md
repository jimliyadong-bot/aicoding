# 小程序用户体系使用指南

## 📋 已实现功能

### 后端 API

| 接口 | 方法 | 路径 | 说明 |
|---|---|---|---|
| 微信登录 | POST | `/api/v1/mp/auth/login_by_code` | 通过 code 换取 token |
| 绑定手机号 | POST | `/api/v1/mp/auth/bind_phone` | 绑定手机号 |
| 获取用户信息 | GET | `/api/v1/mp/user/me` | 获取当前用户信息 |
| 更新用户信息 | PUT | `/api/v1/mp/user/me` | 更新昵称/头像 |

### 小程序功能

- ✅ 登录流程(wx.login → 调后端 → 保存 token)
- ✅ 获取手机号按钮与处理逻辑
- ✅ 个人信息页(昵称/头像展示与修改)

---

## 🚀 快速开始

### 前提条件

1. **微信小程序账号**: 已注册并获取 AppID 和 AppSecret
2. **后端服务已启动**: FastAPI 服务运行在 http://localhost:8000
3. **数据库已初始化**: 运行数据库迁移

### 步骤 1: 配置微信小程序

在 `.env` 文件中添加微信配置:

```env
# 微信小程序配置
WECHAT_APPID=your_appid_here
WECHAT_SECRET=your_secret_here
```

### 步骤 2: 运行数据库迁移

```bash
cd server
alembic revision --autogenerate -m "add mp_user table"
alembic upgrade head
```

### 步骤 3: 注册小程序路由

在 `server/app/main.py` 中添加:

```python
# 小程序路由
from app.api.v1.mp import auth as mp_auth, user as mp_user
app.include_router(mp_auth.router, prefix="/api/v1/mp/auth", tags=["小程序-认证"])
app.include_router(mp_user.router, prefix="/api/v1/mp/user", tags=["小程序-用户"])
```

### 步骤 4: 配置小程序

在微信开发者工具中:

1. 打开 `miniprogram` 目录
2. 填写 AppID
3. 修改 `app.js` 中的 `apiBaseUrl` 为后端地址
4. 编译运行

---

## ✅ 联调步骤

### 1. 启动后端服务

```bash
cd server
python -m app.main
```

**验证**: 访问 http://localhost:8000/docs 查看 API 文档

### 2. 打开微信开发者工具

1. 导入 `miniprogram` 目录
2. 填写 AppID
3. 点击"编译"

### 3. 测试登录流程

1. 点击"微信登录"按钮
2. 查看控制台日志
3. 验证 token 已保存到 Storage
4. 验证跳转到首页

**预期结果**:
- 登录成功提示
- token 保存成功
- 跳转到首页

### 4. 测试手机号绑定

1. 进入"我的"页面
2. 点击"获取手机号"按钮
3. 授权手机号
4. 验证绑定成功

**预期结果**:
- 绑定成功提示
- 手机号显示在页面上

### 5. 测试个人信息修改

1. 在"我的"页面修改昵称
2. 点击"保存修改"
3. 验证更新成功

**预期结果**:
- 保存成功提示
- 昵称更新显示

---

## 📊 小程序目录结构

```
miniprogram/
├── pages/
│   ├── index/              # 首页
│   ├── login/              # 登录页
│   │   ├── login.wxml
│   │   ├── login.js
│   │   ├── login.json
│   │   └── login.wxss
│   └── profile/            # 个人信息页
│       ├── profile.wxml
│       ├── profile.js
│       ├── profile.json
│       └── profile.wxss
├── utils/
│   └── request.js          # API 封装
├── api/
│   ├── auth.js             # 认证接口
│   └── user.js             # 用户接口
├── images/                 # 图片资源
├── app.js
├── app.json
└── app.wxss
```

---

## 🎯 核心代码说明

### 1. 登录流程

```javascript
// 1. 调用 wx.login 获取 code
wx.login({
  success: (res) => {
    const code = res.code
    // 2. 调用后端接口
    loginByCode(code).then(data => {
      // 3. 保存 token
      wx.setStorageSync('token', data.access_token)
      // 4. 跳转首页
      wx.switchTab({ url: '/pages/index/index' })
    })
  }
})
```

### 2. 获取手机号

```xml
<button open-type="getPhoneNumber" bindgetphonenumber="handleGetPhoneNumber">
  获取手机号
</button>
```

```javascript
handleGetPhoneNumber(e) {
  const code = e.detail.code
  bindPhone(code).then(data => {
    wx.showToast({ title: '绑定成功' })
  })
}
```

### 3. API 请求封装

```javascript
function request(options) {
  const token = wx.getStorageSync('token')
  const header = {
    'Content-Type': 'application/json',
    'Authorization': `Bearer ${token}`
  }
  
  wx.request({
    url: `${apiBaseUrl}${options.url}`,
    method: options.method,
    data: options.data,
    header,
    success: (res) => {
      if (res.statusCode === 401) {
        // Token 过期,跳转登录
        wx.redirectTo({ url: '/pages/login/login' })
      }
    }
  })
}
```

---

## 🔧 后端配置

### 环境变量

在 `server/.env` 中添加:

```env
# 微信小程序配置
WECHAT_APPID=wx1234567890abcdef
WECHAT_SECRET=your_secret_here
```

### 配置类

在 `server/app/core/config.py` 中添加:

```python
class Settings(BaseSettings):
    # 微信小程序配置
    WECHAT_APPID: str = ""
    WECHAT_SECRET: str = ""
```

---

## ⚠️ 注意事项

1. **AppID 和 AppSecret**: 需要在微信公众平台获取
2. **手机号权限**: 需要在微信公众平台开通"手机号快速验证"权限
3. **HTTPS**: 生产环境必须使用 HTTPS
4. **域名配置**: 需要在微信公众平台配置服务器域名
5. **Token 刷新**: 当前未实现 refresh token 自动刷新

---

## 🔄 回滚方案

### 删除后端文件

```bash
cd server
rm app/models/mp_user.py
rm app/utils/wechat.py
rm app/schemas/mp_user.py
rm -rf app/api/v1/mp
```

### 删除小程序目录

```bash
rm -rf miniprogram
```

### 回滚数据库

```bash
alembic downgrade -1
```

---

## 📚 相关文档

- [微信小程序官方文档](https://developers.weixin.qq.com/miniprogram/dev/framework/)
- [wx.login 文档](https://developers.weixin.qq.com/miniprogram/dev/api/open-api/login/wx.login.html)
- [获取手机号文档](https://developers.weixin.qq.com/miniprogram/dev/framework/open-ability/getPhoneNumber.html)

---

## ✨ 下一步

1. ✅ 实现 refresh token 自动刷新
2. ✅ 实现头像上传功能
3. ✅ 添加更多业务功能
4. ✅ 优化用户体验
