#using conversion tools version: 1.0.0.117
#------------------------------------------
# Rd, 20/10/2025
# add safe_int function to handle invalid int conversions
#------------------------------------------
from functions.additional_functions import *
from decimal import Decimal
from models import Nitestor

def safe_int(value):
    try:
        if isinstance(value, str):
            value = value.strip()
            if value in ("", "?", None):
                return 0
            return int(value, 0)  # auto-detect base if string like "0x10"
        return int(value) if value is not None else 0
    except Exception:
        return 0
    
def read_nitestorbl(case_type:int, int1:int, int2:int, int3:int, int4:int, char1:string):
    t_nitestor_data = []
    nitestor = None

    t_nitestor = None

    t_nitestor_data, T_nitestor = create_model_like(Nitestor)

    db_session = local_storage.db_session

    int1 = safe_int(int1)
    int2 = safe_int(int2)
    int3 = safe_int(int3)
    int4 = safe_int(int4)
    char1 = char1.strip() if char1 else ""

    def generate_output():
        nonlocal t_nitestor_data, nitestor
        nonlocal case_type, int1, int2, int3, int4, char1


        nonlocal t_nitestor
        nonlocal t_nitestor_data

        return {"t-nitestor": t_nitestor_data}

    if case_type == 1:

        for nitestor in db_session.query(Nitestor).filter(
                 (Nitestor.reihenfolge == int1)).order_by(Nitestor._recid).all():
            t_nitestor = T_nitestor()
            t_nitestor_data.append(t_nitestor)

            buffer_copy(nitestor, t_nitestor)
    elif case_type == 2:

        for nitestor in db_session.query(Nitestor).filter(
                 (Nitestor.night_type == int1) & (Nitestor.reihenfolge == int2)).order_by(Nitestor._recid).all():
            t_nitestor = T_nitestor()
            t_nitestor_data.append(t_nitestor)

            buffer_copy(nitestor, t_nitestor)

    return generate_output()