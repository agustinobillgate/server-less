#using conversion tools version: 1.0.0.117

# =============================================
# Rulita, 10-12-2025
# - Added with_for_update before delete query
# =============================================

from functions.additional_functions import *
from decimal import Decimal
from models import H_artikel, Wgrpdep

def rsubgrp_admin_btn_delbl(departement:int, zknr:int):
    flag = 0
    h_artikel = wgrpdep = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal flag, h_artikel, wgrpdep
        nonlocal departement, zknr

        return {"flag": flag}


    # h_artikel = get_cache (H_artikel, {"departement": [(eq, departement)],"zwkum": [(eq, zknr)]})
    h_artikel = db_session.query(H_artikel).filter(
             (H_artikel.departement == departement) & (H_artikel.zwkum == zknr)).first()

    if h_artikel:
        flag = 1
    else:

        # wgrpdep = get_cache (Wgrpdep, {"departement": [(eq, departement)],"zknr": [(eq, zknr)]})
        wgrpdep = db_session.query(Wgrpdep).filter(
                 (Wgrpdep.departement == departement) & (Wgrpdep.zknr == zknr)).with_for_update().first()
        db_session.delete(wgrpdep)
        pass

    return generate_output()