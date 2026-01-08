-- ============================================
-- YiYa AI Reader - MySQL 8.0 数据库初始化脚本 V2
-- 数据库: yiya_ai_reader
-- 版本: 2.0.0
-- 创建时间: 2026-01-07
-- 说明: 包含管理端(admin_)和小程序(mp_)表结构
-- ============================================

-- 创建数据库
CREATE DATABASE IF NOT EXISTS yiya_ai_reader 
DEFAULT CHARACTER SET utf8mb4 
COLLATE utf8mb4_unicode_ci;

USE yiya_ai_reader;

-- ============================================
-- 1. 管理端用户表 (admin_user)
-- ============================================
DROP TABLE IF EXISTS admin_user;
CREATE TABLE admin_user (
    id BIGINT PRIMARY KEY AUTO_INCREMENT COMMENT '用户ID',
    username VARCHAR(50) NOT NULL UNIQUE COMMENT '用户名',
    password_hash VARCHAR(255) NOT NULL COMMENT '密码哈希(bcrypt)',
    real_name VARCHAR(50) COMMENT '真实姓名',
    phone VARCHAR(20) UNIQUE COMMENT '手机号',
    email VARCHAR(100) UNIQUE COMMENT '邮箱',
    avatar VARCHAR(500) COMMENT '头像URL',
    status TINYINT DEFAULT 1 COMMENT '状态: 0-禁用, 1-启用',
    last_login_at DATETIME COMMENT '最后登录时间',
    last_login_ip VARCHAR(50) COMMENT '最后登录IP',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    deleted_at DATETIME COMMENT '删除时间(软删除)',
    
    INDEX idx_username (username),
    INDEX idx_phone (phone),
    INDEX idx_status (status),
    INDEX idx_deleted_at (deleted_at),
    INDEX idx_created_at (created_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='管理端用户表';

-- ============================================
-- 2. 角色表 (admin_role)
-- ============================================
DROP TABLE IF EXISTS admin_role;
CREATE TABLE admin_role (
    id BIGINT PRIMARY KEY AUTO_INCREMENT COMMENT '角色ID',
    name VARCHAR(50) NOT NULL COMMENT '角色名称',
    code VARCHAR(50) NOT NULL UNIQUE COMMENT '角色编码(如: SUPER_ADMIN)',
    description VARCHAR(200) COMMENT '角色描述',
    status TINYINT DEFAULT 1 COMMENT '状态: 0-禁用, 1-启用',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    deleted_at DATETIME COMMENT '删除时间(软删除)',
    
    INDEX idx_code (code),
    INDEX idx_status (status),
    INDEX idx_deleted_at (deleted_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='角色表';

-- ============================================
-- 3. 权限表 (admin_permission)
-- ============================================
DROP TABLE IF EXISTS admin_permission;
CREATE TABLE admin_permission (
    id BIGINT PRIMARY KEY AUTO_INCREMENT COMMENT '权限ID',
    name VARCHAR(50) NOT NULL COMMENT '权限名称',
    code VARCHAR(100) NOT NULL UNIQUE COMMENT '权限编码(如: sys:user:create)',
    type VARCHAR(20) NOT NULL COMMENT '权限类型: MENU-菜单, BUTTON-按钮, API-接口',
    description VARCHAR(200) COMMENT '权限描述',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    
    INDEX idx_code (code),
    INDEX idx_type (type)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='权限表';

-- ============================================
-- 4. 菜单表 (admin_menu) - 支持树形结构
-- ============================================
DROP TABLE IF EXISTS admin_menu;
CREATE TABLE admin_menu (
    id BIGINT PRIMARY KEY AUTO_INCREMENT COMMENT '菜单ID',
    parent_id BIGINT DEFAULT 0 COMMENT '父菜单ID(0为根节点)',
    name VARCHAR(50) NOT NULL COMMENT '菜单名称',
    path VARCHAR(200) COMMENT '路由路径(如: /system/user)',
    component VARCHAR(200) COMMENT '组件路径(如: views/system/user/index.vue)',
    icon VARCHAR(50) COMMENT '菜单图标',
    level TINYINT DEFAULT 1 COMMENT '菜单层级: 1-一级, 2-二级, 3-三级',
    sort INT DEFAULT 0 COMMENT '排序号(升序)',
    hidden TINYINT DEFAULT 0 COMMENT '是否隐藏: 0-显示, 1-隐藏',
    keep_alive TINYINT DEFAULT 1 COMMENT '是否缓存: 0-不缓存, 1-缓存',
    status TINYINT DEFAULT 1 COMMENT '状态: 0-禁用, 1-启用',
    is_external TINYINT DEFAULT 0 COMMENT '是否外链: 0-否, 1-是',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    deleted_at DATETIME COMMENT '删除时间(软删除)',
    
    INDEX idx_parent_id (parent_id),
    INDEX idx_level (level),
    INDEX idx_sort (sort),
    INDEX idx_status (status),
    INDEX idx_deleted_at (deleted_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='菜单表(树形结构)';

-- ============================================
-- 5. 用户角色关联表 (admin_user_role)
-- ============================================
DROP TABLE IF EXISTS admin_user_role;
CREATE TABLE admin_user_role (
    user_id BIGINT NOT NULL COMMENT '用户ID',
    role_id BIGINT NOT NULL COMMENT '角色ID',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    
    PRIMARY KEY (user_id, role_id),
    INDEX idx_user_id (user_id),
    INDEX idx_role_id (role_id),
    FOREIGN KEY (user_id) REFERENCES admin_user(id) ON DELETE CASCADE,
    FOREIGN KEY (role_id) REFERENCES admin_role(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='用户角色关联表';

-- ============================================
-- 6. 角色权限关联表 (admin_role_permission)
-- ============================================
DROP TABLE IF EXISTS admin_role_permission;
CREATE TABLE admin_role_permission (
    role_id BIGINT NOT NULL COMMENT '角色ID',
    permission_id BIGINT NOT NULL COMMENT '权限ID',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    
    PRIMARY KEY (role_id, permission_id),
    INDEX idx_role_id (role_id),
    INDEX idx_permission_id (permission_id),
    FOREIGN KEY (role_id) REFERENCES admin_role(id) ON DELETE CASCADE,
    FOREIGN KEY (permission_id) REFERENCES admin_permission(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='角色权限关联表';

-- ============================================
-- 7. 角色菜单关联表 (admin_role_menu)
-- ============================================
DROP TABLE IF EXISTS admin_role_menu;
CREATE TABLE admin_role_menu (
    role_id BIGINT NOT NULL COMMENT '角色ID',
    menu_id BIGINT NOT NULL COMMENT '菜单ID',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    
    PRIMARY KEY (role_id, menu_id),
    INDEX idx_role_id (role_id),
    INDEX idx_menu_id (menu_id),
    FOREIGN KEY (role_id) REFERENCES admin_role(id) ON DELETE CASCADE,
    FOREIGN KEY (menu_id) REFERENCES admin_menu(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='角色菜单关联表';

-- ============================================
-- 8. 审计日志表 (admin_audit_log)
-- ============================================
DROP TABLE IF EXISTS admin_audit_log;
CREATE TABLE admin_audit_log (
    id BIGINT PRIMARY KEY AUTO_INCREMENT COMMENT '日志ID',
    user_id BIGINT COMMENT '用户ID',
    username VARCHAR(50) COMMENT '用户名',
    operation VARCHAR(50) NOT NULL COMMENT '操作类型(如: CREATE, UPDATE, DELETE)',
    module VARCHAR(50) COMMENT '模块名称(如: USER, ROLE)',
    description VARCHAR(500) COMMENT '操作描述',
    request_method VARCHAR(10) COMMENT '请求方法(GET/POST/PUT/DELETE)',
    request_url VARCHAR(500) COMMENT '请求URL',
    request_params TEXT COMMENT '请求参数(JSON)',
    response_code INT COMMENT '响应状态码',
    ip_address VARCHAR(50) COMMENT 'IP地址',
    user_agent VARCHAR(500) COMMENT 'User Agent',
    execution_time INT COMMENT '执行时间(毫秒)',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    
    INDEX idx_user_id (user_id),
    INDEX idx_operation (operation),
    INDEX idx_module (module),
    INDEX idx_created_at (created_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='审计日志表';

-- ============================================
-- 9. 小程序用户表 (mp_user)
-- ============================================
DROP TABLE IF EXISTS mp_user;
CREATE TABLE mp_user (
    id BIGINT PRIMARY KEY AUTO_INCREMENT COMMENT '用户ID',
    openid VARCHAR(100) NOT NULL UNIQUE COMMENT '微信openid',
    unionid VARCHAR(100) UNIQUE COMMENT '微信unionid',
    phone VARCHAR(20) UNIQUE COMMENT '手机号',
    nickname VARCHAR(50) COMMENT '昵称',
    avatar VARCHAR(500) COMMENT '头像URL',
    gender TINYINT DEFAULT 0 COMMENT '性别: 0-未知, 1-男, 2-女',
    country VARCHAR(50) COMMENT '国家',
    province VARCHAR(50) COMMENT '省份',
    city VARCHAR(50) COMMENT '城市',
    status TINYINT DEFAULT 1 COMMENT '状态: 0-禁用, 1-启用',
    last_login_at DATETIME COMMENT '最后登录时间',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    deleted_at DATETIME COMMENT '删除时间(软删除)',
    
    INDEX idx_openid (openid),
    INDEX idx_unionid (unionid),
    INDEX idx_phone (phone),
    INDEX idx_status (status),
    INDEX idx_deleted_at (deleted_at),
    INDEX idx_created_at (created_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='小程序用户表';

-- ============================================
-- 初始化数据
-- ============================================

-- 1. 插入默认角色
INSERT INTO admin_role (id, name, code, description, status) VALUES
(1, '超级管理员', 'SUPER_ADMIN', '拥有系统所有权限', 1),
(2, '管理员', 'ADMIN', '拥有系统管理权限', 1),
(3, '普通用户', 'USER', '普通用户权限', 1);

-- 2. 插入默认权限
INSERT INTO admin_permission (id, name, code, type, description) VALUES
-- 系统管理菜单权限
(1, '系统管理', 'sys:manage', 'MENU', '系统管理菜单'),
(2, '用户管理', 'sys:user:view', 'MENU', '用户管理菜单'),
(3, '角色管理', 'sys:role:view', 'MENU', '角色管理菜单'),
(4, '权限管理', 'sys:permission:view', 'MENU', '权限管理菜单'),
(5, '菜单管理', 'sys:menu:view', 'MENU', '菜单管理菜单'),
(6, '审计日志', 'sys:audit:view', 'MENU', '审计日志菜单'),

-- 用户管理权限点
(10, '用户列表', 'sys:user:list', 'API', '用户列表'),
(11, '用户详情', 'sys:user:detail', 'API', '用户详情'),
(12, '创建用户', 'sys:user:create', 'BUTTON', '创建用户按钮'),
(13, '更新用户', 'sys:user:update', 'BUTTON', '更新用户按钮'),
(14, '删除用户', 'sys:user:delete', 'BUTTON', '删除用户按钮'),
(15, '重置密码', 'sys:user:reset', 'BUTTON', '重置密码按钮'),
(16, '分配角色', 'sys:user:assign:role', 'BUTTON', '分配角色按钮'),

-- 角色管理权限点
(20, '角色列表', 'sys:role:list', 'API', '角色列表'),
(21, '角色详情', 'sys:role:detail', 'API', '角色详情'),
(22, '创建角色', 'sys:role:create', 'BUTTON', '创建角色按钮'),
(23, '更新角色', 'sys:role:update', 'BUTTON', '更新角色按钮'),
(24, '删除角色', 'sys:role:delete', 'BUTTON', '删除角色按钮'),
(25, '分配权限', 'sys:role:assign:permission', 'BUTTON', '分配权限按钮'),
(26, '分配菜单', 'sys:role:assign:menu', 'BUTTON', '分配菜单按钮'),

-- 权限管理权限点
(30, '权限列表', 'sys:permission:list', 'API', '权限列表'),
(31, '权限详情', 'sys:permission:detail', 'API', '权限详情'),
(32, '创建权限', 'sys:permission:create', 'BUTTON', '创建权限按钮'),
(33, '更新权限', 'sys:permission:update', 'BUTTON', '更新权限按钮'),
(34, '删除权限', 'sys:permission:delete', 'BUTTON', '删除权限按钮'),

-- 菜单管理权限点
(40, '菜单列表', 'sys:menu:list', 'API', '菜单列表'),
(41, '创建菜单', 'sys:menu:create', 'BUTTON', '创建菜单按钮'),
(42, '更新菜单', 'sys:menu:update', 'BUTTON', '更新菜单按钮'),
(43, '删除菜单', 'sys:menu:delete', 'BUTTON', '删除菜单按钮'),

-- 示例权限点
(90, '示例查看', 'sys:demo:view', 'API', '示例查看'),
(91, '示例列表', 'sys:demo:list', 'API', '示例列表');

-- 3. 插入默认菜单(树形结构)
INSERT INTO admin_menu (id, parent_id, name, path, component, icon, level, sort, hidden, keep_alive, status) VALUES
-- 一级菜单
(1, 0, '仪表盘', '/dashboard', 'views/dashboard/index.vue', 'Dashboard', 1, 1, 0, 1, 1),
(2, 0, '系统管理', '/system', 'Layout', 'Setting', 1, 2, 0, 1, 1),

-- 二级菜单(系统管理下)
(10, 2, '用户管理', '/system/user', 'views/system/user/index.vue', 'User', 2, 1, 0, 1, 1),
(11, 2, '角色管理', '/system/role', 'views/system/role/index.vue', 'UserFilled', 2, 2, 0, 1, 1),
(12, 2, '权限管理', '/system/permission', 'views/system/permission/index.vue', 'Lock', 2, 3, 0, 1, 1),
(13, 2, '菜单管理', '/system/menu', 'views/system/menu/index.vue', 'Menu', 2, 4, 0, 1, 1),
(14, 2, '审计日志', '/system/audit', 'views/system/audit/index.vue', 'Document', 2, 5, 0, 1, 1);

-- 4. 超级管理员角色分配所有权限
INSERT INTO admin_role_permission (role_id, permission_id)
SELECT 1, id FROM admin_permission;

-- 5. 超级管理员角色分配所有菜单
INSERT INTO admin_role_menu (role_id, menu_id)
SELECT 1, id FROM admin_menu;

-- 6. 管理员角色分配部分权限(排除权限管理和菜单管理)
INSERT INTO admin_role_permission (role_id, permission_id)
SELECT 2, id FROM admin_permission
WHERE code NOT LIKE 'sys:permission:%'
  AND code NOT LIKE 'sys:menu:%';

-- 7. 管理员角色分配部分菜单(排除权限管理和菜单管理)
INSERT INTO admin_role_menu (role_id, menu_id)
SELECT 2, id FROM admin_menu 
WHERE id IN (1, 2, 10, 11, 14);

-- ============================================
-- 字段说明
-- ============================================

/*
核心字段解释:

1. admin_user (管理端用户表)
   - id: 用户唯一标识
   - username: 登录用户名(唯一)
   - password_hash: bcrypt 加密的密码哈希
   - real_name: 真实姓名
   - phone/email: 联系方式(唯一)
   - avatar: 头像 URL
   - status: 0-禁用, 1-启用
   - last_login_at/last_login_ip: 登录信息
   - deleted_at: 软删除标记

2. admin_role (角色表)
   - id: 角色唯一标识
   - name: 角色显示名称
   - code: 角色编码(唯一,如: SUPER_ADMIN)
   - description: 角色描述
   - status: 0-禁用, 1-启用
   - deleted_at: 软删除标记

3. admin_permission (权限表)
   - id: 权限唯一标识
   - name: 权限显示名称
   - code: 权限编码(唯一,如: sys:user:create)
   - type: MENU-菜单权限, BUTTON-按钮权限, API-接口权限
   - description: 权限描述

4. admin_menu (菜单表 - 树形结构)
   - id: 菜单唯一标识
   - parent_id: 父菜单 ID(0 为根节点)
   - name: 菜单显示名称
   - path: 前端路由路径
   - component: Vue 组件路径
   - icon: 菜单图标
   - level: 菜单层级(1/2/3)
   - sort: 排序号(升序)
   - hidden: 是否隐藏(0-显示, 1-隐藏)
   - keep_alive: 是否缓存(0-不缓存, 1-缓存)
   - status: 0-禁用, 1-启用
   - is_external: 是否外链(0-否, 1-是)
   - deleted_at: 软删除标记

5. admin_user_role (用户角色关联表)
   - user_id: 用户 ID
   - role_id: 角色 ID
   - 联合主键: (user_id, role_id)
   - 外键约束: 级联删除

6. admin_role_permission (角色权限关联表)
   - role_id: 角色 ID
   - permission_id: 权限 ID
   - 联合主键: (role_id, permission_id)
   - 外键约束: 级联删除

7. admin_role_menu (角色菜单关联表)
   - role_id: 角色 ID
   - menu_id: 菜单 ID
   - 联合主键: (role_id, menu_id)
   - 外键约束: 级联删除

8. admin_audit_log (审计日志表)
   - id: 日志唯一标识
   - user_id/username: 操作用户信息
   - operation: 操作类型(CREATE/UPDATE/DELETE)
   - module: 模块名称(USER/ROLE/MENU)
   - description: 操作描述
   - request_method: HTTP 方法
   - request_url: 请求 URL
   - request_params: 请求参数(JSON)
   - response_code: HTTP 响应码
   - ip_address: 客户端 IP
   - user_agent: 浏览器信息
   - execution_time: 执行耗时(毫秒)

9. mp_user (小程序用户表)
   - id: 用户唯一标识
   - openid: 微信 openid(唯一)
   - unionid: 微信 unionid(唯一,可选)
   - phone: 手机号(唯一)
   - nickname: 昵称
   - avatar: 头像 URL
   - gender: 性别(0-未知, 1-男, 2-女)
   - country/province/city: 地理信息
   - status: 0-禁用, 1-启用
   - last_login_at: 最后登录时间
   - deleted_at: 软删除标记

索引说明:
- 主键索引: 所有表的 id 字段
- 唯一索引: username, code, openid 等唯一字段
- 普通索引: 高频查询字段(status, parent_id, created_at)
- 外键索引: 关联表的外键字段
- 联合主键: 关联表使用联合主键保证唯一性

初始化数据说明:
- 3 个角色: 超级管理员、管理员、普通用户
- 30+ 权限点: 涵盖菜单、按钮、API 三种类型
- 7 个菜单: 1 个仪表盘 + 1 个系统管理 + 5 个子菜单
-- 角色权限关联: 超级管理员拥有所有权限,管理员拥有部分权限
- 角色菜单关联: 超级管理员可见所有菜单,管理员可见部分菜单
*/

-- ============================================
-- 完成
-- ============================================
