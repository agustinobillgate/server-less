#using conversion tools version: 1.0.0.117

# =======================================================
# Rulita, 09-10-2025
# Tiket ID : 8CF423 | Recompile Program
# Issue case_type not define fixing input_list.case_type
# =======================================================

from functions.additional_functions import *
from decimal import Decimal
from models import Zimmer

input_list_data, Input_list = create_model("Input_list", {"case_type":int, "rmno":string})

def read_zimmer_setup_wizardbl(input_list_data:[Input_list]):

    prepare_cache ([Zimmer])

    output_zimmer_data = []
    output_list_data = []
    zimmer = None

    input_list = output_zimmer = output_list = None

    output_zimmer_data, Output_zimmer = create_model("Output_zimmer", {"zinr":string, "view_type":int, "bed_type":int, "etage":int, "zikatnr":int, "sleeping":bool})
    output_list_data, Output_list = create_model("Output_list", {"success_flag":bool, "msg_str":string})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal output_zimmer_data, output_list_data, zimmer


        nonlocal input_list, output_zimmer, output_list
        nonlocal output_zimmer_data, output_list_data

        return {"output-zimmer": output_zimmer_data, "output-list": output_list_data}

    input_list = query(input_list_data, first=True)

    if not input_list:
        output_list = Output_list()
        output_list_data.append(output_list)

        output_list.success_flag = False
        output_list.msg_str = "Error loading.. please contact our Customer Service"

        return generate_output()

    # Rulita
    if input_list.case_type == 1:

        zimmer = get_cache (Zimmer, {"zinr": [(eq, input_list.rmno)]})

        if zimmer:
            output_zimmer = Output_zimmer()
            output_zimmer_data.append(output_zimmer)

            output_zimmer.zinr = zimmer.zinr
            output_zimmer.view_type = zimmer.typ
            output_zimmer.bed_type = zimmer.setup
            output_zimmer.etage = zimmer.etage
            output_zimmer.zikatnr = zimmer.zikatnr
            output_zimmer.sleeping = zimmer.sleeping


            output_list = Output_list()
            output_list_data.append(output_list)

            output_list.success_flag = False
            output_list.msg_str = "Room number " + to_string(input_list.rmNo) + " Already exists. Please change another room number "


        else:
            output_list = Output_list()
            output_list_data.append(output_list)

            output_list.success_flag = True
            output_list.msg_str = "input room number " + to_string(input_list.rmNo) + " successfully created: "

    return generate_output()