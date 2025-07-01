#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import Briefzei

def read_briefzeibl(case_type:int, briefno:int, zeileno:int):
    t_briefzei_list = []
    briefzei = None

    t_briefzei = None

    t_briefzei_list, T_briefzei = create_model_like(Briefzei)

    db_session = local_storage.db_session

    def generate_output():
        nonlocal t_briefzei_list, briefzei
        nonlocal case_type, briefno, zeileno


        nonlocal t_briefzei
        nonlocal t_briefzei_list

        return {"t-briefzei": t_briefzei_list}

    if case_type == 1:

        briefzei = get_cache (Briefzei, {"briefnr": [(eq, briefno)],"briefzeilnr": [(eq, zeileno)]})

        if briefzei:
            t_briefzei = T_briefzei()
            t_briefzei_list.append(t_briefzei)

            buffer_copy(briefzei, t_briefzei)
    elif case_type == 2:

        for briefzei in db_session.query(Briefzei).filter(
                 (Briefzei.briefnr == briefno)).order_by(Briefzei._recid).all():
            t_briefzei = T_briefzei()
            t_briefzei_list.append(t_briefzei)

            buffer_copy(briefzei, t_briefzei)

    return generate_output()