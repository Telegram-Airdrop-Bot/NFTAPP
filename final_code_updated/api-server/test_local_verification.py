from verifier_python import has_nft, get_wallet_nfts_by_collection

def test_local_collection_verification():
    """Test collection-specific NFT verification locally"""
    wallet_address = "EFwPVHhY6vH64MsMDx9ub8Edn4ktYYBcgqNYki1R3rmE"
    collection_id = "j7qeFNnpWTbaf5g9sMCxP2zfKrH5QFgE56SuYjQDQi1"  # Meta Betties
    
    print(f"🔍 Testing Local Collection-Specific NFT Verification")
    print(f"💰 Wallet: {wallet_address}")
    print(f"🎯 Collection: {collection_id}")
    print("=" * 50)
    
    # Test 1: General NFT verification (no collection filter)
    print("\n🔄 Test 1: General NFT verification (any NFT)")
    has_nft_general, count_general = has_nft(wallet_address)
    print(f"📊 Result: has_nft={has_nft_general}, count={count_general}")
    
    if has_nft_general:
        print("✅ General verification: PASSED")
    else:
        print("❌ General verification: FAILED")
    
    # Test 2: Collection-specific verification
    print("\n🔄 Test 2: Collection-specific verification (Meta Betties)")
    has_nft_collection, count_collection = has_nft(wallet_address, collection_id)
    print(f"📊 Result: has_nft={has_nft_collection}, count={count_collection}")
    
    if has_nft_collection:
        print("✅ Collection verification: PASSED")
    else:
        print("❌ Collection verification: FAILED")
    
    # Test 3: Wrong collection verification
    print("\n🔄 Test 3: Wrong collection verification")
    has_nft_wrong, count_wrong = has_nft(wallet_address, "wrong_collection_id")
    print(f"📊 Result: has_nft={has_nft_wrong}, count={count_wrong}")
    
    if has_nft_wrong:
        print("✅ Wrong collection verification: PASSED (unexpected)")
    else:
        print("❌ Wrong collection verification: FAILED (expected)")
    
    # Test 4: Direct NFT fetching
    print("\n🔄 Test 4: Direct NFT fetching by collection")
    nfts_general = get_wallet_nfts_by_collection(wallet_address)
    nfts_collection = get_wallet_nfts_by_collection(wallet_address, collection_id)
    nfts_wrong = get_wallet_nfts_by_collection(wallet_address, "wrong_collection_id")
    
    print(f"📊 General NFTs: {len(nfts_general) if nfts_general else 0}")
    print(f"📊 Meta Betties NFTs: {len(nfts_collection) if nfts_collection else 0}")
    print(f"📊 Wrong collection NFTs: {len(nfts_wrong) if nfts_wrong else 0}")

if __name__ == "__main__":
    test_local_collection_verification() 