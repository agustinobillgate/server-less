#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Bediener, Guest, Htparam, Guestbud

def prepare_guestbud1bl(gastnr:int, user_init:string):

    prepare_cache ([Bediener, Htparam, Guestbud])

    price_decimal = 0
    bill_date = None
    from_date = None
    q1_list_list = []
    bediener = guest = htparam = guestbud = None

    usr = q1_list = None

    q1_list_list, Q1_list = create_model("Q1_list", {"monat":int, "jahr":int, "argtumsatz":Decimal, "f_b_umsatz":Decimal, "sonst_umsatz":Decimal, "room_nights":int, "userinit":string, "rec_id":int})

    Usr = create_buffer("Usr",Bediener)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal price_decimal, bill_date, from_date, q1_list_list, bediener, guest, htparam, guestbud
        nonlocal gastnr, user_init
        nonlocal usr


        nonlocal usr, q1_list
        nonlocal q1_list_list

        return {"price_decimal": price_decimal, "bill_date": bill_date, "from_date": from_date, "q1-list": q1_list_list}

    guest = get_cache (Guest, {"gastnr": [(eq, gastnr)]})

    bediener = get_cache (Bediener, {"userinit": [(eq, user_init)]})

    htparam = get_cache (Htparam, {"paramnr": [(eq, 491)]})
    price_decimal = htparam.finteger

    htparam = get_cache (Htparam, {"paramnr": [(eq, 110)]})
    bill_date = htparam.fdate
    from_date = date_mdy(get_month(bill_date) , 1, get_year(bill_date))

    guestbud_obj_list = {}
    guestbud = Guestbud()
    usr = Bediener()
    for guestbud.monat, guestbud.jahr, guestbud.argtumsatz, guestbud.f_b_umsatz, guestbud.sonst_umsatz, guestbud.room_nights, guestbud._recid, usr.userinit, usr._recid in db_session.query(Guestbud.monat, Guestbud.jahr, Guestbud.argtumsatz, Guestbud.f_b_umsatz, Guestbud.sonst_umsatz, Guestbud.room_nights, Guestbud._recid, Usr.userinit, Usr._recid).join(Usr,(Usr.nr == Guestbud.bediener_nr)).filter(
             (Guestbud.gastnr == gastnr)).order_by(Guestbud.jahr, Guestbud.monat).all():
        if guestbud_obj_list.get(guestbud._recid):
            continue
        else:
            guestbud_obj_list[guestbud._recid] = True


        q1_list = Q1_list()
        q1_list_list.append(q1_list)

        q1_list.monat = guestbud.monat
        q1_list.jahr = guestbud.jahr
        q1_list.argtumsatz =  to_decimal(guestbud.argtumsatz)
        q1_list.f_b_umsatz =  to_decimal(guestbud.f_b_umsatz)
        q1_list.sonst_umsatz =  to_decimal(guestbud.sonst_umsatz)
        q1_list.room_nights = guestbud.room_nights
        q1_list.userinit = usr.userinit
        q1_list.rec_id = guestbud._recid

    return generate_output()