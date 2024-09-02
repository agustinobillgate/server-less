from functions.additional_functions import *
import decimal
from datetime import date
from sqlalchemy import func
import re
from models import Queasy, Zimkateg, Res_line, Zimmer, Outorder

def update_allotmentbyratebl(currcode:str, rmtype:str, curr_month:int, curr_year:int):
    allot_list_list = []
    cat_flag:bool = False
    do_it:bool = False
    occall:[int] = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    occ:[int] = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    ooo:[int] = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    anzahl:int = 0
    i:int = 0
    i_typ:int = 0
    fdate:date = None
    tdate:date = None
    start_date:date = None
    end_date:date = None
    datum:date = None
    rline_origcode:str = ""
    iftask:str = ""
    mestoken:str = ""
    mesvalue:str = ""
    queasy = zimkateg = res_line = zimmer = outorder = None

    allot_list = allot1 = allot2 = allot3 = None

    allot_list_list, Allot_list = create_model("Allot_list", {"bezeich":str, "allotment":[int, 31], "nr":int})

    Allot1 = Allot_list
    allot1_list = allot_list_list

    Allot2 = Allot_list
    allot2_list = allot_list_list

    Allot3 = Allot_list
    allot3_list = allot_list_list


    db_session = local_storage.db_session

    def generate_output():
        nonlocal allot_list_list, cat_flag, do_it, occall, occ, ooo, anzahl, i, i_typ, fdate, tdate, start_date, end_date, datum, rline_origcode, iftask, mestoken, mesvalue, queasy, zimkateg, res_line, zimmer, outorder
        nonlocal allot1, allot2, allot3


        nonlocal allot_list, allot1, allot2, allot3
        nonlocal allot_list_list
        return {"allot-list": allot_list_list}

    queasy = db_session.query(Queasy).filter(
            (Queasy.key == 152)).first()

    if queasy:
        cat_flag = True

    queasy = db_session.query(Queasy).filter(
            (Queasy.key == 152) &  (func.lower(Queasy.char1) == (rmtype).lower())).first()

    if queasy:
        i_typ = queasy.number1

    elif not queasy:

        zimkateg = db_session.query(Zimkateg).filter(
                (func.lower(Zimkateg.kurzbez) == (rmtype).lower())).first()

        if zimkateg:
            i_typ = zimkateg.zikatnr
    allot_list = Allot_list()
    allot_list_list.append(allot_list)

    allot_list.nr = 1
    allot_list.bezeich = "AvailAllRate"


    allot_list = Allot_list()
    allot_list_list.append(allot_list)

    allot_list.nr = 2
    allot_list.bezeich = "AllotByRate"


    allot_list = Allot_list()
    allot_list_list.append(allot_list)

    allot_list.nr = 3
    allot_list.bezeich = "OccByRate"

    allot1 = query(allot1_list, filters=(lambda allot1 :allot1.nr == 1), first=True)

    allot2 = query(allot2_list, filters=(lambda allot2 :allot2.nr == 2), first=True)

    allot3 = query(allot3_list, filters=(lambda allot3 :allot3.nr == 3), first=True)

    if curr_month == 12:
        tdate = date_mdy(1, 1, curr_year + 1)
    else:
        tdate = date_mdy(curr_month + 1, 1, curr_year)
    fdate = date_mdy(curr_month, 1, curr_year)
    tdate = tdate - 1

    if cat_flag:

        res_line_obj_list = []
        for res_line, zimkateg in db_session.query(Res_line, Zimkateg).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr) &  (Zimkateg.typ == i_typ)).filter(
                (Res_line.active_flag <= 1) &  (Res_line.resstatus <= 6) &  (Res_line.resstatus != 3) &  (Res_line.resstatus != 4) &  (Res_line.resstatus != 12) &  (Res_line.resstatus != 11) &  (Res_line.resstatus != 13) &  (Res_line.kontignr >= 0) &  (Res_line.l_zuordnung[2] == 0) &  (Res_line.ankunft <= tdate) &  (Res_line.abreise >= fdate) &  (Res_line.zimmer_wunsch.op("~")(".*\$OrigCode\$.*"))).all():
            if res_line._recid in res_line_obj_list:
                continue
            else:
                res_line_obj_list.append(res_line._recid)


            do_it = True

            if res_line.zinr != "":

                zimmer = db_session.query(Zimmer).filter(
                        (Zimmer.zinr == res_line.zinr)).first()
                do_it = zimmer.sleeping

            if do_it:

                if res_line.ankunft == res_line.abreise:
                    end_date = res_line.abreise
                else:
                    end_date = res_line.abreise - 1

                if res_line.ankunft >= fdate:
                    start_date = res_line.ankunft
                else:
                    start_date = fdate

                if end_date >= tdate:
                    end_date = tdate
                for datum in range(start_date,end_date + 1) :
                    occall[get_day(datum) - 1] = occall[get_day(datum) - 1] + res_line.zimmeranz

                if re.match(".*\$OrigCode\$.*",res_line.zimmer_wunsch):
                    rline_origcode = ""
                    for i in range(1,num_entries(res_line.zimmer_wunsch, ";") - 1 + 1) :
                        iftask = entry(i - 1, res_line.zimmer_wunsch, ";")

                        if substring(iftask, 0, 10) == "$OrigCode$":
                            rline_origcode = substring(iftask, 10)
                            break

                    if rline_origcode.lower()  == (currcode).lower() :
                        for datum in range(start_date,end_date + 1) :
                            occ[get_day(datum) - 1] = occ[get_day(datum) - 1] + res_line.zimmeranz

        zimmer_obj_list = []
        for zimmer, zimkateg in db_session.query(Zimmer, Zimkateg).join(Zimkateg,(Zimkateg.zikatnr == Zimmer.zikatnr) &  (Zimkateg.typ == i_typ) &  (Zimkateg.verfuegbarkeit)).filter(
                (Zimmer.sleeping)).all():
            if zimmer._recid in zimmer_obj_list:
                continue
            else:
                zimmer_obj_list.append(zimmer._recid)


            anzahl = anzahl + 1

        outorder_obj_list = []
        for outorder, zimmer, zimkateg in db_session.query(Outorder, Zimmer, Zimkateg).join(Zimmer,(Zimmer.zinr == Outorder.zinr) &  (Zimmer.sleeping)).join(Zimkateg,(Zimkateg.zikatnr == zimmer.zikatnr) &  (Zimkateg.typ == i_typ)).filter(
                (Outorder.betriebsnr <= 1) &  (Outorder.gespstart <= tdate) &  (Outorder.gespende >= fdate)).all():
            if outorder._recid in outorder_obj_list:
                continue
            else:
                outorder_obj_list.append(outorder._recid)

            if outorder.gespstart <= fdate:
                start_date = fdate
            else:
                start_date = outorder.gespstart

            if outorder.gespende >= tdate:
                end_date = tdate
            else:
                end_date = tdate
            for datum in range(start_date,end_date + 1) :
                ooo[get_day(datum) - 1] = ooo[get_day(datum) - 1] + 1

    elif not cat_flag:

        res_line_obj_list = []
        for res_line, zimkateg in db_session.query(Res_line, Zimkateg).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).filter(
                (Res_line.active_flag <= 1) &  (Res_line.resstatus <= 6) &  (Res_line.resstatus != 3) &  (Res_line.resstatus != 4) &  (Res_line.resstatus != 12) &  (Res_line.resstatus != 11) &  (Res_line.resstatus != 13) &  (Res_line.kontignr >= 0) &  (Res_line.l_zuordnung[2] == 0) &  (Res_line.ankunft <= tdate) &  (Res_line.abreise >= fdate) &  (Res_line.zikatnr == i_typ)).all():
            if res_line._recid in res_line_obj_list:
                continue
            else:
                res_line_obj_list.append(res_line._recid)


            do_it = True

            if res_line.zinr != "":

                zimmer = db_session.query(Zimmer).filter(
                        (Zimmer.zinr == res_line.zinr)).first()
                do_it = zimmer.sleeping

            if do_it:

                if res_line.ankunft == res_line.abreise:
                    end_date = res_line.abreise
                else:
                    end_date = res_line.abreise - 1

                if res_line.ankunft >= fdate:
                    start_date = res_line.ankunft
                else:
                    start_date = fdate

                if end_date >= tdate:
                    end_date = tdate
                for datum in range(start_date,end_date + 1) :
                    occall[get_day(datum) - 1] = occall[get_day(datum) - 1] + res_line.zimmeranz

                if re.match(".*\$OrigCode\$.*",res_line.zimmer_wunsch):
                    rline_origcode = ""
                    for i in range(1,num_entries(res_line.zimmer_wunsch, ";") - 1 + 1) :
                        iftask = entry(i - 1, res_line.zimmer_wunsch, ";")

                        if substring(iftask, 0, 10) == "$OrigCode$":
                            rline_origcode = substring(iftask, 10)
                            break

                    if rline_origcode.lower()  == (currcode).lower() :
                        for datum in range(start_date,end_date + 1) :
                            occ[get_day(datum) - 1] = occ[get_day(datum) - 1] + res_line.zimmeranz

        zimmer_obj_list = []
        for zimmer, zimkateg in db_session.query(Zimmer, Zimkateg).join(Zimkateg,(Zimkateg.zikatnr == Zimmer.zikatnr) &  (Zimkateg.zikatnr == i_typ) &  (Zimkateg.verfuegbarkeit)).filter(
                (Zimmer.sleeping)).all():
            if zimmer._recid in zimmer_obj_list:
                continue
            else:
                zimmer_obj_list.append(zimmer._recid)


            anzahl = anzahl + 1

        outorder_obj_list = []
        for outorder, zimmer, zimkateg in db_session.query(Outorder, Zimmer, Zimkateg).join(Zimmer,(Zimmer.zinr == Outorder.zinr) &  (Zimmer.sleeping)).join(Zimkateg,(Zimkateg.zikatnr == zimmer.zikatnr) &  (Zimkateg.zikatnr == i_typ)).filter(
                (Outorder.betriebsnr <= 1) &  (Outorder.gespstart <= tdate) &  (Outorder.gespende >= fdate)).all():
            if outorder._recid in outorder_obj_list:
                continue
            else:
                outorder_obj_list.append(outorder._recid)

            if outorder.gespstart <= fdate:
                start_date = fdate
            else:
                start_date = outorder.gespstart

            if outorder.gespende >= tdate:
                end_date = tdate
            else:
                end_date = tdate
            for datum in range(start_date,end_date + 1) :
                ooo[get_day(datum) - 1] = ooo[get_day(datum) - 1] + 1
    for datum in range(fdate,tdate + 1) :

        queasy = db_session.query(Queasy).filter(
                (Queasy.key == 171) &  (func.lower(Queasy.char1) == (currcode).lower()) &  (Queasy.number1 == i_typ) &  (Queasy.date1 == datum)).first()

        if queasy:
            allot2.allotment[get_day(datum) - 1] = queasy.number3

            if queasy.number2 != occ[get_day(datum) - 1]:

                queasy = db_session.query(Queasy).first()
                queasy.number2 = occ[get_day(datum) - 1]
                queasy.logi3 = True

                queasy = db_session.query(Queasy).first()


        queasy = db_session.query(Queasy).filter(
                (Queasy.key == 171) &  (Queasy.char1 == "") &  (Queasy.number1 == i_typ) &  (Queasy.date1 == datum)).first()

        if queasy:

            queasy = db_session.query(Queasy).first()
            queasy.number2 = occall[get_day(datum) - 1]
            queasy.number3 = ooo[get_day(datum) - 1]

            queasy = db_session.query(Queasy).first()

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