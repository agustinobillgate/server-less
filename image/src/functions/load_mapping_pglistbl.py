from functions.additional_functions import *
import decimal
from models import Queasy

def load_mapping_pglistbl(pg_number:int, department:int):
    payment_gateway_list_list = []
    queasy = None

    payment_gateway_list = None

    payment_gateway_list_list, Payment_gateway_list = create_model("Payment_gateway_list", {"pg_art_no":int, "pg_art_name":str, "pg_grp_no":int, "pg_grp_name":str, "pg_art_activate":bool, "vhp_art_no":int, "vhp_art_name":str, "vhp_art_dept":int})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal payment_gateway_list_list, queasy


        nonlocal payment_gateway_list
        nonlocal payment_gateway_list_list
        return {"payment-gateway-list": payment_gateway_list_list}

    for queasy in db_session.query(Queasy).filter(
            (Queasy.key == 224) &  (Queasy.number2 == department) &  (Queasy.number1 == pg_number) &  (Queasy.logi1)).all():
        payment_gateway_list = Payment_gateway_list()
        payment_gateway_list_list.append(payment_gateway_list)

        payment_gateway_list.pg_art_no = to_int(entry(0, queasy.char1, "-"))
        payment_gateway_list.pg_art_name = entry(1, queasy.char1, "-")

        if num_entries(queasy.char2, "-") >= 2:
            payment_gateway_list.pg_grp_no = to_int(entry(0, queasy.char2, "-"))
            payment_gateway_list.pg_grp_name = entry(1, queasy.char2, "-")
        else:
            payment_gateway_list.pg_grp_name = queasy.char2
        payment_gateway_list.pg_art_activate = queasy.logi1

        if num_entries(queasy.char3, "-") >= 2:
            payment_gateway_list.vhp_art_no = to_int(entry(0, queasy.char3, "-"))
            payment_gateway_list.vhp_art_name = entry(1, queasy.char3, "-")
        payment_gateway_list.vhp_art_dept = queasy.number2

    return generate_output()