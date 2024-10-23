from functions.additional_functions import *
import decimal
from sqlalchemy import func
from models import Res_line, Reslin_queasy, Arrangement

def copy_fixedrate(resnr:int, reslinnr:int):
    res_line = reslin_queasy = arrangement = None

    resmember = rqueasy = None

    Resmember = create_buffer("Resmember",Res_line)
    Rqueasy = create_buffer("Rqueasy",Reslin_queasy)

    db_session = local_storage.db_session

    def generate_output():
        nonlocal res_line, reslin_queasy, arrangement
        nonlocal resnr, reslinnr
        nonlocal resmember, rqueasy


        nonlocal resmember, rqueasy
        return {}


    res_line = db_session.query(Res_line).filter(
             (Res_line.resnr == resnr) & (Res_line.reslinnr == reslinnr)).first()

    arrangement = db_session.query(Arrangement).filter(
             (Arrangement.arrangement == res_line.arrangement)).first()

    resmember = db_session.query(Resmember).filter(
             (Resmember.resnr == resnr) & (Resmember.reslinnr != reslinnr) & (res_line.active_flag != 2) & (Resmember.resstatus != 12) & (Resmember.resstatus != 11) & (Resmember.resstatus != 13) & (Resmember.arrangement == res_line.arrangement)).first()
    while None != resmember:
        resmember.zipreis =  to_decimal(res_line.zipreis)
        resmember.betriebsnr = res_line.betriebsnr
        resmember.reserve_dec =  to_decimal(res_line.reserve_dec)

        for rqueasy in db_session.query(Rqueasy).filter(
                 (func.lower(Rqueasy.key) == ("fargt-line").lower()) & (Rqueasy.char1 == "") & (Rqueasy.resnr == resnr) & (Rqueasy.number2 == arrangement.argtnr) & (Rqueasy.reslinnr == resmember.reslinnr)).order_by(Rqueasy._recid).all():
            rqueasy_list.remove(rqueasy)

        for reslin_queasy in db_session.query(Reslin_queasy).filter(
                 (func.lower(Reslin_queasy.key) == ("fargt-line").lower()) & (Reslin_queasy.char1 == "") & (Reslin_queasy.resnr == resnr) & (Reslin_queasy.number2 == arrangement.argtnr) & (Reslin_queasy.reslinnr == reslinnr)).order_by(Reslin_queasy._recid).all():
            rqueasy = Rqueasy()
            db_session.add(rqueasy)

            rqueasy.key = "fargt-line"
            rqueasy.number1 = reslin_queasy.number1
            rqueasy.number2 = reslin_queasy.number2
            rqueasy.number3 = reslin_queasy.number3
            rqueasy.resnr = resnr
            rqueasy.reslinnr = resmember.reslinnr
            rqueasy.deci1 =  to_decimal(reslin_queasy.deci1)
            rqueasy.date1 = reslin_queasy.date1
            rqueasy.date2 = reslin_queasy.date2

        for rqueasy in db_session.query(Rqueasy).filter(
                 (func.lower(Rqueasy.key) == ("arrangement").lower()) & (Rqueasy.resnr == resnr) & (Rqueasy.reslinnr == resmember.reslinnr)).order_by(Rqueasy._recid).all():
            rqueasy_list.remove(rqueasy)

        for reslin_queasy in db_session.query(Reslin_queasy).filter(
                 (func.lower(Reslin_queasy.key) == ("arrangement").lower()) & (Reslin_queasy.resnr == resnr) & (Reslin_queasy.reslinnr == reslinnr)).order_by(Reslin_queasy._recid).all():
            rqueasy = Rqueasy()
            db_session.add(rqueasy)

            rqueasy.key = "arrangement"
            rqueasy.resnr = resnr
            rqueasy.reslinnr = resmember.reslinnr
            rqueasy.deci1 =  to_decimal(reslin_queasy.deci1)
            rqueasy.date1 = reslin_queasy.date1
            rqueasy.date2 = reslin_queasy.date2
            rqueasy.char1 = reslin_queasy.char1
            rqueasy.number3 = reslin_queasy.number3

        curr_recid = resmember._recid
        resmember = db_session.query(Resmember).filter(
                 (Resmember.resnr == resnr) & (Resmember.reslinnr != reslinnr) & (res_line.active_flag != 2) & (Resmember.resstatus != 12) & (Resmember.resstatus != 11) & (Resmember.resstatus != 13) & (Resmember.arrangement == res_line.arrangement)).filter(Resmember._recid > curr_recid).first()

    return generate_output()