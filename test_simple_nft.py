#!/usr/bin/env python3
"""
Simple NFT Verification Test
Quick test to identify the specific issue with the API endpoint.
"""

import requests
import json

# Test configuration
HELIUS_API_KEY = "6873bd5e-0b5d-49c4-a9ab-4e7febfd9cd3"
TEST_WALLET = "BWha64zgbukDCVTAK9L9gGReNJaQ9f7faa2ZnBMAr8Tt"

def test_helius_direct():
    """Test Helius API directly"""
    print("🔍 Testing Helius API directly...")
    
    try:
        # Test the exact endpoint that's failing
        url = f"https://api.helius.xyz/v0/addresses/{TEST_WALLET}/nfts?api-key={HELIUS_API_KEY}"
        print(f"📡 URL: {url}")
        
        response = requests.get(url, timeout=30)
        print(f"📊 Status Code: {response.status_code}")
        
        if response.status_code == 200:
            nfts = response.json()
            print(f"✅ Success! Found {len(nfts)} NFTs")
            
            # Show first NFT details
            if nfts:
                first_nft = nfts[0]
                name = first_nft.get("content", {}).get("metadata", {}).get("name", "Unknown")
                collection = first_nft.get("grouping", [{}])[0].get("group_value", "Unknown") if first_nft.get("grouping") else "Unknown"
                print(f"🎨 First NFT: {name} (Collection: {collection})")
            
            return True
        else:
            print(f"❌ Error: {response.status_code}")
            print(f"📄 Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Exception: {e}")
        return False

def test_api_server():
    """Test the failing API server endpoint"""
    print("\n🌐 Testing API Server Endpoint...")
    
    try:
        url = f"https://api-server-wcjc.onrender.com/api/addresses/{TEST_WALLET}/nft-assets?api-key={HELIUS_API_KEY}"
        print(f"📡 URL: {url}")
        
        response = requests.get(url, timeout=30)
        print(f"📊 Status Code: {response.status_code}")
        
        if response.status_code == 200:
            nfts = response.json()
            print(f"✅ Success! Found {len(nfts)} NFTs")
            return True
        else:
            print(f"❌ Error: {response.status_code}")
            print(f"📄 Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Exception: {e}")
        return False

def test_api_server_config():
    """Test the API server config endpoint"""
    print("\n⚙️ Testing API Server Config...")
    
    try:
        url = "https://api-server-wcjc.onrender.com/api/config"
        print(f"📡 URL: {url}")
        
        response = requests.get(url, timeout=30)
        print(f"📊 Status Code: {response.status_code}")
        
        if response.status_code == 200:
            config = response.json()
            print(f"✅ Config successful: {json.dumps(config, indent=2)}")
            return True
        else:
            print(f"❌ Error: {response.status_code}")
            print(f"📄 Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Exception: {e}")
        return False

def main():
    """Run the simple tests"""
    print("🚀 Simple NFT Verification Test")
    print("=" * 50)
    
    # Test 1: Helius API directly
    helius_ok = test_helius_direct()
    
    # Test 2: API server config
    config_ok = test_api_server_config()
    
    # Test 3: API server NFT endpoint
    api_ok = test_api_server()
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 SUMMARY")
    print("=" * 50)
    
    print(f"🔍 Helius API Direct: {'✅ OK' if helius_ok else '❌ FAIL'}")
    print(f"⚙️  API Server Config: {'✅ OK' if config_ok else '❌ FAIL'}")
    print(f"🌐 API Server NFT Endpoint: {'✅ OK' if api_ok else '❌ FAIL'}")
    
    if helius_ok and not api_ok:
        print("\n🎯 DIAGNOSIS: Helius API works, but API server has issues")
        print("💡 The problem is likely in the API server code, not the Helius API")
    elif not helius_ok:
        print("\n🎯 DIAGNOSIS: Helius API itself has issues")
        print("💡 Check your API key and Helius service status")
    else:
        print("\n🎯 DIAGNOSIS: Everything appears to be working")

if __name__ == "__main__":
    main() 