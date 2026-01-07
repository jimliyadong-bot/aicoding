/**
 * 权限指令
 * 用法: v-perm="'sys:user:list'" 或 v-perm="['sys:user:create', 'sys:user:update']"
 */
import { useAuthStore } from '@/stores/auth'

export default {
    mounted(el, binding) {
        const { value } = binding
        const authStore = useAuthStore()

        if (!value) {
            return
        }

        const hasPermission = authStore.hasPermission(value)

        if (!hasPermission) {
            // 移除元素
            el.parentNode?.removeChild(el)
        }
    }
}
