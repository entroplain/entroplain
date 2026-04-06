import type { Metadata } from 'next'
import { Analytics } from '@vercel/analytics/next'
import { SpeedInsights } from '@vercel/speed-insights/next'
import './globals.css'

export const metadata: Metadata = {
  title: 'Entroplain - Early Exit for Efficient Agent Reasoning',
  description: 'Stop wasting tokens. Entroplain detects when LLMs have confidently answered and exits early, saving 30-50% on API costs.',
  openGraph: {
    title: 'Entroplain - Early Exit for Efficient Agent Reasoning',
    description: 'Stop wasting tokens. Detect confident answers and exit early.',
    type: 'website',
  },
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <head>
        <link rel="preconnect" href="https://fonts.googleapis.com" />
        <link rel="preconnect" href="https://fonts.gstatic.com" crossOrigin="anonymous" />
        <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet" />
      </head>
      <body style={{ margin: 0, padding: 0 }}>{children}
        <Analytics />
        <SpeedInsights />
      </body>
    </html>
  )
}
