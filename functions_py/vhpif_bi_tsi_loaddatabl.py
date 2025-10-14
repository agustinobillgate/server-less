#using conversion tools version: 1.0.0.117

# ==========================================
# Rulita, 14-10-2025 
# Tiket ID : F50EA1 | New Compile program if 
# ==========================================

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Htparam, Queasy

def vhpif_bi_tsi_loaddatabl(casetype:int, recid_queasy:int):

    prepare_cache ([Htparam, Queasy])

    if_list_data = []
    data_date:date = None
    send_date:date = None
    htparam = queasy = None

    if_list = None

    if_list_data, If_list = create_model("If_list", {"send_date":date, "from_date":date, "to_date":date, "if_data_type":string, "send_flag":bool, "resend_flag":bool, "recidqueasy":int})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal if_list_data, data_date, send_date, htparam, queasy
        nonlocal casetype, recid_queasy


        nonlocal if_list
        nonlocal if_list_data

        return {"if-list": if_list_data}

    htparam = get_cache (Htparam, {"paramnr": [(eq, 87)]})
    data_date = htparam.fdate - timedelta(days=1)
    send_date = htparam.fdate

    if casetype == 1:

        queasy = get_cache (Queasy, {"key": [(eq, 309)],"date1": [(eq, send_date)],"char1": [(eq, "room")]})

        if not queasy:
            queasy = Queasy()
            db_session.add(queasy)

            queasy.key = 309
            queasy.date1 = send_date
            queasy.date2 = data_date
            queasy.char1 = "ROOM"
            queasy.logi1 = True
            queasy.logi2 = False

        queasy = get_cache (Queasy, {"key": [(eq, 309)],"date1": [(eq, send_date)],"char1": [(eq, "fb")]})

        if not queasy:
            queasy = Queasy()
            db_session.add(queasy)

            queasy.key = 309
            queasy.date1 = send_date
            queasy.date2 = data_date
            queasy.char1 = "FB"
            queasy.logi1 = True
            queasy.logi2 = False

        queasy = get_cache (Queasy, {"key": [(eq, 309)],"date1": [(eq, send_date)],"char1": [(eq, "avail")]})

        if not queasy:
            queasy = Queasy()
            db_session.add(queasy)

            queasy.key = 309
            queasy.date1 = send_date
            queasy.date2 = data_date
            queasy.char1 = "AVAIL"
            queasy.logi1 = True
            queasy.logi2 = False

        for queasy in db_session.query(Queasy).filter(
                 (Queasy.key == 309) & (Queasy.date1 == send_date) & (Queasy.logi1)).order_by(Queasy._recid).all():
            if_list = If_list()
            if_list_data.append(if_list)

            if_list.send_date = queasy.date1
            if_list.from_date = queasy.date2
            if_list.to_date = queasy.date2
            if_list.if_data_type = queasy.char1
            if_list.send_flag = queasy.logi1
            if_list.resend_flag = queasy.logi2
            if_list.recidqueasy = queasy._recid

        for queasy in db_session.query(Queasy).filter(
                 (Queasy.key == 309) & (Queasy.logi2)).order_by(Queasy._recid).all():
            if_list = If_list()
            if_list_data.append(if_list)

            if_list.send_date = queasy.date1
            if_list.from_date = queasy.date2
            if_list.to_date = queasy.date2
            if_list.if_data_type = queasy.char1
            if_list.send_flag = queasy.logi1
            if_list.resend_flag = queasy.logi2
            if_list.recidqueasy = queasy._recid

    elif casetype == 2:

        queasy = get_cache (Queasy, {"_recid": [(eq, recid_queasy)]})

        if queasy:
            queasy.logi1 = False
            queasy.logi2 = False
            pass

    elif casetype == 3:

        for queasy in db_session.query(Queasy).filter(
                 (Queasy.key == 309) & (Queasy.logi2)).order_by(Queasy._recid).all():
            if_list = If_list()
            if_list_data.append(if_list)

            if_list.send_date = queasy.date1
            if_list.from_date = queasy.date2
            if_list.to_date = queasy.date2
            if_list.if_data_type = queasy.char1
            if_list.send_flag = queasy.logi1
            if_list.resend_flag = queasy.logi2
            if_list.recidqueasy = queasy._recid

    elif casetype == 4:

        for queasy in db_session.query(Queasy).filter(
                 (Queasy.key == 309)).order_by(Queasy._recid).all():
            if_list = If_list()
            if_list_data.append(if_list)

            if_list.send_date = queasy.date1
            if_list.from_date = queasy.date2
            if_list.to_date = queasy.date2
            if_list.if_data_type = queasy.char1
            if_list.send_flag = queasy.logi1
            if_list.resend_flag = queasy.logi2
            if_list.recidqueasy = queasy._recid

    return generate_output()