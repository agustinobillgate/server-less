#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from functions.htplogic import htplogic
from functions.read_bill2bl import read_bill2bl
from models import Bill_line, Bill, Res_line, Artikel, Htparam, Waehrung, Counters, Umsatz, Billjournal

def mbns_inv_paywith_deposit_webbl(pvilanguage:int, bil_flag:int, b_recid:int, t_bill_rechnr:int, bill_line_departement:int, transdate:date, billart:int, qty:int, price:Decimal, amount:Decimal, amount_foreign:Decimal, description:string, voucher_nr:string, cancel_str:string, user_init:string, rechnr:int, balance:Decimal, balance_foreign:Decimal):

    prepare_cache ([Bill, Artikel, Htparam, Waehrung, Counters, Umsatz, Billjournal])

    error_desc = ""
    success_flag = False
    t_bill_list = []
    t_bill_line_list = []
    lvcarea:string = "mbns-inv-paywith-deposit-webBL"
    master_str:string = ""
    master_rechnr:string = ""
    master_flag:bool = False
    str1:string = "NS"
    bline_dept:int = 0
    gname:string = ""
    bil_recid:int = 0
    telbill_flag:bool = False
    babill_flag:bool = False
    depoart:int = 0
    depobez:string = ""
    p_253:bool = False
    gastnrmember:int = 0
    price_decimal:int = 0
    double_currency:bool = False
    foreign_rate:bool = False
    exchg_rate:Decimal = 1
    currzeit:int = 0
    bill_date:date = None
    curr_room:string = ""
    skip_it:bool = False
    bill_line = bill = res_line = artikel = htparam = waehrung = counters = umsatz = billjournal = None

    t_bill_line = t_blinebuff = t_bill = resline = buf_artikel = buf_bill_line = None

    t_bill_line_list, T_bill_line = create_model_like(Bill_line, {"bl_recid":int, "artart":int, "tool_tip":string})
    t_blinebuff_list, T_blinebuff = create_model_like(Bill_line, {"bl_recid":int, "artart":int, "tool_tip":string})
    t_bill_list, T_bill = create_model_like(Bill, {"bl_recid":int})

    Resline = create_buffer("Resline",Res_line)
    Buf_artikel = create_buffer("Buf_artikel",Artikel)
    Buf_bill_line = create_buffer("Buf_bill_line",Bill_line)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal error_desc, success_flag, t_bill_list, t_bill_line_list, lvcarea, master_str, master_rechnr, master_flag, str1, bline_dept, gname, bil_recid, telbill_flag, babill_flag, depoart, depobez, p_253, gastnrmember, price_decimal, double_currency, foreign_rate, exchg_rate, currzeit, bill_date, curr_room, skip_it, bill_line, bill, res_line, artikel, htparam, waehrung, counters, umsatz, billjournal
        nonlocal pvilanguage, bil_flag, b_recid, t_bill_rechnr, bill_line_departement, transdate, billart, qty, price, amount, amount_foreign, description, voucher_nr, cancel_str, user_init, rechnr, balance, balance_foreign
        nonlocal resline, buf_artikel, buf_bill_line


        nonlocal t_bill_line, t_blinebuff, t_bill, resline, buf_artikel, buf_bill_line
        nonlocal t_bill_line_list, t_blinebuff_list, t_bill_list

        return {"rechnr": rechnr, "balance": balance, "balance_foreign": balance_foreign, "error_desc": error_desc, "success_flag": success_flag, "t-bill": t_bill_list, "t-bill-line": t_bill_line_list}

    def update_to_bill():

        nonlocal error_desc, success_flag, t_bill_list, t_bill_line_list, lvcarea, master_str, master_rechnr, master_flag, str1, bline_dept, gname, bil_recid, telbill_flag, babill_flag, depoart, depobez, p_253, gastnrmember, price_decimal, double_currency, foreign_rate, exchg_rate, currzeit, bill_date, curr_room, skip_it, bill_line, bill, res_line, artikel, htparam, waehrung, counters, umsatz, billjournal
        nonlocal pvilanguage, bil_flag, b_recid, t_bill_rechnr, bill_line_departement, transdate, billart, qty, price, amount, amount_foreign, description, voucher_nr, cancel_str, user_init, rechnr, balance, balance_foreign
        nonlocal resline, buf_artikel, buf_bill_line


        nonlocal t_bill_line, t_blinebuff, t_bill, resline, buf_artikel, buf_bill_line
        nonlocal t_bill_line_list, t_blinebuff_list, t_bill_list

        htparam = get_cache (Htparam, {"paramnr": [(eq, 110)]})
        bill_date = htparam.fdate

        if transdate != None:
            bill_date = transdate
        else:

            htparam = get_cache (Htparam, {"paramnr": [(eq, 253)]})

            if htparam.flogical and bill_date < get_current_date():
                bill_date = bill_date + timedelta(days=1)

        if amount_foreign == None:
            amount_foreign =  to_decimal("0")

        bill = get_cache (Bill, {"_recid": [(eq, b_recid)]})

        if bill.flag == 1 and bil_flag == 0:
            error_desc = translateExtended ("The Bill was closed / guest checked out", lvcarea, "") + chr_unicode(10) + translateExtended ("Bill entry is no longer possible!", lvcarea, "")
            success_flag = False

            return
        pass
        curr_room = bill.zinr
        gastnrmember = bill.gastnr

        if not artikel.autosaldo:
            bill.rgdruck = 0

        if bill.datum < bill_date or bill.datum == None:
            bill.datum = bill_date
        bill.saldo =  to_decimal(bill.saldo) + to_decimal(amount)

        if double_currency or foreign_rate:
            bill.mwst[98] = bill.mwst[98] + amount_foreign

        if bill.rechnr == 0:

            counters = get_cache (Counters, {"counter_no": [(eq, 3)]})
            counters.counter = counters.counter + 1
            bill.rechnr = counters.counter

            if transdate != None:
                bill.datum = transdate
            pass
        rechnr = bill.rechnr


        bill_line = Bill_line()
        db_session.add(bill_line)

        bill_line.rechnr = bill.rechnr
        bill_line.massnr = bill.resnr
        bill_line.billin_nr = bill.reslinnr
        bill_line.zinr = curr_room
        bill_line.artnr = depoart
        bill_line.anzahl = 1
        bill_line.betrag =  to_decimal(amount)
        bill_line.fremdwbetrag =  to_decimal(amount_foreign)
        bill_line.bezeich = depobez
        bill_line.departement = artikel.departement
        bill_line.zeit = get_current_time_in_seconds()
        bill_line.userinit = user_init
        bill_line.bill_datum = bill_date

        if voucher_nr != "":
            bill_line.bezeich = bill_line.bezeich + "/" + voucher_nr
        pass
        t_bill_line = T_bill_line()
        t_bill_line_list.append(t_bill_line)

        buffer_copy(bill_line, t_bill_line)
        t_bill_line.artart = artikel.artart
        t_bill_line.bl_recid = to_int(bill_line._recid)

        umsatz = get_cache (Umsatz, {"artnr": [(eq, depoart)],"departement": [(eq, artikel.departement)],"datum": [(eq, bill_date)]})

        if not umsatz:
            umsatz = Umsatz()
            db_session.add(umsatz)

            umsatz.artnr = depoart
            umsatz.datum = bill_date
            umsatz.departement = artikel.departement


        umsatz.betrag =  to_decimal(umsatz.betrag) + to_decimal(amount)
        umsatz.anzahl = umsatz.anzahl + 1


        pass
        billjournal = Billjournal()
        db_session.add(billjournal)

        billjournal.rechnr = bill.rechnr
        billjournal.zinr = curr_room
        billjournal.artnr = depoart
        billjournal.anzahl = 1
        billjournal.fremdwaehrng =  to_decimal(amount_foreign)
        billjournal.betrag =  to_decimal(amount)
        billjournal.bezeich = depobez
        billjournal.departement = artikel.departement
        billjournal.epreis =  to_decimal(price)
        billjournal.zeit = get_current_time_in_seconds()
        billjournal.stornogrund = cancel_str
        billjournal.userinit = user_init
        billjournal.bill_datum = bill_date

        if voucher_nr != "":
            billjournal.bezeich = billjournal.bezeich + "/" + voucher_nr
        pass
        balance =  to_decimal(bill.saldo)

        if double_currency or foreign_rate:
            balance_foreign =  to_decimal(bill.mwst[98])
        pass


    htparam = get_cache (Htparam, {"paramnr": [(eq, 1068)]})

    if htparam:

        artikel = get_cache (Artikel, {"artnr": [(eq, htparam.finteger)],"departement": [(eq, 0)]})

        if not artikel or artikel.artart != 5:
            error_desc = translateExtended ("Deposit article not defined.", lvcarea, "")
            success_flag = False

            return generate_output()
        depoart = artikel.artnr
        depobez = artikel.bezeich


    p_253 = get_output(htplogic(253))

    if p_253:
        error_desc = translateExtended ("Night Audit is running, posting not possible", lvcarea, "")
        success_flag = False

        return generate_output()

    htparam = get_cache (Htparam, {"paramnr": [(eq, 491)]})
    price_decimal = htparam.finteger

    htparam = get_cache (Htparam, {"paramnr": [(eq, 240)]})
    double_currency = htparam.flogical

    htparam = get_cache (Htparam, {"paramnr": [(eq, 143)]})
    foreign_rate = htparam.flogical

    if foreign_rate or double_currency:

        htparam = get_cache (Htparam, {"paramnr": [(eq, 144)]})

        waehrung = get_cache (Waehrung, {"wabkurz": [(eq, htparam.fchar)]})

        if waehrung:
            exchg_rate =  to_decimal(waehrung.ankauf) / to_decimal(waehrung.einheit)
    currzeit = get_current_time_in_seconds()
    master_flag = False


    update_to_bill()
    telbill_flag, babill_flag, t_bill_list = get_output(read_bill2bl(5, b_recid, None, None, None, None, None, None, None, None))

    return generate_output()