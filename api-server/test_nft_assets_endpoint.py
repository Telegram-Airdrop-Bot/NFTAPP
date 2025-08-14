import requests
import json

def test_nft_assets_endpoint():
    """Test the NFT assets endpoint for a specific wallet"""
    wallet_address = "BWha64zgbukDCVTAK9L9gGReNJaQ9f7faa2ZnBMAr8Tt"
    api_key = "6873bd5e-0b5d-49c4-a9ab-4e7febfd9cd3"
    
    url = f"https://api-server-wcjc.onrender.com/api/addresses/{wallet_address}/nft-assets?api-key={api_key}"
    
    print(f"🔍 Testing NFT Assets Endpoint")
    print(f"💰 Wallet: {wallet_address}")
    print(f"🔑 API Key: {api_key[:10]}...")
    print(f"🌐 URL: {url}")
    print("=" * 60)
    
    try:
        print("🔄 Making request to NFT assets endpoint...")
        response = requests.get(url, timeout=30)
        
        print(f"📊 Response Status: {response.status_code}")
        print(f"📄 Response Headers: {dict(response.headers)}")
        
        if response.status_code == 200:
            try:
                data = response.json()
                print(f"✅ Success! Response data:")
                print(f"📦 Data type: {type(data)}")
                
                if isinstance(data, list):
                    print(f"🎨 NFTs found: {len(data)}")
                    if data:
                        print(f"📋 First NFT sample:")
                        print(json.dumps(data[0], indent=2))
                elif isinstance(data, dict):
                    print(f"📋 Response structure:")
                    print(json.dumps(data, indent=2))
                else:
                    print(f"📄 Raw response: {data}")
                    
            except json.JSONDecodeError as e:
                print(f"❌ JSON decode error: {e}")
                print(f"📄 Raw response text: {response.text[:500]}...")
                
        else:
            print(f"❌ Request failed with status: {response.status_code}")
            print(f"📄 Error response: {response.text}")
            
    except requests.exceptions.Timeout:
        print("⏰ Request timed out after 30 seconds")
    except requests.exceptions.RequestException as e:
        print(f"❌ Request error: {e}")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")

if __name__ == "__main__":
    test_nft_assets_endpoint() 