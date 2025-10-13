#using conversion tools version: 1.0.0.117

# ==========================================
# Rulita, 10-10-2025
# Tiket ID : 8CF423 | Recompile Program
# ==========================================

from functions.additional_functions import *
from decimal import Decimal
from models import Queasy

t_input_list_data, T_input_list = create_model("T_input_list", {"user_initial":string})

def prepare_dashboard_setup_wizardbl(t_input_list_data:[T_input_list]):
    t_dashboard_list_data = []
    t_data_list_data = []
    total_step:int = 0
    total_step_finished:int = 0
    total_percent:Decimal = to_decimal("0.0")
    queasy = None

    t_dashboard_list = t_list = t_queasy = t_data_list = t_input_list = None

    t_dashboard_list_data, T_dashboard_list = create_model("T_dashboard_list", {"vkey":int, "section_number":int, "subsection_number":Decimal, "sub_subsection_number":Decimal, "section_name":string, "subsection_name":string, "sub_subsection_name":string, "finish_flag":bool})
    t_list_data, T_list = create_model("T_list", {"vkey":int, "section_number":int, "subsection_number":Decimal, "sub_subsection_number":Decimal, "section_name":string, "subsection_name":string, "sub_subsection_name":string, "finish_flag":bool})
    t_queasy_data, T_queasy = create_model_like(Queasy)
    t_data_list_data, T_data_list = create_model("T_data_list", {"continue_flag":bool, "percentage_progress":Decimal})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal t_dashboard_list_data, t_data_list_data, total_step, total_step_finished, total_percent, queasy


        nonlocal t_dashboard_list, t_list, t_queasy, t_data_list, t_input_list
        nonlocal t_dashboard_list_data, t_list_data, t_queasy_data, t_data_list_data

        return {"t-dashboard-list": t_dashboard_list_data, "t-data-list": t_data_list_data}


    t_data_list = T_data_list()
    t_data_list_data.append(t_data_list)


    queasy = get_cache (Queasy, {"key": [(eq, 357)]})

    if queasy:
        t_data_list.continue_flag = True
    else:
        t_data_list.continue_flag = False

        return generate_output()

    for queasy in db_session.query(Queasy).filter(
             (Queasy.key == 357) & (Queasy.number2 == 0)).order_by(Queasy.number1, Queasy.deci1).all():
        t_queasy = T_queasy()
        t_queasy_data.append(t_queasy)

        buffer_copy(queasy, t_queasy)
        t_dashboard_list = T_dashboard_list()
        t_dashboard_list_data.append(t_dashboard_list)

        t_dashboard_list.vkey = 357
        t_dashboard_list.section_number = queasy.number1
        t_dashboard_list.subsection_number =  to_decimal(queasy.deci1)
        t_dashboard_list.section_name = queasy.char1
        t_dashboard_list.subsection_name = queasy.char2
        t_dashboard_list.finish_flag = queasy.logi1

        if queasy.logi1:
            total_step_finished = total_step_finished + 1

    for t_queasy in query(t_queasy_data, filters=(lambda t_queasy: t_queasy.key == 357), sort_by=[("number1",True),("deci1",True)]):

        if t_queasy.number1 == 1:
            t_dashboard_list = T_dashboard_list()
            t_dashboard_list_data.append(t_dashboard_list)

            t_dashboard_list.vkey = 357
            t_dashboard_list.section_number = 2
            t_dashboard_list.subsection_number =  to_decimal("0")
            t_dashboard_list.section_name = "OUTLET"
            t_dashboard_list.subsection_name = ""
            t_dashboard_list.finish_flag = False

        elif t_queasy.number1 == 2 and t_queasy.number2 == 0:
            t_dashboard_list = T_dashboard_list()
            t_dashboard_list_data.append(t_dashboard_list)

            t_dashboard_list.vkey = 357
            t_dashboard_list.section_number = 3
            t_dashboard_list.subsection_number =  to_decimal(3.1)
            t_dashboard_list.section_name = "ROOM"
            t_dashboard_list.subsection_name = "ROOM TYPE"
            t_dashboard_list.finish_flag = False

        elif t_queasy.number1 == 3 and t_queasy.deci1 == 3.1:
            t_dashboard_list = T_dashboard_list()
            t_dashboard_list_data.append(t_dashboard_list)

            t_dashboard_list.vkey = 357
            t_dashboard_list.section_number = 3
            t_dashboard_list.subsection_number =  to_decimal(3.2)
            t_dashboard_list.section_name = "ROOM"
            t_dashboard_list.subsection_name = "BED SETUP"
            t_dashboard_list.finish_flag = False

        elif t_queasy.number1 == 3 and t_queasy.deci1 == 3.2:
            t_dashboard_list = T_dashboard_list()
            t_dashboard_list_data.append(t_dashboard_list)

            t_dashboard_list.vkey = 357
            t_dashboard_list.section_number = 3
            t_dashboard_list.subsection_number =  to_decimal(3.3)
            t_dashboard_list.section_name = "ROOM"
            t_dashboard_list.subsection_name = "ROOM VIEW"
            t_dashboard_list.finish_flag = False

        elif t_queasy.number1 == 3 and t_queasy.deci1 == 3.3:
            t_dashboard_list = T_dashboard_list()
            t_dashboard_list_data.append(t_dashboard_list)

            t_dashboard_list.vkey = 357
            t_dashboard_list.section_number = 3
            t_dashboard_list.subsection_number =  to_decimal(3.4)
            t_dashboard_list.section_name = "ROOM"
            t_dashboard_list.subsection_name = "ROOM SETUP"
            t_dashboard_list.finish_flag = False

        elif t_queasy.number1 == 3 and t_queasy.deci1 == 3.4:
            t_dashboard_list = T_dashboard_list()
            t_dashboard_list_data.append(t_dashboard_list)

            t_dashboard_list.vkey = 357
            t_dashboard_list.section_number = 3
            t_dashboard_list.subsection_number =  to_decimal(3.5)
            t_dashboard_list.section_name = "ROOM"
            t_dashboard_list.subsection_name = "FLOOR PLAN"
            t_dashboard_list.finish_flag = False

        elif t_queasy.number1 == 3 and t_queasy.deci1 == 3.5:
            t_dashboard_list = T_dashboard_list()
            t_dashboard_list_data.append(t_dashboard_list)

            t_dashboard_list.vkey = 357
            t_dashboard_list.section_number = 4
            t_dashboard_list.subsection_number =  to_decimal("0")
            t_dashboard_list.section_name = "USER"
            t_dashboard_list.subsection_name = ""
            t_dashboard_list.finish_flag = False


        break
    total_step = 9
    total_percent = ( to_decimal(total_step_finished) / to_decimal(total_step)) * to_decimal("100")
    t_data_list.percentage_progress = to_decimal(round(total_percent , 2))

    return generate_output()