from functions.additional_functions import *
import decimal
from sqlalchemy import func
from models import Guest, Bediener, Akt_cust

def akt_custlist_btn_gobl(lname:str, usr_init:str):
    err = 0
    q1_list_list = []
    guest = bediener = akt_cust = None

    q1_list = ubuff = None

    q1_list_list, Q1_list = create_model_like(Guest, {"rec_id":int, "aktcust_rec_id":int, "userinit":str, "datum":date, "c_init":str, "a_gastnr":int})

    Ubuff = create_buffer("Ubuff",Bediener)

    db_session = local_storage.db_session

    def generate_output():
        nonlocal err, q1_list_list, guest, bediener, akt_cust
        nonlocal lname, usr_init
        nonlocal ubuff


        nonlocal q1_list, ubuff
        nonlocal q1_list_list
        return {"err": err, "q1-list": q1_list_list}

    ubuff = db_session.query(Ubuff).filter(
             (func.lower(Ubuff.userinit) == (usr_init).lower())).first()

    if not ubuff:
        err = 1

        return generate_output()

    if usr_init >= "":

        akt_cust_obj_list = []
        for akt_cust, guest in db_session.query(Akt_cust, Guest).join(Guest,(Guest.gastnr == Akt_cust.gastnr) & (Guest.phonetik3 == Akt_cust.userinit) & (func.lower(Guest.name) >= (lname).lower()) & (Guest.gastnr != 0)).filter(
                 (func.lower(Akt_cust.userinit) == (usr_init).lower())).order_by(Guest.name).all():
            if akt_cust._recid in akt_cust_obj_list:
                continue
            else:
                akt_cust_obj_list.append(akt_cust._recid)

            q1_list = query(q1_list_list, filters=(lambda q1_list: q1_list.gastnr == guest.gastnr), first=True)

            if not q1_list:
                q1_list = Q1_list()
                q1_list_list.append(q1_list)

                buffer_copy(guest, q1_list)
                q1_list.rec_id = guest._recid
                q1_list.aktcust_rec_id = akt_cust._recid
                q1_list.userinit = akt_cust.userinit
                q1_list.datum = akt_cust.datum
                q1_list.c_init = akt_cust.c_init
                q1_list.a_gastnr = akt_cust.gastnr

    return generate_output()