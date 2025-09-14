import React, { useEffect, useState } from 'react'
const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

export default function Dashboard({ token, onLogout }) {
  const [summary, setSummary] = useState([])
  const [alerts, setAlerts] = useState([])

  async function load() {
    const h = { Authorization: `Bearer ${token}` }
    const s = await fetch(`${API_URL}/metrics/summary?hours=3`, { headers: h }).then(r=>r.json())
    const a = await fetch(`${API_URL}/alerts/`, { headers: h }).then(r=>r.json())
    setSummary(s); setAlerts(a)
  }

  useEffect(()=>{
    load()
    const id = setInterval(load, 5000)
    return ()=>clearInterval(id)
  }, [])

  return (
    <div style={{padding:24,fontFamily:'sans-serif'}}>
      <div style={{display:'flex',justifyContent:'space-between',alignItems:'center'}}>
        <h2>Smart City — Admin Dashboard</h2>
        <button onClick={onLogout}>Logout</button>
      </div>

      <h3>Metrics Summary (last 3h)</h3>
      <table border="1" cellPadding="6" style={{borderCollapse:'collapse'}}>
        <thead>
          <tr><th>Metric</th><th>Count</th><th>Avg</th><th>Min</th><th>Max</th></tr>
        </thead>
        <tbody>
          {summary.map((row, i)=> (
            <tr key={i}>
              <td>{row.metric_type}</td>
              <td>{row.count}</td>
              <td>{row.avg.toFixed(2)}</td>
              <td>{row.min.toFixed(2)}</td>
              <td>{row.max.toFixed(2)}</td>
            </tr>
          ))}
        </tbody>
      </table>

      <h3 style={{marginTop:24}}>Recent Alerts</h3>
      <table border="1" cellPadding="6" style={{borderCollapse:'collapse', width:'100%'}}>
        <thead>
          <tr><th>Time</th><th>Sensor</th><th>Metric</th><th>Severity</th><th>Message</th><th>Ack</th></tr>
        </thead>
        <tbody>
          {alerts.map(a => (
            <tr key={a.id}>
              <td>{new Date(a.created_at).toLocaleString()}</td>
              <td>{a.sensor_id}</td>
              <td>{a.metric_type}</td>
              <td>{a.severity}</td>
              <td>{a.message}</td>
              <td>{a.acknowledged ? '✅' : '❌'}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  )
}
