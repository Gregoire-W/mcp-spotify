import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { StreamableHTTPServerTransport } from '@modelcontextprotocol/sdk/server/streamableHttp.js';
import express from 'express';
import { z } from "zod";
import { listTracksByArtist } from "./clients/spotifyApiClient.js";

const app = express();
app.use(express.json());

// Create server instance
const server = new McpServer({
    name: "spotify",
    version: "1.0.0",
});

server.registerTool(
    "add",
    {
        title: "Best tracks tools",
        description: "List top tracks from a spotify artist",
        inputSchema: { artistName: z.string() },
        outputSchema: {
            artist: z.object({
                id: z.string(),
                name: z.string(),
                image: z.string(),
                followers: z.number(),
                genres: z.array(z.string())
            }),
            tracks: z.array(
                z.object({
                    id: z.string(),
                    name: z.string(),
                    album: z.string(),
                    albumImage: z.string(),
                    duration: z.number(),
                    popularity: z.number(),
                    previewUrl: z.string().nullable(),  // Peut être null
                    spotifyUrl: z.string()
                })
            )
        }
    },
    async ({ artistName }) => {
        const response = await listTracksByArtist(artistName)
        return response
    }
)

app.post('/mcp', async (req, res) => {
    try {
        const transport = new StreamableHTTPServerTransport({
            sessionIdGenerator: undefined,
            enableJsonResponse: true,
            enableDnsRebindingProtection: true,
            allowedHosts: ['127.0.0.1',],
        });

        res.on('close', () => {
            transport.close();
        });

        await server.connect(transport);
        await transport.handleRequest(req, res, req.body);
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