const BASE_URL = process.env.SPOTIFY_API_URL || "http://localhost:8000";

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