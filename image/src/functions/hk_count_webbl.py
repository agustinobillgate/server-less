from functions.additional_functions import *
import decimal
from datetime import date
from functions.read_queasybl import read_queasybl
import re
from models import Queasy, Htparam, Zimmer, Res_line, Zimkateg, Guest, Reservation, Segment, Outorder

def hk_count_webbl(pvilanguage:int):
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
    proz1 = 0
    proz2 = 0
    proz3 = 0
    proz4 = 0
    proz5 = 0
    queue_room_list_list = []
    depart_today_list = []
    departed_list = []
    arrival_today_list = []
    arrived_list = []
    vacant_clean_checked_list = []
    vacant_clean_unchecked_list = []
    occ_clean_list = []
    occ_dirty_list = []
    vacant_dirty_list = []
    ex_depart_list = []
    off_market_list = []
    ooo_room_list = []
    lvcarea:str = ""
    ci_date:date = None
    loop_i:int = 0
    str:str = ""
    str1:str = ""
    loop_j:int = 0
    loopj:int = 0
    queasy = htparam = zimmer = res_line = zimkateg = guest = reservation = segment = outorder = None

    depart_today = departed = arrival_today = arrived = vacant_clean_checked = vacant_clean_unchecked = occ_clean = occ_dirty = vacant_dirty = ex_depart = off_market = ooo_room = queue_room_list = None

    depart_today_list, Depart_today = create_model("Depart_today", {"room":str, "rmtype":str, "gname":str})
    departed_list, Departed = create_model("Departed", {"room":str, "rmtype":str, "gname":str})
    arrival_today_list, Arrival_today = create_model("Arrival_today", {"room":str, "rmtype":str, "gname":str})
    arrived_list, Arrived = create_model("Arrived", {"room":str, "rmtype":str, "gname":str, "arrtime":str, "rsv_remark":str, "guest_pref":str, "room_status":str, "pci":bool})
    vacant_clean_checked_list, Vacant_clean_checked = create_model("Vacant_clean_checked", {"room":str, "rmtype":str, "gname":str})
    vacant_clean_unchecked_list, Vacant_clean_unchecked = create_model("Vacant_clean_unchecked", {"room":str, "rmtype":str, "gname":str})
    occ_clean_list, Occ_clean = create_model("Occ_clean", {"room":str, "rmtype":str, "gname":str})
    occ_dirty_list, Occ_dirty = create_model("Occ_dirty", {"room":str, "rmtype":str, "gname":str})
    vacant_dirty_list, Vacant_dirty = create_model("Vacant_dirty", {"room":str, "rmtype":str, "gname":str})
    ex_depart_list, Ex_depart = create_model("Ex_depart", {"room":str, "rmtype":str, "gname":str})
    off_market_list, Off_market = create_model("Off_market", {"room":str, "rmtype":str, "gname":str})
    ooo_room_list, Ooo_room = create_model("Ooo_room", {"room":str, "rmtype":str, "gname":str})
    queue_room_list_list, Queue_room_list = create_model_like(Queasy)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal departed1, departed2, departing1, departing2, tot_depart1, tot_depart2, arrived1, arrived2, arriving1, arriving2, tot_arrive1, tot_arrive2, vclean, vuncheck, oclean, tot_clean, odirty, vdirty, atoday, tot_dirty, oroom1, oroom2, omroom1, omroom2, oooroom1, oooroom2, comproom1, comproom2, houseroom1, houseroom2, iroom1, iroom2, eocc1, eocc2, proz1, proz2, proz3, proz4, proz5, queue_room_list_list, depart_today_list, departed_list, arrival_today_list, arrived_list, vacant_clean_checked_list, vacant_clean_unchecked_list, occ_clean_list, occ_dirty_list, vacant_dirty_list, ex_depart_list, off_market_list, ooo_room_list, lvcarea, ci_date, loop_i, str, str1, loop_j, loopj, queasy, htparam, zimmer, res_line, zimkateg, guest, reservation, segment, outorder


        nonlocal depart_today, departed, arrival_today, arrived, vacant_clean_checked, vacant_clean_unchecked, occ_clean, occ_dirty, vacant_dirty, ex_depart, off_market, ooo_room, queue_room_list
        nonlocal depart_today_list, departed_list, arrival_today_list, arrived_list, vacant_clean_checked_list, vacant_clean_unchecked_list, occ_clean_list, occ_dirty_list, vacant_dirty_list, ex_depart_list, off_market_list, ooo_room_list, queue_room_list_list
        return {"departed1": departed1, "departed2": departed2, "departing1": departing1, "departing2": departing2, "tot_depart1": tot_depart1, "tot_depart2": tot_depart2, "arrived1": arrived1, "arrived2": arrived2, "arriving1": arriving1, "arriving2": arriving2, "tot_arrive1": tot_arrive1, "tot_arrive2": tot_arrive2, "vclean": vclean, "vuncheck": vuncheck, "oclean": oclean, "tot_clean": tot_clean, "odirty": odirty, "vdirty": vdirty, "atoday": atoday, "tot_dirty": tot_dirty, "oroom1": oroom1, "oroom2": oroom2, "omroom1": omroom1, "omroom2": omroom2, "oooroom1": oooroom1, "oooroom2": oooroom2, "comproom1": comproom1, "comproom2": comproom2, "houseroom1": houseroom1, "houseroom2": houseroom2, "iroom1": iroom1, "iroom2": iroom2, "eocc1": eocc1, "eocc2": eocc2, "proz1": proz1, "proz2": proz2, "proz3": proz3, "proz4": proz4, "proz5": proz5, "queue-room-list": queue_room_list_list, "depart-today": depart_today_list, "departed": departed_list, "arrival-today": arrival_today_list, "arrived": arrived_list, "vacant-clean-checked": vacant_clean_checked_list, "vacant-clean-unchecked": vacant_clean_unchecked_list, "occ-clean": occ_clean_list, "occ-dirty": occ_dirty_list, "vacant-dirty": vacant_dirty_list, "ex-depart": ex_depart_list, "off-market": off_market_list, "ooo-room": ooo_room_list}

    def init_var():

        nonlocal departed1, departed2, departing1, departing2, tot_depart1, tot_depart2, arrived1, arrived2, arriving1, arriving2, tot_arrive1, tot_arrive2, vclean, vuncheck, oclean, tot_clean, odirty, vdirty, atoday, tot_dirty, oroom1, oroom2, omroom1, omroom2, oooroom1, oooroom2, comproom1, comproom2, houseroom1, houseroom2, iroom1, iroom2, eocc1, eocc2, proz1, proz2, proz3, proz4, proz5, queue_room_list_list, depart_today_list, departed_list, arrival_today_list, arrived_list, vacant_clean_checked_list, vacant_clean_unchecked_list, occ_clean_list, occ_dirty_list, vacant_dirty_list, ex_depart_list, off_market_list, ooo_room_list, lvcarea, ci_date, loop_i, str, str1, loop_j, loopj, queasy, htparam, zimmer, res_line, zimkateg, guest, reservation, segment, outorder


        nonlocal depart_today, departed, arrival_today, arrived, vacant_clean_checked, vacant_clean_unchecked, occ_clean, occ_dirty, vacant_dirty, ex_depart, off_market, ooo_room, queue_room_list
        nonlocal depart_today_list, departed_list, arrival_today_list, arrived_list, vacant_clean_checked_list, vacant_clean_unchecked_list, occ_clean_list, occ_dirty_list, vacant_dirty_list, ex_depart_list, off_market_list, ooo_room_list, queue_room_list_list

        tot_zimmer:int = 0
        rm_active:bool = False
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

        res_line_obj_list = []
        for res_line, zimmer in db_session.query(Res_line, Zimmer).join(Zimmer,(Zimmer.zinr == Res_line.zinr)).filter(
                (Res_line.active_flag == 1) &  (Res_line.resstatus != 12) &  (Res_line.ankunft <= ci_date) &  (Res_line.abreise == ci_date) &  (Res_line.l_zuordnung[2] == 0)).all():
            if res_line._recid in res_line_obj_list:
                continue
            else:
                res_line_obj_list.append(res_line._recid)

            if res_line.resstatus == 6:
                departing1 = departing1 + 1

                zimkateg = db_session.query(Zimkateg).filter(
                        (Zimkateg.zikatnr == zimmer.zikatnr)).first()

                guest = db_session.query(Guest).filter(
                        (Guest.gastnr == res_line.gastnrmember)).first()
                departed = Departed()
                departed_list.append(departed)

                departed.room = res_line.zinr
                departed.rmtype = zimkateg.kurzbez
                departed.gname = guest.name + ", " + guest.vorname1 +\
                        " " + guest.anrede1


            departing2 = departing2 + res_line.erwachs + res_line.gratis + res_line.kind1 + res_line.kind2 + res_line.l_zuordnung[3]

        res_line_obj_list = []
        for res_line, zimmer, reservation in db_session.query(Res_line, Zimmer, Reservation).join(Zimmer,(Zimmer.zinr == Res_line.zinr)).join(Reservation,(Reservation.resnr == Res_line.resnr)).filter(
                (Res_line.active_flag == 1) &  (Res_line.resstatus != 12) &  (Res_line.ankunft <= ci_date) &  (Res_line.abreise >= ci_date) &  (Res_line.l_zuordnung[2] == 0)).all():
            if res_line._recid in res_line_obj_list:
                continue
            else:
                res_line_obj_list.append(res_line._recid)

            segment = db_session.query(Segment).filter(
                    (Segment.segmentcode == reservation.segmentcode)).first()

            if zimmer.sleeping and ((res_line.abreise > ci_date) or (res_line.ankunft == ci_date and res_line.abreise == ci_date and res_line.zipreis > 0)):

                if res_line.resstatus == 6:
                    oroom1 = oroom1 + 1
                    eocc1 = eocc1 + 1


                oroom2 = oroom2 + res_line.erwachs + res_line.gratis + res_line.kind1 + res_line.kind2 + res_line.l_zuordnung[3]
                eocc2 = eocc2 + res_line.erwachs + res_line.gratis + res_line.kind1 + res_line.kind2 + res_line.l_zuordnung[3]

            if res_line.ankunft == ci_date:

                if res_line.resstatus == 6:
                    arrived1 = arrived1 + 1

                    zimkateg = db_session.query(Zimkateg).filter(
                            (Zimkateg.zikatnr == zimmer.zikatnr)).first()

                    guest = db_session.query(Guest).filter(
                            (Guest.gastnr == res_line.gastnrmember)).first()
                    arrival_today = Arrival_today()
                    arrival_today_list.append(arrival_today)

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

        res_line_obj_list = []
        for res_line, zimmer in db_session.query(Res_line, Zimmer).join(Zimmer,(Zimmer.zinr == Res_line.zinr)).filter(
                (Res_line.active_flag == 2) &  (Res_line.resstatus == 8) &  (Res_line.ankunft <= ci_date) &  (Res_line.abreise == ci_date) &  (Res_line.l_zuordnung[2] == 0)).all():
            if res_line._recid in res_line_obj_list:
                continue
            else:
                res_line_obj_list.append(res_line._recid)

            if not res_line.zimmerfix:
                departed1 = departed1 + 1

                zimkateg = db_session.query(Zimkateg).filter(
                        (Zimkateg.zikatnr == zimmer.zikatnr)).first()

                guest = db_session.query(Guest).filter(
                        (Guest.gastnr == res_line.gastnrmember)).first()
                depart_today = Depart_today()
                depart_today_list.append(depart_today)

                depart_today.room = res_line.zinr
                depart_today.rmtype = zimkateg.kurzbez
                depart_today.gname = guest.name + ", " + guest.vorname1 +\
                        " " + guest.anrede1


            departed2 = departed2 + res_line.erwachs + res_line.gratis +\
                    res_line.kind1 + res_line.kind2 + res_line.l_zuordnung[3]


        tot_depart1 = departed1 + departing1
        tot_depart2 = departed2 + departing2

        for res_line in db_session.query(Res_line).filter(
                (Res_line.active_flag == 0) &  (Res_line.ankunft == ci_date) &  (Res_line.l_zuordnung[2] == 0)).all():

            zimmer = db_session.query(Zimmer).filter(
                    (Zimmer.zinr == res_line.zinr)).first()
            rm_active = True

            if (zimmer and not zimmer.sleeping):
                rm_active = False

            if (res_line.resstatus == 1 or res_line.resstatus == 2 or res_line.resstatus == 5):
                arriving1 = arriving1 + res_line.zimmeranz

                guest = db_session.query(Guest).filter(
                        (Guest.gastnr == res_line.gastnrmember)).first()
                arrived = Arrived()
                arrived_list.append(arrived)

                arrived.room = res_line.zinr
                arrived.gname = guest.name + ", " + guest.vorname1 +\
                        " " + guest.anrede1
                arrived.arrtime = to_string(res_line.ankzeit, "HH:MM:SS")
                arrived.rsv_remark = res_line.bemerk

                zimkateg = db_session.query(Zimkateg).filter(
                        (Zimkateg.zikatnr == res_line.zikatnr)).first()

                if zimkateg:
                    arrived.rmtype = zimkateg.kurzbez

                if re.match(".*PCIFLAG.*",res_line.zimmer_wunsch):
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

                    if re.match(".*WCI_req.*",str):
                        str1 = entry(1, str, " == ")
                        for loop_j in range(1,num_entries(str1, ",")  + 1) :

                            queasy = db_session.query(Queasy).filter(
                                    (Queasy.key == 160) &  (Queasy.number1 == to_int(entry(loop_j - 1, str1, ",")))).first()

                            if queasy:
                                for loopj in range(1,num_entries(queasy.char1, ";")  + 1) :

                                    if re.match(".*en.*",entry(loopj - 1, queasy.char1, ";")):
                                        arrived.guest_pref = entry(1, entry(loopj - 1, queasy.char1, ";") , " == ") + ", " + arrived.guest_pref


                                        break

            if (res_line.resstatus == 1 or res_line.resstatus == 2 or res_line.resstatus == 5 or res_line.resstatus == 11):
                arriving2 = arriving2 + res_line.zimmeranz * (res_line.erwachs + res_line.gratis + res_line.kind1 + res_line.kind2 + res_line.l_zuordnung[3])
                eocc2 = eocc2 + res_line.zimmeranz * (res_line.erwachs + res_line.gratis + res_line.kind1 + res_line.kind2 + res_line.l_zuordnung[3])
        tot_arrive1 = arrived1 + arriving1
        tot_arrive2 = arrived2 + arriving2

        zimmer_obj_list = []
        for zimmer, zimkateg in db_session.query(Zimmer, Zimkateg).join(Zimkateg,(Zimkateg.zikatnr == Zimmer.zikatnr)).all():
            if zimmer._recid in zimmer_obj_list:
                continue
            else:
                zimmer_obj_list.append(zimmer._recid)

            if zimkateg.verfuegbarkeit:

                outorder = db_session.query(Outorder).filter(
                        (Outorder.zinr == zimmer.zinr) &  (Outorder.gespstart <= ci_date) &  (Outorder.gespende >= ci_date) &  (Outorder.betriebsnr == 2)).first()

                if outorder:
                    omroom1 = omroom1 + 1
                    off_market = Off_market()
                    off_market_list.append(off_market)

                    off_market.room = zimmer.zinr
                    off_market.rmtype = zimkateg.kurzbez
                    off_market.gname = outorder.gespgrund

                if (zimmer.zistatus == 0 or zimmer.zistatus == 1 or zimmer.zistatus == 5):

                    if zimmer.zistatus == 0:
                        vclean = vclean + 1
                        vacant_clean_checked = Vacant_clean_checked()
                        vacant_clean_checked_list.append(vacant_clean_checked)

                        vacant_clean_checked.room = zimmer.zinr
                        vacant_clean_checked.rmtype = zimkateg.kurzbez

                    elif zimmer.zistatus == 1:
                        vuncheck = vuncheck + 1
                        vacant_clean_unchecked = Vacant_clean_unchecked()
                        vacant_clean_unchecked_list.append(vacant_clean_unchecked)

                        vacant_clean_unchecked.room = zimmer.zinr
                        vacant_clean_unchecked.rmtype = zimkateg.kurzbez

                    elif zimmer.zistatus == 5:
                        oclean = oclean + 1
                        occ_clean = Occ_clean()
                        occ_clean_list.append(occ_clean)

                        occ_clean.room = zimmer.zinr
                        occ_clean.rmtype = zimkateg.kurzbez

                        res_line = db_session.query(Res_line).filter(
                                    (Res_line.zinr == zimmer.zinr) &  (Res_line.resstatus == 6) &  (Res_line.active_flag == 1)).first()

                        if res_line:

                            guest = db_session.query(Guest).filter(
                                        (Guest.gastnr == res_line.gastnrmember)).first()

                            if guest:
                                occ_clean.gname = guest.name + ", " + guest.vorname1 + " " + guest.anrede1

                elif (zimmer.zistatus == 2 or zimmer.zistatus == 3 or zimmer.zistatus == 4):

                    if zimmer.zistatus == 2:
                        vdirty = vdirty + 1
                        vacant_dirty = Vacant_dirty()
                        vacant_dirty_list.append(vacant_dirty)

                        vacant_dirty.room = zimmer.zinr
                        vacant_dirty.rmtype = zimkateg.kurzbez

                    elif zimmer.zistatus == 4:
                        odirty = odirty + 1
                        occ_dirty = Occ_dirty()
                        occ_dirty_list.append(occ_dirty)

                        occ_dirty.room = zimmer.zinr
                        occ_dirty.rmtype = zimkateg.kurzbez

                        res_line = db_session.query(Res_line).filter(
                                    (Res_line.zinr == zimmer.zinr) &  (Res_line.resstatus == 6) &  (Res_line.active_flag == 1)).first()

                        if res_line:

                            guest = db_session.query(Guest).filter(
                                        (Guest.gastnr == res_line.gastnrmember)).first()

                            if guest:
                                occ_dirty.gname = guest.name + ", " + guest.vorname1 + " " + guest.anrede1

                    elif zimmer.zistatus == 3:
                        atoday = atoday + 1
                        ex_depart = Ex_depart()
                        ex_depart_list.append(ex_depart)

                        ex_depart.room = zimmer.zinr
                        ex_depart.rmtype = zimkateg.kurzbez

                elif zimmer.zistatus == 6:
                    oooroom1 = oooroom1 + 1
                    ooo_room = Ooo_room()
                    ooo_room_list.append(ooo_room)

                    ooo_room.room = zimmer.zinr
                    ooo_room.rmtype = zimkateg.kurzbez

                    outorder = db_session.query(Outorder).filter(
                                (Outorder.zinr == zimmer.zinr) &  (Outorder.gespstart <= ci_date) &  (Outorder.gespende >= ci_date) &  (Outorder.betriebsnr != 2)).first()

                    if outorder:
                        ooo_room.gname = outorder.gespgrund

                if not zimmer.sleeping:
                    iroom1 = iroom1 + 1

                if zimmer.sleeping:
                    tot_zimmer = tot_zimmer + 1
        proz1 = oroom1 * 100 / tot_zimmer
        proz2 = oooroom1 * 100 / tot_zimmer
        proz3 = eocc1 * 100 / tot_zimmer
        proz4 = comproom1 * 100 / tot_zimmer
        proz5 = houseroom1 * 100 / tot_zimmer

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 87)).first()
    ci_date = htparam.fdate
    init_var()
    queue_room_list_list = get_output(read_queasybl(3, 162, 0, ""))

    for queue_room_list in query(queue_room_list_list):

        if queue_room_list.number1 == 0:
            queue_room_list.char3 = translateExtended ("On Progress", lvcarea, "")

        elif queue_room_list.number1 == 1:
            queue_room_list.char3 = translateExtended ("DONE", lvcarea, "")

    return generate_output()