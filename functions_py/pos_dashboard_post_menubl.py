#using conversion tools version: 1.0.0.117

# ========================
# Rulita, 31-10-2025
# - Recompile program
# ========================

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from functions.prepare_ts_restinvbl import prepare_ts_restinvbl
from functions.ts_hbline_get_pricebl import ts_hbline_get_pricebl
from sqlalchemy import func
from functions.selforder_update_bill_1bl import selforder_update_bill_1bl
from functions.ts_restinv_add_kds_cldbl import ts_restinv_add_kds_cldbl
from functions.add_kitchprbl import add_kitchprbl
from models import H_artikel, H_bill, Kellner, Queasy, H_bill_line, Tisch, Res_line, Htparam

menu_list_data, Menu_list = create_model("Menu_list", {"rec_id":int, "description":string, "qty":int, "price":Decimal, "special_request":string})

def pos_dashboard_post_menubl(language_code:int, rec_id:int, tischnr:int, curr_dept:int, user_init:string, gname:string, pax:int, guestnr:int, curr_room:string, resnr:int, reslinnr:int, session_param:string, order_no:int, menu_list_data:[Menu_list]):

    prepare_cache ([H_artikel, H_bill, Queasy, H_bill_line, Tisch, Res_line])

    rechnr = 0
    mess_str = ""
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
    price_decimal:int = 0
    curr_local:string = ""
    curr_foreign:string = ""
    double_currency:bool = False
    foreign_rate:bool = False
    exchg_rate:Decimal = 1
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
    bill_date:date = None
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
    table_str:string = ""
    curr_table:int = 0
    room_serviceflag:bool = False
    post_mess_result:string = ""
    get_time:string = ""
    record_id:int = 0
    active_flag:int = 1
    h_artikel = h_bill = kellner = queasy = h_bill_line = tisch = res_line = htparam = None

    hbill = t_kellner = t_h_artikel = menu_list = t_h_bill = t_submenu_list = kellner1 = kds_menu_list = sosqsy = bqsy = ordebill_line = None

    hbill_data, Hbill = create_model("Hbill", {"kellner_nr":int})
    t_kellner_data, T_kellner = create_model("T_kellner", {"kellner_nr":int})
    t_h_artikel_data, T_h_artikel = create_model_like(H_artikel, {"rec_id":int})
    t_h_bill_data, T_h_bill = create_model_like(H_bill, {"rec_id":int})
    t_submenu_list_data, T_submenu_list = create_model("T_submenu_list", {"menurecid":int, "zeit":int, "nr":int, "artnr":int, "bezeich":string, "anzahl":int, "zknr":int, "request":string})
    kellner1_data, Kellner1 = create_model_like(Kellner)
    kds_menu_list_data, Kds_menu_list = create_model("Kds_menu_list", {"request":string, "krecid":int, "posted":bool, "nr":int, "artnr":int, "bezeich":string, "anzahl":int, "price":Decimal, "betrag":Decimal, "voucher":string}, {"voucher": ""})

    Sosqsy = create_buffer("Sosqsy",Queasy)
    Bqsy = create_buffer("Bqsy",Queasy)
    Ordebill_line = create_buffer("Ordebill_line",Queasy)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal rechnr, mess_str, amount, mealcoupon_cntrl, must_print, zero_flag, multi_cash, cancel_exist, msg_str, disc_art1, disc_art2, disc_art3, mi_ordertaker, price_decimal, curr_local, curr_foreign, double_currency, foreign_rate, exchg_rate, b_title, deptname, p_223, curr_waiter, fl_code, pos1, pos2, cashless_flag, price, add_zeit, bill_date, cancel_flag, mwst, mwst_foreign, balance, bcol, balance_foreign, fl_code1, fl_code2, fl_code3, p_88, closed, error_str, usr, outlet, err, err1, fract, table_str, curr_table, room_serviceflag, post_mess_result, get_time, record_id, active_flag, h_artikel, h_bill, kellner, queasy, h_bill_line, tisch, res_line, htparam
        nonlocal language_code, rec_id, tischnr, curr_dept, user_init, gname, pax, guestnr, curr_room, resnr, reslinnr, session_param, order_no
        nonlocal sosqsy, bqsy, ordebill_line


        nonlocal hbill, t_kellner, t_h_artikel, menu_list, t_h_bill, t_submenu_list, kellner1, kds_menu_list, sosqsy, bqsy, ordebill_line
        nonlocal hbill_data, t_kellner_data, t_h_artikel_data, t_h_bill_data, t_submenu_list_data, kellner1_data, kds_menu_list_data

        return {"rechnr": rechnr, "mess_str": mess_str}


    if gname == None:
        gname = ""

    if curr_room == None:
        curr_room = ""
    table_str = to_string(tischnr, "99999")
    curr_table = tischnr
    mealcoupon_cntrl, must_print, zero_flag, multi_cash, cancel_exist, msg_str, disc_art1, disc_art2, disc_art3, mi_ordertaker, price_decimal, curr_local, curr_foreign, double_currency, foreign_rate, exchg_rate, b_title, deptname, p_223, curr_waiter, fl_code, pos1, pos2, cashless_flag, hbill_data, t_kellner_data = get_output(prepare_ts_restinvbl(language_code, curr_dept, 0, user_init, None))

    t_kellner = query(t_kellner_data, first=True)

    for sosqsy in db_session.query(Sosqsy).filter(
             (Sosqsy.key == 222) & (Sosqsy.number1 == 1) & (Sosqsy.betriebsnr == curr_dept)).order_by(Sosqsy._recid).all():

        if sosqsy.number2 == 21:
            room_serviceflag = sosqsy.logi1

    if rec_id != 0:

        h_bill = get_cache (H_bill, {"_recid": [(eq, rec_id)],"flag": [(eq, 1)]})

        if h_bill:
            rec_id = 0

    h_bill = get_cache (H_bill, {"tischnr": [(eq, tischnr)],"departement": [(eq, curr_dept)],"flag": [(eq, 0)],"saldo": [(ne, 0)]})

    if h_bill:

        h_bill_line = get_cache (H_bill_line, {"rechnr": [(eq, h_bill.rechnr)],"departement": [(eq, h_bill.departement)]})

        if h_bill_line:
            rec_id = h_bill._recid

    if curr_dept == 1:

        for menu_list in query(menu_list_data):
            add_zeit = add_zeit + 1

            h_artikel = get_cache (H_artikel, {"departement": [(eq, curr_dept)],"artnr": [(eq, menu_list.rec_id)]})

            if h_artikel.epreis1 != 0:
                err, err1, price, fract = get_output(ts_hbline_get_pricebl(h_artikel.artnr, curr_dept))
            else:
                price =  to_decimal(menu_list.price)
            amount =  to_decimal(price) * to_decimal(menu_list.qty)

            if room_serviceflag:

                if length(table_str) == 5:

                    tisch = db_session.query(Tisch).filter(
                             (Tisch.departement == curr_dept) & (matches(Tisch.bezeich,("*" + to_string(curr_table) + "*")))).first()

                    if tisch:
                        curr_table = tisch.tischnr
            bill_date, cancel_flag, fl_code, mwst, mwst_foreign, rechnr, balance, bcol, balance_foreign, fl_code1, fl_code2, fl_code3, p_88, closed, t_h_bill_data, kellner1_data = get_output(selforder_update_bill_1bl(language_code, rec_id, h_artikel._recid, "", None, h_artikel.artart, False, h_artikel.service_code, amount, 0, price, double_currency, menu_list.qty, exchg_rate, price_decimal, user_init, curr_table, curr_dept, user_init, gname, pax, 0, add_zeit, h_artikel.artnr, menu_list.description, "", "", "", menu_list.special_request, "", "", True, False, h_artikel.artnrfront, 0, guestnr, "", False, foreign_rate, curr_room, user_init, resnr, reslinnr, t_submenu_list_data))

            if fl_code == 1:
                mess_str = "Transaction not allowed: Posted item(s) with differrent billing date found."

                return generate_output()

            t_h_bill = query(t_h_bill_data, first=True)

            if t_h_bill:
                rechnr = t_h_bill.rechnr
                rec_id = t_h_bill.rec_id

            if rechnr != 0:

                bqsy = get_cache (Queasy, {"key": [(eq, 225)],"number1": [(eq, curr_dept)],"char1": [(eq, "orderbill")],"logi1": [(eq, True)],"char3": [(eq, session_param)]})

                if bqsy:

                    queasy = db_session.query(Queasy).filter(
                             (Queasy.key == 225) & (Queasy.char1 == ("orderbill-line").lower()) & (entry(3, Queasy.char2, "|") == (session_param).lower()) & (Queasy.number2 == tischnr) & (Queasy.number1 == order_no) & (Queasy.date1 == bqsy.date1) & (to_int(entry(1, Queasy.char3, "|")) == menu_list.rec_id) & (num_entries(Queasy.char3, "|") <= 7)).first()

                    if queasy:
                        queasy.logi2 = True
                        queasy.logi3 = True

                        for h_bill_line in db_session.query(H_bill_line).filter(
                                 (H_bill_line.departement == curr_dept) & (H_bill_line.rechnr == rechnr) & (H_bill_line.artnr == to_int(entry(1, queasy.char3, "|")))).order_by(H_bill_line.zeit.desc()).all():

                            ordebill_line = db_session.query(Ordebill_line).filter(
                                     (Ordebill_line.key == 225) & (Ordebill_line.char1 == ("orderbill-line").lower()) & (entry(3, Ordebill_line.char2, "|") == (session_param).lower()) & (Ordebill_line.number2 == tischnr) & (Ordebill_line.number1 == order_no) & (Ordebill_line.date1 == bqsy.date1) & (to_int(entry(1, Ordebill_line.char3, "|")) == h_bill_line.artnr) & (num_entries(Ordebill_line.char3, "|") >= 8)).first()

                            if ordebill_line:
                                get_time = entry(7, ordebill_line.char3, "|")

                                if to_int(get_time) == h_bill_line.zeit:
                                    pass
                                else:
                                    queasy.char3 = queasy.char3 + "|" + to_string(h_bill_line._recid) + "|" + to_string(h_bill_line.zeit)
                            else:
                                queasy.char3 = queasy.char3 + "|" + to_string(h_bill_line._recid) + "|" + to_string(h_bill_line.zeit)
                            break

                if not closed:
                    kds_menu_list = Kds_menu_list()
                    kds_menu_list_data.append(kds_menu_list)

                    kds_menu_list.request = menu_list.special_request
                    kds_menu_list.krecid = 0
                    kds_menu_list.posted = True
                    kds_menu_list.nr = add_zeit
                    kds_menu_list.artnr = menu_list.rec_id
                    kds_menu_list.bezeich = menu_list.description
                    kds_menu_list.anzahl = menu_list.qty
                    kds_menu_list.price =  to_decimal(price)
                    kds_menu_list.betrag =  to_decimal(amount)
                    kds_menu_list.voucher = ""


    else:

        res_line = db_session.query(Res_line).filter(
                 (Res_line.active_flag == active_flag) & (Res_line.l_zuordnung[inc_value(2)] == 0) & ((Res_line.resstatus == 6) | (Res_line.resstatus == 13)) & (Res_line.gastnrmember == guestnr)).first()

        if res_line:

            h_bill = get_cache (H_bill, {"departement": [(eq, curr_dept)],"flag": [(eq, 0)],"resnr": [(eq, res_line.resnr)]})

            if h_bill:
                record_id = h_bill._recid
            else:
                record_id = 0

        for menu_list in query(menu_list_data):
            add_zeit = add_zeit + 1

            h_artikel = get_cache (H_artikel, {"departement": [(eq, curr_dept)],"artnr": [(eq, menu_list.rec_id)]})

            if record_id == 0:

                t_h_bill = query(t_h_bill_data, first=True)

                if t_h_bill:
                    record_id = t_h_bill.rec_id

            if h_artikel.epreis1 != 0:
                err, err1, price, fract = get_output(ts_hbline_get_pricebl(h_artikel.artnr, curr_dept))
            else:
                price =  to_decimal(menu_list.price)
            amount =  to_decimal(price) * to_decimal(menu_list.qty)

            if room_serviceflag:

                if length(table_str) == 5:

                    tisch = db_session.query(Tisch).filter(
                             (Tisch.departement == curr_dept) & (matches(Tisch.bezeich,("*" + to_string(curr_table) + "*")))).first()

                    if tisch:
                        curr_table = tisch.tischnr
            bill_date, cancel_flag, fl_code, mwst, mwst_foreign, rechnr, balance, bcol, balance_foreign, fl_code1, fl_code2, fl_code3, p_88, closed, t_h_bill_data, kellner1_data = get_output(selforder_update_bill_1bl(language_code, rec_id, h_artikel._recid, "", None, h_artikel.artart, False, h_artikel.service_code, amount, 0, price, double_currency, menu_list.qty, exchg_rate, price_decimal, user_init, curr_table, curr_dept, user_init, gname, pax, 0, add_zeit, h_artikel.artnr, menu_list.description, "", "", "", menu_list.special_request, "", "", True, False, h_artikel.artnrfront, 0, guestnr, "", False, foreign_rate, curr_room, user_init, resnr, reslinnr, t_submenu_list_data))

            if fl_code == 1:
                mess_str = "Transaction not allowed: Posted item(s) with differrent billing date found."

                return generate_output()

            t_h_bill = query(t_h_bill_data, first=True)

            if t_h_bill:
                rechnr = t_h_bill.rechnr
                rec_id = t_h_bill.rec_id

            if rechnr != 0:

                bqsy = get_cache (Queasy, {"key": [(eq, 225)],"number1": [(eq, curr_dept)],"char1": [(eq, "orderbill")],"logi1": [(eq, True)],"char3": [(eq, session_param)]})

                if bqsy:

                    queasy = db_session.query(Queasy).filter(
                             (Queasy.key == 225) & (Queasy.char1 == ("orderbill-line").lower()) & (entry(3, Queasy.char2, "|") == (session_param).lower()) & (Queasy.number2 == tischnr) & (Queasy.number1 == order_no) & (Queasy.date1 == bqsy.date1) & (to_int(entry(1, Queasy.char3, "|")) == menu_list.rec_id) & (num_entries(Queasy.char3, "|") <= 7)).first()

                    if queasy:
                        queasy.logi2 = True
                        queasy.logi3 = True

                        for h_bill_line in db_session.query(H_bill_line).filter(
                                 (H_bill_line.departement == curr_dept) & (H_bill_line.rechnr == rechnr) & (H_bill_line.artnr == to_int(entry(1, queasy.char3, "|")))).order_by(H_bill_line.zeit.desc()).all():

                            ordebill_line = db_session.query(Ordebill_line).filter(
                                     (Ordebill_line.key == 225) & (Ordebill_line.char1 == ("orderbill-line").lower()) & (entry(3, Ordebill_line.char2, "|") == (session_param).lower()) & (Ordebill_line.number2 == tischnr) & (Ordebill_line.number1 == order_no) & (Ordebill_line.date1 == bqsy.date1) & (to_int(entry(1, Ordebill_line.char3, "|")) == h_bill_line.artnr) & (num_entries(Ordebill_line.char3, "|") >= 8)).first()

                            if ordebill_line:
                                get_time = entry(7, ordebill_line.char3, "|")

                                if to_int(get_time) == h_bill_line.zeit:
                                    pass
                                else:
                                    queasy.char3 = queasy.char3 + "|" + to_string(h_bill_line._recid) + "|" + to_string(h_bill_line.zeit)
                            else:
                                queasy.char3 = queasy.char3 + "|" + to_string(h_bill_line._recid) + "|" + to_string(h_bill_line.zeit)
                            break

                if not closed:
                    kds_menu_list = Kds_menu_list()
                    kds_menu_list_data.append(kds_menu_list)

                    kds_menu_list.request = menu_list.special_request
                    kds_menu_list.krecid = 0
                    kds_menu_list.posted = True
                    kds_menu_list.nr = add_zeit
                    kds_menu_list.artnr = menu_list.rec_id
                    kds_menu_list.bezeich = menu_list.description
                    kds_menu_list.anzahl = menu_list.qty
                    kds_menu_list.price =  to_decimal(price)
                    kds_menu_list.betrag =  to_decimal(amount)
                    kds_menu_list.voucher = ""

    if rec_id != 0:

        queasy = get_cache (Queasy, {"key": [(eq, 225)],"number1": [(eq, curr_dept)],"char1": [(eq, "orderbill")],"logi1": [(eq, True)],"number3": [(eq, order_no)],"char3": [(eq, session_param)],"number2": [(eq, curr_table)]})

        if queasy:
            queasy.logi3 = True
            queasy.char2 = queasy.char2 + "|BL=" + to_string(rechnr)
            queasy.betriebsnr = rec_id

        queasy = get_cache (Queasy, {"key": [(eq, 223)],"number1": [(eq, curr_dept)],"char3": [(eq, session_param)],"betriebsnr": [(eq, 0)]})

        if queasy:
            queasy.betriebsnr = rechnr


        pass
    mess_str = "Order Posted Success"

    if rechnr != 0:

        htparam = get_cache (Htparam, {"paramnr": [(eq, 280)]})

        if htparam and htparam.flogical :
            post_mess_result = get_output(ts_restinv_add_kds_cldbl(kds_menu_list_data, tischnr, curr_dept, user_init, rechnr, user_init))

            if post_mess_result.lower()  != ("Post KDS Success!").lower() :
                mess_str = post_mess_result
        error_str = get_output(add_kitchprbl(language_code, "", curr_dept, rechnr, bill_date, user_init))

    return generate_output()