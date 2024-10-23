from functions.additional_functions import *
import decimal
from sqlalchemy import func
from models import Kontline, Queasy, Res_line, Reservation

def global_allotment_checkbl(pvilanguage:int, gastno:int, inp_kontcode:str):
    error_flag = False
    msg_str = ""
    lvcarea:str = "global-allotment"
    kontline = queasy = res_line = reservation = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal error_flag, msg_str, lvcarea, kontline, queasy, res_line, reservation
        nonlocal pvilanguage, gastno, inp_kontcode


        return {"error_flag": error_flag, "msg_str": msg_str}

    def check_global_allotment():

        nonlocal error_flag, msg_str, lvcarea, kontline, queasy, res_line, reservation
        nonlocal pvilanguage, gastno, inp_kontcode

        kline = None
        tokcounter:int = 0
        mesvalue:str = ""
        Kline =  create_buffer("Kline",Kontline)

        queasy = db_session.query(Queasy).filter(
                 (Queasy.key == 147) & (Queasy.number1 == gastno) & (func.lower(Queasy.char1) == (inp_kontcode).lower())).first()
        for tokcounter in range(1,num_entries(queasy.char3, ",")  + 1) :
            mesvalue = entry(tokcounter - 1, queasy.char3, ",")

            if mesvalue != "":

                for res_line in db_session.query(Res_line).filter(
                         (Res_line.gastnr == to_int(mesvalue)) & (Res_line.kontignr > 0) & (Res_line.active_flag <= 1)).order_by(Res_line._recid).all():

                    kline = db_session.query(Kline).filter(
                             (Kline.kontignr == res_line.kontignr)).first()

                    if kline and kline.kontcode == queasy.char1:

                        reservation = db_session.query(Reservation).filter(
                                 (Reservation.resnr == res_line.resnr)).first()
                        msg_str = translateExtended ("Can not remove as reservation found using the allotment:", lvcarea, "") + chr(10) + to_string(reservation.name) + " #" + to_string(res_line.resnr) + " " + to_string(res_line.ankunft) + "-" + to_string(res_line.abreise) + chr(10)
                        error_flag = True

                        return


    check_global_allotment()

    return generate_output()