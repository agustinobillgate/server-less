#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import Gc_giro

def read_gc_girobl(case_type:int):
    t_gc_giro_data = []
    gc_giro = None

    t_gc_giro = None

    t_gc_giro_data, T_gc_giro = create_model_like(Gc_giro, {"rec_id":int})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal t_gc_giro_data, gc_giro
        nonlocal case_type


        nonlocal t_gc_giro
        nonlocal t_gc_giro_data

        return {"t-gc-giro": t_gc_giro_data}

    def assign_it():

        nonlocal t_gc_giro_data, gc_giro
        nonlocal case_type


        nonlocal t_gc_giro
        nonlocal t_gc_giro_data


        t_gc_giro = T_gc_giro()
        t_gc_giro_data.append(t_gc_giro)

        buffer_copy(gc_giro, t_gc_giro)
        t_gc_giro.rec_id = gc_giro._recid


    if case_type == 1:

        for gc_giro in db_session.query(Gc_giro).order_by(Gc_giro._recid).all():
            assign_it()
    elif case_type == 2:

        for gc_giro in db_session.query(Gc_giro).filter(
                 (Gc_giro.giro_status == 0)).order_by(Gc_giro._recid).all():
            assign_it()

    return generate_output()