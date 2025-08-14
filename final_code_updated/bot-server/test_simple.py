import os
from dotenv import load_dotenv

load_dotenv()

def test_environment():
    """Test environment variables"""
    print("🧪 Testing Bot Server Environment...")
    print("=" * 50)
    
    # Check required variables
    bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
    group_id = os.getenv("TELEGRAM_GROUP_ID")
    admin_chat_id = os.getenv("ADMIN_CHAT_ID")
    admin_notifications = os.getenv("ADMIN_NOTIFICATIONS", "true").lower() == "true"
    
    print(f"🤖 BOT_TOKEN: {'✅ Set' if bot_token else '❌ Missing'}")
    print(f"👥 GROUP_ID: {'✅ Set' if group_id else '❌ Missing'}")
    print(f"📢 ADMIN_CHAT_ID: {'✅ Set' if admin_chat_id else '❌ Missing'}")
    print(f"🔔 ADMIN_NOTIFICATIONS: {'✅ Enabled' if admin_notifications else '❌ Disabled'}")
    
    if not bot_token:
        print("\n❌ TELEGRAM_BOT_TOKEN is required!")
    if not group_id:
        print("\n❌ TELEGRAM_GROUP_ID is required!")
    if not admin_chat_id:
        print("\n❌ ADMIN_CHAT_ID is required for notifications!")
    
    print("\n" + "=" * 50)

if __name__ == "__main__":
    test_environment() 