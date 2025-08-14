# Bot Architecture - Fixed Event Loop Issues

## 🔧 **Problem Solved**
The original bot had event loop conflicts because Flask and Telegram bot were trying to use the same event loop. This caused the error:
```
RuntimeError: This event loop is already running
```

## 🏗️ **New Architecture**

### **1. Simple Bot (`bot_simple.py`)**
- **Purpose**: Pure Telegram bot without Flask
- **Features**: 
  - User join/remove logic
  - Admin notifications
  - Analytics tracking
  - Webhook data processing
- **Event Loop**: Single, clean event loop

### **2. Webhook Server (`webhook_server.py`)**
- **Purpose**: Handles verification callbacks from API server
- **Features**:
  - Receives webhook data
  - Stores data in file
  - Provides API for bot to read data
- **Event Loop**: Separate Flask event loop

### **3. API Server (`api_server.py`)**
- **Purpose**: Handles NFT verification requests
- **Features**:
  - NFT verification logic
  - Sends results to webhook server
- **Event Loop**: Separate Flask event loop

## 🔄 **Data Flow**

```
User joins group
    ↓
Bot sends verification link
    ↓
User clicks link → Frontend
    ↓
Frontend connects wallet → API Server
    ↓
API Server verifies NFT → Webhook Server
    ↓
Webhook Server saves data → Bot reads data
    ↓
Bot processes verification → User added/removed
```

## 🚀 **Deployment Instructions**

### **Step 1: Deploy Webhook Server**
```bash
# Deploy to Render using webhook_render.yaml
# Service name: webhook-server
# URL: https://webhook-server-kem4.onrender.com
```

### **Step 2: Deploy Bot Server**
```bash
# Deploy to Render using render.yaml
# Service name: bot-server
# URL: https://bot-server-kem4.onrender.com
```

### **Step 3: Update API Server**
```bash
# Update WEBHOOK_URL in api_server.py
WEBHOOK_URL = "https://webhook-server-kem4.onrender.com/verify_callback"
```

### **Step 4: Update Frontend**
```bash
# Update API server URL in frontend
# Point to your API server
```

## 📋 **Environment Variables**

### **Bot Server (`bot_simple.py`)**
```env
TELEGRAM_BOT_TOKEN=your_bot_token
TELEGRAM_GROUP_ID=your_group_id
ADMIN_CHAT_ID=your_admin_id
ADMIN_NOTIFICATIONS=true
COLLECTION_ID=your_collection_id
WEBHOOK_SERVER_URL=https://webhook-server-kem4.onrender.com
```

### **Webhook Server (`webhook_server.py`)**
```env
# No special environment variables needed
# Uses default Flask configuration
```

### **API Server (`api_server.py`)**
```env
HELIUS_API_KEY=your_helius_key
WEBHOOK_URL=https://webhook-server-kem4.onrender.com/verify_callback
```

## 🔍 **Monitoring**

### **Bot Server Logs**
- User join/leave events
- Verification processing
- Admin notifications
- Webhook data processing

### **Webhook Server Logs**
- Incoming webhook data
- Data storage/retrieval
- Health check responses

### **API Server Logs**
- NFT verification requests
- Helius API calls
- Webhook forwarding

## 🛠️ **Troubleshooting**

### **Event Loop Errors**
- ✅ **Fixed**: Separated Flask and Telegram bot event loops
- ✅ **Fixed**: Webhook server handles HTTP requests
- ✅ **Fixed**: Bot server handles Telegram updates

### **Webhook Communication**
- ✅ **Fixed**: File-based communication between webhook server and bot
- ✅ **Fixed**: Periodic checking for new webhook data
- ✅ **Fixed**: Automatic cleanup after processing

### **Bot Conflicts**
- ✅ **Fixed**: Single bot instance with proper locking
- ✅ **Fixed**: Clean startup and shutdown
- ✅ **Fixed**: Proper error handling

## 📊 **Performance Benefits**

1. **No Event Loop Conflicts**: Each service has its own event loop
2. **Better Error Isolation**: Issues in one service don't affect others
3. **Scalable Architecture**: Can deploy services independently
4. **Easier Debugging**: Clear separation of concerns
5. **Reliable Communication**: File-based webhook data transfer

## 🔄 **Migration from Old Bot**

1. **Stop old bot**: `pkill python` or restart Render service
2. **Deploy new services**: Use new render.yaml files
3. **Update URLs**: Point API server to webhook server
4. **Test functionality**: Verify user join/verification flow
5. **Monitor logs**: Check for any remaining issues

## ✅ **Success Indicators**

- ✅ No "event loop already running" errors
- ✅ Users can join and get verification links
- ✅ Verification process completes successfully
- ✅ Users are added/removed based on NFT ownership
- ✅ Admin notifications work properly
- ✅ Analytics logging functions correctly 