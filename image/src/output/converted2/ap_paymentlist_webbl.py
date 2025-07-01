#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from functions.ap_paylist_btn_go1_cldbl import ap_paylist_btn_go1_cldbl

def ap_paymentlist_webbl(all_supp:bool, remark_flag:bool, from_supp:string, from_date:date, to_date:date, from_remark:string, price_decimal:int, sort_type:int):
    lief_nr1 = 0
    ap_exist = False
    err_code = 0
    ap_paymentlist_list = []
    t_list_list = []
    amount:string = ""
    pay_amount:string = ""

    t_list = output_list = ap_paymentlist = None

    t_list_list, T_list = create_model("T_list", {"artnr":int, "bezeich":string, "betrag":Decimal})
    output_list_list, Output_list = create_model("Output_list", {"srecid":int, "remark":string, "str":string})
    ap_paymentlist_list, Ap_paymentlist = create_model("Ap_paymentlist", {"srecid":int, "remark":string, "billdate":date, "docu_nr":string, "ap_amount":Decimal, "pay_amount":Decimal, "pay_date":date, "id":string, "pay_art":string, "supplier":string, "deliv_note":string, "bank_name":string, "bank_an":string, "bank_acc":string, "flag_string":int})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal lief_nr1, ap_exist, err_code, ap_paymentlist_list, t_list_list, amount, pay_amount
        nonlocal all_supp, remark_flag, from_supp, from_date, to_date, from_remark, price_decimal, sort_type


        nonlocal t_list, output_list, ap_paymentlist
        nonlocal t_list_list, output_list_list, ap_paymentlist_list

        return {"lief_nr1": lief_nr1, "ap_exist": ap_exist, "err_code": err_code, "ap-paymentlist": ap_paymentlist_list, "t-list": t_list_list}


    lief_nr1, ap_exist, err_code, output_list_list, t_list_list = get_output(ap_paylist_btn_go1_cldbl(all_supp, remark_flag, from_supp, from_date, to_date, from_remark, price_decimal, sort_type))

    for output_list in query(output_list_list):
        amount = trim(substring(output_list.str, 38, 25))
        pay_amount = (trim(substring(output_list.str, 63, 25)))

        if pay_amount.lower()  == ("0").lower()  or pay_amount.lower()  == " ":
            pay_amount = "-"

        if matches(amount,r"*TOTAL*"):
            amount = ""

        elif matches(amount,r"*Grand TOTAL*"):
            amount = ""
        ap_paymentlist = Ap_paymentlist()
        ap_paymentlist_list.append(ap_paymentlist)

        ap_paymentlist.srecid = output_list.srecid
        ap_paymentlist.remark = output_list.remark
        ap_paymentlist.billdate = date_mdy(trim(substring(output_list.str, 0, 8)))
        ap_paymentlist.docu_nr = trim(substring(output_list.str, 8, 30))
        ap_paymentlist.ap_amount =  to_decimal(to_decimal(amount))
        ap_paymentlist.pay_amount =  to_decimal(to_decimal(pay_amount))
        ap_paymentlist.pay_date = date_mdy(trim(substring(output_list.str, 88, 8)))
        ap_paymentlist.id = trim(substring(output_list.str, 96, 3))
        ap_paymentlist.pay_art = substring(output_list.str, 99, 20)
        ap_paymentlist.supplier = substring(output_list.str, 151, 24)
        ap_paymentlist.deliv_note = substring(output_list.str, 175, 30)
        ap_paymentlist.bank_name = substring(output_list.str, 251, 35)
        ap_paymentlist.bank_an = substring(output_list.str, 286, 35)
        ap_paymentlist.bank_acc = substring(output_list.str, 321, 35)

        if ap_paymentlist.supplier == " " and ap_paymentlist.docu_nr == " ":
            ap_paymentlist.flag_string = 1

    return generate_output()