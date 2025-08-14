#!/usr/bin/env python3
"""
Simple Bot - Telegram bot only (no Flask webhook)
"""

import os
import asyncio
import time
import json
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters, CommandHandler
from dotenv import load_dotenv

load_dotenv()

# Environment variables
BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
GROUP_ID = os.getenv("TELEGRAM_GROUP_ID")
HELIUS_API_KEY = os.getenv("HELIUS_API_KEY", "6873bd5e-0b5d-49c4-a9ab-4e7febfd9cd3")
COLLECTION_ID = os.getenv("COLLECTION_ID", "j7qeFNnpWTbaf5g9sMCxP2zfKrH5QFgE56SuYjQDQi1")
ADMIN_CHAT_ID = os.getenv("ADMIN_CHAT_ID")
ADMIN_NOTIFICATIONS = os.getenv("ADMIN_NOTIFICATIONS", "true").lower() == "true"
WEBHOOK_SERVER_URL = os.getenv("WEBHOOK_SERVER_URL", "https://bot-server-kem4.onrender.com")

# Check if required environment variables are set
if not BOT_TOKEN:
    print("❌ TELEGRAM_BOT_TOKEN not found in environment variables!")
    print("💡 Please set TELEGRAM_BOT_TOKEN in your environment")
    BOT_TOKEN = "test_token"  # Fallback for testing

if not GROUP_ID:
    print("❌ TELEGRAM_GROUP_ID not found in environment variables!")
    print("💡 Please set TELEGRAM_GROUP_ID in your environment")
    GROUP_ID = "test_group"  # Fallback for testing

print(f"🤖 Bot Configuration:")
print(f"  📱 TELEGRAM_BOT_TOKEN: {'✅ Set' if BOT_TOKEN != 'test_token' else '❌ Missing'}")
print(f"  👥 TELEGRAM_GROUP_ID: {'✅ Set' if GROUP_ID != 'test_group' else '❌ Missing'}")
print(f"  📢 ADMIN_CHAT_ID: {'✅ Set' if ADMIN_CHAT_ID else '❌ Missing'}")
print(f"  🔔 ADMIN_NOTIFICATIONS: {'✅ Enabled' if ADMIN_NOTIFICATIONS else '❌ Disabled'}")
print(f"  🌐 WEBHOOK_SERVER_URL: {WEBHOOK_SERVER_URL}")

# Store user states
user_pending_verification = {}
verified_users = {}

async def process_webhook_data():
    """Process webhook data from webhook server"""
    try:
        # Get webhook data from server
        response = requests.get(f"{WEBHOOK_SERVER_URL}/webhook_data", timeout=5)
        
        if response.status_code == 200:
            data = response.json()
            
            if data.get("status") == "no_data":
                return
            
            # Process the webhook data
            tg_id = data.get('tg_id')
            has_nft = data.get('has_nft')
            username = data.get('username', f'user_{tg_id}')
            wallet_address = data.get('wallet_address', 'N/A')
            nft_count = data.get('nft_count', 0)
            
            print(f"🔍 Processing webhook data:")
            print(f"  👤 User ID: {tg_id}")
            print(f"  👤 Username: {username}")
            print(f"  🎨 Has NFT: {has_nft}")
            print(f"  💎 NFT Count: {nft_count}")
            print(f"  💰 Wallet: {wallet_address}")
            
            # Immediately remove from pending verification
            if tg_id in user_pending_verification:
                print(f"⏰ Removing @{username} from pending verification (webhook received)")
                del user_pending_verification[tg_id]
            
            if has_nft:
                # User has NFT - success
                try:
                    # Unban user first
                    await app.bot.unban_chat_member(GROUP_ID, tg_id)
                    print(f"✅ Unbanned user @{username} (ID: {tg_id})")
                except Exception as unban_error:
                    print(f"⚠️ Could not unban user (may not be banned): {unban_error}")
                
                # Send success message
                success_message = f"""✅ <b>Verification Successful!</b>

🎉 Congratulations @{username}! 

💎 You have been verified as an NFT holder.

🔐 <b>Access Granted:</b> You should now have access to this private group.

🔄 <b>Multiple Verifications:</b> You can verify again anytime with the same Telegram ID.

Welcome to the Meta Betties community! 🚀"""

                await app.bot.send_message(
                    chat_id=GROUP_ID,
                    text=success_message,
                    parse_mode='HTML'
                )
                
                # Log successful verification
                log_entry = {
                    "timestamp": time.time(),
                    "user_id": tg_id,
                    "username": username,
                    "status": "verified",
                    "reason": "nft_verified",
                    "nft_count": nft_count,
                    "wallet_address": wallet_address
                }
                
                with open("analytics.json", "a") as f:
                    f.write(json.dumps(log_entry) + "\n")
                
                print(f"✅ User @{username} (ID: {tg_id}) verified successfully")
                
                # Track as verified
                verified_users[tg_id] = {
                    "username": username,
                    "verified_at": time.time(),
                    "nft_count": nft_count,
                    "wallet_address": wallet_address
                }
                
                # Admin notification
                await notify_admin_verification_success(tg_id, username, nft_count, wallet_address)
                
            else:
                # User has no NFT - remove them
                try:
                    # Send removal message
                    removal_message = f"""❌ <b>Verification Failed</b>

😔 Sorry @{username}, your verification was unsuccessful.

🚫 <b>Access Denied:</b> You do not have the required NFT to access this private group.

💎 <b>Requirements:</b> You must own at least one NFT to join this group.

🔄 <b>Try Again:</b> You can try again anytime by rejoining the group.

You will be removed from the group now."""

                    await app.bot.send_message(
                        chat_id=GROUP_ID,
                        text=removal_message,
                        parse_mode='HTML'
                    )
                    
                    # Remove user from group
                    await app.bot.ban_chat_member(GROUP_ID, tg_id)
                    await app.bot.unban_chat_member(GROUP_ID, tg_id)
                    print(f"❌ Removed @{username} (ID: {tg_id}) - no required NFT")
                    
                    log_entry = {
                        "timestamp": time.time(),
                        "user_id": tg_id,
                        "username": username,
                        "status": "removed",
                        "reason": "no_nft",
                        "wallet_address": wallet_address
                    }
                    
                    with open("analytics.json", "a") as f:
                        f.write(json.dumps(log_entry) + "\n")
                    
                    # Admin notification
                    await notify_admin_verification_failed(tg_id, username, "No NFTs found", wallet_address)
                    
                except Exception as e:
                    print(f"❌ Error removing user: {e}")
            
            # Clear webhook data after processing
            try:
                requests.post(f"{WEBHOOK_SERVER_URL}/clear_webhook_data", timeout=5)
                print("✅ Webhook data cleared")
            except Exception as e:
                print(f"⚠️ Could not clear webhook data: {e}")
                
    except Exception as e:
        print(f"❌ Error processing webhook data: {e}")

async def check_webhook_periodically():
    """Check for webhook data periodically"""
    while True:
        try:
            await process_webhook_data()
            await asyncio.sleep(5)  # Check every 5 seconds
        except Exception as e:
            print(f"❌ Error in webhook check: {e}")
            await asyncio.sleep(10)  # Wait longer on error

async def notify_admin_verification_success(user_id: int, username: str, nft_count: int, wallet_address: str = None):
    """Notify admin about successful verification"""
    if not ADMIN_NOTIFICATIONS or not ADMIN_CHAT_ID:
        return
    
    try:
        notification_text = f"""✅ <b>Verification Success</b>

👤 <b>User:</b> @{username} (ID: {user_id})
💎 <b>NFTs Found:</b> {nft_count}
💰 <b>Wallet:</b> {wallet_address[:8]}...{wallet_address[-8:] if wallet_address else 'N/A'}
⏰ <b>Time:</b> {time.strftime('%Y-%m-%d %H:%M:%S')}

🎉 User has been granted access to the group!"""

        await app.bot.send_message(
            chat_id=ADMIN_CHAT_ID,
            text=notification_text,
            parse_mode='HTML'
        )
        print(f"📢 Admin notified: {username} verification success")
        
    except Exception as e:
        print(f"❌ Error notifying admin: {e}")

async def notify_admin_verification_failed(user_id: int, username: str, reason: str, wallet_address: str = None):
    """Notify admin about failed verification"""
    if not ADMIN_NOTIFICATIONS or not ADMIN_CHAT_ID:
        return
    
    try:
        notification_text = f"""❌ <b>Verification Failed</b>

👤 <b>User:</b> @{username} (ID: {user_id})
🚫 <b>Reason:</b> {reason}
💰 <b>Wallet:</b> {wallet_address[:8]}...{wallet_address[-8:] if wallet_address else 'N/A'}
⏰ <b>Time:</b> {time.strftime('%Y-%m-%d %H:%M:%S')}

😔 User has been removed from the group."""

        await app.bot.send_message(
            chat_id=ADMIN_CHAT_ID,
            text=notification_text,
            parse_mode='HTML'
        )
        print(f"📢 Admin notified: {username} verification failed")
        
    except Exception as e:
        print(f"❌ Error notifying admin: {e}")

async def notify_admin_user_joined(user_id: int, username: str):
    """Notify admin about new user joining"""
    if not ADMIN_NOTIFICATIONS or not ADMIN_CHAT_ID:
        return
    
    try:
        notification_text = f"""👋 <b>New User Joined</b>

👤 <b>User:</b> @{username} (ID: {user_id})
⏰ <b>Time:</b> {time.strftime('%Y-%m-%d %H:%M:%S')}
⏳ <b>Status:</b> Pending verification (10 min timer started)"""

        await app.bot.send_message(
            chat_id=ADMIN_CHAT_ID,
            text=notification_text,
            parse_mode='HTML'
        )
        print(f"📢 Admin notified: {username} joined group")
        
    except Exception as e:
        print(f"❌ Error notifying admin: {e}")

async def auto_remove_unverified(user_id, username, context):
    """Auto-remove user if not verified within 10 minutes"""
    await asyncio.sleep(600)  # 10 minutes
    
    if user_id in user_pending_verification:
        try:
            await context.bot.ban_chat_member(chat_id=GROUP_ID, user_id=user_id)
            await context.bot.unban_chat_member(chat_id=GROUP_ID, user_id=user_id)
            
            # Log removal
            log_entry = {
                "timestamp": time.time(),
                "user_id": user_id,
                "username": username,
                "status": "removed",
                "reason": "timeout"
            }
            
            with open("analytics.json", "a") as f:
                f.write(json.dumps(log_entry) + "\n")
            
            print(f"❌ Removed @{username} (ID: {user_id}) - verification timeout")
            del user_pending_verification[user_id]
            
            # Admin notification for timeout
            await notify_admin_verification_failed(user_id, username, "Verification timeout (10 minutes)", None)
            
        except Exception as e:
            print(f"Error removing user: {e}")

async def welcome(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Welcome new members and send verification link"""
    try:
        print(f"🔔 Welcome function triggered")
        
        # Check if this is the correct group
        if str(update.message.chat.id) != str(GROUP_ID):
            print(f"❌ Wrong group - expected {GROUP_ID}, got {update.message.chat.id}")
            return
        
        if not update.message.new_chat_members:
            print("❌ No new chat members found")
            return
        
        for new_member in update.message.new_chat_members:
            print(f"👤 Processing new member: {new_member.username or new_member.first_name} (ID: {new_member.id})")
            
            if new_member.is_bot:
                print("🤖 Skipping bot member")
                continue
                
            user_id = new_member.id
            username = new_member.username or new_member.first_name
            
            print(f"✅ Processing human member: @{username} (ID: {user_id})")
            
            # Allow multiple verifications - remove old pending status
            if user_id in user_pending_verification:
                print(f"🔄 User @{username} already pending - allowing new verification")
                del user_pending_verification[user_id]
            
            # Create verification link
            verify_link = f"https://admin-q2j7.onrender.com/?tg_id={user_id}"
            print(f"🔗 Verification link: {verify_link}")

            try:
                print(f"📤 Sending welcome message to group {GROUP_ID}")
                
                # Create welcome message
                welcome_text = f"""🎉 <b>Welcome to Meta Betties Private Key!</b>

👋 Hi @{username}, we're excited to have you join our exclusive community!

🔐 <b>Verification Required</b>
To access this private group, you must verify your NFT ownership.

🔗 <b>Click here to verify:</b> <a href="{verify_link}">Verify NFT Ownership</a>

📋 <b>Or copy this link:</b>
<code>{verify_link}</code>

⏰ <b>Time Limit:</b> You have 10 minutes to complete verification, or you'll be automatically removed.

💎 <b>Supported Wallets:</b> Phantom, Solflare, Backpack, Slope, Glow, Clover, Coinbase, Exodus, Brave, Torus, Trust Wallet, Zerion

🔄 <b>Multiple Verifications:</b> You can verify multiple times with the same Telegram ID.

Need help? Contact an admin!"""

                # Send message to group
                sent_message = await context.bot.send_message(
                    chat_id=GROUP_ID,
                    text=welcome_text,
                    parse_mode='HTML',
                    disable_web_page_preview=True
                )
                
                print(f"✅ Welcome message sent successfully to @{username}")

                # Add user to pending verification
                user_pending_verification[user_id] = username
                print(f"⏰ Started 10-minute timer for @{username}")
                print(f"📊 Pending verifications: {len(user_pending_verification)}")
                
                # Start auto-remove timer
                asyncio.create_task(auto_remove_unverified(user_id, username, context))
                
                # Admin notification for new user
                asyncio.create_task(notify_admin_user_joined(user_id, username))
                
            except Exception as e:
                print(f"❌ Error sending message to group: {e}")
                print(f"🔍 Error details: {type(e).__name__}: {str(e)}")
                import traceback
                traceback.print_exc()
                
    except Exception as e:
        print(f"❌ Critical error in welcome function: {e}")
        print(f"🔍 Error details: {type(e).__name__}: {str(e)}")
        import traceback
        traceback.print_exc()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /start command"""
    await update.message.reply_text("✅ Bot is active!")

async def test_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Test function to check if bot is responding"""
    try:
        user = update.effective_user
        chat = update.effective_chat
        
        print(f"🧪 Test message received from @{user.username or user.first_name}")
        print(f"📝 Chat ID: {chat.id}")
        print(f"👤 User ID: {user.id}")
        
        # Send test response
        await update.message.reply_text("✅ Bot is working! Test message received.")
        
        # Also send to group if it's a group chat
        if chat.type in ['group', 'supergroup']:
            await context.bot.send_message(
                chat_id=chat.id,
                text=f"🧪 Test: Bot is responding to messages in this group!"
            )
            
    except Exception as e:
        print(f"❌ Error in test_message: {e}")
        await update.message.reply_text("❌ Bot test failed. Check logs.")

async def analytics(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /analytics command"""
    user = update.effective_user
    chat = update.effective_chat
    
    # Only allow group admins
    member = await context.bot.get_chat_member(chat.id, user.id)
    if member.status not in ["administrator", "creator"]:
        await update.message.reply_text("❌ Only group admins can use this command.")
        return
    
    try:
        with open("analytics.json") as f:
            lines = f.readlines()
        total_verified = sum(1 for l in lines if json.loads(l)["status"] == "verified")
        total_removed = sum(1 for l in lines if json.loads(l)["status"] == "removed")
        recent = [json.loads(l) for l in lines[-10:]]
        msg = f"📊 Group Analytics:\nTotal verified: {total_verified}\nTotal removed: {total_removed}\n\nRecent activity:\n"
        for entry in recent:
            from datetime import datetime
            t = datetime.fromtimestamp(entry["timestamp"]).strftime('%Y-%m-%d %H:%M')
            msg += f"@{entry['username']} - {entry['status']} ({t})\n"
        await update.message.reply_text(msg)
    except Exception as e:
        await update.message.reply_text(f"Error reading analytics: {e}")

async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle errors in the bot"""
    print(f"❌ Exception while handling an update: {context.error}")
    print(f"🔍 Error details: {type(context.error).__name__}: {str(context.error)}")
    import traceback
    traceback.print_exc()

# Create app and add handlers
app = ApplicationBuilder().token(BOT_TOKEN).build()

print("🤖 Setting up bot handlers...")

# Add handlers
app.add_handler(MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, welcome))
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("analytics", analytics))
app.add_handler(CommandHandler("test", test_message))

# Add message handler for all text messages
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, test_message))

print("✅ Bot handlers added successfully")

# Add error handling
app.add_error_handler(error_handler)
print("✅ Error handler added successfully")

print("🤖 Bot running...")

# Start the bot
try:
    print("🤖 Starting bot...")
    
    # Clear any pending updates first
    try:
        app.bot.delete_webhook(drop_pending_updates=True)
        print("✅ Webhook cleared successfully")
    except Exception as e:
        print(f"⚠️ Warning: Could not clear webhook: {e}")
    
    # Check if bot is already running
    try:
        bot_info = app.bot.get_me()
        print(f"✅ Bot info retrieved: @{bot_info.username}")
    except Exception as e:
        print(f"❌ Error getting bot info: {e}")
        print("💡 This might indicate another instance is running")
        import sys
        sys.exit(1)
    
    print("🔄 Starting polling with webhook checking...")
    
    # Start webhook checking task
    asyncio.create_task(check_webhook_periodically())
    print("✅ Webhook checking task started")
    
    app.run_polling(
        drop_pending_updates=True,
        allowed_updates=["message", "callback_query"]
    )
    
except KeyboardInterrupt:
    print("\n⏹️ Bot stopped by user")
except Exception as e:
    print(f"❌ Error starting bot: {e}")
    print("💡 Please make sure only one bot instance is running.")
    print("💡 Try stopping all Python processes and restart.")
    import traceback
    traceback.print_exc() 