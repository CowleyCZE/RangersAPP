import axios from 'axios'

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api'

interface GenerateRequest {
  prompt: string
  project_root?: string
  format?: string
}

interface GenerateResponse {
  success: boolean
  blueprint?: any
  installer_code?: string
  filename?: string
  message?: string
  error?: string
}

export const apiService = {
  async health() {
    const response = await axios.get(`${API_BASE_URL}/health`)
    return response.data
  },

  async generateInstaller(data: GenerateRequest): Promise<GenerateResponse> {
    const response = await axios.post(`${API_BASE_URL}/generate`, {
      prompt: data.prompt,
      project_root: data.project_root || 'scenes',
      format: data.format || 'gdscript',
    })
    return response.data
  },

  async generateBlueprint(prompt: string) {
    const response = await axios.post(`${API_BASE_URL}/generate/json`, {
      prompt,
    })
    return response.data
  },

  downloadFile(content: string, filename: string) {
    const element = document.createElement('a')
    element.setAttribute('href', 'data:text/plain;charset=utf-8,' + encodeURIComponent(content))
    element.setAttribute('download', filename)
    element.style.display = 'none'
    document.body.appendChild(element)
    element.click()
    document.body.removeChild(element)
  },
}
