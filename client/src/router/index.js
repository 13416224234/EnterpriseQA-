import { createRouter, createWebHistory } from "vue-router"

const routes = [
  {
    path: "/login",
    name: "Login",
    component: () => import("../views/Login.vue"),
    meta: { title: "登录", noAuth: true }
  },
  {
    path: "/admin",
    component: () => import("../components/Layout.vue"),
    meta: { role: "admin" },
    redirect: "/admin/home",
    children: [
      { path: "home", name: "AdminHome", component: () => import("../views/admin/Home.vue"), meta: { title: "管理首页" } },
      { path: "users", name: "AdminUsers", component: () => import("../views/admin/Users.vue"), meta: { title: "用户管理" } },
      { path: "documents", name: "AdminDocuments", component: () => import("../views/admin/Documents.vue"), meta: { title: "文档管理" } }
    ]
  },
  {
    path: "/user",
    component: () => import("../components/Layout.vue"),
    meta: { role: "user" },
    redirect: "/user/home",
    children: [
      { path: "home", name: "UserHome", component: () => import("../views/user/Home.vue"), meta: { title: "知识问答" } },
      { path: "chat/:id?", name: "UserChat", component: () => import("../views/user/Chat.vue"), meta: { title: "智能对话" } }
    ]
  },
  { path: "/:pathMatch(.*)*", redirect: "/login" }
]

const router = createRouter({ history: createWebHistory(), routes })

router.beforeEach((to, from, next) => {
  const token = localStorage.getItem("token")
  const role = localStorage.getItem("role")
  if (to.meta.noAuth) {
    if (token) next(role === "admin" ? "/admin/home" : "/user/home")
    else next()
  } else {
    if (!token) next("/login")
    else if (to.meta.role && to.meta.role !== role && role !== "admin")
      next(role === "admin" ? "/admin/home" : "/user/home")
    else next()
  }
})

export default router
