#using conversion tools version: 1.0.0.117

#-----------------------------------------
# Rd, 21/7/225
# requery
#-----------------------------------------

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Res_line, Zimkateg, Htparam, Zimmer, Genstat, Zinrstat, Kontline, Artikel, Fixleist, Arrangement, Reslin_queasy, Paramtext, Outorder, Guest

zikat_list_data, Zikat_list = create_model("Zikat_list", {"selected":bool, "zikatnr":int, "kurzbez":string, "bezeich":string})

def availability1_1bl(pvilanguage:int, printer_nr:int, call_from:int, txt_file:string, curr_date:date, incl_tentative:bool, zikat_list_data:[Zikat_list]):

    prepare_cache ([Zimkateg, Htparam, Zimmer, Genstat, Kontline, Artikel, Fixleist, Arrangement, Reslin_queasy, Paramtext, Outorder])

    msg_str = ""
    room_list_data = []
    sum_list_data = []
    lnldelimeter:string = ""
    ttl_room:List[int] = create_empty_list(21,0)
    occ_room:List[int] = create_empty_list(21,0)
    ooo_room:List[int] = create_empty_list(21,0)
    anz_setup:int = 0
    tot_room:int = 0
    isetup_array:List[int] = create_empty_list(99,0)
    csetup_array:List[string] = create_empty_list(99,"")
    ci_date:date = None
    datum:date = None
    week_list:List[string] = [" Mon ", " Tue ", " Wed ", " Thu ", " Fri ", " Sat ", " Sun "]
    i:int = 0
    j:int = 0
    curr_day:int = 0
    lvcarea:string = "availability1"
    res_line = zimkateg = htparam = zimmer = genstat = zinrstat = kontline = artikel = fixleist = arrangement = reslin_queasy = paramtext = outorder = guest = None

    rmcat_list = room_list = sum_list = tmp_resline = tmp_extra = temp_art = zikat_list = zkbuff = rlist = rlist = None

    rmcat_list_data, Rmcat_list = create_model("Rmcat_list", {"zikatnr":int, "kurzbez":string, "kurzbez1":string, "bezeich":string, "setup":string, "haupt":bool, "anzahl":int, "nr":int, "glores":bool})
    room_list_data, Room_list = create_model("Room_list", {"flag":string, "setup":int, "haupt":bool, "zikatnr":int, "bezeich":string, "room":[Decimal,21], "coom":[string,21], "glores":bool})
    sum_list_data, Sum_list = create_model("Sum_list", {"bezeich":string, "summe":[string,21]})
    tmp_resline_data, Tmp_resline = create_model_like(Res_line)
    tmp_extra_data, Tmp_extra = create_model("Tmp_extra", {"art":int, "typ_pos":string, "pos_from":string, "cdate":date, "room":string, "qty":int})
    temp_art_data, Temp_art = create_model("Temp_art", {"art_nr":int, "art_nm":string})

    Zkbuff = create_buffer("Zkbuff",Zimkateg)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal msg_str, room_list_data, sum_list_data, lnldelimeter, ttl_room, occ_room, ooo_room, anz_setup, tot_room, isetup_array, csetup_array, ci_date, datum, week_list, i, j, curr_day, lvcarea, res_line, zimkateg, htparam, zimmer, genstat, zinrstat, kontline, artikel, fixleist, arrangement, reslin_queasy, paramtext, outorder, guest
        nonlocal pvilanguage, printer_nr, call_from, txt_file, curr_date, incl_tentative
        nonlocal zkbuff


        nonlocal rmcat_list, room_list, sum_list, tmp_resline, tmp_extra, temp_art, zikat_list, zkbuff, rlist, rlist
        nonlocal rmcat_list_data, room_list_data, sum_list_data, tmp_resline_data, tmp_extra_data, temp_art_data

        return {"msg_str": msg_str, "room-list": room_list_data, "sum-list": sum_list_data}

    def backdate_create_browse():

        nonlocal msg_str, room_list_data, sum_list_data, lnldelimeter, ttl_room, occ_room, ooo_room, anz_setup, tot_room, isetup_array, csetup_array, ci_date, datum, week_list, i, j, curr_day, lvcarea, res_line, zimkateg, htparam, zimmer, genstat, zinrstat, kontline, artikel, fixleist, arrangement, reslin_queasy, paramtext, outorder, guest
        nonlocal pvilanguage, printer_nr, call_from, txt_file, curr_date, incl_tentative
        nonlocal zkbuff


        nonlocal rmcat_list, room_list, sum_list, tmp_resline, tmp_extra, temp_art, zikat_list, zkbuff, rlist, rlist
        nonlocal rmcat_list_data, room_list_data, sum_list_data, tmp_resline_data, tmp_extra_data, temp_art_data

        datum_browse:date = None
        fdate:date = None
        tdate:date = None
        do_it:bool = False
        m:int = 0
        anz:int = 0
        s:Decimal = to_decimal("0.0")
        tmp_list:List[int] = create_empty_list(21,0)
        Rlist = Room_list
        rlist_data = room_list_data
        room_list_data.clear()
        sum_list_data.clear()

        rmcat_list = query(rmcat_list_data, first=True)

        if rmcat_list:

            zkbuff_obj_list = {}

            # Rd, 21/7/25
            # requery (AI)
            # for zkbuff in db_session.query(Zkbuff).filter(
            #          ((Zkbuff.zikatnr.in_(list(set([rmcat_list.zikatnr for rmcat_list in rmcat_list_data])))))).order_by(Zkbuff.typ, Zkbuff.zikatnr, rmcat_list.nr).all():
            zikatnr_list = list({rmcat.zikatnr for rmcat in rmcat_list_data})

            zkbuff_list = db_session.query(Zkbuff).filter(
                Zkbuff.zikatnr.in_(zikatnr_list)
            ).order_by(
                Zkbuff.typ,
                Zkbuff.zikatnr
            ).all()
            for zkbuff in zkbuff_list:
                if zkbuff_obj_list.get(zkbuff._recid):
                    continue
                else:
                    zkbuff_obj_list[zkbuff._recid] = True

                rmcat_list = query(rmcat_list_data, (lambda rmcat_list: (zkbuff.zikatnr == rmcat_list.zikatnr)), first=True)
                room_list = Room_list()
                room_list_data.append(room_list)

                m = 1
                while m <= 21:
                    room_list.room[m - 1] = rmcat_list.anzahl
                    m = m + 1
                room_list.zikatnr = rmcat_list.zikatnr
                room_list.setup = rmcat_list.nr
                room_list.haupt = rmcat_list.haupt
                room_list.glores = rmcat_list.glores

                if rmcat_list.anzahl > 0:
                    room_list.bezeich = to_string(rmcat_list.kurzbez1, "x(10)") + to_string(rmcat_list.anzahl, ">>>9")
                else:
                    room_list.bezeich = to_string(rmcat_list.kurzbez1, "x(10)")
        datum_browse = curr_date
        for m in range(1,21 + 1) :

            if datum_browse < ci_date:

                if anz_setup > 0:

                    genstat_obj_list = {}
                    genstat = Genstat()
                    zimkateg = Zimkateg()
                    zimmer = Zimmer()
                    for genstat.zikatnr, genstat.resstatus, genstat.resnr, genstat._recid, zimkateg.zikatnr, zimkateg.kurzbez, zimkateg.bezeichnung, zimkateg._recid, zimmer.setup, zimmer.sleeping, zimmer.zikatnr, zimmer.zinr, zimmer._recid in db_session.query(Genstat.zikatnr, Genstat.resstatus, Genstat.resnr, Genstat._recid, Zimkateg.zikatnr, Zimkateg.kurzbez, Zimkateg.bezeichnung, Zimkateg._recid, Zimmer.setup, Zimmer.sleeping, Zimmer.zikatnr, Zimmer.zinr, Zimmer._recid).join(Zimkateg,(Zimkateg.zikatnr == Genstat.zikatnr)).join(Zimmer,(Zimmer.zinr == Genstat.zinr)).filter(
                             (Genstat.datum == datum_browse) & (Genstat.segmentcode != 0) & (Genstat.nationnr != 0) & (Genstat.zinr != "") & (Genstat.res_logic[inc_value(1)]) & (Genstat.resstatus != 13)).order_by(Genstat._recid).all():
                        if genstat_obj_list.get(genstat._recid):
                            continue
                        else:
                            genstat_obj_list[genstat._recid] = True

                        if genstat.resstatus == 3 and not incl_tentative:
                            do_it = False

                        elif genstat.resstatus == 3 and incl_tentative:
                            do_it = True
                        else:
                            do_it = False

                        if do_it:

                            room_list = query(room_list_data, filters=(lambda room_list: room_list.zikatnr == genstat.zikatnr and room_list.setup == zimmer.setup), first=True)
                            room_list.room[m - 1] = room_list.room[m - 1] - 1
                            occ_room[m - 1] = occ_room[m - 1] + 1

                            room_list = query(room_list_data, filters=(lambda room_list: room_list.zikatnr == genstat.zikatnr and room_list.glores), first=True)

                            if not room_list:

                                room_list = query(room_list_data, filters=(lambda room_list: room_list.zikatnr == genstat.zikatnr), first=True)
                            room_list.room[m - 1] = room_list.room[m - 1] + 1
            else:

                if anz_setup > 0:

                    for res_line in db_session.query(Res_line).filter(
                             (Res_line.active_flag <= 1) & (Res_line.resstatus <= 6) & (Res_line.resstatus != 4) & (((Res_line.ankunft <= datum_browse) & (Res_line.abreise > datum_browse)) | ((Res_line.ankunft == datum_browse) & (Res_line.abreise == datum_browse))) & (Res_line.kontignr < 0) & (Res_line.l_zuordnung[inc_value(2)] == 0)).order_by(Res_line._recid).all():
                        do_it = True

                        if res_line.zinr != "":

                            zimmer = get_cache (Zimmer, {"zinr": [(eq, res_line.zinr)]})
                            do_it = zimmer.sleeping

                        if res_line.kontignr < 0:
                            do_it = False

                        if res_line.resstatus == 3 and not incl_tentative:
                            do_it = False

                        if do_it:

                            room_list = query(room_list_data, filters=(lambda room_list: room_list.zikatnr == res_line.zikatnr and room_list.setup == res_line.setup and not room_list.glores), first=True)

                            if not room_list:

                                room_list = query(room_list_data, filters=(lambda room_list: room_list.zikatnr == res_line.zikatnr and room_list.haupt  and not room_list.glores), first=True)

                            if not room_list:

                                room_list = query(room_list_data, filters=(lambda room_list: room_list.zikatnr == res_line.zikatnr and room_list.setup == res_line.setup), first=True)

                            if not room_list:

                                room_list = query(room_list_data, filters=(lambda room_list: room_list.zikatnr == res_line.zikatnr), first=True)

                            if not room_list:
                                msg_str = ("room-list record missing ResNo:") + " " + to_string(res_line.resnr) + ("Bed Setup:") + " " + to_string(res_line.setup)
                            else:
                                room_list.room[m - 1] = room_list.room[m - 1] - res_line.zimmeranz
                                occ_room[m - 1] = occ_room[m - 1] + res_line.zimmeranz


            datum_browse = datum_browse + timedelta(days=1)
        datum_browse = curr_date
        for m in range(1,21 + 1) :

            if datum_browse < ci_date:

                zinrstat_obj_list = {}
                for zinrstat, zimmer in db_session.query(Zinrstat, Zimmer).join(Zimmer,(Zimmer.zinr == Zinrstat.zinr)).filter(
                         (Zinrstat.datum == datum_browse) & (Zinrstat.zinr == ("ooo").lower())).order_by(Zinrstat._recid).all():
                    if zinrstat_obj_list.get(zinrstat._recid):
                        continue
                    else:
                        zinrstat_obj_list[zinrstat._recid] = True

                    room_list = query(room_list_data, filters=(lambda room_list: room_list.zikatnr == zimmer.zikatnr and room_list.setup == zimmer.setup and room_list.glores == False), first=True)

                    if not room_list:

                        room_list = query(room_list_data, filters=(lambda room_list: room_list.zikatnr == zimmer.zikatnr and room_list.setup == zimmer.setup), first=True)

                    if not room_list:

                        room_list = query(room_list_data, filters=(lambda room_list: room_list.zikatnr == zimmer.zikatnr), first=True)

                    if not room_list:
                        msg_str = ("room-list record missing for OOO RoomNo:") + " " + zimmer.zinr + ("Bed Setup:") + " " + to_string(zimmer.setup)
                    else:
                        for m in range(1,21 + 1) :
                            room_list.room[m - 1] = room_list.room[m - 1] - 1
                            ooo_room[m - 1] = ooo_room[m - 1] + 1


            datum_browse = datum_browse + timedelta(days=1)
        datum_browse = curr_date
        for m in range(1,21 + 1) :

            for kontline in db_session.query(Kontline).filter(
                     (Kontline.kontignr > 0) & (Kontline.betriebsnr == 1) & (Kontline.ankunft <= datum_browse) & (Kontline.abreise >= datum_browse) & (Kontline.kontstatus == 1)).order_by(Kontline._recid).all():

                if anz_setup > 0:

                    room_list = query(room_list_data, filters=(lambda room_list: room_list.zikatnr == kontline.zikatnr and room_list.glores), first=True)
                else:

                    room_list = query(room_list_data, filters=(lambda room_list: room_list.zikatnr == kontline.zikatnr), first=True)
                
                # Rd, 21/7/25
                # add if available
                if room_list:
                    room_list.room[m - 1] = room_list.room[m - 1] - kontline.zimmeranz
                occ_room[m - 1] = occ_room[m - 1] + kontline.zimmeranz

            if datum_browse < ci_date:

                genstat_obj_list = {}
                genstat = Genstat()
                zimkateg = Zimkateg()
                zimmer = Zimmer()
                for genstat.zikatnr, genstat.resstatus, genstat.resnr, genstat._recid, zimkateg.zikatnr, zimkateg.kurzbez, zimkateg.bezeichnung, zimkateg._recid, zimmer.setup, zimmer.sleeping, zimmer.zikatnr, zimmer.zinr, zimmer._recid in db_session.query(Genstat.zikatnr, Genstat.resstatus, Genstat.resnr, Genstat._recid, Zimkateg.zikatnr, Zimkateg.kurzbez, Zimkateg.bezeichnung, Zimkateg._recid, Zimmer.setup, Zimmer.sleeping, Zimmer.zikatnr, Zimmer.zinr, Zimmer._recid).join(Zimkateg,(Zimkateg.zikatnr == Genstat.zikatnr)).join(Zimmer,(Zimmer.zinr == Genstat.zinr)).filter(
                         (Genstat.datum == datum_browse) & (Genstat.segmentcode != 0) & (Genstat.nationnr != 0) & (Genstat.zinr != "") & (Genstat.res_logic[inc_value(1)]) & (Genstat.resstatus != 13)).order_by(Genstat._recid).all():
                    if genstat_obj_list.get(genstat._recid):
                        continue
                    else:
                        genstat_obj_list[genstat._recid] = True

                    if genstat.resstatus != 11 and genstat.resstatus != 13:

                        room_list = query(room_list_data, filters=(lambda room_list: room_list.zikatnr == genstat.zikatnr and room_list.setup == zimmer.setup and not room_list.glores), first=True)

                        if not room_list:

                            room_list = query(room_list_data, filters=(lambda room_list: room_list.zikatnr == genstat.zikatnr and room_list.haupt  and not room_list.glores), first=True)

                        if not room_list:

                            room_list = query(room_list_data, filters=(lambda room_list: room_list.zikatnr == genstat.zikatnr and room_list.setup == zimmer.setup), first=True)

                        if not room_list:

                            room_list = query(room_list_data, filters=(lambda room_list: room_list.zikatnr == genstat.zikatnr), first=True)

                        if not room_list:
                            msg_str = ("room-list record missing ResNo:") + " " + to_string(genstat.resnr) + ("Bed Setup:") + " " + to_string(zimmer.setup)
                        else:
                            room_list.room[m - 1] = room_list.room[m - 1] - 1
                            occ_room[m - 1] = occ_room[m - 1] + 1


            else:

                for res_line in db_session.query(Res_line).filter(
                         (Res_line.active_flag <= 1) & (Res_line.resstatus <= 6) & (Res_line.resstatus != 4) & (((Res_line.ankunft <= datum_browse) & (Res_line.abreise > datum_browse)) | ((Res_line.ankunft == datum_browse) & (Res_line.abreise == datum_browse))) & (Res_line.l_zuordnung[inc_value(2)] == 0)).order_by(Res_line._recid).all():
                    do_it = True

                    if res_line.zinr != "":

                        zimmer = get_cache (Zimmer, {"zinr": [(eq, res_line.zinr)]})
                        do_it = zimmer.sleeping

                    if res_line.kontignr < 0:
                        do_it = False

                    if res_line.resstatus == 3 and not incl_tentative:
                        do_it = False

                    if do_it:

                        room_list = query(room_list_data, filters=(lambda room_list: room_list.zikatnr == res_line.zikatnr and room_list.setup == res_line.setup and not room_list.glores), first=True)

                        if not room_list:

                            room_list = query(room_list_data, filters=(lambda room_list: room_list.zikatnr == res_line.zikatnr and room_list.haupt  and not room_list.glores), first=True)

                        if not room_list:

                            room_list = query(room_list_data, filters=(lambda room_list: room_list.zikatnr == res_line.zikatnr and room_list.setup == res_line.setup), first=True)

                        if not room_list:

                            room_list = query(room_list_data, filters=(lambda room_list: room_list.zikatnr == res_line.zikatnr), first=True)

                        if not room_list:
                            msg_str = ("room-list record missing ResNo:") + " " + to_string(res_line.resnr) + ("Bed Setup:") + " " + to_string(res_line.setup)
                        else:
                            room_list.room[m - 1] = room_list.room[m - 1] - res_line.zimmeranz
                            occ_room[m - 1] = occ_room[m - 1] + res_line.zimmeranz


            datum_browse = datum_browse + timedelta(days=1)
        datum_browse = curr_date
        sum_list = Sum_list()
        sum_list_data.append(sum_list)

        sum_list.bezeich = ("TOTAL room")
        for m in range(1,21 + 1) :
            sum_list.summe[m - 1] = to_string(ttl_room[m - 1], "->>>9")
        sum_list = Sum_list()
        sum_list_data.append(sum_list)

        sum_list.bezeich = ("TOTAL OCC")
        for m in range(1,21 + 1) :
            sum_list.summe[m - 1] = to_string(occ_room[m - 1], "->>>9")
        sum_list = Sum_list()
        sum_list_data.append(sum_list)

        sum_list.bezeich = ("TOTAL OOO")
        for m in range(1,21 + 1) :
            sum_list.summe[m - 1] = to_string(ooo_room[m - 1], "->>>9")
        sum_list = Sum_list()
        sum_list_data.append(sum_list)

        sum_list.bezeich = ("AVAILABLE")
        for m in range(1,21 + 1) :
            s =  to_decimal("0")

            for room_list in query(room_list_data):
                s =  to_decimal(s) + to_decimal(room_list.room[m - 1])
            sum_list.summe[m - 1] = to_string(s, "->>>9")
            tmp_list[m - 1] = s
        sum_list = Sum_list()
        sum_list_data.append(sum_list)

        sum_list.bezeich = ("AVAIL in %")
        for m in range(1,21 + 1) :

            if tot_room > 0:
                s =  to_decimal(to_int(tmp_list[m - 1])) / to_decimal(tot_room) * to_decimal("100")

            if s < 0:
                sum_list.summe[m - 1] = to_string(s, "->>9.9")
            else:
                sum_list.summe[m - 1] = to_string(s, ">>9.9")
        sum_list = Sum_list()
        sum_list_data.append(sum_list)

        sum_list.bezeich = ("OCC in %")
        for m in range(1,21 + 1) :

            if ttl_room[m - 1] > 0:
                s =  to_decimal(occ_room[m - 1]) / to_decimal(ttl_room[m - 1]) * to_decimal("100")

            if s < 0:
                sum_list.summe[m - 1] = to_string(s, "->>9.99")
            else:
                sum_list.summe[m - 1] = to_string(s, ">>9.99")
        sum_list = Sum_list()
        sum_list_data.append(sum_list)

        sum_list.bezeich = ("OVERBOOK")
        for m in range(1,21 + 1) :
            anz = 0

            if tmp_list[m - 1] < 0:
                anz = tmp_list[m - 1]

            if anz < 0:
                sum_list.summe[m - 1] = to_string(- anz, "->>>9")
            else:
                sum_list.summe[m - 1] = to_string(0, "->>>9")

        for room_list in query(room_list_data):
            for m in range(1,21 + 1) :
                room_list.coom[m - 1] = to_string(room_list.room[m - 1], " ->>9")


    def create_tmpextra(art_nr:int, typ_pos:string, pos_from:string, cdate:date, room:string, qty:int):

        nonlocal msg_str, room_list_data, sum_list_data, lnldelimeter, ttl_room, occ_room, ooo_room, anz_setup, tot_room, isetup_array, csetup_array, ci_date, datum, week_list, i, j, curr_day, lvcarea, res_line, zimkateg, htparam, zimmer, genstat, zinrstat, kontline, artikel, fixleist, arrangement, reslin_queasy, paramtext, outorder, guest
        nonlocal pvilanguage, printer_nr, call_from, txt_file, curr_date, incl_tentative
        nonlocal zkbuff


        nonlocal rmcat_list, room_list, sum_list, tmp_resline, tmp_extra, temp_art, zikat_list, zkbuff, rlist, rlist
        nonlocal rmcat_list_data, room_list_data, sum_list_data, tmp_resline_data, tmp_extra_data, temp_art_data


        tmp_extra = Tmp_extra()
        tmp_extra_data.append(tmp_extra)

        tmp_extra.art = art_nr
        tmp_extra.typ_pos = typ_pos
        tmp_extra.pos_from = pos_from
        tmp_extra.cdate = cdate
        tmp_extra.room = room
        tmp_extra.qty = qty


    def calc_extra(tmp_fdate:date):

        nonlocal msg_str, room_list_data, sum_list_data, lnldelimeter, ttl_room, occ_room, ooo_room, anz_setup, tot_room, isetup_array, csetup_array, ci_date, datum, week_list, i, j, curr_day, lvcarea, res_line, zimkateg, htparam, zimmer, genstat, zinrstat, kontline, artikel, fixleist, arrangement, reslin_queasy, paramtext, outorder, guest
        nonlocal pvilanguage, printer_nr, call_from, txt_file, curr_date, incl_tentative
        nonlocal zkbuff


        nonlocal rmcat_list, room_list, sum_list, tmp_resline, tmp_extra, temp_art, zikat_list, zkbuff, rlist, rlist
        nonlocal rmcat_list_data, room_list_data, sum_list_data, tmp_resline_data, tmp_extra_data, temp_art_data

        tdate:date = None
        art_nr:int = 0
        int_art:string = ""
        bdate:date = None
        edate:date = None
        eposdate:date = None
        ndate:date = None
        art_qty:int = 0
        art_rem:int = 0
        tot_used:int = 0
        argtnr:int = 0
        tdate = tmp_fdate + timedelta(days=20)
        tmp_resline_data.clear()
        tmp_extra_data.clear()
        temp_art_data.clear()

        for res_line in db_session.query(Res_line).filter(
                 (not_ (Res_line.abreise < tmp_fdate)) & (not_ (Res_line.ankunft > tdate)) & (Res_line.resstatus != 9) & (Res_line.resstatus != 10) & (Res_line.resstatus != 99) & (Res_line.l_zuordnung[inc_value(2)] == 0)).order_by(Res_line.resnr).all():
            tmp_resline = Tmp_resline()
            tmp_resline_data.append(tmp_resline)

            buffer_copy(res_line, tmp_resline)

        htparam = get_cache (Htparam, {"paramgruppe": [(eq, 5)],"paramnr": [(eq, 2999)]})

        if htparam:
            for i in range(1,num_entries(htparam.fchar , ";")  + 1) :
                int_art = entry(i - 1, htparam.fchar, ";")

                if int_art != "":

                    artikel = get_cache (Artikel, {"artnr": [(eq, int (int_art))],"departement": [(eq, 0)]})

                    if artikel:
                        temp_art = Temp_art()
                        temp_art_data.append(temp_art)

                        temp_art.art_nr = int (int_art)
                        temp_art.art_nm = artikel.bezeich


                        art_nr = int (int_art)

                        for tmp_resline in query(tmp_resline_data, sort_by=[("resnr",False)]):

                            for fixleist in db_session.query(Fixleist).filter(
                                     (Fixleist.resnr == tmp_resline.resnr) & (Fixleist.reslinnr == tmp_resline.reslinnr) & (Fixleist.artnr == art_nr) & (Fixleist.departement == 0)).order_by(Fixleist._recid).all():

                                if tmp_resline.ankunft == tmp_resline.abreise:

                                    if fixleist.sequenz == 1 or fixleist.sequenz == 2 or fixleist.sequenz == 6:
                                        create_tmpextra(art_nr, "Fix-cost line", to_string(fixleist.sequenz), tmp_resline.ankunft, tmp_resline.zinr, fixleist.number)

                                    elif fixleist.sequenz == 4:

                                        if get_day(tmp_resline.ankunft) == 1:
                                            create_tmpextra(art_nr, "Fix-cost line", to_string(fixleist.sequenz), tmp_resline.ankunft, tmp_resline.zinr, fixleist.number)

                                    elif fixleist.sequenz == 5:

                                        if get_day(tmp_resline.ankunft + 1) == 1:
                                            create_tmpextra(art_nr, "Fix-cost line", to_string(fixleist.sequenz), tmp_resline.ankunft, tmp_resline.zinr, fixleist.number)
                                else:

                                    if fixleist.sequenz == 1 or fixleist.sequenz == 2 or fixleist.sequenz == 4 or fixleist.sequenz == 5:

                                        if tmp_resline.ankunft < tmp_fdate:
                                            bdate = tmp_fdate
                                        else:
                                            bdate = tmp_resline.ankunft

                                        if tmp_resline.abreise > tdate:
                                            edate = tdate + timedelta(days=1)

                                        elif tmp_resline.abreise <= tdate:
                                            edate = tmp_resline.abreise

                                    if fixleist.sequenz == 1:

                                        if bdate != None and edate != None:
                                            while bdate < edate :
                                                create_tmpextra(art_nr, "Fix-cost line", to_string(fixleist.sequenz), bdate, tmp_resline.zinr, fixleist.number)
                                                bdate = bdate + timedelta(days=1)

                                    elif fixleist.sequenz == 2:
                                        create_tmpextra(art_nr, "Fix-cost line", to_string(fixleist.sequenz), tmp_resline.ankunft, tmp_resline.zinr, fixleist.number)

                                    elif fixleist.sequenz == 4:

                                        if bdate != None and edate != None:
                                            while bdate < edate :

                                                if get_day(bdate) == 1:
                                                    create_tmpextra(art_nr, "Fix-cost line", to_string(fixleist.sequenz), bdate, tmp_resline.zinr, fixleist.number)
                                                bdate = bdate + timedelta(days=1)

                                    elif fixleist.sequenz == 5:

                                        if bdate != None and edate != None:
                                            while bdate < edate :

                                                if get_day(bdate + 1) == 1:
                                                    create_tmpextra(art_nr, "Fix-cost line", to_string(fixleist.sequenz), bdate, tmp_resline.zinr, fixleist.number)
                                                bdate = bdate + timedelta(days=1)

                                    elif fixleist.sequenz == 6:
                                        eposdate = (fixleist.lfakt + timedelta(days=fixleist.dekade))

                                        if fixleist.lfakt < tmp_fdate:
                                            bdate = tmp_fdate
                                        else:
                                            bdate = fixleist.lfakt

                                        if eposdate > tdate:
                                            edate = tdate + timedelta(days=1)

                                        elif eposdate <= tdate:

                                            if eposdate > tmp_resline.abreise:
                                                edate = tmp_resline.abreise

                                            elif eposdate <= tmp_resline.abreise:
                                                edate = eposdate

                                        if bdate != None and edate != None:
                                            while bdate < edate :
                                                create_tmpextra(art_nr, "Fix-cost line", to_string(fixleist.sequenz), bdate, tmp_resline.zinr, fixleist.number)
                                                bdate = bdate + timedelta(days=1)

                            arrangement = get_cache (Arrangement, {"arrangement": [(eq, tmp_resline.arrangement)]})

                            if arrangement:
                                argtnr = arrangement.argtnr

                            for reslin_queasy in db_session.query(Reslin_queasy).filter(
                                     (Reslin_queasy.key == ("fargt-line").lower()) & (Reslin_queasy.resnr == tmp_resline.resnr) & (Reslin_queasy.reslinnr == tmp_resline.reslinnr) & (Reslin_queasy.number1 == 0) & (Reslin_queasy.number3 == art_nr) & (Reslin_queasy.number2 == argtnr)).order_by(Reslin_queasy._recid).all():

                                if reslin_queasy.date1 < tmp_fdate:
                                    bdate = tmp_fdate
                                else:
                                    bdate = reslin_queasy.date1

                                if reslin_queasy.date2 > tdate:
                                    edate = tdate + timedelta(days=1)

                                elif reslin_queasy.date2 <= tdate:
                                    edate = reslin_queasy.date2

                                if bdate != None and tdate != None:
                                    while bdate < edate :
                                        create_tmpextra(art_nr, "argt line", "0", bdate, tmp_resline.zinr, 1)
                                        bdate = bdate + timedelta(days=1)
        ndate = tmp_fdate
        sum_list = Sum_list()
        sum_list_data.append(sum_list)

        sum_list.bezeich = ""


        tot_used = 0

        for temp_art in query(temp_art_data):

            artikel = get_cache (Artikel, {"artnr": [(eq, temp_art.art_nr)],"departement": [(eq, 0)]})

            if artikel:
                art_qty = artikel.anzahl
                sum_list = Sum_list()
                sum_list_data.append(sum_list)

                sum_list.bezeich = temp_art.art_nm
                ndate = tmp_fdate
                for i in range(1,21 + 1) :

                    for tmp_extra in query(tmp_extra_data, filters=(lambda tmp_extra: tmp_extra.art == temp_art.art_nr and tmp_extra.cdate == ndate and tmp_extra.qty != 0)):
                        tot_used = tot_used + tmp_extra.qty
                    art_rem = art_qty - tot_used
                    sum_list.summe[i - 1] = to_string(art_rem, "->>>9")
                    ndate = tmp_fdate + timedelta(days=i)
                    tot_used = 0


    def get_bedsetup():

        nonlocal msg_str, room_list_data, sum_list_data, lnldelimeter, ttl_room, occ_room, ooo_room, anz_setup, tot_room, isetup_array, csetup_array, ci_date, datum, week_list, i, j, curr_day, lvcarea, res_line, zimkateg, htparam, zimmer, genstat, zinrstat, kontline, artikel, fixleist, arrangement, reslin_queasy, paramtext, outorder, guest
        nonlocal pvilanguage, printer_nr, call_from, txt_file, curr_date, incl_tentative
        nonlocal zkbuff


        nonlocal rmcat_list, room_list, sum_list, tmp_resline, tmp_extra, temp_art, zikat_list, zkbuff, rlist, rlist
        nonlocal rmcat_list_data, room_list_data, sum_list_data, tmp_resline_data, tmp_extra_data, temp_art_data

        for paramtext in db_session.query(Paramtext).filter(
                 (Paramtext.txtnr >= 9201) & (Paramtext.txtnr <= 9299)).order_by(Paramtext.txtnr).all():

            if paramtext.notes != "":

                zimmer = get_cache (Zimmer, {"setup": [(eq, (paramtext.txtnr - 9200))]})

                if zimmer:
                    anz_setup = anz_setup + 1
                    csetup_array[anz_setup - 1] = substring(paramtext.notes, 0, 1)
                    isetup_array[anz_setup - 1] = paramtext.txtnr - 9200


    def count_rmcateg():

        nonlocal msg_str, room_list_data, sum_list_data, lnldelimeter, ttl_room, occ_room, ooo_room, anz_setup, tot_room, isetup_array, csetup_array, ci_date, datum, week_list, i, j, curr_day, lvcarea, res_line, zimkateg, htparam, zimmer, genstat, zinrstat, kontline, artikel, fixleist, arrangement, reslin_queasy, paramtext, outorder, guest
        nonlocal pvilanguage, printer_nr, call_from, txt_file, curr_date, incl_tentative
        nonlocal zkbuff


        nonlocal rmcat_list, room_list, sum_list, tmp_resline, tmp_extra, temp_art, zikat_list, zkbuff, rlist, rlist
        nonlocal rmcat_list_data, room_list_data, sum_list_data, tmp_resline_data, tmp_extra_data, temp_art_data

        zikatnr:int = 0
        tot_room = 0

        for zimmer in db_session.query(Zimmer).filter(
                 (Zimmer.sleeping)).order_by(Zimmer._recid).all():

            zikat_list = query(zikat_list_data, filters=(lambda zikat_list: zikat_list.zikatnr == zimmer.zikatnr and zikat_list.selected), first=True)

            if zikat_list:

                zkbuff = get_cache (Zimkateg, {"zikatnr": [(eq, zikat_list.zikatnr)]})

                if zkbuff:

                    rmcat_list = query(rmcat_list_data, filters=(lambda rmcat_list: rmcat_list.zikatnr == zimmer.zikatnr and rmcat_list.nr == zimmer.setup), first=True)

                    if not rmcat_list:

                        zimkateg = get_cache (Zimkateg, {"zikatnr": [(eq, zimmer.zikatnr)]})

                        if zimkateg:
                            rmcat_list = Rmcat_list()
                            rmcat_list_data.append(rmcat_list)

                            rmcat_list.nr = zimmer.setup
                            rmcat_list.zikatnr = zimkateg.zikatnr
                            rmcat_list.kurzbez = zimkateg.kurzbez
                            rmcat_list.kurzbez1 = zimkateg.kurzbez
                            rmcat_list.bezeich = zimkateg.bezeichnung
                    tot_room = tot_room + 1
                    rmcat_list.anzahl = rmcat_list.anzahl + 1


        for i in range(1,21 + 1) :
            ttl_room[i - 1] = tot_room


    def create_browse():

        nonlocal msg_str, room_list_data, sum_list_data, lnldelimeter, ttl_room, occ_room, ooo_room, anz_setup, tot_room, isetup_array, csetup_array, ci_date, datum, week_list, i, j, curr_day, lvcarea, res_line, zimkateg, htparam, zimmer, genstat, zinrstat, kontline, artikel, fixleist, arrangement, reslin_queasy, paramtext, outorder, guest
        nonlocal pvilanguage, printer_nr, call_from, txt_file, curr_date, incl_tentative
        nonlocal zkbuff


        nonlocal rmcat_list, room_list, sum_list, tmp_resline, tmp_extra, temp_art, zikat_list, zkbuff, rlist, rlist
        nonlocal rmcat_list_data, room_list_data, sum_list_data, tmp_resline_data, tmp_extra_data, temp_art_data

        datum_browse:date = None
        fdate:date = None
        tdate:date = None
        do_it:bool = False
        m:int = 0
        anz:int = 0
        s:Decimal = to_decimal("0.0")
        tmp_list:List[int] = create_empty_list(21,0)
        gmember = None
        Rlist = Room_list
        rlist_data = room_list_data
        room_list_data.clear()
        sum_list_data.clear()
        htparam.fdate = curr_date
        tdate = curr_date + timedelta(days=20)

        rmcat_list = query(rmcat_list_data, first=True)

        if rmcat_list:

            for rmcat_list in query(rmcat_list_data):

                zkbuff = get_cache (Zimkateg, {"zikatnr": [(eq, rmcat_list.zikatnr)]})

                if zkbuff:
                    room_list = Room_list()
                    room_list_data.append(room_list)

                    m = 1
                    while m <= 21:
                        room_list.room[m - 1] = rmcat_list.anzahl
                        m = m + 1
                    room_list.zikatnr = rmcat_list.zikatnr
                    room_list.setup = rmcat_list.nr
                    room_list.haupt = rmcat_list.haupt
                    room_list.glores = rmcat_list.glores

                    if rmcat_list.anzahl > 0:
                        room_list.bezeich = to_string(rmcat_list.kurzbez1, "x(10)") + to_string(rmcat_list.anzahl, ">>>9")
                    else:
                        room_list.bezeich = to_string(rmcat_list.kurzbez1, "x(10)")
        datum_browse = curr_date
        m = 1
        while m <= 21:

            for kontline in db_session.query(Kontline).filter(
                     (Kontline.kontignr > 0) & (Kontline.betriebsnr == 1) & (Kontline.ankunft <= datum_browse) & (Kontline.abreise >= datum_browse) & (Kontline.kontstatus == 1)).order_by(Kontline._recid).all():

                if anz_setup > 0:

                    room_list = query(room_list_data, filters=(lambda room_list: room_list.zikatnr == kontline.zikatnr and room_list.glores), first=True)
                else:

                    room_list = query(room_list_data, filters=(lambda room_list: room_list.zikatnr == kontline.zikatnr), first=True)
                room_list.room[m - 1] = room_list.room[m - 1] - kontline.zimmeranz
                occ_room[m - 1] = occ_room[m - 1] + kontline.zimmeranz

            if anz_setup > 0:

                for res_line in db_session.query(Res_line).filter(
                         (Res_line.active_flag <= 1) & (Res_line.resstatus <= 6) & (Res_line.resstatus != 4) & (((Res_line.ankunft <= datum_browse) & (Res_line.abreise > datum_browse)) | ((Res_line.ankunft == datum_browse) & (Res_line.abreise == datum_browse))) & (Res_line.kontignr < 0) & (Res_line.l_zuordnung[inc_value(2)] == 0)).order_by(Res_line._recid).all():
                    do_it = True

                    if res_line.zinr != "":

                        zimmer = get_cache (Zimmer, {"zinr": [(eq, res_line.zinr)]})
                        do_it = zimmer.sleeping

                    if res_line.resstatus == 3 and not incl_tentative:
                        do_it = False

                    if do_it:

                        room_list = query(room_list_data, filters=(lambda room_list: room_list.zikatnr == res_line.zikatnr and room_list.setup == res_line.setup), first=True)
                        room_list.room[m - 1] = room_list.room[m - 1] - res_line.zimmeranz
                        occ_room[m - 1] = occ_room[m - 1] + res_line.zimmeranz

                        rlist = query(rlist_data, filters=(lambda rlist: rlist.zikatnr == res_line.zikatnr and rlist.glores), first=True)

                        if not rlist:

                            rlist = query(rlist_data, filters=(lambda rlist: rlist.zikatnr == res_line.zikatnr), first=True)
                        rlist.room[m - 1] = rlist.room[m - 1] + res_line.zimmeranz
            m = m + 1
            datum_browse = datum_browse + timedelta(days=1)

        outorder_obj_list = {}
        outorder = Outorder()
        zimmer = Zimmer()
        for outorder.gespende, outorder.gespstart, outorder._recid, zimmer.setup, zimmer.sleeping, zimmer.zikatnr, zimmer.zinr, zimmer._recid in db_session.query(Outorder.gespende, Outorder.gespstart, Outorder._recid, Zimmer.setup, Zimmer.sleeping, Zimmer.zikatnr, Zimmer.zinr, Zimmer._recid).join(Zimmer,(Zimmer.zinr == Outorder.zinr) & (Zimmer.sleeping)).filter(
                 (Outorder.betriebsnr <= 1)).order_by(Outorder._recid).all():
            if outorder_obj_list.get(outorder._recid):
                continue
            else:
                outorder_obj_list[outorder._recid] = True

            zimkateg = get_cache (Zimkateg, {"zikatnr": [(eq, zimmer.zikatnr)]})
            datum_browse = curr_date

            room_list = query(room_list_data, filters=(lambda room_list: room_list.zikatnr == zimmer.zikatnr and room_list.setup == zimmer.setup and room_list.glores == False), first=True)

            if not room_list:

                room_list = query(room_list_data, filters=(lambda room_list: room_list.zikatnr == zimmer.zikatnr and room_list.setup == zimmer.setup), first=True)

            if not room_list:

                room_list = query(room_list_data, filters=(lambda room_list: room_list.zikatnr == zimmer.zikatnr), first=True)

            if not room_list:
                msg_str = ("room-list record missing for OOO RoomNo:") + " " + zimmer.zinr + ("Bed Setup:") + " " + to_string(zimmer.setup)
            else:
                for m in range(1,21 + 1) :

                    if outorder.gespstart <= datum_browse and outorder.gespende >= datum_browse:
                        room_list.room[m - 1] = room_list.room[m - 1] - 1
                        ooo_room[m - 1] = ooo_room[m - 1] + 1


                    datum_browse = datum_browse + timedelta(days=1)
        Gmember =  create_buffer("Gmember",Guest)
        datum_browse = curr_date
        for m in range(1,21 + 1) :

            for res_line in db_session.query(Res_line).filter(
                     (Res_line.active_flag <= 1) & (Res_line.resstatus <= 6) & (Res_line.resstatus != 4) & (((Res_line.ankunft <= datum_browse) & (Res_line.abreise > datum_browse)) | ((Res_line.ankunft == datum_browse) & (Res_line.abreise == datum_browse))) & (Res_line.l_zuordnung[inc_value(2)] == 0)).order_by(Res_line._recid).all():
                do_it = True

                if res_line.zinr != "":

                    zimmer = get_cache (Zimmer, {"zinr": [(eq, res_line.zinr)]})
                    do_it = zimmer.sleeping

                if res_line.kontignr < 0:
                    do_it = False

                if res_line.resstatus == 3 and not incl_tentative:
                    do_it = False

                if do_it:

                    room_list = query(room_list_data, filters=(lambda room_list: room_list.zikatnr == res_line.zikatnr and room_list.setup == res_line.setup and not room_list.glores), first=True)

                    if not room_list:

                        room_list = query(room_list_data, filters=(lambda room_list: room_list.zikatnr == res_line.zikatnr and room_list.haupt  and not room_list.glores), first=True)

                    if not room_list:

                        room_list = query(room_list_data, filters=(lambda room_list: room_list.zikatnr == res_line.zikatnr and room_list.setup == res_line.setup), first=True)

                    if not room_list:

                        room_list = query(room_list_data, filters=(lambda room_list: room_list.zikatnr == res_line.zikatnr), first=True)

                    if not room_list:
                        msg_str = ("room-list record missing ResNo:") + " " + to_string(res_line.resnr) + ("Bed Setup:") + " " + to_string(res_line.setup)
                    else:
                        room_list.room[m - 1] = room_list.room[m - 1] - res_line.zimmeranz
                        occ_room[m - 1] = occ_room[m - 1] + res_line.zimmeranz


            datum_browse = datum_browse + timedelta(days=1)
        sum_list = Sum_list()
        sum_list_data.append(sum_list)

        sum_list.bezeich = ("TOTAL room")
        for m in range(1,21 + 1) :
            sum_list.summe[m - 1] = to_string(ttl_room[m - 1], "->>>9")
        sum_list = Sum_list()
        sum_list_data.append(sum_list)

        sum_list.bezeich = ("TOTAL OCC")
        for m in range(1,21 + 1) :
            sum_list.summe[m - 1] = to_string(occ_room[m - 1], "->>>9")
        sum_list = Sum_list()
        sum_list_data.append(sum_list)

        sum_list.bezeich = ("TOTAL OOO")
        for m in range(1,21 + 1) :
            sum_list.summe[m - 1] = to_string(ooo_room[m - 1], "->>>9")
        sum_list = Sum_list()
        sum_list_data.append(sum_list)

        sum_list.bezeich = ("AVAILABLE")
        for m in range(1,21 + 1) :
            s =  to_decimal("0")

            for room_list in query(room_list_data):
                s =  to_decimal(s) + to_decimal(room_list.room[m - 1])
            sum_list.summe[m - 1] = to_string(s, "->>>9")
            tmp_list[m - 1] = s
        sum_list = Sum_list()
        sum_list_data.append(sum_list)

        sum_list.bezeich = ("AVAIL in %")
        for m in range(1,21 + 1) :

            if tot_room > 0:
                s =  to_decimal(to_int(tmp_list[m - 1])) / to_decimal(tot_room) * to_decimal("100")

            if s < 0:
                sum_list.summe[m - 1] = to_string(s, "->>9.9")
            else:
                sum_list.summe[m - 1] = to_string(s, ">>9.9")
        sum_list = Sum_list()
        sum_list_data.append(sum_list)

        sum_list.bezeich = ("OCC in %")
        for m in range(1,21 + 1) :

            if ttl_room[m - 1] > 0:
                s =  to_decimal(occ_room[m - 1]) / to_decimal(ttl_room[m - 1]) * to_decimal("100")

            if s < 0:
                sum_list.summe[m - 1] = to_string(s, "->>9.99")
            else:
                sum_list.summe[m - 1] = to_string(s, ">>9.99")
        sum_list = Sum_list()
        sum_list_data.append(sum_list)

        sum_list.bezeich = ("OVERBOOK")
        for m in range(1,21 + 1) :
            anz = 0

            if tmp_list[m - 1] < 0:
                anz = tmp_list[m - 1]

            if anz < 0:
                sum_list.summe[m - 1] = to_string(- anz, "->>>9")
            else:
                sum_list.summe[m - 1] = to_string(0, "->>>9")

        for room_list in query(room_list_data):
            for m in range(1,21 + 1) :
                room_list.coom[m - 1] = to_string(room_list.room[m - 1], " ->>9")


    def create_rmcat_list():

        nonlocal msg_str, room_list_data, sum_list_data, lnldelimeter, ttl_room, occ_room, ooo_room, anz_setup, tot_room, isetup_array, csetup_array, ci_date, datum, week_list, i, j, curr_day, lvcarea, res_line, zimkateg, htparam, zimmer, genstat, zinrstat, kontline, artikel, fixleist, arrangement, reslin_queasy, paramtext, outorder, guest
        nonlocal pvilanguage, printer_nr, call_from, txt_file, curr_date, incl_tentative
        nonlocal zkbuff


        nonlocal rmcat_list, room_list, sum_list, tmp_resline, tmp_extra, temp_art, zikat_list, zkbuff, rlist, rlist
        nonlocal rmcat_list_data, room_list_data, sum_list_data, tmp_resline_data, tmp_extra_data, temp_art_data

        n:int = 0
        curr_zikat:int = 0
        haupt:bool = False
        datum_rmcat:date = None

        if anz_setup > 0:

            zimkateg_obj_list = {}
            for zimkateg in db_session.query(Zimkateg).filter(
                     (Zimkateg.verfuegbarkeit)).order_by(Zimkateg._recid).all():
                zikat_list = query(zikat_list_data, (lambda zikat_list: zikat_list.zikatnr == zimkateg.zikatnr and zikat_list.selected), first=True)
                if not zikat_list:
                    continue

                if zimkateg_obj_list.get(zimkateg._recid):
                    continue
                else:
                    zimkateg_obj_list[zimkateg._recid] = True


                haupt = True
                for n in range(1,anz_setup + 1) :

                    paramtext = get_cache (Paramtext, {"txtnr": [(eq, (isetup_array[n - 1] + 9200))]})

                    zimmer = get_cache (Zimmer, {"zikatnr": [(eq, zimkateg.zikatnr)],"setup": [(eq, isetup_array[n - 1])]})

                    if zimmer:
                        rmcat_list = Rmcat_list()
                        rmcat_list_data.append(rmcat_list)

                        rmcat_list.zikatnr = zimkateg.zikatnr
                        rmcat_list.kurzbez = zimkateg.kurzbez
                        rmcat_list.kurzbez1 = zimkateg.kurzbez + substring(paramtext.notes, 0, 1)
                        rmcat_list.bezeich = zimkateg.bezeichnung
                        rmcat_list.setup = paramtext.ptexte
                        rmcat_list.nr = isetup_array[n - 1]
                        rmcat_list.haupt = haupt

                        if haupt :
                            haupt = False
        else:

            zimkateg_obj_list = {}
            for zimkateg in db_session.query(Zimkateg).order_by(Zimkateg._recid).all():
                zikat_list = query(zikat_list_data, (lambda zikat_list: zikat_list.zikatnr == zimkateg.zikatnr and zikat_list.selected), first=True)
                if not zikat_list:
                    continue

                if zimkateg_obj_list.get(zimkateg._recid):
                    continue
                else:
                    zimkateg_obj_list[zimkateg._recid] = True


                rmcat_list = Rmcat_list()
                rmcat_list_data.append(rmcat_list)

                rmcat_list.zikatnr = zimkateg.zikatnr
                rmcat_list.kurzbez = zimkateg.kurzbez
                rmcat_list.kurzbez1 = zimkateg.kurzbez
                rmcat_list.bezeich = zimkateg.bezeichnung
                rmcat_list.haupt = True
        datum_rmcat = curr_date

        if anz_setup > 0:
            n = 1
        else:
            n = 99
        while n <= 21:

            for kontline in db_session.query(Kontline).filter(
                     (Kontline.betriebsnr == 1) & (Kontline.ankunft <= datum_rmcat) & (Kontline.abreise >= datum_rmcat) & (Kontline.kontstatus == 1)).order_by(Kontline.zikatnr).all():

                if curr_zikat != kontline.zikatnr:

                    zimkateg = get_cache (Zimkateg, {"zikatnr": [(eq, kontline.zikatnr)]})

                    rmcat_list = query(rmcat_list_data, filters=(lambda rmcat_list: rmcat_list.zikatnr == kontline.zikatnr and rmcat_list.haupt  and rmcat_list.glores), first=True)

                    if not rmcat_list:
                        rmcat_list = Rmcat_list()
                        rmcat_list_data.append(rmcat_list)

                        rmcat_list.zikatnr = kontline.zikatnr
                        rmcat_list.kurzbez = zimkateg.kurzbez
                        rmcat_list.kurzbez1 = zimkateg.kurzbez
                        rmcat_list.bezeich = zimkateg.bezeichnung
                        rmcat_list.haupt = True
                        rmcat_list.glores = True
                        curr_zikat = zimkateg.zikatnr


            datum_rmcat = datum_rmcat + timedelta(days=1)
            n = n + 1


    htparam = get_cache (Htparam, {"paramnr": [(eq, 87)]})
    ci_date = htparam.fdate
    
    for i in range(1,21 + 1) :
        ttl_room[i - 1] = 0
        occ_room[i - 1] = 0
        ooo_room[i - 1] = 0


    get_bedsetup()
    create_rmcat_list()
    count_rmcateg()

    if curr_date < ci_date:
        backdate_create_browse()
    else:
        create_browse()
    calc_extra(curr_date)

    return generate_output()