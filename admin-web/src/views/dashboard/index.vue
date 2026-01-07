<template>
  <div class="dashboard">
    <el-card>
      <template #header>
        <div class="card-header">
          <span>仪表盘</span>
        </div>
      </template>
      <div class="dashboard-content">
        <el-row :gutter="20">
          <el-col :span="6">
            <el-statistic title="用户总数" :value="1000">
              <template #prefix>
                <el-icon><User /></el-icon>
              </template>
            </el-statistic>
          </el-col>
          <el-col :span="6">
            <el-statistic title="今日访问" :value="500">
              <template #prefix>
                <el-icon><View /></el-icon>
              </template>
            </el-statistic>
          </el-col>
          <el-col :span="6">
            <el-statistic title="消息数" :value="20">
              <template #prefix>
                <el-icon><Message /></el-icon>
              </template>
            </el-statistic>
          </el-col>
          <el-col :span="6">
            <el-statistic title="订单数" :value="150">
              <template #prefix>
                <el-icon><ShoppingCart /></el-icon>
              </template>
            </el-statistic>
          </el-col>
        </el-row>
        
        <el-divider />
        
        <div class="welcome">
          <h2>欢迎使用 YiYa AI Reader 管理平台</h2>
          <p>当前用户: {{ user?.username }}</p>
          <p>角色: {{ user?.real_name }}</p>
          
          <el-divider />
          
          <h3>权限测试</h3>
          <div class="permission-test">
            <el-button type="primary" v-perm="'sys:user:create'">
              创建用户 (需要 sys:user:create 权限)
            </el-button>
            <el-button type="success" v-perm="'sys:role:create'">
              创建角色 (需要 sys:role:create 权限)
            </el-button>
            <el-button type="warning" v-perm="'sys:demo:view'">
              查看示例 (需要 sys:demo:view 权限)
            </el-button>
          </div>
          
          <el-alert
            title="提示"
            type="info"
            :closable="false"
            style="margin-top: 20px"
          >
            上面的按钮会根据当前用户的权限自动显示或隐藏。超级管理员可以看到所有按钮。
          </el-alert>
        </div>
      </div>
    </el-card>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { User, View, Message, ShoppingCart } from '@element-plus/icons-vue'

const authStore = useAuthStore()
const user = computed(() => authStore.user)
</script>

<style scoped lang="scss">
.dashboard {
  .card-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
  }
  
  .dashboard-content {
    .welcome {
      h2 {
        margin-bottom: 20px;
        color: #333;
      }
      
      p {
        margin: 10px 0;
        color: #666;
      }
      
      h3 {
        margin: 20px 0;
        color: #333;
      }
      
      .permission-test {
        display: flex;
        gap: 10px;
        flex-wrap: wrap;
      }
    }
  }
}
</style>
