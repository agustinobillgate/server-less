from functions.additional_functions import *
import decimal
from datetime import date
from sqlalchemy import func
from models import Queasy, Res_line, Zimkateg, Guest, Reservation, History

def hk_preference_btn_exitbl(i_zeit:int, zinr:str, reason:str, user_init:str, answer:bool, fr_date:date):
    t_queasy_list = []
    queasy = res_line = zimkateg = guest = reservation = history = None

    t_queasy = None

    t_queasy_list, T_queasy = create_model_like(Queasy)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal t_queasy_list, queasy, res_line, zimkateg, guest, reservation, history


        nonlocal t_queasy
        nonlocal t_queasy_list
        return {"t-queasy": t_queasy_list}

    res_line = db_session.query(Res_line).filter(
            (Res_line.active_flag == 1) &  (Res_line.resstatus == 6) &  (func.lower(Res_line.(zinr).lower()) == (zinr).lower())).first()

    if not res_line:

        res_line = db_session.query(Res_line).filter(
                (Res_line.active_flag == 1) &  (Res_line.resstatus == 13) &  (func.lower(Res_line.(zinr).lower()) == (zinr).lower()) &  (Res_line.l_zuordnung[2] == 0)).first()

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

    queasy = db_session.query(Queasy).first()
    t_queasy = T_queasy()
    t_queasy_list.append(t_queasy)

    buffer_copy(queasy, t_queasy)

    if answer:

        zimkateg = db_session.query(Zimkateg).filter(
                (Zimkateg.zikatnr == res_line.zikatnr)).first()

        guest = db_session.query(Guest).filter(
                (Guest.gastnr == res_line.gastnrmember)).first()

        reservation = db_session.query(Reservation).filter(
                (Reservation.resnr == res_line.resnr)).first()
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
        history.zipreis = res_line.zipreis
        history.arrangement = res_line.arrangement
        history.abreisezeit = to_string(get_current_time_in_seconds(), "HH:MM")
        history.gastinfo = res_line.name + " - " +\
                guest.adresse1 + ", " + guest.wohnort
        history.segmentcode = reservation.segmentcode
        history.zi_wechsel = False
        history.resnr = res_line.resnr
        history.reslinnr = res_line.reslinnr
        history.betriebsnr = to_int(res_line.pseudofix)


        history.bemerk = "HK_Preference" +\
                ": ==  " +\
                trim(zinr)

        history = db_session.query(History).first()

    return generate_output()