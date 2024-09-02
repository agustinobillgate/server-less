from functions.additional_functions import *
import decimal
from sqlalchemy import func
from models import Hoteldpt

def read_hoteldpt1bl(case_type:int, int1:int, int2:int, char1:str):
    t_hoteldpt_list = []
    hoteldpt = None

    t_hoteldpt = None

    t_hoteldpt_list, T_hoteldpt = create_model_like(Hoteldpt)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal t_hoteldpt_list, hoteldpt


        nonlocal t_hoteldpt
        nonlocal t_hoteldpt_list
        return {"t-hoteldpt": t_hoteldpt_list}

    def assign_it():

        nonlocal t_hoteldpt_list, hoteldpt


        nonlocal t_hoteldpt
        nonlocal t_hoteldpt_list


        t_hoteldpt = T_hoteldpt()
        t_hoteldpt_list.append(t_hoteldpt)

        buffer_copy(hoteldpt, t_hoteldpt)


    CASE case_type
    elif  == 1:

        hoteldpt = db_session.query(Hoteldpt).filter(
                (Hoteldpt.num == int1)).first()

        if hoteldpt:
            assign_it()
    elif  == 2:

        hoteldpt = db_session.query(Hoteldpt).filter(
                (func.lower(Hoteldpt.depart) == (char1).lower()) &  (Hoteldpt.num != int1)).first()

        if hoteldpt:
            assign_it()

    return generate_output()