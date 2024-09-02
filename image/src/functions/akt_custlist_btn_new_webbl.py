from functions.additional_functions import *
import decimal
from sqlalchemy import func
from models import Guest, Akt_cust, Bediener

def akt_custlist_btn_new_webbl(pvilanguage:int, gastnr:int, lname:str, usr_init:str, user_init:str):
    msg_str = ""
    q1_list_list = []
    lvcarea:str = "comp_stataccor"
    guest = akt_cust = bediener = None

    q1_list = akt_cust1 = usr = guest1 = None

    q1_list_list, Q1_list = create_model_like(Guest, {"rec_id":int, "aktcust_rec_id":int, "userinit":str, "datum":date, "c_init":str, "a_gastnr":int})

    Akt_cust1 = Akt_cust
    Usr = Bediener
    Guest1 = Guest

    db_session = local_storage.db_session

    def generate_output():
        nonlocal msg_str, q1_list_list, lvcarea, guest, akt_cust, bediener
        nonlocal akt_cust1, usr, guest1


        nonlocal q1_list, akt_cust1, usr, guest1
        nonlocal q1_list_list
        return {"msg_str": msg_str, "q1-list": q1_list_list}

    def create_list():

        nonlocal msg_str, q1_list_list, lvcarea, guest, akt_cust, bediener
        nonlocal akt_cust1, usr, guest1


        nonlocal q1_list, akt_cust1, usr, guest1
        nonlocal q1_list_list

        answer:bool = False
        Akt_cust1 = Akt_cust
        Usr = Bediener
        Guest1 = Guest
        answer = True

        akt_cust1 = db_session.query(Akt_cust1).filter(
                (Akt_cust1.gastnr == gastnr)).first()

        if akt_cust1:

            guest1 = db_session.query(Guest1).filter(
                    (Guest1.gastnr == gastnr)).first()

            usr = db_session.query(Usr).filter(
                    (Usr.userinit == akt_cust1.userinit)).first()
            msg_str = guest1.name.upper() + translateExtended (" - has been selected by", lvcarea, "") + chr(10) + usr.userinit + " - " + usr.username + chr(10) + translateExtended ("Double_entry not allowed.", lvcarea, "")
        else:

            guest1 = db_session.query(Guest1).filter(
                    (Guest1.gastnr == gastnr)).first()
            guest1.phonetik3 = usr_init
            akt_cust = Akt_cust()
            db_session.add(akt_cust)

            akt_cust.gastnr = gastnr
            akt_cust.c_init = user_init
            akt_cust.userinit = usr_init

            akt_cust = db_session.query(Akt_cust).first()

            guest1 = db_session.query(Guest1).first()

            akt_cust_obj_list = []
            for akt_cust, guest in db_session.query(Akt_cust, Guest).join(Guest,(Guest.gastnr == Akt_cust.gastnr) &  (Guest.phonetik3 == Akt_cust.userinit) &  (func.lower(Guest.name) >= (lname).lower()) &  (Guest.gastnr > 0)).filter(
                    (func.lower(Akt_cust.userinit) == (usr_init).lower())).all():
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


    create_list()

    return generate_output()