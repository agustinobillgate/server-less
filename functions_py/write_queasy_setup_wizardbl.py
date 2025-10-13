#using conversion tools version: 1.0.0.117

# =======================================
# Rulita, 09-10-2025
# Tiket ID : 8CF423 | Recompile program
# =======================================

from functions.additional_functions import *
from decimal import Decimal
from models import Queasy

input_list_data, Input_list = create_model("Input_list", {"case_type":int, "floor":int})
input_queasy_data, Input_queasy = create_model("Input_queasy", {"char1":string, "deci1":int, "deci2":int, "key":int, "number2":int})

def write_queasy_setup_wizardbl(input_list_data:[Input_list], input_queasy_data:[Input_queasy]):

    prepare_cache ([Queasy])

    output_queasy_data = []
    output_list_data = []
    do_it:bool = False
    queasy = None

    input_list = input_queasy = output_queasy = output_list = None

    output_queasy_data, Output_queasy = create_model("Output_queasy", {"char1":string, "deci1":int, "deci2":int, "key":int, "number2":int})
    output_list_data, Output_list = create_model("Output_list", {"success_flag":bool, "msg_str":string})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal output_queasy_data, output_list_data, do_it, queasy


        nonlocal input_list, input_queasy, output_queasy, output_list
        nonlocal output_queasy_data, output_list_data

        return {"output-queasy": output_queasy_data, "output-list": output_list_data}

    def create_sub_section():

        nonlocal output_queasy_data, output_list_data, do_it, queasy


        nonlocal input_list, input_queasy, output_queasy, output_list
        nonlocal output_queasy_data, output_list_data

        queasy = get_cache (Queasy, {"key": [(eq, 357)],"number1": [(eq, 3)],"deci1": [(eq, 3.5)],"char1": [(eq, "room setup")],"char2": [(eq, "floor plan")],"logi1": [(eq, True)]})

        if not queasy:
            queasy = Queasy()
            db_session.add(queasy)

            queasy.key = 357
            queasy.number1 = 3
            queasy.number2 = queasy.number2 + 1
            queasy.deci1 =  to_decimal(3.5)
            queasy.char1 = "ROOM SETUP"
            queasy.char2 = "FLOOR PLAN"
            queasy.logi1 = True


        else:
            pass
            queasy.key = 357
            queasy.number1 = 3
            queasy.number2 = queasy.number2 + 1
            queasy.deci1 =  to_decimal(3.5)
            queasy.char1 = "ROOM SETUP"
            queasy.char2 = "FLOOR PLAN"
            queasy.logi1 = True


            pass
            pass


    def create_section():

        nonlocal output_queasy_data, output_list_data, do_it, queasy


        nonlocal input_list, input_queasy, output_queasy, output_list
        nonlocal output_queasy_data, output_list_data

        queasy = get_cache (Queasy, {"key": [(eq, 357)],"number1": [(eq, 3)],"number2": [(eq, 0)],"deci1": [(eq, 3.5)],"char1": [(eq, "room setup")],"char2": [(eq, "floor plan")],"logi1": [(eq, True)]})

        if not queasy:
            queasy = Queasy()
            db_session.add(queasy)

            queasy.key = 357
            queasy.number1 = 3
            queasy.number2 = 0
            queasy.deci1 =  to_decimal(3.5)
            queasy.char1 = "ROOM SETUP"
            queasy.char2 = "FLOOR PLAN"
            queasy.logi1 = True


            output_list = Output_list()
            output_list_data.append(output_list)

            output_list.success_flag = True
            output_list.msg_str = "Create section from floor plan successfully"


        else:
            output_list = Output_list()
            output_list_data.append(output_list)

            output_list.success_flag = True
            output_list.msg_str = "Create section from floor plan successfully"


    def configure_floor():

        nonlocal output_queasy_data, output_list_data, do_it, queasy


        nonlocal input_list, input_queasy, output_queasy, output_list
        nonlocal output_queasy_data, output_list_data

        is_configured:bool = False

        for input_queasy in query(input_queasy_data):

            for queasy in db_session.query(Queasy).filter(
                     (Queasy.key == input_queasy.key) & (Queasy.number2 == input_queasy.number2)).order_by(Queasy._recid).all():

                if queasy.betriebsnr == input_queasy.number2:
                    is_configured = True
                    break

            if is_configured:
                output_list = Output_list()
                output_list_data.append(output_list)

                output_list.success_flag = True
                output_list.msg_str = "Floor " + to_string(input_queasy.number2) + " configured successfully"


                break
            else:

                queasy = get_cache (Queasy, {"key": [(eq, input_queasy.key)],"number2": [(eq, input_queasy.number2)]})

                if queasy:
                    pass
                    queasy.logi1 = True
                    queasy.betriebsnr = input_queasy.number2


                    pass
                    pass
                    is_configured = True

            if is_configured:
                output_list = Output_list()
                output_list_data.append(output_list)

                output_list.success_flag = True
                output_list.msg_str = "Floor " + to_string(input_queasy.number2) + " configured successfully"


                break

    input_list = query(input_list_data, first=True)

    if not input_list:
        output_list = Output_list()
        output_list_data.append(output_list)

        output_list.success_flag = False
        output_list.msg_str = "Error loading.. please contact our Customer Service"

        return generate_output()
    else:

        input_queasy = query(input_queasy_data, first=True)

        if not input_queasy:

            queasy = get_cache (Queasy, {"key": [(eq, 25)],"number2": [(eq, input_list.floor)],"betriebsnr": [(eq, input_list.floor)]})

            if queasy:
                output_list = Output_list()
                output_list_data.append(output_list)

                output_list.success_flag = True
                output_list.msg_str = "No change to floor plan"

                return generate_output()

    input_queasy = query(input_queasy_data, first=True)

    if not input_queasy:
        output_list = Output_list()
        output_list_data.append(output_list)

        output_list.success_flag = False
        output_list.msg_str = "Error loading.. please contact our Customer Service"

        return generate_output()

    if input_list.case_type == 1:

        for input_queasy in query(input_queasy_data):

            queasy = get_cache (Queasy, {"key": [(eq, input_queasy.key)],"number2": [(eq, input_queasy.number2)],"char1": [(eq, input_queasy.char1)]})

            if queasy:
                pass
                queasy.deci1 =  to_decimal(input_queasy.deci1)
                queasy.deci2 =  to_decimal(input_queasy.deci2)


                do_it = True

                output_queasy = query(output_queasy_data, filters=(lambda output_queasy: output_queasy.key == queasy.key and output_queasy.number2 == queasy.number2 and output_queasy.char1 == queasy.char1 and (output_queasy.deci1 != queasy.deci1 or output_queasy.deci2 != queasy.deci2)), first=True)

                if not output_queasy:
                    output_queasy = Output_queasy()
                    output_queasy_data.append(output_queasy)

                    output_queasy.key = queasy.key
                    output_queasy.number2 = queasy.number2
                    output_queasy.char1 = queasy.char1
                    output_queasy.deci1 = queasy.deci1
                    output_queasy.deci2 = queasy.deci2


                pass
                pass
            else:
                do_it = False
                break

        if do_it :
            output_list = Output_list()
            output_list_data.append(output_list)

            output_list.success_flag = True
            output_list.msg_str = "Create floor plan successfully"


            create_sub_section()
            configure_floor()
        else:
            output_list = Output_list()
            output_list_data.append(output_list)

            output_list.success_flag = False
            output_list.msg_str = "Error create floor plan of room number " + input_queasy.char1 + " is not defined in queasy table"


    elif input_list.case_type == 2:
        create_section()

    return generate_output()