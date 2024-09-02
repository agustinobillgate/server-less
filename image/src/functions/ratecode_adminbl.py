from functions.additional_functions import *
import decimal
from sqlalchemy import func
from models import Queasy, Waehrung

def ratecode_adminbl(case_type:int, int1:int, int2:int, inp_char1:str):
    tb1_list = []
    queasy = waehrung = None

    tb1 = None

    tb1_list, Tb1 = create_model_like(Queasy, {"waehrungsnr":int, "wabkurz":str})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal tb1_list, queasy, waehrung


        nonlocal tb1
        nonlocal tb1_list
        return {"tb1": tb1_list}

    def cr_tb1():

        nonlocal tb1_list, queasy, waehrung


        nonlocal tb1
        nonlocal tb1_list


        tb1 = Tb1()
        tb1_list.append(tb1)

        buffer_copy(waehrung, tb1)
        buffer_copy(queasy, tb1)

    if case_type == 1:

        queasy_obj_list = []
        for queasy, waehrung in db_session.query(Queasy, Waehrung).join(Waehrung,(Waehrungsnr == Queasy.number1)).filter(
                (Queasy.key == int1)).all():
            if queasy._recid in queasy_obj_list:
                continue
            else:
                queasy_obj_list.append(queasy._recid)


            cr_tb1()
    elif case_type == 2:

        queasy_obj_list = []
        for queasy, waehrung in db_session.query(Queasy, Waehrung).join(Waehrung,(Waehrungsnr == Queasy.number1)).filter(
                (Queasy.key == int1) &  (func.lower(Queasy.char1) >= (inp_char1).lower())).all():
            if queasy._recid in queasy_obj_list:
                continue
            else:
                queasy_obj_list.append(queasy._recid)


            cr_tb1()

    return generate_output()