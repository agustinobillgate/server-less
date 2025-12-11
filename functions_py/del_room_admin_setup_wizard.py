#using conversion tools version: 1.0.0.117

# ==========================================
# Rulita, 09-10-2025
# Tiket ID : 8CF423 | Recompile Program

# Rulita, 10-12-2025
# - Added with_for_update before delete query
# ==========================================

from functions.additional_functions import *
from decimal import Decimal
from models import Zimmer, Res_line, Zimkateg, Bediener, Res_history, Htparam, Queasy

input_list_data, Input_list = create_model("Input_list", {"zinr":string, "zikatnr":int, "user_init":string})

def del_room_admin_setup_wizard(input_list_data:[Input_list]):

    prepare_cache ([Res_line, Zimkateg, Bediener, Res_history, Htparam])

    output_zimmer_data = []
    output_list_data = []
    zimmer = res_line = zimkateg = bediener = res_history = htparam = queasy = None

    input_list = output_zimmer = output_list = bf_zimmer = None

    output_zimmer_data, Output_zimmer = create_model("Output_zimmer", {"room_limit":int, "curr_anz":int})
    output_list_data, Output_list = create_model("Output_list", {"success_flag":bool, "msg_str":string})

    Bf_zimmer = create_buffer("Bf_zimmer",Zimmer)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal output_zimmer_data, output_list_data, zimmer, res_line, zimkateg, bediener, res_history, htparam, queasy
        nonlocal bf_zimmer


        nonlocal input_list, output_zimmer, output_list, bf_zimmer
        nonlocal output_zimmer_data, output_list_data

        return {"output-zimmer": output_zimmer_data, "output-list": output_list_data}

    def check_rm_limit():

        nonlocal output_zimmer_data, output_list_data, zimmer, res_line, zimkateg, bediener, res_history, htparam, queasy
        nonlocal bf_zimmer


        nonlocal input_list, output_zimmer, output_list, bf_zimmer
        nonlocal output_zimmer_data, output_list_data

        rbuff = None
        Rbuff =  create_buffer("Rbuff",Zimmer)

        htparam = get_cache (Htparam, {"paramnr": [(eq, 975)]})

        if htparam.finteger > 0:
            output_zimmer = Output_zimmer()
            output_zimmer_data.append(output_zimmer)

            output_zimmer.room_limit = htparam.finteger

        for rbuff in db_session.query(Rbuff).order_by(Rbuff._recid).all():
            output_zimmer.curr_anz = output_zimmer.curr_anz + 1


    def delete_floor():

        nonlocal output_zimmer_data, output_list_data, zimmer, res_line, zimkateg, bediener, res_history, htparam, queasy
        nonlocal bf_zimmer


        nonlocal input_list, output_zimmer, output_list, bf_zimmer
        nonlocal output_zimmer_data, output_list_data

        # queasy = get_cache (Queasy, {"key": [(eq, 25)],"number2": [(eq, zimmer.etage)],"char1": [(eq, zimmer.zinr)]})
        queasy = db_session.query(Queasy).filter(
            (Queasy.key == 25) & (Queasy.number2 == zimmer.etage) & (Queasy.char1 == zimmer.zinr)).with_for_update().first()

        if queasy:
            db_session.delete(queasy)
            pass

        # queasy = get_cache (Queasy, {"key": [(eq, 25)],"number2": [(eq, zimmer.etage)],"betriebsnr": [(ne, 0)]})
        queasy = db_session.query(Queasy).filter(
            (Queasy.key == 25) & (Queasy.number2 == zimmer.etage) & (Queasy.betriebsnr != 0)).with_for_update().first()

        if queasy:
            db_session.refresh(queasy, with_for_update=True)
            queasy.betriebsnr = 0
            queasy.logi1 = False
            db_session.flush()


    input_list = query(input_list_data, first=True)

    if not input_list:
        output_list = Output_list()
        output_list_data.append(output_list)

        output_list.success_flag = False
        output_list.msg_str = "Error loading input-list.. please contact our Customer Service"

        return generate_output()

    for input_list in query(input_list_data, sort_by=[("zinr",False)]):

        res_line = get_cache (Res_line, {"zinr": [(eq, input_list.zinr)]})

        if res_line:
            output_list = Output_list()
            output_list_data.append(output_list)

            output_list.success_flag = False
            output_list.msg_str = "Reservation exists, deleting room number " + res_line.zinr + " not possible."

            return generate_output()
        else:

            # zimkateg = get_cache (Zimkateg, {"zikatnr": [(eq, input_list.zikatnr)]})
            zimkateg = db_session.query(Zimkateg).filter(
                     (Zimkateg.zikatnr == input_list.zikatnr)).with_for_update().first()

            if zimkateg:
                zimkateg.maxzimanz = zimkateg.maxzimanz - 1
                pass
                pass

            # zimmer = get_cache (Zimmer, {"zinr": [(eq, input_list.zinr)]})
            zimmer = db_session.query(Zimmer).filter(
                     (Zimmer.zinr == input_list.zinr)).with_for_update().first()

            if zimmer:

                bediener = get_cache (Bediener, {"userinit": [(eq, input_list.user_init)]})
                res_history = Res_history()
                db_session.add(res_history)

                res_history.nr = bediener.nr
                res_history.datum = get_current_date()
                res_history.zeit = get_current_time_in_seconds()
                res_history.aenderung = "Delete Room Number " + zimmer.zinr


                res_history.action = "Room Admin"
                pass
                pass
                delete_floor()
                db_session.delete(zimmer)
                pass
                output_list = Output_list()
                output_list_data.append(output_list)

                output_list.success_flag = True
                output_list.msg_str = "Room number " + input_list.zinr + " deleted successfully."


            else:
                output_list = Output_list()
                output_list_data.append(output_list)

                output_list.success_flag = False
                output_list.msg_str = "Room number " + input_list.zinr + " does not exist."


            check_rm_limit()

    return generate_output()