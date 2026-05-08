import { useState, useRef } from 'react'
import { useNavigate } from 'react-router-dom'
import axios from 'axios'
import toast from 'react-hot-toast'
import DashboardLayout from '../components/layout/DashboardLayout'
import {
  Upload, Camera, Plus, Loader2, CheckCircle2,
  Package, Leaf, Drumstick, Milk, ShoppingBag, Flame,
} from 'lucide-react'

const API = import.meta.env.VITE_API_URL || '/api'

const CATEGORIES = [
  'Dairy','Produce','Protein','Bakery','Snacks',
  'Beverages','Grains','Condiments','Frozen','Other',
]
const CATEGORY_ICONS: Record<string,JSX.Element> = {
  Dairy:<Milk size={14}/>, Produce:<Leaf size={14}/>, Protein:<Drumstick size={14}/>,
  Bakery:<ShoppingBag size={14}/>, Snacks:<ShoppingBag size={14}/>,
  Beverages:<ShoppingBag size={14}/>, Grains:<ShoppingBag size={14}/>,
  Condiments:<ShoppingBag size={14}/>, Frozen:<Flame size={14}/>, Other:<Package size={14}/>,
}

interface ParsedItem { name: string; quantity: number; unit: string; price_inr: number | null; category: string }

export default function VirtualKitchenPage() {
  const navigate = useNavigate()
  const webUserId = localStorage.getItem('userEmail') || 'demo@aethershelf.app'
  const fileRef = useRef<HTMLInputElement>(null)

  // ── Receipt upload state ─────────────────────────────────────────────────
  const [preview, setPreview] = useState<string | null>(null)
  const [file, setFile] = useState<File | null>(null)
  const [uploading, setUploading] = useState(false)
  const [parsedItems, setParsedItems] = useState<ParsedItem[]>([])
  const [uploadDone, setUploadDone] = useState(false)

  // ── Manual entry state ───────────────────────────────────────────────────
  const [form, setForm] = useState({
    name:'', quantity:'1', unit:'units', category:'Other',
    price:'', shelf_life_days:'7',
  })
  const [adding, setAdding] = useState(false)
  const [addedItems, setAddedItems] = useState<string[]>([])

  // ── Handlers ─────────────────────────────────────────────────────────────
  const onFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const f = e.target.files?.[0]
    if (!f) return
    setFile(f)
    setPreview(URL.createObjectURL(f))
    setParsedItems([])
    setUploadDone(false)
  }

  const uploadReceipt = async () => {
    if (!file) return toast.error('Please select a receipt image first.')
    setUploading(true)
    try {
      const fd = new FormData()
      fd.append('web_user_id', webUserId)
      fd.append('file', file)
      const { data } = await axios.post(`${API}/kitchen/upload-receipt`, fd, {
        headers: { 'Content-Type': 'multipart/form-data' },
      })
      setParsedItems(data.parsed_items || [])
      setUploadDone(true)
      toast.success(`✅ ${data.added_count} items added from receipt!`)
    } catch (err: any) {
      toast.error(err?.response?.data?.detail || 'Receipt upload failed.')
    } finally {
      setUploading(false)
    }
  }

  const addItem = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!form.name.trim()) return toast.error('Item name is required.')
    setAdding(true)
    try {
      const { data } = await axios.post(`${API}/kitchen/add-item`, {
        web_user_id: webUserId,
        name: form.name.trim(),
        quantity: parseFloat(form.quantity) || 1,
        unit: form.unit,
        category: form.category,
        price: form.price ? parseFloat(form.price) : null,
        shelf_life_days: parseInt(form.shelf_life_days) || 7,
      })
      toast.success(data.message || 'Item added!')
      setAddedItems(prev => [form.name.trim(), ...prev])
      setForm({ name:'', quantity:'1', unit:'units', category:'Other', price:'', shelf_life_days:'7' })
    } catch (err: any) {
      toast.error(err?.response?.data?.detail || 'Failed to add item.')
    } finally {
      setAdding(false)
    }
  }

  // ── Styles ───────────────────────────────────────────────────────────────
  const card: React.CSSProperties = {
    background:'#1e1b4b', border:'1px solid rgba(255,255,255,0.08)',
    borderRadius:'20px', padding:'1.6rem',
  }
  const label: React.CSSProperties = {
    display:'block', fontSize:'0.78rem', fontWeight:600,
    color:'rgba(255,255,255,0.5)', marginBottom:'6px', textTransform:'uppercase', letterSpacing:'0.05em',
  }
  const input: React.CSSProperties = {
    width:'100%', background:'rgba(255,255,255,0.06)', border:'1px solid rgba(255,255,255,0.12)',
    borderRadius:'10px', padding:'10px 14px', color:'#fff', fontSize:'0.92rem',
    outline:'none', boxSizing:'border-box',
  }

  return (
    <DashboardLayout>
      <div style={{ maxWidth:'900px', margin:'0 auto', display:'flex', flexDirection:'column', gap:'1.8rem' }}>

        {/* Page header */}
        <div style={{ display:'flex', alignItems:'center', justifyContent:'space-between', flexWrap:'wrap', gap:'12px' }}>
          <div>
            <h1 style={{ margin:0, fontSize:'1.6rem', fontWeight:800, color:'#fff' }}>Virtual Kitchen Setup</h1>
            <p style={{ margin:0, fontSize:'0.88rem', color:'rgba(255,255,255,0.45)', marginTop:'4px' }}>
              No sensors needed — upload a receipt or add items manually
            </p>
          </div>
          <button onClick={() => navigate('/dashboard')}
            style={{ background:'rgba(255,255,255,0.08)', border:'1px solid rgba(255,255,255,0.15)', borderRadius:'10px', padding:'8px 18px', color:'#fff', cursor:'pointer', fontSize:'0.88rem' }}>
            ← Back to Dashboard
          </button>
        </div>

        {/* ── SECTION 1: Receipt Upload ─────────────────────────────────── */}
        <div style={card}>
          <h2 style={{ margin:'0 0 4px', color:'#fff', fontSize:'1.1rem', fontWeight:700 }}>
            <Camera size={18} style={{ verticalAlign:'middle', marginRight:'8px', color:'#818cf8' }}/>
            Inventory Ingestion via Receipt
          </h2>
          <p style={{ margin:'0 0 1.2rem', color:'rgba(255,255,255,0.4)', fontSize:'0.84rem' }}>
            Take a photo of any grocery receipt. Gemini AI extracts every item instantly.
          </p>

          {/* Drop zone */}
          <div
            id="receipt-drop-zone"
            onClick={() => fileRef.current?.click()}
            style={{
              border:`2px dashed ${preview ? 'rgba(99,102,241,0.6)' : 'rgba(255,255,255,0.15)'}`,
              borderRadius:'14px', padding:'2rem', textAlign:'center', cursor:'pointer',
              background: preview ? 'rgba(99,102,241,0.05)' : 'rgba(255,255,255,0.02)',
              transition:'all 0.2s', position:'relative', overflow:'hidden',
            }}
          >
            {preview ? (
              <img src={preview} alt="Receipt preview" style={{ maxHeight:'220px', borderRadius:'10px', objectFit:'contain', maxWidth:'100%' }}/>
            ) : (
              <>
                <Upload size={36} color="rgba(255,255,255,0.3)" style={{ marginBottom:'12px' }}/>
                <p style={{ color:'rgba(255,255,255,0.5)', margin:0, fontSize:'0.9rem' }}>
                  Click to select receipt photo
                </p>
                <p style={{ color:'rgba(255,255,255,0.25)', margin:'4px 0 0', fontSize:'0.78rem' }}>
                  JPG, PNG, WEBP supported
                </p>
              </>
            )}
            <input ref={fileRef} type="file" accept="image/*" onChange={onFileChange} style={{ display:'none' }}/>
          </div>

          {preview && !uploadDone && (
            <button
              id="upload-receipt-btn"
              onClick={uploadReceipt}
              disabled={uploading}
              style={{ marginTop:'1rem', width:'100%', padding:'12px', borderRadius:'12px', border:'none', cursor: uploading ? 'wait' : 'pointer', background:'linear-gradient(135deg,#6366f1,#8b5cf6)', color:'#fff', fontWeight:700, fontSize:'0.95rem', display:'flex', alignItems:'center', justifyContent:'center', gap:'8px' }}
            >
              {uploading ? <><Loader2 size={18} style={{ animation:'spin 1s linear infinite' }}/> Parsing with Gemini AI…</> : <><Upload size={18}/> Parse & Add to Pantry</>}
            </button>
          )}

          {/* Parsed items */}
          {uploadDone && parsedItems.length > 0 && (
            <div style={{ marginTop:'1.2rem' }}>
              <p style={{ color:'#a5b4fc', fontWeight:600, fontSize:'0.85rem', marginBottom:'10px' }}>
                <CheckCircle2 size={14} style={{ verticalAlign:'middle', marginRight:'4px', color:'#34d399' }}/>
                {parsedItems.length} items extracted and added to your pantry:
              </p>
              <div style={{ display:'flex', flexWrap:'wrap', gap:'8px' }}>
                {parsedItems.map((item, i) => (
                  <div key={i} style={{ padding:'6px 14px', borderRadius:'999px', background:'rgba(99,102,241,0.15)', border:'1px solid rgba(99,102,241,0.3)', color:'#c7d2fe', fontSize:'0.82rem', display:'flex', alignItems:'center', gap:'6px' }}>
                    {CATEGORY_ICONS[item.category] || <Package size={14}/>}
                    {item.name} <span style={{ opacity:0.6 }}>×{item.quantity} {item.unit}</span>
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>

        {/* ── SECTION 2: Manual Entry ───────────────────────────────────── */}
        <div style={card}>
          <h2 style={{ margin:'0 0 4px', color:'#fff', fontSize:'1.1rem', fontWeight:700 }}>
            <Plus size={18} style={{ verticalAlign:'middle', marginRight:'8px', color:'#34d399' }}/>
            Manual Item Entry
          </h2>
          <p style={{ margin:'0 0 1.4rem', color:'rgba(255,255,255,0.4)', fontSize:'0.84rem' }}>
            Add items one by one. A Telegram confirmation will be sent after each addition.
          </p>

          <form id="manual-item-form" onSubmit={addItem}>
            <div style={{ display:'grid', gridTemplateColumns:'repeat(auto-fit,minmax(180px,1fr))', gap:'1rem' }}>
              <div style={{ gridColumn:'1/-1' }}>
                <label style={label}>Item Name *</label>
                <input id="item-name-input" style={input} placeholder="e.g. Amul Milk 1L"
                  value={form.name} onChange={e => setForm(f => ({ ...f, name:e.target.value }))}/>
              </div>
              <div>
                <label style={label}>Quantity</label>
                <input id="item-qty-input" type="number" min="0.1" step="0.1" style={input}
                  value={form.quantity} onChange={e => setForm(f => ({ ...f, quantity:e.target.value }))}/>
              </div>
              <div>
                <label style={label}>Unit</label>
                <input id="item-unit-input" style={input} placeholder="L, kg, pcs…"
                  value={form.unit} onChange={e => setForm(f => ({ ...f, unit:e.target.value }))}/>
              </div>
              <div>
                <label style={label}>Category</label>
                <select id="item-category-select" style={{ ...input, appearance:'none' }}
                  value={form.category} onChange={e => setForm(f => ({ ...f, category:e.target.value }))}>
                  {CATEGORIES.map(c => <option key={c} value={c}>{c}</option>)}
                </select>
              </div>
              <div>
                <label style={label}>Price (₹)</label>
                <input id="item-price-input" type="number" min="0" step="0.01" style={input} placeholder="Optional"
                  value={form.price} onChange={e => setForm(f => ({ ...f, price:e.target.value }))}/>
              </div>
              <div>
                <label style={label}>Shelf Life (days)</label>
                <input id="item-shelf-input" type="number" min="1" style={input}
                  value={form.shelf_life_days} onChange={e => setForm(f => ({ ...f, shelf_life_days:e.target.value }))}/>
              </div>
            </div>

            <button id="add-item-submit-btn" type="submit" disabled={adding}
              style={{ marginTop:'1.2rem', padding:'12px 28px', borderRadius:'12px', border:'none', cursor: adding ? 'wait' : 'pointer', background:'linear-gradient(135deg,#10b981,#059669)', color:'#fff', fontWeight:700, fontSize:'0.95rem', display:'flex', alignItems:'center', gap:'8px' }}>
              {adding ? <><Loader2 size={18} style={{ animation:'spin 1s linear infinite' }}/> Adding…</> : <><Plus size={18}/> Add to Virtual Shelf</>}
            </button>
          </form>

          {/* Confirmation feed */}
          {addedItems.length > 0 && (
            <div style={{ marginTop:'1.2rem', display:'flex', flexDirection:'column', gap:'6px' }}>
              {addedItems.map((name, i) => (
                <div key={i} style={{ display:'flex', alignItems:'center', gap:'8px', padding:'8px 12px', borderRadius:'8px', background:'rgba(16,185,129,0.1)', border:'1px solid rgba(16,185,129,0.25)', color:'#34d399', fontSize:'0.85rem' }}>
                  <CheckCircle2 size={14}/> <strong>{name}</strong> added — Telegram confirmation sent ✓
                </div>
              ))}
            </div>
          )}
        </div>
      </div>
      <style>{`@keyframes spin{to{transform:rotate(360deg)}}`}</style>
    </DashboardLayout>
  )
}
