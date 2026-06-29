<template>
  <div class="chat-page">
    <el-row :gutter="16" style="height:100%">
      <el-col :span="6" class="chat-sidebar">
        <el-card shadow="hover" style="height:100%">
          <template #header>
            <div style="display:flex;justify-content:space-between;align-items:center">
              <span>对话列表</span>
              <el-button size="small" type="primary" @click="newConversation">新建</el-button>
            </div>
          </template>
          <div v-if="conversations.length === 0" style="color:#909399;text-align:center;padding:20px">暂无对话</div>
          <div v-for="conv in conversations" :key="conv.id"
            :class="['conv-item', { active: currentConvId === conv.id }]"
            @click="switchConversation(conv.id)">
            <div class="conv-title">{{ conv.title }}</div>
            <div class="conv-time">{{ conv.updated_at }}</div>
            <el-button size="small" type="danger" link @click.stop="deleteConv(conv)">删除</el-button>
          </div>
        </el-card>
      </el-col>
      <el-col :span="18" class="chat-main">
        <el-card shadow="hover" style="height:100%;display:flex;flex-direction:column">
          <div class="messages-area" ref="messagesRef">
            <div v-if="messages.length === 0" class="welcome-msg">
              <h3>您好！我是企业知识库助手</h3>
              <p>请提出您的问题，我将从知识库中检索相关信息为您解答</p>
            </div>
            <div v-for="msg in messages" :key="msg.id"
              :class="['msg-item', msg.role === 'user' ? 'msg-user' : 'msg-assistant']">
              <div class="msg-role">{{ msg.role === 'user' ? '您' : 'AI助手' }}</div>
              <template v-if="msg.role === 'assistant' && hasThinking(msg.content)">
                <el-collapse-transition>
                  <div v-show="expandedThinking[msg.id]" class="thinking-section">
                    <div class="thinking-label">思考过程</div>
                    <div class="thinking-content">{{ getThinking(msg.content) }}</div>
                  </div>
                </el-collapse-transition>
                <el-button size="small" type="primary" link @click="toggleThinking(msg.id)" style="margin-bottom:6px">
                  {{ expandedThinking[msg.id] ? '收起思考' : '展开思考' }}
                </el-button>
                <div class="msg-content">{{ getAnswer(msg.content) }}</div>
              </template>
              <template v-else>
                <div class="msg-content">{{ msg.content }}</div>
              </template>
              <div v-if="msg.sources && msg.sources.length > 0" class="msg-sources">
                <el-tag size="small" v-for="(src, si) in msg.sources.slice(0, 3)" :key="si" type="info" style="margin-right:4px;margin-top:4px">
                  {{ src.document_title || '参考文档' }}
                </el-tag>
              </div>
              <div class="msg-time">{{ msg.created_at }}</div>
            </div>
          </div>
          <div class="input-area">
            <el-input v-model="question" type="textarea" :rows="3" placeholder="请输入您的问题..."
              :disabled="loading" @keydown.enter.prevent="sendQuestion" />
            <el-button type="primary" :loading="loading" @click="sendQuestion" style="margin-top:8px;width:100%">
              {{ loading ? '思考中...' : '发送问题' }}
            </el-button>
          </div>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted, nextTick, watch } from 'vue'
import { useRoute } from 'vue-router'
import { qaApi } from '../../api/index.js'
import { ElMessage, ElMessageBox } from 'element-plus'

const route = useRoute()
const messagesRef = ref(null)
const conversations = ref([])
const messages = ref([])
const currentConvId = ref(null)
const question = ref('')
const loading = ref(false)
const expandedThinking = reactive({})

function hasThinking(content) {
  return content && (content.includes('Thinking Process:') || content.includes('</think>') || content.includes(''))
}

function getThinking(content) {
  const parts = content.split('\n\n')
  if (parts.length > 1) {
    return parts.slice(0, -1).join('\n\n')
  }
  return content
}

function getAnswer(content) {
  const parts = content.split('\n\n')
  if (parts.length > 1) {
    return parts[parts.length - 1]
  }
  return content
}

function toggleThinking(msgId) {
  expandedThinking[msgId] = !expandedThinking[msgId]
}

async function fetchConversations() {
  const res = await qaApi.getConversations()
  if (res.code === 200) conversations.value = res.data
}

async function fetchMessages(convId) {
  const res = await qaApi.getMessages(convId)
  if (res.code === 200) messages.value = res.data
  scrollToBottom()
}

async function switchConversation(convId) {
  currentConvId.value = convId
  await fetchMessages(convId)
}

async function newConversation() {
  currentConvId.value = null
  messages.value = []
  question.value = ''
}

async function deleteConv(conv) {
  ElMessageBox.confirm('删除此对话？', '提示').then(async () => {
    await qaApi.deleteConversation(conv.id)
    if (currentConvId.value === conv.id) { currentConvId.value = null; messages.value = [] }
    fetchConversations()
  }).catch(() => {})
}

async function sendQuestion() {
  if (!question.value.trim() || loading.value) return
  const q = question.value.trim()
  question.value = ''
  loading.value = true
  try {
    const res = await qaApi.ask({ question: q, conversation_id: currentConvId.value })
    if (res.code === 200) {
      currentConvId.value = res.data.conversation_id
      await fetchMessages(currentConvId.value)
      fetchConversations()
    } else {
      ElMessage.error(res.msg)
    }
  } catch (e) {
    ElMessage.error('请求失败：' + (e.message || '网络错误'))
  } finally {
    loading.value = false
  }
}

function scrollToBottom() {
  nextTick(() => {
    if (messagesRef.value) {
      messagesRef.value.scrollTop = messagesRef.value.scrollHeight
    }
  })
}

watch(messages, scrollToBottom, { deep: true })

onMounted(async () => {
  await fetchConversations()
  const convId = route.params.id
  if (convId) {
    currentConvId.value = parseInt(convId)
    await fetchMessages(currentConvId.value)
  }
})
</script>

<style scoped>
.chat-page { height: calc(100vh - 88px); }
.chat-sidebar { height: 100%; }
.chat-main { height: 100%; }
.messages-area { flex: 1; overflow-y: auto; padding: 16px; background: #fafafa; border-radius: 4px; margin-bottom: 12px; }
.welcome-msg { text-align: center; padding: 60px 20px; color: #909399; }
.welcome-msg h3 { color: #303133; margin-bottom: 12px; }
.msg-item { margin-bottom: 16px; padding: 12px; border-radius: 8px; max-width: 85%; }
.msg-user { background: #ecf5ff; margin-left: auto; }
.msg-assistant { background: #f0f9eb; margin-right: auto; }
.msg-role { font-size: 13px; font-weight: bold; margin-bottom: 4px; color: #303133; }
.msg-content { font-size: 14px; line-height: 1.6; white-space: pre-wrap; word-break: break-word; }
.msg-sources { margin-top: 8px; }
.msg-time { font-size: 11px; color: #c0c4cc; margin-top: 4px; text-align: right; }
.input-area { padding: 8px 0; }
.conv-item { padding: 10px 8px; cursor: pointer; border-bottom: 1px solid #f0f0f0; display: flex; align-items: center; gap: 8px; }
.conv-item:hover { background: #f5f7fa; }
.conv-item.active { background: #ecf5ff; }
.conv-title { flex: 1; font-size: 13px; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
.conv-time { font-size: 11px; color: #c0c4cc; white-space: nowrap; }
.thinking-section { margin-bottom: 8px; }
.thinking-label { font-size: 12px; color: #909399; font-weight: bold; margin-bottom: 4px; }
.thinking-content { font-size: 13px; color: #909399; padding: 8px 12px; border-left: 3px solid #dcdfe6; background: #f5f7fa; border-radius: 4px; white-space: pre-wrap; line-height: 1.5; margin-bottom: 8px; max-height: 200px; overflow-y: auto; }
</style>
