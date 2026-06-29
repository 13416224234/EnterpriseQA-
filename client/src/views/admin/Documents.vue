<template>
  <div class="admin-docs">
    <h3 class="page-title">文档管理</h3>
    <el-card shadow="hover">
      <el-upload drag multiple :auto-upload="false" :on-change="handleFileAdd" accept=".txt,.pdf,.docx,.md">
        <el-icon class="upload-icon" :size="48"><UploadFilled /></el-icon>
        <div>拖拽文件到此处，或<em>点击上传</em></div>
        <template #tip><div style="font-size:12px;color:#909399;margin-top:8px">支持 txt/pdf/docx/md，最大50MB，可多选</div></template>
      </el-upload>
      <div v-if="fileList.length > 0" style="margin-top:12px">
        <el-tag v-for="f in fileList" :key="f.uid" closable @close="removeFile(f)" style="margin-right:8px">{{ f.name }}</el-tag>
        <el-button type="primary" :loading="uploading" @click="uploadAll" style="margin-left:8px">上传全部</el-button>
      </div>
    </el-card>
    <el-card shadow="hover" style="margin-top:16px">
      <el-table :data="docList" stripe style="width:100%">
        <el-table-column prop="id" label="ID" width="60" />
        <el-table-column prop="filename" label="文件名" min-width="200" />
        <el-table-column prop="file_type" label="类型" width="80" />
        <el-table-column prop="file_size" label="大小" width="100">
          <template #default="{ row }">{{ row.file_size ? (row.file_size / 1024).toFixed(1) + ' KB' : '-' }}</template>
        </el-table-column>
        <el-table-column prop="created_at" label="上传时间" width="170" />
        <el-table-column label="操作" width="120">
          <template #default="{ row }">
            <el-button size="small" type="danger" @click="deleteDoc(row)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>
      <el-pagination v-model:current-page="page" :page-size="perPage" :total="total"
        layout="prev, pager, next, total" style="margin-top:16px;justify-content:center"
        @current-change="fetchDocs" />
    </el-card>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue"
import { documentApi } from "../../api/index.js"
import { ElMessage, ElMessageBox } from "element-plus"
import { UploadFilled } from "@element-plus/icons-vue"

const docList = ref([])
const fileList = ref([])
const page = ref(1); const perPage = ref(10); const total = ref(0)
const uploading = ref(false)

async function fetchDocs() {
  const res = await documentApi.getList({ page: page.value, per_page: perPage.value })
  if (res.code === 200) { docList.value = res.data.items; total.value = res.data.total }
}
function handleFileAdd(file) { fileList.value.push(file) }
function removeFile(file) { fileList.value = fileList.value.filter(f => f.uid !== file.uid) }
async function uploadAll() {
  if (fileList.value.length === 0) { ElMessage.warning("请选择文件"); return }
  uploading.value = true
  for (const file of fileList.value) {
    const fd = new FormData()
    fd.append("file", file.raw)
    try {
      const res = await documentApi.upload(fd)
      if (res.code === 200) ElMessage.success(file.name + " 上传成功")
      else ElMessage.error(file.name + " " + res.msg)
    } catch (e) { ElMessage.error(file.name + " 上传失败") }
  }
  fileList.value = []
  uploading.value = false
  fetchDocs()
}
async function deleteDoc(row) {
  ElMessageBox.confirm("删除文档 " + row.filename + "？", "提示").then(async () => {
    const res = await documentApi.delete(row.id)
    if (res.code === 200) { ElMessage.success("已删除"); fetchDocs() }
  }).catch(() => {})
}
onMounted(() => { fetchDocs() })
</script>
<style scoped>
.page-title { margin: 0 0 16px; font-size: 18px; color: #303133; }
.upload-icon { margin-bottom: 8px; }
</style>