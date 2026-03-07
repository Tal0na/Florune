import { usePlayer } from "../features/player/usePlayer"
import Button from "./ui/Button"

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
    <aside className="sidebar scrollable">
      <h2>Florune</h2>

      <section className="section">
        <h3>Buscar músicas</h3>
        <input
          className="input"
          value={searchQuery}
          onChange={(e) => setSearchQuery(e.target.value)}
          placeholder="Digite um título ou artista"
        />
      </section>

      <section className="section">
        <h3>Gênero</h3>
        <select
          className="input"
          value={genre}
          onChange={(e) => setGenre(e.target.value)}
        >
          <option value="">Todos</option>
          <option value="rock">Rock</option>
          <option value="pop">Pop</option>
          <option value="electronic">Eletrônica</option>
          <option value="jazz">Jazz</option>
        </select>
      </section>

      <section className="section">
        <h3>Configurações</h3>
        <div className="muted">(Em breve)</div>
      </section>

      <div className="section button-group">
        <Button onClick={resume} disabled={isPlaying || !current}>
          ▶ Play
        </Button>
        <Button onClick={pause} disabled={!isPlaying} variant="ghost">
          ⏸ Pause
        </Button>
      </div>
    </aside>
  )
}
