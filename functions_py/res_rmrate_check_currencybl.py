#using conversion tools version: 1.0.0.117
#------------------------------------------
# Rd, 25/11/2025, with_for_update
#------------------------------------------
from functions.additional_functions import *
from decimal import Decimal
from models import Waehrung, Res_line, Guest_pr, Reslin_queasy, Queasy

def res_rmrate_check_currencybl(pvilanguage:int, resnr:int, reslinnr:int, contcode:string):

    prepare_cache ([Waehrung, Res_line, Queasy])

    msg_str = ""
    lvcarea:string = "res-rmrate"
    waehrung = res_line = guest_pr = reslin_queasy = queasy = None

    waehrung1 = resline = None

    Waehrung1 = create_buffer("Waehrung1",Waehrung)
    Resline = create_buffer("Resline",Res_line)

    db_session = local_storage.db_session
    contcode = contcode.strip()

    def generate_output():
        nonlocal msg_str, lvcarea, waehrung, res_line, guest_pr, reslin_queasy, queasy
        nonlocal pvilanguage, resnr, reslinnr, contcode
        nonlocal waehrung1, resline

        nonlocal waehrung1, resline

        return {"msg_str": msg_str}

    def check_currency():

        nonlocal msg_str, lvcarea, waehrung, res_line, guest_pr, reslin_queasy, queasy
        nonlocal pvilanguage, resnr, reslinnr, contcode
        nonlocal waehrung1, resline

        nonlocal waehrung1, resline

        rline = None
        Rline =  create_buffer("Rline",Res_line)

        reslin_queasy = get_cache (Reslin_queasy, {"key": [(eq, "arrangement")],"resnr": [(eq, resnr)],"reslinnr": [(eq, reslinnr)]})

        if not reslin_queasy:

            if not guest_pr:

                return

            queasy = get_cache (Queasy, {"key": [(eq, 2)],"char1": [(eq, contcode)]})

            if queasy and queasy.number1 != 0:

                waehrung1 = get_cache (Waehrung, {"waehrungsnr": [(eq, queasy.number1)]})

                if waehrung1 and waehrung1.waehrungsnr != res_line.betriebsnr:

                    # rline = get_cache (Res_line, {"_recid": [(eq, res_line._recid)]})
                    rline = db_session.query(Res_line).filter(Res_line._recid == res_line._recid).with_for_update().first()

                    if rline:
                        rline.betriebsnr = waehrung1.waehrungsnr


                        pass
                        msg_str = msg_str + chr_unicode(2) + translateExtended ("No AdHoc Rates found; set back the currency code", lvcarea, "") + chr_unicode(10) + translateExtended ("to", lvcarea, "") + " " + waehrung1.bezeich + " " + translateExtended ("as defined in the contract rates.", lvcarea, "")

    res_line = get_cache (Res_line, {"resnr": [(eq, resnr)],"reslinnr": [(eq, reslinnr)]})

    guest_pr = get_cache (Guest_pr, {"gastnr": [(eq, res_line.gastnr)]})

    return generate_output()