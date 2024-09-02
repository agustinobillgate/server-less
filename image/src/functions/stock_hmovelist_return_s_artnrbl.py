from functions.additional_functions import *
import decimal
from datetime import date
from models import L_artikel, Htparam

def stock_hmovelist_return_s_artnrbl(s_bezeich:str, s_artnr:int):
    close_date = None
    mm = 0
    yy = 0
    l_artikel = htparam = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal close_date, mm, yy, l_artikel, htparam


        return {"close_date": close_date, "mm": mm, "yy": yy}


    l_artikel = db_session.query(L_artikel).filter(
            (L_artikel.artnr == s_artnr)).first()

    if l_artikel:

        if l_artikel.endkum <= 2:

            htparam = db_session.query(Htparam).filter(
                    (Htparam.paramnr == 224)).first()
        else:

            htparam = db_session.query(Htparam).filter(
                    (Htparam.paramnr == 221)).first()
        close_date = htparam.fdate
        mm = get_month(close_date) - 1
        yy = get_year(close_date)

        if mm == 0:
            mm = 12
            yy = yy - 1


        s_bezeich = l_artikel.bezeich

    return generate_output()