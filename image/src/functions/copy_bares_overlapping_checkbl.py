from functions.additional_functions import *
import decimal
from datetime import date
from models import Bk_reser

def copy_bares_overlapping_checkbl(pvilanguage:int, resnr:int, reslinnr:int, datum:date, von_i:int, bis_i:int):
    its_ok = False
    msg_str = ""
    lvcarea:str = "copy_bares"
    bk_reser = None

    resline = None

    Resline = Bk_reser

    db_session = local_storage.db_session

    def generate_output():
        nonlocal its_ok, msg_str, lvcarea, bk_reser
        nonlocal resline


        nonlocal resline
        return {"its_ok": its_ok, "msg_str": msg_str}


    bk_reser = db_session.query(Bk_reser).filter(
            (Bk_reser.veran_nr == resnr) &  (Bk_reser.veran_resnr == reslinnr)).first()

    resline = db_session.query(Resline).filter(
            (Resline.datum == datum) &  (Resline.raum == bk_reser.raum) &  (((Resline.von_i >= von_i) &  (Resline.von_i <= bis_i)) |  ((Resline.bis_i >= von_i) &  (Resline.bis_i <= bis_i)) |  ((Resline.von_i >= Resline.von_i) &  (Resline.bis_i <= Resline.bis_i))) &  (Resline.resstatus == bk_reser.resstatus)).first()

    if not resline:

        return generate_output()
    its_ok = False
    msg_str = "&W" + translateExtended ("Room already blocked for", lvcarea, "") + " " + to_string(datum) + chr(10) + translateExtended ("Starting:", lvcarea, "") + " " + to_string(resline.von_zeit, "99:99") + " " + translateExtended ("Ending:", lvcarea, "") + " " + to_string(resline.bis_zeit, "99:99") + chr(10) + translateExtended ("Status set to Waiting List", lvcarea, "")

    return generate_output()