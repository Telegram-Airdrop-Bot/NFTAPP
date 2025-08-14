# 🛠️ Local Development Guide

## 📋 Overview

This guide will help you set up and run the NFT verification system locally on your computer. The system consists of three main components:

1. **🤖 Bot Server** - Telegram Bot (Python/Flask)
2. **🌐 API Server** - NFT Verification API (Python/Flask)  
3. **🎨 Frontend** - React Web App (Node.js/React)

## 🎯 Prerequisites

Before starting, make sure you have the following installed on your computer:

### **Required Software:**

#### **1. Python (3.8 or higher)**
- **Windows:** Download from [python.org](https://www.python.org/downloads/)
- **macOS:** `brew install python3`
- **Linux:** `sudo apt-get install python3 python3-pip`

#### **2. Node.js (16 or higher)**
- **Windows/macOS:** Download from [nodejs.org](https://nodejs.org/)
- **Linux:** `sudo apt-get install nodejs npm`

#### **3. Git**
- **Windows:** Download from [git-scm.com](https://git-scm.com/)
- **macOS:** `brew install git`
- **Linux:** `sudo apt-get install git`

### **Verify Installation:**
```bash
# Check Python version
python --version
# or
python3 --version

# Check Node.js version
node --version

# Check npm version
npm --version

# Check Git version
git --version
```

## 🚀 Step-by-Step Setup

### **Step 1: Clone and Setup Project**

#### **1.1 Clone the Repository:**
```bash
# Navigate to your desired directory
cd /path/to/your/projects

# Clone the repository
git clone <your-repository-url>
cd Final-NFT-VERIFY-BOT
```

#### **1.2 Create Environment File:**
```bash
# Copy the example environment file
cp env_example.txt .env

# Edit the .env file with your actual values
# You can use any text editor like Notepad, VS Code, etc.
```

#### **1.3 Configure Environment Variables:**
Edit the `.env` file with your actual values:

```env
# Bot Server Environment Variables
TELEGRAM_BOT_TOKEN=your_actual_telegram_bot_token
TELEGRAM_GROUP_ID=your_actual_telegram_group_id
HELIUS_API_KEY=6873bd5e-0b5d-49c4-a9ab-4e7febfd9cd3
COLLECTION_ID=j7qeFNnpWTbaf5g9sMCxP2zfKrH5QFgE56SuYjQDQi1

# API Server Environment Variables
WEBHOOK_URL=http://localhost:5001/verify_callback

# Frontend Environment Variables
REACT_APP_API_URL=http://localhost:5002
```

### **Step 2: Setup Bot Server**

#### **2.1 Navigate to Bot Server Directory:**
```bash
cd bot-server
```

#### **2.2 Create Virtual Environment:**
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

#### **2.3 Install Dependencies:**
```bash
# Install Python packages
pip install -r requirements.txt
```

#### **2.4 Test Bot Server:**
```bash
# Run the bot server
python bot.py
```

**Expected Output:**
```
Bot server started on port 5001
Bot is running...
```

### **Step 3: Setup API Server**

#### **3.1 Open New Terminal Window:**
Keep the bot server running and open a new terminal window.

#### **3.2 Navigate to API Server Directory:**
```bash
cd api-server
```

#### **3.3 Create Virtual Environment:**
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

#### **3.4 Install Dependencies:**
```bash
# Install Python packages
pip install -r requirements.txt
```

#### **3.5 Test API Server:**
```bash
# Run the API server
python api_server.py
```

**Expected Output:**
```
API server started on port 5002
API server is running...
```

### **Step 4: Setup Frontend**

#### **4.1 Open New Terminal Window:**
Keep both servers running and open a new terminal window.

#### **4.2 Navigate to Frontend Directory:**
```bash
cd frontend
```

#### **4.3 Install Dependencies:**
```bash
# Install Node.js packages
npm install
```

#### **4.4 Test Frontend:**
```bash
# Start the React development server
npm start
```

**Expected Output:**
```
Compiled successfully!

You can now view nft-verification-portal in the browser.

  Local:            http://localhost:3000
  On Your Network:  http://192.168.1.xxx:3000
```

## 🌐 Accessing Your Local Development Environment

After starting all three components, you can access:

- **🎨 Frontend:** http://localhost:3000
- **🌐 API Server:** http://localhost:5002
- **🤖 Bot Server:** http://localhost:5001

## 🧪 Testing Your Local Setup

### **Test 1: Frontend Loads**
1. Open your browser
2. Go to `http://localhost:3000`
3. You should see the NFT verification interface

### **Test 2: API Server Health Check**
```bash
# In a new terminal or browser
curl http://localhost:5002/api/config
# Expected: {"helius_api_key": "..."}
```

### **Test 3: Bot Server Health Check**
```bash
# In a new terminal or browser
curl http://localhost:5001/health
# Expected: {"status": "healthy", "service": "bot"}
```

### **Test 4: Complete NFT Verification Flow**
1. Open `http://localhost:3000`
2. Connect your Solana wallet
3. Try to verify an NFT
4. Check if the verification process works

## 🔧 Troubleshooting Common Issues

### **Issue 1: Python Not Found**
**Problem:** `python` command not recognized
**Solution:**
```bash
# Try using python3 instead
python3 --version

# Or add Python to PATH (Windows)
# Add C:\Python3x\ and C:\Python3x\Scripts\ to PATH
```

### **Issue 2: Node.js Not Found**
**Problem:** `node` or `npm` command not recognized
**Solution:**
```bash
# Reinstall Node.js from nodejs.org
# Make sure to check "Add to PATH" during installation
```

### **Issue 3: Port Already in Use**
**Problem:** `Address already in use` error
**Solution:**
```bash
# Find what's using the port (Windows)
netstat -ano | findstr :5001
netstat -ano | findstr :5002
netstat -ano | findstr :3000

# Kill the process (replace PID with actual process ID)
taskkill /PID <PID> /F

# On macOS/Linux:
lsof -ti:5001 | xargs kill -9
lsof -ti:5002 | xargs kill -9
lsof -ti:3000 | xargs kill -9
```

### **Issue 4: Virtual Environment Issues**
**Problem:** `venv` not found or activation fails
**Solution:**
```bash
# Install venv module
pip install virtualenv

# Create virtual environment with virtualenv
virtualenv venv

# Activate (Windows)
venv\Scripts\activate

# Activate (macOS/Linux)
source venv/bin/activate
```

### **Issue 5: npm Install Fails**
**Problem:** npm install errors or timeouts
**Solution:**
```bash
# Clear npm cache
npm cache clean --force

# Try with different registry
npm install --registry https://registry.npmjs.org/

# Or use yarn instead
npm install -g yarn
yarn install
```

### **Issue 6: Environment Variables Not Loading**
**Problem:** `.env` file not being read
**Solution:**
```bash
# Make sure .env file is in the correct directory
# Check if python-dotenv is installed
pip install python-dotenv

# Verify .env file format (no spaces around =)
TELEGRAM_BOT_TOKEN=your_token_here
```

## 📁 Project Structure

```
Final-NFT-VERIFY-BOT/
├── bot-server/
│   ├── bot.py              # Main bot file
│   ├── server.py           # Flask server
│   ├── verifier_js.py      # NFT verification logic
│   ├── requirements.txt     # Python dependencies
│   └── analytics.json      # Bot analytics
├── api-server/
│   ├── api_server.py       # Main API file
│   ├── verifier_js.py      # NFT verification logic
│   └── requirements.txt     # Python dependencies
├── frontend/
│   ├── src/                # React source code
│   ├── public/             # Static files
│   ├── package.json        # Node.js dependencies
│   └── tailwind.config.js  # Tailwind CSS config
├── .env                    # Environment variables
└── env_example.txt         # Environment template
```

## 🔄 Development Workflow

### **Making Changes:**

#### **Bot Server Changes:**
```bash
cd bot-server
# Edit bot.py or server.py
# Restart the server
python bot.py
```

#### **API Server Changes:**
```bash
cd api-server
# Edit api_server.py
# Restart the server
python api_server.py
```

#### **Frontend Changes:**
```bash
cd frontend
# Edit files in src/
# Changes auto-reload in browser
```

### **Hot Reload:**
- **Frontend:** Automatically reloads when you save changes
- **Bot Server:** Manual restart required
- **API Server:** Manual restart required

## 🐛 Debugging

### **Enable Debug Mode:**

#### **Bot Server Debug:**
```python
# In bot.py, add:
import logging
logging.basicConfig(level=logging.DEBUG)
```

#### **API Server Debug:**
```python
# In api_server.py, add:
app.run(debug=True, host='0.0.0.0', port=5002)
```

#### **Frontend Debug:**
- Open browser Developer Tools (F12)
- Check Console tab for errors
- Check Network tab for API calls

### **Logs:**
- **Bot Server:** Check terminal output
- **API Server:** Check terminal output
- **Frontend:** Check browser console

## 🚀 Quick Start Commands

### **One-Command Setup (Advanced Users):**
```bash
# Setup all components at once
# Bot Server
cd bot-server && python -m venv venv && venv\Scripts\activate && pip install -r requirements.txt && python bot.py &

# API Server (new terminal)
cd api-server && python -m venv venv && venv\Scripts\activate && pip install -r requirements.txt && python api_server.py &

# Frontend (new terminal)
cd frontend && npm install && npm start
```

## 📚 Additional Resources

### **Useful Commands:**
```bash
# Check running processes
netstat -ano | findstr :5001
netstat -ano | findstr :5002
netstat -ano | findstr :3000

# Kill all Python processes (Windows)
taskkill /F /IM python.exe

# Kill all Node processes (Windows)
taskkill /F /IM node.exe
```

### **Useful URLs:**
- **Frontend:** http://localhost:3000
- **API Health:** http://localhost:5002/api/config
- **Bot Health:** http://localhost:5001/health

### **Development Tips:**
- Keep all three terminals open for easy access
- Use VS Code or your preferred editor
- Check browser console for frontend errors
- Monitor terminal output for server errors

---

## 🎉 You're Ready!

Your local development environment is now set up! You can:

1. **Develop** - Make changes to any component
2. **Test** - Verify NFT functionality locally
3. **Debug** - Use browser tools and terminal logs
4. **Deploy** - Follow the deployment guide when ready

**Happy coding! 🚀** 