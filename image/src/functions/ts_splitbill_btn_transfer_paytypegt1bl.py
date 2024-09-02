from functions.additional_functions import *
import decimal
from datetime import date
from functions.rest_addgastinfo import rest_addgastinfo
from functions.ts_splitbill_update_billbl import ts_splitbill_update_billbl
from functions.calc_servtaxesbl import calc_servtaxesbl
from models import H_bill_line, Kellner, H_bill, Bill, H_artikel, Counters, Htparam, Artikel, Bill_line, Billjournal, H_journal, Queasy

def ts_splitbill_btn_transfer_paytypegt1bl(rec_id_h_bill:int, bilrecid:int, curr_select:int, multi_vat:bool, balance:decimal, pay_type:int, transdate:date, price_decimal:int, exchg_rate:decimal, foreign_rate:bool, dept:int, change_str:str, add_zeit:int, hoga_card:str, cancel_str:str, curr_waiter:int, curr_room:str, user_init:str, cc_comment:str, guestnr:int, tischnr:int, double_currency:bool, amount_foreign:decimal):
    err_flag = 0
    billart = 0
    qty = 0
    price = 0
    amount = 0
    description = ""
    bill_date = None
    fl_code = 0
    t_h_bill_line_list = []
    bname:str = ""
    payment_found:bool = False
    h_bill_line = kellner = h_bill = bill = h_artikel = counters = htparam = artikel = bill_line = billjournal = h_journal = queasy = None

    vat_list = t_h_bill_line = kellner1 = hbline = hart = foart = None

    vat_list_list, Vat_list = create_model("Vat_list", {"vatproz":decimal, "vatamt":decimal, "netto":decimal, "betrag":decimal, "fbetrag":decimal})
    t_h_bill_line_list, T_h_bill_line = create_model_like(H_bill_line, {"rec_id":int})

    Kellner1 = Kellner
    Hbline = H_bill_line
    Hart = H_artikel
    Foart = Artikel

    db_session = local_storage.db_session

    def generate_output():
        nonlocal err_flag, billart, qty, price, amount, description, bill_date, fl_code, t_h_bill_line_list, bname, payment_found, h_bill_line, kellner, h_bill, bill, h_artikel, counters, htparam, artikel, bill_line, billjournal, h_journal, queasy
        nonlocal kellner1, hbline, hart, foart


        nonlocal vat_list, t_h_bill_line, kellner1, hbline, hart, foart
        nonlocal vat_list_list, t_h_bill_line_list
        return {"err_flag": err_flag, "billart": billart, "qty": qty, "price": price, "amount": amount, "description": description, "bill_date": bill_date, "fl_code": fl_code, "t-h-bill-line": t_h_bill_line_list}

    def update_bill1():

        nonlocal err_flag, billart, qty, price, amount, description, bill_date, fl_code, t_h_bill_line_list, bname, payment_found, h_bill_line, kellner, h_bill, bill, h_artikel, counters, htparam, artikel, bill_line, billjournal, h_journal, queasy
        nonlocal kellner1, hbline, hart, foart


        nonlocal vat_list, t_h_bill_line, kellner1, hbline, hart, foart
        nonlocal vat_list_list, t_h_bill_line_list

        vat_amount:decimal = 0

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

            kellner1 = db_session.query(Kellner1).filter(
                    (Kellner1.kellner_nr == h_bill.kellner_nr) &  (Kellner1.departement == h_bill.departement)).first()

            artikel = db_session.query(Artikel).filter(
                    (Artikel.artnr == kellner1.kcredit_nr) &  (Artikel.departement == 0)).first()

            bill = db_session.query(Bill).filter(
                    (Bill._recid == bilrecid)).first()

            if bill.rechnr == 0:

                counters = db_session.query(Counters).filter(
                        (Counters.counter_no == 3)).first()
                counters = counters + 1
                bill.rechnr = counters

                counters = db_session.query(Counters).first()
        update_bill_umsatz()

        if double_currency or foreign_rate:
            bill.mwst[98] = bill.mwst[98] + amount / exchg_rate

        if bill.datum < bill_date:
            bill.datum = bill_date
        bill.rgdruck = 0
        vat_amount = cal_vat_amount()

        if multi_vat:
            create_vat_list()

        if multi_vat:

            for vat_list in query(vat_list_list):

                if artikel:
                    billart = artikel.artnr
                    description = trim(artikel.bezeich) + "[" + to_string(vat_list.vatproz) + "]" + " *" + to_string(h_bill.rechnr)
                else:
                    description = "[" + to_string(vat_list.vatproz) + "]" + " *" + to_string(h_bill.rechnr)
                bill_line = Bill_line()
                db_session.add(bill_line)

                bill_line.rechnr = bill.rechnr
                bill_line.zinr = bill.zinr
                bill_line.massnr = bill.resnr
                bill_line.billin_nr = bill.reslinnr
                bill_line.artnr = billart
                bill_line.bezeich = description
                bill_line.anzahl = 0
                bill_line.fremdwbetrag = vat_list.fbetrag
                bill_line.betrag = vat_list.betrag
                bill_line.nettobetrag = vat_list.netto
                bill_line.departement = dept
                bill_line.epreis = 0
                bill_line.zeit = get_current_time_in_seconds()
                bill_line.userinit = user_init
                bill_line.bill_datum = bill_date
                bill_line.orts_tax = vat_list.vatAmt
                bill_line.waehrungsnr = curr_select
                bill_line.origin_id = "VAT%," + to_string(vat_list.vatproz * 100) + ";" +\
                        "VAT," + to_string(vat_list.vatAmt * 100) + ";" +\
                        "NET," + to_string(vat_list.netto * 100) + ";"

                bill_line = db_session.query(Bill_line).first()
                billjournal = Billjournal()
                db_session.add(billjournal)

                billjournal.rechnr = bill.rechnr
                billjournal.zinr = bill.zinr
                billjournal.artnr = billart
                billjournal.anzahl = 1
                billjournal.fremdwaehrng = vat_list.fbetrag
                billjournal.betrag = vat_list.betrag
                billjournal.bezeich = description
                billjournal.departement = dept
                billjournal.epreis = 0
                billjournal.zeit = get_current_time_in_seconds()
                billjournal.stornogrund = ""
                billjournal.userinit = user_init
                billjournal.bill_datum = bill_date

                if artikel:
                    billjournal.departement = artikel.departement

                billjournal = db_session.query(Billjournal).first()

        else:

            if artikel:
                billart = artikel.artnr
                description = trim(artikel.bezeich) + " *" + to_string(h_bill.rechnr)
            else:
                description = "*" + to_string(h_bill.rechnr)
            bill_line = Bill_line()
            db_session.add(bill_line)

            bill_line.rechnr = bill.rechnr
            bill_line.zinr = bill.zinr
            bill_line.massnr = bill.resnr
            bill_line.billin_nr = bill.reslinnr
            bill_line.artnr = billart
            bill_line.bezeich = description
            bill_line.anzahl = 0
            bill_line.fremdwbetrag = amount_foreign
            bill_line.betrag = amount
            bill_line.departement = dept
            bill_line.epreis = 0
            bill_line.zeit = get_current_time_in_seconds()
            bill_line.userinit = user_init
            bill_line.bill_datum = bill_date
            bill_line.orts_tax = vat_amount
            bill_line.waehrungsnr = curr_select

            bill_line = db_session.query(Bill_line).first()
            billjournal = Billjournal()
            db_session.add(billjournal)

            billjournal.rechnr = bill.rechnr
            billjournal.zinr = bill.zinr
            billjournal.artnr = billart
            billjournal.anzahl = 1
            billjournal.fremdwaehrng = amount_foreign
            billjournal.betrag = amount
            billjournal.bezeich = description
            billjournal.departement = dept
            billjournal.epreis = 0
            billjournal.zeit = get_current_time_in_seconds()
            billjournal.stornogrund = ""
            billjournal.userinit = user_init
            billjournal.bill_datum = bill_date

            if artikel:
                billjournal.departement = artikel.departement

            billjournal = db_session.query(Billjournal).first()

        bill = db_session.query(Bill).first()
        amount = - amount

    def create_vat_list():

        nonlocal err_flag, billart, qty, price, amount, description, bill_date, fl_code, t_h_bill_line_list, bname, payment_found, h_bill_line, kellner, h_bill, bill, h_artikel, counters, htparam, artikel, bill_line, billjournal, h_journal, queasy
        nonlocal kellner1, hbline, hart, foart


        nonlocal vat_list, t_h_bill_line, kellner1, hbline, hart, foart
        nonlocal vat_list_list, t_h_bill_line_list


        Hbline = H_bill_line
        Hart = H_artikel
        vat_list_list.clear()

        hbline_obj_list = []
        for hbline, hart in db_session.query(Hbline, Hart).join(Hart,(Hart.artnr == Hbline.artnr) &  (Hart.departement == Hbline.departement) &  (Hart.artart == 0)).filter(
                (Hbline.rechnr == h_bill.rechnr) &  (Hbline.departement == h_bill.departement) &  (Hbline.waehrungsnr == curr_select)).all():
            if hbline._recid in hbline_obj_list:
                continue
            else:
                hbline_obj_list.append(hbline._recid)

            htparam = db_session.query(Htparam).filter(
                    (Htparam.paramnr == hart.mwst_code)).first()

            if not htparam:

                vat_list = query(vat_list_list, filters=(lambda vat_list :vat_list.vatproz == 0), first=True)

                if not vat_list:
                    vat_list = Vat_list()
                vat_list_list.append(vat_list)

                vat_list.netto = vat_list.netto + hbline.betrag


            else:

                vat_list = query(vat_list_list, filters=(lambda vat_list :vat_list.vatproz == htparam.fdecimal), first=True)

                if not vat_list:
                    vat_list = Vat_list()
                    vat_list_list.append(vat_list)

                    vat_list.vatproz = htparam.fdecimal

        for vat_list in query(vat_list_list):
            vat_list.vatAmt, vat_list.netto, vat_list.betrag, vat_list.fbetrag = cal_vatamt(vat_list.vatproz)
        amount = 0

        for vat_list in query(vat_list_list):

            if vat_list.betrag == 0:
                vat_list_list.remove(vat_list)

    def update_bill_umsatz():

        nonlocal err_flag, billart, qty, price, amount, description, bill_date, fl_code, t_h_bill_line_list, bname, payment_found, h_bill_line, kellner, h_bill, bill, h_artikel, counters, htparam, artikel, bill_line, billjournal, h_journal, queasy
        nonlocal kellner1, hbline, hart, foart


        nonlocal vat_list, t_h_bill_line, kellner1, hbline, hart, foart
        nonlocal vat_list_list, t_h_bill_line_list


        Hbline = H_bill_line
        Hart = H_artikel
        Foart = Artikel

        hbline_obj_list = []
        for hbline, hart, foart in db_session.query(Hbline, Hart, Foart).join(Hart,(Hart.artnr == Hbline.artnr) &  (Hart.departement == Hbline.departement) &  (Hart.artart == 0)).join(Foart,(Foart.artnr == hart.artnrfront) &  (Foart.departement == hart.departement) &  (Foart.artart == 0)).filter(
                (Hbline.departement == h_bill.departement) &  (Hbline.rechnr == h_bill.rechnr) &  (Hbline.artnr != 0) &  (Hbline.waehrungsnr == curr_select)).all():
            if hbline._recid in hbline_obj_list:
                continue
            else:
                hbline_obj_list.append(hbline._recid)

            if foart.umsatzart == 3 or foart.umsatzart == 5 or foart.umsatzart == 6:
                bill.f_b_umsatz = bill.f_b_umsatz + hbline.betrag


            else:
                bill.sonst_umsatz = bill.sonst_umsatz + hbline.betrag


        bill.gesamtumsatz = bill.gesamtumsatz + amount
        bill.saldo = bill.saldo + amount

    def cal_vat_amount():

        nonlocal err_flag, billart, qty, price, amount, description, bill_date, fl_code, t_h_bill_line_list, bname, payment_found, h_bill_line, kellner, h_bill, bill, h_artikel, counters, htparam, artikel, bill_line, billjournal, h_journal, queasy
        nonlocal kellner1, hbline, hart, foart


        nonlocal vat_list, t_h_bill_line, kellner1, hbline, hart, foart
        nonlocal vat_list_list, t_h_bill_line_list

        mwst = 0
        h_service:decimal = 0
        h_mwst:decimal = 0
        vat2:decimal = 0
        fact:decimal = 0
        fact1:decimal = 0
        unit_price:decimal = 0
        amount:decimal = 0
        incl_mwst:bool = False
        curr_vat:decimal = 0

        def generate_inner_output():
            return mwst
        Hbline = H_bill_line
        Hart = H_artikel

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 134)).first()
        incl_mwst = htparam.flogical

        hbline_obj_list = []
        for hbline, hart in db_session.query(Hbline, Hart).join(Hart,(Hart.artnr == Hbline.artnr) &  (Hart.departement == Hbline.departement) &  (Hart.artart == 0)).filter(
                (Hbline.rechnr == h_bill.rechnr) &  (Hbline.departement == h_bill.departement) &  (Hbline.waehrungsnr == curr_select)).all():
            if hbline._recid in hbline_obj_list:
                continue
            else:
                hbline_obj_list.append(hbline._recid)


            h_service = 0
            h_mwst = 0
            fact = 1

            if incl_mwst:

                artikel = db_session.query(Artikel).filter(
                        (Artikel.artnr == h_Artikel.artnrfront) &  (Artikel.departement == h_Artikel.departement)).first()
                h_service, h_mwst, vat2, fact = get_output(calc_servtaxesbl(1, artikel.artnr, artikel.departement, None))
                h_mwst = h_mwst + vat2

                if curr_vat == 0:
                    curr_vat = h_mwst

                elif curr_vat != h_mwst:
                    multi_vat = True
            amount = hbline.epreis * hbline.anzahl

            if hbline.anzahl != 0:
                unit_price = (hbline.betrag / hbline.anzahl) / fact
            else:
                unit_price = hbline.epreis / fact
            h_service = round(h_service * unit_price * hbline.anzahl, price_decimal)
            h_mwst = round(h_mwst * unit_price * hbline.anzahl, price_decimal)
            mwst = mwst + h_mwst


            pass


        return generate_inner_output()

    def cal_vatamt(vatproz:decimal):

        nonlocal err_flag, billart, qty, price, amount, description, bill_date, fl_code, t_h_bill_line_list, bname, payment_found, h_bill_line, kellner, h_bill, bill, h_artikel, counters, htparam, artikel, bill_line, billjournal, h_journal, queasy
        nonlocal kellner1, hbline, hart, foart


        nonlocal vat_list, t_h_bill_line, kellner1, hbline, hart, foart
        nonlocal vat_list_list, t_h_bill_line_list

        mwst = 0
        netto = 0
        betrag = 0
        fbetrag = 0
        h_service:decimal = 0
        h_mwst:decimal = 0
        vat2:decimal = 0
        fact:decimal = 1
        fact1:decimal = 0
        qty:decimal = 0
        unit_price:decimal = 0
        amount:decimal = 0
        incl_mwst:bool = False
        disc_art1:int = 0
        vatind:int = 0
        vatstr:str = ""
        locstr:str = ""

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
        vatstr = "VAT%," + to_string(vatproz * 100) + ";"

        hbline_obj_list = []
        for hbline, hart in db_session.query(Hbline, Hart).join(Hart,(Hart.artnr == Hbline.artnr) &  (Hart.departement == Hbline.departement) &  (Hart.artart == 0)).filter(
                (Hbline.rechnr == h_bill.rechnr) &  (Hbline.departement == h_bill.departement) &  (Hbline.waehrungsnr == curr_select)).all():
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
                        vatind = 1 + get_index(h_journal.aendertext, vatstr)

                        if htparam.fdecimal == vatproz and h_journal.aendertext == "":
                            netto = netto + hbline.nettobetrag
                            betrag = betrag + hbline.betrag
                            fbetrag = fbetrag + hbline.fremdwbetrag
                            mwst = mwst + h_journal.steuercode / 100

                        elif vatind > 0:
                            locstr = substring(h_journal.aendertext, vatind + len(vatstr) - 1)
                            mwst, netto, betrag, fbetrag = get_vat(locstr, mwst, netto, betrag, fbetrag)

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
                        h_service, h_mwst, vat2, fact = get_output(calc_servtaxesbl(1, artikel.artnr, artikel.departement, hbline.bill_datum))
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

                    if hart.service_code != 0:

                        htparam = db_session.query(Htparam).filter(
                                (Htparam.paramnr == hart.service_code)).first()

                        if htparam.fdecimal != 0:
                            h_service = unit_price * htparam.fdecimal / 100
                            h_service = round(h_service, 2)

                    if hart.mwst_code != 0:

                        htparam = db_session.query(Htparam).filter(
                                (Htparam.paramnr == hart.mwst_code)).first()

                        if htparam.fdecimal != 0:
                            h_mwst = htparam.fdecimal

                            htparam = db_session.query(Htparam).filter(
                                    (Htparam.paramnr == 479)).first()

                            if htparam.flogical:
                                h_mwst = h_mwst * (unit_price + h_service) / 100
                            else:
                                h_mwst = h_mwst * unit_price / 100
                            h_mwst = round(h_mwst * qty, price_decimal)

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

        nonlocal err_flag, billart, qty, price, amount, description, bill_date, fl_code, t_h_bill_line_list, bname, payment_found, h_bill_line, kellner, h_bill, bill, h_artikel, counters, htparam, artikel, bill_line, billjournal, h_journal, queasy
        nonlocal kellner1, hbline, hart, foart


        nonlocal vat_list, t_h_bill_line, kellner1, hbline, hart, foart
        nonlocal vat_list_list, t_h_bill_line_list

        ind:int = 0
        tokcounter:int = 0
        messtr:str = ""
        mestoken:str = ""
        mesvalue:str = ""
        ind = 1 + get_index(curr_str, "VAT%")

        if ind > 0:
            curr_str = substring(curr_str, 0, ind - 1)
        for tokcounter in range(1,num_entries(curr_str, ";") - 1 + 1) :
            messtr = entry(tokcounter - 1, curr_str, ";")
            mestoken = entry(0, messtr, ",")
            mesvalue = entry(1, messtr, ",")

            if mestoken == "VAT":
                mwst = mwst + decimal.Decimal(mesvalue) / 100
            elif mestoken == "NET":
                netto = netto + decimal.Decimal(mesvalue) / 100
            elif mestoken == "AMT":
                betrag = betrag + decimal.Decimal(mesvalue) / 100
            elif mestoken == "FAMT":
                fbetrag = fbetrag + decimal.Decimal(mesvalue) / 100

    def del_queasy():

        nonlocal err_flag, billart, qty, price, amount, description, bill_date, fl_code, t_h_bill_line_list, bname, payment_found, h_bill_line, kellner, h_bill, bill, h_artikel, counters, htparam, artikel, bill_line, billjournal, h_journal, queasy
        nonlocal kellner1, hbline, hart, foart


        nonlocal vat_list, t_h_bill_line, kellner1, hbline, hart, foart
        nonlocal vat_list_list, t_h_bill_line_list

        for queasy in db_session.query(Queasy).filter(
                (Queasy.key == 4) &  (Queasy.number1 == (h_bill.departement + h_bill.rechnr * 100)) &  (Queasy.number2 >= 0) &  (Queasy.deci2 >= 0)).all():
            db_session.delete(queasy)


    h_bill = db_session.query(H_bill).filter(
            (H_bill._recid == rec_id_h_bill)).first()

    bill = db_session.query(Bill).filter(
            (Bill._recid == bilrecid)).first()

    h_bill_line_obj_list = []
    for h_bill_line, h_artikel in db_session.query(H_bill_line, H_artikel).join(H_artikel,(H_artikel.artnr == H_bill_line.artnr) &  (H_artikel.departement == H_bill_line.departement) &  (H_artikel.artart != 0)).filter(
            (H_bill_line.rechnr == h_bill.rechnr) &  (H_bill_line.departement == h_bill.departement) &  (H_bill_line.waehrungsnr == curr_select)).all():
        if h_bill_line._recid in h_bill_line_obj_list:
            continue
        else:
            h_bill_line_obj_list.append(h_bill_line._recid)


        payment_found = True
        break

    if payment_found and multi_vat:
        err_flag = 1

        return generate_output()
    billart = 0
    qty = 1
    price = 0
    amount = - balance

    if bill.rechnr == 0:

        counters = db_session.query(Counters).filter(
                (Counters.counter_no == 3)).first()
        counters = counters + 1

        bill = db_session.query(Bill).first()
        bill.rechnr = counters

        counters = db_session.query(Counters).first()

    if pay_type == 2:
        description = "RmNo " + bill.zinr + " *" + to_string(bill.rechnr)

    elif pay_type == 3 or pay_type == 4:
        description = "Transfer" + " *" + to_string(bill.rechnr)

    h_bill = db_session.query(H_bill).first()
    h_bill.bilname = bname

    h_bill = db_session.query(H_bill).first()

    if pay_type == 2:
        get_output(rest_addgastinfo(h_bill.departement, h_bill.rechnr, bill.resnr, bill.reslinnr, curr_select, transdate))
    bill_date = get_output(ts_splitbill_update_billbl(rec_id_h_bill, 0, 1, 0, dept, amount, transdate, billart, description, change_str, qty, tischnr, price, add_zeit, curr_select, hoga_card, cancel_str, curr_waiter, amount_foreign, curr_room, user_init, cc_comment, guestnr))
    update_bill1()

    if round(h_bill.saldo, price_decimal) == 0:
        del_queasy()

        h_bill = db_session.query(H_bill).first()
        h_bill.flag = 1

        h_bill = db_session.query(H_bill).first()
        fl_code = 1
    else:
        fl_code = 2

    for h_bill_line in db_session.query(H_bill_line).filter(
            (H_bill_line.departement == dept) &  (H_bill_line.rechnr == h_bill.rechnr)).all():
        t_h_bill_line = T_h_bill_line()
        t_h_bill_line_list.append(t_h_bill_line)

        buffer_copy(h_bill_line, t_h_bill_line)
        t_h_bill_line.rec_id = h_bill_line._recid

    return generate_output()