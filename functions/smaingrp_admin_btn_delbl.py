#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import L_hauptgrp, L_artikel

def smaingrp_admin_btn_delbl(l_hauptgrp_endkum:int):
    flag = 0
    l_hauptgrp = l_artikel = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal flag, l_hauptgrp, l_artikel
        nonlocal l_hauptgrp_endkum

        return {"flag": flag}


    l_hauptgrp = get_cache (L_hauptgrp, {"endkum": [(eq, l_hauptgrp_endkum)]})

    l_artikel = get_cache (L_artikel, {"endkum": [(eq, l_hauptgrp_endkum)]})

    if l_artikel:
        flag = 1
    else:
        pass
        db_session.delete(l_hauptgrp)

    return generate_output()