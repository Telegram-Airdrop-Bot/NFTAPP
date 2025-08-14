import requests
import json
import time

def test_optimized_verification():
    """Test the optimized NFT verification system"""
    wallet_address = "EFwPVHhY6vH64MsMDx9ub8Edn4ktYYBcgqNYki1R3rmE"
    collection_id = "j7qeFNnpWTbaf5g9sMCxP2zfKrH5QFgE56SuYjQDQi1"  # Meta Betties
    
    print(f"🔍 Testing Optimized NFT Verification System")
    print(f"💰 Wallet: {wallet_address}")
    print(f"🎯 Collection: {collection_id}")
    print("=" * 60)
    
    # Test 1: Health check
    print("\n🔄 Test 1: Health Check")
    try:
        response = requests.get(
            "https://api-server-wcjc.onrender.com/api/health",
            timeout=10
        )
        print(f"📊 Status: {response.status_code}")
        if response.status_code == 200:
            result = response.json()
            print(f"📄 Health: {json.dumps(result, indent=2)}")
            print("✅ Health check: PASSED")
        else:
            print("❌ Health check: FAILED")
    except Exception as e:
        print(f"❌ Error in health check: {e}")
    
    # Test 2: General NFT verification (any NFT)
    print("\n🔄 Test 2: General NFT verification (any NFT)")
    test_data_1 = {
        "wallet_address": wallet_address,
        "tg_id": "7761809923"
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
    
    # Test 3: Collection-specific verification
    print("\n🔄 Test 3: Collection-specific verification (Meta Betties)")
    test_data_2 = {
        "wallet_address": wallet_address,
        "tg_id": "123456789",
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
    
    # Test 4: Wrong collection verification
    print("\n🔄 Test 4: Wrong collection verification")
    test_data_3 = {
        "wallet_address": wallet_address,
        "tg_id": "123456789",
        "collection_id": "wrong_collection_id"
    }
    
    start_time = time.time()
    try:
        response_3 = requests.post(
            "https://api-server-wcjc.onrender.com/api/verify-nft",
            json=test_data_3,
            timeout=30
        )
        end_time = time.time()
        
        print(f"📊 Status: {response_3.status_code}")
        print(f"⏱️ Response time: {end_time - start_time:.2f}s")
        
        if response_3.status_code == 200:
            result_3 = response_3.json()
            print(f"📄 Result: {json.dumps(result_3, indent=2)}")
            
            if result_3.get("has_nft"):
                print("✅ Wrong collection verification: PASSED (unexpected)")
            else:
                print("❌ Wrong collection verification: FAILED (expected)")
        else:
            print(f"❌ Wrong collection verification failed with status: {response_3.status_code}")
            print(f"📄 Error: {response_3.text}")
            
    except requests.exceptions.Timeout:
        print("⏰ Wrong collection verification: TIMEOUT (30s)")
    except Exception as e:
        print(f"❌ Error in wrong collection verification: {e}")
    
    # Test 5: Performance test with multiple requests
    print("\n🔄 Test 5: Performance test (3 consecutive requests)")
    for i in range(3):
        print(f"\n  📍 Request {i+1}/3:")
        start_time = time.time()
        try:
            response = requests.post(
                "https://api-server-wcjc.onrender.com/api/verify-nft",
                json=test_data_2,
                timeout=30
            )
            end_time = time.time()
            
            print(f"    📊 Status: {response.status_code}")
            print(f"    ⏱️ Response time: {end_time - start_time:.2f}s")
            
            if response.status_code == 200:
                result = response.json()
                print(f"    ✅ Success: {result.get('has_nft')} NFTs")
            else:
                print(f"    ❌ Failed: {response.text}")
                
        except requests.exceptions.Timeout:
            print("    ⏰ TIMEOUT (30s)")
        except Exception as e:
            print(f"    ❌ Error: {e}")
        
        # Small delay between requests
        if i < 2:
            time.sleep(1)
    
    print("\n" + "=" * 60)
    print("🎯 Testing completed! Check results above.")

if __name__ == "__main__":
    test_optimized_verification() 