import { usePlayerStore } from "../features/player/playerStore"

export function usePlayer() {
  const current = usePlayerStore((s) => s.current)
  const playUrl = usePlayerStore((s) => s.playUrl)

  function play(url: string) {
    playUrl(url)
  }

  return {
    current,
    play,
  }
}
