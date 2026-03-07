import { useEffect } from "react"
import { usePlayer } from "./usePlayer"

export default function Player() {
  const { audioRef, current } = usePlayer()

  useEffect(() => {
    if (!current) return
    const audio = audioRef.current
    if (!audio) return

    audio.src = current
    audio.play().catch(() => {
      // ignore autoplay errors
    })
  }, [current, audioRef])

  return <audio ref={audioRef} hidden />
}
