import { defineStore } from 'pinia'
import api from '@/services/api'

interface Note {
  id: number
  title: string
  content: string
  owner: { id: number; username: string }
  collaborators: Array<{ id: number; username: string }>
  created_at: string
  updated_at: string
}

export const useNotesStore = defineStore('notes', {
  state: () => ({
    notes: [] as Note[],
    currentNote: null as Note | null,
    socket: null as WebSocket | null,
  }),

  actions: {
    async fetchNotes() {
      try {
        const response = await api.get('/notes/')
        this.notes = response.data
      } catch (error) {
        console.error('Error fetching notes:', error)
      }
    },

    async createNote(title: string, content: string) {
      try {
        const response = await api.post('/notes/', { title, content })
        this.notes.push(response.data)
        return response.data
      } catch (error) {
        console.error('Error creating note:', error)
      }
    },

    async updateNote(id: number, data: Partial<Note>) {
      try {
        const response = await api.patch(`/notes/${id}/`, data)
        const index = this.notes.findIndex(n => n.id === id)
        if (index !== -1) {
          this.notes[index] = response.data
        }
        return response.data
      } catch (error) {
        console.error('Error updating note:', error)
      }
    },

    async deleteNote(id: number) {
      try {
        await api.delete(`/notes/${id}/`)
        this.notes = this.notes.filter(n => n.id !== id)
      } catch (error) {
        console.error('Error deleting note:', error)
      }
    },

    connectWebSocket(noteId: number) {
      const token = localStorage.getItem('access_token')
      this.socket = new WebSocket(`ws://localhost:8000/ws/notes/${noteId}/?token=${token}`)
      
      this.socket.onmessage = (event) => {
        const data = JSON.parse(event.data)
        if (data.type === 'note_update' && this.currentNote) {
          this.currentNote.content = data.content
        }
      }
    },

    sendUpdate(content: string) {
      if (this.socket) {
        this.socket.send(JSON.stringify({
          type: 'note_update',
          content
        }))
      }
    },

    disconnectWebSocket() {
      if (this.socket) {
        this.socket.close()
        this.socket = null
      }
    }
  }
})