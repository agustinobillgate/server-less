#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import Akt_kont

t_akt_kont_data, T_akt_kont = create_model_like(Akt_kont)

def write_akt_kontbl(case_type:int, t_akt_kont_data:[T_akt_kont]):
    success_flag = False
    akt_kont = None

    t_akt_kont = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal success_flag, akt_kont
        nonlocal case_type


        nonlocal t_akt_kont

        return {"success_flag": success_flag}

    if case_type == 1:

        t_akt_kont = query(t_akt_kont_data, first=True)

        if not t_akt_kont:

            return generate_output()

        akt_kont = get_cache (Akt_kont, {"gastnr": [(eq, t_akt_kont.gastnr)],"kontakt_nr": [(eq, t_akt_kont.kontakt_nr)]})

        if not akt_kont:
            akt_kont = Akt_kont()
            db_session.add(akt_kont)

        buffer_copy(t_akt_kont, akt_kont)
        pass
        success_flag = True
    elif case_type == 2:

        t_akt_kont = query(t_akt_kont_data, first=True)

        if not t_akt_kont:

            return generate_output()

        akt_kont = get_cache (Akt_kont, {"gastnr": [(eq, t_akt_kont.gastnr)],"kontakt_nr": [(eq, t_akt_kont.kontakt_nr)]})

        if akt_kont:
            db_session.delete(akt_kont)
            pass
            success_flag = True
    elif case_type == 3:

        t_akt_kont = query(t_akt_kont_data, first=True)

        if not t_akt_kont:

            return generate_output()
        akt_kont = Akt_kont()
        db_session.add(akt_kont)

        buffer_copy(t_akt_kont, akt_kont)
        success_flag = True

    return generate_output()