from functions.additional_functions import *
import decimal
from sqlalchemy import func
from models import Gc_pi

def gc_fundreport_btn_addbl(docu_nr:str):
    t_gc_pi_list = []
    gc_pi = None

    t_gc_pi = None

    t_gc_pi_list, T_gc_pi = create_model_like(Gc_pi)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal t_gc_pi_list, gc_pi


        nonlocal t_gc_pi
        nonlocal t_gc_pi_list
        return {"t-gc-pi": t_gc_pi_list}

    gc_pi = db_session.query(Gc_pi).filter(
            (func.lower(Gc_pi.(docu_nr).lower()) == (docu_nr).lower())).first()
    t_gc_pi = T_gc_pi()
    t_gc_pi_list.append(t_gc_pi)

    buffer_copy(gc_pi, t_gc_pi)

    return generate_output()