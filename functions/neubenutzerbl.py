#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import Bediener

def neubenutzerbl(case_type:int, name_str:string, id_str:string, nr:int):
    t_bediener_data = []
    bediener = None

    t_bediener = None

    t_bediener_data, T_bediener = create_model_like(Bediener)

    db_session = local_storage.db_session

    def generate_output():
        nonlocal t_bediener_data, bediener
        nonlocal case_type, name_str, id_str, nr


        nonlocal t_bediener
        nonlocal t_bediener_data

        return {"t-bediener": t_bediener_data}

    if case_type == 1:

        bediener = get_cache (Bediener, {"username": [(eq, name_str)],"flag": [(eq, 0)]})

        if bediener:
            t_bediener = T_bediener()
            t_bediener_data.append(t_bediener)

            buffer_copy(bediener, t_bediener)
    elif case_type == 2:

        bediener = get_cache (Bediener, {"username": [(eq, name_str)],"usercode": [(eq, id_str)],"betriebsnr": [(eq, 0)],"flag": [(eq, 0)]})

        if bediener:
            t_bediener = T_bediener()
            t_bediener_data.append(t_bediener)

            buffer_copy(bediener, t_bediener)
    elif case_type == 3:

        for bediener in db_session.query(Bediener).filter(
                 (Bediener.username == (name_str).lower()) & (Bediener.betriebsnr == 1) & (Bediener.flag == 0)).order_by(Bediener._recid).all():
            t_bediener = T_bediener()
            t_bediener_data.append(t_bediener)

            buffer_copy(bediener, t_bediener)
    elif case_type == 4:

        bediener = get_cache (Bediener, {"nr": [(eq, nr)]})

        if bediener:
            t_bediener = T_bediener()
            t_bediener_data.append(t_bediener)

            buffer_copy(bediener, t_bediener)

    return generate_output()