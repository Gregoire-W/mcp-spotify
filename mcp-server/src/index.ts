import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { StreamableHTTPServerTransport } from '@modelcontextprotocol/sdk/server/streamableHttp.js';
import express, { type Request, type Response } from 'express';
import { z } from "zod";
import { listTracksByArtist } from "./clients/spotifyApiClient.js";

const app = express();
app.use(express.json());

function getServer() {

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