#using conversion tools version: 1.0.0.117
#-----------------------------------------
# Rd 4/8/2025
# if available, bezeichnung
#-----------------------------------------
from functions.additional_functions import *
from decimal import Decimal
from models import Artikel, Argt_line, Arrangement

def nsargt_admin_btn_delbl(rec_id:int, q1_list_argtnr:int):

    prepare_cache ([Artikel])

    err = 0
    art_dept = 0
    art_bez = ""
    artikel = argt_line = arrangement = None

    artikel1 = None

    Artikel1 = create_buffer("Artikel1",Artikel)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal err, art_dept, art_bez, artikel, argt_line, arrangement
        nonlocal rec_id, q1_list_argtnr
        nonlocal artikel1


        nonlocal artikel1

        return {"err": err, "art_dept": art_dept, "art_bez": art_bez}


    artikel1 = get_cache (Artikel, {"artart": [(eq, 0)],"artgrp": [(eq, q1_list_argtnr)]})

    if artikel1:
        err = 1
        art_dept = artikel1.departement
        art_bez = artikel1.bezeich

        return generate_output()

    for argt_line in db_session.query(Argt_line).filter(
             (Argt_line.argtnr == q1_list_argtnr)).order_by(Argt_line._recid).all():
        db_session.delete(argt_line)
    pass

    arrangement = get_cache (Arrangement, {"_recid": [(eq, rec_id)]})
    # Rd 4/8/2025
    # if available
    if arrangement:
        db_session.delete(arrangement)
    pass

    return generate_output()