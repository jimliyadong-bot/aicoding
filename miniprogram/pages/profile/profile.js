// pages/profile/profile.js
const { getUserInfo, updateUserInfo } = require('../../api/user')
const { bindPhone } = require('../../api/auth')

Page({
    data: {
        userInfo: {},
        nickname: ''
    },

    onLoad() {
        this.loadUserInfo()
    },

    /**
     * 加载用户信息
     */
    loadUserInfo() {
        getUserInfo().then(data => {
            this.setData({
                userInfo: data,
                nickname: data.nickname || ''
            })
        }).catch(err => {
            console.error('获取用户信息失败:', err)
        })
    },

    /**
     * 昵称输入
     */
    onNicknameInput(e) {
        this.setData({
            nickname: e.detail.value
        })
    },

    /**
     * 上传头像(占位实现)
     */
    handleUploadAvatar() {
        wx.showToast({
            title: '上传头像功能开发中',
            icon: 'none'
        })
    },

    /**
     * 获取手机号
     */
    handleGetPhoneNumber(e) {
        if (e.detail.code) {
            bindPhone(e.detail.code).then(data => {
                wx.showToast({
                    title: '绑定成功',
                    icon: 'success'
                })
                // 重新加载用户信息
                this.loadUserInfo()
            }).catch(err => {
                console.error('绑定手机号失败:', err)
            })
        } else {
            wx.showToast({
                title: '获取手机号失败',
                icon: 'none'
            })
        }
    },

    /**
     * 保存修改
     */
    handleSave() {
        const { nickname } = this.data

        if (!nickname) {
            wx.showToast({
                title: '请输入昵称',
                icon: 'none'
            })
            return
        }

        updateUserInfo({ nickname }).then(data => {
            wx.showToast({
                title: '保存成功',
                icon: 'success'
            })
            this.setData({
                userInfo: data
            })
        }).catch(err => {
            console.error('保存失败:', err)
        })
    }
})
