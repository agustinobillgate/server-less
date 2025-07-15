from functions.additional_functions import *
import decimal
from datetime import date
from functions.prepare_ts_restinvbl import prepare_ts_restinvbl
from functions.ts_hbline_get_pricebl import ts_hbline_get_pricebl
from functions.selforder_update_bill_1bl import selforder_update_bill_1bl
from sqlalchemy import func
from functions.add_kitchprbl import add_kitchprbl
from models import H_artikel, H_bill, Kellner, Queasy, Tisch, H_bill_line, Res_line

def pos_dashboard_post_menubl(language_code:int, rec_id:int, tischnr:int, curr_dept:int, user_init:str, gname:str, pax:int, guestnr:int, curr_room:str, resnr:int, reslinnr:int, session_param:str, order_no:int, menu_list:[Menu_list]):
    rechnr = 0
    mess_str = ""
    amount:decimal = 0
    mealcoupon_cntrl:bool = False
    must_print:bool = False
    zero_flag:bool = False
    multi_cash:bool = False
    cancel_exist:bool = False
    msg_str:str = ""
    disc_art1:int = 0
    disc_art2:int = 0
    disc_art3:int = 0
    mi_ordertaker:bool = True
    price_decimal:int = 0
    curr_local:str = ""
    curr_foreign:str = ""
    double_currency:bool = False
    foreign_rate:bool = False
    exchg_rate:decimal = 1
    b_title:str = ""
    deptname:str = ""
    p_223:bool = False
    curr_waiter:int = 0
    fl_code:int = 0
    pos1:int = 0
    pos2:int = 0
    cashless_flag:bool = False
    price:decimal = 0
    add_zeit:int = 0
    bill_date:date = None
    cancel_flag:bool = False
    mwst:decimal = 0
    mwst_foreign:decimal = 0
    balance:decimal = 0
    bcol:int = 0
    balance_foreign:decimal = 0
    fl_code1:int = 0
    fl_code2:int = 0
    fl_code3:int = 0
    p_88:bool = False
    closed:bool = False
    error_str:str = ""
    usr:str = ""
    outlet:str = ""
    err:bool = False
    err1:bool = False
    fract:decimal = 1
    table_str:str = ""
    curr_table:int = 0
    room_serviceflag:bool = False
    get_time:str = ""
    record_id:int = 0
    active_flag:int = 1
    h_artikel = h_bill = kellner = queasy = tisch = h_bill_line = res_line = None

    hbill = t_kellner = t_h_artikel = menu_list = t_h_bill = t_submenu_list = kellner1 = sosqsy = bqsy = ordebill_line = None

    hbill_list, Hbill = create_model("Hbill", {"kellner_nr":int})
    t_kellner_list, T_kellner = create_model("T_kellner", {"kellner_nr":int})
    t_h_artikel_list, T_h_artikel = create_model_like(H_artikel, {"rec_id":int})
    menu_list_list, Menu_list = create_model("Menu_list", {"rec_id":int, "description":str, "qty":int, "price":decimal, "special_request":str})
    t_h_bill_list, T_h_bill = create_model_like(H_bill, {"rec_id":int})
    t_submenu_list_list, T_submenu_list = create_model("T_submenu_list", {"menurecid":int, "zeit":int, "nr":int, "artnr":int, "bezeich":str, "anzahl":int, "zknr":int, "request":str})
    kellner1_list, Kellner1 = create_model_like(Kellner)

    Sosqsy = Queasy
    Bqsy = Queasy
    Ordebill_line = Queasy

    db_session = local_storage.db_session

    def generate_output():
        nonlocal rechnr, mess_str, amount, mealcoupon_cntrl, must_print, zero_flag, multi_cash, cancel_exist, msg_str, disc_art1, disc_art2, disc_art3, mi_ordertaker, price_decimal, curr_local, curr_foreign, double_currency, foreign_rate, exchg_rate, b_title, deptname, p_223, curr_waiter, fl_code, pos1, pos2, cashless_flag, price, add_zeit, bill_date, cancel_flag, mwst, mwst_foreign, balance, bcol, balance_foreign, fl_code1, fl_code2, fl_code3, p_88, closed, error_str, usr, outlet, err, err1, fract, table_str, curr_table, room_serviceflag, get_time, record_id, active_flag, h_artikel, h_bill, kellner, queasy, tisch, h_bill_line, res_line
        nonlocal sosqsy, bqsy, ordebill_line


        nonlocal hbill, t_kellner, t_h_artikel, menu_list, t_h_bill, t_submenu_list, kellner1, sosqsy, bqsy, ordebill_line
        nonlocal hbill_list, t_kellner_list, t_h_artikel_list, menu_list_list, t_h_bill_list, t_submenu_list_list, kellner1_list
        return {"rechnr": rechnr, "mess_str": mess_str}

    if gname == None:
        gname = ""

    if curr_room == None:
        curr_room = ""
    table_str = to_string(tischnr, "99999")
    curr_table = tischnr
    mealcoupon_cntrl, must_print, zero_flag, multi_cash, cancel_exist, msg_str, disc_art1, disc_art2, disc_art3, mi_ordertaker, price_decimal, curr_local, curr_foreign, double_currency, foreign_rate, exchg_rate, b_title, deptname, p_223, curr_waiter, fl_code, pos1, pos2, cashless_flag, hbill_list, t_kellner_list = get_output(prepare_ts_restinvbl(language_code, curr_dept, 0, user_init, None))

    t_kellner = query(t_kellner_list, first=True)

    for sosqsy in db_session.query(Sosqsy).filter(
            (Sosqsy.key == 222) &  (Sosqsy.number1 == 1) &  (Sosqsy.betriebsnr == curr_dept)).all():

        if sosqsy.number2 == 21:
            room_serviceflag = sosqsy.logi1

    if curr_dept == 1:

        for menu_list in query(menu_list_list):
            add_zeit = add_zeit + 1

            h_artikel = db_session.query(H_artikel).filter(
                    (H_artikel.departement == curr_dept) &  (H_artikel.artnr == menu_list.rec_id)).first()

            if h_artikel.epreis1 != 0:
                err, err1, price, fract = get_output(ts_hbline_get_pricebl(h_artikel.artnr, curr_dept))
            else:
                price = menu_list.price
            amount = price * menu_list.qty

            if room_serviceflag:

                if len(table_str) == 5:

                    tisch = db_session.query(Tisch).filter(
                            (Tisch.departement == curr_dept) &  (Tisch.bezeich.op("~")(".*" + to_string(curr_table) + "*"))).first()

                    if tisch:
                        curr_table = tischnr
            bill_date, cancel_flag, fl_code, mwst, mwst_foreign, rechnr, balance, bcol, balance_foreign, fl_code1, fl_code2, fl_code3, p_88, closed, t_h_bill_list, kellner1_list = get_output(selforder_update_bill_1bl(language_code, rec_id, h_artikel._recid, "", None, h_artikel.artart, False, h_artikel.service_code, amount, 0, price, double_currency, menu_list.qty, exchg_rate, price_decimal, user_init, curr_table, curr_dept, user_init, gname, pax, 0, add_zeit, h_artikel.artnr, menu_list.description, "", "", "", menu_list.special_request, "", "", True, False, h_artikel.artnrfront, 0, guestnr, "", False, foreign_rate, curr_room, user_init, resnr, reslinnr, t_submenu_list))

            if fl_code == 1:
                mess_str = "Transaction not allowed: Posted item(s) with differrent billing date found."

                return generate_output()

            t_h_bill = query(t_h_bill_list, first=True)

            if t_h_bill:
                rechnr = t_h_bill.rechnr
                rec_id = t_h_bill.rec_id

            if rechnr != 0:

                bqsy = db_session.query(Bqsy).filter(
                        (Bqsy.key == 225) &  (Bqsy.number1 == curr_dept) &  (func.lower(Bqsy.char1) == "orderbill") &  (Bqsy.logi1) &  (func.lower(Bqsy.char3) == (session_param).lower())).first()

                if bqsy:

                    queasy = db_session.query(Queasy).filter(
                            (Queasy.key == 225) &  (func.lower(Queasy.char1) == "orderbill_line") &  (entry(3, Queasy.char2, "|Queasy.Queasy.") == (session_param).lower()) &  (Queasy.number2 == tischnr) &  (Queasy.number1 == order_no) &  (Queasy.date1 == bqsy.date1) &  (to_int(entry(1, Queasy.char3, "|Queasy.Queasy.Queasy.")) == menu_list.rec_id) &  (num_entries(Queasy.char3, "|Queasy.Queasy.") <= 7)).first()

                    if queasy:
                        queasy.logi2 = True
                        queasy.logi3 = True

                        for h_bill_line in db_session.query(H_bill_line).filter(
                                (H_bill_line.departement == curr_dept) &  (H_bill_line.rechnr == rechnr) &  (H_bill_line.artnr == to_int(entry(1, queasy.char3, "|")))).all():

                            ordebill_line = db_session.query(Ordebill_line).filter(
                                    (Ordebill_line.key == 225) &  (func.lower(Ordebill_line.char1) == "orderbill_line") &  (entry(3, Ordebill_line.char2, "|Ordebill_line.Ordebill_line.") == (session_param).lower()) &  (Ordebill_line.number2 == tischnr) &  (Ordebill_line.number1 == order_no) &  (Ordebill_line.date1 == bqsy.date1) &  (to_int(entry(1, Ordebill_line.char3, "|Ordebill_line.Ordebill_line.Ordebill_line.")) == h_bill_line.artnr) &  (num_entries(Ordebill_line.char3, "|Ordebill_line.Ordebill_line.") >= 8)).first()

                            if ordebill_line:
                                get_time = entry(7, ordebill_line.char3, "|")

                                if to_int(get_time) == h_bill_line.zeit:
                                    pass
                                else:
                                    queasy.char3 = queasy.char3 + "|" + to_string(h_bill_line._recid) + "|" + to_string(h_bill_line.zeit)
                            else:
                                queasy.char3 = queasy.char3 + "|" + to_string(h_bill_line._recid) + "|" + to_string(h_bill_line.zeit)
                            break
    else:

        res_line = db_session.query(Res_line).filter(
                (Res_line.active_flag == active_flag) &  (Res_line.l_zuordnung[2] == 0) &  ((Res_line.resstatus == 6) |  (Res_line.resstatus == 13)) &  (Res_line.gastnrmember == guestnr)).first()

        if res_line:

            h_bill = db_session.query(H_bill).filter(
                    (H_bill.departement == curr_dept) &  (H_bill.flag == 0) &  (H_bill.resnr == res_line.resnr)).first()

            if h_bill:
                record_id = h_bill._recid
            else:
                record_id = 0

        for menu_list in query(menu_list_list):
            add_zeit = add_zeit + 1

            h_artikel = db_session.query(H_artikel).filter(
                    (H_artikel.departement == curr_dept) &  (H_artikel.artnr == menu_list.rec_id)).first()

            if record_id == 0:

                t_h_bill = query(t_h_bill_list, first=True)

                if t_h_bill:
                    record_id = t_h_bill.rec_id

            if h_artikel.epreis1 != 0:
                err, err1, price, fract = get_output(ts_hbline_get_pricebl(h_artikel.artnr, curr_dept))
            else:
                price = menu_list.price
            amount = price * menu_list.qty

            if room_serviceflag:

                if len(table_str) == 5:

                    tisch = db_session.query(Tisch).filter(
                            (Tisch.departement == curr_dept) &  (Tisch.bezeich.op("~")(".*" + to_string(curr_table) + "*"))).first()

                    if tisch:
                        curr_table = tischnr
            bill_date, cancel_flag, fl_code, mwst, mwst_foreign, rechnr, balance, bcol, balance_foreign, fl_code1, fl_code2, fl_code3, p_88, closed, t_h_bill_list, kellner1_list = get_output(selforder_update_bill_1bl(language_code, rec_id, h_artikel._recid, "", None, h_artikel.artart, False, h_artikel.service_code, amount, 0, price, double_currency, menu_list.qty, exchg_rate, price_decimal, user_init, curr_table, curr_dept, user_init, gname, pax, 0, add_zeit, h_artikel.artnr, menu_list.description, "", "", "", menu_list.special_request, "", "", True, False, h_artikel.artnrfront, 0, guestnr, "", False, foreign_rate, curr_room, user_init, resnr, reslinnr, t_submenu_list))

            if fl_code == 1:
                mess_str = "Transaction not allowed: Posted item(s) with differrent billing date found."

                return generate_output()

            t_h_bill = query(t_h_bill_list, first=True)

            if t_h_bill:
                rechnr = t_h_bill.rechnr
                rec_id = t_h_bill.rec_id

            if rechnr != 0:

                bqsy = db_session.query(Bqsy).filter(
                        (Bqsy.key == 225) &  (Bqsy.number1 == curr_dept) &  (func.lower(Bqsy.char1) == "orderbill") &  (Bqsy.logi1) &  (func.lower(Bqsy.char3) == (session_param).lower())).first()

                if bqsy:

                    queasy = db_session.query(Queasy).filter(
                            (Queasy.key == 225) &  (func.lower(Queasy.char1) == "orderbill_line") &  (entry(3, Queasy.char2, "|Queasy.Queasy.") == (session_param).lower()) &  (Queasy.number2 == tischnr) &  (Queasy.number1 == order_no) &  (Queasy.date1 == bqsy.date1) &  (to_int(entry(1, Queasy.char3, "|Queasy.Queasy.Queasy.")) == menu_list.rec_id) &  (num_entries(Queasy.char3, "|Queasy.Queasy.") <= 7)).first()

                    if queasy:
                        queasy.logi2 = True
                        queasy.logi3 = True

                        for h_bill_line in db_session.query(H_bill_line).filter(
                                (H_bill_line.departement == curr_dept) &  (H_bill_line.rechnr == rechnr) &  (H_bill_line.artnr == to_int(entry(1, queasy.char3, "|")))).all():

                            ordebill_line = db_session.query(Ordebill_line).filter(
                                    (Ordebill_line.key == 225) &  (func.lower(Ordebill_line.char1) == "orderbill_line") &  (entry(3, Ordebill_line.char2, "|Ordebill_line.Ordebill_line.") == (session_param).lower()) &  (Ordebill_line.number2 == tischnr) &  (Ordebill_line.number1 == order_no) &  (Ordebill_line.date1 == bqsy.date1) &  (to_int(entry(1, Ordebill_line.char3, "|Ordebill_line.Ordebill_line.Ordebill_line.")) == h_bill_line.artnr) &  (num_entries(Ordebill_line.char3, "|Ordebill_line.Ordebill_line.") >= 8)).first()

                            if ordebill_line:
                                get_time = entry(7, ordebill_line.char3, "|")

                                if to_int(get_time) == h_bill_line.zeit:
                                    pass
                                else:
                                    queasy.char3 = queasy.char3 + "|" + to_string(h_bill_line._recid) + "|" + to_string(h_bill_line.zeit)
                            else:
                                queasy.char3 = queasy.char3 + "|" + to_string(h_bill_line._recid) + "|" + to_string(h_bill_line.zeit)
                            break

    if rec_id != 0:

        queasy = db_session.query(Queasy).filter(
                (Queasy.key == 225) &  (Queasy.number1 == curr_dept) &  (func.lower(Queasy.char1) == "orderbill") &  (Queasy.logi1) &  (Queasy.number3 == order_no) &  (func.lower(Queasy.char3) == (session_param).lower())).first()

        if queasy:
            queasy.logi3 = True
            queasy.char2 = queasy.char2 + "|BL == " + to_string(rechnr)
            queasy.betriebsnr = rec_id

        queasy = db_session.query(Queasy).filter(
                (Queasy.key == 223) &  (Queasy.number1 == curr_dept) &  (func.lower(Queasy.char3) == (session_param).lower()) &  (Queasy.betriebsnr == 0)).first()

        if queasy:
            queasy.betriebsnr = rechnr


    mess_str = "Order Posted Success"

    if rechnr != 0:
        error_str = get_output(add_kitchprbl(language_code, "", curr_dept, rechnr, bill_date, user_init))

    return generate_output()