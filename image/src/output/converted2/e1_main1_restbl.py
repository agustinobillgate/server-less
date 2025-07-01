#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import Hoteldpt, Kellner

def e1_main1_restbl(user_init:string, pos_dept:int, bediener_username:string):
    do_it = False
    hoteldpt = kellner = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal do_it, hoteldpt, kellner
        nonlocal user_init, pos_dept, bediener_username

        return {"do_it": do_it}


    hoteldpt = get_cache (Hoteldpt, {"num": [(eq, pos_dept)]})

    if hoteldpt:

        kellner = db_session.query(Kellner).filter(
                 (to_string(Kellner.kellner_nr, "99") == (user_init).lower()) & (Kellner.departement == pos_dept)).first()

        if not kellner:

            kellner = get_cache (Kellner, {"kellnername": [(eq, bediener_username)],"departement": [(eq, pos_dept)]})

        if kellner:
            do_it = True

    return generate_output()