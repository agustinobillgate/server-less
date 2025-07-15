#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import Wgrpdep

def select_restsubgrbl(dept:int):

    prepare_cache ([Wgrpdep])

    t_wgrpdep_data = []
    wgrpdep = None

    t_wgrpdep = None

    t_wgrpdep_data, T_wgrpdep = create_model("T_wgrpdep", {"zknr":int, "bezeich":string})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal t_wgrpdep_data, wgrpdep
        nonlocal dept


        nonlocal t_wgrpdep
        nonlocal t_wgrpdep_data

        return {"t-wgrpdep": t_wgrpdep_data}

    for wgrpdep in db_session.query(Wgrpdep).filter(
             (Wgrpdep.departement == dept)).order_by(Wgrpdep._recid).all():
        t_wgrpdep = T_wgrpdep()
        t_wgrpdep_data.append(t_wgrpdep)

        t_wgrpdep.zknr = wgrpdep.zknr
        t_wgrpdep.bezeich = wgrpdep.bezeich

    return generate_output()