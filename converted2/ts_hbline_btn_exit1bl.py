#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import H_journal, Kellner

def ts_hbline_btn_exit1bl(pvilanguage:int, billdate:date, dept:int, curr_rechnr:int, kbuff_kellner_nr:int):

    prepare_cache ([H_journal, Kellner])

    otherkellner = ""
    msg_str = ""
    lvcarea:string = "TS-hbline"
    h_journal = kellner = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal otherkellner, msg_str, lvcarea, h_journal, kellner
        nonlocal pvilanguage, billdate, dept, curr_rechnr, kbuff_kellner_nr

        return {"otherkellner": otherkellner, "msg_str": msg_str}


    h_journal = get_cache (H_journal, {"bill_datum": [(eq, billdate)],"departement": [(eq, dept)],"rechnr": [(eq, curr_rechnr)],"kellner_nr": [(ne, kbuff_kellner_nr),(ne, 0)]})

    if h_journal:

        kellner = get_cache (Kellner, {"kellner_nr": [(eq, h_journal.kellner_nr)],"departement": [(eq, dept)]})

        if kellner:
            otherkellner = kellner.kellnername
        msg_str = msg_str + chr_unicode(2) + "&W" + translateExtended ("This table is being used by other user:", lvcarea, "") + " " + otherkellner

    return generate_output()