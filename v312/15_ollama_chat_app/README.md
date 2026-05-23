# 🦙 Ollama Chat Web Application

A high-performance, local AI chat interface built with **Python**, **Flask**, and **Ollama**. This application provides a modern web-based frontend for interacting with local LLMs, featuring real-time streaming responses, multi-turn conversations, and the ability to call external tools.

## 🚀 Features

- **Local Model Integration**: Seamlessly connects to your local Ollama instance.
- **Automatic Model Discovery**: Dynamically lists all models installed on your local Ollama server.
- **Streaming Responses**: Tokens are streamed in real-time via Server-Sent Events (SSE), including support for "thinking" tokens.
- **Tool Calling (Agents)**:
  - **Web Search**: Integration with the Tavily API to fetch current information from the web.
  - **Crypto Prices**: Real-time cryptocurrency data retrieval via the CoinGecko API.
- **Conversation Management**: Full history support for context-aware interactions.
- **Model Controls**: Configuration for system prompts, temperature, and max token limits.
- **Session Analytics**: Tracking of response times and tokens per second.

---

## 📁 Project Structure

```text
ollama_chat_app/
├── ollama_chat_app.py    # Application entry point & Flask config
├── ollama_helpers.py     # Ollama API logic, tool calling & routes
├── .env                  # API keys (TAVILY_API_KEY)
└── ollama_templates/      # UI templates
    ├── base.html          # Shared layout and CSS
    └── index.html         # Chat interface and JS logic
```

---

## 🛠️ Step-by-Step Implementation Guide

### 1. Prerequisites

#### Install Ollama
1. Download and install Ollama from [ollama.com](https://ollama.com).
2. Start the Ollama server: `ollama serve`.
3. Pull a model you want to use (e.g., `ollama pull llama3.2`).

#### Install Dependencies
```bash
pip install flask requests
```

### 2. Configuration (`.env`)
Create a `.env` file in the root directory to store your API keys for external tools:
```text
TAVILY_API_KEY=your_tavily_api_key_here
```

### 3. Implementation Logic (`ollama_helpers.py`)

The core logic manages the interaction between the Flask server and the local Ollama API.

#### A. Tool Definitions & Implementation
- **Tool Schema**: Define a `TOOLS` list containing function declarations (name, description, parameters) for `web_search` and `get_crypto_price`.
- **Web Search**: Implement a function that queries the Tavily API and returns a formatted string of search results.
- **Crypto Prices**: Implement a function that fetches real-time data from the CoinGecko API.

#### B. Ollama API Interaction
- **Model Discovery**: Use `requests.get("http://localhost:11434/api/tags")` to retrieve the list of installed models.
- **Streaming Generator**: Create a `chat_with_tools` generator that sends requests to `/api/chat` with `stream=True`.
- **SSE Formatting**: Implement a helper that wraps JSON data in the `data: ...\n\n` format for Server-Sent Events.

#### C. The Agentic Loop (Tool Calling)
Implement a loop to handle model-driven tool use:
1. **Stream tokens**: Forward tokens from Ollama to the user.
2. **Detect Tool Calls**: If the `done` chunk contains `tool_calls`, stop streaming and extract the function name and arguments.
3. **Execute Local Tools**: Run the corresponding Python function (`web_search` or `get_crypto_price`).
4. **Feed Results Back**: Append the tool result to the message history and call the API again to get the final response.
5. **Repeat**: Support up to 5 rounds of tool calling per turn.

#### D. Flask Routes
- **`/`**: Renders the chat interface and provides the list of discovered models.
- **`/chat`**: Handles POST requests, extracts conversation history and settings, and returns a `Response` object with `mimetype='text/event-stream'`.

### 4. Application Entry (`ollama_chat_app.py`)
- Initialize the Flask app with `template_folder="ollama_templates"`.
- Register routes by calling `ollama_helpers.setup_routes(app)`.
- Run the app on port 8117.

### 5. Frontend Implementation (`ollama_templates/`)
- **`base.html`**: A clean, dark-themed layout using modern CSS.
- **`index.html`**: 
  - **Sidebar**: Model selector and settings for system prompts and temperature.
  - **Chat Window**: A message area that dynamically appends tokens from the SSE stream.
  - **JS Logic**: Use the `fetch` API and `ReadableStream` to process chunks from the `/chat` endpoint and update the UI in real-time.

---

## 🏃 How to Run

1. Ensure Ollama is running: `ollama serve`.
2. Configure your `.env` file with the Tavily API key.
3. Run the application:
   ```bash
   python ollama_chat_app.py
   ```
4. Open your browser and navigate to:
   **http://localhost:8117**

---

## 📚 Key Concepts Demonstrated

- **Local LLM Deployment**: Interfacing with a locally hosted AI model.
- **Agentic Behavior**: Implementing function calling to let the AI use external tools.
- **Asynchronous Streaming**: Using SSE to eliminate latency in AI responses.
- **State Management**: Maintaining multi-turn conversation history for local models.
- **Frontend/Backend Integration**: Connecting a JavaScript-driven UI to a Python-based AI orchestrator.
- **Performance Tracking**: Measuring response times and token throughput.
