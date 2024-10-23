from functions.additional_functions import *
import decimal
from datetime import date
from functions.gcf_listbl import gcf_listbl

def get_gcflistbl(case_type:int, sorttype:int, lname:str, fname:str):
    first_gastnr = None
    current_lname = ""
    current_fname = ""
    t_guest_list = []

    t_guest = None

    t_guest_list, T_guest = create_model("T_guest", {"akt_gastnr":int, "karteityp":int, "master_gastnr":int, "pr_flag":int, "mc_flag":bool, "gname":str, "adresse":str, "steuernr":str, "firma":str, "namekontakt":str, "phonetik3":str, "rabatt":decimal, "endperiode":date, "firmen_nr":int, "land":str, "wohnort":str, "telefon":str, "plz":str, "geschlecht":str, "ausweis_nr1":str, "gastnr":int, "zahlungsart":int, "kreditlimit":decimal, "bezeich":str, "alertbox":bool, "warningbox":bool}, {"bezeich": ""})


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