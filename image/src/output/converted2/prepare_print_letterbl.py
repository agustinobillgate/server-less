#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from functions.print_letter_disp_arlistbl import print_letter_disp_arlistbl
from models import Htparam

def prepare_print_letterbl(last_sort:int, fdate:date, lname:string):

    prepare_cache ([Htparam])

    ci_date = None
    briefnr = 0
    q1_list_list = []
    htparam = None

    q1_list = None

    q1_list_list, Q1_list = create_model("Q1_list", {"resnr":int, "grpflag":bool, "gastnr":int, "name":string, "vorname1":string, "anrede1":string, "anredefirma":string, "briefnr":int, "ankunft":date, "anztage":int, "abreise":date, "kurzbez":string, "resstatus":int, "groupname":string, "activeflag":int, "roomrate":Decimal, "room_night":int, "bedsetup":string})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal ci_date, briefnr, q1_list_list, htparam
        nonlocal last_sort, fdate, lname


        nonlocal q1_list
        nonlocal q1_list_list

        return {"ci_date": ci_date, "briefnr": briefnr, "q1-list": q1_list_list}

    htparam = get_cache (Htparam, {"paramnr": [(eq, 87)]})
    ci_date = htparam.fdate

    htparam = get_cache (Htparam, {"paramnr": [(eq, 435)]})
    briefnr = htparam.finteger
    q1_list_list = get_output(print_letter_disp_arlistbl(last_sort, fdate, lname))

    return generate_output()