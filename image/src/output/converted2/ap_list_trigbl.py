from functions.additional_functions import *
import decimal
from models import L_segment, L_kredit

def ap_list_trigbl(case_type:int, int1:int):
    fl_avail = False
    char1 = ""
    int2 = 0
    l_segment = l_kredit = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal fl_avail, char1, int2, l_segment, l_kredit
        nonlocal case_type, int1


        return {"fl_avail": fl_avail, "char1": char1, "int2": int2}


    if case_type == 1:

        l_segment = db_session.query(L_segment).filter(
                 (L_segment.l_segmentcode == int1)).first()

        if l_segment:
            char1 = l_segment.l_bezeich
            fl_avail = True

    elif case_type == 2:

        l_kredit = db_session.query(L_kredit).filter(
                 (L_kredit._recid == int1)).first()

        if l_kredit.opart == 2:
            fl_avail = True
        int2 = l_kredit.lief_nr

    return generate_output()