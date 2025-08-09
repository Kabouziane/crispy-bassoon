<template>
  <div class="editor-container">
    <header class="editor-header">
      <button @click="$router.push('/')" class="btn-back">← Retour</button>
      <input
        v-model="noteTitle"
        @blur="saveTitle"
        class="title-input"
        placeholder="Titre de la note"
      />
      <div class="collaborators">
        <span v-for="collab in collaborators" :key="collab.id" class="collaborator">
          {{ collab.username }}
        </span>
        <button @click="showAddCollaborator = true" class="btn-add">+</button>
      </div>
    </header>

    <div class="editor-content">
      <textarea
        v-model="noteContent"
        @input="handleContentChange"
        class="content-editor"
        placeholder="Commencez à écrire..."
      ></textarea>
    </div>

    <!-- Modal ajout collaborateur -->
    <div v-if="showAddCollaborator" class="modal-overlay" @click="showAddCollaborator = false">
      <div class="modal" @click.stop>
        <h3>Ajouter un collaborateur</h3>
        <input v-model="collaboratorUsername" placeholder="Nom d'utilisateur" />
        <div class="modal-actions">
          <button @click="addCollaborator" class="btn-primary">Ajouter</button>
          <button @click="showAddCollaborator = false" class="btn-secondary">Annuler</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue'
import { useRoute } from 'vue-router'
import { useNotesStore } from '@/stores/notes'
import api from '@/services/api'

const route = useRoute()
const notesStore = useNotesStore()

const noteId = Number(route.params.id)
const noteTitle = ref('')
const noteContent = ref('')
const collaborators = ref([])
const showAddCollaborator = ref(false)
const collaboratorUsername = ref('')

let saveTimeout: NodeJS.Timeout

onMounted(async () => {
  try {
    const response = await api.get(`/notes/${noteId}/`)
    noteTitle.value = response.data.title
    noteContent.value = response.data.content
    collaborators.value = response.data.collaborators
    notesStore.currentNote = response.data
    
    // Connexion WebSocket
    notesStore.connectWebSocket(noteId)
  } catch (error) {
    console.error('Error loading note:', error)
  }
})

onUnmounted(() => {
  notesStore.disconnectWebSocket()
  if (saveTimeout) clearTimeout(saveTimeout)
})

const handleContentChange = () => {
  // Debounce save
  if (saveTimeout) clearTimeout(saveTimeout)
  saveTimeout = setTimeout(() => {
    saveContent()
    notesStore.sendUpdate(noteContent.value)
  }, 1000)
}

const saveContent = async () => {
  try {
    await api.patch(`/notes/${noteId}/`, { content: noteContent.value })
  } catch (error) {
    console.error('Error saving content:', error)
  }
}

const saveTitle = async () => {
  try {
    await api.patch(`/notes/${noteId}/`, { title: noteTitle.value })
  } catch (error) {
    console.error('Error saving title:', error)
  }
}

const addCollaborator = async () => {
  try {
    await api.post(`/notes/${noteId}/add_collaborator/`, {
      username: collaboratorUsername.value
    })
    // Recharger les collaborateurs
    const response = await api.get(`/notes/${noteId}/`)
    collaborators.value = response.data.collaborators
    showAddCollaborator.value = false
    collaboratorUsername.value = ''
  } catch (error) {
    console.error('Error adding collaborator:', error)
  }
}
</script>

<style scoped>
.editor-container {
  height: 100vh;
  display: flex;
  flex-direction: column;
}

.editor-header {
  display: flex;
  align-items: center;
  padding: 1rem 2rem;
  border-bottom: 1px solid #eee;
  gap: 1rem;
}

.btn-back {
  background: none;
  border: none;
  font-size: 1rem;
  cursor: pointer;
  color: #007bff;
}

.title-input {
  flex: 1;
  font-size: 1.5rem;
  font-weight: bold;
  border: none;
  outline: none;
  padding: 0.5rem;
}

.collaborators {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.collaborator {
  background: #e9ecef;
  padding: 0.25rem 0.5rem;
  border-radius: 12px;
  font-size: 0.875rem;
}

.btn-add {
  width: 24px;
  height: 24px;
  border-radius: 50%;
  background: #007bff;
  color: white;
  border: none;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
}

.editor-content {
  flex: 1;
  padding: 2rem;
}

.content-editor {
  width: 100%;
  height: 100%;
  border: none;
  outline: none;
  font-size: 1rem;
  line-height: 1.6;
  resize: none;
  font-family: inherit;
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
  max-width: 400px;
}

.modal input {
  width: 100%;
  margin: 1rem 0;
  padding: 0.75rem;
  border: 1px solid #ddd;
  border-radius: 4px;
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