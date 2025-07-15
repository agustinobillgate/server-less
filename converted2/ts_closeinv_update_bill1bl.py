#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from functions.calc_servtaxesbl import calc_servtaxesbl
from models import H_bill, Kellner, Htparam, Artikel, Bill, Counters, Bill_line, Billjournal, H_bill_line, H_artikel, H_journal

def ts_closeinv_update_bill1bl(amount:Decimal, amount_foreign:Decimal, rec_kellner:int, rec_h_bill:int, double_currency:bool, exchg_rate:Decimal, bilrecid:int, value_sign:int, user_init:string, bill_date:date, curr_select:int, price_decimal:int):

    prepare_cache ([Kellner, Htparam, Artikel, Bill, Counters, Bill_line, Billjournal, H_journal])

    billart = 0
    qty = 0
    description = ""
    cancel_str = ""
    t_h_bill_data = []
    multi_vat:bool = False
    vat_amount:Decimal = to_decimal("0.0")
    h_bill = kellner = htparam = artikel = bill = counters = bill_line = billjournal = h_bill_line = h_artikel = h_journal = None

    t_h_bill = vat_list = None

    t_h_bill_data, T_h_bill = create_model_like(H_bill, {"rec_id":int})
    vat_list_data, Vat_list = create_model("Vat_list", {"vatproz":Decimal, "vatamt":Decimal, "netto":Decimal, "betrag":Decimal, "fbetrag":Decimal})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal billart, qty, description, cancel_str, t_h_bill_data, multi_vat, vat_amount, h_bill, kellner, htparam, artikel, bill, counters, bill_line, billjournal, h_bill_line, h_artikel, h_journal
        nonlocal amount, amount_foreign, rec_kellner, rec_h_bill, double_currency, exchg_rate, bilrecid, value_sign, user_init, bill_date, curr_select, price_decimal


        nonlocal t_h_bill, vat_list
        nonlocal t_h_bill_data, vat_list_data

        return {"amount": amount, "amount_foreign": amount_foreign, "billart": billart, "qty": qty, "description": description, "cancel_str": cancel_str, "t-h-bill": t_h_bill_data}

    def update_bill_umsatz(value_sign:int):

        nonlocal billart, qty, description, cancel_str, t_h_bill_data, multi_vat, vat_amount, h_bill, kellner, htparam, artikel, bill, counters, bill_line, billjournal, h_bill_line, h_artikel, h_journal
        nonlocal amount, amount_foreign, rec_kellner, rec_h_bill, double_currency, exchg_rate, bilrecid, user_init, bill_date, curr_select, price_decimal


        nonlocal t_h_bill, vat_list
        nonlocal t_h_bill_data, vat_list_data

        do_it:bool = False
        hbline = None
        hart = None
        foart = None
        Hbline =  create_buffer("Hbline",H_bill_line)
        Hart =  create_buffer("Hart",H_artikel)
        Foart =  create_buffer("Foart",Artikel)

        hbline_obj_list = {}
        for hbline, hart, foart in db_session.query(Hbline, Hart, Foart).join(Hart,(Hart.artnr == Hbline.artnr) & (Hart.departement == Hbline.departement) & (Hart.artart == 0)).join(Foart,(Foart.artnr == Hart.artnrfront) & (Foart.departement == Hart.departement) & (Foart.artart == 0)).filter(
                 (Hbline.departement == h_bill.departement) & (Hbline.rechnr == h_bill.rechnr) & (Hbline.artnr != 0)).order_by(Hbline._recid).all():
            if hbline_obj_list.get(hbline._recid):
                continue
            else:
                hbline_obj_list[hbline._recid] = True

            if curr_select == 0:
                do_it = True
            else:
                do_it = (hbline.waehrungsnr == curr_select)

            if do_it:

                if foart.umsatzart == 3 or foart.umsatzart == 5 or foart.umsatzart == 6:
                    bill.f_b_umsatz =  to_decimal(bill.f_b_umsatz) +\
                        value_sign * to_decimal(hbline.betrag)


                else:
                    bill.sonst_umsatz =  to_decimal(bill.sonst_umsatz) +\
                        value_sign * to_decimal(hbline.betrag)


                bill.gesamtumsatz =  to_decimal(bill.gesamtumsatz) + to_decimal(value_sign) * to_decimal(hbline.betrag)
        bill.saldo =  to_decimal(bill.saldo) + to_decimal(amount)


    def cal_vat_amount():

        nonlocal billart, qty, description, cancel_str, t_h_bill_data, vat_amount, h_bill, kellner, htparam, artikel, bill, counters, bill_line, billjournal, h_bill_line, h_artikel, h_journal
        nonlocal amount_foreign, rec_kellner, rec_h_bill, double_currency, exchg_rate, bilrecid, value_sign, user_init, bill_date, curr_select, price_decimal


        nonlocal t_h_bill, vat_list
        nonlocal t_h_bill_data, vat_list_data

        mwst = to_decimal("0.0")
        h_service:Decimal = to_decimal("0.0")
        h_mwst:Decimal = to_decimal("0.0")
        vat2:Decimal = to_decimal("0.0")
        fact:Decimal = to_decimal("0.0")
        fact1:Decimal = to_decimal("0.0")
        unit_price:Decimal = to_decimal("0.0")
        amount:Decimal = to_decimal("0.0")
        incl_mwst:bool = False
        multi_vat:bool = False
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

                artikel = get_cache (Artikel, {"artnr": [(eq, hart.artnrfront)],"departement": [(eq, hart.departement)]})
                h_service, h_mwst, vat2, fact = get_output(calc_servtaxesbl(1, artikel.artnr, artikel.departement, None))
                h_mwst =  to_decimal(h_mwst) + to_decimal(vat2)

                if curr_vat == 0:
                    curr_vat =  to_decimal(h_mwst)

                elif curr_vat != h_mwst:
                    multi_vat = True
            amount =  to_decimal(hbline.epreis) * to_decimal(hbline.anzahl)
            unit_price =  to_decimal(hbline.epreis) / to_decimal(fact)
            h_service = to_decimal(round(h_service * unit_price , price_decimal))
            h_mwst = to_decimal(round(h_mwst * unit_price , price_decimal))

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


    def create_vat_list(value_sign:int):

        nonlocal billart, qty, description, cancel_str, t_h_bill_data, multi_vat, vat_amount, h_bill, kellner, htparam, artikel, bill, counters, bill_line, billjournal, h_bill_line, h_artikel, h_journal
        nonlocal amount, amount_foreign, rec_kellner, rec_h_bill, double_currency, exchg_rate, bilrecid, user_init, bill_date, curr_select, price_decimal


        nonlocal t_h_bill, vat_list
        nonlocal t_h_bill_data, vat_list_data

        do_it:bool = False
        hbline = None
        hart = None
        Hbline =  create_buffer("Hbline",H_bill_line)
        Hart =  create_buffer("Hart",H_artikel)
        vat_list_data.clear()

        hbline_obj_list = {}
        for hbline, hart in db_session.query(Hbline, Hart).join(Hart,(Hart.artnr == Hbline.artnr) & (Hart.departement == Hbline.departement) & (Hart.artart == 0)).filter(
                 (Hbline.rechnr == h_bill.rechnr) & (Hbline.departement == h_bill.departement)).order_by(Hbline._recid).all():
            if hbline_obj_list.get(hbline._recid):
                continue
            else:
                hbline_obj_list[hbline._recid] = True

            if curr_select == 0:
                do_it = True
            else:
                do_it = (hbline.waehrungsnr == curr_select)

            if do_it:

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

        for vat_list in query(vat_list_data, filters=(lambda vat_list: vat_list.vatproz != 0)):
            vat_list.vatAmt, vat_list.netto, vat_list.betrag, vat_list.fbetrag = cal_vatamt(value_sign, vat_list.vatproz)


    def cal_vatamt(value_sign:int, vatproz:Decimal):

        nonlocal billart, description, cancel_str, t_h_bill_data, multi_vat, vat_amount, h_bill, kellner, htparam, artikel, bill, counters, bill_line, billjournal, h_bill_line, h_artikel, h_journal
        nonlocal amount_foreign, rec_kellner, rec_h_bill, double_currency, exchg_rate, bilrecid, user_init, bill_date, curr_select, price_decimal


        nonlocal t_h_bill, vat_list
        nonlocal t_h_bill_data, vat_list_data

        mwst = to_decimal("0.0")
        netto = to_decimal("0.0")
        betrag = to_decimal("0.0")
        fbetrag = to_decimal("0.0")
        h_service:Decimal = to_decimal("0.0")
        h_mwst:Decimal = to_decimal("0.0")
        vat2:Decimal = to_decimal("0.0")
        fact:Decimal = to_decimal("0.0")
        fact1:Decimal = to_decimal("0.0")
        qty:Decimal = to_decimal("0.0")
        unit_price:Decimal = to_decimal("0.0")
        amount:Decimal = to_decimal("0.0")
        incl_mwst:bool = False
        do_it:bool = False
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
                 (Hbline.rechnr == h_bill.rechnr) & (Hbline.departement == h_bill.departement)).order_by(Hbline._recid).all():
            if hbline_obj_list.get(hbline._recid):
                continue
            else:
                hbline_obj_list[hbline._recid] = True

            if curr_select == 0:
                do_it = True
            else:
                do_it = (hbline.waehrungsnr == curr_select)

            if do_it:

                htparam = get_cache (Htparam, {"paramnr": [(eq, hart.mwst_code)]})

                if htparam:

                    if hart.artnr == disc_art1:

                        h_journal = get_cache (H_journal, {"departement": [(eq, hbline.departement)],"bill_datum": [(eq, hbline.bill_datum)],"rechnr": [(eq, hbline.rechnr)],"artnr": [(eq, hbline.artnr)],"zeit": [(eq, hbline.zeit)]})

                        if h_journal:
                            vatind = get_index(h_journal.aendertext, vatstr)

                            if htparam.fdecimal == vatproz and h_journal.aendertext == "":
                                netto =  to_decimal(netto) + to_decimal(value_sign) * to_decimal(hbline.nettobetrag)
                                betrag =  to_decimal(betrag) + to_decimal(value_sign) * to_decimal(hbline.betrag)
                                fbetrag =  to_decimal(fbetrag) + to_decimal(value_sign) * to_decimal(hbline.fremdwbetrag)
                                mwst =  to_decimal(mwst) + to_decimal(value_sign) * to_decimal(h_journal.steuercode) / to_decimal("100")

                            elif vatind > 0:
                                locstr = substring(h_journal.aendertext, vatind + length(vatstr) - 1)
                                mwst, netto, betrag, fbetrag = get_vat(value_sign, locstr, mwst, netto, betrag, fbetrag)

                    elif htparam.fdecimal == vatproz:
                        netto =  to_decimal(netto) + to_decimal(value_sign) * to_decimal(hbline.nettobetrag)
                        betrag =  to_decimal(betrag) + to_decimal(value_sign) * to_decimal(hbline.betrag)
                        fbetrag =  to_decimal(fbetrag) + to_decimal(value_sign) * to_decimal(hbline.fremdwbetrag)


                        h_service =  to_decimal("0")
                        h_mwst =  to_decimal("0")
                        fact =  to_decimal("1")
                        qty =  to_decimal(hbline.anzahl)

                        if qty < 0:
                            qty =  - to_decimal(qty)

                        if incl_mwst:

                            artikel = get_cache (Artikel, {"artnr": [(eq, hart.artnrfront)],"departement": [(eq, hart.departement)]})
                            h_service, h_mwst, vat2, fact = get_output(calc_servtaxesbl(1, artikel.artnr, artikel.departement, None))
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
                        h_service = to_decimal(round(h_service * unit_price , price_decimal))
                        h_mwst = to_decimal(round(h_mwst * unit_price , price_decimal))

                        if h_service == 0 and h_mwst == 0:
                            pass

                        elif not incl_mwst:

                            if h_service == 0:
                                h_mwst =  to_decimal(hbline.betrag) - to_decimal(amount)

                        if hbline.betrag > 0 and h_mwst < 0:
                            h_mwst =  - to_decimal(h_mwst)

                        elif hbline.betrag < 0 and h_mwst > 0:
                            h_mwst =  - to_decimal(h_mwst)
                        mwst =  to_decimal(mwst) + to_decimal(value_sign) * to_decimal(h_mwst)

        return generate_inner_output()


    def get_vat(value_sign:int, curr_str:string, mwst:Decimal, netto:Decimal, betrag:Decimal, fbetrag:Decimal):

        nonlocal billart, qty, description, cancel_str, t_h_bill_data, multi_vat, vat_amount, h_bill, kellner, htparam, artikel, bill, counters, bill_line, billjournal, h_bill_line, h_artikel, h_journal
        nonlocal amount, amount_foreign, rec_kellner, rec_h_bill, double_currency, exchg_rate, bilrecid, user_init, bill_date, curr_select, price_decimal


        nonlocal t_h_bill, vat_list
        nonlocal t_h_bill_data, vat_list_data

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
                mwst =  to_decimal(mwst) + to_decimal(value_sign) * to_decimal(to_decimal(mesvalue)) / to_decimal("100")
            elif mestoken == "NET":
                netto =  to_decimal(netto) + to_decimal(value_sign) * to_decimal(to_decimal(mesvalue)) / to_decimal("100")
            elif mestoken == "AMT":
                betrag =  to_decimal(betrag) + to_decimal(value_sign) * to_decimal(to_decimal(mesvalue)) / to_decimal("100")
            elif mestoken == "FAMT":
                fbetrag =  to_decimal(fbetrag) + to_decimal(value_sign) * to_decimal(to_decimal(mesvalue)) / to_decimal("100")

        return generate_inner_output()

    kellner = get_cache (Kellner, {"_recid": [(eq, rec_kellner)]})

    h_bill = get_cache (H_bill, {"_recid": [(eq, rec_h_bill)]})

    htparam = get_cache (Htparam, {"paramnr": [(eq, 271)]})

    if htparam.feldtyp == 4:
        multi_vat = htparam.flogical
    billart = 0
    qty = 1
    amount =  - to_decimal(amount)
    amount_foreign =  - to_decimal(amount_foreign)

    if not double_currency:
        amount_foreign =  to_decimal(amount) / to_decimal(exchg_rate)

    if amount != 0:

        artikel = get_cache (Artikel, {"artnr": [(eq, kellner.kcredit_nr)],"departement": [(eq, 0)]})

        if artikel:
            billart = artikel.artnr
            description = trim(artikel.bezeich) + " *" + to_string(h_bill.rechnr)
        else:
            description = "*" + to_string(h_bill.rechnr)

        bill = get_cache (Bill, {"_recid": [(eq, bilrecid)]})

        if bill.rechnr == 0:

            counters = get_cache (Counters, {"counter_no": [(eq, 3)]})
            counters.counter = counters.counter + 1
            bill.rechnr = counters.counter
            pass
        update_bill_umsatz(value_sign)

        if double_currency:
            bill.mwst[98] = bill.mwst[98] + amount_foreign
        bill.rgdruck = 0
        vat_amount = cal_vat_amount()

        if multi_vat:
            create_vat_list(value_sign)

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
                bill_line.artnr = billart
                bill_line.bezeich = description
                bill_line.anzahl = 1
                bill_line.fremdwbetrag =  to_decimal(vat_list.fbetrag)
                bill_line.betrag =  to_decimal(vat_list.betrag)
                bill_line.nettobetrag =  to_decimal(vat_list.netto)
                bill_line.departement = h_bill.departement
                bill_line.epreis =  to_decimal("0")
                bill_line.zeit = get_current_time_in_seconds()
                bill_line.userinit = user_init
                bill_line.bill_datum = bill_date
                bill_line.orts_tax =  to_decimal(vat_list.vatamt)
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
                billjournal.epreis =  to_decimal("0")
                billjournal.zeit = get_current_time_in_seconds()
                billjournal.stornogrund = ""
                billjournal.userinit = user_init
                billjournal.bill_datum = bill_date

                if artikel:
                    billjournal.departement = artikel.departement
                pass

        else:
            bill_line = Bill_line()
            db_session.add(bill_line)

            bill_line.rechnr = bill.rechnr
            bill_line.zinr = bill.zinr
            bill_line.artnr = billart
            bill_line.bezeich = description
            bill_line.anzahl = 1
            bill_line.fremdwbetrag =  to_decimal(amount_foreign)
            bill_line.betrag =  to_decimal(amount)
            bill_line.departement = h_bill.departement
            bill_line.epreis =  to_decimal("0")
            bill_line.zeit = get_current_time_in_seconds()
            bill_line.userinit = user_init
            bill_line.bill_datum = bill_date
            bill_line.orts_tax =  to_decimal(vat_amount)


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
            billjournal.epreis =  to_decimal("0")
            billjournal.zeit = get_current_time_in_seconds()
            billjournal.stornogrund = ""
            billjournal.userinit = user_init
            billjournal.bill_datum = bill_date

            if artikel:
                billjournal.departement = artikel.departement
            pass
        cancel_str = ""
    pass
    h_bill.flag = 1
    pass
    pass
    pass
    t_h_bill = T_h_bill()
    t_h_bill_data.append(t_h_bill)

    buffer_copy(h_bill, t_h_bill)
    t_h_bill.rec_id = h_bill._recid

    return generate_output()