#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import Hoteldpt, Htparam

def prepare_copy_hartikelbl():

    prepare_cache ([Htparam])

    p_852 = 0
    t_hoteldpt_list = []
    hoteldpt = htparam = None

    t_hoteldpt = None

    t_hoteldpt_list, T_hoteldpt = create_model_like(Hoteldpt)

    db_session = local_storage.db_session

    def generate_output():
        nonlocal p_852, t_hoteldpt_list, hoteldpt, htparam


        nonlocal t_hoteldpt
        nonlocal t_hoteldpt_list

        return {"p_852": p_852, "t-hoteldpt": t_hoteldpt_list}

    for hoteldpt in db_session.query(Hoteldpt).order_by(Hoteldpt._recid).all():
        t_hoteldpt = T_hoteldpt()
        t_hoteldpt_list.append(t_hoteldpt)

        buffer_copy(hoteldpt, t_hoteldpt)

    htparam = get_cache (Htparam, {"paramnr": [(eq, 852)]})
    p_852 = htparam.finteger

    return generate_output()