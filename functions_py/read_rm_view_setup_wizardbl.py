#using conversion tools version: 1.0.0.117

# ==========================================
# Rulita, 09-10-2025
# Tiket ID : 8CF423 | Recompile Program
# ==========================================

from functions.additional_functions import *
from decimal import Decimal
from sqlalchemy import func
from models import Paramtext

input_param_data, Input_param = create_model("Input_param", {"case_type":int, "p_txtnr":int, "ptexte":string})

def read_rm_view_setup_wizardbl(input_param_data:[Input_param]):

    prepare_cache ([Paramtext])

    t_paramtext_data = []
    output_list_data = []
    do_it:bool = False
    paramtext = None

    input_param = t_paramtext = output_list = None

    t_paramtext_data, T_paramtext = create_model("T_paramtext", {"sprachcode":int, "ptexte":string})
    output_list_data, Output_list = create_model("Output_list", {"success_flag":bool, "msg_str":string})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal t_paramtext_data, output_list_data, do_it, paramtext


        nonlocal input_param, t_paramtext, output_list
        nonlocal t_paramtext_data, output_list_data

        return {"t-paramtext": t_paramtext_data, "output-list": output_list_data}

    input_param = query(input_param_data, first=True)

    if not input_param:
        output_list = Output_list()
        output_list_data.append(output_list)

        output_list.success_flag = False
        output_list.msg_str = "Error loading.. please contact our Customer Service"

        return generate_output()

    if input_param.case_type == 1:

        if input_param.ptexte != " ":

            for paramtext in db_session.query(Paramtext).filter(
                     (Paramtext.txtnr == input_param.p_txtnr) & (matches(Paramtext.ptexte,"*" + input_param.ptexte + "*"))).order_by(Paramtext.sprachcode).all():
                t_paramtext = T_paramtext()
                t_paramtext_data.append(t_paramtext)

                t_paramtext.sprachcode = paramtext.sprachcode
                t_paramtext.ptexte = paramtext.ptexte


                do_it = True

            if do_it :
                output_list = Output_list()
                output_list_data.append(output_list)

                output_list.success_flag = True
                output_list.msg_str = "Room view setup found."


            else:

                paramtext = get_cache (Paramtext, {"txtnr": [(eq, input_param.p_txtnr)]})

                if not paramtext:
                    output_list = Output_list()
                    output_list_data.append(output_list)

                    output_list.success_flag = False
                    output_list.msg_str = "Room view setup not found. Please create room view type first."


                else:
                    output_list = Output_list()
                    output_list_data.append(output_list)

                    output_list.success_flag = False
                    output_list.msg_str = "Room view setup not found. Please search with other criteria."


        else:

            for paramtext in db_session.query(Paramtext).filter(
                     (Paramtext.txtnr == input_param.p_txtnr) & (Paramtext.ptexte != "")).order_by(Paramtext.sprachcode).all():
                t_paramtext = T_paramtext()
                t_paramtext_data.append(t_paramtext)

                t_paramtext.sprachcode = paramtext.sprachcode
                t_paramtext.ptexte = paramtext.ptexte


                do_it = True

            if do_it :
                output_list = Output_list()
                output_list_data.append(output_list)

                output_list.success_flag = True
                output_list.msg_str = "Room view setup found."


            else:
                output_list = Output_list()
                output_list_data.append(output_list)

                output_list.success_flag = False
                output_list.msg_str = "Room view setup not found. Please create room view type first."

    return generate_output()