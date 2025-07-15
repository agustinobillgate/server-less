#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Mhis_line

def mhis_line_btn_exit2bl(rec_id:int, m_list_datum:date, m_list_cost:Decimal, remark_screen_value:string):

    prepare_cache ([Mhis_line])

    mhis_line = None

    mhis_line1 = None

    Mhis_line1 = create_buffer("Mhis_line1",Mhis_line)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal mhis_line
        nonlocal rec_id, m_list_datum, m_list_cost, remark_screen_value
        nonlocal mhis_line1


        nonlocal mhis_line1

        return {}


    mhis_line1 = get_cache (Mhis_line, {"_recid": [(eq, rec_id)]})
    mhis_line1.datum = m_list_datum
    mhis_line1.cost =  to_decimal(m_list_cost)
    mhis_line1.remark = remark_screen_value
    pass

    return generate_output()