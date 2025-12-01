#using conversion tools version: 1.0.0.117
#-------------------------------------------------------
# Rd, 28/11/2025, with_for_update added
#-------------------------------------------------------
from functions.additional_functions import *
from decimal import Decimal
from models import Bk_raum

bk_list_data, Bk_list = create_model_like(Bk_raum, {"rec_id":int})

def fill_bk_raum_webbl(curr_select:string, t_raum:string, bk_list_data:[Bk_list]):

    prepare_cache ([Bk_raum])

    recid_raum = 0
    bk_raum = None

    bk_list = None

    db_session = local_storage.db_session
    t_raum = t_raum.strip()
    curr_select = curr_select.strip()

    def generate_output():
        nonlocal recid_raum, bk_raum
        nonlocal curr_select, t_raum


        nonlocal bk_list

        return {"recid_raum": recid_raum}

    bk_list = query(bk_list_data, first=True)

    if curr_select.lower()  == ("add").lower() :
        bk_raum = Bk_raum()
        db_session.add(bk_raum)

        buffer_copy(bk_list, bk_raum)

        bk_raum = get_cache (Bk_raum, {"raum": [(eq, bk_list.raum)]})

        if bk_raum:
            recid_raum = bk_raum._recid

    elif curr_select.lower()  == ("chg").lower() :

        # bk_raum = get_cache (Bk_raum, {"raum": [(eq, t_raum)]})
        bk_raum = db_session.query(Bk_raum).filter(Bk_raum.raum == t_raum).with_for_update().first()
        buffer_copy(bk_list, bk_raum)

    return generate_output()