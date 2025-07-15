#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from functions.fb_reconsilehis_cldbl import fb_reconsilehis_cldbl

def fb_reconsilehis_webbl(pvilanguage:int, from_grp:int, food:int, bev:int, from_date:date, to_date:date, ldry:int, dstore:int, double_currency:bool, foreign_nr:int, exchg_rate:Decimal, mi_opt_chk:bool, date1:date, date2:date):
    done = False
    s_list_data = []

    output_list = s_list = None

    output_list_data, Output_list = create_model("Output_list", {"nr":int, "code":int, "bezeich":string, "s":string})
    s_list_data, S_list = create_model("S_list", {"col1":string, "col2":string, "col3":string, "col4":string, "col5":string})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal done, s_list_data
        nonlocal pvilanguage, from_grp, food, bev, from_date, to_date, ldry, dstore, double_currency, foreign_nr, exchg_rate, mi_opt_chk, date1, date2


        nonlocal output_list, s_list
        nonlocal output_list_data, s_list_data

        return {"done": done, "s-list": s_list_data}

    done, output_list_data = get_output(fb_reconsilehis_cldbl(pvilanguage, from_grp, food, bev, from_date, to_date, ldry, dstore, double_currency, foreign_nr, exchg_rate, mi_opt_chk, date1, date2))

    for output_list in query(output_list_data):
        s_list = S_list()
        s_list_data.append(s_list)

        s_list.col1 = substring(output_list.s, 0, 24)
        s_list.col2 = substring(output_list.s, 24, 50)
        s_list.col3 = substring(output_list.s, 74, 18)
        s_list.col4 = substring(output_list.s, 92, 18)
        s_list.col5 = substring(output_list.s, 109, 36)

    return generate_output()