#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from functions.htpdate import htpdate
from models import Kontline, Zimkateg, Zimmer, Outorder, Res_line

def update_global_allotment_browsebl(pvilanguage:int, input_date:date, currcode:string, rmtype:string):

    prepare_cache ([Kontline, Zimkateg, Zimmer, Outorder, Res_line])

    allot_list_list = []
    lvcarea:string = "update-global-allotment"
    curr_date:date = None
    from_date:date = None
    to_date:date = None
    ci_date:date = None
    kontline = zimkateg = zimmer = outorder = res_line = None

    allot_list = abuff1 = abuff2 = None

    allot_list_list, Allot_list = create_model("Allot_list", {"datum":date, "w_day":string, "tot_rm":int, "ooo":int, "occ":int, "avl_rm":int, "stat1":int, "stat2":int, "stat5":int, "glres":int, "avail1":int, "ovb1":int, "allot1":int, "gl_allot":int, "gl_used":int, "gl_remain":int, "allot2":int, "blank_str":string, "avail2":int, "ovb2":int, "s_avail2":int, "expired":bool})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal allot_list_list, lvcarea, curr_date, from_date, to_date, ci_date, kontline, zimkateg, zimmer, outorder, res_line
        nonlocal pvilanguage, input_date, currcode, rmtype


        nonlocal allot_list, abuff1, abuff2
        nonlocal allot_list_list

        return {"allot-list": allot_list_list}

    def create_allot_list():

        nonlocal allot_list_list, lvcarea, curr_date, from_date, to_date, kontline, zimkateg, zimmer, outorder, res_line
        nonlocal pvilanguage, input_date, currcode, rmtype


        nonlocal allot_list, abuff1, abuff2
        nonlocal allot_list_list

        curr_wday:int = 0
        ci_date:date = None
        day_name:List[string] = create_empty_list(8,"")
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
        to_date = from_date + timedelta(days=35)
        to_date = date_mdy(get_month(to_date) , 1, get_year(to_date)) - timedelta(days=1)

        if from_date < ci_date:
            from_date = ci_date
        for curr_date in date_range(from_date,to_date) :
            curr_wday = get_weekday(curr_date) - 1

            if curr_wday == 0:
                curr_wday = 7
            allot_list = Allot_list()
            allot_list_list.append(allot_list)

            allot_list.w_day = day_name[curr_wday - 1]
            allot_list.datum = curr_date


    def create_browse():

        nonlocal allot_list_list, lvcarea, curr_date, from_date, to_date, ci_date, kontline, zimkateg, zimmer, outorder, res_line
        nonlocal pvilanguage, input_date, currcode, rmtype


        nonlocal allot_list, abuff1, abuff2
        nonlocal allot_list_list

        curr_i:int = 0
        i:int = 0
        anz_room:int = 0
        do_it:bool = False
        tmp_list:List[int] = create_empty_list(31,0)
        kline = None
        Abuff1 = Allot_list
        abuff1_list = allot_list_list
        Abuff2 = Allot_list
        abuff2_list = allot_list_list
        Kline =  create_buffer("Kline",Kontline)
        for i in range(1,31 + 1) :
            tmp_list[i - 1] = 0

        zimkateg = get_cache (Zimkateg, {"kurzbez": [(eq, rmtype)]})

        for zimmer in db_session.query(Zimmer).filter(
                 (Zimmer.sleeping) & (Zimmer.zikatnr == zimkateg.zikatnr)).order_by(Zimmer._recid).all():
            anz_room = anz_room + 1
        curr_date = from_date
        for i in range(get_day(from_date),get_day(to_date)  + 1) :

            allot_list = query(allot_list_list, filters=(lambda allot_list: allot_list.datum == curr_date), first=True)
            allot_list.tot_rm = anz_room


            tmp_list[i - 1] = anz_room
            curr_date = curr_date + timedelta(days=1)

        outorder_obj_list = {}
        outorder = Outorder()
        zimmer = Zimmer()
        for outorder.gespstart, outorder.gespende, outorder._recid, zimmer.sleeping, zimmer._recid in db_session.query(Outorder.gespstart, Outorder.gespende, Outorder._recid, Zimmer.sleeping, Zimmer._recid).join(Zimmer,(Zimmer.zinr == Outorder.zinr) & (Zimmer.zikatnr == zimkateg.zikatnr) & (Zimmer.sleeping) & not_ (Outorder.gespstart > to_date) & not_ (Outorder.gespende < from_date)).filter(
                 (Outorder.betriebsnr <= 1)).order_by(Outorder._recid).all():
            if outorder_obj_list.get(outorder._recid):
                continue
            else:
                outorder_obj_list[outorder._recid] = True


            curr_date = from_date
            for i in range(get_day(from_date),get_day(to_date)  + 1) :

                allot_list = query(allot_list_list, filters=(lambda allot_list: allot_list.datum == curr_date), first=True)

                if curr_date >= outorder.gespstart and curr_date <= outorder.gespende:
                    allot_list.ooo = allot_list.ooo + 1
                    tmp_list[i - 1] = tmp_list[i - 1] - 1


                curr_date = curr_date + timedelta(days=1)

        res_line_obj_list = {}
        res_line = Res_line()
        zimmer = Zimmer()
        for res_line.ankunft, res_line.abreise, res_line.zinr, res_line.zimmeranz, res_line.kontignr, res_line._recid, zimmer.sleeping, zimmer._recid in db_session.query(Res_line.ankunft, Res_line.abreise, Res_line.zinr, Res_line.zimmeranz, Res_line.kontignr, Res_line._recid, Zimmer.sleeping, Zimmer._recid).join(Zimmer,(Zimmer.zikatnr == Res_line.zikatnr) & (Zimmer.sleeping)).filter(
                 (Res_line.resstatus == 6) & (Res_line.active_flag == 1) & (Res_line.zikatnr == zimkateg.zikatnr) & not_ (Res_line.ankunft > to_date) & not_ (Res_line.abreise <= from_date) & (Res_line.l_zuordnung[inc_value(2)] == 0)).order_by(Res_line._recid).all():
            if res_line_obj_list.get(res_line._recid):
                continue
            else:
                res_line_obj_list[res_line._recid] = True


            curr_date = from_date
            for i in range(get_day(from_date),get_day(to_date)  + 1) :

                allot_list = query(allot_list_list, filters=(lambda allot_list: allot_list.datum == curr_date), first=True)

                if curr_date >= res_line.ankunft and curr_date < res_line.abreise:
                    allot_list.occ = allot_list.occ + 1
                    tmp_list[i - 1] = tmp_list[i - 1] - 1


                curr_date = curr_date + timedelta(days=1)
        curr_date = from_date
        for i in range(get_day(from_date),get_day(to_date)  + 1) :

            allot_list = query(allot_list_list, filters=(lambda allot_list: allot_list.datum == curr_date), first=True)
            allot_list.avl_rm = tmp_list[i - 1]
            curr_date = curr_date + timedelta(days=1)

        for res_line in db_session.query(Res_line).filter(
                 (Res_line.active_flag == 0) & (Res_line.resstatus == 1) & (Res_line.zikatnr == zimkateg.zikatnr) & not_ (Res_line.ankunft > to_date) & not_ (Res_line.abreise <= from_date) & (Res_line.l_zuordnung[inc_value(2)] == 0)).order_by(Res_line._recid).all():
            do_it = True

            if res_line.zinr != "":

                zimmer = get_cache (Zimmer, {"zinr": [(eq, res_line.zinr)]})
                do_it = zimmer.sleeping

            if do_it:
                curr_date = from_date
                for i in range(get_day(from_date),get_day(to_date)  + 1) :

                    allot_list = query(allot_list_list, filters=(lambda allot_list: allot_list.datum == curr_date), first=True)

                    if curr_date >= res_line.ankunft and curr_date < res_line.abreise:
                        allot_list.stat1 = allot_list.stat1 + res_line.zimmeranz
                        tmp_list[i - 1] = tmp_list[i - 1] - res_line.zimmeranz


                    curr_date = curr_date + timedelta(days=1)

        for res_line in db_session.query(Res_line).filter(
                 (Res_line.active_flag == 0) & (Res_line.resstatus == 2) & (Res_line.zikatnr == zimkateg.zikatnr) & not_ (Res_line.ankunft > to_date) & not_ (Res_line.abreise <= from_date) & (Res_line.l_zuordnung[inc_value(2)] == 0)).order_by(Res_line._recid).all():
            do_it = True

            if res_line.zinr != "":

                zimmer = get_cache (Zimmer, {"zinr": [(eq, res_line.zinr)]})
                do_it = zimmer.sleeping

            if do_it:
                curr_date = from_date
                for i in range(get_day(from_date),get_day(to_date)  + 1) :

                    allot_list = query(allot_list_list, filters=(lambda allot_list: allot_list.datum == curr_date), first=True)

                    if curr_date >= res_line.ankunft and curr_date < res_line.abreise:
                        allot_list.stat2 = allot_list.stat2 + res_line.zimmeranz
                        tmp_list[i - 1] = tmp_list[i - 1] - res_line.zimmeranz


                    curr_date = curr_date + timedelta(days=1)

        for res_line in db_session.query(Res_line).filter(
                 (Res_line.active_flag == 0) & (Res_line.resstatus == 5) & (Res_line.zikatnr == zimkateg.zikatnr) & not_ (Res_line.ankunft > to_date) & not_ (Res_line.abreise <= from_date) & (Res_line.l_zuordnung[inc_value(2)] == 0)).order_by(Res_line._recid).all():
            do_it = True

            if res_line.zinr != "":

                zimmer = get_cache (Zimmer, {"zinr": [(eq, res_line.zinr)]})
                do_it = zimmer.sleeping

            if do_it:
                curr_date = from_date
                for i in range(get_day(from_date),get_day(to_date)  + 1) :

                    allot_list = query(allot_list_list, filters=(lambda allot_list: allot_list.datum == curr_date), first=True)

                    if curr_date >= res_line.ankunft and curr_date < res_line.abreise:
                        allot_list.stat5 = allot_list.stat5 + res_line.zimmeranz
                        tmp_list[i - 1] = tmp_list[i - 1] - res_line.zimmeranz


                    curr_date = curr_date + timedelta(days=1)

        for kontline in db_session.query(Kontline).filter(
                 (Kontline.kontignr > 0) & (Kontline.betriebsnr == 1) & not_ (Kontline.ankunft > to_date) & not_ (Kontline.abreise < from_date) & (Kontline.zikatnr == zimkateg.zikatnr) & (Kontline.kontstatus == 1)).order_by(Kontline._recid).all():
            curr_date = from_date
            for i in range(get_day(from_date),get_day(to_date)  + 1) :

                allot_list = query(allot_list_list, filters=(lambda allot_list: allot_list.datum == curr_date), first=True)

                if curr_date >= kontline.ankunft and curr_date <= kontline.abreise:
                    allot_list.glres = allot_list.glres + kontline.zimmeranz
                    tmp_list[i - 1] = tmp_list[i - 1] - kontline.zimmeranz


                curr_date = curr_date + timedelta(days=1)

        for res_line in db_session.query(Res_line).filter(
                 (Res_line.active_flag <= 1) & (Res_line.resstatus <= 6) & (Res_line.resstatus != 3) & (Res_line.resstatus != 4) & (Res_line.zikatnr == zimkateg.zikatnr) & not_ (Res_line.ankunft > to_date) & not_ (Res_line.abreise <= from_date) & (Res_line.l_zuordnung[inc_value(2)] == 0) & (Res_line.kontignr < 0)).order_by(Res_line._recid).all():
            do_it = True

            if res_line.zinr != "":

                zimmer = get_cache (Zimmer, {"zinr": [(eq, res_line.zinr)]})
                do_it = zimmer.sleeping

            if do_it:
                curr_date = from_date
                for i in range(get_day(from_date),get_day(to_date)  + 1) :

                    allot_list = query(allot_list_list, filters=(lambda allot_list: allot_list.datum == curr_date), first=True)

                    if curr_date >= res_line.ankunft and curr_date < res_line.abreise:
                        allot_list.glres = allot_list.glres - res_line.zimmeranz
                        tmp_list[i - 1] = tmp_list[i - 1] + res_line.zimmeranz


                    curr_date = curr_date + timedelta(days=1)
        curr_date = from_date
        for i in range(get_day(from_date),get_day(to_date)  + 1) :

            allot_list = query(allot_list_list, filters=(lambda allot_list: allot_list.datum == curr_date), first=True)

            if tmp_list[i - 1] > 0:
                allot_list.avail1 = tmp_list[i - 1]
            curr_date = curr_date + timedelta(days=1)
        curr_date = from_date
        for i in range(get_day(from_date),get_day(to_date)  + 1) :

            allot_list = query(allot_list_list, filters=(lambda allot_list: allot_list.datum == curr_date), first=True)

            if tmp_list[i - 1] < 0:
                allot_list.ovb1 = - tmp_list[i - 1]
            curr_date = curr_date + timedelta(days=1)

        for kontline in db_session.query(Kontline).filter(
                 (Kontline.kontignr > 0) & (Kontline.betriebsnr == 0) & not_ (Kontline.ankunft > to_date) & not_ (Kontline.abreise < from_date) & ((Kontline.zikatnr == zimkateg.zikatnr) | (Kontline.zikatnr == 0)) & (Kontline.kontstatus == 1)).order_by(Kontline._recid).all():
            curr_date = from_date
            for i in range(get_day(from_date),get_day(to_date)  + 1) :

                allot_list = query(allot_list_list, filters=(lambda allot_list: allot_list.datum == curr_date), first=True)

                if curr_date >= kontline.ankunft and curr_date <= kontline.abreise:

                    if (curr_date >= ci_date + timedelta(days=kontline.ruecktage)):
                        tmp_list[i - 1] = tmp_list[i - 1] - kontline.zimmeranz

                        if kontline.kontcode.lower()  != (currcode).lower() :
                            allot_list.allot2 = allot_list.allot2 + kontline.zimmeranz

                    if kontline.kontcode.lower()  == (currcode).lower() :
                        allot_list.allot1 = allot_list.allot1 + kontline.zimmeranz
                        allot_list.expired = curr_date < (ci_date + kontline.ruecktage)


                curr_date = curr_date + timedelta(days=1)

        for res_line in db_session.query(Res_line).filter(
                 (Res_line.active_flag <= 1) & (Res_line.resstatus <= 6) & (Res_line.resstatus != 3) & (Res_line.resstatus != 4) & (Res_line.zikatnr == zimkateg.zikatnr) & not_ (Res_line.ankunft > to_date) & not_ (Res_line.abreise <= from_date) & (Res_line.l_zuordnung[inc_value(2)] == 0) & (Res_line.kontignr > 0)).order_by(Res_line._recid).all():
            do_it = True

            if res_line.zinr != "":

                zimmer = get_cache (Zimmer, {"zinr": [(eq, res_line.zinr)]})
                do_it = zimmer.sleeping

            if do_it:

                kline = get_cache (Kontline, {"kontignr": [(eq, res_line.kontignr)]})

                kontline = get_cache (Kontline, {"kontcode": [(eq, kline.kontcode)],"betriebsnr": [(eq, 0)],"ankunft": [(le, res_line.ankunft)],"abreise": [(ge, res_line.ankunft)]})
                curr_date = from_date
                for i in range(get_day(from_date),get_day(to_date)  + 1) :

                    allot_list = query(allot_list_list, filters=(lambda allot_list: allot_list.datum == curr_date), first=True)

                    if (curr_date >= ci_date + timedelta(days=kontline.ruecktage)) and curr_date >= res_line.ankunft and curr_date < res_line.abreise:
                        tmp_list[i - 1] = tmp_list[i - 1] + res_line.zimmeranz

                        if kontline.kontcode.lower()  == (currcode).lower() :
                            allot_list.gl_used = allot_list.gl_used + res_line.zimmeranz
                        else:
                            allot_list.allot2 = allot_list.allot2 - res_line.zimmeranz
                    curr_date = curr_date + timedelta(days=1)
        curr_date = from_date
        for i in range(get_day(from_date),get_day(to_date)  + 1) :

            allot_list = query(allot_list_list, filters=(lambda allot_list: allot_list.datum == curr_date), first=True)

            if tmp_list[i - 1] > 0:
                allot_list.avail2 = tmp_list[i - 1]
            curr_date = curr_date + timedelta(days=1)
        curr_date = from_date
        for i in range(get_day(from_date),get_day(to_date)  + 1) :

            allot_list = query(allot_list_list, filters=(lambda allot_list: allot_list.datum == curr_date), first=True)

            if tmp_list[i - 1] < 0:
                allot_list.ovb2 = - tmp_list[i - 1]
            curr_date = curr_date + timedelta(days=1)

        for allot_list in query(allot_list_list):
            allot_list.gl_allot = allot_list.allot1

            if not allot_list.expired and allot_list.allot1 > allot_list.gl_used:
                allot_list.gl_remain = allot_list.allot1 - allot_list.gl_used

    create_allot_list()
    create_browse()

    return generate_output()