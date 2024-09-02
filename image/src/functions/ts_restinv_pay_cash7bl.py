from functions.additional_functions import *
import decimal
from datetime import date
from functions.rest_addgastinfo import rest_addgastinfo
from functions.ts_voucherui import ts_voucherui
from sqlalchemy import func
from models import Htparam, H_bill, Interface, H_bill_line, H_artikel, Queasy, Tisch, H_umsatz, Artikel

def ts_restinv_pay_cash7bl(rec_id:int, transdate:date, curr_dept:int, disc_art1:int, disc_art2:int, disc_art3:int, kellner_kellner_nr:int):
    bill_date = None
    get_rechnr:int = 0
    get_amount:decimal = 0
    active_deposit:bool = False
    recid_hbill:int = 0
    htparam = h_bill = interface = h_bill_line = h_artikel = queasy = tisch = h_umsatz = artikel = None

    h_art1 = tbuff = paramqsy = searchbill = genparamso = orderbill = orderbilline = orderbill_close = pickup_table = qpayment_gateway = buffq33 = None

    H_art1 = H_artikel
    Tbuff = Tisch
    Paramqsy = Queasy
    Searchbill = Queasy
    Genparamso = Queasy
    Orderbill = Queasy
    Orderbilline = Queasy
    Orderbill_close = Queasy
    Pickup_table = Queasy
    Qpayment_gateway = Queasy
    Buffq33 = Queasy

    db_session = local_storage.db_session

    def generate_output():
        nonlocal bill_date, get_rechnr, get_amount, active_deposit, recid_hbill, htparam, h_bill, interface, h_bill_line, h_artikel, queasy, tisch, h_umsatz, artikel
        nonlocal h_art1, tbuff, paramqsy, searchbill, genparamso, orderbill, orderbilline, orderbill_close, pickup_table, qpayment_gateway, buffq33


        nonlocal h_art1, tbuff, paramqsy, searchbill, genparamso, orderbill, orderbilline, orderbill_close, pickup_table, qpayment_gateway, buffq33
        return {"bill_date": bill_date}

    def fill_cover():

        nonlocal bill_date, get_rechnr, get_amount, active_deposit, recid_hbill, htparam, h_bill, interface, h_bill_line, h_artikel, queasy, tisch, h_umsatz, artikel
        nonlocal h_art1, tbuff, paramqsy, searchbill, genparamso, orderbill, orderbilline, orderbill_close, pickup_table, qpayment_gateway, buffq33


        nonlocal h_art1, tbuff, paramqsy, searchbill, genparamso, orderbill, orderbilline, orderbill_close, pickup_table, qpayment_gateway, buffq33

        f_pax:int = 0
        b_pax:int = 0
        str:str = ""
        H_art1 = H_artikel
        Tbuff = Tisch

        tbuff = db_session.query(Tbuff).filter(
                    (Tbuff.tischnr == h_bill.tischnr) &  (Tbuff.departement == h_bill.departement)).first()

        if tbuff and tbuff.roomcharge and tbuff.kellner_nr != 0:

            tbuff = db_session.query(Tbuff).first()
            tbuff.kellner_nr = 0

            tbuff = db_session.query(Tbuff).first()
        release_tbplan()

        if h_bill.resnr > 0:
            get_output(rest_addgastinfo(h_bill.departement, h_bill.rechnr, h_bill.resnr, h_bill.reslinnr, 0, transdate))

        h_bill = db_session.query(H_bill).first()
        h_bill.kellner_nr = kellner_kellner_nr

        htparam = db_session.query(Htparam).filter(
                    (Htparam.paramnr == 739)).first()

        if htparam.flogical:
            str = get_output(ts_voucherui())

            if str != "":
                h_bill.service[4] = decimal.Decimal(str)

        h_bill = db_session.query(H_bill).first()

        htparam = db_session.query(Htparam).filter(
                    (Htparam.paramnr == 110)).first()
        bill_date = htparam.fdate

        if transdate != None:
            bill_date = transdate
        else:

            htparam = db_session.query(Htparam).filter(
                        (Htparam.paramnr == 253)).first()

            if htparam.flogical and bill_date < get_current_date():
                bill_date = bill_date + 1

        h_umsatz = db_session.query(H_umsatz).filter(
                    (H_umsatz.artnr == 0) &  (H_umsatz.departement == curr_dept) &  (H_umsatz.betriebsnr == curr_dept) &  (H_umsatz.datum == bill_date)).first()

        if not h_umsatz:
            h_umsatz = H_umsatz()
            db_session.add(h_umsatz)

            h_umsatz.artnr = 0
            h_umsatz.departement = curr_dept
            h_umsatz.betriebsnr = curr_dept
            h_umsatz.datum = bill_date
        h_umsatz.anzahl = h_umsatz.anzahl + h_bill.belegung

        if h_bill.belegung != 0:

            h_bill_line_obj_list = []
            for h_bill_line, h_art1, artikel in db_session.query(H_bill_line, H_art1, Artikel).join(H_art1,(H_art1.artnr == H_bill_line.artnr) &  (H_art1.departement == H_bill_line.departement) &  (H_art1.artart == 0)).join(Artikel,(Artikel.artnr == h_art1.artnrfront) &  (Artikel.departement == h_art1.departement)).filter(
                        (H_bill_line.rechnr == h_bill.rechnr) &  (H_bill_line.departement == h_bill.departement) &  (H_bill_line.artnr != disc_art1) &  (H_bill_line.artnr != disc_art2) &  (H_bill_line.artnr != disc_art3)).all():
                if h_bill_line._recid in h_bill_line_obj_list:
                    continue
                else:
                    h_bill_line_obj_list.append(h_bill_line._recid)

                if artikel.umsatzart == 3 or artikel.umsatzart == 5:
                    f_pax = f_pax + h_bill_line.anzahl

                elif artikel.umsatzart == 6:
                    b_pax = b_pax + h_bill_line.anzahl


        if h_bill.belegung > 0:

            if f_pax > h_bill.belegung:
                f_pax = h_bill.belegung

            if b_pax > h_bill.belegung:
                b_pax = h_bill.belegung

        elif h_bill.belegung < 0:

            if f_pax < h_bill.belegung:
                f_pax = h_bill.belegung

            if b_pax < h_bill.belegung:
                b_pax = h_bill.belegung
        h_umsatz.betrag = h_umsatz.betrag + f_pax
        h_umsatz.nettobetrag = h_umsatz.nettobetrag + b_pax

        h_umsatz = db_session.query(H_umsatz).first()

    def release_tbplan():

        nonlocal bill_date, get_rechnr, get_amount, active_deposit, recid_hbill, htparam, h_bill, interface, h_bill_line, h_artikel, queasy, tisch, h_umsatz, artikel
        nonlocal h_art1, tbuff, paramqsy, searchbill, genparamso, orderbill, orderbilline, orderbill_close, pickup_table, qpayment_gateway, buffq33


        nonlocal h_art1, tbuff, paramqsy, searchbill, genparamso, orderbill, orderbilline, orderbill_close, pickup_table, qpayment_gateway, buffq33

        queasy = db_session.query(Queasy).filter(
                (Queasy.key == 31) &  (Queasy.number1 == h_bill.departement) &  (Queasy.number2 == h_bill.tischnr)).first()

        if queasy:

            queasy = db_session.query(Queasy).first()
            queasy.number3 = 0
            queasy.date1 = None

            queasy = db_session.query(Queasy).first()


    def update_selforder():

        nonlocal bill_date, get_rechnr, get_amount, active_deposit, recid_hbill, htparam, h_bill, interface, h_bill_line, h_artikel, queasy, tisch, h_umsatz, artikel
        nonlocal h_art1, tbuff, paramqsy, searchbill, genparamso, orderbill, orderbilline, orderbill_close, pickup_table, qpayment_gateway, buffq33


        nonlocal h_art1, tbuff, paramqsy, searchbill, genparamso, orderbill, orderbilline, orderbill_close, pickup_table, qpayment_gateway, buffq33

        found_bill:int = 0
        session_parameter:str = ""
        mess_str:str = ""
        i_str:int = 0
        mess_token:str = ""
        mess_keyword:str = ""
        mess_value:str = ""
        dynamic_qr:bool = False
        room_serviceflag:bool = False
        Paramqsy = Queasy
        Searchbill = Queasy
        Genparamso = Queasy
        Orderbill = Queasy
        Orderbilline = Queasy
        Orderbill_close = Queasy
        Pickup_table = Queasy
        Qpayment_gateway = Queasy

        for genparamso in db_session.query(Genparamso).filter(
                (Genparamso.key == 222) &  (Genparamso.number1 == 1) &  (Genparamso.betriebsnr == curr_dept)).all():

            if genparamso.number2 == 14:
                dynamic_qr = genparamso.logi1

            if genparamso.number2 == 21:
                room_serviceflag = genparamso.logi1

        for searchbill in db_session.query(Searchbill).filter(
                (Searchbill.key == 225) &  (Searchbill.number1 == curr_dept) &  (func.lower(Searchbill.char1) == "orderbill")).all():
            mess_str = searchbill.char2
            for i_str in range(1,num_entries(mess_str, "|")  + 1) :
                mess_token = entry(i_str - 1, mess_str, "|")
                mess_keyword = entry(0, mess_token, " == ")
                mess_value = entry(1, mess_token, " == ")

                if mess_keyword.lower()  == "BL":
                    found_bill = to_int(mess_value)
                    break

            if found_bill == get_rechnr:
                session_parameter = searchbill.char3
                break

        paramqsy = db_session.query(Paramqsy).filter(
                    (Paramqsy.key == 230) &  (func.lower(Paramqsy.char1) == (session_parameter).lower())).first()

        if paramqsy:
            paramqsy.betriebsnr = get_rechnr

            if dynamic_qr:

                pickup_table = db_session.query(Pickup_table).filter(
                            (Pickup_table.key == 225) &  (func.lower(Pickup_table.char1) == "taken_table") &  (Pickup_table.number1 == curr_dept) &  (Pickup_table.logi1) &  (Pickup_table.logi2) &  (Pickup_table.number2 == paramqsy.number2) &  (entry(0, Pickup_table.char3, "|Pickup_table.") == (session_parameter).lower())).first()

                if pickup_table:
                    pickup_table.char3 = entry(0, pickup_table.char3, "|", session_parameter + "T" + replace_str(to_string(get_current_date()) , "/", "") + replace_str(to_string(get_current_time_in_seconds(), "HH:MM") , ":", ""))

                    pickup_table = db_session.query(Pickup_table).first()

            orderbill = db_session.query(Orderbill).filter(
                        (Orderbill.key == 225) &  (func.lower(Orderbill.char1) == "orderbill") &  (func.lower(Orderbill.char3) == (session_parameter).lower())).first()

            if orderbill:
                orderbill.deci1 = get_amount
                orderbill.logi2 = False
                orderbill.char3 = session_parameter + "T" + replace_str(to_string(get_current_date()) , "/", "") + replace_str(to_string(get_current_time_in_seconds(), "HH:MM") , ":", "")
                orderbill.logi1 = False

                for orderbill_close in db_session.query(Orderbill_close).filter(
                            (Orderbill_close.key == 225) &  (func.lower(Orderbill_close.char1) == "orderbill") &  (func.lower(Orderbill_close.char3) == (session_parameter).lower()) &  (Orderbill_close.logi1)).all():
                    orderbill_close.char3 = session_parameter + "T" + replace_str(to_string(get_current_date()) , "/", "") + replace_str(to_string(get_current_time_in_seconds(), "HH:MM") , ":", "")
                    orderbill_close.logi1 = False

            if dynamic_qr:
                paramqsy.logi1 = True
            else:

                if room_serviceflag:
                    paramqsy.char1 = session_parameter + "T" + replace_str(to_string(get_current_date()) , "/", "") + replace_str(to_string(get_current_time_in_seconds(), "HH:MM") , ":", "")
                    paramqsy.char3 = paramqsy.char3 + "|BL == " + to_string(get_rechnr)
                    paramqsy.logi1 = True


                else:
                    queasy = Queasy()
                    db_session.add(queasy)

                    buffer_copy(paramqsy, queasy)
                    queasy.char1 = session_parameter + "T" + replace_str(to_string(get_current_date()) , "/", "") + replace_str(to_string(get_current_time_in_seconds(), "HH:MM") , ":", "")
                    queasy.betriebsnr = 1
                    queasy.logi1 = True

                for orderbilline in db_session.query(Orderbilline).filter(
                            (Orderbilline.key == 225) &  (func.lower(Orderbilline.char1) == "orderbill_line") &  (entry(3, Orderbilline.char2, "|Orderbilline.") == (session_parameter).lower())).all():
                    orderbilline.char2 = entry(0, orderbilline.char2, "|") + "|" + entry(1, orderbilline.char2, "|") + "|" + entry(2, orderbilline.char2, "|") + "|" + session_parameter + "T" + replace_str(to_string(get_current_date()) , "/", "") + replace_str(to_string(get_current_time_in_seconds(), "HH:MM") , ":", "")

            qpayment_gateway = db_session.query(Qpayment_gateway).filter(
                        (Qpayment_gateway.key == 223) &  (func.lower(Qpayment_gateway.char3) == (session_parameter).lower()) &  (Qpayment_gateway.betriebsnr == get_rechnr)).first()

            if qpayment_gateway:
                qpayment_gateway.betriebsnr = 0

                qpayment_gateway = db_session.query(Qpayment_gateway).first()

            paramqsy = db_session.query(Paramqsy).first()


    def remove_rsv_table():

        nonlocal bill_date, get_rechnr, get_amount, active_deposit, recid_hbill, htparam, h_bill, interface, h_bill_line, h_artikel, queasy, tisch, h_umsatz, artikel
        nonlocal h_art1, tbuff, paramqsy, searchbill, genparamso, orderbill, orderbilline, orderbill_close, pickup_table, qpayment_gateway, buffq33


        nonlocal h_art1, tbuff, paramqsy, searchbill, genparamso, orderbill, orderbilline, orderbill_close, pickup_table, qpayment_gateway, buffq33

        recid_q33:int = 0
        Buffq33 = Queasy

        queasy = db_session.query(Queasy).filter(
                (Queasy.key == 251) &  (Queasy.number1 == recid_hbill)).first()

        if queasy:
            recid_q33 = queasy.number2

            buffq33 = db_session.query(Buffq33).filter(
                    (Buffq33._recid == recid_q33)).first()

            if buffq33:

                buffq33 = db_session.query(Buffq33).first()
                buffq33.betriebsnr = 1

                buffq33 = db_session.query(Buffq33).first()

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 588)).first()

    if htparam:
        active_deposit = htparam.flogical

    h_bill = db_session.query(H_bill).filter(
            (H_bill._recid == rec_id)).first()
    fill_cover()

    h_bill = db_session.query(H_bill).first()
    h_bill.flag = 1
    interface = Interface()
    db_session.add(interface)

    interface.key = 38
    interface.action = True
    interface.nebenstelle = ""
    interface.parameters = "close_bill"
    interface.intfield = h_bill.rechnr
    interface.decfield = h_bill.departement
    interface.int_time = get_current_time_in_seconds()
    interface.intdate = get_current_date()
    interface.resnr = h_bill.resnr
    interface.reslinnr = h_bill.reslinnr

    interface = db_session.query(Interface).first()


    h_bill = db_session.query(H_bill).first()
    get_rechnr = h_bill.rechnr

    for h_bill_line in db_session.query(H_bill_line).filter(
                (H_bill_line.departemen == h_bill.departemen) &  (H_bill_line.rechnr == h_bill.rechnr) &  (H_bill_line.betrag < 0)).all():

        h_artikel = db_session.query(H_artikel).filter(
                    (H_artikel.departemen == h_bill_line.departemen) &  (H_artikel.artnr == h_bill_line.artnr) &  (H_artikel.artart != 0)).first()

        if h_artikel:
            get_amount = get_amount + h_bill_line.betrag

    queasy = db_session.query(Queasy).filter(
                (Queasy.key == 230)).first()

    if queasy:
        update_selforder()
    recid_hbill = h_bill._recid

    if active_deposit:
        remove_rsv_table()


    return generate_output()