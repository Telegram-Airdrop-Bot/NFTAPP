#!/usr/bin/env python3
"""
NFT Verification Test Script
Tests all NFT verification functions to ensure they're working properly.
"""

import requests
import json
import time
from typing import Dict, List, Optional

# Test configuration
HELIUS_API_KEY = "6873bd5e-0b5d-49c4-a9ab-4e7febfd9cd3"
TEST_WALLET = "BWha64zgbukDCVTAK9L9gGReNJaQ9f7faa2ZnBMAr8Tt"  # The wallet from your error
COLLECTION_ID = "j7qeFNnpWTbaf5g9sMCxP2zfKrH5QFgE56SuYjQDQi1"  # Meta Betties collection

def test_helius_api_connection():
    """Test basic Helius API connection"""
    print("🔍 Testing Helius API Connection...")
    
    try:
        # Test balance endpoint
        url = f"https://api.helius.xyz/v0/addresses/{TEST_WALLET}/balances?api-key={HELIUS_API_KEY}"
        response = requests.get(url, timeout=30)
        
        if response.status_code == 200:
            data = response.json()
            balance = data.get("nativeBalance", 0) / 1_000_000_000  # Convert lamports to SOL
            print(f"✅ Helius API connection successful!")
            print(f"💰 Wallet balance: {balance:.4f} SOL")
            return True
        else:
            print(f"❌ Helius API error: {response.status_code}")
            print(f"📄 Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Helius API connection failed: {e}")
        return False

def test_helius_nft_endpoint():
    """Test Helius NFT endpoint directly"""
    print("\n🎨 Testing Helius NFT Endpoint...")
    
    try:
        url = f"https://api.helius.xyz/v0/addresses/{TEST_WALLET}/nfts?api-key={HELIUS_API_KEY}"
        response = requests.get(url, timeout=30)
        
        if response.status_code == 200:
            nfts = response.json()
            print(f"✅ Helius NFT endpoint successful!")
            print(f"📊 Found {len(nfts)} NFTs")
            
            # Show first few NFTs
            for i, nft in enumerate(nfts[:3]):
                name = nft.get("content", {}).get("metadata", {}).get("name", "Unknown")
                collection = nft.get("grouping", [{}])[0].get("group_value", "Unknown") if nft.get("grouping") else "Unknown"
                print(f"  NFT {i+1}: {name} (Collection: {collection})")
            
            return True
        else:
            print(f"❌ Helius NFT endpoint error: {response.status_code}")
            print(f"📄 Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Helius NFT endpoint failed: {e}")
        return False

def test_helius_das_api():
    """Test Helius DAS API for asset search"""
    print("\n🔍 Testing Helius DAS API...")
    
    try:
        url = "https://mainnet.helius-rpc.com/?api-key=" + HELIUS_API_KEY
        payload = {
            "jsonrpc": "2.0",
            "id": "test-id",
            "method": "searchAssets",
            "params": {
                "ownerAddress": TEST_WALLET
            }
        }
        
        response = requests.post(url, json=payload, timeout=30)
        
        if response.status_code == 200:
            data = response.json()
            
            if "error" in data:
                print(f"❌ DAS API error: {data['error']}")
                return False
            
            if "result" in data and "items" in data["result"]:
                items = data["result"]["items"]
                print(f"✅ Helius DAS API successful!")
                print(f"📦 Found {len(items)} total assets")
                
                # Count NFTs vs tokens
                nft_count = 0
                token_count = 0
                
                for item in items:
                    token_standard = item.get("content", {}).get("metadata", {}).get("token_standard", "")
                    if token_standard in ["NonFungible", "non-fungible", "NONFUNGIBLE"]:
                        nft_count += 1
                    elif token_standard in ["Fungible", "fungible", "FUNGIBLE"]:
                        token_count += 1
                
                print(f"🎨 NFTs: {nft_count}")
                print(f"🪙 Tokens: {token_count}")
                
                return True
            else:
                print(f"❌ DAS API response format error")
                print(f"📄 Response: {data}")
                return False
        else:
            print(f"❌ DAS API HTTP error: {response.status_code}")
            print(f"📄 Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Helius DAS API failed: {e}")
        return False

def test_collection_filtering():
    """Test collection filtering functionality"""
    print("\n🎯 Testing Collection Filtering...")
    
    try:
        url = "https://mainnet.helius-rpc.com/?api-key=" + HELIUS_API_KEY
        payload = {
            "jsonrpc": "2.0",
            "id": "test-id",
            "method": "searchAssets",
            "params": {
                "ownerAddress": TEST_WALLET
            }
        }
        
        response = requests.post(url, json=payload, timeout=30)
        
        if response.status_code == 200:
            data = response.json()
            
            if "result" in data and "items" in data["result"]:
                items = data["result"]["items"]
                
                # Filter for Meta Betties collection
                meta_betties_nfts = []
                for item in items:
                    grouping = item.get("grouping", [])
                    if grouping and len(grouping) > 0:
                        collection = grouping[0].get("group_value")
                        if collection == COLLECTION_ID:
                            meta_betties_nfts.append(item)
                
                print(f"✅ Collection filtering successful!")
                print(f"🎯 Meta Betties NFTs found: {len(meta_betties_nfts)}")
                
                if meta_betties_nfts:
                    for i, nft in enumerate(meta_betties_nfts[:3]):
                        name = nft.get("content", {}).get("metadata", {}).get("name", "Unknown")
                        print(f"  Meta Betties NFT {i+1}: {name}")
                
                return True
            else:
                print(f"❌ Collection filtering failed - no items found")
                return False
        else:
            print(f"❌ Collection filtering HTTP error: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Collection filtering failed: {e}")
        return False

def test_api_server_endpoint():
    """Test the deployed API server endpoint"""
    print("\n🌐 Testing Deployed API Server...")
    
    try:
        url = f"https://api-server-wcjc.onrender.com/api/addresses/{TEST_WALLET}/nft-assets?api-key={HELIUS_API_KEY}"
        response = requests.get(url, timeout=30)
        
        print(f"📊 API Server Response Status: {response.status_code}")
        
        if response.status_code == 200:
            nfts = response.json()
            print(f"✅ API Server endpoint successful!")
            print(f"📊 Found {len(nfts)} NFTs")
            return True
        else:
            print(f"❌ API Server error: {response.status_code}")
            print(f"📄 Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ API Server test failed: {e}")
        return False

def test_verification_logic():
    """Test the verification logic"""
    print("\n🔐 Testing Verification Logic...")
    
    try:
        # Simulate the verification process
        url = f"https://api-server-wcjc.onrender.com/api/verify-nft"
        payload = {
            "wallet_address": TEST_WALLET,
            "tg_id": "12345",
            "collection_id": COLLECTION_ID
        }
        
        response = requests.post(url, json=payload, timeout=30)
        
        print(f"📊 Verification Response Status: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Verification endpoint successful!")
            print(f"📊 Result: {json.dumps(result, indent=2)}")
            return True
        else:
            print(f"❌ Verification endpoint error: {response.status_code}")
            print(f"📄 Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Verification test failed: {e}")
        return False

def run_all_tests():
    """Run all tests and provide summary"""
    print("🚀 Starting NFT Verification Tests...")
    print("=" * 60)
    
    tests = [
        ("Helius API Connection", test_helius_api_connection),
        ("Helius NFT Endpoint", test_helius_nft_endpoint),
        ("Helius DAS API", test_helius_das_api),
        ("Collection Filtering", test_collection_filtering),
        ("API Server Endpoint", test_api_server_endpoint),
        ("Verification Logic", test_verification_logic)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        try:
            success = test_func()
            results.append((test_name, success))
        except Exception as e:
            print(f"❌ {test_name} test crashed: {e}")
            results.append((test_name, False))
        
        time.sleep(1)  # Small delay between tests
    
    # Print summary
    print("\n" + "=" * 60)
    print("📊 TEST RESULTS SUMMARY")
    print("=" * 60)
    
    passed = 0
    total = len(results)
    
    for test_name, success in results:
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status} {test_name}")
        if success:
            passed += 1
    
    print(f"\n🎯 Overall Result: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! NFT verification is working properly.")
    elif passed >= total * 0.8:
        print("⚠️  Most tests passed. Some issues need attention.")
    else:
        print("❌ Many tests failed. NFT verification has significant issues.")
    
    return passed, total

if __name__ == "__main__":
    try:
        passed, total = run_all_tests()
        exit(0 if passed == total else 1)
    except KeyboardInterrupt:
        print("\n⏹️  Tests interrupted by user")
        exit(1)
    except Exception as e:
        print(f"\n💥 Test script crashed: {e}")
        exit(1) 