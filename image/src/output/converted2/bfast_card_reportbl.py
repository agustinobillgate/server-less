#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from sqlalchemy import func
from models import Htparam, Mealcoup, Res_line, Guest, Arrangement, Argt_line

def bfast_card_reportbl(room:string, fdate:date, mealtime:string, dummyinput:string):

    prepare_cache ([Htparam, Mealcoup, Res_line, Guest, Arrangement, Argt_line])

    bfast_data_list = []
    getdatanr:int = 0
    i:int = 0
    ii:int = 0
    sumadult:int = 0
    sumcompl:int = 0
    sumchild:int = 0
    sumtotuse:int = 0
    dateval:int = 0
    artgrp_abf:int = 0
    artgrp_lunch:int = 0
    artgrp_dinner:int = 0
    tempresnr:int = 0
    strdayuse:string = ""
    strday:string = ""
    htparam = mealcoup = res_line = guest = arrangement = argt_line = None

    bfast_data = None

    bfast_data_list, Bfast_data = create_model("Bfast_data", {"tdate":date, "roomnr":string, "resnr":int, "guestnr":int, "vip":bool, "nation":string, "guestname":string, "totaladult":int, "totalcompli":int, "totalchild":int, "totaluse":int, "dummychr":string})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal bfast_data_list, getdatanr, i, ii, sumadult, sumcompl, sumchild, sumtotuse, dateval, artgrp_abf, artgrp_lunch, artgrp_dinner, tempresnr, strdayuse, strday, htparam, mealcoup, res_line, guest, arrangement, argt_line
        nonlocal room, fdate, mealtime, dummyinput


        nonlocal bfast_data
        nonlocal bfast_data_list

        return {"bfast-data": bfast_data_list}

    def fill_data(used:int, daycount:int):

        nonlocal bfast_data_list, getdatanr, i, ii, sumadult, sumcompl, sumchild, sumtotuse, dateval, artgrp_abf, artgrp_lunch, artgrp_dinner, tempresnr, strdayuse, strday, htparam, mealcoup, res_line, guest, arrangement, argt_line
        nonlocal room, fdate, mealtime, dummyinput


        nonlocal bfast_data
        nonlocal bfast_data_list

        tdate:date = None
        totadult:int = 0
        totcompli:int = 0
        totchild:int = 0
        j:int = 0
        tmpstr:string = ""
        tmpint:int = 0
        day_use:date = None
        tdate = mealcoup.ankunft + timedelta(days=used)
        day_use = mealcoup.ankunft + timedelta(days=daycount)

        if day_use == fdate:

            arrangement = get_cache (Arrangement, {"arrangement": [(eq, res_line.arrangement)]})

            for argt_line in db_session.query(Argt_line).filter(
                     (Argt_line.argtnr == arrangement.argtnr)).order_by(Argt_line._recid).all():

                if argt_line.argt_artnr == artgrp_abf and mealtime.lower()  == ("Breakfast").lower() :

                    if argt_line.fakt_modus == 3 and (tdate - res_line.ankunft == 1):
                        totadult = res_line.erwachs
                        totcompli = res_line.gratis

                    elif argt_line.fakt_modus == 6 and (tdate - res_line.ankunft <= argt_line.intervall):
                        totadult = res_line.erwachs
                        totcompli = res_line.gratis

                    elif argt_line.fakt_modus != 3 and argt_line.fakt_modus != 6:
                        totadult = res_line.erwachs
                        totcompli = res_line.gratis
                    for j in range(1,num_entries(res_line.zimmer_wunsch, ";")  + 1) :

                        if matches(entry(j - 1, res_line.zimmer_wunsch, ";"),r"*ChAge*"):
                            tmpstr = substring(entry(j - 1, res_line.zimmer_wunsch, ";") , 5)
                    for j in range(1,res_line.kind1 + 1) :

                        if j > num_entries(tmpstr, ","):
                            break

                        if to_int(entry(j - 1, tmpstr, ",")) > 12:
                            tmpint = tmpint + 1
                    totadult = totadult + tmpint
                    totchild = res_line.kind1 - tmpint
                    sumadult = sumadult + totadult
                    sumchild = sumchild + totchild
                    sumcompl = sumcompl + totcompli
            bfast_data = Bfast_data()
            bfast_data_list.append(bfast_data)

            bfast_data.tdate = day_use
            bfast_data.roomnr = mealcoup.zinr
            bfast_data.resnr = mealcoup.resnr
            bfast_data.guestnr = guest.gastnr
            bfast_data.guestname = guest.name + ", " + guest.vorname1 + " " + guest.anrede1
            bfast_data.totaladult = totadult
            bfast_data.totalcompli = totcompli
            bfast_data.totalchild = totchild
            bfast_data.totaluse = mealcoup.verbrauch[daycount - 1]
            sumtotuse = sumtotuse + mealcoup.verbrauch[daycount - 1]


    htparam = get_cache (Htparam, {"paramnr": [(eq, 125)]})

    if htparam:
        artgrp_abf = htparam.finteger

    htparam = get_cache (Htparam, {"paramnr": [(eq, 227)]})

    if htparam:
        artgrp_lunch = htparam.finteger

    htparam = get_cache (Htparam, {"paramnr": [(eq, 228)]})

    if htparam:
        artgrp_dinner = htparam.finteger

    if fdate == None:

        for mealcoup in db_session.query(Mealcoup).filter(
                 (Mealcoup.name == mealtime) & (matches(Mealcoup.zinr,("*" + room + "*")))).order_by(Mealcoup._recid).all():

            res_line = get_cache (Res_line, {"resnr": [(eq, mealcoup.resnr)],"zinr": [(eq, mealcoup.zinr)]})

            if res_line:

                guest = get_cache (Guest, {"gastnr": [(eq, res_line.gastnrmember)]})

                if not guest:

                    guest = get_cache (Guest, {"gastnr": [(eq, res_line.gastnr)]})
                getdatanr = 0
                for ii in range(1,32 + 1) :

                    if mealcoup.verbrauch[ii - 1] != 0:
                        getdatanr = getdatanr + 1
                strdayuse = ""

                if mealcoup.verbrauch[0] != 0:
                    strdayuse = "1;"

                if mealcoup.verbrauch[1] != 0:
                    strdayuse = strdayuse + "2;"

                if mealcoup.verbrauch[2] != 0:
                    strdayuse = strdayuse + "3;"

                if mealcoup.verbrauch[3] != 0:
                    strdayuse = strdayuse + "4;"

                if mealcoup.verbrauch[4] != 0:
                    strdayuse = strdayuse + "5;"

                if mealcoup.verbrauch[5] != 0:
                    strdayuse = strdayuse + "6;"

                if mealcoup.verbrauch[6] != 0:
                    strdayuse = strdayuse + "7;"

                if mealcoup.verbrauch[7] != 0:
                    strdayuse = strdayuse + "8;"

                if mealcoup.verbrauch[8] != 0:
                    strdayuse = strdayuse + "9;"

                if mealcoup.verbrauch[9] != 0:
                    strdayuse = strdayuse + "10;"

                if mealcoup.verbrauch[10] != 0:
                    strdayuse = strdayuse + "11;"

                if mealcoup.verbrauch[11] != 0:
                    strdayuse = strdayuse + "12;"

                if mealcoup.verbrauch[12] != 0:
                    strdayuse = strdayuse + "13;"

                if mealcoup.verbrauch[13] != 0:
                    strdayuse = strdayuse + "14;"

                if mealcoup.verbrauch[14] != 0:
                    strdayuse = strdayuse + "15;"

                if mealcoup.verbrauch[15] != 0:
                    strdayuse = strdayuse + "16;"

                if mealcoup.verbrauch[16] != 0:
                    strdayuse = strdayuse + "17;"

                if mealcoup.verbrauch[17] != 0:
                    strdayuse = strdayuse + "18;"

                if mealcoup.verbrauch[18] != 0:
                    strdayuse = strdayuse + "19;"

                if mealcoup.verbrauch[19] != 0:
                    strdayuse = strdayuse + "20;"

                if mealcoup.verbrauch[20] != 0:
                    strdayuse = strdayuse + "21;"

                if mealcoup.verbrauch[21] != 0:
                    strdayuse = strdayuse + "22;"

                if mealcoup.verbrauch[22] != 0:
                    strdayuse = strdayuse + "23;"

                if mealcoup.verbrauch[23] != 0:
                    strdayuse = strdayuse + "24;"

                if mealcoup.verbrauch[24] != 0:
                    strdayuse = strdayuse + "25;"

                if mealcoup.verbrauch[25] != 0:
                    strdayuse = strdayuse + "26;"

                if mealcoup.verbrauch[26] != 0:
                    strdayuse = strdayuse + "27;"

                if mealcoup.verbrauch[27] != 0:
                    strdayuse = strdayuse + "28;"

                if mealcoup.verbrauch[28] != 0:
                    strdayuse = strdayuse + "29;"

                if mealcoup.verbrauch[29] != 0:
                    strdayuse = strdayuse + "30;"

                if mealcoup.verbrauch[30] != 0:
                    strdayuse = strdayuse + "31;"

                if mealcoup.verbrauch[31] != 0:
                    strdayuse = strdayuse + "32"
                for i in range(1,getdatanr + 1) :
                    dateval = to_int(entry(i - 1, strdayuse, ";"))
                    fill_data(i, dateval)
    else:

        for mealcoup in db_session.query(Mealcoup).filter(
                 (Mealcoup.name == mealtime) & (fdate > Mealcoup.ankunft) & (fdate <= Mealcoup.abreise) & (matches(Mealcoup.zinr,("*" + room + "*")))).order_by(Mealcoup._recid).all():

            res_line = get_cache (Res_line, {"resnr": [(eq, mealcoup.resnr)],"zinr": [(eq, mealcoup.zinr)]})

            if res_line:

                guest = get_cache (Guest, {"gastnr": [(eq, res_line.gastnrmember)]})

                if not guest:

                    guest = get_cache (Guest, {"gastnr": [(eq, res_line.gastnr)]})
                getdatanr = 0
                for ii in range(1,32 + 1) :

                    if mealcoup.verbrauch[ii - 1] != 0:
                        getdatanr = getdatanr + 1
                strdayuse = ""

                if mealcoup.verbrauch[0] != 0:
                    strdayuse = "1;"

                if mealcoup.verbrauch[1] != 0:
                    strdayuse = strdayuse + "2;"

                if mealcoup.verbrauch[2] != 0:
                    strdayuse = strdayuse + "3;"

                if mealcoup.verbrauch[3] != 0:
                    strdayuse = strdayuse + "4;"

                if mealcoup.verbrauch[4] != 0:
                    strdayuse = strdayuse + "5;"

                if mealcoup.verbrauch[5] != 0:
                    strdayuse = strdayuse + "6;"

                if mealcoup.verbrauch[6] != 0:
                    strdayuse = strdayuse + "7;"

                if mealcoup.verbrauch[7] != 0:
                    strdayuse = strdayuse + "8;"

                if mealcoup.verbrauch[8] != 0:
                    strdayuse = strdayuse + "9;"

                if mealcoup.verbrauch[9] != 0:
                    strdayuse = strdayuse + "10;"

                if mealcoup.verbrauch[10] != 0:
                    strdayuse = strdayuse + "11;"

                if mealcoup.verbrauch[11] != 0:
                    strdayuse = strdayuse + "12;"

                if mealcoup.verbrauch[12] != 0:
                    strdayuse = strdayuse + "13;"

                if mealcoup.verbrauch[13] != 0:
                    strdayuse = strdayuse + "14;"

                if mealcoup.verbrauch[14] != 0:
                    strdayuse = strdayuse + "15;"

                if mealcoup.verbrauch[15] != 0:
                    strdayuse = strdayuse + "16;"

                if mealcoup.verbrauch[16] != 0:
                    strdayuse = strdayuse + "17;"

                if mealcoup.verbrauch[17] != 0:
                    strdayuse = strdayuse + "18;"

                if mealcoup.verbrauch[18] != 0:
                    strdayuse = strdayuse + "19;"

                if mealcoup.verbrauch[19] != 0:
                    strdayuse = strdayuse + "20;"

                if mealcoup.verbrauch[20] != 0:
                    strdayuse = strdayuse + "21;"

                if mealcoup.verbrauch[21] != 0:
                    strdayuse = strdayuse + "22;"

                if mealcoup.verbrauch[22] != 0:
                    strdayuse = strdayuse + "23;"

                if mealcoup.verbrauch[23] != 0:
                    strdayuse = strdayuse + "24;"

                if mealcoup.verbrauch[24] != 0:
                    strdayuse = strdayuse + "25;"

                if mealcoup.verbrauch[25] != 0:
                    strdayuse = strdayuse + "26;"

                if mealcoup.verbrauch[26] != 0:
                    strdayuse = strdayuse + "27;"

                if mealcoup.verbrauch[27] != 0:
                    strdayuse = strdayuse + "28;"

                if mealcoup.verbrauch[28] != 0:
                    strdayuse = strdayuse + "29;"

                if mealcoup.verbrauch[29] != 0:
                    strdayuse = strdayuse + "30;"

                if mealcoup.verbrauch[30] != 0:
                    strdayuse = strdayuse + "31;"

                if mealcoup.verbrauch[31] != 0:
                    strdayuse = strdayuse + "32"
                for i in range(1,getdatanr + 1) :
                    dateval = to_int(entry(i - 1, strdayuse, ";"))
                    fill_data(i, dateval)
    bfast_data = Bfast_data()
    bfast_data_list.append(bfast_data)

    bfast_data.roomnr = "T O T A L"
    bfast_data.totaladult = sumadult
    bfast_data.totalcompli = sumcompl
    bfast_data.totalchild = sumchild
    bfast_data.totaluse = sumtotuse

    return generate_output()