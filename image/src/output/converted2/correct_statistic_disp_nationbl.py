#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import Nation

def correct_statistic_disp_nationbl():

    prepare_cache ([Nation])

    t_nation_list = []
    nation = None

    t_nation = None

    t_nation_list, T_nation = create_model("T_nation", {"nationnr":int, "bezeich":string})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal t_nation_list, nation


        nonlocal t_nation
        nonlocal t_nation_list

        return {"t-nation": t_nation_list}

    for nation in db_session.query(Nation).filter(
             (Nation.natcode == 0)).order_by(Nation.bezeich).all():
        t_nation = T_nation()
        t_nation_list.append(t_nation)

        t_nation.nationnr = nation.nationnr
        t_nation.bezeich = nation.bezeich

    return generate_output()