from functions.additional_functions import *
import decimal
from datetime import date
from sqlalchemy import func
from models import Nightaudit, Htparam, Billjournal, Bill, Bill_line

def nt_billdatum():
    progname:str = "nt-billdatum.p"
    curr_rechnr:int = 0
    max_datum:date = None
    nightaudit = htparam = billjournal = bill = bill_line = None

    s_list = None

    s_list_list, S_list = create_model("S_list", {"rechnr":int})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal progname, curr_rechnr, max_datum, nightaudit, htparam, billjournal, bill, bill_line


        nonlocal s_list
        nonlocal s_list_list

        return {}

    nightaudit = db_session.query(Nightaudit).filter(
             (func.lower(Nightaudit.programm) == (progname).lower())).first()

    if not nightaudit:

        return generate_output()
    curr_rechnr = -1

    htparam = db_session.query(Htparam).filter(
             (Htparam.paramnr == 110)).first()

    for billjournal in db_session.query(Billjournal).filter(
             (Billjournal.bill_datum == htparam.fdate)).order_by(Billjournal.rechnr).all():

        if curr_rechnr != billjournal.rechnr:

            bill = db_session.query(Bill).filter(
                     (Bill.rechnr == billjournal.rechnr)).first()

            if bill:
                s_list = S_list()
                s_list_list.append(s_list)

                s_list.rechnr = bill.rechnr
                curr_rechnr = bill.rechnr

    for s_list in query(s_list_list):

        bill = db_session.query(Bill).filter(
                 (Bill.rechnr == s_list.rechnr)).first()
        max_datum = None

        for bill_line in db_session.query(Bill_line).filter(
                 (Bill_line.rechnr == bill.rechnr)).order_by(Bill_line._recid).all():

            if max_datum == None:
                max_datum = bill_line.bill_datum

            elif max_datum < bill_line.bill_datum:
                max_datum = bill_line.bill_datum

        if max_datum > bill.datum:
            bill.datum = max_datum

    return generate_output()