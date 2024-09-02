from functions.additional_functions import *
import decimal
from models import B_storno, Bk_reser, Bk_veran

def sales_activity_list_btnnewbl(resnr:int, add_str:str, user_init:str, counter_reason:int):
    output_list_list = []
    b_storno = bk_reser = bk_veran = None

    output_list = t_b_storno = None

    output_list_list, Output_list = create_model("Output_list", {"outnr":int, "act_str":str})
    t_b_storno_list, T_b_storno = create_model_like(B_storno)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal output_list_list, b_storno, bk_reser, bk_veran


        nonlocal output_list, t_b_storno
        nonlocal output_list_list, t_b_storno_list
        return {"output-list": output_list_list}

    def create_outlist():

        nonlocal output_list_list, b_storno, bk_reser, bk_veran


        nonlocal output_list, t_b_storno
        nonlocal output_list_list, t_b_storno_list

        i:int = 0
        counter_reason = 0
        output_list_list.clear()
        for i in range(1,18 + 1) :

            if b_storno.grund[i - 1] != "":
                output_list = Output_list()
                output_list_list.append(output_list)

                outnr = i
                act_str = b_storno.grund[i - 1]


                counter_reason = i


    b_storno = db_session.query(B_storno).filter(
            (B_storno.bankettnr == resnr)).first()

    if not b_storno:

        bk_reser = db_session.query(Bk_reser).filter(
                (Bk_reser.veran_nr == resnr)).first()

        bk_veran = db_session.query(Bk_veran).filter(
                (Bk_veran.veran_nr == resnr)).first()
        b_storno = B_storno()
        db_session.add(b_storno)

        b_storno.bankettnr = resnr
        b_storno.gastnr = bk_veran.gastnr
        counter_reason = 0

    b_storno = db_session.query(B_storno).first()
    b_storno.grund[17] = add_str.upper() + " " + to_string(get_current_date(), "99/99/99") + "-" + to_string(get_current_time_in_seconds(), "hh:mm:ss") + " (" + user_init + ")"

    b_storno = db_session.query(B_storno).first()
    create_outlist()

    return generate_output()