#using conversion tools version: 1.0.0.117
#-------------------------------------------------------
# Rd, 27/11/2025, with_for_update added
#-------------------------------------------------------
from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from sqlalchemy import func
from models import Queasy, Zimkateg, Res_line, Zimmer, Outorder

def update_allotmentbyratebl(currcode:string, rmtype:string, curr_month:int, curr_year:int):

    prepare_cache ([Queasy, Zimkateg, Res_line, Zimmer, Outorder])

    allot_list_data = []
    cat_flag:bool = False
    do_it:bool = False
    occall:List[int] = create_empty_list(31,0)
    occ:List[int] = create_empty_list(31,0)
    ooo:List[int] = create_empty_list(31,0)
    anzahl:int = 0
    i:int = 0
    i_typ:int = 0
    fdate:date = None
    tdate:date = None
    start_date:date = None
    end_date:date = None
    datum:date = None
    rline_origcode:string = ""
    iftask:string = ""
    mestoken:string = ""
    mesvalue:string = ""
    queasy = zimkateg = res_line = zimmer = outorder = None

    allot_list = allot1 = allot2 = allot3 = None

    allot_list_data, Allot_list = create_model("Allot_list", {"bezeich":string, "allotment":[int,31], "nr":int})

    Allot1 = Allot_list
    allot1_data = allot_list_data

    Allot2 = Allot_list
    allot2_data = allot_list_data

    Allot3 = Allot_list
    allot3_data = allot_list_data

    db_session = local_storage.db_session
    currcode = currcode.strip()
    rmtype = rmtype.strip()

    def generate_output():
        nonlocal allot_list_data, cat_flag, do_it, occall, occ, ooo, anzahl, i, i_typ, fdate, tdate, start_date, end_date, datum, rline_origcode, iftask, mestoken, mesvalue, queasy, zimkateg, res_line, zimmer, outorder
        nonlocal currcode, rmtype, curr_month, curr_year
        nonlocal allot1, allot2, allot3


        nonlocal allot_list, allot1, allot2, allot3
        nonlocal allot_list_data

        return {"allot-list": allot_list_data}

    queasy = get_cache (Queasy, {"key": [(eq, 152)]})

    if queasy:
        cat_flag = True

    queasy = get_cache (Queasy, {"key": [(eq, 152)],"char1": [(eq, rmtype)]})

    if queasy:
        i_typ = queasy.number1

    elif not queasy:

        zimkateg = get_cache (Zimkateg, {"kurzbez": [(eq, rmtype)]})

        if zimkateg:
            i_typ = zimkateg.zikatnr
    allot_list = Allot_list()
    allot_list_data.append(allot_list)

    allot_list.nr = 1
    allot_list.bezeich = "AvailAllRate"


    allot_list = Allot_list()
    allot_list_data.append(allot_list)

    allot_list.nr = 2
    allot_list.bezeich = "AllotByRate"


    allot_list = Allot_list()
    allot_list_data.append(allot_list)

    allot_list.nr = 3
    allot_list.bezeich = "OccByRate"

    allot1 = query(allot1_data, filters=(lambda allot1: allot1.nr == 1), first=True)

    allot2 = query(allot2_data, filters=(lambda allot2: allot2.nr == 2), first=True)

    allot3 = query(allot3_data, filters=(lambda allot3: allot3.nr == 3), first=True)

    if curr_month == 12:
        tdate = date_mdy(1, 1, curr_year + 1)
    else:
        tdate = date_mdy(curr_month + 1, 1, curr_year)
    fdate = date_mdy(curr_month, 1, curr_year)
    tdate = tdate - timedelta(days=1)

    if cat_flag:

        res_line_obj_list = {}
        res_line = Res_line()
        zimkateg = Zimkateg()
        for res_line.zinr, res_line.abreise, res_line.ankunft, res_line.zimmeranz, res_line.zimmer_wunsch, res_line._recid, zimkateg.zikatnr, zimkateg._recid in db_session.query(Res_line.zinr, Res_line.abreise, Res_line.ankunft, Res_line.zimmeranz, Res_line.zimmer_wunsch, Res_line._recid, Zimkateg.zikatnr, Zimkateg._recid).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr) & (Zimkateg.typ == i_typ)).filter(
                 (Res_line.active_flag <= 1) & (Res_line.resstatus <= 6) & (Res_line.resstatus != 3) & (Res_line.resstatus != 4) & (Res_line.resstatus != 12) & (Res_line.resstatus != 11) & (Res_line.resstatus != 13) & (Res_line.kontignr >= 0) & (Res_line.l_zuordnung[inc_value(2)] == 0) & (Res_line.ankunft <= tdate) & (Res_line.abreise >= fdate) & (matches(Res_line.zimmer_wunsch,("*$OrigCode$*")))).order_by(Res_line._recid).all():
            if res_line_obj_list.get(res_line._recid):
                continue
            else:
                res_line_obj_list[res_line._recid] = True


            do_it = True

            if res_line.zinr != "":

                zimmer = get_cache (Zimmer, {"zinr": [(eq, res_line.zinr)]})
                do_it = zimmer.sleeping

            if do_it:

                if res_line.ankunft == res_line.abreise:
                    end_date = res_line.abreise
                else:
                    end_date = res_line.abreise - timedelta(days=1)

                if res_line.ankunft >= fdate:
                    start_date = res_line.ankunft
                else:
                    start_date = fdate

                if end_date >= tdate:
                    end_date = tdate
                for datum in date_range(start_date,end_date) :
                    occall[get_day(datum) - 1] = occall[get_day(datum) - 1] + res_line.zimmeranz

                if matches(res_line.zimmer_wunsch,r"*$OrigCode$*"):
                    rline_origcode = ""
                    for i in range(1,num_entries(res_line.zimmer_wunsch, ";") - 1 + 1) :
                        iftask = entry(i - 1, res_line.zimmer_wunsch, ";")

                        if substring(iftask, 0, 10) == ("$OrigCode$").lower() :
                            rline_origcode = substring(iftask, 10)
                            break

                    if rline_origcode.lower()  == (currcode).lower() :
                        for datum in date_range(start_date,end_date) :
                            occ[get_day(datum) - 1] = occ[get_day(datum) - 1] + res_line.zimmeranz

        zimmer_obj_list = {}
        zimmer = Zimmer()
        zimkateg = Zimkateg()
        for zimmer.sleeping, zimmer._recid, zimkateg.zikatnr, zimkateg._recid in db_session.query(Zimmer.sleeping, Zimmer._recid, Zimkateg.zikatnr, Zimkateg._recid).join(Zimkateg,(Zimkateg.zikatnr == Zimmer.zikatnr) & (Zimkateg.typ == i_typ) & (Zimkateg.verfuegbarkeit)).filter(
                 (Zimmer.sleeping)).order_by(Zimmer.zikatnr).all():
            if zimmer_obj_list.get(zimmer._recid):
                continue
            else:
                zimmer_obj_list[zimmer._recid] = True


            anzahl = anzahl + 1

        outorder_obj_list = {}
        outorder = Outorder()
        zimmer = Zimmer()
        zimkateg = Zimkateg()
        for outorder.gespstart, outorder.gespende, outorder._recid, zimmer.sleeping, zimmer._recid, zimkateg.zikatnr, zimkateg._recid in db_session.query(Outorder.gespstart, Outorder.gespende, Outorder._recid, Zimmer.sleeping, Zimmer._recid, Zimkateg.zikatnr, Zimkateg._recid).join(Zimmer,(Zimmer.zinr == Outorder.zinr) & (Zimmer.sleeping)).join(Zimkateg,(Zimkateg.zikatnr == Zimmer.zikatnr) & (Zimkateg.typ == i_typ)).filter(
                 (Outorder.betriebsnr <= 1) & (Outorder.gespstart <= tdate) & (Outorder.gespende >= fdate)).order_by(Outorder._recid).all():
            if outorder_obj_list.get(outorder._recid):
                continue
            else:
                outorder_obj_list[outorder._recid] = True

            if outorder.gespstart <= fdate:
                start_date = fdate
            else:
                start_date = outorder.gespstart

            if outorder.gespende >= tdate:
                end_date = tdate
            else:
                end_date = tdate
            for datum in date_range(start_date,end_date) :
                ooo[get_day(datum) - 1] = ooo[get_day(datum) - 1] + 1

    elif not cat_flag:

        res_line_obj_list = {}
        res_line = Res_line()
        zimkateg = Zimkateg()
        for res_line.zinr, res_line.abreise, res_line.ankunft, res_line.zimmeranz, res_line.zimmer_wunsch, res_line._recid, zimkateg.zikatnr, zimkateg._recid in db_session.query(Res_line.zinr, Res_line.abreise, Res_line.ankunft, Res_line.zimmeranz, Res_line.zimmer_wunsch, Res_line._recid, Zimkateg.zikatnr, Zimkateg._recid).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).filter(
                 (Res_line.active_flag <= 1) & (Res_line.resstatus <= 6) & (Res_line.resstatus != 3) & (Res_line.resstatus != 4) & (Res_line.resstatus != 12) & (Res_line.resstatus != 11) & (Res_line.resstatus != 13) & (Res_line.kontignr >= 0) & (Res_line.l_zuordnung[inc_value(2)] == 0) & (Res_line.ankunft <= tdate) & (Res_line.abreise >= fdate) & (Res_line.zikatnr == i_typ)).order_by(Res_line._recid).all():
            if res_line_obj_list.get(res_line._recid):
                continue
            else:
                res_line_obj_list[res_line._recid] = True


            do_it = True

            if res_line.zinr != "":

                zimmer = get_cache (Zimmer, {"zinr": [(eq, res_line.zinr)]})
                do_it = zimmer.sleeping

            if do_it:

                if res_line.ankunft == res_line.abreise:
                    end_date = res_line.abreise
                else:
                    end_date = res_line.abreise - timedelta(days=1)

                if res_line.ankunft >= fdate:
                    start_date = res_line.ankunft
                else:
                    start_date = fdate

                if end_date >= tdate:
                    end_date = tdate
                for datum in date_range(start_date,end_date) :
                    occall[get_day(datum) - 1] = occall[get_day(datum) - 1] + res_line.zimmeranz

                if matches(res_line.zimmer_wunsch,r"*$OrigCode$*"):
                    rline_origcode = ""
                    for i in range(1,num_entries(res_line.zimmer_wunsch, ";") - 1 + 1) :
                        iftask = entry(i - 1, res_line.zimmer_wunsch, ";")

                        if substring(iftask, 0, 10) == ("$OrigCode$").lower() :
                            rline_origcode = substring(iftask, 10)
                            break

                    if rline_origcode.lower()  == (currcode).lower() :
                        for datum in date_range(start_date,end_date) :
                            occ[get_day(datum) - 1] = occ[get_day(datum) - 1] + res_line.zimmeranz

        zimmer_obj_list = {}
        zimmer = Zimmer()
        zimkateg = Zimkateg()
        for zimmer.sleeping, zimmer._recid, zimkateg.zikatnr, zimkateg._recid in db_session.query(Zimmer.sleeping, Zimmer._recid, Zimkateg.zikatnr, Zimkateg._recid).join(Zimkateg,(Zimkateg.zikatnr == Zimmer.zikatnr) & (Zimkateg.zikatnr == i_typ) & (Zimkateg.verfuegbarkeit)).filter(
                 (Zimmer.sleeping)).order_by(Zimmer._recid).all():
            if zimmer_obj_list.get(zimmer._recid):
                continue
            else:
                zimmer_obj_list[zimmer._recid] = True


            anzahl = anzahl + 1

        outorder_obj_list = {}
        outorder = Outorder()
        zimmer = Zimmer()
        zimkateg = Zimkateg()
        for outorder.gespstart, outorder.gespende, outorder._recid, zimmer.sleeping, zimmer._recid, zimkateg.zikatnr, zimkateg._recid in db_session.query(Outorder.gespstart, Outorder.gespende, Outorder._recid, Zimmer.sleeping, Zimmer._recid, Zimkateg.zikatnr, Zimkateg._recid).join(Zimmer,(Zimmer.zinr == Outorder.zinr) & (Zimmer.sleeping)).join(Zimkateg,(Zimkateg.zikatnr == Zimmer.zikatnr) & (Zimkateg.zikatnr == i_typ)).filter(
                 (Outorder.betriebsnr <= 1) & (Outorder.gespstart <= tdate) & (Outorder.gespende >= fdate)).order_by(Outorder._recid).all():
            if outorder_obj_list.get(outorder._recid):
                continue
            else:
                outorder_obj_list[outorder._recid] = True

            if outorder.gespstart <= fdate:
                start_date = fdate
            else:
                start_date = outorder.gespstart

            if outorder.gespende >= tdate:
                end_date = tdate
            else:
                end_date = tdate
            for datum in date_range(start_date,end_date) :
                ooo[get_day(datum) - 1] = ooo[get_day(datum) - 1] + 1
    for datum in date_range(fdate,tdate) :

        # queasy = get_cache (Queasy, {"key": [(eq, 171)],"char1": [(eq, currcode)],"number1": [(eq, i_typ)],"date1": [(eq, datum)]})
        queasy = db_session.query(Queasy).filter(
                 (Queasy.key == 171) &
                 (Queasy.char1 == currcode) &
                 (Queasy.number1 == i_typ) &
                 (Queasy.date1 == datum)).with_for_update().first()

        if queasy:
            allot2.allotment[get_day(datum) - 1] = queasy.number3

            if queasy.number2 != occ[get_day(datum) - 1]:
                pass
                queasy.number2 = occ[get_day(datum) - 1]
                queasy.logi3 = True


                pass
                pass
    for i in range(1,31 + 1) :
        allot1.allotment[i - 1] = anzahl - occall[i - 1] - ooo[i - 1]


        allot3.allotment[i - 1] = occ[i - 1]

        if allot2.allotment[i - 1] > allot1.allotment[i - 1]:
            allot2.allotment[i - 1] = allot1.allotment[i - 1]

        if allot1.allotment[i - 1] < 0:
            allot1.allotment[i - 1] = 0

        if allot2.allotment[i - 1] < 0:
            allot2.allotment[i - 1] = 0

    return generate_output()