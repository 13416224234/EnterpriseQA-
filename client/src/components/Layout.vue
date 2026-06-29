<template>
  <el-container class="layout-container">
    <el-aside :width="isCollapse ? '64px' : '220px'" class="layout-aside">
      <div class="aside-header">
        <span v-show="!isCollapse" class="aside-title">知识库系统</span>
        <span v-show="isCollapse" class="aside-title-short">KB</span>
      </div>
      <el-menu :default-active="activeMenu" :collapse="isCollapse" :router="true"
        background-color="#304156" text-color="#bfcbd9" active-text-color="#409EFF">
        <!-- Admin menu -->
        <template v-if="userStore.role === 'admin'">
          <el-menu-item index="/admin/home"><el-icon><DataAnalysis /></el-icon><span>首页统计</span></el-menu-item>
          <el-menu-item index="/admin/users"><el-icon><UserFilled /></el-icon><span>用户管理</span></el-menu-item>
          <el-menu-item index="/admin/documents"><el-icon><Document /></el-icon><span>文档管理</span></el-menu-item>
          <el-divider style="border-color:#4a5a6a;margin:8px 0" />
          <el-menu-item index="/user/home"><el-icon><ChatDotSquare /></el-icon><span>知识问答</span></el-menu-item>
          <el-menu-item index="/user/chat"><el-icon><Message /></el-icon><span>智能对话</span></el-menu-item>
        </template>
        <!-- User menu -->
        <template v-else>
          <el-menu-item index="/user/home"><el-icon><ChatDotSquare /></el-icon><span>知识问答</span></el-menu-item>
          <el-menu-item index="/user/chat"><el-icon><Message /></el-icon><span>智能对话</span></el-menu-item>
        </template>
      </el-menu>
    </el-aside>
    <el-container>
      <el-header class="layout-header">
        <div class="header-left">
          <el-button text @click="isCollapse = !isCollapse" style="color: #fff">
            <el-icon><Fold v-if="!isCollapse" /><Expand v-else /></el-icon>
          </el-button>
          <span class="header-title">{{ route.meta.title || "企业知识库问答系统" }}</span>
        </div>
        <div class="header-right">
          <span class="header-user">欢迎，{{ userStore.userInfo.real_name || userStore.username }}</span>
          <el-button text style="color: #fff" @click="handleLogout">退出登录</el-button>
        </div>
      </el-header>
      <el-main class="layout-main"><router-view /></el-main>
    </el-container>
  </el-container>
</template>

<script setup>
import { ref, computed } from "vue"
import { useRoute, useRouter } from "vue-router"
import { useUserStore } from "../store/index.js"
import { ElMessageBox } from "element-plus"
import { DataAnalysis, UserFilled, Document, ChatDotSquare, Message, Fold, Expand } from "@element-plus/icons-vue"

const route = useRoute()
const router = useRouter()
const userStore = useUserStore()
const isCollapse = ref(false)
const activeMenu = computed(() => route.path)

function handleLogout() {
  ElMessageBox.confirm("确定要退出登录吗？", "提示").then(() => {
    userStore.logout(); router.push("/login")
  }).catch(() => {})
}
</script>

<style scoped>
.layout-container { height: 100vh; }
.layout-aside { background-color: #304156; transition: width 0.3s; overflow: hidden; }
.aside-header { height: 56px; display: flex; align-items: center; justify-content: center;
  color: #fff; font-size: 18px; font-weight: bold; border-bottom: 1px solid rgba(255,255,255,0.1); }
.aside-title-short { font-size: 20px; color: #409EFF; }
.layout-header { display: flex; align-items: center; justify-content: space-between;
  background: #242f3e; color: #fff; height: 56px; padding: 0 16px; }
.header-left { display: flex; align-items: center; gap: 12px; }
.header-title { font-size: 15px; }
.header-right { display: flex; align-items: center; gap: 12px; }
.header-user { font-size: 13px; color: rgba(255,255,255,0.85); }
.layout-main { background: #f0f2f5; padding: 16px; overflow-y: auto; }
</style>
