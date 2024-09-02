from functions.additional_functions import *
import decimal
from datetime import date
from sqlalchemy import func
from models import H_bill, Queasy, Htparam, H_bill_line, Tisch, H_journal

def ts_restinv_move_tablebl(pax:int, curr_tischnr:int, rec_id:int, curr_dept:int, tischnr:int, bilrecid:int, rechnr:int, curr_waiter:int, new_waiter:int):
    bill_date = None
    printed = ""
    balance = 0
    balance_foreign = 0
    fl_code = 0
    fl_code1 = 0
    fl_code2 = 0
    t_h_bill_list = []
    flag_move:bool = False
    old_billno:int = 0
    curr_recid:int = 0
    active_deposit:bool = False
    h_bill = queasy = htparam = h_bill_line = tisch = h_journal = None

    t_h_bill = buf_bill = buffq251 = buffq33 = h_bill1 = qbuff = hbline = pickup_table = orderbill = b_orderbill = orderbill_line = b_orderbill_line = paygateway_session = b_pg_session = selforder_session = genparamso = buff_hbill = None

    t_h_bill_list, T_h_bill = create_model_like(H_bill, {"rec_id":int})

    Buf_bill = H_bill
    Buffq251 = Queasy
    Buffq33 = Queasy
    H_bill1 = H_bill
    Qbuff = Queasy
    Hbline = H_bill_line
    Pickup_table = Queasy
    Orderbill = Queasy
    B_orderbill = Queasy
    Orderbill_line = Queasy
    B_orderbill_line = Queasy
    Paygateway_session = Queasy
    B_pg_session = Queasy
    Selforder_session = Queasy
    Genparamso = Queasy
    Buff_hbill = H_bill

    db_session = local_storage.db_session

    def generate_output():
        nonlocal bill_date, printed, balance, balance_foreign, fl_code, fl_code1, fl_code2, t_h_bill_list, flag_move, old_billno, curr_recid, active_deposit, h_bill, queasy, htparam, h_bill_line, tisch, h_journal
        nonlocal buf_bill, buffq251, buffq33, h_bill1, qbuff, hbline, pickup_table, orderbill, b_orderbill, orderbill_line, b_orderbill_line, paygateway_session, b_pg_session, selforder_session, genparamso, buff_hbill


        nonlocal t_h_bill, buf_bill, buffq251, buffq33, h_bill1, qbuff, hbline, pickup_table, orderbill, b_orderbill, orderbill_line, b_orderbill_line, paygateway_session, b_pg_session, selforder_session, genparamso, buff_hbill
        nonlocal t_h_bill_list
        return {"bill_date": bill_date, "printed": printed, "balance": balance, "balance_foreign": balance_foreign, "fl_code": fl_code, "fl_code1": fl_code1, "fl_code2": fl_code2, "t-h-bill": t_h_bill_list}

    def move_table():

        nonlocal bill_date, printed, balance, balance_foreign, fl_code, fl_code1, fl_code2, t_h_bill_list, flag_move, old_billno, curr_recid, active_deposit, h_bill, queasy, htparam, h_bill_line, tisch, h_journal
        nonlocal buf_bill, buffq251, buffq33, h_bill1, qbuff, hbline, pickup_table, orderbill, b_orderbill, orderbill_line, b_orderbill_line, paygateway_session, b_pg_session, selforder_session, genparamso, buff_hbill


        nonlocal t_h_bill, buf_bill, buffq251, buffq33, h_bill1, qbuff, hbline, pickup_table, orderbill, b_orderbill, orderbill_line, b_orderbill_line, paygateway_session, b_pg_session, selforder_session, genparamso, buff_hbill
        nonlocal t_h_bill_list

        new_rechnr:int = 0
        curr_saldo:decimal = 0
        H_bill1 = H_bill
        Qbuff = Queasy
        Hbline = H_bill_line
        new_rechnr = h_bill.rechnr

        queasy = db_session.query(Queasy).filter(
                    (Queasy.key == 31) &  (Queasy.number1 == curr_dept) &  (Queasy.number2 == curr_tischnr)).first()

        qbuff = db_session.query(Qbuff).filter(
                    (Qbuff.key == 31) &  (Qbuff.number1 == curr_dept) &  (Qbuff.number2 == tischnr)).first()

        if qbuff and qbuff.date1 == None:

            if queasy:
                qbuff.number3 = queasy.number3
                qbuff.date1 = queasy.date1


            else:
                qbuff.number3 = get_current_time_in_seconds()
                qbuff.date1 = get_current_date()

        if qbuff:

            qbuff = db_session.query(Qbuff).first()

        tisch = db_session.query(Tisch).filter(
                    (tischnr == tischnr) &  (Tisch.departement == curr_dept)).first()

        if bilrecid == 0:
            curr_tischnr = h_bill.tischnr
            curr_saldo = h_bill.saldo

            h_bill = db_session.query(H_bill).first()
            h_bill.tischnr = tischnr
            h_bill.rgdruck = 0

            h_bill = db_session.query(H_bill).first()
        else:
            curr_tischnr = h_bill.tischnr
            curr_saldo = h_bill.saldo

            h_bill1 = db_session.query(H_bill1).filter(
                        (H_bill1._recid == bilrecid)).first()
            h_bill1.saldo = h_bill1.saldo + curr_saldo
            h_bill1.mwst[98] = h_bill1.mwst[98] + h_bill.mwst[98]
            h_bill1.tischnr = tischnr
            new_rechnr = h_bill1.rechnr
            h_bill1.rgdruck = 0
            h_bill1.belegung = h_bill1.belegung + h_bill.belegung
            pax = h_bill1.belegung

            h_bill1 = db_session.query(H_bill1).first()
            fl_code = 1

            h_bill = db_session.query(H_bill).first()
            h_bill.saldo = 0
            h_bill.mwst[98] = 0
            h_bill.flag = 1

            h_bill = db_session.query(H_bill).first()

        if queasy:
            queasy.number3 = 0
            queasy.date1 = None

            queasy = db_session.query(Queasy).first()

        for h_bill_line in db_session.query(H_bill_line).filter(
                    (H_bill_line.rechnr == rechnr) &  (H_bill_line.departement == curr_dept)).all():

            hbline = db_session.query(Hbline).filter(
                        (Hbline._recid == h_bill_line._recid)).first()
            bill_date = h_bill_line.bill_datum
            hbline.tischnr = tischnr
            hbline.rechnr = new_rechnr
            hbline.waehrungsnr = 0

            hbline = db_session.query(Hbline).first()

        for h_journal in db_session.query(H_journal).filter(
                    (H_journal.rechnr == rechnr) &  (H_journal.departement == curr_dept) &  (H_journal.bill_datum == bill_date)).all():
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
        h_journal.betrag = - curr_saldo

        h_journal = db_session.query(H_journal).first()
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
        h_journal.betrag = curr_saldo

        h_journal = db_session.query(H_journal).first()


        if curr_waiter == new_waiter:
            rechnr = new_rechnr

            h_bill = db_session.query(H_bill).filter(
                    (H_bill.tischnr == tischnr) &  (H_bill.departement == curr_dept)).first()
            printed = ""
            balance = h_bill.saldo
            balance_foreign = h_bill.mwst[98]
            fl_code1 = 1
        else:
            fl_code2 = 1
        flag_move = True

    def selforder_moveto_emptytable():

        nonlocal bill_date, printed, balance, balance_foreign, fl_code, fl_code1, fl_code2, t_h_bill_list, flag_move, old_billno, curr_recid, active_deposit, h_bill, queasy, htparam, h_bill_line, tisch, h_journal
        nonlocal buf_bill, buffq251, buffq33, h_bill1, qbuff, hbline, pickup_table, orderbill, b_orderbill, orderbill_line, b_orderbill_line, paygateway_session, b_pg_session, selforder_session, genparamso, buff_hbill


        nonlocal t_h_bill, buf_bill, buffq251, buffq33, h_bill1, qbuff, hbline, pickup_table, orderbill, b_orderbill, orderbill_line, b_orderbill_line, paygateway_session, b_pg_session, selforder_session, genparamso, buff_hbill
        nonlocal t_h_bill_list

        sessionid_one:str = ""
        sessionid_two:str = ""
        mess_str:str = ""
        mess_token:str = ""
        mess_keyword:str = ""
        mess_value:str = ""
        guest_name:str = ""
        i_str:int = 0
        validate_rechnr:int = 0
        bill_no:int = 0
        dynamic_qr:bool = False
        room_serviceflag:bool = False
        hbill_date:date = None
        Pickup_table = Queasy
        Orderbill = Queasy
        B_orderbill = Queasy
        Orderbill_line = Queasy
        B_orderbill_line = Queasy
        Paygateway_session = Queasy
        B_pg_session = Queasy
        Selforder_session = Queasy
        Genparamso = Queasy
        Buff_hbill = H_bill

        for genparamso in db_session.query(Genparamso).filter(
                (Genparamso.key == 222) &  (Genparamso.number1 == 1) &  (Genparamso.betriebsnr == curr_dept)).all():

            if genparamso.number2 == 14:
                dynamic_qr = genparamso.logi1

            if genparamso.number2 == 21:
                room_serviceflag = genparamso.logi1

        if not dynamic_qr:

            pickup_table = db_session.query(Pickup_table).filter(
                    (Pickup_table.key == 225) &  (func.lower(Pickup_table.char1) == "taken_table") &  (Pickup_table.logi1) &  (Pickup_table.logi2 == False) &  (Pickup_table.number1 == curr_dept) &  (Pickup_table.number2 == curr_tischnr)).first()

            if pickup_table:
                sessionid_one = entry(0, pickup_table.char3, "|")

            pickup_table = db_session.query(Pickup_table).filter(
                    (Pickup_table.key == 225) &  (func.lower(Pickup_table.char1) == "taken_table") &  (Pickup_table.logi1) &  (Pickup_table.logi2 == False) &  (Pickup_table.number1 == curr_dept) &  (Pickup_table.number2 == tischnr)).first()

            if pickup_table:
                sessionid_two = entry(0, pickup_table.char3, "|")
        else:

            pickup_table = db_session.query(Pickup_table).filter(
                    (Pickup_table.key == 225) &  (func.lower(Pickup_table.char1) == "taken_table") &  (Pickup_table.logi1) &  (Pickup_table.logi2) &  (Pickup_table.number1 == curr_dept) &  (Pickup_table.number2 == curr_tischnr) &  (len(entry(0, Pickup_table.char3, "|Pickup_table.")) <= 20)).first()

            if pickup_table:
                sessionid_one = entry(0, pickup_table.char3, "|")

            pickup_table = db_session.query(Pickup_table).filter(
                    (Pickup_table.key == 225) &  (func.lower(Pickup_table.char1) == "taken_table") &  (Pickup_table.logi1) &  (Pickup_table.logi2) &  (Pickup_table.number1 == curr_dept) &  (Pickup_table.number2 == tischnr) &  (len(entry(0, Pickup_table.char3, "|Pickup_table.")) <= 20)).first()

            if pickup_table:
                sessionid_two = entry(0, pickup_table.char3, "|")
                mess_str = pickup_table.char2
                for i_str in range(1,num_entries(mess_str, "|")  + 1) :
                    mess_token = entry(i_str - 1, mess_str, "|")
                    mess_keyword = entry(0, mess_token, " == ")
                    mess_value = entry(1, mess_token, " == ")

                    if mess_keyword.lower()  == "NM":
                        guest_name = mess_value

                    if guest_name != "":
                        return

        h_bill_line = db_session.query(H_bill_line).filter(
                (H_bill_line.rechnr == rechnr) &  (H_bill_line.departement == curr_dept)).first()

        if h_bill_line:
            hbill_date = h_bill_line.bill_datum

        orderbill = db_session.query(Orderbill).filter(
                (Orderbill.key == 225) &  (func.lower(Orderbill.char1) == "orderbill") &  (Orderbill.number1 == curr_dept) &  (Orderbill.number2 == curr_tischnr) &  (Orderbill.char3 == sessionid_one) &  (Orderbill.logi1) &  (Orderbill.logi3)).first()

        if not orderbill:

            return

        selforder_session = db_session.query(Selforder_session).filter(
                    (Selforder_session.key == 230) &  (Selforder_session.number1 == curr_dept) &  (Selforder_session.number2 == curr_tischnr) &  (Selforder_session.char1 == sessionid_one) &  (Selforder_session.logi1 == False)).first()

        if selforder_session:

            for orderbill in db_session.query(Orderbill).filter(
                        (Orderbill.key == 225) &  (func.lower(Orderbill.char1) == "orderbill") &  (Orderbill.number1 == curr_dept) &  (Orderbill.number2 == curr_tischnr) &  (Orderbill.char3 == sessionid_one) &  (Orderbill.logi1) &  (Orderbill.logi3)).all():
                mess_str = orderbill.char2
                for i_str in range(1,num_entries(mess_str, "|")  + 1) :
                    mess_token = entry(i_str - 1, mess_str, "|")
                    mess_keyword = entry(0, mess_token, " == ")
                    mess_value = entry(1, mess_token, " == ")

                    if mess_keyword.lower()  == "BL":
                        validate_rechnr = to_int(mess_value)

                    if validate_rechnr != 0:
                        break

                b_orderbill = db_session.query(B_orderbill).filter(
                            (B_orderbill._recid == orderbill._recid)).first()

                if b_orderbill:

                    b_orderbill = db_session.query(B_orderbill).first()
                    b_orderbill.number1 = curr_dept
                    b_orderbill.number2 = tischnr
                    b_orderbill.char3 = sessionid_two

                    if not dynamic_qr:
                        b_orderbill.char2 = entry(1, b_orderbill.char2, "|", "NM = GuestTable" + to_string(tischnr))
                    else:
                        b_orderbill.char2 = entry(1, b_orderbill.char2, "|", "NM = " + guest_name)

                    b_orderbill = db_session.query(B_orderbill).first()

            for orderbill_line in db_session.query(Orderbill_line).filter(
                        (Orderbill_line.key == 225) &  (func.lower(Orderbill_line.char1) == "orderbill_line") &  (Orderbill_line.number2 == curr_tischnr) &  (entry(0, Orderbill_line.char2, "|Orderbill_line.Orderbill_line.") == to_string(curr_dept)) &  (entry(3, Orderbill_line.char2, "|Orderbill_line.Orderbill_line.") == sessionid_one)).all():

                b_orderbill_line = db_session.query(B_orderbill_line).filter(
                            (B_orderbill_line._recid == orderbill_line._recid)).first()

                if b_orderbill_line:

                    b_orderbill_line = db_session.query(B_orderbill_line).first()
                    b_orderbill_line.number2 = tischnr
                    b_orderbill_line.char2 = entry(0, b_orderbill_line.char2, "|", to_string(curr_dept))
                    b_orderbill_line.char2 = entry(1, b_orderbill_line.char2, "|", to_string(tischnr))
                    b_orderbill_line.char2 = entry(3, b_orderbill_line.char2, "|", sessionid_two)

                    b_orderbill_line = db_session.query(B_orderbill_line).first()

            if dynamic_qr:
                selforder_session.logi1 = True

                pickup_table = db_session.query(Pickup_table).filter(
                            (Pickup_table.key == 225) &  (func.lower(Pickup_table.char1) == "taken_table") &  (Pickup_table.logi1) &  (Pickup_table.logi2) &  (Pickup_table.number1 == curr_dept) &  (Pickup_table.number2 == curr_tischnr) &  (entry(0, Pickup_table.char3, "|Pickup_table.") == sessionid_one)).first()

                if pickup_table:

                    pickup_table = db_session.query(Pickup_table).first()
                    pickup_table.char3 = entry(0, pickup_table.char3, "|", sessionid_one + "T" + replace_str(to_string(get_current_date()) , "/", "") + replace_str(to_string(get_current_time_in_seconds(), "HH:MM") , ":", ""))

                    pickup_table = db_session.query(Pickup_table).first()

            paygateway_session = db_session.query(Paygateway_session).filter(
                        (Paygateway_session.key == 223) &  (Paygateway_session.number1 == curr_dept) &  (Paygateway_session.char3 == sessionid_one) &  (Paygateway_session.betriebsnr == rechnr)).first()

            if paygateway_session:
                bill_no = paygateway_session.betriebsnr

                b_pg_session = db_session.query(B_pg_session).filter(
                            (B_pg_session.key == 223) &  (B_pg_session.number1 == curr_dept) &  (B_pg_session.char3 == sessionid_two)).first()

                if b_pg_session:

                    b_pg_session = db_session.query(B_pg_session).first()
                    b_pg_session.betriebsnr = bill_no

                    b_pg_session = db_session.query(B_pg_session).first()

                paygateway_session = db_session.query(Paygateway_session).first()
                paygateway_session.betriebsnr = 0

                paygateway_session = db_session.query(Paygateway_session).first()

            selforder_session = db_session.query(Selforder_session).first()


    def selforder_moveto_occtable():

        nonlocal bill_date, printed, balance, balance_foreign, fl_code, fl_code1, fl_code2, t_h_bill_list, flag_move, old_billno, curr_recid, active_deposit, h_bill, queasy, htparam, h_bill_line, tisch, h_journal
        nonlocal buf_bill, buffq251, buffq33, h_bill1, qbuff, hbline, pickup_table, orderbill, b_orderbill, orderbill_line, b_orderbill_line, paygateway_session, b_pg_session, selforder_session, genparamso, buff_hbill


        nonlocal t_h_bill, buf_bill, buffq251, buffq33, h_bill1, qbuff, hbline, pickup_table, orderbill, b_orderbill, orderbill_line, b_orderbill_line, paygateway_session, b_pg_session, selforder_session, genparamso, buff_hbill
        nonlocal t_h_bill_list

        sessionid_one:str = ""
        sessionid_two:str = ""
        mess_str:str = ""
        mess_token:str = ""
        mess_keyword:str = ""
        mess_value:str = ""
        guest_name:str = ""
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
        Pickup_table = Queasy
        Orderbill = Queasy
        B_orderbill = Queasy
        Orderbill_line = Queasy
        B_orderbill_line = Queasy
        Paygateway_session = Queasy
        B_pg_session = Queasy
        Selforder_session = Queasy
        Genparamso = Queasy
        Buff_hbill = H_bill

        for genparamso in db_session.query(Genparamso).filter(
                (Genparamso.key == 222) &  (Genparamso.number1 == 1) &  (Genparamso.betriebsnr == curr_dept)).all():

            if genparamso.number2 == 14:
                dynamic_qr = genparamso.logi1

            if genparamso.number2 == 21:
                room_serviceflag = genparamso.logi1

        if not dynamic_qr:

            pickup_table = db_session.query(Pickup_table).filter(
                    (Pickup_table.key == 225) &  (func.lower(Pickup_table.char1) == "taken_table") &  (Pickup_table.logi1) &  (Pickup_table.logi2 == False) &  (Pickup_table.number1 == curr_dept) &  (Pickup_table.number2 == curr_tischnr)).first()

            if pickup_table:
                sessionid_one = entry(0, pickup_table.char3, "|")

            pickup_table = db_session.query(Pickup_table).filter(
                    (Pickup_table.key == 225) &  (func.lower(Pickup_table.char1) == "taken_table") &  (Pickup_table.logi1) &  (Pickup_table.logi2 == False) &  (Pickup_table.number1 == curr_dept) &  (Pickup_table.number2 == tischnr)).first()

            if pickup_table:
                sessionid_two = entry(0, pickup_table.char3, "|")
        else:

            pickup_table = db_session.query(Pickup_table).filter(
                    (Pickup_table.key == 225) &  (func.lower(Pickup_table.char1) == "taken_table") &  (Pickup_table.logi1) &  (Pickup_table.logi2) &  (Pickup_table.number1 == curr_dept) &  (Pickup_table.number2 == curr_tischnr) &  (len(entry(0, Pickup_table.char3, "|Pickup_table.")) <= 20)).first()

            if pickup_table:
                sessionid_one = entry(0, pickup_table.char3, "|")

            pickup_table = db_session.query(Pickup_table).filter(
                    (Pickup_table.key == 225) &  (func.lower(Pickup_table.char1) == "taken_table") &  (Pickup_table.logi1) &  (Pickup_table.logi2) &  (Pickup_table.number1 == curr_dept) &  (Pickup_table.number2 == tischnr) &  (len(entry(0, Pickup_table.char3, "|Pickup_table.")) <= 20)).first()

            if pickup_table:
                sessionid_two = entry(0, pickup_table.char3, "|")
                mess_str = pickup_table.char2
                for i_str in range(1,num_entries(mess_str, "|")  + 1) :
                    mess_token = entry(i_str - 1, mess_str, "|")
                    mess_keyword = entry(0, mess_token, " == ")
                    mess_value = entry(1, mess_token, " == ")

                    if mess_keyword.lower()  == "NM":
                        guest_name = mess_value

                    if guest_name != "":
                        return

        h_bill = db_session.query(H_bill).filter(
                (H_bill._recid == bilrecid)).first()

        if h_bill:

            h_bill_line = db_session.query(H_bill_line).filter(
                    (H_bill_line.rechnr == rechnr) &  (H_bill_line.departement == curr_dept)).first()

            if h_bill_line:
                hbill_date = h_bill_line.bill_datum

        orderbill = db_session.query(Orderbill).filter(
                (Orderbill.key == 225) &  (func.lower(Orderbill.char1) == "orderbill") &  (Orderbill.number1 == curr_dept) &  (Orderbill.number2 == curr_tischnr) &  (Orderbill.char3 == sessionid_one) &  (Orderbill.logi1) &  (Orderbill.logi3)).first()

        if not orderbill:

            return

        selforder_session = db_session.query(Selforder_session).filter(
                    (Selforder_session.key == 230) &  (Selforder_session.number1 == curr_dept) &  (Selforder_session.number2 == curr_tischnr) &  (Selforder_session.char1 == sessionid_one) &  (Selforder_session.logi1 == False)).first()

        if selforder_session:

            buff_hbill = db_session.query(Buff_hbill).filter(
                        (Buff_hbill._recid == bilrecid)).first()

            if buff_hbill:
                new_billno = buff_hbill.rechnr

            for orderbill in db_session.query(Orderbill).filter(
                        (Orderbill.key == 225) &  (func.lower(Orderbill.char1) == "orderbill") &  (Orderbill.number1 == curr_dept) &  (Orderbill.number2 == tischnr) &  (Orderbill.char3 == sessionid_two) &  (Orderbill.logi1) &  (Orderbill.logi3)).all():
                orderbill_counter = orderbill.number3
                break

            for orderbill in db_session.query(Orderbill).filter(
                        (Orderbill.key == 225) &  (func.lower(Orderbill.char1) == "orderbill") &  (Orderbill.number1 == curr_dept) &  (Orderbill.number2 == curr_tischnr) &  (Orderbill.char3 == sessionid_one) &  (Orderbill.logi1) &  (Orderbill.logi3)).all():
                orderbill_counter = orderbill_counter + 1
                mess_str = orderbill.char2
                for i_str in range(1,num_entries(mess_str, "|")  + 1) :
                    mess_token = entry(i_str - 1, mess_str, "|")
                    mess_keyword = entry(0, mess_token, " == ")
                    mess_value = entry(1, mess_token, " == ")

                    if mess_keyword.lower()  == "BL":
                        validate_rechnr = to_int(mess_value)

                    if validate_rechnr != 0:
                        break

                for orderbill_line in db_session.query(Orderbill_line).filter(
                            (Orderbill_line.key == 225) &  (func.lower(Orderbill_line.char1) == "orderbill_line") &  (Orderbill_line.number1 == orderbill.number3) &  (Orderbill_line.number2 == curr_tischnr) &  (entry(0, Orderbill_line.char2, "|Orderbill_line.Orderbill_line.") == to_string(curr_dept)) &  (entry(3, Orderbill_line.char2, "|Orderbill_line.Orderbill_line.") == sessionid_one)).all():

                    b_orderbill_line = db_session.query(B_orderbill_line).filter(
                                (B_orderbill_line._recid == orderbill_line._recid)).first()

                    if b_orderbill_line:

                        b_orderbill_line = db_session.query(B_orderbill_line).first()
                        b_orderbill_line.number1 = orderbill_counter
                        b_orderbill_line.number2 = tischnr
                        b_orderbill_line.char2 = entry(0, b_orderbill_line.char2, "|", to_string(curr_dept))
                        b_orderbill_line.char2 = entry(1, b_orderbill_line.char2, "|", to_string(tischnr))
                        b_orderbill_line.char2 = entry(3, b_orderbill_line.char2, "|", sessionid_two)

                        b_orderbill_line = db_session.query(B_orderbill_line).first()

                b_orderbill = db_session.query(B_orderbill).filter(
                            (B_orderbill._recid == orderbill._recid)).first()

                if b_orderbill:

                    b_orderbill = db_session.query(B_orderbill).first()
                    b_orderbill.number1 = curr_dept
                    b_orderbill.number2 = tischnr
                    b_orderbill.number3 = orderbill_counter
                    b_orderbill.char3 = sessionid_two

                    if num_entries(b_orderbill.char2, "|") >= 8:
                        b_orderbill.betriebsnr = bilrecid
                        b_orderbill.char2 = entry(7, b_orderbill.char2, "|", "BL = " + to_string(new_billno))

                    if not dynamic_qr:
                        b_orderbill.char2 = entry(1, b_orderbill.char2, "|", "NM = GuestTable" + to_string(tischnr))
                    else:
                        b_orderbill.char2 = entry(1, b_orderbill.char2, "|", "NM = " + guest_name)

                    b_orderbill = db_session.query(B_orderbill).first()

            if dynamic_qr:
                selforder_session.logi1 = True

                pickup_table = db_session.query(Pickup_table).filter(
                            (Pickup_table.key == 225) &  (func.lower(Pickup_table.char1) == "taken_table") &  (Pickup_table.logi1) &  (Pickup_table.logi2) &  (Pickup_table.number1 == curr_dept) &  (Pickup_table.number2 == curr_tischnr) &  (entry(0, Pickup_table.char3, "|Pickup_table.") == sessionid_one)).first()

                if pickup_table:

                    pickup_table = db_session.query(Pickup_table).first()
                    pickup_table.char3 = entry(0, pickup_table.char3, "|", sessionid_one + "T" + replace_str(to_string(get_current_date()) , "/", "") + replace_str(to_string(get_current_time_in_seconds(), "HH:MM") , ":", ""))

                    pickup_table = db_session.query(Pickup_table).first()

            paygateway_session = db_session.query(Paygateway_session).filter(
                        (Paygateway_session.key == 223) &  (Paygateway_session.number1 == curr_dept) &  (Paygateway_session.char3 == sessionid_one) &  (Paygateway_session.betriebsnr == old_billno)).first()

            if paygateway_session:

                paygateway_session = db_session.query(Paygateway_session).first()
                paygateway_session.betriebsnr = 0

                paygateway_session = db_session.query(Paygateway_session).first()

            selforder_session = db_session.query(Selforder_session).first()


    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 588)).first()

    if htparam:
        active_deposit = htparam.flogical

    h_bill = db_session.query(H_bill).filter(
            (H_bill._recid == rec_id)).first()

    if h_bill:
        old_billno = h_bill.rechnr

        buf_bill = db_session.query(Buf_bill).filter(
                (Buf_bill.rechnr == rechnr) &  (Buf_bill.departement == curr_dept) &  (Buf_bill.tischnr == curr_tischnr)).first()

        if not buf_bill:
            fl_code = 2

            return generate_output()
    move_table()

    h_bill = db_session.query(H_bill).first()

    if h_bill:
        t_h_bill = T_h_bill()
        t_h_bill_list.append(t_h_bill)

        buffer_copy(h_bill, t_h_bill)
        t_h_bill.rec_id = h_bill._recid

    if flag_move:

        queasy = db_session.query(Queasy).filter(
                (Queasy.key == 230)).first()

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

            buffq251 = db_session.query(Buffq251).filter(
                    (Buffq251.key == 251) &  (Buffq251.number1 == curr_recid)).first()

            if buffq251:

                buffq33 = db_session.query(Buffq33).filter(
                        (Buffq33._recid == buffq251.number2)).first()

                if buffq33:

                    buffq33 = db_session.query(Buffq33).first()
                    buffq33.number2 = tischnr

                    if num_entries(buffq33.char3, ";") <= 3:
                        buffq33.char3 = buffq33.char3 + "Move Table From " + to_string(curr_tischnr) + " to " + to_string(tischnr) + " - UserID " + to_string(curr_waiter)

                    buffq33 = db_session.query(Buffq33).first()


                if bilrecid != 0:

                    buffq251 = db_session.query(Buffq251).first()
                    buffq251.number1 = curr_recid

                    buffq251 = db_session.query(Buffq251).first()


    return generate_output()