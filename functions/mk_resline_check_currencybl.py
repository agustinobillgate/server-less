from functions.additional_functions import *
import decimal
from sqlalchemy import func
from models import Waehrung, Res_line, Reslin_queasy, Guest_pr, Queasy

def mk_resline_check_currencybl(inp_resno:int, reslinno:int, gastno:int, marknr:int, reslin_list_reserve_dec:decimal):
    w_waehrungsnr = 0
    w_reserve_dec = to_decimal("0.0")
    waehrung_wabkurz = ""
    waehrung = res_line = reslin_queasy = guest_pr = queasy = None

    waehrung1 = None

    Waehrung1 = create_buffer("Waehrung1",Waehrung)

    db_session = local_storage.db_session

    def generate_output():
        nonlocal w_waehrungsnr, w_reserve_dec, waehrung_wabkurz, waehrung, res_line, reslin_queasy, guest_pr, queasy
        nonlocal inp_resno, reslinno, gastno, marknr, reslin_list_reserve_dec
        nonlocal waehrung1


        nonlocal waehrung1
        return {"w_waehrungsnr": w_waehrungsnr, "w_reserve_dec": w_reserve_dec, "waehrung_wabkurz": waehrung_wabkurz}


    res_line = db_session.query(Res_line).filter(
             (Res_line.resnr == inp_resno) & (Res_line.reslinnr == reslinno)).first()

    reslin_queasy = db_session.query(Reslin_queasy).filter(
             (func.lower(Reslin_queasy.key) == ("arrangement").lower()) & (Reslin_queasy.resnr == inp_resno) & (Reslin_queasy.reslinnr == reslinno)).first()

    if not reslin_queasy:

        guest_pr = db_session.query(Guest_pr).filter(
                 (Guest_pr.gastnr == gastno)).first()

        if not guest_pr:

            return generate_output()

        if marknr != 0:

            queasy = db_session.query(Queasy).filter(
                     (Queasy.key == 18) & (Queasy.number1 == marknr)).first()

            if not queasy or (queasy and queasy.char3 == ""):

                queasy = db_session.query(Queasy).filter(
                         (Queasy.key == 2) & (Queasy.char1 == guest_pr.code)).first()
        else:

            queasy = db_session.query(Queasy).filter(
                     (Queasy.key == 2) & (Queasy.char1 == guest_pr.code)).first()

        if queasy:

            if queasy.key == 18:

                waehrung1 = db_session.query(Waehrung1).filter(
                         (Waehrung1.wabkurz == queasy.char3)).first()
            else:

                waehrung1 = db_session.query(Waehrung1).filter(
                         (Waehrung1.waehrungsnr == queasy.number1)).first()

            if waehrung1 and waehrung1.waehrungsnr != res_line.betriebsnr:
                res_line.betriebsnr = waehrung1.waehrungsnr
                w_waehrungsnr = waehrung1.waehrungsnr

                if reslin_list_reserve_dec != 0:
                    res_line.reserve_dec =  to_decimal(waehrung1.ankauf) / to_decimal(waehrung1.einheit)
                    w_reserve_dec =  to_decimal(waehrung1.ankauf) / to_decimal(waehrung1.einheit)
                waehrung_wabkurz = waehrung1.wabkurz

    return generate_output()