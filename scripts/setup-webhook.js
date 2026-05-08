#!/usr/bin/env node
/**
 * setup-webhook.js
 * Registers the Telegram bot webhook to the provided public URL.
 *
 * Usage:
 *   node scripts/setup-webhook.js <PUBLIC_URL>
 *
 * Examples:
 *   node scripts/setup-webhook.js https://abc123.ngrok.io
 *   node scripts/setup-webhook.js https://my-app.vercel.app
 *
 * The script will:
 *   1. Read TELEGRAM_BOT_TOKEN from .env (root or backend/.env)
 *   2. Register <PUBLIC_URL>/api/telegram/webhook with Telegram
 *   3. Print the current webhook info to confirm registration
 */

const https = require('https')
const fs    = require('fs')
const path  = require('path')

// ── Load .env manually (no deps needed) ─────────────────────────────────────
function loadEnv(...paths) {
  for (const p of paths) {
    const full = path.resolve(__dirname, '..', p)
    if (!fs.existsSync(full)) continue
    const lines = fs.readFileSync(full, 'utf8').split('\n')
    for (const line of lines) {
      const m = line.match(/^\s*([A-Z_][A-Z0-9_]*)\s*=\s*(.*)$/)
      if (m && !process.env[m[1]]) {
        process.env[m[1]] = m[2].trim().replace(/^["']|["']$/g, '')
      }
    }
  }
}

loadEnv('.env', 'backend/.env', 'backend/.env.example')

const BOT_TOKEN  = process.env.TELEGRAM_BOT_TOKEN
const PUBLIC_URL = process.argv[2]

if (!BOT_TOKEN || BOT_TOKEN === 'your_telegram_bot_token_here') {
  console.error('\n❌  TELEGRAM_BOT_TOKEN is not set in your .env file.')
  console.error('    Get one from @BotFather → /newbot\n')
  process.exit(1)
}

if (!PUBLIC_URL) {
  console.error('\n❌  Usage: node scripts/setup-webhook.js <PUBLIC_URL>')
  console.error('    Example: node scripts/setup-webhook.js https://abc123.ngrok.io\n')
  process.exit(1)
}

const webhookUrl = `${PUBLIC_URL.replace(/\/$/, '')}/api/telegram/webhook`
const TGAPI      = `https://api.telegram.org/bot${BOT_TOKEN}`

function tgRequest(path, body) {
  return new Promise((resolve, reject) => {
    const data    = body ? JSON.stringify(body) : null
    const options = {
      hostname: 'api.telegram.org',
      path,
      method: body ? 'POST' : 'GET',
      headers: body
        ? { 'Content-Type': 'application/json', 'Content-Length': Buffer.byteLength(data) }
        : {},
    }
    const req = https.request(options, res => {
      let raw = ''
      res.on('data', c => raw += c)
      res.on('end', () => resolve(JSON.parse(raw)))
    })
    req.on('error', reject)
    if (data) req.write(data)
    req.end()
  })
}

async function main() {
  console.log('\n🔗  AetherShelf — Telegram Webhook Setup')
  console.log('─'.repeat(50))
  console.log(`📡  Bot token : ...${BOT_TOKEN.slice(-8)}`)
  console.log(`🌐  Webhook   : ${webhookUrl}\n`)

  // Step 1: delete any old webhook
  await tgRequest(`/bot${BOT_TOKEN}/deleteWebhook`)

  // Step 2: set new webhook
  const setResult = await tgRequest(`/bot${BOT_TOKEN}/setWebhook`, {
    url:             webhookUrl,
    allowed_updates: ['message', 'edited_message'],
    drop_pending_updates: true,
  })

  if (setResult.ok) {
    console.log('✅  Webhook registered successfully!')
  } else {
    console.error('❌  Failed to register webhook:', setResult.description)
    process.exit(1)
  }

  // Step 3: verify
  const info = await tgRequest(`/bot${BOT_TOKEN}/getWebhookInfo`)
  const wi   = info.result
  console.log('\n📋  Webhook info:')
  console.log(`    URL           : ${wi.url}`)
  console.log(`    Pending       : ${wi.pending_update_count}`)
  console.log(`    Last error    : ${wi.last_error_message || 'none'}`)
  console.log(`\n🚀  AetherShelf bot is live! Test it by messaging @${process.env.TELEGRAM_BOT_USERNAME || 'YourBot'} on Telegram.\n`)
}

main().catch(err => { console.error('Fatal:', err); process.exit(1) })
