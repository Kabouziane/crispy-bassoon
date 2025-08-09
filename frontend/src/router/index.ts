import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import LoginView from '../views/LoginView.vue'
import NotesView from '../views/NotesView.vue'
import NoteEditorView from '../views/NoteEditorView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/login',
      name: 'login',
      component: LoginView,
    },
    {
      path: '/',
      name: 'notes',
      component: NotesView,
      meta: { requiresAuth: true },
    },
    {
      path: '/note/:id',
      name: 'note-editor',
      component: NoteEditorView,
      meta: { requiresAuth: true },
    },
  ],
})

router.beforeEach((to) => {
  const authStore = useAuthStore()
  
  if (to.meta.requiresAuth && !authStore.isAuthenticated) {
    return '/login'
  }
  
  if (to.name === 'login' && authStore.isAuthenticated) {
    return '/'
  }
})

export default router
