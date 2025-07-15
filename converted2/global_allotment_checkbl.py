#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import Kontline, Queasy, Res_line, Reservation

def global_allotment_checkbl(pvilanguage:int, gastno:int, inp_kontcode:string):

    prepare_cache ([Kontline, Queasy, Res_line, Reservation])

    error_flag = False
    msg_str = ""
    lvcarea:string = "global-allotment"
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
        mesvalue:string = ""
        Kline =  create_buffer("Kline",Kontline)

        queasy = get_cache (Queasy, {"key": [(eq, 147)],"number1": [(eq, gastno)],"char1": [(eq, inp_kontcode)]})
        for tokcounter in range(1,num_entries(queasy.char3, ",")  + 1) :
            mesvalue = entry(tokcounter - 1, queasy.char3, ",")

            if mesvalue != "":

                for res_line in db_session.query(Res_line).filter(
                         (Res_line.gastnr == to_int(mesvalue)) & (Res_line.kontignr > 0) & (Res_line.active_flag <= 1)).order_by(Res_line._recid).all():

                    kline = get_cache (Kontline, {"kontignr": [(eq, res_line.kontignr)]})

                    if kline and kline.kontcode == queasy.char1:

                        reservation = get_cache (Reservation, {"resnr": [(eq, res_line.resnr)]})
                        msg_str = translateExtended ("Can not remove as reservation found using the allotment:", lvcarea, "") + chr_unicode(10) + to_string(reservation.name) + " #" + to_string(res_line.resnr) + " " + to_string(res_line.ankunft) + "-" + to_string(res_line.abreise) + chr_unicode(10)
                        error_flag = True

                        return


    check_global_allotment()

    return generate_output()