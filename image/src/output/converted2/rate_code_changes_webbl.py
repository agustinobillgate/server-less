#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Reslin_queasy

def rate_code_changes_webbl(from_date:date, to_date:date):

    prepare_cache ([Reslin_queasy])

    tt_rate_changes_list = []
    delimiterd:string = ";"
    char_data:string = ""
    v_rate_before:string = ""
    v_rate_after:string = ""
    v_amount_before:Decimal = to_decimal("0.0")
    v_amount_after:Decimal = to_decimal("0.0")
    v_room_category:string = ""
    reslin_queasy = None

    tt_rate_changes = None

    tt_rate_changes_list, Tt_rate_changes = create_model("Tt_rate_changes", {"dated1":date, "dated2":date, "timed":int, "logi":bool, "rate_before":string, "rate_after":string, "amount_after":Decimal, "amount_before":Decimal, "room_category":string})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal tt_rate_changes_list, delimiterd, char_data, v_rate_before, v_rate_after, v_amount_before, v_amount_after, v_room_category, reslin_queasy
        nonlocal from_date, to_date


        nonlocal tt_rate_changes
        nonlocal tt_rate_changes_list

        return {"tt-rate-changes": tt_rate_changes_list}


    tt_rate_changes_list.clear()

    for reslin_queasy in db_session.query(Reslin_queasy).filter(
             (Reslin_queasy.key == ("dynaChanges").lower()) & (Reslin_queasy.date2 >= from_date) & (Reslin_queasy.date2 <= to_date)).order_by(Reslin_queasy._recid).all():
        char_data = reslin_queasy.char3

        if num_entries(char_data, delimiterd) >= 5:
            v_rate_before = entry(0, char_data, delimiterd)
            v_rate_after = entry(1, char_data, delimiterd)
            v_amount_before =  to_decimal(to_decimal(entry(2 , char_data , delimiterd)) )
            v_amount_after =  to_decimal(to_decimal(entry(3 , char_data , delimiterd)) )
            v_room_category = entry(4, char_data, delimiterd)


            tt_rate_changes = Tt_rate_changes()
            tt_rate_changes_list.append(tt_rate_changes)

            tt_rate_changes.dated1 = reslin_queasy.date1
            tt_rate_changes.dated2 = reslin_queasy.date2
            tt_rate_changes.timed = reslin_queasy.number1
            tt_rate_changes.logi = reslin_queasy.logi1
            tt_rate_changes.rate_before = v_rate_before
            tt_rate_changes.rate_after = v_rate_after
            tt_rate_changes.amount_before =  to_decimal(v_amount_before)
            tt_rate_changes.amount_after =  to_decimal(v_amount_after)
            tt_rate_changes.room_category = v_room_category

    return generate_output()