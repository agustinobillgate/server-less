from functions.additional_functions import *
import decimal
from datetime import date
from functions.resumz_list_btn_gobl import resumz_list_btn_gobl

def resumz_list_btn_go2bl(ldry_flag:bool, ldry:int, dstore:int, from_dept:int, to_dept:int, from_date:date, to_date:date, detailed:bool, long_digit:bool):
    turn_reportlist_list = []

    output_list = turn_reportlist = None

    output_list_list, Output_list = create_model("Output_list", {"mqty":int, "str":str})
    turn_reportlist_list, Turn_reportlist = create_model("Turn_reportlist", {"artno":int, "descr":str, "day_net":decimal, "day_gros":decimal, "day_proz":decimal, "todate_net":decimal, "todate_gros":decimal, "todate_proz":decimal, "mqty":int})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal turn_reportlist_list


        nonlocal output_list, turn_reportlist
        nonlocal output_list_list, turn_reportlist_list
        return {"turn-reportlist": turn_reportlist_list}

    output_list_list = get_output(resumz_list_btn_gobl(ldry_flag, ldry, dstore, from_dept, to_dept, from_date, to_date, detailed, long_digit))
    turn_reportlist_list.clear()

    for output_list in query(output_list_list):
        turn_reportlist = Turn_reportlist()
        turn_reportlist_list.append(turn_reportlist)

        turn_reportlist.artno = to_int(substring(STR, 0, 5))
        turn_reportlist.descr = substring(STR, 5, 24)
        turn_reportlist.day_net = decimal.Decimal(substring(STR, 29, 14))
        turn_reportlist.day_gros = decimal.Decimal(substring(STR, 43, 14))
        turn_reportlist.day_proz = decimal.Decimal(substring(STR, 57, 7))
        turn_reportlist.todate_net = decimal.Decimal(substring(STR, 64, 15))
        turn_reportlist.todate_gros = decimal.Decimal(substring(STR, 79, 15))
        turn_reportlist.todate_proz = decimal.Decimal(substring(STR, 94, 7))
        turn_reportlist.mqty = output_list.mqty

    return generate_output()