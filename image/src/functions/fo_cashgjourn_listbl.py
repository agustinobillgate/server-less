from functions.additional_functions import *
import decimal
from datetime import date
from functions.fo_cashgjournbl import fo_cashgjournbl

def fo_cashgjourn_listbl(pvilanguage:int, case_type:int, curr_shift:int, summary_flag:bool, from_date:date, bline_list:[Bline_list]):
    double_currency = False
    foreign_curr = ""
    fo_cashjour_list_list = []

    bline_list = output_list = fo_cashjour_list = None

    bline_list_list, Bline_list = create_model("Bline_list", {"flag":int, "userinit":str, "selected":bool, "name":str, "bl_recid":int})
    output_list_list, Output_list = create_model("Output_list", {"flag":str, "amt_foreign":decimal, "str_foreign":str, "str":str, "gname":str})
    fo_cashjour_list_list, Fo_cashjour_list = create_model("Fo_cashjour_list", {"datum":date, "zinr":str, "rechnr":int, "artnr":int, "bezeich":str, "dept":str, "l_amount":decimal, "f_amount":decimal, "gname":str, "zeit":str, "id":str})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal double_currency, foreign_curr, fo_cashjour_list_list


        nonlocal bline_list, output_list, fo_cashjour_list
        nonlocal bline_list_list, output_list_list, fo_cashjour_list_list
        return {"double_currency": double_currency, "foreign_curr": foreign_curr, "fo-cashjour-list": fo_cashjour_list_list}


    from_date, double_currency, foreign_curr, bline_list_list, output_list_list = get_output(fo_cashgjournbl(pvilanguage, case_type, curr_shift, summary_flag, from_date, bline_list))
    fo_cashjour_list_list.clear()

    for output_list in query(output_list_list):
        fo_cashjour_list = Fo_cashjour_list()
        fo_cashjour_list_list.append(fo_cashjour_list)

        fo_cashjour_list.datum = date_mdy(substring(output_list.STR, 0, 8))
        fo_cashjour_list.zinr = substring(output_list.STR, 8, 6)
        fo_cashjour_list.rechnr = to_int(substring(output_list.STR, 14, 9))
        fo_cashjour_list.artnr = to_int(substring(output_list.STR, 23, 4))
        fo_cashjour_list.bezeich = substring(output_list.STR, 27, 40)
        fo_cashjour_list.dept = substring(output_list.STR, 67, 17)
        fo_cashjour_list.l_amount = decimal.Decimal(substring(output_list.STR, 84, 17))
        fo_cashjour_list.f_amount = decimal.Decimal(output_list.str_foreign)
        fo_cashjour_list.gname = output_list.gname
        fo_cashjour_list.zeit = substring(output_list.STR, 101, 8)
        fo_cashjour_list.ID = substring(output_list.STR, 109, 3)

    return generate_output()