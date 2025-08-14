import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from nft import get_wallet_nfts_by_collection

def test_nft_fixed():
    """Test the fixed NFT detection logic"""
    wallet_address = "EFwPVHhY6vH64MsMDx9ub8Edn4ktYYBcgqNYki1R3rmE"
    collection_id = "j7qeFNnpWTbaf5g9sMCxP2zfKrH5QFgE56SuYjQDQi1"  # Meta Betties
    
    print(f"🔍 Testing fixed NFT detection for wallet: {wallet_address}")
    print(f"🎯 Collection ID: {collection_id}")
    print("=" * 50)
    
    try:
        # Test general NFT detection (no collection filter)
        print("🔄 Testing general NFT detection...")
        nfts_general = get_wallet_nfts_by_collection(wallet_address)
        print(f"General NFTs found: {len(nfts_general) if nfts_general else 0}")
        
        # Test collection-specific detection
        print("\n🔄 Testing collection-specific detection...")
        nfts_collection = get_wallet_nfts_by_collection(wallet_address, collection_id)
        print(f"Meta Betties NFTs found: {len(nfts_collection) if nfts_collection else 0}")
        
        if nfts_collection:
            print("\n✅ Meta Betties NFTs found:")
            for i, nft in enumerate(nfts_collection[:5]):
                metadata = nft.get("content", {}).get("metadata", {})
                name = metadata.get("name", "Unknown")
                print(f"  {i+1}. {name}")
        else:
            print("\n❌ No Meta Betties NFTs found")
            
    except Exception as e:
        print(f"❌ Error testing NFT detection: {e}")

if __name__ == "__main__":
    test_nft_fixed() 