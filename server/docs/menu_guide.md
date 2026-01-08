# 菜单管理与我的菜单树接口 - 测试指南

## 📋 生成的文件清单

### 新增文件(5 个)

| 文件路径 | 说明 | 核心功能 |
|---|---|---|
| `app/models/menu.py` | 菜单模型 | AdminMenu 模型定义 |
| `app/schemas/menu.py` | 菜单 Schema | 创建、更新、树节点、动态路由 Schema |
| `app/services/menu_service.py` | 菜单服务 | 菜单树查询、CRUD、权限过滤 |
| `app/api/v1/admin/menu.py` | 菜单路由 | 6 个菜单接口 |
| `scripts/seed_menus.py` | 初始化脚本 | 创建菜单和角色分配 |

### 修改文件(3 个)

| 文件路径 | 修改内容 |
|---|---|
| `app/models/role.py` | 添加菜单关联关系 |
| `app/models/associations.py` | 添加角色-菜单关联表 |
| `app/main.py` | 注册菜单路由 |

---

## 🎯 菜单字段说明

| 字段 | 类型 | 说明 |
|---|---|---|
| `id` | BIGINT | 菜单 ID |
| `parent_id` | BIGINT | 父菜单 ID(0 为根节点) |
| `title` | VARCHAR(50) | 菜单标题 |
| `name` | VARCHAR(50) | 路由名称(唯一) |
| `path` | VARCHAR(200) | 路由路径 |
| `component` | VARCHAR(200) | 组件路径 |
| `icon` | VARCHAR(50) | 菜单图标 |
| `sort` | INT | 排序号(升序) |
| `hidden` | TINYINT | 是否隐藏(0-显示,1-隐藏) |
| `keep_alive` | TINYINT | 是否缓存(0-不缓存,1-缓存) |
| `status` | TINYINT | 状态(0-禁用,1-启用) |

---

## 🚀 快速开始

### 步骤 1: 初始化菜单数据

```bash
cd server
python scripts\seed_menus.py
```

**预期输出**:
```
==================================================
开始初始化菜单...
==================================================

[1/2] 创建菜单...
✅ 菜单创建成功!
   共创建 7 个菜单

[2/2] 分配菜单到角色...
✅ 超级管理员菜单分配成功!
   分配 7 个菜单
✅ 普通管理员菜单分配成功!
   分配 4 个菜单
✅ 普通用户菜单分配成功!
   分配 1 个菜单

==================================================
✅ 初始化完成!
==================================================
```

### 步骤 2: 启动服务

```bash
python -m app.main
```

---

## ✅ API 测试

### 1. 获取菜单树

```bash
curl -X GET http://localhost:8000/api/v1/admin/menus/tree \
  -H "Authorization: Bearer <admin_token>"
```

**预期响应**:
```json
{
  "code": 200,
  "message": "获取菜单树成功",
  "data": [
    {
      "id": 1,
      "parent_id": 0,
      "title": "仪表盘",
      "name": "Dashboard",
      "path": "/dashboard",
      "component": "views/dashboard/index.vue",
      "icon": "Dashboard",
      "sort": 1,
      "hidden": 0,
      "keep_alive": 1,
      "status": 1,
      "created_at": "2026-01-07T10:00:00",
      "children": []
    },
    {
      "id": 2,
      "parent_id": 0,
      "title": "系统管理",
      "name": "System",
      "path": "/system",
      "component": "Layout",
      "icon": "Setting",
      "sort": 2,
      "hidden": 0,
      "keep_alive": 1,
      "status": 1,
      "created_at": "2026-01-07T10:00:00",
      "children": [
        {
          "id": 10,
          "parent_id": 2,
          "title": "用户管理",
          "name": "User",
          "path": "/system/user",
          "component": "views/system/user/index.vue",
          "icon": "User",
          "sort": 1,
          "hidden": 0,
          "keep_alive": 1,
          "status": 1,
          "created_at": "2026-01-07T10:00:00",
          "children": []
        }
      ]
    }
  ],
  "trace_id": "xxx"
}
```

### 2. 获取我的菜单树(动态路由)

```bash
# 超级管理员
curl -X GET http://localhost:8000/api/v1/admin/menus/my \
  -H "Authorization: Bearer <admin_token>"
```

**预期响应**(前端可直接使用):
```json
{
  "code": 200,
  "message": "获取我的菜单树成功",
  "data": [
    {
      "id": 1,
      "title": "仪表盘",
      "name": "Dashboard",
      "path": "/dashboard",
      "component": "views/dashboard/index.vue",
      "meta": {
        "icon": "Dashboard",
        "title": "仪表盘",
        "hidden": false,
        "keepAlive": true
      },
      "children": []
    },
    {
      "id": 2,
      "title": "系统管理",
      "name": "System",
      "path": "/system",
      "component": "Layout",
      "meta": {
        "icon": "Setting",
        "title": "系统管理",
        "hidden": false,
        "keepAlive": true
      },
      "children": [
        {
          "id": 10,
          "title": "用户管理",
          "name": "User",
          "path": "/system/user",
          "component": "views/system/user/index.vue",
          "meta": {
            "icon": "User",
            "title": "用户管理",
            "hidden": false,
            "keepAlive": true
          },
          "children": []
        }
      ]
    }
  ],
  "trace_id": "xxx"
}
```

### 3. 创建菜单

```bash
curl -X POST http://localhost:8000/api/v1/admin/menus \
  -H "Authorization: Bearer <admin_token>" \
  -H "Content-Type: application/json" \
  -d '{
    "parent_id": 2,
    "title": "审计日志",
    "name": "AuditLog",
    "path": "/system/audit",
    "component": "views/system/audit/index.vue",
    "icon": "Document",
    "sort": 5
  }'
```

### 4. 更新菜单

```bash
curl -X PUT http://localhost:8000/api/v1/admin/menus/13 \
  -H "Authorization: Bearer <admin_token>" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "菜单配置",
    "sort": 10
  }'
```

### 5. 删除菜单

```bash
curl -X DELETE http://localhost:8000/api/v1/admin/menus/14 \
  -H "Authorization: Bearer <admin_token>"
```

### 6. 更新菜单排序

```bash
curl -X PUT http://localhost:8000/api/v1/admin/menus/13/sort \
  -H "Authorization: Bearer <admin_token>" \
  -H "Content-Type: application/json" \
  -d '{"sort": 3}'
```

---

## 📊 前端集成示例

### Vue 3 + Vue Router

```javascript
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'

const router = useRouter()
const menuRoutes = ref([])

// 获取我的菜单树
const loadMenuRoutes = async () => {
  const { data } = await axios.get('/api/v1/admin/menus/my')
  menuRoutes.value = data.data
  
  // 动态添加路由
  data.data.forEach(route => {
    addRoute(route)
  })
}

// 递归添加路由
const addRoute = (route) => {
  const routeConfig = {
    path: route.path,
    name: route.name,
    component: () => import(`@/${route.component}`),
    meta: route.meta,
    children: []
  }
  
  // 递归处理子路由
  if (route.children && route.children.length > 0) {
    route.children.forEach(child => {
      routeConfig.children.push(addRoute(child))
    })
  }
  
  router.addRoute(routeConfig)
  return routeConfig
}

onMounted(() => {
  loadMenuRoutes()
})
```

---

## 🔍 测试场景

### 场景 1: 超级管理员查看菜单

```bash
# 登录超级管理员
curl -X POST http://localhost:8000/api/v1/admin/auth/login \
  -d '{"username":"<ADMIN_USERNAME>","password":"<ADMIN_PASSWORD>"}'

# 获取我的菜单树
curl -X GET http://localhost:8000/api/v1/admin/menus/my \
  -H "Authorization: Bearer <token>"
```

**预期**: 返回所有菜单(7 个)

### 场景 2: 普通用户查看菜单

```bash
# 登录普通用户(需先创建)
curl -X POST http://localhost:8000/api/v1/admin/auth/login \
  -d '{"username":"user1","password":"<USER_PASSWORD>"}'

# 获取我的菜单树
curl -X GET http://localhost:8000/api/v1/admin/menus/my \
  -H "Authorization: Bearer <token>"
```

**预期**: 只返回仪表盘(1 个菜单)

### 场景 3: 测试菜单 CRUD

```bash
# 创建菜单
curl -X POST http://localhost:8000/api/v1/admin/menus \
  -H "Authorization: Bearer <admin_token>" \
  -d '{"parent_id":2,"title":"测试菜单","name":"Test","path":"/test","component":"views/test/index.vue"}'

# 更新菜单
curl -X PUT http://localhost:8000/api/v1/admin/menus/<id> \
  -H "Authorization: Bearer <admin_token>" \
  -d '{"title":"测试菜单2"}'

# 删除菜单
curl -X DELETE http://localhost:8000/api/v1/admin/menus/<id> \
  -H "Authorization: Bearer <admin_token>"
```

---

## 🔄 回滚方案

```bash
# 删除新增文件
rm app/models/menu.py
rm app/schemas/menu.py
rm app/services/menu_service.py
rm app/api/v1/admin/menu.py
rm scripts/seed_menus.py

# 恢复修改文件
git checkout HEAD -- app/models/role.py app/models/associations.py app/main.py

# 删除测试数据
mysql -u root -p -e "DELETE FROM admin_role_menu; DELETE FROM admin_menu;"
```

---

## ⚠️ 注意事项

1. **菜单名称唯一**: `name` 字段必须唯一
2. **级联删除**: 删除父菜单会删除所有子菜单
3. **权限过滤**: 普通用户只能看到分配的菜单
4. **隐藏菜单**: `hidden=1` 的菜单不在我的菜单树中显示
5. **排序规则**: 按 `sort` 字段升序排列
