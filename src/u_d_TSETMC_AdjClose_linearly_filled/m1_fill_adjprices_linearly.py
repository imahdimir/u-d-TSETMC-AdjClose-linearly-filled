"""
    Assumptions:
        - Only open dates of each ticker have data on adj price data. I.e., Close days are absent.

    """

import pandas as pd
from githubdata import get_data_wo_double_clone
from mirutil.df import save_df_as_prq

from .a_main import *

def get_adj_prices() :
    return get_data_wo_double_clone(gdu.adj_price_s)

def keep_relevant_cols(df) :
    c2k = {
            c.ftic   : None ,
            c.d      : None ,
            c.aclose : None ,
            }

    df = df[c2k.keys()]

    return df

def convert_adj_price_to_py_float(df) :
    df[c.aclose] = df[c.aclose].astype(float)
    return df

def assert_no_nan_adj_price(df) :
    assert df[c.aclose].notna().all() , "There are some nan prices."

def get_tse_work_days() :
    # get tse working days data
    return get_data_wo_double_clone(gdu.tse_wd_s)

def keep_only_open_dates_of_tse(df) :
    msk = df[c.is_tse_open].eq(True)
    df = df[msk]
    return df

def find_first_and_last_day_for_each_firm(df) :
    df[cn.frst_d] = df.groupby(c.ftic)[c.d].transform("min")
    df[cn.lst_d] = df.groupby(c.ftic)[c.d].transform("max")
    return df

def make_all_days_for_each_ticker_if_mkt_open(df_price , df_market_open) :
    # keep ticker and first and last day of each ticker
    df1 = df_price[[c.ftic , cn.frst_d , cn.lst_d]].drop_duplicates()

    # make all days for each ticker if market open, cartesian product
    df = pd.merge(df_market_open , df1 , how = 'cross')

    # keep only days between first and last day of each ticker
    msk = df[c.d].le(df[cn.lst_d])
    msk &= df[c.d].ge(df[cn.frst_d])

    df = df[msk]

    # add price data to each day
    df = pd.merge(df , df_price , how = 'left')

    # sort on date
    df = df.sort_values(by = [c.d])

    return df

def assert_no_duplicate_rows(df) :
    """ no dup rows on (ticker, date) pair """
    msk = df.duplicated(subset = [c.ftic , c.d] , keep = False)
    df1 = df[msk]
    assert df1.empty , "There are duplicated rows"

def gen_is_tic_open_col(df) :
    df[c.is_tic_open] = df[c.aclose].notna()
    return df

def gen_linearly_filled_adj_close(df) :
    df[c.aclose] = df[c.aclose].astype(float)

    # groupby by ticker and fill na linearly
    gps = df.groupby(c.ftic , group_keys = False)
    df[c.aclose_lin] = gps.apply(lambda x : x[[c.aclose]].interpolate())

    assert df[c.aclose_lin].notna().all() , "There are nan lin filled prices."

    return df

def reorder_cols_and_sort(df) :
    colord = {
            c.ftic        : None ,
            c.d           : None ,
            c.jd          : None ,
            c.wd          : None ,
            c.is_tic_open : None ,
            c.aclose      : None ,
            c.aclose_lin  : None ,
            }

    df = df[colord.keys()]

    df = df.sort_values(by = [c.ftic , c.d])

    return df

def main() :
    pass

    ##

    dfp = get_adj_prices()
    dfp = keep_relevant_cols(dfp)
    dfp = convert_adj_price_to_py_float(dfp)
    assert_no_nan_adj_price(dfp)

    ##

    dfw = get_tse_work_days()
    dfw = keep_only_open_dates_of_tse(dfw)

    ##

    dfp = find_first_and_last_day_for_each_firm(dfp)
    df = make_all_days_for_each_ticker_if_mkt_open(dfp , dfw)

    ##

    assert_no_duplicate_rows(df)

    ##

    df = gen_is_tic_open_col(df)

    ##

    df = gen_linearly_filled_adj_close(df)

    ##

    df = reorder_cols_and_sort(df)

    ##

    save_df_as_prq(df , fpn.t0)

##
if __name__ == "__main__" :
    main()
