#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Hoteldpt, H_journal, Kellner

def rest_cjourn_journal_list1bl(from_dept:int, to_dept:int, from_date:date, to_date:date):

    prepare_cache ([Hoteldpt, H_journal, Kellner])

    cancel_journal_list = []
    hoteldpt = h_journal = kellner = None

    cancel_journal = None

    cancel_journal_list, Cancel_journal = create_model("Cancel_journal", {"dept":int, "rechnr":int, "billdate":date, "srecid":int, "depart":string, "tbno":string, "artno":string, "bezeich":string, "cancel":string, "qty":string, "amount":Decimal, "zeit":string, "cname":string})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal cancel_journal_list, hoteldpt, h_journal, kellner
        nonlocal from_dept, to_dept, from_date, to_date


        nonlocal cancel_journal
        nonlocal cancel_journal_list

        return {"cancel-journal": cancel_journal_list}

    def journal_list():

        nonlocal cancel_journal_list, hoteldpt, h_journal, kellner
        nonlocal from_dept, to_dept, from_date, to_date


        nonlocal cancel_journal
        nonlocal cancel_journal_list

        qty:int = 0
        sub_tot:Decimal = to_decimal("0.0")
        tot:Decimal = to_decimal("0.0")
        curr_date:date = None
        last_dept:int = -1
        it_exist:bool = False
        kname:string = ""
        cancel_journal_list.clear()

        for hoteldpt in db_session.query(Hoteldpt).filter(
                 (Hoteldpt.num >= from_dept) & (Hoteldpt.num <= to_dept)).order_by(Hoteldpt.num).all():
            sub_tot =  to_decimal("0")
            it_exist = False
            qty = 0
            for curr_date in date_range(from_date,to_date) :

                for h_journal in db_session.query(H_journal).filter(
                         (H_journal.stornogrund != "") & (H_journal.departement == hoteldpt.num) & (H_journal.bill_datum == curr_date)).order_by(H_journal.sysdate.desc(), H_journal.zeit.desc()).all():

                    kellner = get_cache (Kellner, {"kellner_nr": [(eq, h_journal.kellner_nr)],"departement": [(eq, h_journal.departement)]})
                    kname = ""

                    if kellner:
                        kname = kellner.kellnername
                    cancel_journal = Cancel_journal()
                    cancel_journal_list.append(cancel_journal)

                    cancel_journal.dept = h_journal.departement
                    cancel_journal.rechnr = h_journal.rechnr
                    cancel_journal.billdate = h_journal.bill_datum
                    cancel_journal.srecid = h_journal._recid

                    if kellner:
                        cancel_journal.depart = trim(to_string(hoteldpt.depart, "x(30)"))
                        cancel_journal.tbno = trim(to_string(h_journal.tischnr, ">>>>>9"))
                        cancel_journal.artno = trim(to_string(h_journal.artnr, ">>>>>>>>>>>>9"))
                        cancel_journal.bezeich = trim(to_string(h_journal.bezeich, "x(30)"))
                        cancel_journal.cancel = h_journal.stornogrund
                        cancel_journal.qty = to_string(h_journal.anzahl, "-9999")
                        cancel_journal.amount =  to_decimal(h_journal.betrag)
                        cancel_journal.zeit = to_string(h_journal.zeit, "HH:MM:SS")
                        cancel_journal.cname = kname


                    else:
                        cancel_journal.depart = trim(to_string(hoteldpt.depart, "x(30)"))
                        cancel_journal.tbno = trim(to_string(h_journal.tischnr, ">>>>>9"))
                        cancel_journal.artno = trim(to_string(h_journal.artnr, ">>>>>>>>>>>>9"))
                        cancel_journal.bezeich = trim(to_string(h_journal.bezeich, "x(30)"))
                        cancel_journal.cancel = h_journal.stornogrund
                        cancel_journal.qty = to_string(h_journal.anzahl, "-9999")
                        cancel_journal.amount =  to_decimal(h_journal.betrag)
                        cancel_journal.zeit = to_string(h_journal.zeit, "HH:MM:SS")
                        cancel_journal.cname = kname

    journal_list()

    return generate_output()