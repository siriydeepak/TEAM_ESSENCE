import { useState, useEffect, useCallback, useRef } from 'react'
import { QRCodeSVG } from 'qrcode.react'
import axios from 'axios'
import toast from 'react-hot-toast'
import {
  Bot, RefreshCw, CheckCircle2, Copy, ExternalLink,
  WifiOff, Zap, Shield, Wifi, Clock, Loader2, QrCode,
} from 'lucide-react'

const API         = import.meta.env.VITE_API_URL || '/api'
const BOT_USERNAME = import.meta.env.VITE_TELEGRAM_BOT_USERNAME || 'Aether_shelfBot'
const POLL_MS     = 3000

/* ── shared micro-styles ─────────────────────────────────────────────────── */
const stepCard: React.CSSProperties = {
  display:'flex', gap:'14px', alignItems:'flex-start',
  background:'rgba(255,255,255,0.04)', border:'1px solid rgba(255,255,255,0.08)',
  borderRadius:'14px', padding:'1.1rem',
}
const digitBox: React.CSSProperties = {
  width:'42px', height:'52px', borderRadius:'10px',
  border:'1px solid rgba(255,255,255,0.12)',
  display:'flex', alignItems:'center', justifyContent:'center',
  fontSize:'1.4rem', fontWeight:800, transition:'all 0.3s',
}
const iconBtn: React.CSSProperties = {
  background:'rgba(255,255,255,0.08)', border:'1px solid rgba(255,255,255,0.12)',
  borderRadius:'8px', padding:'8px', cursor:'pointer',
  color:'rgba(255,255,255,0.6)', display:'flex', alignItems:'center',
}

function StepBadge({ n }: { n: string }) {
  return (
    <div style={{ width:'32px', height:'32px', borderRadius:'10px', flexShrink:0,
      background:'linear-gradient(135deg,#6366f1,#8b5cf6)',
      display:'flex', alignItems:'center', justifyContent:'center',
      fontWeight:800, fontSize:'0.9rem', color:'#fff',
      boxShadow:'0 4px 12px rgba(99,102,241,0.35)',
    }}>{n}</div>
  )
}

export default function LinkKitchen() {
  const webUserId = localStorage.getItem('userEmail') || 'demo@aethershelf.app'

  const [syncCode,   setSyncCode]   = useState('')
  const [linked,     setLinked]     = useState(false)
  const [loading,    setLoading]    = useState(true)
  const [refreshing, setRefreshing] = useState(false)
  const [copied,     setCopied]     = useState(false)
  const [waiting,    setWaiting]    = useState(false)
  const [showQR,     setShowQR]     = useState(false)
  const [ttlSec,     setTtlSec]     = useState(300)

  const pollRef = useRef<ReturnType<typeof setInterval> | null>(null)
  const ttlRef  = useRef<ReturnType<typeof setInterval> | null>(null)

  /* bot URL always includes sync code for deep-link /start  */
  const botUrl = syncCode && syncCode !== '------'
    ? `https://t.me/${BOT_USERNAME}?start=${syncCode}`
    : `https://t.me/${BOT_USERNAME}`

  /* ── fetch / generate code ─────────────────────────────────────────────── */
  const fetchCode = useCallback(async (silent = false) => {
    if (!silent) setLoading(true); else setRefreshing(true)
    try {
      const { data } = await axios.post(`${API}/telegram/generate-code`, { web_user_id: webUserId })
      setSyncCode(data.sync_code ?? '------')
      setLinked(!!data.already_linked)
      if (typeof data.ttl_seconds === 'number') setTtlSec(data.ttl_seconds)
    } catch { setSyncCode('------') }
    finally { setLoading(false); setRefreshing(false) }
  }, [webUserId])

  useEffect(() => { fetchCode() }, [fetchCode])

  /* ── TTL countdown ─────────────────────────────────────────────────────── */
  useEffect(() => {
    if (ttlRef.current) clearInterval(ttlRef.current)
    if (linked || loading) return
    ttlRef.current = setInterval(() => {
      setTtlSec(prev => {
        if (prev <= 1) { fetchCode(true); return 300 }
        return prev - 1
      })
    }, 1000)
    return () => { if (ttlRef.current) clearInterval(ttlRef.current) }
  }, [linked, loading, fetchCode])

  /* ── 3-second status poll ──────────────────────────────────────────────── */
  useEffect(() => {
    if (linked || !syncCode || syncCode === '------') return
    setWaiting(true)
    pollRef.current = setInterval(async () => {
      try {
        const { data } = await axios.get(`${API}/telegram/status`, { params: { web_user_id: webUserId } })
        if (data.linked) {
          setLinked(true); setWaiting(false)
          if (pollRef.current) clearInterval(pollRef.current)
          if (ttlRef.current)  clearInterval(ttlRef.current)
          toast.success('🎉 Kitchen linked to Telegram!', { duration: 5000 })
        }
      } catch { /* silent */ }
    }, POLL_MS)
    return () => { if (pollRef.current) clearInterval(pollRef.current) }
  }, [syncCode, linked, webUserId])

  /* ── helpers ───────────────────────────────────────────────────────────── */
  const copyCode = () => {
    if (!syncCode || syncCode === '------') return
    navigator.clipboard.writeText(syncCode).then(() => {
      setCopied(true); toast.success('Sync code copied!')
      setTimeout(() => setCopied(false), 2000)
    })
  }
  const fmtTtl = (s: number) => `${Math.floor(s/60)}:${String(s%60).padStart(2,'0')}`
  const ttlPct  = Math.min(100, (ttlSec / 300) * 100)
  const digits  = syncCode.replace(/\D/g,'').padEnd(6,'-').slice(0,6).split('')

  /* ── render ────────────────────────────────────────────────────────────── */
  return (
    <section id="link-kitchen-section" style={{
      background:'linear-gradient(135deg,#0f0c29,#302b63,#24243e)',
      borderRadius:'20px', padding:'2rem', position:'relative', overflow:'hidden',
      boxShadow:'0 25px 60px rgba(0,0,0,0.4)', border:'1px solid rgba(255,255,255,0.07)',
    }}>
      {/* Ambient blobs */}
      <div style={{ position:'absolute', top:'-60px', right:'-60px', width:'220px', height:'220px', borderRadius:'50%', background:'radial-gradient(circle,rgba(99,102,241,0.35),transparent 70%)', pointerEvents:'none' }}/>
      <div style={{ position:'absolute', bottom:'-40px', left:'30%', width:'160px', height:'160px', borderRadius:'50%', background:'radial-gradient(circle,rgba(20,184,166,0.25),transparent 70%)', pointerEvents:'none' }}/>

      {/* Header */}
      <div style={{ display:'flex', alignItems:'center', gap:'14px', marginBottom:'1.6rem', flexWrap:'wrap' }}>
        <div style={{ width:'48px', height:'48px', borderRadius:'14px', flexShrink:0, background:'linear-gradient(135deg,#6366f1,#8b5cf6)', display:'flex', alignItems:'center', justifyContent:'center', boxShadow:'0 0 20px rgba(99,102,241,0.5)' }}>
          <Bot size={26} color="#fff"/>
        </div>
        <div>
          <h2 style={{ margin:0, fontSize:'1.25rem', fontWeight:700, color:'#fff' }}>Link Your Kitchen</h2>
          <p style={{ margin:0, fontSize:'0.82rem', color:'rgba(255,255,255,0.5)' }}>Aether-Link Protocol · @{BOT_USERNAME}</p>
        </div>
        {/* Status badge */}
        <div style={{ marginLeft:'auto', display:'flex', alignItems:'center', gap:'6px', padding:'6px 14px', borderRadius:'999px',
          background: linked ? 'rgba(20,184,166,0.15)' : waiting ? 'rgba(99,102,241,0.15)' : 'rgba(255,255,255,0.07)',
          border:`1px solid ${linked ? 'rgba(20,184,166,0.5)' : waiting ? 'rgba(99,102,241,0.4)' : 'rgba(255,255,255,0.12)'}` }}>
          {linked
            ? <><CheckCircle2 size={14} color="#14b8a6"/><span style={{ fontSize:'0.78rem', color:'#14b8a6', fontWeight:600 }}>Linked</span></>
            : waiting
              ? <><Loader2 size={14} color="#818cf8" style={{ animation:'spin 1s linear infinite' }}/><span style={{ fontSize:'0.78rem', color:'#818cf8', fontWeight:500 }}>Waiting…</span></>
              : <><WifiOff size={14} color="rgba(255,255,255,0.4)"/><span style={{ fontSize:'0.78rem', color:'rgba(255,255,255,0.4)' }}>Not Linked</span></>
          }
        </div>
      </div>

      {/* ── LINKED state ── */}
      {linked ? (
        <div style={{ background:'rgba(20,184,166,0.08)', border:'1px solid rgba(20,184,166,0.3)', borderRadius:'14px', padding:'1.6rem', textAlign:'center' }}>
          <div style={{ display:'flex', justifyContent:'center', marginBottom:'12px' }}>
            <div style={{ width:'64px', height:'64px', borderRadius:'50%', background:'rgba(20,184,166,0.15)', border:'2px solid rgba(20,184,166,0.5)', display:'flex', alignItems:'center', justifyContent:'center', animation:'pulse-ring 2s infinite' }}>
              <CheckCircle2 size={32} color="#14b8a6"/>
            </div>
          </div>
          <p style={{ color:'#14b8a6', fontWeight:700, fontSize:'1.1rem', margin:'0 0 6px' }}>Kitchen Successfully Linked!</p>
          <p style={{ color:'rgba(255,255,255,0.45)', fontSize:'0.85rem', margin:0 }}>Real-time Telegram alerts are now active for expiring items, additions, and smart cart updates.</p>
        </div>
      ) : (
        <div style={{ display:'flex', gap:'1.4rem', flexWrap:'wrap', alignItems:'flex-start' }}>

          {/* Left: Steps */}
          <div style={{ flex:'1', minWidth:'260px', display:'flex', flexDirection:'column', gap:'1.2rem' }}>

            {/* Step A — QR / Button */}
            <div style={stepCard}>
              <StepBadge n="A"/>
              <div style={{ flex:1 }}>
                <p style={{ margin:'0 0 2px', fontWeight:700, fontSize:'0.95rem', color:'#fff' }}>Open AetherShelf Bot</p>
                <p style={{ margin:'0 0 10px', fontSize:'0.82rem', color:'rgba(255,255,255,0.45)' }}>
                  Scan the QR code or tap the button — your sync code is pre-filled.
                </p>
                <div style={{ display:'flex', gap:'8px', flexWrap:'wrap' }}>
                  <a id="add-aethershelf-bot-btn" href={botUrl} target="_blank" rel="noopener noreferrer"
                    style={{ display:'inline-flex', alignItems:'center', gap:'8px', padding:'9px 16px', borderRadius:'10px', background:'linear-gradient(135deg,#229ED9,#1d8fc4)', color:'#fff', fontWeight:700, fontSize:'0.86rem', textDecoration:'none', boxShadow:'0 6px 20px rgba(34,158,217,0.3)' }}>
                    <Bot size={16}/> Add Bot <ExternalLink size={13}/>
                  </a>
                  <button id="toggle-qr-btn" onClick={() => setShowQR(v => !v)}
                    style={{ display:'inline-flex', alignItems:'center', gap:'6px', padding:'9px 14px', borderRadius:'10px', background:'rgba(99,102,241,0.15)', border:'1px solid rgba(99,102,241,0.35)', color:'#a5b4fc', fontWeight:600, fontSize:'0.86rem', cursor:'pointer' }}>
                    <QrCode size={15}/> {showQR ? 'Hide QR' : 'Show QR'}
                  </button>
                </div>
              </div>
            </div>

            {/* Step B — Sync code */}
            <div style={stepCard}>
              <StepBadge n="B"/>
              <div style={{ flex:1 }}>
                <p style={{ margin:'0 0 2px', fontWeight:700, fontSize:'0.95rem', color:'#fff' }}>Kitchen Sync Code</p>
                <p style={{ margin:'0 0 10px', fontSize:'0.82rem', color:'rgba(255,255,255,0.45)' }}>
                  Type this in the bot — or the QR deep-link fills it automatically.
                </p>
                <div style={{ display:'flex', alignItems:'center', gap:'10px', flexWrap:'wrap' }}>
                  <div style={{ display:'flex', gap:'6px' }}>
                    {loading
                      ? [...Array(6)].map((_,i) => <div key={i} style={{ ...digitBox, background:'rgba(255,255,255,0.05)', opacity:0.5 }}>·</div>)
                      : digits.map((d,i) => (
                          <div key={i} style={{ ...digitBox,
                            color: d==='-' ? 'rgba(255,255,255,0.2)' : '#fff',
                            background: d==='-' ? 'rgba(255,255,255,0.04)' : 'rgba(99,102,241,0.2)',
                            borderColor: d==='-' ? 'rgba(255,255,255,0.08)' : 'rgba(99,102,241,0.5)',
                            boxShadow: d!=='-' ? '0 0 8px rgba(99,102,241,0.3)' : 'none',
                          }}>{d==='-' ? '·' : d}</div>
                        ))
                    }
                  </div>
                  <button id="copy-sync-code-btn" onClick={copyCode} style={iconBtn} title="Copy code">
                    {copied ? <CheckCircle2 size={16} color="#14b8a6"/> : <Copy size={16}/>}
                  </button>
                  <button id="refresh-sync-code-btn" onClick={() => fetchCode(true)} style={iconBtn} title="Refresh">
                    <RefreshCw size={16} style={{ animation: refreshing ? 'spin 1s linear infinite' : 'none' }}/>
                  </button>
                </div>
                {/* TTL bar */}
                {!loading && (
                  <div style={{ marginTop:'12px' }}>
                    <div style={{ display:'flex', justifyContent:'space-between', marginBottom:'5px' }}>
                      <span style={{ fontSize:'0.72rem', color:'rgba(255,255,255,0.35)', display:'flex', alignItems:'center', gap:'4px' }}>
                        <Clock size={11}/> Expires {fmtTtl(ttlSec)}
                      </span>
                      {waiting && (
                        <span style={{ fontSize:'0.72rem', color:'#818cf8', display:'flex', alignItems:'center', gap:'4px' }}>
                          <Loader2 size={11} style={{ animation:'spin 1s linear infinite' }}/> Polling every 3 s…
                        </span>
                      )}
                    </div>
                    <div style={{ height:'3px', background:'rgba(255,255,255,0.08)', borderRadius:'99px', overflow:'hidden' }}>
                      <div style={{ height:'100%', borderRadius:'99px', transition:'width 1s linear', width:`${ttlPct}%`,
                        background: ttlPct > 50 ? '#6366f1' : ttlPct > 20 ? '#f59e0b' : '#ef4444' }}/>
                    </div>
                  </div>
                )}
              </div>
            </div>

            {/* Trust strip */}
            <div style={{ display:'flex', gap:'16px', flexWrap:'wrap' }}>
              {[
                { icon:<Shield size={12}/>, l:'Zero hardware needed' },
                { icon:<Zap size={12}/>, l:'Hardware-agnostic' },
                { icon:<Wifi size={12}/>, l:'Real-time sync' },
              ].map(({ icon, l }) => (
                <div key={l} style={{ display:'flex', alignItems:'center', gap:'5px', color:'rgba(255,255,255,0.32)', fontSize:'0.74rem' }}>
                  {icon}{l}
                </div>
              ))}
            </div>
          </div>

          {/* Right: QR panel */}
          {showQR && (
            <div style={{ flexShrink:0, display:'flex', flexDirection:'column', alignItems:'center', gap:'12px',
              background:'rgba(255,255,255,0.04)', border:'1px solid rgba(255,255,255,0.1)',
              borderRadius:'18px', padding:'20px',
              animation:'fadeIn 0.25s ease',
            }}>
              {/* QR code with gradient-matching wrapper */}
              <div style={{ padding:'12px', background:'#fff', borderRadius:'14px', boxShadow:'0 0 30px rgba(99,102,241,0.4)' }}>
                <QRCodeSVG
                  id="telegram-bot-qr"
                  value={botUrl}
                  size={160}
                  bgColor="#ffffff"
                  fgColor="#302b63"
                  level="H"
                  imageSettings={{
                    src: "data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='%23229ED9'%3E%3Cpath d='M12 0C5.373 0 0 5.373 0 12s5.373 12 12 12 12-5.373 12-12S18.627 0 12 0zm5.894 8.221-1.97 9.28c-.145.658-.537.818-1.084.508l-3-2.21-1.447 1.394c-.16.16-.295.295-.605.295l.213-3.053 5.56-5.023c.242-.213-.054-.333-.373-.12L8.32 14.617l-2.96-.924c-.643-.204-.657-.643.136-.953l11.57-4.461c.537-.194 1.006.131.828.942z'/%3E%3C/svg%3E",
                    x: undefined, y: undefined,
                    height: 32, width: 32,
                    excavate: true,
                  }}
                />
              </div>
              <div style={{ textAlign:'center' }}>
                <p style={{ margin:'0 0 2px', fontWeight:700, color:'#fff', fontSize:'0.88rem' }}>@{BOT_USERNAME}</p>
                <p style={{ margin:0, fontSize:'0.74rem', color:'rgba(255,255,255,0.35)' }}>Scan to open in Telegram</p>
              </div>
              <a href={botUrl} target="_blank" rel="noopener noreferrer"
                style={{ fontSize:'0.76rem', color:'#818cf8', textDecoration:'none', display:'flex', alignItems:'center', gap:'4px' }}>
                <ExternalLink size={11}/> Open link instead
              </a>
            </div>
          )}
        </div>
      )}

      <style>{`
        @keyframes spin { to { transform: rotate(360deg); } }
        @keyframes pulse-ring { 0%,100%{box-shadow:0 0 0 0 rgba(20,184,166,0.4)} 50%{box-shadow:0 0 0 12px rgba(20,184,166,0)} }
        @keyframes fadeIn { from{opacity:0;transform:scale(0.95)} to{opacity:1;transform:scale(1)} }
      `}</style>
    </section>
  )
}
