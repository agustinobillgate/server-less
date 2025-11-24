#using conversion tools version: 1.0.0.117

# =======================================
# Rulita, 17-10-2025 
# Tiket ID : 6526C2 | New compile program
# =======================================
# Rd, 24/11/2025, update last_count for counter update
# =======================================

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from functions.ts_restinv_update_bill1bl import ts_restinv_update_bill1bl
from functions.ts_restinv_update_bill_1bl import ts_restinv_update_bill_1bl
from functions.ts_restinv_btn_transfer_paytypegt1_2bl import ts_restinv_btn_transfer_paytypegt1_2bl
from models import H_bill, Kellner, Bill, Counters, Res_line
from functions.next_counter_for_update import next_counter_for_update

t_submenu_list_data, T_submenu_list = create_model("T_submenu_list", {"menurecid":int, "zeit":int, "nr":int, "artnr":int, "bezeich":string, "anzahl":int, "zknr":int, "request":string})

def ts_restinv_transfer_to_guestbill_webbl(pvilanguage:int, rec_id:int, curr_dept:int, bilrecid:int, balance_foreign:Decimal, 
                                           balance:Decimal, pay_type:int, transdate:date, double_currency:bool, 
                                           exchg_rate:Decimal, kellner1_kcredit_nr:int, foreign_rate:bool, 
                                           user_init:string, price_decimal:int, rec_id_h_artikel:int, deptname:string, 
                                           h_artart:int, cancel_order:bool, h_artikel_service_code:int, order_taker:int, 
                                           tischnr:int, curr_waiter:int, pax:int, kreditlimit:Decimal, add_zeit:int, 
                                           print_to_kitchen:bool, from_acct:bool, h_artnrfront:int, guestnr:int, 
                                           curedept_flag:bool, curr_room:string, hoga_resnr:int, hoga_reslinnr:int, 
                                           incl_vat:bool, get_price:int, mc_str:string, disc_art1:int, disc_art2:int, 
                                           disc_art3:int, t_submenu_list_data:[T_submenu_list]):

    prepare_cache ([H_bill, Bill, Counters, Res_line])

    bill_date = None
    cancel_flag = False
    mwst = to_decimal("0.0")
    mwst_foreign = to_decimal("0.0")
    rechnr = 0
    bcol = 0
    p_88 = False
    closed = False
    avail_bill = False
    billno_str = ""
    cancel_str = ""
    error_message = ""
    t_h_bill_data = []
    t_kellner_data = []
    lvcarea:string = "TS-restinv-transfer-to-guestbill-web"
    billart_bfo:int = 0
    billart:int = 0
    qty:int = 0
    qty_bfo:int = 0
    price:Decimal = to_decimal("0.0")
    amount_foreign:Decimal = to_decimal("0.0")
    amount:Decimal = to_decimal("0.0")
    gname:string = ""
    description:string = ""
    description_bfo:string = ""
    transfer_zinr:string = ""
    fl_code:int = 0
    fl_code1:int = 0
    fl_code2:int = 0
    fl_code3:int = 0
    flag_code:int = 0
    h_bill = kellner = bill = counters = res_line = None

    t_h_bill = t_submenu_list = t_kellner = None

    t_h_bill_data, T_h_bill = create_model_like(H_bill, {"rec_id":int})
    t_kellner_data, T_kellner = create_model_like(Kellner)

    db_session = local_storage.db_session
    last_count = 0
    error_lock = ""
    deptname = deptname.strip()
    curr_room = curr_room.strip()
    user_init = user_init.strip()
    mc_str = mc_str.strip()


    def generate_output():
        nonlocal bill_date, cancel_flag, mwst, mwst_foreign, rechnr, bcol, p_88, closed, avail_bill, billno_str, cancel_str, error_message, t_h_bill_data, t_kellner_data, lvcarea, billart_bfo, billart, qty, qty_bfo, price, amount_foreign, amount, gname, description, description_bfo, transfer_zinr, fl_code, fl_code1, fl_code2, fl_code3, flag_code, h_bill, kellner, bill, counters, res_line
        nonlocal pvilanguage, rec_id, curr_dept, bilrecid, balance_foreign, balance, pay_type, transdate, double_currency, exchg_rate, kellner1_kcredit_nr, foreign_rate, user_init, price_decimal, rec_id_h_artikel, deptname, h_artart, cancel_order, h_artikel_service_code, order_taker, tischnr, curr_waiter, pax, kreditlimit, add_zeit, print_to_kitchen, from_acct, h_artnrfront, guestnr, curedept_flag, curr_room, hoga_resnr, hoga_reslinnr, incl_vat, get_price, mc_str, disc_art1, disc_art2, disc_art3


        nonlocal t_h_bill, t_submenu_list, t_kellner
        nonlocal t_h_bill_data, t_kellner_data

        return {"bill_date": bill_date, "cancel_flag": cancel_flag, "mwst": mwst, "mwst_foreign": mwst_foreign, "rechnr": rechnr, "bcol": bcol, "p_88": p_88, "closed": closed, "avail_bill": avail_bill, "billno_str": billno_str, "cancel_str": cancel_str, "error_message": error_message, "t-h-bill": t_h_bill_data, "t-kellner": t_kellner_data}

    bill = get_cache (Bill, {"_recid": [(eq, bilrecid)]})

    if not bill:
        error_message = "Record ID guest bill not found."

        return generate_output()

    h_bill = get_cache (H_bill, {"_recid": [(eq, rec_id)]})

    if not h_bill:
        error_message = "Record ID Outlet bill not found."

        return generate_output()

    if curr_room == None:
        curr_room = ""

    if user_init == None:
        user_init = ""

    if mc_str == None:
        mc_str = ""

    kellner = get_cache (Kellner, {"kellner_nr": [(eq, h_bill.kellner_nr)],"departement": [(eq, curr_dept)]})

    if kellner:
        t_kellner = T_kellner()
        t_kellner_data.append(t_kellner)

        buffer_copy(kellner, t_kellner)

    t_kellner = query(t_kellner_data, first=True)

    if not t_kellner:
        error_message = "Waiter Account is not found. Please check it."

        return generate_output()

    if bill:
        pass

        if h_bill:
            h_bill.resnr = bill.resnr
            h_bill.reslinnr = bill.reslinnr


            pass
    qty = 1
    price =  to_decimal("0")
    amount_foreign =  - to_decimal(balance_foreign)
    amount =  - to_decimal(balance)
    gname = ""

    if bill.rechnr == 0:

        # counters = get_cache (Counters, {"counter_no": [(eq, 3)]})
        # counters.counter = counters.counter + 1
        # pass
        # pass
        # bill.rechnr = counters.counter

        last_count, error_lock = get_output(next_counter_for_update(3))
        bill.rechnr = last_count
        
        pass

    if pay_type == 2:
        description = "RmNo " + bill.zinr + " *" + to_string(bill.rechnr)
        transfer_zinr = bill.zinr

        res_line = get_cache (Res_line, {"resnr": [(eq, bill.resnr)],"reslinnr": [(eq, bill.reslinnr)]})

        if res_line and h_bill:
            gname = res_line.name
            pass
            h_bill.bilname = gname
            pass
    amount, amount_foreign, bill_date, billart_bfo, qty_bfo, description_bfo, cancel_str, t_h_bill_data = get_output(ts_restinv_update_bill1bl(rec_id, transdate, double_currency, exchg_rate, t_kellner.kcredit_nr, bilrecid, foreign_rate, user_init, gname, hoga_resnr, hoga_reslinnr, price_decimal, amount, amount_foreign))
    pass
    h_bill.flag = 0
    pass
    bill_date, cancel_flag, fl_code, mwst, mwst_foreign, rechnr, balance, bcol, balance_foreign, fl_code1, fl_code2, fl_code3, p_88, closed, t_h_bill_data, t_kellner_data = get_output(ts_restinv_update_bill_1bl(pvilanguage, rec_id, rec_id_h_artikel, deptname, transdate, h_artart, cancel_order, h_artikel_service_code, amount, amount_foreign, price, double_currency, qty, exchg_rate, price_decimal, order_taker, tischnr, curr_dept, curr_waiter, gname, pax, kreditlimit, add_zeit, billart, description, "", "", "", "", "", "", print_to_kitchen, from_acct, h_artnrfront, pay_type, guestnr, transfer_zinr, curedept_flag, foreign_rate, curr_room, user_init, hoga_resnr, hoga_reslinnr, incl_vat, get_price, mc_str, t_submenu_list_data))

    t_h_bill = query(t_h_bill_data, first=True)

    t_kellner = query(t_kellner_data, first=True)

    if fl_code2 == 1:
        billno_str = translateExtended ("BillNo:", lvcarea, "") + " " + to_string(rechnr)

    if h_bill:
        pass
        h_bill.rgdruck = 1
        pass
    bill_date, flag_code, t_h_bill_data = get_output(ts_restinv_btn_transfer_paytypegt1_2bl(rec_id, True, transdate, curr_dept, disc_art1, disc_art2, disc_art3, curr_waiter))

    t_h_bill = query(t_h_bill_data, first=True)
    avail_bill = None != t_h_bill

    return generate_output()