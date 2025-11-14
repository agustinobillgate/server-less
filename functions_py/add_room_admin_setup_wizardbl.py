# using conversion tools version: 1.0.0.117

# =============================================
# Rulita, 09-10-2025
# Tiket ID : 8CF423 | Recompile Program
# Issue : Fixing "txtnr": [(eq, bed_default)]})

# yusufwijasena, 14-11-2025 (62BADE)
# - last update from Malik: Setup Wizard
# =============================================

from functions.additional_functions import *
from decimal import Decimal
from models import Paramtext, Zimmer, Queasy, Zimkateg, Res_line, Htparam

input_list_data, Input_list = create_model(
    "Input_list",
    {
        "case_type": int,
        "rmno": string,
        "rmcatbez": string,
        "user_init": string
    })
input_zimmer_data, Input_zimmer = create_model(
    "Input_zimmer",
    {
        "zinr": string,
        "view_type": int,
        "bed_type": int,
        "etage": int,
        "zikatnr": int,
        "prev_zinr": string,
        "prev_etage": int
    })


def add_room_admin_setup_wizardbl(input_list_data: list[Input_list], input_zimmer_data: list[Input_zimmer]):

    prepare_cache([Paramtext, Zimkateg, Htparam])

    output_zimmer_data = []
    output_list_data = []
    bed_default: int = 0
    floor_mode: string = ""
    room_limit: int = 0  # Malik: Setup Wizard
    curr_anz: int = 0  # Malik: Setup Wizard
    tot_list_rooms: int = 0  # Malik: Setup Wizard
    paramtext = zimmer = queasy = zimkateg = res_line = htparam = None

    input_list = input_zimmer = output_zimmer = output_list = bf_paramtext = bf_zimmer = bf_queasy = None

    output_zimmer_data, Output_zimmer = create_model(
        "Output_zimmer",
        {
            "zinr": string,
            "view_type": string,
            "bed_type": string,
            "etage": int,
            "zikatnr": int,
            "sleeping": bool
        })
    output_list_data, Output_list = create_model(
        "Output_list",
        {
            "success_flag": bool,
            "msg_str": string
        })

    Bf_paramtext = create_buffer("Bf_paramtext", Paramtext)
    Bf_zimmer = create_buffer("Bf_zimmer", Zimmer)
    Bf_queasy = create_buffer("Bf_queasy", Queasy)

    db_session = local_storage.db_session

    def generate_output():
        nonlocal output_zimmer_data, output_list_data, bed_default, floor_mode, room_limit, curr_anz, tot_list_rooms, paramtext, zimmer, queasy, zimkateg, res_line, htparam
        nonlocal bf_paramtext, bf_zimmer, bf_queasy
        nonlocal input_list, input_zimmer, output_zimmer, output_list, bf_paramtext, bf_zimmer, bf_queasy
        nonlocal output_zimmer_data, output_list_data

        return {
            "output-zimmer": output_zimmer_data,
            "output-list": output_list_data
        }

    def fill_zimmer_update():
        nonlocal output_zimmer_data, output_list_data, bed_default, floor_mode, room_limit, curr_anz, tot_list_rooms, paramtext, zimmer, queasy, zimkateg, res_line, htparam
        nonlocal bf_paramtext, bf_zimmer, bf_queasy
        nonlocal input_list, input_zimmer, output_zimmer, output_list, bf_paramtext, bf_zimmer, bf_queasy
        nonlocal output_zimmer_data, output_list_data

        zimmer.typ = input_zimmer.view_type
        zimmer.setup = input_zimmer.bed_type - 9200
        zimmer.etage = input_zimmer.etage
        zimmer.zikatnr = input_zimmer.zikatnr

        if zimmer.setup != input_zimmer.bed_type and zimmer.setup != 0:
            res_line = get_cache(
                Res_line, {"active_flag": [(eq, 1)], "zinr": [(eq, zimmer.zinr)]})
            while res_line is not None:
                res_line.setup = input_zimmer.bed_type

                curr_recid = res_line._recid
                res_line = db_session.query(Res_line).filter(
                    (Res_line.active_flag == 1) & (Res_line.zinr == zimmer.zinr) & (Res_line._recid > curr_recid)).first()

            res_line = get_cache(
                Res_line, {"active_flag": [(eq, 0)], "zinr": [(eq, zimmer.zinr)]})
            while res_line is not None:
                res_line.setup = input_zimmer.bed_type

                curr_recid = res_line._recid
                res_line = db_session.query(Res_line).filter(
                    (Res_line.active_flag == 0) & (Res_line.zinr == zimmer.zinr) & (Res_line._recid > curr_recid)).first()
        bed_default = 9200 + zimmer.setup
        output_zimmer = Output_zimmer()
        output_zimmer_data.append(output_zimmer)

        output_zimmer.zinr = zimmer.zinr
        output_zimmer.etage = zimmer.etage
        output_zimmer.zikatnr = zimmer.zikatnr
        output_zimmer.sleeping = zimmer.sleeping

        paramtext = get_cache(Paramtext, {"txtnr": [(eq, bed_default)]})

        if paramtext:
            output_zimmer.bed_type = paramtext.ptexte

        bf_paramtext = get_cache(
            Paramtext, {"txtnr": [(eq, 230)], "sprachcode": [(eq, zimmer.typ)]})

        if bf_paramtext:
            output_zimmer.view_type = paramtext.ptexte

    def create_section():
        nonlocal output_zimmer_data, output_list_data, bed_default, floor_mode, room_limit, curr_anz, tot_list_rooms, paramtext, zimmer, queasy, zimkateg, res_line, htparam
        nonlocal bf_paramtext, bf_zimmer, bf_queasy
        nonlocal input_list, input_zimmer, output_zimmer, output_list, bf_paramtext, bf_zimmer, bf_queasy
        nonlocal output_zimmer_data, output_list_data

        queasy = get_cache(
            Queasy, {"key": [(eq, 357)], "number1": [(eq, 3)], "deci1": [(eq, 3.4)], "char1": [(eq, "room setup")], "char2": [(eq, "room admin")], "logi1": [(eq, True)]})

        if not queasy:
            queasy = Queasy()
            db_session.add(queasy)

            queasy.key = 357
            queasy.number1 = 3
            queasy.deci1 = to_decimal(3.4)
            queasy.char1 = "ROOM SETUP"
            queasy.char2 = "ROOM ADMIN"
            queasy.logi1 = True

    def create_floor():
        nonlocal output_zimmer_data, output_list_data, bed_default, floor_mode, room_limit, curr_anz, tot_list_rooms, paramtext, zimmer, queasy, zimkateg, res_line, htparam
        nonlocal bf_paramtext, bf_zimmer, bf_queasy
        nonlocal input_list, input_zimmer, output_zimmer, output_list, bf_paramtext, bf_zimmer, bf_queasy
        nonlocal output_zimmer_data, output_list_data

        if floor_mode.lower() == "add":
            queasy = get_cache(
                Queasy, {"key": [(eq, 25)], "number2": [(eq, zimmer.etage)], "char1": [(eq, zimmer.zinr)]})

            if not queasy:
                queasy = Queasy()
                db_session.add(queasy)

                queasy.key = 25
                queasy.number2 = zimmer.etage
                queasy.char1 = zimmer.zinr
                queasy.number1 = 1

            queasy = get_cache(
                Queasy, {"key": [(eq, 25)], "number2": [(eq, zimmer.etage)], "betriebsnr": [(ne, 0)]})

            if queasy:
                queasy.betriebsnr = 0
                queasy.logi1 = False

        elif floor_mode.lower() == "chg":
            if input_zimmer.prev_etage != input_zimmer.etage:
                bf_queasy = db_session.query(Bf_queasy).filter(
                    (Bf_queasy.key == 25) & (Bf_queasy.number2 == input_zimmer.prev_etage) & (Bf_queasy.char1 == trim(input_zimmer.prev_zinr))).first()

                if bf_queasy:
                    db_session.delete(bf_queasy)

                queasy = get_cache(
                    Queasy, {"key": [(eq, 25)], "number2": [(eq, input_zimmer.prev_etage)], "betriebsnr": [(ne, 0)]})

                if queasy:
                    queasy.betriebsnr = 0
                    queasy.logi1 = False

                queasy = get_cache(
                    Queasy, {"key": [(eq, 25)], "number2": [(eq, input_zimmer.etage)], "betriebsnr": [(ne, 0)]})

                if queasy:
                    queasy.betriebsnr = 0
                    queasy.logi1 = False

                queasy = Queasy()
                db_session.add(queasy)

                queasy.key = 25
                queasy.number2 = input_zimmer.etage
                queasy.char1 = input_zimmer.zinr

        elif floor_mode.lower() == "modify/create":
            bf_queasy = db_session.query(Bf_queasy).filter(
                (Bf_queasy.key == 25) & (Bf_queasy.number2 == input_zimmer.prev_etage) & (Bf_queasy.char1 == trim(input_zimmer.prev_zinr))).first()

            if bf_queasy:
                db_session.delete(bf_queasy)

            queasy = get_cache(
                Queasy, {"key": [(eq, 25)], "number2": [(eq, input_zimmer.prev_etage)], "betriebsnr": [(ne, 0)]})

            if queasy:
                queasy.betriebsnr = 0
                queasy.logi1 = False

            queasy = get_cache(
                Queasy, {"key": [(eq, 25)], "number2": [(eq, input_zimmer.etage)], "betriebsnr": [(ne, 0)]})

            if queasy:
                queasy.betriebsnr = 0
                queasy.logi1 = False

            queasy = Queasy()
            db_session.add(queasy)

            queasy.key = 25
            queasy.number2 = zimmer.etage
            queasy.char1 = zimmer.zinr
            queasy.number1 = 1
    # Malik: Setup Wizard
    def check_rm_limit():
        nonlocal output_zimmer_data, output_list_data, bed_default, floor_mode, room_limit, curr_anz, tot_list_rooms, paramtext, zimmer, queasy, zimkateg, res_line, htparam
        nonlocal bf_paramtext, bf_zimmer, bf_queasy
        nonlocal input_list, input_zimmer, output_zimmer, output_list, bf_paramtext, bf_zimmer, bf_queasy
        nonlocal output_zimmer_data, output_list_data

        rbuff = None
        Rbuff = create_buffer("Rbuff", Zimmer)

        htparam = get_cache(Htparam, {"paramnr": [(eq, 975)]})

        if htparam.finteger > 0:
            room_limit = htparam.finteger
        curr_anz = 0

        for rbuff in db_session.query(Rbuff).order_by(Rbuff._recid).all():
            curr_anz = curr_anz + 1

        for input_zimmer in query(input_zimmer_data):
            tot_list_rooms = tot_list_rooms + 1
    # end Malik: Setup Wizard

    input_list = query(input_list_data, first=True)

    if not input_list:
        output_list = Output_list()
        output_list_data.append(output_list)

        output_list.success_flag = False
        output_list.msg_str = "Error loading.. please contact our Customer Service"

        return generate_output()

    input_zimmer = query(input_zimmer_data, first=True)

    if not input_zimmer:
        output_list = Output_list()
        output_list_data.append(output_list)

        output_list.success_flag = False
        output_list.msg_str = "Error loading zimmer.. please contact our Customer Service"

        return generate_output()

    if input_list.case_type == 1:
        # Malik: Setup Wizard
        check_rm_limit()

        if (room_limit - curr_anz) < tot_list_rooms:
            output_list = Output_list()
            output_list_data.append(output_list)

            output_list.success_flag = False
            # output_list.msg_str = "Your license is valid for max. room number = " + to_string(room_limit) + " Please contact our Technical Support for further information"
            output_list.msg_str = f"Your license is valid for max. room number = {to_string(room_limit)} Please contact our Technical Support for further information"

            return generate_output()
        # end Malik: Setup Wizard
        
        for input_zimmer in query(input_zimmer_data, sort_by=[("zinr", True)]):
            zimkateg = get_cache(
                Zimkateg, {"zikatnr": [(eq, input_zimmer.zikatnr)]})

            if zimkateg:
                zimkateg.maxzimanz = zimkateg.maxzimanz + 1

            zimmer = get_cache(Zimmer, {"zinr": [(eq, input_zimmer.zinr)]})

            if not zimmer:
                zimmer = Zimmer()
                db_session.add(zimmer)

                zimmer.zinr = input_zimmer.zinr
                zimmer.typ = input_zimmer.view_type
                zimmer.setup = input_zimmer.bed_type - 9200
                zimmer.etage = input_zimmer.etage
                zimmer.zikatnr = input_zimmer.zikatnr
                zimmer.sleeping = True

                output_zimmer = Output_zimmer()
                output_zimmer_data.append(output_zimmer)

                output_zimmer.zinr = zimmer.zinr
                output_zimmer.etage = zimmer.etage
                output_zimmer.zikatnr = zimmer.zikatnr
                output_zimmer.sleeping = zimmer.sleeping

                bed_default = 9200 + zimmer.setup

                paramtext = get_cache(
                    Paramtext, {"txtnr": [(eq, bed_default)]})

                if paramtext:
                    output_zimmer.bed_type = paramtext.ptexte

                bf_paramtext = get_cache(
                    Paramtext, {"txtnr": [(eq, 230)], "sprachcode": [(eq, zimmer.typ)]})

                if bf_paramtext:
                    output_zimmer.view_type = paramtext.ptexte

                floor_mode = "add"
                create_floor()
                output_list = Output_list()
                output_list_data.append(output_list)

                output_list.success_flag = True
                # output_list.msg_str = "Create room setup number of " + to_string(input_zimmer.zinr) + " successfully."
                output_list.msg_str = f"Create room setup number of {to_string(input_zimmer.zinr)} successfully."

            else:
                output_list = Output_list()
                output_list_data.append(output_list)

                output_list.success_flag = False
                output_list.msg_str = f"Create room setup number of {to_string(input_zimmer.zinr)} already exist. Please create another room number"

    elif input_list.case_type == 2:
        zimmer = get_cache(Zimmer, {"zinr": [(eq, input_zimmer.zinr)]})

        if zimmer:
            if trim(input_zimmer.prev_zinr) != trim(input_zimmer.zinr):
                output_list = Output_list()
                output_list_data.append(output_list)

                output_list.success_flag = False
                output_list.msg_str = f"Room number {to_string(input_zimmer.zinr)} already exist. Please change another room number."

                return generate_output()
            fill_zimmer_update()
            floor_mode = "chg"
            create_floor()
            output_list = Output_list()
            output_list_data.append(output_list)

            output_list.success_flag = True
            output_list.msg_str = f"Update room setup number of {to_string(input_zimmer.zinr)} successfully."

        elif not zimmer and trim(input_zimmer.prev_zinr) != trim(input_zimmer.zinr):
            bf_zimmer = db_session.query(Bf_zimmer).filter(
                (Bf_zimmer.zinr == trim(input_zimmer.prev_zinr))).first()

            if bf_zimmer:
                db_session.delete(bf_zimmer)
            zimmer = Zimmer()
            db_session.add(zimmer)

            zimmer.zinr = input_zimmer.zinr
            zimmer.typ = input_zimmer.view_type
            zimmer.setup = input_zimmer.bed_type - 9200
            zimmer.etage = input_zimmer.etage
            zimmer.zikatnr = input_zimmer.zikatnr
            zimmer.sleeping = True

            output_zimmer = Output_zimmer()
            output_zimmer_data.append(output_zimmer)

            output_zimmer.zinr = zimmer.zinr
            output_zimmer.etage = zimmer.etage
            output_zimmer.zikatnr = zimmer.zikatnr
            output_zimmer.sleeping = zimmer.sleeping

            bed_default = 9200 + zimmer.setup

            paramtext = get_cache(Paramtext, {"txtnr": [(eq, bed_default)]})

            if paramtext:
                output_zimmer.bed_type = paramtext.ptexte

            bf_paramtext = get_cache(
                Paramtext, {"txtnr": [(eq, 230)], "sprachcode": [(eq, zimmer.typ)]})

            if bf_paramtext:
                output_zimmer.view_type = paramtext.ptexte

            floor_mode = "modify/create"
            create_floor()
            output_list = Output_list()
            output_list_data.append(output_list)

            output_list.success_flag = True
            output_list.msg_str = f"Create room setup number of {to_string(input_zimmer.zinr)} successfully."

        else:
            output_list = Output_list()
            output_list_data.append(output_list)

            output_list.success_flag = False
            output_list.msg_str = f"Room number {to_string(input_zimmer.zinr)} not found. Please change another room number."

            return generate_output()

    elif input_list.case_type == 3:
        create_section()

        queasy = get_cache(
            Queasy, {"key": [(eq, 357)], "number1": [(eq, 3)], "deci1": [(eq, 3.4)], "char1": [(eq, "room setup")], "char2": [(eq, "room admin")], "logi1": [(eq, True)]})

        if not queasy:
            output_list = Output_list()
            output_list_data.append(output_list)

            output_list.success_flag = False
            output_list.msg_str = "Error create section.. this section not saved in queasy table. Please contact our Customer Service."

            return generate_output()
        else:
            output_list = Output_list()
            output_list_data.append(output_list)

            output_list.success_flag = True
            output_list.msg_str = "Create section successfully."

    return generate_output()
