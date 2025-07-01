#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal

def delete_eventbl(case_type:int, block_id:string, nr:int):
    success_flag = False

    db_session = local_storage.db_session

    def generate_output():
        nonlocal success_flag
        nonlocal case_type, block_id, nr

        return {"success_flag": success_flag}


    if case_type == 1:

        bk_event = db_session.query(Bk_event).filter(
                 (Bk_event.block_id == (block_id).lower()) & (Bk_event.nr == nr)).first()

        if bk_event:

            bk_event_detail = db_session.query(Bk_event_detail).filter(
                     (Bk_event_detail.block_id == bk_event.block_id) & (Bk_event_detail.nr == bk_event.nr)).first()

            if bk_event_detail:
                bk_event_detail_list.remove(bk_event_detail)
                pass
            bk_event_list.remove(bk_event)
            pass
            success_flag = True

    return generate_output()