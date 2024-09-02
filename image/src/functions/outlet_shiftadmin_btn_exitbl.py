from functions.additional_functions import *
import decimal
from models import Queasy

def outlet_shiftadmin_btn_exitbl(p_list:[P_list], case_type:int, rec_id:int):
    queasy = None

    p_list = None

    p_list_list, P_list = create_model("P_list", {"bezeich":str, "zeit1":int, "zeit2":int, "shift":int})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal queasy


        nonlocal p_list
        nonlocal p_list_list
        return {}

    def fill_new_queasy():

        nonlocal queasy


        nonlocal p_list
        nonlocal p_list_list


        queasy.key = 5
        queasy.char1 = p_list.bezeich
        queasy.number1 = p_list.zeit1
        queasy.number2 = p_list.zeit2
        queasy.number3 = p_list.shift

    p_list = query(p_list_list, first=True)

    if not p_list:

        return generate_output()

    if case_type == 1:
        queasy = Queasy()
        db_session.add(queasy)

        fill_new_queasy()

    elif case_type == 2:

        queasy = db_session.query(Queasy).filter(
                (Queasy._recid == rec_id)).first()

        queasy = db_session.query(Queasy).first()
        queasy.char1 = p_list.bezeich
        queasy.number1 = p_list.zeit1
        queasy.number2 = p_list.zeit2
        queasy.number3 = p_list.shift

        queasy = db_session.query(Queasy).first()

    return generate_output()