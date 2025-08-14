import sys
import os
import time
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from verifier_python import has_nft, get_wallet_nfts_by_collection

def test_local_optimized():
    """Test the optimized NFT verification system locally"""
    wallet_address = "EFwPVHhY6vH64MsMDx9ub8Edn4ktYYBcgqNYki1R3rmE"
    collection_id = "j7qeFNnpWTbaf5g9sMCxP2zfKrH5QFgE56SuYjQDQi1"  # Meta Betties
    
    print(f"🔍 Testing Local Optimized NFT Verification System")
    print(f"💰 Wallet: {wallet_address}")
    print(f"🎯 Collection: {collection_id}")
    print("=" * 60)
    
    # Test 1: General NFT verification (no collection filter)
    print("\n🔄 Test 1: General NFT verification (any NFT)")
    start_time = time.time()
    try:
        has_required_nft, nft_count = has_nft(wallet_address)
        end_time = time.time()
        
        print(f"⏱️ Verification time: {end_time - start_time:.2f}s")
        print(f"📊 Result: has_nft={has_required_nft}, count={nft_count}")
        
        if has_required_nft:
            print("✅ General verification: PASSED")
        else:
            print("❌ General verification: FAILED")
            
    except Exception as e:
        print(f"❌ Error in general verification: {e}")
    
    # Test 2: Collection-specific verification
    print("\n🔄 Test 2: Collection-specific verification (Meta Betties)")
    start_time = time.time()
    try:
        has_required_nft, nft_count = has_nft(wallet_address, collection_id)
        end_time = time.time()
        
        print(f"⏱️ Verification time: {end_time - start_time:.2f}s")
        print(f"📊 Result: has_nft={has_required_nft}, count={nft_count}")
        
        if has_required_nft:
            print("✅ Collection verification: PASSED")
        else:
            print("❌ Collection verification: FAILED")
            
    except Exception as e:
        print(f"❌ Error in collection verification: {e}")
    
    # Test 3: Wrong collection verification
    print("\n🔄 Test 3: Wrong collection verification")
    start_time = time.time()
    try:
        has_required_nft, nft_count = has_nft(wallet_address, "wrong_collection_id")
        end_time = time.time()
        
        print(f"⏱️ Verification time: {end_time - start_time:.2f}s")
        print(f"📊 Result: has_nft={has_required_nft}, count={nft_count}")
        
        if has_required_nft:
            print("✅ Wrong collection verification: PASSED (unexpected)")
        else:
            print("❌ Wrong collection verification: FAILED (expected)")
            
    except Exception as e:
        print(f"❌ Error in wrong collection verification: {e}")
    
    # Test 4: Performance test with multiple requests (testing cache)
    print("\n🔄 Test 4: Performance test (3 consecutive requests - testing cache)")
    for i in range(3):
        print(f"\n  📍 Request {i+1}/3:")
        start_time = time.time()
        try:
            has_required_nft, nft_count = has_nft(wallet_address, collection_id)
            end_time = time.time()
            
            print(f"    ⏱️ Response time: {end_time - start_time:.2f}s")
            print(f"    ✅ Success: {has_required_nft} NFTs, count: {nft_count}")
                
        except Exception as e:
            print(f"    ❌ Error: {e}")
        
        # Small delay between requests
        if i < 2:
            time.sleep(1)
    
    # Test 5: Direct NFT fetching to test caching
    print("\n🔄 Test 5: Direct NFT fetching (testing cache)")
    start_time = time.time()
    try:
        nfts = get_wallet_nfts_by_collection(wallet_address, collection_id)
        end_time = time.time()
        
        print(f"⏱️ First fetch time: {end_time - start_time:.2f}s")
        print(f"📊 NFTs found: {len(nfts) if nfts else 0}")
        
        # Second fetch should be faster due to caching
        start_time = time.time()
        nfts_cached = get_wallet_nfts_by_collection(wallet_address, collection_id)
        end_time = time.time()
        
        print(f"⏱️ Cached fetch time: {end_time - start_time:.2f}s")
        print(f"📊 Cached NFTs found: {len(nfts_cached) if nfts_cached else 0}")
        
        if nfts and nfts_cached and len(nfts) == len(nfts_cached):
            print("✅ Cache test: PASSED (same results, faster response)")
        else:
            print("❌ Cache test: FAILED (different results)")
            
    except Exception as e:
        print(f"❌ Error in cache test: {e}")
    
    print("\n" + "=" * 60)
    print("🎯 Local testing completed! Check results above.")

if __name__ == "__main__":
    test_local_optimized() 