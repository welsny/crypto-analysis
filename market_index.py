#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import glob
import os
import requests

import pandas as pd

N_COINS = 30
T_COST = 0.01 # Average expected transaction cost
TIME_FORMAT = '%Y-%m-%d-%H%M'

class Index():
    def __init__(self, name, rel_comp, init_val=1000):
        """
        :param: name - the name of the index
        :param: rel_comp - relative composition of the Index i.e. percentage values, k->v: Symbol / relative perc.
        """
        self.name = name

        # Normalize rel_comp to sum = 1.0
        total = sum(rel_comp.values())
        rel_comp = {k: v/total for k, v in rel_comp.items()}

        newest = max(glob.iglob('/Users/lola/cmc_data/coin_data/*.csv'))
        df = pd.read_csv(newest)
        df = df[['symbol', 'price_usd']].infer_objects()

        # TODO: Numerics and floating point error??
        self.comp = {sym: init_val * perc / df[df["symbol"] == sym]["price_usd"].iloc[0]
                     for sym, perc in rel_comp.items()}
        print(self.comp)

    def current_price(self):
        """
        Gets the current price of the index.
        """
        newest = max(glob.iglob('/Users/lola/cmc_data/coin_data/*.csv'))
        df = pd.read_csv(newest)
        df = df[['symbol', 'price_usd']].infer_objects()

        for sym, perc in self.comp.items():
            pass

        #TODO: Calculate Price
        #TODO: Add current price to data file

    def _update_comp(self):
        """
        We get the most recent CMC data and update the composition of our index.

        Compositions and transaction costs are recorded in ~/cmc_data/index_info/{NAME}.json
        1) Read the most recent CMC data.csv
        2) Update self.comp
        3) Record new self.comp and transaction costs**

        We choose to do JSON here instead of CSV since the symbols we include can change over time.
        """
        # TODO: Instead of recording transaction costs, we can just record new states for now since we can calculate differences and transaction costs in a different script.
        newest = max(glob.iglob('/Users/lola/cmc_data/coin_data/*.csv'))
        #TODO: Update composition with this .csv
        #TODO: 

def list_indices():
    """
    Returns a list of all Index objects that we are tracking
    """
    pass

def init_strategies():
    newest = max(glob.iglob('/Users/lola/cmc_data/coin_data/*.csv'))
    df = pd.read_csv(newest)
    df = df[['rank', 'symbol', 'price_usd', 'market_cap_usd', '24h_volume_usd',
             'percent_change_24h', 'percent_change_7d']].infer_objects()

    # We should read from our current file so that when we are running on the Cloud we don't waste resources by making redundant requests
    json = requests.get('https://api.coinmarketcap.com/v1/global/').json()
    total_mkt_cap = json['total_market_cap_usd']
    mktcap_cumsum = 100*df['market_cap_usd'].cumsum()/total_mkt_cap

    """
    top_70_perc
    Minimum amount of coins to cover 70% of the CMC. (Top ~6 coins)
    """
    def top_n_perc(n):
        """
        Return the relative composition of the `top_n_perc` index as a dictionary
        """
        ct = len([i for i in mktcap_cumsum if i < n])
        return {df['symbol'][i]: df['market_cap_usd'][i] for i in range(ct)}
    t_70 = top_n_perc(70)
    t_80 = top_n_perc(80)
    Index("top_70_perc", t_70)
    Index("top_80_perc", t_80)

if __name__ == "__main__":
    init_strategies()
