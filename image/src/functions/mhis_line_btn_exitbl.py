from functions.additional_functions import *
import decimal
from datetime import date
from models import Mhis_line

def mhis_line_btn_exitbl(curr_nr:int, m_list_datum:date, m_list_cost:decimal, remark_screen_value:str):
    rec_id = 0
    mhis_line = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal rec_id, mhis_line


        return {"rec_id": rec_id}

    mhis_line = Mhis_line()
    db_session.add(mhis_line)

    mhis_line.nr = curr_nr
    mhis_line.datum = m_list_datum
    mhis_line.cost = m_list_cost
    mhis_line.remark = remark_screen_value

    mhis_line = db_session.query(Mhis_line).first()
    rec_id = mhis_line._recid

    return generate_output()