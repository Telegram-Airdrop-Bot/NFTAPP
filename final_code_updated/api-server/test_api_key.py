#!/usr/bin/env python3
"""
Test script to verify Helius API key configuration
"""

import os
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_api_key():
    """Test the Helius API key configuration"""
    
    print("🔍 Testing Helius API Key Configuration")
    print("=" * 50)
    
    # Check environment variable
    api_key = os.getenv("HELIUS_API_KEY")
    
    if not api_key:
        print("❌ HELIUS_API_KEY not found in environment variables!")
        print("💡 Please set HELIUS_API_KEY in your environment")
        return False
    
    print(f"✅ HELIUS_API_KEY found (length: {len(api_key)})")
    print(f"🔑 API Key preview: {api_key[:8]}...{api_key[-4:]}")
    
    # Test the API key with a simple request
    test_url = f"https://api.helius.xyz/v0/addresses/11111111111111111111111111111112/balances?api-key={api_key}"
    
    try:
        print(f"\n🧪 Testing API key with Helius...")
        response = requests.get(test_url, timeout=10)
        
        if response.status_code == 200:
            print("✅ API key is valid and working!")
            data = response.json()
            print(f"📊 Test response: {data}")
            return True
        else:
            print(f"❌ API key test failed with status {response.status_code}")
            print(f"📄 Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error testing API key: {e}")
        return False

def test_config_endpoint():
    """Test the local config endpoint"""
    
    print(f"\n🔍 Testing Local Config Endpoint")
    print("=" * 50)
    
    try:
        response = requests.get("http://localhost:5001/api/config")
        
        if response.status_code == 200:
            config = response.json()
            print("✅ Config endpoint working")
            print(f"📊 Config: {config}")
            
            if config.get("api_key_status") == "loaded":
                print("✅ API key status: loaded")
                return True
            else:
                print(f"❌ API key status: {config.get('api_key_status')}")
                return False
        else:
            print(f"❌ Config endpoint failed: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Error testing config endpoint: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Starting API Key Tests...\n")
    
    # Test environment variable
    env_test = test_api_key()
    
    # Test local endpoint
    endpoint_test = test_config_endpoint()
    
    print("\n" + "=" * 50)
    print("📊 Test Results:")
    print(f"  Environment Variable: {'✅ PASS' if env_test else '❌ FAIL'}")
    print(f"  Config Endpoint: {'✅ PASS' if endpoint_test else '❌ FAIL'}")
    
    if env_test and endpoint_test:
        print("\n🎉 All tests passed! API key is properly configured.")
    else:
        print("\n❌ Some tests failed. Please check your configuration.")
        print("\n💡 Troubleshooting:")
        print("  1. Check if HELIUS_API_KEY is set in your environment")
        print("  2. Verify the API key is valid")
        print("  3. Ensure the API server is running on port 5001")
        print("  4. Check server logs for any errors") 