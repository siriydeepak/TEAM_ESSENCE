# 🚀 How to Start AetherShelf

## Quick Start Guide (5 Minutes)

This guide will help you get AetherShelf running on your local machine in just 5 minutes.

---

## 📋 Prerequisites

Before you begin, make sure you have:

- ✅ **Node.js 18+** and **npm 9+** installed
- ✅ **Python 3.9+** installed
- ✅ **Git** installed
- ✅ A **Telegram account** (for Aether-Link Protocol)
- ✅ A **Google Gemini API key** (for receipt parsing)

---

## 🎯 Step 1: Clone the Repository

```bash
git clone <your-repository-url>
cd TEAM_ESSENCE
```

---

## 🎯 Step 2: Install Dependencies

### Frontend Dependencies

```bash
cd frontend
npm install
cd ..
```

### Backend Dependencies

```bash
cd backend
pip install -r requirements.txt
cd ..
```

---

## 🎯 Step 3: Configure Environment Variables

### Frontend Configuration

Create `frontend/.env`:

```bash
cd frontend
cp .env.example .env
```

Edit `frontend/.env` and set:

```env
# Backend API URL
VITE_API_URL=http://localhost:8000/api

# Telegram Bot Username (set this after creating your bot)
VITE_TELEGRAM_BOT_USERNAME=Aether_shelfBot

# App Version
VITE_APP_VERSION=2.0.0
```

### Backend Configuration

Create `backend/.env`:

```bash
cd backend
cp .env.example .env
```

Edit `backend/.env` and set:

```env
# ============================================
# TELEGRAM BOT (Required for Aether-Link)
# ============================================
TELEGRAM_BOT_TOKEN=your_bot_token_here
TELEGRAM_BOT_USERNAME=Aether_shelfBot

# ============================================
# GEMINI AI (Required for receipt parsing)
# ============================================
GEMINI_API_KEY=your_gemini_api_key_here

# ============================================
# DATABASE (Optional - uses in-memory if not set)
# ============================================
# For production, use PostgreSQL:
# DATABASE_URL=postgresql://user:password@localhost:5432/aethershelf

# For development, leave empty to use in-memory storage
DATABASE_URL=

# ============================================
# WEATHER API (Optional)
# ============================================
OWM_API_KEY=your_openweathermap_api_key_here
```

---

## 🎯 Step 4: Create Telegram Bot (2 Minutes)

### 4.1 Open Telegram and Search for BotFather

1. Open Telegram app
2. Search for `@BotFather`
3. Start a chat

### 4.2 Create Your Bot

Send this command:
```
/newbot
```

Follow the prompts:
- **Bot name:** AetherShelf Kitchen Assistant
- **Bot username:** Aether_shelfBot (or your preferred name)

### 4.3 Save Your Credentials

BotFather will give you:
```
✅ Token: 1234567890:ABCdefGHIjklMNOpqrsTUVwxyz
✅ Username: Aether_shelfBot
```

**Copy these values** and paste them into `backend/.env`:
```env
TELEGRAM_BOT_TOKEN=1234567890:ABCdefGHIjklMNOpqrsTUVwxyz
TELEGRAM_BOT_USERNAME=Aether_shelfBot
```

Also update `frontend/.env`:
```env
VITE_TELEGRAM_BOT_USERNAME=Aether_shelfBot
```

---

## 🎯 Step 5: Get Gemini API Key (1 Minute)

1. Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Click "Create API Key"
3. Copy the key (starts with `AIza...`)
4. Paste it into `backend/.env`:
   ```env
   GEMINI_API_KEY=AIzaSyC...your_key_here
   ```

---

## 🎯 Step 6: Start the Application

### Option A: Start Both Servers Together (Recommended)

Open **TWO terminals**:

**Terminal 1 - Backend:**
```bash
cd TEAM_ESSENCE/backend
python -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

**Terminal 2 - Frontend:**
```bash
cd TEAM_ESSENCE/frontend
npm run dev
```

### Option B: Start Individually

**Backend Only:**
```bash
cd backend
python -m uvicorn main:app --reload
```

**Frontend Only:**
```bash
cd frontend
npm run dev
```

---

## 🎯 Step 7: Access the Application

### Frontend (Web Dashboard)
```
http://localhost:3005/
```
(Note: Port may vary if 3000-3004 are in use)

### Backend (API)
```
http://localhost:8000/
```

### API Documentation
```
http://localhost:8000/api/docs
```

---

## 🎯 Step 8: Set Up Telegram Webhook (For Production)

### For Local Development (Using ngrok)

1. **Install ngrok:**
   ```bash
   # macOS
   brew install ngrok
   
   # Or download from https://ngrok.com/download
   ```

2. **Start ngrok tunnel:**
   ```bash
   ngrok http 8000
   ```

3. **Copy the HTTPS URL** (e.g., `https://abc123.ngrok.io`)

4. **Set webhook:**
   ```bash
   curl -X POST "https://api.telegram.org/bot<YOUR_BOT_TOKEN>/setWebhook" \
     -d "url=https://abc123.ngrok.io/api/telegram/webhook"
   ```

### For Production Deployment

```bash
curl -X POST "https://api.telegram.org/bot<YOUR_BOT_TOKEN>/setWebhook" \
  -d "url=https://your-domain.com/api/telegram/webhook"
```

### Verify Webhook

```bash
curl "https://api.telegram.org/bot<YOUR_BOT_TOKEN>/getWebhookInfo"
```

---

## ✅ Verification Checklist

Before using the app, verify:

- [ ] Frontend running on http://localhost:3005/ (or another port)
- [ ] Backend running on http://localhost:8000/
- [ ] Can access home page in browser
- [ ] No console errors in browser (press F12)
- [ ] Backend API docs accessible at http://localhost:8000/api/docs
- [ ] `.env` files configured in both frontend and backend
- [ ] Telegram bot created and token saved
- [ ] Gemini API key obtained and saved

---

## 🎨 Available Pages

Once both servers are running, you can access:

| Page | URL | Description |
|------|-----|-------------|
| Home | http://localhost:3005/ | Landing page |
| Login | http://localhost:3005/login | User authentication |
| Dashboard | http://localhost:3005/dashboard | Main dashboard with Aether-Link |
| Inventory | http://localhost:3005/inventory | Inventory management |
| Analytics | http://localhost:3005/analytics | Analytics & insights |
| Cart | http://localhost:3005/cart | Smart cart recommendations |
| Settings | http://localhost:3005/settings | User settings |

---

## 🔗 Test Aether-Link Protocol

### 1. Open Dashboard
Navigate to: http://localhost:3005/dashboard

### 2. Find "Link Your Kitchen" Section
You should see:
- 6-digit sync code
- QR code (click "Show QR")
- "Add Bot" button

### 3. Link Your Telegram

**Method 1: QR Code**
1. Click "Show QR"
2. Open Telegram on your phone
3. Scan the QR code
4. Bot opens with code pre-filled

**Method 2: Direct Link**
1. Click "Add Bot" button
2. Telegram opens in browser/app
3. Click "Start"
4. Code is automatically sent

**Method 3: Manual Entry**
1. Open Telegram
2. Search for `@Aether_shelfBot` (or your bot username)
3. Type `/start` or just the 6-digit code

### 4. Verify Connection

After entering the code, you should see:

**In Telegram:**
```
✅ Kitchen Linked Successfully!

Welcome! Your AetherShelf digital twin is now connected.

You'll receive real-time alerts for:
  🥛 Expiring items
  📦 Inventory additions via receipt
  🛒 Smart cart suggestions
```

**In Dashboard:**
- Status changes to "Linked ✓"
- Green success animation

---

## 🧾 Test Receipt Upload

### 1. Navigate to Virtual Kitchen
Go to: http://localhost:3005/dashboard (scroll down)

### 2. Upload a Receipt
1. Click "Upload Receipt"
2. Select a grocery receipt image (JPG, PNG, WEBP)
3. Wait for processing (2-5 seconds)

### 3. Verify Results
- Items extracted and displayed
- Telegram notification received
- Items added to inventory

---

## 🐛 Troubleshooting

### Issue: "Cannot connect to backend"

**Symptom:** Frontend loads but shows connection errors

**Solution:** Make sure backend is running:
```bash
cd backend
python -m uvicorn main:app --reload
```

### Issue: "Module not found: qrcode.react"

**Solution:** Install the missing dependency:
```bash
cd frontend
npm install qrcode.react
```

### Issue: "Port already in use"

**Solution:** The app will automatically find an available port. Check the terminal output for the actual port number.

Or manually specify a port:
```bash
npm run dev -- --port 3010
```

### Issue: "Telegram bot not responding"

**Solution:**
1. Check webhook status:
   ```bash
   curl "https://api.telegram.org/bot<TOKEN>/getWebhookInfo"
   ```
2. Verify `TELEGRAM_BOT_TOKEN` in `backend/.env`
3. Make sure webhook URL is HTTPS (use ngrok for local dev)
4. Restart backend server

### Issue: "Gemini API error"

**Solution:**
1. Verify `GEMINI_API_KEY` in `backend/.env`
2. Check API quota at [Google AI Studio](https://makersuite.google.com/)
3. Test API key:
   ```bash
   curl "https://generativelanguage.googleapis.com/v1beta/models?key=YOUR_KEY"
   ```

### Issue: "Database connection failed"

**Solution:**
1. For development, leave `DATABASE_URL` empty to use in-memory storage
2. For production, verify PostgreSQL is running:
   ```bash
   pg_isready
   ```
3. Check connection string format:
   ```
   postgresql://user:password@host:5432/database
   ```

### Issue: "Environment variables not working"

**Solution:**
1. Make sure `.env` file exists in both `frontend/` and `backend/` directories
2. Restart both servers after changing `.env`
3. Frontend variables must start with `VITE_` prefix
4. Backend variables are loaded via `python-dotenv`

---

## 🔥 Development Tips

### 1. Hot Reload
Both frontend and backend support hot reload:
- **Frontend:** Changes reflect instantly in browser
- **Backend:** Server restarts automatically on file changes

### 2. API Documentation
Backend provides interactive API docs:
- **Swagger UI:** http://localhost:8000/api/docs
- **ReDoc:** http://localhost:8000/api/redoc

### 3. Browser DevTools
Press **F12** in browser to:
- View console logs
- Inspect network requests
- Debug React components (install React DevTools extension)

### 4. Network Access
Use the network URL to test on mobile devices:
```
http://192.168.1.x:3005/
```
(Check terminal output for exact IP)

### 5. Database Inspection
For PostgreSQL:
```bash
psql -d aethershelf
\dt  # List tables
SELECT * FROM telegram_links;
```

---

## 📚 Next Steps

### For Development:
1. Explore the codebase in `frontend/src/` and `backend/`
2. Read the API documentation at http://localhost:8000/api/docs
3. Check out the React components in `frontend/src/components/`
4. Review the backend services in `backend/services/`

### For Production Deployment:
1. Set up PostgreSQL database
2. Configure production environment variables
3. Deploy to Vercel/Heroku (see README.md)
4. Set up production Telegram webhook
5. Configure domain and SSL certificate

### For Testing:
1. Upload various receipt formats
2. Test weather-based shelf life adjustments
3. Try smart cart recommendations
4. Explore analytics dashboard
5. Test Telegram notifications

---

## 🆘 Need Help?

- **Setup Issues:** Re-read this guide carefully
- **API Errors:** Check http://localhost:8000/api/docs
- **Frontend Errors:** Check browser console (F12)
- **Backend Errors:** Check terminal running backend server
- **Telegram Issues:** Verify bot token and webhook setup
- **General Questions:** See README.md for architecture details

---

## ✅ Success!

If you've completed all steps, you should now have:

- ✅ Frontend running and accessible
- ✅ Backend API running
- ✅ Telegram bot connected
- ✅ Aether-Link Protocol working
- ✅ Receipt upload functional
- ✅ Real-time notifications enabled

**Congratulations! You're ready to use AetherShelf! 🎉**

---

**Built with ❤️ by TEAM_ESSENCE**
