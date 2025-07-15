#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from functions.prepare_ts_restinvbl import prepare_ts_restinvbl
from sqlalchemy import func
from functions.ts_restinv_update_bill_1bl import ts_restinv_update_bill_1bl
from models import H_artikel, H_bill, Kellner, Htparam, Hoteldpt, Wgrpgen, Queasy, Bill, Bill_line, Waehrung

def ts_resplan_openbillbl(pvilanguage:int, s_recid:int, curr_dept:int, curr_date:date, recid_hbill:int, user_init:string, pos_printer:int, curr_flag:string):

    prepare_cache ([H_artikel, Htparam, Hoteldpt, Wgrpgen, Queasy, Bill, Bill_line, Waehrung])

    err_flag = False
    result_msg = ""
    lvcarea:string = "ts-resplan"
    exchg_rate:Decimal = 1
    foreign_payment:Decimal = to_decimal("0.0")
    local_payment:Decimal = to_decimal("0.0")
    deposit_foreign:Decimal = to_decimal("0.0")
    deposit_amount:Decimal = to_decimal("0.0")
    price_decimal:int = 0
    depoart:int = 0
    h_depoart:int = 0
    h_depoart_front:int = 0
    h_depoart_type:int = 0
    hart_recid:int = 0
    h_depobez:string = ""
    gname:string = ""
    str1:string = ""
    table_no:int = 0
    pax:int = 0
    gastno:int = 0
    ns_billno:int = 0
    ft_h:int = 0
    ft_m:int = 0
    from_time:int = 0
    bill_date:date = None
    rsv_date:date = None
    amount:Decimal = to_decimal("0.0")
    mealcoupon_cntrl:bool = False
    must_print:bool = False
    zero_flag:bool = False
    multi_cash:bool = False
    cancel_exist:bool = False
    msg_str:string = ""
    disc_art1:int = 0
    disc_art2:int = 0
    disc_art3:int = 0
    mi_ordertaker:bool = True
    curr_local:string = ""
    curr_foreign:string = ""
    double_currency:bool = False
    foreign_rate:bool = False
    b_title:string = ""
    deptname:string = ""
    p_223:bool = False
    curr_waiter:int = 0
    fl_code:int = 0
    pos1:int = 0
    pos2:int = 0
    cashless_flag:bool = False
    price:Decimal = to_decimal("0.0")
    add_zeit:int = 0
    cancel_flag:bool = False
    mwst:Decimal = to_decimal("0.0")
    mwst_foreign:Decimal = to_decimal("0.0")
    balance:Decimal = to_decimal("0.0")
    bcol:int = 0
    balance_foreign:Decimal = to_decimal("0.0")
    fl_code1:int = 0
    fl_code2:int = 0
    fl_code3:int = 0
    p_88:bool = False
    closed:bool = False
    error_str:string = ""
    usr:string = ""
    outlet:string = ""
    err:bool = False
    err1:bool = False
    fract:Decimal = 1
    service_code:int = 0
    rechnr:int = 0
    voucher_str:string = ""
    voucher_depo:string = ""
    rsvtable_text:string = ""
    h_artikel = h_bill = kellner = htparam = hoteldpt = wgrpgen = queasy = bill = bill_line = waehrung = None

    hbill = t_kellner = t_h_artikel = menu_list = t_h_bill = t_submenu_list = kellner1 = None

    hbill_data, Hbill = create_model("Hbill", {"kellner_nr":int})
    t_kellner_data, T_kellner = create_model("T_kellner", {"kellner_nr":int})
    t_h_artikel_data, T_h_artikel = create_model_like(H_artikel, {"rec_id":int})
    menu_list_data, Menu_list = create_model("Menu_list", {"rec_id":int, "description":string, "qty":int, "price":Decimal, "special_request":string})
    t_h_bill_data, T_h_bill = create_model_like(H_bill, {"rec_id":int})
    t_submenu_list_data, T_submenu_list = create_model("T_submenu_list", {"menurecid":int, "zeit":int, "nr":int, "artnr":int, "bezeich":string, "anzahl":int, "zknr":int, "request":string})
    kellner1_data, Kellner1 = create_model_like(Kellner)

    db_session = local_storage.db_session

    def generate_output():
        nonlocal err_flag, result_msg, lvcarea, exchg_rate, foreign_payment, local_payment, deposit_foreign, deposit_amount, price_decimal, depoart, h_depoart, h_depoart_front, h_depoart_type, hart_recid, h_depobez, gname, str1, table_no, pax, gastno, ns_billno, ft_h, ft_m, from_time, bill_date, rsv_date, amount, mealcoupon_cntrl, must_print, zero_flag, multi_cash, cancel_exist, msg_str, disc_art1, disc_art2, disc_art3, mi_ordertaker, curr_local, curr_foreign, double_currency, foreign_rate, b_title, deptname, p_223, curr_waiter, fl_code, pos1, pos2, cashless_flag, price, add_zeit, cancel_flag, mwst, mwst_foreign, balance, bcol, balance_foreign, fl_code1, fl_code2, fl_code3, p_88, closed, error_str, usr, outlet, err, err1, fract, service_code, rechnr, voucher_str, voucher_depo, rsvtable_text, h_artikel, h_bill, kellner, htparam, hoteldpt, wgrpgen, queasy, bill, bill_line, waehrung
        nonlocal pvilanguage, s_recid, curr_dept, curr_date, recid_hbill, user_init, pos_printer, curr_flag


        nonlocal hbill, t_kellner, t_h_artikel, menu_list, t_h_bill, t_submenu_list, kellner1
        nonlocal hbill_data, t_kellner_data, t_h_artikel_data, menu_list_data, t_h_bill_data, t_submenu_list_data, kellner1_data

        return {"err_flag": err_flag, "result_msg": result_msg}


    mealcoupon_cntrl, must_print, zero_flag, multi_cash, cancel_exist, msg_str, disc_art1, disc_art2, disc_art3, mi_ordertaker, price_decimal, curr_local, curr_foreign, double_currency, foreign_rate, exchg_rate, b_title, deptname, p_223, curr_waiter, fl_code, pos1, pos2, cashless_flag, hbill_data, t_kellner_data = get_output(prepare_ts_restinvbl(pvilanguage, curr_dept, pos_printer, user_init, None))

    if msg_str != "":
        err_flag = True
        result_msg = msg_str

        return generate_output()

    htparam = get_cache (Htparam, {"paramnr": [(eq, 1361)]})

    if htparam:
        depoart = htparam.finteger

    hoteldpt = get_cache (Hoteldpt, {"num": [(eq, curr_dept)]})

    if hoteldpt:
        deptname = hoteldpt.depart

    wgrpgen = db_session.query(Wgrpgen).filter(
             (matches(Wgrpgen.bezeich,"*deposit*"))).first()

    if wgrpgen:

        h_artikel = db_session.query(H_artikel).filter(
                 (H_artikel.endkum == wgrpgen.eknr) & (H_artikel.activeflag)).first()

        if h_artikel:
            hart_recid = h_artikel._recid
            h_depoart = h_artikel.artnr
            h_depoart_type = h_artikel.artart
            h_depobez = h_artikel.bezeich
            h_depoart_front = h_artikel.artnrfront
            service_code = service_code

    queasy = get_cache (Queasy, {"_recid": [(eq, s_recid)]})

    if queasy:
        ns_billno = to_int(queasy.deci2)
        gname = entry(0, queasy.char2, "&&")
        gastno = to_int(entry(2, queasy.char2, "&&"))
        ft_h = to_int(substring(queasy.char1, 0, 2))
        ft_m = to_int(substring(queasy.char1, 2, 2))
        rsv_date = queasy.date1
        deposit_amount =  to_decimal(queasy.deci1)
        table_no = queasy.number2
        pax = queasy.number3

    bill = get_cache (Bill, {"rechnr": [(eq, ns_billno)],"gastnr": [(eq, gastno)],"resnr": [(eq, 0)],"reslinnr": [(eq, 1)],"billtyp": [(eq, curr_dept)],"flag": [(eq, 1)]})

    if bill:

        bill_line = get_cache (Bill_line, {"rechnr": [(eq, bill.rechnr)],"artnr": [(eq, depoart)]})

        if bill_line:
            str1 = entry(0, bill_line.bezeich, "[")
            voucher_depo = trim(entry(1, str1, "/"))

    htparam = get_cache (Htparam, {"paramnr": [(eq, 144)]})

    waehrung = get_cache (Waehrung, {"wabkurz": [(eq, htparam.fchar)]})

    if waehrung:
        exchg_rate =  to_decimal(waehrung.ankauf) / to_decimal(waehrung.einheit)
    deposit_foreign =  to_decimal(deposit_amount) / to_decimal(exchg_rate)
    foreign_payment =  - to_decimal(deposit_amount) / to_decimal(exchg_rate)
    local_payment =  - to_decimal(deposit_amount)


    add_zeit = add_zeit + 1
    bill_date, cancel_flag, fl_code, mwst, mwst_foreign, rechnr, balance, bcol, balance_foreign, fl_code1, fl_code2, fl_code3, p_88, closed, t_h_bill_data, kellner1_data = get_output(ts_restinv_update_bill_1bl(pvilanguage, recid_hbill, hart_recid, deptname, None, h_depoart_type, False, service_code, local_payment, foreign_payment, local_payment, double_currency, 1, exchg_rate, price_decimal, user_init, table_no, curr_dept, curr_waiter, gname, pax, 0, add_zeit, h_depoart, h_depobez, "", voucher_depo, "", "", voucher_str, "", True, False, h_depoart_front, 0, gastno, "", False, foreign_rate, "", user_init, 0, 0, False, 0, "", t_submenu_list_data))

    kellner1 = query(kellner1_data, first=True)

    if fl_code == 1:
        err_flag = True
        result_msg = translateExtended ("Transaction not allowed: Posted item(s) with differrent billing date found.", lvcarea, "")

        return generate_output()

    elif fl_code == 2:
        err_flag = True
        result_msg = translateExtended ("Table has occupied with another guest.", lvcarea, "")

        return generate_output()

    t_h_bill = query(t_h_bill_data, first=True)

    if t_h_bill:

        if curr_flag != "":
            rsvtable_text = "Delete RSV Table"
        else:
            rsvtable_text = ""
        queasy = Queasy()
        db_session.add(queasy)

        queasy.key = 251
        queasy.char1 = rsvtable_text
        queasy.number1 = t_h_bill.rec_id
        queasy.number2 = s_recid


        pass

    return generate_output()