#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from functions.mapping_pglistbl import mapping_pglistbl
from functions.update_mapping_pglistbl import update_mapping_pglistbl

payment_gateway_list_list, Payment_gateway_list = create_model("Payment_gateway_list", {"pg_art_no":int, "pg_art_name":string, "pg_grp_no":int, "pg_grp_name":string, "pg_art_activate":bool, "vhp_art_no":int, "vhp_art_name":string, "vhp_art_dept":int})

def update_mapping_pglist_webbl(payment_gateway_list_list:[Payment_gateway_list], select_dept:string, select_pg:string):
    result_msg = ""
    art_dept:int = 0
    pg_number:int = 0

    payment_gateway_list = vhp_payment_list = payment_gateway = None

    vhp_payment_list_list, Vhp_payment_list = create_model("Vhp_payment_list", {"vhp_art_no":int, "vhp_art_name":string})
    payment_gateway_list, Payment_gateway = create_model("Payment_gateway", {"pg_art_no":int, "pg_art_name":string, "pg_grp_no":int, "pg_grp_name":string, "pg_art_activate":bool, "vhp_art_no":int, "vhp_art_name":string, "vhp_art_dept":int})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal result_msg, art_dept, pg_number
        nonlocal select_dept, select_pg


        nonlocal payment_gateway_list, vhp_payment_list, payment_gateway
        nonlocal vhp_payment_list_list, payment_gateway_list

        return {"payment-gateway-list": payment_gateway_list_list, "result_msg": result_msg}


    payment_gateway_list.clear()

    for payment_gateway_list in query(payment_gateway_list_list):
        payment_gateway = Payment_gateway()
        payment_gateway_list.append(payment_gateway)

        buffer_copy(payment_gateway_list, payment_gateway)
    art_dept = to_int(trim(entry(0, select_dept, "-")))
    pg_number = to_int(trim(entry(0, select_pg, "-")))
    payment_gateway_list_list, vhp_payment_list_list = get_output(mapping_pglistbl(2, 0, pg_number, select_pg, art_dept, ""))

    for payment_gateway in query(payment_gateway_list):

        vhp_payment_list = query(vhp_payment_list_list, filters=(lambda vhp_payment_list: vhp_payment_list.vhp_art_no == payment_gateway.vhp_art_no), first=True)

        if vhp_payment_list:
            payment_gateway.vhp_art_name = vhp_payment_list.vhp_art_name
            payment_gateway.vhp_art_dept = art_dept
        else:
            payment_gateway.vhp_art_no = 0
            payment_gateway.pg_art_activate = False
    payment_gateway_list_list.clear()

    for payment_gateway in query(payment_gateway_list):
        payment_gateway_list = Payment_gateway_list()
        payment_gateway_list_list.append(payment_gateway_list)

        buffer_copy(payment_gateway, payment_gateway_list)
    get_output(update_mapping_pglistbl(pg_number, art_dept, payment_gateway_list_list))
    result_msg = "MAPPING DONE"

    return generate_output()