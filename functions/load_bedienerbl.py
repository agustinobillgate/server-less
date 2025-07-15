#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import Bediener

def load_bedienerbl(case_type:int, int1:int, int2:int, char1:string):
    t_bediener_data = []
    bediener = None

    t_bediener = None

    t_bediener_data, T_bediener = create_model_like(Bediener, {"rec_id":int})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal t_bediener_data, bediener
        nonlocal case_type, int1, int2, char1


        nonlocal t_bediener
        nonlocal t_bediener_data

        return {"t-bediener": t_bediener_data}

    if case_type == 1:

        for bediener in db_session.query(Bediener).filter(
                 (Bediener.flag == int1) & (Bediener.username >= (char1).lower())).order_by(Bediener._recid).all():
            t_bediener = T_bediener()
            t_bediener_data.append(t_bediener)

            buffer_copy(bediener, t_bediener)
            t_bediener.rec_id = bediener._recid
    elif case_type == 2:

        for bediener in db_session.query(Bediener).order_by(Bediener._recid).all():
            t_bediener = T_bediener()
            t_bediener_data.append(t_bediener)

            buffer_copy(bediener, t_bediener)
            t_bediener.rec_id = bediener._recid
    elif case_type == 3:

        for bediener in db_session.query(Bediener).filter(
                 (Bediener.flag == int1)).order_by(Bediener._recid).all():
            t_bediener = T_bediener()
            t_bediener_data.append(t_bediener)

            buffer_copy(bediener, t_bediener)
            t_bediener.rec_id = bediener._recid
    elif case_type == 4:

        bediener = get_cache (Bediener, {"user_group": [(eq, int1)],"flag": [(eq, int2)]})

        if bediener:
            t_bediener = T_bediener()
            t_bediener_data.append(t_bediener)

            buffer_copy(bediener, t_bediener)
            t_bediener.rec_id = bediener._recid
    elif case_type == 5:

        bediener = get_cache (Bediener, {"_recid": [(eq, int1)]})

        if bediener:
            t_bediener = T_bediener()
            t_bediener_data.append(t_bediener)

            buffer_copy(bediener, t_bediener)
            t_bediener.rec_id = bediener._recid
    elif case_type == 6:

        for bediener in db_session.query(Bediener).filter(
                 (Bediener.nr != 0)).order_by(Bediener._recid).all():
            t_bediener = T_bediener()
            t_bediener_data.append(t_bediener)

            buffer_copy(bediener, t_bediener)
            t_bediener.rec_id = bediener._recid

    return generate_output()