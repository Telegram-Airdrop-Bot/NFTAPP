import React, { useState, useEffect } from 'react';
import Solflare from '@solflare-wallet/sdk';
import CONFIG from './config';

function App() {
  const [userAddress, setUserAddress] = useState('');
  const [heliusApiKey, setHeliusApiKey] = useState('');
  const [status, setStatus] = useState({ message: 'Connect your wallet to verify NFT ownership', type: 'info' });
  const [showVerification, setShowVerification] = useState(false);
  const [showNFTs, setShowNFTs] = useState(false);
  const [nfts, setNfts] = useState([]);
  const [nftCount, setNftCount] = useState(0);
  const [verificationResult, setVerificationResult] = useState(null);
  const [welcomeMessage, setWelcomeMessage] = useState('Welcome to Meta Betties Private Key - Connect Wallet & Verify Access');
  const [isMobile, setIsMobile] = useState(false);
  const [isConnectingWallet, setIsConnectingWallet] = useState(false);

  const REACT_APP_API_URL = process.env.REACT_APP_API_URL || 'https://api-server-wcjc.onrender.com';
  const tgId = new URLSearchParams(window.location.search).get('tg_id') || 
               new URLSearchParams(window.location.search).get('telegram_id') ||
               new URLSearchParams(window.location.search).get('tgid') ||
               localStorage.getItem('tg_id');

  useEffect(() => {
    loadConfig();
    detectMobileDevice();
    
    // Store Telegram ID in localStorage for persistence
    if (tgId) {
      localStorage.setItem('tg_id', tgId);
    }
    
    if (!tgId) {
      updateStatus('❌ Missing Telegram ID parameter! Please access this page from the Telegram bot link.', 'error');
      console.error('Telegram ID missing from URL:', window.location.search);
    } else {
      console.log('Telegram ID found:', tgId);
      updateStatus('✅ Telegram ID detected. Please connect your wallet to verify NFT ownership.', 'info');
    }

    // Add page visibility listener for mobile wallet detection
    const handleVisibilityChange = () => {
      if (!document.hidden && isMobile) {
        console.log('User returned to app, checking wallet connection...');
        setTimeout(async () => {
          await detectMobileWalletConnection();
        }, 1000);
      }
    };

    document.addEventListener('visibilitychange', handleVisibilityChange);

    return () => {
      document.removeEventListener('visibilitychange', handleVisibilityChange);
    };
  }, [tgId, isMobile]);

  const loadConfig = async () => {
    try {
      const response = await fetch(`${REACT_APP_API_URL}/api/config`);
      const config = await response.json();
      
      console.log('Config loaded:', config);
      
      if (config.api_key_status === 'missing') {
        updateStatus('❌ API configuration error: Helius API key is missing. Please check server setup.', 'error');
        console.error('Helius API key missing from server configuration');
        return;
      }
      
      if (!config.helius_api_key || config.helius_api_key.length < 10) {
        updateStatus('❌ API configuration error: Invalid Helius API key. Please check server setup.', 'error');
        console.error('Invalid Helius API key:', config.helius_api_key);
        return;
      }
      
      setHeliusApiKey(config.helius_api_key);
      console.log('Helius API key loaded successfully, length:', config.helius_api_key.length);
      updateStatus('✅ API configuration loaded successfully. Ready to verify NFT ownership.', 'success');
      
    } catch (error) {
      console.error('Failed to load configuration:', error);
      updateStatus('❌ Failed to load configuration: ' + error.message, 'error');
    }
  };

  const updateStatus = (message, type = 'info') => {
    setStatus({ message, type });
  };

  // Detect mobile device
  const detectMobileDevice = () => {
    const mobileCheck = /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent);
    setIsMobile(mobileCheck);
    console.log('Mobile device detected:', mobileCheck);
  };

  // Detect mobile wallet connection
  const detectMobileWalletConnection = async () => {
    if (!isMobile) return false;
    
    console.log('Detecting mobile wallet connection...');
    
    try {
      let connectedAddress = null;
      let walletName = '';
      
      // Check for connected wallets
      if (window.solana?.isPhantom && window.solana.isConnected) {
        connectedAddress = window.solana.publicKey?.toString();
        walletName = 'Phantom';
      } else if (window.solflare && window.solflare.isConnected) {
        connectedAddress = window.solflare.publicKey?.toString();
        walletName = 'Solflare';
      } else if (window.xnft?.solana && window.xnft.solana.isConnected) {
        connectedAddress = window.xnft.solana.publicKey?.toString();
        walletName = 'Backpack';
      } else if (window.slope && window.slope.isConnected) {
        connectedAddress = window.slope.publicKey?.toString();
        walletName = 'Slope';
      } else if (window.glow && window.glow.isConnected) {
        connectedAddress = window.glow.publicKey?.toString();
        walletName = 'Glow';
      } else if (window.coinbaseWalletSolana && window.coinbaseWalletSolana.isConnected) {
        connectedAddress = window.coinbaseWalletSolana.publicKey?.toString();
        walletName = 'Coinbase';
      }
      
      // Additional checks for wallets without isConnected property
      if (!connectedAddress) {
        if (window.solana?.isPhantom && window.solana.publicKey) {
          connectedAddress = window.solana.publicKey.toString();
          walletName = 'Phantom';
        } else if (window.solflare && window.solflare.publicKey) {
          connectedAddress = window.solflare.publicKey.toString();
          walletName = 'Solflare';
        } else if (window.xnft?.solana && window.xnft.solana.publicKey) {
          connectedAddress = window.xnft.solana.publicKey.toString();
          walletName = 'Backpack';
        } else if (window.slope && window.slope.publicKey) {
          connectedAddress = window.slope.publicKey.toString();
          walletName = 'Slope';
        } else if (window.glow && window.glow.publicKey) {
          connectedAddress = window.glow.publicKey.toString();
          walletName = 'Glow';
        } else if (window.coinbaseWalletSolana && window.coinbaseWalletSolana.publicKey) {
          connectedAddress = window.coinbaseWalletSolana.publicKey.toString();
          walletName = 'Coinbase';
        }
      }
      
      if (connectedAddress) {
        console.log(`Mobile wallet ${walletName} connected:`, connectedAddress);
        setUserAddress(connectedAddress);
        setIsConnectingWallet(false);
        showVerificationSection();
        updateStatus(`✅ ${walletName} wallet connected successfully! Click "Verify NFT Ownership" to continue.`, 'success');
        return true;
      }
      
      return false;
    } catch (error) {
      console.error('Error detecting mobile wallet connection:', error);
      return false;
    }
  };

  // Handle mobile wallet connection
  const handleMobileWalletConnection = async (walletName) => {
    console.log(`Connecting to ${walletName} on mobile...`);
    setIsConnectingWallet(true);
    updateStatus(`Connecting to ${walletName}...`, 'info');
    
    try {
      let connected = false;
      
      // Try to connect based on wallet name
      switch (walletName) {
        case 'Phantom':
          if (window.solana?.isPhantom) {
            const resp = await window.solana.connect();
            if (resp.publicKey) {
              setUserAddress(resp.publicKey.toString());
              connected = true;
            }
          }
          break;
        case 'Solflare':
          if (window.solflare) {
            const wallet = new Solflare();
            await wallet.connect();
            if (wallet.publicKey) {
              setUserAddress(wallet.publicKey.toString());
              connected = true;
            }
          }
          break;
        case 'Backpack':
          if (window.xnft?.solana) {
            const resp = await window.xnft.solana.connect();
            if (resp.publicKey) {
              setUserAddress(resp.publicKey.toString());
              connected = true;
            }
          }
          break;
        case 'Slope':
          if (window.slope) {
            const resp = await window.slope.connect();
            if (resp.publicKey) {
              setUserAddress(resp.publicKey.toString());
              connected = true;
            }
          }
          break;
        case 'Glow':
          if (window.glow) {
            const resp = await window.glow.connect();
            if (resp.publicKey) {
              setUserAddress(resp.publicKey.toString());
              connected = true;
            }
          }
          break;
        case 'Coinbase':
          if (window.coinbaseWalletSolana) {
            const resp = await window.coinbaseWalletSolana.connect();
            if (resp.publicKey) {
              setUserAddress(resp.publicKey.toString());
              connected = true;
            }
          }
          break;
      }
      
      if (connected) {
        setIsConnectingWallet(false);
        showVerificationSection();
        updateStatus(`✅ ${walletName} wallet connected successfully!`, 'success');
      } else {
        // If direct connection fails, try deep linking
        await openWalletApp(walletName);
      }
    } catch (error) {
      console.log(`${walletName} direct connection failed, trying deep link...`, error);
      await openWalletApp(walletName);
    }
  };

  // Open wallet app via deep link
  const openWalletApp = async (walletName) => {
    const userAgent = navigator.userAgent.toLowerCase();
    const isIOS = /iphone|ipad|ipod/.test(userAgent);
    const isAndroid = /android/.test(userAgent);
    
    let appUrl = '';
    let fallbackUrl = '';
    
    // Set up deep links and fallback URLs
    switch (walletName) {
      case 'Phantom':
        appUrl = 'https://phantom.app/ul/browse/';
        fallbackUrl = isIOS ? 'https://apps.apple.com/app/phantom/id1598432977' : 'https://play.google.com/store/apps/details?id=app.phantom';
        break;
      case 'Solflare':
        appUrl = 'https://solflare.com/';
        fallbackUrl = isIOS ? 'https://apps.apple.com/app/solflare/id1580902717' : 'https://play.google.com/store/apps/details?id=com.solflare.mobile';
        break;
      case 'Backpack':
        appUrl = 'https://backpack.app/';
        fallbackUrl = isIOS ? 'https://apps.apple.com/app/backpack/id6443944476' : 'https://play.google.com/store/apps/details?id=app.backpack';
        break;
      case 'Slope':
        appUrl = 'https://slope.finance/';
        fallbackUrl = isIOS ? 'https://apps.apple.com/app/slope-wallet/id1574624530' : 'https://play.google.com/store/apps/details?id=com.slope.finance';
        break;
      case 'Glow':
        appUrl = 'https://glow.app/';
        fallbackUrl = isIOS ? 'https://apps.apple.com/app/glow-wallet/id1635713293' : 'https://play.google.com/store/apps/details?id=com.glow.wallet';
        break;
      case 'Coinbase':
        appUrl = 'https://wallet.coinbase.com/';
        fallbackUrl = isIOS ? 'https://apps.apple.com/app/coinbase-wallet/id1278383455' : 'https://play.google.com/store/apps/details?id=org.toshi';
        break;
    }
    
    updateStatus(`Opening ${walletName} app... Please approve the connection and return to this page.`, 'info');
    
    try {
      const newWindow = window.open(appUrl, '_blank');
      
      setTimeout(() => {
        if (newWindow && !newWindow.closed) {
          updateStatus(`✅ ${walletName} app opened! Please approve the connection and return here.`, 'success');
        } else {
          console.log(`${walletName} app not found, trying fallback...`);
          window.open(fallbackUrl, '_blank');
          updateStatus(`${walletName} app not found. Please install it from the app store and try again.`, 'error');
          setIsConnectingWallet(false);
        }
      }, 2000);
      
    } catch (error) {
      console.error(`Error opening ${walletName}:`, error);
      window.location.href = appUrl;
    }
  };

  const connectPhantom = async () => {
    try {
      console.log('Attempting to connect Phantom wallet...');
      updateStatus('Connecting to Phantom wallet...', 'info');

      if (typeof window.solana === 'undefined') {
        updateStatus('❌ Phantom extension not found. Please install it from https://phantom.app.', 'error');
        return;
      }

      if (!window.solana.isPhantom) {
        updateStatus('❌ Phantom extension not found. Please install it from https://phantom.app.', 'error');
        return;
      }

      const resp = await window.solana.connect();
      const publicKey = resp.publicKey.toString();
      console.log('Phantom public key:', publicKey);
      
      if (publicKey) {
        setUserAddress(publicKey);
        showVerificationSection();
        updateStatus('✅ Phantom wallet connected successfully!', 'success');
      } else {
        throw new Error('No public key received from Phantom');
      }
    } catch (err) {
      console.error('Phantom connection error:', err);
      
      let errorMessage = 'Phantom connection failed';
      
      if (err.code === 4001) {
        errorMessage = '❌ User rejected Phantom wallet connection. Please try again.';
      } else if (err.code === -32002) {
        errorMessage = '❌ Phantom wallet connection already pending. Please check your wallet.';
      } else if (err.code === -32603) {
        errorMessage = '❌ Phantom wallet internal error. Please try refreshing the page.';
      } else if (err.message && err.message.includes('No public key')) {
        errorMessage = '❌ No wallet address received from Phantom. Please try connecting again.';
      } else if (err.message) {
        errorMessage = '❌ Phantom connection failed: ' + err.message;
      }
      
      updateStatus(errorMessage, 'error');
    }
  };

  const connectSolflare = async () => {
    try {
      console.log('Attempting to connect Solflare wallet...');
      updateStatus('Connecting to Solflare wallet...', 'info');

      const wallet = new Solflare();

      wallet.on('connect', () => {
        console.log('Solflare connected:', wallet.publicKey.toString());
      });

      wallet.on('disconnect', () => {
        console.log('Solflare disconnected');
      });

      await wallet.connect();

      if (wallet.isConnected && wallet.publicKey) {
        const publicKey = wallet.publicKey.toString();
        console.log('Solflare connection successful, public key:', publicKey);
        
        if (publicKey && publicKey.length > 0) {
          setUserAddress(publicKey);
          showVerificationSection();
          updateStatus('✅ Solflare wallet connected successfully!', 'success');
        } else {
          throw new Error('No valid wallet address received from Solflare');
        }
      } else {
        throw new Error('Solflare connection failed - wallet not connected');
      }
    } catch (err) {
      console.error('Solflare connection error:', err);
      
      let errorMessage = 'Solflare connection failed';
      
      if (err.message && err.message.includes('No valid wallet address')) {
        errorMessage = '❌ No wallet address received from Solflare. Please try connecting again.';
      } else if (err.message) {
        errorMessage = '❌ Solflare connection failed: ' + err.message;
      }
      
      updateStatus(errorMessage, 'error');
    }
  };

  const connectBackpack = async () => {
    try {
      if (typeof window.xnft === 'undefined') {
        updateStatus('Backpack extension not found. Please install it from https://backpack.app.', 'error');
        return;
      }

      if (!window.xnft.solana) {
        updateStatus('Backpack extension not found. Please install it from https://backpack.app.', 'error');
        return;
      }

      const resp = await window.xnft.solana.connect();
      setUserAddress(resp.publicKey.toString());
      showVerificationSection();
      updateStatus('✅ Backpack wallet connected successfully!', 'success');
    } catch (err) {
      updateStatus('Backpack connection failed: ' + err.message, 'error');
    }
  };

  const connectSlope = async () => {
    try {
      if (typeof window.slope === 'undefined') {
        updateStatus('Slope extension not found. Please install it from https://slope.finance.', 'error');
        return;
      }

      const resp = await window.slope.connect();
      setUserAddress(resp.publicKey.toString());
      showVerificationSection();
      updateStatus('✅ Slope wallet connected successfully!', 'success');
    } catch (err) {
      updateStatus('Slope connection failed: ' + err.message, 'error');
    }
  };

  const connectGlow = async () => {
    try {
      if (typeof window.glow === 'undefined') {
        updateStatus('Glow extension not found. Please install it from https://glow.app.', 'error');
        return;
      }

      const resp = await window.glow.connect();
      setUserAddress(resp.publicKey.toString());
      showVerificationSection();
      updateStatus('✅ Glow wallet connected successfully!', 'success');
    } catch (err) {
      updateStatus('Glow connection failed: ' + err.message, 'error');
    }
  };

  const connectCoinbase = async () => {
    try {
      if (typeof window.coinbaseWalletSolana === 'undefined') {
        updateStatus('Coinbase extension not found. Please install it from https://wallet.coinbase.com.', 'error');
        return;
      }

      const resp = await window.coinbaseWalletSolana.connect();
      setUserAddress(resp.publicKey.toString());
      showVerificationSection();
      updateStatus('✅ Coinbase wallet connected successfully!', 'success');
    } catch (err) {
      updateStatus('Coinbase connection failed: ' + err.message, 'error');
    }
  };

  const showVerificationSection = () => {
    setShowVerification(true);
    setShowNFTs(false);
    updateStatus('Wallet connected successfully! Click "Fetch NFTs & Verify Ownership" to see your collection and verify access.', 'success');
    // Removed automatic NFT fetching - user must click verify button first
  };

  const fetchAndDisplayNFTs = async () => {
    if (!userAddress) return;
    
    if (!heliusApiKey || heliusApiKey.length < 10) {
      updateStatus('❌ API key not configured. Please refresh the page or contact support.', 'error');
      return;
    }
    
    updateStatus('Fetching your NFT collection...', 'info');
    setNfts([]);
    setShowNFTs(true);

    try {
      const url = `${REACT_APP_API_URL}/api/addresses/${userAddress}/nft-assets?api-key=${heliusApiKey}`;
      console.log('Fetching NFTs from:', url.substring(0, 50) + '...');
      
      const res = await fetch(url);
      console.log('NFT fetch response status:', res.status);
      
      if (!res.ok) {
        const errorData = await res.json().catch(() => ({}));
        console.error('NFT fetch error:', errorData);
        
        if (res.status === 400) {
          throw new Error(errorData.details || 'Invalid API key or request parameters');
        } else if (res.status === 500) {
          throw new Error(errorData.details || 'Server error while fetching NFTs');
        } else {
          throw new Error(`Failed to fetch NFTs: ${res.status} ${res.statusText}`);
        }
      }
      
      const nftData = await res.json();
      console.log('NFT data received:', nftData);

      if (nftData && nftData.length > 0) {
        setNfts(nftData);
        setNftCount(nftData.length);
        updateStatus(`Found ${nftData.length} NFTs in your wallet!`, 'success');
      } else {
        setNfts([]);
        setNftCount(0);
        // Don't show error message here - let verification function handle it
        updateStatus('No NFTs found in your wallet.', 'info');
      }
    } catch (e) {
      console.error('Error fetching NFTs:', e);
      setNfts([]);
      setNftCount(0);
      
      let errorMessage = 'Failed to fetch NFTs: ' + e.message;
      if (e.message.includes('Invalid API key')) {
        errorMessage = '❌ API configuration error. Please refresh the page or contact support.';
      } else if (e.message.includes('Server error')) {
        errorMessage = '❌ Server error while fetching NFTs. Please try again later.';
      } else if (e.message.includes('Failed to fetch')) {
        errorMessage = '❌ Network error. Please check your internet connection and try again.';
      }
      
      updateStatus(errorMessage, 'error');
      throw e; // Re-throw so verification function can handle it
    }
  };

  const verifyNFT = async () => {
    // Check for Telegram ID first
    const currentTgId = tgId || localStorage.getItem('tg_id');
    
    if (!currentTgId) {
      updateStatus('❌ Missing Telegram ID! Please make sure you accessed this page from the Telegram bot link.', 'error');
      console.error('Telegram ID missing:', currentTgId);
      return;
    }

    if (!userAddress) {
      updateStatus('❌ Missing wallet address! Please connect your wallet first.', 'error');
      return;
    }

    console.log('Starting verification with:', { tgId: currentTgId, userAddress });
    updateStatus('Fetching your NFT collection for verification...', 'info');

    try {
      // First, fetch and display NFTs
      await fetchAndDisplayNFTs();
      
      // Then proceed with verification
      updateStatus('Verifying NFT ownership...', 'info');

      const response = await fetch(`${REACT_APP_API_URL}/api/verify-nft`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          wallet_address: userAddress,
          tg_id: currentTgId,
          collection_id: 'j7qeFNnpWTbaf5g9sMCxP2zfKrH5QFgE56SuYjQDQi1'  // Meta Betties collection ID
        })
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const result = await response.json();
      console.log('Verification result:', result);

      if (result.has_nft) {
        const count = result.nft_count || nftCount;
        setVerificationResult({
          success: true,
          nftCount: count,
          message: `✅ Verification successful! You have ${count} NFTs and now have access to the exclusive Telegram group.`
        });
        updateStatus(`✅ Verification successful! You have ${count} NFTs and now have access to the exclusive Telegram group.`, 'success');
        setWelcomeMessage('Welcome to Meta Betties Private Key - Access Granted!');
        
        // Show success message and redirect to Telegram group ONLY on success
        setTimeout(() => {
          updateStatus('🔄 Redirecting to Telegram group...', 'success');
          setTimeout(() => {
            // Redirect to the private Telegram group ONLY on success
            window.location.href = CONFIG.TELEGRAM_GROUPS.PRIVATE_KEY;
          }, 2000);
        }, 1000);
        
      } else {
        setVerificationResult({
          success: false,
          nftCount: 0,
          message: '❌ Required NFT not found in your wallet. You will be removed from the group.'
        });
        updateStatus('❌ Required NFT not found in your wallet. You will be removed from the group.', 'error');
        
        // Show error message but DO NOT redirect - user will be removed from group by bot
        setTimeout(() => {
          updateStatus('You will be removed from the group due to verification failure.', 'error');
          // NO REDIRECT - let the bot handle group removal
        }, 2000);
      }
    } catch (error) {
      console.error('Verification error:', error);
      
      // Handle specific error cases
      let errorMessage = 'Verification failed: ' + error.message;
      if (error.message.includes('Failed to fetch')) {
        errorMessage = 'Network error: Unable to connect to verification server. Please try again.';
      } else if (error.message.includes('HTTP error! status: 500')) {
        errorMessage = 'Server error: Verification service is temporarily unavailable. Please try again later.';
      } else if (error.message.includes('HTTP error! status: 400')) {
        errorMessage = 'Invalid request: Please check your wallet address and try again.';
      }
      
      setVerificationResult({
        success: false,
        nftCount: 0,
        message: errorMessage
      });
      updateStatus(errorMessage, 'error');
    }
  };

  const getStatusClasses = () => {
    const baseClasses = 'mb-6 p-4 rounded-2xl border-2 transition-all duration-300 backdrop-blur-sm';
    const iconClasses = 'w-3 h-3 rounded-full mr-3';
    
    if (status.type === 'success') {
      return {
        container: `${baseClasses} bg-emerald-500/10 border-emerald-400/30 text-emerald-100`,
        icon: `${iconClasses} bg-emerald-400 animate-pulse`
      };
    } else if (status.type === 'error') {
      return {
        container: `${baseClasses} bg-red-500/10 border-red-400/30 text-red-100`,
        icon: `${iconClasses} bg-red-400 animate-pulse`
      };
    } else {
      return {
        container: `${baseClasses} bg-blue-500/10 border-blue-400/30 text-blue-100`,
        icon: `${iconClasses} bg-blue-400 animate-pulse`
      };
    }
  };

  const statusClasses = getStatusClasses();

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-purple-900 to-slate-900 relative overflow-hidden">
      {/* Animated Background */}
      <div className="absolute inset-0">
        <div className="absolute inset-0 bg-gradient-to-r from-purple-500/10 via-pink-500/10 to-blue-500/10 animate-pulse"></div>
        <div className="absolute top-0 left-0 w-full h-full">
          <div className="absolute top-20 left-20 w-72 h-72 bg-purple-500/20 rounded-full blur-3xl animate-bounce"></div>
          <div className="absolute top-40 right-20 w-96 h-96 bg-blue-500/20 rounded-full blur-3xl animate-pulse"></div>
          <div className="absolute bottom-20 left-1/2 w-80 h-80 bg-pink-500/20 rounded-full blur-3xl animate-bounce"></div>
        </div>
      </div>

      <div className="relative z-10 min-h-screen flex items-center justify-center p-4">
        <div className="w-full max-w-4xl">
          {/* Header */}
          <div className="text-center mb-12 animate-fade-in">
            <div className="inline-flex items-center justify-center w-20 h-20 bg-gradient-to-r from-purple-500 to-pink-500 rounded-2xl mb-6 shadow-2xl">
              <svg className="w-10 h-10 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
              </svg>
            </div>
            <h1 className="text-5xl font-bold text-white mb-4 bg-gradient-to-r from-purple-400 to-pink-400 bg-clip-text text-transparent">
              NFT Verification Portal
            </h1>
            <p className="text-xl text-gray-300 max-w-2xl mx-auto leading-relaxed">
              {welcomeMessage}
            </p>
          </div>

          {/* Main Container */}
          <div className="backdrop-blur-xl bg-white/5 rounded-3xl p-8 shadow-2xl border border-white/10 animate-fade-in">
            {/* Status Message */}
            <div className={statusClasses.container}>
              <div className="flex items-center">
                <div className={statusClasses.icon} />
                <span className="font-medium">{status.message}</span>
              </div>
            </div>

            {/* NFT Count Display */}
            {nftCount > 0 && (
              <div className="mb-6 backdrop-blur-xl bg-gradient-to-br from-purple-500/10 to-pink-500/10 rounded-2xl p-6 border border-purple-400/30">
                <div className="flex items-center justify-center space-x-4">
                  <div className="w-16 h-16 bg-gradient-to-br from-purple-500 to-pink-500 rounded-full flex items-center justify-center shadow-lg">
                    <span className="text-2xl">🎨</span>
                  </div>
                  <div className="text-center">
                    <div className="text-3xl font-bold text-white">{nftCount}</div>
                    <div className="text-purple-300 font-medium">NFTs Found</div>
                  </div>
                </div>
              </div>
            )}

            {/* Verification Result Display */}
            {verificationResult && (
              <div className={`mb-6 backdrop-blur-xl rounded-2xl p-6 border ${
                verificationResult.success 
                  ? 'bg-gradient-to-br from-emerald-500/10 to-emerald-600/10 border-emerald-400/30' 
                  : 'bg-gradient-to-br from-red-500/10 to-red-600/10 border-red-400/30'
              }`}>
                <div className="flex items-center justify-center space-x-4">
                  <div className={`w-16 h-16 rounded-full flex items-center justify-center shadow-lg ${
                    verificationResult.success 
                      ? 'bg-gradient-to-br from-emerald-500 to-emerald-600' 
                      : 'bg-gradient-to-br from-red-500 to-red-600'
                  }`}>
                    <span className="text-2xl">
                      {verificationResult.success ? '✅' : '❌'}
                    </span>
                  </div>
                  <div className="text-center">
                    <div className={`text-xl font-bold ${
                      verificationResult.success ? 'text-emerald-100' : 'text-red-100'
                    }`}>
                      {verificationResult.success ? 'Verification Successful!' : 'Verification Failed'}
                    </div>
                    {verificationResult.success && (
                      <div className="text-emerald-300 font-medium">
                        {verificationResult.nftCount} NFTs Verified
                      </div>
                    )}
                    <div className={`text-sm mt-2 ${
                      verificationResult.success ? 'text-emerald-200' : 'text-red-200'
                    }`}>
                      {verificationResult.message}
                    </div>
                  </div>
                </div>
              </div>
            )}

            {/* Wallet Connection Section */}
            {!showVerification && (
              <div className="space-y-6">
                {/* Mobile Connecting State */}
                {isMobile && isConnectingWallet && (
                  <div className="text-center py-8">
                    <div className="inline-flex items-center justify-center w-16 h-16 bg-gradient-to-br from-purple-500 to-purple-600 rounded-full mb-4 shadow-lg animate-pulse">
                      <svg className="w-8 h-8 text-white animate-spin" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
                      </svg>
                    </div>
                    <h3 className="text-xl font-bold text-white mb-2">Connecting Wallet</h3>
                    <p className="text-gray-400">Please approve the connection in your wallet app and return to this page...</p>
                    <div className="mt-4">
                      <button
                        onClick={() => {
                          setIsConnectingWallet(false);
                          updateStatus('Connection cancelled. Please try again.', 'error');
                        }}
                        className="inline-flex items-center px-4 py-2 bg-gradient-to-r from-red-500 to-red-600 text-white rounded-lg hover:from-red-600 hover:to-red-700 transition-all duration-300"
                      >
                        Cancel Connection
                      </button>
                    </div>
                  </div>
                )}

                {/* Mobile Wallet Selection */}
                {isMobile && !isConnectingWallet && (
                  <div className="space-y-6">
                    <div className="text-center">
                      <h3 className="text-2xl font-bold text-white mb-2">Choose Your Solana Wallet</h3>
                      <p className="text-gray-400">Select your preferred wallet to connect and verify NFT ownership</p>
                    </div>
                    
                    {/* Manual Check Button */}
                    <div className="text-center">
                      <button
                        onClick={async () => {
                          updateStatus('🔍 Checking for wallet connection...', 'info');
                          const isConnected = await detectMobileWalletConnection();
                          if (!isConnected) {
                            updateStatus('No wallet connection detected. Please select a wallet to connect.', 'info');
                          }
                        }}
                        className="inline-flex items-center px-4 py-2 bg-gradient-to-r from-green-500 to-green-600 text-white rounded-lg hover:from-green-600 hover:to-green-700 transition-all duration-300"
                      >
                        <svg className="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                        </svg>
                        Check Connection
                      </button>
                    </div>
                    
                    <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-4 gap-4">
                      <button 
                        onClick={() => handleMobileWalletConnection('Phantom')} 
                        className="group relative overflow-hidden bg-gradient-to-br from-purple-500/20 to-purple-600/20 hover:from-purple-500/30 hover:to-purple-600/30 rounded-2xl p-6 text-white transition-all duration-300 border border-purple-400/30 hover:border-purple-400/50 hover:scale-105 hover:shadow-xl hover:shadow-purple-500/25"
                      >
                        <div className="flex flex-col items-center space-y-3">
                          <div className="w-12 h-12 bg-gradient-to-br from-purple-500 to-purple-600 rounded-xl flex items-center justify-center shadow-lg">
                            <span className="text-2xl">🟣</span>
                          </div>
                          <div className="text-center">
                            <div className="font-bold text-lg">Phantom</div>
                            <div className="text-sm text-purple-300">Solana</div>
                          </div>
                        </div>
                      </button>

                      <button 
                        onClick={() => handleMobileWalletConnection('Solflare')} 
                        className="group relative overflow-hidden bg-gradient-to-br from-orange-500/20 to-orange-600/20 hover:from-orange-500/30 hover:to-orange-600/30 rounded-2xl p-6 text-white transition-all duration-300 border border-orange-400/30 hover:border-orange-400/50 hover:scale-105 hover:shadow-xl hover:shadow-orange-500/25"
                      >
                        <div className="flex flex-col items-center space-y-3">
                          <div className="w-12 h-12 bg-gradient-to-br from-orange-500 to-orange-600 rounded-xl flex items-center justify-center shadow-lg">
                            <span className="text-2xl">🟠</span>
                          </div>
                          <div className="text-center">
                            <div className="font-bold text-lg">Solflare</div>
                            <div className="text-sm text-orange-300">Solana</div>
                          </div>
                        </div>
                      </button>

                      <button 
                        onClick={() => handleMobileWalletConnection('Backpack')} 
                        className="group relative overflow-hidden bg-gradient-to-br from-blue-500/20 to-blue-600/20 hover:from-blue-500/30 hover:to-blue-600/30 rounded-2xl p-6 text-white transition-all duration-300 border border-blue-400/30 hover:border-blue-400/50 hover:scale-105 hover:shadow-xl hover:shadow-blue-500/25"
                      >
                        <div className="flex flex-col items-center space-y-3">
                          <div className="w-12 h-12 bg-gradient-to-br from-blue-500 to-blue-600 rounded-xl flex items-center justify-center shadow-lg">
                            <span className="text-2xl">🔵</span>
                          </div>
                          <div className="text-center">
                            <div className="font-bold text-lg">Backpack</div>
                            <div className="text-sm text-blue-300">Solana</div>
                          </div>
                        </div>
                      </button>

                      <button 
                        onClick={() => handleMobileWalletConnection('Slope')} 
                        className="group relative overflow-hidden bg-gradient-to-br from-green-500/20 to-green-600/20 hover:from-green-500/30 hover:to-green-600/30 rounded-2xl p-6 text-white transition-all duration-300 border border-green-400/30 hover:border-green-400/50 hover:scale-105 hover:shadow-xl hover:shadow-green-500/25"
                      >
                        <div className="flex flex-col items-center space-y-3">
                          <div className="w-12 h-12 bg-gradient-to-br from-green-500 to-green-600 rounded-xl flex items-center justify-center shadow-lg">
                            <span className="text-2xl">🟢</span>
                          </div>
                          <div className="text-center">
                            <div className="font-bold text-lg">Slope</div>
                            <div className="text-sm text-green-300">Solana</div>
                          </div>
                        </div>
                      </button>

                      <button 
                        onClick={() => handleMobileWalletConnection('Glow')} 
                        className="group relative overflow-hidden bg-gradient-to-br from-yellow-500/20 to-yellow-600/20 hover:from-yellow-500/30 hover:to-yellow-600/30 rounded-2xl p-6 text-white transition-all duration-300 border border-yellow-400/30 hover:border-yellow-400/50 hover:scale-105 hover:shadow-xl hover:shadow-yellow-500/25"
                      >
                        <div className="flex flex-col items-center space-y-3">
                          <div className="w-12 h-12 bg-gradient-to-br from-yellow-500 to-yellow-600 rounded-xl flex items-center justify-center shadow-lg">
                            <span className="text-2xl">🟡</span>
                          </div>
                          <div className="text-center">
                            <div className="font-bold text-lg">Glow</div>
                            <div className="text-sm text-yellow-300">Solana</div>
                          </div>
                        </div>
                      </button>

                      <button 
                        onClick={() => handleMobileWalletConnection('Coinbase')} 
                        className="group relative overflow-hidden bg-gradient-to-br from-blue-600/20 to-blue-700/20 hover:from-blue-600/30 hover:to-blue-700/30 rounded-2xl p-6 text-white transition-all duration-300 border border-blue-500/30 hover:border-blue-500/50 hover:scale-105 hover:shadow-xl hover:shadow-blue-600/25"
                      >
                        <div className="flex flex-col items-center space-y-3">
                          <div className="w-12 h-12 bg-gradient-to-br from-blue-600 to-blue-700 rounded-xl flex items-center justify-center shadow-lg">
                            <span className="text-2xl">🔵</span>
                          </div>
                          <div className="text-center">
                            <div className="font-bold text-lg">Coinbase</div>
                            <div className="text-sm text-blue-300">Solana</div>
                          </div>
                        </div>
                      </button>
                    </div>
                    
                    {/* Install Wallet Option */}
                    <div className="text-center pt-4 border-t border-white/10">
                      <p className="text-gray-400 mb-4">Don't have a Solana wallet?</p>
                      <div className="flex flex-wrap justify-center gap-3">
                        <a 
                          href="https://phantom.app/" 
                          target="_blank" 
                          rel="noopener noreferrer"
                          className="inline-flex items-center px-4 py-2 bg-gradient-to-r from-purple-500 to-purple-600 text-white rounded-lg hover:from-purple-600 hover:to-purple-700 transition-all duration-300"
                        >
                          <span className="mr-2">🟣</span>
                          Install Phantom
                        </a>
                        <a 
                          href="https://solflare.com/" 
                          target="_blank" 
                          rel="noopener noreferrer"
                          className="inline-flex items-center px-4 py-2 bg-gradient-to-r from-orange-500 to-orange-600 text-white rounded-lg hover:from-orange-600 hover:to-orange-700 transition-all duration-300"
                        >
                          <span className="mr-2">🟠</span>
                          Install Solflare
                        </a>
                      </div>
                    </div>
                  </div>
                )}

                {/* Desktop Wallet Selection */}
                {!isMobile && (
                  <div className="space-y-6">
                    <div className="text-center">
                      <h3 className="text-2xl font-bold text-white mb-2">Choose Your Solana Wallet</h3>
                      <p className="text-gray-400">Select your preferred wallet to connect and verify NFT ownership</p>
                    </div>
                    <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-4 gap-4">
                      <button 
                        onClick={connectPhantom} 
                        className="group relative overflow-hidden bg-gradient-to-br from-purple-500/20 to-purple-600/20 hover:from-purple-500/30 hover:to-purple-600/30 rounded-2xl p-6 text-white transition-all duration-300 border border-purple-400/30 hover:border-purple-400/50 hover:scale-105 hover:shadow-xl hover:shadow-purple-500/25"
                      >
                        <div className="flex flex-col items-center space-y-3">
                          <div className="w-12 h-12 bg-gradient-to-br from-purple-500 to-purple-600 rounded-xl flex items-center justify-center shadow-lg">
                            <span className="text-2xl">🟣</span>
                          </div>
                          <div className="text-center">
                            <div className="font-bold text-lg">Phantom</div>
                            <div className="text-sm text-purple-300">Solana</div>
                          </div>
                        </div>
                      </button>

                      <button 
                        onClick={connectSolflare} 
                        className="group relative overflow-hidden bg-gradient-to-br from-orange-500/20 to-orange-600/20 hover:from-orange-500/30 hover:to-orange-600/30 rounded-2xl p-6 text-white transition-all duration-300 border border-orange-400/30 hover:border-orange-400/50 hover:scale-105 hover:shadow-xl hover:shadow-orange-500/25"
                      >
                        <div className="flex flex-col items-center space-y-3">
                          <div className="w-12 h-12 bg-gradient-to-br from-orange-500 to-orange-600 rounded-xl flex items-center justify-center shadow-lg">
                            <span className="text-2xl">🟠</span>
                          </div>
                          <div className="text-center">
                            <div className="font-bold text-lg">Solflare</div>
                            <div className="text-sm text-orange-300">Solana</div>
                          </div>
                        </div>
                      </button>

                      <button 
                        onClick={connectBackpack} 
                        className="group relative overflow-hidden bg-gradient-to-br from-blue-500/20 to-blue-600/20 hover:from-blue-500/30 hover:to-blue-600/30 rounded-2xl p-6 text-white transition-all duration-300 border border-blue-400/30 hover:border-blue-400/50 hover:scale-105 hover:shadow-xl hover:shadow-blue-500/25"
                      >
                        <div className="flex flex-col items-center space-y-3">
                          <div className="w-12 h-12 bg-gradient-to-br from-blue-500 to-blue-600 rounded-xl flex items-center justify-center shadow-lg">
                            <span className="text-2xl">🔵</span>
                          </div>
                          <div className="text-center">
                            <div className="font-bold text-lg">Backpack</div>
                            <div className="text-sm text-blue-300">Solana</div>
                          </div>
                        </div>
                      </button>

                      <button 
                        onClick={connectSlope} 
                        className="group relative overflow-hidden bg-gradient-to-br from-green-500/20 to-green-600/20 hover:from-green-500/30 hover:to-green-600/30 rounded-2xl p-6 text-white transition-all duration-300 border border-green-400/30 hover:border-green-400/50 hover:scale-105 hover:shadow-xl hover:shadow-green-500/25"
                      >
                        <div className="flex flex-col items-center space-y-3">
                          <div className="w-12 h-12 bg-gradient-to-br from-green-500 to-green-600 rounded-xl flex items-center justify-center shadow-lg">
                            <span className="text-2xl">🟢</span>
                          </div>
                          <div className="text-center">
                            <div className="font-bold text-lg">Slope</div>
                            <div className="text-sm text-green-300">Solana</div>
                          </div>
                        </div>
                      </button>

                      <button 
                        onClick={connectGlow} 
                        className="group relative overflow-hidden bg-gradient-to-br from-yellow-500/20 to-yellow-600/20 hover:from-yellow-500/30 hover:to-yellow-600/30 rounded-2xl p-6 text-white transition-all duration-300 border border-yellow-400/30 hover:border-yellow-400/50 hover:scale-105 hover:shadow-xl hover:shadow-yellow-500/25"
                      >
                        <div className="flex flex-col items-center space-y-3">
                          <div className="w-12 h-12 bg-gradient-to-br from-yellow-500 to-yellow-600 rounded-xl flex items-center justify-center shadow-lg">
                            <span className="text-2xl">🟡</span>
                          </div>
                          <div className="text-center">
                            <div className="font-bold text-lg">Glow</div>
                            <div className="text-sm text-yellow-300">Solana</div>
                          </div>
                        </div>
                      </button>

                      <button 
                        onClick={connectCoinbase} 
                        className="group relative overflow-hidden bg-gradient-to-br from-blue-600/20 to-blue-700/20 hover:from-blue-600/30 hover:to-blue-700/30 rounded-2xl p-6 text-white transition-all duration-300 border border-blue-500/30 hover:border-blue-500/50 hover:scale-105 hover:shadow-xl hover:shadow-blue-600/25"
                      >
                        <div className="flex flex-col items-center space-y-3">
                          <div className="w-12 h-12 bg-gradient-to-br from-blue-600 to-blue-700 rounded-xl flex items-center justify-center shadow-lg">
                            <span className="text-2xl">🔵</span>
                          </div>
                          <div className="text-center">
                            <div className="font-bold text-lg">Coinbase</div>
                            <div className="text-sm text-blue-300">Solana</div>
                          </div>
                        </div>
                      </button>
                    </div>
                  </div>
                )}
              </div>
            )}

            {/* Verification Section */}
            {showVerification && (
              <div className="animate-slide-up">
                <div className="backdrop-blur-xl bg-gradient-to-br from-emerald-500/10 to-emerald-600/10 rounded-2xl p-8 border border-emerald-400/30 mb-6">
                  <div className="flex items-center justify-between mb-6">
                    <h3 className="text-2xl font-bold text-white">Wallet Connected</h3>
                    <div className="flex items-center space-x-3">
                      <div className="w-3 h-3 bg-emerald-400 rounded-full animate-pulse" />
                      <span className="text-emerald-400 font-semibold">Connected</span>
                    </div>
                  </div>
                  <div className="bg-black/20 rounded-xl p-4 mb-6 border border-white/10">
                    <div className="text-sm text-gray-400 mb-2">Wallet Address</div>
                    <div className="font-mono text-white break-all text-lg">
                      {userAddress ? `${userAddress.substring(0, 8)}...${userAddress.substring(userAddress.length - 8)}` : ''}
                    </div>
                  </div>
                  <button 
                    onClick={verifyNFT}
                    className="w-full bg-gradient-to-r from-emerald-500 to-emerald-600 hover:from-emerald-600 hover:to-emerald-700 text-white font-bold py-4 px-8 rounded-xl transition-all duration-300 transform hover:scale-105 shadow-2xl hover:shadow-emerald-500/25 text-lg"
                  >
                    <div className="flex items-center justify-center space-x-3">
                      <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                      </svg>
                      <span>Fetch NFTs & Verify Ownership</span>
                    </div>
                  </button>
                </div>
              </div>
            )}

            {/* NFT Display Section */}
            {showNFTs && (
              <div className="animate-slide-up">
                <div className="backdrop-blur-xl bg-gradient-to-br from-purple-500/10 to-pink-500/10 rounded-2xl p-8 border border-purple-400/30">
                  <h3 className="text-2xl font-bold text-white mb-6 flex items-center">
                    <svg className="w-7 h-7 mr-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10" />
                    </svg>
                    Your NFT Collection ({nftCount} NFTs)
                  </h3>
                  <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-5 gap-4">
                    {nfts.length > 0 ? (
                      nfts.map((nft, index) => (
                        <div key={index} className="nft-card backdrop-blur-xl bg-white/5 rounded-xl p-4 text-center border border-white/10 hover:border-white/20 transition-all duration-300 hover:scale-105">
                          <img
                            src={nft.content?.links?.image || 'data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMTAwIiBoZWlnaHQ9IjEwMCIgdmlld0JveD0iMCAwIDEwMCAxMDAiIGZpbGw9Im5vbmUiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyI+CjxyZWN0IHdpZHRoPSIxMDAiIGhlaWdodD0iMTAwIiBmaWxsPSIjMzc0MTUxIi8+Cjx0ZXh0IHg9IjUwIiB5PSI1MCIgZm9udC1mYW1pbHk9IkFyaWFsIiBmb250LXNpemU9IjEyIiBmaWxsPSJ3aGl0ZSIgdGV4dC1hbmNob3I9Im1pZGRsZSIgZHk9Ii4zZW0iPk5GVDwvdGV4dD4KPC9zdmc+'}
                            alt={nft.content?.metadata?.name || 'NFT'}
                            className="w-full h-32 object-cover rounded-lg mb-3 shadow-lg"
                          />
                          <div className="font-bold text-white text-sm mb-2 truncate">
                            {nft.content?.metadata?.name || 'Unnamed NFT'}
                          </div>
                          <div className="text-xs text-gray-400 truncate">
                            {nft.grouping && nft.grouping.length > 0 ? nft.grouping[0].group_value : ''}
                          </div>
                        </div>
                      ))
                    ) : (
                      <div className="col-span-full text-center py-12">
                        <div className="w-20 h-20 bg-white/10 rounded-full flex items-center justify-center mx-auto mb-6">
                          <svg className="w-10 h-10 text-white/50" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M20 13V6a2 2 0 00-2-2H6a2 2 0 00-2 2v7m16 0v5a2 2 0 01-2 2H6a2 2 0 01-2-2v-5m16 0h-2.586a1 1 0 00-.707.293l-2.414 2.414a1 1 0 01-.707.293h-3.172a1 1 0 01-.707-.293l-2.414-2.414A1 1 0 006.586 13H4" />
                          </svg>
                        </div>
                        <div className="text-white/70 text-lg">No NFTs found in your wallet.</div>
                      </div>
                    )}
                  </div>
                </div>
              </div>
            )}
          </div>

          {/* Footer */}
          <div className="text-center mt-12 text-gray-400 text-sm">
            <p className="mb-2">Secure verification powered by blockchain technology</p>
            <p>© 2025 Meta Betties Private Key - All rights reserved</p>
            
            {/* Developer Information */}
            <div className="mt-6 pt-6 border-t border-white/10">
              <div className="flex items-center justify-center space-x-2 mb-2">
                <svg className="w-4 h-4 text-gray-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
                </svg>
                <span className="text-gray-500 font-medium">Developer</span>
              </div>
              <div className="text-gray-600 mb-2">
                <span className="font-semibold">Jharna Khanam</span>
              </div>
              <div className="flex items-center justify-center space-x-1">
                <svg className="w-4 h-4 text-blue-400" fill="currentColor" viewBox="0 0 24 24">
                  <path d="M12 0C5.373 0 0 5.373 0 12s5.373 12 12 12 12-5.373 12-12S18.627 0 12 0zm5.894 8.221l-1.97 9.28c-.145.658-.537.818-1.084.508l-3-2.21-1.446 1.394c-.14.18-.357.295-.6.295-.002 0-.003 0-.005 0l.213-3.054 5.56-5.022c.24-.213-.054-.334-.373-.121l-6.869 4.326-2.96-.924c-.64-.203-.658-.64.135-.954l11.566-4.458c.538-.196 1.006.128.832.941z"/>
                </svg>
                <span className="text-blue-400 font-medium">@mushfiqmoon</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default App; 
