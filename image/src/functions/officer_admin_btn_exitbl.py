from functions.additional_functions import *
import decimal
from models import Queasy, H_artikel

def officer_admin_btn_exitbl(s_list:[S_list], curr_select:str, rec_id:int):
    err_code = 0
    t_queasy_list = []
    queasy = h_artikel = None

    s_list = t_queasy = None

    s_list_list, S_list = create_model_like(Queasy, {"char4":str})
    t_queasy_list, T_queasy = create_model_like(Queasy, {"rec_id":int})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal err_code, t_queasy_list, queasy, h_artikel


        nonlocal s_list, t_queasy
        nonlocal s_list_list, t_queasy_list
        return {"err_code": err_code, "t-queasy": t_queasy_list}

    def fill_new_queasy():

        nonlocal err_code, t_queasy_list, queasy, h_artikel


        nonlocal s_list, t_queasy
        nonlocal s_list_list, t_queasy_list


        queasy.key = 105
        queasy.number3 = s_list.number3
        queasy.deci3 = s_list.deci3
        queasy.char1 = s_list.char1
        queasy.char2 = s_list.char2
        queasy.char3 = h_artikel.bezeich + "&" + s_list.char4 + "&"


        t_queasy.key = 105
        t_queasy.number3 = s_list.number3
        t_queasy.deci3 = s_list.deci3
        t_queasy.char1 = s_list.char1
        t_queasy.char2 = s_list.char2
        t_queasy.char3 = h_artikel.bezeich + "&" + s_list.char4 + "&"
        t_queasy.rec_id = queasy._recid


    s_list = query(s_list_list, first=True)

    h_artikel = db_session.query(H_artikel).filter(
            (H_artikel.artnr == s_list.number3) &  (H_artikel.departement == 1) &  (H_artikel.artart == 11)).first()

    if not h_artikel:
        err_code = 1

        return generate_output()

    if curr_select.lower()  == "add":
        queasy = Queasy()
        db_session.add(queasy)

        t_queasy = T_queasy()
        t_queasy_list.append(t_queasy)

        fill_new_queasy()

        return generate_output()

    elif curr_select.lower()  == "chg":

        if s_list.char1 == "":
            1
        else:

            queasy = db_session.query(Queasy).filter(
                    (Queasy._recid == rec_id)).first()
            queasy.char1 = s_list.char1
            queasy.char2 = s_list.char2
            queasy.char3 = h_artikel.bezeich + "&" + s_list.char4 + "&"
            queasy.number3 = s_list.number3


            queasy.deci3 = s_list.deci3

            queasy = db_session.query(Queasy).first()
            t_queasy = T_queasy()
            t_queasy_list.append(t_queasy)

            buffer_copy(queasy, t_queasy)
            t_queasy.rec_id = queasy._recid

        return generate_output()