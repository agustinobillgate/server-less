#using conversion tools version: 1.0.0.117
#------------------------------------------
# Rd, 24/11/2025, Update last counter 
#------------------------------------------
from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from functions.rest_addgastinfo import rest_addgastinfo
from functions.ts_splitbill_update_billbl import ts_splitbill_update_billbl
from functions.calc_servtaxesbl import calc_servtaxesbl
from models import H_bill_line, Kellner, H_bill, Bill, H_artikel, Counters, Htparam, Artikel, Bill_line, Billjournal, H_journal, Queasy
from sqlalchemy.orm import flag_modified

def ts_splitbill_btn_transfer_paytypegt1bl(rec_id_h_bill:int, bilrecid:int, curr_select:int, multi_vat:bool, balance:Decimal, 
                                           pay_type:int, transdate:date, price_decimal:int, exchg_rate:Decimal, foreign_rate:bool, 
                                           dept:int, change_str:string, add_zeit:int, hoga_card:string, cancel_str:string, 
                                           curr_waiter:int, curr_room:string, user_init:string, cc_comment:string, guestnr:int, 
                                           tischnr:int, double_currency:bool, amount_foreign:Decimal):

    prepare_cache ([Kellner, H_bill, Bill, H_artikel, Counters, Htparam, Artikel, Bill_line, Billjournal, H_journal])

    err_flag = 0
    billart = 0
    qty = 0
    price = to_decimal("0.0")
    amount = to_decimal("0.0")
    description = ""
    bill_date = None
    fl_code = 0
    t_h_bill_line_data = []
    bname:string = ""
    payment_found:bool = False
    h_bill_line = kellner = h_bill = bill = h_artikel = counters = htparam = artikel = bill_line = billjournal = h_journal = queasy = None

    vat_list = t_h_bill_line = kellner1 = None

    vat_list_data, Vat_list = create_model("Vat_list", {"vatproz":Decimal, "vatamt":Decimal, "netto":Decimal, "betrag":Decimal, "fbetrag":Decimal})
    t_h_bill_line_data, T_h_bill_line = create_model_like(H_bill_line, {"rec_id":int})

    Kellner1 = create_buffer("Kellner1",Kellner)

    db_session = local_storage.db_session
    change_str = change_str.strip()
    hoga_card = hoga_card.strip()
    cancel_str = cancel_str.strip()
    curr_room = curr_room.strip()
    cc_comment = cc_comment.strip()


    def generate_output():
        nonlocal err_flag, billart, qty, price, amount, description, bill_date, fl_code, t_h_bill_line_data, bname, payment_found, h_bill_line, kellner, h_bill, bill, h_artikel, counters, htparam, artikel, bill_line, billjournal, h_journal, queasy
        nonlocal rec_id_h_bill, bilrecid, curr_select, multi_vat, balance, pay_type, transdate, price_decimal, exchg_rate, foreign_rate, dept, change_str, add_zeit, hoga_card, cancel_str, curr_waiter, curr_room, user_init, cc_comment, guestnr, tischnr, double_currency, amount_foreign
        nonlocal kellner1


        nonlocal vat_list, t_h_bill_line, kellner1
        nonlocal vat_list_data, t_h_bill_line_data

        return {"amount_foreign": amount_foreign, "err_flag": err_flag, "billart": billart, "qty": qty, "price": price, "amount": amount, "description": description, "bill_date": bill_date, "fl_code": fl_code, "t-h-bill-line": t_h_bill_line_data}

    def update_bill1():

        nonlocal err_flag, billart, qty, price, amount, description, bill_date, fl_code, t_h_bill_line_data, bname, payment_found, h_bill_line, kellner, h_bill, bill, h_artikel, counters, htparam, artikel, bill_line, billjournal, h_journal, queasy
        nonlocal rec_id_h_bill, bilrecid, curr_select, multi_vat, balance, pay_type, transdate, price_decimal, exchg_rate, foreign_rate, dept, change_str, add_zeit, hoga_card, cancel_str, curr_waiter, curr_room, user_init, cc_comment, guestnr, tischnr, double_currency, amount_foreign
        nonlocal kellner1


        nonlocal vat_list, t_h_bill_line, kellner1
        nonlocal vat_list_data, t_h_bill_line_data

        vat_amount:Decimal = to_decimal("0.0")

        htparam = get_cache (Htparam, {"paramnr": [(eq, 110)]})
        bill_date = htparam.fdate

        if transdate != None:
            bill_date = transdate
        else:

            htparam = get_cache (Htparam, {"paramnr": [(eq, 253)]})

            if htparam.flogical and bill_date < get_current_date():
                bill_date = bill_date + timedelta(days=1)
        billart = 0
        qty = 1
        amount =  - to_decimal(amount)
        amount_foreign =  - to_decimal(amount_foreign)

        if not double_currency:
            amount_foreign =  to_decimal(amount) / to_decimal(exchg_rate)

        if amount != 0:

            kellner1 = get_cache (Kellner, {"kellner_nr": [(eq, h_bill.kellner_nr)],"departement": [(eq, h_bill.departement)]})

            artikel = get_cache (Artikel, {"artnr": [(eq, kellner1.kcredit_nr)],"departement": [(eq, 0)]})

            # bill = get_cache (Bill, {"_recid": [(eq, bilrecid)]})
            bill = db_session.query(Bill).filter(Bill._recid == bilrecid).with_for_update().first()

            if bill.rechnr == 0:

                # counters = get_cache (Counters, {"counter_no": [(eq, 3)]})
                counters = db_session.query(Counters).filter(Counters.counter_no == 3).with_for_update().first()
                counters.counter = counters.counter + 1
                bill.rechnr = counters.counter

                pass
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

                for vat_list in query(vat_list_data):

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
                    bill_line.anzahl = 1
                    bill_line.fremdwbetrag =  to_decimal(vat_list.fbetrag)
                    bill_line.betrag =  to_decimal(vat_list.betrag)
                    bill_line.nettobetrag =  to_decimal(vat_list.netto)
                    bill_line.departement = dept
                    bill_line.epreis =  to_decimal("0")
                    bill_line.zeit = get_current_time_in_seconds()
                    bill_line.userinit = user_init
                    bill_line.bill_datum = bill_date
                    bill_line.orts_tax =  to_decimal(vat_list.vatAmt)
                    bill_line.waehrungsnr = curr_select
                    bill_line.origin_id = "VAT%," + to_string(vat_list.vatproz * 100) + ";" +\
                            "VAT," + to_string(vat_list.vatAmt * 100) + ";" +\
                            "NET," + to_string(vat_list.netto * 100) + ";"


                    pass
                    billjournal = Billjournal()
                    db_session.add(billjournal)

                    billjournal.rechnr = bill.rechnr
                    billjournal.zinr = bill.zinr
                    billjournal.artnr = billart
                    billjournal.anzahl = 1
                    billjournal.fremdwaehrng =  to_decimal(vat_list.fbetrag)
                    billjournal.betrag =  to_decimal(vat_list.betrag)
                    billjournal.bezeich = description
                    billjournal.departement = dept
                    billjournal.epreis =  to_decimal("0")
                    billjournal.zeit = get_current_time_in_seconds()
                    billjournal.stornogrund = ""
                    billjournal.userinit = user_init
                    billjournal.bill_datum = bill_date

                    if artikel:
                        billjournal.departement = artikel.departement
                    pass

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
                bill_line.anzahl = 1
                bill_line.fremdwbetrag =  to_decimal(amount_foreign)
                bill_line.betrag =  to_decimal(amount)
                bill_line.departement = dept
                bill_line.epreis =  to_decimal("0")
                bill_line.zeit = get_current_time_in_seconds()
                bill_line.userinit = user_init
                bill_line.bill_datum = bill_date
                bill_line.orts_tax =  to_decimal(vat_amount)
                bill_line.waehrungsnr = curr_select


                pass
                billjournal = Billjournal()
                db_session.add(billjournal)

                billjournal.rechnr = bill.rechnr
                billjournal.zinr = bill.zinr
                billjournal.artnr = billart
                billjournal.anzahl = 1
                billjournal.fremdwaehrng =  to_decimal(amount_foreign)
                billjournal.betrag =  to_decimal(amount)
                billjournal.bezeich = description
                billjournal.departement = dept
                billjournal.epreis =  to_decimal("0")
                billjournal.zeit = get_current_time_in_seconds()
                billjournal.stornogrund = ""
                billjournal.userinit = user_init
                billjournal.bill_datum = bill_date

                if artikel:
                    billjournal.departement = artikel.departement
                pass
            pass
            amount =  - to_decimal(amount)
        flag_modified(bill, "mwst")


    def create_vat_list():

        nonlocal err_flag, billart, qty, price, amount, description, bill_date, fl_code, t_h_bill_line_data, bname, payment_found, h_bill_line, kellner, h_bill, bill, h_artikel, counters, htparam, artikel, bill_line, billjournal, h_journal, queasy
        nonlocal rec_id_h_bill, bilrecid, curr_select, multi_vat, balance, pay_type, transdate, price_decimal, exchg_rate, foreign_rate, dept, change_str, add_zeit, hoga_card, cancel_str, curr_waiter, curr_room, user_init, cc_comment, guestnr, tischnr, double_currency, amount_foreign
        nonlocal kellner1


        nonlocal vat_list, t_h_bill_line, kellner1
        nonlocal vat_list_data, t_h_bill_line_data

        hbline = None
        hart = None
        Hbline =  create_buffer("Hbline",H_bill_line)
        Hart =  create_buffer("Hart",H_artikel)
        vat_list_data.clear()

        hbline_obj_list = {}
        for hbline, hart in db_session.query(Hbline, Hart).join(Hart,(Hart.artnr == Hbline.artnr) & (Hart.departement == Hbline.departement) & (Hart.artart == 0)).filter(
                 (Hbline.rechnr == h_bill.rechnr) & (Hbline.departement == h_bill.departement) & (Hbline.waehrungsnr == curr_select)).order_by(Hbline._recid).all():
            if hbline_obj_list.get(hbline._recid):
                continue
            else:
                hbline_obj_list[hbline._recid] = True

            htparam = get_cache (Htparam, {"paramnr": [(eq, hart.mwst_code)]})

            if not htparam:

                vat_list = query(vat_list_data, filters=(lambda vat_list: vat_list.vatproz == 0), first=True)

                if not vat_list:
                    vat_list = Vat_list()
                    vat_list_data.append(vat_list)

                vat_list.netto =  to_decimal(vat_list.netto) + to_decimal(hbline.betrag)


            else:

                vat_list = query(vat_list_data, filters=(lambda vat_list: vat_list.vatproz == htparam.fdecimal), first=True)

                if not vat_list:
                    vat_list = Vat_list()
                    vat_list_data.append(vat_list)

                    vat_list.vatproz =  to_decimal(htparam.fdecimal)

        for vat_list in query(vat_list_data):
            vat_list.vatAmt, vat_list.netto, vat_list.betrag, vat_list.fbetrag = cal_vatamt(vat_list.vatproz)
        amount =  to_decimal("0")

        for vat_list in query(vat_list_data):

            if vat_list.betrag == 0:
                vat_list_data.remove(vat_list)


    def update_bill_umsatz():

        nonlocal err_flag, billart, qty, price, amount, description, bill_date, fl_code, t_h_bill_line_data, bname, payment_found, h_bill_line, kellner, h_bill, bill, h_artikel, counters, htparam, artikel, bill_line, billjournal, h_journal, queasy
        nonlocal rec_id_h_bill, bilrecid, curr_select, multi_vat, balance, pay_type, transdate, price_decimal, exchg_rate, foreign_rate, dept, change_str, add_zeit, hoga_card, cancel_str, curr_waiter, curr_room, user_init, cc_comment, guestnr, tischnr, double_currency, amount_foreign
        nonlocal kellner1


        nonlocal vat_list, t_h_bill_line, kellner1
        nonlocal vat_list_data, t_h_bill_line_data

        hbline = None
        hart = None
        foart = None
        Hbline =  create_buffer("Hbline",H_bill_line)
        Hart =  create_buffer("Hart",H_artikel)
        Foart =  create_buffer("Foart",Artikel)

        hbline_obj_list = {}
        for hbline, hart, foart in db_session.query(Hbline, Hart, Foart).join(Hart,(Hart.artnr == Hbline.artnr) & (Hart.departement == Hbline.departement) & (Hart.artart == 0)).join(Foart,(Foart.artnr == Hart.artnrfront) & (Foart.departement == Hart.departement) & (Foart.artart == 0)).filter(
                 (Hbline.departement == h_bill.departement) & (Hbline.rechnr == h_bill.rechnr) & (Hbline.artnr != 0) & (Hbline.waehrungsnr == curr_select)).order_by(Hbline._recid).all():
            if hbline_obj_list.get(hbline._recid):
                continue
            else:
                hbline_obj_list[hbline._recid] = True

            if foart.umsatzart == 3 or foart.umsatzart == 5 or foart.umsatzart == 6:
                bill.f_b_umsatz =  to_decimal(bill.f_b_umsatz) + to_decimal(hbline.betrag)


            else:
                bill.sonst_umsatz =  to_decimal(bill.sonst_umsatz) + to_decimal(hbline.betrag)


        bill.gesamtumsatz =  to_decimal(bill.gesamtumsatz) + to_decimal(amount)
        bill.saldo =  to_decimal(bill.saldo) + to_decimal(amount)


    def cal_vat_amount():

        nonlocal err_flag, billart, qty, price, description, bill_date, fl_code, t_h_bill_line_data, bname, payment_found, h_bill_line, kellner, h_bill, bill, h_artikel, counters, htparam, artikel, bill_line, billjournal, h_journal, queasy
        nonlocal rec_id_h_bill, bilrecid, curr_select, multi_vat, balance, pay_type, transdate, price_decimal, exchg_rate, foreign_rate, dept, change_str, add_zeit, hoga_card, cancel_str, curr_waiter, curr_room, user_init, cc_comment, guestnr, tischnr, double_currency, amount_foreign
        nonlocal kellner1


        nonlocal vat_list, t_h_bill_line, kellner1
        nonlocal vat_list_data, t_h_bill_line_data

        mwst = to_decimal("0.0")
        h_service:Decimal = to_decimal("0.0")
        h_mwst:Decimal = to_decimal("0.0")
        vat2:Decimal = to_decimal("0.0")
        fact:Decimal = to_decimal("0.0")
        fact1:Decimal = to_decimal("0.0")
        unit_price:Decimal = to_decimal("0.0")
        amount:Decimal = to_decimal("0.0")
        incl_mwst:bool = False
        curr_vat:Decimal = to_decimal("0.0")
        hbline = None
        hart = None

        def generate_inner_output():
            return (mwst)

        Hbline =  create_buffer("Hbline",H_bill_line)
        Hart =  create_buffer("Hart",H_artikel)

        htparam = get_cache (Htparam, {"paramnr": [(eq, 134)]})
        incl_mwst = htparam.flogical

        hbline_obj_list = {}
        for hbline, hart in db_session.query(Hbline, Hart).join(Hart,(Hart.artnr == Hbline.artnr) & (Hart.departement == Hbline.departement) & (Hart.artart == 0)).filter(
                 (Hbline.rechnr == h_bill.rechnr) & (Hbline.departement == h_bill.departement) & (Hbline.waehrungsnr == curr_select)).order_by(Hbline._recid).all():
            if hbline_obj_list.get(hbline._recid):
                continue
            else:
                hbline_obj_list[hbline._recid] = True


            h_service =  to_decimal("0")
            h_mwst =  to_decimal("0")
            fact =  to_decimal("1")

            if incl_mwst:

                artikel = get_cache (Artikel, {"artnr": [(eq, h_artikel.artnrfront)],"departement": [(eq, h_artikel.departement)]})
                h_service, h_mwst, vat2, fact = get_output(calc_servtaxesbl(1, artikel.artnr, artikel.departement, None))
                h_mwst =  to_decimal(h_mwst) + to_decimal(vat2)

                if curr_vat == 0:
                    curr_vat =  to_decimal(h_mwst)

                elif curr_vat != h_mwst:
                    multi_vat = True
            amount =  to_decimal(hbline.epreis) * to_decimal(hbline.anzahl)

            if hbline.anzahl != 0:
                unit_price = ( to_decimal(hbline.betrag) / to_decimal(hbline.anzahl)) / to_decimal(fact)
            else:
                unit_price =  to_decimal(hbline.epreis) / to_decimal(fact)
            h_service = to_decimal(round(h_service * unit_price * hbline.anzahl , price_decimal))
            h_mwst = to_decimal(round(h_mwst * unit_price * hbline.anzahl , price_decimal))
            mwst =  to_decimal(mwst) + to_decimal(h_mwst)


        return generate_inner_output()


    def cal_vatamt(vatproz:Decimal):

        nonlocal err_flag, billart, price, description, bill_date, fl_code, t_h_bill_line_data, bname, payment_found, h_bill_line, kellner, h_bill, bill, h_artikel, counters, htparam, artikel, bill_line, billjournal, h_journal, queasy
        nonlocal rec_id_h_bill, bilrecid, curr_select, multi_vat, balance, pay_type, transdate, price_decimal, exchg_rate, foreign_rate, dept, change_str, add_zeit, hoga_card, cancel_str, curr_waiter, curr_room, user_init, cc_comment, guestnr, tischnr, double_currency, amount_foreign
        nonlocal kellner1


        nonlocal vat_list, t_h_bill_line, kellner1
        nonlocal vat_list_data, t_h_bill_line_data

        mwst = to_decimal("0.0")
        netto = to_decimal("0.0")
        betrag = to_decimal("0.0")
        fbetrag = to_decimal("0.0")
        h_service:Decimal = to_decimal("0.0")
        h_mwst:Decimal = to_decimal("0.0")
        vat2:Decimal = to_decimal("0.0")
        fact:Decimal = 1
        fact1:Decimal = to_decimal("0.0")
        qty:Decimal = to_decimal("0.0")
        unit_price:Decimal = to_decimal("0.0")
        amount:Decimal = to_decimal("0.0")
        incl_mwst:bool = False
        disc_art1:int = 0
        vatind:int = 0
        vatstr:string = ""
        locstr:string = ""
        hbline = None
        hart = None

        def generate_inner_output():
            return (mwst, netto, betrag, fbetrag)

        Hbline =  create_buffer("Hbline",H_bill_line)
        Hart =  create_buffer("Hart",H_artikel)

        htparam = get_cache (Htparam, {"paramnr": [(eq, 134)]})
        incl_mwst = htparam.flogical

        htparam = get_cache (Htparam, {"paramnr": [(eq, 557)]})
        disc_art1 = htparam.finteger
        vatstr = "VAT%," + to_string(vatproz * 100) + ";"

        hbline_obj_list = {}
        for hbline, hart in db_session.query(Hbline, Hart).join(Hart,(Hart.artnr == Hbline.artnr) & (Hart.departement == Hbline.departement) & (Hart.artart == 0)).filter(
                 (Hbline.rechnr == h_bill.rechnr) & (Hbline.departement == h_bill.departement) & (Hbline.waehrungsnr == curr_select)).order_by(Hbline._recid).all():
            if hbline_obj_list.get(hbline._recid):
                continue
            else:
                hbline_obj_list[hbline._recid] = True

            htparam = get_cache (Htparam, {"paramnr": [(eq, hart.mwst_code)]})

            if htparam:

                if hart.artnr == disc_art1:

                    h_journal = get_cache (H_journal, {"departement": [(eq, hbline.departement)],"bill_datum": [(eq, hbline.bill_datum)],"rechnr": [(eq, hbline.rechnr)],"artnr": [(eq, hbline.artnr)],"zeit": [(eq, hbline.zeit)]})

                    if h_journal:
                        vatind = get_index(h_journal.aendertext, vatstr)

                        if htparam.fdecimal == vatproz and h_journal.aendertext == "":
                            netto =  to_decimal(netto) + to_decimal(hbline.nettobetrag)
                            betrag =  to_decimal(betrag) + to_decimal(hbline.betrag)
                            fbetrag =  to_decimal(fbetrag) + to_decimal(hbline.fremdwbetrag)
                            mwst =  to_decimal(mwst) + to_decimal(h_journal.steuercode) / to_decimal("100")

                        elif vatind > 0:
                            locstr = substring(h_journal.aendertext, vatind + length(vatstr) - 1)
                            mwst, netto, betrag, fbetrag = get_vat(locstr, mwst, netto, betrag, fbetrag)

                elif htparam.fdecimal == vatproz:
                    netto =  to_decimal(netto) + to_decimal(hbline.nettobetrag)
                    betrag =  to_decimal(betrag) + to_decimal(hbline.betrag)
                    fbetrag =  to_decimal(fbetrag) + to_decimal(hbline.fremdwbetrag)


                    h_service =  to_decimal("0")
                    h_mwst =  to_decimal("0")
                    fact =  to_decimal("1")
                    qty =  to_decimal(hbline.anzahl)

                    if qty < 0:
                        qty =  - to_decimal(qty)

                    if incl_mwst:

                        artikel = get_cache (Artikel, {"artnr": [(eq, hart.artnrfront)],"departement": [(eq, hart.departement)]})
                        h_service, h_mwst, vat2, fact = get_output(calc_servtaxesbl(1, artikel.artnr, artikel.departement, hbline.bill_datum))
                        h_mwst =  to_decimal(h_mwst) + to_decimal(vat2)


                    amount =  to_decimal(hbline.epreis) * to_decimal(qty)

                    if hbline.betrag > 0 and amount < 0:
                        amount =  - to_decimal(amount)

                    elif hbline.betrag < 0 and amount > 0:
                        amount =  - to_decimal(amount)
                    unit_price =  to_decimal(hbline.epreis) / to_decimal(fact)

                    if incl_mwst:

                        if qty != 0:
                            unit_price = ( to_decimal(hbline.betrag) / to_decimal(qty)) / to_decimal(fact)
                        else:
                            unit_price =  to_decimal(hbline.betrag) / to_decimal(fact)

                    if unit_price < 0:
                        unit_price =  - to_decimal(unit_price)

                    if hart.service_code != 0:

                        htparam = get_cache (Htparam, {"paramnr": [(eq, hart.service_code)]})

                        if htparam.fdecimal != 0:
                            h_service =  to_decimal(unit_price) * to_decimal(htparam.fdecimal) / to_decimal("100")
                            h_service = to_decimal(round(h_service , 2))

                    if hart.mwst_code != 0:

                        htparam = get_cache (Htparam, {"paramnr": [(eq, hart.mwst_code)]})

                        if htparam.fdecimal != 0:
                            h_mwst =  to_decimal(htparam.fdecimal)

                            htparam = get_cache (Htparam, {"paramnr": [(eq, 479)]})

                            if htparam.flogical:
                                h_mwst =  to_decimal(h_mwst) * to_decimal((unit_price) + to_decimal(h_service)) / to_decimal("100")
                            else:
                                h_mwst =  to_decimal(h_mwst) * to_decimal(unit_price) / to_decimal("100")
                            h_mwst = to_decimal(round(h_mwst * qty , price_decimal))

                    if h_service == 0 and h_mwst == 0:
                        pass

                    elif not incl_mwst:

                        if h_service == 0:
                            h_mwst =  to_decimal(hbline.betrag) - to_decimal(amount)

                    if hbline.betrag > 0 and h_mwst < 0:
                        h_mwst =  - to_decimal(h_mwst)

                    elif hbline.betrag < 0 and h_mwst > 0:
                        h_mwst =  - to_decimal(h_mwst)
                    mwst =  to_decimal(mwst) + to_decimal(h_mwst)

        return generate_inner_output()


    def get_vat(curr_str:string, mwst:Decimal, netto:Decimal, betrag:Decimal, fbetrag:Decimal):

        nonlocal err_flag, billart, qty, price, amount, description, bill_date, fl_code, t_h_bill_line_data, bname, payment_found, h_bill_line, kellner, h_bill, bill, h_artikel, counters, htparam, artikel, bill_line, billjournal, h_journal, queasy
        nonlocal rec_id_h_bill, bilrecid, curr_select, multi_vat, balance, pay_type, transdate, price_decimal, exchg_rate, foreign_rate, dept, change_str, add_zeit, hoga_card, cancel_str, curr_waiter, curr_room, user_init, cc_comment, guestnr, tischnr, double_currency, amount_foreign
        nonlocal kellner1


        nonlocal vat_list, t_h_bill_line, kellner1
        nonlocal vat_list_data, t_h_bill_line_data

        ind:int = 0
        tokcounter:int = 0
        messtr:string = ""
        mestoken:string = ""
        mesvalue:string = ""

        def generate_inner_output():
            return (mwst, netto, betrag, fbetrag)

        ind = get_index(curr_str, "VAT%")

        if ind > 0:
            curr_str = substring(curr_str, 0, ind - 1)
        for tokcounter in range(1,num_entries(curr_str, ";") - 1 + 1) :
            messtr = entry(tokcounter - 1, curr_str, ";")
            mestoken = entry(0, messtr, ",")
            mesvalue = entry(1, messtr, ",")

            if mestoken == "VAT":
                mwst =  to_decimal(mwst) + to_decimal(to_decimal(mesvalue)) / to_decimal("100")
            elif mestoken == "NET":
                netto =  to_decimal(netto) + to_decimal(to_decimal(mesvalue)) / to_decimal("100")
            elif mestoken == "AMT":
                betrag =  to_decimal(betrag) + to_decimal(to_decimal(mesvalue)) / to_decimal("100")
            elif mestoken == "FAMT":
                fbetrag =  to_decimal(fbetrag) + to_decimal(to_decimal(mesvalue)) / to_decimal("100")

        return generate_inner_output()


    def del_queasy():

        nonlocal err_flag, billart, qty, price, amount, description, bill_date, fl_code, t_h_bill_line_data, bname, payment_found, h_bill_line, kellner, h_bill, bill, h_artikel, counters, htparam, artikel, bill_line, billjournal, h_journal, queasy
        nonlocal rec_id_h_bill, bilrecid, curr_select, multi_vat, balance, pay_type, transdate, price_decimal, exchg_rate, foreign_rate, dept, change_str, add_zeit, hoga_card, cancel_str, curr_waiter, curr_room, user_init, cc_comment, guestnr, tischnr, double_currency, amount_foreign
        nonlocal kellner1


        nonlocal vat_list, t_h_bill_line, kellner1
        nonlocal vat_list_data, t_h_bill_line_data

        for queasy in db_session.query(Queasy).filter(
                 (Queasy.key == 4) & (Queasy.number1 == (h_bill.departement + h_bill.rechnr * 100)) & 
                 (Queasy.number2 >= 0) & (Queasy.deci2 >= 0)).order_by(Queasy._recid).with_for_update().all():
            db_session.delete(queasy)
        pass

    h_bill = get_cache (H_bill, {"_recid": [(eq, rec_id_h_bill)]})

    bill = get_cache (Bill, {"_recid": [(eq, bilrecid)]})

    h_bill_line_obj_list = {}
    for h_bill_line, h_artikel in db_session.query(H_bill_line, H_artikel).join(H_artikel,(H_artikel.artnr == H_bill_line.artnr) & (H_artikel.departement == H_bill_line.departement) & (H_artikel.artart != 0)).filter(
             (H_bill_line.rechnr == h_bill.rechnr) & (H_bill_line.departement == h_bill.departement) & (H_bill_line.waehrungsnr == curr_select)).order_by(H_bill_line._recid).yield_per(100):
        if h_bill_line_obj_list.get(h_bill_line._recid):
            continue
        else:
            h_bill_line_obj_list[h_bill_line._recid] = True


        payment_found = True
        break

    if payment_found and multi_vat:
        err_flag = 1

        return generate_output()
    billart = 0
    qty = 1
    price =  to_decimal("0")
    amount =  - to_decimal(balance)

    if bill.rechnr == 0:

        # counters = get_cache (Counters, {"counter_no": [(eq, 3)]})
        counters = db_session.query(Counters).filter(Counters.counter_no == 3).with_for_update().first()
        counters.counter = counters.counter + 1
        bill.rechnr = counters.counter
        
        pass

    if pay_type == 2:
        description = "RmNo " + bill.zinr + " *" + to_string(bill.rechnr)

    elif pay_type == 3 or pay_type == 4:
        description = "Transfer" + " *" + to_string(bill.rechnr)
    pass
    h_bill.bilname = bname
    pass

    if pay_type == 2:
        get_output(rest_addgastinfo(h_bill.departement, h_bill.rechnr, bill.resnr, bill.reslinnr, curr_select, transdate))
    bill_date = get_output(ts_splitbill_update_billbl(rec_id_h_bill, 0, 1, 0, dept, amount, transdate, billart, description, change_str, qty, tischnr, price, add_zeit, curr_select, hoga_card, cancel_str, curr_waiter, amount_foreign, curr_room, user_init, cc_comment, guestnr))
    update_bill1()

    if round(h_bill.saldo, price_decimal) == 0:
        del_queasy()
        pass
        h_bill.flag = 1
        pass
        fl_code = 1
    else:
        fl_code = 2

    for h_bill_line in db_session.query(H_bill_line).filter(
             (H_bill_line.departement == dept) & (H_bill_line.rechnr == h_bill.rechnr)).order_by(H_bill_line._recid).all():
        t_h_bill_line = T_h_bill_line()
        t_h_bill_line_data.append(t_h_bill_line)

        buffer_copy(h_bill_line, t_h_bill_line)
        t_h_bill_line.rec_id = h_bill_line._recid

    return generate_output()