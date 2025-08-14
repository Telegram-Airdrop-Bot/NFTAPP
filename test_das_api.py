import requests
import json

# Test wallet address
WALLET_ADDRESS = "EFwPVHhY6vH64MsMDx9ub8Edn4ktYYBcgqNYki1R3rmE"
HELIUS_API_KEY = "6873bd5e-0b5d-49c4-a9ab-4e7febfd9cd3"
DAS_API_URL = "https://mainnet.helius-rpc.com"

def test_das_api(method, params, description):
    """Test DAS API call and print detailed response"""
    url = f"{DAS_API_URL}/?api-key={HELIUS_API_KEY}"
    payload = {
        "jsonrpc": "2.0",
        "id": "test-id",
        "method": method,
        "params": params
    }
    
    print(f"\n🧪 Testing: {description}")
    print(f"URL: {url}")
    print(f"Payload: {json.dumps(payload, indent=2)}")
    
    try:
        response = requests.post(url, json=payload, timeout=30)
        print(f"Status Code: {response.status_code}")
        print(f"Response Headers: {dict(response.headers)}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Success! Response: {json.dumps(data, indent=2)}")
            
            if "result" in data:
                if "items" in data["result"]:
                    print(f"📊 Found {len(data['result']['items'])} items")
                else:
                    print(f"📊 Result keys: {list(data['result'].keys())}")
            else:
                print(f"❌ No 'result' in response")
        else:
            print(f"❌ Error Response: {response.text}")
            
    except Exception as e:
        print(f"❌ Exception: {e}")

def main():
    print("🔍 Testing Helius DAS API")
    print("=" * 60)
    
    # Test token search
    token_params = {
        "ownerAddress": WALLET_ADDRESS,
        "tokenType": ["fungible"],
        "displayOptions": {
            "showZeroBalance": False
        }
    }
    test_das_api("searchAssets", token_params, "Token Search")
    
    # Test NFT search
    nft_params = {
        "ownerAddress": WALLET_ADDRESS,
        "tokenType": ["non-fungible"],
        "displayOptions": {
            "showZeroBalance": False
        }
    }
    test_das_api("searchAssets", nft_params, "NFT Search")
    
    # Test with different parameters
    print("\n" + "=" * 60)
    print("Testing Alternative Parameters:")
    
    # Test without tokenType filter
    simple_params = {
        "ownerAddress": WALLET_ADDRESS
    }
    test_das_api("searchAssets", simple_params, "Simple Asset Search")
    
    # Test getAssetsByOwner method
    owner_params = {
        "ownerAddress": WALLET_ADDRESS
    }
    test_das_api("getAssetsByOwner", owner_params, "Get Assets By Owner")

if __name__ == "__main__":
    main() 