import { useEffect, useRef } from 'react'
import Message from './Message'

const BOOT_LINES = [
  'OPENCLAW TERMINAL  v1.0.0',
  'LANGGRAPH REACT AGENT  //  FASTAPI BACKEND',
  '─────────────────────────────────────────',
  'EDUBOT DB ONLINE',
  'APP DB ONLINE',
  'AGENT READY',
  '─────────────────────────────────────────',
  '▶  Configura USER_ID y CHAT_ID en el panel',
  '▶  Escribe tu consulta y pulsa ENTER',
]

export default function ChatWindow({ messages, loading }) {
  const bottomRef = useRef(null)

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [messages, loading])

  return (
    <div className="chat-window">
      {messages.length === 0 && (
        <div className="chat-boot">
          <pre className="boot-logo">{`
 ██████╗ ██████╗ ███████╗███╗   ██╗ ██████╗██╗      █████╗ ██╗    ██╗
██╔═══██╗██╔══██╗██╔════╝████╗  ██║██╔════╝██║     ██╔══██╗██║    ██║
██║   ██║██████╔╝█████╗  ██╔██╗ ██║██║     ██║     ███████║██║ █╗ ██║
██║   ██║██╔═══╝ ██╔══╝  ██║╚██╗██║██║     ██║     ██╔══██║██║███╗██║
╚██████╔╝██║     ███████╗██║ ╚████║╚██████╗███████╗██║  ██║╚███╔███╔╝
 ╚═════╝ ╚═╝     ╚══════╝╚═╝  ╚═══╝ ╚═════╝╚══════╝╚═╝  ╚═╝ ╚══╝╚══╝ `}</pre>
          <div className="boot-lines">
            {BOOT_LINES.map((line, i) => (
              <div key={i} className="boot-line" style={{ animationDelay: `${i * 80}ms` }}>
                {line}
              </div>
            ))}
            <div className="boot-cursor">
              <span className="blink">█</span>
            </div>
          </div>
        </div>
      )}

      {messages.map((msg) => (
        <Message key={msg.id} message={msg} />
      ))}

      {loading && (
        <div className="loading-row">
          <span className="loading-tag">[AGENT]</span>
          <span className="loading-text">
            PROCESANDO
            <span className="blink">█</span>
          </span>
        </div>
      )}

      <div ref={bottomRef} />
    </div>
  )
}
