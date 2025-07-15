#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import Guest, Bediener, Akt_cust

def akt_custlist_btn_gobl(lname:string, usr_init:string):

    prepare_cache ([Akt_cust])

    err = 0
    q1_list_data = []
    guest = bediener = akt_cust = None

    q1_list = ubuff = None

    q1_list_data, Q1_list = create_model_like(Guest, {"rec_id":int, "aktcust_rec_id":int, "userinit":string, "datum":date, "c_init":string, "a_gastnr":int})

    Ubuff = create_buffer("Ubuff",Bediener)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal err, q1_list_data, guest, bediener, akt_cust
        nonlocal lname, usr_init
        nonlocal ubuff


        nonlocal q1_list, ubuff
        nonlocal q1_list_data

        return {"err": err, "q1-list": q1_list_data}

    ubuff = db_session.query(Ubuff).filter(
             (Ubuff.userinit == (usr_init).lower())).first()

    if not ubuff:
        err = 1

        return generate_output()

    if usr_init >= "":

        akt_cust_obj_list = {}
        for akt_cust, guest in db_session.query(Akt_cust, Guest).join(Guest,(Guest.gastnr == Akt_cust.gastnr) & (Guest.phonetik3 == Akt_cust.userinit) & (Guest.name >= (lname).lower()) & (Guest.gastnr != 0)).filter(
                 (Akt_cust.userinit == (usr_init).lower())).order_by(Guest.name).all():
            if akt_cust_obj_list.get(akt_cust._recid):
                continue
            else:
                akt_cust_obj_list[akt_cust._recid] = True

            q1_list = query(q1_list_data, filters=(lambda q1_list: q1_list.gastnr == guest.gastnr), first=True)

            if not q1_list:
                q1_list = Q1_list()
                q1_list_data.append(q1_list)

                buffer_copy(guest, q1_list)
                q1_list.rec_id = guest._recid
                q1_list.aktcust_rec_id = akt_cust._recid
                q1_list.userinit = akt_cust.userinit
                q1_list.datum = akt_cust.datum
                q1_list.c_init = akt_cust.c_init
                q1_list.a_gastnr = akt_cust.gastnr

    return generate_output()