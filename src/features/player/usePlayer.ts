import { usePlayerStore } from "./playerStore"

export function usePlayer() {
  const {
    audioRef,
    current,
    isPlaying,
    progress,
    duration,
    playlist,
    currentIndex,
    searchQuery,
    genre,
    playIndex,
    playUrl,
    next,
    prev,
    setPlaylist,
    setSearchQuery,
    setGenre,
    setProgress,
    setDuration,
    setIsPlaying,
  } = usePlayerStore()

  function pause() {
    const audio = audioRef.current
    if (audio) {
      audio.pause()
      setIsPlaying(false)
    }
  }

  function resume() {
    const audio = audioRef.current
    if (audio) {
      audio
        .play()
        .then(() => setIsPlaying(true))
        .catch(() => {
          /* ignore autoplay issues */
        })
    }
  }

  function stop() {
    const audio = audioRef.current
    if (audio) {
      audio.pause()
      audio.currentTime = 0
      setIsPlaying(false)
    }
  }

  return {
    audioRef,
    current,
    isPlaying,
    progress,
    duration,
    playlist,
    currentIndex,
    searchQuery,
    genre,
    playIndex,
    playUrl,
    pause,
    resume,
    stop,
    next,
    prev,
    setPlaylist,
    setSearchQuery,
    setGenre,
    setProgress,
    setDuration,
    setIsPlaying,
  }
}
