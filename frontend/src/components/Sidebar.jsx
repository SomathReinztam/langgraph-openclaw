import { useState } from 'react'
import { createUser, createChat } from '../api'

const MODELS = {
  google: ['gemini-2.5-pro', 'gemini-2.0-flash', 'gemini-1.5-pro'],
  groq: ['llama-3.3-70b-versatile', 'mixtral-8x7b-32768'],
  deepseek: ['deepseek-chat', 'deepseek-reasoner'],
}

export default function Sidebar({ userId, chatId, onUserIdChange, onChatIdChange, onClear }) {
  const [section, setSection] = useState(null) // 'user' | 'chat' | null
  const [userForm, setUserForm] = useState({ name: '', email: '', password: '' })
  const [chatForm, setChatForm] = useState({ client: 'google', model: MODELS.google[0], temperature: '0.2' })
  const [status, setStatus] = useState(null) // { ok: bool, msg: string }

  function setOk(msg) {
    setStatus({ ok: true, msg })
    setTimeout(() => setStatus(null), 3000)
  }
  function setErr(msg) {
    setStatus({ ok: false, msg })
  }

  async function handleCreateUser(e) {
    e.preventDefault()
    try {
      await createUser(userForm.name, userForm.email, userForm.password)
      setOk('USUARIO CREADO')
      setUserForm({ name: '', email: '', password: '' })
      setSection(null)
    } catch (err) {
      setErr(err.message)
    }
  }

  async function handleCreateChat(e) {
    e.preventDefault()
    try {
      await createChat(Number(userId), {
        client: chatForm.client,
        model: chatForm.model,
        temperature: Number(chatForm.temperature),
      })
      setOk('CHAT CREADO')
      setSection(null)
    } catch (err) {
      setErr(err.message)
    }
  }

  function handleClientChange(client) {
    setChatForm({ client, model: MODELS[client][0], temperature: chatForm.temperature })
  }

  function toggleSection(name) {
    setSection((s) => (s === name ? null : name))
    setStatus(null)
  }

  return (
    <aside className="sidebar">
      {/* Session config */}
      <div className="sb-block">
        <div className="sb-title">SESSION</div>
        <label className="sb-label">USER_ID</label>
        <input
          className="term-input"
          type="number"
          min="1"
          value={userId}
          onChange={(e) => onUserIdChange(Number(e.target.value))}
        />
        <label className="sb-label">CHAT_ID</label>
        <input
          className="term-input"
          type="number"
          min="1"
          value={chatId}
          onChange={(e) => onChatIdChange(Number(e.target.value))}
        />
      </div>

      {/* New user */}
      <div className="sb-block">
        <button
          className={`sb-toggle ${section === 'user' ? 'open' : ''}`}
          onClick={() => toggleSection('user')}
        >
          {section === 'user' ? '▼' : '▶'} NUEVO USUARIO
        </button>
        {section === 'user' && (
          <form className="sb-form" onSubmit={handleCreateUser}>
            <label className="sb-label">NAME</label>
            <input
              className="term-input"
              value={userForm.name}
              onChange={(e) => setUserForm((f) => ({ ...f, name: e.target.value }))}
              required
            />
            <label className="sb-label">EMAIL</label>
            <input
              className="term-input"
              type="email"
              value={userForm.email}
              onChange={(e) => setUserForm((f) => ({ ...f, email: e.target.value }))}
              required
            />
            <label className="sb-label">PASSWORD</label>
            <input
              className="term-input"
              type="password"
              value={userForm.password}
              onChange={(e) => setUserForm((f) => ({ ...f, password: e.target.value }))}
              required
            />
            <button className="term-btn" type="submit">
              [ CREAR ]
            </button>
          </form>
        )}
      </div>

      {/* New chat */}
      <div className="sb-block">
        <button
          className={`sb-toggle ${section === 'chat' ? 'open' : ''}`}
          onClick={() => toggleSection('chat')}
        >
          {section === 'chat' ? '▼' : '▶'} NUEVO CHAT
        </button>
        {section === 'chat' && (
          <form className="sb-form" onSubmit={handleCreateChat}>
            <label className="sb-label">CLIENT</label>
            <select
              className="term-input term-select"
              value={chatForm.client}
              onChange={(e) => handleClientChange(e.target.value)}
            >
              <option value="google">google</option>
              <option value="groq">groq</option>
              <option value="deepseek">deepseek</option>
            </select>
            <label className="sb-label">MODEL</label>
            <select
              className="term-input term-select"
              value={chatForm.model}
              onChange={(e) => setChatForm((f) => ({ ...f, model: e.target.value }))}
            >
              {(MODELS[chatForm.client] ?? []).map((m) => (
                <option key={m} value={m}>
                  {m}
                </option>
              ))}
            </select>
            <label className="sb-label">TEMPERATURE</label>
            <input
              className="term-input"
              type="number"
              step="0.1"
              min="0"
              max="2"
              value={chatForm.temperature}
              onChange={(e) => setChatForm((f) => ({ ...f, temperature: e.target.value }))}
              required
            />
            <button className="term-btn" type="submit">
              [ CREAR ]
            </button>
          </form>
        )}
      </div>

      {/* Clear chat */}
      <div className="sb-block">
        <button className="sb-toggle danger" onClick={onClear}>
          ✕ LIMPIAR CHAT
        </button>
      </div>

      {/* Status */}
      {status && (
        <div
          className={`sb-status ${status.ok ? 'ok' : 'err'}`}
          onClick={() => setStatus(null)}
        >
          {status.ok ? '✓' : '✗'} {status.msg}
        </div>
      )}

      <div className="sb-footer">
        <div>OPENCLAW v1.0</div>
        <div>LANGGRAPH + FASTAPI</div>
      </div>
    </aside>
  )
}
