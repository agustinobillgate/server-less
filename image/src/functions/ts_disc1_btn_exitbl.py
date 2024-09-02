from functions.additional_functions import *
import decimal
from datetime import date
from functions.calc_servtaxesbl import calc_servtaxesbl
from models import H_bill, H_artikel, Htparam, H_bill_line, H_umsatz, Umsatz, H_journal, Artikel, Arrangement, Argt_line, Billjournal

def ts_disc1_btn_exitbl(rec_id:int, billart:int, dept:int, transdate:date, amount:decimal, description:str, netto_betrag:decimal, exchg_rate:decimal, tischnr:int, curr_select:int, disc_value:decimal, qty:int, cancel_str:str, curr_waiter:int, procent:decimal, b_artnrfront:int, o_artnrfront:int, price_decimal:int, user_init:str, disc_list:[Disc_list], vat_list:[Vat_list], menu:[Menu]):
    h_bill = h_artikel = htparam = h_bill_line = h_umsatz = umsatz = h_journal = artikel = arrangement = argt_line = billjournal = None

    menu = disc_list = vat_list = artikel1 = hart = foart = vathtp = None

    menu_list, Menu = create_model("Menu", {"artnr":int, "anzahl":int, "departement":int, "prtflag":int, "pos":int, "bcolor":int, "epreis":decimal, "betrag":decimal, "fremdwbetrag":decimal, "bezeich":str, "bez0":str}, {"bcolor": 1})
    disc_list_list, Disc_list = create_model("Disc_list", {"h_artnr":int, "bezeich":str, "artnr":int, "mwst":int, "service":int, "umsatzart":int, "defaultflag":bool, "amount":decimal, "netto_amt":decimal, "service_amt":decimal, "mwst_amt":decimal})
    vat_list_list, Vat_list = create_model("Vat_list", {"artno":int, "vatproz":decimal, "vatamt":decimal, "netto":decimal, "betrag":decimal, "fbetrag":decimal})

    Artikel1 = Artikel
    Hart = H_artikel
    Foart = Artikel
    Vathtp = Htparam

    db_session = local_storage.db_session

    def generate_output():
        nonlocal h_bill, h_artikel, htparam, h_bill_line, h_umsatz, umsatz, h_journal, artikel, arrangement, argt_line, billjournal
        nonlocal artikel1, hart, foart, vathtp


        nonlocal menu, disc_list, vat_list, artikel1, hart, foart, vathtp
        nonlocal menu_list, disc_list_list, vat_list_list
        return {}

    def update_bill(h_artart:int, h_artnrfront:int):

        nonlocal h_bill, h_artikel, htparam, h_bill_line, h_umsatz, umsatz, h_journal, artikel, arrangement, argt_line, billjournal
        nonlocal artikel1, hart, foart, vathtp


        nonlocal menu, disc_list, vat_list, artikel1, hart, foart, vathtp
        nonlocal menu_list, disc_list_list, vat_list_list

        bill_date:date = None
        curr_time:int = 0
        vat_amount:decimal = 0
        separate_disc_flag:bool = False
        amount_list:decimal = 0
        amount_list = - amount

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 281)).first()

        if htparam.paramgruppe == 19:
            separate_disc_flag = htparam.flogical

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

        h_bill = db_session.query(H_bill).first()
        h_bill.saldo = h_bill.saldo + amount
        h_bill.rgdruck = 0
        vat_amount = cal_vat_amount()
        curr_time = get_current_time_in_seconds()

        if not separate_disc_flag:
            h_bill_line = H_bill_line()
            db_session.add(h_bill_line)

            h_bill_line.rechnr = h_bill.rechnr
            h_bill_line.artnr = billart
            h_bill_line.bezeich = description
            h_bill_line.anzahl = 1
            h_bill_line.nettobetrag = netto_betrag
            h_bill_line.betrag = round(amount, price_decimal)
            h_bill_line.fremdwbetrag = round(amount / exchg_rate, 2)
            h_bill_line.tischnr = tischnr
            h_bill_line.departement = h_bill.departement
            h_bill_line.zeit = curr_time
            h_bill_line.bill_datum = bill_date
            h_bill_line.waehrungsnr = curr_select

            if disc_value == 0:
                h_bill_line.epreis = netto_betrag

            h_bill_line = db_session.query(H_bill_line).first()

        for disc_list in query(disc_list_list, filters=(lambda disc_list :(disc_list.h_artnr == billart) or (disc_list.netto_amt != 0))):

            if disc_list.amount != 0:
                amount_list = amount_list + disc_list.amount

                if amount_list < 0:
                    disc_list.amount = disc_list.amount - amount_list

                if separate_disc_flag:
                    h_bill_line = H_bill_line()
                    db_session.add(h_bill_line)

                    h_bill_line.rechnr = h_bill.rechnr
                    h_bill_line.artnr = disc_list.h_artnr
                    h_bill_line.bezeich = disc_list.bezeich
                    h_bill_line.anzahl = 1
                    h_bill_line.nettobetrag = disc_list.netto_amt
                    h_bill_line.betrag = disc_list.amount
                    h_bill_line.fremdwbetrag = round(disc_list.amount / exchg_rate, price_decimal)
                    h_bill_line.tischnr = tischnr
                    h_bill_line.departement = h_bill.departement
                    h_bill_line.zeit = curr_time
                    h_bill_line.bill_datum = bill_date
                    h_bill_line.waehrungsnr = curr_select

                    h_bill_line = db_session.query(H_bill_line).first()

                h_umsatz = db_session.query(H_umsatz).filter(
                            (H_umsatz.artnr == disc_list.h_artnr) &  (H_umsatz.departement == dept) &  (H_umsatz.datum == bill_date)).first()

                if not h_umsatz:
                    h_umsatz = H_umsatz()
                    db_session.add(h_umsatz)

                    h_umsatz.artnr = disc_list.h_artnr
                    h_umsatz.datum = bill_date
                    h_umsatz.departement = dept


                h_umsatz.betrag = h_umsatz.betrag + round(disc_list.amount, price_decimal)
                h_umsatz.anzahl = h_umsatz.anzahl + qty

                h_umsatz = db_session.query(H_umsatz).first()

                umsatz = db_session.query(Umsatz).filter(
                            (Umsatz.artnr == disc_list.artnr) &  (Umsatz.departement == dept) &  (Umsatz.datum == bill_date)).first()

                if not umsatz:
                    umsatz = Umsatz()
                    db_session.add(umsatz)

                    umsatz.artnr = disc_list.artnr
                    umsatz.datum = bill_date
                    umsatz.departement = dept


                umsatz.betrag = umsatz.betrag + round(disc_list.amount, price_decimal)
                umsatz.anzahl = umsatz.anzahl + qty

                umsatz = db_session.query(Umsatz).first()
            h_journal = H_journal()
            db_session.add(h_journal)

            h_journal.rechnr = h_bill.rechnr
            h_journal.artnr = disc_list.h_artnr
            h_journal.anzahl = qty
            h_journal.betrag = round(disc_list.amount, price_decimal)
            h_journal.steuercode = vat_amount
            h_journal.bezeich = disc_list.bezeich
            h_journal.tischnr = tischnr
            h_journal.departement = h_bill.departement
            h_journal.zeit = curr_time
            h_journal.stornogrund = cancel_str
            h_journal.kellner_nr = curr_waiter
            h_journal.bill_datum = bill_date
            h_journal.artnrfront = h_artnrfront
            h_journal.aendertext = ""
            h_journal.artart = h_artart

            if disc_list.h_artnr == billart:
                h_journal.epreis = netto_betrag

                for vat_list in query(vat_list_list):
                    h_journal.aendertext = h_journal.aendertext +\
                            "VAT%," + to_string(vat_list.vatProz * 100) + ";" +\
                            "VAT," + to_string(vat_list.vatAmt * 100) + ";" +\
                            "NET," + to_string(vat_list.netto * 100) + ";" +\
                            "AMT," + to_string(vat_list.betrag * 100) + ";" +\
                            "FAMT," + to_string(vat_list.fbetrag * 100) + ";"

            h_journal = db_session.query(H_journal).first()

        cancel_str = ""

    def update_rev_argtart(h_artnrfront:int):

        nonlocal h_bill, h_artikel, htparam, h_bill_line, h_umsatz, umsatz, h_journal, artikel, arrangement, argt_line, billjournal
        nonlocal artikel1, hart, foart, vathtp


        nonlocal menu, disc_list, vat_list, artikel1, hart, foart, vathtp
        nonlocal menu_list, disc_list_list, vat_list_list

        amount:decimal = 0

        for menu in query(menu_list, filters=(lambda menu :MENU.prtflag == 1)):
            h_artikel = db_session.query(H_artikel).filter((H_artikel.artnr == MENU.artnr) &  (H_artikel.departement == h_bill.departement)).first()
            if not h_artikel:
                continue

            artikel = db_session.query(Artikel).filter((Artikel.artnr == h_Artikel.artnrfront) &  (Artikel.departement == h_Artikel.departement) &  (Artikel.artart == 9) &  (Artikel.artgrp != 0)).first()
            if not artikel:
                continue

            amount = - procent / 100 * MENU.betrag
            rev_bdown(h_artnrfront, menu.anzahl, amount)

    def rev_bdown(h_artnrfront:int, qty:int, amount:decimal):

        nonlocal h_bill, h_artikel, htparam, h_bill_line, h_umsatz, umsatz, h_journal, artikel, arrangement, argt_line, billjournal
        nonlocal artikel1, hart, foart, vathtp


        nonlocal menu, disc_list, vat_list, artikel1, hart, foart, vathtp
        nonlocal menu_list, disc_list_list, vat_list_list

        discart:int = 0
        bill_date:date = None
        rest_betrag:decimal = 0
        argt_betrag:decimal = 0
        Artikel1 = Artikel

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 110)).first()
        rest_betrag = amount
        bill_date = htparam.fdate

        if transdate != None:
            bill_date = transdate
        else:

            htparam = db_session.query(Htparam).filter(
                    (Htparam.paramnr == 253)).first()

            if htparam.flogical and bill_date < get_current_date():
                bill_date = bill_date + 1

        if artikel.umsatzart == 3 or artikel.umsatzart == 5:
            discart = h_artnrfront

        elif artikel.umsatzart == 6:

            if b_artnrfront != 0:
                discart = b_artnrfront
            else:
                discart = h_artnrfront
        else:

            if o_artnrfront != 0:
                discart = o_artnrfront
            else:
                discart = h_artnrfront

        umsatz = db_session.query(Umsatz).filter(
                (Umsatz.artnr == discart) &  (Umsatz.departement == artikel.departement) &  (Umsatz.datum == bill_date)).first()

        if not umsatz:
            umsatz = Umsatz()
            db_session.add(umsatz)

            umsatz.artnr = discart
            umsatz.datum = bill_date
            umsatz.departement = artikel.departement


        umsatz.betrag = umsatz.betrag - amount

        umsatz = db_session.query(Umsatz).first()
        rest_betrag = amount

        arrangement = db_session.query(Arrangement).filter(
                (Arrangement.argtnr == artikel.artgrp)).first()

        for argt_line in db_session.query(Argt_line).filter(
                (Argt_line.argtnr == arrangement.argtnr)).all():

            if argt_line.betrag != 0:
                argt_betrag = - procent / 100 * argt_line.betrag * qty
                argt_betrag = round(argt_betrag, price_decimal)
                rest_betrag = rest_betrag - argt_betrag


            else:
                argt_betrag = amount * argt_line.vt_percnt / 100
                argt_betrag = round(argt_betrag, price_decimal)
                rest_betrag = rest_betrag - argt_betrag

            artikel1 = db_session.query(Artikel1).filter(
                    (Artikel1.artnr == argt_line.argt_artnr) &  (Artikel1.departement == argt_line.departement)).first()

            umsatz = db_session.query(Umsatz).filter(
                    (Umsatz.artnr == argt_line.argt_artnr) &  (Umsatz.departement == argt_line.departement) &  (Umsatz.datum == bill_date)).first()

            if not umsatz:
                umsatz = Umsatz()
                db_session.add(umsatz)

                umsatz.artnr = argt_line.argt_artnr
                umsatz.datum = bill_date
                umsatz.departement = argt_line.departement


            umsatz.betrag = umsatz.betrag + argt_betrag

            umsatz = db_session.query(Umsatz).first()
            billjournal = Billjournal()
            db_session.add(billjournal)

            billjournal.rechnr = h_bill.rechnr
            billjournal.artnr = artikel1.artnr
            billjournal.anzahl = 1
            billjournal.fremdwaehrng = argt_line.betrag
            billjournal.betrag = argt_betrag
            billjournal.bezeich = artikel1.bezeich +\
                    "<" + to_string(h_bill.departement, "99") + ">"
            billjournal.departement = artikel1.departement
            billjournal.epreis = 0
            billjournal.zeit = get_current_time_in_seconds()
            billjournal.userinit = user_init
            billjournal.bill_datum = bill_date

            billjournal = db_session.query(Billjournal).first()

        artikel1 = db_session.query(Artikel1).filter(
                (Artikel1.artnr == arrangement.artnr_logis) &  (Artikel1.departement == arrangement.intervall)).first()

        umsatz = db_session.query(Umsatz).filter(
                (Umsatz.artnr == artikel1.artnr) &  (Umsatz.departement == artikel1.departement) &  (Umsatz.datum == bill_date)).first()

        if not umsatz:
            umsatz = Umsatz()
            db_session.add(umsatz)

            umsatz.artnr = artikel1.artnr
            umsatz.datum = bill_date
            umsatz.departement = artikel1.departement


        umsatz.betrag = umsatz.betrag + rest_betrag

        umsatz = db_session.query(Umsatz).first()
        billjournal = Billjournal()
        db_session.add(billjournal)

        billjournal.rechnr = h_bill.rechnr
        billjournal.artnr = artikel1.artnr
        billjournal.anzahl = 1
        billjournal.betrag = rest_betrag
        billjournal.bezeich = artikel1.bezeich +\
                "<" + to_string(h_bill.departement, "99") + ">"
        billjournal.departement = artikel1.departement
        billjournal.epreis = 0
        billjournal.zeit = get_current_time_in_seconds()
        billjournal.userinit = user_init
        billjournal.bill_datum = bill_date

        billjournal = db_session.query(Billjournal).first()

    def cal_vat_amount():

        nonlocal h_bill, h_artikel, htparam, h_bill_line, h_umsatz, umsatz, h_journal, artikel, arrangement, argt_line, billjournal
        nonlocal artikel1, hart, foart, vathtp


        nonlocal menu, disc_list, vat_list, artikel1, hart, foart, vathtp
        nonlocal menu_list, disc_list_list, vat_list_list

        mwst = 0
        h_service:decimal = 0
        h_mwst:decimal = 0
        vat2:decimal = 0
        fact:decimal = 0
        fact1:decimal = 0
        qty:decimal = 0
        unit_price:decimal = 0
        menu_amt:decimal = 0
        famount:decimal = 0
        incl_mwst:bool = False
        anz_vat:int = 0

        def generate_inner_output():
            return mwst
        Hart = H_artikel
        Foart = Artikel
        Vathtp = Htparam
        vat_list_list.clear()

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 134)).first()
        incl_mwst = htparam.flogical
        famount = round(amount / exchg_rate, 2)

        for menu in query(menu_list, filters=(lambda menu :MENU.prtflag == 1)):

            hart = db_session.query(Hart).filter(
                    (Hart.artnr == MENU.artnr) &  (Hart.departement == MENU.departement) &  (Hart.artart == 0)).first()

            foart = db_session.query(Foart).filter(
                    (Foart.artnr == hart.artnrfront) &  (Foart.departement == hart.departement)).first()
            h_service = 0
            h_mwst = 0
            fact = 1
            qty = MENU.anzahl

            if qty < 0:
                qty = - qty


            if incl_mwst:
                h_service, h_mwst, vat2, fact = get_output(calc_servtaxesbl(1, foart.artnr, foart.departement, None))
                h_mwst = h_mwst + vat2


            menu_amt = MENU.epreis * qty

            if MENU.betrag > 0 and menu_amt < 0:
                menu_amt = - menu_amt

            elif MENU.betrag < 0 and menu_amt > 0:
                menu_amt = - menu_amt
            unit_price = MENU.epreis

            if incl_mwst:

                if qty != 0:
                    unit_price = (MENU.betrag / qty) / fact
                else:
                    unit_price = MENU.epreis / fact
                unit_price = round(unit_price, price_decimal)
            h_service = round(h_service * unit_price, price_decimal)
            h_mwst = round(h_mwst * unit_price, price_decimal)

            if h_service == 0 and h_mwst == 0:
                1

            elif not incl_mwst:

                if h_service == 0:
                    h_mwst = MENU.betrag - menu_amt

            if MENU.betrag > 0 and h_mwst < 0:
                h_mwst = - h_mwst

            elif MENU.betrag < 0 and h_mwst > 0:
                h_mwst = - h_mwst
            mwst = mwst - h_mwst

            if h_mwst != 0 and vathtp:

                vat_list = query(vat_list_list, filters=(lambda vat_list :vat_list.artNo == foart.artnr), first=True)

                if not vat_list:
                    vat_list = Vat_list()
                    vat_list_list.append(vat_list)

                    vat_list.artNo = foart.artnr

                    if vathtp:
                        vat_list.vatProz = vathtp.fdecimal
                vat_list.vatamt = vat_list.vatamt - h_mwst * procent / 100
                vat_list.betrag = vat_list.betrag - MENU.betrag * procent / 100


        mwst = mwst * procent / 100

        for vat_list in query(vat_list_list):
            vat_list.vatAmt = round(vat_list.vatAmt, price_decimal)
            vat_list.netto = vat_list.betrag - vat_list.vatAmt
            vat_list.fbetrag = round(vat_list.betrag / exchg_rate, 2)


        return generate_inner_output()

    h_bill = db_session.query(H_bill).filter(
            (H_bill._recid == rec_id)).first()

    h_artikel = db_session.query(H_artikel).filter(
            (H_artikel.artnr == billart) &  (H_artikel.departement == dept)).first()
    update_bill(h_artikel.artart, h_artikel.artnrfront)
    update_rev_argtart(h_artikel.artnrfront)

    return generate_output()