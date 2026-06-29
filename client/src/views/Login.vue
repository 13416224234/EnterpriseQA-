<template>
  <div class="login-container">
    <div class="login-card">
      <div class="login-header">
        <div class="login-logo">
          <svg viewBox="0 0 48 48" width="48" height="48">
            <path fill="#409EFF" d="M24 4L4 14v20l20 10 20-10V14L24 4z"/>
            <path fill="#fff" d="M24 12l-12 6v12l12 6 12-6V18l-12-6z"/>
          </svg>
        </div>
        <h2>企业知识库问答系统</h2>
        <p class="login-desc">智能检索 · 高效问答 · 知识共享</p>
      </div>
      <el-form :model="form" :rules="rules" ref="formRef" class="login-form">
        <el-form-item prop="username">
          <el-input v-model="form.username" placeholder="用户名" :prefix-icon="User" size="large" />
        </el-form-item>
        <el-form-item prop="password">
          <el-input v-model="form.password" type="password" placeholder="密码" :prefix-icon="Lock" size="large" show-password />
        </el-form-item>
        <el-form-item>
          <el-button type="primary" size="large" class="login-btn" :loading="loading" @click="handleLogin">登 录</el-button>
        </el-form-item>
      </el-form>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive } from "vue"
import { useRouter } from "vue-router"
import { User, Lock } from "@element-plus/icons-vue"
import { ElMessage } from "element-plus"
import { authApi } from "../api/index.js"
import { useUserStore } from "../store/index.js"

const router = useRouter()
const userStore = useUserStore()
const formRef = ref(null)
const loading = ref(false)

const form = reactive({ username: "admin", password: "123456" })
const rules = {
  username: [{ required: true, message: "请输入用户名", trigger: "blur" }],
  password: [{ required: true, message: "请输入密码", trigger: "blur" }]
}

async function handleLogin() {
  const valid = await formRef.value.validate().catch(() => false)
  if (!valid) return
  loading.value = true
  try {
    const res = await authApi.login(form)
    if (res.code === 200) {
      userStore.login(res.data.token, res.data.user)
      ElMessage.success("登录成功")
      const role = res.data.user.role
      router.push(role === "admin" ? "/admin/home" : "/user/home")
    } else {
      ElMessage.error(res.msg)
    }
  } catch (err) {
    ElMessage.error("登录失败：" + (err.message || "网络错误"))
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.login-container { height: 100vh; display: flex; align-items: center; justify-content: center;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); }
.login-card { width: 400px; padding: 40px; background: #fff; border-radius: 12px; box-shadow: 0 20px 60px rgba(0,0,0,0.15); }
.login-header { text-align: center; margin-bottom: 30px; }
.login-header h2 { margin: 12px 0 6px; color: #303133; font-size: 22px; }
.login-desc { color: #909399; font-size: 13px; margin: 0; }
.login-btn { width: 100%; }
</style>
