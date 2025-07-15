#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import Arrangement, Waehrung

t_arrangement_data, T_arrangement = create_model_like(Arrangement)

def write_arrangementbl(case_type:int, char1:string, t_arrangement_data:[T_arrangement]):

    prepare_cache ([Arrangement, Waehrung])

    success_flag = False
    arrangement = waehrung = None

    t_arrangement = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal success_flag, arrangement, waehrung
        nonlocal case_type, char1


        nonlocal t_arrangement

        return {"success_flag": success_flag}

    t_arrangement = query(t_arrangement_data, first=True)

    if not t_arrangement:

        return generate_output()

    if case_type == 1:
        arrangement = Arrangement()
        db_session.add(arrangement)

        buffer_copy(t_arrangement, arrangement)

        if char1 != "":

            waehrung = get_cache (Waehrung, {"bezeich": [(eq, char1)]})
            arrangement.betriebsnr = waehrung.waehrungsnr


        pass
        success_flag = True


    elif case_type == 2:

        arrangement = get_cache (Arrangement, {"argtnr": [(eq, t_arrangement.argtnr)],"arrangement": [(eq, t_arrangement.arrangement)]})

        if arrangement:
            buffer_copy(t_arrangement, arrangement)

            if char1 != "":

                waehrung = get_cache (Waehrung, {"bezeich": [(eq, char1)]})
                arrangement.betriebsnr = waehrung.waehrungsnr


            pass
            success_flag = True

    return generate_output()