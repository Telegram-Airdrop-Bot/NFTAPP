#!/usr/bin/env python3
"""
Show Collection ID Information for NFT Verification Bot
"""

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def show_collection_info():
    """Display collection ID and related configuration"""
    
    print("🎨 NFT Verification Bot - Collection ID Information")
    print("=" * 50)
    
    # Get collection ID from environment
    collection_id = os.getenv("COLLECTION_ID", "j7qeFNnpWTbaf5g9sMCxP2zfKrH5QFgE56SuYjQDQi1")
    
    print(f"📋 Current Collection ID: {collection_id}")
    print(f"📝 Collection Name: Meta Betties (based on ID)")
    print(f"🔗 Blockchain: Solana")
    
    print("\n📁 Configuration Files:")
    print("  ✅ bot-server/bot.py - Main bot file")
    print("  ✅ bot-server/webhook_server.py - Webhook handler")
    print("  ✅ api-server/api_server.py - API server")
    print("  ✅ nft.py - NFT verification logic")
    
    print("\n🔧 Environment Variables:")
    print(f"  COLLECTION_ID={collection_id}")
    print(f"  HELIUS_API_KEY={'✅ Set' if os.getenv('HELIUS_API_KEY') else '❌ Missing'}")
    print(f"  TELEGRAM_BOT_TOKEN={'✅ Set' if os.getenv('TELEGRAM_BOT_TOKEN') else '❌ Missing'}")
    print(f"  TELEGRAM_GROUP_ID={'✅ Set' if os.getenv('TELEGRAM_GROUP_ID') else '❌ Missing'}")
    
    print("\n🎯 How to Change Collection ID:")
    print("1. Set environment variable: COLLECTION_ID=your_new_collection_id")
    print("2. Or modify the default value in bot.py line 16")
    print("3. Restart the bot server")
    
    print("\n📊 Verification Process:")
    print("1. User joins Telegram group")
    print("2. Bot sends verification link")
    print("3. User connects wallet")
    print("4. System checks for NFTs in collection: " + collection_id)
    print("5. If found: User gets access")
    print("6. If not found: User gets removed")

if __name__ == "__main__":
    show_collection_info() 