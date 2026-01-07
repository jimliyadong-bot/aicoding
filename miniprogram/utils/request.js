/**
 * API 请求封装
 */
const app = getApp()

/**
 * 发起请求
 */
function request(options) {
    const { url, method = 'GET', data = {}, needAuth = true } = options

    return new Promise((resolve, reject) => {
        const token = wx.getStorageSync('token')
        const header = {
            'Content-Type': 'application/json'
        }

        if (needAuth && token) {
            header['Authorization'] = `Bearer ${token}`
        }

        wx.request({
            url: `${app.globalData.apiBaseUrl}${url}`,
            method,
            data,
            header,
            success: (res) => {
                if (res.statusCode === 200) {
                    if (res.data.code === 200) {
                        resolve(res.data.data)
                    } else {
                        wx.showToast({
                            title: res.data.message || '请求失败',
                            icon: 'none'
                        })
                        reject(res.data)
                    }
                } else if (res.statusCode === 401) {
                    // Token 过期,跳转登录
                    wx.removeStorageSync('token')
                    wx.redirectTo({
                        url: '/pages/login/login'
                    })
                    reject(res.data)
                } else {
                    wx.showToast({
                        title: '网络错误',
                        icon: 'none'
                    })
                    reject(res.data)
                }
            },
            fail: (err) => {
                wx.showToast({
                    title: '网络错误',
                    icon: 'none'
                })
                reject(err)
            }
        })
    })
}

module.exports = {
    request
}
