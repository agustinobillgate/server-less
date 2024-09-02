from functions.additional_functions import *
import decimal
from datetime import date
import re
from sqlalchemy import func
from models import Bediener, Kontline, Guest, Zimkateg, Guest_pr, Res_line, Reservation

def glores_review_webbl(pvilanguage:int, delflag:bool, from_date:date, to_date:date, ci_date:date, resflag1:bool, gflag:bool, cflag:bool, from_name:str, to_name:str):
    str_detail_list = []
    str_summary_list = []
    sum_list_list = []
    lvcarea:str = "glores_review"
    loopi:int = 0
    str_parse:str = ""
    bediener = kontline = guest = zimkateg = guest_pr = res_line = reservation = None

    sum_list = output_list = str_detail = str_summary = k_list = res_list = usr = allot_list = None

    sum_list_list, Sum_list = create_model("Sum_list", {"datum":date, "gastnr":int, "firma":str, "kontcode":str, "zikatnr":int, "kurzbez":str, "erwachs":int, "kind1":int, "gloanz":int, "gresanz":int, "resanz":int, "resnrstr":str})
    output_list_list, Output_list = create_model("Output_list", {"str":str})
    str_detail_list, Str_detail = create_model("Str_detail", {"company_name":str, "address":str, "city":str, "glorescode":str, "pricecode":str, "start_date":str, "pax":str, "ending_date":str, "rmcat":str, "argt":str, "id":str, "chgid":str, "create_date":str, "comments":str, "dates_period":str, "dates_number":[str, 31], "dates_str":[str, 31], "reserved_room":[str, 31], "used_reservation":[str, 31], "not_used":[str, 31], "avail_room":[str, 31], "overbooking":[str, 31], "reservations":str, "residents":str, "cancel_res":str})
    str_summary_list, Str_summary = create_model("Str_summary", {"total_reserve":[str, 31], "used_reserve":[str, 31], "not_used":[str, 31]})
    k_list_list, K_list = create_model("K_list", {"gastnr":int, "bediener_nr":int, "kontcode":str, "ankunft":date, "zikatnr":int, "argt":str, "zimmeranz":[int, 31], "erwachs":int, "kind1":int, "ruecktage":int, "overbooking":int, "abreise":date, "useridanlage":str, "resdate":date, "bemerk":str})
    res_list_list, Res_list = create_model("Res_list", {"flag":str, "count":int, "s1":str})
    allot_list_list, Allot_list = create_model_like(Kontline)

    Usr = Bediener

    db_session = local_storage.db_session

    def generate_output():
        nonlocal str_detail_list, str_summary_list, sum_list_list, lvcarea, loopi, str_parse, bediener, kontline, guest, zimkateg, guest_pr, res_line, reservation
        nonlocal usr


        nonlocal sum_list, output_list, str_detail, str_summary, k_list, res_list, usr, allot_list
        nonlocal sum_list_list, output_list_list, str_detail_list, str_summary_list, k_list_list, res_list_list, allot_list_list
        return {"str-detail": str_detail_list, "str-summary": str_summary_list, "sum-list": sum_list_list}

    def create_list(del_flag:bool):

        nonlocal str_detail_list, str_summary_list, sum_list_list, lvcarea, loopi, str_parse, bediener, kontline, guest, zimkateg, guest_pr, res_line, reservation
        nonlocal usr


        nonlocal sum_list, output_list, str_detail, str_summary, k_list, res_list, usr, allot_list
        nonlocal sum_list_list, output_list_list, str_detail_list, str_summary_list, k_list_list, res_list_list, allot_list_list

        datum:date = None
        usr_init:str = ""
        i:int = 0
        count:int = 0
        currresnr:int = 0
        anz1:[int] = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        anz2:[int] = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        t_anz0:[int] = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        t_anz1:[int] = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        t_anz2:[int] = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        avail_allotm:[int] = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        overbook:[int] = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        wday:str = ""
        loopdatum:int = 0
        loopdatstr:int = 0

        if del_flag:
            output_list_list.clear()
        allot_list_list.clear()
        k_list_list.clear()
        res_list_list.clear()
        sum_list_list.clear()
        for i in range(1,31 + 1) :
            t_anz0[i - 1] = 0
            t_anz1[i - 1] = 0
            t_anz2[i - 1] = 0
            avail_allotm[i - 1] = 0
            overbook[i - 1] = 0
        create_alist()

        for k_list in query(k_list_list):
            guest = db_session.query(Guest).filter((Guest.gastnr == k_list.gastnr)).first()
            if not guest:
                continue


            usr = db_session.query(Usr).filter(
                    (Usr.nr == k_list.bediener_nr)).first()

            zimkateg = db_session.query(Zimkateg).filter(
                    (Zimkateg.zikatnr == k_list.zikatnr)).first()
            str_detail = Str_detail()
            str_detail_list.append(str_detail)

            output_list = Output_list()
            output_list_list.append(output_list)

            STR = translateExtended ("Company  Name  :", lvcarea, "") + " " + guest.name + ", " + guest.anredefirma
            output_list = Output_list()
            output_list_list.append(output_list)

            STR = translateExtended ("Address        :", lvcarea, "") + " " + guest.adresse1 + " " + guest.adresse2
            output_list = Output_list()
            output_list_list.append(output_list)

            STR = translateExtended ("City           :", lvcarea, "") + " " + guest.wohnort + " " + guest.plz
            output_list = Output_list()
            output_list_list.append(output_list)

            STR = translateExtended ("Code           :", lvcarea, "") + " " + k_list.kontcode + "         " + translateExtended ("PriceCode :", lvcarea, "") + " "

            guest_pr = db_session.query(Guest_pr).filter(
                    (Guest_pr.gastnr == guest.gastnr)).first()

            if guest_pr:
                STR = STR + guest_pr.code
            output_list = Output_list()
            output_list_list.append(output_list)

            STR = translateExtended ("Start", lvcarea, "") + "  " + to_string(k_list.ankunft) + "  " + translateExtended ("Pax", lvcarea, "") + " " + to_string(k_list.erwachs) + "/" + to_string(k_list.kind1)
            output_list = Output_list()
            output_list_list.append(output_list)

            STR = translateExtended ("Ending", lvcarea, "") + " " + to_string(k_list.abreise) + "  " + translateExtended ("RmCat", lvcarea, "") + " "

            if zimkateg:
                STR = STR + to_string(zimkateg.kurzbez, "x(6)")
            else:
                STR = STR + "      "

            if usr:
                usr_init = usr.userinit
            else:
                usr_init = "  "
            STR = STR + "  " + translateExtended ("Arg", lvcarea, "") + " " + to_string(k_list.argt, "x(5)") + "  " + translateExtended ("ID", lvcarea, "") + " " + to_string(usr_init) + "  " + translateExtended ("ChgID", lvcarea, "") + " " + to_string(k_list.useridanlage, "x(2)") + "  " + translateExtended ("Date", lvcarea, "") + " " + to_string(k_list.resdat)

            if k_list.bemerk != "":
                output_list = Output_list()
                output_list_list.append(output_list)

                STR = translateExtended ("Comment        :", lvcarea, "") + " " + k_list.bemerk
            output_list = Output_list()
            output_list_list.append(output_list)

            STR = translateExtended ("Dates          :", lvcarea, "") + " " + to_string(from_date) + " - " + to_string(to_date)
            str_detail.company_name = guest.name
            str_detail.address = guest.adresse1
            str_detail.city = guest.wohnort + " " + guest.plz
            str_detail.glorescode = k_list.kontcode
            str_detail.pricecode = guest_pr.code
            str_detail.start_date = to_string(k_list.ankunft)
            str_detail.pax = to_string(k_list.erwachs) + "/" + to_string(k_list.kind1)
            str_detail.ending_date = to_string(k_list.abreise)
            str_detail.rmcat = to_string(zimkateg.kurzbez, "x(6)")
            str_detail.argt = to_string(k_list.argt, "x(5)")
            str_detail.id = to_string(usr_init)
            str_detail.chgID = to_string(k_list.useridanlage, "x(2)")
            str_detail.create_date = to_string(k_list.resdat)
            str_detail.comments = k_list.bemerk
            str_detail.dates_period = to_string(from_date) + " - " + to_string(to_date)


            pass
            output_list = Output_list()
            output_list_list.append(output_list)

            STR = "                "
            datum = from_date
            loopdatum = 0
            while datum <= to_date:
                STR = STR + to_string(get_day(datum) , "99 ")
                loopdatum = loopdatum + 1
                str_detail.dates_number[loopdatum - 1] = to_string(get_day(datum) , "99")


                datum = datum + 1
            output_list = Output_list()
            output_list_list.append(output_list)

            STR = "                "
            datum = from_date
            loopdatstr = 0
            while datum <= to_date:
                STR = STR + wday[get_weekday(datum) - 1] + " "
                loopdatstr = loopdatstr + 1
                str_detail.dates_str[loopdatstr - 1] = wday[get_weekday(datum) - 1]


                datum = datum + 1
            output_list = Output_list()
            output_list_list.append(output_list)

            for i in range(1,108 + 1) :
                STR = STR + "-"
            output_list = Output_list()
            output_list_list.append(output_list)

            STR = to_string(translateExtended ("Reserved Room", lvcarea, "") , "x(15)")
            datum = from_date
            i = 1
            while datum <= to_date:

                if datum >= k_list.ankunft and datum <= k_list.abreise and datum >= (ci_date):
                    t_anz0[i - 1] = t_anz0[i - 1] + k_list.zimmeranz[i - 1]
                    STR = STR + to_string(k_list.zimmeranz[i - 1], "-99")
                    str_detail.reserved_room[i - 1] = to_string(k_list.zimmeranz[i - 1], "-99")


                else:
                    STR = STR + " 00"
                    str_detail.reserved_room[i - 1] = "00"
                i = i + 1
                datum = datum + 1
            for i in range(1,31 + 1) :
                anz1[i - 1] = 0
                anz2[i - 1] = 0

            for res_line in db_session.query(Res_line).filter(
                    (Res_line.gastnr == k_list.gastnr) &  (Res_line.active_flag <= 1) &  (not (Res_line.ankunft > to_date)) &  (not (Res_line.abreise < from_date)) &  (Res_line.resstatus <= 6) &  (Res_line.resstatus != 3) &  (Res_line.resstatus != 4) &  (Res_line.kontignr == 0)).all():
                for datum in range(from_date,to_date + 1) :

                    if res_line.ankunft <= datum and res_line.abreise > datum:

                        sum_list = query(sum_list_list, filters=(lambda sum_list :sum_list.datum == datum and sum_list.gastnr == res_line.gastnr and sum_list.zikatnr == res_line.zikatnr and sum_list.erwachs >= res_line.erwachs), first=True)

                        if not sum_list:

                            sum_list = query(sum_list_list, filters=(lambda sum_list :sum_list.datum == datum and sum_list.gastnr == res_line.gastnr and sum_list.zikatnr == res_line.zikatnr), first=True)

                        if sum_list:
                            sum_list.resAnz = sum_list.resAnz + res_line.zimmeranz

                        if currresnr != res_line.resnr:
                            currresnr = res_line.resnr
                            sum_list.resnrStr = sum_list.resnrStr +\
                                    trim(to_string(res_line.resnr, ">>>>>>>9")) + "; "


            count = 0

            res_line_obj_list = []
            for res_line, kontline in db_session.query(Res_line, Kontline).join(Kontline,(Kontline.kontignr == - Res_line.kontignr) &  (Kontline.kontcode == k_list.kontcode) &  (Kontline.betriebsnr == 1) &  (Kontline.kontstat == 1)).filter(
                    (Res_line.gastnr == k_list.gastnr) &  (Res_line.active_flag <= 1) &  (not (Res_line.ankunft > to_date)) &  (not (Res_line.abreise < from_date)) &  (Res_line.resstatus <= 6) &  (Res_line.resstatus != 3) &  (Res_line.resstatus != 4) &  (Res_line.kontignr < 0)).all():
                if res_line._recid in res_line_obj_list:
                    continue
                else:
                    res_line_obj_list.append(res_line._recid)

                reservation = db_session.query(Reservation).filter(
                        (Reservation.resnr == res_line.resnr)).first()
                for datum in range(from_date,to_date + 1) :

                    if res_line.ankunft <= datum and res_line.abreise > datum:

                        sum_list = query(sum_list_list, filters=(lambda sum_list :sum_list.datum == datum and sum_list.gastnr == res_line.gastnr and sum_list.kontcode == k_list.kontcode), first=True)

                        if sum_list:
                            sum_list.gresAnz = sum_list.gresAnz + res_line.zimmeranz

                if resflag1 and res_line.active_flag == 0:
                    res_list = Res_list()
                    res_list_list.append(res_list)

                    res_list.flag = "r"
                    count = count + 1
                    res_list.count = count
                    s1 = "   " + translateExtended ("ResNo", lvcarea, "") + " " + to_string(res_line.resnr, ">>>>>>9") + " " + translateExtended ("Arrival", lvcarea, "") + " " + to_string(res_line.ankunft) + "  " + translateExtended ("Qty", lvcarea, "") + " " + to_string(res_line.zimmeranz, "99") + "  " + translateExtended ("Pax", lvcarea, "") + " " + to_string(res_line.erwachs) + "/" + to_string(res_line.kind1) + "  " + translateExtended ("Departure", lvcarea, "") + " " + to_string(res_line.abreise) + "  " + translateExtended ("ID", lvcarea, "") + " " + to_string(reservation.useridanlage, "x(2)") + "  " + translateExtended ("ChgID", lvcarea, "") + " " + to_string(res_line.changed_id, "x(2)")

                    if res_line.bemerk != "":
                        res_list = Res_list()
                        res_list_list.append(res_list)

                        count = count + 1
                        res_list.flag = "r"
                        s1 = translateExtended ("Comment        :", lvcarea, "") + " " + res_line.bemerk

                if gflag and res_line.active_flag == 2:
                    res_list = Res_list()
                    res_list_list.append(res_list)

                    res_list.flag = "g"
                    count = count + 1
                    res_list.count = count
                    s1 = "   " + translateExtended ("ResNo", lvcarea, "") + " " + to_string(res_line.resnr, ">>>>>>9") + " " + translateExtended ("Arrival", lvcarea, "") + " " + to_string(res_line.ankunft) + "  " + translateExtended ("Qty", lvcarea, "") + " " + to_string(res_line.zimmeranz, "99") + "  " + translateExtended ("Pax", lvcarea, "") + " " + to_string(res_line.erwachs) + "/" + to_string(res_line.kind1) + "  " + translateExtended ("Departure", lvcarea, "") + " " + to_string(res_line.abreise) + "  " + translateExtended ("ID", lvcarea, "") + " " + to_string(reservation.useridanlage, "x(2)") + "  " + translateExtended ("ChgID", lvcarea, "") + " " + to_string(res_line.changed_id, "x(2)")

                    if res_line.bemerk != "":
                        res_list = Res_list()
                        res_list_list.append(res_list)

                        count = count + 1
                        res_list.flag = "g"
                        s1 = translateExtended ("Comment        :", lvcarea, "") + " " + res_line.bemerk
                datum = from_date
                i = 1
                while datum <= to_date:

                    if datum >= res_line.ankunft and datum < res_line.abreise:
                        anz1[i - 1] = anz1[i - 1] + res_line.zimmeranz
                    i = i + 1
                    datum = datum + 1
            datum = from_date
            i = 1
            while datum <= to_date:
                anz2[i - 1] = k_list.zimmeranz[i - 1] - anz1[i - 1]
                i = i + 1
                datum = datum + 1
            i = 1
            datum = from_date
            while datum <= to_date:
                t_anz1[i - 1] = t_anz1[i - 1] + anz1[i - 1]
                t_anz2[i - 1] = t_anz2[i - 1] + anz2[i - 1]
                i = i + 1
                datum = datum + 1
            output_list = Output_list()
            output_list_list.append(output_list)

            output_list.str = to_string(translateExtended ("Used Rservation", lvcarea, "") , "x(15)")
            datum = from_date
            i = 1
            while datum <= to_date:
                STR = STR + to_string(anz1[i - 1], "-99")
                str_detail.used_reservation[i - 1] = to_string(anz1[i - 1], "-99")


                i = i + 1
                datum = datum + 1
            output_list = Output_list()
            output_list_list.append(output_list)

            STR = to_string(translateExtended ("Not used", lvcarea, "") , "x(15)")
            datum = from_date
            i = 1
            while datum <= to_date:

                if anz2[i - 1] > 0:
                    STR = STR + to_string(anz2[i - 1], "-99")
                    str_detail.not_used[i - 1] = to_string(anz2[i - 1], "-99")


                else:
                    STR = STR + " 00"
                    str_detail.not_used[i - 1] = "00"


                i = i + 1
                datum = datum + 1
            output_list = Output_list()
            output_list_list.append(output_list)

            STR = to_string(translateExtended ("Available", lvcarea, "") , "x(15)")
            datum = from_date
            i = 1
            while datum <= to_date:

                if datum >= (ci_date + k_list.ruecktage):

                    if anz2[i - 1] > 0:
                        avail_allotm[i - 1] = anz2[i - 1]
                        STR = STR + to_string(avail_allotm[i - 1], "-99")
                        str_detail.avail_room[i - 1] = to_string(avail_allotm[i - 1], "-99")


                    else:
                        avail_allotm[i - 1] = 0
                        STR = STR + " 00"
                        str_detail.avail_room[i - 1] = "00"


                else:
                    avail_allotm[i - 1] = 0
                    STR = STR + " 00"
                    str_detail.avail_room[i - 1] = "00"


                i = i + 1
                datum = datum + 1
            output_list = Output_list()
            output_list_list.append(output_list)

            STR = to_string(translateExtended ("Overbooking", lvcarea, "") , "x(15)")
            datum = from_date
            i = 1
            while datum <= to_date:

                if datum >= (ci_date + k_list.ruecktage):

                    if anz2[i - 1] < 0:
                        overbook[i - 1] = - anz2[i - 1]
                        STR = STR + to_string(overbook[i - 1], "-99")
                        str_detail.overbooking[i - 1] = to_string(overbook[i - 1], "-99")


                    else:
                        overbook[i - 1] = 0
                        STR = STR + " 00"
                        str_detail.overbooking[i - 1] = "00"


                else:
                    overbook[i - 1] = 0
                    STR = STR + " 00"
                    str_detail.overbooking[i - 1] = "00"


                i = i + 1
                datum = datum + 1

            if resflag1:
                i = 1
                output_list = Output_list()
                output_list_list.append(output_list)

                STR = translateExtended ("Reservations :", lvcarea, "") + " "

                for res_list in query(res_list_list, filters=(lambda res_list :res_list.flag.lower()  == "r")):

                    if i > 1:
                        output_list = Output_list()
                        output_list_list.append(output_list)

                        STR = "             " + s1
                    else:
                        STR = STR + s1
                    i = i + 1
                    str_detail.reservations = s1

            if gflag:
                i = 1
                output_list = Output_list()
                output_list_list.append(output_list)

                STR = translateExtended ("Residents   :", lvcarea, "") + " "

                for res_list in query(res_list_list, filters=(lambda res_list :res_list.flag.lower()  == "g")):

                    if i > 1:
                        output_list = Output_list()
                        output_list_list.append(output_list)

                        STR = "             " + s1
                    else:
                        STR = STR + s1
                    i = i + 1
                    str_detail.residents = s1

            if cflag:

                res_line_obj_list = []
                for res_line, kontline in db_session.query(Res_line, Kontline).join(Kontline,(Kontline.kontignr == - Res_line.kontignr) &  (Kontline.kontcode == k_list.kontcode) &  (Kontline.betriebsnr == 1) &  (Kontline.kontstat == 1)).filter(
                        (Res_line.kontignr < 0) &  (Res_line.gastnr == kontline.gastnr) &  (Res_line.resstatus == 9)).all():
                    if res_line._recid in res_line_obj_list:
                        continue
                    else:
                        res_line_obj_list.append(res_line._recid)

                    reservation = db_session.query(Reservation).filter(
                            (Reservation.resnr == res_line.resnr)).first()
                    res_list = Res_list()
                    res_list_list.append(res_list)

                    res_list.flag = "c"
                    count = count + 1
                    res_list.count = count
                    s1 = "   " + translateExtended ("ResNo", lvcarea, "") + " " + to_string(res_line.resnr, ">>>>>>9") + " " + translateExtended ("Arrival", lvcarea, "") + " " + to_string(res_line.ankunft) + "  " + translateExtended ("Qty", lvcarea, "") + " " + to_string(res_line.zimmeranz, "99") + "  " + translateExtended ("Pax", lvcarea, "") + " " + to_string(res_line.erwachs) + "/" + to_string(res_line.kind1) + "  " + translateExtended ("Departure", lvcarea, "") + " " + to_string(res_line.abreise) + "  " + translateExtended ("ID", lvcarea, "") + " " + to_string(reservation.useridanlage, "x(2)") + "  " + translateExtended ("ChgID", lvcarea, "") + " " + to_string(res_line.changed_id, "x(2)")

                    if res_line.bemerk != "":
                        res_list = Res_list()
                        res_list_list.append(res_list)

                        count = count + 1
                        res_list.flag = "r"
                        s1 = translateExtended ("Comment        :", lvcarea, "") + " " + res_line.bemerk
                i = 1
                output_list = Output_list()
                output_list_list.append(output_list)

                STR = translateExtended ("Cancelled   :", lvcarea, "") + " "

                for res_list in query(res_list_list, filters=(lambda res_list :res_list.flag.lower()  == "c")):

                    if i > 1:
                        output_list = Output_list()
                        output_list_list.append(output_list)

                        STR = "             " + s1
                    else:
                        STR = STR + s1
                    str_detail.cancel_res = s1


                    i = i + 1
            output_list = Output_list()
            output_list_list.append(output_list)

            for i in range(1,108 + 1) :
                STR = STR + " == "
            output_list = Output_list()
            output_list_list.append(output_list)

        count = 2
        for i in range(1,31 + 1) :

            if t_anz0[i - 1] >= 100:
                count = 3

        if count == 3:
            i = 1
            datum = from_date
            output_list = Output_list()
            output_list_list.append(output_list)

            while datum <= to_date:

                if i <= 1:
                    STR = to_string(translateExtended ("Total Reserve", lvcarea, "") , "x(14)") + to_string(t_anz0[i - 1], "->>>9")
                else:
                    STR = STR + to_string(t_anz0[i - 1], "->>>>9")
                i = i + 2
                datum = datum + 2
            i = 2
            datum = from_date + 1
            output_list = Output_list()
            output_list_list.append(output_list)

            STR = "               "
            while datum <= to_date:
                STR = STR + to_string(t_anz0[i - 1], "->>>>9")
                i = i + 2
                datum = datum + 2
        else:
            i = 1
            datum = from_date
            output_list = Output_list()
            output_list_list.append(output_list)

            while datum <= to_date:

                if i <= 1:
                    STR = to_string(translateExtended ("Total Reserve", lvcarea, "") , "x(15)") + to_string(t_anz0[i - 1], "->9")
                else:
                    STR = STR + to_string(t_anz0[i - 1], "->9")
                i = i + 1
                datum = datum + 1
        count = 2
        for i in range(1,31 + 1) :

            if t_anz1[i - 1] >= 100:
                count = 3

        if count == 3:
            i = 1
            datum = from_date
            output_list = Output_list()
            output_list_list.append(output_list)

            while datum <= to_date:

                if i <= 1:
                    STR = to_string(translateExtended ("Used Reserve", lvcarea, "") , "x(15)") + to_string(t_anz1[i - 1], "->>>>9")
                else:
                    STR = STR + to_string(t_anz1[i - 1], "->>>>9")
                i = i + 2
                datum = datum + 2
            i = 2
            datum = from_date + 1
            output_list = Output_list()
            output_list_list.append(output_list)

            STR = "         "
            while datum <= to_date:
                STR = STR + to_string(t_anz1[i - 1], "->>>>9")
                i = i + 2
                datum = datum + 2
        else:
            i = 1
            datum = from_date
            output_list = Output_list()
            output_list_list.append(output_list)

            while datum <= to_date:

                if i <= 1:
                    STR = to_string(translateExtended ("Used Reserve", lvcarea, "") , "x(15)") + to_string(t_anz1[i - 1], "->9")
                else:
                    STR = STR + to_string(t_anz1[i - 1], "->9")
                i = i + 1
                datum = datum + 1
        count = 2
        for i in range(1,31 + 1) :

            if t_anz2[i - 1] >= 100:
                count = 3

        if count == 3:
            i = 1
            datum = from_date
            output_list = Output_list()
            output_list_list.append(output_list)

            while datum <= to_date:

                if t_anz2[i - 1] > 0:

                    if i <= 1:
                        STR = to_string(translateExtended ("Not used", lvcarea, "") , "x(15)") + to_string(t_anz2[i - 1], "->>>>9")
                    else:
                        STR = STR + to_string(t_anz2[i - 1], "->>>>9")
                else:

                    if i <= 1:
                        STR = to_string(translateExtended ("Not used", lvcarea, "") , "x(15)") + to_string(0, "->>>>9")
                    else:
                        STR = STR + to_string(0, "->>>>9")
                i = i + 2
                datum = datum + 2
            i = 2
            datum = from_date + 1
            output_list = Output_list()
            output_list_list.append(output_list)

            STR = "         "
            while datum <= to_date:
                STR = STR + to_string(t_anz2[i - 1], "->>>>9")
                i = i + 2
                datum = datum + 2
        else:
            i = 1
            datum = from_date
            output_list = Output_list()
            output_list_list.append(output_list)

            while datum <= to_date:

                if t_anz2[i - 1] > 0:

                    if i <= 1:
                        STR = to_string(translateExtended ("Not used", lvcarea, "") , "x(15)") + to_string(t_anz2[i - 1], "->9")
                    else:
                        STR = STR + to_string(t_anz2[i - 1], "->9")
                else:

                    if i <= 1:
                        STR = to_string(translateExtended ("Not used", lvcarea, "") , "x(15)") + to_string(0, "->9")
                    else:
                        STR = STR + to_string(0, "->9")
                i = i + 1
                datum = datum + 1

    def create_alist():

        nonlocal str_detail_list, str_summary_list, sum_list_list, lvcarea, loopi, str_parse, bediener, kontline, guest, zimkateg, guest_pr, res_line, reservation
        nonlocal usr


        nonlocal sum_list, output_list, str_detail, str_summary, k_list, res_list, usr, allot_list
        nonlocal sum_list_list, output_list_list, str_detail_list, str_summary_list, k_list_list, res_list_list, allot_list_list

        curr_code:str = ""
        d:date = None
        d1:date = None
        d2:date = None
        i:int = 0

        kontline_obj_list = []
        for kontline, guest in db_session.query(Kontline, Guest).join(Guest,(Guest.gastnr == Kontline.gastnr) &  (func.lower(Guest.name) >= (from_name).lower()) &  (func.lower(Guest.name) <= (to_name).lower())).filter(
                (Kontline.betriebsnr == 1) &  (not (Kontline.ankunft > to_date)) &  (not (Kontline.abreise < from_date)) &  (Kontline.kontstat == 1)).all():
            if kontline._recid in kontline_obj_list:
                continue
            else:
                kontline_obj_list.append(kontline._recid)

            if curr_code != kontline.kontcode:

                usr = db_session.query(Usr).filter(
                        (Usr.nr == kontline.bediener_nr)).first()
                curr_code = kontline.kontcode
                k_list = K_list()
                k_list_list.append(k_list)

                k_list.gastnr = guest.gastnr
                k_list.kontcode = curr_code
                k_list.ankunft = kontline.ankunft
                k_list.zikatnr = kontline.zikatnr
                k_list.argt = kontline.arrangement
                k_list.erwachs = kontline.erwachs
                k_list.kind1 = kontline.kind1
                k_list.ruecktage = kontline.ruecktage
                k_list.overbooking = kontline.overbooking
                k_list.abreise = kontline.abreise
                k_list.useridanlage = kontline.useridanlage
                k_list.resdat = kontline.resdat
                k_list.bemerk = kontline.bemerk

                if usr:
                    k_list.bediener_nr = usr.nr
            else:
                k_list.abreise = kontline.abreise

            if from_date > kontline.ankunft:
                d1 = from_date
            else:
                d1 = kontline.ankunft

            if to_date < kontline.abreise:
                d2 = to_date
            else:
                d2 = kontline.abreise
            i = d1 - from_date
            for d in range(d1,d2 + 1) :
                sum_list = Sum_list()
                sum_list_list.append(sum_list)


                zimkateg = db_session.query(Zimkateg).filter(
                        (Zimkateg.zikatnr == k_list.zikatnr)).first()
                sum_list.datum = d
                sum_list.gastnr = kontline.gastnr
                sum_list.firma = guest.name
                sum_list.kontcode = kontline.kontcode
                sum_list.zikatnr = kontline.zikatnr
                sum_list.gloAnz = kontline.zimmeranz
                sum_list.erwachs = kontline.erwachs
                sum_list.kind1 = kontline.kind1

                if zimkateg:
                    sum_list.kurzbez = zimkateg.kurzbez


                i = i + 1

                if d >= kontline.ankunft and d <= kontline.abreise:
                    k_list.zimmeranz[i - 1] = kontline.zimmeranz


    create_list(delflag)
    str_summary = Str_summary()
    str_summary_list.append(str_summary)


    for output_list in query(output_list_list):

        if re.match(".*total reserve.*",output_list.str):
            str_parse = substring(output_list.str, 14)
            for loopi in range(1,num_entries(str_parse, " ")  + 1) :

                if loopi <= 31:
                    str_summary.total_reserve[loopi - 1] = entry(loopi - 1, str_parse, " ")

        elif re.match(".*used reserve.*",output_list.str):
            str_parse = substring(output_list.str, 14)
            for loopi in range(1,num_entries(str_parse, " ")  + 1) :

                if loopi <= 31:
                    str_summary.used_reserve[loopi - 1] = entry(loopi - 1, str_parse, " ")

        elif re.match(".*not used.*",output_list.str):
            str_parse = substring(output_list.str, 14)
            for loopi in range(1,num_entries(str_parse, " ")  + 1) :

                if loopi <= 31:
                    str_summary.not_used[loopi - 1] = entry(loopi - 1, str_parse, " ")

    return generate_output()