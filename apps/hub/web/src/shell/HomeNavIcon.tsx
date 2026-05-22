import { useId } from 'react'

/** Hearth flame for pinned Home control — docs/design/mockups/dashboard-*.html */

type Props = {
  className?: string
}

export function HomeNavIcon({ className }: Props) {
  const gradientId = useId()
  return (
    <svg className={className} viewBox="0 0 256 256" aria-hidden width={22} height={22}>
      <defs>
        <linearGradient id={gradientId} x1="78" y1="56" x2="178" y2="212" gradientUnits="userSpaceOnUse">
          <stop offset="0" stopColor="#FFB84D" />
          <stop offset="0.54" stopColor="#F97316" />
          <stop offset="1" stopColor="#B83A14" />
        </linearGradient>
      </defs>
      <path
        fill={`url(#${gradientId})`}
        d="M129 216c-34.2 0-58-21.8-58-53.1 0-20.6 11.1-37.1 27.3-52.7 13.2-12.7 22.5-27 28.8-45.9 22.3 19.7 34.3 40.1 34.3 58.6 8.9-7 14.7-17.1 17-29.5 19.2 17.4 28.6 38.1 28.6 62.8 0 36.1-30.8 59.8-78 59.8Z"
      />
    </svg>
  )
}
