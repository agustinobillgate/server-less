#using conversion tools version: 1.0.0.119

# =========================================
# Rulita, 21-11-2025
# Fix missing program endpoint getAvailOOO
# =========================================

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Res_line, Zimkateg, Zimmer, Paramtext, Kontline, Outorder, Guest

def hk_check_availability_ooobl(from_date:date, to_date:date, zinr:string):

    prepare_cache ([Res_line, Zimkateg, Zimmer, Paramtext, Kontline, Outorder])

    notavail_list_data = []
    zikatnr:int = 0
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
    incl_tentative:bool = False
    loopi:int = 0
    loop_datum:date = None
    res_line = zimkateg = zimmer = paramtext = kontline = outorder = guest = None

    rmcat_list = room_list = sum_list = tmp_resline = tmp_extra = temp_art = zikat_list = notavail_list = zkbuff = rlist = None

    rmcat_list_data, Rmcat_list = create_model("Rmcat_list", {"zikatnr":int, "kurzbez":string, "kurzbez1":string, "bezeich":string, "setup":string, "haupt":bool, "anzahl":int, "nr":int, "glores":bool})
    room_list_data, Room_list = create_model("Room_list", {"flag":string, "setup":int, "haupt":bool, "zikatnr":int, "bezeich":string, "room":[Decimal,21], "coom":[string,21], "glores":bool})
    sum_list_data, Sum_list = create_model("Sum_list", {"bezeich":string, "summe":[string,21]})
    tmp_resline_data, Tmp_resline = create_model_like(Res_line)
    tmp_extra_data, Tmp_extra = create_model("Tmp_extra", {"art":int, "typ_pos":string, "pos_from":string, "cdate":date, "room":string, "qty":int})
    temp_art_data, Temp_art = create_model("Temp_art", {"art_nr":int, "art_nm":string})
    zikat_list_data, Zikat_list = create_model("Zikat_list", {"selected":bool, "zikatnr":int, "kurzbez":string, "bezeich":string})
    notavail_list_data, Notavail_list = create_model("Notavail_list", {"datum":date, "rmtype":string, "avail_room":int})

    Zkbuff = create_buffer("Zkbuff",Zimkateg)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal notavail_list_data, zikatnr, lnldelimeter, ttl_room, occ_room, ooo_room, anz_setup, tot_room, isetup_array, csetup_array, ci_date, datum, week_list, i, j, curr_day, incl_tentative, loopi, loop_datum, res_line, zimkateg, zimmer, paramtext, kontline, outorder, guest
        nonlocal from_date, to_date, zinr
        nonlocal zkbuff


        nonlocal rmcat_list, room_list, sum_list, tmp_resline, tmp_extra, temp_art, zikat_list, notavail_list, zkbuff, rlist
        nonlocal rmcat_list_data, room_list_data, sum_list_data, tmp_resline_data, tmp_extra_data, temp_art_data, zikat_list_data, notavail_list_data

        return {"notavail-list": notavail_list_data}

    def get_bedsetup():

        nonlocal notavail_list_data, zikatnr, lnldelimeter, ttl_room, occ_room, ooo_room, anz_setup, tot_room, isetup_array, csetup_array, ci_date, datum, week_list, i, j, curr_day, incl_tentative, loopi, loop_datum, res_line, zimkateg, zimmer, paramtext, kontline, outorder, guest
        nonlocal from_date, to_date, zinr
        nonlocal zkbuff


        nonlocal rmcat_list, room_list, sum_list, tmp_resline, tmp_extra, temp_art, zikat_list, notavail_list, zkbuff, rlist
        nonlocal rmcat_list_data, room_list_data, sum_list_data, tmp_resline_data, tmp_extra_data, temp_art_data, zikat_list_data, notavail_list_data

        for paramtext in db_session.query(Paramtext).filter(
                 (Paramtext.txtnr >= 9201) & (Paramtext.txtnr <= 9299)).order_by(Paramtext.txtnr).all():

            if paramtext.notes != "":

                zimmer = get_cache (Zimmer, {"setup": [(eq, (paramtext.txtnr - 9200))]})

                if zimmer:
                    anz_setup = anz_setup + 1
                    csetup_array[anz_setup - 1] = substring(paramtext.notes, 0, 1)
                    isetup_array[anz_setup - 1] = paramtext.txtnr - 9200


    def create_rmcat_list():

        nonlocal notavail_list_data, zikatnr, lnldelimeter, ttl_room, occ_room, ooo_room, anz_setup, tot_room, isetup_array, csetup_array, ci_date, datum, week_list, i, j, curr_day, incl_tentative, loopi, loop_datum, res_line, zimkateg, zimmer, paramtext, kontline, outorder, guest
        nonlocal from_date, to_date, zinr
        nonlocal zkbuff


        nonlocal rmcat_list, room_list, sum_list, tmp_resline, tmp_extra, temp_art, zikat_list, notavail_list, zkbuff, rlist
        nonlocal rmcat_list_data, room_list_data, sum_list_data, tmp_resline_data, tmp_extra_data, temp_art_data, zikat_list_data, notavail_list_data

        n:int = 0
        curr_zikat:int = 0
        haupt:bool = False
        datum_rmcat:date = None

        if anz_setup > 0:

            for zimkateg in db_session.query(Zimkateg).filter(
                     (Zimkateg.verfuegbarkeit)).order_by(Zimkateg._recid).all():
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

                for zimkateg in db_session.query(Zimkateg).order_by(Zimkateg._recid).all():
                    rmcat_list = Rmcat_list()
                    rmcat_list_data.append(rmcat_list)

                    rmcat_list.zikatnr = zimkateg.zikatnr
                    rmcat_list.kurzbez = zimkateg.kurzbez
                    rmcat_list.kurzbez1 = zimkateg.kurzbez
                    rmcat_list.bezeich = zimkateg.bezeichnung
                    rmcat_list.haupt = True
        for datum_rmcat in date_range(from_date,to_date) :

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


    def count_rmcateg():

        nonlocal notavail_list_data, lnldelimeter, ttl_room, occ_room, ooo_room, anz_setup, tot_room, isetup_array, csetup_array, ci_date, datum, week_list, i, j, curr_day, incl_tentative, loopi, loop_datum, res_line, zimkateg, zimmer, paramtext, kontline, outorder, guest
        nonlocal from_date, to_date, zinr
        nonlocal zkbuff


        nonlocal rmcat_list, room_list, sum_list, tmp_resline, tmp_extra, temp_art, zikat_list, notavail_list, zkbuff, rlist
        nonlocal rmcat_list_data, room_list_data, sum_list_data, tmp_resline_data, tmp_extra_data, temp_art_data, zikat_list_data, notavail_list_data

        zikatnr:int = 0
        tot_room = 0

        for zimmer in db_session.query(Zimmer).filter(
                 (Zimmer.sleeping)).order_by(Zimmer._recid).all():

            zkbuff = get_cache (Zimkateg, {"zikatnr": [(eq, zimmer.zikatnr)]})

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


    def create_browse():

        nonlocal notavail_list_data, zikatnr, lnldelimeter, ttl_room, occ_room, ooo_room, anz_setup, tot_room, isetup_array, csetup_array, ci_date, datum, week_list, i, j, curr_day, incl_tentative, loopi, loop_datum, res_line, zimkateg, zimmer, paramtext, kontline, outorder, guest
        nonlocal from_date, to_date, zinr
        nonlocal zkbuff


        nonlocal rmcat_list, room_list, sum_list, tmp_resline, tmp_extra, temp_art, zikat_list, notavail_list, zkbuff, rlist
        nonlocal rmcat_list_data, room_list_data, sum_list_data, tmp_resline_data, tmp_extra_data, temp_art_data, zikat_list_data, notavail_list_data

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
        fdate = from_date
        tdate = to_date

        rmcat_list = query(rmcat_list_data, filters=(lambda rmcat_list: rmcat_list.zikatnr == zikatnr), first=True)

        if rmcat_list:

            for rmcat_list in query(rmcat_list_data, filters=(lambda rmcat_list: rmcat_list.zikatnr == zikatnr)):

                zkbuff = get_cache (Zimkateg, {"zikatnr": [(eq, rmcat_list.zikatnr)]})

                if zkbuff:
                    room_list = Room_list()
                    room_list_data.append(room_list)

                    m = 1
                    for datum_browse in date_range(fdate,tdate) :
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
        m = 1
        for datum_browse in date_range(fdate,tdate) :

            for kontline in db_session.query(Kontline).filter(
                     (Kontline.kontignr > 0) & (Kontline.betriebsnr == 1) & (Kontline.ankunft <= datum_browse) & (Kontline.abreise >= datum_browse) & (Kontline.kontstatus == 1) & (Kontline.zikatnr == zikatnr)).order_by(Kontline._recid).all():

                if anz_setup > 0:

                    room_list = query(room_list_data, filters=(lambda room_list: room_list.zikatnr == kontline.zikatnr and room_list.glores), first=True)
                else:

                    room_list = query(room_list_data, filters=(lambda room_list: room_list.zikatnr == kontline.zikatnr), first=True)
                room_list.room[m - 1] = room_list.room[m - 1] - kontline.zimmeranz
                occ_room[m - 1] = occ_room[m - 1] + kontline.zimmeranz

            if anz_setup > 0:

                for res_line in db_session.query(Res_line).filter(
                         (Res_line.active_flag <= 1) & (Res_line.resstatus <= 6) & (Res_line.resstatus != 4) & (((Res_line.ankunft <= datum_browse) & (Res_line.abreise > datum_browse)) | ((Res_line.ankunft == datum_browse) & (Res_line.abreise == datum_browse))) & (Res_line.kontignr < 0) & (Res_line.l_zuordnung[inc_value(2)] == 0) & (Res_line.zikatnr == zikatnr)).order_by(Res_line._recid).all():
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

        outorder_obj_list = {}
        outorder = Outorder()
        zimmer = Zimmer()
        for outorder.gespende, outorder.gespstart, outorder._recid, zimmer.zikatnr, zimmer.setup, zimmer.sleeping, zimmer._recid in db_session.query(Outorder.gespende, Outorder.gespstart, Outorder._recid, Zimmer.zikatnr, Zimmer.setup, Zimmer.sleeping, Zimmer._recid).join(Zimmer,(Zimmer.zinr == Outorder.zinr) & (Zimmer.zikatnr == zikatnr) & (Zimmer.sleeping)).filter(
                 (Outorder.betriebsnr <= 1)).order_by(Outorder._recid).all():
            if outorder_obj_list.get(outorder._recid):
                continue
            else:
                outorder_obj_list[outorder._recid] = True

            zimkateg = get_cache (Zimkateg, {"zikatnr": [(eq, zimmer.zikatnr)]})

            room_list = query(room_list_data, filters=(lambda room_list: room_list.zikatnr == zimmer.zikatnr and room_list.setup == zimmer.setup and room_list.glores == False), first=True)

            if not room_list:

                room_list = query(room_list_data, filters=(lambda room_list: room_list.zikatnr == zimmer.zikatnr and room_list.setup == zimmer.setup), first=True)

            if not room_list:

                room_list = query(room_list_data, filters=(lambda room_list: room_list.zikatnr == zimmer.zikatnr), first=True)
            m = 1


            for datum_browse in date_range(fdate,tdate) :

                if outorder.gespstart <= datum_browse and outorder.gespende >= datum_browse:
                    room_list.room[m - 1] = room_list.room[m - 1] - 1
                    ooo_room[m - 1] = ooo_room[m - 1] + 1
                    m = m + 1


        Gmember =  create_buffer("Gmember",Guest)
        m = 1


        for datum_browse in date_range(fdate,tdate) :

            for res_line in db_session.query(Res_line).filter(
                     (Res_line.active_flag <= 1) & (Res_line.resstatus <= 6) & (Res_line.resstatus != 4) & (((Res_line.ankunft <= datum_browse) & (Res_line.abreise > datum_browse)) | ((Res_line.ankunft == datum_browse) & (Res_line.abreise == datum_browse))) & (Res_line.l_zuordnung[inc_value(2)] == 0) & (Res_line.zikatnr == zikatnr)).order_by(Res_line._recid).all():
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
                    room_list.room[m - 1] = room_list.room[m - 1] - res_line.zimmeranz
                    occ_room[m - 1] = occ_room[m - 1] + res_line.zimmeranz


            m = m + 1

    zimmer = get_cache (Zimmer, {"zinr": [(eq, zinr)]})

    if zimmer:
        zikatnr = zimmer.zikatnr


    get_bedsetup()
    create_rmcat_list()
    count_rmcateg()
    create_browse()

    for room_list in query(room_list_data):
        loopi = 1


        for loop_datum in date_range(from_date,to_date) :

            if room_list.room[loopi - 1] == 0:
                notavail_list = Notavail_list()
                notavail_list_data.append(notavail_list)

                notavail_list.datum = loop_datum
                notavail_list.rmtype = room_list.bezeich
                notavail_list.avail_room = room_list.room[loopi - 1]


            loopi = loopi + 1

    for notavail_list in query(notavail_list_data):
        pass

    return generate_output()