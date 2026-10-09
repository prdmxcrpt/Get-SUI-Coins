# Get Sui Coins

This repository provides a comprehensive list of Sui ecosystem coins (`coins.json`) and a Python script (`fetch_sui_coins.py`) to update the list from multi-chain sources such as CoinGecko and DexScreener.

## Data Overview

`coins.json` contains information on all Sui tokens found, including:
- `id`: Identifier for the coin
- `symbol`: Token ticker symbol (e.g., `SUI`, `USDC`)
- `name`: Full token name
- `coin_type`: Full Sui Move type address (e.g., `0x2::sui::SUI`)
- `image`: URL to token image icon (where available)
- `current_price_usd`: Current price in USD (where available)
- `market_cap_usd`: Market capitalization in USD (where available)

## Updating the Coin List

To re-fetch and update the coin list, run:

```bash
python3 fetch_sui_coins.py
```

## Running Tests

To run the validation test suite:

```bash
python3 test_coins.py
```
