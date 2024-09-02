from functions.additional_functions import *
import decimal
from models import Fa_artikel, Mathis

def fa_artlist_find_new_artnrbl(endkum:int, zwkum:int):
    new_artnr = 0
    fa_artikel = mathis = None

    fa_art1 = mhis = None

    Fa_art1 = Fa_artikel
    Mhis = Mathis

    db_session = local_storage.db_session

    def generate_output():
        nonlocal new_artnr, fa_artikel, mathis
        nonlocal fa_art1, mhis


        nonlocal fa_art1, mhis
        return {"new_artnr": new_artnr}


    fa_art1_obj_list = []
    for fa_art1, mhis in db_session.query(Fa_art1, Mhis).join(Mhis,(Mhis.nr == Fa_art1.nr)).filter(
            (Fa_art1.subgrp == zwkum) &  (Fa_art1.gnr == endkum)).all():
        if fa_art1._recid in fa_art1_obj_list:
            continue
        else:
            fa_art1_obj_list.append(fa_art1._recid)


        new_artnr = to_int(mhis.asset) + 1

        return generate_output()
    new_artnr = endkum * 10000000 + zwkum * 10000 + 1

    return generate_output()