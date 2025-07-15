#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from functions.fo_cashgjournbl import fo_cashgjournbl

bline_list_data, Bline_list = create_model("Bline_list", {"flag":int, "userinit":string, "selected":bool, "name":string, "bl_recid":int})

def fo_cashgjourn_listbl(pvilanguage:int, case_type:int, curr_shift:int, summary_flag:bool, from_date:date, bline_list_data:[Bline_list]):
    double_currency = False
    foreign_curr = ""
    fo_cashjour_list_data = []

    bline_list = output_list = fo_cashjour_list = None

    output_list_data, Output_list = create_model("Output_list", {"flag":string, "amt_foreign":Decimal, "str_foreign":string, "str":string, "gname":string})
    fo_cashjour_list_data, Fo_cashjour_list = create_model("Fo_cashjour_list", {"datum":date, "zinr":string, "rechnr":int, "artnr":int, "bezeich":string, "dept":string, "l_amount":Decimal, "f_amount":Decimal, "gname":string, "zeit":string, "id":string})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal double_currency, foreign_curr, fo_cashjour_list_data
        nonlocal pvilanguage, case_type, curr_shift, summary_flag, from_date


        nonlocal bline_list, output_list, fo_cashjour_list
        nonlocal output_list_data, fo_cashjour_list_data

        return {"from_date": from_date, "double_currency": double_currency, "foreign_curr": foreign_curr, "bline-list": bline_list_data, "fo-cashjour-list": fo_cashjour_list_data}


    from_date, double_currency, foreign_curr, bline_list_data, output_list_data = get_output(fo_cashgjournbl(pvilanguage, case_type, curr_shift, summary_flag, from_date, bline_list_data))
    fo_cashjour_list_data.clear()

    for output_list in query(output_list_data):
        fo_cashjour_list = Fo_cashjour_list()
        fo_cashjour_list_data.append(fo_cashjour_list)

        fo_cashjour_list.datum = date_mdy(substring(output_list.str, 0, 8))
        fo_cashjour_list.zinr = substring(output_list.str, 8, 6)
        fo_cashjour_list.rechnr = to_int(substring(output_list.str, 14, 9))
        fo_cashjour_list.artnr = to_int(substring(output_list.str, 23, 4))
        fo_cashjour_list.bezeich = substring(output_list.str, 27, 40)
        fo_cashjour_list.dept = substring(output_list.str, 67, 17)
        fo_cashjour_list.l_amount = to_decimal(substring(output_list.str, 84, 17))
        fo_cashjour_list.f_amount =  to_decimal(to_decimal(output_list.str_foreign) )
        fo_cashjour_list.gname = output_list.gname
        fo_cashjour_list.zeit = substring(output_list.str, 101, 8)
        fo_cashjour_list.id = substring(output_list.str, 109, 3)

    return generate_output()