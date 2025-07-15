#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import Queasy, Waehrung

def ratecode_adminbl(case_type:int, int1:int, int2:int, inp_char1:string):
    tb1_data = []
    queasy = waehrung = None

    tb1 = None

    tb1_data, Tb1 = create_model_like(Queasy, {"waehrungsnr":int, "wabkurz":string})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal tb1_data, queasy, waehrung
        nonlocal case_type, int1, int2, inp_char1


        nonlocal tb1
        nonlocal tb1_data

        return {"tb1": tb1_data}

    def cr_tb1():

        nonlocal tb1_data, queasy, waehrung
        nonlocal case_type, int1, int2, inp_char1


        nonlocal tb1
        nonlocal tb1_data


        tb1 = Tb1()
        tb1_data.append(tb1)

        buffer_copy(waehrung, tb1)
        buffer_copy(queasy, tb1)


    if case_type == 1:

        queasy_obj_list = {}
        for queasy, waehrung in db_session.query(Queasy, Waehrung).join(Waehrung,(Waehrung.waehrungsnr == Queasy.number1)).filter(
                 (Queasy.key == int1)).order_by(Queasy.logi2.desc(), Queasy.char2).all():
            if queasy_obj_list.get(queasy._recid):
                continue
            else:
                queasy_obj_list[queasy._recid] = True


            cr_tb1()
    elif case_type == 2:

        queasy_obj_list = {}
        for queasy, waehrung in db_session.query(Queasy, Waehrung).join(Waehrung,(Waehrung.waehrungsnr == Queasy.number1)).filter(
                 (Queasy.key == int1) & (Queasy.char1 >= (inp_char1).lower())).order_by(Queasy.logi2.desc(), Queasy.char1).all():
            if queasy_obj_list.get(queasy._recid):
                continue
            else:
                queasy_obj_list[queasy._recid] = True


            cr_tb1()

    return generate_output()