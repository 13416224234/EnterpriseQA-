import { defineStore } from "pinia"
import { ref, computed } from "vue"
import axios from "axios"

export const useUserStore = defineStore("user", () => {
  const token = ref(localStorage.getItem("token") || "")
  const userInfo = ref(JSON.parse(localStorage.getItem("userInfo") || "{}"))
  const isLoggedIn = computed(() => !!token.value)
  const role = computed(() => userInfo.value.role || "")

  function login(loginToken, info) {
    token.value = loginToken
    userInfo.value = info
    localStorage.setItem("token", loginToken)
    localStorage.setItem("role", info.role)
    localStorage.setItem("userInfo", JSON.stringify(info))
    axios.defaults.headers.common["Authorization"] = "Bearer " + loginToken
  }

  function logout() {
    token.value = ""
    userInfo.value = {}
    localStorage.removeItem("token")
    localStorage.removeItem("role")
    localStorage.removeItem("userInfo")
    delete axios.defaults.headers.common["Authorization"]
  }

  return { token, userInfo, isLoggedIn, role, login, logout }
})
