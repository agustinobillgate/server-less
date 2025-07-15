#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal

def link_unlink_ratecode_check_webbl(case_type:int, inp_tb1char1:string, adjust_combo:string, adjust_value:Decimal, inp_char3:string):


    db_session = local_storage.db_session

    def generate_output():
        nonlocal case_type, inp_tb1char1, adjust_combo, adjust_value, inp_char3

        return {"inp_char3": inp_char3}


    if case_type == 1:

        if inp_char3 == "":
            inp_char3 = ";" + inp_tb1char1 + ";"
        else:

            if substring(inp_char3, length(inp_char3) - 1) != (";").lower() :
                inp_char3 = inp_char3 + ";"
            inp_char3 = inp_char3 + inp_tb1char1 + ";"

        if adjust_combo.lower()  == ("Using Percentage(%)").lower() :
            inp_char3 = inp_char3 + "%" + to_string(adjust_value * 100) + ";"
        else:
            inp_char3 = inp_char3 + "A" + to_string(adjust_value * 100) + ";"
    elif case_type == 2:
        inp_char3 = entry(0, inp_char3, ";") + ";" + entry(1, inp_char3, ";") + ";"

        if adjust_combo.lower()  == ("Using Percentage(%)").lower() :
            inp_char3 = inp_char3 + "%" + to_string(adjust_value * 100) + ";"
        else:
            inp_char3 = inp_char3 + "A" + to_string(adjust_value * 100) + ";"

    return generate_output()