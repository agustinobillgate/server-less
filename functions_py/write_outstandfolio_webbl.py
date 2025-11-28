#using conversion tools version: 1.0.0.117
#-----------------------------------------
# Rd 23/7/2025
# gitlab: 949
# validate rechnr
#-----------------------------------------

# =============================================
# Rulita, 28-11-2025
# - Added with_for_update all query 
# =============================================

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Queasy, Bill, Bediener, Res_history

payload_list_data, Payload_list = create_model("Payload_list", {"ns_rechnr":int, "payment_type":int, "rechnr_remark":int, "input_remark":string, "rechnr_due_date":int, "due_date":date, "mode":int, "user_init":string, "bill_type":string})

def write_outstandfolio_webbl(payload_list_data:[Payload_list]):

    prepare_cache ([Queasy, Bill, Bediener, Res_history])

    guarantee_payment_data = []
    queasy = bill = bediener = res_history = None

    payload_list = guarantee_payment = buff_queasy = None

    guarantee_payment_data, Guarantee_payment = create_model("Guarantee_payment", {"payment_type":string, "payment_number":int})

    Buff_queasy = create_buffer("Buff_queasy",Queasy)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal guarantee_payment_data, queasy, bill, bediener, res_history
        nonlocal buff_queasy


        nonlocal payload_list, guarantee_payment, buff_queasy
        nonlocal guarantee_payment_data

        return {"guarantee-payment": guarantee_payment_data}


    payload_list = query(payload_list_data, first=True)

    if payload_list.mode == 1:

        for queasy in db_session.query(Queasy).filter(
                 (Queasy.key == 9)).order_by(Queasy._recid).all():
            guarantee_payment = Guarantee_payment()
            guarantee_payment_data.append(guarantee_payment)

            guarantee_payment.payment_type = queasy.char1
            guarantee_payment.payment_number = queasy.number1


    else:

        if payload_list.ns_rechnr == None:
            payload_list.ns_rechnr = 0

        if payload_list.ns_rechnr != 0:

            bill = get_cache (Bill, {"rechnr": [(eq, payload_list.ns_rechnr)],"flag": [(eq, 0)],"saldo": [(ne, 0)]})

            if bill:

                if payload_list.bill_type.lower()  == ("NS").lower() :

                    buff_queasy = get_cache (Queasy, {"key": [(eq, 9)],"number1": [(eq, payload_list.payment_type)]})

                    if buff_queasy:

                        # queasy = get_cache (Queasy, {"key": [(eq, 350)],"number1": [(eq, bill.rechnr)]})
                        queasy = db_session.query(Queasy).filter(
                            (Queasy.key == 350) &
                            (Queasy.number1 == bill.rechnr)).with_for_update().first()

                        if queasy:
                            # pass
                            queasy.char1 = buff_queasy.char1
                            db_session.refresh(queasy,with_for_update=True)

                            # pass
                            # pass
                        else:
                            queasy = Queasy()
                            db_session.add(queasy)

                            queasy.key = 350
                            queasy.number1 = bill.rechnr
                            queasy.char1 = buff_queasy.char1
                            queasy.char2 = "NS"

                elif payload_list.bill_type.lower()  == ("M").lower() :

                    buff_queasy = get_cache (Queasy, {"key": [(eq, 9)],"number1": [(eq, payload_list.payment_type)]})

                    if buff_queasy:

                        # queasy = get_cache (Queasy, {"key": [(eq, 350)],"number1": [(eq, bill.rechnr)]})
                        queasy = db_session.query(Queasy).filter(
                            (Queasy.key == 350) &
                            (Queasy.number1 == bill.rechnr)).with_for_update().first()

                        if queasy:
                            # pass
                            queasy.char1 = buff_queasy.char1
                            db_session.refresh(queasy,with_for_update=True)

                            # pass
                            # pass
                        else:
                            queasy = Queasy()
                            db_session.add(queasy)

                            queasy.key = 350
                            queasy.number1 = bill.rechnr
                            queasy.char1 = buff_queasy.char1
                            queasy.char2 = "M"


                else:

                    buff_queasy = get_cache (Queasy, {"key": [(eq, 9)],"number1": [(eq, payload_list.payment_type)]})

                    if buff_queasy:

                        # queasy = get_cache (Queasy, {"key": [(eq, 350)],"number1": [(eq, bill.rechnr)]})
                        queasy = db_session.query(Queasy).filter(
                            (Queasy.key == 350) &
                            (Queasy.number1 == bill.rechnr)).with_for_update().first()

                        if queasy:
                            # pass
                            queasy.char1 = buff_queasy.char1

                            db_session.refresh(queasy,with_for_update=True)
                            # pass
                            # pass
                        else:
                            queasy = Queasy()
                            db_session.add(queasy)

                            queasy.key = 350
                            queasy.number1 = bill.rechnr
                            queasy.char1 = buff_queasy.char1

        if payload_list.rechnr_remark != None:
            # Rd 23/7/2025
            try:
                rechnr = int(payload_list.rechnr_remark)
            except ValueError:
                rechnr = 0
            if payload_list.bill_type.lower()  == ("NS").lower() :
                
               

                # bill = get_cache (Bill, {"rechnr": [(eq, rechnr)],"flag": [(eq, 0)],"saldo": [(ne, 0)]})
                bill = db_session.query(Bill).filter(
                         (Bill.rechnr == rechnr) & (Bill.flag == 0) & (Bill.saldo != 0)).with_for_update().first()

                if bill:

                    if bill.vesrdepot != payload_list.input_remark:

                        bediener = get_cache (Bediener, {"userinit": [(eq, payload_list.user_init)]})
                        res_history = Res_history()
                        db_session.add(res_history)

                        res_history.nr = bediener.nr
                        res_history.datum = get_current_date()
                        res_history.zeit = get_current_time_in_seconds()
                        res_history.action = "Outstanding Folio"


                        res_history.aenderung = "Outstanding Folio: billNo " + to_string(bill.rechnr) + " and BillType:" + payload_list.bill_type + " " + bill.vesrdepot + " changed to " + payload_list.input_remark
                        pass
                        pass
                        pass
                        bill.vesrdepot = payload_list.input_remark

                        db_session.refresh(bill,with_for_update=True)
                        pass
                        # pass

            elif payload_list.bill_type.lower()  == ("M").lower() :
               
                # bill = get_cache (Bill, {"rechnr": [(eq, rechnr)],"flag": [(eq, 0)],"saldo": [(ne, 0)]})
                bill = db_session.query(Bill).filter(
                         (Bill.rechnr == rechnr) & (Bill.flag == 0) & (Bill.saldo != 0)).with_for_update().first()
                if bill:

                    if bill.vesrdepot != payload_list.input_remark:

                        bediener = get_cache (Bediener, {"userinit": [(eq, payload_list.user_init)]})
                        res_history = Res_history()
                        db_session.add(res_history)

                        res_history.nr = bediener.nr
                        res_history.datum = get_current_date()
                        res_history.zeit = get_current_time_in_seconds()
                        res_history.action = "Outstanding Folio"


                        res_history.aenderung = "Outstanding Folio: billNo " + to_string(bill.rechnr) + " and BillType:" + payload_list.bill_type + " " + bill.vesrdepot + " changed to " + payload_list.input_remark
                        pass
                        pass
                        pass
                        bill.vesrdepot = payload_list.input_remark

                        db_session.refresh(bill,with_for_update=True)
                        # pass
                        # pass
            else:

                # bill = get_cache (Bill, {"rechnr": [(eq, rechnr)],"flag": [(eq, 0)],"saldo": [(ne, 0)]})
                bill = db_session.query(Bill).filter(
                         (Bill.rechnr == rechnr) & (Bill.flag == 0) & (Bill.saldo != 0)).with_for_update().first()

                if bill:

                    if bill.vesrdepot != payload_list.input_remark:

                        bediener = get_cache (Bediener, {"userinit": [(eq, payload_list.user_init)]})
                        res_history = Res_history()
                        db_session.add(res_history)

                        res_history.nr = bediener.nr
                        res_history.datum = get_current_date()
                        res_history.zeit = get_current_time_in_seconds()
                        res_history.action = "Outstanding Folio"


                        res_history.aenderung = "Outstanding Folio: billNo " + to_string(bill.rechnr) + " and BillType:GB" + " " + bill.vesrdepot + " changed to " + payload_list.input_remark
                        pass
                        pass
                        pass
                        bill.vesrdepot = payload_list.input_remark

                        db_session.refresh(bill,with_for_update=True)
                        # pass
                        # pass

        if payload_list.rechnr_due_date != None:

            if payload_list.bill_type.lower()  == ("NS").lower() :

                # queasy = get_cache (Queasy, {"key": [(eq, 350)],"number1": [(eq, payload_list.rechnr_due_date)]})
                queasy = db_session.query(Queasy).filter(
                    (Queasy.key == 350) &
                    (Queasy.number1 == payload_list.rechnr_due_date)).with_for_update().first()

                if not queasy:
                    queasy = Queasy()
                    db_session.add(queasy)

                    queasy.key = 350
                    queasy.number1 = payload_list.rechnr_due_date
                    queasy.date1 = payload_list.due_date
                    queasy.char2 = "NS"


                else:
                    pass
                    queasy.date1 = payload_list.due_date

                    db_session.refresh(queasy,with_for_update=True)
                    # pass  
                    # pass

            elif payload_list.bill_type.lower()  == ("M").lower() :

                # queasy = get_cache (Queasy, {"key": [(eq, 350)],"number1": [(eq, payload_list.rechnr_due_date)]})
                queasy = db_session.query(Queasy).filter(
                    (Queasy.key == 350) &
                    (Queasy.number1 == payload_list.rechnr_due_date)).with_for_update().first()

                if not queasy:
                    queasy = Queasy()
                    db_session.add(queasy)

                    queasy.key = 350
                    queasy.number1 = payload_list.rechnr_due_date
                    queasy.date1 = payload_list.due_date
                    queasy.char2 = "M"


                else:
                    pass
                    queasy.date1 = payload_list.due_date
                    db_session.refresh(queasy,with_for_update=True)
                    # pass
                    # pass
            else:

                # queasy = get_cache (Queasy, {"key": [(eq, 350)],"number1": [(eq, payload_list.rechnr_due_date)]})
                queasy = db_session.query(Queasy).filter(
                    (Queasy.key == 350) &
                    (Queasy.number1 == payload_list.rechnr_due_date)).with_for_update().first()

                if not queasy:
                    queasy = Queasy()
                    db_session.add(queasy)

                    queasy.key = 350
                    queasy.number1 = payload_list.rechnr_due_date
                    queasy.date1 = payload_list.due_date


                else:
                    pass
                    queasy.date1 = payload_list.due_date
                    db_session.refresh(queasy,with_for_update=True) 
                    # pass

    return generate_output()