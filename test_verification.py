#!/usr/bin/env python3
"""
Test script for NFT verification system
"""

import requests
import json
import time

def test_webhook():
    """Test the webhook endpoint"""
    print("🧪 Testing webhook endpoint...")
    
    # Test data
    test_data = {
        "verification_id": "test_123_456_789",
        "wallet_address": "EFwPVHhY6vH64MsMDx9ub8Edn4ktYYBcgqNYki1R3rmE",
        "nft_count": 3,
        "verified": True,
        "timestamp": int(time.time())
    }
    
    try:
        response = requests.post(
            "http://localhost:5000/verify",
            json=test_data,
            headers={"Content-Type": "application/json"}
        )
        
        print(f"📊 Response Status: {response.status_code}")
        print(f"📄 Response: {response.text}")
        
        if response.status_code == 200:
            print("✅ Webhook test successful!")
        else:
            print("❌ Webhook test failed!")
            
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to webhook server. Make sure the bot is running.")
    except Exception as e:
        print(f"❌ Error testing webhook: {e}")

def test_helius_api():
    """Test Helius API connection"""
    print("\n🧪 Testing Helius API...")
    
    url = "https://mainnet.helius-rpc.com/?api-key=6873bd5e-0b5d-49c4-a9ab-4e7febfd9cd3"
    
    payload = {
        "jsonrpc": "2.0",
        "id": "my-id",
        "method": "searchAssets",
        "params": {
            "ownerAddress": "EFwPVHhY6vH64MsMDx9ub8Edn4ktYYBcgqNYki1R3rmE"
        }
    }
    
    try:
        response = requests.post(url, json=payload)
        print(f"📊 Response Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            if "result" in data and "items" in data["result"]:
                nfts = [item for item in data["result"]["items"] 
                       if item.get("content", {}).get("metadata", {}).get("token_standard") == "NonFungible"]
                print(f"✅ Helius API working! Found {len(nfts)} NFTs")
            else:
                print("⚠️ Helius API response format unexpected")
        else:
            print(f"❌ Helius API error: {response.text}")
            
    except Exception as e:
        print(f"❌ Error testing Helius API: {e}")

def test_verification_flow():
    """Test the complete verification flow"""
    print("\n🧪 Testing complete verification flow...")
    
    # Simulate user joining
    print("1️⃣ Simulating user join...")
    
    # Simulate verification data
    verification_data = {
        "verification_id": "test_user_123",
        "wallet_address": "EFwPVHhY6vH64MsMDx9ub8Edn4ktYYBcgqNYki1R3rmE",
        "nft_count": 2,
        "verified": True,
        "timestamp": int(time.time())
    }
    
    print("2️⃣ Sending verification data...")
    print(f"   Wallet: {verification_data['wallet_address']}")
    print(f"   NFTs: {verification_data['nft_count']}")
    print(f"   Verified: {verification_data['verified']}")
    
    try:
        response = requests.post(
            "http://localhost:5000/verify",
            json=verification_data,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            print("✅ Verification flow test successful!")
        else:
            print(f"❌ Verification flow test failed: {response.text}")
            
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to verification server")
    except Exception as e:
        print(f"❌ Error in verification flow: {e}")

if __name__ == "__main__":
    print("🚀 NFT Verification System Test")
    print("=" * 40)
    
    test_webhook()
    test_helius_api()
    test_verification_flow()
    
    print("\n📋 Test Summary:")
    print("- Webhook endpoint should be accessible at http://localhost:5000/verify")
    print("- Helius API should return NFT data")
    print("- Verification flow should process data correctly")
    print("\n💡 Make sure the bot is running before testing!") 