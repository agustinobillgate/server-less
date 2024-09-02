from functions.additional_functions import *
import decimal
from models import L_quote

def chg_pr_avail_l_quotebl(s_list_artnr:int):
    avail_l_quote = False
    l_quote = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal avail_l_quote, l_quote


        return {"avail_l_quote": avail_l_quote}


    l_quote = db_session.query(L_quote).filter(
            (L_quote.artnr == s_list_artnr) &  (L_quote.lief_nr != 0)).first()

    if l_quote:
        avail_l_quote = True

    return generate_output()