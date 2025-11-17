# using conversion tools version: 1.0.0.119
"""_yusufwijasena_17/11/2025

    Ticket ID: 20FD2B
        remark: - fix python indentation 
                - fix (Reslin_queasy.key).lower() == "dynachanges")
"""
from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Reslin_queasy


def if_vhp_changes_rate_codebl():

    prepare_cache([Reslin_queasy])

    send_list_data = []
    reslin_queasy = None

    send_list = breslin = None

    send_list_data, Send_list = create_model(
        "Send_list",
        {
            "datum_change": date,
            "datum_avail": date,
            "rcode_before": str,
            "rcode_after": str,
            "amount_before": str,
            "amount_after": str,
            "rec_id": int,
            "rm_type": str
        })

    Breslin = create_buffer("Breslin", Reslin_queasy)

    db_session = local_storage.db_session

    def generate_output():
        nonlocal send_list_data, reslin_queasy
        nonlocal breslin
        nonlocal send_list, breslin
        nonlocal send_list_data

        return {"send-list": send_list_data}

    for reslin_queasy in db_session.query(Reslin_queasy).filter(
            ((Reslin_queasy.key).lower() == "dynachanges") & (Reslin_queasy.logi1)).order_by(Reslin_queasy._recid).all():
        send_list = Send_list()
        send_list_data.append(send_list)

        send_list.datum_change = reslin_queasy.date2
        send_list.datum_avail = reslin_queasy.date1
        send_list.rcode_before = entry(0, reslin_queasy.char3, ";")
        send_list.rcode_after = entry(1, reslin_queasy.char3, ";")
        send_list.amount_before = entry(2, reslin_queasy.char3, ";")
        send_list.amount_after = entry(3, reslin_queasy.char3, ";")
        send_list.rm_type = entry(4, reslin_queasy.char3, ";")
        send_list.rec_id = reslin_queasy._recid

        breslin = get_cache(
            Reslin_queasy, {"_recid": [(eq, reslin_queasy._recid)]})
        breslin.logi1 = False
        breslin.logi2 = True

    return generate_output()
