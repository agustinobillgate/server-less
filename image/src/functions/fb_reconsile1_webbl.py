from functions.additional_functions import *
import decimal
from datetime import date
from functions.fb_reconsile1bl import fb_reconsile1bl

def fb_reconsile1_webbl(pvilanguage:int, from_grp:int, food:int, bev:int, from_date:date, to_date:date, date1:date, date2:date, mi_opt_chk:bool, double_currency:bool, exchg_rate:decimal, foreign_nr:int):
    done = False
    fb_list_list = []

    output_list = fb_list = None

    output_list_list, Output_list = create_model("Output_list", {"curr_counter":int, "nr":int, "store":int, "amount":decimal, "bezeich":str, "s":str})
    fb_list_list, Fb_list = create_model("Fb_list", {"curr_counter":int, "str1":str, "str2":str, "str3":str, "str4":str, "str5":str})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal done, fb_list_list


        nonlocal output_list, fb_list
        nonlocal output_list_list, fb_list_list
        return {"done": done, "fb-list": fb_list_list}

    done, output_list_list = get_output(fb_reconsile1bl(pvilanguage, from_grp, food, bev, from_date, to_date, date1, date2, mi_opt_chk, double_currency, exchg_rate, foreign_nr))

    for output_list in query(output_list_list):
        fb_list = Fb_list()
        fb_list_list.append(fb_list)

        fb_list.curr_counter = output_list.curr_counter
        fb_list.str1 = substring(output_list.s, 0, 24)
        fb_list.str2 = substring(output_list.s, 24, 33)
        fb_list.str3 = substring(output_list.s, 57, 15)
        fb_list.str4 = substring(output_list.s, 72, 15)
        fb_list.str5 = substring(output_list.s, 87, 23)

    return generate_output()