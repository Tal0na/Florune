import { usePlayer } from "../features/player/usePlayer"

export default function PlaylistSidebar() {
  const { playlist, currentIndex, playIndex } = usePlayer()

  return (
    <aside className="rightSidebar scrollable">
      <h2>Playlists</h2>
      <section className="section">
        {playlist.length === 0 ? (
          <div className="muted">Nenhuma playlist carregada.</div>
        ) : (
          <ul className="playlist-list">
            {playlist.map((track, index) => (
              <li
                key={track.id}
                onClick={() => playIndex(index)}
                className={
                  index === currentIndex
                    ? "playlist-item active"
                    : "playlist-item"
                }
              >
                <strong className="playlist-item-title">{track.title}</strong>
                <span className="playlist-item-meta">{track.artist}</span>
              </li>
            ))}
          </ul>
        )}
      </section>
    </aside>
  )
}
