#using conversion tools version: 1.0.0.117

# ==========================================
# Rulita, 09-10-2025
# Tiket ID : 8CF423 | Recompile Program
# ==========================================

from functions.additional_functions import *
from decimal import Decimal
from models import Zimmer, Paramtext

input_param_data, Input_param = create_model("Input_param", {"case_type":int, "int1":int, "int2":int, "int3":int})

def delete_paramtext_setup_wizardbl(input_param_data:[Input_param]):
    output_param_data = []
    do_it:bool = False
    zimmer = paramtext = None

    input_param = output_param = None

    output_param_data, Output_param = create_model("Output_param", {"success_flag":bool, "msg_str":string})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal output_param_data, do_it, zimmer, paramtext


        nonlocal input_param, output_param
        nonlocal output_param_data

        return {"output-param": output_param_data}


    input_param = query(input_param_data, first=True)

    if not input_param:
        output_param = Output_param()
        output_param_data.append(output_param)

        output_param.success_flag = False
        output_param.msg_str = "Error loading.. please contact our Customer Service"

        return generate_output()

    for input_param in query(input_param_data):

        zimmer = get_cache (Zimmer, {"setup": [(eq, (input_param.int1 - 9200))]})

        if zimmer:
            do_it = True
            output_param = Output_param()
            output_param_data.append(output_param)

            output_param.success_flag = False
            output_param.msg_str = "Record bed type : " + to_string(input_param.int1) + " already used in room setup. Please delete another bed type"


            break

    if do_it :

        return generate_output()

    for input_param in query(input_param_data):

        paramtext = get_cache (Paramtext, {"txtnr": [(eq, input_param.int1)],"number": [(eq, input_param.int2)],"sprachcode": [(eq, input_param.int3)]})

        if paramtext:
            db_session.delete(paramtext)
            pass
            output_param = Output_param()
            output_param_data.append(output_param)

            output_param.success_flag = True
            output_param.msg_str = "Deleted bed number " + to_string(input_param.int1) + "Successfully."


        else:
            output_param = Output_param()
            output_param_data.append(output_param)

            output_param.success_flag = False
            output_param.msg_str = "Record bed type : " + to_string(input_param.int1) + " not found. Please delete another bed type"

    return generate_output()