#!/usr/bin/env python3
"""
Test Bot Welcome Message - Debug why welcome messages aren't being sent
"""

import os
import asyncio
from dotenv import load_dotenv
from telegram import Bot
from telegram.error import TelegramError

load_dotenv()

async def test_bot_functionality():
    """Test bot functionality and welcome message"""
    
    print("🧪 Testing Bot Welcome Message Functionality")
    print("=" * 60)
    
    # Get environment variables
    BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
    GROUP_ID = os.getenv("TELEGRAM_GROUP_ID")
    ADMIN_CHAT_ID = os.getenv("ADMIN_CHAT_ID")
    
    print(f"🔧 Environment Variables:")
    print(f"  BOT_TOKEN: {'✅ Set' if BOT_TOKEN else '❌ Missing'}")
    print(f"  GROUP_ID: {'✅ Set' if GROUP_ID else '❌ Missing'}")
    print(f"  ADMIN_CHAT_ID: {'✅ Set' if ADMIN_CHAT_ID else '❌ Missing'}")
    
    if not BOT_TOKEN:
        print("❌ BOT_TOKEN is missing! Please set TELEGRAM_BOT_TOKEN in your environment.")
        return
    
    if not GROUP_ID:
        print("❌ GROUP_ID is missing! Please set TELEGRAM_GROUP_ID in your environment.")
        return
    
    # Test bot connection
    print("\n🤖 Testing Bot Connection...")
    try:
        bot = Bot(token=BOT_TOKEN)
        bot_info = await bot.get_me()
        print(f"  ✅ Bot connected successfully!")
        print(f"  📱 Bot Name: {bot_info.first_name}")
        print(f"  🆔 Bot Username: @{bot_info.username}")
        print(f"  🆔 Bot ID: {bot_info.id}")
    except TelegramError as e:
        print(f"  ❌ Bot connection failed: {e}")
        return
    
    # Test group access
    print("\n👥 Testing Group Access...")
    try:
        chat = await bot.get_chat(GROUP_ID)
        print(f"  ✅ Group access successful!")
        print(f"  📝 Group Name: {chat.title}")
        print(f"  🆔 Group ID: {chat.id}")
        print(f"  👥 Group Type: {chat.type}")
        
        # Check if bot is admin
        bot_member = await bot.get_chat_member(GROUP_ID, bot_info.id)
        print(f"  🔑 Bot Status: {bot_member.status}")
        
        # Check permissions based on member type
        if hasattr(bot_member, 'can_send_messages'):
            print(f"  ✉️ Can Send Messages: {bot_member.can_send_messages}")
        elif bot_member.status in ['administrator', 'creator']:
            print(f"  ✉️ Can Send Messages: ✅ (Admin/Creator)")
        else:
            print(f"  ✉️ Can Send Messages: ❓ (Unknown permissions)")
        
    except TelegramError as e:
        print(f"  ❌ Group access failed: {e}")
        print("  💡 Make sure:")
        print("    - Bot is added to the group")
        print("    - Bot has permission to send messages")
        print("    - GROUP_ID is correct")
        return
    
    # Test welcome message
    print("\n📤 Testing Welcome Message...")
    try:
        test_username = "test_user"
        test_user_id = 123456789
        
        # Create verification link
        verify_link = f"https://admin-q2j7.onrender.com/?tg_id={test_user_id}"
        
        # Create welcome message
        welcome_text = f"""🎉 <b>Welcome to Meta Betties Private Key!</b>

👋 Hi @{test_username}, we're excited to have you join our exclusive community!

🔐 <b>Verification Required</b>
To access this private group, you must verify your NFT ownership.

🔗 <b>Click here to verify:</b> <a href="{verify_link}">Verify NFT Ownership</a>

📋 <b>Or copy this link:</b>
<code>{verify_link}</code>

⏰ <b>Time Limit:</b> You have 5 minutes to complete verification, or you'll be automatically removed.

💎 <b>Supported Wallets:</b> Phantom, Solflare, Backpack, Slope, Glow, Clover, Coinbase, Exodus, Brave, Torus, Trust Wallet, Zerion

🔄 <b>Multiple Verifications:</b> You can verify multiple times with the same Telegram ID.

Need help? Contact an admin!"""

        # Send test message
        sent_message = await bot.send_message(
            chat_id=GROUP_ID,
            text=welcome_text,
            parse_mode='HTML',
            disable_web_page_preview=True
        )
        
        print(f"  ✅ Test welcome message sent successfully!")
        print(f"  📄 Message ID: {sent_message.message_id}")
        print(f"  🔗 Verification Link: {verify_link}")
        
    except TelegramError as e:
        print(f"  ❌ Welcome message failed: {e}")
        print("  💡 Possible issues:")
        print("    - Bot doesn't have permission to send messages")
        print("    - HTML parsing error in message")
        print("    - Group settings don't allow bot messages")
    
    # Test admin notification
    if ADMIN_CHAT_ID:
        print("\n📢 Testing Admin Notification...")
        try:
            admin_text = f"""🧪 <b>Bot Test Notification</b>

⏰ <b>Time:</b> {time.strftime('%Y-%m-%d %H:%M:%S')}
🤖 <b>Bot:</b> @{bot_info.username}
👥 <b>Group:</b> {chat.title}

✅ Bot is working correctly!"""

            await bot.send_message(
                chat_id=ADMIN_CHAT_ID,
                text=admin_text,
                parse_mode='HTML'
            )
            print(f"  ✅ Admin notification sent successfully!")
            
        except TelegramError as e:
            print(f"  ❌ Admin notification failed: {e}")
    
    print("\n🎯 Troubleshooting Guide:")
    print("1. ✅ Check if bot is added to the group")
    print("2. ✅ Check if bot has 'Send Messages' permission")
    print("3. ✅ Check if GROUP_ID is correct")
    print("4. ✅ Check if BOT_TOKEN is valid")
    print("5. ✅ Check if bot server is running")
    print("6. ✅ Check bot logs for errors")
    
    print("\n🔧 Common Issues:")
    print("- Bot not added to group")
    print("- Bot doesn't have permission to send messages")
    print("- Wrong GROUP_ID")
    print("- Bot server not running")
    print("- Network connectivity issues")

if __name__ == "__main__":
    import time
    asyncio.run(test_bot_functionality()) 