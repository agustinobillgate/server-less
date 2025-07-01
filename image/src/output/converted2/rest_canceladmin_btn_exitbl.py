#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import Queasy

p_list_list, P_list = create_model("P_list", {"bezeich":string, "num":int})

def rest_canceladmin_btn_exitbl(p_list_list:[P_list], case_type:int, rec_id:int):

    prepare_cache ([Queasy])

    queasy = None

    p_list = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal queasy
        nonlocal case_type, rec_id


        nonlocal p_list

        return {}

    def fill_new_queasy():

        nonlocal queasy
        nonlocal case_type, rec_id


        nonlocal p_list


        queasy.key = 11
        queasy.number1 = p_list.num
        queasy.char1 = p_list.bezeich


    p_list = query(p_list_list, first=True)

    if case_type == 1:
        queasy = Queasy()
        db_session.add(queasy)

        fill_new_queasy()

    elif case_type == 1:

        queasy = get_cache (Queasy, {"_recid": [(eq, rec_id)]})
        pass
        queasy.char1 = p_list.bezeich
        pass

    return generate_output()