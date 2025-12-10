import React, { useState } from 'react'
import './App.css'
import DataViewer from './components/DataViewer'
import ButtonGroup from './components/ButtonGroup'

function App() {
  const [activeTable, setActiveTable] = useState(null)
  const [loading, setLoading] = useState(false)

  const handleTableSelect = (tableName) => {
    setActiveTable(tableName)
  }

  return (
    <div className="app">
      <header className="app-header">
        <h1>📊 Hệ thống Quản lý Điểm danh</h1>
        <p>Xem chi tiết thông tin các bảng trong database</p>
      </header>

      <main className="app-main">
        <ButtonGroup 
          onTableSelect={handleTableSelect}
          activeTable={activeTable}
        />
        
        {activeTable && (
          <DataViewer 
            tableName={activeTable}
            onClose={() => setActiveTable(null)}
          />
        )}
      </main>
    </div>
  )
}

export default App

