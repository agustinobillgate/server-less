#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from functions.tada_post_paymentbl import tada_post_paymentbl
from models import H_bill, Kellner, Queasy, H_artikel, Tisch

def tada_dashboard_post_paymentbl(user_init:string, deptno:int, orderid:int, payment_artnr:int, payment_amount:Decimal):

    prepare_cache ([Queasy, H_artikel])

    result_message = ""
    vhp_artno:int = 0
    vhp_artdep:int = 0
    i_str:int = 0
    mess_token:string = ""
    mess_keyword:string = ""
    mess_value:string = ""
    language_code:int = 1
    service_code:int = 0
    rec_id:int = 0
    tischnr:int = 0
    curr_dept:int = 0
    pax:int = 0
    resnr:int = 0
    reslinnr:int = 0
    fl_code:int = 0
    fl_code1:int = 0
    fl_code2:int = 0
    fl_code3:int = 0
    bill_date:date = None
    cancel_flag:bool = False
    mwst:Decimal = to_decimal("0.0")
    mwst_foreign:Decimal = to_decimal("0.0")
    balance:Decimal = to_decimal("0.0")
    bcol:int = 0
    balance_foreign:Decimal = to_decimal("0.0")
    p_88:bool = False
    closed:bool = False
    rechnr:int = 0
    h_bill = kellner = queasy = h_artikel = tisch = None

    t_h_bill = t_submenu_list = t_kellner1 = tablecolor = orderhdr = orderline = mapping = None

    t_h_bill_list, T_h_bill = create_model_like(H_bill, {"rec_id":int})
    t_submenu_list_list, T_submenu_list = create_model("T_submenu_list", {"menurecid":int, "zeit":int, "nr":int, "artnr":int, "bezeich":string, "anzahl":int, "zknr":int, "request":string})
    t_kellner1_list, T_kellner1 = create_model_like(Kellner)

    Tablecolor = create_buffer("Tablecolor",Queasy)
    Orderhdr = create_buffer("Orderhdr",Queasy)
    Orderline = create_buffer("Orderline",Queasy)
    Mapping = create_buffer("Mapping",Queasy)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal result_message, vhp_artno, vhp_artdep, i_str, mess_token, mess_keyword, mess_value, language_code, service_code, rec_id, tischnr, curr_dept, pax, resnr, reslinnr, fl_code, fl_code1, fl_code2, fl_code3, bill_date, cancel_flag, mwst, mwst_foreign, balance, bcol, balance_foreign, p_88, closed, rechnr, h_bill, kellner, queasy, h_artikel, tisch
        nonlocal user_init, deptno, orderid, payment_artnr, payment_amount
        nonlocal tablecolor, orderhdr, orderline, mapping


        nonlocal t_h_bill, t_submenu_list, t_kellner1, tablecolor, orderhdr, orderline, mapping
        nonlocal t_h_bill_list, t_submenu_list_list, t_kellner1_list

        return {"result_message": result_message}


    curr_dept = deptno
    pax = 1

    orderhdr = get_cache (Queasy, {"key": [(eq, 271)],"betriebsnr": [(eq, 1)],"number1": [(eq, deptno)],"number2": [(eq, orderid)]})

    if orderhdr:
        rechnr = orderhdr.number3
        tischnr = to_int(entry(1, orderhdr.char2, "|"))

    mapping = get_cache (Queasy, {"key": [(eq, 270)],"number1": [(eq, 3)],"number2": [(eq, payment_artnr)],"betriebsnr": [(eq, deptno)]})

    if mapping:
        vhp_artno = mapping.number3
        vhp_artdep = mapping.betriebsnr

    h_artikel = get_cache (H_artikel, {"departement": [(eq, vhp_artdep)],"artnr": [(eq, vhp_artno)]})
    bill_date, cancel_flag, fl_code, mwst, mwst_foreign, rechnr, balance, bcol, balance_foreign, fl_code1, fl_code2, fl_code3, p_88, closed, t_h_bill_list, t_kellner1_list = get_output(tada_post_paymentbl(language_code, rec_id, h_artikel._recid, "", None, h_artikel.artart, False, h_artikel.service_code, - to_decimal(payment_amount), - to_decimal(payment_amount), 0, False, 1, 1, 0, user_init, tischnr, curr_dept, user_init, "", pax, 0, 0, h_artikel.artnr, h_artikel.bezeich, "", "", "", "", "", "", True, False, h_artikel.artnrfront, 0, 0, "", False, False, "", user_init, resnr, reslinnr, t_submenu_list_list))

    if closed:

        tablecolor = get_cache (Queasy, {"key": [(eq, 31)],"number1": [(eq, curr_dept)],"betriebsnr": [(eq, 0)],"number2": [(eq, tischnr)]})

        if tablecolor:

            tisch = get_cache (Tisch, {"departement": [(eq, tablecolor.number1)],"tischnr": [(eq, tablecolor.number2)]})

            if tisch:
                tablecolor.date1 = None
                tablecolor.number3 = 0


    result_message = "0 - Post Payment Success!"

    return generate_output()