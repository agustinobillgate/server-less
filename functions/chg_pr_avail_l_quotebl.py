#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import L_quote

def chg_pr_avail_l_quotebl(s_list_artnr:int):
    avail_l_quote = False
    l_quote = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal avail_l_quote, l_quote
        nonlocal s_list_artnr

        return {"avail_l_quote": avail_l_quote}


    l_quote = get_cache (L_quote, {"artnr": [(eq, s_list_artnr)],"lief_nr": [(ne, 0)]})

    if l_quote:
        avail_l_quote = True

    return generate_output()