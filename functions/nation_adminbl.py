#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import Nation, Prmarket

def nation_adminbl(int1:int):

    prepare_cache ([Prmarket])

    t_nation_data = []
    t_nation1_data = []
    a:int = 0
    nation = prmarket = None

    t_nation1 = t_nation = None

    t_nation1_data, T_nation1 = create_model_like(Nation)
    t_nation_data, T_nation = create_model_like(Nation, {"marksegm":string, "rec_id":int})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal t_nation_data, t_nation1_data, a, nation, prmarket
        nonlocal int1


        nonlocal t_nation1, t_nation
        nonlocal t_nation1_data, t_nation_data

        return {"t-nation": t_nation_data, "t-nation1": t_nation1_data}


    for nation in db_session.query(Nation).filter(
             (Nation.natcode == int1)).order_by(Nation.kurzbez).all():
        t_nation = T_nation()
        t_nation_data.append(t_nation)

        buffer_copy(nation, t_nation)
        t_nation.rec_id = nation._recid


        a = to_int(entry(1, nation.bezeich, ";"))

        prmarket = get_cache (Prmarket, {"nr": [(eq, a)]})

        if prmarket:
            t_nation.marksegm = prmarket.bezeich

    for nation in db_session.query(Nation).order_by(Nation._recid).all():
        t_nation1 = T_nation1()
        t_nation1_data.append(t_nation1)

        buffer_copy(nation, t_nation1)

    return generate_output()