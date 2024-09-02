from functions.additional_functions import *
import decimal
from models import H_bill_line, Htparam, H_journal

def ts_restinv_disp_requestbl(t_recid:int):
    request_str = ""
    h_bill_line = htparam = h_journal = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal request_str, h_bill_line, htparam, h_journal


        return {"request_str": request_str}

    def disp_request():

        nonlocal request_str, h_bill_line, htparam, h_journal

        h_bill_line = db_session.query(H_bill_line).filter(
                (H_bill_line._recid == t_recid)).first()

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 557)).first()

        h_journal = db_session.query(H_journal).filter(
                (H_journal.artnr == h_bill_line.artnr) &  (H_journal.departement == h_bill_line.departement) &  (H_journal.rechnr == h_bill_line.rechnr) &  (H_journal.bill_datum == h_bill_line.bill_datum) &  (H_journal.zeit == h_bill_line.zeit) &  (H_journal.sysdate == h_bill_line.sysdate) &  (H_journal.schankbuch == t_recid)).first()

        if h_journal and h_journal.artnr != htparam.finteger:
            request_str = h_journal.aendertext
        else:
            request_str = ""

    disp_request()

    return generate_output()