#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import Res_line, Reslin_queasy, Arrangement

def copy_fixedrate(resnr:int, reslinnr:int):

    prepare_cache ([Arrangement])

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


    res_line = get_cache (Res_line, {"resnr": [(eq, resnr)],"reslinnr": [(eq, reslinnr)]})

    arrangement = get_cache (Arrangement, {"arrangement": [(eq, res_line.arrangement)]})

    resmember = db_session.query(Resmember).filter(
             (Resmember.resnr == resnr) & (Resmember.reslinnr != reslinnr) & (res_line.active_flag != 2) & (Resmember.resstatus != 12) & (Resmember.resstatus != 11) & (Resmember.resstatus != 13) & (Resmember.arrangement == res_line.arrangement)).first()
    while None != resmember:
        pass
        resmember.zipreis =  to_decimal(res_line.zipreis)
        resmember.betriebsnr = res_line.betriebsnr
        resmember.reserve_dec =  to_decimal(res_line.reserve_dec)
        pass

        for rqueasy in db_session.query(Rqueasy).filter(
                 (Rqueasy.key == ("fargt-line").lower()) & (Rqueasy.char1 == "") & (Rqueasy.resnr == resnr) & (Rqueasy.number2 == arrangement.argtnr) & (Rqueasy.reslinnr == resmember.reslinnr)).order_by(Rqueasy._recid).all():
            db_session.delete(rqueasy)

        for reslin_queasy in db_session.query(Reslin_queasy).filter(
                 (Reslin_queasy.key == ("fargt-line").lower()) & (Reslin_queasy.char1 == "") & (Reslin_queasy.resnr == resnr) & (Reslin_queasy.number2 == arrangement.argtnr) & (Reslin_queasy.reslinnr == reslinnr)).order_by(Reslin_queasy._recid).all():
            rqueasy = Reslin_queasy()
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
            pass

        for rqueasy in db_session.query(Rqueasy).filter(
                 (Rqueasy.key == ("arrangement").lower()) & (Rqueasy.resnr == resnr) & (Rqueasy.reslinnr == resmember.reslinnr)).order_by(Rqueasy._recid).all():
            db_session.delete(rqueasy)

        for reslin_queasy in db_session.query(Reslin_queasy).filter(
                 (Reslin_queasy.key == ("arrangement").lower()) & (Reslin_queasy.resnr == resnr) & (Reslin_queasy.reslinnr == reslinnr)).order_by(Reslin_queasy._recid).all():
            rqueasy = Reslin_queasy()
            db_session.add(rqueasy)

            rqueasy.key = "arrangement"
            rqueasy.resnr = resnr
            rqueasy.reslinnr = resmember.reslinnr
            rqueasy.deci1 =  to_decimal(reslin_queasy.deci1)
            rqueasy.date1 = reslin_queasy.date1
            rqueasy.date2 = reslin_queasy.date2
            rqueasy.char1 = reslin_queasy.char1
            rqueasy.number3 = reslin_queasy.number3
            pass

        curr_recid = resmember._recid
        resmember = db_session.query(Resmember).filter(
                 (Resmember.resnr == resnr) & (Resmember.reslinnr != reslinnr) & (res_line.active_flag != 2) & (Resmember.resstatus != 12) & (Resmember.resstatus != 11) & (Resmember.resstatus != 13) & (Resmember.arrangement == res_line.arrangement) & (Resmember._recid > curr_recid)).first()

    return generate_output()