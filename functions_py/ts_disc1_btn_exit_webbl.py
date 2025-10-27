#using conversion tools version: 1.0.0.117
# pyright: reportAttributeAccessIssue=false

"""_yusufwijasena_21/10/2025

    TicketID: 
        _issue_:    - change import from function to function_py
                    - fix python indentation
                    - fix var initialization
"""

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from functions_py.calc_servtaxesbl import calc_servtaxesbl
from models import H_bill, H_artikel, Htparam, H_bill_line, H_umsatz, Umsatz, H_journal, Artikel, Arrangement, Argt_line, Billjournal

disc_list_data, Disc_list = create_model("Disc_list", {"h_artnr":int, "bezeich":str, "artnr":int, "mwst":int, "service":int, "umsatzart":int, "defaultflag":bool, "amount":Decimal, "netto_amt":Decimal, "service_amt":Decimal, "mwst_amt":Decimal})
vat_list_data, Vat_list = create_model("Vat_list", {"artno":int, "vatproz":Decimal, "vatamt":Decimal, "netto":Decimal, "betrag":Decimal, "fbetrag":Decimal})
payload_list_data, Payload_list = create_model("Payload_list", {"voucher_number":str})
menu_data, Menu = create_model("Menu", {"artnr":int, "anzahl":int, "departement":int, "prtflag":int, "pos":int, "bcolor":int, "epreis":Decimal, "betrag":Decimal, "fremdwbetrag":Decimal, "bezeich":str, "bez0":str}, {"bcolor": 1})

def ts_disc1_btn_exit_webbl(rec_id:int, billart:int, dept:int, transdate:date, amount:Decimal, description:str, netto_betrag:Decimal, exchg_rate:Decimal, tischnr:int, curr_select:int, disc_value:Decimal, qty:int, cancel_str:str, curr_waiter:int, procent:Decimal, b_artnrfront:int, o_artnrfront:int, price_decimal:int, user_init:str, disc_list_data:Disc_list, vat_list_data:Vat_list, payload_list_data:Payload_list, menu_data:Menu):

    prepare_cache ([H_bill, H_artikel, Htparam, H_bill_line, H_umsatz, Umsatz, H_journal, Artikel, Arrangement, Argt_line, Billjournal])

    h_bill = h_artikel = htparam = h_bill_line = h_umsatz = umsatz = h_journal = artikel = arrangement = argt_line = billjournal = None

    menu = disc_list = vat_list = payload_list = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal h_bill, h_artikel, htparam, h_bill_line, h_umsatz, umsatz, h_journal, artikel, arrangement, argt_line, billjournal
        nonlocal rec_id, billart, dept, transdate, amount, description, netto_betrag, exchg_rate, tischnr, curr_select, disc_value, qty, cancel_str, curr_waiter, procent, b_artnrfront, o_artnrfront, price_decimal, user_init
        nonlocal menu, disc_list, vat_list, payload_list

        return {}

    def update_bill(h_artart:int, h_artnrfront:int):
        nonlocal h_bill, h_artikel, htparam, h_bill_line, h_umsatz, umsatz, h_journal, artikel, arrangement, argt_line, billjournal
        nonlocal rec_id, billart, dept, transdate, amount, description, netto_betrag, exchg_rate, tischnr, curr_select, disc_value, qty, cancel_str, curr_waiter, procent, b_artnrfront, o_artnrfront, price_decimal, user_init
        nonlocal menu, disc_list, vat_list, payload_list

        bill_date:date 
        curr_time:int = 0
        vat_amount:Decimal = to_decimal("0.0")
        separate_disc_flag:bool = False
        amount_list:Decimal = to_decimal("0.0")
        desc_bill:str = ""
        amount_list =  - (to_decimal(amount))

        htparam = get_cache (Htparam, {"paramnr": [(eq, 281)]})

        if htparam.paramgruppe == 19:
            separate_disc_flag = htparam.flogical

        htparam = get_cache (Htparam, {"paramnr": [(eq, 110)]})
        bill_date = htparam.fdate

        if transdate != None:
            bill_date = transdate
        else:

            htparam = get_cache (Htparam, {"paramnr": [(eq, 253)]})

            if htparam.flogical and bill_date < get_current_date():
                bill_date = bill_date + timedelta(days=1)
        pass
        h_bill.saldo =  to_decimal(h_bill.saldo + amount)
        h_bill.rgdruck = 0
        vat_amount = cal_vat_amount()
        curr_time = get_current_time_in_seconds()

        if not separate_disc_flag:

            if trim(payload_list.voucher_number) != "":
                desc_bill = trim(description) + " " + "/" + " " + payload_list.voucher_number
            else:
                desc_bill = description
            h_bill_line = H_bill_line()

            h_bill_line.rechnr = h_bill.rechnr
            h_bill_line.artnr = billart
            h_bill_line.bezeich = desc_bill
            h_bill_line.anzahl = 1
            h_bill_line.nettobetrag =  to_decimal(netto_betrag)
            h_bill_line.betrag = to_decimal(round(amount , price_decimal))
            h_bill_line.fremdwbetrag = to_decimal(round(amount / exchg_rate , 2))
            h_bill_line.tischnr = tischnr
            h_bill_line.departement = h_bill.departement
            h_bill_line.zeit = curr_time
            h_bill_line.bill_datum = bill_date
            h_bill_line.waehrungsnr = curr_select

            db_session.add(h_bill_line)

            if disc_value == 0:
                h_bill_line.epreis =  to_decimal(netto_betrag)
            pass

        if trim(payload_list.voucher_number) != "":
            desc_bill = " " + "/" + " " + payload_list.voucher_number
        else:
            desc_bill = ""

        for disc_list in query(disc_list_data, filters=(lambda disc_list:(disc_list.h_artnr == billart) or (disc_list.netto_amt != 0))):

            if disc_list.amount != 0:

                if procent > 0:
                    amount_list =  to_decimal(amount_list + disc_list.amount)

                    if amount_list < 0:
                        disc_list.amount =  to_decimal(disc_list.amount - amount_list)

                if separate_disc_flag:
                    h_bill_line = H_bill_line()

                    h_bill_line.rechnr = h_bill.rechnr
                    h_bill_line.artnr = disc_list.h_artnr
                    h_bill_line.bezeich = disc_list.bezeich
                    h_bill_line.anzahl = 1
                    h_bill_line.nettobetrag =  to_decimal(disc_list.netto_amt)
                    h_bill_line.betrag =  to_decimal(disc_list.amount)
                    h_bill_line.fremdwbetrag = to_decimal(round(disc_list.amount / exchg_rate , price_decimal))
                    h_bill_line.tischnr = tischnr
                    h_bill_line.departement = h_bill.departement
                    h_bill_line.zeit = curr_time
                    h_bill_line.bill_datum = bill_date
                    h_bill_line.waehrungsnr = curr_select

                    db_session.add(h_bill_line)

                    pass

                h_umsatz = get_cache (H_umsatz, {
                    "artnr": [(eq, disc_list.h_artnr)],
                    "departement": [(eq, dept)],
                    "datum": [(eq, bill_date)]})

                if not h_umsatz:
                    h_umsatz = H_umsatz()

                    h_umsatz.artnr = disc_list.h_artnr
                    h_umsatz.datum = bill_date
                    h_umsatz.departement = dept

                    db_session.add(h_umsatz)

                h_umsatz.betrag = to_decimal(h_umsatz.betrag + round(disc_list.amount , price_decimal))
                h_umsatz.anzahl = h_umsatz.anzahl + qty


                pass

                umsatz = get_cache (Umsatz, {
                    "artnr": [(eq, disc_list.artnr)],
                    "departement": [(eq, dept)],
                    "datum": [(eq, bill_date)]})

                if not umsatz:
                    umsatz = Umsatz()

                    umsatz.artnr = disc_list.artnr
                    umsatz.datum = bill_date
                    umsatz.departement = dept

                    db_session.add(umsatz)

                umsatz.betrag = to_decimal(umsatz.betrag + round(disc_list.amount , price_decimal))
                umsatz.anzahl = umsatz.anzahl + qty


                pass
            h_journal = H_journal()

            h_journal.rechnr = h_bill.rechnr
            h_journal.artnr = disc_list.h_artnr
            h_journal.anzahl = qty
            h_journal.betrag = to_decimal(round(disc_list.amount , price_decimal))
            h_journal.steuercode = vat_amount
            h_journal.bezeich = disc_list.bezeich + desc_bill
            h_journal.tischnr = tischnr
            h_journal.departement = h_bill.departement
            h_journal.zeit = curr_time
            h_journal.stornogrund = cancel_str
            h_journal.kellner_nr = curr_waiter
            h_journal.bill_datum = bill_date
            h_journal.artnrfront = h_artnrfront
            h_journal.aendertext = ""
            h_journal.artart = h_artart

            db_session.add(h_journal)

            if disc_list.h_artnr == billart:
                h_journal.epreis =  to_decimal(netto_betrag)

                for vat_list in query(vat_list_data):
                    h_journal.aendertext = h_journal.aendertext +\
                            "VAT%," + to_string(vat_list.vatProz * 100) + ";" +\
                            "VAT," + to_string(vat_list.vatAmt * 100) + ";" +\
                            "NET," + to_string(vat_list.netto * 100) + ";" +\
                            "AMT," + to_string(vat_list.betrag * 100) + ";" +\
                            "FAMT," + to_string(vat_list.fbetrag * 100) + ";"

            pass
        cancel_str = ""

    def update_rev_argtart(h_artnrfront:int):
        nonlocal h_bill, h_artikel, htparam, h_bill_line, h_umsatz, umsatz, h_journal, artikel, arrangement, argt_line, billjournal
        nonlocal rec_id, billart, dept, transdate, description, netto_betrag, exchg_rate, tischnr, curr_select, disc_value, qty, cancel_str, curr_waiter, procent, b_artnrfront, o_artnrfront, price_decimal, user_init
        nonlocal menu, disc_list, vat_list, payload_list

        amount:Decimal = to_decimal("0.0")

        h_artikel_obj_list = {}
        for h_artikel, artikel in db_session.query(H_artikel, Artikel).join(Artikel,(Artikel.artnr == H_artikel.artnrfront) & (Artikel.departement == H_artikel.departement) & (Artikel.artart == 9) & (Artikel.artgrp != 0)).filter(
            ((H_artikel.artnr.in_(list(set([menu.artnr for menu in menu_data if menu.prtflag == 1])))) & (H_artikel.departement == h_bill.departement))).order_by(H_artikel._recid).all():
            if h_artikel_obj_list.get(h_artikel._recid):
                continue
            else:
                h_artikel_obj_list[h_artikel._recid] = True

            menu = query(menu_data, (lambda menu: (h_artikel.artnr == menu.artnr)), first=True)
            amount =  - (to_decimal(procent) / to_decimal("100") * to_decimal(menu.betrag))
            rev_bdown(h_artnrfront, menu.anzahl, amount)


    def rev_bdown(h_artnrfront:int, qty:int, amount:Decimal):
        nonlocal h_bill, h_artikel, htparam, h_bill_line, h_umsatz, umsatz, h_journal, artikel, arrangement, argt_line, billjournal
        nonlocal rec_id, billart, dept, transdate, description, netto_betrag, exchg_rate, tischnr, curr_select, disc_value, cancel_str, curr_waiter, procent, b_artnrfront, o_artnrfront, price_decimal, user_init
        nonlocal menu, disc_list, vat_list, payload_list

        discart:int = 0
        bill_date:date 
        rest_betrag:Decimal = to_decimal("0.0")
        argt_betrag:Decimal = to_decimal("0.0")
        artikel1 = None
        Artikel1 =  create_buffer("Artikel1",Artikel)

        htparam = get_cache (Htparam, {"paramnr": [(eq, 110)]})
        rest_betrag =  to_decimal(amount)
        bill_date = htparam.fdate

        if transdate != None:
            bill_date = transdate
        else:

            htparam = get_cache (Htparam, {"paramnr": [(eq, 253)]})

            if htparam.flogical and bill_date < get_current_date():
                bill_date = bill_date + timedelta(days=1)

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

        umsatz = get_cache (Umsatz, {
            "artnr": [(eq, discart)],
            "departement": [(eq, artikel.departement)],
            "datum": [(eq, bill_date)]})

        if not umsatz:
            umsatz = Umsatz()

            umsatz.artnr = discart
            umsatz.datum = bill_date
            umsatz.departement = artikel.departement

            db_session.add(umsatz)

        umsatz.betrag =  to_decimal(umsatz.betrag - amount)

        rest_betrag =  to_decimal(amount)

        arrangement = get_cache (Arrangement, {
            "argtnr": [(eq, artikel.artgrp)]})

        for argt_line in db_session.query(Argt_line).filter(
                 (Argt_line.argtnr == arrangement.argtnr)).order_by(Argt_line._recid).all():

            if argt_line.betrag != 0:
                argt_betrag =  - (to_decimal(procent) / to_decimal("100") * to_decimal(argt_line.betrag) * to_decimal(qty))
                argt_betrag =  to_decimal(round(argt_betrag , price_decimal))
                rest_betrag =  to_decimal(rest_betrag - argt_betrag)


            else:
                argt_betrag =  to_decimal(amount) * to_decimal(argt_line.vt_percnt) / to_decimal("100")
                argt_betrag =  to_decimal(round(argt_betrag , price_decimal))
                rest_betrag =  to_decimal(rest_betrag - argt_betrag)

            artikel1 = get_cache (Artikel, {
                "artnr": [(eq, argt_line.argt_artnr)],
                "departement": [(eq, argt_line.departement)]})

            umsatz = get_cache (Umsatz, {
                "artnr": [(eq, argt_line.argt_artnr)],
                "departement": [(eq, argt_line.departement)],
                "datum": [(eq, bill_date)]})

            if not umsatz:
                umsatz = Umsatz()

                umsatz.artnr = argt_line.argt_artnr
                umsatz.datum = bill_date
                umsatz.departement = argt_line.departement

                db_session.add(umsatz)

            umsatz.betrag =  to_decimal(umsatz.betrag + argt_betrag)

            billjournal = Billjournal()

            billjournal.rechnr = h_bill.rechnr
            billjournal.artnr = artikel1.artnr
            billjournal.anzahl = 1
            billjournal.fremdwaehrng =  to_decimal(argt_line.betrag)
            billjournal.betrag =  to_decimal(argt_betrag)
            billjournal.bezeich = artikel1.bezeich + "<" + to_string(h_bill.departement, "99") + ">"
            billjournal.departement = artikel1.departement
            billjournal.epreis =  to_decimal("0")
            billjournal.zeit = get_current_time_in_seconds()
            billjournal.userinit = user_init
            billjournal.bill_datum = bill_date

            db_session.add(billjournal)

            pass

        artikel1 = get_cache (Artikel, {
            "artnr": [(eq, arrangement.artnr_logis)],
            "departement": [(eq, arrangement.intervall)]})

        umsatz = get_cache (Umsatz, {
            "artnr": [(eq, artikel1.artnr)],
            "departement": [(eq, artikel1.departement)],
            "datum": [(eq, bill_date)]})

        if not umsatz:
            umsatz = Umsatz()

            umsatz.artnr = artikel1.artnr
            umsatz.datum = bill_date
            umsatz.departement = artikel1.departement

            db_session.add(umsatz)

        umsatz.betrag =  to_decimal(umsatz.betrag + rest_betrag)


        billjournal = Billjournal()

        billjournal.rechnr = h_bill.rechnr
        billjournal.artnr = artikel1.artnr
        billjournal.anzahl = 1
        billjournal.betrag =  to_decimal(rest_betrag)
        billjournal.bezeich = artikel1.bezeich + "<" + to_string(h_bill.departement, "99") + ">"
        billjournal.departement = artikel1.departement
        billjournal.epreis =  to_decimal("0.0")
        billjournal.zeit = get_current_time_in_seconds()
        billjournal.userinit = user_init
        billjournal.bill_datum = bill_date

        db_session.add(billjournal)

        pass


    def cal_vat_amount():
        nonlocal h_bill, h_artikel, htparam, h_bill_line, h_umsatz, umsatz, h_journal, artikel, arrangement, argt_line, billjournal
        nonlocal rec_id, billart, dept, transdate, amount, description, netto_betrag, exchg_rate, tischnr, curr_select, disc_value, cancel_str, curr_waiter, procent, b_artnrfront, o_artnrfront, price_decimal, user_init
        nonlocal menu, disc_list, vat_list, payload_list

        mwst = to_decimal("0.0")
        h_service:Decimal = to_decimal("0.0")
        h_mwst:Decimal = to_decimal("0.0")
        vat2:Decimal = to_decimal("0.0")
        fact:Decimal = to_decimal("0.0")
        fact1:Decimal = to_decimal("0.0")
        qty:Decimal = to_decimal("0.0")
        unit_price:Decimal = to_decimal("0.0")
        menu_amt:Decimal = to_decimal("0.0")
        famount:Decimal = to_decimal("0.0")
        incl_mwst:bool = False
        anz_vat:int = 0
        hart = None
        foart = None
        vathtp = None

        def generate_inner_output():
            return (mwst)

        Hart =  create_buffer("Hart",H_artikel)
        Foart =  create_buffer("Foart",Artikel)
        Vathtp =  create_buffer("Vathtp",Htparam)
        vat_list_data.clear()

        htparam = get_cache (Htparam, {
            "paramnr": [(eq, 134)]})
        incl_mwst = htparam.flogical
        famount = to_decimal(round(amount / exchg_rate , 2))

        for menu in query(menu_data, filters=(lambda menu: menu.menu.prtflag == 1)):

            hart = get_cache (H_artikel, {
                "artnr": [(eq, menu.artnr)],
                "departement": [(eq, menu.departement)],
                "artart": [(eq, 0)]})

            foart = get_cache (Artikel, {
                "artnr": [(eq, hart.artnrfront)],
                "departement": [(eq, hart.departement)]})
            h_service =  to_decimal("0")
            h_mwst =  to_decimal("0")
            fact =  to_decimal("1")
            qty =  to_decimal(menu.anzahl)

            if qty < 0:
                qty =  - (to_decimal(qty))
            pass

            if incl_mwst:
                h_service, h_mwst, vat2, fact = get_output(calc_servtaxesbl(1, foart.artnr, foart.departement, None))
                h_mwst =  to_decimal(h_mwst + vat2)


            menu_amt =  to_decimal(menu.epreis * qty)

            if menu.betrag > 0 and menu_amt < 0:
                menu_amt =  - (to_decimal(menu_amt))

            elif menu.betrag < 0 and menu_amt > 0:
                menu_amt =  - (to_decimal(menu_amt))
            unit_price =  to_decimal(menu.epreis)

            if incl_mwst:

                if qty != 0:
                    unit_price = to_decimal((menu.betrag / qty) / fact)
                else:
                    unit_price =  to_decimal(menu.epreis / fact)
                unit_price = to_decimal(round(unit_price , price_decimal))
            h_service = to_decimal(round(h_service * unit_price , price_decimal))
            h_mwst = to_decimal(round(h_mwst * unit_price , price_decimal))

            if h_service == 0 and h_mwst == 0:
                pass

            elif not incl_mwst:

                if h_service == 0:
                    h_mwst =  to_decimal(menu.betrag - menu_amt)

            if menu.betrag > 0 and h_mwst < 0:
                h_mwst =  - (to_decimal(h_mwst))

            elif menu.betrag < 0 and h_mwst > 0:
                h_mwst =  - (to_decimal(h_mwst))
            mwst =  to_decimal(mwst - h_mwst)

            if h_mwst != 0 and vathtp:

                vat_list = query(vat_list_data, filters=(lambda vat_list: vat_list.artNo == foart.artnr), first=True)

                if not vat_list:
                    vat_list = Vat_list()
                    vat_list_data.append(vat_list)

                    vat_list.artno = foart.artnr

                    if vathtp:
                        vat_list.vatproz =  to_decimal(vathtp.fdecimal)
                vat_list.vatamt =  to_decimal(vat_list.vatamt - h_mwst * procent) / to_decimal("100")
                vat_list.betrag =  to_decimal(vat_list.betrag - menu.betrag * procent) / to_decimal("100")


        mwst =  to_decimal(mwst * procent) / to_decimal("100")

        for vat_list in query(vat_list_data):
            vat_list.vatamt = to_decimal(round(vat_list.vatAmt , price_decimal))
            vat_list.netto =  to_decimal(vat_list.betrag - vat_list.vatAmt)
            vat_list.fbetrag = to_decimal(round(vat_list.betrag / exchg_rate , 2))

        return generate_inner_output()

    payload_list = query(payload_list_data, first=True)

    h_bill = get_cache (H_bill, {
        "_recid": [(eq, rec_id)]})

    h_artikel = get_cache (H_artikel, {
        "artnr": [(eq, billart)],
        "departement": [(eq, dept)]})
    update_bill(h_artikel.artart, h_artikel.artnrfront)
    update_rev_argtart(h_artikel.artnrfront)

    return generate_output()