#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import Gc_pitype

def read_gc_pitypebl(case_type:int):
    t_gc_pitype_data = []
    gc_pitype = None

    t_gc_pitype = None

    t_gc_pitype_data, T_gc_pitype = create_model_like(Gc_pitype)

    db_session = local_storage.db_session

    def generate_output():
        nonlocal t_gc_pitype_data, gc_pitype
        nonlocal case_type


        nonlocal t_gc_pitype
        nonlocal t_gc_pitype_data

        return {"t-gc-pitype": t_gc_pitype_data}

    def assign_it():

        nonlocal t_gc_pitype_data, gc_pitype
        nonlocal case_type


        nonlocal t_gc_pitype
        nonlocal t_gc_pitype_data


        t_gc_pitype = T_gc_pitype()
        t_gc_pitype_data.append(t_gc_pitype)

        buffer_copy(gc_pitype, t_gc_pitype)


    if case_type == 1:

        for gc_pitype in db_session.query(Gc_pitype).order_by(Gc_pitype.activeflag, Gc_pitype.nr).all():
            assign_it()

    return generate_output()