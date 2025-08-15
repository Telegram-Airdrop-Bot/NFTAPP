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
  CoinbaseWalletAdapter,
  LedgerWalletAdapter
} from "@solana/wallet-adapter-wallets";

import "@solana/wallet-adapter-react-ui/styles.css";
import "./styles.css"; // Tailwind entry (make sure tailwind is configured)

// ---------------------
// CONFIG (Change these)
// ---------------------
const NETWORK = WalletAdapterNetwork.Mainnet; // or Devnet
const RPC_ENDPOINT = "https://api.mainnet-beta.solana.com"; // or your RPC
// Your backend base URL (API server that implements your endpoint list)
const API_BASE = "https://api-server-wcjc.onrender.com"; // <-- Updated with correct API server

// Optional: default collection id for Meta Betties
const DEFAULT_COLLECTION = "j7qeFNnpWTbaf5g9sMCxP2zfKrH5QFgE56SuYjQDQi1";

// ---------------------
// Utilities
// ---------------------
const shortAddress = (addr = "", len = 6) =>
  addr ? `${addr.slice(0, len)}...${addr.slice(-4)}` : "";

const isoNow = () => new Date().toISOString();

// ---------------------
// Wallet + UI Component
// ---------------------
function WalletPanel({ onVerify }) {
  const { publicKey, connected, signTransaction, signAllTransactions, disconnect } = useWallet();
  const [status, setStatus] = useState("");
  const [verifying, setVerifying] = useState(false);
  const [nftCount, setNftCount] = useState(null);
  const [lastVerifiedAt, setLastVerifiedAt] = useState(null);

  const walletAddress = publicKey ? publicKey.toBase58() : null;

  const doVerify = useCallback(
    async (collectionId = DEFAULT_COLLECTION, tg_id = null) => {
      if (!walletAddress) {
        setStatus("🚫 Please connect your wallet first.");
        return;
      }
      setVerifying(true);
      setStatus("⏳ Sending verification request...");

      try {
        const payload = {
          wallet_address: walletAddress,
          tg_id, // optional, can be null or a real Telegram ID if you have it
          collection_id: collectionId
        };

        const res = await fetch(`${API_BASE}/api/verify-nft`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(payload),
        });

        const data = await res.json();

        if (!res.ok) {
          setStatus(`⚠️ Verification failed: ${data.error || res.statusText}`);
        } else {
          if (data.has_nft) {
            setStatus(`✅ Verified — ${data.nft_count || 1} NFT(s) found. Access granted.`);
          } else {
            setStatus("❌ No matching NFT found for this wallet.");
          }
          setNftCount(data.nft_count ?? 0);
          setLastVerifiedAt(data.verification_time ?? isoNow());
        }

        // expose to parent for side-effects (optional)
        if (typeof onVerify === "function") onVerify({ walletAddress, ...data });
      } catch (err) {
        console.error("verify error", err);
        setStatus("⚠️ Error while verifying. Check console.");
      } finally {
        setVerifying(false);
      }
    },
    [walletAddress, onVerify]
  );

  const fetchAssets = useCallback(async (apiKey = null) => {
    if (!walletAddress) {
      setStatus("🚫 Please connect your wallet first to fetch assets.");
      return;
    }
    setStatus("⏳ Fetching NFT assets from backend...");
    try {
      // This endpoint should proxy Helius and accept optional api-key query if you want
      const url = `${API_BASE}/api/addresses/${walletAddress}/nft-assets`;
      const res = await fetch(url, { method: "GET" });
      if (!res.ok) {
        const txt = await res.text();
        setStatus(`⚠️ Failed to fetch assets: ${res.status}`);
        console.error(txt);
        return null;
      }
      const nfts = await res.json();
      setStatus(`📦 Found ${nfts.length} assets (showing first 6)`);
      return nfts;
    } catch (e) {
      console.error(e);
      setStatus("⚠️ Error fetching assets.");
      return null;
    }
  }, [walletAddress]);

  return (
    <div className="w-full max-w-3xl bg-white/5 backdrop-blur-sm rounded-2xl p-6 shadow-lg">
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
        <div>
          <h2 className="text-xl font-semibold">Meta Betties — NFT Verification</h2>
          <p className="text-sm text-slate-300 mt-1">
            Connect a Solana wallet (Phantom/Solflare/Torus/Coinbase/Ledger). Then click Verify to let the backend confirm NFT ownership.
          </p>
        </div>

        <div className="flex items-center gap-3">
          <WalletMultiButton className="px-3 py-2 rounded-lg" />
          {connected && (
            <button
              onClick={() => navigator.clipboard?.writeText(walletAddress)}
              className="text-sm px-3 py-2 bg-slate-700/60 rounded-lg"
              title={walletAddress}
            >
              {shortAddress(walletAddress)}
            </button>
          )}
        </div>
      </div>

      <div className="mt-4 grid grid-cols-1 sm:grid-cols-3 gap-3">
        <div className="p-3 bg-white/3 rounded-lg">
          <div className="text-xs text-slate-300">Status</div>
          <div className="text-sm mt-1">{status || "Idle"}</div>
        </div>

        <div className="p-3 bg-white/3 rounded-lg">
          <div className="text-xs text-slate-300">Last Verified</div>
          <div className="text-sm mt-1">{lastVerifiedAt ? new Date(lastVerifiedAt).toLocaleString() : "—"}</div>
        </div>

        <div className="p-3 bg-white/3 rounded-lg">
          <div className="text-xs text-slate-300">NFT Count</div>
          <div className="text-sm mt-1">{nftCount !== null ? nftCount : "—"}</div>
        </div>
      </div>

      <div className="mt-4 flex flex-col sm:flex-row gap-3">
        <button
          onClick={() => doVerify(DEFAULT_COLLECTION, null)}
          disabled={verifying}
          className="flex-1 px-4 py-2 rounded-lg bg-gradient-to-r from-emerald-500 to-green-600 text-white font-medium disabled:opacity-60"
        >
          {verifying ? "Verifying..." : "Verify NFT & Request Access"}
        </button>

        <button
          onClick={async () => {
            const assets = await fetchAssets();
            // show small preview modal (simple alert for demo)
            if (assets) {
              const preview = assets
                .slice(0, 6)
                .map((a, i) => {
                  const name = a.content?.metadata?.name || "Unknown";
                  const collection = a.grouping?.[0]?.group_value || "collection?";
                  return `${i + 1}. ${name} (${collection})`;
                })
                .join("\n");
              alert(`First ${Math.min(6, assets.length)} assets:\n\n${preview}`);
            }
          }}
          className="px-4 py-2 rounded-lg bg-slate-700 text-white"
        >
          View NFT Assets
        </button>

        {connected && (
          <button
            onClick={() => {
              // trigger a health check call
              fetch(`${API_BASE}/api/health`)
                .then((r) => r.json())
                .then((d) => alert(`Server: ${d.status}\nVersion: ${d.version}\n${d.timestamp}`))
                .catch((e) => alert("Health check failed"));
            }}
            className="px-4 py-2 rounded-lg border border-slate-600 text-white"
          >
            Health Check
          </button>
        )}
      </div>
    </div>
  );
}

// ---------------------
// Main App
// ---------------------
export default function App() {
  // Setup wallet adapters
  const wallets = useMemo(
    () => [
      new PhantomWalletAdapter(),
      new SolflareWalletAdapter({ network: NETWORK }),
      new TorusWalletAdapter(),
      new CoinbaseWalletAdapter(),
      new LedgerWalletAdapter(),
      // Note: some adapters might be undefined in some environments (Backpack in web not installed) -
      // using optional chaining above prevents crashes. You can add more adapters here.
    ].filter(Boolean),
    []
  );

  // Connection provider
  const endpoint = RPC_ENDPOINT;

  // Optional: fetch configuration from backend (Configuration Endpoint)
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

  // onVerify callback to handle responses (e.g., show toast, open modal)
  const handleVerify = (result) => {
    // If backend sends webhook to Telegram, you may show a friendly message here
    // e.g. show "Check Telegram for access" when verified
    console.log("verify result", result);
    // Example UI side-effect:
    if (result.has_nft) {
      // you might open instructions modal to ask user to check Telegram
      // or show a "Go to Telegram" button
    }
  };

  return (
    <ConnectionProvider endpoint={endpoint}>
      <WalletProvider wallets={wallets} autoConnect>
        <WalletModalProvider>
          <div className="min-h-screen bg-gradient-to-br from-slate-900 via-indigo-900 to-black text-white flex items-center justify-center p-6">
            <div className="w-full max-w-5xl">
              <header className="flex items-center justify-between mb-6">
                <div>
                  <h1 className="text-3xl font-bold">Meta Betties — Verification Portal</h1>
                  <p className="text-sm text-slate-300 mt-1">Secure NFT verification for Telegram access • Mobile & Web friendly</p>
                </div>

                <div className="text-right">
                  <div className="text-xs text-slate-400">Server</div>
                  <div className="text-sm">{config?.version ? `v${config.version}` : "—"}</div>
                </div>
              </header>

              <main className="space-y-6">
                <WalletPanel onVerify={handleVerify} />

                <section className="bg-white/3 rounded-2xl p-6">
                  <h3 className="text-lg font-semibold mb-2">How it works</h3>
                  <ol className="list-decimal ml-5 text-sm text-slate-300 space-y-1">
                    <li>Connect your Solana wallet (Phantom, Solflare, Torus, Coinbase, Ledger).</li>
                    <li>Click <strong>Verify NFT</strong>. App calls backend <code>/api/verify-nft</code>.</li>
                    <li>Backend checks Helius (or RPC) & sends webhook to Telegram bot if verified.</li>
                    <li>Telegram bot grants access to private group.</li>
                  </ol>
                </section>

                <footer className="text-xs text-slate-400 text-center">
                  © {new Date().getFullYear()} Meta Betties Verification — Built with React + Tailwind CSS
                </footer>
              </main>
            </div>
          </div>
        </WalletModalProvider>
      </WalletProvider>
    </ConnectionProvider>
  );
}
