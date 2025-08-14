import requests

def test_bot_health():
    """Test bot server health"""
    url = "https://bot-server-kem4.onrender.com/health"
    
    print("🏥 Testing Bot Server Health...")
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