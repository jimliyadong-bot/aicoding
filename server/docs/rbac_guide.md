# RBAC 鉴权与权限点 - 测试指南

## 📋 生成的文件清单

### 新增文件(8 个)

| 文件路径 | 说明 | 核心功能 |
|---|---|---|
| `app/models/role.py` | 角色模型 | AdminRole 模型定义 |
| `app/models/permission.py` | 权限模型 | AdminPermission 模型定义 |
| `app/models/associations.py` | 关联表模型 | 用户-角色、角色-权限关联 |
| `app/services/permission_service.py` | 权限服务 | 权限检查、超级管理员判断 |
| `app/core/permissions.py` | 权限依赖装饰器 | require_perm 等装饰器 |
| `app/api/v1/admin/demo.py` | 示例接口 | 4 个权限验证示例 |
| `scripts/seed_permissions.py` | 初始化脚本 | 创建角色和权限 |
| `docs/rbac_guide.md` | 测试指南 | 本文档 |

### 修改文件(2 个)

| 文件路径 | 修改内容 |
|---|---|
| `app/models/user.py` | 添加角色关联关系 |
| `app/main.py` | 注册示例路由 |

---

## 🎯 权限编码规则

### 格式

```
{模块}:{资源}:{操作}
```

### 示例

| 权限编码 | 说明 |
|---|---|---|
| `sys:user:list` | 查看用户列表 |
| `sys:user:detail` | 查看用户详情 |
| `sys:user:create` | 创建用户 |
| `sys:user:update` | 更新用户 |
| `sys:user:delete` | 删除用户 |
| `sys:user:reset` | 重置用户密码 |
| `sys:user:assign:role` | 分配用户角色 |
| `sys:role:list` | 查看角色列表 |
| `sys:role:detail` | 查看角色详情 |
| `sys:role:assign:permission` | 分配角色权限 |
| `sys:role:assign:menu` | 分配角色菜单 |
| `sys:demo:view` | 查看示例(测试用) |

---

## 🔑 超级管理员策略

### 策略说明

**超级管理员**(角色编码: `SUPER_ADMIN`)拥有以下特权:

1. **绕过权限检查**: 不检查具体权限,直接通过所有权限验证
2. **访问所有接口**: 可以访问任何需要权限的接口
3. **无需绑定权限**: 不需要在数据库中绑定权限记录

### 实现逻辑

```python
# 在权限检查前,先判断是否为超级管理员
if PermissionService.is_super_admin(user):
    return True  # 直接通过

# 普通用户检查具体权限
return PermissionService.has_permission(user, permission_code)
```

---

## 🚀 快速开始

### 步骤 1: 初始化权限和角色

```bash
# 进入 server 目录
cd d:\Projects\ai-develop\workspace\antigravity\yiya_ai_reader\server

# 运行初始化脚本
python scripts\seed_permissions.py
```

**命令用途**: 创建角色(SUPER_ADMIN, ADMIN, USER)和权限(sys:user:*, sys:role:*, sys:demo:*)。

**预期输出**:
```
==================================================
开始初始化权限和角色...
==================================================

[1/3] 创建角色...
✅ 角色创建成功!
   - 超级管理员 (SUPER_ADMIN)
   - 管理员 (ADMIN)
   - 普通用户 (USER)

[2/3] 创建权限...
✅ 权限创建成功!
   共创建 20 个权限

[3/3] 分配超级管理员角色...
✅ 超级管理员角色分配成功!
   用户: admin
   角色: 超级管理员 (SUPER_ADMIN)

==================================================
✅ 初始化完成!
==================================================
```

### 步骤 2: 启动服务

```bash
python -m app.main
```

---

## ✅ 测试场景

### 场景 1: 超级管理员访问(应该成功)

#### 1.1 登录超级管理员

```bash
curl -X POST http://localhost:8000/api/v1/admin/auth/login \
  -H "Content-Type: application/json" \
  -d "{\"username\":\"<ADMIN_USERNAME>\",\"password\":\"<ADMIN_PASSWORD>\"}"
```

**保存 Token**:
```bash
export ACCESS_TOKEN="<access_token>"
```

#### 1.2 访问需要权限的接口

```bash
curl -X GET http://localhost:8000/api/v1/admin/demo/need_perm \
  -H "Authorization: Bearer $ACCESS_TOKEN"
```

**预期响应**:
```json
{
  "code": 200,
  "message": "success",
  "data": {
    "message": "你有权限访问此接口",
    "user": "admin",
    "required_permission": "sys:demo:view",
    "user_permissions": [],
    "is_super_admin": true
  },
  "trace_id": "xxx"
}
```

**说明**: 超级管理员绕过权限检查,即使没有绑定 `sys:demo:view` 权限也能访问。

---

### 场景 2: 普通用户无权限访问(应该失败)

#### 2.1 创建普通用户

```sql
-- 连接数据库
mysql -u root -p yiya_ai_reader

-- 创建普通用户
INSERT INTO admin_user (username, password_hash, real_name, status)
VALUES ('user1', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYzpLaOBzL6', '普通用户', 1);

-- 分配 USER 角色
INSERT INTO admin_user_role (user_id, role_id)
VALUES ((SELECT id FROM admin_user WHERE username = 'user1'), 3);
```

**密码**: <USER_PASSWORD>(仅用于测试)

#### 2.2 登录普通用户

```bash
curl -X POST http://localhost:8000/api/v1/admin/auth/login \
  -H "Content-Type: application/json" \
  -d "{\"username\":\"user1\",\"password\":\"<USER_PASSWORD>\"}"
```

**保存 Token**:
```bash
export USER1_TOKEN="<access_token>"
```

#### 2.3 访问需要权限的接口

```bash
curl -X GET http://localhost:8000/api/v1/admin/demo/need_perm \
  -H "Authorization: Bearer $USER1_TOKEN"
```

**预期响应**:
```json
{
  "code": 403,
  "message": "缺少权限: sys:demo:view",
  "data": null,
  "trace_id": "xxx"
}
```

**说明**: 普通用户没有 `sys:demo:view` 权限,访问被拒绝。

---

### 场景 3: 给普通用户分配权限(应该成功)

#### 3.1 给 USER 角色分配权限

```sql
-- 给 USER 角色分配 sys:demo:view 权限
INSERT INTO admin_role_permission (role_id, permission_id)
SELECT 3, id FROM admin_permission WHERE code = 'sys:demo:view';
```

#### 3.2 重新登录获取新权限

```bash
# 重新登录(刷新权限)
curl -X POST http://localhost:8000/api/v1/admin/auth/login \
  -H "Content-Type: application/json" \
  -d "{\"username\":\"user1\",\"password\":\"<USER_PASSWORD>\"}"

export USER1_TOKEN="<new_access_token>"
```

#### 3.3 再次访问接口

```bash
curl -X GET http://localhost:8000/api/v1/admin/demo/need_perm \
  -H "Authorization: Bearer $USER1_TOKEN"
```

**预期响应**:
```json
{
  "code": 200,
  "message": "success",
  "data": {
    "message": "你有权限访问此接口",
    "user": "user1",
    "required_permission": "sys:demo:view",
    "user_permissions": ["sys:demo:view"],
    "is_super_admin": false
  },
  "trace_id": "xxx"
}
```

**说明**: 分配权限后,普通用户可以访问接口。

---

### 场景 4: 测试其他权限装饰器

#### 4.1 测试任意权限(require_any_perm)

```bash
curl -X GET http://localhost:8000/api/v1/admin/demo/need_any_perm \
  -H "Authorization: Bearer $USER1_TOKEN"
```

**说明**: 只要有 `sys:demo:view` 或 `sys:demo:list` 任意一个权限即可访问。

#### 4.2 测试超级管理员专属接口

```bash
curl -X GET http://localhost:8000/api/v1/admin/demo/super_admin_only \
  -H "Authorization: Bearer $ACCESS_TOKEN"
```

**预期**: 超级管理员可以访问

```bash
curl -X GET http://localhost:8000/api/v1/admin/demo/super_admin_only \
  -H "Authorization: Bearer $USER1_TOKEN"
```

**预期**: 普通用户返回 403 错误

#### 4.3 测试公开接口

```bash
curl -X GET http://localhost:8000/api/v1/admin/demo/public
```

**说明**: 公开接口无需 Token 即可访问。

---

## 📊 权限依赖装饰器使用

### 1. require_perm - 单个权限

```python
@router.get("/users")
async def get_users(
    current_user: AdminUser = Depends(require_perm("sys:user:list"))
):
    """需要 sys:user:list 权限"""
    return {"users": []}
```

### 2. require_any_perm - 任意权限

```python
@router.get("/users")
async def get_users(
    current_user: AdminUser = Depends(require_any_perm("sys:user:list", "sys:user:detail"))
):
    """需要 sys:user:list 或 sys:user:detail 任意权限"""
    return {"users": []}
```

### 3. require_all_perms - 所有权限

```python
@router.post("/users")
async def create_user(
    current_user: AdminUser = Depends(require_all_perms("sys:user:create", "sys:user:assign"))
):
    """需要 sys:user:create 和 sys:user:assign 所有权限"""
    return {"message": "创建成功"}
```

### 4. require_super_admin - 超级管理员

```python
@router.delete("/system/reset")
async def reset_system(
    current_user: AdminUser = Depends(require_super_admin())
):
    """仅超级管理员可访问"""
    return {"message": "系统重置成功"}
```

---

## 🔍 验证清单

- [ ] 运行 `seed_permissions.py` 初始化数据
- [ ] 超级管理员可以访问所有接口
- [ ] 普通用户访问无权限接口返回 403
- [ ] 给普通用户分配权限后可以访问
- [ ] `require_perm` 装饰器工作正常
- [ ] `require_any_perm` 装饰器工作正常
- [ ] `require_super_admin` 装饰器工作正常
- [ ] 权限编码格式符合规范
- [ ] 数据库关联关系正确

---

## 🔄 回滚方案

### 删除新增文件

```bash
cd server

rm app/models/role.py
rm app/models/permission.py
rm app/models/associations.py
rm app/services/permission_service.py
rm app/core/permissions.py
rm app/api/v1/admin/demo.py
rm scripts/seed_permissions.py
```

### 恢复修改文件

```bash
git checkout HEAD -- app/models/user.py app/main.py
```

### 删除测试数据

```sql
DELETE FROM admin_role_permission;
DELETE FROM admin_user_role WHERE user_id > 1;
DELETE FROM admin_permission;
DELETE FROM admin_role;
DELETE FROM admin_user WHERE id > 1;
```

---

## 📚 相关文档

- [架构设计文档](file:///d:/Projects/ai-develop/workspace/antigravity/yiya_ai_reader/docs/architecture.md)
- [认证接口文档](file:///d:/Projects/ai-develop/workspace/antigravity/yiya_ai_reader/server/docs/auth_api.md)

---

## ⚠️ 注意事项

1. **超级管理员**: 拥有所有权限,无需绑定
2. **权限编码**: 使用 `module:resource:action` 格式
3. **重新登录**: 修改权限后需要重新登录才能生效
4. **数据库同步**: 确保数据库表结构与模型一致
5. **测试环境**: 建议在测试环境中验证权限逻辑
