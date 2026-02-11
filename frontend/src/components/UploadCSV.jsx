import { useState } from 'react'
import axios from 'axios'

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'

export default function UploadCSV({ onUploaded, token, setToken }) {
  const [file, setFile] = useState(null)
  const [loading, setLoading] = useState(false)
  const [message, setMessage] = useState('')

  const getToken = async () => {
    const response = await axios.post(`${API_BASE_URL}/upload/token`, null, {
      params: { username: 'admin', password: 'admin123' }
    })
    setToken(response.data.access_token)
    return response.data.access_token
  }

  const handleUpload = async (event) => {
    event.preventDefault()
    if (!file) {
      setMessage('Please choose a CSV file.')
      return
    }

    try {
      setLoading(true)
      setMessage('')
      const authToken = token || (await getToken())

      const formData = new FormData()
      formData.append('file', file)

      const response = await axios.post(`${API_BASE_URL}/upload`, formData, {
        headers: {
          Authorization: `Bearer ${authToken}`,
          'Content-Type': 'multipart/form-data'
        }
      })

      setMessage(response.data.message)
      onUploaded()
    } catch (error) {
      setMessage(error.response?.data?.detail || 'Upload failed.')
    } finally {
      setLoading(false)
    }
  }

  return (
    <form onSubmit={handleUpload} style={{ marginBottom: 20 }}>
      <h3>Upload Operator CSV</h3>
      <input type="file" accept=".csv" onChange={(e) => setFile(e.target.files?.[0] || null)} />
      <button type="submit" disabled={loading} style={{ marginLeft: 8 }}>
        {loading ? 'Uploading...' : 'Upload'}
      </button>
      {message && <p>{message}</p>}
      <small>CSV columns required: name,type,location</small>
    </form>
  )
}
