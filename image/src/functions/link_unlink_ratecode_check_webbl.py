from functions.additional_functions import *
import decimal

def link_unlink_ratecode_check_webbl(case_type:int, inp_tb1char1:str, adjust_combo:str, adjust_value:decimal, inp_char3:str):

    db_session = local_storage.db_session

    def generate_output():
        return {}


    if case_type == 1:

        if inp_char3 == "":
            inp_char3 = ";" + inp_tb1char1 + ";"
        else:

            if substring(inp_char3, len(inp_char3) - 1) != ";":
                inp_char3 = inp_char3 + ";"
            inp_char3 = inp_char3 + inp_tb1char1 + ";"

        if adjust_combo.lower()  == "Using Percentage(%)":
            inp_char3 = inp_char3 + "%" + to_string(adjust_value * 100) + ";"
        else:
            inp_char3 = inp_char3 + "A" + to_string(adjust_value * 100) + ";"
    elif case_type == 2:
        inp_char3 = entry(0, inp_char3, ";") + ";" + entry(1, inp_char3, ";") + ";"

        if adjust_combo.lower()  == "Using Percentage(%)":
            inp_char3 = inp_char3 + "%" + to_string(adjust_value * 100) + ";"
        else:
            inp_char3 = inp_char3 + "A" + to_string(adjust_value * 100) + ";"

    return generate_output()