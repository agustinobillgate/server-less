#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import Reservation, Res_line, Htparam, Waehrung

def mk_mainres_reserve_decbl(resnr:int):

    prepare_cache ([Reservation, Res_line, Htparam, Waehrung])

    exchg_rate:Decimal = to_decimal("0.0")
    reservation = res_line = htparam = waehrung = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal exchg_rate, reservation, res_line, htparam, waehrung
        nonlocal resnr

        return {}


    reservation = get_cache (Reservation, {"resnr": [(eq, resnr)]})

    if not reservation.insurance:

        for res_line in db_session.query(Res_line).filter(
                 (Res_line.resnr == reservation.resnr) & ((Res_line.resstatus == 6) | (Res_line.resstatus == 13)) & (Res_line.reserve_dec != 0)).order_by(Res_line._recid).all():
            res_line.reserve_dec =  to_decimal("0")

        return generate_output()

    htparam = get_cache (Htparam, {"paramnr": [(eq, 144)]})

    waehrung = get_cache (Waehrung, {"wabkurz": [(eq, htparam.fchar)]})

    if waehrung:
        exchg_rate =  to_decimal(waehrung.ankauf) / to_decimal(waehrung.einheit)

    if exchg_rate != 0:

        for res_line in db_session.query(Res_line).filter(
                 (Res_line.resnr == reservation.resnr) & ((Res_line.resstatus == 6) | (Res_line.resstatus == 13)) & (Res_line.reserve_dec == 0)).order_by(Res_line._recid).all():
            res_line.reserve_dec =  to_decimal(exchg_rate)


    return generate_output()