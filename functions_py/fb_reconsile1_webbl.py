#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from functions.fb_reconsile1bl import fb_reconsile1bl

def fb_reconsile1_webbl(pvilanguage:int, from_grp:int, food:int, bev:int, from_date:date, to_date:date, date1:date, date2:date, mi_opt_chk:bool, double_currency:bool, exchg_rate:Decimal, foreign_nr:int):
    done = False
    fb_list_data = []

    output_list = fb_list = None

    output_list_data, Output_list = create_model("Output_list", {"curr_counter":int, "nr":int, "store":int, "amount":Decimal, "bezeich":string, "s":string})
    fb_list_data, Fb_list = create_model("Fb_list", {"curr_counter":int, "str1":string, "str2":string, "str3":string, "str4":string, "str5":string})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal done, fb_list_data
        nonlocal pvilanguage, from_grp, food, bev, from_date, to_date, date1, date2, mi_opt_chk, double_currency, exchg_rate, foreign_nr


        nonlocal output_list, fb_list
        nonlocal output_list_data, fb_list_data

        return {"done": done, "fb-list": fb_list_data}

    done, output_list_data = get_output(fb_reconsile1bl(pvilanguage, from_grp, food, bev, from_date, to_date, date1, date2, mi_opt_chk, double_currency, exchg_rate, foreign_nr))

    for output_list in query(output_list_data, sort_by=[("curr_counter",False)]):
        fb_list = Fb_list()
        fb_list_data.append(fb_list)

        fb_list.curr_counter = output_list.curr_counter
        fb_list.str1 = substring(output_list.s, 0, 24)
        fb_list.str2 = substring(output_list.s, 24, 33)
        fb_list.str3 = substring(output_list.s, 57, 15)
        fb_list.str4 = substring(output_list.s, 72, 15)
        fb_list.str5 = substring(output_list.s, 87, 23)

    return generate_output()