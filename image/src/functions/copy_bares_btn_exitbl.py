from functions.additional_functions import *
import decimal
from datetime import date
from sqlalchemy import func
from models import Bediener, Bk_veran, Bk_reser, Bk_func, Bk_raum, Counters

def copy_bares_btn_exitbl(s_list:[S_list], resnr:int, reslinnr:int, res_flag:bool, user_init:str):
    von_i:int = 0
    bis_i:int = 0
    week_list:[str] = ["", "", "", "", "", "", "", ""]
    rstat_chr:[str] = ["", "", "", ""]
    bediener = bk_veran = bk_reser = bk_func = bk_raum = counters = None

    s_list = bk_main = bk_res1 = bk_func1 = None

    s_list_list, S_list = create_model("S_list", {"datum":date, "ftime":str, "ttime":str, "raum":str, "wday":str, "raum1":str, "resstatus":int})

    Bk_main = Bk_veran
    Bk_res1 = Bk_reser
    Bk_func1 = Bk_func

    db_session = local_storage.db_session

    def generate_output():
        nonlocal von_i, bis_i, week_list, rstat_chr, bediener, bk_veran, bk_reser, bk_func, bk_raum, counters
        nonlocal bk_main, bk_res1, bk_func1


        nonlocal s_list, bk_main, bk_res1, bk_func1
        nonlocal s_list_list
        return {}

    def create_resline():

        nonlocal von_i, bis_i, week_list, rstat_chr, bediener, bk_veran, bk_reser, bk_func, bk_raum, counters
        nonlocal bk_main, bk_res1, bk_func1


        nonlocal s_list, bk_main, bk_res1, bk_func1
        nonlocal s_list_list

        curr_resnr:int = 0
        reslin_nr:int = 1
        Bk_main = Bk_veran
        Bk_res1 = Bk_reser
        Bk_func1 = Bk_func
        curr_resnr = resnr

        for s_list in query(s_list_list):

            if not res_flag:
                reslin_nr = get_reslinnr()
            else:

                counters = db_session.query(Counters).filter(
                            (Counters.counter_no == 16)).first()

                if not counters:
                    counters = Counters()
                    db_session.add(counters)

                    counters.counter_no = 16
                    counters.counter_bez = "Banquet Reservation No."


                counters = counters + 1

                counters = db_session.query(Counters).first()
                curr_resnr = counters
                bk_main = Bk_main()
                db_session.add(bk_main)

                buffer_copy(bk_veran, bk_main,except_fields=["bk_veran.veran_nr","bk_veran.rechnr"])
                bk_main.veran_nr = curr_resnr
                bk_main.resnr = 1
                bk_main.bediener_nr = bediener.nr

                bk_main = db_session.query(Bk_main).first()
            von_i = to_int(substring(s_list.ftime, 0, 2)) * 2 + to_int(substring(s_list.ftime, 2, 2)) / 30 + 1
            bis_i = to_int(substring(s_list.ttime, 0, 2)) * 2 + to_int(substring(s_list.ttime, 2, 2)) / 30 + 1
            bk_res1 = Bk_res1()
            db_session.add(bk_res1)

            buffer_copy(bk_reser, bk_res1,except_fields=["bk_reser.datum","bk_reser.veran_resnr","bk_reser.resstatus"])
            bk_res1.datum = s_list.datum
            bk_res1.bis_datum = s_list.datum
            bk_res1.veran_nr = curr_resnr
            bk_res1.veran_resnr = reslin_nr
            bk_res1.veran_seite = reslin_nr
            bk_res1.resstatus = s_list.resstatus
            bk_res1.von_zeit = s_list.ftime
            bk_res1.bis_zeit = s_list.ttime
            bk_res1.von_i = von_i
            bk_res1.bis_i = bis_i
            bk_res1.bediener_nr = bediener.nr
            bk_res1.raum = s_list.raum1

            bk_res1 = db_session.query(Bk_res1).first()

            bk_func1 = Bk_func1()
            db_session.add(bk_func1)

            buffer_copy(bk_func, bk_func1,except_fields=["bk_func.datum","bk_func.veran_seite","bk_func.ape__getraenke","bk_func.resstatus"])
            bk_func1.datum = s_list.datum
            bk_func1.bis_datum = s_list.datum
            bk_func1.veran_nr = curr_resnr
            bk_func1.veran_seite = reslin_nr
            bk_func1.resstatus = s_list.resstatus
            bk_func1.wochentag = week_list[get_weekday(s_list.datum - 1) - 1]
            bk_func1.resnr[0] = reslin_nr
            bk_func1.vgeschrieben = user_init
            bk_func1.vkontrolliert = user_init
            bk_func1.c_resstatus[0] = rstat_chr[s_list.resstatus - 1]
            bk_func1.r_resstatus[0] = s_list.resstatus
            bk_func1.raeume[0] = s_list.raum1
            bk_func1.uhrzeit = to_string(s_list.ftime, "99:99") + " - " + to_string(s_list.ttime, "99:99")

            bk_func1 = db_session.query(Bk_func1).first()

    def get_reslinnr():

        nonlocal von_i, bis_i, week_list, rstat_chr, bediener, bk_veran, bk_reser, bk_func, bk_raum, counters
        nonlocal bk_main, bk_res1, bk_func1


        nonlocal s_list, bk_main, bk_res1, bk_func1
        nonlocal s_list_list

        reslin_nr = 0

        def generate_inner_output():
            return reslin_nr
        Bk_res1 = Bk_reser

        for bk_res1 in db_session.query(Bk_res1).filter(
                (Bk_res1.veran_nr == resnr)).all():
            reslin_nr = bk_res1.veran_resnr + 1

            return generate_inner_output()


        return generate_inner_output()

    bediener = db_session.query(Bediener).filter(
            (func.lower(Bediener.userinit) == (user_init).lower())).first()

    bk_veran = db_session.query(Bk_veran).filter(
            (Bk_veran.veran_nr == resnr)).first()

    bk_reser = db_session.query(Bk_reser).filter(
            (Bk_reser.veran_nr == resnr) &  (Bk_reser.veran_resnr == reslinnr)).first()

    bk_func = db_session.query(Bk_func).filter(
            (Bk_func.veran_nr == resnr) &  (Bk_func.veran_seite == reslinnr)).first()

    bk_raum = db_session.query(Bk_raum).filter(
            (Bk_raum.raum == bk_reser.raum)).first()
    create_resline()

    return generate_output()