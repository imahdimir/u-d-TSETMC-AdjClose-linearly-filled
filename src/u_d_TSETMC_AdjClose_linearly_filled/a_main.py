"""

    """

from namespace_mahdimir import tse as tse_ns
from namespace_mahdimir import tse_github_data_url as tgdu
from run_py import DefaultDirs

class GDU :
    g = tgdu.GitHubDataUrl()

    adj_price_s = g.adj_price
    tse_wd_s = g.tse_work_days
    tsetmc_adjclose_lin_t = g.tsetmc_adjclose_lin

class Dirs :
    dd = DefaultDirs(make_default_dirs = True)

    gd = dd.gd
    t = dd.t

class FPN :
    dyr = Dirs()

    # temp data
    t0 = dyr.t / 't0.prq'

class ColName :
    frst_d = "FirstDate"
    lst_d = "LastDate"

# class instances %%
c = tse_ns.Col()  # namespace
gdu = GDU()
dyr = Dirs()
fpn = FPN()
cn = ColName()
