#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import H_bill, Queasy, Htparam, H_bill_line, Tisch, H_journal

def ts_restinv_move_tablebl(pax:int, curr_tischnr:int, rec_id:int, curr_dept:int, tischnr:int, bilrecid:int, rechnr:int, curr_waiter:int, new_waiter:int):

    prepare_cache ([H_bill, Queasy, Htparam, H_bill_line, H_journal])

    bill_date = None
    printed = ""
    balance = to_decimal("0.0")
    balance_foreign = to_decimal("0.0")
    fl_code = 0
    fl_code1 = 0
    fl_code2 = 0
    t_h_bill_data = []
    flag_move:bool = False
    old_billno:int = 0
    curr_recid:int = 0
    active_deposit:bool = False
    h_bill = queasy = htparam = h_bill_line = tisch = h_journal = None

    t_h_bill = buf_bill = buffq251 = buffq33 = None

    t_h_bill_data, T_h_bill = create_model_like(H_bill, {"rec_id":int})

    Buf_bill = create_buffer("Buf_bill",H_bill)
    Buffq251 = create_buffer("Buffq251",Queasy)
    Buffq33 = create_buffer("Buffq33",Queasy)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal bill_date, printed, balance, balance_foreign, fl_code, fl_code1, fl_code2, t_h_bill_data, flag_move, old_billno, curr_recid, active_deposit, h_bill, queasy, htparam, h_bill_line, tisch, h_journal
        nonlocal pax, curr_tischnr, rec_id, curr_dept, tischnr, bilrecid, rechnr, curr_waiter, new_waiter
        nonlocal buf_bill, buffq251, buffq33


        nonlocal t_h_bill, buf_bill, buffq251, buffq33
        nonlocal t_h_bill_data

        return {"pax": pax, "bill_date": bill_date, "printed": printed, "balance": balance, "balance_foreign": balance_foreign, "fl_code": fl_code, "fl_code1": fl_code1, "fl_code2": fl_code2, "t-h-bill": t_h_bill_data}

    def move_table():

        nonlocal bill_date, printed, balance, balance_foreign, fl_code, fl_code1, fl_code2, t_h_bill_data, flag_move, old_billno, curr_recid, active_deposit, h_bill, queasy, htparam, h_bill_line, tisch, h_journal
        nonlocal pax, curr_tischnr, rec_id, curr_dept, tischnr, bilrecid, rechnr, curr_waiter, new_waiter
        nonlocal buf_bill, buffq251, buffq33


        nonlocal t_h_bill, buf_bill, buffq251, buffq33
        nonlocal t_h_bill_data

        new_rechnr:int = 0
        curr_saldo:Decimal = to_decimal("0.0")
        h_bill1 = None
        qbuff = None
        hbline = None
        H_bill1 =  create_buffer("H_bill1",H_bill)
        Qbuff =  create_buffer("Qbuff",Queasy)
        Hbline =  create_buffer("Hbline",H_bill_line)
        new_rechnr = h_bill.rechnr

        queasy = get_cache (Queasy, {"key": [(eq, 31)],"number1": [(eq, curr_dept)],"number2": [(eq, curr_tischnr)]})

        qbuff = get_cache (Queasy, {"key": [(eq, 31)],"number1": [(eq, curr_dept)],"number2": [(eq, tischnr)]})

        if qbuff and qbuff.date1 == None:
            pass

            if queasy:
                qbuff.number3 = queasy.number3
                qbuff.date1 = queasy.date1


            else:
                qbuff.number3 = get_current_time_in_seconds()
                qbuff.date1 = get_current_date()

        if qbuff:
            pass
        pass

        tisch = get_cache (Tisch, {"tischnr": [(eq, tischnr)],"departement": [(eq, curr_dept)]})

        if bilrecid == 0:
            curr_tischnr = h_bill.tischnr
            curr_saldo =  to_decimal(h_bill.saldo)
            pass
            h_bill.tischnr = tischnr
            h_bill.rgdruck = 0
            pass
        else:
            curr_tischnr = h_bill.tischnr
            curr_saldo =  to_decimal(h_bill.saldo)

            h_bill1 = get_cache (H_bill, {"_recid": [(eq, bilrecid)]})
            h_bill1.saldo =  to_decimal(h_bill1.saldo) + to_decimal(curr_saldo)
            h_bill1.mwst[98] = h_bill1.mwst[98] + h_bill.mwst[98]
            h_bill1.tischnr = tischnr
            new_rechnr = h_bill1.rechnr
            h_bill1.rgdruck = 0
            h_bill1.belegung = h_bill1.belegung + h_bill.belegung
            pax = h_bill1.belegung


            pass
            fl_code = 1
            pass
            h_bill.saldo =  to_decimal("0")
            h_bill.mwst[98] = 0
            h_bill.flag = 1


            pass

        if queasy:
            pass
            queasy.number3 = 0
            queasy.date1 = None


            pass
            pass

        for h_bill_line in db_session.query(H_bill_line).filter(
                     (H_bill_line.rechnr == rechnr) & (H_bill_line.departement == curr_dept)).order_by(H_bill_line._recid).all():

            hbline = get_cache (H_bill_line, {"_recid": [(eq, h_bill_line._recid)]})
            pass
            bill_date = h_bill_line.bill_datum
            hbline.tischnr = tischnr
            hbline.rechnr = new_rechnr
            hbline.waehrungsnr = 0


            pass
            pass

        for h_journal in db_session.query(H_journal).filter(
                     (H_journal.rechnr == rechnr) & (H_journal.departement == curr_dept) & (H_journal.bill_datum == bill_date)).order_by(H_journal._recid).all():
            h_journal.tischnr = tischnr
            h_journal.rechnr = new_rechnr


        h_journal = H_journal()
        db_session.add(h_journal)

        h_journal.rechnr = h_bill.rechnr

        if bilrecid != 0:
            h_journal.bezeich = "To Table " + to_string(h_bill1.tischnr) + " *" + to_string(h_bill1.rechnr)
        else:
            h_journal.bezeich = "To Table " + to_string(tischnr) + " *" + to_string(h_bill.rechnr)
        h_journal.tischnr = curr_tischnr
        h_journal.departement = h_bill.departement
        h_journal.zeit = get_current_time_in_seconds()
        h_journal.kellner_nr = curr_waiter
        h_journal.bill_datum = bill_date
        h_journal.artnrfront = 0
        h_journal.aendertext = ""
        h_journal.betrag =  - to_decimal(curr_saldo)


        pass
        h_journal = H_journal()
        db_session.add(h_journal)


        if bilrecid != 0:
            h_journal.rechnr = h_bill1.rechnr
        else:
            h_journal.rechnr = h_bill.rechnr
        h_journal.bezeich = "From Table " + to_string(curr_tischnr) + " *" + to_string(h_bill.rechnr)
        h_journal.tischnr = tischnr
        h_journal.departement = h_bill.departement
        h_journal.zeit = get_current_time_in_seconds()
        h_journal.kellner_nr = curr_waiter
        h_journal.bill_datum = bill_date
        h_journal.artnrfront = 0
        h_journal.aendertext = ""
        h_journal.betrag =  to_decimal(curr_saldo)
        pass

        if curr_waiter == new_waiter:
            rechnr = new_rechnr

            h_bill = get_cache (H_bill, {"tischnr": [(eq, tischnr)],"departement": [(eq, curr_dept)]})
            printed = ""
            balance =  to_decimal(h_bill.saldo)
            balance_foreign =  to_decimal(h_bill.mwst[98])
            fl_code1 = 1
        else:
            fl_code2 = 1
        flag_move = True


    def selforder_moveto_emptytable():

        nonlocal bill_date, printed, balance, balance_foreign, fl_code, fl_code1, fl_code2, t_h_bill_data, flag_move, old_billno, curr_recid, active_deposit, h_bill, queasy, htparam, h_bill_line, tisch, h_journal
        nonlocal pax, curr_tischnr, rec_id, curr_dept, tischnr, bilrecid, rechnr, curr_waiter, new_waiter
        nonlocal buf_bill, buffq251, buffq33


        nonlocal t_h_bill, buf_bill, buffq251, buffq33
        nonlocal t_h_bill_data

        pickup_table = None
        orderbill = None
        b_orderbill = None
        orderbill_line = None
        b_orderbill_line = None
        paygateway_session = None
        b_pg_session = None
        selforder_session = None
        genparamso = None
        buff_hbill = None
        sessionid_one:string = ""
        sessionid_two:string = ""
        mess_str:string = ""
        mess_token:string = ""
        mess_keyword:string = ""
        mess_value:string = ""
        guest_name:string = ""
        i_str:int = 0
        validate_rechnr:int = 0
        bill_no:int = 0
        dynamic_qr:bool = False
        room_serviceflag:bool = False
        hbill_date:date = None
        Pickup_table =  create_buffer("Pickup_table",Queasy)
        Orderbill =  create_buffer("Orderbill",Queasy)
        B_orderbill =  create_buffer("B_orderbill",Queasy)
        Orderbill_line =  create_buffer("Orderbill_line",Queasy)
        B_orderbill_line =  create_buffer("B_orderbill_line",Queasy)
        Paygateway_session =  create_buffer("Paygateway_session",Queasy)
        B_pg_session =  create_buffer("B_pg_session",Queasy)
        Selforder_session =  create_buffer("Selforder_session",Queasy)
        Genparamso =  create_buffer("Genparamso",Queasy)
        Buff_hbill =  create_buffer("Buff_hbill",H_bill)

        for genparamso in db_session.query(Genparamso).filter(
                 (Genparamso.key == 222) & (Genparamso.number1 == 1) & (Genparamso.betriebsnr == curr_dept)).order_by(Genparamso._recid).all():

            if genparamso.number2 == 14:
                dynamic_qr = genparamso.logi1

            if genparamso.number2 == 21:
                room_serviceflag = genparamso.logi1

        if not dynamic_qr:

            pickup_table = get_cache (Queasy, {"key": [(eq, 225)],"char1": [(eq, "taken-table")],"logi1": [(eq, True)],"logi2": [(eq, False)],"number1": [(eq, curr_dept)],"number2": [(eq, curr_tischnr)]})

            if pickup_table:
                sessionid_one = entry(0, pickup_table.char3, "|")

            pickup_table = get_cache (Queasy, {"key": [(eq, 225)],"char1": [(eq, "taken-table")],"logi1": [(eq, True)],"logi2": [(eq, False)],"number1": [(eq, curr_dept)],"number2": [(eq, tischnr)]})

            if pickup_table:
                sessionid_two = entry(0, pickup_table.char3, "|")
        else:

            pickup_table = db_session.query(Pickup_table).filter(
                     (Pickup_table.key == 225) & (Pickup_table.char1 == ("taken-table").lower()) & (Pickup_table.logi1) & (Pickup_table.logi2) & (Pickup_table.number1 == curr_dept) & (Pickup_table.number2 == curr_tischnr) & (length(entry(0, Pickup_table.char3, "|")) <= 20)).first()

            if pickup_table:
                sessionid_one = entry(0, pickup_table.char3, "|")

            pickup_table = db_session.query(Pickup_table).filter(
                     (Pickup_table.key == 225) & (Pickup_table.char1 == ("taken-table").lower()) & (Pickup_table.logi1) & (Pickup_table.logi2) & (Pickup_table.number1 == curr_dept) & (Pickup_table.number2 == tischnr) & (length(entry(0, Pickup_table.char3, "|")) <= 20)).first()

            if pickup_table:
                sessionid_two = entry(0, pickup_table.char3, "|")
                mess_str = pickup_table.char2
                for i_str in range(1,num_entries(mess_str, "|")  + 1) :
                    mess_token = entry(i_str - 1, mess_str, "|")
                    mess_keyword = entry(0, mess_token, "=")
                    mess_value = entry(1, mess_token, "=")

                    if mess_keyword.lower()  == ("NM").lower() :
                        guest_name = mess_value

                    if guest_name != "":
                        return

        h_bill_line = get_cache (H_bill_line, {"rechnr": [(eq, rechnr)],"departement": [(eq, curr_dept)]})

        if h_bill_line:
            hbill_date = h_bill_line.bill_datum

        orderbill = get_cache (Queasy, {"key": [(eq, 225)],"char1": [(eq, "orderbill")],"number1": [(eq, curr_dept)],"number2": [(eq, curr_tischnr)],"char3": [(eq, sessionid_one)],"logi1": [(eq, True)]})

        if not orderbill:

            return

        selforder_session = get_cache (Queasy, {"key": [(eq, 230)],"number1": [(eq, curr_dept)],"number2": [(eq, curr_tischnr)],"char1": [(eq, sessionid_one)],"logi1": [(eq, False)]})

        if selforder_session:

            for orderbill in db_session.query(Orderbill).filter(
                         (Orderbill.key == 225) & (Orderbill.char1 == ("orderbill").lower()) & (Orderbill.number1 == curr_dept) & (Orderbill.number2 == curr_tischnr) & (Orderbill.char3 == sessionid_one) & (Orderbill.logi1) & (Orderbill.logi3)).order_by(Orderbill.number3).yield_per(100):
                mess_str = orderbill.char2
                for i_str in range(1,num_entries(mess_str, "|")  + 1) :
                    mess_token = entry(i_str - 1, mess_str, "|")
                    mess_keyword = entry(0, mess_token, "=")
                    mess_value = entry(1, mess_token, "=")

                    if mess_keyword.lower()  == ("BL").lower() :
                        validate_rechnr = to_int(mess_value)

                    if validate_rechnr != 0:
                        break

                b_orderbill = get_cache (Queasy, {"_recid": [(eq, orderbill._recid)]})

                if b_orderbill:
                    pass
                    b_orderbill.number1 = curr_dept
                    b_orderbill.number2 = tischnr
                    b_orderbill.char3 = sessionid_two

                    if not dynamic_qr:
                        b_orderbill.char2 = entry(1, b_orderbill.char2, "|", "NM=GuestTable" + to_string(tischnr))
                    else:
                        b_orderbill.char2 = entry(1, b_orderbill.char2, "|", "NM=" + guest_name)
                    pass
                    pass

            for orderbill_line in db_session.query(Orderbill_line).filter(
                         (Orderbill_line.key == 225) & (Orderbill_line.char1 == ("orderbill-line").lower()) & (Orderbill_line.number2 == curr_tischnr) & (entry(0, Orderbill_line.char2, "|") == to_string(curr_dept)) & (entry(3, Orderbill_line.char2, "|") == sessionid_one) & (Orderbill_line.logi2) & (Orderbill_line.logi3)).order_by(Orderbill_line._recid).all():

                b_orderbill_line = get_cache (Queasy, {"_recid": [(eq, orderbill_line._recid)]})

                if b_orderbill_line:
                    pass
                    b_orderbill_line.number2 = tischnr
                    b_orderbill_line.char2 = entry(0, b_orderbill_line.char2, "|", to_string(curr_dept))
                    b_orderbill_line.char2 = entry(1, b_orderbill_line.char2, "|", to_string(tischnr))
                    b_orderbill_line.char2 = entry(3, b_orderbill_line.char2, "|", sessionid_two)


                    pass
                    pass

            if dynamic_qr:
                pass
                selforder_session.logi1 = True
                pass

                pickup_table = db_session.query(Pickup_table).filter(
                             (Pickup_table.key == 225) & (Pickup_table.char1 == ("taken-table").lower()) & (Pickup_table.logi1) & (Pickup_table.logi2) & (Pickup_table.number1 == curr_dept) & (Pickup_table.number2 == curr_tischnr) & (entry(0, Pickup_table.char3, "|") == sessionid_one)).first()

                if pickup_table:
                    pass
                    pickup_table.char3 = entry(0, pickup_table.char3, "|", sessionid_one + "T" + replace_str(to_string(get_current_date()) , "/", "") + replace_str(to_string(get_current_time_in_seconds(), "HH:MM") , ":", ""))
                    pass
                    pass

            paygateway_session = get_cache (Queasy, {"key": [(eq, 223)],"number1": [(eq, curr_dept)],"char3": [(eq, sessionid_one)],"betriebsnr": [(eq, rechnr)]})

            if paygateway_session:
                bill_no = paygateway_session.betriebsnr

                b_pg_session = get_cache (Queasy, {"key": [(eq, 223)],"number1": [(eq, curr_dept)],"char3": [(eq, sessionid_two)]})

                if b_pg_session:
                    pass
                    b_pg_session.betriebsnr = bill_no
                    pass
                    pass
                pass
                paygateway_session.betriebsnr = 0
                pass
                pass
            pass


    def selforder_moveto_occtable():

        nonlocal bill_date, printed, balance, balance_foreign, fl_code, fl_code1, fl_code2, t_h_bill_data, flag_move, old_billno, curr_recid, active_deposit, h_bill, queasy, htparam, h_bill_line, tisch, h_journal
        nonlocal pax, curr_tischnr, rec_id, curr_dept, tischnr, bilrecid, rechnr, curr_waiter, new_waiter
        nonlocal buf_bill, buffq251, buffq33


        nonlocal t_h_bill, buf_bill, buffq251, buffq33
        nonlocal t_h_bill_data

        pickup_table = None
        orderbill = None
        b_orderbill = None
        orderbill_line = None
        b_orderbill_line = None
        paygateway_session = None
        b_pg_session = None
        selforder_session = None
        genparamso = None
        buff_hbill = None
        sessionid_one:string = ""
        sessionid_two:string = ""
        mess_str:string = ""
        mess_token:string = ""
        mess_keyword:string = ""
        mess_value:string = ""
        guest_name:string = ""
        i_str:int = 0
        validate_rechnr:int = 0
        bill_no:int = 0
        new_billno:int = 0
        orderbill_counter:int = 0
        orderbill_count:int = 0
        orderbill_line_count:int = 0
        dynamic_qr:bool = False
        room_serviceflag:bool = False
        hbill_date:date = None
        Pickup_table =  create_buffer("Pickup_table",Queasy)
        Orderbill =  create_buffer("Orderbill",Queasy)
        B_orderbill =  create_buffer("B_orderbill",Queasy)
        Orderbill_line =  create_buffer("Orderbill_line",Queasy)
        B_orderbill_line =  create_buffer("B_orderbill_line",Queasy)
        Paygateway_session =  create_buffer("Paygateway_session",Queasy)
        B_pg_session =  create_buffer("B_pg_session",Queasy)
        Selforder_session =  create_buffer("Selforder_session",Queasy)
        Genparamso =  create_buffer("Genparamso",Queasy)
        Buff_hbill =  create_buffer("Buff_hbill",H_bill)

        for genparamso in db_session.query(Genparamso).filter(
                 (Genparamso.key == 222) & (Genparamso.number1 == 1) & (Genparamso.betriebsnr == curr_dept)).order_by(Genparamso._recid).all():

            if genparamso.number2 == 14:
                dynamic_qr = genparamso.logi1

            if genparamso.number2 == 21:
                room_serviceflag = genparamso.logi1

        if not dynamic_qr:

            pickup_table = get_cache (Queasy, {"key": [(eq, 225)],"char1": [(eq, "taken-table")],"logi1": [(eq, True)],"logi2": [(eq, False)],"number1": [(eq, curr_dept)],"number2": [(eq, curr_tischnr)]})

            if pickup_table:
                sessionid_one = entry(0, pickup_table.char3, "|")

            pickup_table = get_cache (Queasy, {"key": [(eq, 225)],"char1": [(eq, "taken-table")],"logi1": [(eq, True)],"logi2": [(eq, False)],"number1": [(eq, curr_dept)],"number2": [(eq, tischnr)]})

            if pickup_table:
                sessionid_two = entry(0, pickup_table.char3, "|")
        else:

            pickup_table = db_session.query(Pickup_table).filter(
                     (Pickup_table.key == 225) & (Pickup_table.char1 == ("taken-table").lower()) & (Pickup_table.logi1) & (Pickup_table.logi2) & (Pickup_table.number1 == curr_dept) & (Pickup_table.number2 == curr_tischnr) & (length(entry(0, Pickup_table.char3, "|")) <= 20)).first()

            if pickup_table:
                sessionid_one = entry(0, pickup_table.char3, "|")

            pickup_table = db_session.query(Pickup_table).filter(
                     (Pickup_table.key == 225) & (Pickup_table.char1 == ("taken-table").lower()) & (Pickup_table.logi1) & (Pickup_table.logi2) & (Pickup_table.number1 == curr_dept) & (Pickup_table.number2 == tischnr) & (length(entry(0, Pickup_table.char3, "|")) <= 20)).first()

            if pickup_table:
                sessionid_two = entry(0, pickup_table.char3, "|")
                mess_str = pickup_table.char2
                for i_str in range(1,num_entries(mess_str, "|")  + 1) :
                    mess_token = entry(i_str - 1, mess_str, "|")
                    mess_keyword = entry(0, mess_token, "=")
                    mess_value = entry(1, mess_token, "=")

                    if mess_keyword.lower()  == ("NM").lower() :
                        guest_name = mess_value

                    if guest_name != "":
                        return

        h_bill = get_cache (H_bill, {"_recid": [(eq, bilrecid)]})

        if h_bill:

            h_bill_line = get_cache (H_bill_line, {"rechnr": [(eq, rechnr)],"departement": [(eq, curr_dept)]})

            if h_bill_line:
                hbill_date = h_bill_line.bill_datum

        orderbill = get_cache (Queasy, {"key": [(eq, 225)],"char1": [(eq, "orderbill")],"number1": [(eq, curr_dept)],"number2": [(eq, curr_tischnr)],"char3": [(eq, sessionid_one)],"logi1": [(eq, True)]})

        if not orderbill:

            return

        selforder_session = get_cache (Queasy, {"key": [(eq, 230)],"number1": [(eq, curr_dept)],"number2": [(eq, curr_tischnr)],"char1": [(eq, sessionid_one)],"logi1": [(eq, False)]})

        if selforder_session:

            buff_hbill = get_cache (H_bill, {"_recid": [(eq, bilrecid)]})

            if buff_hbill:
                new_billno = buff_hbill.rechnr

            for orderbill in db_session.query(Orderbill).filter(
                         (Orderbill.key == 225) & (Orderbill.char1 == ("orderbill").lower()) & (Orderbill.number1 == curr_dept) & (Orderbill.number2 == tischnr) & (Orderbill.char3 == sessionid_two) & (Orderbill.logi1) & (Orderbill.logi3)).order_by(Orderbill.number3.desc()).yield_per(100):
                orderbill_counter = orderbill.number3
                break

            for orderbill in db_session.query(Orderbill).filter(
                         (Orderbill.key == 225) & (Orderbill.char1 == ("orderbill").lower()) & (Orderbill.number1 == curr_dept) & (Orderbill.number2 == curr_tischnr) & (Orderbill.char3 == sessionid_one) & (Orderbill.logi1) & (Orderbill.logi3)).order_by(Orderbill.number3).yield_per(100):
                orderbill_counter = orderbill_counter + 1
                mess_str = orderbill.char2
                for i_str in range(1,num_entries(mess_str, "|")  + 1) :
                    mess_token = entry(i_str - 1, mess_str, "|")
                    mess_keyword = entry(0, mess_token, "=")
                    mess_value = entry(1, mess_token, "=")

                    if mess_keyword.lower()  == ("BL").lower() :
                        validate_rechnr = to_int(mess_value)

                    if validate_rechnr != 0:
                        break

                for orderbill_line in db_session.query(Orderbill_line).filter(
                             (Orderbill_line.key == 225) & (Orderbill_line.char1 == ("orderbill-line").lower()) & (Orderbill_line.number1 == orderbill.number3) & (Orderbill_line.number2 == curr_tischnr) & (entry(0, Orderbill_line.char2, "|") == to_string(curr_dept)) & (entry(3, Orderbill_line.char2, "|") == sessionid_one) & (Orderbill_line.logi2) & (Orderbill_line.logi3)).order_by(Orderbill_line._recid).all():

                    b_orderbill_line = get_cache (Queasy, {"_recid": [(eq, orderbill_line._recid)]})

                    if b_orderbill_line:
                        pass
                        b_orderbill_line.number1 = orderbill_counter
                        b_orderbill_line.number2 = tischnr
                        b_orderbill_line.char2 = entry(0, b_orderbill_line.char2, "|", to_string(curr_dept))
                        b_orderbill_line.char2 = entry(1, b_orderbill_line.char2, "|", to_string(tischnr))
                        b_orderbill_line.char2 = entry(3, b_orderbill_line.char2, "|", sessionid_two)


                        pass
                        pass

                b_orderbill = get_cache (Queasy, {"_recid": [(eq, orderbill._recid)]})

                if b_orderbill:
                    pass
                    b_orderbill.number1 = curr_dept
                    b_orderbill.number2 = tischnr
                    b_orderbill.number3 = orderbill_counter
                    b_orderbill.char3 = sessionid_two

                    if num_entries(b_orderbill.char2, "|") >= 8:
                        b_orderbill.betriebsnr = bilrecid
                        b_orderbill.char2 = entry(7, b_orderbill.char2, "|", "BL=" + to_string(new_billno))

                    if not dynamic_qr:
                        b_orderbill.char2 = entry(1, b_orderbill.char2, "|", "NM=GuestTable" + to_string(tischnr))
                    else:
                        b_orderbill.char2 = entry(1, b_orderbill.char2, "|", "NM=" + guest_name)
                    pass
                    pass

            if dynamic_qr:
                pass
                selforder_session.logi1 = True
                pass

                pickup_table = db_session.query(Pickup_table).filter(
                             (Pickup_table.key == 225) & (Pickup_table.char1 == ("taken-table").lower()) & (Pickup_table.logi1) & (Pickup_table.logi2) & (Pickup_table.number1 == curr_dept) & (Pickup_table.number2 == curr_tischnr) & (entry(0, Pickup_table.char3, "|") == sessionid_one)).first()

                if pickup_table:
                    pass
                    pickup_table.char3 = entry(0, pickup_table.char3, "|", sessionid_one + "T" + replace_str(to_string(get_current_date()) , "/", "") + replace_str(to_string(get_current_time_in_seconds(), "HH:MM") , ":", ""))
                    pass
                    pass

            paygateway_session = get_cache (Queasy, {"key": [(eq, 223)],"number1": [(eq, curr_dept)],"char3": [(eq, sessionid_one)],"betriebsnr": [(eq, old_billno)]})

            if paygateway_session:
                pass
                paygateway_session.betriebsnr = 0
                pass
                pass
            pass


    htparam = get_cache (Htparam, {"paramnr": [(eq, 588)]})

    if htparam:
        active_deposit = htparam.flogical

    h_bill = get_cache (H_bill, {"_recid": [(eq, rec_id)]})

    if h_bill:
        old_billno = h_bill.rechnr

        buf_bill = get_cache (H_bill, {"rechnr": [(eq, rechnr)],"departement": [(eq, curr_dept)],"tischnr": [(eq, curr_tischnr)]})

        if not buf_bill:
            fl_code = 2

            return generate_output()
    move_table()
    pass

    if h_bill:
        t_h_bill = T_h_bill()
        t_h_bill_data.append(t_h_bill)

        buffer_copy(h_bill, t_h_bill)
        t_h_bill.rec_id = h_bill._recid

    if flag_move:

        queasy = get_cache (Queasy, {"key": [(eq, 230)]})

        if queasy:

            if bilrecid != 0:
                selforder_moveto_occtable()
            else:
                selforder_moveto_emptytable()

        if active_deposit:

            if bilrecid != 0:
                curr_recid = bilrecid
            else:
                curr_recid = rec_id

            buffq251 = get_cache (Queasy, {"key": [(eq, 251)],"number1": [(eq, curr_recid)]})

            if buffq251:

                buffq33 = get_cache (Queasy, {"_recid": [(eq, buffq251.number2)]})

                if buffq33:
                    pass
                    buffq33.number2 = tischnr

                    if num_entries(buffq33.char3, ";") <= 3:
                        buffq33.char3 = buffq33.char3 + "Move Table From " + to_string(curr_tischnr) + " to " + to_string(tischnr) + " - UserID " + to_string(curr_waiter)
                    pass
                    pass

                if bilrecid != 0:
                    pass
                    buffq251.number1 = curr_recid
                    pass
                    pass

    return generate_output()