<template>
  <div class="role-management">
    <el-card class="search-card">
      <el-form :inline="true">
        <el-form-item>
          <el-button type="success" @click="handleAdd" v-perm="'sys:role:create'">新增角色</el-button>
        </el-form-item>
      </el-form>
    </el-card>

    <el-card class="table-card">
      <el-table :data="tableData" border stripe v-loading="loading">
        <el-table-column prop="id" label="ID" width="80" />
        <el-table-column prop="name" label="角色名称" />
        <el-table-column prop="code" label="角色编码" />
        <el-table-column prop="description" label="描述" />
        <el-table-column prop="status" label="状态" width="100">
          <template #default="{ row }">
            <el-tag :type="row.status === 1 ? 'success' : 'danger'">
              {{ row.status === 1 ? '启用' : '禁用' }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="350" fixed="right">
          <template #default="{ row }">
            <el-button type="primary" size="small" @click="handleEdit(row)" v-perm="'sys:role:update'">编辑</el-button>
            <el-button type="warning" size="small" @click="handleAssignPermissions(row)" v-perm="'sys:role:assign'">绑定权限</el-button>
            <el-button type="success" size="small" @click="handleAssignMenus(row)" v-perm="'sys:role:assign'">绑定菜单</el-button>
            <el-button type="danger" size="small" @click="handleDelete(row)" v-perm="'sys:role:delete'">删除</el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>

    <!-- 新增/编辑 Drawer -->
    <el-drawer v-model="drawerVisible" :title="drawerTitle" size="600px">
      <el-form :model="formData" :rules="rules" ref="formRef" label-width="100px">
        <el-form-item label="角色名称" prop="name">
          <el-input v-model="formData.name" placeholder="请输入角色名称" />
        </el-form-item>
        <el-form-item label="角色编码" prop="code">
          <el-input v-model="formData.code" placeholder="请输入角色编码" :disabled="isEdit" />
        </el-form-item>
        <el-form-item label="描述" prop="description">
          <el-input v-model="formData.description" type="textarea" placeholder="请输入描述" />
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

    <!-- 绑定权限 Drawer -->
    <el-drawer v-model="permissionDrawerVisible" title="绑定权限" size="600px">
      <el-tree
        ref="permissionTreeRef"
        :data="permissionTree"
        show-checkbox
        node-key="id"
        :props="{ children: 'children', label: 'name' }"
      />
      <template #footer>
        <el-button @click="permissionDrawerVisible = false">取消</el-button>
        <el-button type="primary" @click="handleSubmitPermissions" :loading="submitting">确定</el-button>
      </template>
    </el-drawer>

    <!-- 绑定菜单 Drawer -->
    <el-drawer v-model="menuDrawerVisible" title="绑定菜单" size="600px">
      <el-tree
        ref="menuTreeRef"
        :data="menuTree"
        show-checkbox
        node-key="id"
        :props="{ children: 'children', label: 'title' }"
      />
      <template #footer>
        <el-button @click="menuDrawerVisible = false">取消</el-button>
        <el-button type="primary" @click="handleSubmitMenus" :loading="submitting">确定</el-button>
      </template>
    </el-drawer>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { getRoleList, createRole, updateRole, deleteRole, assignPermissions, assignMenus, getRolePermissions, getRoleMenus } from '@/api/role'
import { getPermissionTree } from '@/api/permission'
import { getMenuTree } from '@/api/menu'

const loading = ref(false)
const submitting = ref(false)
const drawerVisible = ref(false)
const permissionDrawerVisible = ref(false)
const menuDrawerVisible = ref(false)
const isEdit = ref(false)
const formRef = ref(null)
const permissionTreeRef = ref(null)
const menuTreeRef = ref(null)

const tableData = ref([])
const permissionTree = ref([])
const menuTree = ref([])
const currentRoleId = ref(null)

const formData = reactive({
  id: null,
  name: '',
  code: '',
  description: '',
  status: 1
})

const rules = {
  name: [{ required: true, message: '请输入角色名称', trigger: 'blur' }],
  code: [{ required: true, message: '请输入角色编码', trigger: 'blur' }]
}

const drawerTitle = ref('新增角色')

const loadData = async () => {
  loading.value = true
  try {
    const res = await getRoleList()
    if (res.code === 200) {
      tableData.value = res.data || []
    }
  } catch (error) {
    console.error('加载数据失败:', error)
  } finally {
    loading.value = false
  }
}

const handleAdd = () => {
  isEdit.value = false
  drawerTitle.value = '新增角色'
  Object.assign(formData, { id: null, name: '', code: '', description: '', status: 1 })
  drawerVisible.value = true
}

const handleEdit = (row) => {
  isEdit.value = true
  drawerTitle.value = '编辑角色'
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
        const res = isEdit.value ? await updateRole(formData.id, data) : await createRole(data)
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
    await ElMessageBox.confirm('确定要删除该角色吗?', '提示', { type: 'warning' })
    const res = await deleteRole(row.id)
    if (res.code === 200) {
      ElMessage.success('删除成功')
      loadData()
    }
  } catch (error) {
    if (error !== 'cancel') console.error('删除失败:', error)
  }
}

const handleAssignPermissions = async (row) => {
  currentRoleId.value = row.id
  const [permRes, rolePermRes] = await Promise.all([
    getPermissionTree(),
    getRolePermissions(row.id)
  ])
  if (permRes.code === 200) permissionTree.value = permRes.data || []
  if (rolePermRes.code === 200) {
    const checkedKeys = rolePermRes.data.map(p => p.id)
    setTimeout(() => permissionTreeRef.value?.setCheckedKeys(checkedKeys), 100)
  }
  permissionDrawerVisible.value = true
}

const handleSubmitPermissions = async () => {
  submitting.value = true
  try {
    const checkedKeys = permissionTreeRef.value?.getCheckedKeys() || []
    const res = await assignPermissions(currentRoleId.value, checkedKeys)
    if (res.code === 200) {
      ElMessage.success('绑定成功')
      permissionDrawerVisible.value = false
    }
  } catch (error) {
    console.error('绑定失败:', error)
  } finally {
    submitting.value = false
  }
}

const handleAssignMenus = async (row) => {
  currentRoleId.value = row.id
  const [menuRes, roleMenuRes] = await Promise.all([
    getMenuTree(true),
    getRoleMenus(row.id)
  ])
  if (menuRes.code === 200) menuTree.value = menuRes.data || []
  if (roleMenuRes.code === 200) {
    const checkedKeys = roleMenuRes.data.map(m => m.id)
    setTimeout(() => menuTreeRef.value?.setCheckedKeys(checkedKeys), 100)
  }
  menuDrawerVisible.value = true
}

const handleSubmitMenus = async () => {
  submitting.value = true
  try {
    const checkedKeys = menuTreeRef.value?.getCheckedKeys() || []
    const res = await assignMenus(currentRoleId.value, checkedKeys)
    if (res.code === 200) {
      ElMessage.success('绑定成功')
      menuDrawerVisible.value = false
    }
  } catch (error) {
    console.error('绑定失败:', error)
  } finally {
    submitting.value = false
  }
}

onMounted(() => {
  loadData()
})
</script>

<style scoped lang="scss">
.role-management {
  .search-card {
    margin-bottom: 20px;
  }
}
</style>
