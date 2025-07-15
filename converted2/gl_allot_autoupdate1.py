from functions.additional_functions import *
import decimal
from datetime import date
from sqlalchemy import func
from functions.htplogic import htplogic
from functions.htpdate import htpdate
from models import Kontline, Queasy, Zimkateg, Counters, Zimmer, Outorder, Res_line

def gl_allot_autoupdate1(gastno:int, zikatno:int, rmcat:str, from_date:date, to_date:date):
    doneflag = False
    allot_list_list = []
    i_counter:int = 0
    curr_date:date = None
    date1:date = None
    date2:date = None
    ci_date:date = None
    na_running:bool = False
    curr_year:int = 0
    kontline = queasy = zimkateg = counters = zimmer = outorder = res_line = None

    allot_list = t_kontline = kbuff = qbuff = bufkline = bufkline1 = None

    allot_list_list, Allot_list = create_model("Allot_list", {"datum":date, "tot_rm":int, "ooo":int, "occ":int, "arrival":int, "glres":int, "allot1":int, "allot2":int, "gl_allot":int, "allot_qty":int, "room_type":str})
    t_kontline_list, T_kontline = create_model_like(Kontline)

    Kbuff = create_buffer("Kbuff",Kontline)
    Qbuff = create_buffer("Qbuff",Queasy)
    Bufkline = create_buffer("Bufkline",Kontline)
    Bufkline1 = create_buffer("Bufkline1",Kontline)

    db_session = local_storage.db_session

    def generate_output():
        nonlocal doneflag, allot_list_list, i_counter, curr_date, date1, date2, ci_date, na_running, curr_year, kontline, queasy, zimkateg, counters, zimmer, outorder, res_line
        nonlocal gastno, zikatno, rmcat, from_date, to_date
        nonlocal kbuff, qbuff, bufkline, bufkline1


        nonlocal allot_list, t_kontline, kbuff, qbuff, bufkline, bufkline1
        nonlocal allot_list_list, t_kontline_list

        return {"doneflag": doneflag, "allot-list": allot_list_list}

    def step1():

        nonlocal doneflag, allot_list_list, i_counter, curr_date, date1, date2, ci_date, na_running, curr_year, kontline, queasy, zimkateg, counters, zimmer, outorder, res_line
        nonlocal gastno, zikatno, rmcat, from_date, to_date
        nonlocal kbuff, qbuff, bufkline, bufkline1


        nonlocal allot_list, t_kontline, kbuff, qbuff, bufkline, bufkline1
        nonlocal allot_list_list, t_kontline_list

        i_delta1:int = 1

        for kontline in db_session.query(Kontline).filter(
                 (Kontline.gastnr == gastno) & (Kontline.zikatnr == zimkateg.zikatnr)).order_by(Kontline.ankunft).all():

            if not t_kontline:
                t_kontline = T_kontline()
                t_kontline_list.append(t_kontline)

                buffer_copy(kontline, t_kontline)

            if kontline.abreise < from_date:
                pass

            elif kontline.ankunft > to_date:
                pass

            elif kontline.ankunft < kontline.abreise:
                date1 = kontline.ankunft
                date2 = kontline.abreise

                kbuff = db_session.query(Kbuff).filter(
                         (Kbuff._recid == kontline._recid)).first()
                kbuff.abreise = kbuff.ankunft


                for curr_date in date_range((date1 + 1),date2) :

                    counters = db_session.query(Counters).filter(
                             (Counters.counter_no == 10)).first()
                    counters.counter = counters.counter + 1
                    kbuff = Kbuff()
                    db_session.add(kbuff)

                    buffer_copy(kontline, kbuff,except_fields=["ankunft","abreise","kontignr"])
                    kbuff.kontignr = counters.counter
                    kbuff.ankunft = curr_date
                    kbuff.abreise = curr_date

                    if curr_date > to_date:
                        curr_date = date2
                        kbuff.abreise = curr_date


    def step2():

        nonlocal doneflag, allot_list_list, i_counter, date1, date2, ci_date, na_running, curr_year, kontline, queasy, zimkateg, counters, zimmer, outorder, res_line
        nonlocal gastno, zikatno, rmcat, from_date, to_date
        nonlocal kbuff, qbuff, bufkline, bufkline1


        nonlocal allot_list, t_kontline, kbuff, qbuff, bufkline, bufkline1
        nonlocal allot_list_list, t_kontline_list

        i:int = 0
        anz_room:int = 0
        avail_room:int = 0
        curr_day:int = 0
        mm:int = 0
        curr_date:date = None
        do_it:bool = False
        calc_occ:bool = False
        calc_arrival:bool = False
        calc_glres:bool = False
        calc_allot2:bool = False
        datum:date = None
        datum1:date = None
        datum2:date = None
        kline = None
        Kline =  create_buffer("Kline",Kontline)

        for zimmer in db_session.query(Zimmer).filter(
                 (Zimmer.sleeping) & (Zimmer.zikatnr == zimkateg.zikatnr)).order_by(Zimmer._recid).all():
            anz_room = anz_room + 1
        for curr_date in date_range(from_date,to_date) :
            allot_list = Allot_list()
            allot_list_list.append(allot_list)

            allot_list.datum = curr_date
            allot_list.tot_rm = anz_room
            allot_list.room_type = to_string(zimkateg.zikatnr)


            pass

        for outorder in db_session.query(Outorder).filter(
                 (Outorder.betriebsnr <= 1)).order_by(Outorder._recid).all():

            zimmer = db_session.query(Zimmer).filter(
                     (Zimmer.zinr == outorder.zinr) & (Zimmer.zikatnr == zimkateg.zikatnr) & (Zimmer.sleeping) & (not outorder.gespstart > to_date) & (not outorder.gespende < from_date)).first()

            if zimmer:
                for curr_date in date_range(from_date,to_date) :

                    allot_list = query(allot_list_list, filters=(lambda allot_list: allot_list.datum == curr_date and allot_list.room_type == to_string(zimkateg.zikatnr)), first=True)

                    if curr_date >= outorder.gespstart and curr_date <= outorder.gespende:
                        allot_list.ooo = allot_list.ooo + 1

        res_line = db_session.query(Res_line).filter(
                 (not Res_line.ankunft > to_date) & (not Res_line.abreise <= from_date) & (Res_line.l_zuordnung[inc_value(2)] == 0) & (Res_line.zikatnr == zimkateg.zikatnr)).first()
        while None != res_line:
            calc_occ = False
            calc_arrival = False
            calc_glres = False
            calc_allot2 = False

            if res_line.resstatus == 6 and res_line.active_flag == 1:

                zimmer = db_session.query(Zimmer).filter(
                         (Zimmer.zikatnr == res_line.zikatnr) & (Zimmer.sleeping)).first()

                if zimmer:
                    calc_occ = True

            if res_line.active_flag == 0 and (res_line.resstatus <= 2 or res_line.resstatus == 5):
                calc_arrival = True

                if res_line.zinr != "":

                    zimmer = db_session.query(Zimmer).filter(
                             (Zimmer.zinr == res_line.zinr)).first()
                    calc_arrival = zimmer.sleeping

            if res_line.active_flag <= 1 and res_line.resstatus <= 6 and res_line.resstatus != 3 and res_line.resstatus != 4 and res_line.kontignr < 0:
                calc_glres = True

                if res_line.zinr != "":

                    zimmer = db_session.query(Zimmer).filter(
                             (Zimmer.zinr == res_line.zinr)).first()
                    calc_glres = zimmer.sleeping
                calc_allot2 = True

                kontline = db_session.query(Kontline).filter(
                         (Kontline.gastnr == gastno) & (Kontline.kontignr == res_line.kontignr)).first()
                calc_allot2 = not None != kontline

                if calc_allot2 and res_line.zinr != "":

                    zimmer = db_session.query(Zimmer).filter(
                             (Zimmer.zinr == res_line.zinr)).first()
                    calc_allot2 = zimmer.sleeping

                    kline = db_session.query(Kline).filter(
                             (Kline.kontignr == res_line.kontignr)).first()

                    bufkline = db_session.query(Bufkline).filter(
                             (Bufkline.kontcode == kline.kontcode) & (Bufkline.betriebsnr == 0) & (res_line.ankunft >= Bufkline.ankunft) & (res_line.ankunft <= Bufkline.abreise)).first()

            if res_line.ankunft >= from_date:
                datum1 = res_line.ankunft
            else:
                datum1 = from_date

            if res_line.abreise <= to_date:
                datum2 = res_line.abreise - timedelta(days=1)
            else:
                datum2 = to_date
            for curr_date in date_range(datum1,datum2) :

                allot_list = query(allot_list_list, filters=(lambda allot_list: allot_list.datum == curr_date and allot_list.room_type == to_string(zimkateg.zikatnr)), first=True)

                if curr_date >= res_line.ankunft and curr_date < res_line.abreise:

                    if calc_occ:
                        allot_list.occ = allot_list.occ + 1

                    if calc_arrival:
                        allot_list.arrival = allot_list.arrival + res_line.zimmeranz

                    if calc_glres:
                        allot_list.glres = allot_list.glres - res_line.zimmeranz

                if calc_allot2:

                    allot_list = query(allot_list_list, filters=(lambda allot_list: allot_list.datum == curr_date and allot_list.room_type == to_string(zimkateg.zikatnr)), first=True)

                    if (curr_date >= ci_date + timedelta(days=bufkline.ruecktage)) and curr_date >= res_line.ankunft and curr_date < res_line.abreise:
                        allot_list.allot2 = allot_list.allot2 + res_line.zimmeranz

            curr_recid = res_line._recid
            res_line = db_session.query(Res_line).filter(
                     (not Res_line.ankunft > to_date) & (not Res_line.abreise <= from_date) & (Res_line.l_zuordnung[inc_value(2)] == 0) & (Res_line.zikatnr == zimkateg.zikatnr) & (Res_line._recid > curr_recid)).first()

        for kontline in db_session.query(Kontline).filter(
                 (Kontline.kontignr > 0) & (Kontline.betriebsnr == 1) & (not Kontline.ankunft > to_date) & (not Kontline.abreise < from_date) & (Kontline.zikatnr == zimkateg.zikatnr) & (Kontline.kontstat == 1)).order_by(Kontline._recid).all():
            for curr_date in date_range(from_date,to_date) :

                allot_list = query(allot_list_list, filters=(lambda allot_list: allot_list.datum == curr_date and allot_list.room_type == to_string(zimkateg.zikatnr)), first=True)

                if curr_date >= kontline.ankunft and curr_date <= kontline.abreise:
                    allot_list.glres = allot_list.glres + kontline.zimmeranz

        for kontline in db_session.query(Kontline).filter(
                 (Kontline.kontignr > 0) & (Kontline.gastnr != gastno) & (Kontline.betriebsnr == 0) & (not Kontline.ankunft > to_date) & (not Kontline.abreise < from_date) & ((Kontline.zikatnr == zimkateg.zikatnr) | (Kontline.zikatnr == 0)) & (Kontline.kontstat == 1)).order_by(Kontline._recid).all():
            for curr_date in date_range(from_date,to_date) :

                allot_list = query(allot_list_list, filters=(lambda allot_list: allot_list.datum == curr_date and allot_list.room_type == to_string(zimkateg.zikatnr)), first=True)

                if curr_date >= kontline.ankunft and curr_date <= kontline.abreise:

                    if curr_date >= (ci_date + timedelta(days=kontline.ruecktage)):
                        allot_list.allot1 = allot_list.allot1 + kontline.zimmeranz


        for mm in range(1,get_month(from_date) - 1 + 1) :
            curr_date = date_mdy(mm, 1, get_year(from_date)) + timedelta(days=35)
            curr_date = date_mdy(get_month(curr_date) , 1, get_year(curr_date)) - timedelta(days=1)
            curr_day = curr_day + get_day(curr_date)


        curr_day = curr_day + get_day(from_date) - 1

        for allot_list in query(allot_list_list, sort_by=[("datum",False)]):
            curr_day = curr_day + 1

            if curr_year != get_year(allot_list.datum):
                curr_year = get_year(allot_list.datum)

                qbuff = db_session.query(Qbuff).filter(
                         (Qbuff.key == 37) & (Qbuff.number1 == curr_year)).first()

            kontline = db_session.query(Kontline).filter(
                         (Kontline.gastnr == gastno) & (Kontline.zikatnr == zimkateg.zikatnr) & (Kontline.ankunft == allot_list.datum)).first()

            if not kontline:

                counters = db_session.query(Counters).filter(
                             (Counters.counter_no == 10)).first()
                counters.counter = counters.counter + 1
                kontline = Kontline()
                db_session.add(kontline)

                buffer_copy(t_kontline, kontline,except_fields=["ankunft","abreise","kontignr"])
                kontline.kontignr = counters.counter
                kontline.ankunft = allot_list.datum
                kontline.abreise = allot_list.datum


            avail_room = allot_list.tot_rm - allot_list.ooo - allot_list.occ -\
                    allot_list.arrival - allot_list.glres -\
                    allot_list.allot1 + allot_list.allot2

            if qbuff and substring(qbuff.char3, curr_day - 1, 1) == ("C").lower() :
                kontline.zimmeranz = 0
                avail_room = 0

            elif avail_room > 0:
                kontline.zimmeranz = avail_room
            else:
                kontline.zimmeranz = 0
            kontline.bemerk = "Updated on " + to_string(get_current_date()) +\
                    " - " + to_string(get_current_time_in_seconds(), "HH:mm:SS") + " by system."


            allot_list.allot_qty = avail_room

        doneflag = True


    pass

    if zikatno != 0:

        zimkateg = db_session.query(Zimkateg).filter(
                 (Zimkateg.zikatnr == zikatno)).first()

    elif rmcat != "":

        zimkateg = db_session.query(Zimkateg).filter(
                 (func.lower(Zimkateg.kurzbez) == (rmcat).lower())).first()

    if not zimkateg:

        return generate_output()
    na_running = get_output(htplogic(253))

    if na_running:

        return generate_output()
    ci_date = get_output(htpdate(87))
    step1()
    step2()

    return generate_output()