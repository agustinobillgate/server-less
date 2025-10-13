#using conversion tools version: 1.0.0.117

# ==========================================
# Rulita, 09-10-2025
# Tiket ID : 8CF423 | Recompile Program
# ==========================================

from functions.additional_functions import *
from decimal import Decimal
from sqlalchemy import func
from models import Zimkateg, Queasy

input_list_data, Input_list = create_model("Input_list", {"bezeichnung":string})

def prepare_rmcat_admin_setup_wizardbl(input_list_data:[Input_list]):

    prepare_cache ([Queasy])

    t_zimkateg_data = []
    output_list_data = []
    do_it:bool = False
    zimkateg = queasy = None

    t_zimkateg = input_list = output_list = pqueasy = None

    t_zimkateg_data, T_zimkateg = create_model_like(Zimkateg, {"priority":int, "max_avail":int, "msg_str":string})
    output_list_data, Output_list = create_model("Output_list", {"success_flag":bool, "msg_str":string})

    Pqueasy = create_buffer("Pqueasy",Queasy)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal t_zimkateg_data, output_list_data, do_it, zimkateg, queasy
        nonlocal pqueasy


        nonlocal t_zimkateg, input_list, output_list, pqueasy
        nonlocal t_zimkateg_data, output_list_data

        return {"t-zimkateg": t_zimkateg_data, "output-list": output_list_data}

    input_list = query(input_list_data, first=True)

    if not input_list:
        output_list = Output_list()
        output_list_data.append(output_list)

        output_list.success_flag = False
        output_list.msg_str = "Error loading.. please contact our Customer Service"

        return generate_output()

    if input_list.bezeichnung == "":

        for zimkateg in db_session.query(Zimkateg).order_by(Zimkateg._recid).all():
            t_zimkateg = T_zimkateg()
            t_zimkateg_data.append(t_zimkateg)

            buffer_copy(zimkateg, t_zimkateg)

            output_list = query(output_list_data, first=True)

            if not output_list:
                output_list = Output_list()
                output_list_data.append(output_list)

                output_list.success_flag = True
                output_list.msg_str = "Room type found."

            pqueasy = get_cache (Queasy, {"key": [(eq, 325)],"number1": [(eq, zimkateg.zikatnr)]})

            if pqueasy:
                t_zimkateg.priority = pqueasy.number2
                t_zimkateg.max_avail = pqueasy.number3


            do_it = True

        if do_it == False:
            output_list = Output_list()
            output_list_data.append(output_list)

            output_list.success_flag = False
            output_list.msg_str = "Room type not found. Please create a room type first"


    else:

        for zimkateg in db_session.query(Zimkateg).filter(
                 (matches(Zimkateg.bezeichnung,"*" + input_list.bezeichnung + "*"))).order_by(Zimkateg._recid).all():
            t_zimkateg = T_zimkateg()
            t_zimkateg_data.append(t_zimkateg)

            buffer_copy(zimkateg, t_zimkateg)

            output_list = query(output_list_data, first=True)

            if not output_list:
                output_list = Output_list()
                output_list_data.append(output_list)

                output_list.success_flag = True
                output_list.msg_str = "Room type found."

            pqueasy = get_cache (Queasy, {"key": [(eq, 325)],"number1": [(eq, zimkateg.zikatnr)]})

            if pqueasy:
                t_zimkateg.priority = pqueasy.number2
                t_zimkateg.max_avail = pqueasy.number3


            do_it = True

        if do_it == False:

            zimkateg = db_session.query(Zimkateg).first()

            if not zimkateg:
                output_list = Output_list()
                output_list_data.append(output_list)

                output_list.success_flag = False
                output_list.msg_str = "Room type not found. Please create a room type first."

                return generate_output()
            else:
                output_list = Output_list()
                output_list_data.append(output_list)

                output_list.success_flag = False
                output_list.msg_str = "Room type not found. Please search with other criteria."

    return generate_output()