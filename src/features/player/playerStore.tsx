import { create } from "zustand"
import { createRef } from "react"

export type Track = {
  id: string
  title: string
  artist: string
  album: string
  url: string
  genre?: string
}

type PlayerState = {
  playlist: Track[]
  currentIndex: number | null
  current: string
  isPlaying: boolean
  progress: number
  duration: number
  searchQuery: string
  genre: string
  audioRef: React.RefObject<HTMLAudioElement | null>

  setPlaylist: (tracks: Track[]) => void
  playIndex: (index: number) => void
  playUrl: (url: string) => void
  next: () => void
  prev: () => void
  setIsPlaying: (isPlaying: boolean) => void
  setProgress: (seconds: number) => void
  setDuration: (seconds: number) => void
  setSearchQuery: (query: string) => void
  setGenre: (genre: string) => void
}

export const usePlayerStore = create<PlayerState>((set, get) => ({
  playlist: [],
  currentIndex: null,
  current: "",
  isPlaying: false,
  progress: 0,
  duration: 0,
  searchQuery: "",
  genre: "",
  audioRef: createRef<HTMLAudioElement>(),

  setPlaylist: (tracks) => set({ playlist: tracks }),

  playUrl: (url) =>
    set({ current: url, isPlaying: true, progress: 0, duration: 0 }),

  playIndex: (index) => {
    const { playlist } = get()
    const track = playlist[index]
    if (!track) return
    set({
      currentIndex: index,
      current: track.url,
      isPlaying: true,
      progress: 0,
      duration: 0,
    })
  },

  next: () => {
    const { playlist, currentIndex } = get()
    if (!playlist.length) return
    const nextIndex =
      currentIndex === null ? 0 : (currentIndex + 1) % playlist.length
    get().playIndex(nextIndex)
  },

  prev: () => {
    const { playlist, currentIndex } = get()
    if (!playlist.length) return
    const prevIndex =
      currentIndex === null
        ? 0
        : (currentIndex - 1 + playlist.length) % playlist.length
    get().playIndex(prevIndex)
  },

  setIsPlaying: (isPlaying) => set({ isPlaying }),
  setProgress: (seconds) => set({ progress: seconds }),
  setDuration: (seconds) => set({ duration: seconds }),
  setSearchQuery: (query) => set({ searchQuery: query }),
  setGenre: (genre) => set({ genre }),
}))
