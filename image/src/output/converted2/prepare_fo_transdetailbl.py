#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from functions.htpdate import htpdate
from models import Billjournal, Bill, Res_line, Artikel

def prepare_fo_transdetailbl(bill_no:int, billdate:date, artno:int, amount:Decimal, systdate:date, systtime:int):

    prepare_cache ([Bill, Res_line, Artikel])

    created = False
    found = False
    err = 0
    temp_bjournal_list = []
    currdate:date = None
    ci_dt:date = None
    co_dt:date = None
    fr_date:date = None
    to_date:date = None
    billjournal = bill = res_line = artikel = None

    temp_bjournal = None

    temp_bjournal_list, Temp_bjournal = create_model_like(Billjournal, {"item_name":string}, {"item_name": ""})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal created, found, err, temp_bjournal_list, currdate, ci_dt, co_dt, fr_date, to_date, billjournal, bill, res_line, artikel
        nonlocal bill_no, billdate, artno, amount, systdate, systtime


        nonlocal temp_bjournal
        nonlocal temp_bjournal_list

        return {"created": created, "found": found, "err": err, "temp-bjournal": temp_bjournal_list}

    def transdetail():

        nonlocal created, found, err, temp_bjournal_list, currdate, ci_dt, co_dt, fr_date, to_date, billjournal, bill, res_line, artikel
        nonlocal bill_no, billdate, artno, amount, systdate, systtime


        nonlocal temp_bjournal
        nonlocal temp_bjournal_list


        found = False

        for billjournal in db_session.query(Billjournal).filter(
                 (substring(Billjournal.bezeich, 0, 1) == ("*").lower()) & (Billjournal.bill_datum == billdate) & (Billjournal.artnr == artno) & (Billjournal.anzahl == 0) & (Billjournal.betrag == amount) & (((Billjournal.sysdate == systdate) & (Billjournal.zeit > systtime)) | ((Billjournal.sysdate > systdate)))).order_by(Billjournal.sysdate, Billjournal.zeit).yield_per(100):

            if to_int(replace_str(entry(0, billjournal.bezeich, ";") , "*", "")) == bill_no:
                err = 5
                temp_bjournal = Temp_bjournal()
                temp_bjournal_list.append(temp_bjournal)

                buffer_copy(billjournal, temp_bjournal)
                temp_bjournal.item_name = billjournal.bezeich
                systdate = billjournal.sysdate
                systtime = billjournal.zeit
                bill_no = billjournal.rechnr
                created = True
                found = True


                break

    currdate = get_output(htpdate(110))

    bill = get_cache (Bill, {"rechnr": [(eq, bill_no)]})

    if bill and billdate == None:
        err = 1

        if bill.resnr > 0 and bill.reslinnr > 0:

            res_line = get_cache (Res_line, {"resnr": [(eq, bill.resnr)],"reslinnr": [(eq, bill.parent_nr)]})

            if res_line:
                ci_dt = res_line.ankunft
                co_dt = res_line.abreise


        else:

            billjournal = get_cache (Billjournal, {"rechnr": [(eq, bill.rechnr)]})

            if billjournal:
                fr_date = billjournal.bill_datum
                to_date = billjournal.bill_datum
                ci_dt = fr_date - timedelta(days=30)
                co_dt = to_date + timedelta(days=30)

            billjournal = db_session.query(Billjournal).filter(
                     (Billjournal.rechnr == bill.rechnr)).order_by(Billjournal._recid.desc()).first()

            if billjournal:

                if fr_date > billjournal.bill_datum:
                    fr_date = billjournal.bill_datum
                    ci_dt = fr_date - timedelta(days=30)

                if to_date < billjournal.bill_datum:
                    to_date = billjournal.bill_datum
                    co_dt = to_date + timedelta(days=30)


        err = 2

        if ci_dt != None:

            for billjournal in db_session.query(Billjournal).filter(
                     (substring(Billjournal.bezeich, 0, 1) == ("*").lower()) & (Billjournal.anzahl == 0)).order_by(Billjournal._recid).all():

                if to_int(replace_str(entry(0, billjournal.bezeich, ";") , "*", "")) == bill_no:
                    err = 4
                    temp_bjournal = Temp_bjournal()
                    temp_bjournal_list.append(temp_bjournal)

                    buffer_copy(billjournal, temp_bjournal)

                    artikel = get_cache (Artikel, {"artnr": [(eq, billjournal.artnr)],"departement": [(eq, billjournal.depart)]})

                    if artikel:
                        temp_bjournal.item_name = artikel.bezeich


                    else:
                        temp_bjournal.item_name = billjournal.bezeich
                    created = True


    elif bill and billdate != None:
        while True:
            transdetail()

            if not found:
                break

    return generate_output()