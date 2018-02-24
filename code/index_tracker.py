#!/usr/bin/env python
# -*- coding: utf-8 -*-

from market_index import Index

"""
This script will contain methods for initializing, tracking, and updating index compositions.

TECH NOTES:
    We should create some sample indicies with data that we have now, and implement tracking first.
    Composition update will come much further in the future.
"""

def list_indices():
    """
    Returns a list of all Index objects that we are tracking
    """
    pass

def init_strategies():
    newest = max(glob.iglob(f'{DIR}/cmc_data/coin_data/*.csv'))
    df = pd.read_csv(newest)
    df = df[['rank', 'symbol', 'price_usd', 'market_cap_usd', '24h_volume_usd',
             'percent_change_24h', 'percent_change_7d']].infer_objects()

    # We should read from our current file so that when we are running on the Cloud we don't waste resources by making redundant requests
    newest = max(glob.iglob(f'{DIR}/cmc_data/global_data/*.csv'))
    total_mkt_cap = pd.read_csv(newest).iloc[0].total_market_cap_usd

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
        return dict(zip(df.symbol[:ct], df.market_cap_usd))
    t_70 = top_n_perc(70)
    t_80 = top_n_perc(80)
    Index("top_70_perc", t_70)
    Index("top_80_perc", t_80)

if __name__ == "__main__":
    init_strategies()

