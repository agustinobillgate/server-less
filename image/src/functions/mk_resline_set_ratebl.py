from functions.additional_functions import *
import decimal
from datetime import date
from sqlalchemy import func
from functions.htpdate import htpdate
from functions.ratecode_rate import ratecode_rate
from models import Res_line, Arrangement, Reslin_queasy, Guest_pr, Queasy, Katpreis

def mk_resline_set_ratebl(direct_change:bool, fixed_rate:bool, ebdisc_flag:bool, kbdisc_flag:bool, rate_readonly:bool, gastnr:int, res_mode:str, argt:str, contcode:str, bookdate:date, reslin_list:[Reslin_list]):
    restricted_disc = False
    new_rate = 0
    rate_tooltip = ""
    wd_array:[int] = [0, 0, 0, 0, 0, 0, 0, 0, 0]
    res_line = arrangement = reslin_queasy = guest_pr = queasy = katpreis = None

    reslin_list = None

    reslin_list_list, Reslin_list = create_model_like(Res_line)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal restricted_disc, new_rate, rate_tooltip, wd_array, res_line, arrangement, reslin_queasy, guest_pr, queasy, katpreis


        nonlocal reslin_list
        nonlocal reslin_list_list
        return {"restricted_disc": restricted_disc, "new_rate": new_rate, "rate_tooltip": rate_tooltip}

    def get_rackrate(erwachs:int, kind1:int, kind2:int):

        nonlocal restricted_disc, new_rate, rate_tooltip, wd_array, res_line, arrangement, reslin_queasy, guest_pr, queasy, katpreis


        nonlocal reslin_list
        nonlocal reslin_list_list

        rate:decimal = 0

        if erwachs >= 1 and erwachs <= 4:
            rate = rate + katpreis.perspreis[erwachs - 1]
        rate = rate + kind1 * katpreis.kindpreis[0] + kind2 * katpreis.kindpreis[1]
        return rate

    def set_roomrate():

        nonlocal restricted_disc, new_rate, rate_tooltip, wd_array, res_line, arrangement, reslin_queasy, guest_pr, queasy, katpreis


        nonlocal reslin_list
        nonlocal reslin_list_list

        ci_date:date = None
        datum:date = None
        curr_zikatnr:int = 0
        current_rate:decimal = 0
        rate_found:bool = False
        early_flag:bool = False
        kback_flag:bool = False

        arrangement = db_session.query(Arrangement).filter(
                (func.lower(Arrangement) == (argt).lower())).first()

        if not arrangement:

            return
        ci_date = get_output(htpdate(87))

        reslin_list = query(reslin_list_list, first=True)
        current_rate = reslin_list.zipreis
        datum = reslin_list.ankunft

        if res_mode.lower()  == "inhouse":
            datum = ci_date

        if reslin_list.l_zuordnung[0] != 0:
            curr_zikatnr = reslin_list.l_zuordnung[0]
        else:
            curr_zikatnr = reslin_list.zikatnr

        if reslin_list.erwachs == 0 and reslin_list.kind1 == 0 and reslin_list.kind2 == 0:
            new_rate = 0

            return

        if fixed_rate:

            reslin_queasy = db_session.query(Reslin_queasy).filter(
                    (func.lower(Reslin_queasy.key) == "arrangement") &  (Reslin_queasy.resnr == reslin_list.resnr) &  (Reslin_queasy.reslinnr == reslin_list.reslinnr) &  (Reslin_queasy.datum >= Reslin_queasy.date1) &  (Reslin_queasy.datum <= Reslin_queasy.date2)).first()

            if reslin_queasy:
                new_rate = reslin_queasy.deci1
                rate_tooltip = ""

                return

        guest_pr = db_session.query(Guest_pr).filter(
                (Guest_pr.gastnr == gastnr)).first()

        if guest_pr:

            queasy = db_session.query(Queasy).filter(
                    (Queasy.key == 18) &  (Queasy.number1 == reslin_list.reserve_int)).first()

            if queasy and queasy.logi3:
                datum = reslin_list.ankunft

            if bookdate != None:
                rate_found, new_rate, restricted_disc, kback_flag = get_output(ratecode_rate(ebdisc_flag, kbdisc_flag, reslin_list.resnr, reslin_list.reslinnr, ("!" + contcode), bookdate, datum, reslin_list.ankunft, reslin_list.abreise, reslin_list.reserve_int, arrangement.argtnr, curr_zikatnr, reslin_list.erwachs, reslin_list.kind1, reslin_list.kind2, reslin_list.reserve_dec, reslin_list.betriebsnr))
            else:
                rate_found, new_rate, restricted_disc, kback_flag = get_output(ratecode_rate(ebdisc_flag, kbdisc_flag, reslin_list.resnr, reslin_list.reslinnr, ("!" + contcode), ci_date, datum, reslin_list.ankunft, reslin_list.abreise, reslin_list.reserve_int, arrangement.argtnr, curr_zikatnr, reslin_list.erwachs, reslin_list.kind1, reslin_list.kind2, reslin_list.reserve_dec, reslin_list.betriebsnr))

            if rate_found:

                return

        if res_mode.lower()  == "inhouse":

            katpreis = db_session.query(Katpreis).filter(
                    (Katpreis.zikatnr == curr_zikatnr) &  (Katpreis.argtnr == arrangement.argtnr) &  (Katpreis.startperiode <= datum) &  (Katpreis.endperiode >= datum) &  (Katpreis.betriebsnr == wd_array[get_weekday(datum) - 1])).first()

            if not katpreis:

                katpreis = db_session.query(Katpreis).filter(
                        (Katpreis.zikatnr == curr_zikatnr) &  (Katpreis.argtnr == arrangement.argtnr) &  (Katpreis.startperiode <= datum) &  (Katpreis.endperiode >= datum) &  (Katpreis.betriebsnr == 0)).first()
        else:

            katpreis = db_session.query(Katpreis).filter(
                    (Katpreis.zikatnr == curr_zikatnr) &  (Katpreis.argtnr == arrangement.argtnr) &  (Katpreis.datum >= Katpreis.startperiode) &  (Katpreis.datum <= Katpreis.endperiode) &  (Katpreis.betriebsnr == wd_array[get_weekday(datum) - 1])).first()

            if not katpreis:

                katpreis = db_session.query(Katpreis).filter(
                        (Katpreis.zikatnr == curr_zikatnr) &  (Katpreis.argtnr == arrangement.argtnr) &  (Katpreis.datum >= Katpreis.startperiode) &  (Katpreis.datum <= Katpreis.endperiode) &  (Katpreis.betriebsnr == 0)).first()

        if katpreis:
            new_rate = get_rackrate (reslin_list.erwachs, reslin_list.kind1, reslin_list.kind2)
        else:
            new_rate = 0

        if not direct_change and not rate_readonly:

            if current_rate != 0 and new_rate == 0:
                new_rate = current_rate


    set_roomrate()

    return generate_output()