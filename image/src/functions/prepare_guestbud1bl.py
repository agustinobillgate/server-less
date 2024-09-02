from functions.additional_functions import *
import decimal
from datetime import date
from sqlalchemy import func
from models import Bediener, Guest, Htparam, Guestbud

def prepare_guestbud1bl(gastnr:int, user_init:str):
    price_decimal = 0
    bill_date = None
    from_date = None
    q1_list_list = []
    bediener = guest = htparam = guestbud = None

    usr = q1_list = None

    q1_list_list, Q1_list = create_model("Q1_list", {"monat":int, "jahr":int, "argtumsatz":decimal, "f_b_umsatz":decimal, "sonst_umsatz":decimal, "room_nights":int, "userinit":str, "rec_id":int})

    Usr = Bediener

    db_session = local_storage.db_session

    def generate_output():
        nonlocal price_decimal, bill_date, from_date, q1_list_list, bediener, guest, htparam, guestbud
        nonlocal usr


        nonlocal usr, q1_list
        nonlocal q1_list_list
        return {"price_decimal": price_decimal, "bill_date": bill_date, "from_date": from_date, "q1-list": q1_list_list}

    guest = db_session.query(Guest).filter(
            (Guest.gastnr == gastnr)).first()

    bediener = db_session.query(Bediener).filter(
            (func.lower(Bediener.userinit) == (user_init).lower())).first()

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 491)).first()
    price_decimal = htparam.finteger

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 110)).first()
    bill_date = htparam.fdate
    from_date = date_mdy(get_month(bill_date) , 1, get_year(bill_date))

    guestbud_obj_list = []
    for guestbud, usr in db_session.query(Guestbud, Usr).join(Usr,(Usr.nr == Guestbud.bediener_nr)).filter(
            (Guestbud.gastnr == gastnr)).all():
        if guestbud._recid in guestbud_obj_list:
            continue
        else:
            guestbud_obj_list.append(guestbud._recid)


        q1_list = Q1_list()
        q1_list_list.append(q1_list)

        q1_list.monat = guestbud.monat
        q1_list.jahr = guestbud.jahr
        q1_list.argtumsatz = guestbud.argtumsatz
        q1_list.f_b_umsatz = guestbud.f_b_umsatz
        q1_list.sonst_umsatz = guestbud.sonst_umsatz
        q1_list.room_nights = guestbud.room_nights
        q1_list.userinit = usr.userinit
        q1_list.rec_id = guestbud._recid

    return generate_output()