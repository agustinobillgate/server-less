#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Mhis_line

def mhis_line_btn_exitbl(curr_nr:int, m_list_datum:date, m_list_cost:Decimal, remark_screen_value:string):

    prepare_cache ([Mhis_line])

    rec_id = 0
    mhis_line = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal rec_id, mhis_line
        nonlocal curr_nr, m_list_datum, m_list_cost, remark_screen_value

        return {"rec_id": rec_id}

    mhis_line = Mhis_line()
    db_session.add(mhis_line)

    mhis_line.nr = curr_nr
    mhis_line.datum = m_list_datum
    mhis_line.cost =  to_decimal(m_list_cost)
    mhis_line.remark = remark_screen_value
    pass
    rec_id = mhis_line._recid

    return generate_output()