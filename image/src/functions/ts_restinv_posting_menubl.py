from functions.additional_functions import *
import decimal
from datetime import date
from sqlalchemy import func
from functions.ts_restinv_run_help3bl import ts_restinv_run_help3bl
from functions.ts_restinv_update_bill_1bl import ts_restinv_update_bill_1bl
from models import H_artikel, H_bill, Kellner, Bediener

def ts_restinv_posting_menubl(case_type:int, pvilanguage:int, tischnr:int, curr_dept:int, cancel_reason:str, double_currency:bool, exchg_rate:decimal, price_decimal:int, transdate:date, foreign_rate:bool, deptname:str, cancel_order:bool, order_taker:int, curr_waiter:int, gname:str, pax:int, kreditlimit:decimal, change_str:str, cc_comment:str, hoga_card:str, print_to_kitchen:bool, from_acct:bool, pay_type:int, guestnr:int, transfer_zinr:str, curedept_flag:bool, curr_room:str, user_init:str, hoga_resnr:int, hoga_reslinnr:int, incl_vat:bool, get_price:int, mc_str:str, tp_bediener:[Tp_bediener], submenu_list:[Submenu_list], cancel_flag:bool, menu_list:[Menu_list], t_h_bill:[T_h_bill]):
    avail_bill = False
    not_access = False
    not_access1 = False
    bill_date = None
    mwst = 0
    mwst_foreign = 0
    rechnr = 0
    balance = 0
    bcol = 0
    balance_foreign = 0
    fl_code = 0
    fl_code1 = 0
    fl_code2 = 0
    fl_code3 = 0
    fl_code4 = 0
    fl_code5 = 0
    p_88 = False
    closed = False
    amount = 0
    kellner1_list = []
    t_h_artikel_list = []
    menurecid:int = 0
    add_zeit:int = 0
    billart:int = 0
    req_str:str = ""
    voucher_str:str = ""
    request_str:str = ""
    perm:[int] = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    zugriff:bool = True
    loopn:int = 0
    description:str = ""
    qty:int = 0
    price:decimal = 0
    cancel_str:str = ""
    amount_foreign:decimal = 0
    curr_zeit:int = 0
    krecid:int = 0
    h_artikel = h_bill = kellner = bediener = None

    t_menu_list = menu_list = submenu_list = bmenu = t_h_artikel = t_h_bill = kellner1 = t_submenu_list = tp_bediener = tp_bediener1 = None

    t_menu_list_list, T_menu_list = create_model("T_menu_list", {"request":str, "krecid":int, "posted":bool, "nr":int, "artnr":int, "bezeich":str, "anzahl":int, "price":decimal, "betrag":decimal, "voucher":str}, {"anzahl": 1, "voucher": ""})
    menu_list_list, Menu_list = create_model("Menu_list", {"request":str, "krecid":int, "posted":bool, "nr":int, "artnr":int, "bezeich":str, "anzahl":int, "price":decimal, "betrag":decimal, "voucher":str}, {"anzahl": 1, "voucher": ""})
    submenu_list_list, Submenu_list = create_model("Submenu_list", {"menurecid":int, "zeit":int, "nr":int, "artnr":int, "bezeich":str, "anzahl":int, "zknr":int, "request":str})
    bmenu_list, Bmenu = create_model("Bmenu", {"request":str, "krecid":int, "posted":bool, "nr":int, "artnr":int, "bezeich":str, "anzahl":int, "price":decimal, "betrag":decimal, "voucher":str, "rec_menu":int}, {"anzahl": 1, "voucher": ""})
    t_h_artikel_list, T_h_artikel = create_model_like(H_artikel, {"rec_id":int})
    t_h_bill_list, T_h_bill = create_model_like(H_bill, {"rec_id":int})
    kellner1_list, Kellner1 = create_model_like(Kellner)
    t_submenu_list_list, T_submenu_list = create_model("T_submenu_list", {"menurecid":int, "zeit":int, "nr":int, "artnr":int, "bezeich":str, "anzahl":int, "zknr":int, "request":str})
    tp_bediener_list, Tp_bediener = create_model_like(Bediener)
    tp_bediener1_list, Tp_bediener1 = create_model_like(Bediener)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal avail_bill, not_access, not_access1, bill_date, mwst, mwst_foreign, rechnr, balance, bcol, balance_foreign, fl_code, fl_code1, fl_code2, fl_code3, fl_code4, fl_code5, p_88, closed, amount, kellner1_list, t_h_artikel_list, menurecid, add_zeit, billart, req_str, voucher_str, request_str, perm, zugriff, loopn, description, qty, price, cancel_str, amount_foreign, curr_zeit, krecid, h_artikel, h_bill, kellner, bediener


        nonlocal t_menu_list, menu_list, submenu_list, bmenu, t_h_artikel, t_h_bill, kellner1, t_submenu_list, tp_bediener, tp_bediener1
        nonlocal t_menu_list_list, menu_list_list, submenu_list_list, bmenu_list, t_h_artikel_list, t_h_bill_list, kellner1_list, t_submenu_list_list, tp_bediener_list, tp_bediener1_list
        return {"avail_bill": avail_bill, "not_access": not_access, "not_access1": not_access1, "bill_date": bill_date, "mwst": mwst, "mwst_foreign": mwst_foreign, "rechnr": rechnr, "balance": balance, "bcol": bcol, "balance_foreign": balance_foreign, "fl_code": fl_code, "fl_code1": fl_code1, "fl_code2": fl_code2, "fl_code3": fl_code3, "fl_code4": fl_code4, "fl_code5": fl_code5, "p_88": p_88, "closed": closed, "amount": amount, "kellner1": kellner1_list, "t-h-artikel": t_h_artikel_list}

    def update_bill(h_artart:int, h_artnrfront:int):

        nonlocal avail_bill, not_access, not_access1, bill_date, mwst, mwst_foreign, rechnr, balance, bcol, balance_foreign, fl_code, fl_code1, fl_code2, fl_code3, fl_code4, fl_code5, p_88, closed, amount, kellner1_list, t_h_artikel_list, menurecid, add_zeit, billart, req_str, voucher_str, request_str, perm, zugriff, loopn, description, qty, price, cancel_str, amount_foreign, curr_zeit, krecid, h_artikel, h_bill, kellner, bediener


        nonlocal t_menu_list, menu_list, submenu_list, bmenu, t_h_artikel, t_h_bill, kellner1, t_submenu_list, tp_bediener, tp_bediener1
        nonlocal t_menu_list_list, menu_list_list, submenu_list_list, bmenu_list, t_h_artikel_list, t_h_bill_list, kellner1_list, t_submenu_list_list, tp_bediener_list, tp_bediener1_list

        do_itprint:bool = False
        by_txtprint:bool = False
        closed:bool = False
        rec_id:int = 0
        rec_id_artikel:int = 0
        service_code:int = 0

        if h_artart == 0:

            tp_bediener1 = query(tp_bediener1_list, first=True)
            for loopn in range(1,len(tp_bediener1.permissions)  + 1) :
                perm[loopn - 1] = to_int(substring(tp_bediener1.permissions, loopn - 1, 1))

            if perm[18] < 2:
                zugriff = False

            if zugriff == False:
                not_access1 = True

                return
        else:

            tp_bediener1 = query(tp_bediener1_list, first=True)
            for loopn in range(1,len(tp_bediener1.permissions)  + 1) :
                perm[loopn - 1] = to_int(substring(tp_bediener1.permissions, loopn - 1, 1))

            if perm[19] < 2:
                zugriff = False

            if zugriff == False:
                not_access1 = True

                return

        if zugriff:

            for submenu_list in query(submenu_list_list):
                t_submenu_list = T_submenu_list()
                t_submenu_list_list.append(t_submenu_list)

                buffer_copy(submenu_list, t_submenu_list)

            t_h_bill = query(t_h_bill_list, first=True)

            if not t_h_bill:
                rec_id = 0
            else:
                rec_id = t_h_bill.rec_id

            if not t_h_artikel:
                rec_id_artikel = 0
                service_code = 0
            else:
                rec_id_artikel = t_h_artikel.rec_id
                service_code = t_h_artikel.service_code
            bill_date, cancel_flag, fl_code2, mwst, mwst_foreign, rechnr, balance, bcol, balance_foreign, fl_code3, fl_code4, fl_code5, p_88, closed, t_h_bill_list, kellner1_list = get_output(ts_restinv_update_bill_1bl(pvilanguage, rec_id, rec_id_artikel, deptname, transdate, h_artart, cancel_order, service_code, amount, amount_foreign, price, double_currency, qty, exchg_rate, price_decimal, order_taker, tischnr, curr_dept, curr_waiter, gname, pax, kreditlimit, add_zeit, billart, description, change_str, cc_comment, cancel_str, req_str, voucher_str, hoga_card, print_to_kitchen, from_acct, h_artnrfront, pay_type, guestnr, transfer_zinr, curedept_flag, foreign_rate, curr_room, user_init, hoga_resnr, hoga_reslinnr, incl_vat, get_price, mc_str, t_submenu_list))

            if fl_code2 == 1:

                return

            if case_type == 1:

                if fl_code2 == 2:
                    avail_bill = True

                    return

    t_menu_list_list.clear()
    bmenu_list.clear()

    if cancel_reason == None:
        cancel_reason = ""

    if change_str == None:
        change_str = ""

    if cc_comment == None:
        cc_comment = ""

    if hoga_card == None:
        hoga_card = ""

    if transfer_zinr == None:
        transfer_zinr = ""

    if curr_room == None:
        curr_room = ""

    if mc_str == None:
        mc_str = ""

    if gname == None:
        gname = ""

    for menu_list in query(menu_list_list, filters=(lambda menu_list :menu_list.nr > 0)):
        t_menu_list = T_menu_list()
        t_menu_list_list.append(t_menu_list)

        buffer_copy(menu_list, t_menu_list)
        bmenu = Bmenu()
        bmenu_list.append(bmenu)

        buffer_copy(menu_list, bmenu)
        bmenu.rec_menu = menu_list._recid

    bediener = db_session.query(Bediener).filter(
            (func.lower(Bediener.userinit) == (user_init).lower())).first()

    if bediener:
        tp_bediener1 = Tp_bediener1()
        tp_bediener1_list.append(tp_bediener1)

        buffer_copy(bediener, tp_bediener1)

    for menu_list in query(menu_list_list, filters=(lambda menu_list :menu_list.nr > 0)):
        curr_zeit = get_current_time_in_seconds()
        add_zeit = add_zeit + 1
        menurecid = menu_list._recid
        billart = menu_list.artnr
        req_str = menu_list.REQUEST
        request_str = menu_list.REQUEST

        if num_entries(menu_list.voucher, ";") > 1:
            voucher_str = entry(0, menu_list.voucher, ";")
            incl_vat = logical(entry(1, menu_list.voucher, ";"))
        description, qty, price, cancel_str, amount_foreign, amount, fl_code, fl_code1, t_h_artikel_list = get_output(ts_restinv_run_help3bl(menu_list.artnr, menu_list.bezeich, menu_list.anzahl, menu_list.price, curr_dept, cancel_reason, double_currency, exchg_rate, price_decimal, transdate, cancel_flag, foreign_rate))

        if fl_code1 == 1:

            tp_bediener1 = query(tp_bediener1_list, first=True)
            for loopn in range(1,len(tp_bediener1.permissions)  + 1) :
                perm[loopn - 1] = to_int(substring(tp_bediener1.permissions, loopn - 1, 1))

            if perm[51] < 2:
                zugriff = False

            if zugriff == False:
                not_access = True

                return generate_output()

        t_h_artikel = query(t_h_artikel_list, first=True)
        krecid = menu_list.krecid
        menu_list_list.remove(menu_list)

        if price != 0 and amount == 0:
            1
        else:
            update_bill(t_h_artikel.artart, t_h_artikel.artnrfront)

            bmenu = query(bmenu_list, filters=(lambda bmenu :bmenu.rec_menu == menurecid), first=True)

            if bmenu:
                bmenu_list.remove(bmenu)
        add_zeit = 0
        menurecid = 0

    return generate_output()