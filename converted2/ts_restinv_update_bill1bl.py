#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from functions.calc_servtaxesbl import calc_servtaxesbl
from models import H_bill, Bill, Htparam, Artikel, Counters, Bill_line, Billjournal, H_bill_line, H_artikel, Queasy, H_journal

def ts_restinv_update_bill1bl(rec_id_h_bill:int, transdate:date, double_currency:bool, exchg_rate:Decimal, kellner1_kcredit_nr:int, bilrecid:int, foreign_rate:bool, user_init:string, gname:string, hoga_resnr:int, hoga_reslinnr:int, price_decimal:int, amount:Decimal, amount_foreign:Decimal):

    prepare_cache ([Bill, Htparam, Artikel, Counters, Bill_line, Billjournal, H_bill_line, Queasy, H_journal])

    bill_date = None
    billart = 0
    qty = to_decimal("0.0")
    description = ""
    cancel_str = ""
    t_h_bill_data = []
    vat_amount:Decimal = to_decimal("0.0")
    multi_vat:bool = False
    get_rechnr:int = 0
    get_amount:Decimal = to_decimal("0.0")
    curr_dept:int = 0
    active_deposit:bool = False
    h_bill = bill = htparam = artikel = counters = bill_line = billjournal = h_bill_line = h_artikel = queasy = h_journal = None

    t_h_bill = vat_list = None

    t_h_bill_data, T_h_bill = create_model_like(H_bill, {"rec_id":int})
    vat_list_data, Vat_list = create_model("Vat_list", {"vatproz":Decimal, "vatamt":Decimal, "netto":Decimal, "betrag":Decimal, "fbetrag":Decimal})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal bill_date, billart, qty, description, cancel_str, t_h_bill_data, vat_amount, multi_vat, get_rechnr, get_amount, curr_dept, active_deposit, h_bill, bill, htparam, artikel, counters, bill_line, billjournal, h_bill_line, h_artikel, queasy, h_journal
        nonlocal rec_id_h_bill, transdate, double_currency, exchg_rate, kellner1_kcredit_nr, bilrecid, foreign_rate, user_init, gname, hoga_resnr, hoga_reslinnr, price_decimal, amount, amount_foreign


        nonlocal t_h_bill, vat_list
        nonlocal t_h_bill_data, vat_list_data

        return {"amount": amount, "amount_foreign": amount_foreign, "bill_date": bill_date, "billart": billart, "qty": qty, "description": description, "cancel_str": cancel_str, "t-h-bill": t_h_bill_data}

    def cal_vat_amount():

        nonlocal bill_date, billart, description, cancel_str, t_h_bill_data, vat_amount, get_rechnr, get_amount, curr_dept, active_deposit, h_bill, bill, htparam, artikel, counters, bill_line, billjournal, h_bill_line, h_artikel, queasy, h_journal
        nonlocal rec_id_h_bill, transdate, double_currency, exchg_rate, kellner1_kcredit_nr, bilrecid, foreign_rate, user_init, gname, hoga_resnr, hoga_reslinnr, price_decimal, amount_foreign


        nonlocal t_h_bill, vat_list
        nonlocal t_h_bill_data, vat_list_data

        mwst = to_decimal("0.0")
        h_service:Decimal = to_decimal("0.0")
        h_mwst:Decimal = to_decimal("0.0")
        vat2:Decimal = to_decimal("0.0")
        fact:Decimal = to_decimal("0.0")
        fact1:Decimal = to_decimal("0.0")
        qty:Decimal = to_decimal("0.0")
        unit_price:Decimal = to_decimal("0.0")
        amount:Decimal = to_decimal("0.0")
        incl_mwst:bool = False
        multi_vat:bool = False
        curr_vat:Decimal = to_decimal("0.0")
        disc_art1:int = 0
        hbline = None
        hart = None

        def generate_inner_output():
            return (mwst)

        Hbline =  create_buffer("Hbline",H_bill_line)
        Hart =  create_buffer("Hart",H_artikel)

        htparam = get_cache (Htparam, {"paramnr": [(eq, 134)]})
        incl_mwst = htparam.flogical

        htparam = get_cache (Htparam, {"paramnr": [(eq, 557)]})
        disc_art1 = htparam.finteger

        hbline_obj_list = {}
        for hbline, hart in db_session.query(Hbline, Hart).join(Hart,(Hart.artnr == Hbline.artnr) & (Hart.departement == Hbline.departement) & (Hart.artart == 0)).filter(
                 (Hbline.rechnr == h_bill.rechnr) & (Hbline.departement == h_bill.departement)).order_by(Hbline._recid).all():
            if hbline_obj_list.get(hbline._recid):
                continue
            else:
                hbline_obj_list[hbline._recid] = True

            if hart.artnr == disc_art1:

                h_journal = get_cache (H_journal, {"departement": [(eq, hbline.departement)],"bill_datum": [(eq, hbline.bill_datum)],"rechnr": [(eq, hbline.rechnr)],"artnr": [(eq, hbline.artnr)],"zeit": [(eq, hbline.zeit)]})

                if h_journal:
                    mwst =  to_decimal(mwst) + to_decimal(h_journal.steuercode) / to_decimal("100")
            else:
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

                    if curr_vat == 0:
                        curr_vat =  to_decimal(h_mwst)

                    elif curr_vat != h_mwst:
                        multi_vat = True
                amount =  to_decimal(hbline.epreis) * to_decimal(qty)

                if hbline.betrag > 0 and amount < 0:
                    amount =  - to_decimal(amount)

                elif hbline.betrag < 0 and amount > 0:
                    amount =  - to_decimal(amount)

                if qty != 0:
                    unit_price = ( to_decimal(hbline.betrag) / to_decimal(qty)) / to_decimal(fact)
                else:
                    unit_price =  to_decimal(hbline.epreis) / to_decimal(fact)

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
                mwst =  to_decimal(mwst) + to_decimal(h_mwst)

        return generate_inner_output()


    def create_vat_list():

        nonlocal bill_date, billart, qty, description, cancel_str, t_h_bill_data, vat_amount, multi_vat, get_rechnr, get_amount, curr_dept, active_deposit, h_bill, bill, htparam, artikel, counters, bill_line, billjournal, h_bill_line, h_artikel, queasy, h_journal
        nonlocal rec_id_h_bill, transdate, double_currency, exchg_rate, kellner1_kcredit_nr, bilrecid, foreign_rate, user_init, gname, hoga_resnr, hoga_reslinnr, price_decimal, amount, amount_foreign


        nonlocal t_h_bill, vat_list
        nonlocal t_h_bill_data, vat_list_data

        service:Decimal = to_decimal("0.0")
        vat:Decimal = to_decimal("0.0")
        vat2:Decimal = to_decimal("0.0")
        fact:Decimal = to_decimal("0.0")
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

            artikel = get_cache (Artikel, {"artnr": [(eq, hart.artnrfront)],"departement": [(eq, hart.departement)]})

            htparam = get_cache (Htparam, {"paramnr": [(eq, artikel.mwst_code)]})

            if not htparam:

                vat_list = query(vat_list_data, filters=(lambda vat_list: vat_list.vatproz == 0), first=True)

                if not vat_list:
                    vat_list = Vat_list()
                    vat_list_data.append(vat_list)

                vat_list.netto =  to_decimal(vat_list.netto) + to_decimal(hbline.betrag)


            else:
                service, vat, vat2, fact = get_output(calc_servtaxesbl(1, artikel.artnr, artikel.departement, None))
                vat =  to_decimal(vat) + to_decimal(vat2)

                vat_list = query(vat_list_data, filters=(lambda vat_list: vat_list.vatproz == vat * 100), first=True)

                if not vat_list:
                    vat_list = Vat_list()
                    vat_list_data.append(vat_list)

                    vat_list.vatproz =  to_decimal(vat) * to_decimal("100")

        for vat_list in query(vat_list_data):
            vat_list.vatAmt, vat_list.netto, vat_list.betrag, vat_list.fbetrag = cal_vatamt(vat_list.vatproz)
        amount =  to_decimal("0")

        for vat_list in query(vat_list_data):

            if vat_list.betrag == 0:
                vat_list_data.remove(vat_list)


    def update_bill_umsatz():

        nonlocal bill_date, billart, qty, description, cancel_str, t_h_bill_data, vat_amount, multi_vat, get_rechnr, get_amount, curr_dept, active_deposit, h_bill, bill, htparam, artikel, counters, bill_line, billjournal, h_bill_line, h_artikel, queasy, h_journal
        nonlocal rec_id_h_bill, transdate, double_currency, exchg_rate, kellner1_kcredit_nr, bilrecid, foreign_rate, user_init, gname, hoga_resnr, hoga_reslinnr, price_decimal, amount, amount_foreign


        nonlocal t_h_bill, vat_list
        nonlocal t_h_bill_data, vat_list_data

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

            if foart.umsatzart == 3 or foart.umsatzart == 5 or foart.umsatzart == 6:
                bill.f_b_umsatz =  to_decimal(bill.f_b_umsatz) + to_decimal(hbline.betrag)


            else:
                bill.sonst_umsatz =  to_decimal(bill.sonst_umsatz) + to_decimal(hbline.betrag)


        bill.gesamtumsatz =  to_decimal(bill.gesamtumsatz) + to_decimal(h_bill.gesamtumsatz)
        bill.saldo =  to_decimal(bill.saldo) + to_decimal(amount)


    def cal_vatamt(vatproz:Decimal):

        nonlocal bill_date, billart, description, cancel_str, t_h_bill_data, vat_amount, multi_vat, get_rechnr, get_amount, curr_dept, active_deposit, h_bill, bill, htparam, artikel, counters, bill_line, billjournal, h_bill_line, h_artikel, queasy, h_journal
        nonlocal rec_id_h_bill, transdate, double_currency, exchg_rate, kellner1_kcredit_nr, bilrecid, foreign_rate, user_init, gname, hoga_resnr, hoga_reslinnr, price_decimal, amount_foreign


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
        disc_art1:int = 0
        vatind:int = 0
        vatstr:string = ""
        locstr:string = ""
        sourcestr:string = ""
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
        vatstr = "vat%," + to_string(vatproz * 100) + ";"

        hbline_obj_list = {}
        for hbline, hart in db_session.query(Hbline, Hart).join(Hart,(Hart.artnr == Hbline.artnr) & (Hart.departement == Hbline.departement) & (Hart.artart == 0)).filter(
                 (Hbline.rechnr == h_bill.rechnr) & (Hbline.departement == h_bill.departement)).order_by(Hbline._recid).all():
            if hbline_obj_list.get(hbline._recid):
                continue
            else:
                hbline_obj_list[hbline._recid] = True

            htparam = get_cache (Htparam, {"paramnr": [(eq, hart.mwst_code)]})

            if htparam:

                if hart.artnr == disc_art1:

                    h_journal = get_cache (H_journal, {"departement": [(eq, hbline.departement)],"bill_datum": [(eq, hbline.bill_datum)],"rechnr": [(eq, hbline.rechnr)],"artnr": [(eq, hbline.artnr)],"zeit": [(eq, hbline.zeit)]})

                    if h_journal:
                        sourcestr = h_journal.aendertext
                        vatind = get_index(sourcestr, vatstr)

                        if htparam.fdecimal == vatproz and sourcestr == "":
                            netto =  to_decimal(netto) + to_decimal(hbline.nettobetrag)
                            betrag =  to_decimal(betrag) + to_decimal(hbline.betrag)
                            fbetrag =  to_decimal(fbetrag) + to_decimal(hbline.fremdwbetrag)
                            mwst =  to_decimal(mwst) + to_decimal(h_journal.steuercode) / to_decimal("100")


                        else:
                            while vatind > 0:
                                locstr = substring(sourcestr, vatind + length(vatstr) - 1)
                                mwst, netto, betrag, fbetrag = get_vat(locstr, mwst, netto, betrag, fbetrag)
                                sourcestr = locstr
                                vatind = get_index(sourcestr, vatstr)

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
                    mwst =  to_decimal(mwst) + to_decimal(h_mwst)

        return generate_inner_output()


    def get_vat(curr_str:string, mwst:Decimal, netto:Decimal, betrag:Decimal, fbetrag:Decimal):

        nonlocal bill_date, billart, qty, description, cancel_str, t_h_bill_data, vat_amount, multi_vat, get_rechnr, get_amount, curr_dept, active_deposit, h_bill, bill, htparam, artikel, counters, bill_line, billjournal, h_bill_line, h_artikel, queasy, h_journal
        nonlocal rec_id_h_bill, transdate, double_currency, exchg_rate, kellner1_kcredit_nr, bilrecid, foreign_rate, user_init, gname, hoga_resnr, hoga_reslinnr, price_decimal, amount, amount_foreign


        nonlocal t_h_bill, vat_list
        nonlocal t_h_bill_data, vat_list_data

        ind:int = 0
        tokcounter:int = 0
        messtr:string = ""
        mestoken:string = ""
        mesvalue:string = ""

        def generate_inner_output():
            return (mwst, netto, betrag, fbetrag)

        ind = get_index(curr_str, "vat%")

        if ind > 0:
            curr_str = substring(curr_str, 0, ind - 1)
        for tokcounter in range(1,num_entries(curr_str, ";") - 1 + 1) :
            messtr = entry(tokcounter - 1, curr_str, ";")
            mestoken = entry(0, messtr, ",")
            mesvalue = entry(1, messtr, ",")

            if mestoken == "vat":
                mwst =  to_decimal(mwst) + to_decimal(to_decimal(mesvalue)) / to_decimal("100")
            elif mestoken == "NET":
                netto =  to_decimal(netto) + to_decimal(to_decimal(mesvalue)) / to_decimal("100")
            elif mestoken == "AMT":
                betrag =  to_decimal(betrag) + to_decimal(to_decimal(mesvalue)) / to_decimal("100")
            elif mestoken == "FAMT":
                fbetrag =  to_decimal(fbetrag) + to_decimal(to_decimal(mesvalue)) / to_decimal("100")

        return generate_inner_output()


    def update_selforder():

        nonlocal bill_date, billart, qty, description, cancel_str, t_h_bill_data, vat_amount, multi_vat, get_rechnr, get_amount, curr_dept, active_deposit, h_bill, bill, htparam, artikel, counters, bill_line, billjournal, h_bill_line, h_artikel, queasy, h_journal
        nonlocal rec_id_h_bill, transdate, double_currency, exchg_rate, kellner1_kcredit_nr, bilrecid, foreign_rate, user_init, gname, hoga_resnr, hoga_reslinnr, price_decimal, amount, amount_foreign


        nonlocal t_h_bill, vat_list
        nonlocal t_h_bill_data, vat_list_data

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
            paramqsy.betriebsnr = get_rechnr

            if dynamic_qr:

                pickup_table = db_session.query(Pickup_table).filter(
                             (Pickup_table.key == 225) & (Pickup_table.char1 == ("taken-table").lower()) & (Pickup_table.number1 == curr_dept) & (Pickup_table.logi1) & (Pickup_table.logi2) & (Pickup_table.number2 == paramqsy.number2) & (entry(0, Pickup_table.char3, "|") == (session_parameter).lower())).first()

                if pickup_table:
                    pickup_table.char3 = entry(0, pickup_table.char3, "|", session_parameter + "T" + replace_str(to_string(get_current_date()) , "/", "") + replace_str(to_string(get_current_time_in_seconds(), "HH:MM") , ":", ""))


                    pass

            orderbill = get_cache (Queasy, {"key": [(eq, 225)],"char1": [(eq, "orderbill")],"char3": [(eq, session_parameter)],"logi1": [(eq, True)],"logi3": [(eq, True)]})

            if orderbill:
                orderbill.deci1 =  to_decimal(get_amount)
                orderbill.logi2 = False
                orderbill.char3 = session_parameter + "T" + replace_str(to_string(get_current_date()) , "/", "") + replace_str(to_string(get_current_time_in_seconds(), "HH:MM") , ":", "")
                orderbill.logi1 = False

                for orderbill_close in db_session.query(Orderbill_close).filter(
                             (Orderbill_close.key == 225) & (Orderbill_close.char1 == ("orderbill").lower()) & (Orderbill_close.char3 == (session_parameter).lower()) & (Orderbill_close.logi1) & (Orderbill_close.logi3)).order_by(Orderbill_close._recid).all():
                    orderbill_close.char3 = session_parameter + "T" + replace_str(to_string(get_current_date()) , "/", "") + replace_str(to_string(get_current_time_in_seconds(), "HH:MM") , ":", "")
                    orderbill_close.logi1 = False

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

                for orderbilline in db_session.query(Orderbilline).filter(
                             (Orderbilline.key == 225) & (Orderbilline.char1 == ("orderbill-line").lower()) & (entry(3, Orderbilline.char2, "|") == (session_parameter).lower())).order_by(Orderbilline._recid).all():

                    if orderbilline.logi2 and orderbilline.logi3:
                        orderbilline.char2 = entry(0, orderbilline.char2, "|") + "|" + entry(1, orderbilline.char2, "|") + "|" + entry(2, orderbilline.char2, "|") + "|" + session_parameter + "T" + replace_str(to_string(get_current_date()) , "/", "") + replace_str(to_string(get_current_time_in_seconds(), "HH:MM") , ":", "")
                    else:

                        if num_entries(orderbilline.char3, "|") > 8 and entry(8, orderbilline.char3, "|") != "":
                            orderbilline.char2 = entry(0, orderbilline.char2, "|") + "|" + entry(1, orderbilline.char2, "|") + "|" + entry(2, orderbilline.char2, "|") + "|" + session_parameter + "T" + replace_str(to_string(get_current_date()) , "/", "") + replace_str(to_string(get_current_time_in_seconds(), "HH:MM") , ":", "")

            qpayment_gateway = get_cache (Queasy, {"key": [(eq, 223)],"char3": [(eq, session_parameter)],"betriebsnr": [(eq, get_rechnr)]})

            if qpayment_gateway:
                qpayment_gateway.betriebsnr = 0
                pass
            pass


    def remove_rsv_table():

        nonlocal bill_date, billart, qty, description, cancel_str, t_h_bill_data, vat_amount, multi_vat, get_rechnr, get_amount, curr_dept, active_deposit, h_bill, bill, htparam, artikel, counters, bill_line, billjournal, h_bill_line, h_artikel, queasy, h_journal
        nonlocal rec_id_h_bill, transdate, double_currency, exchg_rate, kellner1_kcredit_nr, bilrecid, foreign_rate, user_init, gname, hoga_resnr, hoga_reslinnr, price_decimal, amount, amount_foreign


        nonlocal t_h_bill, vat_list
        nonlocal t_h_bill_data, vat_list_data

        recid_q33:int = 0
        buffq33 = None
        Buffq33 =  create_buffer("Buffq33",Queasy)

        queasy = get_cache (Queasy, {"key": [(eq, 251)],"number1": [(eq, rec_id_h_bill)]})

        if queasy:
            recid_q33 = queasy.number2

            buffq33 = get_cache (Queasy, {"_recid": [(eq, recid_q33)]})

            if buffq33:
                pass
                buffq33.betriebsnr = 1


                pass
                pass

    h_bill = get_cache (H_bill, {"_recid": [(eq, rec_id_h_bill)]})

    if not h_bill:

        return generate_output()

    bill = get_cache (Bill, {"_recid": [(eq, bilrecid)]})
    curr_dept = h_bill.departement

    if gname == None:
        gname = ""

    if user_init == None:
        user_init = ""

    htparam = get_cache (Htparam, {"paramnr": [(eq, 588)]})

    if htparam:
        active_deposit = htparam.flogical

    htparam = get_cache (Htparam, {"paramnr": [(eq, 271)]})

    if htparam.feldtyp == 4:
        multi_vat = htparam.flogical

    htparam = get_cache (Htparam, {"paramnr": [(eq, 110)]})
    bill_date = htparam.fdate

    if transdate != None:
        bill_date = transdate
    else:

        htparam = get_cache (Htparam, {"paramnr": [(eq, 253)]})

        if htparam.flogical and bill_date < get_current_date():
            bill_date = bill_date + timedelta(days=1)
    billart = 0
    qty =  to_decimal("1")
    amount =  - to_decimal(amount)
    amount_foreign =  - to_decimal(amount_foreign)

    if not double_currency:
        amount_foreign =  to_decimal(amount) / to_decimal(exchg_rate)

    if amount != 0:

        artikel = get_cache (Artikel, {"artnr": [(eq, kellner1_kcredit_nr)],"departement": [(eq, 0)]})

        if artikel:
            billart = artikel.artnr
            description = trim(artikel.bezeich) + " *" + to_string(h_bill.rechnr)
        else:
            description = "*" + to_string(h_bill.rechnr)
        pass

        if bill.rechnr == 0:

            counters = get_cache (Counters, {"counter_no": [(eq, 3)]})
            counters.counter = counters.counter + 1
            pass
            bill.rechnr = counters.counter
        update_bill_umsatz()

        if bill.datum < bill_date:
            bill.datum = bill_date

        if foreign_rate and not double_currency:
            bill.mwst[98] = bill.mwst[98] + amount / exchg_rate

        elif double_currency:
            bill.mwst[98] = bill.mwst[98] + amount_foreign
        bill.rgdruck = 0
        pass
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
        billjournal.departement = h_bill.departement
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
    h_bill.bilname = gname

    if hoga_resnr > 0 and h_bill.resnr == 0:
        h_bill.resnr = hoga_resnr
        h_bill.reslinnr = hoga_reslinnr


    pass
    get_rechnr = h_bill.rechnr

    for h_bill_line in db_session.query(H_bill_line).filter(
                 (H_bill_line.departement == h_bill.departement) & (H_bill_line.rechnr == h_bill.rechnr) & (H_bill_line.betrag < 0)).order_by(H_bill_line._recid).all():

        h_artikel = get_cache (H_artikel, {"departement": [(eq, h_bill_line.departement)],"artnr": [(eq, h_bill_line.artnr)],"artart": [(ne, 0)]})

        if h_artikel:
            get_amount =  to_decimal(get_amount) + to_decimal(h_bill_line.betrag)

    queasy = get_cache (Queasy, {"key": [(eq, 230)]})

    if queasy:
        update_selforder()

    if active_deposit:
        remove_rsv_table()
    t_h_bill = T_h_bill()
    t_h_bill_data.append(t_h_bill)

    buffer_copy(h_bill, t_h_bill)
    t_h_bill.rec_id = h_bill._recid


    amount =  - to_decimal(amount)
    amount_foreign =  - to_decimal(amount_foreign)

    return generate_output()