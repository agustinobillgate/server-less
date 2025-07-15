#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import L_segment, L_kredit

def ap_list_trigbl(case_type:int, int1:int):

    prepare_cache ([L_segment, L_kredit])

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

        l_segment = get_cache (L_segment, {"l_segmentcode": [(eq, int1)]})

        if l_segment:
            char1 = l_segment.l_bezeich
            fl_avail = True

    elif case_type == 2:

        l_kredit = get_cache (L_kredit, {"_recid": [(eq, int1)]})

        if l_kredit.opart == 2:
            fl_avail = True
        int2 = l_kredit.lief_nr

    return generate_output()