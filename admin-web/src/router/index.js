/**
 * 路由配置
 */
import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { ElMessage } from 'element-plus'

// 静态路由
const staticRoutes = [
    {
        path: '/login',
        name: 'Login',
        component: () => import('@/views/login/index.vue'),
        meta: { title: '登录', requiresAuth: false }
    },
    {
        path: '/',
        redirect: '/dashboard'
    }
]

// 创建路由实例
const router = createRouter({
    history: createWebHistory(import.meta.env.BASE_URL),
    routes: staticRoutes
})

// 是否已添加动态路由
let dynamicRoutesAdded = false

// 路由守卫
router.beforeEach(async (to, from, next) => {
    const authStore = useAuthStore()
    const token = authStore.token

    // 设置页面标题
    document.title = to.meta.title ? `${to.meta.title} - YiYa AI Reader` : 'YiYa AI Reader'

    if (to.path === '/login') {
        // 已登录则跳转到首页
        if (token) {
            next('/')
        } else {
            next()
        }
    } else {
        // 需要登录
        if (!token) {
            next('/login')
            return
        }

        // 添加动态路由
        if (!dynamicRoutesAdded && authStore.menus.length > 0) {
            try {
                addDynamicRoutes(authStore.menus)
                dynamicRoutesAdded = true
                // 重新导航到目标路由
                next({ ...to, replace: true })
            } catch (error) {
                console.error('添加动态路由失败:', error)
                ElMessage.error('加载菜单失败')
                next('/login')
            }
        } else if (!dynamicRoutesAdded) {
            // 还没有菜单数据,先获取
            try {
                await authStore.getMenus()
                if (authStore.menus.length > 0) {
                    addDynamicRoutes(authStore.menus)
                    dynamicRoutesAdded = true
                    next({ ...to, replace: true })
                } else {
                    next()
                }
            } catch (error) {
                console.error('获取菜单失败:', error)
                next()
            }
        } else {
            next()
        }
    }
})

/**
 * 添加动态路由
 */
function addDynamicRoutes(menus) {
    // Layout 组件
    const Layout = () => import('@/components/Layout/index.vue')

    // 将菜单转换为路由
    const routes = menuToRoutes(menus)

    // 添加到路由
    routes.forEach(route => {
        router.addRoute(route)
    })

    // 添加 404 路由
    router.addRoute({
        path: '/:pathMatch(.*)*',
        name: 'NotFound',
        component: () => import('@/views/404.vue')
    })
}

/**
 * 菜单转路由
 */
function menuToRoutes(menus) {
    const Layout = () => import('@/components/Layout/index.vue')
    const routes = []

    menus.forEach(menu => {
        const route = {
            path: menu.path,
            name: menu.name,
            component: menu.component === 'Layout' ? Layout : loadView(menu.component),
            meta: {
                title: menu.meta.title,
                icon: menu.meta.icon,
                hidden: menu.meta.hidden,
                keepAlive: menu.meta.keepAlive
            },
            children: []
        }

        // 处理子路由
        if (menu.children && menu.children.length > 0) {
            route.children = menuToRoutes(menu.children)
        }

        routes.push(route)
    })

    return routes
}

/**
 * 视图组件映射
 */
const viewModules = import.meta.glob('@/views/**/*.vue')

/**
 * 加载视图组件
 */
function loadView(view) {
    if (!view) {
        return () => import('@/views/404.vue')
    }

    // 标准化路径:移除 views/ 前缀(如果有)
    let normalizedPath = view.replace(/^views\//, '')

    // 尝试多种路径格式
    const pathsToTry = [
        `/src/views/${normalizedPath}`,  // views/dashboard/index.vue -> /src/views/dashboard/index.vue
        `/src/views/${normalizedPath}/index.vue`,  // dashboard -> /src/views/dashboard/index.vue
        `/src/views/${view}`,  // 原始路径
        `/src/views/${view}/index.vue`  // 原始路径 + index.vue
    ]

    for (const path of pathsToTry) {
        if (viewModules[path]) {
            return viewModules[path]
        }
    }

    console.warn(`View not found: ${view}, tried paths:`, pathsToTry)
    return () => import('@/views/404.vue')
}

/**
 * 重置路由
 */
export function resetRouter() {
    dynamicRoutesAdded = false
    // 重新创建路由实例
    const newRouter = createRouter({
        history: createWebHistory(import.meta.env.BASE_URL),
        routes: staticRoutes
    })
    router.matcher = newRouter.matcher
}

export default router
