/**
 * 用户相关 API
 */
const { request } = require('../utils/request')

/**
 * 获取当前用户信息
 */
function getUserInfo() {
    return request({
        url: '/api/v1/mp/user/me',
        method: 'GET'
    })
}

/**
 * 更新用户信息
 */
function updateUserInfo(data) {
    return request({
        url: '/api/v1/mp/user/me',
        method: 'PUT',
        data
    })
}

module.exports = {
    getUserInfo,
    updateUserInfo
}
