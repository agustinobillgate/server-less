#using conversion tools version: 1.0.0.119

from functions.additional_functions import *
from decimal import Decimal
from models import H_rezept, H_rezlin

def chg_rezeipt_chg_rezlinbl(s_rezlin_h_recid:int, h_rezept_recid:int, qty:Decimal, lostfact:Decimal):

    prepare_cache ([H_rezept, H_rezlin])

    artnrlager = 0
    h_rezept = h_rezlin = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal artnrlager, h_rezept, h_rezlin
        nonlocal s_rezlin_h_recid, h_rezept_recid, qty, lostfact

        return {"artnrlager": artnrlager}


    h_rezept = db_session.query(H_rezept).filter(H_rezept._recid == h_rezept_recid).first()

    h_rezlin = db_session.query(H_rezlin).filter(H_rezlin._recid == s_rezlin_h_recid).first()
    
    db_session.refresh(h_rezlin, with_for_update=True)
    h_rezlin.menge =  to_decimal(qty)
    h_rezlin.lostfact =  to_decimal(lostfact)
    db_session.flush()

    db_session.refresh(h_rezept, with_for_update=True)
    h_rezept.datummod = get_current_date()
    db_session.flush()
    
    artnrlager = h_rezlin.artnrlager

    return generate_output()