#using conversion tools version: 1.0.0.117
#------------------------------------------
# Rd, 16/9/2025
# zimkateg.verfuegbarkeit -> blm ada di for loop

#------------------------------------------


from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from functions.read_queasybl import read_queasybl
from models import Queasy, Htparam, Zimmer, Res_line, Zimkateg, Guest, Reservation, Segment, Outorder

def hk_count_1_webbl(pvilanguage:int):

    prepare_cache ([Queasy, Htparam, Zimmer, Res_line, Zimkateg, Guest, Reservation, Segment, Outorder])

    departed1 = 0
    departed2 = 0
    departing1 = 0
    departing2 = 0
    tot_depart1 = 0
    tot_depart2 = 0
    arrived1 = 0
    arrived2 = 0
    arriving1 = 0
    arriving2 = 0
    tot_arrive1 = 0
    tot_arrive2 = 0
    vclean = 0
    vuncheck = 0
    oclean = 0
    tot_clean = 0
    odirty = 0
    vdirty = 0
    atoday = 0
    tot_dirty = 0
    oroom1 = 0
    oroom2 = 0
    omroom1 = 0
    omroom2 = 0
    oooroom1 = 0
    oooroom2 = 0
    comproom1 = 0
    comproom2 = 0
    houseroom1 = 0
    houseroom2 = 0
    iroom1 = 0
    iroom2 = 0
    eocc1 = 0
    eocc2 = 0
    proz1 = to_decimal("0.0")
    proz2 = to_decimal("0.0")
    proz3 = to_decimal("0.0")
    proz4 = to_decimal("0.0")
    proz5 = to_decimal("0.0")
    queue_room_list_data = []
    depart_today_data = []
    departed_data = []
    arrival_today_data = []
    arrived_data = []
    vacant_clean_checked_data = []
    vacant_clean_unchecked_data = []
    occ_clean_data = []
    occ_dirty_data = []
    vacant_dirty_data = []
    ex_depart_data = []
    off_market_data = []
    ooo_room_data = []
    paying_room_data = []
    lvcarea:string = ""
    ci_date:date = None
    loop_i:int = 0
    str:string = ""
    str1:string = ""
    loop_j:int = 0
    loopj:int = 0
    resbemerk:string = ""
    queasy = htparam = zimmer = res_line = zimkateg = guest = reservation = segment = outorder = None

    depart_today = departed = arrival_today = arrived = vacant_clean_checked = vacant_clean_unchecked = occ_clean = occ_dirty = vacant_dirty = ex_depart = off_market = ooo_room = paying_room = queue_room_list = None

    depart_today_data, Depart_today = create_model("Depart_today", {"room":string, "rmtype":string, "gname":string})
    departed_data, Departed = create_model("Departed", {"room":string, "rmtype":string, "gname":string})
    arrival_today_data, Arrival_today = create_model("Arrival_today", {"room":string, "rmtype":string, "gname":string})
    arrived_data, Arrived = create_model("Arrived", {"room":string, "rmtype":string, "gname":string, "arrtime":string, "rsv_remark":string, "guest_pref":string, "room_status":string, "pci":bool})
    vacant_clean_checked_data, Vacant_clean_checked = create_model("Vacant_clean_checked", {"room":string, "rmtype":string, "gname":string})
    vacant_clean_unchecked_data, Vacant_clean_unchecked = create_model("Vacant_clean_unchecked", {"room":string, "rmtype":string, "gname":string})
    occ_clean_data, Occ_clean = create_model("Occ_clean", {"room":string, "rmtype":string, "gname":string})
    occ_dirty_data, Occ_dirty = create_model("Occ_dirty", {"room":string, "rmtype":string, "gname":string})
    vacant_dirty_data, Vacant_dirty = create_model("Vacant_dirty", {"room":string, "rmtype":string, "gname":string})
    ex_depart_data, Ex_depart = create_model("Ex_depart", {"room":string, "rmtype":string, "gname":string})
    off_market_data, Off_market = create_model("Off_market", {"room":string, "rmtype":string, "gname":string})
    ooo_room_data, Ooo_room = create_model("Ooo_room", {"room":string, "rmtype":string, "gname":string})
    paying_room_data, Paying_room = create_model("Paying_room", {"room":int, "pax":int, "percentage":Decimal})
    queue_room_list_data, Queue_room_list = create_model_like(Queasy)

    db_session = local_storage.db_session

    def generate_output():
        nonlocal departed1, departed2, departing1, departing2, tot_depart1, tot_depart2, arrived1, arrived2, arriving1, arriving2, tot_arrive1, tot_arrive2, vclean, vuncheck, oclean, tot_clean, odirty, vdirty, atoday, tot_dirty, oroom1, oroom2, omroom1, omroom2, oooroom1, oooroom2, comproom1, comproom2, houseroom1, houseroom2, iroom1, iroom2, eocc1, eocc2, proz1, proz2, proz3, proz4, proz5, queue_room_list_data, depart_today_data, departed_data, arrival_today_data, arrived_data, vacant_clean_checked_data, vacant_clean_unchecked_data, occ_clean_data, occ_dirty_data, vacant_dirty_data, ex_depart_data, off_market_data, ooo_room_data, paying_room_data, lvcarea, ci_date, loop_i, str, str1, loop_j, loopj, resbemerk, queasy, htparam, zimmer, res_line, zimkateg, guest, reservation, segment, outorder
        nonlocal pvilanguage


        nonlocal depart_today, departed, arrival_today, arrived, vacant_clean_checked, vacant_clean_unchecked, occ_clean, occ_dirty, vacant_dirty, ex_depart, off_market, ooo_room, paying_room, queue_room_list
        nonlocal depart_today_data, departed_data, arrival_today_data, arrived_data, vacant_clean_checked_data, vacant_clean_unchecked_data, occ_clean_data, occ_dirty_data, vacant_dirty_data, ex_depart_data, off_market_data, ooo_room_data, paying_room_data, queue_room_list_data

        return {"departed1": departed1, "departed2": departed2, "departing1": departing1, "departing2": departing2, "tot_depart1": tot_depart1, "tot_depart2": tot_depart2, "arrived1": arrived1, "arrived2": arrived2, "arriving1": arriving1, "arriving2": arriving2, "tot_arrive1": tot_arrive1, "tot_arrive2": tot_arrive2, "vclean": vclean, "vuncheck": vuncheck, "oclean": oclean, "tot_clean": tot_clean, "odirty": odirty, "vdirty": vdirty, "atoday": atoday, "tot_dirty": tot_dirty, "oroom1": oroom1, "oroom2": oroom2, "omroom1": omroom1, "omroom2": omroom2, "oooroom1": oooroom1, "oooroom2": oooroom2, "comproom1": comproom1, "comproom2": comproom2, "houseroom1": houseroom1, "houseroom2": houseroom2, "iroom1": iroom1, "iroom2": iroom2, "eocc1": eocc1, "eocc2": eocc2, "proz1": proz1, "proz2": proz2, "proz3": proz3, "proz4": proz4, "proz5": proz5, "queue-room-list": queue_room_list_data, "depart-today": depart_today_data, "departed": departed_data, "arrival-today": arrival_today_data, "arrived": arrived_data, "vacant-clean-checked": vacant_clean_checked_data, "vacant-clean-unchecked": vacant_clean_unchecked_data, "occ-clean": occ_clean_data, "occ-dirty": occ_dirty_data, "vacant-dirty": vacant_dirty_data, "ex-depart": ex_depart_data, "off-market": off_market_data, "ooo-room": ooo_room_data, "paying-room": paying_room_data}

    def init_var():

        nonlocal departed1, departed2, departing1, departing2, tot_depart1, tot_depart2, arrived1, arrived2, arriving1, arriving2, tot_arrive1, tot_arrive2, vclean, vuncheck, oclean, tot_clean, odirty, vdirty, atoday, tot_dirty, oroom1, oroom2, omroom1, omroom2, oooroom1, oooroom2, comproom1, comproom2, houseroom1, houseroom2, iroom1, iroom2, eocc1, eocc2, proz1, proz2, proz3, proz4, proz5, queue_room_list_data, depart_today_data, departed_data, arrival_today_data, arrived_data, vacant_clean_checked_data, vacant_clean_unchecked_data, occ_clean_data, occ_dirty_data, vacant_dirty_data, ex_depart_data, off_market_data, ooo_room_data, paying_room_data, lvcarea, ci_date, loop_i, str, str1, loop_j, loopj, resbemerk, queasy, htparam, zimmer, res_line, zimkateg, guest, reservation, segment, outorder
        nonlocal pvilanguage


        nonlocal depart_today, departed, arrival_today, arrived, vacant_clean_checked, vacant_clean_unchecked, occ_clean, occ_dirty, vacant_dirty, ex_depart, off_market, ooo_room, paying_room, queue_room_list
        nonlocal depart_today_data, departed_data, arrival_today_data, arrived_data, vacant_clean_checked_data, vacant_clean_unchecked_data, occ_clean_data, occ_dirty_data, vacant_dirty_data, ex_depart_data, off_market_data, ooo_room_data, paying_room_data, queue_room_list_data

        tot_zimmer:int = 0
        rm_active:bool = False
        actflag1:int = 0
        actflag2:int = 0
        tot_payrm:int = 0
        tot_pax:int = 0
        tot_avail:int = 0
        departed1 = 0
        departed2 = 0
        departing1 = 0
        departing2 = 0
        arrived1 = 0
        arrived2 = 0
        arriving1 = 0
        arriving2 = 0
        vclean = 0
        vuncheck = 0
        oclean = 0
        vdirty = 0
        odirty = 0
        atoday = 0
        omroom1 = 0
        oroom1 = 0
        oroom2 = 0
        oooroom1 = 0
        oooroom2 = 0
        iroom1 = 0
        iroom2 = 0
        eocc1 = 0
        eocc2 = 0
        houseroom1 = 0
        houseroom2 = 0
        comproom1 = 0
        comproom2 = 0
        tot_zimmer = 0
        tot_payrm = 0
        tot_avail = 0


        res_line_obj_list = {}
        res_line = Res_line()
        zimmer = Zimmer()
        for res_line.gastnrmember, res_line.zinr, res_line.erwachs, res_line.gratis, res_line.kind1, res_line.kind2, res_line.l_zuordnung, res_line.abreise, res_line.zipreis, res_line.resstatus, res_line.bemerk, res_line.ankzeit, res_line.zikatnr, res_line.zimmeranz, res_line.zimmer_wunsch, res_line.gastnr, res_line.ankunft, res_line._recid, zimmer.zikatnr, zimmer.zinr, zimmer.zistatus, zimmer.sleeping, zimmer._recid in db_session.query(Res_line.gastnrmember, Res_line.zinr, Res_line.erwachs, Res_line.gratis, Res_line.kind1, Res_line.kind2, Res_line.l_zuordnung, Res_line.abreise, Res_line.zipreis, Res_line.resstatus, Res_line.bemerk, Res_line.ankzeit, Res_line.zikatnr, Res_line.zimmeranz, Res_line.zimmer_wunsch, Res_line.gastnr, Res_line.ankunft, Res_line._recid, Zimmer.zikatnr, Zimmer.zinr, Zimmer.zistatus, Zimmer.sleeping, Zimmer._recid).join(Zimmer,(Zimmer.zinr == Res_line.zinr)).filter(
                 (Res_line.active_flag == 1) & (Res_line.resstatus != 12) & (Res_line.ankunft <= ci_date) & (Res_line.abreise == ci_date) & (Res_line.l_zuordnung[inc_value(2)] == 0)).order_by(Res_line._recid).all():
            if res_line_obj_list.get(res_line._recid):
                continue
            else:
                res_line_obj_list[res_line._recid] = True

            if res_line.resstatus == 6:
                departing1 = departing1 + 1

                zimkateg = get_cache (Zimkateg, {"zikatnr": [(eq, zimmer.zikatnr)]})

                guest = get_cache (Guest, {"gastnr": [(eq, res_line.gastnrmember)]})
                departed = Departed()
                departed_data.append(departed)

                departed.room = res_line.zinr
                departed.rmtype = zimkateg.kurzbez
                departed.gname = guest.name + ", " + guest.vorname1 +\
                        " " + guest.anrede1


            departing2 = departing2 + res_line.erwachs + res_line.gratis + res_line.kind1 + res_line.kind2 + res_line.l_zuordnung[3]

        res_line_obj_list = {}
        res_line = Res_line()
        zimmer = Zimmer()
        reservation = Reservation()
        for res_line.gastnrmember, res_line.zinr, res_line.erwachs, res_line.gratis, res_line.kind1, res_line.kind2, res_line.l_zuordnung, res_line.abreise, res_line.zipreis, res_line.resstatus, res_line.bemerk, res_line.ankzeit, res_line.zikatnr, res_line.zimmeranz, res_line.zimmer_wunsch, res_line.gastnr, res_line.ankunft, res_line._recid, zimmer.zikatnr, zimmer.zinr, zimmer.zistatus, zimmer.sleeping, zimmer._recid, reservation.segmentcode, reservation._recid in db_session.query(Res_line.gastnrmember, Res_line.zinr, Res_line.erwachs, Res_line.gratis, Res_line.kind1, Res_line.kind2, Res_line.l_zuordnung, Res_line.abreise, Res_line.zipreis, Res_line.resstatus, Res_line.bemerk, Res_line.ankzeit, Res_line.zikatnr, Res_line.zimmeranz, Res_line.zimmer_wunsch, Res_line.gastnr, Res_line.ankunft, Res_line._recid, Zimmer.zikatnr, Zimmer.zinr, Zimmer.zistatus, Zimmer.sleeping, Zimmer._recid, Reservation.segmentcode, Reservation._recid).join(Zimmer,(Zimmer.zinr == Res_line.zinr)).join(Reservation,(Reservation.resnr == Res_line.resnr)).filter(
                 (Res_line.active_flag == 1) & (Res_line.resstatus != 12) & (Res_line.ankunft <= ci_date) & (Res_line.abreise >= ci_date) & (Res_line.l_zuordnung[inc_value(2)] == 0)).order_by(Res_line.resnr).all():
            if res_line_obj_list.get(res_line._recid):
                continue
            else:
                res_line_obj_list[res_line._recid] = True

            segment = get_cache (Segment, {"segmentcode": [(eq, reservation.segmentcode)]})

            if zimmer.sleeping and ((res_line.abreise > ci_date) or (res_line.ankunft == ci_date and res_line.abreise == ci_date and res_line.zipreis > 0)):

                if res_line.resstatus == 6:
                    oroom1 = oroom1 + 1
                    eocc1 = eocc1 + 1


                oroom2 = oroom2 + res_line.erwachs + res_line.gratis + res_line.kind1 + res_line.kind2 + res_line.l_zuordnung[3]
                eocc2 = eocc2 + res_line.erwachs + res_line.gratis + res_line.kind1 + res_line.kind2 + res_line.l_zuordnung[3]

            if res_line.ankunft == ci_date:

                if res_line.resstatus == 6:
                    arrived1 = arrived1 + 1

                    zimkateg = get_cache (Zimkateg, {"zikatnr": [(eq, zimmer.zikatnr)]})

                    guest = get_cache (Guest, {"gastnr": [(eq, res_line.gastnrmember)]})
                    arrival_today = Arrival_today()
                    arrival_today_data.append(arrival_today)

                    arrival_today.room = res_line.zinr
                    arrival_today.rmtype = zimkateg.kurzbez
                    arrival_today.gname = guest.name + ", " + guest.vorname1 +\
                            " " + guest.anrede1


                arrived2 = arrived2 + (res_line.erwachs + res_line.gratis + res_line.kind1 + res_line.kind2 + res_line.l_zuordnung[3])

            if segment:

                if segment.betriebsnr == 2:

                    if res_line.resstatus == 6:
                        houseroom1 = houseroom1 + 1


                    houseroom2 = houseroom2 + res_line.erwachs + res_line.gratis + res_line.kind1 + res_line.kind2 + res_line.l_zuordnung[3]

                elif segment.betriebsnr == 1 or res_line.gratis > 0:

                    if res_line.resstatus == 6:
                        comproom1 = comproom1 + 1


                    comproom2 = comproom2 + res_line.erwachs + res_line.gratis + res_line.kind1 + res_line.kind2 + res_line.l_zuordnung[3]

            if not zimmer.sleeping:
                iroom2 = iroom2 + res_line.erwachs + res_line.gratis + res_line.kind1 + res_line.kind2 + res_line.l_zuordnung[3]

        res_line_obj_list = {}
        res_line = Res_line()
        zimmer = Zimmer()
        for res_line.gastnrmember, res_line.zinr, res_line.erwachs, res_line.gratis, res_line.kind1, res_line.kind2, res_line.l_zuordnung, res_line.abreise, res_line.zipreis, res_line.resstatus, res_line.bemerk, res_line.ankzeit, res_line.zikatnr, res_line.zimmeranz, res_line.zimmer_wunsch, res_line.gastnr, res_line.ankunft, res_line._recid, zimmer.zikatnr, zimmer.zinr, zimmer.zistatus, zimmer.sleeping, zimmer._recid in db_session.query(Res_line.gastnrmember, Res_line.zinr, Res_line.erwachs, Res_line.gratis, Res_line.kind1, Res_line.kind2, Res_line.l_zuordnung, Res_line.abreise, Res_line.zipreis, Res_line.resstatus, Res_line.bemerk, Res_line.ankzeit, Res_line.zikatnr, Res_line.zimmeranz, Res_line.zimmer_wunsch, Res_line.gastnr, Res_line.ankunft, Res_line._recid, Zimmer.zikatnr, Zimmer.zinr, Zimmer.zistatus, Zimmer.sleeping, Zimmer._recid).join(Zimmer,(Zimmer.zinr == Res_line.zinr)).filter(
                 (Res_line.active_flag == 2) & (Res_line.resstatus == 8) & (Res_line.ankunft <= ci_date) & (Res_line.abreise == ci_date) & (Res_line.l_zuordnung[inc_value(2)] == 0)).order_by(Res_line._recid).all():
            if res_line_obj_list.get(res_line._recid):
                continue
            else:
                res_line_obj_list[res_line._recid] = True

            if not res_line.zimmerfix:
                departed1 = departed1 + 1

                zimkateg = get_cache (Zimkateg, {"zikatnr": [(eq, zimmer.zikatnr)]})

                guest = get_cache (Guest, {"gastnr": [(eq, res_line.gastnrmember)]})
                depart_today = Depart_today()
                depart_today_data.append(depart_today)

                depart_today.room = res_line.zinr
                depart_today.rmtype = zimkateg.kurzbez
                depart_today.gname = guest.name + ", " + guest.vorname1 +\
                        " " + guest.anrede1


            departed2 = departed2 + res_line.erwachs + res_line.gratis +\
                    res_line.kind1 + res_line.kind2 + res_line.l_zuordnung[3]


        tot_depart1 = departed1 + departing1
        tot_depart2 = departed2 + departing2

        for res_line in db_session.query(Res_line).filter(
                 (Res_line.active_flag == 0) & (Res_line.ankunft == ci_date) & (Res_line.l_zuordnung[inc_value(2)] == 0)).order_by(Res_line._recid).all():

            zimmer = get_cache (Zimmer, {"zinr": [(eq, res_line.zinr)]})
            rm_active = True

            if (zimmer and not zimmer.sleeping):
                rm_active = False

            if (res_line.resstatus == 1 or res_line.resstatus == 2 or res_line.resstatus == 5):
                resbemerk = res_line.bemerk
                resbemerk = replace_str(resbemerk, chr_unicode(10) , "")
                resbemerk = replace_str(resbemerk, chr_unicode(13) , "")
                resbemerk = replace_str(resbemerk, "~n", "")
                resbemerk = replace_str(resbemerk, "\\n", "")
                resbemerk = replace_str(resbemerk, "~r", "")
                resbemerk = replace_str(resbemerk, "~r~n", "")
                resbemerk = replace_str(resbemerk, "&nbsp;", " ")
                resbemerk = replace_str(resbemerk, "</p>", "</p></p>")
                resbemerk = replace_str(resbemerk, "</p>", chr_unicode(13))
                resbemerk = replace_str(resbemerk, "<BR>", chr_unicode(13))
                resbemerk = replace_str(resbemerk, chr_unicode(10) + chr_unicode(13) , "")

                if length(resbemerk) < 3:
                    resbemerk = replace_str(resbemerk, chr_unicode(32) , "")

                if length(resbemerk) < 3:
                    resbemerk = ""

                if length(resbemerk) == None:
                    resbemerk = ""
                arriving1 = arriving1 + 1

                guest = get_cache (Guest, {"gastnr": [(eq, res_line.gastnrmember)]})
                arrived = Arrived()
                arrived_data.append(arrived)

                arrived.room = res_line.zinr
                arrived.gname = guest.name + ", " + guest.vorname1 +\
                        " " + guest.anrede1
                arrived.arrtime = to_string(res_line.ankzeit, "HH:MM:SS")
                arrived.rsv_remark = resbemerk

                zimkateg = get_cache (Zimkateg, {"zikatnr": [(eq, res_line.zikatnr)]})

                if zimkateg:
                    arrived.rmtype = zimkateg.kurzbez

                if matches(res_line.zimmer_wunsch,r"*PCIFLAG=YES*"):
                    arrived.pci = True

                if rm_active:
                    eocc1 = eocc1 + res_line.zimmeranz

                if zimmer:

                    if zimmer.zistatus == 0:
                        arrived.room_status = "Vacant Clean Checked"

                    elif zimmer.zistatus == 1:
                        arrived.room_status = "Vacant Clean Unchecked"

                    elif zimmer.zistatus == 2:
                        arrived.room_status = "Vacant Dirty"

                    elif zimmer.zistatus == 3:
                        arrived.room_status = "Expected Departure"

                    elif zimmer.zistatus == 4:
                        arrived.room_status = "Occupied Dirty"

                    elif zimmer.zistatus == 5:
                        arrived.room_status = "Occupied Cleaned"

                    elif zimmer.zistatus == 6:
                        arrived.room_status = "Out Of Order"

                    elif zimmer.zistatus == 7:
                        arrived.room_status = "Off Market"

                    elif zimmer.zistatus == 8:
                        arrived.room_status = "Do Not Disturb"
                for loop_i in range(1,num_entries(res_line.zimmer_wunsch, ";") - 1 + 1) :
                    str = entry(loop_i - 1, res_line.zimmer_wunsch, ";")

                    if matches(str,r"*WCI-req*"):
                        str1 = entry(1, str, "=")
                        for loop_j in range(1,num_entries(str1, ",")  + 1) :

                            queasy = get_cache (Queasy, {"key": [(eq, 160)],"number1": [(eq, to_int(entry(loop_j - 1, str1, ",")))]})

                            if queasy:
                                for loopj in range(1,num_entries(queasy.char1, ";")  + 1) :

                                    if matches(entry(loopj - 1, queasy.char1, ";"),r"*en*"):
                                        arrived.guest_pref = entry(1, entry(loopj - 1, queasy.char1, ";") , "=") + ", " + arrived.guest_pref


                                        break

            if (res_line.resstatus == 1 or res_line.resstatus == 2 or res_line.resstatus == 5 or res_line.resstatus == 11):
                arriving2 = arriving2 + res_line.zimmeranz * (res_line.erwachs + res_line.gratis + res_line.kind1 + res_line.kind2 + res_line.l_zuordnung[3])
                eocc2 = eocc2 + res_line.zimmeranz * (res_line.erwachs + res_line.gratis + res_line.kind1 + res_line.kind2 + res_line.l_zuordnung[3])
        tot_arrive1 = arrived1 + arriving1
        tot_arrive2 = arrived2 + arriving2

        zimmer_obj_list = {}
        zimmer = Zimmer()
        zimkateg = Zimkateg()
        for zimmer.zikatnr, zimmer.zinr, zimmer.zistatus, zimmer.sleeping, zimmer._recid, zimkateg.kurzbez, zimkateg._recid, zimkateg.verfuegbarkeit \
            in db_session.query(Zimmer.zikatnr, Zimmer.zinr, Zimmer.zistatus, Zimmer.sleeping, Zimmer._recid, Zimkateg.kurzbez, Zimkateg._recid, Zimkateg.verfuegbarkeit)\
            .join(Zimkateg,(Zimkateg.zikatnr == Zimmer.zikatnr))\
            .order_by(Zimmer._recid).all():
            if zimmer_obj_list.get(zimmer._recid):
                continue
            else:
                zimmer_obj_list[zimmer._recid] = True

            if zimkateg.verfuegbarkeit:
                outorder = get_cache (Outorder, {"zinr": [(eq, zimmer.zinr)],"gespstart": [(le, ci_date)],"gespende": [(ge, ci_date)],"betriebsnr": [(eq, 2)]})

                if outorder:
                    omroom1 = omroom1 + 1
                    off_market = Off_market()
                    off_market_data.append(off_market)

                    off_market.room = zimmer.zinr
                    off_market.rmtype = zimkateg.kurzbez
                    off_market.gname = outorder.gespgrund

                if (zimmer.zistatus == 0 or zimmer.zistatus == 1 or zimmer.zistatus == 5):

                    if zimmer.zistatus == 0:
                        vclean = vclean + 1
                        vacant_clean_checked = Vacant_clean_checked()
                        vacant_clean_checked_data.append(vacant_clean_checked)

                        vacant_clean_checked.room = zimmer.zinr
                        vacant_clean_checked.rmtype = zimkateg.kurzbez

                    elif zimmer.zistatus == 1:
                        vuncheck = vuncheck + 1
                        vacant_clean_unchecked = Vacant_clean_unchecked()
                        vacant_clean_unchecked_data.append(vacant_clean_unchecked)

                        vacant_clean_unchecked.room = zimmer.zinr
                        vacant_clean_unchecked.rmtype = zimkateg.kurzbez

                    elif zimmer.zistatus == 5:
                        oclean = oclean + 1
                        occ_clean = Occ_clean()
                        occ_clean_data.append(occ_clean)

                        occ_clean.room = zimmer.zinr
                        occ_clean.rmtype = zimkateg.kurzbez

                        res_line = get_cache (Res_line, {"zinr": [(eq, zimmer.zinr)],"resstatus": [(eq, 6)],"active_flag": [(eq, 1)]})

                        if res_line:

                            guest = get_cache (Guest, {"gastnr": [(eq, res_line.gastnrmember)]})

                            if guest:
                                occ_clean.gname = guest.name + ", " + guest.vorname1 + " " + guest.anrede1

                elif (zimmer.zistatus == 2 or zimmer.zistatus == 3 or zimmer.zistatus == 4):

                    if zimmer.zistatus == 2:
                        vdirty = vdirty + 1
                        vacant_dirty = Vacant_dirty()
                        vacant_dirty_data.append(vacant_dirty)

                        vacant_dirty.room = zimmer.zinr
                        vacant_dirty.rmtype = zimkateg.kurzbez

                    elif zimmer.zistatus == 4:
                        odirty = odirty + 1
                        occ_dirty = Occ_dirty()
                        occ_dirty_data.append(occ_dirty)

                        occ_dirty.room = zimmer.zinr
                        occ_dirty.rmtype = zimkateg.kurzbez

                        res_line = get_cache (Res_line, {"zinr": [(eq, zimmer.zinr)],"resstatus": [(eq, 6)],"active_flag": [(eq, 1)]})

                        if res_line:

                            guest = get_cache (Guest, {"gastnr": [(eq, res_line.gastnrmember)]})

                            if guest:
                                occ_dirty.gname = guest.name + ", " + guest.vorname1 + " " + guest.anrede1

                    elif zimmer.zistatus == 3:
                        atoday = atoday + 1
                        ex_depart = Ex_depart()
                        ex_depart_data.append(ex_depart)

                        ex_depart.room = zimmer.zinr
                        ex_depart.rmtype = zimkateg.kurzbez

                elif zimmer.zistatus == 6:
                    oooroom1 = oooroom1 + 1
                    ooo_room = Ooo_room()
                    ooo_room_data.append(ooo_room)

                    ooo_room.room = zimmer.zinr
                    ooo_room.rmtype = zimkateg.kurzbez

                    outorder = get_cache (Outorder, {"zinr": [(eq, zimmer.zinr)],"gespstart": [(le, ci_date)],"gespende": [(ge, ci_date)],"betriebsnr": [(ne, 2)]})

                    if outorder:
                        ooo_room.gname = outorder.gespgrund

                if not zimmer.sleeping:
                    iroom1 = iroom1 + 1

                if zimmer.sleeping:
                    tot_zimmer = tot_zimmer + 1

        for zimmer in db_session.query(Zimmer).filter(
                 (Zimmer.sleeping)).order_by(Zimmer._recid).all():
            tot_avail = tot_avail + 1

        res_line_obj_list = {}
        res_line = Res_line()
        zimkateg = Zimkateg()
        reservation = Reservation()
        guest = Guest()
        zimmer = Zimmer()
        for res_line.gastnrmember, res_line.zinr, res_line.erwachs, res_line.gratis, res_line.kind1, res_line.kind2, res_line.l_zuordnung, res_line.abreise, res_line.zipreis, res_line.resstatus, res_line.bemerk, res_line.ankzeit, res_line.zikatnr, res_line.zimmeranz, res_line.zimmer_wunsch, res_line.gastnr, res_line.ankunft, res_line._recid, zimkateg.kurzbez, zimkateg._recid, reservation.segmentcode, reservation._recid, guest.name, guest.vorname1, guest.anrede1, guest._recid, zimmer.zikatnr, zimmer.zinr, zimmer.zistatus, zimmer.sleeping, zimmer._recid in db_session.query(Res_line.gastnrmember, Res_line.zinr, Res_line.erwachs, Res_line.gratis, Res_line.kind1, Res_line.kind2, Res_line.l_zuordnung, Res_line.abreise, Res_line.zipreis, Res_line.resstatus, Res_line.bemerk, Res_line.ankzeit, Res_line.zikatnr, Res_line.zimmeranz, Res_line.zimmer_wunsch, Res_line.gastnr, Res_line.ankunft, Res_line._recid, Zimkateg.kurzbez, Zimkateg._recid, Reservation.segmentcode, Reservation._recid, Guest.name, Guest.vorname1, Guest.anrede1, Guest._recid, Zimmer.zikatnr, Zimmer.zinr, Zimmer.zistatus, Zimmer.sleeping, Zimmer._recid).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Guest,(Guest.gastnr == Reservation.gastnr)).join(Zimmer,(Zimmer.zinr == Res_line.zinr) & (Zimmer.sleeping)).filter(
                 (Res_line.active_flag >= 1) & (Res_line.active_flag <= 1) & (Res_line.resstatus != 9) & (Res_line.resstatus != 10) & (Res_line.resstatus != 12) & (Res_line.ankunft <= ci_date) & (Res_line.abreise >= ci_date)).order_by(Res_line.zinr, Res_line.erwachs.desc(), Res_line.name).all():
            if res_line_obj_list.get(res_line._recid):
                continue
            else:
                res_line_obj_list[res_line._recid] = True

            if zimmer.sleeping and (res_line.zipreis > 0 or res_line.zipreis == 0) and res_line.resstatus != 13 and res_line.erwachs > 0:

                queasy = get_cache (Queasy, {"key": [(eq, 14)],"char1": [(eq, res_line.zinr)],"date1": [(le, ci_date)],"date2": [(ge, ci_date)]})

                if not queasy:
                    tot_payrm = tot_payrm + res_line.zimmeranz
                    tot_pax = tot_pax + res_line.erwachs

                elif queasy and queasy.number3 != res_line.gastnr:
                    tot_payrm = tot_payrm + res_line.zimmeranz
                    tot_pax = tot_pax + res_line.erwachs
        paying_room = Paying_room()
        paying_room_data.append(paying_room)

        paying_room.room = tot_payrm
        paying_room.pax = tot_pax
        paying_room.percentage =  to_decimal(tot_payrm) / to_decimal(tot_avail) * to_decimal("100")

        if tot_zimmer == 0:
            proz1 =  to_decimal(None)
            proz2 =  to_decimal(None)
            proz3 =  to_decimal(None)
            proz4 =  to_decimal(None)
            proz5 =  to_decimal(None)
        else:
            proz1 =  to_decimal(oroom1) * to_decimal("100") / to_decimal(tot_zimmer)
            proz2 =  to_decimal(oooroom1) * to_decimal("100") / to_decimal(tot_zimmer)
            proz3 =  to_decimal(eocc1) * to_decimal("100") / to_decimal(tot_zimmer)
            proz4 =  to_decimal(comproom1) * to_decimal("100") / to_decimal(tot_zimmer)
            proz5 =  to_decimal(houseroom1) * to_decimal("100") / to_decimal(tot_zimmer)

    htparam = get_cache (Htparam, {"paramnr": [(eq, 87)]})
    ci_date = htparam.fdate
    init_var()
    queue_room_list_data = get_output(read_queasybl(3, 162, 0, ""))

    for queue_room_list in query(queue_room_list_data):

        if queue_room_list.number1 == 0:
            queue_room_list.char3 = translateExtended ("On Progress", lvcarea, "")

        elif queue_room_list.number1 == 1:
            queue_room_list.char3 = translateExtended ("DONE", lvcarea, "")

    return generate_output()