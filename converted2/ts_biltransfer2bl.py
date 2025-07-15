#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import Queasy

def ts_biltransfer2bl(mc_str:string):
    do_it = False
    t_queasy_data = []
    queasy = None

    t_queasy = None

    t_queasy_data, T_queasy = create_model("T_queasy", {"char3":string, "char1":string, "number3":int, "deci3":Decimal})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal do_it, t_queasy_data, queasy
        nonlocal mc_str


        nonlocal t_queasy
        nonlocal t_queasy_data

        return {"do_it": do_it, "t-queasy": t_queasy_data}

    queasy = get_cache (Queasy, {"key": [(eq, 105)],"number2": [(eq, 0)],"deci2": [(eq, 0)],"char2": [(eq, mc_str)],"logi2": [(eq, False)]})
    do_it = None != queasy

    if queasy:
        t_queasy = T_queasy()
        t_queasy_data.append(t_queasy)

        t_queasy.char3 = queasy.char3
        t_queasy.char1 = queasy.char1
        t_queasy.number3 = queasy.number3
        t_queasy.deci3 =  to_decimal(queasy.deci3)

    return generate_output()