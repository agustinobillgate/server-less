from functions.additional_functions import *
import decimal
from sqlalchemy import func
from models import Arrangement, Waehrung

def write_arrangementbl(case_type:int, char1:str, t_arrangement:[T_arrangement]):
    success_flag = False
    arrangement = waehrung = None

    t_arrangement = None

    t_arrangement_list, T_arrangement = create_model_like(Arrangement)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal success_flag, arrangement, waehrung


        nonlocal t_arrangement
        nonlocal t_arrangement_list
        return {"success_flag": success_flag}

    t_arrangement = query(t_arrangement_list, first=True)

    if not t_arrangement:

        return generate_output()

    if case_type == 1:
        arrangement = Arrangement()
        db_session.add(arrangement)

        buffer_copy(t_arrangement, arrangement)

        if char1 != "":

            waehrung = db_session.query(Waehrung).filter(
                    (func.lower(Waehrung.bezeich) == (char1).lower())).first()
            arrangement.betriebsnr = waehrungsnr

        success_flag = True


    elif case_type == 2:

        arrangement = db_session.query(Arrangement).filter(
                (Arrangement.argtnr == t_Arrangement.argtnr) &  (Arrangement == t_Arrangement)).first()

        if arrangement:
            buffer_copy(t_arrangement, arrangement)

            if char1 != "":

                waehrung = db_session.query(Waehrung).filter(
                        (func.lower(Waehrung.bezeich) == (char1).lower())).first()
                arrangement.betriebsnr = waehrungsnr

            success_flag = True

    return generate_output()