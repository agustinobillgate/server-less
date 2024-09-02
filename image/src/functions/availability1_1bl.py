from functions.additional_functions import *
import decimal
from datetime import date
from sqlalchemy import func
from models import Res_line, Zimkateg, Htparam, Artikel, Fixleist, Arrangement, Reslin_queasy, Paramtext, Zimmer, Kontline, Outorder, Guest

zikat_list_list, Zikat_list = create_model("Zikat_list", {"selected":bool, "zikatnr":int, "kurzbez":str, "bezeich":str})

def availability1_1bl(pvilanguage:int, printer_nr:int, call_from:int, txt_file:str, curr_date:date, incl_tentative:bool, zikat_list:[Zikat_list]):
    msg_str = ""
    room_list_list = []
    sum_list_list = []
    lnldelimeter:str = ""
    ttl_room:[int] = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    occ_room:[int] = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    ooo_room:[int] = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    anz_setup:int = 0
    tot_room:int = 0
    isetup_array:[int] = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    csetup_array:str = ""
    ci_date:date = None
    datum:date = None
    week_list:[str] = ["", "", "", "", "", "", "", "", "", "", "", "", "", "", ""]
    i:int = 0
    j:int = 0
    curr_day:int = 0
    lvcarea:str = "availability1"
    res_line = zimkateg = htparam = artikel = fixleist = arrangement = reslin_queasy = paramtext = zimmer = kontline = outorder = guest = None

    rmcat_list = room_list = sum_list = tmp_resline = tmp_extra = temp_art = zikat_list = zkbuff = rlist = gmember = None

    rmcat_list_list, Rmcat_list = create_model("Rmcat_list", {"zikatnr":int, "kurzbez":str, "kurzbez1":str, "bezeich":str, "setup":str, "haupt":bool, "anzahl":int, "nr":int, "glores":bool})
    room_list_list, Room_list = create_model("Room_list", {"flag":str, "setup":int, "haupt":bool, "zikatnr":int, "bezeich":str, "room":[decimal, 21], "coom":[str, 21], "glores":bool})
    sum_list_list, Sum_list = create_model("Sum_list", {"bezeich":str, "summe":[str, 21]})
    tmp_resline_list, Tmp_resline = create_model_like(Res_line)
    tmp_extra_list, Tmp_extra = create_model("Tmp_extra", {"art":int, "typ_pos":str, "pos_from":str, "cdate":date, "room":str, "qty":int})
    temp_art_list, Temp_art = create_model("Temp_art", {"art_nr":int, "art_nm":str})

    Zkbuff = Zimkateg
    Rlist = Room_list
    rlist_list = room_list_list

    Gmember = Guest

    db_session = local_storage.db_session

    def generate_output():
        nonlocal msg_str, room_list_list, sum_list_list, lnldelimeter, ttl_room, occ_room, ooo_room, anz_setup, tot_room, isetup_array, csetup_array, ci_date, datum, week_list, i, j, curr_day, lvcarea, res_line, zimkateg, htparam, artikel, fixleist, arrangement, reslin_queasy, paramtext, zimmer, kontline, outorder, guest
        nonlocal zkbuff, rlist, gmember


        nonlocal rmcat_list, room_list, sum_list, tmp_resline, tmp_extra, temp_art, zikat_list, zkbuff, rlist, gmember
        nonlocal rmcat_list_list, room_list_list, sum_list_list, tmp_resline_list, tmp_extra_list, temp_art_list
        global zikat_list_list
        return {"msg_str": msg_str, "room-list": room_list_list, "sum-list": sum_list_list}

    def create_tmpextra(art_nr:int, typ_pos:str, pos_from:str, cdate:date, room:str, qty:int):

        nonlocal msg_str, room_list_list, sum_list_list, lnldelimeter, ttl_room, occ_room, ooo_room, anz_setup, tot_room, isetup_array, csetup_array, ci_date, datum, week_list, i, j, curr_day, lvcarea, res_line, zimkateg, htparam, artikel, fixleist, arrangement, reslin_queasy, paramtext, zimmer, kontline, outorder, guest
        nonlocal zkbuff, rlist, gmember


        nonlocal rmcat_list, room_list, sum_list, tmp_resline, tmp_extra, temp_art, zikat_list, zkbuff, rlist, gmember
        nonlocal rmcat_list_list, room_list_list, sum_list_list, tmp_resline_list, tmp_extra_list, temp_art_list
        global zikat_list_list


        tmp_extra = Tmp_extra()
        tmp_extra_list.append(tmp_extra)

        tmp_extra.art = art_nr
        tmp_extra.typ_pos = typ_pos
        tmp_extra.pos_from = pos_from
        tmp_extra.cdate = cdate
        tmp_extra.room = room
        tmp_extra.qty = qty

    def calc_extra(fdate:date):

        nonlocal msg_str, room_list_list, sum_list_list, lnldelimeter, ttl_room, occ_room, ooo_room, anz_setup, tot_room, isetup_array, csetup_array, ci_date, datum, week_list, i, j, curr_day, lvcarea, res_line, zimkateg, htparam, artikel, fixleist, arrangement, reslin_queasy, paramtext, zimmer, kontline, outorder, guest
        nonlocal zkbuff, rlist, gmember


        nonlocal rmcat_list, room_list, sum_list, tmp_resline, tmp_extra, temp_art, zikat_list, zkbuff, rlist, gmember
        nonlocal rmcat_list_list, room_list_list, sum_list_list, tmp_resline_list, tmp_extra_list, temp_art_list
        global zikat_list_list

        tdate:date = None
        art_nr:int = 0
        int_art:str = ""
        bdate:date = None
        edate:date = None
        eposdate:date = None
        ndate:date = None
        art_qty:int = 0
        art_rem:int = 0
        tot_used:int = 0
        argtnr:int = 0
        tdate = fdate + 20
        tmp_resline_list.clear()
        tmp_extra_list.clear()
        temp_art_list.clear()

        for res_line in db_session.query(Res_line).filter(
                (not (Res_line.abreise < fdate)) &  (not (Res_line.ankunft > tdate)) &  (Res_line.resstatus != 9) &  (Res_line.resstatus != 10) &  (Res_line.resstatus != 99) &  (Res_line.l_zuordnung[2] == 0)).all():
            tmp_resline = Tmp_resline()
            tmp_resline_list.append(tmp_resline)

            buffer_copy(res_line, tmp_resline)

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramgruppe == 5) &  (Htparam.paramnr == 2999)).first()

        if htparam:
            for i in range(1,num_entries(htparam.fchar , ";")  + 1) :
                int_art = entry(i - 1, htparam.fchar, ";")

                if int_art != "":

                    artikel = db_session.query(Artikel).filter(
                            (Artikel.artnr == int (int_art)) &  (Artikel.departement == 0)).first()

                    if artikel:
                        temp_art = Temp_art()
                        temp_art_list.append(temp_art)

                        temp_art.art_nr = int (int_art)
                        temp_art.art_nm = artikel.bezeich


                        art_nr = int (int_art)

                        for tmp_resline in query(tmp_resline_list):

                            for fixleist in db_session.query(Fixleist).filter(
                                    (Fixleist.resnr == tmp_resline.resnr) &  (Fixleist.reslinnr == tmp_resline.reslinnr) &  (Fixleist.artnr == art_nr) &  (Fixleist.departement == 0)).all():

                                if tmp_resline.ankunft == tmp_resline.abreise:

                                    if fixleist.sequenz == 1 or fixleist.sequenz == 2 or fixleist.sequenz == 6:
                                        create_tmpextra(art_nr, "Fix_cost line", to_string(fixleist.sequenz), tmp_resline.ankunft, tmp_resline.zinr, fixleist.number)

                                    elif fixleist.sequenz == 4:

                                        if get_day(tmp_resline.ankunft) == 1:
                                            create_tmpextra(art_nr, "Fix_cost line", to_string(fixleist.sequenz), tmp_resline.ankunft, tmp_resline.zinr, fixleist.number)

                                    elif fixleist.sequenz == 5:

                                        if get_day(tmp_resline.ankunft + 1) == 1:
                                            create_tmpextra(art_nr, "Fix_cost line", to_string(fixleist.sequenz), tmp_resline.ankunft, tmp_resline.zinr, fixleist.number)
                                else:

                                    if fixleist.sequenz == 1 or fixleist.sequenz == 2 or fixleist.sequenz == 4 or fixleist.sequenz == 5:

                                        if tmp_resline.ankunft < fdate:
                                            bdate = fdate
                                        else:
                                            bdate = tmp_resline.ankunft

                                        if tmp_resline.abreise > tdate:
                                            edate = tdate + 1

                                        elif tmp_resline.abreise <= tdate:
                                            edate = tmp_resline.abreise

                                    if fixleist.sequenz == 1:
                                        while bdate < edate :
                                            create_tmpextra(art_nr, "Fix_cost line", to_string(fixleist.sequenz), bdate, tmp_resline.zinr, fixleist.number)
                                            bdate = bdate + 1

                                    elif fixleist.sequenz == 2:
                                        create_tmpextra(art_nr, "Fix_cost line", to_string(fixleist.sequenz), tmp_resline.ankunft, tmp_resline.zinr, fixleist.number)

                                    elif fixleist.sequenz == 4:
                                        while bdate < edate :

                                            if get_day(bdate) == 1:
                                                create_tmpextra(art_nr, "Fix_cost line", to_string(fixleist.sequenz), bdate, tmp_resline.zinr, fixleist.number)
                                            bdate = bdate + 1

                                    elif fixleist.sequenz == 5:
                                        while bdate < edate :

                                            if get_day(bdate + 1) == 1:
                                                create_tmpextra(art_nr, "Fix_cost line", to_string(fixleist.sequenz), bdate, tmp_resline.zinr, fixleist.number)
                                            bdate = bdate + 1

                                    elif fixleist.sequenz == 6:
                                        eposdate = (fixleist.lfakt + fixleist.dekade)

                                        if fixleist.lfakt < fdate:
                                            bdate = fdate
                                        else:
                                            bdate = fixleist.lfakt

                                        if eposdate > tdate:
                                            edate = tdate + 1

                                        elif eposdate <= tdate:

                                            if eposdate > tmp_resline.abreise:
                                                edate = tmp_resline.abreise

                                            elif eposdate <= tmp_resline.abreise:
                                                edate = eposdate
                                        while bdate < edate :
                                            create_tmpextra(art_nr, "Fix_cost line", to_string(fixleist.sequenz), bdate, tmp_resline.zinr, fixleist.number)
                                            bdate = bdate + 1

                            arrangement = db_session.query(Arrangement).filter(
                                    (Arrangement == tmp_resline.arrangement)).first()

                            if arrangement:
                                argtnr = arrangement.argtnr

                            for reslin_queasy in db_session.query(Reslin_queasy).filter(
                                    (func.lower(Reslin_queasy.key) == "fargt_line") &  (Reslin_queasy.resnr == tmp_resline.resnr) &  (Reslin_queasy.reslinnr == tmp_resline.reslinnr) &  (Reslin_queasy.number1 == 0) &  (Reslin_queasy.number3 == art_nr) &  (Reslin_queasy.number2 == argtnr)).all():

                                if reslin_queasy.date1 < fdate:
                                    bdate = fdate
                                else:
                                    bdate = reslin_queasy.date1

                                if reslin_queasy.date2 > tdate:
                                    edate = tdate + 1

                                elif reslin_queasy.date2 <= tdate:
                                    edate = reslin_queasy.date2
                                while bdate < edate :
                                    create_tmpextra(art_nr, "argt line", "0", bdate, tmp_resline.zinr, 1)
                                    bdate = bdate + 1
        ndate = fdate
        sum_list = Sum_list()
        sum_list_list.append(sum_list)

        sum_list.bezeich = ""


        tot_used = 0

        for temp_art in query(temp_art_list):

            artikel = db_session.query(Artikel).filter(
                    (Artikel.artnr == temp_art.art_nr) &  (Artikel.departement == 0)).first()

            if artikel:
                art_qty = artikel.anzahl
                sum_list = Sum_list()
                sum_list_list.append(sum_list)

                sum_list.bezeich = temp_art.art_nm
                ndate = fdate
                for i in range(1,21 + 1) :

                    for tmp_extra in query(tmp_extra_list, filters=(lambda tmp_extra :tmp_extra.art == temp_art.art_nr and tmp_extra.cdate == ndate and tmp_extra.qty != 0)):
                        tot_used = tot_used + tmp_extra.qty
                    art_rem = art_qty - tot_used
                    sum_list.summe[i - 1] = to_string(art_rem, "->>>9")
                    ndate = fdate + i
                    tot_used = 0

    def get_bedsetup():

        nonlocal msg_str, room_list_list, sum_list_list, lnldelimeter, ttl_room, occ_room, ooo_room, anz_setup, tot_room, isetup_array, csetup_array, ci_date, datum, week_list, i, j, curr_day, lvcarea, res_line, zimkateg, htparam, artikel, fixleist, arrangement, reslin_queasy, paramtext, zimmer, kontline, outorder, guest
        nonlocal zkbuff, rlist, gmember


        nonlocal rmcat_list, room_list, sum_list, tmp_resline, tmp_extra, temp_art, zikat_list, zkbuff, rlist, gmember
        nonlocal rmcat_list_list, room_list_list, sum_list_list, tmp_resline_list, tmp_extra_list, temp_art_list
        global zikat_list_list

        for paramtext in db_session.query(Paramtext).filter(
                (Paramtext.txtnr >= 9201) &  (Paramtext.txtnr <= 9299)).all():

            if paramtext.notes != "":

                zimmer = db_session.query(Zimmer).filter(
                        (Zimmer.setup == (paramtext.txtnr - 9200))).first()

                if zimmer:
                    anz_setup = anz_setup + 1
                    csetup_array[anz_setup - 1] = substring(paramtext.notes, 0, 1)
                    isetup_array[anz_setup - 1] = paramtext.txtnr - 9200

    def count_rmcateg():

        nonlocal msg_str, room_list_list, sum_list_list, lnldelimeter, ttl_room, occ_room, ooo_room, anz_setup, tot_room, isetup_array, csetup_array, ci_date, datum, week_list, i, j, curr_day, lvcarea, res_line, zimkateg, htparam, artikel, fixleist, arrangement, reslin_queasy, paramtext, zimmer, kontline, outorder, guest
        nonlocal zkbuff, rlist, gmember


        nonlocal rmcat_list, room_list, sum_list, tmp_resline, tmp_extra, temp_art, zikat_list, zkbuff, rlist, gmember
        nonlocal rmcat_list_list, room_list_list, sum_list_list, tmp_resline_list, tmp_extra_list, temp_art_list
        global zikat_list_list

        zikatnr:int = 0
        tot_room = 0

        zimmer_obj_list = []
        for zimmer, zikat_list, zkbuff in db_session.query(Zimmer, Zikat_list, Zkbuff).join(Zikat_list,(Zikat_list.zikatnr == Zimmer.zikatnr) &  (Zikat_list.SELECTED)).join(Zkbuff,(Zkbuff.zikatnr == zikat_list.zikatnr)).filter(
                (Zimmer.sleeping)).all():
            if zimmer._recid in zimmer_obj_list:
                continue
            else:
                zimmer_obj_list.append(zimmer._recid)

            rmcat_list = query(rmcat_list_list, filters=(lambda rmcat_list :rmcat_list.zikatnr == zimmer.zikatnr and rmcat_list.nr == zimmer.setup), first=True)

            if not rmcat_list:

                zimkateg = db_session.query(Zimkateg).filter(
                        (Zimkateg.zikatnr == zimmer.zikatnr)).first()
                rmcat_list = Rmcat_list()
                rmcat_list_list.append(rmcat_list)

                rmcat_list.nr = zimmer.setup
                rmcat_list.zikatnr = zimkateg.zikatnr
                rmcat_list.kurzbez = zimkateg.kurzbez
                rmcat_list.kurzbez1 = zimkateg.kurzbez
                rmcat_list.bezeich = zimkateg.bezeich
            tot_room = tot_room + 1
            rmcat_list.anzahl = rmcat_list.anzahl + 1
        for i in range(1,21 + 1) :
            ttl_room[i - 1] = tot_room

    def create_browse():

        nonlocal msg_str, room_list_list, sum_list_list, lnldelimeter, ttl_room, occ_room, ooo_room, anz_setup, tot_room, isetup_array, csetup_array, ci_date, datum, week_list, i, j, curr_day, lvcarea, res_line, zimkateg, htparam, artikel, fixleist, arrangement, reslin_queasy, paramtext, zimmer, kontline, outorder, guest
        nonlocal zkbuff, rlist, gmember


        nonlocal rmcat_list, room_list, sum_list, tmp_resline, tmp_extra, temp_art, zikat_list, zkbuff, rlist, gmember
        nonlocal rmcat_list_list, room_list_list, sum_list_list, tmp_resline_list, tmp_extra_list, temp_art_list
        global zikat_list_list

        datum:date = None
        fdate:date = None
        tdate:date = None
        do_it:bool = False
        i:int = 0
        anz:int = 0
        s:decimal = 0
        tmp_list:[int] = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        Rlist = Room_list
        room_list_list.clear()
        sum_list_list.clear()
        fdate = curr_date
        tdate = curr_date + 20

        for rmcat_list in query(rmcat_list_list):
            zkbuff = db_session.query(Zkbuff).filter((Zkbuff.zikatnr == rmcat_list.zikatnr)).first()
            if not zkbuff:
                continue

            room_list = Room_list()
            room_list_list.append(room_list)

            i = 1
            while i <= 21:
                room_list.room[i - 1] = rmcat_list.anzahl
                i = i + 1
            room_list.zikatnr = rmcat_list.zikatnr
            room_list.setup = rmcat_list.nr
            room_list.haupt = rmcat_list.haupt
            room_list.glores = rmcat_list.glores

            if rmcat_list.anzahl > 0:
                room_list.bezeich = to_string(rmcat_list.kurzbez1, "x(10)") + to_string(rmcat_list.anzahl, ">>>9")
            else:
                room_list.bezeich = to_string(rmcat_list.kurzbez1, "x(10)")
        datum = curr_date
        i = 1
        while i <= 21:

            for kontline in db_session.query(Kontline).filter(
                    (Kontline.kontignr > 0) &  (Kontline.betriebsnr == 1) &  (Kontline.ankunft <= datum) &  (Kontline.abreise >= datum) &  (Kontline.kontstat == 1)).all():

                if anz_setup > 0:

                    room_list = query(room_list_list, filters=(lambda room_list :room_list.zikatnr == kontline.zikatnr and room_list.glores), first=True)
                else:

                    room_list = query(room_list_list, filters=(lambda room_list :room_list.zikatnr == kontline.zikatnr), first=True)
                room_list.room[i - 1] = room_list.room[i - 1] - kontline.zimmeranz
                occ_room[i - 1] = occ_room[i - 1] + kontline.zimmeranz

            if anz_setup > 0:

                for res_line in db_session.query(Res_line).filter(
                        (Res_line.active_flag <= 1) &  (Res_line.resstatus <= 6) &  (Res_line.resstatus != 4) &  (((Res_line.ankunft <= datum) &  (Res_line.abreise > datum)) |  ((Res_line.ankunft == datum) &  (Res_line.abreise == datum))) &  (Res_line.kontignr < 0) &  (Res_line.l_zuordnung[2] == 0)).all():
                    do_it = True

                    if res_line.zinr != "":

                        zimmer = db_session.query(Zimmer).filter(
                                (Zimmer.zinr == res_line.zinr)).first()
                        do_it = zimmer.sleeping

                    if res_line.resstatus == 3 and not incl_tentative:
                        do_it = False

                    if do_it:

                        room_list = query(room_list_list, filters=(lambda room_list :room_list.zikatnr == res_line.zikatnr and room_list.setup == res_line.setup), first=True)
                        room_list.room[i - 1] = room_list.room[i - 1] - res_line.zimmeranz
                        occ_room[i - 1] = occ_room[i - 1] + res_line.zimmeranz

                        rlist = query(rlist_list, filters=(lambda rlist :rlist.zikatnr == res_line.zikatnr and rlist.glores), first=True)

                        if not rlist:

                            rlist = query(rlist_list, filters=(lambda rlist :rlist.zikatnr == res_line.zikatnr), first=True)
                        rlist.room[i - 1] = rlist.room[i - 1] + res_line.zimmeranz

            i = i + 1
            datum = datum + 1

        outorder_obj_list = []
        for outorder, zimmer in db_session.query(Outorder, Zimmer).join(Zimmer,(Zimmer.zinr == Outorder.zinr) &  (Zimmer.sleeping)).filter(
                (Outorder.betriebsnr <= 1)).all():
            if outorder._recid in outorder_obj_list:
                continue
            else:
                outorder_obj_list.append(outorder._recid)

            zimkateg = db_session.query(Zimkateg).filter(
                    (Zimkateg.zikatnr == zimmer.zikatnr)).first()
            datum = curr_date

            room_list = query(room_list_list, filters=(lambda room_list :room_list.zikatnr == zimmer.zikatnr and room_list.setup == zimmer.setup and room_list.glores == False), first=True)

            if not room_list:

                room_list = query(room_list_list, filters=(lambda room_list :room_list.zikatnr == zimmer.zikatnr and room_list.setup == zimmer.setup), first=True)

            if not room_list:

                room_list = query(room_list_list, filters=(lambda room_list :room_list.zikatnr == zimmer.zikatnr), first=True)

            if not room_list:
                msg_str = ("room_list record missing for OOO RoomNo:") + " " + zimmer.zinr + ("Bed Setup:") + " " + to_string(zimmer.setup)
            else:
                for i in range(1,21 + 1) :

                    if outorder.gespstart <= datum and outorder.gespende >= datum:
                        room_list.room[i - 1] = room_list.room[i - 1] - 1
                        ooo_room[i - 1] = ooo_room[i - 1] + 1


                    datum = datum + 1
        Gmember = Guest
        datum = curr_date
        for i in range(1,21 + 1) :

            for res_line in db_session.query(Res_line).filter(
                    (Res_line.active_flag <= 1) &  (Res_line.resstatus <= 6) &  (Res_line.resstatus != 4) &  (((Res_line.ankunft <= datum) &  (Res_line.abreise > datum)) |  ((Res_line.ankunft == datum) &  (Res_line.abreise == datum))) &  (Res_line.l_zuordnung[2] == 0)).all():
                do_it = True

                if res_line.zinr != "":

                    zimmer = db_session.query(Zimmer).filter(
                            (Zimmer.zinr == res_line.zinr)).first()
                    do_it = zimmer.sleeping

                if res_line.kontignr < 0:
                    do_it = False

                if res_line.resstatus == 3 and not incl_tentative:
                    do_it = False

                if do_it:

                    room_list = query(room_list_list, filters=(lambda room_list :room_list.zikatnr == res_line.zikatnr and room_list.setup == res_line.setup and not room_list.glores), first=True)

                    if not room_list:

                        room_list = query(room_list_list, filters=(lambda room_list :room_list.zikatnr == res_line.zikatnr and room_list.haupt  and not room_list.glores), first=True)

                    if not room_list:

                        room_list = query(room_list_list, filters=(lambda room_list :room_list.zikatnr == res_line.zikatnr and room_list.setup == res_line.setup), first=True)

                    if not room_list:

                        room_list = query(room_list_list, filters=(lambda room_list :room_list.zikatnr == res_line.zikatnr), first=True)

                    if not room_list:
                        msg_str = ("room_list record missing ResNo:") + " " + to_string(res_line.resnr) + ("Bed Setup:") + " " + to_string(res_line.setup)
                    else:
                        room_list.room[i - 1] = room_list.room[i - 1] - res_line.zimmeranz
                        occ_room[i - 1] = occ_room[i - 1] + res_line.zimmeranz


            datum = datum + 1
        sum_list = Sum_list()
        sum_list_list.append(sum_list)

        sum_list.bezeich = ("TOTAL room")
        for i in range(1,21 + 1) :
            sum_list.summe[i - 1] = to_string(ttl_room[i - 1], "->>>9")
        sum_list = Sum_list()
        sum_list_list.append(sum_list)

        sum_list.bezeich = ("TOTAL OCC")
        for i in range(1,21 + 1) :
            sum_list.summe[i - 1] = to_string(occ_room[i - 1], "->>>9")
        sum_list = Sum_list()
        sum_list_list.append(sum_list)

        sum_list.bezeich = ("TOTAL OOO")
        for i in range(1,21 + 1) :
            sum_list.summe[i - 1] = to_string(ooo_room[i - 1], "->>>9")
        sum_list = Sum_list()
        sum_list_list.append(sum_list)

        sum_list.bezeich = ("AVAILABLE")
        for i in range(1,21 + 1) :
            s = 0

            for room_list in query(room_list_list):
                s = s + room_list.room[i - 1]
            sum_list.summe[i - 1] = to_string(s, "->>>9")
            tmp_list[i - 1] = s
        sum_list = Sum_list()
        sum_list_list.append(sum_list)

        sum_list.bezeich = ("AVAIL in %")
        for i in range(1,21 + 1) :
            s = to_int(tmp_list[i - 1]) / tot_room * 100

            if s < 0:
                sum_list.summe[i - 1] = to_string(s, "->>9.9")
            else:
                sum_list.summe[i - 1] = to_string(s, ">>9.9")
        sum_list = Sum_list()
        sum_list_list.append(sum_list)

        sum_list.bezeich = ("OCC in %")
        for i in range(1,21 + 1) :
            s = occ_room[i - 1] / ttl_room[i - 1] * 100

            if s < 0:
                sum_list.summe[i - 1] = to_string(s, "->>9.99")
            else:
                sum_list.summe[i - 1] = to_string(s, ">>9.99")
        sum_list = Sum_list()
        sum_list_list.append(sum_list)

        sum_list.bezeich = ("OVERBOOK")
        for i in range(1,21 + 1) :
            anz = 0

            if tmp_list[i - 1] < 0:
                anz = tmp_list[i - 1]

            if anz < 0:
                sum_list.summe[i - 1] = to_string(- anz, "->>>9")
            else:
                sum_list.summe[i - 1] = to_string(0, "->>>9")

        for room_list in query(room_list_list):
            for i in range(1,21 + 1) :
                room_list.coom[i - 1] = to_string(room_list.room[i - 1], " ->>9")

    def create_rmcat_list():

        nonlocal msg_str, room_list_list, sum_list_list, lnldelimeter, ttl_room, occ_room, ooo_room, anz_setup, tot_room, isetup_array, csetup_array, ci_date, datum, week_list, i, j, curr_day, lvcarea, res_line, zimkateg, htparam, artikel, fixleist, arrangement, reslin_queasy, paramtext, zimmer, kontline, outorder, guest
        nonlocal zkbuff, rlist, gmember


        nonlocal rmcat_list, room_list, sum_list, tmp_resline, tmp_extra, temp_art, zikat_list, zkbuff, rlist, gmember
        nonlocal rmcat_list_list, room_list_list, sum_list_list, tmp_resline_list, tmp_extra_list, temp_art_list
        global zikat_list_list

        i:int = 0
        curr_zikat:int = 0
        haupt:bool = False
        datum:date = None

        if anz_setup > 0:

            zimkateg_obj_list = []
            for zimkateg, zikat_list in db_session.query(Zimkateg, Zikat_list).join(Zikat_list,(Zikat_list.zikatnr == Zimkateg.zikatnr) &  (Zikat_list.SELECTED)).filter(
                    (Zimkateg.verfuegbarkeit)).all():
                if zimkateg._recid in zimkateg_obj_list:
                    continue
                else:
                    zimkateg_obj_list.append(zimkateg._recid)


                haupt = True
                for i in range(1,anz_setup + 1) :

                    paramtext = db_session.query(Paramtext).filter(
                            (Paramtext.txtnr == (isetup_array[i - 1] + 9200))).first()

                    zimmer = db_session.query(Zimmer).filter(
                            (Zimmer.zikatnr == zimkateg.zikatnr) &  (Zimmer.setup == isetup_array[i - 1])).first()

                    if zimmer:
                        rmcat_list = Rmcat_list()
                        rmcat_list_list.append(rmcat_list)

                        rmcat_list.zikatnr = zimkateg.zikatnr
                        rmcat_list.kurzbez = zimkateg.kurzbez
                        rmcat_list.kurzbez1 = zimkateg.kurzbez + substring(paramtext.notes, 0, 1)
                        rmcat_list.bezeich = zimkateg.bezeich
                        rmcat_list.setup = paramtext.ptexte
                        rmcat_list.nr = isetup_array[i - 1]
                        rmcat_list.haupt = haupt

                        if haupt :
                            haupt = False
        else:

            zimkateg_obj_list = []
            for zimkateg, zikat_list in db_session.query(Zimkateg, Zikat_list).join(Zikat_list,(Zikat_list.zikatnr == Zimkateg.zikatnr) &  (Zikat_list.SELECTED)).all():
                if zimkateg._recid in zimkateg_obj_list:
                    continue
                else:
                    zimkateg_obj_list.append(zimkateg._recid)


                rmcat_list = Rmcat_list()
                rmcat_list_list.append(rmcat_list)

                rmcat_list.zikatnr = zimkateg.zikatnr
                rmcat_list.kurzbez = zimkateg.kurzbez
                rmcat_list.kurzbez1 = zimkateg.kurzbez
                rmcat_list.bezeich = zimkateg.bezeich
                rmcat_list.haupt = True
        datum = curr_date

        if anz_setup > 0:
            i = 1
        else:
            i = 99
        while i <= 21:

            for kontline in db_session.query(Kontline).filter(
                    (Kontline.betriebsnr == 1) &  (Kontline.ankunft <= datum) &  (Kontline.abreise >= datum) &  (Kontline.kontstat == 1)).all():

                if curr_zikat != kontline.zikatnr:

                    zimkateg = db_session.query(Zimkateg).filter(
                            (Zimkateg.zikatnr == kontline.zikatnr)).first()

                    rmcat_list = query(rmcat_list_list, filters=(lambda rmcat_list :rmcat_list.zikatnr == kontline.zikatnr and rmcat_list.haupt  and rmcat_list.glores), first=True)

                    if not rmcat_list:
                        rmcat_list = Rmcat_list()
                        rmcat_list_list.append(rmcat_list)

                        rmcat_list.zikatnr = kontline.zikatnr
                        rmcat_list.kurzbez = zimkateg.kurzbez
                        rmcat_list.kurzbez1 = zimkateg.kurzbez
                        rmcat_list.bezeich = zimkateg.bezeich
                        rmcat_list.haupt = True
                        rmcat_list.glores = True
                        curr_zikat = zimkateg.zikatnr


            datum = datum + 1
            i = i + 1

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 87)).first()
    ci_date = htparam.fdate
    for i in range(1,21 + 1) :
        ttl_room[i - 1] = 0
        occ_room[i - 1] = 0
        ooo_room[i - 1] = 0


    get_bedsetup()
    create_rmcat_list()
    count_rmcateg()
    create_browse()
    calc_extra(curr_date)

    return generate_output()