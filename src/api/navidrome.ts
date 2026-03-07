const BASE = "http://localhost:4533"

export function streamSong(id: string) {
  return `${BASE}/rest/stream?id=${id}&u=user&p=pass&v=1.16.1&c=typemood`
}