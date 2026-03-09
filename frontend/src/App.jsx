import { useState, useCallback } from 'react'
import Sidebar from './components/Sidebar'
import ChatWindow from './components/ChatWindow'
import InputBar from './components/InputBar'
import { runEduChat } from './api'

let _id = 0
const nextId = () => ++_id

export default function App() {
  const [userId, setUserId] = useState(1)
  const [chatId, setChatId] = useState(1)
  const [messages, setMessages] = useState([])
  const [loading, setLoading] = useState(false)

  const sendMessage = useCallback(
    async (text) => {
      if (!text.trim() || loading) return

      setMessages((prev) => [...prev, { id: nextId(), type: 'human', content: text }])
      setLoading(true)

      try {
        const data = await runEduChat(userId, chatId, text)
        const items = data.educhat_response ?? []
        setMessages((prev) => [...prev, { id: nextId(), type: 'response', items }])
      } catch (err) {
        setMessages((prev) => [
          ...prev,
          { id: nextId(), type: 'error', content: err.message },
        ])
      } finally {
        setLoading(false)
      }
    },
    [userId, chatId, loading],
  )

  const clearChat = useCallback(() => setMessages([]), [])

  return (
    <div className="app">
      <header className="app-header">
        <span className="header-logo">▓▓ EDUBOT TERMINAL</span>
        <span className="header-status">
          USER:<span className="header-val">{userId}</span> | CHAT:
          <span className="header-val">{chatId}</span> | STATUS:
          <span className={`header-val ${loading ? 'status-busy' : 'status-ready'}`}>
            {loading ? 'PROCESSING' : 'READY'}
          </span>
        </span>
      </header>

      <div className="app-body">
        <Sidebar
          userId={userId}
          chatId={chatId}
          onUserIdChange={setUserId}
          onChatIdChange={setChatId}
          onClear={clearChat}
        />
        <div className="chat-area">
          <ChatWindow messages={messages} loading={loading} />
          <InputBar onSend={sendMessage} loading={loading} />
        </div>
      </div>
    </div>
  )
}
