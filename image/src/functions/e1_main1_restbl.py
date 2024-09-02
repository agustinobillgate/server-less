from functions.additional_functions import *
import decimal
from sqlalchemy import func
from models import Hoteldpt, Kellner

def e1_main1_restbl(user_init:str, pos_dept:int, bediener_username:str):
    do_it = False
    hoteldpt = kellner = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal do_it, hoteldpt, kellner


        return {"do_it": do_it}


    hoteldpt = db_session.query(Hoteldpt).filter(
            (Hoteldpt.num == pos_dept)).first()

    if hoteldpt:

        kellner = db_session.query(Kellner).filter(
                (to_string(Kellner_nr, "99") == (user_init).lower()) &  (Kellner.departement == pos_dept)).first()

        if not kellner:

            kellner = db_session.query(Kellner).filter(
                    (func.lower(Kellnername) == (bediener_username).lower()) &  (Kellner.departement == pos_dept)).first()

        if kellner:
            do_it = True

    return generate_output()