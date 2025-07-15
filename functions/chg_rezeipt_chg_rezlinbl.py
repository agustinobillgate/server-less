#using conversion tools version: 1.0.0.117

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


    h_rezept = get_cache (H_rezept, {"_recid": [(eq, h_rezept_recid)]})

    h_rezlin = get_cache (H_rezlin, {"_recid": [(eq, s_rezlin_h_recid)]})
    pass
    h_rezlin.menge =  to_decimal(qty)
    h_rezlin.lostfact =  to_decimal(lostfact)


    pass
    pass
    h_rezept.datummod = get_current_date()
    pass
    artnrlager = h_rezlin.artnrlager

    return generate_output()