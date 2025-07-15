#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import Mhis_line, Mathis

def prepare_mhis_linebl(curr_nr:int):

    prepare_cache ([Mathis])

    b_tittle = ""
    t_mhis_line_data = []
    mhis_line = mathis = None

    t_mhis_line = None

    t_mhis_line_data, T_mhis_line = create_model_like(Mhis_line, {"rec_id":int})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal b_tittle, t_mhis_line_data, mhis_line, mathis
        nonlocal curr_nr


        nonlocal t_mhis_line
        nonlocal t_mhis_line_data

        return {"b_tittle": b_tittle, "t-mhis-line": t_mhis_line_data}

    mathis = get_cache (Mathis, {"nr": [(eq, curr_nr)]})

    if mathis:
        b_tittle = mathis.name + " - " + b_tittle

    for mhis_line in db_session.query(Mhis_line).filter(
             (Mhis_line.nr == curr_nr)).order_by(Mhis_line._recid).all():
        t_mhis_line = T_mhis_line()
        t_mhis_line_data.append(t_mhis_line)

        buffer_copy(mhis_line, t_mhis_line)
        t_mhis_line.rec_id = mhis_line._recid

    return generate_output()