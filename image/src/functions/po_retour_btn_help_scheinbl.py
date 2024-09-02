from functions.additional_functions import *
import decimal
from sqlalchemy import func
from models import L_kredit, L_ophdr, L_lager

def po_retour_btn_help_scheinbl(l_orderhdr_docu_nr:str, l_orderhdr_lief_nr:int, docu_nr:str, lscheinnr:str):
    curr_lager = 0
    lager_bezeich = ""
    err_code = 0
    l_kredit = l_ophdr = l_lager = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal curr_lager, lager_bezeich, err_code, l_kredit, l_ophdr, l_lager


        return {"curr_lager": curr_lager, "lager_bezeich": lager_bezeich, "err_code": err_code}


    l_kredit = db_session.query(L_kredit).filter(
            (func.lower(L_kredit.name) == (l_orderhdr_docu_nr).lower()) &  (L_kredit.lief_nr == l_orderhdr_lief_nr) &  (L_kredit.zahlkonto > 0)).first()

    if l_kredit:
        err_code = 1

        return generate_output()

    l_ophdr = db_session.query(L_ophdr).filter(
            (func.lower(L_ophdr.(docu_nr).lower()) == (docu_nr).lower()) &  (func.lower(L_ophdr.(lscheinnr).lower()) == (lscheinnr).lower())).first()
    curr_lager = l_ophdr.lager_nr

    l_lager = db_session.query(L_lager).filter(
            (L_lager.lager_nr == curr_lager)).first()
    lager_bezeich = l_lager.bezeich

    return generate_output()