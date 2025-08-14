#!/usr/bin/env python3
"""
Test script to verify Helius DAS API implementation
"""

import os
import requests
import json
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_das_api():
    """Test the Helius DAS API directly"""
    api_key = os.getenv("HELIUS_API_KEY")
    
    if not api_key:
        print("❌ HELIUS_API_KEY not found")
        return False
    
    print("🧪 Testing Helius DAS API Implementation")
    print("=" * 60)
    
    # Test wallet address (use a known valid Solana address)
    test_wallet = "11111111111111111111111111111112"  # System Program (known valid address)
    
    print(f"🔍 Testing with wallet: {test_wallet}")
    
    # Test the DAS API searchAssets method
    das_url = "https://mainnet.helius-rpc.com"
    
    payload = {
        "jsonrpc": "2.0",
        "id": "test-das",
        "method": "searchAssets",
        "params": {
            "ownerAddress": test_wallet,
            "tokenType": "all",
            "displayOptions": {
                "showUnverifiedCollections": True,
                "showZeroBalance": False
            }
        }
    }
    
    try:
        print(f"🌐 Calling DAS API: {das_url}")
        print(f"📦 Request payload: {json.dumps(payload, indent=2)}")
        
        response = requests.post(
            f"{das_url}/?api-key={api_key}",
            json=payload,
            timeout=30,
            headers={'Content-Type': 'application/json'}
        )
        
        print(f"📊 Response status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            
            # Check for JSON-RPC errors
            if "error" in data:
                print(f"❌ DAS API error: {data['error']}")
                return False
            
            # Check response structure
            if "result" in data and "items" in data["result"]:
                assets = data["result"]["items"]
                print(f"✅ Success! Found {len(assets)} assets")
                
                # Show first few assets for verification
                for i, asset in enumerate(assets[:3]):
                    print(f"\n📦 Asset {i+1}:")
                    print(f"   ID: {asset.get('id', 'N/A')}")
                    print(f"   Interface: {asset.get('interface', 'N/A')}")
                    
                    content = asset.get('content', {})
                    metadata = content.get('metadata', {})
                    print(f"   Name: {metadata.get('name', 'N/A')}")
                    print(f"   Token Standard: {metadata.get('token_standard', 'N/A')}")
                    
                    grouping = asset.get('grouping', [])
                    if grouping:
                        print(f"   Collection: {grouping[0].get('group_value', 'N/A')}")
                
                return True
            else:
                print(f"❌ Unexpected response format: {data}")
                return False
        else:
            print(f"❌ HTTP error: {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Request failed: {e}")
        return False

def test_collection_filtering():
    """Test collection filtering with DAS API"""
    api_key = os.getenv("HELIUS_API_KEY")
    
    if not api_key:
        return False
    
    print(f"\n🔍 Testing Collection Filtering")
    print("=" * 60)
    
    # Test with a known collection
    test_collection = "J1S9H3QjnRtBbbuD4HjPV6RpRhwuk4zKbxsnCHuTgh9w"  # Mad Lads collection
    
    print(f"🎯 Testing collection: {test_collection}")
    
    # Test the getAssetsByGroup method
    das_url = "https://mainnet.helius-rpc.com"
    
    payload = {
        "jsonrpc": "2.0",
        "id": "test-collection",
        "method": "getAssetsByGroup",
        "params": {
            "groupKey": "collection",
            "groupValue": test_collection,
            "page": 1,
            "limit": 5
        }
    }
    
    try:
        response = requests.post(
            f"{das_url}/?api-key={api_key}",
            json=payload,
            timeout=30,
            headers={'Content-Type': 'application/json'}
        )
        
        if response.status_code == 200:
            data = response.json()
            
            if "error" in data:
                print(f"❌ Collection API error: {data['error']}")
                return False
            
            if "result" in data and "items" in data["result"]:
                items = data["result"]["items"]
                print(f"✅ Collection test successful! Found {len(items)} items")
                
                # Show first item details
                if items:
                    first_item = items[0]
                    print(f"📦 First item: {first_item.get('id', 'N/A')}")
                    print(f"   Name: {first_item.get('content', {}).get('metadata', {}).get('name', 'N/A')}")
                
                return True
            else:
                print(f"❌ Unexpected collection response format")
                return False
        else:
            print(f"❌ Collection API HTTP error: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Collection API request failed: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Helius DAS API Test Suite")
    print("=" * 60)
    
    # Test basic DAS API functionality
    das_test = test_das_api()
    
    # Test collection filtering
    collection_test = test_collection_filtering()
    
    print("\n" + "=" * 60)
    print("📊 Test Results:")
    print(f"  DAS API Basic: {'✅ PASS' if das_test else '❌ FAIL'}")
    print(f"  Collection Filtering: {'✅ PASS' if collection_test else '❌ FAIL'}")
    
    if das_test and collection_test:
        print("\n🎉 All DAS API tests passed! The new implementation should work correctly.")
        print("\n💡 Benefits of DAS API:")
        print("   ✅ More reliable NFT detection")
        print("   ✅ Better collection filtering")
        print("   ✅ Improved error handling")
        print("   ✅ Modern API standards")
    else:
        print("\n❌ Some tests failed. Please check the implementation.") 