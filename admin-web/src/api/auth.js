/**
 * 认证相关 API
 */
import request from '@/utils/request'

/**
 * 登录
 */
export function login(data) {
    return request({
        url: '/api/v1/admin/auth/login',
        method: 'post',
        data
    })
}

/**
 * 刷新 token
 */
export function refreshToken(refreshToken) {
    return request({
        url: '/api/v1/admin/auth/refresh',
        method: 'post',
        data: {
            refresh_token: refreshToken
        }
    })
}

/**
 * 获取当前用户信息
 */
export function getUserInfo() {
    return request({
        url: '/api/v1/admin/auth/me',
        method: 'get'
    })
}

/**
 * 登出
 */
export function logout(refreshToken) {
    return request({
        url: '/api/v1/admin/auth/logout',
        method: 'post',
        data: {
            refresh_token: refreshToken
        }
    })
}
