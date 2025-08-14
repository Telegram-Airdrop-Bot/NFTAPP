import requests
import json

def test_wallet_nfts():
    """Test NFT detection for the specific wallet"""
    wallet_address = "EFwPVHhY6vH64MsMDx9ub8Edn4ktYYBcgqNYki1R3rmE"
    collection_id = "j7qeFNnpWTbaf5g9sMCxP2zfKrH5QFgE56SuYjQDQi1"  # Default collection ID
    
    print(f"🔍 Testing wallet: {wallet_address}")
    print(f"🎯 Collection ID: {collection_id}")
    print("=" * 50)
    
    # Using Helius DAS API
    url = "https://mainnet.helius-rpc.com/?api-key=6873bd5e-0b5d-49c4-a9ab-4e7febfd9cd3"
    payload = {
        "jsonrpc": "2.0",
        "id": "my-id",
        "method": "searchAssets",
        "params": {
            "ownerAddress": wallet_address
        }
    }
    
    try:
        print("📤 Fetching all assets...")
        response = requests.post(url, json=payload, timeout=30)
        print(f"📊 Response Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            
            if "result" in data and "items" in data["result"]:
                all_items = data["result"]["items"]
                print(f"📦 Total items received: {len(all_items)}")
                
                # Show first 5 items for debugging
                print("\n🔍 First 5 items:")
                for i, item in enumerate(all_items[:5]):
                    content = item.get("content", {})
                    metadata = content.get("metadata", {})
                    token_standard = metadata.get("token_standard", "Unknown")
                    interface = item.get("interface", "Unknown")
                    name = metadata.get("name", "Unknown")
                    
                    # Check grouping for collection
                    grouping = item.get("grouping", [])
                    collection = grouping[0].get("group_value", "Unknown") if grouping else "Unknown"
                    
                    print(f"  Item {i+1}:")
                    print(f"    Name: {name}")
                    print(f"    Token Standard: {token_standard}")
                    print(f"    Interface: {interface}")
                    print(f"    Collection: {collection}")
                    print(f"    Is Meta Betties: {'✅' if collection == collection_id else '❌'}")
                    print()
                
                # Filter for NFTs
                nfts = []
                for item in all_items:
                    content = item.get("content", {})
                    metadata = content.get("metadata", {})
                    token_standard = metadata.get("token_standard", "")
                    
                    # Check if it's an NFT
                    is_nft = False
                    if token_standard in ["NonFungible", "non-fungible", "NONFUNGIBLE"]:
                        is_nft = True
                    elif item.get("interface") in ["V1_NFT", "MplCoreAsset"]:
                        is_nft = True
                    elif content.get("files") or metadata.get("name") or metadata.get("symbol"):
                        is_nft = True
                    
                    if is_nft:
                        nfts.append(item)
                
                print(f"🎨 Total NFTs found: {len(nfts)}")
                
                # Check Meta Betties collection specifically
                meta_betties_nfts = []
                for nft in nfts:
                    grouping = nft.get("grouping", [])
                    if grouping and grouping[0].get("group_value") == collection_id:
                        meta_betties_nfts.append(nft)
                
                print(f"🎯 Meta Betties NFTs found: {len(meta_betties_nfts)}")
                
                if meta_betties_nfts:
                    print("\n✅ Meta Betties NFTs:")
                    for i, nft in enumerate(meta_betties_nfts[:3]):
                        metadata = nft.get("content", {}).get("metadata", {})
                        name = metadata.get("name", "Unknown")
                        print(f"  {i+1}. {name}")
                else:
                    print("\n❌ No Meta Betties NFTs found")
                
                # Show all collections
                collections = {}
                for nft in nfts:
                    grouping = nft.get("grouping", [])
                    if grouping:
                        collection = grouping[0].get("group_value", "Unknown")
                        collections[collection] = collections.get(collection, 0) + 1
                
                print(f"\n📊 All NFT Collections:")
                for collection, count in sorted(collections.items(), key=lambda x: x[1], reverse=True):
                    is_meta_betties = "✅ Meta Betties" if collection == collection_id else ""
                    print(f"  {collection}: {count} NFTs {is_meta_betties}")
                
            else:
                print("❌ No items found in response")
                
        else:
            print(f"❌ API request failed: {response.status_code}")
            print(f"Response: {response.text}")
            
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    test_wallet_nfts() 