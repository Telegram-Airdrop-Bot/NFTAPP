# NFT Verification Telegram Bot

A Telegram bot that automatically verifies NFT ownership when users join groups. Users must have at least 1 NFT in their Solana wallet to stay in the group.

## Features

### 🔐 Automatic NFT Verification
- **Welcome Message**: When users join a group, they receive a welcome message with a verification link
- **Verification Link**: Users click the link to connect their Solana wallet and verify NFT ownership
- **Automatic Removal**: Users without sufficient NFTs are automatically removed from the group
- **Timeout System**: Users have 5 minutes to complete verification before being removed

### 💰 Wallet Analysis
- **SOL Balance**: Check SOL balance of any wallet
- **Token Holdings**: View token holdings count
- **NFT Count**: Check NFT ownership for specific collections

### 🛠️ Admin Commands
- **Status**: View current verification status and pending verifications
- **Cleanup**: Remove expired verification sessions

## Setup Instructions

### 1. Prerequisites
- Python 3.8+
- Telegram Bot Token (from @BotFather)
- Helius API Key (for Solana blockchain data)

### 2. Installation
```bash
pip install python-telegram-bot requests
```

### 3. Configuration
Edit the configuration variables in `nft.py`:

```python
# Replace with your actual API keys
HELIUS_API_KEY = "your_helius_api_key"
TELEGRAM_BOT_TOKEN = "your_telegram_bot_token"

# Verification settings
VERIFICATION_LINK = "https://your-domain.com/verification.html"
MIN_NFT_REQUIRED = 1  # Minimum NFTs required
VERIFICATION_TIMEOUT = 300  # 5 minutes timeout
```

### 4. Deploy Verification Website
1. Upload `verification.html` to your web server
2. Update `VERIFICATION_LINK` in the bot configuration
3. Ensure the website can communicate with your bot (webhook setup)

### 5. Bot Permissions
Make sure your bot has these permissions in the group:
- **Ban Users**: To remove unverified users
- **Send Messages**: To send welcome and status messages
- **Read Messages**: To monitor group activity

## Usage

### For Users
1. **Join Group**: When you join a group with this bot, you'll receive a welcome message
2. **Click Verification Link**: Click the verification link in the welcome message
3. **Connect Wallet**: Connect your Solana wallet (Phantom recommended)
4. **Verify NFTs**: The system will check if you have at least 1 NFT
5. **Stay or Leave**: If verified, you stay; if not, you're automatically removed

### For Admins
- `/status` - View verification statistics
- `/cleanup` - Remove expired verification sessions
- `/start` - Start manual wallet checking

### Manual Wallet Checking
Users can also manually check wallets:
```
/start
```
Then send a wallet address like:
```
EFwPVHhY6vH64MsMDx9ub8Edn4ktYYBcgqNYki1R3rmE
```

## How It Works

### 1. User Joins Group
```python
# Bot detects user join event
async def handle_user_joined(update, context, user, chat):
    # Send welcome message with verification link
    # Create verification session
    # Schedule timeout check
```

### 2. Verification Process
```python
# User clicks verification link
# Connects Solana wallet
# Bot checks NFT ownership via Helius API
async def verify_wallet_nft_ownership(wallet_address, user_id, chat_id, verification_id):
    # Get NFTs from wallet
    # Check if count >= MIN_NFT_REQUIRED
    # Update verification status
```

### 3. Automatic Management
```python
# If verified: User stays in group
# If not verified: User removed from group
# If timeout: User removed from group
```

## API Integration

### Helius API
The bot uses Helius API to:
- Check SOL balance
- Get token holdings
- Verify NFT ownership

### Telegram Bot API
- Handle group member updates
- Send messages
- Manage user permissions

## Security Features

- **Verification Timeout**: Users must verify within 5 minutes
- **Session Management**: Each verification has a unique session ID
- **Automatic Cleanup**: Expired sessions are automatically removed
- **Admin Controls**: Only admins can view status and cleanup

## Customization

### Change Minimum NFTs Required
```python
MIN_NFT_REQUIRED = 2  # Require 2 NFTs instead of 1
```

### Change Verification Timeout
```python
VERIFICATION_TIMEOUT = 600  # 10 minutes instead of 5
```

### Add Collection Filter
```python
# In verify_wallet_nft_ownership function
nfts = get_wallet_nfts_by_collection(wallet_address, "specific_collection_id")
```

### Custom Welcome Message
Edit the welcome message in `handle_user_joined()` function.

## Troubleshooting

### Common Issues

1. **Bot not responding to joins**
   - Check bot permissions in group
   - Ensure bot is added to group

2. **Verification link not working**
   - Check VERIFICATION_LINK configuration
   - Ensure website is accessible

3. **API errors**
   - Verify Helius API key is valid
   - Check API rate limits

4. **Users not being removed**
   - Check bot has "Ban Users" permission
   - Verify timeout settings

### Debug Commands
```python
# Add to main() function for debugging
print(f"🔍 Debug: Pending verifications: {len(pending_verifications)}")
```

## File Structure

```
├── nft.py                 # Main bot code
├── verification.html      # Verification website
├── README.md             # This file
└── requirements.txt      # Python dependencies
```

## Dependencies

```txt
python-telegram-bot>=20.0
requests>=2.25.0
```

## License

This project is open source. Feel free to modify and distribute.

## Support

For issues or questions:
1. Check the troubleshooting section
2. Review bot logs for error messages
3. Verify API keys and permissions
4. Test with a small group first

---

**Note**: This bot requires users to have Phantom wallet or similar Solana wallet installed to complete verification. 