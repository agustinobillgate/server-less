#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import Nation

t_nation_data, T_nation = create_model_like(Nation)

def write_nationbl(case_type:int, t_nation_data:[T_nation]):
    success_flag = False
    nation = None

    t_nation = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal success_flag, nation
        nonlocal case_type


        nonlocal t_nation

        return {"success_flag": success_flag}

    t_nation = query(t_nation_data, first=True)

    if not t_nation:

        return generate_output()

    if case_type == 1:
        nation = Nation()
        db_session.add(nation)

        buffer_copy(t_nation, nation)
        success_flag = True
    elif case_type == 2:

        nation = get_cache (Nation, {"kurzbez": [(eq, t_nation.kurzbez)],"untergruppe": [(eq, t_nation.untergruppe)],"natcode": [(eq, t_nation.natcode)]})

        if nation:
            buffer_copy(t_nation, nation)
            success_flag = True

    return generate_output()