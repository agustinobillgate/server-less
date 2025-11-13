#using conversion tools version: 1.0.0.119

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from functions.htpdate import htpdate
from models import Billjournal, Bill, Res_line, Artikel

def prepare_fo_transdetail_lnlbl(bill_no:int, billdate:date, artno:int, amount:Decimal, systdate:date, systtime:int):

    prepare_cache ([Res_line, Artikel])

    created = False
    temp_bjournal_data = []
    currdate:date = None
    ci_dt:date = None
    co_dt:date = None
    old_room:string = ""
    old_billno:int = 0
    tf_billno:int = 0
    zeit:int = 0
    err:int = 0
    found:bool = False
    fr_date:date = None
    to_date:date = None
    billjournal = bill = res_line = artikel = None

    temp_bjournal = t_bill = buf_bill = None

    temp_bjournal_data, Temp_bjournal = create_model_like(Billjournal, {"item_name":string, "from_roomno":string, "from_billno":int, "from_qty":int, "bj_recid":int}, {"item_name": ""})
    t_bill_data, T_bill = create_model_like(Bill, {"rec_id":int})

    Buf_bill = create_buffer("Buf_bill",Bill)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal created, temp_bjournal_data, currdate, ci_dt, co_dt, old_room, old_billno, tf_billno, zeit, err, found, fr_date, to_date, billjournal, bill, res_line, artikel
        nonlocal bill_no, billdate, artno, amount, systdate, systtime
        nonlocal buf_bill


        nonlocal temp_bjournal, t_bill, buf_bill
        nonlocal temp_bjournal_data, t_bill_data

        return {"created": created, "temp-bjournal": temp_bjournal_data}

    def transdetail():

        nonlocal created, temp_bjournal_data, currdate, ci_dt, co_dt, old_room, old_billno, tf_billno, zeit, err, found, fr_date, to_date, billjournal, bill, res_line, artikel
        nonlocal bill_no, billdate, artno, amount, systdate, systtime
        nonlocal buf_bill


        nonlocal temp_bjournal, t_bill, buf_bill
        nonlocal temp_bjournal_data, t_bill_data


        found = False

        for billjournal in db_session.query(Billjournal).filter(
                 (substring(Billjournal.bezeich, 0, 1) == ("*").lower()) & (Billjournal.bill_datum == billdate) & (Billjournal.artnr == artno) & (Billjournal.anzahl == 0) & (Billjournal.betrag == amount) & (((Billjournal.sysdate == systdate) & (Billjournal.zeit > systtime)) | ((Billjournal.sysdate > systdate)))).order_by(Billjournal.sysdate, Billjournal.zeit).all():

            if to_int(replace_str(entry(0, billjournal.bezeich, ";") , "*", "")) == bill_no:
                err = 5
                temp_bjournal = Temp_bjournal()
                temp_bjournal_data.append(temp_bjournal)

                buffer_copy(billjournal, temp_bjournal)
                temp_bjournal.item_name = billjournal.bezeich
                temp_bjournal.bj_recid = billjournal._recid
                systdate = billjournal.sysdate
                systtime = billjournal.zeit
                bill_no = billjournal.rechnr
                created = True
                found = True


                break


    currdate = get_output(htpdate(110))

    buf_bill = db_session.query(Buf_bill).filter(
             (Buf_bill.rechnr == bill_no)).first()

    if buf_bill:
        old_room = buf_bill.zinr
        old_billno = buf_bill.rechnr
        t_bill = T_bill()
        t_bill_data.append(t_bill)

        buffer_copy(buf_bill, t_bill)
        t_bill.rec_id = buf_bill._recid

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
            zeit = get_current_time_in_seconds()

            for billjournal in db_session.query(Billjournal).filter(
                     (substring(Billjournal.bezeich, 0, 1) == ("*").lower()) & (substring(entry(0, Billjournal.bezeich, ";") , 1) == to_string(bill_no)) & (Billjournal.anzahl == 0)).order_by(Billjournal._recid).all():
                err = 4
                temp_bjournal = Temp_bjournal()
                temp_bjournal_data.append(temp_bjournal)

                buffer_copy(billjournal, temp_bjournal)
                temp_bjournal.bj_recid = billjournal._recid

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

    for temp_bjournal in query(temp_bjournal_data):
        temp_bjournal.from_roomno = old_room
        temp_bjournal.from_billno = old_billno

    for temp_bjournal in query(temp_bjournal_data):

        billjournal = get_cache (Billjournal, {"rechnr": [(eq, temp_bjournal.from_billno)],"departement": [(eq, temp_bjournal.departement)],"artnr": [(eq, temp_bjournal.artnr)]})

        if billjournal:
            temp_bjournal.from_qty = billjournal.anzahl

    return generate_output()