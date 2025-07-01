#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Queasy, Res_line, Zimkateg, Guest, Reservation, History

def hk_preference_btn_exitbl(i_zeit:int, zinr:string, reason:string, user_init:string, answer:bool, fr_date:date):

    prepare_cache ([Res_line, Zimkateg, Reservation, History])

    t_queasy_list = []
    queasy = res_line = zimkateg = guest = reservation = history = None

    t_queasy = None

    t_queasy_list, T_queasy = create_model_like(Queasy)

    db_session = local_storage.db_session

    def generate_output():
        nonlocal t_queasy_list, queasy, res_line, zimkateg, guest, reservation, history
        nonlocal i_zeit, zinr, reason, user_init, answer, fr_date


        nonlocal t_queasy
        nonlocal t_queasy_list

        return {"t-queasy": t_queasy_list}

    res_line = get_cache (Res_line, {"active_flag": [(eq, 1)],"resstatus": [(eq, 6)],"zinr": [(eq, zinr)]})

    if not res_line:

        res_line = get_cache (Res_line, {"active_flag": [(eq, 1)],"resstatus": [(eq, 13)],"zinr": [(eq, zinr)],"l_zuordnung[2]": [(eq, 0)]})

    if not res_line:

        return generate_output()
    queasy = Queasy()
    db_session.add(queasy)

    queasy.key = 24
    queasy.date1 = fr_date
    queasy.char1 = zinr
    queasy.number1 = i_zeit
    queasy.number2 = res_line.gastnrmember
    queasy.char2 = user_init
    queasy.char3 = reason


    pass
    t_queasy = T_queasy()
    t_queasy_list.append(t_queasy)

    buffer_copy(queasy, t_queasy)

    if answer:

        zimkateg = get_cache (Zimkateg, {"zikatnr": [(eq, res_line.zikatnr)]})

        guest = get_cache (Guest, {"gastnr": [(eq, res_line.gastnrmember)]})

        reservation = get_cache (Reservation, {"resnr": [(eq, res_line.resnr)]})
        history = History()
        db_session.add(history)

        history.gastnr = res_line.gastnrmember
        history.ankunft = res_line.ankunft
        history.abreise = res_line.abreise
        history.zimmeranz = res_line.zimmeranz
        history.zikateg = zimkateg.kurzbez
        history.zinr = zinr
        history.erwachs = res_line.erwachs
        history.gratis = res_line.gratis
        history.zipreis =  to_decimal(res_line.zipreis)
        history.arrangement = res_line.arrangement
        history.abreisezeit = to_string(get_current_time_in_seconds(), "HH:MM")
        history.gastinfo = res_line.name + " - " +\
                guest.adresse1 + ", " + guest.wohnort
        history.segmentcode = reservation.segmentcode
        history.zi_wechsel = False
        history.resnr = res_line.resnr
        history.reslinnr = res_line.reslinnr
        history.betriebsnr = to_int(res_line.pseudofix)


        history.bemerk = "HK-Preference" +\
                ":= " +\
                trim(zinr)


        pass

    return generate_output()