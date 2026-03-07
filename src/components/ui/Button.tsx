import type { ButtonHTMLAttributes } from "react"

type ButtonVariant = "primary" | "ghost"

type Props = ButtonHTMLAttributes<HTMLButtonElement> & {
  variant?: ButtonVariant
}

export default function Button({
  variant = "primary",
  className = "",
  ...props
}: Props) {
  const variantClass = variant === "ghost" ? "btn--ghost" : "btn--primary"
  return (
    <button
      className={["btn", variantClass, className].filter(Boolean).join(" ")}
      {...props}
    />
  )
}
