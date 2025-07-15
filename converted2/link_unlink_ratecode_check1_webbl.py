#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import Queasy

def link_unlink_ratecode_check1_webbl(case_type:int, inp_tb1char1:string, adjust_combo:string, adjust_value:Decimal, rate_code:string, inp_char3:string):

    prepare_cache ([Queasy])

    result_message = ""
    found_child:bool = False
    child_code:string = ""
    queasy = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal result_message, found_child, child_code, queasy
        nonlocal case_type, inp_tb1char1, adjust_combo, adjust_value, rate_code, inp_char3

        return {"inp_char3": inp_char3, "result_message": result_message}


    if case_type == 1:

        for queasy in db_session.query(Queasy).filter(
                 (Queasy.key == 2) & (num_entries(Queasy.char3, ";") > 2) & (entry(1, Queasy.char3, ";") == (rate_code).lower())).order_by(Queasy._recid).all():
            child_code = queasy.char1
            found_child = True
            break

        if found_child:
            result_message = "Ratecode has become the parent of child: " + child_code + chr_unicode(10) + "Link ratecode not possible."

            return generate_output()

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