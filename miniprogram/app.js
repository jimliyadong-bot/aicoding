// app.js
const { request } = require('./utils/request')

App({
    onLaunch() {
        // 检查登录状态
        const token = wx.getStorageSync('token')
        if (!token) {
            // 未登录,跳转到登录页
            wx.redirectTo({
                url: '/pages/login/login'
            })
        }
    },

    globalData: {
        userInfo: null,
        apiBaseUrl: 'http://localhost:8000'  // 后端 API 地址
    }
})
