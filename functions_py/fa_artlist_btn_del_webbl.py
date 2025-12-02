#using conversion tools version: 1.0.0.117

# ==================================
# Rulita, 27-11-2025
# - Added with_for_update all query 
# ==================================

from functions.additional_functions import *
from decimal import Decimal
from models import Mathis, Fa_artikel, Queasy

def fa_artlist_btn_del_webbl(mathis_nr:int):
    mathis = fa_artikel = queasy = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal mathis, fa_artikel, queasy
        nonlocal mathis_nr

        return {}


    # mathis = get_cache (Mathis, {"nr": [(eq, mathis_nr)]})
    mathis = db_session.query(Mathis).filter(
             (Mathis.nr == mathis_nr)).with_for_update().first()

    if mathis:
        # pass
        db_session.delete(mathis)
        # pass
        db_session.refresh(mathis,with_for_update=True)

        # fa_artikel = get_cache (Fa_artikel, {"nr": [(eq, mathis_nr)]})
        fa_artikel = db_session.query(Fa_artikel).filter(
                 (Fa_artikel.nr == mathis_nr)).with_for_update().first()

        if fa_artikel:
            # pass
            db_session.delete(fa_artikel)
            # pass
            db_session.refresh(fa_artikel,with_for_update=True)

        # queasy = get_cache (Queasy, {"key": [(eq, 314)],"number1": [(eq, mathis_nr)]})
        queasy = db_session.query(Queasy).filter(
                 (Queasy.key == 314) & (Queasy.number1 == mathis_nr)).with_for_update().first()

        if queasy:
            # pass
            db_session.delete(queasy)
            # pass
            db_session.refresh(queasy,with_for_update=True)

    return generate_output()
