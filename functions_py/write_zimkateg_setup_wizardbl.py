#using conversion tools version: 1.0.0.117

# =======================================
# Rulita, 09-10-2025
# Tiket ID : 8CF423 | Recompile program
# Rd, 28/11/2025, with_for_update added
# =======================================

from functions.additional_functions import *
from decimal import Decimal
from models import Zimkateg, Queasy

t_zimkateg_data, T_zimkateg = create_model("T_zimkateg", {"zikatnr":int, "kurzbez":string, "bezeichnung":string, "case_type":int})

def write_zimkateg_setup_wizardbl(t_zimkateg_data:[T_zimkateg]):

    prepare_cache ([Zimkateg, Queasy])

    output_param_data = []
    counter:int = 0
    ot_flag:bool = False
    zimkateg = queasy = None

    t_zimkateg = output_param = None

    output_param_data, Output_param = create_model("Output_param", {"success_flag":bool, "msg_str":string})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal output_param_data, counter, ot_flag, zimkateg, queasy


        nonlocal t_zimkateg, output_param
        nonlocal output_param_data

        return {"output-param": output_param_data}

    def create_section():

        nonlocal output_param_data, counter, ot_flag, zimkateg, queasy


        nonlocal t_zimkateg, output_param
        nonlocal output_param_data

        queasy = get_cache (Queasy, {"key": [(eq, 357)],"number1": [(eq, 3)],"deci1": [(eq, 3.1)],"char1": [(eq, "room setup")],"char2": [(eq, "room type")],"logi1": [(eq, True)]})

        if not queasy:
            queasy = Queasy()
            db_session.add(queasy)

            queasy.key = 357
            queasy.number1 = 3
            queasy.deci1 =  to_decimal(3.1)
            queasy.char1 = "ROOM SETUP"
            queasy.char2 = "ROOM TYPE"
            queasy.logi1 = True

    t_zimkateg = query(t_zimkateg_data, first=True)

    if not t_zimkateg:
        output_param = Output_param()
        output_param_data.append(output_param)

        output_param.success_flag = False
        output_param.msg_str = "Error loading.. please contact our Customer Service"

        return generate_output()

    if t_zimkateg.case_type == 1:

        for t_zimkateg in query(t_zimkateg_data):

            for zimkateg in db_session.query(Zimkateg).filter(
                     (Zimkateg.zikatnr > 0)).order_by(Zimkateg.zikatnr.desc()).all():
                counter = zimkateg.zikatnr
                break

            zimkateg = get_cache (Zimkateg, {"kurzbez": [(eq, t_zimkateg.kurzbez)]})

            if not zimkateg:
                zimkateg = Zimkateg()
                db_session.add(zimkateg)

                zimkateg.zikatnr = counter + 1
                zimkateg.kurzbez = t_zimkateg.kurzbez
                zimkateg.bezeichnung = t_zimkateg.bezeichnung
                zimkateg.verfuegbarkeit = True
                zimkateg.zibelstat = True
                zimkateg.active = True

                queasy = get_cache (Queasy, {"key": [(eq, 325)],"number1": [(eq, t_zimkateg.zikatnr)]})

                if not queasy:
                    queasy = Queasy()
                    db_session.add(queasy)

                    queasy.key = 325
                    queasy.number1 = t_zimkateg.zikatnr
                    queasy.number2 = 0
                    queasy.number3 = 0


                output_param = Output_param()
                output_param_data.append(output_param)

                output_param.success_flag = True
                output_param.msg_str = "create room type " + to_string(zimkateg.zikatnr) + " successfully."


            else:
                output_param = Output_param()
                output_param_data.append(output_param)

                output_param.success_flag = False
                output_param.msg_str = "Room Type Code " + to_string(zimkateg.kurzbez) + " Already Exist. Please Change"


    elif t_zimkateg.case_type == 2:

        # zimkateg = get_cache (Zimkateg, {"zikatnr": [(eq, t_zimkateg.zikatnr)]})
        zimkateg = db_session.query(Zimkateg).filter(
                 (Zimkateg.zikatnr == t_zimkateg.zikatnr)).with_for_update().first()

        if zimkateg:
            zimkateg.zikatnr = t_zimkateg.zikatnr
            zimkateg.kurzbez = t_zimkateg.kurzbez
            zimkateg.bezeichnung = t_zimkateg.bezeichnung

            queasy = get_cache (Queasy, {"key": [(eq, 325)],"number1": [(eq, t_zimkateg.zikatnr)]})

            if not queasy:
                queasy = Queasy()
                db_session.add(queasy)

                queasy.key = 325
                queasy.number1 = t_zimkateg.zikatnr
                queasy.number2 = 0
                queasy.number3 = 0


            pass
            pass
            output_param = Output_param()
            output_param_data.append(output_param)

            output_param.success_flag = True
            output_param.msg_str = "update room type successfully."


        else:
            output_param = Output_param()
            output_param_data.append(output_param)

            output_param.success_flag = False
            output_param.msg_str = "Room type not found. Please modify another room type"


    elif t_zimkateg.case_type == 3:
        create_section()
        output_param = Output_param()
        output_param_data.append(output_param)

        output_param.success_flag = True


        output_param.msg_str = "create section for room type successfully."

    return generate_output()