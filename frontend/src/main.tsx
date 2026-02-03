import React from 'react'
import ReactDOM from 'react-dom/client'
import SimpleApp from './SimpleApp.tsx'
import './index.css'

// 只使用新版界面（SimpleApp）
ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <SimpleApp />
  </React.StrictMode>,
)
