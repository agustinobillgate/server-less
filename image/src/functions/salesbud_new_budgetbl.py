from functions.additional_functions import *
import decimal
from models import Salesbud

def salesbud_new_budgetbl(mm:int, yy:int, room:int, lodging:decimal, fb:decimal, sonst:decimal, bediener_nr:int, user_init:str):
    t_salesbud_list = []
    salesbud = None

    t_salesbud = None

    t_salesbud_list, T_salesbud = create_model_like(Salesbud, {"rec_id":int})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal t_salesbud_list, salesbud


        nonlocal t_salesbud
        nonlocal t_salesbud_list
        return {"t-salesbud": t_salesbud_list}

    salesbud = db_session.query(Salesbud).filter(
            (Salesbud.monat == mm) &  (Salesbud.jahr == yy) &  (Salesbud.bediener_nr == bediener_nr)).first()

    if not salesbud:
        salesbud = Salesbud()
        db_session.add(salesbud)

        salesbud.monat = mm
        salesbud.jahr = yy
        salesbud.bediener_nr = bediener_nr
    salesbud.room_nights = room
    salesbud.argtumsatz = lodging
    salesbud.f_b_umsatz = fb
    salesbud.sonst_umsatz = sonst
    salesbud.gesamtumsatz = lodging + fb + sonst
    salesbud.id = user_init

    for salesbud in db_session.query(Salesbud).all():
        t_salesbud = T_salesbud()
        t_salesbud_list.append(t_salesbud)

        buffer_copy(salesbud, t_salesbud)
        t_salesbud.rec_id = salesbud._recid

    return generate_output()