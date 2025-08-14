# 🚀 Multi-Server Deployment Guide

## 📋 Overview

This project is deployed across 3 different servers:

1. **🤖 Bot Server** - Telegram Bot (Render)
2. **🌐 API Server** - NFT Verification API (Render)  
3. **🎨 Frontend** - React Web App (Netlify)

## 🏗️ Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Frontend      │    │   API Server    │    │   Bot Server    │
│   (Netlify)     │◄──►│   (Render)      │◄──►│   (Render)      │
│                 │    │                 │    │                 │
│ React Web App   │    │ Flask API       │    │ Telegram Bot    │
│ NFT Verification│    │ NFT Verification│    │ Group Management│
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## 🚀 Deployment Steps

### 0. 🔧 Local Environment Setup

Before deploying, set up your local environment variables:

#### **Create .env file:**
```bash
# Copy the example file
cp env_example.txt .env

# Edit the .env file with your actual values
# TELEGRAM_BOT_TOKEN=your_actual_bot_token
# TELEGRAM_GROUP_ID=your_actual_group_id
```

#### **Required Environment Variables:**
```env
# Bot Server
TELEGRAM_BOT_TOKEN=your_telegram_bot_token
TELEGRAM_GROUP_ID=your_telegram_group_id
HELIUS_API_KEY=6873bd5e-0b5d-49c4-a9ab-4e7febfd9cd3
COLLECTION_ID=j7qeFNnpWTbaf5g9sMCxP2zfKrH5QFgE56SuYjQDQi1

# API Server
WEBHOOK_URL=https://meta-betties-bot-server.onrender.com/verify_callback

# Frontend
REACT_APP_API_URL=https://meta-betties-api-server.onrender.com
```

### 1. 🤖 Bot Server (Render)

#### **Repository Setup:**
```bash
# Create bot-server repository
git init
git add .
git commit -m "Initial bot server commit"
git remote add origin https://github.com/yourusername/meta-betties-bot-server
git push -u origin main
```

#### **Render Deployment:**
1. Go to [Render Dashboard](https://dashboard.render.com)
2. Click "New +" → "Web Service"
3. Connect your GitHub repository
4. Configure:
   - **Name:** `meta-betties-bot-server`
   - **Environment:** `Python`
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `python bot.py`

#### **Environment Variables:**
```env
TELEGRAM_BOT_TOKEN=your_telegram_bot_token
TELEGRAM_GROUP_ID=your_telegram_group_id
HELIUS_API_KEY=6873bd5e-0b5d-49c4-a9ab-4e7febfd9cd3
COLLECTION_ID=j7qeFNnpWTbaf5g9sMCxP2zfKrH5QFgE56SuYjQDQi1
WEBHOOK_URL=https://meta-betties-api-server.onrender.com/api/verify-nft
```

#### **Health Check:**
- **URL:** `https://meta-betties-bot-server.onrender.com/health`
- **Expected Response:** `{"status": "healthy", "service": "bot"}`

---

### 2. 🌐 API Server (Render)

#### **Repository Setup:**
```bash
# Create api-server repository
git init
git add .
git commit -m "Initial API server commit"
git remote add origin https://github.com/yourusername/meta-betties-api-server
git push -u origin main
```

#### **Render Deployment:**
1. Go to [Render Dashboard](https://dashboard.render.com)
2. Click "New +" → "Web Service"
3. Connect your GitHub repository
4. Configure:
   - **Name:** `meta-betties-api-server`
   - **Environment:** `Python`
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `python api_server.py`

#### **Environment Variables:**
```env
HELIUS_API_KEY=6873bd5e-0b5d-49c4-a9ab-4e7febfd9cd3
COLLECTION_ID=j7qeFNnpWTbaf5g9sMCxP2zfKrH5QFgE56SuYjQDQi1
WEBHOOK_URL=https://meta-betties-bot-server.onrender.com/verify_callback
```

#### **Health Check:**
- **URL:** `https://meta-betties-api-server.onrender.com/api/config`
- **Expected Response:** `{"helius_api_key": "..."}`

---

### 3. 🎨 Frontend (Netlify)

#### **Repository Setup:**
```bash
# Create frontend repository
git init
git add .
git commit -m "Initial frontend commit"
git remote add origin https://github.com/yourusername/meta-betties-frontend
git push -u origin main
```

#### **Netlify Deployment:**
1. Go to [Netlify Dashboard](https://app.netlify.com)
2. Click "New site from Git"
3. Connect your GitHub repository
4. Configure:
   - **Repository:** `meta-betties-frontend`
   - **Branch:** `main`
   - **Build command:** `npm run build`
   - **Publish directory:** `build`

#### **Environment Variables:**
```env
REACT_APP_API_URL=https://meta-betties-api-server.onrender.com
```

#### **Custom Domain (Optional):**
- **Domain:** `nft-verify.metabetties.com`
- **SSL:** Automatic

---

## 🔗 Server URLs

### **Production URLs:**
- **Frontend:** `https://meta-betties-frontend.netlify.app`
- **API Server:** `https://meta-betties-api-server.onrender.com`
- **Bot Server:** `https://meta-betties-bot-server.onrender.com`

### **Health Check URLs:**
- **Frontend:** `https://meta-betties-frontend.netlify.app`
- **API Server:** `https://meta-betties-api-server.onrender.com/api/config`
- **Bot Server:** `https://meta-betties-bot-server.onrender.com/health`

---

## ⚙️ Configuration Files

### **Bot Server (`bot-server/`):**
```
├── bot.py              # Main bot file
├── verifier_js.py      # NFT verification logic
├── requirements.txt     # Python dependencies
├── render.yaml         # Render deployment config
└── .env               # Environment variables (local)
```

### **API Server (`api-server/`):**
```
├── api_server.py       # Main API file
├── verifier_js.py      # NFT verification logic
├── requirements.txt     # Python dependencies
├── render.yaml         # Render deployment config
└── .env               # Environment variables (local)
```

### **Frontend (`frontend/`):**
```
├── src/
│   ├── App.js          # Main React component
│   └── config.js       # Configuration settings
├── public/
│   └── _redirects      # Netlify redirects
├── package.json        # Node.js dependencies
├── netlify.toml        # Netlify deployment config
└── .env               # Environment variables (local)
```

---

## 🔄 Deployment Order

### **Step 1: Deploy Bot Server**
1. Deploy bot server to Render
2. Get the bot server URL
3. Test health check endpoint

### **Step 2: Deploy API Server**
1. Update API server webhook URL to bot server
2. Deploy API server to Render
3. Test API endpoints

### **Step 3: Deploy Frontend**
1. Update frontend API URL to API server
2. Deploy frontend to Netlify
3. Test complete flow

---

## 🧪 Testing Deployment

### **Bot Server Test:**
```bash
curl https://meta-betties-bot-server.onrender.com/health
# Expected: {"status": "healthy", "service": "bot"}
```

### **API Server Test:**
```bash
curl https://meta-betties-api-server.onrender.com/api/config
# Expected: {"helius_api_key": "..."}
```

### **Frontend Test:**
```bash
curl https://meta-betties-frontend.netlify.app
# Expected: React app loads successfully
```

### **Complete Flow Test:**
1. Visit frontend URL
2. Connect wallet
3. Verify NFT
4. Check Telegram group access

---

## 🔧 Troubleshooting

### **Common Issues:**

#### **Bot Server Issues:**
- **Problem:** Bot not responding
- **Solution:** Check BOT_TOKEN and GROUP_ID environment variables

#### **API Server Issues:**
- **Problem:** NFT verification failing
- **Solution:** Check HELIUS_API_KEY and webhook URL

#### **Frontend Issues:**
- **Problem:** API calls failing
- **Solution:** Check REACT_APP_API_URL environment variable

### **Logs:**
- **Render:** Dashboard → Service → Logs
- **Netlify:** Dashboard → Site → Functions → Logs

---

## 📊 Monitoring

### **Health Checks:**
- **Bot Server:** `/health` endpoint
- **API Server:** `/api/config` endpoint
- **Frontend:** Main page loads

### **Analytics:**
- **Bot Analytics:** Stored in `analytics.json`
- **API Analytics:** Render dashboard metrics
- **Frontend Analytics:** Netlify analytics

---

## 🔐 Security

### **Environment Variables:**
- ✅ Never commit `.env` files
- ✅ Use Render/Netlify environment variables
- ✅ Rotate API keys regularly

### **CORS Configuration:**
- ✅ API server allows all origins for development
- ✅ Configure specific origins for production

### **SSL/HTTPS:**
- ✅ Automatic SSL on Render
- ✅ Automatic SSL on Netlify

---

## 🚀 Final URLs

After deployment, your services will be available at:

- **🌐 Frontend:** `https://meta-betties-frontend.netlify.app`
- **🔗 API:** `https://meta-betties-api-server.onrender.com`
- **🤖 Bot:** `https://meta-betties-bot-server.onrender.com`
- **📱 Telegram:** `https://t.me/MetaBettiesPrivateKey`

---

**🎉 Deployment Complete!** Your NFT verification system is now live across multiple servers! 