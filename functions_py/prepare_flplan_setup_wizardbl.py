#using conversion tools version: 1.0.0.117

# ==========================================
# Rulita, 09-10-2025
# Tiket ID : 8CF423 | Recompile Program
# ==========================================

from functions.additional_functions import *
from decimal import Decimal
from models import Queasy

input_list_data, Input_list = create_model("Input_list", {"floor":int})

def prepare_flplan_setup_wizardbl(input_list_data:[Input_list]):

    prepare_cache ([Queasy])

    floor_list_data = []
    t_queasy_data = []
    output_list_data = []
    is_setup:bool = False
    queasy = None

    input_list = floor_list = t_queasy = output_list = buff_queasy = None

    floor_list_data, Floor_list = create_model("Floor_list", {"id":int, "char1":string, "issetup":bool})
    t_queasy_data, T_queasy = create_model("T_queasy", {"key":int, "number1":int, "number2":int, "deci1":Decimal, "char1":string, "char2":string, "logi1":bool})
    output_list_data, Output_list = create_model("Output_list", {"success_flag":bool, "msg_str":string})

    Buff_queasy = create_buffer("Buff_queasy",Queasy)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal floor_list_data, t_queasy_data, output_list_data, is_setup, queasy
        nonlocal buff_queasy


        nonlocal input_list, floor_list, t_queasy, output_list, buff_queasy
        nonlocal floor_list_data, t_queasy_data, output_list_data

        return {"floor-list": floor_list_data, "t-queasy": t_queasy_data, "output-list": output_list_data}

    def read_section():

        nonlocal floor_list_data, t_queasy_data, output_list_data, is_setup, queasy
        nonlocal buff_queasy


        nonlocal input_list, floor_list, t_queasy, output_list, buff_queasy
        nonlocal floor_list_data, t_queasy_data, output_list_data

        queasy = get_cache (Queasy, {"key": [(eq, 357)],"number1": [(eq, 3)],"deci1": [(eq, 3.5)],"char1": [(eq, "room setup")],"char2": [(eq, "floor plan")],"logi1": [(eq, True)]})

        if queasy:
            queasy = Queasy()
            db_session.add(queasy)

            t_queasy.key = queasy.key
            t_queasy.number1 = queasy.number1
            t_queasy.number2 = queasy.number2
            t_queasy.deci1 =  to_decimal(queasy.deci1)
            t_queasy.char1 = queasy.char1
            t_queasy.char2 = queasy.char2
            t_queasy.logi1 = queasy.logi1

    input_list = query(input_list_data, first=True)

    if not input_list:
        output_list = Output_list()
        output_list_data.append(output_list)

        output_list.success_flag = False
        output_list.msg_str = "Error loading.. please contact our Customer Service"

        return generate_output()
    read_section()

    if input_list.floor != 0:

        queasy = get_cache (Queasy, {"key": [(eq, 25)],"number2": [(eq, input_list.floor)],"betriebsnr": [(eq, input_list.floor)]})

        if queasy:
            floor_list = Floor_list()
            floor_list_data.append(floor_list)

            floor_list.id = queasy.number2
            floor_list.char1 = "Floor " + to_string(queasy.number2)
            floor_list.issetup = queasy.logi1

            output_list = query(output_list_data, first=True)

            if not output_list:
                output_list = Output_list()
                output_list_data.append(output_list)

                output_list.success_flag = True
                output_list.msg_str = "Get specific floor successfully "


        else:

            queasy = get_cache (Queasy, {"key": [(eq, 25)],"number2": [(eq, input_list.floor)],"betriebsnr": [(eq, 0)]})

            if queasy:
                floor_list = Floor_list()
                floor_list_data.append(floor_list)

                floor_list.id = queasy.number2
                floor_list.char1 = "Floor " + to_string(queasy.number2)
                floor_list.issetup = queasy.logi1

                output_list = query(output_list_data, first=True)

                if not output_list:
                    output_list = Output_list()
                    output_list_data.append(output_list)

                    output_list.success_flag = True
                    output_list.msg_str = "Get specific floor successfully "


    else:

        for queasy in db_session.query(Queasy).filter(
                 (Queasy.key == 25) & (Queasy.char1 != "") & (Queasy.betriebsnr != 0)).order_by(Queasy.number2).all():

            floor_list = query(floor_list_data, filters=(lambda floor_list: floor_list.id == queasy.number2 and queasy.number2 != 0), first=True)

            if not floor_list:

                if queasy.betriebsnr == queasy.number2:
                    floor_list = Floor_list()
                    floor_list_data.append(floor_list)

                    floor_list.id = queasy.number2
                    floor_list.char1 = "Floor " + to_string(queasy.number2)
                    floor_list.issetup = queasy.logi1

            output_list = query(output_list_data, first=True)

            if not output_list:
                output_list = Output_list()
                output_list_data.append(output_list)

                output_list.success_flag = True
                output_list.msg_str = "Get ALL floor successfully "

        for queasy in db_session.query(Queasy).filter(
                 (Queasy.key == 25) & (Queasy.char1 != "") & (Queasy.betriebsnr == 0)).order_by(Queasy.number2).all():

            floor_list = query(floor_list_data, filters=(lambda floor_list: floor_list.id == queasy.number2 and queasy.number2 != 0), first=True)

            if not floor_list:

                if queasy.betriebsnr == queasy.number2:
                    floor_list = Floor_list()
                    floor_list_data.append(floor_list)

                    floor_list.id = queasy.number2
                    floor_list.char1 = "Floor " + to_string(queasy.number2)
                    floor_list.issetup = queasy.logi1


                else:
                    floor_list = Floor_list()
                    floor_list_data.append(floor_list)

                    floor_list.id = queasy.number2
                    floor_list.char1 = "Floor " + to_string(queasy.number2)
                    floor_list.issetup = queasy.logi1

            output_list = query(output_list_data, first=True)

            if not output_list:
                output_list = Output_list()
                output_list_data.append(output_list)

                output_list.success_flag = True
                output_list.msg_str = "Get ALL floor successfully "

    return generate_output()