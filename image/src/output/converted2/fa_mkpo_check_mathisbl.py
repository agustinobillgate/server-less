#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import Mathis

t_mathis_list, T_mathis = create_model_like(Mathis)

def fa_mkpo_check_mathisbl(art_nr:int, t_mathis_list:[T_mathis]):
    avail_mathis = True
    mathis = None

    t_mathis = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal avail_mathis, mathis
        nonlocal art_nr


        nonlocal t_mathis

        return {"avail_mathis": avail_mathis, "t-mathis": t_mathis_list}

    mathis = get_cache (Mathis, {"nr": [(eq, art_nr)]})

    if not mathis:
        avail_mathis = False

    for mathis in db_session.query(Mathis).filter(
             (Mathis.nr == art_nr)).order_by(Mathis._recid).all():
        t_mathis = T_mathis()
        t_mathis_list.append(t_mathis)

        buffer_copy(mathis, t_mathis)

    return generate_output()