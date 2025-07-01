#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Queasy, Gl_jouhdr

def odoo_journal_historybl(from_date:date, to_date:date):

    prepare_cache ([Queasy, Gl_jouhdr])

    history_list_list = []
    queasy = gl_jouhdr = None

    history_list = bqueasy = None

    history_list_list, History_list = create_model("History_list", {"datum":date, "refno":string, "bezeich":string, "timestamp":int})

    Bqueasy = create_buffer("Bqueasy",Queasy)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal history_list_list, queasy, gl_jouhdr
        nonlocal from_date, to_date
        nonlocal bqueasy


        nonlocal history_list, bqueasy
        nonlocal history_list_list

        return {"history-list": history_list_list}


    history_list_list.clear()

    if from_date == None and to_date == None:
        to_date = get_current_date()
        from_date = to_date - timedelta(days=7)

    if to_date - from_date > 30:

        return generate_output()

    for bqueasy in db_session.query(Bqueasy).filter(
             (Bqueasy.key == 345) & (Bqueasy.date1 >= from_date) & (Bqueasy.date1 <= to_date) & (Bqueasy.logi1 == False) & (Bqueasy.logi2) & (Bqueasy.logi3 == False)).order_by(Bqueasy.date1).all():
        history_list = History_list()
        history_list_list.append(history_list)

        history_list.datum = bqueasy.date1
        history_list.refno = bqueasy.char1
        history_list.timestamp = bqueasy.number2

        gl_jouhdr = get_cache (Gl_jouhdr, {"refno": [(eq, bqueasy.char1)]})

        if gl_jouhdr:
            history_list.bezeich = gl_jouhdr.bezeich

    return generate_output()