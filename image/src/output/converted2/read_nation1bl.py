#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import Nation

def read_nation1bl(case_type:int, int1:int, int2:int, int3:int, char1:string, char2:string, logic1:bool):
    t_nation_list = []
    nation = None

    t_nation = None

    t_nation_list, T_nation = create_model_like(Nation)

    db_session = local_storage.db_session

    def generate_output():
        nonlocal t_nation_list, nation
        nonlocal case_type, int1, int2, int3, char1, char2, logic1


        nonlocal t_nation
        nonlocal t_nation_list

        return {"t-nation": t_nation_list}

    if case_type == 1:

        nation = get_cache (Nation, {"untergruppe": [(eq, int1)],"natcode": [(eq, int2)]})

        if nation:
            t_nation = T_nation()
            t_nation_list.append(t_nation)

            buffer_copy(nation, t_nation)
    elif case_type == 2:

        for nation in db_session.query(Nation).filter(
                 (Nation.natcode == int1)).order_by(Nation._recid).all():
            t_nation = T_nation()
            t_nation_list.append(t_nation)

            buffer_copy(nation, t_nation)
    elif case_type == 3:

        nation = get_cache (Nation, {"kurzbez": [(eq, char1)],"natcode": [(eq, int1)]})

        if nation:
            t_nation = T_nation()
            t_nation_list.append(t_nation)

            buffer_copy(nation, t_nation)

    return generate_output()