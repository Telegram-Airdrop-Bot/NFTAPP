#!/usr/bin/env python3
"""
NFT Verification Locations - Shows where verification happens in the codebase
"""

import os
from pathlib import Path

def show_verification_locations():
    """Display all locations where NFT verification occurs"""
    
    print("🔍 NFT Verification Locations in Your Codebase")
    print("=" * 60)
    
    verification_locations = {
        "1. API Server (Main Verification)": {
            "file": "api-server/api_server.py",
            "function": "verify_nft()",
            "lines": "47-146",
            "description": "Main endpoint that receives verification requests from frontend",
            "key_code": "has_required_nft, nft_count = has_nft(wallet_address, collection_id)"
        },
        
        "2. Python Verifier (Core Logic)": {
            "file": "api-server/verifier_python.py", 
            "function": "has_nft_python()",
            "lines": "168-209",
            "description": "Core verification logic using Helius API",
            "key_code": "nfts = get_wallet_nfts_by_collection(wallet_address, collection_id)"
        },
        
        "3. NFT Collection Filter": {
            "file": "api-server/verifier_python.py",
            "function": "get_wallet_nfts_by_collection()", 
            "lines": "62-166",
            "description": "Fetches NFTs and filters by collection ID",
            "key_code": "if nft_collection == collection_id:"
        },
        
        "4. Bot Server Webhook": {
            "file": "bot-server/bot.py",
            "function": "verify_callback()",
            "lines": "449-520", 
            "description": "Receives verification results and handles user access",
            "key_code": "if has_nft: # User has NFT - keep them in group"
        },
        
        "5. Webhook Server": {
            "file": "bot-server/webhook_server.py",
            "function": "verify_callback()",
            "lines": "32-50",
            "description": "Alternative webhook handler for verification callbacks",
            "key_code": "save_webhook_data(data)"
        },
        
        "6. NFT Verification Module": {
            "file": "nft.py",
            "function": "verify_wallet_nft_ownership()",
            "lines": "287-310",
            "description": "Legacy verification function",
            "key_code": "nfts = get_wallet_nfts_by_collection(wallet_address)"
        }
    }
    
    for location, details in verification_locations.items():
        print(f"\n📍 {location}")
        print(f"   📄 File: {details['file']}")
        print(f"   🔧 Function: {details['function']}")
        print(f"   📍 Lines: {details['lines']}")
        print(f"   📝 Description: {details['description']}")
        print(f"   💻 Key Code: {details['key_code']}")
    
    print("\n🔄 Verification Flow:")
    print("1. Frontend → API Server (/api/verify-nft)")
    print("2. API Server → Python Verifier (has_nft_python)")
    print("3. Python Verifier → Helius API (NFT check)")
    print("4. API Server → Bot Server (webhook)")
    print("5. Bot Server → Telegram (user access control)")
    
    print("\n🎯 Collection ID Usage:")
    print("• Default: j7qeFNnpWTbaf5g9sMCxP2zfKrH5QFgE56SuYjQDQi1 (Meta Betties)")
    print("• Environment Variable: COLLECTION_ID")
    print("• Filter Logic: Only NFTs from this collection count")
    
    print("\n🔧 Key Verification Points:")
    print("✅ Wallet address validation")
    print("✅ Helius API NFT fetch")
    print("✅ Collection ID filtering")
    print("✅ NFT count verification")
    print("✅ Webhook result handling")
    print("✅ Telegram group access control")

if __name__ == "__main__":
    show_verification_locations() 