#using conversion tools version: 1.0.0.117

# ==========================================
# Rulita, 10-10-2025
# Tiket ID : 8CF423 | Recompile Program
# ==========================================

from functions.additional_functions import *
from decimal import Decimal
from models import Queasy

input_list_data, Input_list = create_model("Input_list", {"curr_section":int, "curr_subsection":Decimal, "section_title":string, "subsection_title":string})

def save_progress_setup_wizardbl(input_list_data:[Input_list]):

    prepare_cache ([Queasy])

    output_list_data = []
    curr_section:int = 0
    curr_subsection:Decimal = to_decimal("0.0")
    section_title:string = ""
    subsection_title:string = ""
    queasy = None

    input_list = output_list = None

    output_list_data, Output_list = create_model("Output_list", {"msg_str":string, "success_flag":bool})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal output_list_data, curr_section, curr_subsection, section_title, subsection_title, queasy


        nonlocal input_list, output_list
        nonlocal output_list_data

        return {"output-list": output_list_data}

    def create_section():

        nonlocal output_list_data, curr_section, curr_subsection, section_title, subsection_title, queasy


        nonlocal input_list, output_list
        nonlocal output_list_data

        queasy = get_cache (Queasy, {"key": [(eq, 357)],"number1": [(eq, curr_section)],"number2": [(eq, 0)],"deci1": [(eq, curr_subsection)],"char1": [(eq, section_title)],"char2": [(eq, subsection_title)],"logi1": [(eq, True)]})

        if not queasy:
            queasy = Queasy()
            db_session.add(queasy)

            queasy.key = 357
            queasy.number1 = curr_section
            queasy.number2 = 0
            queasy.deci1 =  to_decimal(curr_subsection)
            queasy.char1 = section_title
            queasy.char2 = subsection_title
            queasy.logi1 = True


        output_list.msg_str = "Progress saved successfully"
        output_list.success_flag = True


    output_list = Output_list()
    output_list_data.append(output_list)


    input_list = query(input_list_data, first=True)

    if not input_list:
        output_list.msg_str = "Error loading.. please contact our Customer Service"
        output_list.success_flag = False

        return generate_output()
    else:
        curr_section = input_list.curr_section
        curr_subsection =  to_decimal(input_list.curr_subsection)

        if input_list.section_title == None:
            section_title = ""
        else:
            section_title = input_list.section_title

        if input_list.subsection_title == None:
            subsection_title = ""
        else:
            subsection_title = input_list.subsection_title

    if curr_section == 0:
        output_list.msg_str = "Section number can't be empty"
        output_list.success_flag = False

        return generate_output()

    elif curr_subsection == 0 and curr_section != 2:
        output_list.msg_str = "Subsection number can't be empty"
        output_list.success_flag = False

        return generate_output()

    elif section_title == "":
        output_list.msg_str = "Section name can't be empty"
        output_list.success_flag = False

        return generate_output()

    elif subsection_title == "" and curr_section != 2:
        output_list.msg_str = "Subsection name can't be empty"
        output_list.success_flag = False

        return generate_output()
    else:
        create_section()

    return generate_output()