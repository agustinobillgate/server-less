#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import Queasy

p_list_data, P_list = create_model("P_list", {"bezeich":string, "zeit1":int, "zeit2":int, "shift":int})

def outlet_shiftadmin_btn_exitbl(p_list_data:[P_list], case_type:int, rec_id:int):

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


        queasy.key = 5
        queasy.char1 = p_list.bezeich
        queasy.number1 = p_list.zeit1
        queasy.number2 = p_list.zeit2
        queasy.number3 = p_list.shift


    p_list = query(p_list_data, first=True)

    if not p_list:

        return generate_output()

    if case_type == 1:
        queasy = Queasy()
        db_session.add(queasy)

        fill_new_queasy()

    elif case_type == 2:

        queasy = get_cache (Queasy, {"_recid": [(eq, rec_id)]})
        pass
        queasy.char1 = p_list.bezeich
        queasy.number1 = p_list.zeit1
        queasy.number2 = p_list.zeit2
        queasy.number3 = p_list.shift
        pass

    return generate_output()