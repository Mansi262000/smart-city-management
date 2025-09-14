import React, { useState } from 'react'
const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

export default function Login({ onLogin }) {
  const [email, setEmail] = useState('admin@city.local')
  const [password, setPassword] = useState('admin123')
  const [err, setErr] = useState(null)

  async function submit(e) {
    e.preventDefault()
    setErr(null)
    try {
      const r = await fetch(`${API_URL}/auth/login`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email, password })
      })
      if (!r.ok) throw new Error('Login failed')
      const data = await r.json()
      onLogin(data.access_token)
    } catch (e) {
      setErr(e.message)
    }
  }

  return (
    <div style={{display:'grid',placeItems:'center',height:'100vh',fontFamily:'sans-serif'}}>
      <form onSubmit={submit} style={{border:'1px solid #ddd',padding:24,borderRadius:12,minWidth:320}}>
        <h2>Smart City — Login</h2>
        <div>
          <label>Email</label><br/>
          <input value={email} onChange={e=>setEmail(e.target.value)} style={{width:'100%'}}/>
        </div>
        <div style={{marginTop:8}}>
          <label>Password</label><br/>
          <input type="password" value={password} onChange={e=>setPassword(e.target.value)} style={{width:'100%'}}/>
        </div>
        {err && <p style={{color:'red'}}>{err}</p>}
        <button style={{marginTop:12}}>Login</button>
      </form>
    </div>
  )
}
