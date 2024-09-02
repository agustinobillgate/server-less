from functions.additional_functions import *
import decimal
from models import Reservation, Res_line, Htparam, Waehrung

def mk_mainres_reserve_decbl(resnr:int):
    exchg_rate:decimal = 0
    reservation = res_line = htparam = waehrung = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal exchg_rate, reservation, res_line, htparam, waehrung


        return {}


    reservation = db_session.query(Reservation).filter(
            (Reservation.resnr == resnr)).first()

    if not reservation.insurance:

        for res_line in db_session.query(Res_line).filter(
                (Res_line.resnr == reservation.resnr) &  ((Res_line.resstatus == 6) |  (Res_line.resstatus == 13)) &  (Res_line.reserve_dec != 0)).all():
            res_line.reserve_dec = 0

        return generate_output()

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 144)).first()

    waehrung = db_session.query(Waehrung).filter(
            (Waehrung.wabkurz == htparam.fchar)).first()

    if waehrung:
        exchg_rate = waehrung.ankauf / waehrung.einheit

    if exchg_rate != 0:

        for res_line in db_session.query(Res_line).filter(
                (Res_line.resnr == reservation.resnr) &  ((Res_line.resstatus == 6) |  (Res_line.resstatus == 13)) &  (Res_line.reserve_dec == 0)).all():
            res_line.reserve_dec = exchg_rate


    return generate_output()