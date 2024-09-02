from functions.additional_functions import *
import decimal
from datetime import date
from functions.print_letter_disp_arlistbl import print_letter_disp_arlistbl
from models import Htparam

def prepare_print_letterbl(last_sort:int, fdate:date, lname:str):
    ci_date = None
    briefnr = 0
    q1_list_list = []
    htparam = None

    q1_list = None

    q1_list_list, Q1_list = create_model("Q1_list", {"resnr":int, "grpflag":bool, "gastnr":int, "name":str, "vorname1":str, "anrede1":str, "anredefirma":str, "briefnr":int, "ankunft":date, "anztage":int, "abreise":date, "kurzbez":str, "resstatus":int, "groupname":str, "activeflag":int, "roomrate":decimal, "room_night":int, "bedsetup":str})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal ci_date, briefnr, q1_list_list, htparam


        nonlocal q1_list
        nonlocal q1_list_list
        return {"ci_date": ci_date, "briefnr": briefnr, "q1-list": q1_list_list}

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 87)).first()
    ci_date = htparam.fdate

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 435)).first()
    briefnr = htparam.finteger
    q1_list_list = get_output(print_letter_disp_arlistbl(last_sort, fdate, lname))

    return generate_output()