#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import Wgrpgen

def select_restmaingrpbl():

    prepare_cache ([Wgrpgen])

    t_wgrpgen_data = []
    wgrpgen = None

    t_wgrpgen = None

    t_wgrpgen_data, T_wgrpgen = create_model("T_wgrpgen", {"eknr":int, "bezeich":string})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal t_wgrpgen_data, wgrpgen


        nonlocal t_wgrpgen
        nonlocal t_wgrpgen_data

        return {"t-wgrpgen": t_wgrpgen_data}

    for wgrpgen in db_session.query(Wgrpgen).order_by(Wgrpgen._recid).all():
        t_wgrpgen = T_wgrpgen()
        t_wgrpgen_data.append(t_wgrpgen)

        t_wgrpgen.eknr = wgrpgen.eknr
        t_wgrpgen.bezeich = wgrpgen.bezeich

    return generate_output()