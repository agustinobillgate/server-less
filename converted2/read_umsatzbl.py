#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Umsatz

def read_umsatzbl(case_type:int, artno:int, deptno:int, datum:date):
    t_umsatz_data = []
    umsatz = None

    t_umsatz = None

    t_umsatz_data, T_umsatz = create_model_like(Umsatz)

    db_session = local_storage.db_session

    def generate_output():
        nonlocal t_umsatz_data, umsatz
        nonlocal case_type, artno, deptno, datum


        nonlocal t_umsatz
        nonlocal t_umsatz_data

        return {"t-umsatz": t_umsatz_data}

    if case_type == 1:

        umsatz = get_cache (Umsatz, {"artnr": [(eq, artno)],"departement": [(eq, deptno)],"datum": [(eq, datum)]})

        if umsatz:
            t_umsatz = T_umsatz()
            t_umsatz_data.append(t_umsatz)

            buffer_copy(umsatz, t_umsatz)

    return generate_output()