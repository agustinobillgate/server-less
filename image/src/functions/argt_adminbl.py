from functions.additional_functions import *
import decimal
from models import Arrangement, Waehrung

def argt_adminbl():
    t_arrangement_list = []
    arrangement = waehrung = None

    t_arrangement = waehrung1 = None

    t_arrangement_list, T_arrangement = create_model_like(Arrangement, {"waehrungsnr":str})

    Waehrung1 = Waehrung

    db_session = local_storage.db_session

    def generate_output():
        nonlocal t_arrangement_list, arrangement, waehrung
        nonlocal waehrung1


        nonlocal t_arrangement, waehrung1
        nonlocal t_arrangement_list
        return {"t-arrangement": t_arrangement_list}

    for arrangement in db_session.query(Arrangement).filter(
            (Arrangement.segmentcode == 0)).all():
        t_arrangement = T_arrangement()
        t_arrangement_list.append(t_arrangement)

        buffer_copy(arrangement, t_arrangement)

        waehrung1 = db_session.query(Waehrung1).filter(
                (Waehrung1.waehrungsnr == arrangement.betriebsnr)).first()
        t_arrangement.waehrungsnr = waehrung1.bezeich

    return generate_output()