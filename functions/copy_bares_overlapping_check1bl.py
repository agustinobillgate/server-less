#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Bk_reser

def copy_bares_overlapping_check1bl(pvilanguage:int, resnr:int, reslinnr:int, datum:date, raum:string, von_i:int, bis_i:int):

    prepare_cache ([Bk_reser])

    its_ok = True
    msg_str = ""
    lvcarea:string = "copy-bares"
    bk_reser = None

    resline = None

    Resline = create_buffer("Resline",Bk_reser)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal its_ok, msg_str, lvcarea, bk_reser
        nonlocal pvilanguage, resnr, reslinnr, datum, raum, von_i, bis_i
        nonlocal resline


        nonlocal resline

        return {"its_ok": its_ok, "msg_str": msg_str}


    bk_reser = get_cache (Bk_reser, {"veran_nr": [(eq, resnr)],"veran_resnr": [(eq, reslinnr)]})

    resline = db_session.query(Resline).filter(
             (Resline.datum == datum) & (Resline.raum == (raum).lower()) & (((Resline.von_i >= von_i) & (Resline.von_i <= bis_i)) | ((Resline.bis_i >= von_i) & (Resline.bis_i <= bis_i)) | ((von_i >= Resline.von_i) & (bis_i <= Resline.bis_i))) & (Resline.resstatus == bk_reser.resstatus)).first()

    if not resline:

        return generate_output()
    its_ok = False
    msg_str = "&W" + translateExtended ("Room already blocked for", lvcarea, "") + " " + to_string(datum) + chr_unicode(10) + translateExtended ("Starting:", lvcarea, "") + " " + to_string(resline.von_zeit, "99:99") + " " + translateExtended ("Ending:", lvcarea, "") + " " + to_string(resline.bis_zeit, "99:99") + chr_unicode(10) + translateExtended ("Status set to Waiting List", lvcarea, "")

    return generate_output()