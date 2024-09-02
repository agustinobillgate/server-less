from functions.additional_functions import *
import decimal
from models import Briefzei

def read_briefzeibl(case_type:int, briefno:int, zeileno:int):
    t_briefzei_list = []
    briefzei = None

    t_briefzei = None

    t_briefzei_list, T_briefzei = create_model_like(Briefzei)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal t_briefzei_list, briefzei


        nonlocal t_briefzei
        nonlocal t_briefzei_list
        return {"t-briefzei": t_briefzei_list}

    if case_type == 1:

        briefzei = db_session.query(Briefzei).filter(
                (Briefzei.briefnr == briefno) &  (Briefzeilnr == zeileno)).first()

        if briefzei:
            t_briefzei = T_briefzei()
            t_briefzei_list.append(t_briefzei)

            buffer_copy(briefzei, t_briefzei)
    elif case_type == 2:

        for briefzei in db_session.query(Briefzei).filter(
                (Briefzei.briefnr == briefno)).all():
            t_briefzei = T_briefzei()
            t_briefzei_list.append(t_briefzei)

            buffer_copy(briefzei, t_briefzei)

    return generate_output()