# 🤖 Bot Welcome Message & NFT Verification Link Location

## 📍 **Exact Location in Code**

### **File: `bot-server/bot.py`**

### **🔔 Welcome Function (Lines 156-265)**
```python
async def welcome(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Welcome new members and send verification link"""
```

### **📤 Where the Message is Sent**

#### **1. Verification Link Creation (Line 185)**
```python
# Create verification link - UPDATE THIS URL
verify_link = f"https://admin-q2j7.onrender.com/?tg_id={user_id}"
print(f"🔗 Verification link: {verify_link}")
```

#### **2. Welcome Message Content (Lines 187-205)**
```python
# Create welcome message
welcome_text = f"""🎉 <b>Welcome to Meta Betties Private Key!</b>

👋 Hi @{username}, we're excited to have you join our exclusive community!

🔐 <b>Verification Required</b>
To access this private group, you must verify your NFT ownership.

🔗 <b>Click here to verify:</b> <a href="{verify_link}">Verify NFT Ownership</a>

📋 <b>Or copy this link:</b>
<code>{verify_link}</code>

⏰ <b>Time Limit:</b> You have 5 minutes to complete verification, or you'll be automatically removed.

💎 <b>Supported Wallets:</b> Phantom, Solflare, Backpack, Slope, Glow, Clover, Coinbase, Exodus, Brave, Torus, Trust Wallet, Zerion

🔄 <b>Multiple Verifications:</b> You can verify multiple times with the same Telegram ID.

Need help? Contact an admin!"""
```

#### **3. Message Sending (Lines 207-215)**
```python
# Send message to group
sent_message = await context.bot.send_message(
    chat_id=GROUP_ID,
    text=welcome_text,
    parse_mode='HTML',
    disable_web_page_preview=True
)

print(f"✅ Welcome message sent successfully to @{username}")
print(f"📄 Message ID: {sent_message.message_id}")
```

### **🎯 Handler Setup (Line 590)**
```python
# Add handlers
app.add_handler(MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, welcome))
```

## 🔄 **Complete Flow**

### **Step 1: User Joins Group**
- User joins the Telegram group
- Bot detects new member via `filters.StatusUpdate.NEW_CHAT_MEMBERS`

### **Step 2: Welcome Function Triggered**
```python
async def welcome(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Check if correct group
    if str(update.message.chat.id) != str(GROUP_ID):
        return
    
    # Process each new member
    for new_member in update.message.new_chat_members:
        if new_member.is_bot:
            continue
            
        user_id = new_member.id
        username = new_member.username or new_member.first_name
```

### **Step 3: Create Verification Link**
```python
# Create verification link
verify_link = f"https://admin-q2j7.onrender.com/?tg_id={user_id}"
```

### **Step 4: Send Welcome Message**
```python
# Send message to group with verification link
await context.bot.send_message(
    chat_id=GROUP_ID,
    text=welcome_text,
    parse_mode='HTML',
    disable_web_page_preview=True
)
```

### **Step 5: Start Timer**
```python
# Add user to pending verification
user_pending_verification[user_id] = username

# Start auto-remove timer
asyncio.create_task(auto_remove_unverified(user_id, username, context))
```

## 📋 **Message Content Breakdown**

### **🎉 Welcome Header**
```
🎉 Welcome to Meta Betties Private Key!
```

### **👋 User Greeting**
```
👋 Hi @{username}, we're excited to have you join our exclusive community!
```

### **🔐 Verification Requirement**
```
🔐 Verification Required
To access this private group, you must verify your NFT ownership.
```

### **🔗 Verification Link**
```
🔗 Click here to verify: Verify NFT Ownership
📋 Or copy this link: https://admin-q2j7.onrender.com/?tg_id={user_id}
```

### **⏰ Time Limit**
```
⏰ Time Limit: You have 5 minutes to complete verification, or you'll be automatically removed.
```

### **💎 Supported Wallets**
```
💎 Supported Wallets: Phantom, Solflare, Backpack, Slope, Glow, Clover, Coinbase, Exodus, Brave, Torus, Trust Wallet, Zerion
```

### **🔄 Multiple Verifications**
```
🔄 Multiple Verifications: You can verify multiple times with the same Telegram ID.
```

## 🎯 **Key Points**

### **✅ What Works**
- **Automatic detection** of new group members
- **Welcome message** with verification link
- **5-minute timer** for verification
- **Auto-removal** if not verified
- **Admin notifications** for new users
- **Multiple verification** support

### **🔧 Configuration**
- **GROUP_ID**: Target Telegram group
- **BOT_TOKEN**: Bot authentication
- **Verification URL**: `https://admin-q2j7.onrender.com/?tg_id={user_id}`

### **📱 User Experience**
1. **User joins group** → Bot automatically sends welcome message
2. **Welcome message** contains verification link
3. **User clicks link** → Opens verification portal
4. **User verifies NFT** → Gets access to private group
5. **If not verified** → Bot removes user after 5 minutes

## 🚀 **Result**

The bot automatically sends a welcome message with an NFT verification link whenever a new user joins the Telegram group. The message includes:

- **Personalized greeting** with username
- **Clear verification instructions**
- **Clickable verification link**
- **Copyable link for manual use**
- **Time limit information**
- **Supported wallet list**
- **Multiple verification support**

**The welcome message is sent automatically to every new group member!** 🎉 