from functions.additional_functions import *
import decimal
from datetime import date
import re
from models import Htparam, Mealcoup, Res_line, Guest, Arrangement, Argt_line

def bfast_card_reportbl(room:str, fdate:date, mealtime:str, dummyinput:str):
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
    strdayuse:str = ""
    strday:str = ""
    htparam = mealcoup = res_line = guest = arrangement = argt_line = None

    bfast_data = None

    bfast_data_list, Bfast_data = create_model("Bfast_data", {"tdate":date, "roomnr":str, "resnr":int, "guestnr":int, "vip":bool, "nation":str, "guestname":str, "totaladult":int, "totalcompli":int, "totalchild":int, "totaluse":int, "dummychr":str})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal bfast_data_list, getdatanr, i, ii, sumadult, sumcompl, sumchild, sumtotuse, dateval, artgrp_abf, artgrp_lunch, artgrp_dinner, tempresnr, strdayuse, strday, htparam, mealcoup, res_line, guest, arrangement, argt_line


        nonlocal bfast_data
        nonlocal bfast_data_list
        return {"bfast-data": bfast_data_list}

    def fill_data(used:int, daycount:int):

        nonlocal bfast_data_list, getdatanr, i, ii, sumadult, sumcompl, sumchild, sumtotuse, dateval, artgrp_abf, artgrp_lunch, artgrp_dinner, tempresnr, strdayuse, strday, htparam, mealcoup, res_line, guest, arrangement, argt_line


        nonlocal bfast_data
        nonlocal bfast_data_list

        tdate:date = None
        totadult:int = 0
        totcompli:int = 0
        totchild:int = 0
        j:int = 0
        tmpstr:str = ""
        tmpint:int = 0
        day_use:date = None
        tdate = mealcoup.ankunft + used
        day_use = mealcoup.ankunft + daycount

        if day_use == fdate:

            arrangement = db_session.query(Arrangement).filter(
                    (Arrangement == res_line.arrangement)).first()

            for argt_line in db_session.query(Argt_line).filter(
                    (Argt_line.argtnr == arrangement.argtnr)).all():

                if argt_line.argt_artnr == artgrp_abf and mealtime.lower()  == "Breakfast":

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

                        if re.match(".*ChAge.*",entry(j - 1, res_line.zimmer_wunsch, ";")):
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
            bfast_data.roomNr = mealcoup.zinr
            bfast_data.resNr = mealcoup.resnr
            bfast_data.guestNr = guest.gastnr
            bfast_data.guestName = guest.name + ", " + guest.vorname1 + " " + guest.anrede1
            bfast_data.totalAdult = totadult
            bfast_data.totalCompli = totcompli
            bfast_data.totalChild = totchild
            bfast_data.totalUse = mealcoup.verbrauch[daycount - 1]
            sumtotuse = sumtotuse + mealcoup.verbrauch[daycount - 1]

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 125)).first()

    if htparam:
        artgrp_abf = htparam.finteger

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 227)).first()

    if htparam:
        artgrp_lunch = htparam.finteger

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 228)).first()

    if htparam:
        artgrp_dinner = htparam.finteger

    if fdate == None:

        for mealcoup in db_session.query(Mealcoup).filter(
                (Mealcoup.name == mealtime) &  (Mealcoup.zinr.op("~")(".*" + room + ".*"))).all():

            res_line = db_session.query(Res_line).filter(
                    (Res_line.resnr == mealcoup.resnr) &  (Res_line.zinr == mealcoup.zinr)).first()

            if res_line:

                guest = db_session.query(Guest).filter(
                        (Guest.gastnr == res_line.gastnrmember)).first()

                if not guest:

                    guest = db_session.query(Guest).filter(
                            (Guest.gastnr == res_line.gastnr)).first()
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
                (Mealcoup.name == mealtime) &  (Mealcoup.fdate > Mealcoup.ankunft) &  (Mealcoup.fdate <= Mealcoup.abreise) &  (Mealcoup.zinr.op("~")(".*" + room + ".*"))).all():

            res_line = db_session.query(Res_line).filter(
                    (Res_line.resnr == mealcoup.resnr) &  (Res_line.zinr == mealcoup.zinr)).first()

            if res_line:

                guest = db_session.query(Guest).filter(
                        (Guest.gastnr == res_line.gastnrmember)).first()

                if not guest:

                    guest = db_session.query(Guest).filter(
                            (Guest.gastnr == res_line.gastnr)).first()
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

    bfast_data.roomNr = "T O T A L"
    bfast_data.totalAdult = sumadult
    bfast_data.totalCompli = sumcompl
    bfast_data.totalChild = sumchild
    bfast_data.totalUse = sumtotuse

    return generate_output()