#using conversion tools version: 1.0.0.113

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Hoteldpt, H_artikel, H_journal, Htparam, Exrate, H_bill, Kellner, Artikel, H_bill_line, H_cost

def hmcoup_list_btn_go_1bl(double_currency:bool, foreign_nr:int, exchg_rate:Decimal, billdate:date, from_dept:int, to_dept:int, from_date:date, to_date:date):

    prepare_cache ([Hoteldpt, H_artikel, H_journal, Htparam, Exrate, H_bill, Kellner, Artikel, H_bill_line, H_cost])

    c_list_list = []
    it_exist:bool = False
    hoteldpt = h_artikel = h_journal = htparam = exrate = h_bill = kellner = artikel = h_bill_line = h_cost = None

    h_list = c_list = None

    h_list_list, H_list = create_model("H_list", {"rechnr":int, "departement":int, "datum":date, "betrag":Decimal, "bezeich":string})
    c_list_list, C_list = create_model("C_list", {"nr":int, "datum":date, "dept":int, "deptname":string, "rechnr":int, "pax":int, "bezeich":string, "f_betrag":Decimal, "f_cost":Decimal, "b_betrag":Decimal, "b_cost":Decimal, "betrag":Decimal, "t_cost":Decimal, "o_cost":Decimal, "usr_id":string})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal c_list_list, it_exist, hoteldpt, h_artikel, h_journal, htparam, exrate, h_bill, kellner, artikel, h_bill_line, h_cost
        nonlocal double_currency, foreign_nr, exchg_rate, billdate, from_dept, to_dept, from_date, to_date


        nonlocal h_list, c_list
        nonlocal h_list_list, c_list_list

        return {"c-list": c_list_list}

    def create_mplist():

        nonlocal c_list_list, it_exist, hoteldpt, h_artikel, h_journal, htparam, exrate, h_bill, kellner, artikel, h_bill_line, h_cost
        nonlocal double_currency, foreign_nr, exchg_rate, billdate, from_dept, to_dept, from_date, to_date


        nonlocal h_list, c_list
        nonlocal h_list_list, c_list_list


        h_list_list.clear()

        for hoteldpt in db_session.query(Hoteldpt).filter(
                 (Hoteldpt.num >= from_dept) & (Hoteldpt.num <= to_dept)).order_by(Hoteldpt.num).all():
            if hoteldpt:
                h_journal_obj_list = {}
                h_journal = H_journal()
                h_artikel = H_artikel()
                for h_journal.rechnr, h_journal.departement, h_journal.bill_datum, h_journal.bezeich, h_journal.betrag, h_journal._recid, h_artikel.artnr, h_artikel.departement, h_artikel.prozent, h_artikel._recid in db_session.query(H_journal.rechnr, H_journal.departement, H_journal.bill_datum, H_journal.bezeich, H_journal.betrag, H_journal._recid, H_artikel.artnr, H_artikel.departement, H_artikel.prozent, H_artikel._recid).join(H_artikel,(H_artikel.artnr == H_journal.artnr) & (H_artikel.departement == hoteldpt.num) & (H_artikel.artart == 12)).filter(
                         (H_journal.bill_datum >= from_date) & (H_journal.bill_datum <= to_date) & (H_journal.departement == hoteldpt.num)).order_by(H_journal.rechnr).all():
                    if h_journal_obj_list.get(h_journal._recid):
                        continue
                    else:
                        h_journal_obj_list[h_journal._recid] = True

                    h_list = query(h_list_list, filters=(lambda h_list: h_list.rechnr == h_journal.rechnr and h_list.departement == h_journal.departement and h_list.datum == h_journal.bill_datum and h_list.bezeich == h_journal.bezeich), first=True)

                    if not h_list:
                        h_list = H_list()
                        h_list_list.append(h_list)

                        h_list.rechnr = h_journal.rechnr
                        h_list.departement = h_journal.departement
                        h_list.datum = h_journal.bill_datum
                        h_list.bezeich = h_journal.bezeich
                    h_list.betrag =  to_decimal(h_list.betrag) + to_decimal(h_journal.betrag)

        for h_list in query(h_list_list, filters=(lambda h_list: h_list.betrag == 0)):
            h_list_list.remove(h_list)

    # ... rest of the code

    create_mplist()
    journal_list()

    return generate_output()
