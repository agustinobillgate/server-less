#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import Gc_piacct

def read_gc_piacctbl(case_type:int, int1:int):
    t_gc_piacct_data = []
    gc_piacct = None

    t_gc_piacct = None

    t_gc_piacct_data, T_gc_piacct = create_model_like(Gc_piacct)

    db_session = local_storage.db_session

    def generate_output():
        nonlocal t_gc_piacct_data, gc_piacct
        nonlocal case_type, int1


        nonlocal t_gc_piacct
        nonlocal t_gc_piacct_data

        return {"t-gc-piacct": t_gc_piacct_data}

    if case_type == 1:

        for gc_piacct in db_session.query(Gc_piacct).filter(
                 (Gc_piacct.activeflag == int1)).order_by(Gc_piacct.nr).all():
            t_gc_piacct = T_gc_piacct()
            t_gc_piacct_data.append(t_gc_piacct)

            buffer_copy(gc_piacct, t_gc_piacct)

    return generate_output()