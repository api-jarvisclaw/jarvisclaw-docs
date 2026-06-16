import { defineConfig } from 'vitepress'

export default defineConfig({
  title: 'JarvisClaw',
  description: 'AI API Gateway — Smart routing, pay per call via x402',
  head: [
    ['link', { rel: 'icon', href: '/favicon.ico' }],
  ],
  themeConfig: {
    logo: '/logo.svg',
    nav: [
      { text: 'Docs', link: '/quickstart' },
      { text: 'API Reference', link: '/api/chat-completions' },
      { text: 'MCP & Agents', link: '/mcp' },
      { text: 'Dashboard', link: 'https://api.jarvisclaw.ai' },
    ],
    sidebar: [
      {
        text: 'Getting Started',
        items: [
          { text: 'Quick Start', link: '/quickstart' },
          { text: 'Smart Router', link: '/smart-router' },
        ],
      },
      {
        text: 'SDK',
        items: [
          { text: 'Python & Go SDK', link: '/sdk' },
          { text: 'Async & Concurrent', link: '/async' },
        ],
      },
      {
        text: 'Payments',
        items: [
          { text: 'Agent Payments (x402)', link: '/x402' },
          { text: 'Solana Payments', link: '/solana' },
          { text: 'Billing & Limits', link: '/billing' },
        ],
      },
      {
        text: 'Agent & MCP',
        items: [
          { text: 'MCP Configuration', link: '/mcp' },
          { text: 'Agent Registry', link: '/agent-registry' },
          { text: 'Discovery Protocol', link: '/discovery' },
        ],
      },
      {
        text: 'API Reference',
        items: [
          { text: 'Overview', link: '/api/' },
          { text: 'Chat Completions', link: '/api/chat-completions' },
          { text: 'Image Generation', link: '/api/image-generation' },
          { text: 'Video Generation', link: '/api/video-generation' },
          { text: 'Music Generation', link: '/api/music-generation' },
          { text: 'Audio & TTS', link: '/api/audio' },
          { text: 'Web Search', link: '/api/web-search' },
          { text: 'Prediction Markets', link: '/api/prediction-markets' },
          { text: 'DEX Trading (0x)', link: '/api/dex-trading' },
          { text: 'Compute (Sandbox)', link: '/api/compute' },
          { text: 'Crypto Data (Surf)', link: '/api/crypto-data' },
          { text: 'Phone & Voice', link: '/api/phone-voice' },
          { text: 'Trading Markets', link: '/api/trading-markets' },
          { text: 'RealFace & Portrait', link: '/api/realface' },
          { text: 'Errors', link: '/api/errors' },
        ],
      },
      {
        text: 'Reference',
        items: [
          { text: 'Models', link: '/models' },
          { text: 'Security', link: '/security' },
        ],
      },
    ],
    socialLinks: [
      { icon: 'github', link: 'https://github.com/api-jarvisclaw' },
    ],
    search: {
      provider: 'local',
    },
    footer: {
      message: 'Pay per call. No subscription. No rate limits.',
    },
  },
})
