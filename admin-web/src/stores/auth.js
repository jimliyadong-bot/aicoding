/**
 * 认证 Store
 * 管理用户登录状态、token、用户信息、权限和菜单
 */
import { defineStore } from 'pinia'
import { ref } from 'vue'
import * as authApi from '@/api/auth'
import { getMyMenus } from '@/api/menu'
import { setToken, setRefreshToken, getRefreshToken, clearAuth } from '@/utils/auth'

export const useAuthStore = defineStore('auth', () => {
    // 状态
    const token = ref(localStorage.getItem('access_token') || '')
    const refreshTokenValue = ref(localStorage.getItem('refresh_token') || '')
    const user = ref(null)
    const permissions = ref([])
    const menus = ref([])

    /**
     * 登录
     */
    async function login(username, password) {
        try {
            const res = await authApi.login({ username, password })

            if (res.code === 200) {
                const { access_token, refresh_token } = res.data

                // 保存 token
                token.value = access_token
                refreshTokenValue.value = refresh_token
                setToken(access_token)
                setRefreshToken(refresh_token)

                // 获取用户信息
                await getUserInfo()

                // 获取菜单
                await getMenus()

                return true
            }

            return false
        } catch (error) {
            console.error('登录失败:', error)
            return false
        }
    }

    /**
     * 刷新 token
     */
    async function refreshToken() {
        try {
            const refresh = getRefreshToken()
            if (!refresh) {
                return null
            }

            const res = await authApi.refreshToken(refresh)

            if (res.code === 200) {
                const { access_token } = res.data
                token.value = access_token
                setToken(access_token)
                return access_token
            }

            return null
        } catch (error) {
            console.error('刷新 token 失败:', error)
            throw error
        }
    }

    /**
     * 获取用户信息
     */
    async function getUserInfo() {
        try {
            const res = await authApi.getUserInfo()

            if (res.code === 200) {
                user.value = res.data

                if (Array.isArray(res.data.permissions)) {
                    permissions.value = res.data.permissions
                }
            }
        } catch (error) {
            console.error('获取用户信息失败:', error)
        }
    }

    /**
     * 获取菜单列表
     */
    async function getMenus() {
        try {
            const res = await getMyMenus()

            if (res.code === 200) {
                menus.value = res.data

                // 从菜单中提取权限(如果需要)
                extractPermissions(res.data)
            }
        } catch (error) {
            console.error('获取菜单失败:', error)
            throw error // 抛出错误供调用方处理
        }
    }

    /**
     * 从菜单中提取权限
     */
    function extractPermissions(menuList) {
        const perms = []

        function extract(menus) {
            menus.forEach(menu => {
                // 如果菜单有权限标识,添加到权限列表
                if (menu.permission) {
                    perms.push(menu.permission)
                }

                // 递归处理子菜单
                if (menu.children && menu.children.length > 0) {
                    extract(menu.children)
                }
            })
        }

        extract(menuList)
        if (perms.length > 0) {
            permissions.value = perms
        }
    }

    /**
     * 登出
     */
    async function logout() {
        try {
            const refresh = getRefreshToken()
            if (refresh) {
                await authApi.logout(refresh)
            }
        } catch (error) {
            console.error('登出失败:', error)
        } finally {
            // 清除状态
            token.value = ''
            refreshTokenValue.value = ''
            user.value = null
            permissions.value = []
            menus.value = []
            clearAuth()
        }
    }

    /**
     * 检查是否有权限
     */
    function hasPermission(permission) {
        if (!permission) return true

        if (Array.isArray(permission)) {
            return permission.some(p => permissions.value.includes(p))
        }

        return permissions.value.includes(permission)
    }

    return {
        token,
        refreshTokenValue,
        user,
        permissions,
        menus,
        login,
        refreshToken,
        getUserInfo,
        getMenus,
        logout,
        hasPermission
    }
})
