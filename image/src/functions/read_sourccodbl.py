from functions.additional_functions import *
import decimal
from models import Sourccod

def read_sourccodbl(case_type:int, sourceno:int):
    t_sourccod_list = []
    sourccod = None

    t_sourccod = None

    t_sourccod_list, T_sourccod = create_model_like(Sourccod)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal t_sourccod_list, sourccod


        nonlocal t_sourccod
        nonlocal t_sourccod_list
        return {"t-sourccod": t_sourccod_list}

    if case_type == 1:

        sourccod = db_session.query(Sourccod).filter(
                (Sourccod.source_code == sourceno) &  (Sourccod.betriebsnr == 0)).first()

        if sourccod:
            t_sourccod = T_sourccod()
            t_sourccod_list.append(t_sourccod)

            buffer_copy(sourccod, t_sourccod)
    elif case_type == 2:

        sourccod = db_session.query(Sourccod).filter(
                (Sourccod.betriebsnr == 0)).first()

        if sourccod:
            t_sourccod = T_sourccod()
            t_sourccod_list.append(t_sourccod)

            buffer_copy(sourccod, t_sourccod)
    elif case_type == 3:

        for sourccod in db_session.query(Sourccod).filter(
                (Sourccod.betriebsnr == 0)).all():
            t_sourccod = T_sourccod()
            t_sourccod_list.append(t_sourccod)

            buffer_copy(sourccod, t_sourccod)

    elif case_type == 4:

        sourccod = db_session.query(Sourccod).filter(
                (Sourccod.source_code == sourceno)).first()

        if sourccod:
            t_sourccod = T_sourccod()
            t_sourccod_list.append(t_sourccod)

            buffer_copy(sourccod, t_sourccod)
    elif case_type == 5:

        for sourccod in db_session.query(Sourccod).filter(
                (Sourccod.betriebsnr == 0) &  (Sourccod.source_code != sourceno)).all():
            t_sourccod = T_sourccod()
            t_sourccod_list.append(t_sourccod)

            buffer_copy(sourccod, t_sourccod)
    elif case_type == 6:

        for sourccod in db_session.query(Sourccod).filter(
                (Sourccod.source_code != sourceno)).all():
            t_sourccod = T_sourccod()
            t_sourccod_list.append(t_sourccod)

            buffer_copy(sourccod, t_sourccod)
    elif case_type == 7:

        sourccod = db_session.query(Sourccod).first()

        if sourccod:
            t_sourccod = T_sourccod()
            t_sourccod_list.append(t_sourccod)

            buffer_copy(sourccod, t_sourccod)
    elif case_type == 8:

        for sourccod in db_session.query(Sourccod).all():
            t_sourccod = T_sourccod()
            t_sourccod_list.append(t_sourccod)

            buffer_copy(sourccod, t_sourccod)

    return generate_output()