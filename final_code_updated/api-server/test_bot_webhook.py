import requests
import json

def test_bot_webhook():
    """Test the bot server webhook"""
    url = "https://bot-server-kem4.onrender.com/verify_callback"
    
    test_data = {
        "tg_id": "123456789",
        "has_nft": True,
        "username": "test_user",
        "nft_count": 45,
        "wallet_address": "EFwPVHhY6vH64MsMDx9ub8Edn4ktYYBcgqNYki1R3rmE"
    }
    
    print("🧪 Testing Bot Server Webhook...")
    print(f"📤 URL: {url}")
    print(f"📦 Data: {json.dumps(test_data, indent=2)}")
    
    try:
        response = requests.post(url, json=test_data, timeout=30)
        print(f"📊 Status Code: {response.status_code}")
        print(f"📄 Response: {response.text}")
        
        if response.status_code == 200:
            print("✅ Bot Server Webhook is working!")
        else:
            print("❌ Bot Server Webhook returned error")
            
    except Exception as e:
        print(f"❌ Error testing bot webhook: {e}")

def test_bot_health():
    """Test bot server health endpoint"""
    url = "https://bot-server-kem4.onrender.com/health"
    
    print("\n🏥 Testing Bot Server Health...")
    print(f"📤 URL: {url}")
    
    try:
        response = requests.get(url, timeout=30)
        print(f"📊 Status Code: {response.status_code}")
        print(f"📄 Response: {response.text}")
        
        if response.status_code == 200:
            print("✅ Bot Server is healthy!")
        else:
            print("❌ Bot Server health check failed")
            
    except Exception as e:
        print(f"❌ Error testing bot health: {e}")

if __name__ == "__main__":
    test_bot_health()
    test_bot_webhook() 