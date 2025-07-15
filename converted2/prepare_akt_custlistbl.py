#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import Guest, Htparam, Bediener, Akt_cust

def prepare_akt_custlistbl(user_init:string, lname:string):

    prepare_cache ([Htparam, Bediener, Akt_cust])

    ext_char = ""
    usr_name = ""
    usr_init = ""
    old_init = ""
    tot_gcf = 0
    q1_list_data = []
    guest = htparam = bediener = akt_cust = None

    q1_list = None

    q1_list_data, Q1_list = create_model_like(Guest, {"rec_id":int, "aktcust_rec_id":int, "userinit":string, "datum":date, "c_init":string, "a_gastnr":int})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal ext_char, usr_name, usr_init, old_init, tot_gcf, q1_list_data, guest, htparam, bediener, akt_cust
        nonlocal user_init, lname


        nonlocal q1_list
        nonlocal q1_list_data

        return {"ext_char": ext_char, "usr_name": usr_name, "usr_init": usr_init, "old_init": old_init, "tot_gcf": tot_gcf, "q1-list": q1_list_data}

    htparam = get_cache (Htparam, {"paramnr": [(eq, 148)]})
    ext_char = htparam.fchar

    bediener = get_cache (Bediener, {"userinit": [(eq, user_init)]})
    usr_name = bediener.username
    usr_init = user_init
    old_init = usr_init
    tot_gcf = 0

    if usr_init != "":

        akt_cust_obj_list = {}
        for akt_cust, guest in db_session.query(Akt_cust, Guest).join(Guest,(Guest.gastnr == Akt_cust.gastnr) & (Guest.phonetik3 == Akt_cust.userinit) & (Guest.name >= (lname).lower()) & (Guest.gastnr > 0)).filter(
                 (Akt_cust.userinit == (usr_init).lower())).order_by(Guest.name).all():
            if akt_cust_obj_list.get(akt_cust._recid):
                continue
            else:
                akt_cust_obj_list[akt_cust._recid] = True


            q1_list = Q1_list()
            q1_list_data.append(q1_list)

            buffer_copy(guest, q1_list)
            q1_list.rec_id = guest._recid
            q1_list.aktcust_rec_id = akt_cust._recid
            q1_list.userinit = akt_cust.userinit
            q1_list.datum = akt_cust.datum
            q1_list.c_init = akt_cust.c_init
            q1_list.a_gastnr = akt_cust.gastnr


            tot_gcf = tot_gcf + 1


    return generate_output()