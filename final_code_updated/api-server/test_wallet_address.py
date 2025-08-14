#!/usr/bin/env python3
"""
Test script to validate wallet addresses and test Helius API
"""

import os
import requests
import re
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def validate_wallet_address(address):
    """Validate Solana wallet address format"""
    print(f"🔍 Validating wallet address: {address}")
    
    if not address:
        print("❌ Address is empty")
        return False
    
    print(f"📏 Address length: {len(address)}")
    
    if len(address) < 32 or len(address) > 44:
        print(f"❌ Invalid length: {len(address)} (should be 32-44 characters)")
        return False
    
    if not re.match(r'^[A-Za-z0-9]+$', address):
        print("❌ Contains invalid characters")
        return False
    
    print("✅ Address format is valid")
    return True

def test_helius_api(wallet_address):
    """Test Helius API directly"""
    api_key = os.getenv("HELIUS_API_KEY")
    
    if not api_key:
        print("❌ HELIUS_API_KEY not found")
        return False
    
    print(f"\n🧪 Testing Helius API with wallet: {wallet_address}")
    
    # Test the exact endpoint we're using
    url = f"https://api.helius.xyz/v0/addresses/{wallet_address}/nfts?api-key={api_key}"
    print(f"🌐 URL: {url[:50]}...")
    
    try:
        response = requests.get(url, timeout=30)
        print(f"📊 Response status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Success! Found {len(data)} NFTs")
            return True
        else:
            print(f"❌ Error response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Request failed: {e}")
        return False

def test_alternative_endpoints(wallet_address):
    """Test alternative Helius endpoints"""
    api_key = os.getenv("HELIUS_API_KEY")
    
    if not api_key:
        return False
    
    print(f"\n🔄 Testing alternative Helius endpoints...")
    
    # Test different endpoints
    endpoints = [
        f"https://api.helius.xyz/v0/addresses/{wallet_address}/balances?api-key={api_key}",
        f"https://api.helius.xyz/v0/addresses/{wallet_address}/nfts?api-key={api_key}",
        f"https://api.helius.xyz/v0/addresses/{wallet_address}/tokens?api-key={api_key}"
    ]
    
    for i, endpoint in enumerate(endpoints):
        try:
            print(f"\n🔍 Testing endpoint {i+1}: {endpoint[:50]}...")
            response = requests.get(endpoint, timeout=10)
            print(f"   Status: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                if 'tokens' in data:
                    print(f"   ✅ Tokens: {len(data['tokens'])}")
                elif 'nfts' in data:
                    print(f"   ✅ NFTs: {len(data['nfts'])}")
                else:
                    print(f"   ✅ Data: {type(data)}")
            else:
                print(f"   ❌ Error: {response.text[:100]}")
                
        except Exception as e:
            print(f"   ❌ Failed: {e}")

if __name__ == "__main__":
    print("🚀 Wallet Address Validation & Helius API Test")
    print("=" * 60)
    
    # Test with the address from the error
    test_address = "BWha64zgbukDCVTAK9L9gGReNJaQ9f7faa2mb4e-4e7febfd9cd3"
    
    print(f"📝 Testing address: {test_address}")
    
    # Validate format
    is_valid = validate_wallet_address(test_address)
    
    if is_valid:
        # Test Helius API
        test_helius_api(test_address)
        
        # Test alternative endpoints
        test_alternative_endpoints(test_address)
    else:
        print("\n❌ Address validation failed, cannot test API")
    
    print("\n" + "=" * 60)
    print("💡 If the address is valid but API fails, check:")
    print("   1. API key validity")
    print("   2. Network connectivity")
    print("   3. Helius API status")
    print("   4. Rate limiting") 