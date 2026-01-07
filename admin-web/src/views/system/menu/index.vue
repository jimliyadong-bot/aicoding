<template>
  <div class="menu-management">
    <el-card class="search-card">
      <el-form :inline="true">
        <el-form-item>
          <el-button type="success" @click="handleAdd(null)" v-perm="'sys:menu:create'">新增菜单</el-button>
        </el-form-item>
      </el-form>
    </el-card>

    <el-card class="table-card">
      <el-table
        :data="tableData"
        border
        stripe
        v-loading="loading"
        row-key="id"
        :tree-props="{ children: 'children' }"
      >
        <el-table-column prop="title" label="菜单标题" width="200" />
        <el-table-column prop="name" label="路由名称" />
        <el-table-column prop="path" label="路由路径" />
        <el-table-column prop="component" label="组件路径" />
        <el-table-column prop="icon" label="图标" width="80">
          <template #default="{ row }">
            <el-icon v-if="row.icon"><component :is="row.icon" /></el-icon>
          </template>
        </el-table-column>
        <el-table-column prop="sort" label="排序" width="80" />
        <el-table-column prop="hidden" label="隐藏" width="80">
          <template #default="{ row }">
            <el-tag :type="row.hidden === 1 ? 'danger' : 'success'">
              {{ row.hidden === 1 ? '是' : '否' }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="status" label="状态" width="80">
          <template #default="{ row }">
            <el-tag :type="row.status === 1 ? 'success' : 'danger'">
              {{ row.status === 1 ? '启用' : '禁用' }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="250" fixed="right">
          <template #default="{ row }">
            <el-button type="success" size="small" @click="handleAdd(row)" v-perm="'sys:menu:create'">新增子菜单</el-button>
            <el-button type="primary" size="small" @click="handleEdit(row)" v-perm="'sys:menu:update'">编辑</el-button>
            <el-button type="danger" size="small" @click="handleDelete(row)" v-perm="'sys:menu:delete'">删除</el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>

    <!-- 新增/编辑 Drawer -->
    <el-drawer v-model="drawerVisible" :title="drawerTitle" size="600px">
      <el-form :model="formData" :rules="rules" ref="formRef" label-width="100px">
        <el-form-item label="父菜单" prop="parent_id">
          <el-tree-select
            v-model="formData.parent_id"
            :data="menuTreeOptions"
            :props="{ label: 'title', value: 'id' }"
            placeholder="请选择父菜单(不选则为根菜单)"
            clearable
          />
        </el-form-item>
        <el-form-item label="菜单标题" prop="title">
          <el-input v-model="formData.title" placeholder="请输入菜单标题" />
        </el-form-item>
        <el-form-item label="路由名称" prop="name">
          <el-input v-model="formData.name" placeholder="请输入路由名称(唯一)" />
        </el-form-item>
        <el-form-item label="路由路径" prop="path">
          <el-input v-model="formData.path" placeholder="请输入路由路径" />
        </el-form-item>
        <el-form-item label="组件路径" prop="component">
          <el-input v-model="formData.component" placeholder="如: views/system/user/index.vue" />
        </el-form-item>
        <el-form-item label="图标" prop="icon">
          <el-input v-model="formData.icon" placeholder="请输入图标名称" />
        </el-form-item>
        <el-form-item label="排序" prop="sort">
          <el-input-number v-model="formData.sort" :min="0" />
        </el-form-item>
        <el-form-item label="是否隐藏" prop="hidden">
          <el-radio-group v-model="formData.hidden">
            <el-radio :label="0">否</el-radio>
            <el-radio :label="1">是</el-radio>
          </el-radio-group>
        </el-form-item>
        <el-form-item label="是否缓存" prop="keep_alive">
          <el-radio-group v-model="formData.keep_alive">
            <el-radio :label="1">是</el-radio>
            <el-radio :label="0">否</el-radio>
          </el-radio-group>
        </el-form-item>
        <el-form-item label="状态" prop="status">
          <el-radio-group v-model="formData.status">
            <el-radio :label="1">启用</el-radio>
            <el-radio :label="0">禁用</el-radio>
          </el-radio-group>
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="drawerVisible = false">取消</el-button>
        <el-button type="primary" @click="handleSubmit" :loading="submitting">确定</el-button>
      </template>
    </el-drawer>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { getMenuTree, createMenu, updateMenu, deleteMenu } from '@/api/menu'

const loading = ref(false)
const submitting = ref(false)
const drawerVisible = ref(false)
const isEdit = ref(false)
const formRef = ref(null)

const tableData = ref([])
const menuTreeOptions = ref([])

const formData = reactive({
  id: null,
  parent_id: 0,
  title: '',
  name: '',
  path: '',
  component: '',
  icon: '',
  sort: 0,
  hidden: 0,
  keep_alive: 1,
  status: 1
})

const rules = {
  title: [{ required: true, message: '请输入菜单标题', trigger: 'blur' }],
  name: [{ required: true, message: '请输入路由名称', trigger: 'blur' }]
}

const drawerTitle = ref('新增菜单')

const loadData = async () => {
  loading.value = true
  try {
    const res = await getMenuTree(true)
    if (res.code === 200) {
      tableData.value = res.data || []
      menuTreeOptions.value = [{ id: 0, title: '根菜单', children: res.data || [] }]
    }
  } catch (error) {
    console.error('加载数据失败:', error)
  } finally {
    loading.value = false
  }
}

const handleAdd = (row) => {
  isEdit.value = false
  drawerTitle.value = row ? '新增子菜单' : '新增菜单'
  Object.assign(formData, {
    id: null,
    parent_id: row ? row.id : 0,
    title: '',
    name: '',
    path: '',
    component: '',
    icon: '',
    sort: 0,
    hidden: 0,
    keep_alive: 1,
    status: 1
  })
  drawerVisible.value = true
}

const handleEdit = (row) => {
  isEdit.value = true
  drawerTitle.value = '编辑菜单'
  Object.assign(formData, row)
  drawerVisible.value = true
}

const handleSubmit = async () => {
  if (!formRef.value) return
  await formRef.value.validate(async (valid) => {
    if (valid) {
      submitting.value = true
      try {
        const data = { ...formData }
        delete data.id
        const res = isEdit.value ? await updateMenu(formData.id, data) : await createMenu(data)
        if (res.code === 200) {
          ElMessage.success(isEdit.value ? '更新成功' : '创建成功')
          drawerVisible.value = false
          loadData()
        }
      } catch (error) {
        console.error('提交失败:', error)
      } finally {
        submitting.value = false
      }
    }
  })
}

const handleDelete = async (row) => {
  try {
    await ElMessageBox.confirm('确定要删除该菜单吗?(将级联删除子菜单)', '提示', { type: 'warning' })
    const res = await deleteMenu(row.id)
    if (res.code === 200) {
      ElMessage.success('删除成功')
      loadData()
    }
  } catch (error) {
    if (error !== 'cancel') console.error('删除失败:', error)
  }
}

onMounted(() => {
  loadData()
})
</script>

<style scoped lang="scss">
.menu-management {
  .search-card {
    margin-bottom: 20px;
  }
}
</style>
