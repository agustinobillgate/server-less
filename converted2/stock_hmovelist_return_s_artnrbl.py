#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import L_artikel, Htparam

def stock_hmovelist_return_s_artnrbl(s_bezeich:string, s_artnr:int):

    prepare_cache ([L_artikel, Htparam])

    close_date = None
    mm = None
    yy = None
    l_artikel = htparam = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal close_date, mm, yy, l_artikel, htparam
        nonlocal s_bezeich, s_artnr

        return {"s_bezeich": s_bezeich, "close_date": close_date, "mm": mm, "yy": yy}


    l_artikel = get_cache (L_artikel, {"artnr": [(eq, s_artnr)]})

    if l_artikel:

        if l_artikel.endkum <= 2:

            htparam = get_cache (Htparam, {"paramnr": [(eq, 224)]})
        else:

            htparam = get_cache (Htparam, {"paramnr": [(eq, 221)]})
        close_date = htparam.fdate
        mm = get_month(close_date) - 1
        yy = get_year(close_date)

        if mm == 0:
            mm = 12
            yy = yy - 1


        s_bezeich = l_artikel.bezeich

    return generate_output()