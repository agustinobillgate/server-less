from functions.additional_functions import *
import decimal
from datetime import date
from models import Umsatz

def read_umsatzbl(case_type:int, artno:int, deptno:int, datum:date):
    t_umsatz_list = []
    umsatz = None

    t_umsatz = None

    t_umsatz_list, T_umsatz = create_model_like(Umsatz)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal t_umsatz_list, umsatz


        nonlocal t_umsatz
        nonlocal t_umsatz_list
        return {"t-umsatz": t_umsatz_list}

    if case_type == 1:

        umsatz = db_session.query(Umsatz).filter(
                (Umsatz.artnr == artno) &  (Umsatz.departement == deptno) &  (Umsatz.datum == datum)).first()

        if umsatz:
            t_umsatz = T_umsatz()
            t_umsatz_list.append(t_umsatz)

            buffer_copy(umsatz, t_umsatz)

    return generate_output()