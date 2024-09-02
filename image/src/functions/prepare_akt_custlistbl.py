from functions.additional_functions import *
import decimal
from sqlalchemy import func
from models import Guest, Htparam, Bediener, Akt_cust

def prepare_akt_custlistbl(user_init:str, lname:str):
    ext_char = ""
    usr_name = ""
    usr_init = ""
    old_init = ""
    tot_gcf = 0
    q1_list_list = []
    guest = htparam = bediener = akt_cust = None

    q1_list = None

    q1_list_list, Q1_list = create_model_like(Guest, {"rec_id":int, "aktcust_rec_id":int, "userinit":str, "datum":date, "c_init":str, "a_gastnr":int})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal ext_char, usr_name, usr_init, old_init, tot_gcf, q1_list_list, guest, htparam, bediener, akt_cust


        nonlocal q1_list
        nonlocal q1_list_list
        return {"ext_char": ext_char, "usr_name": usr_name, "usr_init": usr_init, "old_init": old_init, "tot_gcf": tot_gcf, "q1-list": q1_list_list}

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 148)).first()
    ext_char = htparam.fchar

    bediener = db_session.query(Bediener).filter(
            (func.lower(Bediener.userinit) == (user_init).lower())).first()
    usr_name = bediener.username
    usr_init = user_init
    old_init = usr_init
    tot_gcf = 0

    if usr_init != "":

        akt_cust_obj_list = []
        for akt_cust, guest in db_session.query(Akt_cust, Guest).join(Guest,(Guest.gastnr == Akt_cust.gastnr) &  (Guest.phonetik3 == Akt_cust.userinit) &  (func.lower(Guest.name) >= (lname).lower()) &  (Guest.gastnr > 0)).filter(
                (Akt_cust.userinit == usr_init)).all():
            if akt_cust._recid in akt_cust_obj_list:
                continue
            else:
                akt_cust_obj_list.append(akt_cust._recid)


            q1_list = Q1_list()
            q1_list_list.append(q1_list)

            buffer_copy(guest, q1_list)
            q1_list.rec_id = guest._recid
            q1_list.aktcust_rec_id = akt_cust._recid
            q1_list.userinit = akt_cust.userinit
            q1_list.datum = akt_cust.datum
            q1_list.c_init = akt_cust.c_init
            q1_list.a_gastnr = akt_cust.gastnr


            tot_gcf = tot_gcf + 1


    return generate_output()