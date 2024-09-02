from functions.additional_functions import *
import decimal
from datetime import date
from models import Hoteldpt, H_journal

def view_hbillbl(dept:int, inp_rechnr:int, datum:date):
    depart = ""
    t_h_journal_list = []
    hoteldpt = h_journal = None

    t_h_journal = None

    t_h_journal_list, T_h_journal = create_model("T_h_journal", {"artnr":int, "bezeich":str, "anzahl":int, "epreis":decimal, "betrag":decimal, "rechnr":int, "departement":int, "bill_datum":date, "sysdate":date, "zeit":int})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal depart, t_h_journal_list, hoteldpt, h_journal


        nonlocal t_h_journal
        nonlocal t_h_journal_list
        return {"depart": depart, "t-h-journal": t_h_journal_list}

    hoteldpt = db_session.query(Hoteldpt).filter(
            (Hoteldpt.num == dept)).first()
    depart = hoteldpt.depart

    for h_journal in db_session.query(H_journal).filter(
            (H_journal.rechnr == inp_rechnr) &  (H_journal.departement == dept) &  (H_journal.bill_datum == datum)).all():
        t_h_journal = T_h_journal()
        t_h_journal_list.append(t_h_journal)

        t_h_journal.artnr = h_journal.artnr
        t_h_journal.bezeich = h_journal.bezeich
        t_h_journal.anzahl = h_journal.anzahl
        t_h_journal.epreis = h_journal.epreis
        t_h_journal.betrag = h_journal.betrag
        t_h_journal.rechnr = h_journal.rechnr
        t_h_journal.departement = h_journal.departement
        t_h_journal.bill_datum = h_journal.bill_datum
        t_h_journal.sysdate = h_journal.sysdate
        t_h_journal.zeit = h_journal.zeit

    return generate_output()