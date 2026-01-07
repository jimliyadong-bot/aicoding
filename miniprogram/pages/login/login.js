// pages/login/login.js
const { loginByCode } = require('../../api/auth')

Page({
    data: {
        loading: false
    },

    /**
     * 处理登录
     */
    handleLogin() {
        this.setData({ loading: true })

        wx.login({
            success: (res) => {
                if (res.code) {
                    // 调用后端接口
                    loginByCode(res.code).then(data => {
                        // 保存 token
                        wx.setStorageSync('token', data.access_token)
                        wx.setStorageSync('refresh_token', data.refresh_token)

                        // 跳转首页
                        wx.switchTab({
                            url: '/pages/index/index'
                        })

                        wx.showToast({
                            title: '登录成功',
                            icon: 'success'
                        })
                    }).catch(err => {
                        console.error('登录失败:', err)
                    }).finally(() => {
                        this.setData({ loading: false })
                    })
                } else {
                    wx.showToast({
                        title: '获取 code 失败',
                        icon: 'none'
                    })
                    this.setData({ loading: false })
                }
            },
            fail: () => {
                wx.showToast({
                    title: '登录失败',
                    icon: 'none'
                })
                this.setData({ loading: false })
            }
        })
    }
})
