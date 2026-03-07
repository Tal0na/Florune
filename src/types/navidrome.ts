const NAVIDROME = "http://192.168.15.2:4533"
const USER = "talona"
const PASS = "123"

export async function getRandomSongs() {

  const res = await fetch(
    `${NAVIDROME}/rest/getRandomSongs?u=${USER}&p=${PASS}&v=1.16.1&c=typemood&f=json&size=10`
  )

  const data = await res.json()

  return data["subsonic-response"].randomSongs.song
}

export function streamUrl(id: string) {
  return `${NAVIDROME}/rest/stream?id=${id}&u=${USER}&p=${PASS}&v=1.16.1&c=typemood`
}
