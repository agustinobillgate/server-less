from functions.additional_functions import *
import decimal
from models import L_segment, L_lieferant

def segment_admin_btn_delartbl(l_segmentcode:int):
    flag = 0
    l_segment = l_lieferant = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal flag, l_segment, l_lieferant


        return {"flag": flag}


    l_segment = db_session.query(L_segment).filter(
            (l_segmentcode == l_segmentcode)).first()

    l_lieferant = db_session.query(L_lieferant).filter(
            (L_lieferant.segment1 == l_segmentcode)).first()

    if l_artikel:
        flag = 1
    else:

        l_segment = db_session.query(L_segment).first()
        db_session.delete(l_segment)

    return generate_output()