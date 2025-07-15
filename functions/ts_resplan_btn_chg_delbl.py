#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import Queasy

def ts_resplan_btn_chg_delbl(s_recid:int):

    prepare_cache ([Queasy])

    t_queasy_data = []
    queasy = None

    t_queasy = None

    t_queasy_data, T_queasy = create_model("T_queasy", {"char1":string, "char2":string, "number3":int, "rec_id":int})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal t_queasy_data, queasy
        nonlocal s_recid


        nonlocal t_queasy
        nonlocal t_queasy_data

        return {"t-queasy": t_queasy_data}

    queasy = get_cache (Queasy, {"_recid": [(eq, s_recid)]})

    if not queasy:

        return generate_output()
    t_queasy = T_queasy()
    t_queasy_data.append(t_queasy)

    t_queasy.char1 = queasy.char1
    t_queasy.char2 = queasy.char2
    t_queasy.number3 = queasy.number3
    t_queasy.rec_id = queasy._recid

    return generate_output()