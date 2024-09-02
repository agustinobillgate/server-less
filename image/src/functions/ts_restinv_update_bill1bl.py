from functions.additional_functions import *
import decimal
from datetime import date
from functions.calc_servtaxesbl import calc_servtaxesbl
from sqlalchemy import func
from models import H_bill, Bill, Htparam, Artikel, Counters, Bill_line, Billjournal, H_bill_line, H_artikel, Queasy, H_journal

def ts_restinv_update_bill1bl(rec_id_h_bill:int, transdate:date, double_currency:bool, exchg_rate:decimal, kellner1_kcredit_nr:int, bilrecid:int, foreign_rate:bool, user_init:str, gname:str, hoga_resnr:int, hoga_reslinnr:int, price_decimal:int, amount:decimal, amount_foreign:decimal):
    bill_date = None
    billart = 0
    qty = 0
    description = ""
    cancel_str = ""
    t_h_bill_list = []
    vat_amount:decimal = 0
    multi_vat:bool = False
    get_rechnr:int = 0
    get_amount:decimal = 0
    curr_dept:int = 0
    active_deposit:bool = False
    h_bill = bill = htparam = artikel = counters = bill_line = billjournal = h_bill_line = h_artikel = queasy = h_journal = None

    t_h_bill = vat_list = hbline = hart = foart = paramqsy = searchbill = genparamso = orderbill = orderbilline = orderbill_close = pickup_table = qpayment_gateway = buffq33 = None

    t_h_bill_list, T_h_bill = create_model_like(H_bill, {"rec_id":int})
    vat_list_list, Vat_list = create_model("Vat_list", {"vatproz":decimal, "vatamt":decimal, "netto":decimal, "betrag":decimal, "fbetrag":decimal})

    Hbline = H_bill_line
    Hart = H_artikel
    Foart = Artikel
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
        nonlocal bill_date, billart, qty, description, cancel_str, t_h_bill_list, vat_amount, multi_vat, get_rechnr, get_amount, curr_dept, active_deposit, h_bill, bill, htparam, artikel, counters, bill_line, billjournal, h_bill_line, h_artikel, queasy, h_journal
        nonlocal hbline, hart, foart, paramqsy, searchbill, genparamso, orderbill, orderbilline, orderbill_close, pickup_table, qpayment_gateway, buffq33


        nonlocal t_h_bill, vat_list, hbline, hart, foart, paramqsy, searchbill, genparamso, orderbill, orderbilline, orderbill_close, pickup_table, qpayment_gateway, buffq33
        nonlocal t_h_bill_list, vat_list_list
        return {"bill_date": bill_date, "billart": billart, "qty": qty, "description": description, "cancel_str": cancel_str, "t-h-bill": t_h_bill_list}

    def cal_vat_amount():

        nonlocal bill_date, billart, qty, description, cancel_str, t_h_bill_list, vat_amount, multi_vat, get_rechnr, get_amount, curr_dept, active_deposit, h_bill, bill, htparam, artikel, counters, bill_line, billjournal, h_bill_line, h_artikel, queasy, h_journal
        nonlocal hbline, hart, foart, paramqsy, searchbill, genparamso, orderbill, orderbilline, orderbill_close, pickup_table, qpayment_gateway, buffq33


        nonlocal t_h_bill, vat_list, hbline, hart, foart, paramqsy, searchbill, genparamso, orderbill, orderbilline, orderbill_close, pickup_table, qpayment_gateway, buffq33
        nonlocal t_h_bill_list, vat_list_list

        mwst = 0
        h_service:decimal = 0
        h_mwst:decimal = 0
        vat2:decimal = 0
        fact:decimal = 0
        fact1:decimal = 0
        qty:decimal = 0
        unit_price:decimal = 0
        amount:decimal = 0
        incl_mwst:bool = False
        multi_vat:bool = False
        curr_vat:decimal = 0
        disc_art1:int = 0

        def generate_inner_output():
            return mwst
        Hbline = H_bill_line
        Hart = H_artikel

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 134)).first()
        incl_mwst = htparam.flogical

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 557)).first()
        disc_art1 = htparam.finteger

        hbline_obj_list = []
        for hbline, hart in db_session.query(Hbline, Hart).join(Hart,(Hart.artnr == Hbline.artnr) &  (Hart.departement == Hbline.departement) &  (Hart.artart == 0)).filter(
                (Hbline.rechnr == h_bill.rechnr) &  (Hbline.departement == h_bill.departement)).all():
            if hbline._recid in hbline_obj_list:
                continue
            else:
                hbline_obj_list.append(hbline._recid)

            if hart.artnr == disc_art1:

                h_journal = db_session.query(H_journal).filter(
                        (H_journal.departement == hbline.departement) &  (H_journal.bill_datum == hbline.bill_datum) &  (H_journal.rechnr == hbline.rechnr) &  (H_journal.artnr == hbline.artnr) &  (H_journal.zeit == hbline.zeit)).first()

                if h_journal:
                    mwst = mwst + h_journal.steuercode / 100
            else:
                h_service = 0
                h_mwst = 0
                fact = 1
                qty = hbline.anzahl

                if qty < 0:
                    qty = - qty

                if incl_mwst:

                    artikel = db_session.query(Artikel).filter(
                            (Artikel.artnr == hart.artnrfront) &  (Artikel.departement == hart.departement)).first()
                    h_service, h_mwst, vat2, fact = get_output(calc_servtaxesbl(1, artikel.artnr, artikel.departement, None))
                    h_mwst = h_mwst + vat2

                    if curr_vat == 0:
                        curr_vat = h_mwst

                    elif curr_vat != h_mwst:
                        multi_vat = True
                amount = hbline.epreis * qty

                if hbline.betrag > 0 and amount < 0:
                    amount = - amount

                elif hbline.betrag < 0 and amount > 0:
                    amount = - amount

                if qty != 0:
                    unit_price = (hbline.betrag / qty) / fact
                else:
                    unit_price = hbline.epreis / fact

                if unit_price < 0:
                    unit_price = - unit_price
                h_service = round(h_service * unit_price, price_decimal)
                h_mwst = round(h_mwst * unit_price, price_decimal)

                if h_service == 0 and h_mwst == 0:
                    1

                elif not incl_mwst:

                    if h_service == 0:
                        h_mwst = hbline.betrag - amount

                if hbline.betrag > 0 and h_mwst < 0:
                    h_mwst = - h_mwst

                elif hbline.betrag < 0 and h_mwst > 0:
                    h_mwst = - h_mwst
                mwst = mwst + h_mwst


        return generate_inner_output()

    def create_vat_list():

        nonlocal bill_date, billart, qty, description, cancel_str, t_h_bill_list, vat_amount, multi_vat, get_rechnr, get_amount, curr_dept, active_deposit, h_bill, bill, htparam, artikel, counters, bill_line, billjournal, h_bill_line, h_artikel, queasy, h_journal
        nonlocal hbline, hart, foart, paramqsy, searchbill, genparamso, orderbill, orderbilline, orderbill_close, pickup_table, qpayment_gateway, buffq33


        nonlocal t_h_bill, vat_list, hbline, hart, foart, paramqsy, searchbill, genparamso, orderbill, orderbilline, orderbill_close, pickup_table, qpayment_gateway, buffq33
        nonlocal t_h_bill_list, vat_list_list

        service:decimal = 0
        vat:decimal = 0
        vat2:decimal = 0
        fact:decimal = 0
        Hbline = H_bill_line
        Hart = H_artikel
        vat_list_list.clear()

        hbline_obj_list = []
        for hbline, hart in db_session.query(Hbline, Hart).join(Hart,(Hart.artnr == Hbline.artnr) &  (Hart.departement == Hbline.departement) &  (Hart.artart == 0)).filter(
                (Hbline.rechnr == h_bill.rechnr) &  (Hbline.departement == h_bill.departement)).all():
            if hbline._recid in hbline_obj_list:
                continue
            else:
                hbline_obj_list.append(hbline._recid)

            artikel = db_session.query(Artikel).filter(
                    (Artikel.artnr == hart.artnrfront) &  (Artikel.departement == hart.departement)).first()

            htparam = db_session.query(Htparam).filter(
                    (Htparam.paramnr == artikel.mwst_code)).first()

            if not htparam:

                vat_list = query(vat_list_list, filters=(lambda vat_list :vat_list.vatproz == 0), first=True)

                if not vat_list:
                    vat_list = Vat_list()
                vat_list_list.append(vat_list)

                vat_list.netto = vat_list.netto + hbline.betrag


            else:
                service, vat, vat2, fact = get_output(calc_servtaxesbl(1, artikel.artnr, artikel.departement, None))
                vat = vat + vat2

                vat_list = query(vat_list_list, filters=(lambda vat_list :vat_list.vatproz == vat * 100), first=True)

                if not vat_list:
                    vat_list = Vat_list()
                    vat_list_list.append(vat_list)

                    vat_list.vatproz = vat * 100

        for vat_list in query(vat_list_list):
            vat_list.vatAmt, vat_list.netto, vat_list.betrag, vat_list.fbetrag = cal_vatamt(vat_list.vatproz)
        amount = 0

        for vat_list in query(vat_list_list):

            if vat_list.betrag == 0:
                vat_list_list.remove(vat_list)

    def update_bill_umsatz():

        nonlocal bill_date, billart, qty, description, cancel_str, t_h_bill_list, vat_amount, multi_vat, get_rechnr, get_amount, curr_dept, active_deposit, h_bill, bill, htparam, artikel, counters, bill_line, billjournal, h_bill_line, h_artikel, queasy, h_journal
        nonlocal hbline, hart, foart, paramqsy, searchbill, genparamso, orderbill, orderbilline, orderbill_close, pickup_table, qpayment_gateway, buffq33


        nonlocal t_h_bill, vat_list, hbline, hart, foart, paramqsy, searchbill, genparamso, orderbill, orderbilline, orderbill_close, pickup_table, qpayment_gateway, buffq33
        nonlocal t_h_bill_list, vat_list_list


        Hbline = H_bill_line
        Hart = H_artikel
        Foart = Artikel

        hbline_obj_list = []
        for hbline, hart, foart in db_session.query(Hbline, Hart, Foart).join(Hart,(Hart.artnr == Hbline.artnr) &  (Hart.departement == Hbline.departement) &  (Hart.artart == 0)).join(Foart,(Foart.artnr == hart.artnrfront) &  (Foart.departement == hart.departement) &  (Foart.artart == 0)).filter(
                (Hbline.departement == h_bill.departement) &  (Hbline.rechnr == h_bill.rechnr) &  (Hbline.artnr != 0)).all():
            if hbline._recid in hbline_obj_list:
                continue
            else:
                hbline_obj_list.append(hbline._recid)

            if foart.umsatzart == 3 or foart.umsatzart == 5 or foart.umsatzart == 6:
                bill.f_b_umsatz = bill.f_b_umsatz + hbline.betrag


            else:
                bill.sonst_umsatz = bill.sonst_umsatz + hbline.betrag


        bill.gesamtumsatz = bill.gesamtumsatz + h_bill.gesamtumsatz
        bill.saldo = bill.saldo + amount

    def cal_vatamt(vatproz:decimal):

        nonlocal bill_date, billart, qty, description, cancel_str, t_h_bill_list, vat_amount, multi_vat, get_rechnr, get_amount, curr_dept, active_deposit, h_bill, bill, htparam, artikel, counters, bill_line, billjournal, h_bill_line, h_artikel, queasy, h_journal
        nonlocal hbline, hart, foart, paramqsy, searchbill, genparamso, orderbill, orderbilline, orderbill_close, pickup_table, qpayment_gateway, buffq33


        nonlocal t_h_bill, vat_list, hbline, hart, foart, paramqsy, searchbill, genparamso, orderbill, orderbilline, orderbill_close, pickup_table, qpayment_gateway, buffq33
        nonlocal t_h_bill_list, vat_list_list

        mwst = 0
        netto = 0
        betrag = 0
        fbetrag = 0
        h_service:decimal = 0
        h_mwst:decimal = 0
        vat2:decimal = 0
        fact:decimal = 0
        fact1:decimal = 0
        qty:decimal = 0
        unit_price:decimal = 0
        amount:decimal = 0
        incl_mwst:bool = False
        disc_art1:int = 0
        vatind:int = 0
        vatstr:str = ""
        locstr:str = ""
        sourcestr:str = ""

        def generate_inner_output():
            return mwst, netto, betrag, fbetrag
        Hbline = H_bill_line
        Hart = H_artikel

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 134)).first()
        incl_mwst = htparam.flogical

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 557)).first()
        disc_art1 = htparam.finteger
        vatstr = "vat%," + to_string(vatproz * 100) + ";"

        hbline_obj_list = []
        for hbline, hart in db_session.query(Hbline, Hart).join(Hart,(Hart.artnr == Hbline.artnr) &  (Hart.departement == Hbline.departement) &  (Hart.artart == 0)).filter(
                (Hbline.rechnr == h_bill.rechnr) &  (Hbline.departement == h_bill.departement)).all():
            if hbline._recid in hbline_obj_list:
                continue
            else:
                hbline_obj_list.append(hbline._recid)

            htparam = db_session.query(Htparam).filter(
                    (Htparam.paramnr == hart.mwst_code)).first()

            if htparam:

                if hart.artnr == disc_art1:

                    h_journal = db_session.query(H_journal).filter(
                            (H_journal.departement == hbline.departement) &  (H_journal.bill_datum == hbline.bill_datum) &  (H_journal.rechnr == hbline.rechnr) &  (H_journal.artnr == hbline.artnr) &  (H_journal.zeit == hbline.zeit)).first()

                    if h_journal:
                        sourcestr = h_journal.aendertext
                        vatind = 1 + get_index(sourcestr, vatstr)

                        if htparam.fdecimal == vatproz and sourcestr == "":
                            netto = netto + hbline.nettobetrag
                            betrag = betrag + hbline.betrag
                            fbetrag = fbetrag + hbline.fremdwbetrag
                            mwst = mwst + h_journal.steuercode / 100


                        else:
                            while vatind > 0:
                                locstr = substring(sourcestr, vatind + len(vatstr) - 1)
                                mwst, netto, betrag, fbetrag = get_vat(locstr, mwst, netto, betrag, fbetrag)
                                sourcestr = locstr
                                vatind = 1 + get_index(sourcestr, vatstr)

                elif htparam.fdecimal == vatproz:
                    netto = netto + hbline.nettobetrag
                    betrag = betrag + hbline.betrag
                    fbetrag = fbetrag + hbline.fremdwbetrag


                    h_service = 0
                    h_mwst = 0
                    fact = 1
                    qty = hbline.anzahl

                    if qty < 0:
                        qty = - qty

                    if incl_mwst:

                        artikel = db_session.query(Artikel).filter(
                                (Artikel.artnr == hart.artnrfront) &  (Artikel.departement == hart.departement)).first()
                        h_service, h_mwst, vat2, fact = get_output(calc_servtaxesbl(1, artikel.artnr, artikel.departement, None))
                        h_mwst = h_mwst + vat2


                    amount = hbline.epreis * qty

                    if hbline.betrag > 0 and amount < 0:
                        amount = - amount

                    elif hbline.betrag < 0 and amount > 0:
                        amount = - amount
                    unit_price = hbline.epreis / fact

                    if incl_mwst:

                        if qty != 0:
                            unit_price = (hbline.betrag / qty) / fact
                        else:
                            unit_price = hbline.betrag / fact

                    if unit_price < 0:
                        unit_price = - unit_price
                    h_service = round(h_service * unit_price, price_decimal)
                    h_mwst = round(h_mwst * unit_price, price_decimal)

                    if h_service == 0 and h_mwst == 0:
                        1

                    elif not incl_mwst:

                        if h_service == 0:
                            h_mwst = hbline.betrag - amount

                    if hbline.betrag > 0 and h_mwst < 0:
                        h_mwst = - h_mwst

                    elif hbline.betrag < 0 and h_mwst > 0:
                        h_mwst = - h_mwst
                    mwst = mwst + h_mwst


        return generate_inner_output()

    def get_vat(curr_str:str, mwst:decimal, netto:decimal, betrag:decimal, fbetrag:decimal):

        nonlocal bill_date, billart, qty, description, cancel_str, t_h_bill_list, vat_amount, multi_vat, get_rechnr, get_amount, curr_dept, active_deposit, h_bill, bill, htparam, artikel, counters, bill_line, billjournal, h_bill_line, h_artikel, queasy, h_journal
        nonlocal hbline, hart, foart, paramqsy, searchbill, genparamso, orderbill, orderbilline, orderbill_close, pickup_table, qpayment_gateway, buffq33


        nonlocal t_h_bill, vat_list, hbline, hart, foart, paramqsy, searchbill, genparamso, orderbill, orderbilline, orderbill_close, pickup_table, qpayment_gateway, buffq33
        nonlocal t_h_bill_list, vat_list_list

        ind:int = 0
        tokcounter:int = 0
        messtr:str = ""
        mestoken:str = ""
        mesvalue:str = ""
        ind = 1 + get_index(curr_str, "vat%")

        if ind > 0:
            curr_str = substring(curr_str, 0, ind - 1)
        for tokcounter in range(1,num_entries(curr_str, ";") - 1 + 1) :
            messtr = entry(tokcounter - 1, curr_str, ";")
            mestoken = entry(0, messtr, ",")
            mesvalue = entry(1, messtr, ",")

            if mestoken == "vat":
                mwst = mwst + decimal.Decimal(mesvalue) / 100
            elif mestoken == "NET":
                netto = netto + decimal.Decimal(mesvalue) / 100
            elif mestoken == "AMT":
                betrag = betrag + decimal.Decimal(mesvalue) / 100
            elif mestoken == "FAMT":
                fbetrag = fbetrag + decimal.Decimal(mesvalue) / 100

    def update_selforder():

        nonlocal bill_date, billart, qty, description, cancel_str, t_h_bill_list, vat_amount, multi_vat, get_rechnr, get_amount, curr_dept, active_deposit, h_bill, bill, htparam, artikel, counters, bill_line, billjournal, h_bill_line, h_artikel, queasy, h_journal
        nonlocal hbline, hart, foart, paramqsy, searchbill, genparamso, orderbill, orderbilline, orderbill_close, pickup_table, qpayment_gateway, buffq33


        nonlocal t_h_bill, vat_list, hbline, hart, foart, paramqsy, searchbill, genparamso, orderbill, orderbilline, orderbill_close, pickup_table, qpayment_gateway, buffq33
        nonlocal t_h_bill_list, vat_list_list

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

        nonlocal bill_date, billart, qty, description, cancel_str, t_h_bill_list, vat_amount, multi_vat, get_rechnr, get_amount, curr_dept, active_deposit, h_bill, bill, htparam, artikel, counters, bill_line, billjournal, h_bill_line, h_artikel, queasy, h_journal
        nonlocal hbline, hart, foart, paramqsy, searchbill, genparamso, orderbill, orderbilline, orderbill_close, pickup_table, qpayment_gateway, buffq33


        nonlocal t_h_bill, vat_list, hbline, hart, foart, paramqsy, searchbill, genparamso, orderbill, orderbilline, orderbill_close, pickup_table, qpayment_gateway, buffq33
        nonlocal t_h_bill_list, vat_list_list

        recid_q33:int = 0
        Buffq33 = Queasy

        queasy = db_session.query(Queasy).filter(
                (Queasy.key == 251) &  (Queasy.number1 == rec_id_h_bill)).first()

        if queasy:
            recid_q33 = queasy.number2

            buffq33 = db_session.query(Buffq33).filter(
                    (Buffq33._recid == recid_q33)).first()

            if buffq33:

                buffq33 = db_session.query(Buffq33).first()
                buffq33.betriebsnr = 1

                buffq33 = db_session.query(Buffq33).first()

    h_bill = db_session.query(H_bill).filter(
            (H_bill._recid == rec_id_h_bill)).first()

    bill = db_session.query(Bill).filter(
            (Bill._recid == bilrecid)).first()
    curr_dept = h_bill.departement

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 588)).first()

    if htparam:
        active_deposit = htparam.flogical

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 271)).first()

    if htparam.feldtyp == 4:
        multi_vat = htparam.flogical

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
    billart = 0
    qty = 1
    amount = - amount
    amount_foreign = - amount_foreign

    if not double_currency:
        amount_foreign = amount / exchg_rate

    if amount != 0:

        artikel = db_session.query(Artikel).filter(
                (Artikel.artnr == kellner1_kcredit_nr) &  (Artikel.departement == 0)).first()

        if artikel:
            billart = artikel.artnr
            description = trim(artikel.bezeich) + " *" + to_string(h_bill.rechnr)
    else:
        description = "*" + to_string(h_bill.rechnr)

    bill = db_session.query(Bill).first()

    if bill.rechnr == 0:

        counters = db_session.query(Counters).filter(
                (Counters.counter_no == 3)).first()
        counters = counters + 1

        counters = db_session.query(Counters).first()
        bill.rechnr = counters
    update_bill_umsatz()

    if bill.datum < bill_date:
        bill.datum = bill_date

    if foreign_rate and not double_currency:
        bill.mwst[98] = bill.mwst[98] + amount / exchg_rate

    elif double_currency:
        bill.mwst[98] = bill.mwst[98] + amount_foreign
    bill.rgdruck = 0

    bill = db_session.query(Bill).first()
    vat_amount = cal_vat_amount()
    bill_line = Bill_line()
    db_session.add(bill_line)

    bill_line.rechnr = bill.rechnr
    bill_line.zinr = bill.zinr
    bill_line.massnr = bill.resnr
    bill_line.billin_nr = bill.reslinnr
    bill_line.artnr = billart
    bill_line.bezeich = description
    bill_line.anzahl = 1
    bill_line.fremdwbetrag = amount_foreign
    bill_line.betrag = amount
    bill_line.departement = h_bill.departement
    bill_line.epreis = 0
    bill_line.zeit = get_current_time_in_seconds()
    bill_line.userinit = user_init
    bill_line.bill_datum = bill_date
    bill_line.orts_tax = vat_amount

    bill_line = db_session.query(Bill_line).first()
    billjournal = Billjournal()
    db_session.add(billjournal)

    billjournal.rechnr = bill.rechnr
    billjournal.zinr = bill.zinr
    billjournal.departement = h_bill.departement
    billjournal.artnr = billart
    billjournal.anzahl = 1
    billjournal.fremdwaehrng = amount_foreign
    billjournal.betrag = amount
    billjournal.bezeich = description
    billjournal.epreis = 0
    billjournal.zeit = get_current_time_in_seconds()
    billjournal.stornogrund = ""
    billjournal.userinit = user_init
    billjournal.bill_datum = bill_date

    if artikel:
        billjournal.departement = artikel.departement

    billjournal = db_session.query(Billjournal).first()
    cancel_str = ""

    h_bill = db_session.query(H_bill).first()
    h_bill.flag = 1
    h_bill.bilname = gname

    if hoga_resnr > 0 and h_bill.resnr == 0:
        h_bill.resnr = hoga_resnr
        h_bill.reslinnr = hoga_reslinnr

    h_bill = db_session.query(H_bill).first()
    get_rechnr = h_bill.rechnr

    for h_bill_line in db_session.query(H_bill_line).filter(
                (H_bill_line.departement == h_bill.departement) &  (H_bill_line.rechnr == h_bill.rechnr) &  (H_bill_line.betrag < 0)).all():

        h_artikel = db_session.query(H_artikel).filter(
                    (H_artikel.departement == h_bill_line.departement) &  (H_artikel.artnr == h_bill_line.artnr) &  (H_artikel.artart != 0)).first()

        if h_artikel:
            get_amount = get_amount + h_bill_line.betrag

    queasy = db_session.query(Queasy).filter(
                (Queasy.key == 230)).first()

    if queasy:
        update_selforder()

    if active_deposit:
        remove_rsv_table()

    t_h_bill = T_h_bill()
    t_h_bill_list.append(t_h_bill)

    buffer_copy(h_bill, t_h_bill)
    t_h_bill.rec_id = h_bill._recid


    amount = - amount
    amount_foreign = - amount_foreign

    return generate_output()