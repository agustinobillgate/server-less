from functions.additional_functions import *
import decimal
from models import Brief

def read_briefbl(briefno:int, grpno:int):
    t_brief_list = []
    brief = None

    t_brief = None

    t_brief_list, T_brief = create_model_like(Brief)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal t_brief_list, brief


        nonlocal t_brief
        nonlocal t_brief_list
        return {"t-brief": t_brief_list}

    if briefno != 0 and (grpno == 0 or grpno == None):

        brief = db_session.query(Brief).filter(
                (Briefnr == briefno)).first()

        if brief:
            t_brief = T_brief()
            t_brief_list.append(t_brief)

            buffer_copy(brief, t_brief)

    elif grpno != 0:

        if briefno != 0:

            brief = db_session.query(Brief).filter(
                    (Briefkateg == grpno) &  (Briefnr == briefno)).first()

            if brief:
                t_brief = T_brief()
                t_brief_list.append(t_brief)

                buffer_copy(brief, t_brief)
        else:

            for brief in db_session.query(Brief).filter(
                    (Briefkateg == grpno)).all():
                t_brief = T_brief()
                t_brief_list.append(t_brief)

                buffer_copy(brief, t_brief)

    return generate_output()