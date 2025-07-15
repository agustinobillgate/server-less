#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import Artikel, Queasy

t_artikel_data, T_artikel = create_model_like(Artikel, {"rec_id":int, "minibar":bool})

def write_artikel_1bl(case_type:int, t_artikel_data:[T_artikel]):

    prepare_cache ([Queasy])

    success_flag = False
    artikel = queasy = None

    t_artikel = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal success_flag, artikel, queasy
        nonlocal case_type


        nonlocal t_artikel

        return {"success_flag": success_flag}

    t_artikel = query(t_artikel_data, first=True)

    if not t_artikel:

        return generate_output()

    if case_type == 1:
        artikel = Artikel()
        db_session.add(artikel)

        buffer_copy(t_artikel, artikel)
        pass
        success_flag = True
        queasy = Queasy()
        db_session.add(queasy)

        queasy.key = 266
        queasy.number1 = t_artikel.departement
        queasy.number2 = t_artikel.artnr
        queasy.logi1 = t_artikel.minibar


    elif case_type == 2:

        artikel = get_cache (Artikel, {"_recid": [(eq, t_artikel.rec_id)]})

        if artikel:
            buffer_copy(t_artikel, artikel)
            pass
            success_flag = True

        queasy = get_cache (Queasy, {"key": [(eq, 266)],"number1": [(eq, t_artikel.departement)],"number2": [(eq, t_artikel.artnr)]})

        if not queasy:
            queasy = Queasy()
            db_session.add(queasy)

            queasy.key = 266
            queasy.number1 = t_artikel.departement
            queasy.number2 = t_artikel.artnr
            queasy.logi1 = t_artikel.minibar


        else:
            queasy.logi1 = t_artikel.minibar
        pass

    return generate_output()