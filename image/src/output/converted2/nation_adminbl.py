#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import Nation, Prmarket

def nation_adminbl(int1:int):

    prepare_cache ([Prmarket])

    t_nation_list = []
    t_nation1_list = []
    a:int = 0
    nation = prmarket = None

    t_nation1 = t_nation = None

    t_nation1_list, T_nation1 = create_model_like(Nation)
    t_nation_list, T_nation = create_model_like(Nation, {"marksegm":string, "rec_id":int})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal t_nation_list, t_nation1_list, a, nation, prmarket
        nonlocal int1


        nonlocal t_nation1, t_nation
        nonlocal t_nation1_list, t_nation_list

        return {"t-nation": t_nation_list, "t-nation1": t_nation1_list}


    for nation in db_session.query(Nation).filter(
             (Nation.natcode == int1)).order_by(Nation.kurzbez).all():
        t_nation = T_nation()
        t_nation_list.append(t_nation)

        buffer_copy(nation, t_nation)
        t_nation.rec_id = nation._recid


        a = to_int(entry(1, nation.bezeich, ";"))

        prmarket = get_cache (Prmarket, {"nr": [(eq, a)]})

        if prmarket:
            t_nation.marksegm = prmarket.bezeich

    for nation in db_session.query(Nation).order_by(Nation._recid).all():
        t_nation1 = T_nation1()
        t_nation1_list.append(t_nation1)

        buffer_copy(nation, t_nation1)

    return generate_output()