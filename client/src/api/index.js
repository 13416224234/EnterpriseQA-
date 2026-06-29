import axios from "axios"

const request = axios.create({
  baseURL: "/api",
  timeout: 60000
})

request.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem("token")
    if (token) config.headers.Authorization = "Bearer " + token
    return config
  },
  (error) => Promise.reject(error)
)

request.interceptors.response.use(
  (response) => {
    const res = response.data
    if (res.code === 401) { localStorage.clear(); window.location.href = "/login" }
    return res
  },
  (error) => Promise.reject(error)
)

export const authApi = {
  login: (data) => request.post("/auth/login", data),
  register: (data) => request.post("/auth/register", data),
  getUserInfo: () => request.get("/auth/info")
}

export const adminApi = {
  getDashboard: () => request.get("/admin/dashboard"),
  getUsers: (params) => request.get("/admin/users", { params }),
  updateUser: (id, data) => request.put("/admin/users/" + id, data),
  deleteUser: (id) => request.delete("/admin/users/" + id),
  getCategories: () => request.get("/admin/categories"),
  createCategory: (data) => request.post("/admin/categories", data),
  deleteCategory: (id) => request.delete("/admin/categories/" + id)
}

export const documentApi = {
  upload: (formData) => request.post("/document/upload", formData, { headers: { "Content-Type": "multipart/form-data" } }),
  getList: (params) => request.get("/document/list", { params }),
  delete: (id) => request.delete("/document/" + id),
  revectorize: (id) => request.post("/document/" + id + "/revectorize")
}

export const qaApi = {
  getConversations: () => request.get("/qa/conversations"),
  createConversation: (data) => request.post("/qa/conversations", data),
  deleteConversation: (id) => request.delete("/qa/conversations/" + id),
  getMessages: (convId) => request.get("/qa/conversations/" + convId + "/messages"),
  ask: (data) => request.post("/qa/ask", data)
}

export default request
