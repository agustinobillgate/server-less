#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import Bk_raum

bk_list_list, Bk_list = create_model_like(Bk_raum, {"rec_id":int})

def fill_bk_raum_webbl(curr_select:string, t_raum:string, bk_list_list:[Bk_list]):

    prepare_cache ([Bk_raum])

    recid_raum = 0
    bk_raum = None

    bk_list = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal recid_raum, bk_raum
        nonlocal curr_select, t_raum


        nonlocal bk_list

        return {"recid_raum": recid_raum}

    bk_list = query(bk_list_list, first=True)

    if curr_select.lower()  == ("add").lower() :
        bk_raum = Bk_raum()
        db_session.add(bk_raum)

        buffer_copy(bk_list, bk_raum)

        bk_raum = get_cache (Bk_raum, {"raum": [(eq, bk_list.raum)]})

        if bk_raum:
            recid_raum = bk_raum._recid

    elif curr_select.lower()  == ("chg").lower() :

        bk_raum = get_cache (Bk_raum, {"raum": [(eq, t_raum)]})
        pass
        buffer_copy(bk_list, bk_raum)
        pass

    return generate_output()