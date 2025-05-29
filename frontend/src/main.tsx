import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import { Analytics } from '@vercel/analytics/react'
import './index.css'
import Home from './pages/Home.tsx'

createRoot(document.getElementById('root')!).render(
  <StrictMode>
    <Home />
    <Analytics />
  </StrictMode>,
)
