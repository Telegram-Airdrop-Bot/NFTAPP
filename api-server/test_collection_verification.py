import requests
import json

def test_collection_verification():
    """Test collection-specific NFT verification"""
    wallet_address = "EFwPVHhY6vH64MsMDx9ub8Edn4ktYYBcgqNYki1R3rmE"
    collection_id = "j7qeFNnpWTbaf5g9sMCxP2zfKrH5QFgE56SuYjQDQi1"  # Meta Betties
    
    print(f"🔍 Testing Collection-Specific NFT Verification")
    print(f"💰 Wallet: {wallet_address}")
    print(f"🎯 Collection: {collection_id}")
    print("=" * 50)
    
    # Test 1: General NFT verification (no collection filter)
    print("\n🔄 Test 1: General NFT verification (any NFT)")
    test_data_1 = {
        "wallet_address": wallet_address,
        "tg_id": "7761809923"
    }
    
    try:
        response_1 = requests.post(
            "https://api-server-wcjc.onrender.com/api/verify-nft",
            json=test_data_1,
            timeout=30
        )
        print(f"📊 Status: {response_1.status_code}")
        result_1 = response_1.json()
        print(f"📄 Result: {json.dumps(result_1, indent=2)}")
        
        if result_1.get("has_nft"):
            print("✅ General verification: PASSED")
        else:
            print("❌ General verification: FAILED")
            
    except Exception as e:
        print(f"❌ Error in general verification: {e}")
    
    # Test 2: Collection-specific verification
    print("\n🔄 Test 2: Collection-specific verification (Meta Betties)")
    test_data_2 = {
        "wallet_address": wallet_address,
        "tg_id": "123456789",
        "collection_id": collection_id
    }
    
    try:
        response_2 = requests.post(
            "https://api-server-wcjc.onrender.com/api/verify-nft",
            json=test_data_2,
            timeout=30
        )
        print(f"📊 Status: {response_2.status_code}")
        result_2 = response_2.json()
        print(f"📄 Result: {json.dumps(result_2, indent=2)}")
        
        if result_2.get("has_nft"):
            print("✅ Collection verification: PASSED")
        else:
            print("❌ Collection verification: FAILED")
            
    except Exception as e:
        print(f"❌ Error in collection verification: {e}")
    
    # Test 3: Wrong collection verification
    print("\n🔄 Test 3: Wrong collection verification")
    test_data_3 = {
        "wallet_address": wallet_address,
        "tg_id": "123456789",
        "collection_id": "wrong_collection_id"
    }
    
    try:
        response_3 = requests.post(
            "https://api-server-wcjc.onrender.com/api/verify-nft",
            json=test_data_3,
            timeout=30
        )
        print(f"📊 Status: {response_3.status_code}")
        result_3 = response_3.json()
        print(f"📄 Result: {json.dumps(result_3, indent=2)}")
        
        if result_3.get("has_nft"):
            print("✅ Wrong collection verification: PASSED (unexpected)")
        else:
            print("❌ Wrong collection verification: FAILED (expected)")
            
    except Exception as e:
        print(f"❌ Error in wrong collection verification: {e}")

if __name__ == "__main__":
    test_collection_verification() 