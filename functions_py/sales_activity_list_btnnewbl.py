#using conversion tools version: 1.0.0.117
#-------------------------------------------------------
# Rd, 28/11/2025, with_for_update added
#-------------------------------------------------------
from functions.additional_functions import *
from decimal import Decimal
from models import B_storno, Bk_reser, Bk_veran
from sqlalchemy.orm.attributes import flag_modified

def sales_activity_list_btnnewbl(resnr:int, add_str:string, user_init:string, counter_reason:int):

    prepare_cache ([B_storno, Bk_veran])

    output_list_data = []
    b_storno = bk_reser = bk_veran = None

    output_list = t_b_storno = None

    output_list_data, Output_list = create_model("Output_list", {"outnr":int, "act_str":string})
    t_b_storno_data, T_b_storno = create_model_like(B_storno)

    db_session = local_storage.db_session
    add_str = add_str.strip()

    def generate_output():
        nonlocal output_list_data, b_storno, bk_reser, bk_veran
        nonlocal resnr, add_str, user_init, counter_reason


        nonlocal output_list, t_b_storno
        nonlocal output_list_data, t_b_storno_data

        return {"counter_reason": counter_reason, "output-list": output_list_data}

    def create_outlist():

        nonlocal output_list_data, b_storno, bk_reser, bk_veran
        nonlocal resnr, add_str, user_init, counter_reason


        nonlocal output_list, t_b_storno
        nonlocal output_list_data, t_b_storno_data

        i:int = 0
        counter_reason = 0
        output_list_data.clear()
        for i in range(1,18 + 1) :

            if b_storno.grund[i - 1] != "":
                output_list = Output_list()
                output_list_data.append(output_list)

                outnr = i
                act_str = b_storno.grund[i - 1]


                counter_reason = i

    # b_storno = get_cache (B_storno, {"bankettnr": [(eq, resnr)]})
    b_storno = db_session.query(B_storno).filter(B_storno.bankettnr == resnr).with_for_update().first()

    if not b_storno:

        bk_reser = get_cache (Bk_reser, {"veran_nr": [(eq, resnr)]})

        bk_veran = get_cache (Bk_veran, {"veran_nr": [(eq, resnr)]})
        b_storno = B_storno()
        db_session.add(b_storno)

        b_storno.bankettnr = resnr
        b_storno.gastnr = bk_veran.gastnr
        counter_reason = 0
    pass
    b_storno.grund[17] = add_str.upper() + " " + to_string(get_current_date(), "99/99/99") + "-" + to_string(get_current_time_in_seconds(), "hh:mm:ss") + " (" + user_init + ")"
    pass
    create_outlist()
    flag_modified(b_storno, "grund")

    return generate_output()