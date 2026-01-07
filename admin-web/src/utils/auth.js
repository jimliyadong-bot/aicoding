/**
 * 认证工具函数
 */

const TOKEN_KEY = 'access_token'
const REFRESH_TOKEN_KEY = 'refresh_token'

/**
 * 获取 token
 */
export function getToken() {
    return localStorage.getItem(TOKEN_KEY)
}

/**
 * 设置 token
 */
export function setToken(token) {
    localStorage.setItem(TOKEN_KEY, token)
}

/**
 * 移除 token
 */
export function removeToken() {
    localStorage.removeItem(TOKEN_KEY)
}

/**
 * 获取 refresh token
 */
export function getRefreshToken() {
    return localStorage.getItem(REFRESH_TOKEN_KEY)
}

/**
 * 设置 refresh token
 */
export function setRefreshToken(token) {
    localStorage.setItem(REFRESH_TOKEN_KEY, token)
}

/**
 * 移除 refresh token
 */
export function removeRefreshToken() {
    localStorage.removeItem(REFRESH_TOKEN_KEY)
}

/**
 * 清除所有认证信息
 */
export function clearAuth() {
    removeToken()
    removeRefreshToken()
}
