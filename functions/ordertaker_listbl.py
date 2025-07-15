#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Htparam, H_artikel, H_bill, H_journal, Hoteldpt

def ordertaker_listbl(usr_nr:int, from_date:date, to_date:date):

    prepare_cache ([Htparam, H_bill, H_journal, Hoteldpt])

    odtaker_list_data = []
    long_digit:bool = False
    qty:int = 0
    sub_tot:Decimal = to_decimal("0.0")
    tot:Decimal = to_decimal("0.0")
    curr_date:date = None
    count_data:int = 0
    htparam = h_artikel = h_bill = h_journal = hoteldpt = None

    odtaker_list = None

    odtaker_list_data, Odtaker_list = create_model("Odtaker_list", {"datum":date, "tableno":string, "billno":int, "artno":int, "bezeich":string, "qty":int, "amount":Decimal, "departement":string, "zeit":string, "id":string, "tb":string})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal odtaker_list_data, long_digit, qty, sub_tot, tot, curr_date, count_data, htparam, h_artikel, h_bill, h_journal, hoteldpt
        nonlocal usr_nr, from_date, to_date


        nonlocal odtaker_list
        nonlocal odtaker_list_data

        return {"odtaker-list": odtaker_list_data}

    def create_list():

        nonlocal odtaker_list_data, long_digit, qty, sub_tot, tot, curr_date, count_data, htparam, h_artikel, h_bill, h_journal, hoteldpt
        nonlocal usr_nr, from_date, to_date


        nonlocal odtaker_list
        nonlocal odtaker_list_data


        odtaker_list = Odtaker_list()
        odtaker_list_data.append(odtaker_list)


        hoteldpt = get_cache (Hoteldpt, {"num": [(eq, h_journal.departement)]})
        odtaker_list.datum = h_journal.bill_datum
        odtaker_list.tableno = to_string(h_journal.tischnr, ">>>9")
        odtaker_list.billno = h_journal.rechnr
        odtaker_list.artno = h_journal.artnr
        odtaker_list.bezeich = h_journal.bezeich
        odtaker_list.qty = h_journal.anzahl
        odtaker_list.amount =  to_decimal(h_journal.betrag)
        odtaker_list.zeit = to_string(h_journal.zeit, "HH:MM")
        odtaker_list.id = to_string(h_bill.betriebsnr, ">>>9")
        odtaker_list.tb = to_string(h_bill.kellner_nr, ">>>9")
        odtaker_list.departement = hoteldpt.depart


    htparam = get_cache (Htparam, {"paramnr": [(eq, 246)]})
    long_digit = htparam.flogical
    odtaker_list_data.clear()

    if usr_nr == 0:

        h_journal_obj_list = {}
        for h_journal, h_artikel, h_bill in db_session.query(H_journal, H_artikel, H_bill).join(H_artikel,(H_artikel.artnr == H_journal.artnr) & (H_artikel.departement == H_journal.departement) & (H_artikel.artart == 0)).join(H_bill,(H_bill.rechnr == H_journal.rechnr) & (H_bill.departement == H_journal.departement) & (H_bill.betriebsnr > 0)).filter(
                 (H_journal.bill_datum >= from_date) & (H_journal.bill_datum <= to_date)).order_by(H_journal.rechnr, H_journal.sysdate, H_journal.zeit).all():
            if h_journal_obj_list.get(h_journal._recid):
                continue
            else:
                h_journal_obj_list[h_journal._recid] = True


            create_list()
            qty = qty + h_journal.anzahl
            sub_tot =  to_decimal(sub_tot) + to_decimal(h_journal.betrag)
            tot =  to_decimal(tot) + to_decimal(h_journal.betrag)
            count_data = count_data + 1
    else:

        h_journal_obj_list = {}
        for h_journal, h_artikel, h_bill in db_session.query(H_journal, H_artikel, H_bill).join(H_artikel,(H_artikel.artnr == H_journal.artnr) & (H_artikel.departement == H_journal.departement) & (H_artikel.artart == 0)).join(H_bill,(H_bill.rechnr == H_journal.rechnr) & (H_bill.departement == H_journal.departement) & (H_bill.betriebsnr == usr_nr)).filter(
                 (H_journal.bill_datum >= from_date) & (H_journal.bill_datum <= to_date)).order_by(H_journal.rechnr, H_journal.sysdate, H_journal.zeit).all():
            if h_journal_obj_list.get(h_journal._recid):
                continue
            else:
                h_journal_obj_list[h_journal._recid] = True


            create_list()
            qty = qty + h_journal.anzahl
            sub_tot =  to_decimal(sub_tot) + to_decimal(h_journal.betrag)
            tot =  to_decimal(tot) + to_decimal(h_journal.betrag)
            count_data = count_data + 1

    if count_data > 0:
        odtaker_list = Odtaker_list()
        odtaker_list_data.append(odtaker_list)

        odtaker_list.datum = None
        odtaker_list.tableno = ""
        odtaker_list.billno = 0
        odtaker_list.artno = 0
        odtaker_list.bezeich = "T O T A L"
        odtaker_list.departement = ""
        odtaker_list.qty = qty
        odtaker_list.amount =  to_decimal(tot)
        odtaker_list.zeit = ""
        odtaker_list.id = ""
        odtaker_list.tb = ""

    return generate_output()