#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import Guest, Akt_cust, Bediener

def akt_custlist_btn_new_webbl(pvilanguage:int, gastnr:int, lname:string, usr_init:string, user_init:string):

    prepare_cache ([Guest, Akt_cust, Bediener])

    msg_str = ""
    q1_list_list = []
    lvcarea:string = "comp-stataccor"
    guest = akt_cust = bediener = None

    q1_list = None

    q1_list_list, Q1_list = create_model_like(Guest, {"rec_id":int, "aktcust_rec_id":int, "userinit":string, "datum":date, "c_init":string, "a_gastnr":int})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal msg_str, q1_list_list, lvcarea, guest, akt_cust, bediener
        nonlocal pvilanguage, gastnr, lname, usr_init, user_init


        nonlocal q1_list
        nonlocal q1_list_list

        return {"msg_str": msg_str, "q1-list": q1_list_list}

    def create_list():

        nonlocal msg_str, q1_list_list, lvcarea, guest, akt_cust, bediener
        nonlocal pvilanguage, gastnr, lname, usr_init, user_init


        nonlocal q1_list
        nonlocal q1_list_list

        akt_cust1 = None
        usr = None
        guest1 = None
        answer:bool = False
        Akt_cust1 =  create_buffer("Akt_cust1",Akt_cust)
        Usr =  create_buffer("Usr",Bediener)
        Guest1 =  create_buffer("Guest1",Guest)
        answer = True

        akt_cust1 = get_cache (Akt_cust, {"gastnr": [(eq, gastnr)]})

        if akt_cust1:

            guest1 = get_cache (Guest, {"gastnr": [(eq, gastnr)]})

            usr = get_cache (Bediener, {"userinit": [(eq, akt_cust1.userinit)]})
            msg_str = guest1.name.upper() + translateExtended (" - has been selected by", lvcarea, "") + chr_unicode(10) + usr.userinit + " - " + usr.username + chr_unicode(10) + translateExtended ("Double-entry not allowed.", lvcarea, "")
        else:

            guest1 = get_cache (Guest, {"gastnr": [(eq, gastnr)]})
            guest1.phonetik3 = usr_init
            akt_cust = Akt_cust()
            db_session.add(akt_cust)

            akt_cust.gastnr = gastnr
            akt_cust.c_init = user_init
            akt_cust.userinit = usr_init


            pass
            pass

            akt_cust_obj_list = {}
            akt_cust = Akt_cust()
            guest = Guest()
            for akt_cust._recid, akt_cust.userinit, akt_cust.datum, akt_cust.c_init, akt_cust.gastnr, guest.name, guest.phonetik3, guest._recid in db_session.query(Akt_cust._recid, Akt_cust.userinit, Akt_cust.datum, Akt_cust.c_init, Akt_cust.gastnr, Guest.name, Guest.phonetik3, Guest._recid).join(Guest,(Guest.gastnr == Akt_cust.gastnr) & (Guest.phonetik3 == Akt_cust.userinit) & (Guest.name >= (lname).lower()) & (Guest.gastnr > 0)).filter(
                     (Akt_cust.userinit == (usr_init).lower())).order_by(Guest.name).all():
                if akt_cust_obj_list.get(akt_cust._recid):
                    continue
                else:
                    akt_cust_obj_list[akt_cust._recid] = True


                q1_list = Q1_list()
                q1_list_list.append(q1_list)

                buffer_copy(guest, q1_list)
                q1_list.rec_id = guest._recid
                q1_list.aktcust_rec_id = akt_cust._recid
                q1_list.userinit = akt_cust.userinit
                q1_list.datum = akt_cust.datum
                q1_list.c_init = akt_cust.c_init
                q1_list.a_gastnr = akt_cust.gastnr

    create_list()

    return generate_output()