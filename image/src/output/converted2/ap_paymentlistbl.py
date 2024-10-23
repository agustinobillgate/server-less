from functions.additional_functions import *
import decimal
from datetime import date
from functions.ap_paylist_btn_go_bl import ap_paylist_btn_go_bl

def ap_paymentlistbl(all_supp:bool, remark_flag:bool, from_supp:str, from_date:date, to_date:date, from_remark:str, price_decimal:int):
    lief_nr1 = 0
    ap_exist = False
    err_code = 0
    ap_paymentlist_list = []
    t_list_list = []
    amount:str = ""

    t_list = output_list = ap_paymentlist = None

    t_list_list, T_list = create_model("T_list", {"artnr":int, "bezeich":str, "betrag":decimal})
    output_list_list, Output_list = create_model("Output_list", {"srecid":int, "remark":str, "str":str})
    ap_paymentlist_list, Ap_paymentlist = create_model("Ap_paymentlist", {"srecid":int, "remark":str, "billdate":date, "docu_nr":str, "ap_amount":decimal, "pay_amount":decimal, "pay_date":date, "id":str, "pay_art":str, "supplier":str, "deliv_note":str})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal lief_nr1, ap_exist, err_code, ap_paymentlist_list, t_list_list, amount
        nonlocal all_supp, remark_flag, from_supp, from_date, to_date, from_remark, price_decimal


        nonlocal t_list, output_list, ap_paymentlist
        nonlocal t_list_list, output_list_list, ap_paymentlist_list
        return {"lief_nr1": lief_nr1, "ap_exist": ap_exist, "err_code": err_code, "ap-paymentlist": ap_paymentlist_list, "t-list": t_list_list}


    lief_nr1, ap_exist, err_code, output_list_list, t_list_list = get_output(ap_paylist_btn_go_bl(all_supp, remark_flag, from_supp, from_date, to_date, from_remark, price_decimal))

    for output_list in query(output_list_list):
        amount = trim(substring(output_list.str, 38, 17))

        if amount.lower()  == ("TOTAL").lower() :
            amount = ""

        elif amount.lower()  == ("Grand TOTAL").lower() :
            amount = ""
        ap_paymentlist = Ap_paymentlist()
        ap_paymentlist_list.append(ap_paymentlist)

        ap_paymentlist.srecid = output_list.srecid
        ap_paymentlist.remark = output_list.remark
        ap_paymentlist.billdate = date_mdy(trim(substring(output_list.str, 0, 8)))
        ap_paymentlist.docu_nr = trim(substring(output_list.str, 8, 30))
        ap_paymentlist.ap_amount =  to_decimal(to_decimal(amount) )
        ap_paymentlist.pay_amount = to_decimal(substring(output_list.str, 55, 17))
        ap_paymentlist.pay_date = date_mdy(trim(substring(output_list.str, 72, 8)))
        ap_paymentlist.id = trim(substring(output_list.str, 80, 3))
        ap_paymentlist.pay_art = substring(output_list.str, 83, 20)
        ap_paymentlist.supplier = substring(output_list.str, 135, 24)
        ap_paymentlist.deliv_note = substring(output_list.str, 160, 30)

    return generate_output()