import { type Track, type Tracks } from "../types/track.js";

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
            console.error("No authorization code available. Call setCode() first.");
            return { success: false, message: "No authorization code available. You should login with your spotify account first." }
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
            console.error(`Token refresh failed: ${response.statusText}`);
            return { success: false, message: "Token refresh failed" }
        }

        const data = await response.json();
        this.token = data.access_token;
        this.expire = Math.floor(Date.now() / 1000) + data.expires_in - 30;
        return { success: true, message: "Token refreshed successfuly" }
    }

    private async getToken() {

        let response: { success: boolean, message: string }
        if (!this.isTokenValid()) {
            response = await this.refreshToken();
        } else {
            response = { success: true, message: "Token already exists and still valid" };
        }
        return { token: this.token, success: response.success, message: response.message }
    }

    public async createPlaylist(playlistName: string, playlistDesc: string, isPublic: boolean = false) {
        try {
            const { token, success, message } = await this.getToken()
            if (!success) {
                return { success: false, message: message }
            }

            const headers = { "Authorization": `Bearer ${token}` }

            const reponse = await fetch(`${this.baseUrl}/me`, {
                method: "GET",
                headers: headers,
            })
            const userData = await reponse.json();

            const url = `${this.baseUrl}/users/${userData.id}/playlists`;

            const response = await fetch(url, {
                method: "POST",
                headers: headers,
                body: JSON.stringify({
                    name: playlistName,
                    description: playlistDesc,
                    public: isPublic,
                })

            });
            const playlistData = await response.json()

            return { success: true, playlistId: playlistData.id }
        } catch {
            return { success: false }
        }

    }

    public async search(query: string, type: string, limit: number) {

        try {
            const { token, success, message } = await this.getToken()
            if (!success) {
                return { success: false, message: message }
            }
            const headers = { "Authorization": `Bearer ${token}` };

            // Construire l'URL avec les query parameters
            const params = new URLSearchParams({
                q: query,
                type: type,
                limit: limit.toString()
            });

            const response = await fetch(`https://api.spotify.com/v1/search?${params}`, {
                method: "GET",
                headers: headers
            });

            if (!response.ok) {
                console.error("Error while fetching search endpoint");
                return { success: false }
            }

            const data = await response.json();
            const tracks: Tracks = data.tracks

            return {
                tracks: tracks.items.map((track: Track) => {
                    return {
                        uri: track.uri,
                        name: track.name,
                        artists: track.artists.map((artist) => artist.name),
                        album: track.album.name,
                    }
                }),
                success: true
            }

        } catch (error) {
            return { success: false }
        }

    }

    public async addTrackToPlaylist(playlistId: string, uris: string[]) {

        try {
            const { token, success, message } = await this.getToken()
            if (!success) {
                return { success: false, message: message }
            }
            const headers = { "Authorization": `Bearer ${token}` };

            await fetch(`https://api.spotify.com/v1/playlists/${playlistId}/tracks`, {
                method: "POST",
                headers: headers,
                body: JSON.stringify({
                    uris: uris,
                    position: 0
                })
            })

            return { success: true, message: "Music added with success" }

        } catch (error) {
            return { success: false, message: "Error while adding music to playlist. Try again later" }
        }
    }

}

// Helper function pour obtenir l'instance singleton
export function getSpotifyApiClient(): SpotifyApiClient {
    return SpotifyApiClient.getInstance();
}