/**
 * 认证相关 API
 */
const { request } = require('../utils/request')

/**
 * 通过 code 登录
 */
function loginByCode(code) {
    return request({
        url: '/api/v1/mp/auth/login_by_code',
        method: 'POST',
        data: { code },
        needAuth: false
    })
}

/**
 * 绑定手机号
 */
function bindPhone(code) {
    return request({
        url: '/api/v1/mp/auth/bind_phone',
        method: 'POST',
        data: { code }
    })
}

module.exports = {
    loginByCode,
    bindPhone
}
