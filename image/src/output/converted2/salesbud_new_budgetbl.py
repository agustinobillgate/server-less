#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import Salesbud

def salesbud_new_budgetbl(mm:int, yy:int, room:int, lodging:Decimal, fb:Decimal, sonst:Decimal, bediener_nr:int, user_init:string):
    t_salesbud_list = []
    salesbud = None

    t_salesbud = None

    t_salesbud_list, T_salesbud = create_model_like(Salesbud, {"rec_id":int})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal t_salesbud_list, salesbud
        nonlocal mm, yy, room, lodging, fb, sonst, bediener_nr, user_init


        nonlocal t_salesbud
        nonlocal t_salesbud_list

        return {"t-salesbud": t_salesbud_list}

    salesbud = get_cache (Salesbud, {"monat": [(eq, mm)],"jahr": [(eq, yy)],"bediener_nr": [(eq, bediener_nr)]})

    if not salesbud:
        salesbud = Salesbud()
        db_session.add(salesbud)

        salesbud.monat = mm
        salesbud.jahr = yy
        salesbud.bediener_nr = bediener_nr
    salesbud.room_nights = room
    salesbud.argtumsatz =  to_decimal(lodging)
    salesbud.f_b_umsatz =  to_decimal(fb)
    salesbud.sonst_umsatz =  to_decimal(sonst)
    salesbud.gesamtumsatz =  to_decimal(lodging) + to_decimal(fb) + to_decimal(sonst)
    salesbud.id = user_init

    for salesbud in db_session.query(Salesbud).order_by(Salesbud._recid).all():
        t_salesbud = T_salesbud()
        t_salesbud_list.append(t_salesbud)

        buffer_copy(salesbud, t_salesbud)
        t_salesbud.rec_id = salesbud._recid

    return generate_output()