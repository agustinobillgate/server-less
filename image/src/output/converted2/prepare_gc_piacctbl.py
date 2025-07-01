#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import Gc_piacct

def prepare_gc_piacctbl():
    t_gc_piacct_list = []
    gc_piacct = None

    t_gc_piacct = None

    t_gc_piacct_list, T_gc_piacct = create_model_like(Gc_piacct)

    db_session = local_storage.db_session

    def generate_output():
        nonlocal t_gc_piacct_list, gc_piacct


        nonlocal t_gc_piacct
        nonlocal t_gc_piacct_list

        return {"t-gc-piacct": t_gc_piacct_list}

    for gc_piacct in db_session.query(Gc_piacct).order_by(Gc_piacct.activeflag, Gc_piacct.nr).all():
        t_gc_piacct = T_gc_piacct()
        t_gc_piacct_list.append(t_gc_piacct)

        buffer_copy(gc_piacct, t_gc_piacct)

    return generate_output()