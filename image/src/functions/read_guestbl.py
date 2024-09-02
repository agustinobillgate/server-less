from functions.additional_functions import *
import decimal
from sqlalchemy import func
from models import Guest, Bill

def read_guestbl(case_type:int, gastno:int, gname:str, fname:str):
    t_guest_list = []
    guest = bill = None

    t_guest = None

    t_guest_list, T_guest = create_model_like(Guest)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal t_guest_list, guest, bill


        nonlocal t_guest
        nonlocal t_guest_list
        return {"t-guest": t_guest_list}

    def delete_procedure():

        nonlocal t_guest_list, guest, bill


        nonlocal t_guest
        nonlocal t_guest_list

    hHandle = THIS_PROCEDURE

    if case_type == 1:

        if gastno > 0:

            guest = db_session.query(Guest).filter(
                    (Guest.gastnr == gastno)).first()

        elif gname != "":

            guest = db_session.query(Guest).filter(
                    (func.lower(Guest.name) == (gname).lower()) &  (Guest.gastnr > 0)).first()
    elif case_type == 2:

        guest = db_session.query(Guest).filter(
                (func.lower(Guest.name) == (gname).lower()) &  ((Guest.vorname1 + Guest.anredefirma) == (fname).lower()) &  (Guest.gastnr > 0)).first()
    elif case_type == 3:

        if gastno > 0:

            guest = db_session.query(Guest).filter(
                    (Guest.gastnr == gastno)).first()

        elif gname != "":

            guest = db_session.query(Guest).filter(
                    (func.lower(Guest.name) == (gname).lower()) &  (Guest.gastnr > 0)).first()
    elif case_type == 4:

        guest = db_session.query(Guest).filter(
                (func.lower(Guest.name) == (gname).lower()) &  (func.lower(Guest.vorname1) == (fname).lower()) &  (Guest.gastnr != gastno)).first()
    elif case_type == 5:

        if fname != "":

            guest = db_session.query(Guest).filter(
                    (func.lower(Guest.name) == (gname).lower()) &  ((Guest.vorname1 + Guest.anredefirma) == (fname).lower()) &  (Guest.gastnr > 0)).first()
        else:

            guest = db_session.query(Guest).filter(
                    (func.lower(Guest.name) == (gname).lower()) &  (Guest.gastnr > 0)).first()
    elif case_type == 6:

        guest = db_session.query(Guest).filter(
                (func.lower(Guest.name) == (gname).lower()) &  ((Guest.vorname1 + Guest.anredefirma) == (fname).lower()) &  (Guest.karteityp == gastno) &  (Guest.gastnr > 0)).first()
    elif case_type == 7:

        guest = db_session.query(Guest).filter(
                (Guest.karteityp >= 1) &  (Guest.gastnr > gastno) &  (Guest.firmen_nr > 0)).first()
    elif case_type == 8:

        guest = db_session.query(Guest).filter(
                (Guest.karteityp >= 1) &  (Guest.gastnr > gastno) &  (Guest.steuernr != "")).first()
    elif case_type == 9:

        guest = db_session.query(Guest).filter(
                (func.lower(Guest.name) == (gname).lower()) |  ((func.lower(Guest.name) + ", " + Guest.anredefirma) == (gname).lower())).first()
    elif case_type == 10:

        guest = db_session.query(Guest).first()
    elif case_type == 11:

        guest = db_session.query(Guest).filter(
                (func.lower(Guest.ausweis_nr1) == (gname).lower()) &  (Guest.karteityp == 0) &  (Guest.gastnr > 0)).first()
    elif case_type == 12:

        guest = db_session.query(Guest).filter(
                (Guest.master_gastnr == gastno) &  (Guest.karteityp == 0) &  (Guest.gastnr > 0)).first()
    elif case_type == 13:

        guest = db_session.query(Guest).filter(
                (Guest.karteityp == 0)).first()
    elif case_type == 14:

        guest = db_session.query(Guest).filter(
                (func.lower(Guest.nation1) == (gname).lower())).first()
    elif case_type == 15:

        guest = db_session.query(Guest).filter(
                (Guest.gastnr == gastno) &  (Guest.karteityp > 0)).first()
    elif case_type == 16:

        bill = db_session.query(Bill).filter(
                (Bill.rechnr == gastno)).first()

        if not bill:

            return generate_output()

        guest = db_session.query(Guest).filter(
                (Guest.gastnr == bill.gastnr)).first()
    elif case_type == 17:

        guest = db_session.query(Guest).filter(
                (Guest.karteityp == 1) &  (func.lower(Guest.name) == (gname).lower()) &  (Guest.gastnr != gastno) &  (Guest.gastnr > 0)).first()
    elif case_type == 18:

        guest = db_session.query(Guest).filter(
                (Guest.karteityp == 2) &  (func.lower(Guest.name) == (gname).lower()) &  (Guest.gastnr != gastno) &  (Guest.gastnr > 0)).first()

    if guest:
        t_guest = T_guest()
        t_guest_list.append(t_guest)

        buffer_copy(guest, t_guest)

    return generate_output()