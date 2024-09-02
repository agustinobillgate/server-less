from functions.additional_functions import *
import decimal
from datetime import date
from functions.fb_reconsilehisbl import fb_reconsilehisbl

def fb_reconsilehis_webbl(pvilanguage:int, from_grp:int, food:int, bev:int, from_date:date, to_date:date, ldry:int, dstore:int, double_currency:bool, foreign_nr:int, exchg_rate:decimal, mi_opt_chk:bool, date1:date, date2:date):
    done = False
    s_list_list = []

    output_list = s_list = None

    output_list_list, Output_list = create_model("Output_list", {"nr":int, "code":int, "bezeich":str, "s":str})
    s_list_list, S_list = create_model("S_list", {"col1":str, "col2":str, "col3":str, "col4":str, "col5":str})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal done, s_list_list


        nonlocal output_list, s_list
        nonlocal output_list_list, s_list_list
        return {"done": done, "s-list": s_list_list}

    done, output_list_list = get_output(fb_reconsilehisbl(pvilanguage, from_grp, food, bev, from_date, to_date, ldry, dstore, double_currency, foreign_nr, exchg_rate, mi_opt_chk, date1, date2))

    for output_list in query(output_list_list):
        s_list = S_list()
        s_list_list.append(s_list)

        s_list.col1 = substring(output_list.s, 0, 24)
        s_list.col2 = substring(output_list.s, 24, 33)
        s_list.col3 = substring(output_list.s, 57, 15)
        s_list.col4 = substring(output_list.s, 72, 15)
        s_list.col5 = substring(output_list.s, 87, 23)

    return generate_output()