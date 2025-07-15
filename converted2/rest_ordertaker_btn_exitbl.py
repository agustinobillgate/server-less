#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import Queasy

p_list_data, P_list = create_model("P_list", {"bezeich":string, "code":string, "num":int, "usr_init":string})

def rest_ordertaker_btn_exitbl(p_list_data:[P_list], case_type:int, rec_id:int):

    prepare_cache ([Queasy])

    t_recid = 0
    queasy = None

    p_list = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal t_recid, queasy
        nonlocal case_type, rec_id


        nonlocal p_list

        return {"t_recid": t_recid}

    def fill_new_queasy():

        nonlocal t_recid, queasy
        nonlocal case_type, rec_id


        nonlocal p_list


        queasy.key = 10
        queasy.number1 = p_list.num
        queasy.char1 = p_list.code
        queasy.char2 = p_list.bezeich
        queasy.char3 = p_list.usr_init


    p_list = query(p_list_data, first=True)

    if case_type == 1:
        queasy = Queasy()
        db_session.add(queasy)

        fill_new_queasy()
        pass
        t_recid = queasy._recid

    elif case_type == 2:

        queasy = get_cache (Queasy, {"_recid": [(eq, rec_id)]})
        pass
        queasy.char1 = p_list.code
        queasy.char2 = p_list.bezeich
        queasy.char3 = p_list.usr_init
        pass

    return generate_output()