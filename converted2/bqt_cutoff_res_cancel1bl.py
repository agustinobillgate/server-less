#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import Bk_veran, Bk_reser, Guest, Bk_raum

def bqt_cutoff_res_cancel1bl(pvilanguage:int, o_resnr:int, o_reslinnr:int):

    prepare_cache ([Bk_veran, Bk_reser, Guest, Bk_raum])

    msg_str = ""
    msg_strq = ""
    recid_bk_reser = 0
    lvcarea:string = "bqt-cutoff"
    gname:string = ""
    bk_veran = bk_reser = guest = bk_raum = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal msg_str, msg_strq, recid_bk_reser, lvcarea, gname, bk_veran, bk_reser, guest, bk_raum
        nonlocal pvilanguage, o_resnr, o_reslinnr

        return {"msg_str": msg_str, "msg_strq": msg_strq, "recid_bk_reser": recid_bk_reser}


    bk_veran = get_cache (Bk_veran, {"veran_nr": [(eq, o_resnr)]})

    if not bk_veran:

        return generate_output()

    if (bk_veran.deposit_payment[0] + bk_veran.deposit_payment[1] + bk_veran.deposit_payment[2] + bk_veran.deposit_payment[3] + bk_veran.deposit_payment[4] + bk_veran.deposit_payment[5] + bk_veran.deposit_payment[6] + bk_veran.deposit_payment[7] + bk_veran.deposit_payment[8]) > 0:

        bk_reser = get_cache (Bk_reser, {"veran_nr": [(eq, bk_veran.veran_nr)],"veran_resnr": [(ne, o_reslinnr)],"resstatus": [(eq, 1)]})

        if not bk_reser:
            msg_str = translateExtended ("Deposit exists, cancel reservation not possible.", lvcarea, "")

            return generate_output()

    if bk_veran.rechnr > 0:

        bk_reser = get_cache (Bk_reser, {"veran_nr": [(eq, bk_veran.veran_nr)],"veran_resnr": [(ne, o_reslinnr)],"resstatus": [(eq, 1)]})

        if not bk_reser:
            msg_str = translateExtended ("Bill exists, cancel reservation not possible.", lvcarea, "")

            return generate_output()

    guest = get_cache (Guest, {"gastnr": [(eq, bk_veran.gastnr)]})

    if guest:
        gname = guest.name

    bk_reser = get_cache (Bk_reser, {"veran_nr": [(eq, o_resnr)],"veran_seite": [(eq, o_reslinnr)]})

    if bk_reser:

        bk_raum = get_cache (Bk_raum, {"raum": [(eq, bk_reser.raum)]})

        if bk_raum:
            msg_strq = "&Q" + translateExtended ("Do you really want to delete reservation of", lvcarea, "") + chr_unicode(10) + gname + " - " + translateExtended ("Room:", lvcarea, "") + " " + bk_raum.bezeich + chr_unicode(10) + translateExtended ("Date:", lvcarea, "") + " " + to_string(bk_reser.datum) + " - " + to_string(bk_reser.bis_datum) + " " + translateExtended ("Time:", lvcarea, "") + " " + to_string(bk_reser.von_zeit, "99:99") + " - " + to_string(bk_reser.bis_zeit, "99:99") + "?"
        recid_bk_reser = bk_reser._recid

    return generate_output()