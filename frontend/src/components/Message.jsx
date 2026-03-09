import { useState } from 'react'

/* ── Tool call (AI requesting a tool) ── */
function ToolCallBlock({ toolCall }) {
  const [open, setOpen] = useState(false)
  return (
    <div className="tc-block">
      <button className="tc-header" onClick={() => setOpen((o) => !o)}>
        <span className="tc-arrow">{open ? '▼' : '▶'}</span>
        <span className="tc-badge">TOOL CALL</span>
        <span className="tc-name">{toolCall.name}</span>
        <span className="tc-hint">{open ? 'colapsar args' : 'ver args'}</span>
      </button>
      {open && (
        <pre className="tc-args">{JSON.stringify(toolCall.args, null, 2)}</pre>
      )}
    </div>
  )
}

/* ── Tool output (result from a tool) ── */
function ToolOutputBlock({ item }) {
  const [open, setOpen] = useState(false)

  let display = item.content
  try {
    display = JSON.stringify(JSON.parse(item.content), null, 2)
  } catch {
    /* not JSON, show as-is */
  }

  return (
    <div className="to-block">
      <button className="to-header" onClick={() => setOpen((o) => !o)}>
        <span className="to-arrow">{open ? '▼' : '▶'}</span>
        <span className="to-badge">TOOL OUTPUT</span>
        <span className="to-name">{item.name}</span>
        <span className="to-hint">{open ? 'colapsar' : 'expandir'}</span>
      </button>
      {open && <pre className="to-content">{display}</pre>}
    </div>
  )
}

/* ── Token metadata footer ── */
function TokenMeta({ meta }) {
  if (!meta) return null
  return (
    <div className="token-meta">
      ▸ tokens › in:{meta.input_tokens} out:{meta.output_tokens} total:{meta.total_tokens}
    </div>
  )
}

/* ── One AI item from the response list ── */
function AiItem({ item }) {
  const hasTools = item.tool_calls?.length > 0
  const hasContent = item.content?.trim().length > 0

  return (
    <div className="ai-item">
      {hasTools && (
        <div className="ai-calling">
          <span className="ai-calling-label">⟳ LLAMANDO TOOLS</span>
          {item.tool_calls.map((tc, i) => (
            <ToolCallBlock key={i} toolCall={tc} />
          ))}
        </div>
      )}
      {hasContent && (
        <div className="ai-content">
          <span className="ai-prefix">[AGENT]</span>
          <span className="ai-text">{item.content}</span>
        </div>
      )}
      <TokenMeta meta={item.usage_metadata} />
    </div>
  )
}

/* ── Main message component ── */
export default function Message({ message }) {
  if (message.type === 'human') {
    return (
      <div className="msg msg-human">
        <span className="msg-prompt">{'>'}</span>
        <span className="msg-human-text">{message.content}</span>
      </div>
    )
  }

  if (message.type === 'error') {
    return (
      <div className="msg msg-error">
        <span className="msg-prompt">✗</span>
        <span>{message.content}</span>
      </div>
    )
  }

  if (message.type === 'response') {
    return (
      <div className="msg msg-response">
        {message.items.map((item, i) => {
          if (item.type === 'Ai') return <AiItem key={i} item={item} />
          if (item.type === 'Tool') return <ToolOutputBlock key={i} item={item} />
          return null
        })}
      </div>
    )
  }

  return null
}
