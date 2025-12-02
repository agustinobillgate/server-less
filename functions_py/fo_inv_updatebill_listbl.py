#using conversion tools version: 1.0.0.117
#------------------------------------------
# Rd, 3/12/2025, Locking Test
#------------------------------------------
from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from functions.htplogic import htplogic
from functions.read_billbl import read_billbl
from functions.htpdate import htpdate
from functions.fo_invoice_update_bill1bl import fo_invoice_update_bill1bl
from functions.fo_invoice_update_masterbillbl import fo_invoice_update_masterbillbl
from functions.fo_invoice_update_bill2bl import fo_invoice_update_bill2bl
from functions.fo_invoice_disp_totbalancebl import fo_invoice_disp_totbalancebl
from functions.fo_invoice_disp_bill_linebl import fo_invoice_disp_bill_linebl
from models import Bill, Bill_line, Bediener, Res_line, Artikel

def fo_inv_updatebill_listbl(bil_recid:int, curr_rechnr:int, tbill_flag:int, change_date:bool, resnr:int, 
                             reslinnr:int, pvilanguage:int, bil_flag:int, transdate:date, billart:int, curr_department:int, 
                             amount:Decimal, amount_foreign:Decimal, description:string, qty:int, curr_room:string, user_init:string, 
                             artnr:int, price:Decimal, exchg_rate:Decimal, price_decimal:int, double_currency:bool, p_83:bool, 
                             kreditlimit:Decimal, foreign_rate:bool, bill_date:date, voucher_nr:string, cancel_str:string):

    prepare_cache ([Res_line, Artikel])

    msgstr = ""
    master_str = ""
    master_rechnr = ""
    balance = to_decimal("0.0")
    balance_foreign = to_decimal("0.0")
    void_approve = False
    flag2 = 0
    flag3 = 0
    tot_balance = to_decimal("0.0")
    t_bill_data = []
    t_bill_line_data = []
    spbill_list_data = []
    lvcarea:string = "fo-inv-updatebill-list"
    room:string = ""
    gname:string = ""
    billdatum:date = None
    skip_it:bool = False
    buff_rechnr:int = 0
    master_flag:bool = False
    currzeit:int = 0
    ex_rate:Decimal = to_decimal("0.0")
    mess_str:string = ""
    msg_str:string = ""
    flag1:int = 0
    rechnr:int = 0
    cancel_flag:bool = False
    p_253:bool = False
    zugriff:bool = True
    err_str:string = ""
    bill = bill_line = bediener = res_line = artikel = None

    t_bill = spbill_list = t_bill_line = tp_bediener = None

    t_bill_data, T_bill = create_model_like(Bill)
    spbill_list_data, Spbill_list = create_model("Spbill_list", {"selected":bool, "bl_recid":int}, {"selected": True})
    t_bill_line_data, T_bill_line = create_model_like(Bill_line, {"rec_id":int})
    tp_bediener_data, Tp_bediener = create_model_like(Bediener)
    """
    def fo_inv_updatebill_listbl(bil_recid:int, curr_rechnr:int, tbill_flag:int, change_date:bool, resnr:int, 
                             reslinnr:int, pvilanguage:int, bil_flag:int, transdate:date, billart:int, curr_department:int, 
                             amount:Decimal, amount_foreign:Decimal, description:string, qty:int, curr_room:string, user_init:string, 
                             artnr:int, price:Decimal, exchg_rate:Decimal, price_decimal:int, double_currency:bool, p_83:bool, 
                             kreditlimit:Decimal, foreign_rate:bool, bill_date:date, voucher_nr:string, cancel_str:string):"""
    db_session = local_storage.db_session
    description = description.strip()
    curr_room = curr_room.strip()
    voucher_nr = voucher_nr.strip()
    cancel_str = cancel_str.strip()
    

    def generate_output():
        nonlocal msgstr, master_str, master_rechnr, balance, balance_foreign, void_approve, flag2, flag3, tot_balance, t_bill_data, t_bill_line_data, spbill_list_data, lvcarea, room, gname, billdatum, skip_it, buff_rechnr, master_flag, currzeit, ex_rate, mess_str, msg_str, flag1, rechnr, cancel_flag, p_253, zugriff, err_str, bill, bill_line, bediener, res_line, artikel
        nonlocal bil_recid, curr_rechnr, tbill_flag, change_date, resnr, reslinnr, pvilanguage, bil_flag, transdate, billart, curr_department, amount, amount_foreign, description, qty, curr_room, user_init, artnr, price, exchg_rate, price_decimal, double_currency, p_83, kreditlimit, foreign_rate, bill_date, voucher_nr, cancel_str


        nonlocal t_bill, spbill_list, t_bill_line, tp_bediener
        nonlocal t_bill_data, spbill_list_data, t_bill_line_data, tp_bediener_data

        return {"cancel_str": cancel_str, "msgstr": msgstr, "master_str": master_str, "master_rechnr": master_rechnr, "balance": balance, "balance_foreign": balance_foreign, "void_approve": void_approve, "flag2": flag2, "flag3": flag3, "tot_balance": tot_balance, "t-bill": t_bill_data, "t-bill-line": t_bill_line_data, "spbill-list": spbill_list_data}

    def red_bcol():

        nonlocal msgstr, master_str, master_rechnr, balance, balance_foreign, void_approve, flag2, flag3, tot_balance, t_bill_data, t_bill_line_data, spbill_list_data, lvcarea, room, gname, billdatum, skip_it, buff_rechnr, master_flag, currzeit, ex_rate, mess_str, msg_str, flag1, rechnr, cancel_flag, p_253, zugriff, err_str, bill, bill_line, bediener, res_line, artikel
        nonlocal bil_recid, curr_rechnr, tbill_flag, change_date, resnr, reslinnr, pvilanguage, bil_flag, transdate, billart, curr_department, amount, amount_foreign, description, qty, curr_room, user_init, artnr, price, exchg_rate, price_decimal, double_currency, p_83, kreditlimit, foreign_rate, bill_date, voucher_nr, cancel_str


        nonlocal t_bill, spbill_list, t_bill_line, tp_bediener
        nonlocal t_bill_data, spbill_list_data, t_bill_line_data, tp_bediener_data

        if p_83:
            msgstr = translateExtended ("Transaction goes over creditlimit of", lvcarea, "") + " " + trim(to_string(kreditlimit, ">,>>>,>>>,>>9.99"))


    def disp_bill_line():

        nonlocal msgstr, master_str, master_rechnr, balance, balance_foreign, void_approve, flag2, flag3, tot_balance, t_bill_data, t_bill_line_data, spbill_list_data, lvcarea, room, gname, billdatum, skip_it, buff_rechnr, master_flag, currzeit, ex_rate, mess_str, msg_str, flag1, rechnr, cancel_flag, p_253, zugriff, err_str, bill, bill_line, bediener, res_line, artikel
        nonlocal bil_recid, curr_rechnr, tbill_flag, change_date, resnr, reslinnr, pvilanguage, bil_flag, transdate, billart, curr_department, amount, amount_foreign, description, qty, curr_room, user_init, artnr, price, exchg_rate, price_decimal, double_currency, p_83, kreditlimit, foreign_rate, bill_date, voucher_nr, cancel_str


        nonlocal t_bill, spbill_list, t_bill_line, tp_bediener
        nonlocal t_bill_data, spbill_list_data, t_bill_line_data, tp_bediener_data


        t_bill_line_data, spbill_list_data = get_output(fo_invoice_disp_bill_linebl(bil_recid, double_currency))


    def zugriff_test(user_init:string, array_nr:int, expected_nr:int):

        nonlocal msgstr, master_str, master_rechnr, balance, balance_foreign, void_approve, flag2, flag3, tot_balance, t_bill_data, t_bill_line_data, spbill_list_data, lvcarea, room, gname, billdatum, skip_it, buff_rechnr, master_flag, currzeit, ex_rate, mess_str, msg_str, flag1, rechnr, cancel_flag, p_253, zugriff, err_str, bill, bill_line, bediener, res_line, artikel
        nonlocal bil_recid, curr_rechnr, tbill_flag, change_date, resnr, reslinnr, pvilanguage, bil_flag, transdate, billart, curr_department, amount, amount_foreign, description, qty, curr_room, artnr, price, exchg_rate, price_decimal, double_currency, p_83, kreditlimit, foreign_rate, bill_date, voucher_nr, cancel_str


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


    p_253 = get_output(htplogic(253))

    if p_253:
        msgstr = translateExtended ("Night Audit is running, posting not possible", lvcarea, "")

        return generate_output()

    if curr_rechnr != 0:
        t_bill_data = get_output(read_billbl(2, curr_rechnr, resnr, reslinnr, bil_flag))

        t_bill = query(t_bill_data, first=True)

        if t_bill and t_bill.flag == 1:
            zugriff, msgstr = zugriff_test(user_init, 38, 2)

            if not zugriff:
                msgstr = translateExtended ("Not possible", lvcarea, "") + chr_unicode(10) + translateExtended ("Selected Bill Already Closed", lvcarea, "")

                return generate_output()
    billdatum = get_output(htpdate(110))

    if transdate != None:
        billdatum = transdate

    res_line = get_cache (Res_line, {"resnr": [(eq, resnr)],"reslinnr": [(eq, reslinnr)]})

    if res_line and tbill_flag == 1 and change_date:

        if billdatum > res_line.abreise:
            msgstr = translateExtended ("Posting Date Can not be later than Check-out Date", lvcarea, "") + " " + to_string(res_line.abreise)

            return generate_output()

    artikel = get_cache (Artikel, {"artnr": [(eq, billart)],"departement": [(eq, curr_department)]})

    if artikel.artart == 9 and artikel.artgrp == 0:
        skip_it, buff_rechnr = get_output(fo_invoice_update_bill1bl(resnr, reslinnr, billdatum))

        if skip_it:

            if buff_rechnr == -1:
                msgstr = translateExtended ("Posting room Charge is not allowed when Night Audit is Running.", lvcarea, "")
            else:
                msgstr = translateExtended ("Not possible", lvcarea, "") + chr_unicode(10) + translateExtended ("room Charge Already Posted", lvcarea, "") + " to bill no " + to_string(buff_rechnr)

            return generate_output()
    currzeit = get_current_time_in_seconds()
    master_flag = False

    bill = get_cache (Bill, {"_recid": [(eq, bil_recid)]})

    if not bill:

        return generate_output()

    if tbill_flag == 0:
        ex_rate, mess_str, master_str, master_rechnr, master_flag = get_output(fo_invoice_update_masterbillbl(pvilanguage, bil_recid, curr_department, currzeit, amount, amount_foreign, billart, description, qty, curr_room, user_init, artikel.artnr, price, cancel_str, exchg_rate, price_decimal, double_currency, master_flag))

        if mess_str != "":
            msgstr = mess_str

    if not master_flag:
        msg_str, balance, balance_foreign, cancel_flag, void_approve, flag1, flag2, flag3, rechnr, t_bill_data = get_output(fo_invoice_update_bill2bl(pvilanguage, bil_recid, artikel.artnr, bil_flag, amount, amount_foreign, price_decimal, double_currency, foreign_rate, bill_date, transdate, billart, description, qty, curr_room, user_init, artikel.artnr, price, cancel_str, currzeit, voucher_nr, exchg_rate, bil_recid, artikel.departement))

        if msg_str != "":
            msgstr = msg_str

            return generate_output()

        t_bill = query(t_bill_data, first=True)

        if flag2 == 1:

            if balance > kreditlimit:
                red_bcol()

        if flag3 == 1:

            if balance > kreditlimit:
                red_bcol()

            if t_bill:
                disp_bill_line()

    if bil_flag == 0:
        tot_balance =  to_decimal("0")

        if t_bill.parent_nr == 0:
            tot_balance =  to_decimal(t_bill.saldo)
        else:
            tot_balance = get_output(fo_invoice_disp_totbalancebl(bil_recid))
    cancel_str = ""

    return generate_output()