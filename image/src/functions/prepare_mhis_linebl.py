from functions.additional_functions import *
import decimal
from models import Mhis_line, Mathis

def prepare_mhis_linebl(curr_nr:int):
    b_tittle = ""
    t_mhis_line_list = []
    mhis_line = mathis = None

    t_mhis_line = None

    t_mhis_line_list, T_mhis_line = create_model_like(Mhis_line, {"rec_id":int})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal b_tittle, t_mhis_line_list, mhis_line, mathis


        nonlocal t_mhis_line
        nonlocal t_mhis_line_list
        return {"b_tittle": b_tittle, "t-mhis-line": t_mhis_line_list}

    mathis = db_session.query(Mathis).filter(
            (Mathis.nr == curr_nr)).first()
    b_tittle = mathis.name + " - " + b_tittle

    for mhis_line in db_session.query(Mhis_line).filter(
            (Mhis_line.nr == curr_nr)).all():
        t_mhis_line = T_mhis_line()
        t_mhis_line_list.append(t_mhis_line)

        buffer_copy(mhis_line, t_mhis_line)
        t_mhis_line.rec_id = mhis_line._recid

    return generate_output()