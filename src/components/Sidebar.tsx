import { usePlayer } from "../features/player/usePlayer"

export default function Sidebar() {
  const {
    playlist,
    currentIndex,
    isPlaying,
    searchQuery,
    genre,
    setSearchQuery,
    setGenre,
    pause,
    resume,
  } = usePlayer()
  const current = currentIndex !== null ? playlist[currentIndex] : null

  return (
    <div className="sidebar">
      <h2>Florune</h2>

      <div style={{ marginTop: 16 }}>
        <strong>Buscar músicas</strong>
        <input
          value={searchQuery}
          onChange={(e) => setSearchQuery(e.target.value)}
          placeholder="Digite um título ou artista"
          style={{
            width: "100%",
            marginTop: 8,
            padding: 8,
            borderRadius: 8,
            border: "1px solid rgba(255,255,255,0.18)",
            background: "rgba(255,255,255,0.06)",
            color: "#fff",
          }}
        />
      </div>

      <div style={{ marginTop: 18 }}>
        <strong>Gênero</strong>
        <select
          value={genre}
          onChange={(e) => setGenre(e.target.value)}
          style={{
            width: "100%",
            marginTop: 8,
            padding: 8,
            borderRadius: 8,
            border: "1px solid rgba(255,255,255,0.18)",
            background: "rgba(255,255,255,0.06)",
            color: "#fff",
          }}
        >
          <option value="">Todos</option>
          <option value="rock">Rock</option>
          <option value="pop">Pop</option>
          <option value="electronic">Eletrônica</option>
          <option value="jazz">Jazz</option>
        </select>
      </div>

      <div style={{ marginTop: 20 }}>
        <strong>Configurações</strong>
        <div style={{ marginTop: 8, fontSize: 14, color: "#d1d5db" }}>
          (Em breve)
        </div>
      </div>

      <div
        style={{
          marginTop: 20,
          display: "flex",
          flexDirection: "column",
          gap: 10,
        }}
      >
        <button onClick={resume} disabled={isPlaying || !current}>
          ▶ Play
        </button>
        <button onClick={pause} disabled={!isPlaying}>
          ⏸ Pause
        </button>
      </div>
    </div>
  )
}
