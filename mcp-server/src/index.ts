// npx @modelcontextprotocol/inspector http://localhost:3000/mcp

import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { StreamableHTTPServerTransport } from '@modelcontextprotocol/sdk/server/streamableHttp.js';
import express, { type Request, type Response } from 'express';
import cors from 'cors';
import { z } from "zod";
import { getSpotifyApiClient } from "./clients/spotifyApiClient.js";

const app = express();
app.use(express.json());

// Configuration CORS pour l'inspecteur MCP
const corsOptions = {
    origin: (origin: string | undefined, callback: (err: Error | null, allow?: boolean) => void) => {
        // Allow requests with no origin (like mobile apps or Postman)
        if (!origin) return callback(null, true);

        // Allow all localhost and 127.0.0.1 on any port
        if (origin.startsWith('http://localhost:') ||
            origin.startsWith('http://127.0.0.1:') ||
            origin === 'http://localhost' ||
            origin === 'http://127.0.0.1') {
            console.log(`Request accepted from: ${origin}`)
            return callback(null, true);
        }

        console.log('Origin not allowed:', origin);
        callback(new Error('Not allowed by CORS'));
    },
    methods: ['GET', 'POST', 'OPTIONS'],
    allowedHeaders: ['Content-Type', 'Authorization', 'Mcp-Session-Id', 'mcp-protocol-version', 'accept'],
    exposedHeaders: ['Mcp-Session-Id', 'X-Request-Id', 'Content-Type'],
    credentials: false,
    maxAge: 86400 // Cache preflight for 24 hours
};

app.use(cors(corsOptions));

function getServer() {

    // Create server instance
    const server = new McpServer({
        name: "spotify",
        version: "1.0.0",
    });

    server.registerTool(
        "createPlaylist",
        {
            title: "Create a new Spotify playlist",
            description: "Creates a new playlist in the user's Spotify account. Provide a name, optional description, and choose whether it should be public or private. The playlist will be created empty and ready to add tracks.",
            inputSchema: { playlistName: z.string(), playlistDescription: z.string(), isPublic: z.boolean() },
            outputSchema: { success: z.boolean() }
        },
        async ({ playlistName, playlistDescription, isPublic }) => {
            const client = getSpotifyApiClient()
            const response = await client.createPlaylist(playlistName, playlistDescription, isPublic)
            return {
                content: [{ type: 'text', text: JSON.stringify(response) }],
                structuredContent: response
            };
        }
    )

    return server;
}

app.post('/mcp', async (req: Request, res: Response) => {
    try {
        console.log('Received MCP request:', {
            method: req.method,
            body: JSON.stringify(req.body).substring(0, 200),
            headers: req.headers
        });

        const code = req.header('X-Session-ID');
        if (code) {
            const client = getSpotifyApiClient();
            client.setCode(code);
        }

        const server = getServer();

        const transport = new StreamableHTTPServerTransport({
            sessionIdGenerator: undefined,
        });

        res.on('close', () => {
            console.log("Request close");
            transport.close();
            server.close();
        });

        await server.connect(transport);
        console.log('Server connected to transport');

        await transport.handleRequest(req, res, req.body);
        console.log('Request handled successfully');
    } catch (error) {
        console.error('Error handling MCP request:', error);
        if (!res.headersSent) {
            res.status(500).json({
                jsonrpc: '2.0',
                error: {
                    code: -32603,
                    message: 'Internal server error'
                },
                id: null
            });
        }
    }
});

const port = parseInt(process.env.PORT || '3000');
app.listen(port, () => {
    console.log(`MCP Server running on http://localhost:${port}/mcp`);
}).on('error', error => {
    console.error('Server error:', error);
    process.exit(1);
});