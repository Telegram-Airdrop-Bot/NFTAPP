import requests
import json

def test_verification_flow():
    """Test the complete verification flow"""
    wallet_address = "EFwPVHhY6vH64MsMDx9ub8Edn4ktYYBcgqNYki1R3rmE"
    tg_id = "123456789"
    
    print(f"🔍 Testing Complete Verification Flow")
    print(f"💰 Wallet: {wallet_address}")
    print(f"👤 Telegram ID: {tg_id}")
    print("=" * 50)
    
    # Step 1: Test API Server
    print("\n🔄 Step 1: Testing API Server")
    api_data = {
        "wallet_address": wallet_address,
        "tg_id": tg_id
    }
    
    try:
        api_response = requests.post(
            "https://api-server-wcjc.onrender.com/api/verify-nft",
            json=api_data,
            timeout=30
        )
        print(f"📊 API Status: {api_response.status_code}")
        
        if api_response.status_code == 200:
            api_result = api_response.json()
            print(f"📄 API Result: {json.dumps(api_result, indent=2)}")
            
            if api_result.get("has_nft"):
                print("✅ API verification: PASSED")
            else:
                print("❌ API verification: FAILED")
        else:
            print(f"❌ API error: {api_response.text}")
            
    except Exception as e:
        print(f"❌ API error: {e}")
    
    # Step 2: Test Bot Server Webhook
    print("\n🔄 Step 2: Testing Bot Server Webhook")
    webhook_data = {
        "tg_id": tg_id,
        "has_nft": True,
        "username": "test_user",
        "nft_count": 251,
        "wallet_address": wallet_address
    }
    
    try:
        webhook_response = requests.post(
            "https://bot-server-kem4.onrender.com/verify_callback",
            json=webhook_data,
            timeout=30
        )
        print(f"📊 Webhook Status: {webhook_response.status_code}")
        print(f"📄 Webhook Response: {webhook_response.text}")
        
        if webhook_response.status_code == 200:
            print("✅ Bot server webhook: PASSED")
        else:
            print("❌ Bot server webhook: FAILED")
            
    except Exception as e:
        print(f"❌ Webhook error: {e}")
    
    # Step 3: Test Frontend URL
    print("\n🔄 Step 3: Testing Frontend URL")
    frontend_url = f"https://admin-q2j7.onrender.com/?tg_id={tg_id}"
    print(f"🔗 Frontend URL: {frontend_url}")
    print("📋 Copy this URL and test in browser")
    
    # Step 4: Test Telegram Group URLs
    print("\n🔄 Step 4: Testing Telegram Group URLs")
    private_group = "https://t.me/MetaBettiesPrivateKey"
    main_group = "https://t.me/MetaBettiesMain"
    
    print(f"🔗 Private Group: {private_group}")
    print(f"🔗 Main Group: {main_group}")
    print("📋 Test these URLs in browser")

if __name__ == "__main__":
    test_verification_flow() 