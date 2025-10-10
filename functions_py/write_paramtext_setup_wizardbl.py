#using conversion tools version: 1.0.0.117

# =======================================
# Rulita, 09-10-2025
# Tiket ID : 8CF423 | Recompile program
# =======================================

from functions.additional_functions import *
from decimal import Decimal
from models import Paramtext, Queasy

t_paramtext_data, T_paramtext = create_model("T_paramtext", {"txtnr":int, "notes":string, "ptexte":string, "case_type":int})

def write_paramtext_setup_wizardbl(t_paramtext_data:[T_paramtext]):

    prepare_cache ([Paramtext, Queasy])

    output_param_data = []
    counter:int = 0
    is_same:bool = False
    paramtext = queasy = None

    t_paramtext = output_param = bf_paramtext = None

    output_param_data, Output_param = create_model("Output_param", {"success_flag":bool, "msg_str":string})

    Bf_paramtext = create_buffer("Bf_paramtext",Paramtext)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal output_param_data, counter, is_same, paramtext, queasy
        nonlocal bf_paramtext


        nonlocal t_paramtext, output_param, bf_paramtext
        nonlocal output_param_data

        return {"output-param": output_param_data}

    def create_section():

        nonlocal output_param_data, counter, is_same, paramtext, queasy
        nonlocal bf_paramtext


        nonlocal t_paramtext, output_param, bf_paramtext
        nonlocal output_param_data

        queasy = get_cache (Queasy, {"key": [(eq, 357)],"number1": [(eq, 3)],"deci1": [(eq, 3.2)],"char1": [(eq, "room setup")],"char2": [(eq, "bed setup")],"logi1": [(eq, True)]})

        if not queasy:
            queasy = Queasy()
            db_session.add(queasy)

            queasy.key = 357
            queasy.number1 = 3
            queasy.deci1 =  to_decimal(3.2)
            queasy.char1 = "ROOM SETUP"
            queasy.char2 = "BED SETUP"
            queasy.logi1 = True

    t_paramtext = query(t_paramtext_data, first=True)

    if not t_paramtext:
        output_param = Output_param()
        output_param_data.append(output_param)

        output_param.success_flag = False
        output_param.msg_str = "Error loading.. please contact our Customer Service"

        return generate_output()

    if t_paramtext.case_type == 1:

        paramtext = get_cache (Paramtext, {"txtnr": [(eq, t_paramtext.txtnr)]})

        if paramtext:

            bf_paramtext = db_session.query(Bf_paramtext).filter(
                     (Bf_paramtext.txtnr >= 9200) & (Bf_paramtext.txtnr <= 9299) & ((Bf_paramtext.notes == t_paramtext.notes) | (Bf_paramtext.ptexte == t_paramtext.ptexte))).first()

            if bf_paramtext and bf_paramtext.txtnr != paramtext.txtnr:
                output_param = Output_param()
                output_param_data.append(output_param)

                output_param.success_flag = False
                output_param.msg_str = "Bed type code or bed type description " + to_string(t_paramtext.txtnr) + " - " + t_paramtext.ptexte + " already exist. Please change and Update again."


            else:
                pass
                paramtext.ptexte = t_paramtext.ptexte
                paramtext.notes = t_paramtext.notes


                pass
                pass
                output_param = Output_param()
                output_param_data.append(output_param)

                output_param.success_flag = True
                output_param.msg_str = "update bed successfully."


        else:
            output_param = Output_param()
            output_param_data.append(output_param)

            output_param.success_flag = False
            output_param.msg_str = "Bed type code or bed type description " + to_string(t_paramtext.txtnr) + " - " + t_paramtext.ptexte + " already exist. Please change and Update again."


    elif t_paramtext.case_type == 2:

        for t_paramtext in query(t_paramtext_data):

            for paramtext in db_session.query(Paramtext).filter(
                     (Paramtext.txtnr >= 9200) & (Paramtext.txtnr <= 9299)).order_by(Paramtext.txtnr.desc()).all():
                counter = paramtext.txtnr
                break

            for paramtext in db_session.query(Paramtext).filter(
                     (Paramtext.txtnr >= 9200) & (Paramtext.txtnr <= 9299)).order_by(Paramtext._recid).all():

                if trim(paramtext.ptexte) == trim(t_paramtext.ptexte) or trim(paramtext.notes) == trim(t_paramtext.notes):
                    output_param = Output_param()
                    output_param_data.append(output_param)

                    output_param.success_flag = False
                    output_param.msg_str = "Bed type number " + to_string(counter + 1) + " - " + t_paramtext.ptexte + " already exists. Please change and Create again."


                    is_same = True
                    break

            if is_same:
                break

            if counter == 0:
                counter = 9201

            paramtext = get_cache (Paramtext, {"txtnr": [(eq, (counter + 1))]})

            if not paramtext:

                bf_paramtext = db_session.query(Bf_paramtext).filter(
                         (paramtext.txtnr >= 9200) & (paramtext.txtnr <= 9299) & ((Bf_paramtext.ptexte == t_paramtext.ptexte) | (Bf_paramtext.notes == t_paramtext.notes))).first()

                if not bf_paramtext:
                    paramtext = Paramtext()
                    db_session.add(paramtext)

                    paramtext.txtnr = counter + 1
                    paramtext.ptexte = t_paramtext.ptexte
                    paramtext.notes = t_paramtext.notes


                    output_param = Output_param()
                    output_param_data.append(output_param)

                    output_param.success_flag = True
                    output_param.msg_str = "Create bed " + to_string(paramtext.txtnr) + " - " + paramtext.ptexte + " successfully."


                else:
                    output_param = Output_param()
                    output_param_data.append(output_param)

                    output_param.success_flag = False
                    output_param.msg_str = "bed type code or bed type description " + to_string(counter + 1) + " - " + t_paramtext.ptexte + " already exists. Please change and Create again."


            else:
                output_param = Output_param()
                output_param_data.append(output_param)

                output_param.success_flag = False
                output_param.msg_str = "Bed type number " + to_string(counter + 1) + " - " + t_paramtext.ptexte + " already exists. Please change and Create again."


    elif t_paramtext.case_type == 3:
        create_section()
        output_param = Output_param()
        output_param_data.append(output_param)

        output_param.success_flag = True
        output_param.msg_str = "create section for bed successfully."

    return generate_output()