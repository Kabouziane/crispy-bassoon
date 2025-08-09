<template>
  <div class="debug-container">
    <h1>🔧 Debug - Système de Notes</h1>
    
    <div class="debug-section">
      <h2>Test API Backend</h2>
      <button @click="testBackend" class="btn">Tester Backend</button>
      <pre v-if="backendResult">{{ backendResult }}</pre>
    </div>

    <div class="debug-section">
      <h2>Test Connexion</h2>
      <form @submit.prevent="testLogin">
        <input v-model="username" placeholder="Username" />
        <input v-model="password" type="password" placeholder="Password" />
        <button type="submit" class="btn">Test Login</button>
      </form>
      <pre v-if="loginResult">{{ loginResult }}</pre>
    </div>

    <div class="debug-section">
      <h2>État Auth Store</h2>
      <pre>{{ authState }}</pre>
    </div>

    <div class="debug-section">
      <h2>Accès Direct</h2>
      <button @click="$router.push('/')" class="btn">Aller aux Notes</button>
      <button @click="bypassAuth" class="btn">Bypass Auth</button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { useAuthStore } from '@/stores/auth'
import api from '@/services/api'
import axios from 'axios'

const authStore = useAuthStore()
const username = ref('karim')
const password = ref('123')
const backendResult = ref('')
const loginResult = ref('')

const authState = computed(() => ({
  isAuthenticated: authStore.isAuthenticated,
  user: authStore.user,
  hasToken: !!localStorage.getItem('access_token')
}))

const testBackend = async () => {
  try {
    const response = await axios.get('http://127.0.0.1:8000/api/notes/')
    backendResult.value = `❌ Erreur: ${response.status}`
  } catch (error: any) {
    if (error.response?.status === 401) {
      backendResult.value = '✅ Backend OK - Auth requise'
    } else {
      backendResult.value = `❌ Erreur: ${error.message}`
    }
  }
}

const testLogin = async () => {
  try {
    const response = await axios.post('http://127.0.0.1:8000/api/token/', {
      username: username.value,
      password: password.value
    })
    loginResult.value = `✅ Login OK: ${JSON.stringify(response.data, null, 2)}`
    
    // Sauvegarder les tokens
    localStorage.setItem('access_token', response.data.access)
    localStorage.setItem('refresh_token', response.data.refresh)
    authStore.isAuthenticated = true
    
  } catch (error: any) {
    loginResult.value = `❌ Login failed: ${error.response?.data || error.message}`
  }
}

const bypassAuth = () => {
  authStore.isAuthenticated = true
  authStore.user = { id: 1, username: 'debug', email: 'debug@test.com' }
}
</script>

<style scoped>
.debug-container {
  max-width: 800px;
  margin: 2rem auto;
  padding: 2rem;
  font-family: monospace;
}

.debug-section {
  margin: 2rem 0;
  padding: 1rem;
  border: 1px solid #ddd;
  border-radius: 4px;
}

.btn {
  background: #007bff;
  color: white;
  border: none;
  padding: 0.5rem 1rem;
  margin: 0.5rem;
  border-radius: 4px;
  cursor: pointer;
}

input {
  display: block;
  width: 200px;
  margin: 0.5rem 0;
  padding: 0.5rem;
  border: 1px solid #ddd;
  border-radius: 4px;
}

pre {
  background: #f5f5f5;
  padding: 1rem;
  border-radius: 4px;
  overflow-x: auto;
  white-space: pre-wrap;
}
</style>