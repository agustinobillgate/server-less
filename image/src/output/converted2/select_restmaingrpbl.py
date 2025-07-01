#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import Wgrpgen

def select_restmaingrpbl():

    prepare_cache ([Wgrpgen])

    t_wgrpgen_list = []
    wgrpgen = None

    t_wgrpgen = None

    t_wgrpgen_list, T_wgrpgen = create_model("T_wgrpgen", {"eknr":int, "bezeich":string})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal t_wgrpgen_list, wgrpgen


        nonlocal t_wgrpgen
        nonlocal t_wgrpgen_list

        return {"t-wgrpgen": t_wgrpgen_list}

    for wgrpgen in db_session.query(Wgrpgen).order_by(Wgrpgen._recid).all():
        t_wgrpgen = T_wgrpgen()
        t_wgrpgen_list.append(t_wgrpgen)

        t_wgrpgen.eknr = wgrpgen.eknr
        t_wgrpgen.bezeich = wgrpgen.bezeich

    return generate_output()