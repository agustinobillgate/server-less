#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from functions.htplogic import htplogic
from functions.read_billbl import read_billbl
from functions.htpdate import htpdate
from functions.fo_invoice_disp_totbalancebl import fo_invoice_disp_totbalancebl
from functions.fo_invoice_disp_bill_linebl import fo_invoice_disp_bill_linebl
from models import Bill, Bill_line, Bediener, Htparam, Artikel, Res_line, Umsatz, Billjournal

def fo_inv_paywith_deposit_webbl(pvilanguage:int, bill_recid:int, user_init:string, curr_rechnr:int, res_number:int, resllin_number:int, bill_flag:int, transdate:date, tbill_flag:int, change_date:bool, pay_depoamount:Decimal, amount_foreign:Decimal, curr_room:string, exchg_rate:Decimal, price_decimal:int, double_currency:bool, p_83:bool, kreditlimit:Decimal, foreign_rate:bool, bill_date:date, voucher_nr:string, cancel_str:string):

    prepare_cache ([Bill_line, Htparam, Artikel, Res_line, Umsatz, Billjournal])

    error_desc = ""
    balance = to_decimal("0.0")
    balance_foreign = to_decimal("0.0")
    void_approve = False
    flag3 = 0
    tot_balance = to_decimal("0.0")
    t_bill_data = []
    t_bill_line_data = []
    spbill_list_data = []
    lvcarea:string = "fo-inv-paywith-deposit-webBL"
    depoart:int = 0
    depobez:string = ""
    p_253:bool = False
    zugriff:bool = True
    billdatum:date = None
    r_recid:int = 0
    na_running:bool = False
    gastnrmember:int = 0
    bill = bill_line = bediener = htparam = artikel = res_line = umsatz = billjournal = None

    t_bill = spbill_list = t_bill_line = tp_bediener = None

    t_bill_data, T_bill = create_model_like(Bill)
    spbill_list_data, Spbill_list = create_model("Spbill_list", {"selected":bool, "bl_recid":int}, {"selected": True})
    t_bill_line_data, T_bill_line = create_model_like(Bill_line, {"rec_id":int})
    tp_bediener_data, Tp_bediener = create_model_like(Bediener)

    db_session = local_storage.db_session

    def generate_output():
        nonlocal error_desc, balance, balance_foreign, void_approve, flag3, tot_balance, t_bill_data, t_bill_line_data, spbill_list_data, lvcarea, depoart, depobez, p_253, zugriff, billdatum, r_recid, na_running, gastnrmember, bill, bill_line, bediener, htparam, artikel, res_line, umsatz, billjournal
        nonlocal pvilanguage, bill_recid, user_init, curr_rechnr, res_number, resllin_number, bill_flag, transdate, tbill_flag, change_date, pay_depoamount, amount_foreign, curr_room, exchg_rate, price_decimal, double_currency, p_83, kreditlimit, foreign_rate, bill_date, voucher_nr, cancel_str


        nonlocal t_bill, spbill_list, t_bill_line, tp_bediener
        nonlocal t_bill_data, spbill_list_data, t_bill_line_data, tp_bediener_data

        return {"cancel_str": cancel_str, "error_desc": error_desc, "balance": balance, "balance_foreign": balance_foreign, "void_approve": void_approve, "flag3": flag3, "tot_balance": tot_balance, "t-bill": t_bill_data, "t-bill-line": t_bill_line_data, "spbill-list": spbill_list_data}

    def update_to_bill():

        nonlocal error_desc, balance, balance_foreign, void_approve, flag3, tot_balance, t_bill_data, t_bill_line_data, spbill_list_data, lvcarea, depoart, depobez, p_253, zugriff, billdatum, r_recid, na_running, gastnrmember, bill, bill_line, bediener, htparam, artikel, res_line, umsatz, billjournal
        nonlocal pvilanguage, bill_recid, user_init, curr_rechnr, res_number, resllin_number, bill_flag, transdate, tbill_flag, change_date, pay_depoamount, amount_foreign, curr_room, exchg_rate, price_decimal, double_currency, p_83, kreditlimit, foreign_rate, bill_date, voucher_nr, cancel_str


        nonlocal t_bill, spbill_list, t_bill_line, tp_bediener
        nonlocal t_bill_data, spbill_list_data, t_bill_line_data, tp_bediener_data

        bill = get_cache (Bill, {"_recid": [(eq, bill_recid)]})
        r_recid = bill._recid

        bill = get_cache (Bill, {"_recid": [(eq, r_recid)]})

        if bill.flag == 1 and bill_flag == 0:
            error_desc = translateExtended ("The Bill was closed / guest checked out", lvcarea, "") + chr_unicode(10) + "Bill entry is no longer possible!"
            pass
            pass

            return
        else:
            balance =  to_decimal(balance) + to_decimal(pay_depoamount)
            balance_foreign =  to_decimal(balance_foreign) + to_decimal(amount_foreign)
            bill.saldo =  to_decimal(bill.saldo) + to_decimal(pay_depoamount)

            if price_decimal == 0 and bill.saldo <= 0.4 and bill.saldo >= -0.4:
                bill.saldo =  to_decimal("0")

            if double_currency or foreign_rate:
                bill.mwst[98] = bill.mwst[98] + amount_foreign

            if bill.datum < bill_date or bill.datum == None:
                bill.datum = bill_date

            htparam = get_cache (Htparam, {"paramnr": [(eq, 253)]})
            na_running = htparam.flogical

            htparam = get_cache (Htparam, {"paramnr": [(eq, 110)]})
            bill_date = htparam.fdate

            if transdate != None:
                bill_date = transdate
            else:

                if na_running and bill_date < get_current_date():
                    bill_date = bill_date + timedelta(days=1)

            res_line = get_cache (Res_line, {"resnr": [(eq, bill.resnr)],"reslinnr": [(eq, bill.reslinnr)]})

            if res_line:
                gastnrmember = res_line.gastnrmember
            else:
                gastnrmember = bill.gastnr
            bill_line = Bill_line()
            db_session.add(bill_line)

            bill_line.rechnr = bill.rechnr
            bill_line.artnr = depoart
            bill_line.bezeich = depobez
            bill_line.anzahl = 1
            bill_line.betrag =  to_decimal(pay_depoamount)
            bill_line.fremdwbetrag =  to_decimal(amount_foreign)
            bill_line.zinr = curr_room
            bill_line.departement = artikel.departement
            bill_line.bill_datum = bill_date
            bill_line.zeit = get_current_time_in_seconds()
            bill_line.userinit = user_init

            if voucher_nr != "":
                bill_line.bezeich = bill_line.bezeich + "/" + voucher_nr

            if res_line:
                bill_line.massnr = res_line.resnr
                bill_line.billin_nr = res_line.reslinnr
                bill_line.arrangement = res_line.arrangement


            pass

            umsatz = get_cache (Umsatz, {"artnr": [(eq, depoart)],"departement": [(eq, artikel.departement)],"datum": [(eq, bill_date)]})

            if not umsatz:
                umsatz = Umsatz()
                db_session.add(umsatz)

                umsatz.artnr = depoart
                umsatz.datum = bill_date
                umsatz.departement = artikel.departement


            umsatz.betrag =  to_decimal(umsatz.betrag) + to_decimal(pay_depoamount)
            umsatz.anzahl = umsatz.anzahl + 1


            pass
            billjournal = Billjournal()
            db_session.add(billjournal)

            billjournal.rechnr = bill.rechnr
            billjournal.artnr = depoart
            billjournal.anzahl = 1
            billjournal.fremdwaehrng =  to_decimal(amount_foreign)
            billjournal.betrag =  to_decimal(pay_depoamount)
            billjournal.bezeich = depobez
            billjournal.zinr = curr_room
            billjournal.departement = artikel.departement
            billjournal.epreis =  to_decimal(pay_depoamount)
            billjournal.zeit = get_current_time_in_seconds()
            billjournal.stornogrund = cancel_str
            billjournal.userinit = user_init
            billjournal.bill_datum = bill_date
            cancel_str = ""
            void_approve = False

            if res_line:
                billjournal.comment = to_string(res_line.resnr) + ";" + to_string(res_line.reslinnr)

            if voucher_nr != "":
                billjournal.bezeich = billjournal.bezeich + "/" + voucher_nr
            pass
        balance =  to_decimal(bill.saldo)

        if double_currency or foreign_rate:
            balance_foreign =  to_decimal(bill.mwst[98])
        flag3 = 1
        pass
        t_bill = T_bill()
        t_bill_data.append(t_bill)

        buffer_copy(bill, t_bill)


    def zugriff_test(user_init:string, array_nr:int, expected_nr:int):

        nonlocal error_desc, balance, balance_foreign, void_approve, flag3, tot_balance, t_bill_data, t_bill_line_data, spbill_list_data, lvcarea, depoart, depobez, p_253, zugriff, billdatum, r_recid, na_running, gastnrmember, bill, bill_line, bediener, htparam, artikel, res_line, umsatz, billjournal
        nonlocal pvilanguage, bill_recid, curr_rechnr, res_number, resllin_number, bill_flag, transdate, tbill_flag, change_date, pay_depoamount, amount_foreign, curr_room, exchg_rate, price_decimal, double_currency, p_83, kreditlimit, foreign_rate, bill_date, voucher_nr, cancel_str


        nonlocal t_bill, spbill_list, t_bill_line, tp_bediener
        nonlocal t_bill_data, spbill_list_data, t_bill_line_data, tp_bediener_data

        zugriff = True
        msgstr = ""
        n:int = 0
        perm:List[int] = create_empty_list(120,0)
        s1:string = ""
        s2:string = ""

        def generate_inner_output():
            return (zugriff, msgstr)


        if user_init == "":
            zugriff = False
            msgstr = translateExtended ("User not defined.", lvcarea, "")

            return generate_inner_output()
        else:

            bediener = get_cache (Bediener, {"userinit": [(eq, user_init)]})

            if bediener:
                tp_bediener = Tp_bediener()
                tp_bediener_data.append(tp_bediener)

                buffer_copy(bediener, tp_bediener)
            else:
                zugriff = False
                msgstr = translateExtended ("User not defined.", lvcarea, "")

                return generate_inner_output()
        for n in range(1,length(tp_bediener.permissions)  + 1) :
            perm[n - 1] = to_int(substring(tp_bediener.permissions, n - 1, 1))

        if perm[array_nr - 1] < expected_nr:
            zugriff = False
            s1 = to_string(array_nr, "999")
            s2 = to_string(expected_nr)
            msgstr = translateExtended ("Sorry, No Access Right, Access Code =", lvcarea, "") + " " + s1 + s2

            return generate_inner_output()

        return generate_inner_output()


    def disp_bill_line():

        nonlocal error_desc, balance, balance_foreign, void_approve, flag3, tot_balance, t_bill_data, t_bill_line_data, spbill_list_data, lvcarea, depoart, depobez, p_253, zugriff, billdatum, r_recid, na_running, gastnrmember, bill, bill_line, bediener, htparam, artikel, res_line, umsatz, billjournal
        nonlocal pvilanguage, bill_recid, user_init, curr_rechnr, res_number, resllin_number, bill_flag, transdate, tbill_flag, change_date, pay_depoamount, amount_foreign, curr_room, exchg_rate, price_decimal, double_currency, p_83, kreditlimit, foreign_rate, bill_date, voucher_nr, cancel_str


        nonlocal t_bill, spbill_list, t_bill_line, tp_bediener
        nonlocal t_bill_data, spbill_list_data, t_bill_line_data, tp_bediener_data


        t_bill_line_data, spbill_list_data = get_output(fo_invoice_disp_bill_linebl(bill_recid, double_currency))

    htparam = get_cache (Htparam, {"paramnr": [(eq, 1068)]})

    if htparam:

        artikel = get_cache (Artikel, {"artnr": [(eq, htparam.finteger)],"departement": [(eq, 0)]})

        if not artikel or artikel.artart != 5:
            error_desc = translateExtended ("Deposit article not defined.", lvcarea, "")

            return generate_output()
        depoart = artikel.artnr
        depobez = artikel.bezeich


    p_253 = get_output(htplogic(253))

    if p_253:
        error_desc = translateExtended ("Night Audit is running, posting not possible", lvcarea, "")

        return generate_output()

    if curr_rechnr != 0:
        t_bill_data = get_output(read_billbl(2, curr_rechnr, res_number, resllin_number, bill_flag))

        t_bill = query(t_bill_data, first=True)

        if t_bill and t_bill.flag == 1:
            zugriff, error_desc = zugriff_test(user_init, 38, 2)

            if not zugriff:
                error_desc = translateExtended ("Not possible", lvcarea, "") + chr_unicode(10) + translateExtended ("Selected Bill Already Closed", lvcarea, "")

                return generate_output()
    billdatum = get_output(htpdate(110))

    if transdate != None:
        billdatum = transdate

    res_line = get_cache (Res_line, {"resnr": [(eq, res_number)],"reslinnr": [(eq, resllin_number)]})

    if res_line and tbill_flag == 1 and change_date:

        if billdatum > res_line.abreise:
            error_desc = translateExtended ("Posting Date Can not be later than Check-out Date", lvcarea, "") + " " + to_string(res_line.abreise)

            return generate_output()
    update_to_bill()

    t_bill = query(t_bill_data, first=True)

    if flag3 == 1:

        if t_bill:
            disp_bill_line()

    if bill_flag == 0:
        tot_balance =  to_decimal("0")

        if t_bill.parent_nr == 0:
            tot_balance =  to_decimal(t_bill.saldo)
        else:
            tot_balance = get_output(fo_invoice_disp_totbalancebl(bill_recid))

    return generate_output()