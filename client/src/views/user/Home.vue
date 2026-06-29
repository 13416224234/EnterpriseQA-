<template>
  <div class="user-home">
    <el-row :gutter="20">
      <el-col :span="16">
        <el-card shadow="hover">
          <template #header>知识文档列表</template>
          <el-table :data="docList" stripe style="width:100%">
            <el-table-column prop="title" label="文档标题" min-width="200" />
            <el-table-column prop="category_name" label="分类" width="120" />
            <el-table-column prop="file_type" label="格式" width="80" />
            <el-table-column prop="created_at" label="上传时间" width="170" />
            <el-table-column label="操作" width="120">
              <template #default="{ row }">
                <el-button size="small" type="primary" @click="openChat(row)">提问</el-button>
              </template>
            </el-table-column>
          </el-table>
          <el-pagination v-model:current-page="page" :page-size="perPage" :total="total"
            layout="prev, pager, next" style="margin-top:16px;justify-content:center"
            @current-change="fetchDocs" />
        </el-card>
      </el-col>
      <el-col :span="8">
        <el-card shadow="hover">
          <template #header>快速开始</template>
          <div class="quick-start">
            <p>欢迎使用企业知识库问答系统！</p>
            <p>您可以通过以下方式使用：</p>
            <ol>
              <li>浏览左侧文档列表，点击"提问"进入对话</li>
              <li>在"智能对话"中直接输入问题</li>
              <li>系统会从知识库中检索相关内容并回答</li>
            </ol>
            <el-divider />
            <el-button type="primary" size="large" @click="$router.push('/user/chat')" style="width:100%">
              开始智能问答
            </el-button>
          </div>
        </el-card>
        <el-card shadow="hover" style="margin-top:16px">
          <template #header>我的对话</template>
          <div v-if="conversations.length === 0" style="color:#909399;text-align:center;padding:20px">暂无对话记录</div>
          <div v-for="conv in conversations" :key="conv.id" class="conv-item" @click="$router.push('/user/chat/' + conv.id)">
            <div class="conv-title">{{ conv.title }}</div>
            <div class="conv-time">{{ conv.updated_at }}</div>
          </div>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue"
import { useRouter } from "vue-router"
import { documentApi, qaApi } from "../../api/index.js"

const router = useRouter()
const docList = ref([])
const conversations = ref([])
const page = ref(1); const perPage = ref(10); const total = ref(0)

async function fetchDocs() {
  const res = await documentApi.getList({ page: page.value, per_page: perPage.value })
  if (res.code === 200) { docList.value = res.data.items; total.value = res.data.total }
}
async function fetchConversations() {
  const res = await qaApi.getConversations()
  if (res.code === 200) conversations.value = res.data.slice(0, 10)
}
function openChat(row) { router.push("/user/chat") }
onMounted(() => { fetchDocs(); fetchConversations() })
</script>

<style scoped>
.quick-start p { color: #606266; line-height: 1.8; }
.quick-start ol { padding-left: 20px; color: #606266; line-height: 2; }
.conv-item { padding: 8px 0; cursor: pointer; border-bottom: 1px solid #f0f0f0; }
.conv-item:hover { color: #409EFF; }
.conv-title { font-size: 14px; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
.conv-time { font-size: 12px; color: #909399; margin-top: 4px; }
</style>
