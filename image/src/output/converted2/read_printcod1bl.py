#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import Printcod

def read_printcod1bl(case_type:int, char1:string, char2:string, char3:string):
    t_printcod_list = []
    printcod = None

    t_printcod = None

    t_printcod_list, T_printcod = create_model_like(Printcod)

    db_session = local_storage.db_session

    def generate_output():
        nonlocal t_printcod_list, printcod
        nonlocal case_type, char1, char2, char3


        nonlocal t_printcod
        nonlocal t_printcod_list

        return {"t-printcod": t_printcod_list}

    def assign_it():

        nonlocal t_printcod_list, printcod
        nonlocal case_type, char1, char2, char3


        nonlocal t_printcod
        nonlocal t_printcod_list


        t_printcod = T_printcod()
        t_printcod_list.append(t_printcod)

        buffer_copy(printcod, t_printcod)


    if case_type == 1:

        printcod = get_cache (Printcod, {"emu": [(eq, char1)]})

        if printcod:
            assign_it()
    elif case_type == 2:

        for printcod in db_session.query(Printcod).order_by(Printcod.emu).all():
            assign_it()

    return generate_output()