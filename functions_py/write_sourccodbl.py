#using conversion tools version: 1.0.0.117
#-------------------------------------------------------
# Rd, 27/11/2025, with_for_update added
#-------------------------------------------------------
from functions.additional_functions import *
from decimal import Decimal
from models import Sourccod

t_sourccod_data, T_sourccod = create_model_like(Sourccod)

def write_sourccodbl(case_type:int, t_sourccod_data:[T_sourccod]):
    success_flag = False
    sourccod = None

    t_sourccod = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal success_flag, sourccod
        nonlocal case_type


        nonlocal t_sourccod

        return {"success_flag": success_flag}

    t_sourccod = query(t_sourccod_data, first=True)

    if not t_sourccod:

        return generate_output()

    if case_type == 1:
        sourccod = Sourccod()
        db_session.add(sourccod)

        buffer_copy(t_sourccod, sourccod)
        pass
        success_flag = True
    elif case_type == 2:

        # sourccod = get_cache (Sourccod, {"source_code": [(eq, t_sourccod.source_code)]})
        sourccod = db_session.query(Sourccod).filter(
                 (Sourccod.source_code == t_sourccod.source_code)).with_for_update().first()

        if sourccod:
            buffer_copy(t_sourccod, sourccod)
            pass
            success_flag = True
    elif case_type == 3:

        # sourccod = get_cache (Sourccod, {"source_code": [(eq, t_sourccod.source_code)]})
        sourccod = db_session.query(Sourccod).filter(
                 (Sourccod.source_code == t_sourccod.source_code)).with_for_update().first()

        if Sourccod:
            db_session.delete(sourccod)
            pass
            success_flag = True

    return generate_output()