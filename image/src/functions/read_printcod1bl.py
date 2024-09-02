from functions.additional_functions import *
import decimal
from sqlalchemy import func
from models import Printcod

def read_printcod1bl(case_type:int, char1:str, char2:str, char3:str):
    t_printcod_list = []
    printcod = None

    t_printcod = None

    t_printcod_list, T_printcod = create_model_like(Printcod)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal t_printcod_list, printcod


        nonlocal t_printcod
        nonlocal t_printcod_list
        return {"t-printcod": t_printcod_list}

    def assign_it():

        nonlocal t_printcod_list, printcod


        nonlocal t_printcod
        nonlocal t_printcod_list


        t_printcod = T_printcod()
        t_printcod_list.append(t_printcod)

        buffer_copy(printcod, t_printcod)

    if case_type == 1:

        printcod = db_session.query(Printcod).filter(
                (func.lower(Printcod.emu) == (char1).lower())).first()

        if printcod:
            assign_it()
    elif case_type == 2:

        for printcod in db_session.query(Printcod).all():
            assign_it()

    return generate_output()