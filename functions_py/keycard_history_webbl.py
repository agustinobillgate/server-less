#using conversion tools version: 1.0.0.117
#------------------------------------------
# Rd, 19/8/2025
# input_list.fromdate
#------------------------------------------

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Bediener, Res_history

input_list_data, Input_list = create_model("Input_list", {"from_date":date, "to_date":date, "usrid":string})

def keycard_history_webbl(input_list_data:[Input_list]):

    prepare_cache ([Bediener, Res_history])

    output_list_data = []
    err_msg = ""
    bediener = res_history = None

    ubuff = input_list = output_list = None

    output_list_data, Output_list = create_model("Output_list", {"datum":date, "aenderung":string, "username":string, "zeit":string})

    Ubuff = create_buffer("Ubuff",Bediener)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal output_list_data, err_msg, bediener, res_history
        nonlocal ubuff


        nonlocal ubuff, input_list, output_list
        nonlocal output_list_data

        return {"output-list": output_list_data, "err_msg": err_msg}

    def create_list():

        nonlocal output_list_data, err_msg, bediener, res_history
        nonlocal ubuff


        nonlocal ubuff, input_list, output_list
        nonlocal output_list_data

        # Rd 19/8/2025
        # if input_list.usrID != "" and input_list.usrID != None:
        if input_list.usrid != "" and input_list.usrid != None:

            bediener = get_cache (Bediener, {"userinit": [(eq, trim(entry(0, input_list.usrid, "-")))]})

            if bediener:

                for res_history in db_session.query(Res_history).filter(
                         (Res_history.datum >= input_list.from_date) & (Res_history.datum <= input_list.to_date) & (Res_history.action == ("Keycard").lower()) & (Res_history.nr == bediener.nr)).order_by(Res_history.datum, Res_history.zeit).all():
                    output_list = Output_list()
                    output_list_data.append(output_list)

                    output_list.datum = res_history.datum
                    output_list.aenderung = res_history.aenderung
                    output_list.zeit = to_string(res_history.zeit, "HH:MM:SS")

                    ubuff = get_cache (Bediener, {"nr": [(eq, res_history.nr)]})

                    if ubuff:
                        output_list.username = ubuff.username
            else:
                err_msg = "ERROR : User not found"

                return
        else:

            # for res_history in db_session.query(Res_history).filter(
            #          (Res_history.datum >= from_date) & (Res_history.datum <= to_date) & (Res_history.action == ("Keycard").lower())).order_by(Res_history.datum, Res_history.zeit).all():
            for res_history in db_session.query(Res_history).filter(
                     (Res_history.datum >= input_list.from_date) & (Res_history.datum <= input_list.to_date) & (Res_history.action == ("Keycard").lower())).order_by(Res_history.datum, Res_history.zeit).all():
                
                
                output_list = Output_list()
                output_list_data.append(output_list)

                output_list.datum = res_history.datum
                output_list.aenderung = res_history.aenderung
                output_list.zeit = to_string(res_history.zeit, "HH:MM:SS")

                ubuff = get_cache (Bediener, {"nr": [(eq, res_history.nr)]})

                if ubuff:
                    output_list.username = ubuff.username

    input_list = query(input_list_data, filters=(lambda input_list: input_list.from_date != None and input_list.to_date != None), first=True)

    if not input_list:
        err_msg = "ERROR : Date input can't be null"

        return generate_output()
    create_list()

    return generate_output()