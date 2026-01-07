/**
 * 菜单相关 API
 */
import request from '@/utils/request'

/**
 * 获取我的菜单树(动态路由)
 */
export function getMyMenus() {
    return request({
        url: '/api/v1/admin/menus/my',
        method: 'get'
    })
}

/**
 * 获取菜单树
 */
export function getMenuTree(includeDisabled = false) {
    return request({
        url: '/api/v1/admin/menus/tree',
        method: 'get',
        params: {
            include_disabled: includeDisabled
        }
    })
}

/**
 * 获取菜单详情
 */
export function getMenuDetail(id) {
    return request({
        url: `/api/v1/admin/menus/${id}`,
        method: 'get'
    })
}

/**
 * 创建菜单
 */
export function createMenu(data) {
    return request({
        url: '/api/v1/admin/menus',
        method: 'post',
        data
    })
}

/**
 * 更新菜单
 */
export function updateMenu(id, data) {
    return request({
        url: `/api/v1/admin/menus/${id}`,
        method: 'put',
        data
    })
}

/**
 * 删除菜单
 */
export function deleteMenu(id) {
    return request({
        url: `/api/v1/admin/menus/${id}`,
        method: 'delete'
    })
}

/**
 * 更新菜单排序
 */
export function updateMenuSort(id, sort) {
    return request({
        url: `/api/v1/admin/menus/${id}/sort`,
        method: 'put',
        data: { sort }
    })
}
