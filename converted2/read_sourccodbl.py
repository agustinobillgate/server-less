#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import Sourccod

def read_sourccodbl(case_type:int, sourceno:int):
    t_sourccod_data = []
    sourccod = None

    t_sourccod = None

    t_sourccod_data, T_sourccod = create_model_like(Sourccod)

    db_session = local_storage.db_session

    def generate_output():
        nonlocal t_sourccod_data, sourccod
        nonlocal case_type, sourceno


        nonlocal t_sourccod
        nonlocal t_sourccod_data

        return {"t-sourccod": t_sourccod_data}

    if case_type == 1:

        sourccod = get_cache (Sourccod, {"source_code": [(eq, sourceno)],"betriebsnr": [(eq, 0)]})

        if sourccod:
            t_sourccod = T_sourccod()
            t_sourccod_data.append(t_sourccod)

            buffer_copy(sourccod, t_sourccod)
    elif case_type == 2:

        sourccod = get_cache (Sourccod, {"betriebsnr": [(eq, 0)]})

        if sourccod:
            t_sourccod = T_sourccod()
            t_sourccod_data.append(t_sourccod)

            buffer_copy(sourccod, t_sourccod)
    elif case_type == 3:

        for sourccod in db_session.query(Sourccod).filter(
                 (Sourccod.betriebsnr == 0)).order_by(Sourccod.source_code).all():
            t_sourccod = T_sourccod()
            t_sourccod_data.append(t_sourccod)

            buffer_copy(sourccod, t_sourccod)

    elif case_type == 4:

        sourccod = get_cache (Sourccod, {"source_code": [(eq, sourceno)]})

        if sourccod:
            t_sourccod = T_sourccod()
            t_sourccod_data.append(t_sourccod)

            buffer_copy(sourccod, t_sourccod)
    elif case_type == 5:

        for sourccod in db_session.query(Sourccod).filter(
                 (Sourccod.betriebsnr == 0) & (Sourccod.source_code != sourceno)).order_by(Sourccod.source_code).all():
            t_sourccod = T_sourccod()
            t_sourccod_data.append(t_sourccod)

            buffer_copy(sourccod, t_sourccod)
    elif case_type == 6:

        for sourccod in db_session.query(Sourccod).filter(
                 (Sourccod.source_code != sourceno)).order_by(Sourccod.source_code).all():
            t_sourccod = T_sourccod()
            t_sourccod_data.append(t_sourccod)

            buffer_copy(sourccod, t_sourccod)
    elif case_type == 7:

        sourccod = db_session.query(Sourccod).first()

        if sourccod:
            t_sourccod = T_sourccod()
            t_sourccod_data.append(t_sourccod)

            buffer_copy(sourccod, t_sourccod)
    elif case_type == 8:

        for sourccod in db_session.query(Sourccod).order_by(Sourccod.source_code).all():
            t_sourccod = T_sourccod()
            t_sourccod_data.append(t_sourccod)

            buffer_copy(sourccod, t_sourccod)

    return generate_output()