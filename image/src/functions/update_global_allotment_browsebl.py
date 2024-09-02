from functions.additional_functions import *
import decimal
from datetime import date
from functions.htpdate import htpdate
from sqlalchemy import func
from models import Kontline, Zimkateg, Zimmer, Outorder, Res_line

def update_global_allotment_browsebl(pvilanguage:int, input_date:date, currcode:str, rmtype:str):
    allot_list_list = []
    lvcarea:str = "update_global_allotment"
    curr_date:date = None
    from_date:date = None
    to_date:date = None
    ci_date:date = None
    kontline = zimkateg = zimmer = outorder = res_line = None

    allot_list = abuff1 = abuff2 = kline = None

    allot_list_list, Allot_list = create_model("Allot_list", {"datum":date, "w_day":str, "tot_rm":int, "ooo":int, "occ":int, "avl_rm":int, "stat1":int, "stat2":int, "stat5":int, "glres":int, "avail1":int, "ovb1":int, "allot1":int, "gl_allot":int, "gl_used":int, "gl_remain":int, "allot2":int, "blank_str":str, "avail2":int, "ovb2":int, "s_avail2":int, "expired":bool})

    Abuff1 = Allot_list
    abuff1_list = allot_list_list

    Abuff2 = Allot_list
    abuff2_list = allot_list_list

    Kline = Kontline

    db_session = local_storage.db_session

    def generate_output():
        nonlocal allot_list_list, lvcarea, curr_date, from_date, to_date, ci_date, kontline, zimkateg, zimmer, outorder, res_line
        nonlocal abuff1, abuff2, kline


        nonlocal allot_list, abuff1, abuff2, kline
        nonlocal allot_list_list
        return {"allot-list": allot_list_list}

    def create_allot_list():

        nonlocal allot_list_list, lvcarea, curr_date, from_date, to_date, ci_date, kontline, zimkateg, zimmer, outorder, res_line
        nonlocal abuff1, abuff2, kline


        nonlocal allot_list, abuff1, abuff2, kline
        nonlocal allot_list_list

        curr_wday:int = 0
        ci_date:date = None
        day_name:[str] = ["", "", "", "", "", "", "", "", ""]
        day_name[0] = translateExtended ("SUN", lvcarea, "")
        day_name[1] = translateExtended ("MON", lvcarea, "")
        day_name[2] = translateExtended ("TUE", lvcarea, "")
        day_name[3] = translateExtended ("WED", lvcarea, "")
        day_name[4] = translateExtended ("THU", lvcarea, "")
        day_name[5] = translateExtended ("FRI", lvcarea, "")
        day_name[6] = translateExtended ("SAT", lvcarea, "")
        day_name[7] = translateExtended ("SUN", lvcarea, "")


        ci_date = get_output(htpdate(87))
        from_date = input_date
        to_date = from_date + 35
        to_date = date_mdy(get_month(to_date) , 1, get_year(to_date)) - 1

        if from_date < ci_date:
            from_date = ci_date
        for curr_date in range(from_date,to_date + 1) :
            curr_wday = get_weekday(curr_date) - 1

            if curr_wday == 0:
                curr_wday = 7
            allot_list = Allot_list()
            allot_list_list.append(allot_list)

            allot_list.w_day = day_name[curr_wday - 1]
            allot_list.datum = curr_date

    def create_browse():

        nonlocal allot_list_list, lvcarea, curr_date, from_date, to_date, ci_date, kontline, zimkateg, zimmer, outorder, res_line
        nonlocal abuff1, abuff2, kline


        nonlocal allot_list, abuff1, abuff2, kline
        nonlocal allot_list_list

        curr_i:int = 0
        i:int = 0
        anz_room:int = 0
        do_it:bool = False
        tmp_list:[int] = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        Abuff1 = Allot_list
        Abuff2 = Allot_list
        Kline = Kontline
        for i in range(1,31 + 1) :
            tmp_list[i - 1] = 0

        zimkateg = db_session.query(Zimkateg).filter(
                (func.lower(Zimkateg.kurzbez) == (rmtype).lower())).first()

        for zimmer in db_session.query(Zimmer).filter(
                (Zimmer.sleeping) &  (Zimmer.zikatnr == zimkateg.zikatnr)).all():
            anz_room = anz_room + 1
        curr_date = from_date
        for i in range(get_day(from_date),get_day(to_date)  + 1) :

            allot_list = query(allot_list_list, filters=(lambda allot_list :allot_list.datum == curr_date), first=True)
            allot_list.tot_rm = anz_room


            tmp_list[i - 1] = anz_room
            curr_date = curr_date + 1

        outorder_obj_list = []
        for outorder, zimmer in db_session.query(Outorder, Zimmer).join(Zimmer,(Zimmer.zinr == Outorder.zinr) &  (Zimmer.zikatnr == zimkateg.zikatnr) &  (Zimmer.sleeping) &  (not Outorder.gespstart > to_date) &  (not Outorder.gespende < from_date)).filter(
                (Outorder.betriebsnr <= 1)).all():
            if outorder._recid in outorder_obj_list:
                continue
            else:
                outorder_obj_list.append(outorder._recid)


            curr_date = from_date
            for i in range(get_day(from_date),get_day(to_date)  + 1) :

                allot_list = query(allot_list_list, filters=(lambda allot_list :allot_list.datum == curr_date), first=True)

                if curr_date >= outorder.gespstart and curr_date <= outorder.gespende:
                    allot_list.ooo = allot_list.ooo + 1
                    tmp_list[i - 1] = tmp_list[i - 1] - 1


                curr_date = curr_date + 1

        res_line_obj_list = []
        for res_line, zimmer in db_session.query(Res_line, Zimmer).join(Zimmer,(Zimmer.zikatnr == Res_line.zikatnr) &  (Zimmer.sleeping)).filter(
                (Res_line.resstatus == 6) &  (Res_line.active_flag == 1) &  (Res_line.zikatnr == zimkateg.zikatnr) &  (not Res_line.ankunft > to_date) &  (not Res_line.abreise <= from_date) &  (Res_line.l_zuordnung[2] == 0)).all():
            if res_line._recid in res_line_obj_list:
                continue
            else:
                res_line_obj_list.append(res_line._recid)


            curr_date = from_date
            for i in range(get_day(from_date),get_day(to_date)  + 1) :

                allot_list = query(allot_list_list, filters=(lambda allot_list :allot_list.datum == curr_date), first=True)

                if curr_date >= res_line.ankunft and curr_date < res_line.abreise:
                    allot_list.occ = allot_list.occ + 1
                    tmp_list[i - 1] = tmp_list[i - 1] - 1


                curr_date = curr_date + 1
        curr_date = from_date
        for i in range(get_day(from_date),get_day(to_date)  + 1) :

            allot_list = query(allot_list_list, filters=(lambda allot_list :allot_list.datum == curr_date), first=True)
            allot_list.avl_rm = tmp_list[i - 1]
            curr_date = curr_date + 1

        for res_line in db_session.query(Res_line).filter(
                (Res_line.active_flag == 0) &  (Res_line.resstatus == 1) &  (Res_line.zikatnr == zimkateg.zikatnr) &  (not Res_line.ankunft > to_date) &  (not Res_line.abreise <= from_date) &  (Res_line.l_zuordnung[2] == 0)).all():
            do_it = True

            if res_line.zinr != "":

                zimmer = db_session.query(Zimmer).filter(
                        (Zimmer.zinr == res_line.zinr)).first()
                do_it = zimmer.sleeping

            if do_it:
                curr_date = from_date
                for i in range(get_day(from_date),get_day(to_date)  + 1) :

                    allot_list = query(allot_list_list, filters=(lambda allot_list :allot_list.datum == curr_date), first=True)

                    if curr_date >= res_line.ankunft and curr_date < res_line.abreise:
                        allot_list.stat1 = allot_list.stat1 + res_line.zimmeranz
                        tmp_list[i - 1] = tmp_list[i - 1] - res_line.zimmeranz


                    curr_date = curr_date + 1

        for res_line in db_session.query(Res_line).filter(
                (Res_line.active_flag == 0) &  (Res_line.resstatus == 2) &  (Res_line.zikatnr == zimkateg.zikatnr) &  (not Res_line.ankunft > to_date) &  (not Res_line.abreise <= from_date) &  (Res_line.l_zuordnung[2] == 0)).all():
            do_it = True

            if res_line.zinr != "":

                zimmer = db_session.query(Zimmer).filter(
                        (Zimmer.zinr == res_line.zinr)).first()
                do_it = zimmer.sleeping

            if do_it:
                curr_date = from_date
                for i in range(get_day(from_date),get_day(to_date)  + 1) :

                    allot_list = query(allot_list_list, filters=(lambda allot_list :allot_list.datum == curr_date), first=True)

                    if curr_date >= res_line.ankunft and curr_date < res_line.abreise:
                        allot_list.stat2 = allot_list.stat2 + res_line.zimmeranz
                        tmp_list[i - 1] = tmp_list[i - 1] - res_line.zimmeranz


                    curr_date = curr_date + 1

        for res_line in db_session.query(Res_line).filter(
                (Res_line.active_flag == 0) &  (Res_line.resstatus == 5) &  (Res_line.zikatnr == zimkateg.zikatnr) &  (not Res_line.ankunft > to_date) &  (not Res_line.abreise <= from_date) &  (Res_line.l_zuordnung[2] == 0)).all():
            do_it = True

            if res_line.zinr != "":

                zimmer = db_session.query(Zimmer).filter(
                        (Zimmer.zinr == res_line.zinr)).first()
                do_it = zimmer.sleeping

            if do_it:
                curr_date = from_date
                for i in range(get_day(from_date),get_day(to_date)  + 1) :

                    allot_list = query(allot_list_list, filters=(lambda allot_list :allot_list.datum == curr_date), first=True)

                    if curr_date >= res_line.ankunft and curr_date < res_line.abreise:
                        allot_list.stat5 = allot_list.stat5 + res_line.zimmeranz
                        tmp_list[i - 1] = tmp_list[i - 1] - res_line.zimmeranz


                    curr_date = curr_date + 1

        for kontline in db_session.query(Kontline).filter(
                (Kontline.kontignr > 0) &  (Kontline.betriebsnr == 1) &  (not Kontline.ankunft > to_date) &  (not Kontline.abreise < from_date) &  (Kontline.zikatnr == zimkateg.zikatnr) &  (Kontline.kontstat == 1)).all():
            curr_date = from_date
            for i in range(get_day(from_date),get_day(to_date)  + 1) :

                allot_list = query(allot_list_list, filters=(lambda allot_list :allot_list.datum == curr_date), first=True)

                if curr_date >= kontline.ankunft and curr_date <= kontline.abreise:
                    allot_list.glres = allot_list.glres + kontline.zimmeranz
                    tmp_list[i - 1] = tmp_list[i - 1] - kontline.zimmeranz


                curr_date = curr_date + 1

        for res_line in db_session.query(Res_line).filter(
                (Res_line.active_flag <= 1) &  (Res_line.resstatus <= 6) &  (Res_line.resstatus != 3) &  (Res_line.resstatus != 4) &  (Res_line.zikatnr == zimkateg.zikatnr) &  (not Res_line.ankunft > to_date) &  (not Res_line.abreise <= from_date) &  (Res_line.l_zuordnung[2] == 0) &  (Res_line.kontignr < 0)).all():
            do_it = True

            if res_line.zinr != "":

                zimmer = db_session.query(Zimmer).filter(
                        (Zimmer.zinr == res_line.zinr)).first()
                do_it = zimmer.sleeping

            if do_it:
                curr_date = from_date
                for i in range(get_day(from_date),get_day(to_date)  + 1) :

                    allot_list = query(allot_list_list, filters=(lambda allot_list :allot_list.datum == curr_date), first=True)

                    if curr_date >= res_line.ankunft and curr_date < res_line.abreise:
                        allot_list.glres = allot_list.glres - res_line.zimmeranz
                        tmp_list[i - 1] = tmp_list[i - 1] + res_line.zimmeranz


                    curr_date = curr_date + 1
        curr_date = from_date
        for i in range(get_day(from_date),get_day(to_date)  + 1) :

            allot_list = query(allot_list_list, filters=(lambda allot_list :allot_list.datum == curr_date), first=True)

            if tmp_list[i - 1] > 0:
                allot_list.avail1 = tmp_list[i - 1]
            curr_date = curr_date + 1
        curr_date = from_date
        for i in range(get_day(from_date),get_day(to_date)  + 1) :

            allot_list = query(allot_list_list, filters=(lambda allot_list :allot_list.datum == curr_date), first=True)

            if tmp_list[i - 1] < 0:
                allot_list.ovb1 = - tmp_list[i - 1]
            curr_date = curr_date + 1

        for kontline in db_session.query(Kontline).filter(
                (Kontline.kontignr > 0) &  (Kontline.betriebsnr == 0) &  (not Kontline.ankunft > to_date) &  (not Kontline.abreise < from_date) &  ((Kontline.zikatnr == zimkateg.zikatnr) |  (Kontline.zikatnr == 0)) &  (Kontline.kontstat == 1)).all():
            curr_date = from_date
            for i in range(get_day(from_date),get_day(to_date)  + 1) :

                allot_list = query(allot_list_list, filters=(lambda allot_list :allot_list.datum == curr_date), first=True)

                if curr_date >= kontline.ankunft and curr_date <= kontline.abreise:

                    if (curr_date >= ci_date + kontline.ruecktage):
                        tmp_list[i - 1] = tmp_list[i - 1] - kontline.zimmeranz

                        if kontline.kontcode.lower()  != (currcode).lower() :
                            allot_list.allot2 = allot_list.allot2 + kontline.zimmeranz

                    if kontline.kontcode.lower()  == (currcode).lower() :
                        allot_list.allot1 = allot_list.allot1 + kontline.zimmeranz
                        allot_list.expired = curr_date < (ci_date + kontline.ruecktage)


                curr_date = curr_date + 1

        for res_line in db_session.query(Res_line).filter(
                (Res_line.active_flag <= 1) &  (Res_line.resstatus <= 6) &  (Res_line.resstatus != 3) &  (Res_line.resstatus != 4) &  (Res_line.zikatnr == zimkateg.zikatnr) &  (not Res_line.ankunft > to_date) &  (not Res_line.abreise <= from_date) &  (Res_line.l_zuordnung[2] == 0) &  (Res_line.kontignr > 0)).all():
            do_it = True

            if res_line.zinr != "":

                zimmer = db_session.query(Zimmer).filter(
                        (Zimmer.zinr == res_line.zinr)).first()
                do_it = zimmer.sleeping

            if do_it:

                kline = db_session.query(Kline).filter(
                        (Kline.kontignr == res_line.kontignr)).first()

                kontline = db_session.query(Kontline).filter(
                        (Kontline.kontcode == kline.kontcode) &  (Kontline.betriebsnr == 0) &  (res_line.ankunft >= Kontline.ankunft) &  (res_line.ankunft <= Kontline.abreise)).first()
                curr_date = from_date
                for i in range(get_day(from_date),get_day(to_date)  + 1) :

                    allot_list = query(allot_list_list, filters=(lambda allot_list :allot_list.datum == curr_date), first=True)

                    if (curr_date >= ci_date + kontline.ruecktage) and curr_date >= res_line.ankunft and curr_date < res_line.abreise:
                        tmp_list[i - 1] = tmp_list[i - 1] + res_line.zimmeranz

                        if kontline.kontcode.lower()  == (currcode).lower() :
                            allot_list.gl_used = allot_list.gl_used + res_line.zimmeranz
                        else:
                            allot_list.allot2 = allot_list.allot2 - res_line.zimmeranz
                    curr_date = curr_date + 1
        curr_date = from_date
        for i in range(get_day(from_date),get_day(to_date)  + 1) :

            allot_list = query(allot_list_list, filters=(lambda allot_list :allot_list.datum == curr_date), first=True)

            if tmp_list[i - 1] > 0:
                allot_list.avail2 = tmp_list[i - 1]
            curr_date = curr_date + 1
        curr_date = from_date
        for i in range(get_day(from_date),get_day(to_date)  + 1) :

            allot_list = query(allot_list_list, filters=(lambda allot_list :allot_list.datum == curr_date), first=True)

            if tmp_list[i - 1] < 0:
                allot_list.ovb2 = - tmp_list[i - 1]
            curr_date = curr_date + 1

        for allot_list in query(allot_list_list):
            allot_list.gl_allot = allot_list.allot1

            if not allot_list.expired and allot_list.allot1 > allot_list.gl_used:
                allot_list.gl_remain = allot_list.allot1 - allot_list.gl_used


    create_allot_list()
    create_browse()

    return generate_output()