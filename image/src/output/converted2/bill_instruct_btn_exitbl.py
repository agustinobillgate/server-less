from functions.additional_functions import *
import decimal
from models import Queasy

t_queasy_list, T_queasy = create_model_like(Queasy)

def bill_instruct_btn_exitbl(t_queasy_list:[T_queasy], case_type:int):
    success_flag = False
    queasy = None

    t_queasy = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal success_flag, queasy
        nonlocal case_type


        nonlocal t_queasy
        nonlocal t_queasy_list
        return {"success_flag": success_flag}

    def fill_new_queasy():

        nonlocal success_flag, queasy
        nonlocal case_type


        nonlocal t_queasy
        nonlocal t_queasy_list


        queasy.key = 9
        queasy.number1 = t_queasy.number1
        queasy.char1 = t_queasy.char1
        queasy.logi1 = t_queasy.logi1


    t_queasy = query(t_queasy_list, first=True)

    if case_type == 1:
        queasy = Queasy()
        db_session.add(queasy)

        fill_new_queasy()
        success_flag = True

    elif case_type == 2:

        queasy = db_session.query(Queasy).filter(
                 (Queasy.key == 9) & (Queasy.number1 == t_queasy.number1)).first()

        if queasy:
            queasy.char1 = t_queasy.char1
            queasy.logi1 = t_queasy.logi1
            success_flag = True

    return generate_output()