import { useEffect, useState } from 'react'
import axios from 'axios'

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'

export default function RiskTable({ refreshKey }) {
  const [rows, setRows] = useState([])
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

  useEffect(() => {
    const fetchScores = async () => {
      try {
        setLoading(true)
        setError('')
        const response = await axios.get(`${API_BASE_URL}/risk`)
        setRows(response.data)
      } catch (err) {
        setError(err.response?.data?.detail || 'Failed to load risk scores.')
      } finally {
        setLoading(false)
      }
    }

    fetchScores()
  }, [refreshKey])

  if (loading) return <p>Loading risk scores...</p>
  if (error) return <p>{error}</p>

  return (
    <div>
      <h3>Operator Risk Scores</h3>
      <table border="1" cellPadding="8" style={{ borderCollapse: 'collapse', width: '100%' }}>
        <thead>
          <tr>
            <th>Name</th>
            <th>Type</th>
            <th>Location</th>
            <th>Risk Score</th>
          </tr>
        </thead>
        <tbody>
          {rows.map((row) => (
            <tr key={row.operator_id}>
              <td>{row.name}</td>
              <td>{row.type}</td>
              <td>{row.location}</td>
              <td>{row.risk_score}</td>
            </tr>
          ))}
          {rows.length === 0 && (
            <tr>
              <td colSpan="4" style={{ textAlign: 'center' }}>
                No data yet. Upload a CSV first.
              </td>
            </tr>
          )}
        </tbody>
      </table>
    </div>
  )
}
