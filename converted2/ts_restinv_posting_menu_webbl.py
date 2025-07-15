#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from functions.ts_restinv_run_help3bl import ts_restinv_run_help3bl
from sqlalchemy import func
from functions.ts_restinv_update_bill_cldbl import ts_restinv_update_bill_cldbl
from models import H_artikel, H_bill, Kellner, Bediener, Queasy, Wgrpdep

tp_bediener_data, Tp_bediener = create_model_like(Bediener)
submenu_list_data, Submenu_list = create_model("Submenu_list", {"menurecid":int, "zeit":int, "nr":int, "artnr":int, "bezeich":string, "anzahl":int, "zknr":int, "request":string})
menu_list_data, Menu_list = create_model("Menu_list", {"request":string, "krecid":int, "posted":bool, "nr":int, "artnr":int, "bezeich":string, "anzahl":int, "price":Decimal, "betrag":Decimal, "voucher":string}, {"anzahl": 1, "voucher": ""})
t_h_bill_data, T_h_bill = create_model_like(H_bill, {"rec_id":int})

def ts_restinv_posting_menu_webbl(case_type:int, pvilanguage:int, tischnr:int, curr_dept:int, cancel_reason:string, double_currency:bool, exchg_rate:Decimal, price_decimal:int, transdate:date, foreign_rate:bool, deptname:string, cancel_order:bool, order_taker:int, curr_waiter:int, gname:string, pax:int, kreditlimit:Decimal, change_str:string, cc_comment:string, hoga_card:string, print_to_kitchen:bool, from_acct:bool, pay_type:int, guestnr:int, transfer_zinr:string, curedept_flag:bool, curr_room:string, user_init:string, hoga_resnr:int, hoga_reslinnr:int, incl_vat:bool, get_price:int, mc_str:string, segment_code:int, tp_bediener_data:[Tp_bediener], submenu_list_data:[Submenu_list], cancel_flag:bool, menu_list_data:[Menu_list], t_h_bill_data:[T_h_bill]):
    avail_bill = False
    not_access = False
    not_access1 = False
    bill_date = None
    mwst = to_decimal("0.0")
    mwst_foreign = to_decimal("0.0")
    rechnr = 0
    balance = to_decimal("0.0")
    bcol = 0
    balance_foreign = to_decimal("0.0")
    fl_code = 0
    fl_code1 = 0
    fl_code2 = 0
    fl_code3 = 0
    fl_code4 = 0
    fl_code5 = 0
    p_88 = False
    closed = False
    amount = to_decimal("0.0")
    kellner1_data = []
    t_h_artikel_data = []
    menurecid:int = 0
    add_zeit:int = 0
    billart:int = 0
    req_str:string = ""
    voucher_str:string = ""
    request_str:string = ""
    perm:List[int] = create_empty_list(120,0)
    zugriff:bool = True
    loopn:int = 0
    description:string = ""
    qty:int = 0
    price:Decimal = to_decimal("0.0")
    cancel_str:string = ""
    amount_foreign:Decimal = to_decimal("0.0")
    curr_zeit:int = 0
    krecid:int = 0
    hbill_recid:int = 0
    long_time:int = 0
    first_flag:bool = False
    menulist_nr:int = 0
    menulist_artno:int = 0
    menulist_bez:string = ""
    h_artikel = h_bill = kellner = bediener = queasy = wgrpdep = None

    t_menu_list = menu_list = submenu_list = bmenu = t_h_artikel = t_h_bill = kellner1 = t_h_bill_tmp = t_submenu_list = tp_bediener = tp_bediener1 = None

    t_menu_list_data, T_menu_list = create_model("T_menu_list", {"request":string, "krecid":int, "posted":bool, "nr":int, "artnr":int, "bezeich":string, "anzahl":int, "price":Decimal, "betrag":Decimal, "voucher":string}, {"anzahl": 1, "voucher": ""})
    bmenu_data, Bmenu = create_model("Bmenu", {"request":string, "krecid":int, "posted":bool, "nr":int, "artnr":int, "bezeich":string, "anzahl":int, "price":Decimal, "betrag":Decimal, "voucher":string, "rec_menu":int}, {"anzahl": 1, "voucher": ""})
    t_h_artikel_data, T_h_artikel = create_model_like(H_artikel, {"rec_id":int})
    kellner1_data, Kellner1 = create_model_like(Kellner)
    t_h_bill_tmp_data, T_h_bill_tmp = create_model_like(H_bill, {"rec_id":int})
    t_submenu_list_data, T_submenu_list = create_model("T_submenu_list", {"menurecid":int, "zeit":int, "nr":int, "artnr":int, "bezeich":string, "anzahl":int, "zknr":int, "request":string})
    tp_bediener1_data, Tp_bediener1 = create_model_like(Bediener)

    db_session = local_storage.db_session

    def generate_output():
        nonlocal avail_bill, not_access, not_access1, bill_date, mwst, mwst_foreign, rechnr, balance, bcol, balance_foreign, fl_code, fl_code1, fl_code2, fl_code3, fl_code4, fl_code5, p_88, closed, amount, kellner1_data, t_h_artikel_data, menurecid, add_zeit, billart, req_str, voucher_str, request_str, perm, zugriff, loopn, description, qty, price, cancel_str, amount_foreign, curr_zeit, krecid, hbill_recid, long_time, first_flag, menulist_nr, menulist_artno, menulist_bez, h_artikel, h_bill, kellner, bediener, queasy, wgrpdep
        nonlocal case_type, pvilanguage, tischnr, curr_dept, cancel_reason, double_currency, exchg_rate, price_decimal, transdate, foreign_rate, deptname, cancel_order, order_taker, curr_waiter, gname, pax, kreditlimit, change_str, cc_comment, hoga_card, print_to_kitchen, from_acct, pay_type, guestnr, transfer_zinr, curedept_flag, curr_room, user_init, hoga_resnr, hoga_reslinnr, incl_vat, get_price, mc_str, segment_code, cancel_flag


        nonlocal t_menu_list, menu_list, submenu_list, bmenu, t_h_artikel, t_h_bill, kellner1, t_h_bill_tmp, t_submenu_list, tp_bediener, tp_bediener1
        nonlocal t_menu_list_data, bmenu_data, t_h_artikel_data, kellner1_data, t_h_bill_tmp_data, t_submenu_list_data, tp_bediener1_data

        return {"cancel_flag": cancel_flag, "menu-list": menu_list_data, "t-h-bill": t_h_bill_data, "avail_bill": avail_bill, "not_access": not_access, "not_access1": not_access1, "bill_date": bill_date, "mwst": mwst, "mwst_foreign": mwst_foreign, "rechnr": rechnr, "balance": balance, "bcol": bcol, "balance_foreign": balance_foreign, "fl_code": fl_code, "fl_code1": fl_code1, "fl_code2": fl_code2, "fl_code3": fl_code3, "fl_code4": fl_code4, "fl_code5": fl_code5, "p_88": p_88, "closed": closed, "amount": amount, "kellner1": kellner1_data, "t-h-artikel": t_h_artikel_data}

    def update_bill(h_artart:int, h_artnrfront:int):

        nonlocal avail_bill, not_access, not_access1, bill_date, mwst, mwst_foreign, rechnr, balance, bcol, balance_foreign, fl_code, fl_code1, fl_code2, fl_code3, fl_code4, fl_code5, p_88, amount, kellner1_data, t_h_artikel_data, menurecid, add_zeit, billart, req_str, voucher_str, request_str, perm, zugriff, loopn, description, qty, price, cancel_str, amount_foreign, curr_zeit, krecid, hbill_recid, long_time, first_flag, menulist_nr, menulist_artno, menulist_bez, h_artikel, h_bill, kellner, bediener, queasy, wgrpdep
        nonlocal case_type, pvilanguage, tischnr, curr_dept, cancel_reason, double_currency, exchg_rate, price_decimal, transdate, foreign_rate, deptname, cancel_order, order_taker, curr_waiter, gname, pax, kreditlimit, change_str, cc_comment, hoga_card, print_to_kitchen, from_acct, pay_type, guestnr, transfer_zinr, curedept_flag, curr_room, user_init, hoga_resnr, hoga_reslinnr, incl_vat, get_price, mc_str, segment_code, cancel_flag


        nonlocal t_menu_list, menu_list, submenu_list, bmenu, t_h_artikel, t_h_bill, kellner1, t_h_bill_tmp, t_submenu_list, tp_bediener, tp_bediener1
        nonlocal t_menu_list_data, bmenu_data, t_h_artikel_data, kellner1_data, t_h_bill_tmp_data, t_submenu_list_data, tp_bediener1_data

        do_itprint:bool = False
        by_txtprint:bool = False
        closed:bool = False
        rec_id:int = 0
        tmp_recid:int = 0
        rec_id_artikel:int = 0
        service_code:int = 0

        if h_artart == 0:

            tp_bediener1 = query(tp_bediener1_data, first=True)
            for loopn in range(1,length(tp_bediener1.permissions)  + 1) :
                perm[loopn - 1] = to_int(substring(tp_bediener1.permissions, loopn - 1, 1))

            if perm[18] < 2:
                zugriff = False

            if zugriff == False:
                not_access1 = True

                return
        else:

            tp_bediener1 = query(tp_bediener1_data, first=True)
            for loopn in range(1,length(tp_bediener1.permissions)  + 1) :
                perm[loopn - 1] = to_int(substring(tp_bediener1.permissions, loopn - 1, 1))

            if perm[19] < 2:
                zugriff = False

            if zugriff == False:
                not_access1 = True

                return

        if zugriff:

            for submenu_list in query(submenu_list_data):
                t_submenu_list = T_submenu_list()
                t_submenu_list_data.append(t_submenu_list)

                buffer_copy(submenu_list, t_submenu_list)

            t_h_bill_tmp = query(t_h_bill_tmp_data, first=True)

            if not t_h_bill_tmp:
                rec_id = 0
            else:
                rec_id = t_h_bill_tmp.rec_id

            if not t_h_artikel:
                rec_id_artikel = 0
                service_code = 0
            else:
                rec_id_artikel = t_h_artikel.rec_id
                service_code = t_h_artikel.service_code
            bill_date, cancel_flag, fl_code2, mwst, mwst_foreign, rechnr, balance, bcol, balance_foreign, fl_code3, fl_code4, fl_code5, p_88, closed, t_h_bill_tmp_data, kellner1_data = get_output(ts_restinv_update_bill_cldbl(pvilanguage, rec_id, rec_id_artikel, deptname, transdate, h_artart, cancel_order, service_code, amount, amount_foreign, price, double_currency, qty, exchg_rate, price_decimal, order_taker, tischnr, curr_dept, curr_waiter, gname, pax, kreditlimit, add_zeit, billart, description, change_str, cc_comment, cancel_str, req_str, voucher_str, hoga_card, print_to_kitchen, from_acct, h_artnrfront, pay_type, guestnr, transfer_zinr, curedept_flag, foreign_rate, curr_room, user_init, hoga_resnr, hoga_reslinnr, incl_vat, get_price, mc_str, segment_code, t_submenu_list_data))

            t_h_bill_tmp = query(t_h_bill_tmp_data, first=True)

            if t_h_bill_tmp:
                tmp_recid = t_h_bill_tmp.rec_id
            else:
                tmp_recid = 0

            if fl_code2 == 1:

                return

            if case_type == 1:

                if fl_code2 == 2:
                    avail_bill = True

                    return

            if rec_id == 0 and not closed:

                t_h_bill_tmp = query(t_h_bill_tmp_data, first=True)

                if t_h_bill_tmp:

                    queasy = get_cache (Queasy, {"key": [(eq, 31)],"number1": [(eq, curr_dept)],"number2": [(eq, tischnr)]})

                    if queasy:
                        queasy.number3 = get_current_time_in_seconds()
                        queasy.date1 = get_current_date()


                        pass
                        pass

    long_time = get_current_time_in_seconds()

    t_h_bill = query(t_h_bill_data, first=True)

    if not t_h_bill:
        hbill_recid = 0
    else:
        hbill_recid = t_h_bill.rec_id

    if hbill_recid == 0:

        queasy = get_cache (Queasy, {"key": [(eq, 351)],"number1": [(eq, curr_dept)],"number2": [(eq, tischnr)]})

        if queasy:
            fl_code2 = 2
            avail_bill = True


            pass

            return generate_output()
        else:
            queasy = Queasy()
            db_session.add(queasy)

            queasy.key = 351
            queasy.number1 = curr_dept
            queasy.number2 = tischnr


            pass
            first_flag = True
    else:
        first_flag = True

    if first_flag:

        for t_h_bill in query(t_h_bill_data):
            t_h_bill_tmp = T_h_bill_tmp()
            t_h_bill_tmp_data.append(t_h_bill_tmp)

            buffer_copy(t_h_bill, t_h_bill_tmp)
        t_menu_list_data.clear()
        bmenu_data.clear()

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

        for menu_list in query(menu_list_data, filters=(lambda menu_list: menu_list.nr > 0), sort_by=[("nr",False)]):
            t_menu_list = T_menu_list()
            t_menu_list_data.append(t_menu_list)

            buffer_copy(menu_list, t_menu_list)
            bmenu = Bmenu()
            bmenu_data.append(bmenu)

            buffer_copy(menu_list, bmenu)

        bediener = get_cache (Bediener, {"userinit": [(eq, user_init)]})

        if bediener:
            tp_bediener1 = Tp_bediener1()
            tp_bediener1_data.append(tp_bediener1)

            buffer_copy(bediener, tp_bediener1)

        for menu_list in query(menu_list_data, filters=(lambda menu_list: menu_list.nr > 0), sort_by=[("nr",False)]):
            menulist_nr = menu_list.nr
            menulist_artno = menu_list.artnr
            menulist_bez = menu_list.bezeich


            curr_zeit = get_current_time_in_seconds()
            add_zeit = add_zeit + 1
            billart = menu_list.artnr
            req_str = menu_list.request
            request_str = menu_list.request

            if num_entries(menu_list.voucher, ";") > 1:
                voucher_str = entry(0, menu_list.voucher, ";")
                incl_vat = logical(entry(1, menu_list.voucher, ";"))
            description, qty, price, cancel_str, amount_foreign, amount, fl_code, fl_code1, t_h_artikel_data = get_output(ts_restinv_run_help3bl(menu_list.artnr, menu_list.bezeich, menu_list.anzahl, menu_list.price, curr_dept, cancel_reason, double_currency, exchg_rate, price_decimal, transdate, cancel_flag, foreign_rate))

            t_h_artikel = query(t_h_artikel_data, first=True)

            if fl_code1 == 1:

                tp_bediener1 = query(tp_bediener1_data, first=True)
                for loopn in range(1,length(tp_bediener1.permissions)  + 1) :
                    perm[loopn - 1] = to_int(substring(tp_bediener1.permissions, loopn - 1, 1))

                if perm[51] < 2:
                    zugriff = False

                if not zugriff and amount < 0 and t_h_artikel.artart == 0:

                    wgrpdep = db_session.query(Wgrpdep).filter(
                             (Wgrpdep.zknr == t_h_artikel.zwkum) & (Wgrpdep.departement == t_h_artikel.departement) & (matches(Wgrpdep.bezeich,"*DISCOUNT*"))).first()

                    if wgrpdep:

                        if perm[78] < 2:
                            zugriff = False
                        else:
                            zugriff = True

                if zugriff == False:
                    not_access = True

                    return generate_output()
            krecid = menu_list.krecid
            menu_list_data.remove(menu_list)

            if price != 0 and amount == 0:
                pass
            else:
                update_bill(t_h_artikel.artart, t_h_artikel.artnrfront)

                bmenu = query(bmenu_data, filters=(lambda bmenu: bmenu.rec_menu == menurecid), first=True)

                if bmenu:
                    bmenu_data.remove(bmenu)
            add_zeit = 0
        t_h_bill_data.clear()

        for t_h_bill_tmp in query(t_h_bill_tmp_data):
            t_h_bill = T_h_bill()
            t_h_bill_data.append(t_h_bill)

            buffer_copy(t_h_bill_tmp, t_h_bill)

        for queasy in db_session.query(Queasy).filter(
                 (Queasy.key == 351) & (Queasy.number1 == curr_dept) & (Queasy.number2 == tischnr)).order_by(Queasy._recid).all():
            db_session.delete(queasy)
        pass

    return generate_output()