#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import Hoteldpt, Kellner

def pos_dashboard_check_waiteraccountbl(user_init:string, pos_dept:int, bediener_username:string):

    prepare_cache ([Hoteldpt])

    active_waiter = False
    hoteldpt = kellner = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal active_waiter, hoteldpt, kellner
        nonlocal user_init, pos_dept, bediener_username

        return {"active_waiter": active_waiter}


    hoteldpt = get_cache (Hoteldpt, {"num": [(eq, pos_dept)]})

    if hoteldpt:

        kellner = get_cache (Kellner, {"kellner_nr": [(eq, to_int(user_init))],"departement": [(eq, hoteldpt.num)]})

        if not kellner:

            kellner = get_cache (Kellner, {"kellnername": [(eq, bediener_username)],"departement": [(eq, hoteldpt.num)]})

        if kellner:
            active_waiter = True

            return generate_output()

    return generate_output()