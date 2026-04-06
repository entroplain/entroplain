import type { Metadata } from 'next'
import './globals.css'

export const metadata: Metadata = {
  title: 'Entroplain - Early Exit for Efficient Agent Reasoning',
  description: 'Stop wasting tokens. Entroplain detects when LLMs have confidently answered and exits early, saving 30-50% on API costs.',
  openGraph: {
    title: 'Entroplain - Early Exit for Efficient Agent Reasoning',
    description: 'Stop wasting tokens. Detect confident answers and exit early.',
    url: 'https://entroplain.com',
    siteName: 'Entroplain',
    type: 'website',
  },
  twitter: {
    card: 'summary_large_image',
    title: 'Entroplain - Early Exit for Efficient Agent Reasoning',
    description: 'Stop wasting tokens. Detect confident answers and exit early.',
  },
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  )
}
