#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from functions.gcf_listbl import gcf_listbl

def get_gcflistbl(case_type:int, sorttype:int, lname:string, fname:string):
    first_gastnr = None
    current_lname = ""
    current_fname = ""
    t_guest_list = []

    t_guest = None

    t_guest_list, T_guest = create_model("T_guest", {"akt_gastnr":int, "karteityp":int, "master_gastnr":int, "pr_flag":int, "mc_flag":bool, "gname":string, "adresse":string, "steuernr":string, "firma":string, "namekontakt":string, "phonetik3":string, "rabatt":Decimal, "endperiode":date, "firmen_nr":int, "land":string, "wohnort":string, "telefon":string, "plz":string, "geschlecht":string, "ausweis_nr1":string, "gastnr":int, "zahlungsart":int, "kreditlimit":Decimal, "bezeich":string, "alertbox":bool, "warningbox":bool}, {"bezeich": ""})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal first_gastnr, current_lname, current_fname, t_guest_list
        nonlocal case_type, sorttype, lname, fname


        nonlocal t_guest
        nonlocal t_guest_list

        return {"first_gastnr": first_gastnr, "current_lname": current_lname, "current_fname": current_fname, "t-guest": t_guest_list}

    if case_type == 1:
        t_guest_list.clear()
        first_gastnr, current_lname, current_fname, t_guest_list = get_output(gcf_listbl(1, sorttype, "", "", None))
    else:
        first_gastnr, current_lname, current_fname, t_guest_list = get_output(gcf_listbl(2, sorttype, lname, "", 0))

    return generate_output()