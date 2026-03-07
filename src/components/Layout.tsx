import type { ReactNode } from "react"
import Sidebar from "./Sidebar"

type Props = {
  children: ReactNode
}

export default function Layout({ children }: Props) {
  return (
    <div className="layout">
      <Sidebar />

      <main className="content">{children}</main>
    </div>
  )
}
