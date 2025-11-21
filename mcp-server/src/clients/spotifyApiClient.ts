const BASE_URL = process.env.SPOTIFY_API_URL;

export async function listTracksByArtist(artistName: string) {

    const response = await fetch(`${BASE_URL}/v1/list_tracks/`, {
        method: "POST",
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ artist_name: artistName })
    })

    if (!response.ok) {
        throw new Error(`API Error: ${response.statusText}`);
    }

    return await response.json();
}

export class SpotifyApiClient {

    private static instance: SpotifyApiClient | null = null;

    private baseUrl: string;
    private token: null | string;
    private expire: number;
    private clientSecret: string;
    private clientId: string;
    private apiVersion: string;
    private code: string | null;

    private constructor() {
        this.token = null;
        this.expire = 0;
        this.code = null;
        this.clientSecret = process.env.SPOTIFY_CLIENT_SECRET || "";
        this.clientId = process.env.SPOTIFY_CLIENT_ID || "";
        this.apiVersion = "v1"
        this.baseUrl = `https://api.spotify.com/${this.apiVersion}`;
    }

    public static getInstance(): SpotifyApiClient {
        if (!SpotifyApiClient.instance) {
            SpotifyApiClient.instance = new SpotifyApiClient();
        }
        return SpotifyApiClient.instance;
    }

    public setCode(code: string): void {
        this.code = code;
    }

    private isTokenValid() {
        return this.token && this.expire > Math.floor(Date.now() / 1000)
    }

    private async refreshToken() {
        if (!this.code) {
            throw new Error("No authorization code available. Call setCode() first.");
        }

        const response = await fetch("https://accounts.spotify.com/api/token", {
            method: "POST",
            headers: {
                "Content-Type": "application/x-www-form-urlencoded",
                'Authorization': `Basic ${Buffer.from(`${this.clientId}:${this.clientSecret}`).toString('base64')}`,
            },
            body: new URLSearchParams({
                "grant_type": "authorization_code",
                "code": this.code,
                "redirect_uri": "http://127.0.0.1:8080/",
            })
        })

        if (!response.ok) {
            throw new Error(`Token refresh failed: ${response.statusText}`);
        }

        const data = await response.json();
        this.token = data.access_token;
        this.expire = Math.floor(Date.now() / 1000) + data.expires_in - 30;
    }

    private async getToken() {

        if (!this.isTokenValid()) {
            await this.refreshToken();
        }
        return this.token
    }

    public async createPlaylist(playlistName: string, playlistDesc: string, isPublic: boolean = false) {
        try {
            const token = await this.getToken()
            const headers = { "Authorization": `Bearer ${token}` }

            const reponse = await fetch(`${this.baseUrl}/me`, {
                method: "GET",
                headers: headers,
            })
            const data = await reponse.json();

            const url = `${this.baseUrl}/users/${data.id}/playlists`;

            await fetch(url, {
                method: "POST",
                headers: headers,
                body: JSON.stringify({
                    name: playlistName,
                    description: playlistDesc,
                    public: isPublic,
                })

            });
            return { success: true }
        } catch {
            return { success: false }
        }

    }

}

// Helper function pour obtenir l'instance singleton
export function getSpotifyApiClient(): SpotifyApiClient {
    return SpotifyApiClient.getInstance();
}