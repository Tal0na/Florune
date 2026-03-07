import type { ReactNode } from "react"
import Sidebar from "./Sidebar"
import PlaylistSidebar from "./PlaylistSidebar"

type Props = {
  children: ReactNode
}

export default function Layout({ children }: Props) {
  return (
    <div className="layout">
      <Sidebar />

      <main className="content">{children}</main>

      <PlaylistSidebar />
    </div>
  )
}
