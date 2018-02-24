#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import glob
import os
import requests

import pandas as pd

N_COINS = 30
T_COST = 0.01 # Average expected transaction cost
TIME_FORMAT = '%Y-%m-%d-%H%M'

DIR = '/Users/lola'

class Index():
    def __init__(self, name, rel_comp, init_val=1000):
        """
        :param: name - the name of the index
        :param: rel_comp - relative composition of the Index i.e. percentage values, k->v: Symbol / relative perc.
        :param: init_val - the initial value of our index in USD
        """
        self.name = name

        # Normalize pdf:
        total = sum(rel_comp.values())
        rel_comp = {k: v/total for k, v in rel_comp.items()}

        newest = max(glob.iglob(f'{DIR}/cmc_data/coin_data/*.csv'))
        df = pd.read_csv(newest)
        df = df[['symbol', 'price_usd']].infer_objects()

        # TODO: Numerics and floating point error??
        self.comp = {sym: init_val * perc / df[df["symbol"] == sym].iloc[0].price_usd
                     for sym, perc in rel_comp.items()}
        print(self.comp)

    def current_price(self):
        """
        Gets the current price of the index.
        """
        newest = max(glob.iglob(f'{DIR}/cmc_data/coin_data/*.csv'))
        df = pd.read_csv(newest).infer_objects()

        price = dict(zip(df.symbol, df.price_usd))

        return sum(amt * price[sym] for sym, amt in self.comp.items())

        # result = 0
        # for sym, amount in self.comp.items():
        #     result += amount * df[df['symbol'] == sym].iloc[0].price_usd
        # return result

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
        # TODO: Need to do some domain research into Indicies such as SPY 500 to see how they choose to update holdings, pay dividends (irrelevant for us), etc.
        # TODO (tech notes): We can just serially record new states for now and calculate differences and transaction costs in a different script that reads from this data.
        newest = max(glob.iglob(f'{DIR}/cmc_data/coin_data/*.csv'))

