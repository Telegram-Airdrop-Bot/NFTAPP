import sys
import os
import time
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from verifier_python import has_nft, get_wallet_nfts_by_collection

def test_wallet_locally():
    """Test the wallet locally to see if it has NFTs"""
    wallet_address = "BWha64zgbukDCVTAK9L9gGReNJaQ9f7faa2ZnBMAr8Tt"
    collection_id = "j7qeFNnpWTbaf5g9sMCxP2zfKrH5QFgE56SuYjQDQi1"  # Meta Betties
    
    print(f"🔍 Testing Wallet Locally")
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
    
    # Test 3: Direct NFT fetching
    print("\n🔄 Test 3: Direct NFT fetching")
    start_time = time.time()
    try:
        nfts = get_wallet_nfts_by_collection(wallet_address)
        end_time = time.time()
        
        print(f"⏱️ Fetch time: {end_time - start_time:.2f}s")
        print(f"📊 NFTs found: {len(nfts) if nfts else 0}")
        
        if nfts:
            print(f"📋 First few NFTs:")
            for i, nft in enumerate(nfts[:3]):
                metadata = nft.get("content", {}).get("metadata", {})
                name = metadata.get("name", "Unknown")
                print(f"  {i+1}. {name}")
        else:
            print("❌ No NFTs found")
            
    except Exception as e:
        print(f"❌ Error in direct NFT fetching: {e}")
    
    print("\n" + "=" * 60)
    print("🎯 Local testing completed! Check results above.")

if __name__ == "__main__":
    test_wallet_locally() 