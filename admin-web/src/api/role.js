/**
 * 角色管理 API
 */
import request from '@/utils/request'

/**
 * 获取角色列表
 */
export function getRoleList(params) {
    return request({
        url: '/api/v1/admin/roles',
        method: 'get',
        params
    })
}

/**
 * 获取角色详情
 */
export function getRoleDetail(id) {
    return request({
        url: `/api/v1/admin/roles/${id}`,
        method: 'get'
    })
}

/**
 * 创建角色
 */
export function createRole(data) {
    return request({
        url: '/api/v1/admin/roles',
        method: 'post',
        data
    })
}

/**
 * 更新角色
 */
export function updateRole(id, data) {
    return request({
        url: `/api/v1/admin/roles/${id}`,
        method: 'put',
        data
    })
}

/**
 * 删除角色
 */
export function deleteRole(id) {
    return request({
        url: `/api/v1/admin/roles/${id}`,
        method: 'delete'
    })
}

/**
 * 绑定权限
 */
export function assignPermissions(id, permissionIds) {
    return request({
        url: `/api/v1/admin/roles/${id}/permissions`,
        method: 'post',
        data: { permission_ids: permissionIds }
    })
}

/**
 * 绑定菜单
 */
export function assignMenus(id, menuIds) {
    return request({
        url: `/api/v1/admin/roles/${id}/menus`,
        method: 'post',
        data: { menu_ids: menuIds }
    })
}

/**
 * 获取角色的权限
 */
export function getRolePermissions(id) {
    return request({
        url: `/api/v1/admin/roles/${id}/permissions`,
        method: 'get'
    })
}

/**
 * 获取角色的菜单
 */
export function getRoleMenus(id) {
    return request({
        url: `/api/v1/admin/roles/${id}/menus`,
        method: 'get'
    })
}
