import requests
import json

def test_api_server():
    """Test the API server"""
    url = "https://api-server-wcjc.onrender.com/api/verify-nft"
    
    test_data = {
        "wallet_address": "9WzDXwBbmkg8ZTbNMqUxvQRAyrZzDsGYdLVL9zYtAWWM",
        "tg_id": "123456789"
    }
    
    print("🧪 Testing API Server...")
    print(f"📤 URL: {url}")
    print(f"📦 Data: {json.dumps(test_data, indent=2)}")
    
    try:
        response = requests.post(url, json=test_data, timeout=30)
        print(f"📊 Status Code: {response.status_code}")
        print(f"📄 Response: {json.dumps(response.json(), indent=2)}")
        
        if response.status_code == 200:
            print("✅ API Server is working!")
        else:
            print("❌ API Server returned error")
            
    except Exception as e:
        print(f"❌ Error testing API: {e}")

if __name__ == "__main__":
    test_api_server() 