from functions.additional_functions import *
import decimal
from datetime import date
from models import L_artikel, Htparam

def sarticle_list_btn_help1bl(s_artnr:int):
    s_bezeich = ""
    close_date = None
    mm = 0
    yy = 0
    l_artikel = htparam = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal s_bezeich, close_date, mm, yy, l_artikel, htparam


        return {"s_bezeich": s_bezeich, "close_date": close_date, "mm": mm, "yy": yy}


    l_artikel = db_session.query(L_artikel).filter(
            (L_artikel.artnr == s_artnr)).first()
    s_bezeich = l_artikel.bezeich

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

    return generate_output()