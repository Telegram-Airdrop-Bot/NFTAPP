import requests
from typing import Dict, Optional, List
from telegram import Update, ChatMemberUpdated, ChatMember
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ConversationHandler,
    ContextTypes,
    filters,
    ChatMemberHandler,
)
import asyncio
import json
from datetime import datetime, timedelta
from flask import Flask, request, jsonify
from threading import Thread

# Flask app for webhook
webhook_app = Flask(__name__)

# Configuration
HELIUS_API_KEY = "6873bd5e-0b5d-49c4-a9ab-4e7febfd9cd3"  # Replace with your Helius API key
HELIUS_API_URL = "https://api.helius.xyz/v0"  # Keep v0 for balance
DAS_API_URL = "https://mainnet.helius-rpc.com"  # DAS API endpoint
TELEGRAM_BOT_TOKEN = "7045327114:AAE_l_8xkgQHKuSpQLWmgkjiuRdFMxwrI8E"  # Replace with your Telegram bot token
LAMPORTS_PER_SOL = 1_000_000_000  # Conversion factor for SOL (1 SOL = 1e9 lamports)

# Default collection ID (Meta Betties)
DEFAULT_COLLECTION_ID = "j7qeFNnpWTbaf5g9sMCxP2zfKrH5QFgE56SuYjQDQi1"

# Verification settings
VERIFICATION_LINK = "https://your-verification-site.com/verify"  # Replace with your verification site
MIN_NFT_REQUIRED = 1  # Minimum NFTs required to stay in group
VERIFICATION_TIMEOUT = 300  # 5 minutes timeout for verification

# Conversation states
WALLET_ADDRESS = 1
COLLECTION_ID = 2

# Cache for API responses to avoid repeated calls
wallet_cache = {}

# Store pending verifications
pending_verifications = {}

# Global bot application reference for webhook
bot_application = None

@webhook_app.route('/verify', methods=['POST'])
def verify_webhook():
    """
    Webhook endpoint to receive verification data from verification website.
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No data received'}), 400
        
        verification_id = data.get('verification_id')
        wallet_address = data.get('wallet_address')
        nft_count = data.get('nft_count', 0)
        verified = data.get('verified', False)
        
        if not verification_id or not wallet_address:
            return jsonify({'error': 'Missing required fields'}), 400
        
        print(f"🔗 Webhook received: {verification_id} - {wallet_address} - {nft_count} NFTs")
        
        # Process verification asynchronously
        if bot_application:
            asyncio.run_coroutine_threadsafe(
                process_verification_webhook(verification_id, wallet_address, nft_count, verified),
                bot_application.loop
            )
        
        return jsonify({'success': True, 'message': 'Verification processed'}), 200
        
    except Exception as e:
        print(f"❌ Webhook error: {e}")
        return jsonify({'error': str(e)}), 500

async def process_verification_webhook(verification_id: str, wallet_address: str, nft_count: int, verified: bool):
    """
    Process verification data received from webhook.
    """
    try:
        if verification_id not in pending_verifications:
            print(f"❌ Verification ID {verification_id} not found in pending verifications")
            return
        
        verification_data = pending_verifications[verification_id]
        user_id = verification_data['user_id']
        chat_id = verification_data['chat_id']
        username = verification_data['username']
        
        print(f"✅ Processing verification for {username} (User ID: {user_id})")
        
        if verified and nft_count >= MIN_NFT_REQUIRED:
            # User is verified - update status
            verification_data['verified'] = True
            verification_data['wallet_address'] = wallet_address
            verification_data['nft_count'] = nft_count
            
            # Send success message
            await bot_application.bot.send_message(
                chat_id=chat_id,
                text=f"✅ *Verification Successful!*\n\n"
                     f"Welcome {username}! 🎉\n"
                     f"Your wallet has {nft_count} NFT(s).\n"
                     f"You can now stay in the group!"
            )
            
            print(f"✅ User {username} verified successfully with {nft_count} NFTs")
            
        else:
            # User failed verification - remove from group
            try:
                await bot_application.bot.ban_chat_member(
                    chat_id=chat_id,
                    user_id=user_id,
                    until_date=datetime.now() + timedelta(seconds=30)
                )
                
                await bot_application.bot.send_message(
                    chat_id=chat_id,
                    text=f"❌ *Verification Failed*\n\n"
                         f"User {username} was removed.\n"
                         f"Reason: Insufficient NFTs (found: {nft_count}, required: {MIN_NFT_REQUIRED})"
                )
                
                print(f"❌ User {username} removed - insufficient NFTs ({nft_count})")
                
            except Exception as e:
                print(f"❌ Error removing user {username}: {e}")
        
        # Clean up verification data
        del pending_verifications[verification_id]
        
    except Exception as e:
        print(f"❌ Error processing verification webhook: {e}")

def run_webhook_server():
    """
    Run the Flask webhook server in a separate thread.
    """
    webhook_app.run(host='0.0.0.0', port=5000, debug=False)

async def handle_chat_member_update(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Handle when a user joins or leaves the group.
    """
    result = False
    
    # Check if this is a chat member update
    if update.chat_member:
        chat_member = update.chat_member
        user = chat_member.new_chat_member.user
        chat = update.effective_chat
        
        # Check if user joined the group
        if (chat_member.old_chat_member.status == ChatMember.LEFT and 
            chat_member.new_chat_member.status in [ChatMember.MEMBER, ChatMember.ADMINISTRATOR]):
            
            print(f"👋 User {user.id} ({user.username or user.first_name}) joined group {chat.title}")
            await handle_user_joined(update, context, user, chat)
            result = True
            
        # Check if user left the group
        elif (chat_member.old_chat_member.status in [ChatMember.MEMBER, ChatMember.ADMINISTRATOR] and 
              chat_member.new_chat_member.status == ChatMember.LEFT):
            
            print(f"👋 User {user.id} ({user.username or user.first_name}) left group {chat.title}")
            await handle_user_left(update, context, user, chat)
            result = True
    
    return result

async def handle_user_joined(update: Update, context: ContextTypes.DEFAULT_TYPE, user, chat) -> None:
    """
    Handle when a user joins the group - send welcome message with verification link.
    """
    try:
        # Create verification session
        verification_id = f"{user.id}_{chat.id}_{datetime.now().timestamp()}"
        pending_verifications[verification_id] = {
            'user_id': user.id,
            'chat_id': chat.id,
            'username': user.username or user.first_name,
            'joined_at': datetime.now(),
            'verified': False
        }
        
        # Send welcome message with verification link
        welcome_message = (
            f"🎉 *Welcome to {chat.title}!* 🎉\n\n"
            f"Hi {user.first_name}! 👋\n\n"
            "🔐 *NFT Verification Required*\n"
            "To stay in this group, you need to verify that you own at least 1 NFT.\n\n"
            f"📋 *Verification Steps:*\n"
            f"1️⃣ Click the verification link below\n"
            f"2️⃣ Connect your Solana wallet\n"
            f"3️⃣ We'll check if you have at least {MIN_NFT_REQUIRED} NFT\n"
            f"4️⃣ If verified, you'll stay in the group\n\n"
            f"⏰ *Time Limit:* {VERIFICATION_TIMEOUT//60} minutes\n\n"
            f"🔗 [Click Here to Verify]({VERIFICATION_LINK}?id={verification_id})\n\n"
            f"❓ Need help? Contact an admin."
        )
        
        await context.bot.send_message(
            chat_id=chat.id,
            text=welcome_message,
            parse_mode='Markdown',
            disable_web_page_preview=True
        )
        
        # Schedule automatic removal if not verified within timeout
        context.job_queue.run_once(
            check_verification_timeout,
            VERIFICATION_TIMEOUT,
            data={'verification_id': verification_id, 'user_id': user.id, 'chat_id': chat.id}
        )
        
        print(f"✅ Welcome message sent to {user.username or user.first_name} with verification link")
        
    except Exception as e:
        print(f"❌ Error handling user join: {e}")

async def handle_user_left(update: Update, context: ContextTypes.DEFAULT_TYPE, user, chat) -> None:
    """
    Handle when a user leaves the group - clean up verification data.
    """
    try:
        # Remove any pending verifications for this user
        verification_ids_to_remove = []
        for vid, data in pending_verifications.items():
            if data['user_id'] == user.id and data['chat_id'] == chat.id:
                verification_ids_to_remove.append(vid)
        
        for vid in verification_ids_to_remove:
            del pending_verifications[vid]
        
        print(f"🧹 Cleaned up verification data for {user.username or user.first_name}")
        
    except Exception as e:
        print(f"❌ Error handling user leave: {e}")

async def check_verification_timeout(context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Check if verification has timed out and remove user if not verified.
    """
    job = context.job
    data = job.data
    verification_id = data['verification_id']
    user_id = data['user_id']
    chat_id = data['chat_id']
    
    if verification_id in pending_verifications:
        verification_data = pending_verifications[verification_id]
        
        if not verification_data['verified']:
            try:
                # Remove user from group
                await context.bot.ban_chat_member(
                    chat_id=chat_id,
                    user_id=user_id,
                    until_date=datetime.now() + timedelta(seconds=30)  # Ban for 30 seconds (removes immediately)
                )
                
                # Send removal message
                await context.bot.send_message(
                    chat_id=chat_id,
                    text=f"⏰ *Verification Timeout*\n\n"
                         f"User verification timed out and was removed from the group.\n"
                         f"They can rejoin and try again."
                )
                
                print(f"⏰ User {verification_data['username']} removed due to verification timeout")
                
            except Exception as e:
                print(f"❌ Error removing user due to timeout: {e}")
        
        # Clean up verification data
        del pending_verifications[verification_id]

async def verify_wallet_nft_ownership(wallet_address: str, user_id: int, chat_id: int, verification_id: str) -> bool:
    """
    Verify if a wallet has the required number of NFTs.
    """
    try:
        # Get NFTs for the wallet
        nfts = get_wallet_nfts_by_collection(wallet_address)
        
        if nfts is not None and len(nfts) >= MIN_NFT_REQUIRED:
            # Update verification status
            if verification_id in pending_verifications:
                pending_verifications[verification_id]['verified'] = True
                pending_verifications[verification_id]['wallet_address'] = wallet_address
                pending_verifications[verification_id]['nft_count'] = len(nfts)
            
            print(f"✅ User {user_id} verified with {len(nfts)} NFTs")
            return True
        else:
            print(f"❌ User {user_id} failed verification - insufficient NFTs")
            return False
            
    except Exception as e:
        print(f"❌ Error verifying wallet: {e}")
        return False

async def handle_verification_webhook(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Handle verification webhook from external verification site.
    This would be called when user completes verification on external site.
    """
    try:
        # This would receive data from your verification website
        # Format: {"verification_id": "xxx", "wallet_address": "xxx", "user_id": 123}
        data = update.message.text  # In real implementation, this would be webhook data
        
        # Parse verification data (this is a simplified example)
        # In real implementation, you'd get this from webhook POST data
        verification_data = json.loads(data)
        verification_id = verification_data.get('verification_id')
        wallet_address = verification_data.get('wallet_address')
        user_id = verification_data.get('user_id')
        
        if verification_id in pending_verifications:
            verification_info = pending_verifications[verification_id]
            
            # Verify NFT ownership
            is_verified = await verify_wallet_nft_ownership(wallet_address, user_id, verification_info['chat_id'], verification_id)
            
            if is_verified:
                # Send success message
                await context.bot.send_message(
                    chat_id=verification_info['chat_id'],
                    text=f"✅ *Verification Successful!*\n\n"
                         f"Welcome {verification_info['username']}! 🎉\n"
                         f"Your wallet has {verification_info['nft_count']} NFT(s).\n"
                         f"You can now stay in the group!"
                )
            else:
                # Remove user from group
                await context.bot.ban_chat_member(
                    chat_id=verification_info['chat_id'],
                    user_id=user_id,
                    until_date=datetime.now() + timedelta(seconds=30)
                )
                
                await context.bot.send_message(
                    chat_id=verification_info['chat_id'],
                    text=f"❌ *Verification Failed*\n\n"
                         f"User {verification_info['username']} was removed.\n"
                         f"Reason: Insufficient NFTs (required: {MIN_NFT_REQUIRED})"
                )
        
    except Exception as e:
        print(f"❌ Error handling verification webhook: {e}")

def get_wallet_balance(wallet_address: str) -> Optional[float]:
    """
    Fetch the SOL balance of a wallet using Helius API.
    Args:
        wallet_address: The Solana wallet address.
    Returns:
        SOL balance as a float, or None if the request fails.
    """
    # Check cache first
    if wallet_address in wallet_cache and 'balance' in wallet_cache[wallet_address]:
        print(f"💰 Using cached SOL balance for {wallet_address}")
        return wallet_cache[wallet_address]['balance']
    
    url = f"{HELIUS_API_URL}/addresses/{wallet_address}/balances?api-key={HELIUS_API_KEY}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        balance = data.get("nativeBalance", 0) / LAMPORTS_PER_SOL
        
        # Cache the result
        if wallet_address not in wallet_cache:
            wallet_cache[wallet_address] = {}
        wallet_cache[wallet_address]['balance'] = balance
        
        return balance
    except requests.RequestException as e:
        print(f"Error fetching wallet balance: {e}")
        return None

def get_wallet_tokens(wallet_address: str) -> Optional[List[Dict]]:
    """
    Fetch token holdings of a wallet using Helius DAS API.
    Args:
        wallet_address: The Solana wallet address.
    Returns:
        List of token holdings, or None if the request fails.
    """
    # Check cache first
    if wallet_address in wallet_cache and 'tokens' in wallet_cache[wallet_address]:
        print(f"🪙 Using cached tokens for {wallet_address}")
        return wallet_cache[wallet_address]['tokens']
    
    # Using Helius DAS API for tokens - simpler approach
    url = f"{DAS_API_URL}/?api-key={HELIUS_API_KEY}"
    payload = {
        "jsonrpc": "2.0",
        "id": "my-id",
        "method": "searchAssets",
        "params": {
            "ownerAddress": wallet_address
        }
    }
    
    print(f"🔍 Fetching tokens for wallet: {wallet_address}")
    
    try:
        response = requests.post(url, json=payload)
        print(f"📊 Response Status: {response.status_code}")
        
        response.raise_for_status()
        data = response.json()
        
        # Check for error in response
        if "error" in data:
            print(f"❌ API Error: {data['error']}")
            return None
        
        if "result" in data and "items" in data["result"]:
            all_items = data["result"]["items"]
            print(f"📦 Total items received: {len(all_items)}")
            
            # Log first few items for debugging
            for i, item in enumerate(all_items[:3]):
                token_standard = item.get("content", {}).get("metadata", {}).get("token_standard", "Unknown")
                interface = item.get("interface", "Unknown")
                print(f"  Item {i+1}: token_standard = {token_standard}, interface = {interface}")
            
            # Filter for fungible tokens - try different possible values
            tokens = [item for item in all_items 
                     if item.get("content", {}).get("metadata", {}).get("token_standard") in ["Fungible", "fungible", "FUNGIBLE"]]
            
            print(f"🪙 Fungible tokens found: {len(tokens)}")
            
            # Cache the result
            if wallet_address not in wallet_cache:
                wallet_cache[wallet_address] = {}
            wallet_cache[wallet_address]['tokens'] = tokens
            
            return tokens
        else:
            print(f"❌ No 'result' or 'items' in response")
            return []
    except requests.RequestException as e:
        print(f"❌ Error fetching token holdings: {e}")
        return None

def get_wallet_nfts_by_collection(wallet_address: str, collection_id: str = None) -> Optional[List[Dict]]:
    """
    Fetch NFTs owned by a wallet for a specific collection using Helius DAS API.
    Args:
        wallet_address: The Solana wallet address.
        collection_id: The collection ID to filter by (optional).
    Returns:
        List of NFTs, or None if the request fails.
    """
    # Check cache first
    cache_key = f"{wallet_address}_{collection_id}" if collection_id else wallet_address
    if cache_key in wallet_cache and 'nfts' in wallet_cache[cache_key]:
        print(f"🎨 Using cached NFTs for {wallet_address}")
        return wallet_cache[cache_key]['nfts']
    
    # Using Helius DAS API for NFTs - simpler approach
    url = f"{DAS_API_URL}/?api-key={HELIUS_API_KEY}"
    payload = {
        "jsonrpc": "2.0",
        "id": "my-id",
        "method": "searchAssets",
        "params": {
            "ownerAddress": wallet_address
        }
    }
    
    print(f"🎨 Fetching NFTs for wallet: {wallet_address}")
    if collection_id:
        print(f"🎯 Filtering by collection: {collection_id}")
    
    try:
        response = requests.post(url, json=payload)
        print(f"📊 Response Status: {response.status_code}")
        
        response.raise_for_status()
        data = response.json()
        
        # Check for error in response
        if "error" in data:
            print(f"❌ API Error: {data['error']}")
            return None
        
        if "result" in data and "items" in data["result"]:
            all_items = data["result"]["items"]
            print(f"📦 Total items received: {len(all_items)}")
            
            # Log first few items for debugging
            for i, item in enumerate(all_items[:3]):
                token_standard = item.get("content", {}).get("metadata", {}).get("token_standard", "Unknown")
                interface = item.get("interface", "Unknown")
                grouping = item.get("grouping", [])
                collection = grouping[0].get("group_value", "Unknown") if grouping and len(grouping) > 0 else "Unknown"
                print(f"  Item {i+1}: token_standard = {token_standard}, interface = {interface}, collection = {collection}")
            
            # Improved NFT filtering - check multiple criteria
            nfts = []
            for item in all_items:
                # Check if it's an NFT based on multiple criteria
                is_nft = False
                
                # Criterion 1: Token standard
                token_standard = item.get("content", {}).get("metadata", {}).get("token_standard", "")
                if token_standard in ["NonFungible", "non-fungible", "NONFUNGIBLE"]:
                    is_nft = True
                
                # Criterion 2: Interface type
                interface = item.get("interface", "")
                if interface in ["V1_NFT", "MplCoreAsset"]:
                    is_nft = True
                
                # Criterion 3: Has files or name/symbol
                content = item.get("content", {})
                files = content.get("files", [])
                metadata = content.get("metadata", {})
                name = metadata.get("name", "")
                symbol = metadata.get("symbol", "")
                
                if files or name or symbol:
                    is_nft = True
                
                # Criterion 4: Check for NFT keywords in description
                description = metadata.get("description", "")
                if any(keyword in description.lower() for keyword in ["nft", "non-fungible", "token"]):
                    is_nft = True
                
                if is_nft:
                    nfts.append(item)
            
            # If collection_id is specified, filter by collection
            if collection_id:
                filtered_nfts = []
                for nft in nfts:
                    grouping = nft.get("grouping", [])
                    if grouping and len(grouping) > 0:
                        nft_collection = grouping[0].get("group_value")
                        if nft_collection == collection_id:
                            filtered_nfts.append(nft)
                nfts = filtered_nfts
                print(f"🎨 NFTs in collection {collection_id}: {len(nfts)}")
            else:
                print(f"🎨 Non-fungible tokens found: {len(nfts)}")
            
            # Cache the result
            if cache_key not in wallet_cache:
                wallet_cache[cache_key] = {}
            wallet_cache[cache_key]['nfts'] = nfts
            
            return nfts
        else:
            print(f"❌ No 'result' or 'items' in response")
            return []
    except requests.RequestException as e:
        print(f"❌ Error fetching NFTs: {e}")
        return None

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """
    Start the conversation and prompt for a wallet address.
    """
    await update.message.reply_text(
        "🌟 Welcome! Send me any Solana wallet address to check its SOL, tokens, and NFTs.\n\n"
        "You can also specify a collection ID to check for specific NFTs!\n\n"
        "Format: `wallet_address` or `wallet_address:collection_id`\n\n"
        "Example: `EFwPVHhY6vH64MsMDx9ub8Edn4ktYYBcgqNYki1R3rmE`\n"
        "Example: `EFwPVHhY6vH64MsMDx9ub8Edn4ktYYBcgqNYki1R3rmE:j7qeFNnpWTbaf5g9sMCxP2zfKrH5QFgE56SuYjQDQi1`"
    )
    return WALLET_ADDRESS

async def handle_wallet_address(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """
    Handle the wallet address provided by the user and display results.
    """
    user_input = update.message.text.strip()
    
    # Parse wallet address and collection ID
    if ":" in user_input:
        parts = user_input.split(":", 1)
        wallet_address = parts[0].strip()
        collection_id = parts[1].strip()
    else:
        wallet_address = user_input
        collection_id = None

    # Basic validation (Solana addresses are typically 32-44 characters)
    if len(wallet_address) < 32 or len(wallet_address) > 44:
        await update.message.reply_text(
            "❌ Invalid Solana wallet address. Please provide a valid address."
        )
        return WALLET_ADDRESS

    print(f"\n🔍 Processing wallet: {wallet_address}")
    if collection_id:
        print(f"🎯 Collection ID: {collection_id}")
    
    # Fetch wallet data
    sol_balance = get_wallet_balance(wallet_address)
    tokens = get_wallet_tokens(wallet_address)
    nfts = get_wallet_nfts_by_collection(wallet_address, collection_id)

    print(f"💰 SOL Balance: {sol_balance}")
    print(f"🪙 Tokens result: {tokens}")
    print(f"🎨 NFTs result: {nfts}")
    
    if tokens is not None:
        print(f"🪙 Token count: {len(tokens)}")
    if nfts is not None:
        print(f"🎨 NFT count: {len(nfts)}")

    # Prepare response
    response = f"📊 *Wallet Analysis for {wallet_address}* 📊\n\n"
    
    if collection_id:
        response += f"🎯 *Collection Filter: {collection_id}*\n\n"

    # SOL Balance
    response += "💰 *SOL Balance*\n"
    if sol_balance is not None:
        response += f"  {sol_balance:.4f} SOL\n"
    else:
        response += "  Failed to fetch SOL balance.\n"

    # Token Holdings - Only show count
    response += "\n🪙 *Tokens*\n"
    if tokens:
        response += f"  {len(tokens)} token(s) found\n"
    else:
        response += "  No tokens found or failed to fetch token data.\n"

    # NFTs - Only show count
    response += "\n🎨 *NFTs*\n"
    if collection_id:
        response += f"  {len(nfts) if nfts else 0} NFT(s) found in collection\n"
    else:
        response += f"  {len(nfts) if nfts else 0} NFT(s) found\n"
    
    if not nfts:
        response += "  No NFTs found or failed to fetch NFT data.\n"

    response += "\n🔄 Send another wallet address to check again, or use /start to restart."

    print(f"📤 Sending response to user")
    await update.message.reply_text(response, parse_mode='Markdown')
    return WALLET_ADDRESS

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """
    Cancel the conversation.
    """
    await update.message.reply_text("Operation cancelled. Use /start to try again.")
    return ConversationHandler.END

def main() -> None:
    """Run the Telegram bot."""
    print("🚀 Starting NFT Wallet Checker Bot...")
    print("✅ Bot is ready! Users can now check multiple wallets continuously.")
    print(f"🎯 Default collection ID: {DEFAULT_COLLECTION_ID}")
    print("🔐 Group verification system enabled!")
    print(f"📋 Minimum NFTs required: {MIN_NFT_REQUIRED}")
    print(f"⏰ Verification timeout: {VERIFICATION_TIMEOUT//60} minutes")
    
    global bot_application
    bot_application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

    # Set up conversation handler for manual wallet checking
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            WALLET_ADDRESS: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_wallet_address)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )

    bot_application.add_handler(conv_handler)
    
    # Add chat member handler for group join/leave events
    bot_application.add_handler(ChatMemberHandler(handle_chat_member_update, ChatMemberHandler.CHAT_MEMBER))
    
    # Add verification webhook handler (for testing - in production this would be a webhook endpoint)
    bot_application.add_handler(MessageHandler(filters.Regex(r'^\{.*"verification_id".*\}'), handle_verification_webhook))
    
    # Add admin commands
    bot_application.add_handler(CommandHandler("status", show_verification_status))
    bot_application.add_handler(CommandHandler("cleanup", cleanup_pending_verifications))
    
    # Run the Flask webhook server in a separate thread
    webhook_thread = Thread(target=run_webhook_server)
    webhook_thread.start()

    bot_application.run_polling()

async def show_verification_status(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Show current verification status (admin command).
    """
    if not update.effective_user.id in [123456789]:  # Replace with admin user IDs
        await update.message.reply_text("❌ You don't have permission to use this command.")
        return
    
    pending_count = len(pending_verifications)
    verified_count = sum(1 for v in pending_verifications.values() if v.get('verified', False))
    
    status_message = (
        f"📊 *Verification Status*\n\n"
        f"⏳ Pending verifications: {pending_count}\n"
        f"✅ Verified users: {verified_count}\n"
        f"❌ Unverified users: {pending_count - verified_count}\n\n"
        f"🕐 Timeout: {VERIFICATION_TIMEOUT//60} minutes\n"
        f"🎯 Min NFTs required: {MIN_NFT_REQUIRED}"
    )
    
    await update.message.reply_text(status_message, parse_mode='Markdown')

async def cleanup_pending_verifications(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Clean up expired verifications (admin command).
    """
    if not update.effective_user.id in [123456789]:  # Replace with admin user IDs
        await update.message.reply_text("❌ You don't have permission to use this command.")
        return
    
    current_time = datetime.now()
    expired_count = 0
    
    verification_ids_to_remove = []
    for vid, data in pending_verifications.items():
        if (current_time - data['joined_at']).total_seconds() > VERIFICATION_TIMEOUT:
            verification_ids_to_remove.append(vid)
            expired_count += 1
    
    for vid in verification_ids_to_remove:
        del pending_verifications[vid]
    
    await update.message.reply_text(
        f"🧹 Cleaned up {expired_count} expired verifications.\n"
        f"Remaining: {len(pending_verifications)}"
    )

if __name__ == "__main__":
    main()