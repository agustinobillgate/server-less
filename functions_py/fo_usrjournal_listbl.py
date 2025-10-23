#using conversion tools version: 1.0.0.117
#------------------------------------------
# Rd, 27/8/2025
# kolom kosong, output_list.str
#------------------------------------------

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from functions.fo_usrjournal_cldbl import fo_usrjournal_cldbl

def fo_usrjournal_listbl(incl_trans:bool, excl_trans:bool, trans_only:bool, from_date:date, to_date:date, from_dept:int, to_dept:int, from_art:int, to_art:int, usr_init:string, long_digit:bool, foreign_flag:bool):
    fo_usrjourn_list_data = []

    output_list = fo_usrjourn_list = None

    output_list_data, Output_list = create_model("Output_list", {"str":string, "gname":string})
    fo_usrjourn_list_data, Fo_usrjourn_list = create_model("Fo_usrjourn_list", {"rec_id":int, "datum":date, "zinr":string, "rechnr":int, "artnr":int, "bezeich":string, "dept":string, "qty":int, "amount":Decimal, "gname":string, "zeit":string, "id":string, "sysdate":date})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal fo_usrjourn_list_data
        nonlocal incl_trans, excl_trans, trans_only, from_date, to_date, from_dept, to_dept, from_art, to_art, usr_init, long_digit, foreign_flag


        nonlocal output_list, fo_usrjourn_list
        nonlocal output_list_data, fo_usrjourn_list_data

        return {"fo-usrjourn-list": fo_usrjourn_list_data}

    output_list_data = get_output(fo_usrjournal_cldbl(incl_trans, excl_trans, trans_only, from_date, to_date, from_dept, to_dept, from_art, to_art, usr_init, long_digit, foreign_flag))
    fo_usrjourn_list_data.clear()

    for output_list in query(output_list_data):
        fo_usrjourn_list = Fo_usrjourn_list()
        fo_usrjourn_list_data.append(fo_usrjourn_list)

        fo_usrjourn_list.datum = date_mdy(substring(output_list.str, 0, 8))
        fo_usrjourn_list.zinr = substring(output_list.str, 8, 6)
        fo_usrjourn_list.rechnr = to_int(substring(output_list.str, 14, 9))
        fo_usrjourn_list.artnr = to_int(substring(output_list.str, 23, 4))
        fo_usrjourn_list.bezeich = substring(output_list.str, 27, 60)
        fo_usrjourn_list.dept = substring(output_list.str, 87, 22)
        fo_usrjourn_list.qty = to_int(substring(output_list.str, 109, 5))
        fo_usrjourn_list.amount = to_decimal(substring(output_list.str, 114, 17))
        fo_usrjourn_list.gname = output_list.gname
        fo_usrjourn_list.zeit = substring(output_list.str, 131, 8)
        fo_usrjourn_list.id = substring(output_list.str, 139, 4)
        fo_usrjourn_list.sysdate = date_mdy(substring(output_list.str, 143, 8))
        fo_usrjourn_list.rec_id = to_int(substring(output_list.str, 151, 122))

    return generate_output()