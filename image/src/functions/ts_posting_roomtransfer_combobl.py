from functions.additional_functions import *
import decimal
from datetime import date
from functions.read_hotelnamebl import read_hotelnamebl
from functions.ts_rzinr_btn_exitbl import ts_rzinr_btn_exitbl
from functions.prepare_ts_restinv_1bl import prepare_ts_restinv_1bl
from functions.combo_transfer_bill_1bl import combo_transfer_bill_1bl
from functions.ts_restinv_btn_transfer_paytype1bl import ts_restinv_btn_transfer_paytype1bl
from functions.ts_restinv_update_bill_1bl import ts_restinv_update_bill_1bl
from functions.ts_restsale_update_h_billbl import ts_restsale_update_h_billbl
from functions.ts_restinv_del_queasybl import ts_restinv_del_queasybl
from models import H_bill, Kellner, H_artikel

def ts_posting_roomtransfer_combobl(language_code:int, vkey:str, h_recid:int, bill_no:int, tischnr:int, pax:int, curr_dept:int, guestnr:int, user_init:str, pf_file1:str, pf_file2:str, curr_room:str, kreditlimit:decimal, roomtf_code:str, roomtf_resnr:int, roomtf_reslinnr:int, dept_mbar:int, dept_ldry:int, bilrecid:int):
    mess_info = ""
    mess_quest1 = ""
    mess_quest2 = ""
    vsuccess = False
    vclosed = False
    disc_art1:int = 0
    disc_art2:int = 0
    disc_art3:int = 0
    mi_ordertaker:bool = True
    price_decimal:int = 0
    curr_local:str = ""
    curr_foreign:str = ""
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
    c_param870:str = ""
    add_zeit:int = 0
    activate_deposit:bool = False
    bill_date:date = None
    p_88:bool = False
    amt:decimal = 0
    amt_foreign:decimal = 0
    msg_str:str = ""
    msg_str1:str = ""
    msg_str2:str = ""
    balance_foreign:decimal = 0
    balance:decimal = 0
    paid:decimal = 0
    billart:int = 0
    qty:int = 0
    price:decimal = 0
    amount_foreign:decimal = 0
    amount:decimal = 0
    gname:str = ""
    description:str = ""
    transfer_zinr:str = ""
    cancel_flag:bool = False
    mwst:decimal = 0
    mwst_foreign:decimal = 0
    bcol:int = 0
    fl_code1:int = 0
    fl_code2:int = 0
    fl_code3:int = 0
    closed:bool = False
    mealcoupon_cntrl:bool = False
    must_print:bool = False
    zero_flag:bool = False
    multi_cash:bool = False
    cancel_exist:bool = False
    double_currency:bool = False
    dept_name:str = ""
    cancel_str:str = ""
    flag_code:int = 0
    connect_param:str = ""
    connect_paramssl:str = ""
    lreturn:bool = False
    htl_name:str = ""
    cc_comment:str = ""
    success_flag:bool = False
    var_testing:str = ""
    rec_id_artikel:int = 0
    service_code:int = 0
    rechnr:int = 0
    h_bill = kellner = h_artikel = None

    t_h_bill = kellner1 = hbill = t_kellner = t_h_artikel = t_submenu_list = p_list = None

    t_h_bill_list, T_h_bill = create_model_like(H_bill, {"rec_id":int})
    kellner1_list, Kellner1 = create_model_like(Kellner)
    hbill_list, Hbill = create_model("Hbill", {"kellner_nr":int})
    t_kellner_list, T_kellner = create_model("T_kellner", {"kellner_nr":int})
    t_h_artikel_list, T_h_artikel = create_model_like(H_artikel, {"rec_id":int})
    t_submenu_list_list, T_submenu_list = create_model("T_submenu_list", {"menurecid":int, "zeit":int, "nr":int, "artnr":int, "bezeich":str, "anzahl":int, "zknr":int, "request":str})
    p_list_list, P_list = create_model("P_list", {"rechnr":int, "dept":int, "billno":int, "printed_line":int, "b_recid":int, "last_amount":decimal, "last_famount":decimal})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal mess_info, mess_quest1, mess_quest2, vsuccess, vclosed, disc_art1, disc_art2, disc_art3, mi_ordertaker, price_decimal, curr_local, curr_foreign, foreign_rate, exchg_rate, b_title, deptname, p_223, curr_waiter, fl_code, pos1, pos2, cashless_flag, c_param870, add_zeit, activate_deposit, bill_date, p_88, amt, amt_foreign, msg_str, msg_str1, msg_str2, balance_foreign, balance, paid, billart, qty, price, amount_foreign, amount, gname, description, transfer_zinr, cancel_flag, mwst, mwst_foreign, bcol, fl_code1, fl_code2, fl_code3, closed, mealcoupon_cntrl, must_print, zero_flag, multi_cash, cancel_exist, double_currency, dept_name, cancel_str, flag_code, connect_param, connect_paramssl, lreturn, htl_name, cc_comment, success_flag, var_testing, rec_id_artikel, service_code, rechnr, h_bill, kellner, h_artikel


        nonlocal t_h_bill, kellner1, hbill, t_kellner, t_h_artikel, t_submenu_list, p_list
        nonlocal t_h_bill_list, kellner1_list, hbill_list, t_kellner_list, t_h_artikel_list, t_submenu_list_list, p_list_list
        return {"mess_info": mess_info, "mess_quest1": mess_quest1, "mess_quest2": mess_quest2, "vsuccess": vsuccess, "vclosed": vclosed}

    if vkey.lower()  == "checkRoomTfCombo":

        h_bill = db_session.query(H_bill).filter(
                (H_bill._recid == h_recid)).first()

        if h_bill:
            balance_foreign = h_bill.mwst[98]
            balance = h_bill.saldo
            t_h_bill = T_h_bill()
            t_h_bill_list.append(t_h_bill)

            buffer_copy(h_bill, t_h_bill)

        t_h_bill = query(t_h_bill_list, first=True)
        connect_param = "-H " + entry(0, pf_file2, ":") + " -S " + entry(1, pf_file2, ":") + " -DirectConnect -sessionModel Session_free"
        connect_paramssl = connect_param + " -ssl -nohostverify"
        lreturn = set_combo_session(connect_paramssl, None, None, None)

        if not lreturn:
            lreturn = set_combo_session(connect_param, None, None, None)

        if lreturn:
            local_storage.combo_flag = True
            htl_name = get_output(read_hotelnamebl("A120"))
            local_storage.combo_flag = False


        if roomtf_code != "" and (curr_dept == dept_mbar or curr_dept == dept_ldry):
            fl_code = 1

        elif roomtf_code != "" and curr_dept != dept_mbar and curr_dept != dept_ldry:
            fl_code = 2
        local_storage.combo_flag = True
        bilrecid, msg_str, msg_str1, msg_str2 = get_output(ts_rzinr_btn_exitbl(language_code, fl_code, roomtf_code, roomtf_resnr, roomtf_reslinnr, balance))
        local_storage.combo_flag = False


        if msg_str != "":

            if fl_code == 1:
                mess_quest1 = substring(msg_str, 3)

            elif fl_code == 2:
                mess_info = substring(msg_str, 1)

                return generate_output()

        if msg_str1 != "":
            mess_quest2 = substring(msg_str1, 3)

        if msg_str2 != "":
            mess_info = msg_str2

            return generate_output()
        reset_combo_session()

        vsuccess = True

    elif vkey.lower()  == "postRoomTfCombo":
        mealcoupon_cntrl, must_print, zero_flag, multi_cash, cancel_exist, msg_str, disc_art1, disc_art2, disc_art3, mi_ordertaker, price_decimal, curr_local, curr_foreign, double_currency, foreign_rate, exchg_rate, b_title, deptname, p_223, curr_waiter, fl_code, pos1, pos2, cashless_flag, c_param870, activate_deposit, hbill_list, t_kellner_list = get_output(prepare_ts_restinv_1bl(language_code, curr_dept, 1, user_init, None))

        hbill = query(hbill_list, first=True)

        t_kellner = query(t_kellner_list, first=True)

        if msg_str != "":
            mess_info = substring(msg_str, 1)

            return generate_output()

        h_bill = db_session.query(H_bill).filter(
                (H_bill._recid == h_recid)).first()

        if h_bill:
            balance_foreign = h_bill.mwst[98]
            balance = h_bill.saldo
            t_h_bill = T_h_bill()
            t_h_bill_list.append(t_h_bill)

            buffer_copy(h_bill, t_h_bill)

        t_h_bill = query(t_h_bill_list, first=True)
        connect_param = "-H " + entry(0, pf_file2, ":") + " -S " + entry(1, pf_file2, ":") + " -DirectConnect -sessionModel Session_free"
        connect_paramssl = connect_param + " -ssl -nohostverify"
        lreturn = set_combo_session(connect_paramssl, None, None, None)

        if not lreturn:
            lreturn = set_combo_session(connect_param, None, None, None)

        if lreturn:
            local_storage.combo_flag = True
            htl_name = get_output(read_hotelnamebl("A120"))
            local_storage.combo_flag = False

        local_storage.combo_flag = True
        cc_comment, success_flag, msg_str, gname = get_output(combo_transfer_bill_1bl(language_code, 1, curr_dept, deptname, bill_no, None, double_currency, exchg_rate, bilrecid, foreign_rate, user_init, balance, balance_foreign))
        local_storage.combo_flag = False

        reset_combo_session()


        if msg_str != "":
            mess_info = msg_str

            return generate_output()

        if success_flag:
            paid = - balance
            billart, qty, description, price, amount_foreign, amount, bill_date, fl_code, fl_code1, msg_str, var_testing, t_h_artikel_list = get_output(ts_restinv_btn_transfer_paytype1bl(language_code, t_h_bill.rec_id, guestnr, curr_dept, paid, exchg_rate, price_decimal, balance, None, disc_art1, disc_art2, disc_art3, t_kellner_nr))

            t_h_artikel = query(t_h_artikel_list, first=True)

            if msg_str != "":
                mess_info = msg_str

                return generate_output()

            if fl_code == 1:
                fl_code = 0

                if not t_h_artikel:
                    rec_id_artikel = 0
                    service_code = 0
                else:
                    rec_id_artikel = t_h_artikel.rec_id
                    service_code = t_h_artikel.service_code
                bill_date, cancel_flag, fl_code, mwst, mwst_foreign, rechnr, balance, bcol, balance_foreign, fl_code1, fl_code2, fl_code3, p_88, vclosed, t_h_bill_list, kellner1_list = get_output(ts_restinv_update_bill_1bl(language_code, h_recid, rec_id_artikel, deptname, None, t_h_artikel.artart, False, service_code, amount, amount_foreign, price, double_currency, qty, exchg_rate, price_decimal, 0, tischnr, curr_dept, user_init, gname, pax, kreditlimit, 1, billart, description, "", cc_comment, "", "", "", "", True, False, t_h_artikel.artnrfront, 1, guestnr, "", False, foreign_rate, curr_room, user_init, 0, 0, False, 0, "", t_submenu_list))

                t_h_bill = query(t_h_bill_list, first=True)

                kellner1 = query(kellner1_list, first=True)

                if fl_code == 1:
                    mess_info = "Transaction not allowed: Posted item(s) with differrent billing date found."

                    return generate_output()

                elif fl_code == 2:

                    return generate_output()

                if t_h_artikel.artart == 2 and vclosed:
                    get_output(ts_restsale_update_h_billbl(t_h_bill.rec_id))
                    p_list_list = get_output(ts_restinv_del_queasybl(p_list, t_h_bill.rec_id, False))

            elif fl_code == 2:
                mess_info = "NOT DEFINED: F/O Article" + " " + to_string(billart) + chr(10) + "C/L Posting not possible."

                return generate_output()

            elif fl_code == 3:
                mess_info = "F/O Article not available."

                return generate_output()
        vsuccess = True

    return generate_output()