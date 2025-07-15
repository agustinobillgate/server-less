#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import Queasy

def kitchen_display_update_statusbl(qhead_recid:int, status_nr:int):

    prepare_cache ([Queasy])

    ok_flag = False
    queasy = None

    q_kds_head = q_kds_line = None

    Q_kds_head = create_buffer("Q_kds_head",Queasy)
    Q_kds_line = create_buffer("Q_kds_line",Queasy)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal ok_flag, queasy
        nonlocal qhead_recid, status_nr
        nonlocal q_kds_head, q_kds_line


        nonlocal q_kds_head, q_kds_line

        return {"ok_flag": ok_flag}


    q_kds_head = get_cache (Queasy, {"_recid": [(eq, qhead_recid)]})

    if q_kds_head:
        pass
        q_kds_head.deci2 =  to_decimal(status_nr)
        pass
        pass

        for q_kds_line in db_session.query(Q_kds_line).filter(
                 (Q_kds_line.key == 255) & (Q_kds_line.deci2 == qhead_recid)).order_by(Q_kds_line._recid).all():
            q_kds_line.char3 = "1"
        ok_flag = True
    else:
        ok_flag = False

    return generate_output()