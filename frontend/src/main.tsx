import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import './index.css'
import Home from './pages/Home.tsx'

// TypeScript declaration for Google Analytics
declare global {
  interface Window {
    dataLayer: unknown[];
    gtag: (...args: unknown[]) => void;
  }
}

const GA_MEASUREMENT_ID = "G-TKEPB5L1DE"

const script = document.createElement('script')
script.src = `https://www.googletagmanager.com/gtag/js?id=${GA_MEASUREMENT_ID}`;
script.async = true
document.head.appendChild(script)

window.dataLayer = window.dataLayer || []
function gtag(...args: unknown[]) {
  window.dataLayer.push(args)
}
gtag('js', new Date())
gtag('config', GA_MEASUREMENT_ID)

createRoot(document.getElementById('root')!).render(
  <StrictMode>
    <Home />
  </StrictMode>,
)