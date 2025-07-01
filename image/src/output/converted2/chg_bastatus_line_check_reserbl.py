#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import Bk_reser

def chg_bastatus_line_check_reserbl(r_recid:int, sorttype:int):

    prepare_cache ([Bk_reser])

    its_ok = True
    bk_reser = None

    resline = None

    Resline = create_buffer("Resline",Bk_reser)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal its_ok, bk_reser
        nonlocal r_recid, sorttype
        nonlocal resline


        nonlocal resline

        return {"its_ok": its_ok}


    bk_reser = get_cache (Bk_reser, {"_recid": [(eq, r_recid)]})

    if bk_reser:

        resline = db_session.query(Resline).filter(
                 (Resline.datum == bk_reser.datum) & (Resline.raum == bk_reser.raum) & (((Resline.von_i >= bk_reser.von_i) & (Resline.von_i <= bk_reser.bis_i)) | ((Resline.bis_i >= bk_reser.von_i) & (Resline.bis_i <= bk_reser.bis_i)) | ((bk_reser.von_i >= Resline.von_i) & (bk_reser.bis_i <= Resline.bis_i))) & ((Resline._recid != bk_reser._recid)) & (Resline.resstatus == sorttype)).first()

        if resline:

            if resline.resstatus == 1:
                its_ok = False

                return generate_output()

            if resline.resstatus == 2:
                its_ok = False

                return generate_output()

    return generate_output()