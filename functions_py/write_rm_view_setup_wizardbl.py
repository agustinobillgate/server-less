#using conversion tools version: 1.0.0.117

# =======================================
# Rulita, 09-10-2025
# Tiket ID : 8CF423 | Recompile program
# =======================================

from functions.additional_functions import *
from decimal import Decimal
from models import Paramtext, Queasy

t_paramtext_data, T_paramtext = create_model("T_paramtext", {"sprachcode":int, "ptexte":string, "case_type":int, "txtnr":int})

def write_rm_view_setup_wizardbl(t_paramtext_data:[T_paramtext]):

    prepare_cache ([Paramtext, Queasy])

    output_param_data = []
    counter:int = 0
    do_it:bool = False
    is_same:bool = False
    paramtext = queasy = None

    t_paramtext = output_param = None

    output_param_data, Output_param = create_model("Output_param", {"success_flag":bool, "msg_str":string})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal output_param_data, counter, do_it, is_same, paramtext, queasy


        nonlocal t_paramtext, output_param
        nonlocal output_param_data

        return {"output-param": output_param_data}

    def create_section():

        nonlocal output_param_data, counter, do_it, is_same, paramtext, queasy


        nonlocal t_paramtext, output_param
        nonlocal output_param_data

        queasy = get_cache (Queasy, {"key": [(eq, 357)],"number1": [(eq, 3)],"deci1": [(eq, 3.3)],"char1": [(eq, "room setup")],"char2": [(eq, "room view")],"logi1": [(eq, True)]})

        if not queasy:
            queasy = Queasy()
            db_session.add(queasy)

            queasy.key = 357
            queasy.number1 = 3
            queasy.deci1 =  to_decimal(3.3)
            queasy.char1 = "ROOM SETUP"
            queasy.char2 = "ROOM VIEW"
            queasy.logi1 = True

    t_paramtext = query(t_paramtext_data, first=True)

    if not t_paramtext:
        output_param = Output_param()
        output_param_data.append(output_param)

        output_param.success_flag = False
        output_param.msg_str = "Error loading.. please contact our Customer Service"

        return generate_output()

    if t_paramtext.case_type == 1:

        paramtext = db_session.query(Paramtext).filter(
                 (Paramtext.txtnr == t_paramtext.txtnr) & (trim(Paramtext.ptexte) == trim(t_paramtext.ptexte))).first()

        if paramtext:
            output_param = Output_param()
            output_param_data.append(output_param)

            output_param.success_flag = False
            output_param.msg_str = "Room view name already exist"

            return generate_output()

        paramtext = get_cache (Paramtext, {"txtnr": [(eq, t_paramtext.txtnr)],"sprachcode": [(eq, t_paramtext.sprachcode)]})

        if paramtext:
            paramtext.ptexte = t_paramtext.ptexte


            do_it = True
            pass
            pass

        if do_it :
            output_param = Output_param()
            output_param_data.append(output_param)

            output_param.success_flag = True
            output_param.msg_str = "Update room view successfully."


        else:
            output_param = Output_param()
            output_param_data.append(output_param)

            output_param.success_flag = False
            output_param.msg_str = "Room view not found. Please modify another room view"


    elif t_paramtext.case_type == 2:

        for t_paramtext in query(t_paramtext_data):

            for paramtext in db_session.query(Paramtext).filter(
                     (Paramtext.txtnr == 230)).order_by(Paramtext.sprachcode.desc()).all():
                counter = paramtext.sprachcode + 1
                break

            for paramtext in db_session.query(Paramtext).filter(
                     (Paramtext.txtnr == 230)).order_by(Paramtext._recid).all():

                if trim(paramtext.ptexte) == trim(t_paramtext.ptexte):
                    output_param = Output_param()
                    output_param_data.append(output_param)

                    output_param.success_flag = False
                    output_param.msg_str = "Room view code [" + to_string(counter) + " " + to_string(t_paramtext.ptexte) + "] already exists. Please change the room view code or Create again."


                    is_same = True
                    break

            if is_same:
                break

            paramtext = get_cache (Paramtext, {"txtnr": [(eq, 230)],"sprachcode": [(eq, counter)]})

            if not paramtext:
                paramtext = Paramtext()
                db_session.add(paramtext)

                paramtext.sprachcode = counter
                paramtext.ptexte = t_paramtext.ptexte
                paramtext.txtnr = t_paramtext.txtnr


                output_param = Output_param()
                output_param_data.append(output_param)

                output_param.success_flag = True
                output_param.msg_str = "Create room view " + to_string(counter) + " " + to_string(t_paramtext.ptexte) + " successfully."


            else:
                output_param = Output_param()
                output_param_data.append(output_param)

                output_param.success_flag = False
                output_param.msg_str = "Room view code [" + to_string(counter) + " " + to_string(t_paramtext.ptexte) + "] already exists. Please change the room view code or Create again."


    elif t_paramtext.case_type == 3:
        create_section()
        output_param = Output_param()
        output_param_data.append(output_param)

        output_param.success_flag = True
        output_param.msg_str = "Create section for room view successfully."

    return generate_output()