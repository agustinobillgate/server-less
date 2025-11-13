#using conversion tools version: 1.0.0.119

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from sqlalchemy import func
from functions.reservation_cancel_with_deposit_1bl import reservation_cancel_with_deposit_1bl
from functions.intevent_1 import intevent_1
from functions.del_reslinebl import del_reslinebl
from models import Queasy, Guest, Reservation, Res_line, Zimkateg

def if_vhp_bookeng_cancelbl(becode:int, uniq_id:string, ota_code:string):

    prepare_cache ([Queasy, Guest, Reservation, Res_line, Zimkateg])

    success_flag = False
    msg_str = ""
    cancel_msg:string = ""
    del_mainres:bool = False
    cm_gastno:int = 0
    ota_gastnr:int = 0
    check_integer:int = 0
    cat_flag:bool = False
    bill_date:date = None
    upto_date:date = None
    zikatnr:int = 0
    iftask:string = ""
    rline_origcode:string = ""
    i:int = 0
    queasy = guest = reservation = res_line = zimkateg = None

    qsy = rqueasy = bqueasy = None

    Qsy = create_buffer("Qsy",Queasy)
    Rqueasy = create_buffer("Rqueasy",Queasy)
    Bqueasy = create_buffer("Bqueasy",Queasy)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal success_flag, msg_str, cancel_msg, del_mainres, cm_gastno, ota_gastnr, check_integer, cat_flag, bill_date, upto_date, zikatnr, iftask, rline_origcode, i, queasy, guest, reservation, res_line, zimkateg
        nonlocal becode, uniq_id, ota_code
        nonlocal qsy, rqueasy, bqueasy


        nonlocal qsy, rqueasy, bqueasy

        return {"success_flag": success_flag, "msg_str": msg_str}


    queasy = get_cache (Queasy, {"key": [(eq, 159)],"number1": [(eq, becode)]})

    if queasy:
        cm_gastno = queasy.number2

    queasy = get_cache (Queasy, {"key": [(eq, 152)]})

    if queasy:
        cat_flag = True

    if ota_code != "":

        guest = db_session.query(Guest).filter(
                 (matches(trim(entry(0, Guest.steuernr, "|")),trim(ota_code)))).first()

        if not guest:

            guest = get_cache (Guest, {"gastnr": [(eq, cm_gastno)]})

            if guest:
                ota_gastnr = guest.gastnr
            else:
                msg_str = "GuestNo " + to_string(cm_gastno) + " not found"

                return generate_output()
        else:
            ota_gastnr = guest.gastnr
    else:
        ota_gastnr = cm_gastno

    reservation = get_cache (Reservation, {"gastnr": [(eq, ota_gastnr)],"vesrdepot": [(eq, uniq_id)],"activeflag": [(eq, 0)]})

    if not reservation:

        reservation = get_cache (Reservation, {"vesrdepot": [(eq, uniq_id)],"activeflag": [(eq, 0)]})

    if not reservation:
        msg_str = "Reservation " + uniq_id + " not found"

        reservation = get_cache (Reservation, {"vesrdepot": [(eq, uniq_id)]})

        if reservation:

            for res_line in db_session.query(Res_line).filter(
                     (Res_line.resnr == reservation.resnr)).order_by(Res_line._recid).all():

                if res_line.ankunft == res_line.abreise:
                    upto_date = res_line.abreise
                else:
                    upto_date = res_line.abreise - timedelta(days=1)
                for bill_date in date_range(res_line.ankunft,upto_date) :

                    zimkateg = get_cache (Zimkateg, {"zikatnr": [(eq, res_line.zikatnr)]})

                    if zimkateg:

                        if cat_flag:
                            zikatnr = zimkateg.typ
                        else:
                            zikatnr = zimkateg.zikatnr
                    rline_origcode = ""
                    for i in range(1,num_entries(res_line.zimmer_wunsch, ";") - 1 + 1) :
                        iftask = entry(i - 1, res_line.zimmer_wunsch, ";")

                        if substring(iftask, 0, 10) == ("$OrigCode$").lower() :
                            rline_origcode = substring(iftask, 10)
                            break

                    qsy = get_cache (Queasy, {"key": [(eq, 171)],"date1": [(eq, bill_date)],"number1": [(eq, zikatnr)],"char1": [(eq, rline_origcode)]})

                    if qsy and qsy.logi1 == False and qsy.logi2 == False:

                        bqueasy = get_cache (Queasy, {"_recid": [(eq, qsy._recid)]})

                        if bqueasy:
                            bqueasy.logi2 = True
                            pass
                            pass

                    qsy = get_cache (Queasy, {"key": [(eq, 171)],"date1": [(eq, bill_date)],"number1": [(eq, zikatnr)],"char1": [(eq, "")]})

                    if qsy and qsy.logi1 == False and qsy.logi2 == False:

                        bqueasy = get_cache (Queasy, {"_recid": [(eq, qsy._recid)]})

                        if bqueasy:
                            bqueasy.logi2 = True
                            pass
                            pass

        return generate_output()
    else:

        res_line = get_cache (Res_line, {"resnr": [(eq, reservation.resnr)],"l_zuordnung[2]": [(eq, 0)],"active_flag": [(eq, 0)]})

    if not res_line:
        msg_str = "Cancel Reservation " + uniq_id + " not possible."

        return generate_output()
    else:

        if reservation.depositgef != 0:
            get_output(reservation_cancel_with_deposit_1bl(res_line.resnr, res_line.reslinnr, "Cancelled by BookEngine"))
            get_output(intevent_1(14, "", "Priscilla", res_line.resnr, res_line.reslinnr))
        else:

            for res_line in db_session.query(Res_line).filter(
                     (Res_line.resnr == reservation.resnr) & ((Res_line.active_flag != 1) & (Res_line.resstatus != 6) & (Res_line.resstatus != 13) & (Res_line.resstatus != 8) & (Res_line.resstatus != 10))).order_by(Res_line._recid).all():
                del_mainres, cancel_msg = get_output(del_reslinebl(1, "cancel", res_line.resnr, res_line.reslinnr, "**", "Cancelled by BookEngine"))

                if cancel_msg != "":
                    msg_str = msg_str + cancel_msg + " "


                get_output(intevent_1(14, "", "Priscilla", res_line.resnr, res_line.reslinnr))

        success_flag = True

    return generate_output()