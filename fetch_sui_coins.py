#!/usr/bin/env python3
"""
Script to fetch Sui ecosystem coins from multiple data sources (CoinGecko, DexScreener)
and output a consolidated list of Sui coins.
"""

import json
import urllib.request
import time
import sys

def fetch_coingecko_sui_coins():
    print("Fetching Sui coins from CoinGecko API...")
    coins_map = {}

    # 1. Fetch from coins/list with platform info
    url_list = "https://api.coingecko.com/api/v3/coins/list?include_platform=true"
    try:
        req = urllib.request.Request(url_list, headers={"User-Agent": "Mozilla/5.0"})
        res = urllib.request.urlopen(req)
        data = json.loads(res.read().decode('utf-8'))

        for c in data:
            platforms = c.get("platforms", {}) or {}
            sui_addr = platforms.get("sui")
            if sui_addr:
                cid = c.get("id")
                coins_map[cid] = {
                    "id": cid,
                    "symbol": (c.get("symbol") or "").upper(),
                    "name": c.get("name") or "",
                    "coin_type": sui_addr
                }
    except Exception as e:
        print(f"Warning: Failed to fetch CoinGecko coins list: {e}")

    time.sleep(1)

    # 2. Fetch from sui-ecosystem category markets for additional metadata / coins
    url_cat = "https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&category=sui-ecosystem&per_page=250"
    try:
        req = urllib.request.Request(url_cat, headers={"User-Agent": "Mozilla/5.0"})
        res = urllib.request.urlopen(req)
        cat_data = json.loads(res.read().decode('utf-8'))

        for c in cat_data:
            cid = c.get("id")
            if cid in coins_map:
                coins_map[cid]["image"] = c.get("image")
                coins_map[cid]["current_price_usd"] = c.get("current_price")
                coins_map[cid]["market_cap_usd"] = c.get("market_cap")
            else:
                coins_map[cid] = {
                    "id": cid,
                    "symbol": (c.get("symbol") or "").upper(),
                    "name": c.get("name") or "",
                    "coin_type": None,
                    "image": c.get("image"),
                    "current_price_usd": c.get("current_price"),
                    "market_cap_usd": c.get("market_cap")
                }
    except Exception as e:
        print(f"Warning: Failed to fetch CoinGecko category markets: {e}")

    return list(coins_map.values())


def fetch_dexscreener_sui_coins():
    print("Fetching Sui tokens from DexScreener API...")
    tokens_map = {}

    # Query DexScreener for pairs with Sui
    url = "https://api.dexscreener.com/latest/dex/tokens/0x2::sui::SUI"
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        res = urllib.request.urlopen(req)
        data = json.loads(res.read().decode('utf-8'))
        pairs = data.get("pairs", []) or []

        for pair in pairs:
            if pair.get("chainId") == "sui":
                for token_key in ["baseToken", "quoteToken"]:
                    t = pair.get(token_key, {})
                    addr = t.get("address")
                    if addr and addr not in tokens_map:
                        tokens_map[addr] = {
                            "symbol": (t.get("symbol") or "").upper(),
                            "name": t.get("name") or "",
                            "coin_type": addr
                        }
    except Exception as e:
        print(f"Warning: Failed to fetch DexScreener tokens: {e}")

    return list(tokens_map.values())


def main():
    cg_coins = fetch_coingecko_sui_coins()
    dex_coins = fetch_dexscreener_sui_coins()

    print(f"Fetched {len(cg_coins)} coins from CoinGecko.")
    print(f"Fetched {len(dex_coins)} coins from DexScreener.")

    # Consolidate coins by coin_type / symbol / id
    consolidated = {}

    for c in cg_coins:
        key = c.get("coin_type") or c.get("id")
        consolidated[key] = c

    for d in dex_coins:
        coin_type = d.get("coin_type")
        if coin_type in consolidated:
            if not consolidated[coin_type].get("coin_type"):
                consolidated[coin_type]["coin_type"] = coin_type
        else:
            cid = f"dexscreener-{d['symbol'].lower()}"
            consolidated[coin_type] = {
                "id": cid,
                "symbol": d["symbol"],
                "name": d["name"],
                "coin_type": coin_type
            }

    coin_list = sorted(consolidated.values(), key=lambda x: (x.get("symbol") or "", x.get("name") or ""))

    output_filepath = "coins.json"
    with open(output_filepath, "w", encoding="utf-8") as f:
        json.dump(coin_list, f, indent=2, ensure_ascii=False)

    print(f"Successfully generated {output_filepath} with {len(coin_list)} Sui coins!")

if __name__ == "__main__":
    main()
