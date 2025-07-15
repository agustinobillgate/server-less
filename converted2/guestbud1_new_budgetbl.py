#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import Bediener, Guest, Guestbud

def guestbud1_new_budgetbl(gastnr:int, mm:int, yy:int, room:int, lodging:Decimal, fb:Decimal, sonst:Decimal, user_init:string):

    prepare_cache ([Bediener, Guest, Guestbud])

    q1_list_data = []
    bediener = guest = guestbud = None

    usr = q1_list = None

    q1_list_data, Q1_list = create_model("Q1_list", {"monat":int, "jahr":int, "argtumsatz":Decimal, "f_b_umsatz":Decimal, "sonst_umsatz":Decimal, "room_nights":int, "userinit":string, "rec_id":int})

    Usr = create_buffer("Usr",Bediener)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal q1_list_data, bediener, guest, guestbud
        nonlocal gastnr, mm, yy, room, lodging, fb, sonst, user_init
        nonlocal usr


        nonlocal usr, q1_list
        nonlocal q1_list_data

        return {"q1-list": q1_list_data}

    bediener = get_cache (Bediener, {"userinit": [(eq, user_init)]})

    guest = get_cache (Guest, {"gastnr": [(eq, gastnr)]})

    guestbud = get_cache (Guestbud, {"monat": [(eq, mm)],"jahr": [(eq, yy)],"gastnr": [(eq, guest.gastnr)]})

    if not guestbud:
        guestbud = Guestbud()
        db_session.add(guestbud)

        guestbud.monat = mm
        guestbud.jahr = yy
        guestbud.gastnr = guest.gastnr
    guestbud.room_nights = room
    guestbud.argtumsatz =  to_decimal(lodging)
    guestbud.f_b_umsatz =  to_decimal(fb)
    guestbud.sonst_umsatz =  to_decimal(sonst)
    guestbud.gesamtumsatz =  to_decimal(lodging) + to_decimal(fb) + to_decimal(sonst)
    guestbud.bediener_nr = bediener.nr

    guestbud_obj_list = {}
    guestbud = Guestbud()
    usr = Bediener()
    for guestbud.monat, guestbud.jahr, guestbud.argtumsatz, guestbud.f_b_umsatz, guestbud.sonst_umsatz, guestbud.room_nights, guestbud._recid, guestbud.gastnr, guestbud.gesamtumsatz, guestbud.bediener_nr, usr.nr, usr._recid, usr.userinit in db_session.query(Guestbud.monat, Guestbud.jahr, Guestbud.argtumsatz, Guestbud.f_b_umsatz, Guestbud.sonst_umsatz, Guestbud.room_nights, Guestbud._recid, Guestbud.gastnr, Guestbud.gesamtumsatz, Guestbud.bediener_nr, Usr.nr, Usr._recid, Usr.userinit).join(Usr,(Usr.nr == Guestbud.bediener_nr)).filter(
             (Guestbud.gastnr == gastnr)).order_by(Guestbud.jahr, Guestbud.monat).all():
        if guestbud_obj_list.get(guestbud._recid):
            continue
        else:
            guestbud_obj_list[guestbud._recid] = True


        q1_list = Q1_list()
        q1_list_data.append(q1_list)

        q1_list.monat = guestbud.monat
        q1_list.jahr = guestbud.jahr
        q1_list.argtumsatz =  to_decimal(guestbud.argtumsatz)
        q1_list.f_b_umsatz =  to_decimal(guestbud.f_b_umsatz)
        q1_list.sonst_umsatz =  to_decimal(guestbud.sonst_umsatz)
        q1_list.room_nights = guestbud.room_nights
        q1_list.userinit = usr.userinit
        q1_list.rec_id = guestbud._recid

    return generate_output()