#!/usr/bin/env python3
"""
Test script for NFT verification
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from verifier_python import has_nft, get_wallet_nfts_by_collection

def test_nft_detection():
    """Test NFT detection with different wallet addresses"""

    # Test wallets (some with NFTs, some without)
    test_wallets = [
        "EFwPVHhY6vH64MsMDx9ub8Edn4ktYYBcgqNYki1R3rmE",  # Test wallet
  # Another example
    ]

    print("🧪 Testing NFT Detection (Any NFT will pass)...")
    print("=" * 50)

    for i, wallet in enumerate(test_wallets, 1):
        print(f"\n🔍 Test {i}: Wallet {wallet}")
        print("-" * 30)

        try:
            # Test general NFT detection (no collection filter)
            print("🔄 Testing general NFT detection...")
            nfts_general = get_wallet_nfts_by_collection(wallet)
            print(f"General NFTs found: {len(nfts_general) if nfts_general else 0}")

            # Test has_nft function (any NFT will pass)
            print("🔄 Testing has_nft function...")
            has_nft_result, count = has_nft(wallet)
            print(f"has_nft result: {has_nft_result}, count: {count}")

            if has_nft_result:
                print("✅ Verification: PASSED (has NFTs)")
            else:
                print("❌ Verification: FAILED (no NFTs)")

        except Exception as e:
            print(f"❌ Error testing wallet {wallet}: {e}")

        print("-" * 30)

if __name__ == "__main__":
    test_nft_detection() 