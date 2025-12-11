import { create } from 'zustand'

interface GenerateState {
  prompt: string
  isLoading: boolean
  generatedCode: string | null
  generatedBlueprint: any | null
  filename: string | null
  error: string | null
  
  setPrompt: (prompt: string) => void
  setLoading: (loading: boolean) => void
  setGeneratedCode: (code: string | null) => void
  setGeneratedBlueprint: (blueprint: any | null) => void
  setFilename: (filename: string | null) => void
  setError: (error: string | null) => void
  reset: () => void
}

export const useGenerateStore = create<GenerateState>((set) => ({
  prompt: '',
  isLoading: false,
  generatedCode: null,
  generatedBlueprint: null,
  filename: null,
  error: null,
  
  setPrompt: (prompt) => set({ prompt }),
  setLoading: (isLoading) => set({ isLoading }),
  setGeneratedCode: (generatedCode) => set({ generatedCode }),
  setGeneratedBlueprint: (generatedBlueprint) => set({ generatedBlueprint }),
  setFilename: (filename) => set({ filename }),
  setError: (error) => set({ error }),
  reset: () => set({
    prompt: '',
    isLoading: false,
    generatedCode: null,
    generatedBlueprint: null,
    filename: null,
    error: null,
  }),
}))
