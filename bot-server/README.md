# 🤖 Bot Server - Conflict Resolution Guide

## 🚨 **Conflict Error: "terminated by other getUpdates request"**

এই error হয় যখন একই bot token দিয়ে দুইটি bot instance run হচ্ছে।

## 🔧 **Solutions:**

### **Solution 1: Use Startup Script (Recommended)**
```bash
python start_bot.py
```
এই script automatically conflict check করবে এবং existing processes kill করবে।

### **Solution 2: Manual Conflict Resolution**

#### **Step 1: Stop All Python Processes**
```bash
# Linux/Mac
pkill python

# Windows
taskkill /f /im python.exe
```

#### **Step 2: Delete Lock File**
```bash
rm bot_server.lock
```

#### **Step 3: Restart Bot**
```bash
python bot.py
```

### **Solution 3: Check for Duplicate Files**

আপনার bot-server folder এ শুধুমাত্র এই files থাকা উচিত:
- ✅ `bot.py` (main bot file)
- ✅ `start_bot.py` (startup script)
- ✅ `requirements.txt`
- ✅ `render.yaml`

❌ `server.py` (deleted - duplicate file)

### **Solution 4: Environment Variables**

আপনার environment variables সঠিকভাবে set করা আছে কিনা check করুন:

```bash
# Required Environment Variables
TELEGRAM_BOT_TOKEN=your_bot_token_here
TELEGRAM_GROUP_ID=your_group_id_here
HELIUS_API_KEY=your_helius_api_key_here
ADMIN_CHAT_ID=your_admin_chat_id_here
```

### **Solution 5: Hosting Platform Restart**

যদি hosting platform (Render/Vercel/Netlify) ব্যবহার করছেন:

1. **Stop** the current deployment
2. **Wait** 30 seconds
3. **Redeploy** the application

## 🔍 **Debugging Steps:**

### **1. Check Running Processes**
```bash
# Linux/Mac
ps aux | grep python

# Windows
tasklist | findstr python
```

### **2. Check Bot Status**
```bash
# Test bot connection
curl https://api.telegram.org/bot<YOUR_BOT_TOKEN>/getMe
```

### **3. Check Logs**
```bash
# View recent logs
tail -f bot_server.log
```

## 🚀 **Safe Startup Commands:**

### **Option 1: Use Startup Script**
```bash
python start_bot.py
```

### **Option 2: Manual Safe Start**
```bash
# 1. Kill existing processes
pkill python

# 2. Wait 5 seconds
sleep 5

# 3. Start bot
python bot.py
```

### **Option 3: Docker (if using)**
```bash
# Stop all containers
docker stop $(docker ps -q)

# Remove containers
docker rm $(docker ps -aq)

# Start fresh
docker-compose up
```

## 📋 **Common Issues & Solutions:**

| Issue | Solution |
|-------|----------|
| Lock file exists | Delete `bot_server.lock` |
| Multiple Python processes | Kill with `pkill python` |
| Webhook conflicts | Clear webhook with bot API |
| Environment variables missing | Check `.env` file |
| Hosting platform issues | Restart deployment |

## 🔧 **Emergency Reset:**

যদি সব কিছু fail করে:

```bash
# 1. Stop everything
pkill python
rm -f bot_server.lock

# 2. Clear webhook
curl -X POST https://api.telegram.org/bot<YOUR_BOT_TOKEN>/deleteWebhook

# 3. Wait
sleep 10

# 4. Start fresh
python bot.py
```

## 📞 **Support:**

যদি সমস্যা persist করে:
1. Check logs for specific error messages
2. Verify bot token is correct
3. Ensure only one deployment is running
4. Contact support with error logs 