from functions.additional_functions import *
import decimal
from sqlalchemy import func
from models import Waehrung, Res_line, Guest_pr, Reslin_queasy, Queasy

def res_rmrate_check_currencybl(pvilanguage:int, resnr:int, reslinnr:int, contcode:str):
    msg_str = ""
    lvcarea:str = "res_rmrate"
    waehrung = res_line = guest_pr = reslin_queasy = queasy = None

    waehrung1 = resline = rline = None

    Waehrung1 = Waehrung
    Resline = Res_line
    Rline = Res_line

    db_session = local_storage.db_session

    def generate_output():
        nonlocal msg_str, lvcarea, waehrung, res_line, guest_pr, reslin_queasy, queasy
        nonlocal waehrung1, resline, rline


        nonlocal waehrung1, resline, rline
        return {"msg_str": msg_str}

    def check_currency():

        nonlocal msg_str, lvcarea, waehrung, res_line, guest_pr, reslin_queasy, queasy
        nonlocal waehrung1, resline, rline


        nonlocal waehrung1, resline, rline


        Rline = Res_line

        reslin_queasy = db_session.query(Reslin_queasy).filter(
                (func.lower(Reslin_queasy.key) == "arrangement") &  (Reslin_queasy.resnr == resnr) &  (Reslin_queasy.reslinnr == reslinnr)).first()

        if not reslin_queasy:

            if not guest_pr:

                return

            queasy = db_session.query(Queasy).filter(
                    (Queasy.key == 2) &  (func.lower(Queasy.char1) == (contcode).lower())).first()

            if queasy and queasy.number1 != 0:

                waehrung1 = db_session.query(Waehrung1).filter(
                        (Waehrung1.waehrungsnr == queasy.number1)).first()

                if waehrung1 and waehrung1.waehrungsnr != res_line.betriebsnr:

                    rline = db_session.query(Rline).filter(
                            (Rline._recid == res_line._recid)).first()

                    if rline:
                        rline.betriebsnr = waehrung1.waehrungsnr

                        rline = db_session.query(Rline).first()
                        msg_str = msg_str + chr(2) + translateExtended ("No AdHoc Rates found; set back the currency code", lvcarea, "") + chr(10) + translateExtended ("to", lvcarea, "") + " " + waehrung1.bezeich + " " + translateExtended ("as defined in the contract rates.", lvcarea, "")


    res_line = db_session.query(Res_line).filter(
            (Res_line.resnr == resnr) &  (Res_line.reslinnr == reslinnr)).first()

    guest_pr = db_session.query(Guest_pr).filter(
            (Guest_pr.gastnr == res_line.gastnr)).first()

    return generate_output()