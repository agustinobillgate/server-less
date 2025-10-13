#using conversion tools version: 1.0.0.117

# ============================================================
# Rulita, 09-10-2025
# Tiket ID : 8CF423 | Recompile Program
# Issue fixing {"txtnr": [(eq, (zimmer.setup + bed_default))]}
# ============================================================

from functions.additional_functions import *
from decimal import Decimal
from models import Paramtext, Zimmer, Htparam

input_list_data, Input_list = create_model("Input_list", {"zinr":string, "zikatnr":int})

def prepare_room_admin_setup_wizardbl(input_list_data:[Input_list]):

    prepare_cache ([Paramtext, Zimmer, Htparam])

    output_zimmer_data = []
    output_limit_data = []
    output_list_data = []
    do_it:bool = False
    room_limit:int = 0
    curr_anz:int = 0
    bed_default:int = 9200
    paramtext = zimmer = htparam = None

    input_list = output_zimmer = output_limit = output_list = bf_paramtext = None

    output_zimmer_data, Output_zimmer = create_model("Output_zimmer", {"zinr":string, "view_type":string, "bed_type":string, "etage":int, "bed_type_code":string, "view_type_code":int, "bed_type_txtnr":int})
    output_limit_data, Output_limit = create_model("Output_limit", {"room_limit":int, "curr_anz":int})
    output_list_data, Output_list = create_model("Output_list", {"success_flag":bool, "msg_str":string})

    Bf_paramtext = create_buffer("Bf_paramtext",Paramtext)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal output_zimmer_data, output_limit_data, output_list_data, do_it, room_limit, curr_anz, bed_default, paramtext, zimmer, htparam
        nonlocal bf_paramtext


        nonlocal input_list, output_zimmer, output_limit, output_list, bf_paramtext
        nonlocal output_zimmer_data, output_limit_data, output_list_data

        return {"output-zimmer": output_zimmer_data, "output-limit": output_limit_data, "output-list": output_list_data}

    def check_rm_limit():

        nonlocal output_zimmer_data, output_limit_data, output_list_data, do_it, room_limit, curr_anz, bed_default, paramtext, zimmer, htparam
        nonlocal bf_paramtext


        nonlocal input_list, output_zimmer, output_limit, output_list, bf_paramtext
        nonlocal output_zimmer_data, output_limit_data, output_list_data

        rbuff = None
        Rbuff =  create_buffer("Rbuff",Zimmer)

        htparam = get_cache (Htparam, {"paramnr": [(eq, 975)]})

        if htparam.finteger > 0:
            room_limit = htparam.finteger
        curr_anz = 0

        for rbuff in db_session.query(Rbuff).order_by(Rbuff._recid).all():
            curr_anz = curr_anz + 1

    input_list = query(input_list_data, first=True)

    if not input_list:
        output_list = Output_list()
        output_list_data.append(output_list)

        output_list.success_flag = True
        output_list.msg_str = "Error loading.. please contact our Customer Service"


    check_rm_limit()
    output_limit = Output_limit()
    output_limit_data.append(output_limit)

    output_limit.room_limit = room_limit
    output_limit.curr_anz = curr_anz

    if input_list.zinr == " " and input_list.zikatnr == 0:

        for zimmer in db_session.query(Zimmer).filter(
                 (Zimmer.sleeping)).order_by(Zimmer.zinr).all():
            output_zimmer = Output_zimmer()
            output_zimmer_data.append(output_zimmer)

            output_zimmer.zinr = zimmer.zinr
            output_zimmer.etage = zimmer.etage

            paramtext = get_cache (Paramtext, {"txtnr": [(eq, (zimmer.setup + bed_default))]})

            if paramtext:
                output_zimmer.bed_type = paramtext.ptexte
                output_zimmer.bed_type_code = paramtext.notes
                output_zimmer.bed_type_txtnr = paramtext.txtnr

            bf_paramtext = get_cache (Paramtext, {"txtnr": [(eq, 230)],"sprachcode": [(eq, zimmer.typ)]})

            if bf_paramtext:
                output_zimmer.view_type = bf_paramtext.ptexte
                output_zimmer.view_type_code = bf_paramtext.sprachcode


            do_it = True

        if do_it :
            output_list = Output_list()
            output_list_data.append(output_list)

            output_list.success_flag = True
            output_list.msg_str = "Room setup found."


        else:
            output_list = Output_list()
            output_list_data.append(output_list)

            output_list.success_flag = False
            output_list.msg_str = "Room setup not found. Please create room type first."

    elif input_list.zinr == " " and input_list.zikatnr != 0:

        for zimmer in db_session.query(Zimmer).filter(
                 (Zimmer.zikatnr == input_list.zikatnr) & (Zimmer.sleeping)).order_by(Zimmer.zinr).all():
            output_zimmer = Output_zimmer()
            output_zimmer_data.append(output_zimmer)

            output_zimmer.zinr = zimmer.zinr
            output_zimmer.etage = zimmer.etage

            paramtext = get_cache (Paramtext, {"txtnr": [(eq, (zimmer.setup + bed_default))]})

            if paramtext:
                output_zimmer.bed_type = paramtext.ptexte
                output_zimmer.bed_type_code = paramtext.notes
                output_zimmer.bed_type_txtnr = paramtext.txtnr

            bf_paramtext = get_cache (Paramtext, {"txtnr": [(eq, 230)],"sprachcode": [(eq, zimmer.typ)]})

            if bf_paramtext:
                output_zimmer.view_type = bf_paramtext.ptexte
                output_zimmer.view_type_code = bf_paramtext.sprachcode


            do_it = True
    else:

        for zimmer in db_session.query(Zimmer).filter(
                 (Zimmer.zinr == input_list.zinr)).order_by(Zimmer._recid).all():
            output_zimmer = Output_zimmer()
            output_zimmer_data.append(output_zimmer)

            output_zimmer.zinr = zimmer.zinr
            output_zimmer.etage = zimmer.etage

            paramtext = get_cache (Paramtext, {"txtnr": [(eq, (zimmer.setup + bed_default))]})

            if paramtext:
                output_zimmer.bed_type = paramtext.ptexte
                output_zimmer.bed_type_code = paramtext.notes
                output_zimmer.bed_type_txtnr = paramtext.txtnr

            bf_paramtext = get_cache (Paramtext, {"txtnr": [(eq, 230)],"sprachcode": [(eq, zimmer.typ)]})

            if bf_paramtext:
                output_zimmer.view_type = bf_paramtext.ptexte
                output_zimmer.view_type_code = bf_paramtext.sprachcode


            do_it = True

    if do_it :

        output_list = query(output_list_data, first=True)

        if not output_list:
            output_list = Output_list()
            output_list_data.append(output_list)

            output_list.success_flag = True
            output_list.msg_str = "Room setup found."


    else:

        zimmer = db_session.query(Zimmer).first()

        if not zimmer:
            output_list = Output_list()
            output_list_data.append(output_list)

            output_list.success_flag = False
            output_list.msg_str = "Room setup not found. Please create room type first."


        else:
            output_list = Output_list()
            output_list_data.append(output_list)

            output_list.success_flag = False
            output_list.msg_str = "Room setup not found. Please search another room number."

    return generate_output()