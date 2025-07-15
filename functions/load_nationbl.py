#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import Nation

def load_nationbl(case_type:int):
    t_nation_data = []
    nation = None

    t_nation = None

    t_nation_data, T_nation = create_model_like(Nation)

    db_session = local_storage.db_session

    def generate_output():
        nonlocal t_nation_data, nation
        nonlocal case_type


        nonlocal t_nation
        nonlocal t_nation_data

        return {"t-nation": t_nation_data}

    if case_type == 1:

        for nation in db_session.query(Nation).order_by(Nation._recid).all():
            t_nation = T_nation()
            t_nation_data.append(t_nation)

            buffer_copy(nation, t_nation)

    return generate_output()