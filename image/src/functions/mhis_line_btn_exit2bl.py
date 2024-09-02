from functions.additional_functions import *
import decimal
from datetime import date
from models import Mhis_line

def mhis_line_btn_exit2bl(rec_id:int, m_list_datum:date, m_list_cost:decimal, remark_screen_value:str):
    mhis_line = None

    mhis_line1 = None

    Mhis_line1 = Mhis_line

    db_session = local_storage.db_session

    def generate_output():
        nonlocal mhis_line
        nonlocal mhis_line1


        nonlocal mhis_line1
        return {}


    mhis_line1 = db_session.query(Mhis_line1).filter(
            (Mhis_line1._recid == rec_id)).first()
    mhis_line1.datum = m_list_datum
    mhis_line1.cost = m_list_cost
    mhis_line1.remark = remark_screen_value

    mhis_line1 = db_session.query(Mhis_line1).first()

    return generate_output()