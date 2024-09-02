from functions.additional_functions import *
import decimal
from models import Sourccod

def write_sourccodbl(case_type:int, t_sourccod:[T_sourccod]):
    success_flag = False
    sourccod = None

    t_sourccod = None

    t_sourccod_list, T_sourccod = create_model_like(Sourccod)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal success_flag, sourccod


        nonlocal t_sourccod
        nonlocal t_sourccod_list
        return {"success_flag": success_flag}

    t_sourccod = query(t_sourccod_list, first=True)

    if not t_sourccod:

        return generate_output()

    if case_type == 1:
        sourccod = Sourccod()
        db_session.add(sourccod)

        buffer_copy(t_sourccod, sourccod)

        success_flag = True
    elif case_type == 2:

        sourccod = db_session.query(Sourccod).filter(
                (Sourccod.source_code == t_Sourccod.source_code)).first()

        if Sourccod:
            buffer_copy(t_sourccod, sourccod)

            success_flag = True
    elif case_type == 3:

        sourccod = db_session.query(Sourccod).filter(
                (Sourccod.source_code == t_Sourccod.source_code)).first()

        if Sourccod:
            db_session.delete(sourccod)

            success_flag = True

    return generate_output()