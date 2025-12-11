import { useEffect } from 'react'
import { Toaster } from 'react-hot-toast'
import { Header } from './components/Header'
import { PromptInput } from './components/PromptInput'
import { CodeOutput } from './components/CodeOutput'
import { Examples } from './components/Examples'
import { apiService } from './services/api'
import './index.css'

function App() {
  useEffect(() => {
    // Check backend health
    apiService.health()
      .catch(() => {
        console.warn('Backend not available')
      })
  }, [])

  return (
    <>
      <Toaster position="top-right" />
      <Header />
      
      <div className="container-main">
        <div className="w-full">
          <div className="max-w-6xl mx-auto">
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 mb-12">
              <div className="card p-8">
                <PromptInput />
              </div>

              <div className="bg-white rounded-lg shadow-2xl p-8">
                <CodeOutput />
              </div>
            </div>

            <Examples />
          </div>
        </div>
      </div>
    </>
  )
}

export default App
