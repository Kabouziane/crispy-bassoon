<template>
  <div class="notes-container">
    <header class="header">
      <h1>Notes Collaboratives</h1>
      <div class="header-actions">
        <button @click="showCreateModal = true" class="btn-primary">
          Nouvelle Note
        </button>
        <button @click="authStore.logout()" class="btn-secondary">
          Déconnexion
        </button>
      </div>
    </header>

    <div class="notes-grid">
      <div
        v-for="note in notesStore.notes"
        :key="note.id"
        @click="openNote(note)"
        class="note-card"
      >
        <h3>{{ note.title }}</h3>
        <p>{{ note.content.substring(0, 100) }}...</p>
        <div class="note-meta">
          <small>Par {{ note.owner.username }}</small>
          <small>{{ formatDate(note.updated_at) }}</small>
        </div>
      </div>
    </div>

    <!-- Modal création -->
    <div v-if="showCreateModal" class="modal-overlay" @click="showCreateModal = false">
      <div class="modal" @click.stop>
        <h3>Nouvelle Note</h3>
        <input v-model="newNoteTitle" placeholder="Titre" />
        <textarea v-model="newNoteContent" placeholder="Contenu"></textarea>
        <div class="modal-actions">
          <button @click="createNote" class="btn-primary">Créer</button>
          <button @click="showCreateModal = false" class="btn-secondary">Annuler</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { useNotesStore } from '@/stores/notes'

const router = useRouter()
const authStore = useAuthStore()
const notesStore = useNotesStore()

const showCreateModal = ref(false)
const newNoteTitle = ref('')
const newNoteContent = ref('')

onMounted(() => {
  notesStore.fetchNotes()
})

const openNote = (note: any) => {
  router.push(`/note/${note.id}`)
}

const createNote = async () => {
  if (newNoteTitle.value.trim()) {
    await notesStore.createNote(newNoteTitle.value, newNoteContent.value)
    showCreateModal.value = false
    newNoteTitle.value = ''
    newNoteContent.value = ''
  }
}

const formatDate = (dateString: string) => {
  return new Date(dateString).toLocaleDateString('fr-FR')
}
</script>

<style scoped>
.notes-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 2rem;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2rem;
}

.header-actions {
  display: flex;
  gap: 1rem;
}

.notes-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 1.5rem;
}

.note-card {
  background: white;
  padding: 1.5rem;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
  cursor: pointer;
  transition: transform 0.2s;
}

.note-card:hover {
  transform: translateY(-2px);
}

.note-meta {
  display: flex;
  justify-content: space-between;
  margin-top: 1rem;
  color: #666;
}

.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0,0,0,0.5);
  display: flex;
  justify-content: center;
  align-items: center;
}

.modal {
  background: white;
  padding: 2rem;
  border-radius: 8px;
  width: 90%;
  max-width: 500px;
}

.modal input, .modal textarea {
  width: 100%;
  margin: 1rem 0;
  padding: 0.75rem;
  border: 1px solid #ddd;
  border-radius: 4px;
}

.modal textarea {
  height: 150px;
  resize: vertical;
}

.modal-actions {
  display: flex;
  gap: 1rem;
  justify-content: flex-end;
}

.btn-primary {
  background: #007bff;
  color: white;
  border: none;
  padding: 0.75rem 1.5rem;
  border-radius: 4px;
  cursor: pointer;
}

.btn-secondary {
  background: #6c757d;
  color: white;
  border: none;
  padding: 0.75rem 1.5rem;
  border-radius: 4px;
  cursor: pointer;
}
</style>