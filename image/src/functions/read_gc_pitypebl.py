from functions.additional_functions import *
import decimal
from models import Gc_pitype

def read_gc_pitypebl(case_type:int):
    t_gc_pitype_list = []
    gc_pitype = None

    t_gc_pitype = None

    t_gc_pitype_list, T_gc_pitype = create_model_like(Gc_pitype)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal t_gc_pitype_list, gc_pitype


        nonlocal t_gc_pitype
        nonlocal t_gc_pitype_list
        return {"t-gc-pitype": t_gc_pitype_list}

    def assign_it():

        nonlocal t_gc_pitype_list, gc_pitype


        nonlocal t_gc_pitype
        nonlocal t_gc_pitype_list


        t_gc_pitype = T_gc_pitype()
        t_gc_pitype_list.append(t_gc_pitype)

        buffer_copy(gc_pitype, t_gc_pitype)

    if case_type == 1:

        for gc_pitype in db_session.query(Gc_pitype).all():
            assign_it()

    return generate_output()