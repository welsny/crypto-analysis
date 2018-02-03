#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time
import pandas as pd
import requests
from datetime import datetime

"""
Saves data from CMC into .csv format. N_COINS and DELAY are configurable below.
"""

DIR = '~/cmc_data'
TIME_FORMAT = '%Y-%m-%d-%H%M'
N_COINS = 30
DELAY = 5*60

if __name__ == '__main__':
    while True:
        time_str = datetime.now().strftime(TIME_FORMAT)

        # Individual Coin Data
        df = pd.read_json(f'https://api.coinmarketcap.com/v1/ticker/?limit={N_COINS}')
        df = df[['rank', 'symbol', 'price_usd', 'market_cap_usd', '24h_volume_usd',
                 'percent_change_1h', 'percent_change_24h', 'percent_change_7d']]
        df = df.infer_objects()
        df.to_csv(f'{DIR}/coin_data/{time_str}.csv', index=False)

        # Global Data
        json = requests.get('https://api.coinmarketcap.com/v1/global/').json()
        gdf = pd.DataFrame([json]).infer_objects()
        gdf = gdf[['total_market_cap_usd', 'total_24h_volume_usd',
                   'active_markets', 'active_currencies', 'active_assets']]
        gdf.to_csv(f'{DIR}/global_data/{time_str}.csv', index=False)

        time.sleep(DELAY)

