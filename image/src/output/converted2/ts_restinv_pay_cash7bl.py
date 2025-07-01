#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from functions.rest_addgastinfo import rest_addgastinfo
from models import Htparam, H_bill, Interface, H_bill_line, H_artikel, Queasy, Tisch, H_umsatz, Artikel

def ts_restinv_pay_cash7bl(rec_id:int, transdate:date, curr_dept:int, disc_art1:int, disc_art2:int, disc_art3:int, kellner_kellner_nr:int):

    prepare_cache ([Htparam, H_bill, Interface, H_bill_line, Queasy, H_umsatz, Artikel])

    bill_date = None
    get_rechnr:int = 0
    get_amount:Decimal = to_decimal("0.0")
    active_deposit:bool = False
    recid_hbill:int = 0
    htparam = h_bill = interface = h_bill_line = h_artikel = queasy = tisch = h_umsatz = artikel = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal bill_date, get_rechnr, get_amount, active_deposit, recid_hbill, htparam, h_bill, interface, h_bill_line, h_artikel, queasy, tisch, h_umsatz, artikel
        nonlocal rec_id, transdate, curr_dept, disc_art1, disc_art2, disc_art3, kellner_kellner_nr

        return {"bill_date": bill_date}

    def fill_cover():

        nonlocal bill_date, get_rechnr, get_amount, active_deposit, recid_hbill, htparam, h_bill, interface, h_bill_line, h_artikel, queasy, tisch, h_umsatz, artikel
        nonlocal rec_id, transdate, curr_dept, disc_art1, disc_art2, disc_art3, kellner_kellner_nr

        f_pax:int = 0
        b_pax:int = 0
        str:string = ""
        h_art1 = None
        tbuff = None
        H_art1 =  create_buffer("H_art1",H_artikel)
        Tbuff =  create_buffer("Tbuff",Tisch)

        tbuff = db_session.query(Tbuff).filter(
                     (Tbuff.tischnr == h_bill.tischnr) & (Tbuff.departement == h_bill.departement)).first()

        if tbuff and tbuff.roomcharge and tbuff.kellner_nr != 0:
            pass
            tbuff.kellner_nr = 0


            pass
            pass
        release_tbplan()

        if h_bill.resnr > 0:
            get_output(rest_addgastinfo(h_bill.departement, h_bill.rechnr, h_bill.resnr, h_bill.reslinnr, 0, transdate))
        pass
        h_bill.kellner_nr = kellner_kellner_nr

        htparam = get_cache (Htparam, {"paramnr": [(eq, 739)]})

        if htparam.flogical:

            if str != "":
                h_bill.service[4] = to_decimal(str)


        pass

        htparam = get_cache (Htparam, {"paramnr": [(eq, 110)]})
        bill_date = htparam.fdate

        if transdate != None:
            bill_date = transdate
        else:

            htparam = get_cache (Htparam, {"paramnr": [(eq, 253)]})

            if htparam.flogical and bill_date < get_current_date():
                bill_date = bill_date + timedelta(days=1)

        h_umsatz = get_cache (H_umsatz, {"artnr": [(eq, 0)],"departement": [(eq, curr_dept)],"betriebsnr": [(eq, curr_dept)],"datum": [(eq, bill_date)]})

        if not h_umsatz:
            h_umsatz = H_umsatz()
            db_session.add(h_umsatz)

            h_umsatz.artnr = 0
            h_umsatz.departement = curr_dept
            h_umsatz.betriebsnr = curr_dept
            h_umsatz.datum = bill_date
        h_umsatz.anzahl = h_umsatz.anzahl + h_bill.belegung

        if h_bill.belegung != 0:

            h_bill_line_obj_list = {}
            for h_bill_line, h_art1, artikel in db_session.query(H_bill_line, H_art1, Artikel).join(H_art1,(H_art1.artnr == H_bill_line.artnr) & (H_art1.departement == H_bill_line.departement) & (H_art1.artart == 0)).join(Artikel,(Artikel.artnr == H_art1.artnrfront) & (Artikel.departement == H_art1.departement)).filter(
                         (H_bill_line.rechnr == h_bill.rechnr) & (H_bill_line.departement == h_bill.departement) & (H_bill_line.artnr != disc_art1) & (H_bill_line.artnr != disc_art2) & (H_bill_line.artnr != disc_art3)).order_by(H_bill_line._recid).all():
                if h_bill_line_obj_list.get(h_bill_line._recid):
                    continue
                else:
                    h_bill_line_obj_list[h_bill_line._recid] = True

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
        h_umsatz.betrag =  to_decimal(h_umsatz.betrag) + to_decimal(f_pax)
        h_umsatz.nettobetrag =  to_decimal(h_umsatz.nettobetrag) + to_decimal(b_pax)
        pass
        pass
        pass


    def release_tbplan():

        nonlocal bill_date, get_rechnr, get_amount, active_deposit, recid_hbill, htparam, h_bill, interface, h_bill_line, h_artikel, queasy, tisch, h_umsatz, artikel
        nonlocal rec_id, transdate, curr_dept, disc_art1, disc_art2, disc_art3, kellner_kellner_nr

        queasy = get_cache (Queasy, {"key": [(eq, 31)],"number1": [(eq, h_bill.departement)],"number2": [(eq, h_bill.tischnr)]})

        if queasy:
            pass
            queasy.number3 = 0
            queasy.date1 = None


            pass
            pass


    def update_selforder():

        nonlocal bill_date, get_rechnr, get_amount, active_deposit, recid_hbill, htparam, h_bill, interface, h_bill_line, h_artikel, queasy, tisch, h_umsatz, artikel
        nonlocal rec_id, transdate, curr_dept, disc_art1, disc_art2, disc_art3, kellner_kellner_nr

        paramqsy = None
        searchbill = None
        genparamso = None
        orderbill = None
        orderbilline = None
        orderbill_close = None
        pickup_table = None
        qpayment_gateway = None
        found_bill:int = 0
        session_parameter:string = ""
        mess_str:string = ""
        i_str:int = 0
        mess_token:string = ""
        mess_keyword:string = ""
        mess_value:string = ""
        dynamic_qr:bool = False
        room_serviceflag:bool = False
        Paramqsy =  create_buffer("Paramqsy",Queasy)
        Searchbill =  create_buffer("Searchbill",Queasy)
        Genparamso =  create_buffer("Genparamso",Queasy)
        Orderbill =  create_buffer("Orderbill",Queasy)
        Orderbilline =  create_buffer("Orderbilline",Queasy)
        Orderbill_close =  create_buffer("Orderbill_close",Queasy)
        Pickup_table =  create_buffer("Pickup_table",Queasy)
        Qpayment_gateway =  create_buffer("Qpayment_gateway",Queasy)

        for genparamso in db_session.query(Genparamso).filter(
                 (Genparamso.key == 222) & (Genparamso.number1 == 1) & (Genparamso.betriebsnr == curr_dept)).order_by(Genparamso._recid).all():

            if genparamso.number2 == 14:
                dynamic_qr = genparamso.logi1

            if genparamso.number2 == 21:
                room_serviceflag = genparamso.logi1

        for searchbill in db_session.query(Searchbill).filter(
                 (Searchbill.key == 225) & (Searchbill.number1 == curr_dept) & (Searchbill.char1 == ("orderbill").lower())).order_by(Searchbill._recid).yield_per(100):
            mess_str = searchbill.char2
            for i_str in range(1,num_entries(mess_str, "|")  + 1) :
                mess_token = entry(i_str - 1, mess_str, "|")
                mess_keyword = entry(0, mess_token, "=")
                mess_value = entry(1, mess_token, "=")

                if mess_keyword.lower()  == ("BL").lower() :
                    found_bill = to_int(mess_value)
                    break

            if found_bill == get_rechnr:
                session_parameter = searchbill.char3
                break

        paramqsy = get_cache (Queasy, {"key": [(eq, 230)],"char1": [(eq, session_parameter)]})

        if paramqsy:
            pass
            paramqsy.betriebsnr = get_rechnr

            if dynamic_qr:

                pickup_table = db_session.query(Pickup_table).filter(
                             (Pickup_table.key == 225) & (Pickup_table.char1 == ("taken-table").lower()) & (Pickup_table.number1 == curr_dept) & (Pickup_table.logi1) & (Pickup_table.logi2) & (Pickup_table.number2 == paramqsy.number2) & (entry(0, Pickup_table.char3, "|") == (session_parameter).lower())).first()

                if pickup_table:
                    pass
                    pickup_table.char3 = entry(0, pickup_table.char3, "|", session_parameter + "T" + replace_str(to_string(get_current_date()) , "/", "") + replace_str(to_string(get_current_time_in_seconds(), "HH:MM") , ":", ""))


                    pass
                    pass

            orderbill = get_cache (Queasy, {"key": [(eq, 225)],"char1": [(eq, "orderbill")],"char3": [(eq, session_parameter)],"logi1": [(eq, True)],"logi3": [(eq, True)]})

            if orderbill:
                pass
                orderbill.deci1 =  to_decimal(get_amount)
                orderbill.logi2 = False
                orderbill.char3 = session_parameter + "T" + replace_str(to_string(get_current_date()) , "/", "") + replace_str(to_string(get_current_time_in_seconds(), "HH:MM") , ":", "")
                orderbill.logi1 = False
                pass

                orderbill_close = get_cache (Queasy, {"key": [(eq, 225)],"char1": [(eq, "orderbill")],"char3": [(eq, session_parameter)],"logi1": [(eq, True)],"logi3": [(eq, True)]})
                while None != orderbill_close:
                    pass
                    orderbill_close.char3 = session_parameter + "T" + replace_str(to_string(get_current_date()) , "/", "") + replace_str(to_string(get_current_time_in_seconds(), "HH:MM") , ":", "")
                    orderbill_close.logi1 = False


                    pass
                    pass

                    curr_recid = orderbill_close._recid
                    orderbill_close = db_session.query(Orderbill_close).filter(
                                 (Orderbill_close.key == 225) & (Orderbill_close.char1 == ("orderbill").lower()) & (Orderbill_close.char3 == (session_parameter).lower()) & (Orderbill_close.logi1) & (Orderbill_close.logi3) & (Orderbill_close._recid > curr_recid)).first()
                pass

            if dynamic_qr:
                paramqsy.logi1 = True
            else:

                if room_serviceflag:
                    paramqsy.char1 = session_parameter + "T" + replace_str(to_string(get_current_date()) , "/", "") + replace_str(to_string(get_current_time_in_seconds(), "HH:MM") , ":", "")
                    paramqsy.char3 = paramqsy.char3 + "|BL=" + to_string(get_rechnr)
                    paramqsy.logi1 = True


                else:
                    queasy = Queasy()
                    db_session.add(queasy)

                    buffer_copy(paramqsy, queasy)
                    queasy.char1 = session_parameter + "T" + replace_str(to_string(get_current_date()) , "/", "") + replace_str(to_string(get_current_time_in_seconds(), "HH:MM") , ":", "")
                    queasy.betriebsnr = 1
                    queasy.logi1 = True

                orderbilline = db_session.query(Orderbilline).filter(
                             (Orderbilline.key == 225) & (Orderbilline.char1 == ("orderbill-line").lower()) & (entry(3, Orderbilline.char2, "|") == (session_parameter).lower())).first()
                while None != orderbilline:
                    pass

                    if orderbilline.logi2 and orderbilline.logi3:
                        orderbilline.char2 = entry(0, orderbilline.char2, "|") + "|" + entry(1, orderbilline.char2, "|") + "|" + entry(2, orderbilline.char2, "|") + "|" + session_parameter + "T" + replace_str(to_string(get_current_date()) , "/", "") + replace_str(to_string(get_current_time_in_seconds(), "HH:MM") , ":", "")
                    else:

                        if num_entries(orderbilline.char3, "|") > 8 and entry(8, orderbilline.char3, "|") != "":
                            orderbilline.char2 = entry(0, orderbilline.char2, "|") + "|" + entry(1, orderbilline.char2, "|") + "|" + entry(2, orderbilline.char2, "|") + "|" + session_parameter + "T" + replace_str(to_string(get_current_date()) , "/", "") + replace_str(to_string(get_current_time_in_seconds(), "HH:MM") , ":", "")
                    pass
                    pass

                    curr_recid = orderbilline._recid
                    orderbilline = db_session.query(Orderbilline).filter(
                                 (Orderbilline.key == 225) & (Orderbilline.char1 == ("orderbill-line").lower()) & (entry(3, Orderbilline.char2, "|") == (session_parameter).lower()) & (Orderbilline._recid > curr_recid)).first()

            qpayment_gateway = get_cache (Queasy, {"key": [(eq, 223)],"char3": [(eq, session_parameter)],"betriebsnr": [(eq, get_rechnr)]})

            if qpayment_gateway:
                pass
                qpayment_gateway.betriebsnr = 0
                pass
                pass
            pass
            pass


    def remove_rsv_table():

        nonlocal bill_date, get_rechnr, get_amount, active_deposit, recid_hbill, htparam, h_bill, interface, h_bill_line, h_artikel, queasy, tisch, h_umsatz, artikel
        nonlocal rec_id, transdate, curr_dept, disc_art1, disc_art2, disc_art3, kellner_kellner_nr

        recid_q33:int = 0
        buffq33 = None
        Buffq33 =  create_buffer("Buffq33",Queasy)

        queasy = get_cache (Queasy, {"key": [(eq, 251)],"number1": [(eq, recid_hbill)]})

        if queasy:
            recid_q33 = queasy.number2

            buffq33 = get_cache (Queasy, {"_recid": [(eq, recid_q33)]})

            if buffq33:
                pass
                buffq33.betriebsnr = 1


                pass
                pass

    htparam = get_cache (Htparam, {"paramnr": [(eq, 588)]})

    if htparam:
        active_deposit = htparam.flogical

    h_bill = get_cache (H_bill, {"_recid": [(eq, rec_id)]})
    fill_cover()

    h_bill = get_cache (H_bill, {"_recid": [(eq, rec_id)]})
    pass
    h_bill.flag = 1
    interface = Interface()
    db_session.add(interface)

    interface.key = 38
    interface.action = True
    interface.nebenstelle = ""
    interface.parameters = "close-bill"
    interface.intfield = h_bill.rechnr
    interface.decfield =  to_decimal(h_bill.departement)
    interface.int_time = get_current_time_in_seconds()
    interface.intdate = get_current_date()
    interface.resnr = h_bill.resnr
    interface.reslinnr = h_bill.reslinnr


    pass
    pass
    pass
    get_rechnr = h_bill.rechnr

    for h_bill_line in db_session.query(H_bill_line).filter(
                 (H_bill_line.departemen == h_bill.departemen) & (H_bill_line.rechnr == h_bill.rechnr) & (H_bill_line.betrag < 0)).order_by(H_bill_line._recid).all():

        h_artikel = get_cache (H_artikel, {"departement": [(eq, h_bill_line.departemen)],"artnr": [(eq, h_bill_line.artnr)],"artart": [(ne, 0)]})

        if h_artikel:
            get_amount =  to_decimal(get_amount) + to_decimal(h_bill_line.betrag)

    queasy = get_cache (Queasy, {"key": [(eq, 230)]})

    if queasy:
        update_selforder()
    recid_hbill = h_bill._recid

    if active_deposit:
        remove_rsv_table()
    pass

    return generate_output()