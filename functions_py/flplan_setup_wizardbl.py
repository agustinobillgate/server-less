#using conversion tools version: 1.0.0.117

# ==========================================
# Rulita, 09-10-2025
# Tiket ID : 8CF423 | Recompile Program
# ==========================================

from functions.additional_functions import *
from decimal import Decimal
from models import Queasy

input_list_data, Input_list = create_model("Input_list", {"floor":int})

def flplan_setup_wizardbl(input_list_data:[Input_list]):

    prepare_cache ([Queasy])

    queasy_list_data = []
    output_list_data = []
    do_it:bool = False
    queasy = None

    input_list = queasy_list = output_list = None

    queasy_list_data, Queasy_list = create_model("Queasy_list", {"char1":string, "deci1":Decimal, "deci2":Decimal, "key":int, "number2":int})
    output_list_data, Output_list = create_model("Output_list", {"success_flag":bool, "msg_str":string})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal queasy_list_data, output_list_data, do_it, queasy


        nonlocal input_list, queasy_list, output_list
        nonlocal queasy_list_data, output_list_data

        return {"queasy-list": queasy_list_data, "output-list": output_list_data}

    input_list = query(input_list_data, first=True)

    if not input_list:
        output_list = Output_list()
        output_list_data.append(output_list)

        output_list.success_flag = False
        output_list.msg_str = "Error loading.. please contact our Customer Service"

        return generate_output()

    for queasy in db_session.query(Queasy).filter(
             (Queasy.key == 25) & (Queasy.number2 == input_list.floor)).order_by(Queasy.char1).all():
        queasy_list = Queasy_list()
        queasy_list_data.append(queasy_list)

        queasy_list.char1 = queasy.char1
        queasy_list.deci1 =  to_decimal(queasy.deci1)
        queasy_list.deci2 =  to_decimal(queasy.deci2)
        queasy_list.key = queasy.key
        queasy_list.number2 = queasy.number2

        output_list = query(output_list_data, first=True)

        if not output_list:
            output_list = Output_list()
            output_list_data.append(output_list)

            output_list.success_flag = True
            output_list.msg = "get room of floor " + to_string(input_list.floor) + " successfully"

    return generate_output()