from functions.additional_functions import *
import decimal
from datetime import date
from sqlalchemy import func
import re
from models import Res_line, Htparam, Zimmer, Bresline, Paramtext, Outorder, Zinrstat

def iproom_assignmentbl(arrival_guest:[Arrival_guest]):
    err_code = 0
    fdate:date = None
    tdate:date = None
    ci_date:date = None
    tot_room:int = 0
    occ_room:int = 0
    occ_perc:decimal = 0
    occ1:decimal = None
    occ2:decimal = 0
    uppest_floor:int = -999
    lowest_floor:int = +999
    mid_floor:int = 0
    uppest_occ_floor:int = 0
    lowest_occ_floor:int = 0
    min_day:int = 3
    cfloor:int = 0
    guest_zinr:str = ""
    curr_co_date:date = None
    curr_zikatnr:int = None
    csetup_array:str = ""
    curr_time:int = 0
    res_line = htparam = zimmer = bresline = paramtext = outorder = zinrstat = None

    arrival_guest = ci_glist = floor_list = avail_room = bedsetup = resline = tresline = tarrival = bavail = bresline = resbuff = flbuff = curr_rline = None

    arrival_guest_list, Arrival_guest = create_model("Arrival_guest", {"i_counter":int, "gastno":int, "resnr":int, "reslinnr":int, "gast":str, "ci":date, "co":date, "rmtype":str, "zinr":str, "argt":str, "adult":str, "child":str, "rmtype_str":str, "room_sharer":bool, "pre_checkin":bool, "argt_str":str, "preference":str, "new_zinr":bool, "zikatnr":int, "l_selected":bool, "kontakt_nr":int, "room_stat":int, "res_status":int})
    ci_glist_list, Ci_glist = create_model("Ci_glist", {"l_selected":bool, "i_counter":int, "resnr":int, "reslinnr":int, "ci":date, "co":date, "rmtype":str, "zinr":str, "room_sharer":bool, "main_reslin":int, "pre_checkin":bool, "preference":str, "pref_floor":int, "pref_bedtype":int, "pref_smoke":int, "new_zinr":bool, "zikatnr":int})
    floor_list_list, Floor_list = create_model("Floor_list", {"floor_number":int, "occupied_room":int, "priority":int})
    avail_room_list, Avail_room = create_model("Avail_room", {"zinr":str, "floor_number":int, "smoke_flag":int, "bed_type":int, "next_guest":bool, "next_arrival":date, "prev_guest":bool, "num_use":int}, {"bed_type": 1, "next_arrival": None})
    bedsetup_list, Bedsetup = create_model("Bedsetup", {"i_setup":int, "room_flag":int})

    Resline = Res_line
    Tresline = Res_line
    Tarrival = Arrival_guest
    tarrival_list = arrival_guest_list

    Bavail = Avail_room
    bavail_list = avail_room_list

    Bresline = Res_line
    Resbuff = Res_line
    Flbuff = Floor_list
    flbuff_list = floor_list_list

    Curr_rline = Res_line

    db_session = local_storage.db_session

    def generate_output():
        nonlocal err_code, fdate, tdate, ci_date, tot_room, occ_room, occ_perc, occ1, occ2, uppest_floor, lowest_floor, mid_floor, uppest_occ_floor, lowest_occ_floor, min_day, cfloor, guest_zinr, curr_co_date, curr_zikatnr, csetup_array, curr_time, res_line, htparam, zimmer, bresline, paramtext, outorder, zinrstat
        nonlocal resline, tresline, tarrival, bavail, bresline, resbuff, flbuff, curr_rline


        nonlocal arrival_guest, ci_glist, floor_list, avail_room, bedsetup, resline, tresline, tarrival, bavail, bresline, resbuff, flbuff, curr_rline
        nonlocal arrival_guest_list, ci_glist_list, floor_list_list, avail_room_list, bedsetup_list
        return {"err_code": err_code}

    def calc_room():

        nonlocal err_code, fdate, tdate, ci_date, tot_room, occ_room, occ_perc, occ1, occ2, uppest_floor, lowest_floor, mid_floor, uppest_occ_floor, lowest_occ_floor, min_day, cfloor, guest_zinr, curr_co_date, curr_zikatnr, csetup_array, curr_time, res_line, htparam, zimmer, bresline, paramtext, outorder, zinrstat
        nonlocal resline, tresline, tarrival, bavail, bresline, resbuff, flbuff, curr_rline


        nonlocal arrival_guest, ci_glist, floor_list, avail_room, bedsetup, resline, tresline, tarrival, bavail, bresline, resbuff, flbuff, curr_rline
        nonlocal arrival_guest_list, ci_glist_list, floor_list_list, avail_room_list, bedsetup_list


        Resbuff = Res_line
        Flbuff = Floor_list

        zimmer = db_session.query(Zimmer).filter(
                (Zimmer.sleeping)).first()
        while None != zimmer:

            if zimmer.etage < lowest_floor:
                lowest_floor = zimmer.etage

            elif zimmer.etage > uppest_floor:
                uppest_floor = zimmer.etage


            tot_room = tot_room + 1

            floor_list = query(floor_list_list, filters=(lambda floor_list :floor_list.floor_number == zimmer.etage), first=True)

            if not floor_list:
                floor_list = Floor_list()
                floor_list_list.append(floor_list)

                floor_list.floor_number = zimmer.etage

            if zimmer.zistatus == 4 or zimmer.zistatus == 5:
                floor_list.occupied_room = floor_list.occupied_room + 1


            else:

                resbuff = db_session.query(Resbuff).filter(
                            (Resbuff.zinr == zimmer.zinr) &  (Resbuff.abreise == ci_date) &  (Resbuff.resstatus <= 8)).first()

                if resbuff:
                    floor_list.occupied_room = floor_list.occupied_room + 1

            zimmer = db_session.query(Zimmer).filter(
                    (Zimmer.sleeping)).first()
        mid_floor = round((uppest_floor + lowest_floor) / 2, 0)

        for floor_list in query(floor_list_list, filters=(lambda floor_list :floor_list.occupied_room == 0)):

            if floor_list.floor_number == lowest_floor:

                flbuff = query(flbuff_list, filters=(lambda flbuff :flbuff.floor_number == floor_list.floor_number + 1), first=True)

                if flbuff and flbuff.occupied_room > 0:
                    floor_list.priority = 1

            if floor_list.floor_number == uppest_floor:

                flbuff = query(flbuff_list, filters=(lambda flbuff :flbuff.floor_number == floor_list.floor_number - 1), first=True)

                if flbuff and flbuff.occupied_room > 0:
                    floor_list.priority = 1
            else:

                flbuff = query(flbuff_list, filters=(lambda flbuff :flbuff.floor_number == floor_list.floor_number + 1), first=True)

                if flbuff and flbuff.occupied_room > 0:
                    floor_list.priority = 1

                if floor_list.priority == 0:

                    flbuff = query(flbuff_list, filters=(lambda flbuff :flbuff.floor_number == floor_list.floor_number - 1), first=True)

                    if flbuff and flbuff.occupied_room > 0:
                        floor_list.priority = 1

        for floor_list in query(floor_list_list, filters=(lambda floor_list :floor_list.occupied_room > 0)):
            lowest_occ_floor = floor_list.floor_number
            break

        for floor_list in query(floor_list_list, filters=(lambda floor_list :floor_list.occupied_room > 0)):
            uppest_occ_floor = floor_list.floor_number
            break

    def create_glist():

        nonlocal err_code, fdate, tdate, ci_date, tot_room, occ_room, occ_perc, occ1, occ2, uppest_floor, lowest_floor, mid_floor, uppest_occ_floor, lowest_occ_floor, min_day, cfloor, guest_zinr, curr_co_date, curr_zikatnr, csetup_array, curr_time, res_line, htparam, zimmer, bresline, paramtext, outorder, zinrstat
        nonlocal resline, tresline, tarrival, bavail, bresline, resbuff, flbuff, curr_rline


        nonlocal arrival_guest, ci_glist, floor_list, avail_room, bedsetup, resline, tresline, tarrival, bavail, bresline, resbuff, flbuff, curr_rline
        nonlocal arrival_guest_list, ci_glist_list, floor_list_list, avail_room_list, bedsetup_list

        loopi:int = 0
        messvalue:str = ""

        for arrival_guest in query(arrival_guest_list):
            ci_glist = Ci_glist()
            ci_glist_list.append(ci_glist)

            buffer_copy(arrival_guest, ci_glist)
            for loopi in range(1,num_entries(arrival_guest.preference, "$") - 1 + 1) :
                messvalue = entry(loopi - 1, arrival_guest.preference, "$")

                if messvalue == "HIGHER FLOOR":
                    ci_glist.pref_floor = 1


                elif messvalue == "LOWEST FLOOR":
                    ci_glist.pref_floor = 2


                elif messvalue == "ONE BIG BED":
                    ci_glist.pref_bedtype = 1


                elif messvalue == "TWO SINGLE":
                    ci_glist.pref_bedtype = 2


                elif messvalue == "NO SMOKING":
                    ci_glist.pref_smoke = 1


                elif messvalue == "NON SMOKING":
                    ci_glist.pref_smoke = 1


                elif messvalue == "NO SMOKING ROOM":
                    ci_glist.pref_smoke = 1


                elif messvalue == "NON SMOKING ROOM":
                    ci_glist.pref_smoke = 1


                elif messvalue == "SMOKING":
                    ci_glist.pref_smoke = 2


                elif messvalue == "SMOKING ROOM":
                    ci_glist.pref_smoke = 2

    def calc_occ():

        nonlocal err_code, fdate, tdate, ci_date, tot_room, occ_room, occ_perc, occ1, occ2, uppest_floor, lowest_floor, mid_floor, uppest_occ_floor, lowest_occ_floor, min_day, cfloor, guest_zinr, curr_co_date, curr_zikatnr, csetup_array, curr_time, res_line, htparam, zimmer, bresline, paramtext, outorder, zinrstat
        nonlocal resline, tresline, tarrival, bavail, bresline, resbuff, flbuff, curr_rline


        nonlocal arrival_guest, ci_glist, floor_list, avail_room, bedsetup, resline, tresline, tarrival, bavail, bresline, resbuff, flbuff, curr_rline
        nonlocal arrival_guest_list, ci_glist_list, floor_list_list, avail_room_list, bedsetup_list

        do_it:bool = False
        Bresline = Res_line

        if occ1 == None:

            for bresline in db_session.query(Bresline).filter(
                    (Bresline.active_flag <= 1) &  (Bresline.resstatus <= 6) &  (Bresline.resstatus != 3) &  (Bresline.resstatus != 4) &  (Bresline.resstatus != 12) &  (Bresline.resstatus != 11) &  (Bresline.resstatus != 13) &  (Bresline.ankunft <= ci_date) &  (Bresline.abreise > ci_date) &  (Bresline.l_zuordnung[2] == 0)).all():
                do_it = True

                if bresline.zinr != "":

                    zimmer = db_session.query(Zimmer).filter(
                            (Zimmer.zinr == bresline.zinr)).first()
                    do_it = zimmer.sleeping

                if do_it:
                    occ_room = occ_room + bresline.zimmeranz
            occ1 = occ_room / tot_room * 100

        for bresline in db_session.query(Bresline).filter(
                    (Bresline.active_flag <= 1) &  (Bresline.resstatus <= 6) &  (Bresline.resstatus != 3) &  (Bresline.resstatus != 4) &  (Bresline.resstatus != 12) &  (Bresline.resstatus != 11) &  (Bresline.resstatus != 13) &  (Bresline.ankunft <= curr_co_date) &  (Bresline.abreise > curr_co_date) &  (Bresline.l_zuordnung[2] == 0)).all():
            do_it = True

            if bresline.zinr != "":

                zimmer = db_session.query(Zimmer).filter(
                            (Zimmer.zinr == bresline.zinr)).first()
                do_it = zimmer.sleeping

            if do_it:
                occ_room = occ_room + bresline.zimmeranz
        occ2 = occ_room / tot_room * 100

        if occ1 > occ2:
            occ% = occ1
        else:
            occ% = occ2

    def bed_setup():

        nonlocal err_code, fdate, tdate, ci_date, tot_room, occ_room, occ_perc, occ1, occ2, uppest_floor, lowest_floor, mid_floor, uppest_occ_floor, lowest_occ_floor, min_day, cfloor, guest_zinr, curr_co_date, curr_zikatnr, csetup_array, curr_time, res_line, htparam, zimmer, bresline, paramtext, outorder, zinrstat
        nonlocal resline, tresline, tarrival, bavail, bresline, resbuff, flbuff, curr_rline


        nonlocal arrival_guest, ci_glist, floor_list, avail_room, bedsetup, resline, tresline, tarrival, bavail, bresline, resbuff, flbuff, curr_rline
        nonlocal arrival_guest_list, ci_glist_list, floor_list_list, avail_room_list, bedsetup_list

        for paramtext in db_session.query(Paramtext).filter(
                (Paramtext.txtnr >= 9201) &  (Paramtext.txtnr <= 9299)).all():

            if paramtext.notes != "":

                zimmer = db_session.query(Zimmer).filter(
                        (Zimmer.setup == (paramtext.txtnr - 9200))).first()

                if zimmer:
                    bedsetup = Bedsetup()
                    bedsetup_list.append(bedsetup)

                    bedsetup.i_setup = zimmer.setup

                    if re.match(".*twin.*",paramtext.ptexte):
                        bedsetup.room_flag = 2


                    else:
                        bedsetup.room_flag = 1

    def room_avail(recid_resline:int):

        nonlocal err_code, fdate, tdate, ci_date, tot_room, occ_room, occ_perc, occ1, occ2, uppest_floor, lowest_floor, mid_floor, uppest_occ_floor, lowest_occ_floor, min_day, cfloor, guest_zinr, curr_co_date, curr_zikatnr, csetup_array, curr_time, res_line, htparam, zimmer, bresline, paramtext, outorder, zinrstat
        nonlocal resline, tresline, tarrival, bavail, bresline, resbuff, flbuff, curr_rline


        nonlocal arrival_guest, ci_glist, floor_list, avail_room, bedsetup, resline, tresline, tarrival, bavail, bresline, resbuff, flbuff, curr_rline
        nonlocal arrival_guest_list, ci_glist_list, floor_list_list, avail_room_list, bedsetup_list

        ci_date:date = None
        co_date:date = None
        zikatnr:int = 0
        feature:str = ""
        loopi:int = 0
        do_it:bool = False
        frdate:date = None
        tdate:date = None
        Curr_rline = Res_line
        Resbuff = Res_line

        curr_rline = db_session.query(Curr_rline).filter(
                (Curr_rline._recid == recid_resline)).first()
        ci_date = curr_rline.ankunft
        co_date = curr_rline.abreise
        zikatnr = curr_rline.zikatnr

        zimmer = db_session.query(Zimmer).filter(
                (Zimmer.sleeping) &  (Zimmer.zikatnr == zikatnr) &  (Zimmer.zistatus == 0)).first()
        while None != zimmer:
            do_it = True

            outorder = db_session.query(Outorder).filter(
                    (Outorder.zinr == zimmer.zinr) &  (((Outorder.gespstart >= ci_date) &  (Outorder.gespende <= co_date)) |  ((Outorder.gespstart >= ci_date)))).first()

            if outorder:
                do_it = False

            if do_it:

                resbuff = db_session.query(Resbuff).filter(
                        (Resbuff.zinr == zimmer.zinr) &  (not Resbuff.abreise <= ci_date) &  (not Resbuff.ankunft >= co_date) &  (Resbuff.active_flag <= 1) &  (Resbuff._recid != recid_resline)).first()

                if resbuff:
                    do_it = False

            if do_it :
                avail_room = Avail_room()
                avail_room_list.append(avail_room)

                avail_room.zinr = zimmer.zinr
                avail_room.floor_number = zimmer.etage


                feature = fill_feature()
                for loopi in range(1,num_entries(feature, ";")  + 1) :

                    if entry(loopi - 1, feature, ";") == "NON SMOOKING" or entry(loopi - 1, feature, ";") == "NS" or entry(loopi - 1, feature, ";") == "NO SMOOKING":
                        avail_room.smoke_flag = 1

                    elif entry(loopi - 1, feature, ";") == "SMOOKING" or entry(loopi - 1, feature, ";") == "SM" or entry(loopi - 1, feature, ";") == "SMOOKING Room":
                        avail_room.smoke_flag = 2

                bedsetup = query(bedsetup_list, filters=(lambda bedsetup :bedsetup.i_setup == zimmer.setup), first=True)

                if bedsetup:
                    avail_room.bed_type = bedsetup.room_flag

                resbuff = db_session.query(Resbuff).filter(
                        (Resbuff.active_flag == 0) &  (Resbuff.zinr == zimmer.zinr) &  (Resbuff.abreise >= ci_date) &  (Resbuff._recid != recid_resline)).first()

                if resbuff:
                    avail_room.next_guest = True
                    avail_room.next_arrival = resbuff.ankunft

                resbuff = db_session.query(Resbuff).filter(
                        (Resbuff.resstatus == 8) &  (Resbuff.zinr == zimmer.zinr) &  (Resbuff.abreise == ci_date)).first()

                if resbuff:
                    avail_room.prev_guest = True

            zimmer = db_session.query(Zimmer).filter(
                    (Zimmer.sleeping) &  (Zimmer.zikatnr == zikatnr) &  (Zimmer.zistatus == 0)).first()

        if get_day(ci_date) == 1 and get_month(ci_date) == 1:
            frdate = date_mdy(get_month(ci_date) - 1, 1, get_year(ci_date) - 1)


        else:

            if get_day(ci_date) == 1:
                frdate = date_mdy(get_month(ci_date) - 1, 1, get_year(ci_date))


            else:
                frdate = date_mdy(get_month(ci_date) , 1, get_year(ci_date))


        tdate = ci_date - 1

        zinrstat = db_session.query(Zinrstat).filter(
                (Zinrstat.datum >= frdate) &  (Zinrstat.datum <= tdate)).first()
        while None != zinrstat:

            avail_room = query(avail_room_list, filters=(lambda avail_room :avail_room.zinr == zinrstat.zinr), first=True)

            if avail_room:
                avail_room.num_use = avail_room.num_use + 1

            zinrstat = db_session.query(Zinrstat).filter(
                    (Zinrstat.datum >= frdate) &  (Zinrstat.datum <= tdate)).first()

    def peak_occ():

        nonlocal err_code, fdate, tdate, ci_date, tot_room, occ_room, occ_perc, occ1, occ2, uppest_floor, lowest_floor, mid_floor, uppest_occ_floor, lowest_occ_floor, min_day, cfloor, guest_zinr, curr_co_date, curr_zikatnr, csetup_array, curr_time, res_line, htparam, zimmer, bresline, paramtext, outorder, zinrstat
        nonlocal resline, tresline, tarrival, bavail, bresline, resbuff, flbuff, curr_rline


        nonlocal arrival_guest, ci_glist, floor_list, avail_room, bedsetup, resline, tresline, tarrival, bavail, bresline, resbuff, flbuff, curr_rline
        nonlocal arrival_guest_list, ci_glist_list, floor_list_list, avail_room_list, bedsetup_list

        guest_zinr = ""
        do_it:bool = False

        def generate_inner_output():
            return guest_zinr

        if ci_glist.pref_bedtype != 0:

            if ci_glist.pref_floor == 1 and ci_glist.pref_smoke != 0:

                for avail_room in query(avail_room_list, filters=(lambda avail_room :avail_room.bed_type == ci_glist.pref_bedtype and avail_room.next_arrival == ci_glist.co)):
                    do_it = ci_glist.pref_smoke == avail_room.smoke_flag

                    if do_it:
                        guest_zinr = avail_room.zinr

                        return generate_inner_output()


            elif ci_glist.pref_floor != 1 and ci_glist.pref_smoke != 0:

                for avail_room in query(avail_room_list, filters=(lambda avail_room :avail_room.bed_type == ci_glist.pref_bedtype and avail_room.next_arrival == ci_glist.co)):
                    do_it = ci_glist.pref_smoke == avail_room.smoke_flag

                    if do_it:
                        guest_zinr = avail_room.zinr

                        return generate_inner_output()


            if ci_glist.pref_floor == 1:

                for avail_room in query(avail_room_list, filters=(lambda avail_room :avail_room.bed_type == ci_glist.pref_bedtype and avail_room.next_arrival == ci_glist.co)):
                    guest_zinr = avail_room.zinr

                    return generate_inner_output()


            elif ci_glist.pref_floor != 1:

                for avail_room in query(avail_room_list, filters=(lambda avail_room :avail_room.bed_type == ci_glist.pref_bedtype and avail_room.next_arrival == ci_glist.co)):
                    guest_zinr = avail_room.zinr

                    return generate_inner_output()


        if ci_glist.pref_floor == 1 and ci_glist.pref_smoke != 0:

            for avail_room in query(avail_room_list, filters=(lambda avail_room :avail_room.next_arrival == ci_glist.co)):
                do_it = ci_glist.pref_smoke == avail_room.smoke_flag

                if do_it:
                    guest_zinr = avail_room.zinr

                    return generate_inner_output()


        elif ci_glist.pref_floor != 1 and ci_glist.pref_smoke != 0:

            for avail_room in query(avail_room_list, filters=(lambda avail_room :avail_room.next_arrival == ci_glist.co)):
                do_it = ci_glist.pref_smoke == avail_room.smoke_flag

                if do_it:
                    guest_zinr = avail_room.zinr

                    return generate_inner_output()


        if ci_glist.pref_floor == 1:

            for avail_room in query(avail_room_list, filters=(lambda avail_room :avail_room.next_arrival == ci_glist.co)):
                guest_zinr = avail_room.zinr

                return generate_inner_output()


        elif ci_glist.pref_floor != 1:

            for avail_room in query(avail_room_list, filters=(lambda avail_room :avail_room.next_arrival == ci_glist.co)):
                guest_zinr = avail_room.zinr

                return generate_inner_output()


        if guest_zinr == "":
            guest_zinr = peak_occ1()


        return generate_inner_output()

    def peak_occ1():

        nonlocal err_code, fdate, tdate, ci_date, tot_room, occ_room, occ_perc, occ1, occ2, uppest_floor, lowest_floor, mid_floor, uppest_occ_floor, lowest_occ_floor, min_day, cfloor, guest_zinr, curr_co_date, curr_zikatnr, csetup_array, curr_time, res_line, htparam, zimmer, bresline, paramtext, outorder, zinrstat
        nonlocal resline, tresline, tarrival, bavail, bresline, resbuff, flbuff, curr_rline


        nonlocal arrival_guest, ci_glist, floor_list, avail_room, bedsetup, resline, tresline, tarrival, bavail, bresline, resbuff, flbuff, curr_rline
        nonlocal arrival_guest_list, ci_glist_list, floor_list_list, avail_room_list, bedsetup_list

        guest_zinr = ""
        do_it:bool = False

        def generate_inner_output():
            return guest_zinr

        for avail_room in query(avail_room_list, filters=(lambda avail_room :avail_room.next_guest)):
            guest_zinr = avail_room.zinr

            return generate_inner_output()

        if guest_zinr == "":
            guest_zinr = high_occ()


        return generate_inner_output()

    def high_occ():

        nonlocal err_code, fdate, tdate, ci_date, tot_room, occ_room, occ_perc, occ1, occ2, uppest_floor, lowest_floor, mid_floor, uppest_occ_floor, lowest_occ_floor, min_day, cfloor, guest_zinr, curr_co_date, curr_zikatnr, csetup_array, curr_time, res_line, htparam, zimmer, bresline, paramtext, outorder, zinrstat
        nonlocal resline, tresline, tarrival, bavail, bresline, resbuff, flbuff, curr_rline


        nonlocal arrival_guest, ci_glist, floor_list, avail_room, bedsetup, resline, tresline, tarrival, bavail, bresline, resbuff, flbuff, curr_rline
        nonlocal arrival_guest_list, ci_glist_list, floor_list_list, avail_room_list, bedsetup_list

        guest_zinr = ""
        do_it:bool = False

        def generate_inner_output():
            return guest_zinr

        if ci_glist.pref_bedtype != 0:

            if ci_glist.pref_floor == 1 and ci_glist.pref_smoke != 0:

                for avail_room in query(avail_room_list, filters=(lambda avail_room :avail_room.bed_type == ci_glist.pref_bedtype)):
                    do_it = ci_glist.pref_smoke == avail_room.smoke_flag

                    if do_it:
                        guest_zinr = avail_room.zinr

                        return generate_inner_output()


            elif ci_glist.pref_floor != 1 and ci_glist.pref_smoke != 0:

                for avail_room in query(avail_room_list, filters=(lambda avail_room :avail_room.bed_type == ci_glist.pref_bedtype)):
                    do_it = ci_glist.pref_smoke == avail_room.smoke_flag

                    if do_it:
                        guest_zinr = avail_room.zinr

                        return generate_inner_output()


            if ci_glist.pref_floor == 1:

                for avail_room in query(avail_room_list, filters=(lambda avail_room :avail_room.bed_type == ci_glist.pref_bedtype)):
                    guest_zinr = avail_room.zinr

                    return generate_inner_output()


            elif ci_glist.pref_floor != 1:

                for avail_room in query(avail_room_list, filters=(lambda avail_room :avail_room.bed_type == ci_glist.pref_bedtype)):
                    guest_zinr = avail_room.zinr

                    return generate_inner_output()


        if ci_glist.pref_floor == 1 and ci_glist.pref_smoke != 0:

            for avail_room in query(avail_room_list):
                do_it = ci_glist.pref_smoke == avail_room.smoke_flag

                if do_it:
                    guest_zinr = avail_room.zinr

                    return generate_inner_output()


        elif ci_glist.pref_floor != 1 and ci_glist.pref_smoke != 0:

            for avail_room in query(avail_room_list):
                do_it = ci_glist.pref_smoke == avail_room.smoke_flag

                if do_it:
                    guest_zinr = avail_room.zinr

                    return generate_inner_output()


        if ci_glist.pref_floor == 1:

            for avail_room in query(avail_room_list):
                guest_zinr = avail_room.zinr

                return generate_inner_output()


        elif ci_glist.pref_floor != 1:

            for avail_room in query(avail_room_list):
                guest_zinr = avail_room.zinr

                return generate_inner_output()

        return generate_inner_output()

    def low_occ():

        nonlocal err_code, fdate, tdate, ci_date, tot_room, occ_room, occ_perc, occ1, occ2, uppest_floor, lowest_floor, mid_floor, uppest_occ_floor, lowest_occ_floor, min_day, cfloor, guest_zinr, curr_co_date, curr_zikatnr, csetup_array, curr_time, res_line, htparam, zimmer, bresline, paramtext, outorder, zinrstat
        nonlocal resline, tresline, tarrival, bavail, bresline, resbuff, flbuff, curr_rline


        nonlocal arrival_guest, ci_glist, floor_list, avail_room, bedsetup, resline, tresline, tarrival, bavail, bresline, resbuff, flbuff, curr_rline
        nonlocal arrival_guest_list, ci_glist_list, floor_list_list, avail_room_list, bedsetup_list

        guest_zinr = ""
        do_it:bool = False

        def generate_inner_output():
            return guest_zinr

        if ci_glist.pref_bedtype != 0:

            if ci_glist.pref_floor == 1 and ci_glist.pref_smoke != 0:

                for avail_room in query(avail_room_list, filters=(lambda avail_room :avail_room.bed_type == ci_glist.pref_bedtype)):
                    floor_list = db_session.query(Floor_list).filter((Floor_list.floor_number == avail_room.floor_number) &  (Floor_list.occupied_room > 0)).first()
                    if not floor_list:
                        continue

                    do_it = ci_glist.pref_smoke == avail_room.smoke_flag

                    if do_it:
                        guest_zinr = avail_room.zinr

                        return generate_inner_output()


            elif ci_glist.pref_floor != 1 and ci_glist.pref_smoke != 0:

                for avail_room in query(avail_room_list, filters=(lambda avail_room :avail_room.bed_type == ci_glist.pref_bedtype)):
                    floor_list = db_session.query(Floor_list).filter((Floor_list.floor_number == avail_room.floor_number) &  (Floor_list.occupied_room > 0)).first()
                    if not floor_list:
                        continue

                    do_it = ci_glist.pref_smoke == avail_room.smoke_flag

                    if do_it:
                        guest_zinr = avail_room.zinr

                        return generate_inner_output()


            if ci_glist.pref_floor == 1:

                for avail_room in query(avail_room_list, filters=(lambda avail_room :avail_room.bed_type == ci_glist.pref_bedtype)):
                    floor_list = db_session.query(Floor_list).filter((Floor_list.floor_number == avail_room.floor_number) &  (Floor_list.occupied_room > 0)).first()
                    if not floor_list:
                        continue

                    guest_zinr = avail_room.zinr

                    return generate_inner_output()


            elif ci_glist.pref_floor != 1:

                for avail_room in query(avail_room_list, filters=(lambda avail_room :avail_room.bed_type == ci_glist.pref_bedtype)):
                    floor_list = db_session.query(Floor_list).filter((Floor_list.floor_number == avail_room.floor_number) &  (Floor_list.occupied_room > 0)).first()
                    if not floor_list:
                        continue

                    guest_zinr = avail_room.zinr

                    return generate_inner_output()


        if ci_glist.pref_floor == 1 and ci_glist.pref_smoke != 0:

            for avail_room in query(avail_room_list):
                floor_list = db_session.query(Floor_list).filter((Floor_list.floor_number == avail_room.floor_number) &  (Floor_list.occupied_room > 0)).first()
                if not floor_list:
                    continue

                do_it = ci_glist.pref_smoke == avail_room.smoke_flag

                if do_it:
                    guest_zinr = avail_room.zinr

                    return generate_inner_output()


        elif ci_glist.pref_floor != 1 and ci_glist.pref_smoke != 0:

            for avail_room in query(avail_room_list):
                floor_list = db_session.query(Floor_list).filter((Floor_list.floor_number == avail_room.floor_number) &  (Floor_list.occupied_room > 0)).first()
                if not floor_list:
                    continue

                do_it = ci_glist.pref_smoke == avail_room.smoke_flag

                if do_it:
                    guest_zinr = avail_room.zinr

                    return generate_inner_output()


        if ci_glist.pref_floor == 1:

            for avail_room in query(avail_room_list):
                floor_list = db_session.query(Floor_list).filter((Floor_list.floor_number == avail_room.floor_number) &  (Floor_list.occupied_room > 0)).first()
                if not floor_list:
                    continue

                guest_zinr = avail_room.zinr

                return generate_inner_output()


        elif ci_glist.pref_floor != 1:

            for avail_room in query(avail_room_list):
                floor_list = db_session.query(Floor_list).filter((Floor_list.floor_number == avail_room.floor_number) &  (Floor_list.occupied_room > 0)).first()
                if not floor_list:
                    continue

                guest_zinr = avail_room.zinr

                return generate_inner_output()


        if guest_zinr == "":
            guest_zinr = low_occ1()


        return generate_inner_output()

    def low_occ1():

        nonlocal err_code, fdate, tdate, ci_date, tot_room, occ_room, occ_perc, occ1, occ2, uppest_floor, lowest_floor, mid_floor, uppest_occ_floor, lowest_occ_floor, min_day, cfloor, guest_zinr, curr_co_date, curr_zikatnr, csetup_array, curr_time, res_line, htparam, zimmer, bresline, paramtext, outorder, zinrstat
        nonlocal resline, tresline, tarrival, bavail, bresline, resbuff, flbuff, curr_rline


        nonlocal arrival_guest, ci_glist, floor_list, avail_room, bedsetup, resline, tresline, tarrival, bavail, bresline, resbuff, flbuff, curr_rline
        nonlocal arrival_guest_list, ci_glist_list, floor_list_list, avail_room_list, bedsetup_list

        guest_zinr = ""
        do_it:bool = False

        def generate_inner_output():
            return guest_zinr

        if ci_glist.pref_bedtype != 0:

            if ci_glist.pref_floor == 1 and ci_glist.pref_smoke != 0:

                for avail_room in query(avail_room_list, filters=(lambda avail_room :avail_room.bed_type == ci_glist.pref_bedtype)):
                    floor_list = db_session.query(Floor_list).filter((Floor_list.floor_number == avail_room.floor_number) &  (Floor_list.occupied_room == 0) &  (Floor_list.floor_number > lowest_occ_floor) &  (Floor_list.floor_number < uppest_occ_floor)).first()
                    if not floor_list:
                        continue

                    do_it = ci_glist.pref_smoke == avail_room.smoke_flag

                    if do_it:
                        guest_zinr = avail_room.zinr

                        return generate_inner_output()


            elif ci_glist.pref_floor != 1 and ci_glist.pref_smoke != 0:

                for avail_room in query(avail_room_list, filters=(lambda avail_room :avail_room.bed_type == ci_glist.pref_bedtype)):
                    floor_list = db_session.query(Floor_list).filter((Floor_list.floor_number == avail_room.floor_number) &  (Floor_list.occupied_room == 0) &  (Floor_list.floor_number > lowest_occ_floor) &  (Floor_list.floor_number < uppest_occ_floor)).first()
                    if not floor_list:
                        continue

                    do_it = ci_glist.pref_smoke == avail_room.smoke_flag

                    if do_it:
                        guest_zinr = avail_room.zinr

                        return generate_inner_output()


            if ci_glist.pref_floor == 1:

                for avail_room in query(avail_room_list, filters=(lambda avail_room :avail_room.bed_type == ci_glist.pref_bedtype)):
                    floor_list = db_session.query(Floor_list).filter((Floor_list.floor_number == avail_room.floor_number) &  (Floor_list.occupied_room == 0) &  (Floor_list.floor_number > lowest_occ_floor) &  (Floor_list.floor_number < uppest_occ_floor)).first()
                    if not floor_list:
                        continue

                    guest_zinr = avail_room.zinr

                    return generate_inner_output()


            elif ci_glist.pref_floor != 1:

                for avail_room in query(avail_room_list, filters=(lambda avail_room :avail_room.bed_type == ci_glist.pref_bedtype)):
                    floor_list = db_session.query(Floor_list).filter((Floor_list.floor_number == avail_room.floor_number) &  (Floor_list.occupied_room == 0) &  (Floor_list.floor_number > lowest_occ_floor) &  (Floor_list.floor_number < uppest_occ_floor)).first()
                    if not floor_list:
                        continue

                    guest_zinr = avail_room.zinr

                    return generate_inner_output()


        if ci_glist.pref_floor == 1 and ci_glist.pref_smoke != 0:

            for avail_room in query(avail_room_list):
                floor_list = db_session.query(Floor_list).filter((Floor_list.floor_number == avail_room.floor_number) &  (Floor_list.occupied_room == 0) &  (Floor_list.floor_number > lowest_occ_floor) &  (Floor_list.floor_number < uppest_occ_floor)).first()
                if not floor_list:
                    continue

                do_it = ci_glist.pref_smoke == avail_room.smoke_flag

                if do_it:
                    guest_zinr = avail_room.zinr

                    return generate_inner_output()


        elif ci_glist.pref_floor != 1 and ci_glist.pref_smoke != 0:

            for avail_room in query(avail_room_list):
                floor_list = db_session.query(Floor_list).filter((Floor_list.floor_number == avail_room.floor_number) &  (Floor_list.occupied_room == 0) &  (Floor_list.floor_number > lowest_occ_floor) &  (Floor_list.floor_number < uppest_occ_floor)).first()
                if not floor_list:
                    continue

                do_it = ci_glist.pref_smoke == avail_room.smoke_flag

                if do_it:
                    guest_zinr = avail_room.zinr

                    return generate_inner_output()


        if ci_glist.pref_floor == 1:

            for avail_room in query(avail_room_list):
                floor_list = db_session.query(Floor_list).filter((Floor_list.floor_number == avail_room.floor_number) &  (Floor_list.occupied_room == 0) &  (Floor_list.floor_number > lowest_occ_floor) &  (Floor_list.floor_number < uppest_occ_floor)).first()
                if not floor_list:
                    continue

                guest_zinr = avail_room.zinr

                return generate_inner_output()


        elif ci_glist.pref_floor != 1:

            for avail_room in query(avail_room_list):
                floor_list = db_session.query(Floor_list).filter((Floor_list.floor_number == avail_room.floor_number) &  (Floor_list.occupied_room == 0) &  (Floor_list.floor_number > lowest_occ_floor) &  (Floor_list.floor_number < uppest_occ_floor)).first()
                if not floor_list:
                    continue

                guest_zinr = avail_room.zinr

                return generate_inner_output()


        if guest_zinr == "":
            guest_zinr = low_occ2()


        return generate_inner_output()

    def low_occ2():

        nonlocal err_code, fdate, tdate, ci_date, tot_room, occ_room, occ_perc, occ1, occ2, uppest_floor, lowest_floor, mid_floor, uppest_occ_floor, lowest_occ_floor, min_day, cfloor, guest_zinr, curr_co_date, curr_zikatnr, csetup_array, curr_time, res_line, htparam, zimmer, bresline, paramtext, outorder, zinrstat
        nonlocal resline, tresline, tarrival, bavail, bresline, resbuff, flbuff, curr_rline


        nonlocal arrival_guest, ci_glist, floor_list, avail_room, bedsetup, resline, tresline, tarrival, bavail, bresline, resbuff, flbuff, curr_rline
        nonlocal arrival_guest_list, ci_glist_list, floor_list_list, avail_room_list, bedsetup_list

        guest_zinr = ""
        do_it:bool = False

        def generate_inner_output():
            return guest_zinr

        if ci_glist.pref_bedtype != 0:

            if ci_glist.pref_floor == 1 and ci_glist.pref_smoke != 0:

                for avail_room in query(avail_room_list, filters=(lambda avail_room :avail_room.bed_type == ci_glist.pref_bedtype)):
                    floor_list = db_session.query(Floor_list).filter((Floor_list.floor_number == avail_room.floor_number) &  (Floor_list.occupied_room == 0) &  (Floor_list.floor_number > uppest_occ_floor)).first()
                    if not floor_list:
                        continue

                    do_it = ci_glist.pref_smoke == avail_room.smoke_flag

                    if do_it:
                        guest_zinr = avail_room.zinr

                        return generate_inner_output()


            elif ci_glist.pref_floor != 1 and ci_glist.pref_smoke != 0:

                for avail_room in query(avail_room_list, filters=(lambda avail_room :avail_room.bed_type == ci_glist.pref_bedtype)):
                    floor_list = db_session.query(Floor_list).filter((Floor_list.floor_number == avail_room.floor_number) &  (Floor_list.occupied_room == 0) &  (Floor_list.floor_number < lowest_occ_floor)).first()
                    if not floor_list:
                        continue

                    do_it = ci_glist.pref_smoke == avail_room.smoke_flag

                    if do_it:
                        guest_zinr = avail_room.zinr

                        return generate_inner_output()


            if ci_glist.pref_floor == 1:

                for avail_room in query(avail_room_list, filters=(lambda avail_room :avail_room.bed_type == ci_glist.pref_bedtype)):
                    floor_list = db_session.query(Floor_list).filter((Floor_list.floor_number == avail_room.floor_number) &  (Floor_list.occupied_room == 0) &  (Floor_list.floor_number > uppest_occ_floor)).first()
                    if not floor_list:
                        continue

                    guest_zinr = avail_room.zinr

                    return generate_inner_output()


            elif ci_glist.pref_floor != 1:

                for avail_room in query(avail_room_list, filters=(lambda avail_room :avail_room.bed_type == ci_glist.pref_bedtype)):
                    floor_list = db_session.query(Floor_list).filter((Floor_list.floor_number == avail_room.floor_number) &  (Floor_list.occupied_room == 0) &  (Floor_list.floor_number < lowest_occ_floor)).first()
                    if not floor_list:
                        continue

                    guest_zinr = avail_room.zinr

                    return generate_inner_output()


        if ci_glist.pref_floor == 1 and ci_glist.pref_smoke != 0:

            for avail_room in query(avail_room_list):
                floor_list = db_session.query(Floor_list).filter((Floor_list.floor_number == avail_room.floor_number) &  (Floor_list.occupied_room == 0) &  (Floor_list.floor_number > lowest_occ_floor)).first()
                if not floor_list:
                    continue

                do_it = ci_glist.pref_smoke == avail_room.smoke_flag

                if do_it:
                    guest_zinr = avail_room.zinr

                    return generate_inner_output()


        elif ci_glist.pref_floor != 1 and ci_glist.pref_smoke != 0:

            for avail_room in query(avail_room_list):
                floor_list = db_session.query(Floor_list).filter((Floor_list.floor_number == avail_room.floor_number) &  (Floor_list.occupied_room == 0) &  (Floor_list.floor_number < lowest_occ_floor)).first()
                if not floor_list:
                    continue

                do_it = ci_glist.pref_smoke == avail_room.smoke_flag

                if do_it:
                    guest_zinr = avail_room.zinr

                    return generate_inner_output()


        if ci_glist.pref_floor == 1:

            for avail_room in query(avail_room_list):
                floor_list = db_session.query(Floor_list).filter((Floor_list.floor_number == avail_room.floor_number) &  (Floor_list.occupied_room == 0) &  (Floor_list.floor_number > uppest_occ_floor)).first()
                if not floor_list:
                    continue

                guest_zinr = avail_room.zinr

                return generate_inner_output()


        elif ci_glist.pref_floor != 1:

            for avail_room in query(avail_room_list):
                floor_list = db_session.query(Floor_list).filter((Floor_list.floor_number == avail_room.floor_number) &  (Floor_list.occupied_room == 0) &  (Floor_list.floor_number < lowest_occ_floor)).first()
                if not floor_list:
                    continue

                guest_zinr = avail_room.zinr

                return generate_inner_output()


        if guest_zinr == "":
            guest_zinr = low_occ3()


        return generate_inner_output()

    def low_occ3():

        nonlocal err_code, fdate, tdate, ci_date, tot_room, occ_room, occ_perc, occ1, occ2, uppest_floor, lowest_floor, mid_floor, uppest_occ_floor, lowest_occ_floor, min_day, cfloor, guest_zinr, curr_co_date, curr_zikatnr, csetup_array, curr_time, res_line, htparam, zimmer, bresline, paramtext, outorder, zinrstat
        nonlocal resline, tresline, tarrival, bavail, bresline, resbuff, flbuff, curr_rline


        nonlocal arrival_guest, ci_glist, floor_list, avail_room, bedsetup, resline, tresline, tarrival, bavail, bresline, resbuff, flbuff, curr_rline
        nonlocal arrival_guest_list, ci_glist_list, floor_list_list, avail_room_list, bedsetup_list

        guest_zinr = ""
        do_it:bool = False

        def generate_inner_output():
            return guest_zinr

        if ci_glist.pref_bedtype != 0:

            if ci_glist.pref_floor == 1 and ci_glist.pref_smoke != 0:

                for avail_room in query(avail_room_list, filters=(lambda avail_room :avail_room.bed_type == ci_glist.pref_bedtype)):
                    floor_list = db_session.query(Floor_list).filter((Floor_list.floor_number == avail_room.floor_number) &  (Floor_list.occupied_room == 0) &  (Floor_list.floor_number < lowest_occ_floor)).first()
                    if not floor_list:
                        continue

                    do_it = ci_glist.pref_smoke == avail_room.smoke_flag

                    if do_it:
                        guest_zinr = avail_room.zinr

                        return generate_inner_output()


            elif ci_glist.pref_floor != 1 and ci_glist.pref_smoke != 0:

                for avail_room in query(avail_room_list, filters=(lambda avail_room :avail_room.bed_type == ci_glist.pref_bedtype)):
                    floor_list = db_session.query(Floor_list).filter((Floor_list.floor_number == avail_room.floor_number) &  (Floor_list.occupied_room == 0) &  (Floor_list.floor_number > uppest_occ_floor)).first()
                    if not floor_list:
                        continue

                    do_it = ci_glist.pref_smoke == avail_room.smoke_flag

                    if do_it:
                        guest_zinr = avail_room.zinr

                        return generate_inner_output()


            if ci_glist.pref_floor == 1:

                for avail_room in query(avail_room_list, filters=(lambda avail_room :avail_room.bed_type == ci_glist.pref_bedtype)):
                    floor_list = db_session.query(Floor_list).filter((Floor_list.floor_number == avail_room.floor_number) &  (Floor_list.occupied_room == 0) &  (Floor_list.floor_number < lowest_occ_floor)).first()
                    if not floor_list:
                        continue

                    guest_zinr = avail_room.zinr

                    return generate_inner_output()


            elif ci_glist.pref_floor != 1:

                for avail_room in query(avail_room_list, filters=(lambda avail_room :avail_room.bed_type == ci_glist.pref_bedtype)):
                    floor_list = db_session.query(Floor_list).filter((Floor_list.floor_number == avail_room.floor_number) &  (Floor_list.occupied_room == 0) &  (Floor_list.floor_number > uppest_occ_floor)).first()
                    if not floor_list:
                        continue

                    guest_zinr = avail_room.zinr

                    return generate_inner_output()


        if ci_glist.pref_floor == 1 and ci_glist.pref_smoke != 0:

            for avail_room in query(avail_room_list):
                floor_list = db_session.query(Floor_list).filter((Floor_list.floor_number == avail_room.floor_number) &  (Floor_list.occupied_room == 0) &  (Floor_list.floor_number < lowest_occ_floor)).first()
                if not floor_list:
                    continue

                do_it = ci_glist.pref_smoke == avail_room.smoke_flag

                if do_it:
                    guest_zinr = avail_room.zinr

                    return generate_inner_output()


        elif ci_glist.pref_floor != 1 and ci_glist.pref_smoke != 0:

            for avail_room in query(avail_room_list):
                floor_list = db_session.query(Floor_list).filter((Floor_list.floor_number == avail_room.floor_number) &  (Floor_list.occupied_room == 0) &  (Floor_list.floor_number > uppest_occ_floor)).first()
                if not floor_list:
                    continue

                do_it = ci_glist.pref_smoke == avail_room.smoke_flag

                if do_it:
                    guest_zinr = avail_room.zinr

                    return generate_inner_output()


        if ci_glist.pref_floor == 1:

            for avail_room in query(avail_room_list):
                floor_list = db_session.query(Floor_list).filter((Floor_list.floor_number == avail_room.floor_number) &  (Floor_list.occupied_room == 0) &  (Floor_list.floor_number < lowest_occ_floor)).first()
                if not floor_list:
                    continue

                guest_zinr = avail_room.zinr

                return generate_inner_output()


        elif ci_glist.pref_floor != 1:

            for avail_room in query(avail_room_list):
                floor_list = db_session.query(Floor_list).filter((Floor_list.floor_number == avail_room.floor_number) &  (Floor_list.occupied_room == 0) &  (Floor_list.floor_number > uppest_occ_floor)).first()
                if not floor_list:
                    continue

                guest_zinr = avail_room.zinr

                return generate_inner_output()

        return generate_inner_output()

    def fill_feature():

        nonlocal err_code, fdate, tdate, ci_date, tot_room, occ_room, occ_perc, occ1, occ2, uppest_floor, lowest_floor, mid_floor, uppest_occ_floor, lowest_occ_floor, min_day, cfloor, guest_zinr, curr_co_date, curr_zikatnr, csetup_array, curr_time, res_line, htparam, zimmer, bresline, paramtext, outorder, zinrstat
        nonlocal resline, tresline, tarrival, bavail, bresline, resbuff, flbuff, curr_rline


        nonlocal arrival_guest, ci_glist, floor_list, avail_room, bedsetup, resline, tresline, tarrival, bavail, bresline, resbuff, flbuff, curr_rline
        nonlocal arrival_guest_list, ci_glist_list, floor_list_list, avail_room_list, bedsetup_list

        feature = ""
        i:int = 0
        j:int = 0
        k:int = 0
        n:int = 0
        ch:str = ""

        def generate_inner_output():
            return feature
        n = 0
        j = 1
        for i in range(1,len(zimmer.himmelsr)  + 1) :

            if substring(zimmer.himmelsr, i - 1, 1) == ";" or substring(zimmer.himmelsr, i - 1, 1) == ",":
                ch = ""
                for k in range(j,(j + n - 1)  + 1) :

                    if substring(zimmer.himmelsr, k - 1, 1) != chr (10):
                        ch = ch + substring(zimmer.himmelsr, k - 1, 1)

                if feature == "":
                    feature = trim(ch)
                else:
                    feature = feature + ";" + trim(ch)
                j = i + 1
                n = 0
            else:
                n = n + 1

        if n != 0:
            ch = ""
            for k in range(j,(j + n - 1)  + 1) :

                if substring(zimmer.himmelsr, k - 1, 1) != chr (10):
                    ch = ch + substring(zimmer.himmelsr, k - 1, 1)

            if feature == "":
                feature = trim(ch)
            else:
                feature = feature + ";" + trim(ch)


        return generate_inner_output()


    curr_time = get_current_time_in_seconds()

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 87)).first()
    ci_date = htparam.fdate


    create_glist()
    calc_room()
    bed_setup()

    for ci_glist in query(ci_glist_list, filters=(lambda ci_glist :ci_glist.room_sharer == False)):

        res_line = db_session.query(Res_line).filter(
                (Res_line.resnr == ci_glist.resnr) &  (Res_line.reslinnr == ci_glist.reslinnr)).first()

        if curr_co_date != ci_glist.co or curr_zikatnr != ci_glist.zikatnr:

            if curr_co_date != ci_glist.co:
                calc_occ()
            curr_co_date = ci_glist.co
            curr_zikatnr = ci_glist.zikatnr


            avail_room._list.clear()
            room_avail(res_line._recid)

        if ci_glist.new_zinr  and res_line.zinr != "":

            res_line = db_session.query(Res_line).first()
            res_line.zinr = ""
            ci_glist.zinr = ""

            res_line = db_session.query(Res_line).first()

        if not ci_glist.l_selected and occ% >= 80 and res_line.zinr == "":
            break

        if res_line.zinr != "":

            resline = db_session.query(Resline).filter(
                    (Resline.zinr == res_line.zinr) &  (not Resline.abreise <= res_line.ankunft) &  (not Resline.ankunft >= res_line.abreise) &  (Resline.active_flag <= 1) &  (Resline._recid != res_line._recid)).first()

            if resline:

                arrival_guest = query(arrival_guest_list, filters=(lambda arrival_guest :arrival_guest.resnr == ci_glist.resnr and arrival_guest.reslinnr == ci_glist.reslinnr), first=True)

                if arrival_guest:
                    arrival_guest.room_stat = 1

            zimmer = db_session.query(Zimmer).filter(
                    (Zimmer.zinr == res_line.zinr)).first()

            if zimmer.zistatus != 0:

                arrival_guest = query(arrival_guest_list, filters=(lambda arrival_guest :arrival_guest.resnr == ci_glist.resnr and arrival_guest.reslinnr == ci_glist.reslinnr), first=True)

                if arrival_guest:
                    arrival_guest.room_stat = 2
        else:
            REPEAT:

        if occ% >= 80:
            guest_zinr = peak_occ()

        elif occ% >= 60 and occ% < 80:
            guest_zinr = high_occ()
        else:
            guest_zinr = low_occ()

        if guest_zinr == "":

            arrival_guest = query(arrival_guest_list, filters=(lambda arrival_guest :arrival_guest.resnr == ci_glist.resnr and arrival_guest.reslinnr == ci_glist.reslinnr), first=True)

            if arrival_guest:
                arrival_guest.room_stat = 3
            break

        bavail = query(bavail_list, filters=(lambda bavail :bavail.zinr.lower()  == (guest_zinr).lower()), first=True)
        bavail_list.remove(bavail)


        resline = db_session.query(Resline).filter(
                (func.lower(Resline.zinr) == (guest_zinr).lower()) &  (not Resline.abreise <= res_line.ankunft) &  (not Resline.ankunft >= res_line.abreise) &  (Resline.active_flag <= 1) &  (Resline._recid != res_line._recid)).first()

        if not resline:
            ci_glist.zinr = guest_zinr

            res_line = db_session.query(Res_line).first()
            res_line.zinr = guest_zinr

            res_line = db_session.query(Res_line).first()

            arrival_guest = query(arrival_guest_list, filters=(lambda arrival_guest :arrival_guest.resnr == ci_glist.resnr and arrival_guest.reslinnr == ci_glist.reslinnr), first=True)

            if arrival_guest:
                arrival_guest.zinr = guest_zinr

            bresline = db_session.query(Bresline).filter(
                    (Bresline.resnr == res_line.resnr) &  (Bresline.resstatus == 11) &  (Bresline.kontakt_nr == res_line.kontakt_nr)).first()

            if bresline:

                bresline = db_session.query(Bresline).first()
                bresline.zinr = guest_zinr

                bresline = db_session.query(Bresline).first()


            break

    return generate_output()