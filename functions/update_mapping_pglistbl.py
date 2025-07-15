from functions.additional_functions import *
import decimal
from models import Queasy

def update_mapping_pglistbl(pg_number:int, art_dept:int, payment_gateway_list:[Payment_gateway_list]):
    queasy = None

    payment_gateway_list = None

    payment_gateway_list_list, Payment_gateway_list = create_model("Payment_gateway_list", {"pg_art_no":int, "pg_art_name":str, "pg_grp_no":int, "pg_grp_name":str, "pg_art_activate":bool, "vhp_art_no":int, "vhp_art_name":str, "vhp_art_dept":int})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal queasy


        nonlocal payment_gateway_list
        nonlocal payment_gateway_list_list
        return {}

    for payment_gateway_list in query(payment_gateway_list_list):

        queasy = db_session.query(Queasy).filter(
                (Queasy.key == 224) &  (Queasy.number1 == pg_number) &  (Queasy.number2 == art_dept) &  (Queasy.char1 == to_string(payment_gateway_list.pg_art_no) + "-" + payment_gateway_list.pg_art_name) &  (Queasy.logi1 != payment_gateway_list.pg_art_activate) &  (Queasy.char3 != to_string(payment_gateway_list.vhp_art_no) + "-" + payment_gateway_list.vhp_art_name)).first()

        if queasy:
            queasy.logi1 = payment_gateway_list.pg_art_activate

            if payment_gateway_list.pg_art_activate:
                queasy.char3 = to_string(payment_gateway_list.vhp_art_no) + "-" + payment_gateway_list.vhp_art_name
            else:
                queasy.char3 = ""

    return generate_output()