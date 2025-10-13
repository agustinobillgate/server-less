#using conversion tools version: 1.0.0.117

# ==========================================
# Rulita, 09-10-2025
# Tiket ID : 8CF423 | Recompile Program
# ==========================================

from functions.additional_functions import *
from decimal import Decimal
from sqlalchemy import func
from models import Paramtext

input_list_data, Input_list = create_model("Input_list", {"case_type":int, "int1":int, "int2":int, "int3":int, "char1":string})

def read_paramtext_setup_wizardbl(input_list_data:[Input_list]):

    prepare_cache ([Paramtext])

    t_paramtext_data = []
    output_list_data = []
    do_it:bool = False
    paramtext = None

    input_list = t_paramtext = output_list = None

    t_paramtext_data, T_paramtext = create_model("T_paramtext", {"txtnr":int, "notes":string, "ptexte":string})
    output_list_data, Output_list = create_model("Output_list", {"success_flag":bool, "msg_str":string})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal t_paramtext_data, output_list_data, do_it, paramtext


        nonlocal input_list, t_paramtext, output_list
        nonlocal t_paramtext_data, output_list_data

        return {"t-paramtext": t_paramtext_data, "output-list": output_list_data}

    def assign_it():

        nonlocal t_paramtext_data, output_list_data, do_it, paramtext


        nonlocal input_list, t_paramtext, output_list
        nonlocal t_paramtext_data, output_list_data


        t_paramtext = T_paramtext()
        t_paramtext_data.append(t_paramtext)

        t_paramtext.txtnr = paramtext.txtnr
        t_paramtext.ptexte = paramtext.ptexte
        t_paramtext.notes = paramtext.notes


    input_list = query(input_list_data, first=True)

    if not input_list:
        output_list = Output_list()
        output_list_data.append(output_list)

        output_list.success_flag = False
        output_list.msg_str = "Error loading.. please contact our Customer Service"

        return generate_output()

    if input_list.case_type == 1:

        if input_list.char1 == " ":

            for paramtext in db_session.query(Paramtext).filter(
                     (Paramtext.txtnr >= input_list.int1) & (Paramtext.txtnr <= input_list.int2)).order_by(Paramtext._recid).all():
                assign_it()
                do_it = True

            if do_it :

                output_list = query(output_list_data, first=True)

                if not output_list:
                    output_list = Output_list()
                    output_list_data.append(output_list)

                    output_list.success_flag = True
                    output_list.msg_str = "Bed setup found."


            else:
                output_list = Output_list()
                output_list_data.append(output_list)

                output_list.success_flag = False
                output_list.msg_str = "Bed setup not found. Please create bed type first."


        else:

            for paramtext in db_session.query(Paramtext).filter(
                     (Paramtext.txtnr >= input_list.int1) & (Paramtext.txtnr <= input_list.int2) & (matches(Paramtext.ptexte,"*" + input_list.char1 + "*"))).order_by(Paramtext._recid).all():
                do_it = True
                assign_it()

            if do_it :

                output_list = query(output_list_data, first=True)

                if not output_list:
                    output_list = Output_list()
                    output_list_data.append(output_list)

                    output_list.success_flag = True
                    output_list.msg_str = "Bed setup found."


            else:

                paramtext = get_cache (Paramtext, {"txtnr": [(ge, input_list.int1),(le, input_list.int2)]})

                if not paramtext:
                    output_list = Output_list()
                    output_list_data.append(output_list)

                    output_list.success_flag = False
                    output_list.msg_str = "Bed setup not found. Please create bed type first."


                else:
                    output_list = Output_list()
                    output_list_data.append(output_list)

                    output_list.success_flag = False
                    output_list.msg_str = "Bed setup not found. Please search with other criteria."

    return generate_output()