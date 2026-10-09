#!/usr/bin/env python3
import json
import os
import unittest

class TestSuiCoins(unittest.TestCase):
    def setUp(self):
        self.json_file = "coins.json"
        self.assertTrue(os.path.exists(self.json_file), "coins.json does not exist")
        with open(self.json_file, "r", encoding="utf-8") as f:
            self.coins = json.load(f)

    def test_coins_list_not_empty(self):
        self.assertIsInstance(self.coins, list)
        self.assertGreater(len(self.coins), 0, "coins.json should not be empty")

    def test_coins_fields(self):
        sui_found = False
        for coin in self.coins:
            self.assertIn("symbol", coin)
            self.assertIn("name", coin)
            self.assertIsInstance(coin["symbol"], str)
            self.assertIsInstance(coin["name"], str)
            if coin["symbol"].upper() == "SUI":
                sui_found = True
                self.assertIsNotNone(coin.get("coin_type"))
        self.assertTrue(sui_found, "Native SUI token should be in coins.json")

if __name__ == "__main__":
    unittest.main()
