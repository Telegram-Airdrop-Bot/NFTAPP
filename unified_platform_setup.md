# 🌐 Unified Platform Setup - Web & Mobile

## Overview
Both web-based and mobile-based users will have access to the same NFT verification functionality with seamless cross-platform experience.

## 🎯 **Unified Features**

### **✅ Same Functionality for Both Platforms**
- **Wallet Connection**: Phantom, Solflare, Backpack, etc.
- **NFT Verification**: Collection filtering (Meta Betties)
- **Mobile Auto-Detection**: Automatic wallet detection on mobile
- **Web Interface**: Same UI for both platforms
- **Verification Process**: Identical verification flow
- **Redirect Logic**: Success redirect, failure no redirect

## 📱 **Mobile-Specific Features**

### **Auto-Detection & Connection**
```javascript
// Mobile device detection
const isMobile = /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent);

if (isMobile) {
  // Auto-detect available wallets
  const availableWallets = mobileWallets.filter(wallet => wallet.check());
  
  if (availableWallets.length === 1) {
    // Auto-connect to single wallet
    await wallet.connect();
  } else if (availableWallets.length > 1) {
    // Show web interface with highlighted wallets
    showVerificationSection();
    highlightAvailableWallets(availableWallets);
  }
}
```

### **Mobile Wallet Support**
- **Phantom Mobile** 🟣
- **Solflare Mobile** 🟠
- **Backpack Mobile** 🔵
- **Slope Mobile** 🟢
- **Glow Mobile** 🟡
- **Clover Mobile** 🟦
- **Coinbase Wallet** 🔵
- **Exodus Mobile** 🟣
- **Brave Wallet** 🦁
- **Torus Wallet** 🌀
- **Trust Wallet** 🛡️
- **Zerion Wallet** 💰

## 💻 **Web-Specific Features**

### **Manual Wallet Selection**
- **Same UI** as mobile but manual selection
- **All wallet buttons** available
- **No auto-detection** - user selects manually
- **Same verification process**

## 🔄 **Unified Verification Flow**

### **Step 1: Platform Detection**
```javascript
// Both platforms use same detection
const isMobile = /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent);
```

### **Step 2: Wallet Connection**
- **Mobile**: Auto-detect and connect
- **Web**: Manual selection
- **Both**: Same connection methods

### **Step 3: NFT Verification**
- **Both platforms**: Same API call
- **Both platforms**: Same collection filtering
- **Both platforms**: Same verification logic

### **Step 4: Result Handling**
- **Success**: Redirect to private Telegram group
- **Failure**: No redirect, bot removes from group

## 🚀 **Deployment Setup**

### **Frontend Deployment (Render)**
```yaml
services:
  - type: web
    name: meta-betties-frontend
    env: node
    buildCommand: npm ci --legacy-peer-deps && npm run build
    startCommand: npm start
    envVars:
      - key: REACT_APP_API_URL
        value: https://api-server-wcjc.onrender.com
```

### **API Server Deployment (Render)**
```yaml
services:
  - type: web
    name: api-server-wcjc
    env: python
    buildCommand: pip install -r requirements.txt
    startCommand: python api_server.py
```

### **Bot Server Deployment (Render)**
```yaml
services:
  - type: web
    name: bot-server
    env: python
    buildCommand: pip install -r requirements.txt
    startCommand: python bot.py
```

## 📱 **Mobile User Experience**

### **Automatic Flow**
1. **User opens verification link** on mobile
2. **System detects mobile device** automatically
3. **System scans for available wallets**
4. **If one wallet**: Auto-connects immediately
5. **If multiple wallets**: Shows selection with highlights
6. **User selects wallet** (if multiple)
7. **System auto-verifies** NFT ownership
8. **System auto-completes** verification
9. **User gets redirected** to Telegram group

### **Mobile Features**
- **Auto-detection** of mobile wallets
- **Smart selection** for multiple wallets
- **Touch-optimized** UI
- **Fast connection** process
- **Seamless verification**

## 💻 **Web User Experience**

### **Manual Flow**
1. **User opens verification link** on desktop
2. **System shows wallet selection** grid
3. **User manually selects** preferred wallet
4. **User connects wallet** manually
5. **System verifies** NFT ownership
6. **System completes** verification
7. **User gets redirected** to Telegram group

### **Web Features**
- **Manual wallet selection**
- **Desktop-optimized** UI
- **Full wallet support**
- **Same verification process**
- **Same redirect logic**

## 🔧 **Technical Implementation**

### **Unified Code Base**
```javascript
// Same verification function for both platforms
const verifyNFT = async () => {
  const response = await fetch(`${REACT_APP_API_URL}/api/verify-nft`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      wallet_address: userAddress,
      tg_id: tgId,
      collection_id: 'j7qeFNnpWTbaf5g9sMCxP2zfKrH5QFgE56SuYjQDQi1'
    })
  });
  
  const result = await response.json();
  
  if (result.has_nft) {
    // Success - redirect to private group
    setTimeout(() => {
      window.location.href = CONFIG.TELEGRAM_GROUPS.PRIVATE_KEY;
    }, 2000);
  } else {
    // Failure - no redirect, bot handles removal
    updateStatus('You will be removed from the group due to verification failure.', 'error');
  }
};
```

### **Platform-Specific Enhancements**
```javascript
// Mobile auto-detection
if (isMobile) {
  autoConnectMobileWallet();
} else {
  // Web - show manual selection
  showVerificationSection();
}
```

## 🎯 **User Access URLs**

### **Primary Verification URL**
```
https://meta-betties-frontend.onrender.com/?tg_id={user_id}
```

### **Direct API Access**
```
https://api-server-wcjc.onrender.com/api/verify-nft
```

### **Bot Webhook**
```
https://bot-server.onrender.com/verify_callback
```

## 📊 **Cross-Platform Benefits**

### **✅ Unified Experience**
- **Same functionality** on both platforms
- **Same verification process**
- **Same redirect logic**
- **Same error handling**

### **✅ Platform Optimization**
- **Mobile**: Auto-detection and fast connection
- **Web**: Manual selection and full control
- **Both**: Touch and mouse optimized UI

### **✅ Consistent Results**
- **Same API endpoints** for both platforms
- **Same collection filtering** (Meta Betties)
- **Same success/failure handling**
- **Same Telegram group access**

## 🎉 **Result**

Both web and mobile users now have:

- **✅ Same NFT verification functionality**
- **✅ Same wallet support**
- **✅ Same verification process**
- **✅ Same redirect logic**
- **✅ Platform-optimized experience**
- **✅ Seamless cross-platform access**

**Users can access the same functionality whether they're on mobile or desktop!** 🚀 