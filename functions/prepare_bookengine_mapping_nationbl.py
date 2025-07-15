#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import Nation, Queasy

def prepare_bookengine_mapping_nationbl(bookengid:int):

    prepare_cache ([Nation, Queasy])

    t_mapping_nation_data = []
    nation = queasy = None

    t_mapping_nation = None

    t_mapping_nation_data, T_mapping_nation = create_model("T_mapping_nation", {"nationvhp":string, "nationbe":string, "descr":string, "nr":int})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal t_mapping_nation_data, nation, queasy
        nonlocal bookengid


        nonlocal t_mapping_nation
        nonlocal t_mapping_nation_data

        return {"t-mapping-nation": t_mapping_nation_data}

    for nation in db_session.query(Nation).filter(
             (Nation.natcode == 0)).order_by(Nation.kurzbez).all():
        t_mapping_nation = T_mapping_nation()
        t_mapping_nation_data.append(t_mapping_nation)

        t_mapping_nation.nationvhp = nation.kurzbez
        t_mapping_nation.descr = entry(0, nation.bezeich, ";")
        t_mapping_nation.nr = nation.nationnr

        queasy = get_cache (Queasy, {"key": [(eq, 165)],"number1": [(eq, bookengid)],"number2": [(eq, nation.nationnr)]})

        if queasy:
            t_mapping_nation.nationbe = queasy.char2
        else:
            queasy = Queasy()
            db_session.add(queasy)

            queasy.key = 165
            queasy.number1 = bookengid
            queasy.number2 = nation.nationnr
            queasy.char1 = nation.kurzbez

    return generate_output()