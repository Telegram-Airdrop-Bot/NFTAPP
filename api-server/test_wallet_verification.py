import requests
import json
import time

def test_wallet_verification():
    """Test the main NFT verification endpoint for a specific wallet"""
    wallet_address = "BWha64zgbukDCVTAK9L9gGReNJaQ9f7faa2ZnBMAr8Tt"
    
    print(f"🔍 Testing Main NFT Verification Endpoint")
    print(f"💰 Wallet: {wallet_address}")
    print("=" * 60)
    
    # Test 1: General NFT verification (no collection filter)
    print("\n🔄 Test 1: General NFT verification (any NFT)")
    test_data_1 = {
        "wallet_address": wallet_address,
        "tg_id": "test_user_123"
    }
    
    start_time = time.time()
    try:
        response_1 = requests.post(
            "https://api-server-wcjc.onrender.com/api/verify-nft",
            json=test_data_1,
            timeout=30
        )
        end_time = time.time()
        
        print(f"📊 Status: {response_1.status_code}")
        print(f"⏱️ Response time: {end_time - start_time:.2f}s")
        
        if response_1.status_code == 200:
            result_1 = response_1.json()
            print(f"📄 Result: {json.dumps(result_1, indent=2)}")
            
            if result_1.get("has_nft"):
                print("✅ General verification: PASSED")
            else:
                print("❌ General verification: FAILED")
        else:
            print(f"❌ General verification failed with status: {response_1.status_code}")
            print(f"📄 Error: {response_1.text}")
            
    except requests.exceptions.Timeout:
        print("⏰ General verification: TIMEOUT (30s)")
    except Exception as e:
        print(f"❌ Error in general verification: {e}")
    
    # Test 2: Collection-specific verification (Meta Betties)
    print("\n🔄 Test 2: Collection-specific verification (Meta Betties)")
    collection_id = "j7qeFNnpWTbaf5g9sMCxP2zfKrH5QFgE56SuYjQDQi1"
    test_data_2 = {
        "wallet_address": wallet_address,
        "tg_id": "test_user_456",
        "collection_id": collection_id
    }
    
    start_time = time.time()
    try:
        response_2 = requests.post(
            "https://api-server-wcjc.onrender.com/api/verify-nft",
            json=test_data_2,
            timeout=30
        )
        end_time = time.time()
        
        print(f"📊 Status: {response_2.status_code}")
        print(f"⏱️ Response time: {end_time - start_time:.2f}s")
        
        if response_2.status_code == 200:
            result_2 = response_2.json()
            print(f"📄 Result: {json.dumps(result_2, indent=2)}")
            
            if result_2.get("has_nft"):
                print("✅ Collection verification: PASSED")
            else:
                print("❌ Collection verification: FAILED")
        else:
            print(f"❌ Collection verification failed with status: {response_2.status_code}")
            print(f"📄 Error: {response_2.text}")
            
    except requests.exceptions.Timeout:
        print("⏰ Collection verification: TIMEOUT (30s)")
    except Exception as e:
        print(f"❌ Error in collection verification: {e}")
    
    # Test 3: Health check
    print("\n🔄 Test 3: Health Check")
    try:
        response_health = requests.get(
            "https://api-server-wcjc.onrender.com/api/health",
            timeout=10
        )
        print(f"📊 Status: {response_health.status_code}")
        if response_health.status_code == 200:
            result_health = response_health.json()
            print(f"📄 Health: {json.dumps(result_health, indent=2)}")
            print("✅ Health check: PASSED")
        else:
            print("❌ Health check: FAILED")
    except Exception as e:
        print(f"❌ Error in health check: {e}")
    
    print("\n" + "=" * 60)
    print("🎯 Testing completed! Check results above.")

if __name__ == "__main__":
    test_wallet_verification() 