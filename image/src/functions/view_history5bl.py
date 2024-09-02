from functions.additional_functions import *
import decimal
from datetime import date
from models import H_journal

def view_history5bl(billno:int, deptno:int, billdate:date):
    hjou_list_list = []
    h_journal = None

    hjou_list = None

    hjou_list_list, Hjou_list = create_model("Hjou_list", {"artnr":int, "anzahl":int, "bezeich":str, "epreis":decimal, "betrag":decimal, "waehrungsnr":int, "bill_datum":date, "zeit":int})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal hjou_list_list, h_journal


        nonlocal hjou_list
        nonlocal hjou_list_list
        return {"hjou-list": hjou_list_list}

    pass


    for h_journal in db_session.query(H_journal).filter(
            (H_journal.rechnr == billno) &  (H_journal.departement == deptno) &  (H_journal.bill_datum == billdate)).all():
        hjou_list = Hjou_list()
        hjou_list_list.append(hjou_list)

        buffer_copy(h_journal, hjou_list)

    return generate_output()