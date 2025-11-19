# 🎵 Spotify MCP Server

A Model Context Protocol (MCP) implementation for Spotify, built from scratch to demonstrate how MCP servers work in practice. Create playlists, search for music, and explore Spotify's features through a standardized AI integration layer.

> **Learning Project**: This project was created to understand MCP internals by building a real-world implementation with Spotify integration.

## 📺 Demo

_[Demo video/screenshot coming soon]_

## 🤔 What is MCP?

The **Model Context Protocol (MCP)** is an open standard that enables AI models to securely interact with external tools and data sources. Think of it as a universal adapter that lets AI assistants (like Claude, ChatGPT, or Gemini) use your applications and services.

### How it works

```
┌─────────────┐         ┌─────────────┐         ┌──────────────┐
│             │  MCP    │             │  HTTP   │              │
│  AI Model   │ ◄─────► │ MCP Server  │ ◄─────► │ Spotify API  │
│  (Client)   │         │ (TypeScript)│         │   (Python)   │
│             │         │             │         │              │
└─────────────┘         └─────────────┘         └──────────────┘
```

1. **AI Model** sends requests to the MCP Server using the MCP protocol
2. **MCP Server** processes requests and communicates with the Spotify API wrapper
3. **Spotify API** handles authentication and interactions with Spotify's services
4. Results flow back through the chain to the AI model

## 🏗️ Architecture

This project consists of three main components running in Docker containers:

### 🐍 Spotify API (`spotify-api/`)
A FastAPI wrapper around Spotify's Web API that handles:
- OAuth authentication with Spotify
- Rate limiting and error handling
- Clean REST endpoints for the MCP server

### 🔧 MCP Server (`mcp-server/`)
A TypeScript implementation of the MCP protocol that:
- Exposes Spotify features as MCP tools
- Translates between MCP protocol and HTTP requests
- Manages sessions and handles CORS for browser-based clients

### 🤖 MCP Client (`mcp-client/`)
A Python client demonstrating MCP usage:
- Connects to the MCP server via HTTP
- Lists available tools
- Executes tool calls and displays results

### Communication Flow

```
MCP Client ──[MCP Protocol]──► MCP Server ──[HTTP]──► Spotify API ──[OAuth]──► Spotify
```

## 🚀 Installation

### Prerequisites

- [Docker Desktop](https://www.docker.com/products/docker-desktop/) installed and running
- A Spotify Developer account
- An AI API key (Google AI, OpenAI, or Anthropic)

### 1. Spotify Developer Setup

1. Go to [Spotify for Developers](https://developer.spotify.com/dashboard)
2. Create a new app
3. Note your **Client ID** and **Client Secret**
4. Add `http://localhost:8000/callback` to your app's Redirect URIs

### 2. AI API Key

Choose one of the following providers:

- **Google AI Studio** (Free): [Get API Key](https://aistudio.google.com/app/apikey)
- **OpenAI**: [Get API Key](https://platform.openai.com/api-keys)
- **Anthropic**: [Get API Key](https://console.anthropic.com/)

### 3. Environment Configuration

Create two environment files in the project root:

#### `spotify-api/app/.env`
```env
SPOTIFY_CLIENT_ID=your_spotify_client_id
SPOTIFY_CLIENT_SECRET=your_spotify_client_secret
SPOTIFY_REDIRECT_URI=http://localhost:8000/callback
```

#### `mcp-client/.env` (optional, for AI integration)
```env
# Choose one provider
GOOGLE_AI_API_KEY=your_google_api_key
# OPENAI_API_KEY=your_openai_api_key
# ANTHROPIC_API_KEY=your_anthropic_api_key
```

## 🎮 Usage

### Start the Project

```bash
# Clone the repository
git clone https://github.com/Gregoire-W/mcp-spotify.git
cd mcp-spotify

# Start all services
docker compose up --build
```

That's it! The services will be available at:
- **Spotify API**: http://localhost:8000
- **MCP Server**: http://localhost:3000/mcp
- **MCP Client**: Runs once and exits (check logs with `docker compose logs mcp-client`)

### Test with MCP Inspector

You can also test the server using the official MCP Inspector:

```bash
npx @modelcontextprotocol/inspector http://localhost:3000/mcp
```

### Stop the Project

```bash
docker compose down
```

## 🛠️ Technology Stack

- **MCP Server**: TypeScript, Express, [@modelcontextprotocol/sdk](https://www.npmjs.com/package/@modelcontextprotocol/sdk)
- **Spotify API**: Python, FastAPI, [Spotipy](https://spotipy.readthedocs.io/)
- **MCP Client**: Python, [MCP Python SDK](https://github.com/modelcontextprotocol/python-sdk)
- **Containerization**: Docker, Docker Compose

## 📚 Documentation & Resources

### Official Documentation
- [Model Context Protocol Specification](https://modelcontextprotocol.io/)
- [MCP TypeScript SDK](https://github.com/modelcontextprotocol/typescript-sdk)
- [MCP Python SDK](https://github.com/modelcontextprotocol/python-sdk)
- [Spotify Web API](https://developer.spotify.com/documentation/web-api)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)

### Learning Resources
- [Anthropic's MCP Announcement](https://www.anthropic.com/news/model-context-protocol)
- [Building MCP Servers - A Guide](https://modelcontextprotocol.io/docs/building-servers)

## 🤝 Contributing

This is a learning project, but contributions are welcome! Feel free to:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [Anthropic](https://www.anthropic.com/) for creating the Model Context Protocol
- [Spotify](https://www.spotify.com/) for their comprehensive Web API
- The open-source community for the amazing tools and libraries

---

**Note**: This project is for educational purposes and is not affiliated with Spotify or Anthropic.