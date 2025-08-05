// Configuration file for redirect URLs and settings

export const CONFIG = {
  // Telegram Group URLs
  TELEGRAM_GROUPS: {
    PRIVATE_KEY: 'https://t.me/MetaBettiesPrivateKey', // Exclusive group for NFT holders
    MAIN_GROUP: 'https://t.me/bugsfixinggroup', // Main group for everyone
    SUPPORT: 'https://t.me/MetaBettiesSupport' // Support group
  },
  
  // Redirect Settings
  REDIRECT: {
    SUCCESS_DELAY: 3000, // Delay before redirect after successful verification (3 seconds)
    ERROR_DELAY: 3000, // Delay before showing error message (3 seconds)
    ENABLE_AUTO_REDIRECT: true // Enable automatic redirect after verification
  },
  
  // Verification Messages
  MESSAGES: {
    SUCCESS: '✅ Verification successful! You have {count} NFTs and now have access to the exclusive Telegram group.',
    ERROR: '❌ Required NFT not found in your wallet. Access denied.',
    REDIRECTING: '🔄 Redirecting to Telegram group...',
    ACCESS_DENIED: '❌ Access denied. You will be redirected to the main group.'
  },
  
  // API Settings
  API: {
    BASE_URL: process.env.REACT_APP_API_URL || 'https://api-server-wcjc.onrender.com',
    TIMEOUT: 30000 // 30 seconds timeout
  }
};


export default CONFIG; 
