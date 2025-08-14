# 🔧 Welcome Message Troubleshooting

## Problem
When users join the group, the welcome message with NFT verification link is not being sent.

## 🔍 **Debugging Steps**

### **1. Check Bot Configuration**
```bash
# Run the test script
python test_bot_welcome.py
```

### **2. Check Environment Variables**
Make sure these are set in your `.env` file:
```env
TELEGRAM_BOT_TOKEN=your_bot_token_here
TELEGRAM_GROUP_ID=your_group_id_here
ADMIN_CHAT_ID=your_admin_chat_id_here
```

### **3. Check Bot Permissions**
The bot needs these permissions in the group:
- ✅ **Send Messages**
- ✅ **Read Messages**
- ✅ **Add Members** (optional)

## 🛠️ **Common Issues & Solutions**

### **Issue 1: Bot Not Added to Group**
**Symptoms:**
- Bot can't access group
- Error: "Chat not found"

**Solution:**
1. Add bot to the group as admin
2. Give bot "Send Messages" permission
3. Make sure GROUP_ID is correct

### **Issue 2: Wrong GROUP_ID**
**Symptoms:**
- Bot can't find the group
- Messages sent to wrong group

**Solution:**
1. Get correct group ID:
   - Add @userinfobot to your group
   - Send any message
   - Bot will show group ID
2. Update GROUP_ID in environment

### **Issue 3: Bot Server Not Running**
**Symptoms:**
- No welcome messages sent
- Bot doesn't respond to commands

**Solution:**
1. Check if bot server is running:
   ```bash
   python bot-server/bot.py
   ```
2. Look for error messages in console
3. Restart bot server if needed

### **Issue 4: Bot Handler Not Working**
**Symptoms:**
- Bot responds to commands but not to new members

**Solution:**
Check if welcome handler is properly added:
```python
# In bot.py
app.add_handler(MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, welcome))
```

## 🧪 **Testing Steps**

### **Step 1: Test Bot Connection**
```python
# Test if bot can connect
bot = Bot(token=BOT_TOKEN)
bot_info = await bot.get_me()
print(f"Bot: @{bot_info.username}")
```

### **Step 2: Test Group Access**
```python
# Test if bot can access group
chat = await bot.get_chat(GROUP_ID)
print(f"Group: {chat.title}")
```

### **Step 3: Test Welcome Message**
```python
# Test sending welcome message
welcome_text = "🎉 Welcome to the group!"
await bot.send_message(chat_id=GROUP_ID, text=welcome_text)
```

### **Step 4: Test New Member Handler**
1. Add a test user to the group
2. Check if welcome message is sent
3. Check bot console for errors

## 🔧 **Manual Fixes**

### **Fix 1: Restart Bot Server**
```bash
# Stop current bot
Ctrl+C

# Start bot again
python bot-server/bot.py
```

### **Fix 2: Clear Bot Webhook**
```python
# In bot.py, add this before starting:
app.bot.delete_webhook(drop_pending_updates=True)
```

### **Fix 3: Check Bot Logs**
Look for these messages in bot console:
- ✅ "Bot handlers added successfully"
- ✅ "Bot running..."
- ✅ "Processing human member: @username"

### **Fix 4: Test Welcome Function**
Add this test command to bot:
```python
@app.add_handler(CommandHandler("test_welcome", test_welcome))

async def test_welcome(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Test welcome message"""
    await welcome(update, context)
```

## 📋 **Checklist**

### **✅ Bot Setup**
- [ ] Bot token is valid
- [ ] Bot is added to group
- [ ] Bot has "Send Messages" permission
- [ ] GROUP_ID is correct

### **✅ Server Setup**
- [ ] Bot server is running
- [ ] No error messages in console
- [ ] Welcome handler is added
- [ ] Environment variables are set

### **✅ Group Setup**
- [ ] Group allows bot messages
- [ ] Group is not restricted
- [ ] Bot is admin (recommended)

## 🎯 **Quick Test**

Run this command to test the bot:
```bash
python test_bot_welcome.py
```

This will:
1. ✅ Test bot connection
2. ✅ Test group access
3. ✅ Test welcome message
4. ✅ Test admin notification
5. ✅ Show detailed error messages

## 🚀 **Expected Result**

When a user joins the group, you should see:
1. **Bot console:** "Processing human member: @username"
2. **Group message:** Welcome message with verification link
3. **Admin notification:** Instant notification to admin

**If any step fails, the test script will show exactly what's wrong!** 🎯 