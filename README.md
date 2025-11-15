# 🎵 MCP Spotify

> A complete project to learn how to build a Model Context Protocol (MCP) server from scratch, using the Spotify API as a practical use case.

---

## 📋 Table of Contents

- [Introduction](#-introduction)
- [Project Architecture](#️-project-architecture)
- [Installation](#-installation)
  - [1. Spotify API (FastAPI)](#1-spotify-api-fastapi)
  - [2. MCP Server](#2-mcp-server)
  - [3. MCP Client](#3-mcp-client)
- [Usage](#-usage)
- [Documentation](#-documentation)
- [Contributing](#-contributing)

---

## 🎯 Introduction

This project is a **hands-on tutorial** to understand and implement the **Model Context Protocol (MCP)** by building a complete application around the Spotify API.

### What is MCP?

The Model Context Protocol is a standardized protocol that enables language models (LLMs) to interact with external data sources in a structured and secure manner.

### Project Goals

1. **Learn MCP**: Understand the protocol by building a server from scratch
2. **REST API**: Create a FastAPI gateway to Spotify
3. **Complete Architecture**: Implement the MCP client-server pattern
4. **Real Use Case**: Query and manipulate Spotify data through LLMs

### Tech Stack

- **API**: FastAPI + Python 3.9+
- **MCP Server**: Python (coming soon)
- **MCP Client**: Python (coming soon)
- **External API**: Spotify Web API
- **Containerization**: Docker

---

## 🏗️ Project Architecture

```
mcp-spotify/
├── spotify-api/       # FastAPI REST API (gateway to Spotify)
├── mcp-server/        # MCP Server (protocol implementation)
├── mcp-client/        # MCP Client (server usage)
└── README.md          # This file
```

### Data Flow

```
┌─────────────┐       ┌─────────────┐       ┌──────────────┐       ┌──────────────┐
│  MCP Client │ ◄───► │  MCP Server │ ◄───► │  Spotify API │ ◄───► │  Spotify Web │
│   (User)    │       │  (Protocol) │       │   (FastAPI)  │       │     API      │
└─────────────┘       └─────────────┘       └──────────────┘       └──────────────┘
```

---

## 🚀 Installation

### Prerequisites

- Python 3.9 or higher
- Docker (optional, for containerization)
- A Spotify Developer account ([create an account](https://developer.spotify.com/dashboard))

### Spotify Configuration

1. Go to the [Spotify Developer Dashboard](https://developer.spotify.com/dashboard)
2. Create a new application
3. Get your `Client ID` and `Client Secret`

---

## 1. Spotify API (FastAPI)

The FastAPI API serves as a gateway between the MCP server and the Spotify API. It handles authentication and exposes REST endpoints.

### Local Installation

```bash
# Navigate to the spotify-api folder
cd spotify-api

# Install dependencies
pip install -r requirements.txt

# Create the .env file
# Copy the content below and replace with your credentials
```

**File `spotify-api/app/.env`:**

```env
SPOTIFY_CLIENT_ID=your_client_id
SPOTIFY_CLIENT_SECRET=your_client_secret
```

### Local Launch

```bash
# From the spotify-api folder
uvicorn app.main:app --reload --port 8000
```

The API will be accessible at: **http://localhost:8000**  
Interactive documentation: **http://localhost:8000/docs**

---

### Docker Installation (Recommended)

The project uses Docker Compose to orchestrate all services. From the **root directory**:

```bash
# Build and start all services
docker-compose up

# Or in detached mode (background)
docker-compose up -d

# Rebuild and start (after code changes)
docker-compose up --build

# View logs
docker-compose logs -f

# Stop all services
docker-compose down
```

The API will be accessible at: **http://localhost:8000**  
Interactive documentation: **http://localhost:8000/docs**

**Note**: Make sure you have created the `.env` file in `spotify-api/app/.env` with your Spotify credentials before running Docker Compose.

---

### Available Endpoints

| Method | Endpoint | Description |
|---------|----------|-------------|
| `GET` | `/docs` | Interactive Swagger documentation |
| `POST` | `/v1/spotify/` | List top tracks by artist |

---

## 2. MCP Server

🚧 **Under Development**

The MCP server will implement the Model Context Protocol to expose Spotify functionalities to LLMs.

---

## 3. MCP Client

🚧 **Under Development**

The MCP client will allow interaction with the server through natural language commands.

---

## 📚 Documentation

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Spotify Web API](https://developer.spotify.com/documentation/web-api)
- [Model Context Protocol](https://modelcontextprotocol.io/)

---

## 🤝 Contributing

This project is a learning exercise. Feel free to:

- Report bugs
- Suggest improvements
- Add features

---

## 📝 License

Educational project - Free to use

---

**Happy learning! 🎓🎵**
