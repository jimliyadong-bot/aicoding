# MySQL 建表 SQL - 运行指南

## 📋 文件说明

**文件**: [`schema_v2.sql`](file:///d:/Projects/ai-develop/workspace/antigravity/yiya_ai_reader/docs/database/schema_v2.sql)

**包含内容**:
- ✅ 9 张核心表(管理端 8 张 + 小程序 1 张)
- ✅ 完整的索引设计(主键、唯一索引、普通索引、外键索引)
- ✅ 初始化数据(3 个角色、30+ 权限、7 个菜单、1 个超级管理员)
- ✅ 详细的字段注释和说明

---

## 🚀 运行命令

### 方式 1: 命令行执行(推荐)

```bash
# 进入项目目录
cd d:\Projects\ai-develop\workspace\antigravity\yiya_ai_reader

# 执行 SQL 脚本
mysql -u root -p < docs/database/schema_v2.sql
```

### 方式 2: MySQL 客户端执行

```bash
# 登录 MySQL
mysql -u root -p

# 在 MySQL 命令行中执行
mysql> source d:/Projects/ai-develop/workspace/antigravity/yiya_ai_reader/docs/database/schema_v2.sql;
```

### 方式 3: 指定数据库执行

```bash
# 如果数据库已存在,直接在指定数据库中执行
mysql -u root -p yiya_ai_reader < docs/database/schema_v2.sql
```

---

## ✅ 验证步骤

### 1. 验证数据库创建

```sql
-- 查看所有数据库
SHOW DATABASES;

-- 应该看到 yiya_ai_reader 数据库
```

### 2. 验证表结构

```sql
-- 切换到数据库
USE yiya_ai_reader;

-- 查看所有表
SHOW TABLES;

-- 应该看到以下 9 张表:
-- +---------------------------+
-- | Tables_in_yiya_ai_reader  |
-- +---------------------------+
-- | admin_audit_log           |
-- | admin_menu                |
-- | admin_permission          |
-- | admin_role                |
-- | admin_role_menu           |
-- | admin_role_permission     |
-- | admin_user                |
-- | admin_user_role           |
-- | mp_user                   |
-- +---------------------------+
```

### 3. 验证表字段

```sql
-- 查看用户表结构
DESC admin_user;

-- 查看菜单表结构(验证树形字段)
DESC admin_menu;

-- 查看小程序用户表结构
DESC mp_user;
```

### 4. 验证索引

```sql
-- 查看用户表索引
SHOW INDEX FROM admin_user;

-- 查看菜单表索引
SHOW INDEX FROM admin_menu;

-- 查看关联表索引
SHOW INDEX FROM admin_user_role;
```

### 5. 验证初始化数据

```sql
-- 查看角色数据(应该有 3 条)
SELECT * FROM admin_role;

-- 查看权限数据(应该有 30+ 条)
SELECT COUNT(*) FROM admin_permission;

-- 查看菜单数据(应该有 7 条)
SELECT id, parent_id, name, level, sort FROM admin_menu ORDER BY sort;

-- 查看超级管理员用户(应该有 1 条)
SELECT id, username, real_name, status FROM admin_user;

-- 查看超级管理员的角色(应该有 1 条)
SELECT u.username, r.name, r.code 
FROM admin_user u
JOIN admin_user_role ur ON u.id = ur.user_id
JOIN admin_role r ON ur.role_id = r.id
WHERE u.username = 'admin';

-- 查看超级管理员的权限数量(应该有 30+ 条)
SELECT COUNT(*) 
FROM admin_user_role ur
JOIN admin_role_permission rp ON ur.role_id = rp.role_id
WHERE ur.user_id = 1;

-- 查看超级管理员的菜单数量(应该有 7 条)
SELECT COUNT(*) 
FROM admin_user_role ur
JOIN admin_role_menu rm ON ur.role_id = rm.role_id
WHERE ur.user_id = 1;
```

### 6. 验证菜单树形结构

```sql
-- 查看菜单树(一级菜单)
SELECT id, name, path, icon, level, sort 
FROM admin_menu 
WHERE parent_id = 0 
ORDER BY sort;

-- 查看系统管理下的子菜单(二级菜单)
SELECT id, parent_id, name, path, icon, level, sort 
FROM admin_menu 
WHERE parent_id = 2 
ORDER BY sort;
```

### 7. 验证外键约束

```sql
-- 查看用户角色关联表的外键
SELECT 
    CONSTRAINT_NAME,
    TABLE_NAME,
    COLUMN_NAME,
    REFERENCED_TABLE_NAME,
    REFERENCED_COLUMN_NAME
FROM INFORMATION_SCHEMA.KEY_COLUMN_USAGE
WHERE TABLE_SCHEMA = 'yiya_ai_reader'
AND TABLE_NAME = 'admin_user_role'
AND REFERENCED_TABLE_NAME IS NOT NULL;
```

---

## 🔍 预期结果

### 角色数据
```
+----+-----------------+-------------+------------------------+--------+
| id | name            | code        | description            | status |
+----+-----------------+-------------+------------------------+--------+
|  1 | 超级管理员      | SUPER_ADMIN | 拥有系统所有权限       |      1 |
|  2 | 管理员          | ADMIN       | 拥有系统管理权限       |      1 |
|  3 | 普通用户        | USER        | 普通用户权限           |      1 |
+----+-----------------+-------------+------------------------+--------+
```

### 菜单树结构
```
+----+-----------+--------------+-------+------+
| id | parent_id | name         | level | sort |
+----+-----------+--------------+-------+------+
|  1 |         0 | 仪表盘       |     1 |    1 |
|  2 |         0 | 系统管理     |     1 |    2 |
| 10 |         2 | 用户管理     |     2 |    1 |
| 11 |         2 | 角色管理     |     2 |    2 |
| 12 |         2 | 权限管理     |     2 |    3 |
| 13 |         2 | 菜单管理     |     2 |    4 |
| 14 |         2 | 审计日志     |     2 |    5 |
+----+-----------+--------------+-------+------+
```

### 超级管理员用户
```
+----+----------+-----------------+--------+
| id | username | real_name       | status |
+----+----------+-----------------+--------+
|  1 | admin    | 超级管理员      |      1 |
+----+----------+-----------------+--------+
```

**默认密码**: `admin123`

---

## 🔄 回滚方案

### 方案 1: 删除整个数据库(完全清理)

```sql
DROP DATABASE IF EXISTS yiya_ai_reader;
```

### 方案 2: 删除所有表(保留数据库)

```sql
USE yiya_ai_reader;

-- 先删除有外键约束的表
DROP TABLE IF EXISTS admin_audit_log;
DROP TABLE IF EXISTS admin_role_menu;
DROP TABLE IF EXISTS admin_role_permission;
DROP TABLE IF EXISTS admin_user_role;

-- 再删除主表
DROP TABLE IF EXISTS admin_menu;
DROP TABLE IF EXISTS admin_permission;
DROP TABLE IF EXISTS admin_role;
DROP TABLE IF EXISTS admin_user;
DROP TABLE IF EXISTS mp_user;
```

### 方案 3: 恢复到旧版本

```bash
# 如果之前有备份
mysql -u root -p yiya_ai_reader < docs/database/schema.sql
```

---

## 📊 表统计信息

| 表名 | 类型 | 字段数 | 索引数 | 初始数据 |
|---|---|---|---|---|
| `admin_user` | 主表 | 13 | 5 | 1 条 |
| `admin_role` | 主表 | 8 | 3 | 3 条 |
| `admin_permission` | 主表 | 7 | 2 | 30+ 条 |
| `admin_menu` | 主表 | 15 | 5 | 7 条 |
| `admin_user_role` | 关联表 | 3 | 4 | 1 条 |
| `admin_role_permission` | 关联表 | 3 | 4 | 30+ 条 |
| `admin_role_menu` | 关联表 | 3 | 4 | 7 条 |
| `admin_audit_log` | 日志表 | 14 | 4 | 0 条 |
| `mp_user` | 主表 | 15 | 6 | 0 条 |

**总计**: 9 张表, 81 个字段, 41 个索引

---

## 🎯 下一步操作

1. **执行 SQL 脚本**: 使用上述运行命令执行建表脚本
2. **验证数据**: 按照验证步骤检查表结构和数据
3. **更新后端配置**: 修改 `server/.env` 中的数据库连接信息
4. **运行后端服务**: 测试后端与数据库的连接
5. **测试登录**: 使用 `admin/admin123` 登录管理端

---

## ⚠️ 注意事项

1. **备份数据**: 如果数据库已有数据,请先备份
2. **权限检查**: 确保 MySQL 用户有创建数据库和表的权限
3. **字符集**: 确认 MySQL 支持 `utf8mb4` 字符集
4. **外键约束**: 删除数据时注意外键级联删除
5. **密码安全**: 生产环境请修改默认管理员密码
6. **索引优化**: 根据实际查询场景调整索引

---

## 📞 问题排查

### 问题 1: 外键约束错误

**错误**: `Cannot add foreign key constraint`

**解决**:
```sql
-- 检查存储引擎
SHOW TABLE STATUS WHERE Name = 'admin_user';

-- 确保所有表都是 InnoDB
ALTER TABLE admin_user ENGINE=InnoDB;
```

### 问题 2: 字符集错误

**错误**: `Unknown character set: 'utf8mb4'`

**解决**:
```sql
-- 检查 MySQL 版本(需要 5.5.3+)
SELECT VERSION();

-- 查看支持的字符集
SHOW CHARACTER SET LIKE 'utf8%';
```

### 问题 3: 权限不足

**错误**: `Access denied for user`

**解决**:
```sql
-- 授予权限
GRANT ALL PRIVILEGES ON yiya_ai_reader.* TO 'your_user'@'localhost';
FLUSH PRIVILEGES;
```
