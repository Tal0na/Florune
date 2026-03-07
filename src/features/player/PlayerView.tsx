import { useEffect, useMemo, useState } from "react"
import { getRandomSongs, streamUrl } from "../../types/navidrome"
import { usePlayer } from "./usePlayer"
import "../../styles/PlayerView.css"

type NavidromeSong = {
  id: string
  title: string
  artist: string
  album: string
  url: string
}

function formatTime(seconds: number) {
  const mins = Math.floor(seconds / 60)
  const secs = Math.floor(seconds % 60)
  return `${mins}:${secs.toString().padStart(2, "0")}`
}

export default function PlayerView() {
  const {
    current,
    isPlaying,
    playlist,
    currentIndex,
    searchQuery,
    genre,
    playIndex,
    pause,
    resume,
    stop,
    next,
    prev,
    setPlaylist,
    progress,
    duration,
    setProgress,
    setDuration,
    setIsPlaying,
    audioRef,
  } = usePlayer()

  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  const filteredPlaylist = useMemo(() => {
    const query = searchQuery.trim().toLowerCase()

    return playlist
      .map((song, index) => ({ song, index }))
      .filter(({ song }) => {
        if (query) {
          const haystack = `${song.title} ${song.artist}`.toLowerCase()
          if (!haystack.includes(query)) return false
        }
        if (genre) {
          return song.genre?.toLowerCase() === genre.toLowerCase()
        }
        return true
      })
  }, [playlist, searchQuery, genre])

  const currentSong = useMemo(() => {
    if (currentIndex === null) return null
    return playlist[currentIndex] ?? null
  }, [currentIndex, playlist])

  useEffect(() => {
    setLoading(true)
    setError(null)

    getRandomSongs()
      .then((data) => {
        const normalized: NavidromeSong[] = (data ?? []).map((song: any) => ({
          id: song.id,
          title: song.title,
          artist: song.artist || song.artistName || "Unknown artist",
          album: song.album || song.albumName || "Unknown album",
          url: streamUrl(song.id),
        }))
        setPlaylist(normalized)
      })
      .catch((err) => {
        console.error(err)
        setError("Não foi possível carregar as músicas do Navidrome.")
      })
      .finally(() => setLoading(false))
  }, [setPlaylist])

  useEffect(() => {
    const audio = audioRef.current
    if (!audio) return

    audio.src = current

    if (current) {
      audio
        .play()
        .then(() => setIsPlaying(true))
        .catch(() => {
          // ignore autoplay issues; user can still click play
        })
    }

    const onTimeUpdate = () => setProgress(audio.currentTime)
    const onLoadedMetadata = () => setDuration(audio.duration)
    const onEnded = () => next()

    audio.addEventListener("timeupdate", onTimeUpdate)
    audio.addEventListener("loadedmetadata", onLoadedMetadata)
    audio.addEventListener("ended", onEnded)

    return () => {
      audio.removeEventListener("timeupdate", onTimeUpdate)
      audio.removeEventListener("loadedmetadata", onLoadedMetadata)
      audio.removeEventListener("ended", onEnded)
    }
  }, [audioRef, current, next, setDuration, setIsPlaying, setProgress])

  function handleSeek(value: number) {
    const audio = audioRef.current
    if (!audio) return
    audio.currentTime = value
    setProgress(value)
  }

  return (
    <div className="app">
      <header className="player-header">
        <h1>TypeMood</h1>
        <p className="subtitle">Navidrome player minimal</p>
      </header>

      {error && <div className="error">{error}</div>}

      <section className="playlist">
        <h2>Lista de reprodução</h2>
        {loading ? (
          <p>Carregando músicas…</p>
        ) : (
          <ul>
            {filteredPlaylist.map(({ song, index }) => (
              <li
                key={song.id}
                className={index === currentIndex ? "active" : ""}
              >
                <button className="track" onClick={() => playIndex(index)}>
                  <span className="track-title">{song.title}</span>
                  <span className="track-meta">
                    {song.artist} — {song.album}
                  </span>
                </button>
              </li>
            ))}
          </ul>
        )}
      </section>

      <div className="player-bar">
        <div className="bar-left">
          <div className="track-info">
            <div className="track-title">
              {currentSong?.title ?? "Nenhuma faixa selecionada"}
            </div>
            <div className="track-meta">
              {currentSong
                ? `${currentSong.artist} • ${currentSong.album}`
                : "Escolha uma faixa para começar"}
            </div>
          </div>
        </div>

        <div className="bar-center">
          <div className="controls">
            <button onClick={prev} disabled={!current}>
              ◀︎
            </button>
            <button onClick={pause} disabled={!isPlaying}>
              ⏸️
            </button>
            <button onClick={resume} disabled={isPlaying || !current}>
              ▶️
            </button>
            <button onClick={stop} disabled={!current}>
              ⏹️
            </button>
            <button onClick={next} disabled={!current}>
              ▶︎
            </button>
          </div>

          <div className="progress">
            <span className="time">{formatTime(progress)}</span>
            <input
              className="slider"
              type="range"
              min={0}
              max={duration || 0}
              value={progress}
              onChange={(event) => handleSeek(Number(event.target.value))}
              disabled={!current}
            />
            <span className="time">{formatTime(duration || 0)}</span>
          </div>
        </div>

        <div className="bar-right">
          <div className="track-meta">
            {isPlaying ? "Tocando agora" : "Pausado"}
          </div>
        </div>
      </div>

      <audio ref={audioRef} />
    </div>
  )
}
