#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Hoteldpt, H_journal

def view_hbillbl(dept:int, inp_rechnr:int, datum:date):

    prepare_cache ([Hoteldpt, H_journal])

    depart = ""
    t_h_journal_data = []
    hoteldpt = h_journal = None

    t_h_journal = None

    t_h_journal_data, T_h_journal = create_model("T_h_journal", {"artnr":int, "bezeich":string, "anzahl":int, "epreis":Decimal, "betrag":Decimal, "rechnr":int, "departement":int, "bill_datum":date, "sysdate":date, "zeit":int, "rec_id":int})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal depart, t_h_journal_data, hoteldpt, h_journal
        nonlocal dept, inp_rechnr, datum


        nonlocal t_h_journal
        nonlocal t_h_journal_data

        return {"depart": depart, "t-h-journal": t_h_journal_data}

    hoteldpt = get_cache (Hoteldpt, {"num": [(eq, dept)]})
    depart = hoteldpt.depart

    for h_journal in db_session.query(H_journal).filter(
             (H_journal.rechnr == inp_rechnr) & (H_journal.departement == dept) & (H_journal.bill_datum == datum)).order_by(H_journal.sysdate, H_journal.zeit).all():
        t_h_journal = T_h_journal()
        t_h_journal_data.append(t_h_journal)

        t_h_journal.artnr = h_journal.artnr
        t_h_journal.bezeich = h_journal.bezeich
        t_h_journal.anzahl = h_journal.anzahl
        t_h_journal.epreis =  to_decimal(h_journal.epreis)
        t_h_journal.betrag =  to_decimal(h_journal.betrag)
        t_h_journal.rechnr = h_journal.rechnr
        t_h_journal.departement = h_journal.departement
        t_h_journal.bill_datum = h_journal.bill_datum
        t_h_journal.sysdate = h_journal.sysdate
        t_h_journal.zeit = h_journal.zeit
        t_h_journal.rec_id = h_journal._recid

    return generate_output()