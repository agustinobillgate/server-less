#using conversion tools version: 1.0.0.117
#-------------------------------------------
# Rd 22/7/2025
# Rd, 24/11/2025, Update last counter dengan next_counter_for_update
#-------------------------------------------
from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Bediener, Bk_veran, Bk_reser, Bk_func, Bk_raum, Counters
from functions.next_counter_for_update import next_counter_for_update

s_list_data, S_list = create_model("S_list", {"datum":date, "ftime":string, "ttime":string, "raum":string, "wday":string, "raum1":string, "resstatus":int})

def copy_bares_btn_exitbl(s_list_data:[S_list], resnr:int, reslinnr:int, res_flag:bool, user_init:string):

    prepare_cache ([Bediener, Bk_reser, Counters])

    von_i:int = 0
    bis_i:int = 0
    tmp_usernr:int = 0
    week_list:List[string] = ["Monday ", "Tuesday ", "Wednesday", "Thursday ", "Friday ", "Saturday ", "Sunday "]
    rstat_chr:List[string] = ["F", "T", "W"]
    bediener = bk_veran = bk_reser = bk_func = bk_raum = counters = None

    s_list = None

    db_session = local_storage.db_session
    last_count = 0
    error_lock:string = ""

    def generate_output():
        nonlocal von_i, bis_i, tmp_usernr, week_list, rstat_chr, bediener, bk_veran, bk_reser, bk_func, bk_raum, counters
        nonlocal resnr, reslinnr, res_flag, user_init


        nonlocal s_list

        return {}

    def create_resline():

        nonlocal von_i, bis_i, tmp_usernr, week_list, rstat_chr, bediener, bk_veran, bk_reser, bk_func, bk_raum, counters
        nonlocal resnr, reslinnr, res_flag, user_init


        nonlocal s_list

        curr_resnr:int = 0
        reslin_nr:int = 1
        bk_main = None
        bk_res1 = None
        bk_func1 = None
        Bk_main =  create_buffer("Bk_main",Bk_veran)
        Bk_res1 =  create_buffer("Bk_res1",Bk_reser)
        Bk_func1 =  create_buffer("Bk_func1",Bk_func)
        curr_resnr = resnr

        for s_list in query(s_list_data):

            if not res_flag:
                reslin_nr = get_reslinnr()
            else:

                # counters = get_cache (Counters, {"counter_no": [(eq, 16)]})

                # if not counters:
                #     counters = Counters()
                #     db_session.add(counters)

                #     counters.counter_no = 16
                #     counters.counter_bez = "Banquet Reservation No."


                # counters.counter = counters.counter + 1
                pass
                # curr_resnr = counters.counter
                last_count, error_lock = get_output(next_counter_for_update(16))
                curr_resnr = last_count

                bk_main = Bk_veran()
                db_session.add(bk_main)

                buffer_copy(bk_veran, bk_main,except_fields=["bk_veran.veran_nr","bk_veran.rechnr"])
                bk_main.veran_nr = curr_resnr
                bk_main.resnr = 1
                bk_main.bediener_nr = tmp_usernr


                pass
            von_i = to_int(substring(s_list.ftime, 0, 2)) * 2 + to_int(substring(s_list.ftime, 2, 2)) / 30 + 1
            bis_i = to_int(substring(s_list.ttime, 0, 2)) * 2 + to_int(substring(s_list.ttime, 2, 2)) / 30 + 1
            bk_res1 = Bk_reser()
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
            bk_res1.bediener_nr = tmp_usernr
            bk_res1.raum = s_list.raum1


            pass
            pass
            bk_func1 = Bk_func()
            db_session.add(bk_func1)

            buffer_copy(bk_func, bk_func1,except_fields=["bk_func.datum","bk_func.veran_seite","bk_func.resstatus"])
            bk_func1.datum = s_list.datum
            bk_func1.bis_datum = s_list.datum
            bk_func1.veran_nr = curr_resnr
            bk_func1.veran_seite = reslin_nr
            bk_func1.resstatus = s_list.resstatus
            
            #Rd 22/7/2025
            # bk_func1.wochentag = week_list[get_weekday(s_list.datum - 1) - 1]
            adjusted_date = s_list.datum - timedelta(days=1)
            bk_func1.wochentag = week_list[get_weekday(adjusted_date) - 1]
            
            bk_func1.resnr[0] = reslin_nr
            bk_func1.vgeschrieben = user_init
            bk_func1.vkontrolliert = user_init
            bk_func1.c_resstatus[0] = rstat_chr[s_list.resstatus - 1]
            bk_func1.r_resstatus[0] = s_list.resstatus
            bk_func1.raeume[0] = s_list.raum1
            bk_func1.uhrzeit = to_string(s_list.ftime, "99:99") + " - " + to_string(s_list.ttime, "99:99")


            pass
            pass


    def get_reslinnr():

        nonlocal von_i, bis_i, tmp_usernr, week_list, rstat_chr, bediener, bk_veran, bk_reser, bk_func, bk_raum, counters
        nonlocal resnr, reslinnr, res_flag, user_init


        nonlocal s_list

        reslin_nr = 1
        bk_res1 = None

        def generate_inner_output():
            return (reslin_nr)

        Bk_res1 =  create_buffer("Bk_res1",Bk_reser)

        for bk_res1 in db_session.query(Bk_res1).filter(
                 (Bk_res1.veran_nr == resnr)).order_by(Bk_res1.veran_resnr.desc()).all():
            reslin_nr = bk_res1.veran_resnr + 1

            return generate_inner_output()

        return generate_inner_output()


    bediener = get_cache (Bediener, {"userinit": [(eq, user_init)]})

    if bediener:
        tmp_usernr = bediener.nr

    bk_veran = get_cache (Bk_veran, {"veran_nr": [(eq, resnr)]})

    if bk_veran:

        bk_reser = get_cache (Bk_reser, {"veran_nr": [(eq, resnr)],"veran_resnr": [(eq, reslinnr)]})

        if bk_reser:

            bk_func = get_cache (Bk_func, {"veran_nr": [(eq, resnr)],"veran_seite": [(eq, reslinnr)]})

            if bk_func:

                bk_raum = get_cache (Bk_raum, {"raum": [(eq, bk_reser.raum)]})
                create_resline()

    return generate_output()