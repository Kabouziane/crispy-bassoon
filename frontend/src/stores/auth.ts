import { defineStore } from 'pinia'
import api from '@/services/api'

interface User {
  id: number
  username: string
  email: string
}

export const useAuthStore = defineStore('auth', {
  state: () => ({
    user: null as User | null,
    isAuthenticated: false,
  }),

  actions: {
    async login(username: string, password: string) {
      try {
        const response = await api.post('/token/', { username, password })
        localStorage.setItem('access_token', response.data.access)
        localStorage.setItem('refresh_token', response.data.refresh)
        this.isAuthenticated = true
        await this.fetchUser()
        return true
      } catch {
        return false
      }
    },

    async fetchUser() {
      try {
        const response = await api.get('/user/')
        this.user = response.data
      } catch {
        this.logout()
      }
    },

    logout() {
      localStorage.removeItem('access_token')
      localStorage.removeItem('refresh_token')
      this.user = null
      this.isAuthenticated = false
    },

    checkAuth() {
      const token = localStorage.getItem('access_token')
      if (token) {
        this.isAuthenticated = true
        this.fetchUser()
      }
    }
  }
})