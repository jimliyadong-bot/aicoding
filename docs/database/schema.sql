-- ============================================
-- 三端项目数据库初始化脚本
-- 数据库: yiya_ai_reader
-- 版本: 1.0.0
-- 创建时间: 2026-01-06
-- ============================================

-- 创建数据库
CREATE DATABASE IF NOT EXISTS yiya_ai_reader DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

USE yiya_ai_reader;

-- ============================================
-- 1. 用户表
-- ============================================
DROP TABLE IF EXISTS sys_user;
CREATE TABLE sys_user (
    id BIGINT PRIMARY KEY AUTO_INCREMENT COMMENT '用户ID',
    username VARCHAR(50) NOT NULL UNIQUE COMMENT '用户名',
    password_hash VARCHAR(255) NOT NULL COMMENT '密码哈希',
    phone VARCHAR(20) UNIQUE COMMENT '手机号',
    email VARCHAR(100) UNIQUE COMMENT '邮箱',
    avatar VARCHAR(500) COMMENT '头像URL',
    nickname VARCHAR(50) COMMENT '昵称',
    gender TINYINT DEFAULT 0 COMMENT '性别: 0-未知, 1-男, 2-女',
    openid VARCHAR(100) UNIQUE COMMENT '微信openid',
    unionid VARCHAR(100) UNIQUE COMMENT '微信unionid',
    status TINYINT DEFAULT 1 COMMENT '状态: 0-禁用, 1-启用',
    last_login_at DATETIME COMMENT '最后登录时间',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    deleted_at DATETIME COMMENT '删除时间（软删除）',
    INDEX idx_username (username),
    INDEX idx_phone (phone),
    INDEX idx_openid (openid),
    INDEX idx_status (status),
    INDEX idx_deleted_at (deleted_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='用户表';

-- ============================================
-- 2. 角色表
-- ============================================
DROP TABLE IF EXISTS sys_role;
CREATE TABLE sys_role (
    id BIGINT PRIMARY KEY AUTO_INCREMENT COMMENT '角色ID',
    name VARCHAR(50) NOT NULL COMMENT '角色名称',
    code VARCHAR(50) NOT NULL UNIQUE COMMENT '角色编码',
    description VARCHAR(200) COMMENT '角色描述',
    status TINYINT DEFAULT 1 COMMENT '状态: 0-禁用, 1-启用',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    deleted_at DATETIME COMMENT '删除时间（软删除）',
    INDEX idx_code (code),
    INDEX idx_status (status),
    INDEX idx_deleted_at (deleted_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='角色表';

-- ============================================
-- 3. 权限表
-- ============================================
DROP TABLE IF EXISTS sys_permission;
CREATE TABLE sys_permission (
    id BIGINT PRIMARY KEY AUTO_INCREMENT COMMENT '权限ID',
    name VARCHAR(50) NOT NULL COMMENT '权限名称',
    code VARCHAR(100) NOT NULL UNIQUE COMMENT '权限编码',
    type VARCHAR(20) NOT NULL COMMENT '权限类型: MENU, BUTTON, API',
    description VARCHAR(200) COMMENT '权限描述',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    INDEX idx_code (code),
    INDEX idx_type (type)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='权限表';

-- ============================================
-- 4. 菜单表
-- ============================================
DROP TABLE IF EXISTS sys_menu;
CREATE TABLE sys_menu (
    id BIGINT PRIMARY KEY AUTO_INCREMENT COMMENT '菜单ID',
    parent_id BIGINT DEFAULT 0 COMMENT '父菜单ID（0为顶级菜单）',
    name VARCHAR(50) NOT NULL COMMENT '菜单名称',
    path VARCHAR(200) COMMENT '路由路径',
    component VARCHAR(200) COMMENT '组件路径',
    icon VARCHAR(50) COMMENT '菜单图标',
    sort INT DEFAULT 0 COMMENT '排序',
    status TINYINT DEFAULT 1 COMMENT '状态: 0-禁用, 1-启用',
    is_external TINYINT DEFAULT 0 COMMENT '是否外链: 0-否, 1-是',
    is_cache TINYINT DEFAULT 1 COMMENT '是否缓存: 0-否, 1-是',
    is_visible TINYINT DEFAULT 1 COMMENT '是否显示: 0-否, 1-是',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    deleted_at DATETIME COMMENT '删除时间（软删除）',
    INDEX idx_parent_id (parent_id),
    INDEX idx_status (status),
    INDEX idx_deleted_at (deleted_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='菜单表';

-- ============================================
-- 5. 用户角色关联表
-- ============================================
DROP TABLE IF EXISTS sys_user_role;
CREATE TABLE sys_user_role (
    user_id BIGINT NOT NULL COMMENT '用户ID',
    role_id BIGINT NOT NULL COMMENT '角色ID',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    PRIMARY KEY (user_id, role_id),
    INDEX idx_user_id (user_id),
    INDEX idx_role_id (role_id),
    FOREIGN KEY (user_id) REFERENCES sys_user(id) ON DELETE CASCADE,
    FOREIGN KEY (role_id) REFERENCES sys_role(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='用户角色关联表';

-- ============================================
-- 6. 角色权限关联表
-- ============================================
DROP TABLE IF EXISTS sys_role_permission;
CREATE TABLE sys_role_permission (
    role_id BIGINT NOT NULL COMMENT '角色ID',
    permission_id BIGINT NOT NULL COMMENT '权限ID',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    PRIMARY KEY (role_id, permission_id),
    INDEX idx_role_id (role_id),
    INDEX idx_permission_id (permission_id),
    FOREIGN KEY (role_id) REFERENCES sys_role(id) ON DELETE CASCADE,
    FOREIGN KEY (permission_id) REFERENCES sys_permission(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='角色权限关联表';

-- ============================================
-- 7. 菜单权限关联表
-- ============================================
DROP TABLE IF EXISTS sys_menu_permission;
CREATE TABLE sys_menu_permission (
    menu_id BIGINT NOT NULL COMMENT '菜单ID',
    permission_id BIGINT NOT NULL COMMENT '权限ID',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    PRIMARY KEY (menu_id, permission_id),
    INDEX idx_menu_id (menu_id),
    INDEX idx_permission_id (permission_id),
    FOREIGN KEY (menu_id) REFERENCES sys_menu(id) ON DELETE CASCADE,
    FOREIGN KEY (permission_id) REFERENCES sys_permission(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='菜单权限关联表';

-- ============================================
-- 8. 审计日志表
-- ============================================
DROP TABLE IF EXISTS sys_audit_log;
CREATE TABLE sys_audit_log (
    id BIGINT PRIMARY KEY AUTO_INCREMENT COMMENT '日志ID',
    user_id BIGINT COMMENT '用户ID',
    username VARCHAR(50) COMMENT '用户名',
    operation VARCHAR(50) NOT NULL COMMENT '操作类型',
    module VARCHAR(50) COMMENT '模块名称',
    description VARCHAR(500) COMMENT '操作描述',
    request_method VARCHAR(10) COMMENT '请求方法',
    request_url VARCHAR(500) COMMENT '请求URL',
    request_params TEXT COMMENT '请求参数',
    response_code INT COMMENT '响应状态码',
    ip_address VARCHAR(50) COMMENT 'IP地址',
    user_agent VARCHAR(500) COMMENT 'User Agent',
    execution_time INT COMMENT '执行时间（毫秒）',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    INDEX idx_user_id (user_id),
    INDEX idx_operation (operation),
    INDEX idx_created_at (created_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='审计日志表';

-- ============================================
-- 初始化数据
-- ============================================

-- 插入默认角色
INSERT INTO sys_role (id, name, code, description, status) VALUES
(1, '超级管理员', 'SUPER_ADMIN', '拥有系统所有权限', 1),
(2, '管理员', 'ADMIN', '拥有系统管理权限', 1),
(3, '普通用户', 'USER', '普通用户权限', 1);

-- 插入默认权限
INSERT INTO sys_permission (id, name, code, type, description) VALUES
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

-- 插入默认菜单
INSERT INTO sys_menu (id, parent_id, name, path, component, icon, sort, status) VALUES
-- 一级菜单
(1, 0, '仪表盘', '/dashboard', 'views/dashboard/index.vue', 'Dashboard', 1, 1),
(2, 0, '系统管理', '/system', 'Layout', 'Setting', 2, 1),

-- 二级菜单
(10, 2, '用户管理', '/system/user', 'views/system/user/index.vue', 'User', 1, 1),
(11, 2, '角色管理', '/system/role', 'views/system/role/index.vue', 'UserFilled', 2, 1),
(12, 2, '权限管理', '/system/permission', 'views/system/permission/index.vue', 'Lock', 3, 1),
(13, 2, '菜单管理', '/system/menu', 'views/system/menu/index.vue', 'Menu', 4, 1),
(14, 2, '审计日志', '/system/audit', 'views/system/audit/index.vue', 'Document', 5, 1);

-- 菜单权限关联
INSERT INTO sys_menu_permission (menu_id, permission_id) VALUES
-- 系统管理菜单
(2, 1),
-- 用户管理菜单
(10, 2), (10, 10), (10, 11), (10, 12), (10, 13), (10, 14), (10, 15), (10, 16),
-- 角色管理菜单
(11, 3), (11, 20), (11, 21), (11, 22), (11, 23), (11, 24), (11, 25), (11, 26),
-- 权限管理菜单
(12, 4), (12, 30), (12, 31), (12, 32), (12, 33), (12, 34),
-- 菜单管理菜单
(13, 5), (13, 40), (13, 41), (13, 42), (13, 43),
-- 审计日志菜单
(14, 6);

-- 超级管理员角色分配所有权限
INSERT INTO sys_role_permission (role_id, permission_id)
SELECT 1, id FROM sys_permission;

-- 管理员角色分配部分权限（排除权限管理和菜单管理）
INSERT INTO sys_role_permission (role_id, permission_id)
SELECT 2, id FROM sys_permission
WHERE code NOT LIKE 'sys:permission:%'
  AND code NOT LIKE 'sys:menu:%';

-- ============================================
-- 完成
-- ============================================
