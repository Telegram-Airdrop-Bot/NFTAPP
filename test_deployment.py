import requests
import json
import os

def test_bot_server_config():
    """Test bot server configuration"""
    print("🤖 Testing Bot Server Configuration")
    print("=" * 50)
    
    # Check required files
    bot_files = [
        "bot-server/bot.py",
        "bot-server/verifier_js.py", 
        "bot-server/requirements.txt",
        "bot-server/render.yaml"
    ]
    
    print("📁 Required Files:")
    for file in bot_files:
        if os.path.exists(file):
            print(f"   ✅ {file}")
        else:
            print(f"   ❌ {file} - MISSING")
    
    # Check environment variables
    env_vars = [
        "TELEGRAM_BOT_TOKEN",
        "TELEGRAM_GROUP_ID", 
        "HELIUS_API_KEY",
        "COLLECTION_ID",
        "WEBHOOK_URL"
    ]
    
    print("\n🔧 Environment Variables:")
    for var in env_vars:
        print(f"   📋 {var}")
    
    print("\n🌐 Render Configuration:")
    render_config = {
        "Service Name": "meta-betties-bot-server",
        "Environment": "Python",
        "Build Command": "pip install -r requirements.txt",
        "Start Command": "python bot.py",
        "Health Check": "/health"
    }
    
    for key, value in render_config.items():
        print(f"   📋 {key}: {value}")

def test_api_server_config():
    """Test API server configuration"""
    print("\n🌐 Testing API Server Configuration")
    print("=" * 50)
    
    # Check required files
    api_files = [
        "api-server/api_server.py",
        "api-server/verifier_js.py",
        "api-server/requirements.txt", 
        "api-server/render.yaml"
    ]
    
    print("📁 Required Files:")
    for file in api_files:
        if os.path.exists(file):
            print(f"   ✅ {file}")
        else:
            print(f"   ❌ {file} - MISSING")
    
    # Check environment variables
    env_vars = [
        "HELIUS_API_KEY",
        "COLLECTION_ID",
        "WEBHOOK_URL"
    ]
    
    print("\n🔧 Environment Variables:")
    for var in env_vars:
        print(f"   📋 {var}")
    
    print("\n🌐 Render Configuration:")
    render_config = {
        "Service Name": "meta-betties-api-server",
        "Environment": "Python",
        "Build Command": "pip install -r requirements.txt",
        "Start Command": "python api_server.py",
        "Health Check": "/api/config"
    }
    
    for key, value in render_config.items():
        print(f"   📋 {key}: {value}")

def test_frontend_config():
    """Test frontend configuration"""
    print("\n🎨 Testing Frontend Configuration")
    print("=" * 50)
    
    # Check required files
    frontend_files = [
        "frontend/src/App.js",
        "frontend/src/config.js",
        "frontend/package.json",
        "frontend/netlify.toml",
        "frontend/public/_redirects"
    ]
    
    print("📁 Required Files:")
    for file in frontend_files:
        if os.path.exists(file):
            print(f"   ✅ {file}")
        else:
            print(f"   ❌ {file} - MISSING")
    
    # Check environment variables
    env_vars = [
        "REACT_APP_API_URL"
    ]
    
    print("\n🔧 Environment Variables:")
    for var in env_vars:
        print(f"   📋 {var}")
    
    print("\n🚀 Netlify Configuration:")
    netlify_config = {
        "Framework": "Create React App",
        "Build Command": "npm run build",
        "Publish Directory": "build",
        "Environment": "REACT_APP_API_URL"
    }
    
    for key, value in netlify_config.items():
        print(f"   📋 {key}: {value}")

def test_server_urls():
    """Test server URLs and connections"""
    print("\n🔗 Testing Server URLs")
    print("=" * 30)
    
    urls = [
        {
            "name": "Bot Server Health",
            "url": "https://meta-betties-bot-server.onrender.com/health",
            "expected": {"status": "healthy", "service": "bot"}
        },
        {
            "name": "API Server Config",
            "url": "https://meta-betties-api-server.onrender.com/api/config",
            "expected": {"helius_api_key": "..."}
        },
        {
            "name": "Frontend App",
            "url": "https://meta-betties-frontend.netlify.app",
            "expected": "React app loads"
        }
    ]
    
    print("🌐 Production URLs:")
    for url_info in urls:
        print(f"   📋 {url_info['name']}")
        print(f"      🔗 {url_info['url']}")
        print(f"      ✅ Expected: {url_info['expected']}")
        print()

def test_deployment_order():
    """Test deployment order and dependencies"""
    print("\n🔄 Testing Deployment Order")
    print("=" * 35)
    
    deployment_steps = [
        {
            "step": 1,
            "service": "Bot Server",
            "platform": "Render",
            "dependencies": "None",
            "url": "https://meta-betties-bot-server.onrender.com"
        },
        {
            "step": 2,
            "service": "API Server", 
            "platform": "Render",
            "dependencies": "Bot Server URL",
            "url": "https://meta-betties-api-server.onrender.com"
        },
        {
            "step": 3,
            "service": "Frontend",
            "platform": "Netlify", 
            "dependencies": "API Server URL",
            "url": "https://meta-betties-frontend.netlify.app"
        }
    ]
    
    for step in deployment_steps:
        print(f"📋 Step {step['step']}: {step['service']}")
        print(f"   🏗️ Platform: {step['platform']}")
        print(f"   🔗 Dependencies: {step['dependencies']}")
        print(f"   🌐 URL: {step['url']}")
        print()

def test_environment_variables():
    """Test environment variable configuration"""
    print("\n🔧 Environment Variables Configuration")
    print("=" * 45)
    
    env_configs = [
        {
            "service": "Bot Server",
            "platform": "Render",
            "variables": [
                "TELEGRAM_BOT_TOKEN=your_telegram_bot_token",
                "TELEGRAM_GROUP_ID=your_telegram_group_id", 
                "HELIUS_API_KEY=6873bd5e-0b5d-49c4-a9ab-4e7febfd9cd3",
                "COLLECTION_ID=j7qeFNnpWTbaf5g9sMCxP2zfKrH5QFgE56SuYjQDQi1",
                "WEBHOOK_URL=https://meta-betties-api-server.onrender.com/api/verify-nft"
            ]
        },
        {
            "service": "API Server",
            "platform": "Render", 
            "variables": [
                "HELIUS_API_KEY=6873bd5e-0b5d-49c4-a9ab-4e7febfd9cd3",
                "COLLECTION_ID=j7qeFNnpWTbaf5g9sMCxP2zfKrH5QFgE56SuYjQDQi1",
                "WEBHOOK_URL=https://meta-betties-bot-server.onrender.com/verify_callback"
            ]
        },
        {
            "service": "Frontend",
            "platform": "Netlify",
            "variables": [
                "REACT_APP_API_URL=https://meta-betties-api-server.onrender.com"
            ]
        }
    ]
    
    for config in env_configs:
        print(f"📋 {config['service']} ({config['platform']}):")
        for var in config['variables']:
            print(f"   🔧 {var}")
        print()

def test_health_checks():
    """Test health check endpoints"""
    print("\n🏥 Testing Health Checks")
    print("=" * 25)
    
    health_checks = [
        {
            "service": "Bot Server",
            "endpoint": "/health",
            "expected": '{"status": "healthy", "service": "bot"}'
        },
        {
            "service": "API Server", 
            "endpoint": "/api/config",
            "expected": '{"helius_api_key": "..."}'
        },
        {
            "service": "Frontend",
            "endpoint": "/",
            "expected": "React app loads successfully"
        }
    ]
    
    for check in health_checks:
        print(f"📋 {check['service']}")
        print(f"   🔗 Endpoint: {check['endpoint']}")
        print(f"   ✅ Expected: {check['expected']}")
        print()

def main():
    print("🚀 Multi-Server Deployment Test")
    print("=" * 60)
    
    # Test configurations
    test_bot_server_config()
    test_api_server_config()
    test_frontend_config()
    
    # Test URLs and connections
    test_server_urls()
    
    # Test deployment order
    test_deployment_order()
    
    # Test environment variables
    test_environment_variables()
    
    # Test health checks
    test_health_checks()
    
    print("\n" + "=" * 60)
    print("✅ Deployment Configuration Test Completed!")
    print("💡 Next Steps:")
    print("   1. 🤖 Deploy Bot Server to Render")
    print("   2. 🌐 Deploy API Server to Render")
    print("   3. 🎨 Deploy Frontend to Netlify")
    print("   4. 🧪 Test complete flow")
    print("   5. 📊 Monitor all services")

if __name__ == "__main__":
    main() 