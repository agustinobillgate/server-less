#using conversion tools version: 1.0.0.117

# ==========================================
# Rulita, 09-10-2025
# Tiket ID : 8CF423 | Recompile Program
# ==========================================

from functions.additional_functions import *
from decimal import Decimal
from models import Zimmer, Zimkateg

input_param_data, Input_param = create_model("Input_param", {"zikatnr":int})

def rmcat_admin_setup_wizardbl(input_param_data:[Input_param]):
    output_param_data = []
    zimmer = zimkateg = None

    input_param = output_param = None

    output_param_data, Output_param = create_model("Output_param", {"success_flag":bool, "msg_str":string})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal output_param_data, zimmer, zimkateg


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

        zimmer = get_cache (Zimmer, {"zikatnr": [(eq, input_param.zikatnr)]})

        if zimmer:
            output_param = Output_param()
            output_param_data.append(output_param)

            output_param.success_flag = False
            output_param.msg_str = "Room under this category exists, deleting not possible."


        else:

            zimkateg = get_cache (Zimkateg, {"zikatnr": [(eq, input_param.zikatnr)]})

            if zimkateg:
                output_param = Output_param()
                output_param_data.append(output_param)

                output_param.success_flag = True
                output_param.msg_str = "Deleted Number " + to_string(zimkateg.zikatnr) + " Of Room Type Successfully."


                db_session.delete(zimkateg)
            else:
                output_param = Output_param()
                output_param_data.append(output_param)

                output_param.success_flag = False
                output_param.msg_str = "Record room type " + to_string(input_param.zikatnr) + " not found. Please delete another room type"

    return generate_output()