#using conversion tools version: 1.0.0.117
#-------------------------------------------------------
# Rd, 27/11/2025, with_for_update added
#-------------------------------------------------------
from functions.additional_functions import *
from decimal import Decimal
from models import Artikel, Wgrpgen

def rmaingrp_admin_btn_delbl(wgrpgen_eknr:int):
    flag = 0
    artikel = wgrpgen = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal flag, artikel, wgrpgen
        nonlocal wgrpgen_eknr

        return {"flag": flag}


    artikel = get_cache (Artikel, {"endkum": [(eq, wgrpgen_eknr)]})

    if artikel:
        flag = 1


    else:

        # wgrpgen = get_cache (Wgrpgen, {"eknr": [(eq, wgrpgen_eknr)]})
        wgrpgen = db_session.query(Wgrpgen).filter(
                 (Wgrpgen.eknr == wgrpgen_eknr)).with_for_update().first()

        if wgrpgen:
            pass
            db_session.delete(wgrpgen)
            pass

    return generate_output()