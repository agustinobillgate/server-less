from functions.additional_functions import *
import decimal
from sqlalchemy import func
from models import Bediener, Guest, Guestbud

def guestbud1_new_budgetbl(gastnr:int, mm:int, yy:int, room:int, lodging:decimal, fb:decimal, sonst:decimal, user_init:str):
    q1_list_list = []
    bediener = guest = guestbud = None

    usr = q1_list = None

    q1_list_list, Q1_list = create_model("Q1_list", {"monat":int, "jahr":int, "argtumsatz":decimal, "f_b_umsatz":decimal, "sonst_umsatz":decimal, "room_nights":int, "userinit":str, "rec_id":int})

    Usr = Bediener

    db_session = local_storage.db_session

    def generate_output():
        nonlocal q1_list_list, bediener, guest, guestbud
        nonlocal usr


        nonlocal usr, q1_list
        nonlocal q1_list_list
        return {"q1-list": q1_list_list}

    bediener = db_session.query(Bediener).filter(
            (func.lower(Bediener.userinit) == (user_init).lower())).first()

    guest = db_session.query(Guest).filter(
            (Guest.gastnr == gastnr)).first()

    guestbud = db_session.query(Guestbud).filter(
            (Guestbud.monat == mm) &  (Guestbud.jahr == yy) &  (Guestbud.gastnr == guest.gastnr)).first()

    if not guestbud:
        guestbud = Guestbud()
        db_session.add(guestbud)

        guestbud.monat = mm
        guestbud.jahr = yy
        guestbud.gastnr = guest.gastnr
    guestbud.room_nights = room
    guestbud.argtumsatz = lodging
    guestbud.f_b_umsatz = fb
    guestbud.sonst_umsatz = sonst
    guestbud.gesamtumsatz = lodging + fb + sonst
    guestbud.bediener_nr = bediener.nr

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