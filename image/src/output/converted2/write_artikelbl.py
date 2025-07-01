#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import Artikel

t_artikel_list, T_artikel = create_model_like(Artikel, {"rec_id":int})

def write_artikelbl(case_type:int, t_artikel_list:[T_artikel]):
    success_flag = False
    artikel = None

    t_artikel = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal success_flag, artikel
        nonlocal case_type


        nonlocal t_artikel

        return {"success_flag": success_flag}

    t_artikel = query(t_artikel_list, first=True)

    if not t_artikel:

        return generate_output()

    if case_type == 1:
        artikel = Artikel()
        db_session.add(artikel)

        buffer_copy(t_artikel, artikel)
        pass
        success_flag = True
    elif case_type == 2:

        artikel = get_cache (Artikel, {"_recid": [(eq, t_artikel.rec_id)]})

        if artikel:
            buffer_copy(t_artikel, artikel)
            pass
            success_flag = True

    return generate_output()