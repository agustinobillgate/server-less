from functions.additional_functions import *
import decimal
from models import Queasy

def rest_ordertaker_btn_exitbl(p_list:[P_list], case_type:int, rec_id:int):
    t_recid = 0
    queasy = None

    p_list = None

    p_list_list, P_list = create_model("P_list", {"bezeich":str, "code":str, "num":int, "usr_init":str})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal t_recid, queasy


        nonlocal p_list
        nonlocal p_list_list
        return {"t_recid": t_recid}

    def fill_new_queasy():

        nonlocal t_recid, queasy


        nonlocal p_list
        nonlocal p_list_list


        queasy.key = 10
        queasy.number1 = p_list.num
        queasy.char1 = p_list.code
        queasy.char2 = p_list.bezeich
        queasy.char3 = p_list.usr_init

    p_list = query(p_list_list, first=True)

    if case_type == 1:
        queasy = Queasy()
        db_session.add(queasy)

        fill_new_queasy()

        queasy = db_session.query(Queasy).first()
        t_recid = queasy._recid

    elif case_type == 2:

        queasy = db_session.query(Queasy).filter(
                (Queasy._recid == rec_id)).first()

        queasy = db_session.query(Queasy).first()
        queasy.char1 = p_list.code
        queasy.char2 = p_list.bezeich
        queasy.char3 = p_list.usr_init

        queasy = db_session.query(Queasy).first()

    return generate_output()