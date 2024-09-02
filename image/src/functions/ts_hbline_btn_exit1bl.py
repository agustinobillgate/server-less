from functions.additional_functions import *
import decimal
from datetime import date
from models import H_journal, Kellner

def ts_hbline_btn_exit1bl(pvilanguage:int, billdate:date, dept:int, curr_rechnr:int, kbuff_kellner_nr:int):
    otherkellner = ""
    msg_str = ""
    lvcarea:str = "TS_hbline"
    h_journal = kellner = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal otherkellner, msg_str, lvcarea, h_journal, kellner


        return {"otherkellner": otherkellner, "msg_str": msg_str}


    h_journal = db_session.query(H_journal).filter(
            (H_journal.bill_datum == billdate) &  (H_journal.departement == dept) &  (H_journal.rechnr == curr_rechnr) &  (H_journal.kellner_nr != kbuff_kellner_nr) &  (H_journal.kellner_nr != 0)).first()

    if h_journal:

        kellner = db_session.query(Kellner).filter(
                (Kellner_nr == h_journal.kellner_nr) &  (Kellner.departement == dept)).first()

        if kellner:
            otherkellner = kellnername
        msg_str = msg_str + chr(2) + "&W" + translateExtended ("This table is being used by other user:", lvcarea, "") + " " + otherkellner

    return generate_output()