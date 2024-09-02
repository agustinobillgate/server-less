from functions.additional_functions import *
import decimal
from datetime import date
from models import Hoteldpt, H_journal, Kellner

def rest_cjourn_journal_list1bl(from_dept:int, to_dept:int, from_date:date, to_date:date):
    cancel_journal_list = []
    hoteldpt = h_journal = kellner = None

    cancel_journal = None

    cancel_journal_list, Cancel_journal = create_model("Cancel_journal", {"dept":int, "rechnr":int, "billdate":date, "srecid":int, "depart":str, "tbno":str, "artno":str, "bezeich":str, "cancel":str, "qty":str, "amount":decimal, "zeit":str, "cname":str})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal cancel_journal_list, hoteldpt, h_journal, kellner


        nonlocal cancel_journal
        nonlocal cancel_journal_list
        return {"cancel-journal": cancel_journal_list}

    def journal_list():

        nonlocal cancel_journal_list, hoteldpt, h_journal, kellner


        nonlocal cancel_journal
        nonlocal cancel_journal_list

        qty:int = 0
        sub_tot:decimal = 0
        tot:decimal = 0
        curr_date:date = None
        last_dept:int = -1
        it_exist:bool = False
        kname:str = ""
        cancel_journal_list.clear()

        for hoteldpt in db_session.query(Hoteldpt).filter(
                (Hoteldpt.num >= from_dept) &  (Hoteldpt.num <= to_dept)).all():
            sub_tot = 0
            it_exist = False
            qty = 0
            for curr_date in range(from_date,to_date + 1) :

                for h_journal in db_session.query(H_journal).filter(
                        (H_journal.stornogrund != "") &  (H_journal.departement == hoteldpt.num) &  (H_journal.bill_datum == curr_date)).all():

                    kellner = db_session.query(Kellner).filter(
                            (Kellner_nr == h_journal.kellner_nr) &  (Kellner.departement == h_journal.departement)).first()
                    kname = ""

                    if kellner:
                        kname = kellnername
                    cancel_journal = Cancel_journal()
                    cancel_journal_list.append(cancel_journal)

                    cancel_journal.dept = h_journal.departement
                    cancel_journal.rechnr = h_journal.rechnr
                    cancel_journal.billdate = h_journal.bill_datum
                    cancel_journal.srecid = h_journal._recid

                    if kellner:
                        cancel_journal.depart = to_string(hoteldpt.depart, "x(30)")
                        cancel_journal.tbno = to_string(h_journal.tischnr, ">>>>>9")
                        cancel_journal.artno = to_string(h_journal.artnr, ">>>>9")
                        cancel_journal.bezeich = to_string(h_journal.bezeich, "x(30)")
                        cancel_journal.cancel = to_string(h_journal.stornogrund, "x(30)")
                        cancel_journal.qty = to_string(h_journal.anzahl, "-9999")
                        cancel_journal.amount = h_journal.betrag
                        cancel_journal.zeit = to_string(h_journal.zeit, "HH:MM:SS")
                        cancel_journal.cname = kname


                    else:
                        cancel_journal.depart = to_string(hoteldpt.depart, "x(30)")
                        cancel_journal.tbno = to_string(h_journal.tischnr, ">>>>>9")
                        cancel_journal.artno = to_string(h_journal.artnr, ">>>>9")
                        cancel_journal.bezeich = to_string(h_journal.bezeich, "x(30)")
                        cancel_journal.cancel = to_string(h_journal.stornogrund, "x(30)")
                        cancel_journal.qty = to_string(h_journal.anzahl, "-9999")
                        cancel_journal.amount = h_journal.betrag
                        cancel_journal.zeit = to_string(h_journal.zeit, "HH:MM:SS")
                        cancel_journal.cname = kname


    journal_list()

    return generate_output()