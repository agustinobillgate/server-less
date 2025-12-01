#using conversion tools version: 1.0.0.117

# ==========================================
# Rulita, 09-10-2025
# Tiket ID : 8CF423 | Recompile Program
# Rd, 28/11/2025, with_for_update added
# ==========================================

from functions.additional_functions import *
from decimal import Decimal
from models import Zimmer, Paramtext

input_param_data, Input_param = create_model("Input_param", {"case_type":int, "txtnr":int, "sprachcode":int})

def delete_rm_view_setup_wizardbl(input_param_data:[Input_param]):
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

        zimmer = get_cache (Zimmer, {"typ": [(eq, input_param.sprachcode)]})

        if zimmer:
            do_it = True
            output_param = Output_param()
            output_param_data.append(output_param)

            output_param.success_flag = False
            output_param.msg_str = "Record room view number of " + to_string(input_param.sprachcode) + " already used in room setup. Please delete another room view"


            break

    if do_it :

        return generate_output()

    for input_param in query(input_param_data):

        if input_param.case_type == 1:

            # paramtext = get_cache (Paramtext, {"txtnr": [(eq, input_param.txtnr)],"sprachcode": [(eq, input_param.sprachcode)]})
            paramtext = db_session.query(Paramtext).filter(
                     (Paramtext.txtnr == input_param.txtnr) & (Paramtext.sprachcode == input_param.sprachcode)).with_for_update().first()

            if paramtext:

                output_param = query(output_param_data, first=True)

                if not output_param:
                    output_param = Output_param()
                    output_param_data.append(output_param)

                    output_param.success_flag = True
                    output_param.msg_str = "Deleted room view number of successfully."


                db_session.delete(paramtext)
            else:

                output_param = query(output_param_data, first=True)

                if not output_param:
                    output_param = Output_param()
                    output_param_data.append(output_param)

                    output_param.success_flag = False
                    output_param.msg_str = "Record room view number of " + to_string(input_param.sprachcode) + " not found. Please delete another room view"

    return generate_output()