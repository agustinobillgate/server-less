#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import Queasy, H_artikel

s_list_data, S_list = create_model_like(Queasy, {"char4":string})

def officer_admin_btn_exitbl(s_list_data:[S_list], curr_select:string, rec_id:int):

    prepare_cache ([H_artikel])

    err_code = 0
    t_queasy_data = []
    queasy = h_artikel = None

    s_list = t_queasy = None

    t_queasy_data, T_queasy = create_model_like(Queasy, {"rec_id":int})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal err_code, t_queasy_data, queasy, h_artikel
        nonlocal curr_select, rec_id


        nonlocal s_list, t_queasy
        nonlocal t_queasy_data

        return {"err_code": err_code, "t-queasy": t_queasy_data}

    def fill_new_queasy():

        nonlocal err_code, t_queasy_data, queasy, h_artikel
        nonlocal curr_select, rec_id


        nonlocal s_list, t_queasy
        nonlocal t_queasy_data


        queasy.key = 105
        queasy.number3 = s_list.number3
        queasy.deci3 =  to_decimal(s_list.deci3)
        queasy.char1 = s_list.char1
        queasy.char2 = s_list.char2
        queasy.char3 = h_artikel.bezeich + "&" + s_list.char4 + "&"


        t_queasy.key = 105
        t_queasy.number3 = s_list.number3
        t_queasy.deci3 =  to_decimal(s_list.deci3)
        t_queasy.char1 = s_list.char1
        t_queasy.char2 = s_list.char2
        t_queasy.char3 = h_artikel.bezeich + "&" + s_list.char4 + "&"
        t_queasy.rec_id = queasy._recid

    s_list = query(s_list_data, first=True)

    h_artikel = get_cache (H_artikel, {"artnr": [(eq, s_list.number3)],"departement": [(eq, 1)],"artart": [(eq, 11)]})

    if not h_artikel:
        err_code = 1

        return generate_output()

    if curr_select.lower()  == ("add").lower() :
        queasy = Queasy()
        db_session.add(queasy)

        t_queasy = T_queasy()
        t_queasy_data.append(t_queasy)

        fill_new_queasy()

        return generate_output()

    elif curr_select.lower()  == ("chg").lower() :

        if s_list.char1 == "":
            pass
        else:

            queasy = get_cache (Queasy, {"_recid": [(eq, rec_id)]})
            queasy.char1 = s_list.char1
            queasy.char2 = s_list.char2
            queasy.char3 = h_artikel.bezeich + "&" + s_list.char4 + "&"
            queasy.number3 = s_list.number3


            queasy.deci3 =  to_decimal(s_list.deci3)
            pass
            t_queasy = T_queasy()
            t_queasy_data.append(t_queasy)

            buffer_copy(queasy, t_queasy)
            t_queasy.rec_id = queasy._recid

        return generate_output()

    return generate_output()