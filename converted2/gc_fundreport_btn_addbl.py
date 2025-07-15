#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import Gc_pi

def gc_fundreport_btn_addbl(docu_nr:string):
    t_gc_pi_data = []
    gc_pi = None

    t_gc_pi = None

    t_gc_pi_data, T_gc_pi = create_model_like(Gc_pi)

    db_session = local_storage.db_session

    def generate_output():
        nonlocal t_gc_pi_data, gc_pi
        nonlocal docu_nr


        nonlocal t_gc_pi
        nonlocal t_gc_pi_data

        return {"t-gc-pi": t_gc_pi_data}

    gc_pi = get_cache (Gc_pi, {"docu_nr": [(eq, docu_nr)]})
    t_gc_pi = T_gc_pi()
    t_gc_pi_data.append(t_gc_pi)

    buffer_copy(gc_pi, t_gc_pi)

    return generate_output()