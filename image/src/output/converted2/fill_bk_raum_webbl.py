from functions.additional_functions import *
import decimal
from sqlalchemy import func
from models import Bk_raum

bk_list_list, Bk_list = create_model_like(Bk_raum, {"rec_id":int})

def fill_bk_raum_webbl(curr_select:str, t_raum:str, bk_list_list:[Bk_list]):
    recid_raum = 0
    bk_raum = None

    bk_list = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal recid_raum, bk_raum
        nonlocal curr_select, t_raum


        nonlocal bk_list
        nonlocal bk_list_list
        return {"recid_raum": recid_raum}

    bk_list = query(bk_list_list, first=True)

    if curr_select.lower()  == ("add").lower() :
        bk_raum = Bk_raum()
        db_session.add(bk_raum)

        buffer_copy(bk_list, bk_raum)

        bk_raum = db_session.query(Bk_raum).filter(
                 (Bk_raum.raum == bk_list.raum)).first()

        if bk_raum:
            recid_raum = bk_raum._recid

    elif curr_select.lower()  == ("chg").lower() :

        bk_raum = db_session.query(Bk_raum).filter(
                 (func.lower(Bk_raum.raum) == (t_raum).lower())).first()
        buffer_copy(bk_list, bk_raum)

    return generate_output()