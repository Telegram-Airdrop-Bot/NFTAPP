import React, { useState, useEffect, useMemo } from 'react';
import { ConnectionProvider, WalletProvider } from '@solana/wallet-adapter-react';
import { WalletModalProvider } from '@solana/wallet-adapter-react-ui';
import { BackpackWalletAdapter } from '@solana/wallet-adapter-backpack';
import { 
  PhantomWalletAdapter, 
  SolflareWalletAdapter, 
  SlopeWalletAdapter, 
  GlowWalletAdapter 
} from '@solana/wallet-adapter-wallets';
import { useWallet } from '@solana/wallet-adapter-react';
import Solflare from '@solflare-wallet/sdk';
import CONFIG from './config';
import '@solana/wallet-adapter-react-ui/styles.css';

function App() {
  const endpoint = 'https://api.mainnet-beta.solana.com';

  const wallets = useMemo(
    () => [
      new PhantomWalletAdapter(),
      new SolflareWalletAdapter({ network: 'mainnet-beta' }),
      new BackpackWalletAdapter(),
      new SlopeWalletAdapter(),
      new GlowWalletAdapter(),
    ],
    []
  );

  return (
    <ConnectionProvider endpoint={endpoint}>
      <WalletProvider wallets={wallets} autoConnect={true}>
        <WalletModalProvider>
          <NFTVerificationApp />
        </WalletModalProvider>
      </WalletProvider>
    </ConnectionProvider>
  );
}

function NFTVerificationApp() {
  const { publicKey, connect, disconnect, connected, wallet } = useWallet();
  const [userAddress, setUserAddress] = useState('');
  const [heliusApiKey, setHeliusApiKey] = useState('');
  const [status, setStatus] = useState({ message: 'Connect your wallet to verify NFT ownership', type: 'info' });
  const [showVerification, setShowVerification] = useState(false);
  const [showNFTs, setShowNFTs] = useState(false);
  const [nfts, setNfts] = useState([]);
  const [nftCount, setNftCount] = useState(0);
  const [verificationResult, setVerificationResult] = useState(null);
  const [welcomeMessage, setWelcomeMessage] = useState('Welcome to Meta Betties Private Key - Exclusive NFT Verification Portal');
  const [isMobile, setIsMobile] = useState(false);
  const [isConnectingWallet, setIsConnectingWallet] = useState(false);
  const [availableWallets, setAvailableWallets] = useState([]);
  const [selectedWallet, setSelectedWallet] = useState(null);
  const [showInstallButtons, setShowInstallButtons] = useState(false);

  const REACT_APP_API_URL = process.env.REACT_APP_API_URL || 'https://api-server-wcjc.onrender.com';
  const tgId = new URLSearchParams(window.location.search).get('tg_id') || 
               new URLSearchParams(window.location.search).get('telegram_id') ||
               new URLSearchParams(window.location.search).get('tgid') ||
               localStorage.getItem('tg_id');

  useEffect(() => {
    loadConfig();
    detectMobileDevice();
    
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

    const handleVisibilityChange = () => {
      if (!document.hidden && isMobile && isConnectingWallet) {
        console.log('User returned to app - checking connection');
        setTimeout(() => {
          detectAvailableWallets().forEach(wallet => {
            if (wallet.name === selectedWallet?.name) {
              wallet.connector().then(address => {
                if (address) {
                  handleConnectionSuccess(wallet.name, address);
                }
              });
            }
          });
        }, 1000);
      }
    };

    document.addEventListener('visibilitychange', handleVisibilityChange);
    return () => {
      document.removeEventListener('visibilitychange', handleVisibilityChange);
    };
  }, [tgId, isMobile, isConnectingWallet, selectedWallet]);

  useEffect(() => {
    if (connected && publicKey) {
      const address = publicKey.toString();
      setUserAddress(address);
      showVerificationSection();
      updateStatus(`✅ ${wallet?.adapter?.name || 'Wallet'} connected successfully!`, 'success');
    }
  }, [connected, publicKey, wallet]);

  useEffect(() => {
    if (isMobile) {
      detectAvailableWallets();
    }
  }, [isMobile]);

  const loadConfig = async () => {
    try {
      const response = await fetch(`${REACT_APP_API_URL}/api/config`);
      const config = await response.json();
      setHeliusApiKey(config.helius_api_key);
      if (!config.helius_api_key) {
        updateStatus('API configuration not found. Please check server setup.', 'error');
      }
    } catch (error) {
      updateStatus('Failed to load configuration: ' + error.message, 'error');
    }
  };

  const updateStatus = (message, type = 'info') => {
    setStatus({ message, type });
  };

  const detectMobileDevice = () => {
    const userAgent = navigator.userAgent.toLowerCase();
    const isMobileCheck = /android|webos|iphone|ipad|ipod|blackberry|iemobile|opera mini/i.test(userAgent);
    const isInAppBrowser = /telegramwebapp|fb_iab|instagram|line|whatsapp|twitter|discord/i.test(userAgent);
    const isStandalone = window.navigator.standalone === true;
    
    const mobile = isMobileCheck || isInAppBrowser || isStandalone;
    setIsMobile(mobile);
    
    if (isInAppBrowser) {
      updateStatus('⚠️ In-app browser detected. Some wallet features may be limited.', 'info');
    }
  };

  const detectAvailableWallets = () => {
    const wallets = [];
    
    if (window.solana?.isPhantom || window.phantom?.solana) {
      wallets.push({ name: 'Phantom', icon: '🟣', connector: connectPhantomMobile });
    }
    if (window.solflare || window.Solflare) {
      wallets.push({ name: 'Solflare', icon: '🟠', connector: connectSolflareMobile });
    }
    if (window.xnft?.solana) {
      wallets.push({ name: 'Backpack', icon: '🎒', connector: connectBackpackMobile });
    }
    if (window.slope) {
      wallets.push({ name: 'Slope', icon: '🟢', connector: connectSlopeMobile });
    }
    if (window.glow) {
      wallets.push({ name: 'Glow', icon: '✨', connector: connectGlowMobile });
    }
    if (window.coinbaseWalletSolana) {
      wallets.push({ name: 'Coinbase', icon: '🔵', connector: connectCoinbaseMobile });
    }

    if (wallets.length === 0) {
      wallets.push(
        { name: 'Phantom', icon: '🟣', connector: () => openWalletApp('Phantom') },
        { name: 'Solflare', icon: '🟠', connector: () => openWalletApp('Solflare') }
      );
    }

    setAvailableWallets(wallets);
    return wallets;
  };

  const connectPhantomMobile = async () => {
    try {
      if (window.phantom?.solana) {
        const resp = await window.phantom.solana.connect();
        return resp.publicKey.toString();
      }
      if (window.solana?.isPhantom) {
        const resp = await window.solana.connect();
        return resp.publicKey.toString();
      }
      throw new Error("Phantom not found");
    } catch (error) {
      await openWalletApp('Phantom');
      return null;
    }
  };

  const connectSolflareMobile = async () => {
    try {
      if (window.solflare) {
        if (window.solflare.connect) {
          await window.solflare.connect();
        }
        return window.solflare.publicKey?.toString();
      }
      if (window.Solflare) {
        const wallet = new window.Solflare();
        await wallet.connect();
        return wallet.publicKey?.toString();
      }
      throw new Error("Solflare not found");
    } catch (error) {
      await openWalletApp('Solflare');
      return null;
    }
  };

  const connectBackpackMobile = async () => {
    try {
      if (window.xnft?.solana) {
        const resp = await window.xnft.solana.connect();
        return resp.publicKey.toString();
      }
      throw new Error("Backpack not found");
    } catch (error) {
      await openWalletApp('Backpack');
      return null;
    }
  };

  const connectSlopeMobile = async () => {
    try {
      if (window.slope) {
        const resp = await window.slope.connect();
        return resp.publicKey.toString();
      }
      throw new Error("Slope not found");
    } catch (error) {
      await openWalletApp('Slope');
      return null;
    }
  };

  const connectGlowMobile = async () => {
    try {
      if (window.glow) {
        const resp = await window.glow.connect();
        return resp.publicKey.toString();
      }
      throw new Error("Glow not found");
    } catch (error) {
      await openWalletApp('Glow');
      return null;
    }
  };

  const connectCoinbaseMobile = async () => {
    try {
      if (window.coinbaseWalletSolana) {
        const resp = await window.coinbaseWalletSolana.connect();
        return resp.publicKey.toString();
      }
      throw new Error("Coinbase not found");
    } catch (error) {
      await openWalletApp('Coinbase');
      return null;
    }
  };

  const handleMobileWalletSelect = async (wallet) => {
    setSelectedWallet(wallet);
    setIsConnectingWallet(true);
    updateStatus(`Connecting to ${wallet.name}...`, 'info');

    try {
      const address = await wallet.connector();
      
      if (address) {
        handleConnectionSuccess(wallet.name, address);
        return;
      }

      startConnectionPolling(wallet.name);
    } catch (error) {
      handleMobileError(error, wallet.name);
    }
  };

  const handleConnectionSuccess = (walletName, address) => {
    setUserAddress(address);
    setIsConnectingWallet(false);
    setShowVerification(true);
    updateStatus(`✅ ${walletName} connected!`, 'success');
    fetchAndDisplayNFTs();
  };

  const startConnectionPolling = (walletName) => {
    let attempts = 0;
    const maxAttempts = 10;
    const pollInterval = 2000;

    const poll = async () => {
      attempts++;
      
      if (attempts >= maxAttempts) {
        updateStatus(`Could not connect to ${walletName}`, 'error');
        setIsConnectingWallet(false);
        return;
      }

      const wallets = detectAvailableWallets();
      const wallet = wallets.find(w => w.name === walletName);
      
      if (wallet) {
        try {
          const address = await wallet.connector();
          if (address) {
            handleConnectionSuccess(walletName, address);
            return;
          }
        } catch (error) {
          console.error(`Polling connection error:`, error);
        }
      }

      setTimeout(poll, pollInterval);
    };

    poll();
  };

  const handleMobileError = (error, walletName) => {
    console.error(`${walletName} connection error:`, error);
    
    let errorMessage = '';
    if (error.message.includes('User rejected')) {
      errorMessage = 'Connection cancelled by user';
    } else if (error.message.includes('Not found')) {
      errorMessage = `${walletName} not installed`;
      setShowInstallButtons(true);
    } else {
      errorMessage = `Failed to connect to ${walletName}`;
    }
    
    updateStatus(`❌ ${errorMessage}`, 'error');
    setIsConnectingWallet(false);
  };

  const openWalletApp = async (walletName) => {
    const userAgent = navigator.userAgent.toLowerCase();
    const isIOS = /iphone|ipad|ipod/.test(userAgent);
    const isInAppBrowser = /telegramwebapp|fb_iab|instagram|line|whatsapp|twitter|discord/i.test(userAgent);
    
    let appUrl = '';
    let fallbackUrl = '';
    let deepLinkUrl = '';
    
    switch (walletName) {
      case 'Phantom':
        deepLinkUrl = 'phantom://';
        appUrl = 'https://phantom.app/ul/browse/';
        fallbackUrl = isIOS ? 'https://apps.apple.com/app/phantom/id1598432977' : 'https://play.google.com/store/apps/details?id=app.phantom';
        break;
      case 'Solflare':
        deepLinkUrl = 'solflare://';
        appUrl = 'https://solflare.com/';
        fallbackUrl = isIOS ? 'https://apps.apple.com/app/solflare/id1580902717' : 'https://play.google.com/store/apps/details?id=com.solflare.mobile';
        break;
      case 'Backpack':
        deepLinkUrl = 'backpack://';
        appUrl = 'https://backpack.app/';
        fallbackUrl = isIOS ? 'https://apps.apple.com/app/backpack/id6443944476' : 'https://play.google.com/store/apps/details?id=app.backpack';
        break;
      case 'Slope':
        deepLinkUrl = 'slope://';
        appUrl = 'https://slope.finance/';
        fallbackUrl = isIOS ? 'https://apps.apple.com/app/slope-wallet/id1574624530' : 'https://play.google.com/store/apps/details?id=com.slope.finance';
        break;
      case 'Glow':
        deepLinkUrl = 'glow://';
        appUrl = 'https://glow.app/';
        fallbackUrl = isIOS ? 'https://apps.apple.com/app/glow-wallet/id1635713293' : 'https://play.google.com/store/apps/details?id=com.glow.wallet';
        break;
      case 'Coinbase':
        deepLinkUrl = 'coinbase://';
        appUrl = 'https://wallet.coinbase.com/';
        fallbackUrl = isIOS ? 'https://apps.apple.com/app/coinbase-wallet/id1278383455' : 'https://play.google.com/store/apps/details?id=org.toshi';
        break;
    }
    
    updateStatus(`Opening ${walletName} app... Please approve the connection and return to this page.`, 'info');
    
    try {
      if (isInAppBrowser) {
        updateStatus(`⚠️ In-app browser detected. Opening ${walletName} in external browser...`, 'info');
        
        if (window.Telegram?.WebApp) {
          window.Telegram.WebApp.openTelegramLink(appUrl);
        } else {
          window.open(appUrl, '_blank');
        }
        
        setTimeout(() => {
          updateStatus(`✅ ${walletName} opened in external browser! Please approve the connection and return here.`, 'success');
        }, 2000);
        return;
      }
      
      if (deepLinkUrl) {
        try {
          window.location.href = deepLinkUrl;
          setTimeout(() => {
            window.open(appUrl, '_blank');
          }, 1000);
        } catch (error) {
          window.open(appUrl, '_blank');
        }
      } else {
        window.open(appUrl, '_blank');
      }
      
      setTimeout(() => {
        updateStatus(`✅ ${walletName} app opened! Please approve the connection and return here.`, 'success');
      }, 2000);
    } catch (error) {
      console.error(`Error opening ${walletName}:`, error);
      updateStatus(`${walletName} app not found. Opening app store...`, 'info');
      setTimeout(() => {
        window.open(fallbackUrl, '_blank');
        updateStatus(`${walletName} app not found. Please install it from the app store and try again.`, 'error');
        setIsConnectingWallet(false);
      }, 1000);
    }
  };

  const showVerificationSection = () => {
    setShowVerification(true);
    setShowNFTs(false);
    updateStatus('Wallet connected successfully! Click "Verify NFT Ownership" to continue.', 'success');
    fetchAndDisplayNFTs();
  };

  const fetchAndDisplayNFTs = async () => {
    const address = publicKey ? publicKey.toString() : userAddress;
    if (!address) return;
    
    updateStatus('Fetching your NFT collection...', 'info');
    setNfts([]);
    setShowNFTs(true);

    try {
      const url = `${REACT_APP_API_URL}/api/addresses/${address}/nft-assets?api-key=${heliusApiKey}`;
      const res = await fetch(url);
      const nftData = await res.json();

      if (nftData && nftData.length > 0) {
        setNfts(nftData);
        setNftCount(nftData.length);
        updateStatus(`Found ${nftData.length} NFTs in your wallet! Click "Verify NFT Ownership" to continue.`, 'success');
      } else {
        setNfts([]);
        setNftCount(0);
        updateStatus('No NFTs found in your wallet.', 'error');
      }
    } catch (e) {
      setNfts([]);
      setNftCount(0);
      updateStatus('Failed to fetch NFTs: ' + e.message, 'error');
    }
  };

  const verifyNFT = async () => {
    const currentTgId = tgId || localStorage.getItem('tg_id');
    
    if (!currentTgId) {
      updateStatus('❌ Missing Telegram ID! Please make sure you accessed this page from the Telegram bot link.', 'error');
      console.error('Telegram ID missing:', currentTgId);
      return;
    }

    const address = publicKey ? publicKey.toString() : userAddress;
    if (!address) {
      updateStatus('❌ Missing wallet address! Please connect your wallet first.', 'error');
      return;
    }

    console.log('Starting verification with:', { tgId: currentTgId, userAddress: address });
    updateStatus('Verifying NFT ownership...', 'info');

    try {
      const response = await fetch(`${REACT_APP_API_URL}/api/verify-nft`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          wallet_address: address,
          tg_id: currentTgId,
          collection_id: 'j7qeFNnpWTbaf5g9sMCxP2zfKrH5QFgE56SuYjQDQi1'
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
        
        setTimeout(() => {
          updateStatus('🔄 Redirecting to Telegram group...', 'success');
          setTimeout(() => {
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
        
        setTimeout(() => {
          updateStatus('You will be removed from the group due to verification failure.', 'error');
        }, 2000);
      }
    } catch (error) {
      console.error('Verification error:', error);
      
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

          <div className="backdrop-blur-xl bg-white/5 rounded-3xl p-8 shadow-2xl border border-white/10 animate-fade-in">
            <div className={statusClasses.container}>
              <div className="flex items-center">
                <div className={statusClasses.icon} />
                <span className="font-medium">{status.message}</span>
              </div>
            </div>

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

            {!showVerification && (
              <div className="space-y-6">
                {isMobile && isConnectingWallet && (
                  <div className="text-center py-8">
                    <div className="inline-flex items-center justify-center w-16 h-16 bg-gradient-to-br from-purple-500 to-purple-600 rounded-full mb-4 shadow-lg animate-pulse">
                      <svg className="w-8 h-8 text-white animate-spin" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
                      </svg>
                    </div>
                    <h3 className="text-xl font-bold text-white mb-2">Connecting to {selectedWallet?.name || 'Wallet'}</h3>
                    <p className="text-gray-400 mb-4">Please approve the connection in your wallet app and return to this page...</p>
                    
                    <div className="bg-gradient-to-r from-blue-500/10 to-purple-500/10 rounded-xl p-4 mb-4 border border-blue-400/30">
                      <div className="text-sm text-gray-300 space-y-2">
                        <p>1. Open your {selectedWallet?.name || 'wallet'} app</p>
                        <p>2. Approve the connection request</p>
                        <p>3. Return to this page</p>
                        <p>4. Wait for automatic detection</p>
                      </div>
                    </div>
                    
                    <div className="flex flex-col sm:flex-row gap-3 justify-center">
                      <button
                        onClick={async () => {
                          updateStatus('🔍 Checking for wallet connection...', 'info');
                          const isConnected = await detectAvailableWallets().some(w => 
                            w.name === selectedWallet?.name && w.connector().then(Boolean)
                          );
                          if (!isConnected) {
                            updateStatus('No wallet connection detected yet. Please try again.', 'info');
                          }
                        }}
                        className="inline-flex items-center px-4 py-2 bg-gradient-to-r from-green-500 to-green-600 text-white rounded-lg hover:from-green-600 hover:to-green-700 transition-all duration-300"
                      >
                        <svg className="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                        </svg>
                        Check Connection
                      </button>
                      
                      <button
                        onClick={() => {
                          setIsConnectingWallet(false);
                          updateStatus('Connection cancelled. Please try again.', 'error');
                        }}
                        className="inline-flex items-center px-4 py-2 bg-gradient-to-r from-red-500 to-red-600 text-white rounded-lg hover:from-red-600 hover:to-red-700 transition-all duration-300"
                      >
                        <svg className="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M6 18L18 6M6 6l12 12" />
                        </svg>
                        Cancel Connection
                      </button>
                    </div>
                  </div>
                )}

                {isMobile && !isConnectingWallet && (
                  <div className="space-y-6">
                    <div className="text-center">
                      <h3 className="text-2xl font-bold text-white mb-2">Choose Your Solana Wallet</h3>
                      <p className="text-gray-400">Select your preferred wallet to connect and verify NFT ownership</p>
                    </div>
                    
                    {showInstallButtons && (
                      <div className="bg-gradient-to-r from-yellow-500/10 to-orange-500/10 rounded-xl p-4 border border-yellow-400/30">
                        <div className="flex items-center space-x-3 mb-2">
                          <div className="w-6 h-6 bg-yellow-500 rounded-full flex items-center justify-center">
                            <svg className="w-3 h-3 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.964-.833-2.732 0L3.732 16.5c-.77.833.192 2.5 1.732 2.5z" />
                            </svg>
                          </div>
                          <h5 className="text-yellow-300 font-semibold text-sm">Wallet Not Found</h5>
                        </div>
                        <div className="text-xs text-yellow-200">
                          <p>You need to install a Solana wallet to continue</p>
                        </div>
                        <div className="flex flex-wrap justify-center gap-2 mt-3">
                          <a 
                            href="https://phantom.app/" 
                            target="_blank" 
                            rel="noopener noreferrer"
                            className="inline-flex items-center px-3 py-1.5 bg-gradient-to-r from-purple-500 to-purple-600 text-white rounded-lg hover:from-purple-600 hover:to-purple-700 transition-all duration-300 text-sm"
                          >
                            <span className="mr-1">🟣</span>
                            Install Phantom
                          </a>
                          <a 
                            href="https://solflare.com/" 
                            target="_blank" 
                            rel="noopener noreferrer"
                            className="inline-flex items-center px-3 py-1.5 bg-gradient-to-r from-orange-500 to-orange-600 text-white rounded-lg hover:from-orange-600 hover:to-orange-700 transition-all duration-300 text-sm"
                          >
                            <span className="mr-1">🟠</span>
                            Install Solflare
                          </a>
                        </div>
                      </div>
                    )}
                    
                    <div className="grid grid-cols-2 gap-4">
                      {availableWallets.map((wallet) => (
                        <button 
                          key={wallet.name}
                          onClick={() => handleMobileWalletSelect(wallet)}
                          className="group relative overflow-hidden bg-gradient-to-br from-purple-500/20 to-purple-600/20 hover:from-purple-500/30 hover:to-purple-600/30 rounded-2xl p-6 text-white transition-all duration-300 border border-purple-400/30 hover:border-purple-400/50 hover:scale-105 hover:shadow-xl hover:shadow-purple-500/25 active:scale-95"
                        >
                          <div className="flex flex-col items-center space-y-3">
                            <div className="w-16 h-16 bg-gradient-to-br from-purple-500 to-purple-600 rounded-xl flex items-center justify-center shadow-lg">
                              <span className="text-3xl">{wallet.icon}</span>
                            </div>
                            <div className="text-center">
                              <div className="font-bold text-lg">{wallet.name}</div>
                              <div className="text-sm text-purple-300">Tap to connect</div>
                            </div>
                          </div>
                        </button>
                      ))}
                    </div>
                  </div>
                )}

                {!isMobile && (
                  <div className="space-y-6">
                    <div className="text-center">
                      <h3 className="text-2xl font-bold text-white mb-2">Choose Your Solana Wallet</h3>
                      <p className="text-gray-400">Select your preferred wallet to connect and verify NFT ownership</p>
                    </div>
                    
                    <div className="text-center mb-6">
                      <button
                        onClick={() => connect()}
                        className="inline-flex items-center px-6 py-3 bg-gradient-to-r from-purple-500 to-pink-500 text-white rounded-xl hover:from-purple-600 hover:to-pink-600 transition-all duration-300 transform hover:scale-105 shadow-2xl hover:shadow-purple-500/25"
                      >
                        <svg className="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
                        </svg>
                        Connect Wallet (Recommended)
                      </button>
                    </div>
                    
                    <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-4 gap-4">
                      <button 
                        onClick={connectPhantomMobile} 
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
                        onClick={connectSolflareMobile} 
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
                        onClick={connectBackpackMobile} 
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
                        onClick={connectSlopeMobile} 
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
                        onClick={connectGlowMobile} 
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
                        onClick={connectCoinbaseMobile} 
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
                      {publicKey ? `${publicKey.toString().substring(0, 8)}...${publicKey.toString().substring(publicKey.toString().length - 8)}` : 
                       userAddress ? `${userAddress.substring(0, 8)}...${userAddress.substring(userAddress.length - 8)}` : ''}
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
                      <span>Verify NFT Ownership</span>
                    </div>
                  </button>
                </div>
              </div>
            )}

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

          <div className="text-center mt-12 text-gray-400 text-sm">
            <p className="mb-2">Secure verification powered by blockchain technology</p>
            <p>© 2025 Meta Betties Private Key - All rights reserved</p>
            
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
