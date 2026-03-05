# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**langgraph-openclaw** is a FastAPI-based conversational AI system that wraps a LangGraph ReAct agent. The agent answers natural language questions by querying a PostgreSQL database that contains Discord monitoring data for solar energy companies (Solenium/Unergy). There are two separate databases: the **app DB** (stores users, chats, and conversation history) and the **edubot DB** (the source Discord data the agent queries).

## Commands

**Start the app DB (PostgreSQL with pgVector):**
```bash
docker compose up -d
```

**Initialize app DB tables (run once after Docker is up):**
```bash
python3 -m src.database.crud
```

**Run the FastAPI server:**
```bash
uvicorn src.api.main:app --host 0.0.0.0 --port 8000
```

**Run the LangGraph agent interactively (standalone, no API):**
```bash
python3 -m src.edubot.graphs.chatedudbv1
```

**Generate edubot DB documentation:**
```bash
python3 -m src.utils.db_utils
```

**Manual API test scripts (requires the server to be running):**
```bash
python3 test/api/newuser.py       # Create a test user
python3 test/api/newchat.py       # Create a test chat
python3 test/api/runeduchat.py    # Send a test message to the agent
```

## Architecture

### Dual Database Design
- **App DB** (`chatedubot`): Managed by this codebase via SQLAlchemy ORM. Contains `appusers`, `chat`, and `message` tables. Runs in Docker (`docker-compose.yaml`).
- **Edubot DB** (`edubot`): External read-only source (Discord monitoring system). Connection settings come from `DB_*` env vars (not `APP_DB_*`).

### Request Lifecycle (`POST /runeduchat/`)
1. Router (`src/api/routers/run_educhat.py`) receives `user_id`, `chat_id`, `human_message`.
2. `config_educhat()` (`src/database/run_chat.py`) reads the `chat_model_provider` JSON from the `chat` table to determine which LLM (Google/Groq/DeepSeek) and model to use.
3. `run_educhat()` fetches all prior messages for `chat_id` from the `message` table, reconstructs LangChain message objects (including `tool_calls` and `usage_metadata` from JSON), and invokes the compiled LangGraph.
4. The LangGraph (`src/edubot/graphs/chatedudbv1.py`) runs a ReAct loop: LLM → optional tool calls → LLM → repeat, with a hard cap of **5 API calls**.
5. The three PostgreSQL tools in `src/edubot/tools/toolkit.py` query the **edubot DB** (not the app DB): `get_db_tables_names`, `get_tables_schemas`, `query_data_base` (max 15 rows per call).
6. All messages (Human, AI with tool_calls, Tool) are saved to the `message` table as JSON. The full response list is returned.

### Key Files
| File | Purpose |
|---|---|
| `src/api/main.py` | FastAPI app, router registration |
| `src/api/routers/run_educhat.py` | Main active endpoint (`/runeduchat/`) |
| `src/database/run_chat.py` | `config_educhat` + `run_educhat` orchestration logic |
| `src/database/crud.py` | SQLAlchemy CRUD; run as `__main__` to create tables |
| `src/database/models.py` | SQLAlchemy ORM models |
| `src/database/schemas.py` | Pydantic models, TypedDict schemas, custom exceptions |
| `src/edubot/graphs/chatedudbv1.py` | LangGraph state machine (ReAct pattern) |
| `src/edubot/tools/toolkit.py` | PostgreSQL tool wrappers for the agent |
| `src/edubot/prompts/educhatv1.py` | System prompts (use `SYSTEM_PROMPT_4`, the latest) |
| `src/edubot/prompts/agent.py` | `DB_SKILL_1`: full edubot DB schema context injected at runtime |
| `src/utils/settings.py` | All env var loading via `python-dotenv` |

### LLM Provider Selection
The `ChatModelProvider` config (stored as JSON in the `chat.chat_model_provider` column) determines the LLM at runtime:
- `client: "google"` → `ChatGoogleGenerativeAI`
- `client: "groq"` → `ChatGroq`
- `client: "deepseek"` → `ChatDeepSeek`

### Message Storage Format
Messages are stored as JSON in `message.message`. AI messages carry `tool_calls` and `usage_metadata` as nested JSON; Tool messages carry `tool_call_id` and `name`. The reconstruction logic in `run_chat.py` must handle all three types to correctly replay conversation history.

## Environment Variables

Two `.env` variable groups are required:
- `APP_DB_*` — credentials for the app DB (Docker PostgreSQL)
- `DB_*` — credentials for the external edubot DB
- `GOOGLE_API_KEY`, `GROQ_API_KEY`, `DEEPSEEK_API_KEY` — LLM provider keys
- `FAST_API_PORT` — defaults to 8000
