from functions.additional_functions import *
import decimal
from datetime import date
from functions.ar_debtlistbl import ar_debtlistbl

def ar_debtlist_btn_gobl(pvilanguage:int, from_name:str, to_name:str, from_date:date, to_date:date, from_art:int, to_art:int, tot_flag:bool, lesspay:bool, show_inv:bool):
    d_rechnr = 0
    output_list_list = []
    edit_list_list = []
    msg_str = ""
    lvcarea:str = "ar_debtlist"

    output_list = edit_list = None

    output_list_list, Output_list = create_model("Output_list", {"ar_recid":int, "info":str, "wabkurz":str, "maildate":date, "inv_no":str, "str":str, "ref_no1":int, "ref_no2":str, "ci_date":date, "co_date":date, "nights":int})
    edit_list_list, Edit_list = create_model("Edit_list", {"rechnr":int, "datum":date, "zinr":str, "billname":str, "lamt":decimal, "famt":decimal, "fcurr":str, "ar_recid":int, "amt_change":bool, "curr_change":bool, "curr_nr":int})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal d_rechnr, output_list_list, edit_list_list, msg_str, lvcarea


        nonlocal output_list, edit_list
        nonlocal output_list_list, edit_list_list
        return {"d_rechnr": d_rechnr, "output-list": output_list_list, "edit-list": edit_list_list, "msg_str": msg_str}

    d_rechnr, output_list_list, edit_list_list = get_output(ar_debtlistbl(from_name, to_name, from_date, to_date, from_art, to_art, tot_flag, lesspay, show_inv))

    if show_inv and d_rechnr != 0:
        msg_str = translateExtended ("Bill ", lvcarea, "") + to_string(d_rechnr) + " " + translateExtended ("no longer exists.", lvcarea, "")

    return generate_output()