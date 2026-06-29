<template>
  <div class="admin-users">
    <h3 class="page-title">用户管理</h3>
    <el-card shadow="hover" class="search-card">
      <el-form :inline="true">
        <el-form-item label="关键词">
          <el-input v-model="keyword" placeholder="搜索用户名" clearable @clear="search" @keyup.enter="search" />
        </el-form-item>
        <el-form-item><el-button type="primary" @click="search">搜索</el-button></el-form-item>
      </el-form>
    </el-card>
    <el-card shadow="hover" style="margin-top: 16px">
      <el-table :data="userList" stripe style="width: 100%">
        <el-table-column prop="id" label="ID" width="60" />
        <el-table-column prop="username" label="用户名" width="120" />
        <el-table-column prop="real_name" label="真实姓名" width="120" />
        <el-table-column prop="email" label="邮箱" />
        <el-table-column prop="role" label="角色" width="100">
          <template #default="{ row }">
            <el-tag :type="row.role === 'admin' ? 'danger' : 'primary'">{{ row.role === "admin" ? "管理员" : "普通用户" }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="status" label="状态" width="100">
          <template #default="{ row }">
            <el-tag :type="row.status === 1 ? 'success' : 'info'">{{ row.status === 1 ? "正常" : "禁用" }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="created_at" label="创建时间" width="170" />
        <el-table-column label="操作" width="180">
          <template #default="{ row }">
            <el-button size="small" @click="toggleStatus(row)">{{ row.status === 1 ? "禁用" : "启用" }}</el-button>
            <el-button size="small" type="danger" @click="handleDelete(row)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>
      <el-pagination v-model:current-page="page" :page-size="perPage" :total="total"
        layout="prev, pager, next, total" style="margin-top: 16px; justify-content: center"
        @current-change="fetchUsers" />
    </el-card>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue"
import { adminApi } from "../../api/index.js"
import { ElMessage, ElMessageBox } from "element-plus"

const userList = ref([])
const page = ref(1)
const perPage = ref(10)
const total = ref(0)
const keyword = ref("")

async function fetchUsers() {
  const res = await adminApi.getUsers({ page: page.value, per_page: perPage.value, keyword: keyword.value })
  if (res.code === 200) { userList.value = res.data.items; total.value = res.data.total }
}
function search() { page.value = 1; fetchUsers() }
async function toggleStatus(row) {
  const newStatus = row.status === 1 ? 0 : 1
  const res = await adminApi.updateUser(row.id, { status: newStatus })
  if (res.code === 200) { ElMessage.success(newStatus === 1 ? "已启用" : "已禁用"); fetchUsers() }
}
async function handleDelete(row) {
  ElMessageBox.confirm("确定删除用户 " + row.username + " 吗？", "提示").then(async () => {
    const res = await adminApi.deleteUser(row.id)
    if (res.code === 200) { ElMessage.success("删除成功"); fetchUsers() }
  }).catch(() => {})
}
onMounted(fetchUsers)
</script>
<style scoped>
.page-title { margin: 0 0 16px; font-size: 18px; color: #303133; }
.search-card .el-form { margin-bottom: -18px; }
</style>
