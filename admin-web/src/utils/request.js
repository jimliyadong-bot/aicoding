/**
 * axios 封装
 * 功能:
 * 1. 自动添加 Authorization 头
 * 2. 401 自动刷新 token 并重试
 * 3. 统一错误提示
 */
import axios from 'axios'
import { ElMessage } from 'element-plus'
import { useAuthStore } from '@/stores/auth'
import router from '@/router'

// 创建 axios 实例
const request = axios.create({
    baseURL: import.meta.env.VITE_API_BASE_URL,
    timeout: 30000
})

// 是否正在刷新 token
let isRefreshing = false
// 待重试的请求队列
let requests = []

// 请求拦截器
request.interceptors.request.use(
    config => {
        const authStore = useAuthStore()
        const token = authStore.token

        if (token) {
            config.headers.Authorization = `Bearer ${token}`
        }

        return config
    },
    error => {
        return Promise.reject(error)
    }
)

// 响应拦截器
request.interceptors.response.use(
    response => {
        // 返回 data 字段
        return response.data
    },
    async error => {
        const { config, response } = error

        // 401 未授权
        if (response?.status === 401 && !config._retry) {
            if (!isRefreshing) {
                isRefreshing = true
                config._retry = true

                try {
                    const authStore = useAuthStore()
                    // 尝试刷新 token
                    const newToken = await authStore.refreshToken()

                    if (newToken) {
                        // 更新请求头
                        config.headers.Authorization = `Bearer ${newToken}`

                        // 重试所有待处理的请求
                        requests.forEach(cb => cb(newToken))
                        requests = []

                        // 重试当前请求
                        return request(config)
                    }
                } catch (refreshError) {
                    // 刷新失败,清除登录状态并跳转登录页
                    const authStore = useAuthStore()
                    authStore.logout()
                    router.push('/login')
                    ElMessage.error('登录已过期,请重新登录')
                    return Promise.reject(refreshError)
                } finally {
                    isRefreshing = false
                }
            } else {
                // 正在刷新 token,将请求加入队列
                return new Promise(resolve => {
                    requests.push(token => {
                        config.headers.Authorization = `Bearer ${token}`
                        resolve(request(config))
                    })
                })
            }
        }

        // 其他错误
        const message = response?.data?.message || error.message || '请求失败'
        ElMessage.error(message)

        return Promise.reject(error)
    }
)

export default request
