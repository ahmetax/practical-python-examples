# 🤖 Gemini Chat Web Application

A sophisticated AI chat interface built with **Python**, **Flask**, and the **Google Gemini API**. This application implements a real-time streaming chat experience with support for multi-turn conversations and external tool calling (web search and cryptocurrency pricing).

## 🚀 Features

- **AI-Powered Chat**: Direct integration with Google Gemini models via the Google AI Studio API.
- **Streaming Responses**: Tokens are streamed in real-time using Server-Sent Events (SSE), providing a seamless "typing" experience.
- **Tool Calling (Function Calling)**:
  - **Web Search**: Integration with the Tavily API to fetch current information from the web.
  - **Crypto Prices**: Real-time cryptocurrency data retrieval via the CoinGecko API.
- **Conversation Management**: Maintains a multi-turn chat history to allow the AI to remember previous exchanges.
- **Advanced Model Controls**: User-configurable settings including model selection, system prompts, temperature, and max token limits.
- **Performance Analytics**: Real-time tracking of response time and tokens per second.

---

## 📁 Project Structure

```text
gemini_chat_app/
├── gemini_chat_app.py    # Application entry point & Flask config
├── gemini_helpers.py     # Gemini API logic, tool calling & routes
├── .env                  # API keys (GEMINI_API_KEY, TAVILY_API_KEY)
└── gemini_templates/      # UI templates
    ├── base.html          # Shared layout and CSS
    └── index.html         # Chat interface and JS logic
```

---

## 🛠️ Step-by-Step Implementation Guide

### 1. Prerequisites & API Keys
You will need the following keys:
- **Gemini API Key**: Get it for free at [Google AI Studio](https://aistudio.google.com).
- **Tavily API Key**: Sign up at [Tavily](https://tavily.com) for web search capabilities.

Install dependencies:
```bash
pip install flask requests
```

### 2. Configuration (`.env`)
Create a `.env` file in the root directory to securely store your keys:
```text
GEMINI_API_KEY=your_gemini_api_key_here
TAVILY_API_KEY=your_tavily_api_key_here
```

### 3. Implementation Logic (`gemini_helpers.py`)

The core logic handles the interaction between the Flask server and the Gemini API.

#### A. Tool Definitions & Integration
- **Tool Schema**: Define a `TOOLS` list using the OpenAI-compatible format. Each tool must have a `name`, `description`, and `parameters` object defining its expected input.
- **Web Search (Tavily)**: Implement a function that calls the Tavily API and returns formatted search snippets and URLs.
- **Crypto Prices (CoinGecko)**: Implement a function that queries the CoinGecko API for real-time prices and market data.

#### B. Gemini API Bridge
- **Message Mapping**: Create a helper to convert standard chat roles (`user`, `assistant`, `system`) into Gemini's native `contents` format.
- **Payload Construction**: Build a request payload that includes the conversation history, `systemInstruction` (for the system prompt), and `generationConfig` (temperature, max tokens).
- **SSE Streaming**: Use `requests.post(..., stream=True)` to call the `:streamGenerateContent` endpoint. Implement a generator that parses the raw SSE stream and yields JSON chunks.

#### C. The Tool-Calling Cycle (Agentic Loop)
Implement a recursive-like loop to handle tool execution:
1. **Request**: Send the current history to Gemini.
2. **Observation**: If the model returns a `functionCall` instead of text:
   - Identify the function name and arguments.
   - Execute the corresponding local Python function (Search or Crypto).
   - Append the tool's output to the history as a `tool` role message.
   - Loop back to Step 1 so the model can interpret the tool's results.
3. **Final Response**: When the model returns text, stream it to the client.

#### D. Flask Routes
- **`/`**: Renders the chat UI and provides a list of supported models.
- **`/chat`**: Handles POST requests. It extracts chat settings and returns a `Response` object with `mimetype='text/event-stream'`, wrapping the tool-calling generator in `stream_with_context`.

### 4. Application Entry (`gemini_chat_app.py`)
- Initialize a Flask application and set a `secret_key`.
- Configure the `template_folder` to use `gemini_templates`.
- Register all routes via `gemini_helpers.setup_routes(app)`.
- Run the app on port 8118.

### 5. Frontend Implementation (`gemini_templates/`)
- **`base.html`**: Define the HTML skeleton, including a modern dark-theme CSS layout and a responsive navigation bar.
- **`index.html`**: 
  - **Sidebar**: Create a settings panel for the system prompt, temperature, and max tokens.
  - **Chat Window**: Implement a message feed that supports markdown-like rendering.
  - **JS Integration**: Use the `fetch` API and a `ReadableStream` to consume the SSE endpoint. Implement a token-by-token rendering loop and a timer to calculate tokens per second.

---

## 🏃 How to Run

1. Ensure the `.env` file is configured with your API keys.
2. Run the application:
   ```bash
   python gemini_chat_app.py
   ```
3. Open your browser and navigate to:
   **http://localhost:8118**

---

## 📚 Key Concepts Demonstrated

- **Generative AI Integration**: Interfacing with large language models (LLMs) via REST APIs.
- **Tool Calling (Agents)**: Enabling an AI to interact with the real world through function execution.
- **Server-Sent Events (SSE)**: Implementing real-time data streaming from server to client.
- **Context Management**: Maintaining conversation state in multi-turn interactions.
- **Hybrid API Architecture**: Combining multiple APIs (Gemini, Tavily, CoinGecko) into a single coherent application.
- **Modern Frontend**: Creating a responsive AI chat UI with asynchronous data handling.
