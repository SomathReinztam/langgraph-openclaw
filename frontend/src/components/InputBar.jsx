import { useState, useRef } from 'react'

export default function InputBar({ onSend, loading }) {
  const [text, setText] = useState('')
  const ref = useRef(null)

  function handleKeyDown(e) {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      submit()
    }
  }

  function submit() {
    const trimmed = text.trim()
    if (!trimmed || loading) return
    onSend(trimmed)
    setText('')
    ref.current?.focus()
  }

  return (
    <div className="input-bar">
      <span className="input-prompt">{'>'}</span>
      <textarea
        ref={ref}
        className="input-area"
        rows={2}
        value={text}
        onChange={(e) => setText(e.target.value)}
        onKeyDown={handleKeyDown}
        placeholder="Escribe tu consulta...  (ENTER envía · SHIFT+ENTER nueva línea)"
        disabled={loading}
        autoFocus
      />
      <button
        className={`input-send ${loading ? 'disabled' : ''}`}
        onClick={submit}
        disabled={loading}
      >
        {loading ? (
          <>
            <span className="blink">█</span>
          </>
        ) : (
          '[ SEND ]'
        )}
      </button>
    </div>
  )
}
