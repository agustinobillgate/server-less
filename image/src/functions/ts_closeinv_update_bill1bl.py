from functions.additional_functions import *
import decimal
from datetime import date
from functions.calc_servtaxesbl import calc_servtaxesbl
from models import H_bill, Kellner, Htparam, Artikel, Bill, Counters, Bill_line, Billjournal, H_bill_line, H_artikel, H_journal

def ts_closeinv_update_bill1bl(amount:decimal, amount_foreign:decimal, rec_kellner:int, rec_h_bill:int, double_currency:bool, exchg_rate:decimal, bilrecid:int, value_sign:int, user_init:str, bill_date:date, curr_select:int, price_decimal:int):
    billart = 0
    qty = 0
    description = ""
    cancel_str = ""
    t_h_bill_list = []
    multi_vat:bool = False
    vat_amount:decimal = 0
    h_bill = kellner = htparam = artikel = bill = counters = bill_line = billjournal = h_bill_line = h_artikel = h_journal = None

    t_h_bill = vat_list = hbline = hart = foart = None

    t_h_bill_list, T_h_bill = create_model_like(H_bill, {"rec_id":int})
    vat_list_list, Vat_list = create_model("Vat_list", {"vatproz":decimal, "vatamt":decimal, "netto":decimal, "betrag":decimal, "fbetrag":decimal})

    Hbline = H_bill_line
    Hart = H_artikel
    Foart = Artikel

    db_session = local_storage.db_session

    def generate_output():
        nonlocal billart, qty, description, cancel_str, t_h_bill_list, multi_vat, vat_amount, h_bill, kellner, htparam, artikel, bill, counters, bill_line, billjournal, h_bill_line, h_artikel, h_journal
        nonlocal hbline, hart, foart


        nonlocal t_h_bill, vat_list, hbline, hart, foart
        nonlocal t_h_bill_list, vat_list_list
        return {"billart": billart, "qty": qty, "description": description, "cancel_str": cancel_str, "t-h-bill": t_h_bill_list}

    def update_bill_umsatz(value_sign:int):

        nonlocal billart, qty, description, cancel_str, t_h_bill_list, multi_vat, vat_amount, h_bill, kellner, htparam, artikel, bill, counters, bill_line, billjournal, h_bill_line, h_artikel, h_journal
        nonlocal hbline, hart, foart


        nonlocal t_h_bill, vat_list, hbline, hart, foart
        nonlocal t_h_bill_list, vat_list_list

        do_it:bool = False
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

            if curr_select == 0:
                do_it = True
            else:
                do_it = (hbline.waehrungsnr == curr_select)

            if do_it:

                if foart.umsatzart == 3 or foart.umsatzart == 5 or foart.umsatzart == 6:
                    bill.f_b_umsatz = bill.f_b_umsatz +\
                        value_sign * hbline.betrag


                else:
                    bill.sonst_umsatz = bill.sonst_umsatz +\
                        value_sign * hbline.betrag


                bill.gesamtumsatz = bill.gesamtumsatz + value_sign * hbline.betrag
        bill.saldo = bill.saldo + amount

    def cal_vat_amount():

        nonlocal billart, qty, description, cancel_str, t_h_bill_list, multi_vat, vat_amount, h_bill, kellner, htparam, artikel, bill, counters, bill_line, billjournal, h_bill_line, h_artikel, h_journal
        nonlocal hbline, hart, foart


        nonlocal t_h_bill, vat_list, hbline, hart, foart
        nonlocal t_h_bill_list, vat_list_list

        mwst = 0
        h_service:decimal = 0
        h_mwst:decimal = 0
        vat2:decimal = 0
        fact:decimal = 0
        fact1:decimal = 0
        unit_price:decimal = 0
        amount:decimal = 0
        incl_mwst:bool = False
        multi_vat:bool = False
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
                        (Artikel.artnr == hart.artnrfront) &  (Artikel.departement == hart.departement)).first()
                h_service, h_mwst, vat2, fact = get_output(calc_servtaxesbl(1, artikel.artnr, artikel.departement, None))
                h_mwst = h_mwst + vat2

                if curr_vat == 0:
                    curr_vat = h_mwst

                elif curr_vat != h_mwst:
                    multi_vat = True
            amount = hbline.epreis * hbline.anzahl
            unit_price = hbline.epreis / fact
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

    def create_vat_list(value_sign:int):

        nonlocal billart, qty, description, cancel_str, t_h_bill_list, multi_vat, vat_amount, h_bill, kellner, htparam, artikel, bill, counters, bill_line, billjournal, h_bill_line, h_artikel, h_journal
        nonlocal hbline, hart, foart


        nonlocal t_h_bill, vat_list, hbline, hart, foart
        nonlocal t_h_bill_list, vat_list_list

        do_it:bool = False
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

            if curr_select == 0:
                do_it = True
            else:
                do_it = (hbline.waehrungsnr == curr_select)

            if do_it:

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

        for vat_list in query(vat_list_list, filters=(lambda vat_list :vat_list.vatproz != 0)):
            vat_list.vatAmt, vat_list.netto, vat_list.betrag, vat_list.fbetrag = cal_vatamt(value_sign, vat_list.vatproz)

    def cal_vatamt(value_sign:int, vatproz:decimal):

        nonlocal billart, qty, description, cancel_str, t_h_bill_list, multi_vat, vat_amount, h_bill, kellner, htparam, artikel, bill, counters, bill_line, billjournal, h_bill_line, h_artikel, h_journal
        nonlocal hbline, hart, foart


        nonlocal t_h_bill, vat_list, hbline, hart, foart
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
        do_it:bool = False
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
                (Hbline.rechnr == h_bill.rechnr) &  (Hbline.departement == h_bill.departement)).all():
            if hbline._recid in hbline_obj_list:
                continue
            else:
                hbline_obj_list.append(hbline._recid)

            if curr_select == 0:
                do_it = True
            else:
                do_it = (hbline.waehrungsnr == curr_select)

            if do_it:

                htparam = db_session.query(Htparam).filter(
                        (Htparam.paramnr == hart.mwst_code)).first()

                if htparam:

                    if hart.artnr == disc_art1:

                        h_journal = db_session.query(H_journal).filter(
                                (H_journal.departement == hbline.departement) &  (H_journal.bill_datum == hbline.bill_datum) &  (H_journal.rechnr == hbline.rechnr) &  (H_journal.artnr == hbline.artnr) &  (H_journal.zeit == hbline.zeit)).first()

                        if h_journal:
                            vatind = 1 + get_index(h_journal.aendertext, vatstr)

                            if htparam.fdecimal == vatproz and h_journal.aendertext == "":
                                netto = netto + value_sign * hbline.nettobetrag
                                betrag = betrag + value_sign * hbline.betrag
                                fbetrag = fbetrag + value_sign * hbline.fremdwbetrag
                                mwst = mwst + value_sign * h_journal.steuercode / 100

                            elif vatind > 0:
                                locstr = substring(h_journal.aendertext, vatind + len(vatstr) - 1)
                                mwst, netto, betrag, fbetrag = get_vat(value_sign, locstr, mwst, netto, betrag, fbetrag)

                    elif htparam.fdecimal == vatproz:
                        netto = netto + value_sign * hbline.nettobetrag
                        betrag = betrag + value_sign * hbline.betrag
                        fbetrag = fbetrag + value_sign * hbline.fremdwbetrag


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
                        mwst = mwst + value_sign * h_mwst


        return generate_inner_output()

    def get_vat(value_sign:int, curr_str:str, mwst:decimal, netto:decimal, betrag:decimal, fbetrag:decimal):

        nonlocal billart, qty, description, cancel_str, t_h_bill_list, multi_vat, vat_amount, h_bill, kellner, htparam, artikel, bill, counters, bill_line, billjournal, h_bill_line, h_artikel, h_journal
        nonlocal hbline, hart, foart


        nonlocal t_h_bill, vat_list, hbline, hart, foart
        nonlocal t_h_bill_list, vat_list_list

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
                mwst = mwst + value_sign * decimal.Decimal(mesvalue) / 100
            elif mestoken == "NET":
                netto = netto + value_sign * decimal.Decimal(mesvalue) / 100
            elif mestoken == "AMT":
                betrag = betrag + value_sign * decimal.Decimal(mesvalue) / 100
            elif mestoken == "FAMT":
                fbetrag = fbetrag + value_sign * decimal.Decimal(mesvalue) / 100


    kellner = db_session.query(Kellner).filter(
            (Kellner._recid == rec_kellner)).first()

    h_bill = db_session.query(H_bill).filter(
            (H_bill._recid == rec_h_bill)).first()

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 271)).first()

    if htparam.feldtyp == 4:
        multi_vat = htparam.flogical
    billart = 0
    qty = 1
    amount = - amount
    amount_foreign = - amount_foreign

    if not double_currency:
        amount_foreign = amount / exchg_rate

    if amount != 0:

        artikel = db_session.query(Artikel).filter(
                (Artikel.artnr == kellner.kcredit_nr) &  (Artikel.departement == 0)).first()

        bill = db_session.query(Bill).filter(
                (Bill._recid == bilrecid)).first()

        if bill.rechnr == 0:

            counters = db_session.query(Counters).filter(
                    (Counters.counter_no == 3)).first()
            counters = counters + 1
            bill.rechnr = counters

            counters = db_session.query(Counters).first()
    update_bill_umsatz(value_sign)

    if double_currency:
        bill.mwst[98] = bill.mwst[98] + amount_foreign
    bill.rgdruck = 0
    vat_amount = cal_vat_amount()

    if multi_vat:
        create_vat_list(value_sign)

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
            bill_line.artnr = billart
            bill_line.bezeich = description
            bill_line.anzahl = 1
            bill_line.fremdwbetrag = vat_list.fbetrag
            bill_line.betrag = vat_list.betrag
            bill_line.nettobetrag = vat_list.netto
            bill_line.departement = h_bill.departement
            bill_line.epreis = 0
            bill_line.zeit = get_current_time_in_seconds()
            bill_line.userinit = user_init
            bill_line.bill_datum = bill_date
            bill_line.orts_tax = vat_list.vatamt
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

    h_bill = db_session.query(H_bill).first()

    bill = db_session.query(Bill).first()


    h_bill = db_session.query(H_bill).first()
    t_h_bill = T_h_bill()
    t_h_bill_list.append(t_h_bill)

    buffer_copy(h_bill, t_h_bill)
    t_h_bill.rec_id = h_bill._recid

    return generate_output()