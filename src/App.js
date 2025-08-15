// App.js
import React, { useMemo, useState, useEffect, useCallback } from "react";
import { Connection, PublicKey } from "@solana/web3.js";

import {
  WalletAdapterNetwork
} from "@solana/wallet-adapter-base";

import {
  ConnectionProvider,
  WalletProvider,
  useWallet
} from "@solana/wallet-adapter-react";

import {
  WalletModalProvider,
  WalletMultiButton
} from "@solana/wallet-adapter-react-ui";

import {
  PhantomWalletAdapter,
  SolflareWalletAdapter,
  TorusWalletAdapter,
  CoinbaseWalletAdapter
} from "@solana/wallet-adapter-wallets";

// Temporarily comment out problematic mobile adapter
// import { SolanaMobileWalletAdapter } from "@solana-mobile/wallet-adapter-mobile";

import "@solana/wallet-adapter-react-ui/styles.css";
import "./styles.css";
import { CONFIG } from "./config";

// ---------------------
// CONFIG (Change these)
// ---------------------
const NETWORK = WalletAdapterNetwork.Mainnet;
const RPC_ENDPOINT = "https://api.mainnet-beta.solana.com";
const API_BASE = "https://api-server-wcjc.onrender.com";
const DEFAULT_COLLECTION = "j7qeFNnpWTbaf5g9sMCxP2zfKrH5QFgE56SuYjQDQi1";

// ---------------------
// Utilities
// ---------------------
const shortAddress = (addr = "", len = 6) =>
  addr ? `${addr.slice(0, len)}...${addr.slice(-4)}` : "";

const isoNow = () => new Date().toISOString();

// ---------------------
// Professional Status Component
// ---------------------
function StatusIndicator({ type, message }) {
  const statusClasses = {
    success: "status-success",
    error: "status-error",
    warning: "status-warning",
    info: "status-info"
  };

  const icons = {
    success: "✅",
    error: "❌",
    warning: "⚠️",
    info: "ℹ️"
  };

  return (
    <div className={`${statusClasses[type]} p-4 rounded-2xl border-2 transition-all duration-300 backdrop-blur-sm`}>
      <div className="flex items-center space-x-3">
        <span className="text-2xl">{icons[type]}</span>
        <span className="font-medium">{message}</span>
      </div>
    </div>
  );
}

// ---------------------
// Professional Stats Card
// ---------------------
function StatsCard({ title, value, icon, gradient = "gradient-primary" }) {
  return (
    <div className="card-elevated p-4 md:p-6 text-center group">
      <div className={`w-12 h-12 md:w-16 md:h-16 ${gradient} rounded-xl md:rounded-2xl flex items-center justify-center mx-auto mb-3 md:mb-4 shadow-lg group-hover:shadow-glow transition-all duration-300`}>
        <span className="text-2xl md:text-3xl">{icon}</span>
      </div>
      <div className="heading-3 mb-2 text-lg md:text-xl lg:text-2xl">{value}</div>
      <div className="text-caption text-xs md:text-sm">{title}</div>
    </div>
  );
}

// ---------------------
// Professional Wallet Panel
// ---------------------
function WalletPanel({ onVerify }) {
  const { publicKey, connected, signTransaction, signAllTransactions, disconnect } = useWallet();
  const [status, setStatus] = useState({ type: "info", message: "🔗 Welcome! Connect your Solana wallet to start NFT verification" });
  const [verifying, setVerifying] = useState(false);
  const [nftCount, setNftCount] = useState(null);
  const [lastVerifiedAt, setLastVerifiedAt] = useState(new Date().toISOString());
  const [tgId, setTgId] = useState("7761809923"); // Add Telegram ID state with user's ID

  const walletAddress = publicKey ? publicKey.toBase58() : null;

  // Auto-fetch Telegram ID from URL parameters
  useEffect(() => {
    const urlParams = new URLSearchParams(window.location.search);
    const tgIdFromUrl = urlParams.get('tg_id') || urlParams.get('telegram_id') || urlParams.get('id');
    
    if (tgIdFromUrl) {
      setTgId(tgIdFromUrl);
      console.log("📱 Telegram ID fetched from URL:", tgIdFromUrl);
      
      // Show success message that ID was auto-fetched
      setStatus({ 
        type: "success", 
        message: `📱 Telegram ID automatically fetched: ${tgIdFromUrl}` 
      });
    }
  }, []);

  // Save auto-connect preference when wallet connects
  useEffect(() => {
    if (connected && publicKey) {
      // Save that user wants auto-connect for future sessions
      localStorage.setItem('wallet_auto_connect', 'true');
      console.log("💾 Auto-connect preference saved for future sessions");
      
      // Show success message when wallet connects
      setStatus({ 
        type: "success", 
        message: `🎉 Wallet connected successfully! Address: ${shortAddress(publicKey.toBase58())}` 
      });
    } else if (!connected) {
      // Show message when wallet disconnects
      setStatus({ 
        type: "info", 
        message: "🔌 Wallet disconnected. Connect your wallet to get started." 
      });
    }
  }, [connected, publicKey]);

  // DEVELOPER CREDIT PROTECTION - DO NOT REMOVE (SILENT)
  useEffect(() => {
    // Protect developer credit from removal (silent protection)
    const protectDeveloperCredit = () => {
      const developerCredit = document.querySelector('.developer-credit-locked');
      const backupCredit = document.querySelector('[data-protection="developer-credit-backup"]');
      
      if (!developerCredit && backupCredit) {
        // Silent restore without console warnings
        const footer = document.querySelector('footer .card');
        if (footer) {
          const restoredCredit = backupCredit.cloneNode(true);
          restoredCredit.classList.remove('hidden');
          restoredCredit.classList.add('developer-credit-locked');
          footer.appendChild(restoredCredit);
        }
      }
      
      // Silent protection check
      if (!developerCredit) {
        // Protection active but silent
      }
    };
    
    // Check immediately
    protectDeveloperCredit();
    
    // Set up continuous protection
    const protectionInterval = setInterval(protectDeveloperCredit, 5000);
    
    // Add mutation observer to detect DOM changes (silent)
    const observer = new MutationObserver((mutations) => {
      mutations.forEach((mutation) => {
        if (mutation.type === 'childList') {
          const developerCredit = document.querySelector('.developer-credit-locked');
          if (!developerCredit) {
            // Silent restore
            protectDeveloperCredit();
          }
        }
      });
    });
    
    // Start observing
    observer.observe(document.body, { childList: true, subtree: true });
    
    // Cleanup
    return () => {
      clearInterval(protectionInterval);
      observer.disconnect();
    };
  }, []);

  // Mobile wallet detection
  useEffect(() => {
    const detectMobileWallets = () => {
      const mobileWallets = [];
      
      try {
        // Check for Phantom
        if (window.solana?.isPhantom) {
          mobileWallets.push("Phantom");
          console.log("📱 Phantom wallet detected on mobile");
        }
        
        // Check for Solflare
        if (window.solflare?.isSolflare) {
          mobileWallets.push("Solflare");
          console.log("📱 Solflare wallet detected on mobile");
        }
        
        // Check for Torus
        if (window.torus) {
          mobileWallets.push("Torus");
          console.log("📱 Torus wallet detected on mobile");
        }
        
        // Check for Coinbase
        if (window.coinbaseWallet) {
          mobileWallets.push("Coinbase");
          console.log("📱 Coinbase wallet detected on mobile");
        }
        
        // Check for mobile-specific wallets
        if (window.navigator.userAgent.includes('Mobile')) {
          console.log("📱 Mobile device detected");
          if (mobileWallets.length > 0) {
            console.log("📱 Available mobile wallets:", mobileWallets.join(", "));
          } else {
            console.log("📱 No mobile wallets detected, user may need to install one");
          }
        }
      } catch (error) {
        console.warn("⚠️ Error detecting mobile wallets:", error);
      }
    };
    
    detectMobileWallets();
    
    // Set up continuous monitoring for newly installed wallets
    const checkForNewWallets = () => {
      try {
        // Check if any new wallets were installed
        if (window.solana?.isPhantom || window.solflare?.isSolflare || window.torus || window.coinbaseWallet) {
          console.log("🎉 New wallet detected! Attempting auto-connection...");
          
          // Trigger wallet detection again
          detectMobileWallets();
          
          // Auto-connect if user has previously connected
          if (localStorage.getItem('wallet_auto_connect') === 'true') {
            console.log("🔄 Auto-connecting to newly detected wallet...");
            // The WalletMultiButton will handle the connection
          }
        }
      } catch (error) {
        console.warn("⚠️ Error checking for new wallets:", error);
      }
    };
    
    // Check every 2 seconds for newly installed wallets
    const walletCheckInterval = setInterval(checkForNewWallets, 2000);
    
    // Cleanup interval on unmount
    return () => clearInterval(walletCheckInterval);
  }, []);

  const doVerify = useCallback(
    async (collectionId = DEFAULT_COLLECTION, tg_id = null) => {
      if (!walletAddress) {
        setStatus({ type: "warning", message: "🚫 Please connect your wallet first." });
        return;
      }
      
      // Use tg_id parameter or state value, fallback to user's default ID
      const telegramId = tg_id || tgId || "7761809923";
      
      if (!telegramId) {
        setStatus({ type: "warning", message: "🚫 Please enter your Telegram ID." });
        return;
      }
      
      setVerifying(true);
      setStatus({ type: "info", message: "⏳ Sending verification request..." });

      try {
        const payload = {
          wallet_address: walletAddress,
          tg_id: telegramId,
          collection_id: collectionId
        };

        const res = await fetch(`${API_BASE}/api/verify-nft`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(payload),
        });

        const data = await res.json();

        if (!res.ok) {
          setStatus({ type: "error", message: `⚠️ Verification failed: ${data.error || res.statusText}` });
        } else {
          if (data.has_nft) {
            setStatus({ type: "success", message: `✅ Verified — ${data.nft_count || 1} NFT(s) found. Access granted.` });
            
            // Automatically redirect to private group after successful verification
            setTimeout(() => {
              const privateGroupUrl = CONFIG.TELEGRAM_GROUPS.PRIVATE_KEY; // Use config for private group link
              setStatus({ type: "success", message: `🎉 Redirecting to private group...` });
              
              // Open private group in new tab
              window.open(privateGroupUrl, '_blank');
              
              // Show success message
              setStatus({ type: "success", message: `🎉 Access granted! Redirected to private group.` });
            }, 2000);
            
          } else {
            setStatus({ type: "error", message: "❌ No matching NFT found for this wallet." });
            
            // Automatically redirect to main group after failed verification
            setTimeout(() => {
              setStatus({ type: "warning", message: `⚠️ No NFT found. Redirecting to main group in 3 seconds...` });
              
              // Redirect to main group after 3 seconds
              setTimeout(() => {
                const mainGroupUrl = CONFIG.TELEGRAM_GROUPS.MAIN_GROUP;
                window.open(mainGroupUrl, '_blank');
                
                setStatus({ type: "warning", message: `⚠️ Redirected to main group. Please acquire required NFT to rejoin private group.` });
              }, 3000);
            }, 1000);
            
            // Show instructions for acquiring NFT
            const instructions = `
🔑 To join the private group, you need:
• Minimum 1 NFT from collection: ${collectionId}
• Or any NFT from the specified collection

💡 Steps:
1. Acquire the required NFT
2. Come back and verify again
3. You'll be automatically redirected to private group

📱 Main Group: ${CONFIG.TELEGRAM_GROUPS.MAIN_GROUP}
            `;
            
            alert(instructions);
          }
          setNftCount(data.nft_count ?? 0);
          setLastVerifiedAt(new Date().toISOString());
        }

        if (typeof onVerify === "function") onVerify({ walletAddress, ...data });
      } catch (err) {
        console.error("verify error", err);
        setStatus({ type: "error", message: "⚠️ Error while verifying. Check console." });
      } finally {
        setVerifying(false);
      }
    },
    [walletAddress, tgId, onVerify]
  );

  return (
    <div className="card space-component">
      <div className="flex flex-col lg:flex-row lg:items-center lg:justify-between gap-4 md:gap-6 mb-6 md:mb-8">
        <div className="flex-1">
          <h2 className="heading-2 mb-3 text-xl md:text-2xl lg:text-3xl">Meta Betties — NFT Verification</h2>
          {/* Description text removed */}
        </div>

        <div className="flex flex-row items-center gap-3 md:gap-4">
          <WalletMultiButton className="wallet-connect-btn text-sm md:text-base px-4 md:px-8 py-3 md:py-4" />
          {connected && (
            <button
              onClick={() => navigator.clipboard?.writeText(walletAddress)}
              className="btn btn-secondary text-xs md:text-sm px-3 md:px-6 py-2 md:py-3"
              title={walletAddress}
            >
              {shortAddress(walletAddress)}
            </button>
          )}
        </div>
        
        {/* Mobile Wallet Instructions */}
        {!connected && window.navigator.userAgent.includes('Mobile') && (
          <div className="mt-4 p-4 bg-blue-500/20 border border-blue-400/30 rounded-xl">
            <p className="text-sm text-blue-200 text-center mb-3">
              📱 <strong>Mobile Users:</strong> Install a Solana wallet app for automatic connection
            </p>
            <p className="text-xs text-blue-300 text-center mb-3">
              💡 <strong>Note:</strong> Your Telegram ID will be automatically fetched from the URL when you visit this page
            </p>
            <div className="flex flex-wrap justify-center gap-2">
              <a 
                href="https://apps.apple.com/app/phantom-crypto-wallet/id1598432977" 
                target="_blank" 
                rel="noopener noreferrer"
                className="inline-flex items-center px-3 py-1 bg-purple-600/80 text-white text-xs rounded-lg hover:bg-purple-500/80 transition-colors"
              >
                📱 Phantom (iOS)
              </a>
              <a 
                href="https://play.google.com/store/apps/details?id=app.phantom" 
                target="_blank" 
                rel="noopener noreferrer"
                className="inline-flex items-center px-3 py-1 bg-purple-600/80 text-white text-xs rounded-lg hover:bg-purple-500/80 transition-colors"
              >
                🤖 Phantom (Android)
              </a>
              <a 
                href="https://apps.apple.com/app/solflare-wallet/id1580902717" 
                target="_blank" 
                rel="noopener noreferrer"
                className="inline-flex items-center px-3 py-1 bg-orange-600/80 text-white text-xs rounded-lg hover:bg-orange-500/80 transition-colors"
              >
                📱 Solflare (iOS)
              </a>
              <a 
                href="https://play.google.com/store/apps/details?id=com.solflare.mobile" 
                target="_blank" 
                rel="noopener noreferrer"
                className="inline-flex items-center px-3 py-1 bg-orange-600/80 text-white text-xs rounded-lg hover:bg-orange-500/80 transition-colors"
              >
                🤖 Solflare (Android)
              </a>
              <a 
                href="https://apps.apple.com/app/torus-wallet/id1486384457" 
                target="_blank" 
                rel="noopener noreferrer"
                className="inline-flex items-center px-3 py-1 bg-blue-600/80 text-white text-xs rounded-lg hover:bg-blue-500/80 transition-colors"
              >
                📱 Torus (iOS)
              </a>
              <a 
                href="https://play.google.com/store/apps/details?id=com.torus.wallet" 
                target="_blank" 
                rel="noopener noreferrer"
                className="inline-flex items-center px-3 py-1 bg-blue-600/80 text-white text-xs rounded-lg hover:bg-blue-500/80 transition-colors"
              >
                🤖 Torus (Android)
              </a>
            </div>
            <p className="text-xs text-blue-300 text-center mt-2">
              💡 After installation, refresh the page or wait a few seconds for automatic detection
            </p>
            <div className="flex justify-center mt-3">
              <button
                onClick={() => {
                  window.location.reload();
                }}
                className="inline-flex items-center px-3 py-1 bg-blue-600/80 text-white text-xs rounded-lg hover:bg-blue-500/80 transition-colors"
              >
                🔄 Refresh Page
              </button>
            </div>
          </div>
        )}
      </div>

      {/* Telegram ID Input - Hidden but functional */}
      <div className="hidden">
        <label htmlFor="tgId" className="block text-sm md:text-base font-medium text-white mb-2">
          Telegram ID (Auto-fetched from URL or enter manually)
        </label>
        <div className="flex flex-col sm:flex-row gap-3">
          <input
            id="tgId"
            type="text"
            value={tgId}
            onChange={(e) => setTgId(e.target.value)}
            placeholder="Telegram ID (auto-fetched from URL or enter manually)"
            className="input flex-1 text-sm md:text-base px-3 md:px-4 py-2 md:py-3"
          />
        </div>
        <p className="text-caption mt-2 text-xs md:text-sm">
          ID automatically fetched from URL parameters (tg_id, telegram_id, or id) or enter manually
        </p>
      </div>

      {/* Status Display */}
      <StatusIndicator type={status.type} message={status.message} />

      {/* Stats Grid */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-3 md:gap-4 mt-6 md:mt-8">
        <StatsCard 
          title="Status" 
          value={status.message || "Idle"} 
          icon="📊"
          gradient="gradient-info"
        />
        <StatsCard 
          title="Last Verified" 
          value={(() => {
            const date = new Date(lastVerifiedAt);
            return date.toLocaleDateString() + ' ' + date.toLocaleTimeString();
          })()} 
          icon="⏰"
          gradient="gradient-warning"
        />
        <StatsCard 
          title="NFT Count" 
          value={nftCount !== null ? nftCount : "—"} 
          icon="🎨"
          gradient="gradient-success"
        />
      </div>

      {/* Action Buttons */}
      <div className="flex flex-col sm:flex-row gap-3 md:gap-4 mt-6 md:mt-8">
        <button
          onClick={() => doVerify(DEFAULT_COLLECTION, tgId)}
          disabled={verifying}
          className="btn btn-success flex-1 text-sm md:text-base px-4 md:px-6 py-3 md:py-4"
        >
          {verifying ? (
            <div className="flex items-center space-x-2">
              <div className="animate-spin rounded-full h-4 w-4 md:h-5 md:w-5 border-b-2 border-white"></div>
              <span>Verifying...</span>
            </div>
          ) : (
            "Verify NFT & Request Access"
          )}
        </button>
      </div>
    </div>
  );
}

// ---------------------
// Professional Feature Card
// ---------------------
function FeatureCard({ icon, title, description, gradient = "gradient-primary" }) {
  return (
    <div className="card-elevated p-4 md:p-6 text-center group">
      <div className={`w-12 h-12 md:w-16 md:h-16 ${gradient} rounded-xl md:rounded-2xl flex items-center justify-center mx-auto mb-3 md:mb-4 shadow-lg group-hover:shadow-glow transition-all duration-300`}>
        <span className="text-2xl md:text-3xl">{icon}</span>
      </div>
      <h3 className="heading-3 mb-2 md:mb-3 text-lg md:text-xl lg:text-2xl">{title}</h3>
      <p className="text-body text-xs md:text-sm">{description}</p>
    </div>
  );
}

// ---------------------
// Main App
// ---------------------
export default function App() {
  const wallets = useMemo(
    () => [
      new PhantomWalletAdapter(),
      new SolflareWalletAdapter({ network: NETWORK }),
      new TorusWalletAdapter(),
      new CoinbaseWalletAdapter(),
      // Temporarily remove problematic adapters
      // new LedgerWalletAdapter(),
      // new SolanaMobileWalletAdapter(),
    ].filter(Boolean),
    []
  );

  const endpoint = RPC_ENDPOINT;
  const [config, setConfig] = useState(null);
  
  useEffect(() => {
    (async () => {
      try {
        const res = await fetch(`${API_BASE}/api/config`);
        if (res.ok) {
          setConfig(await res.json());
        }
      } catch (e) {
        console.warn("Could not fetch config:", e);
      }
    })();
  }, []);

  const handleVerify = (result) => {
    console.log("verify result", result);
    if (result.has_nft) {
      // Show success message or redirect
    }
  };

  return (
    <ConnectionProvider endpoint={endpoint}>
      <WalletProvider wallets={wallets} autoConnect>
        <WalletModalProvider>
          <div className="min-h-screen bg-gradient-to-br from-slate-900 via-purple-900 to-slate-900 text-white">
            {/* Animated Background */}
            <div className="fixed inset-0 overflow-hidden pointer-events-none">
              <div className="absolute top-20 left-20 w-72 h-72 bg-purple-500/20 rounded-full blur-3xl animate-float"></div>
              <div className="absolute top-40 right-20 w-96 h-96 bg-blue-500/20 rounded-full blur-3xl animate-pulse-slow"></div>
              <div className="absolute bottom-20 left-1/2 w-80 h-80 bg-pink-500/20 rounded-full blur-3xl animate-bounce-slow"></div>
            </div>

            <div className="relative z-10 container-responsive py-8 md:py-16 lg:py-24">
              {/* Header */}
              <header className="text-center mb-8 md:mb-16">
                <div className="inline-flex items-center justify-center w-16 h-16 md:w-24 md:h-24 bg-gradient-to-r from-purple-600 via-pink-600 to-purple-600 rounded-2xl md:rounded-3xl mb-6 md:mb-8 shadow-2xl hover:shadow-glow transition-all duration-300">
                  <span className="text-3xl md:text-5xl">🔐</span>
                </div>
                <h1 className="heading-1 mb-4 md:mb-6 text-2xl md:text-4xl lg:text-5xl">Meta Betties — Verification Portal</h1>
                <p className="text-body text-lg md:text-xl max-w-3xl mx-auto px-4">
                  Secure NFT verification for Telegram access • Professional & Mobile friendly
                </p>
                
                {config?.version && (
                  <div className="mt-4 md:mt-6 inline-flex items-center space-x-2 bg-white/10 backdrop-blur-sm rounded-full px-3 md:px-4 py-2 border border-white/20">
                    <span className="text-caption text-xs md:text-sm">Server Version</span>
                    <span className="font-semibold text-white text-sm md:text-base">v{config.version}</span>
                  </div>
                )}
              </header>

              {/* Main Content */}
              <main className="space-y-12">
                <WalletPanel onVerify={handleVerify} />

                {/* Features Section */}
                <section className="space-component">
                  <h2 className="heading-2 text-center mb-8 md:mb-12 text-xl md:text-2xl lg:text-3xl">How It Works</h2>
                  <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 md:gap-6">
                    <FeatureCard
                      icon="🔗"
                      title="Connect Wallet"
                      description="Connect your Solana wallet (Phantom, Solflare, Torus, Coinbase)"
                      gradient="gradient-primary"
                    />
                    <FeatureCard
                      icon="✅"
                      title="Verify NFT"
                      description="Click Verify NFT. App calls backend /api/verify-nft endpoint"
                      gradient="gradient-success"
                    />
                    <FeatureCard
                      icon="🤖"
                      title="Backend Check"
                      description="Backend checks Helius (or RPC) & sends webhook to Telegram bot if verified"
                      gradient="gradient-warning"
                    />
                    <FeatureCard
                      icon="📱"
                      title="Telegram Access"
                      description="Telegram bot grants access to private group automatically"
                      gradient="gradient-info"
                    />
                  </div>
                </section>

              </main>

              {/* Footer */}
              <footer className="text-center mt-12 md:mt-20">
                <div className="card p-6 md:p-8">
                  <p className="text-caption mb-3 md:mb-4 text-xs md:text-sm">
                    © {new Date().getFullYear()} Meta Betties Verification Portal
                  </p>
                  
                  {/* LOCKED DEVELOPER CREDIT - DO NOT REMOVE */}
                  <div className="developer-credit-locked" data-protected="true" data-developer="mushfiqur-rahaman" data-version="1.0" data-locked="true">
                    <p className="text-body mb-3 md:mb-4 text-sm md:text-base">
                      Developer: <a href="https://i-am-mushfiqur.netlify.app/" target="_blank" rel="noopener noreferrer" className="font-semibold text-blue-300 hover:text-blue-200 transition-colors underline">Mushfiqur Rahaman</a>
                    </p>
                  </div>
                  
                  {/* Additional Protection Layer */}
                  <div className="hidden" data-protection="developer-credit-backup">
                    <p className="text-body text-sm md:text-base">
                      Developer: <a href="https://i-am-mushfiqur.netlify.app/" target="_blank" rel="noopener noreferrer" className="font-semibold text-blue-300">Mushfiqur Rahaman</a>
                    </p>
                  </div>
                </div>
              </footer>
            </div>
          </div>
        </WalletModalProvider>
      </WalletProvider>
    </ConnectionProvider>
  );
}
