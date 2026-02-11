import { useState } from 'react'
import UploadCSV from './components/UploadCSV'
import RiskTable from './components/RiskTable'

export default function App() {
  const [refreshKey, setRefreshKey] = useState(0)
  const [token, setToken] = useState('')

  return (
    <main style={{ maxWidth: 960, margin: '2rem auto', fontFamily: 'Arial, sans-serif' }}>
      <h1>Oil Risk Scoring MVP</h1>
      <UploadCSV
        token={token}
        setToken={setToken}
        onUploaded={() => setRefreshKey((prev) => prev + 1)}
      />
      <RiskTable refreshKey={refreshKey} />
    </main>
  )
}
