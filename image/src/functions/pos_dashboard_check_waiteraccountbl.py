from functions.additional_functions import *
import decimal
from sqlalchemy import func
from models import Hoteldpt, Kellner

def pos_dashboard_check_waiteraccountbl(user_init:str, pos_dept:int, bediener_username:str):
    active_waiter = False
    hoteldpt = kellner = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal active_waiter, hoteldpt, kellner


        return {"active_waiter": active_waiter}


    hoteldpt = db_session.query(Hoteldpt).filter(
            (Hoteldpt.num == pos_dept)).first()

    if hoteldpt:

        kellner = db_session.query(Kellner).filter(
                (to_string(Kellner_nr, "99") == (user_init).lower()) &  (Kellner.departement == hoteldpt.num)).first()

        if not kellner:

            kellner = db_session.query(Kellner).filter(
                    (func.lower(Kellnername) == (bediener_username).lower()) &  (Kellner.departement == hoteldpt.num)).first()

        if kellner:
            active_waiter = True

            return generate_output()