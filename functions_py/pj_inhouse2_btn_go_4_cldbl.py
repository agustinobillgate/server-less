#using conversion tools version: 1.0.0.117
#------------------------------------------
# Rd, 22/8/2025
# beda sorting
# sorttype = 1 -> room, function query() merubah sort order,
# gmember.nation1 blm termasuk dalam for db_session, di tambahkan manual.
#------------------------------------------
from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Queasy, Htparam, Zkstat, Zinrstat, Paramtext, Guest, Reservation, Zimmer, Zimkateg, Res_line, Guestseg, Segment, Mc_guest, Mc_types, Nation, Waehrung, Reslin_queasy, Mealcoup, Genstat

def pj_inhouse2_btn_go_4_cldbl(sorttype:int, datum:date, curr_date:date, curr_gastnr:int, froom:string, troom:string, exc_depart:bool, incl_gcomment:bool, incl_rsvcomment:bool, prog_name:string, disp_accompany:bool, disp_exclinact:bool, split_rsv_print:bool, exc_compli:bool):

    prepare_cache ([Htparam, Zkstat, Zinrstat, Paramtext, Guest, Reservation, Zimmer, Zimkateg, Res_line, Guestseg, Segment, Mc_guest, Mc_types, Nation, Waehrung, Reslin_queasy, Mealcoup, Genstat])

    tot_payrm = 0
    tot_rm = 0
    tot_a = 0
    tot_c = 0
    tot_co = 0
    tot_avail = 0
    tot_rmqty = 0
    inactive = 0
    cl_list_data = []
    s_list_data = []
    t_buff_queasy_data = []
    vipnr1:int = 999999999
    vipnr2:int = 999999999
    vipnr3:int = 999999999
    vipnr4:int = 999999999
    vipnr5:int = 999999999
    vipnr6:int = 999999999
    vipnr7:int = 999999999
    vipnr8:int = 999999999
    vipnr9:int = 999999999
    tot_room:int = 0
    all_room:int = 0
    all_remark:string = ""
    queasy = htparam = zkstat = zinrstat = paramtext = guest = reservation = zimmer = zimkateg = res_line = guestseg = segment = mc_guest = mc_types = nation = waehrung = reslin_queasy = mealcoup = genstat = None

    setup_list = str_list = cl_list = s_list = zinr_list = t_buff_queasy = None

    setup_list_data, Setup_list = create_model("Setup_list", {"nr":int, "char":string})
    str_list_data, Str_list = create_model("Str_list", {"flag":int, "rflag":bool, "line1":string, "line2":string, "line3":string, "company":string}, {"rflag": True})
    cl_list_data, Cl_list = create_model("Cl_list", {"flag":int, "karteityp":int, "nr":int, "vip":string, "resnr":int, "name":string, "groupname":string, "rmno":string, "qty":int, "arrive":date, "depart":date, "rmcat":string, "ratecode":string, "zipreis":Decimal, "kurzbez":string, "bezeich":string, "a":int, "c":int, "co":int, "pax":string, "nat":string, "nation":string, "argt":string, "company":string, "flight":string, "etd":string, "paym":int, "segm":string, "telefon":string, "mobil_tel":string, "created":date, "createid":string, "bemerk":string, "bemerk01":string, "bemerk02":string, "bemerk03":string, "bemerk04":string, "bemerk05":string, "bemerk06":string, "bemerk07":string, "bemerk08":string, "bemerk1":string, "ci_time":string, "curr":string, "spreq":string, "tot_bfast":int, "local_reg":string, "rsv_comment":string, "other_comment":string, "g_comment":string, "zinr_bez":string, "flag_guest":int, "etage":int, "birthdate":date})
    s_list_data, S_list = create_model("S_list", {"rmcat":string, "bezeich":string, "nat":string, "anz":int, "adult":int, "proz":Decimal, "child":int, "rmqty":int})
    zinr_list_data, Zinr_list = create_model("Zinr_list", {"resnr":int, "reslinnr":int, "zinr":string})
    t_buff_queasy_data, T_buff_queasy = create_model_like(Queasy)

    db_session = local_storage.db_session

    def generate_output():
        nonlocal tot_payrm, tot_rm, tot_a, tot_c, tot_co, tot_avail, tot_rmqty, inactive, cl_list_data, s_list_data, t_buff_queasy_data, vipnr1, vipnr2, vipnr3, vipnr4, vipnr5, vipnr6, vipnr7, vipnr8, vipnr9, tot_room, all_room, all_remark, queasy, htparam, zkstat, zinrstat, paramtext, guest, reservation, zimmer, zimkateg, res_line, guestseg, segment, mc_guest, mc_types, nation, waehrung, reslin_queasy, mealcoup, genstat
        nonlocal sorttype, datum, curr_date, curr_gastnr, froom, troom, exc_depart, incl_gcomment, incl_rsvcomment, prog_name, disp_accompany, disp_exclinact, split_rsv_print, exc_compli


        nonlocal setup_list, str_list, cl_list, s_list, zinr_list, t_buff_queasy
        nonlocal setup_list_data, str_list_data, cl_list_data, s_list_data, zinr_list_data, t_buff_queasy_data
        # for cl in cl_list_data:
        #     print(cl.rmno)

        return {"tot_payrm": tot_payrm, "tot_rm": tot_rm, "tot_a": tot_a, "tot_c": tot_c, "tot_co": tot_co, "tot_avail": tot_avail, "tot_rmqty": tot_rmqty, "inactive": inactive, "cl-list": cl_list_data, "s-list": s_list_data, "t-buff-queasy": t_buff_queasy_data}

    def bed_setup():

        nonlocal tot_payrm, tot_rm, tot_a, tot_c, tot_co, tot_avail, tot_rmqty, inactive, cl_list_data, s_list_data, t_buff_queasy_data, vipnr1, vipnr2, vipnr3, vipnr4, vipnr5, vipnr6, vipnr7, vipnr8, vipnr9, tot_room, all_room, all_remark, queasy, htparam, zkstat, zinrstat, paramtext, guest, reservation, zimmer, zimkateg, res_line, guestseg, segment, mc_guest, mc_types, nation, waehrung, reslin_queasy, mealcoup, genstat
        nonlocal sorttype, datum, curr_date, curr_gastnr, froom, troom, exc_depart, incl_gcomment, incl_rsvcomment, prog_name, disp_accompany, disp_exclinact, split_rsv_print, exc_compli

        nonlocal setup_list, str_list, cl_list, s_list, zinr_list, t_buff_queasy
        nonlocal setup_list_data, str_list_data, cl_list_data, s_list_data, zinr_list_data, t_buff_queasy_data

        setup_list = Setup_list()
        setup_list_data.append(setup_list)

        setup_list.nr = 1
        setup_list.char = " "

        for paramtext in db_session.query(Paramtext).filter(
                 (Paramtext.txtnr >= 9201) & (Paramtext.txtnr <= 9299)).order_by(Paramtext._recid).all():
            setup_list = Setup_list()
            setup_list_data.append(setup_list)

            setup_list.nr = paramtext.txtnr - 9199
            setup_list.char = substring(paramtext.notes, 0, 1)


    def create_inhouse():

        nonlocal tot_payrm, tot_rm, tot_a, tot_c, tot_co, tot_avail, tot_rmqty, inactive, cl_list_data, s_list_data, t_buff_queasy_data, vipnr1, vipnr2, vipnr3, vipnr4, vipnr5, vipnr6, vipnr7, vipnr8, vipnr9, tot_room, all_room, all_remark, queasy, htparam, zkstat, zinrstat, paramtext, guest, reservation, zimmer, zimkateg, res_line, guestseg, segment, mc_guest, mc_types, nation, waehrung, reslin_queasy, mealcoup, genstat
        nonlocal sorttype, datum, curr_date, curr_gastnr, froom, troom, exc_depart, incl_gcomment, incl_rsvcomment, prog_name, disp_accompany, disp_exclinact, split_rsv_print, exc_compli

        nonlocal setup_list, str_list, cl_list, s_list, zinr_list, t_buff_queasy
        nonlocal setup_list_data, str_list_data, cl_list_data, s_list_data, zinr_list_data, t_buff_queasy_data

        i:int = 0
        j:int = 0
        vip_flag:string = ""
        nr:int = 0
        str:string = ""
        actflag1:int = 0
        actflag2:int = 0
        do_it:bool = False
        gmember = None
        gbuff = None
        rbuff = None
        Gmember =  create_buffer("Gmember",Guest)
        Gbuff =  create_buffer("Gbuff",Guest)
        Rbuff =  create_buffer("Rbuff",Reservation)
        zinr_list_data.clear()

        if datum == curr_date:
            actflag1 = 1
            actflag2 = 1
        else:
            actflag1 = 1
            actflag2 = 2
        tot_payrm = 0
        tot_rm = 0
        tot_a = 0
        tot_c = 0
        tot_co = 0
        inactive = 0
        s_list_data.clear()
        cl_list_data.clear()
        str_list_data.clear()
        tot_avail = 0

        for zimmer in db_session.query(Zimmer).filter(
                 (Zimmer.sleeping)).order_by(Zimmer._recid).all():
            tot_avail = tot_avail + 1

        res_line_obj_list = {}
        res_line = Res_line()
        zimkateg = Zimkateg()
        reservation = Reservation()
        guest = Guest()
        gmember = Guest()
        print("Sort by Room.")
        for res_line.setup, res_line.zinr, res_line.resnr, res_line.name, res_line.zipreis, res_line.ankunft, res_line.abreise, res_line.zimmeranz, \
            res_line.erwachs, res_line.kind1, res_line.kind2, res_line.gratis, res_line.arrangement, res_line.flight_nr, res_line.ankzeit, \
            res_line.resstatus, res_line.betriebsnr, res_line.reslinnr, res_line.zimmer_wunsch, res_line.zimmerfix, res_line.gastnrmember, \
            res_line.bemerk, res_line.gastnr, res_line._recid, zimkateg.kurzbez, zimkateg.bezeichnung, zimkateg._recid, reservation.segmentcode, \
            reservation.resdat, reservation.useridanlage, reservation.resnr, reservation._recid, guest.name, guest.vorname1, guest.anrede1, \
            guest.anredefirma, guest.gastnr, guest.karteityp, guest._recid, gmember.name, gmember.vorname1, gmember.anrede1, gmember.anredefirma, \
            gmember.gastnr, gmember.karteityp, gmember._recid, gmember.nation1, \
            gmember.nation2, \
            gmember.email_adr, gmember.geburtdatum1, gmember.telefon, gmember.mobil_telefon \
            in db_session.query(Res_line.setup, Res_line.zinr, Res_line.resnr, Res_line.name, Res_line.zipreis, Res_line.ankunft, Res_line.abreise, 
                                Res_line.zimmeranz, Res_line.erwachs, Res_line.kind1, Res_line.kind2, Res_line.gratis, Res_line.arrangement, Res_line.flight_nr, \
                                Res_line.ankzeit, Res_line.resstatus, Res_line.betriebsnr, Res_line.reslinnr, Res_line.zimmer_wunsch, Res_line.zimmerfix, \
                                Res_line.gastnrmember, Res_line.bemerk, Res_line.gastnr, Res_line._recid, Zimkateg.kurzbez, Zimkateg.bezeichnung, \
                                Zimkateg._recid, Reservation.segmentcode, Reservation.resdat, Reservation.useridanlage, Reservation.resnr, \
                                Reservation._recid, Guest.name, Guest.vorname1, Guest.anrede1, Guest.anredefirma, Guest.gastnr, Guest.karteityp, \
                                Guest._recid, Gmember.name, Gmember.vorname1, Gmember.anrede1, Gmember.anredefirma, Gmember.gastnr, Gmember.karteityp, \
                                Gmember._recid, Gmember.nation1, Gmember.nation2, Gmember.email_adr, Gmember.geburtdatum1, Gmember.telefon, Gmember.mobil_telefon).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).join(Reservation,(Reservation.resnr == Res_line.resnr) \
                        ).join(Guest,(Guest.gastnr == Reservation.gastnr)).join(Gmember,(Gmember.gastnr == Res_line.gastnrmember)).filter(
                                (Res_line.active_flag >= actflag1) & 
                                (Res_line.active_flag <= actflag2) & 
                                (Res_line.resstatus != 9) & 
                                (Res_line.resstatus != 10) & 
                                (Res_line.resstatus != 12) & 
                                (Res_line.ankunft <= datum) & 
                                (Res_line.abreise >= datum) & 
                                (Res_line.zinr >= (froom).lower()) & 
                                (Res_line.zinr <= (troom).lower()) \
                        # ).order_by(Res_line.zinr).all():
                        ).order_by(Res_line.zinr, Res_line.erwachs.desc(), Res_line.name).all():
            if res_line_obj_list.get(res_line._recid):
                continue
            else:
                res_line_obj_list[res_line._recid] = True
            # print(res_line.zinr)
            if exc_depart and res_line.abreise == datum:
                pass
            else:

                setup_list = query(setup_list_data, filters=(lambda setup_list: setup_list.nr == res_line.setup + 1), first=True)

                zimmer = get_cache (Zimmer, {"zinr": [(eq, res_line.zinr)]})
                nr = nr + 1
                vip_flag = ""

                guestseg = db_session.query(Guestseg).filter(
                         (Guestseg.gastnr == gmember.gastnr) & ((Guestseg.segmentcode == vipnr1) | (Guestseg.segmentcode == vipnr2) | (Guestseg.segmentcode == vipnr3) | (Guestseg.segmentcode == vipnr4) | (Guestseg.segmentcode == vipnr5) | (Guestseg.segmentcode == vipnr6) | (Guestseg.segmentcode == vipnr7) | (Guestseg.segmentcode == vipnr8) | (Guestseg.segmentcode == vipnr9))).first()

                if guestseg:

                    segment = get_cache (Segment, {"segmentcode": [(eq, guestseg.segmentcode)]})
                    vip_flag = segment.bezeich


                cl_list = Cl_list()
                cl_list_data.append(cl_list)

                cl_list.nr = nr
                cl_list.rmcat = zimkateg.kurzbez + setup_list.char
                cl_list.kurzbez = zimkateg.kurzbez
                cl_list.bezeich = zimkateg.bezeichnung
                cl_list.nat = gmember.nation1
                # print("CNat:", cl_list.nat)
                cl_list.resnr = res_line.resnr
                cl_list.vip = vip_flag
                cl_list.name = res_line.name
                cl_list.rmno = res_line.zinr
                cl_list.zipreis =  to_decimal(res_line.zipreis)
                cl_list.arrive = res_line.ankunft
                cl_list.depart = res_line.abreise
                cl_list.qty = res_line.zimmeranz
                cl_list.a = res_line.erwachs
                cl_list.c = res_line.kind1 + res_line.kind2
                cl_list.co = res_line.gratis
                cl_list.argt = res_line.arrangement
                cl_list.flight = substring(res_line.flight_nr, 11, 6)
                cl_list.etd = substring(res_line.flight_nr, 17, 5)
                cl_list.ci_time = to_string(res_line.ankzeit, "HH:MM")
                cl_list.paym = reservation.segmentcode
                cl_list.created = reservation.resdat
                cl_list.createid = reservation.useridanlage
                cl_list.etage = zimmer.etage
                cl_list.zinr_bez = zimmer.bezeich
                cl_list.birthdate = gmember.geburtdatum1
                cl_list.telefon = gmember.telefon
                cl_list.mobil_tel = gmember.mobil_telefon

                if res_line.resstatus != 11 and res_line.resstatus != 13:
                    cl_list.flag_guest = 1


                else:
                    cl_list.flag_guest = 2

                mc_guest = get_cache (Mc_guest, {"gastnr": [(eq, gmember.gastnr)]})

                if mc_guest:
                    cl_list.telefon = gmember.telefon + ";" + mc_guest.cardnum

                    mc_types = get_cache (Mc_types, {"nr": [(eq, mc_guest.nr)]})

                    if mc_types:
                        cl_list.mobil_tel = gmember.mobil_telefon + ";" + mc_types.bezeich
                    else:
                        cl_list.mobil_tel = gmember.mobil_telefon
                else:
                    cl_list.telefon = gmember.telefon

                nation = get_cache (Nation, {"kurzbez": [(eq, gmember.nation2)]})

                if nation:
                    cl_list.local_reg = nation.bezeich

                waehrung = get_cache (Waehrung, {"waehrungsnr": [(eq, res_line.betriebsnr)]})

                if waehrung:
                    cl_list.curr = waehrung.wabkurz + ";" + gmember.email_adr

                reslin_queasy = get_cache (Reslin_queasy, {"key": [(eq, "specialrequest")],"resnr": [(eq, res_line.resnr)],"reslinnr": [(eq, res_line.reslinnr)]})

                if reslin_queasy:
                    cl_list.spreq = reslin_queasy.char3 + "," + cl_list.spreq

                reslin_queasy = get_cache (Reslin_queasy, {"key": [(eq, "arrangement")],"resnr": [(eq, res_line.resnr)],"reslinnr": [(eq, res_line.reslinnr)],"date1": [(le, datum)],"date2": [(ge, datum)]})

                if reslin_queasy:

                    if reslin_queasy.char2 != "":
                        cl_list.ratecode = reslin_queasy.char2
                    else:
                        for i in range(1,num_entries(res_line.zimmer_wunsch, ";") - 1 + 1) :
                            str = entry(i - 1, res_line.zimmer_wunsch, ";")

                            if substring(str, 0, 6) == ("$CODE$").lower() :
                                cl_list.ratecode = substring(str, 6)
                                break

                mealcoup = get_cache (Mealcoup, {"name": [(eq, "breakfast")],"resnr": [(eq, res_line.resnr)],"zinr": [(eq, res_line.zinr)]})

                if mealcoup:
                    cl_list.tot_bfast = mealcoup.verbrauch[0] + mealcoup.verbrauch[1] + mealcoup.verbrauch[2] + mealcoup.verbrauch[3] + mealcoup.verbrauch[4] +\
                            mealcoup.verbrauch[5] + mealcoup.verbrauch[6] + mealcoup.verbrauch[7] + mealcoup.verbrauch[8] + mealcoup.verbrauch[9] +\
                            mealcoup.verbrauch[10] + mealcoup.verbrauch[11] + mealcoup.verbrauch[12] + mealcoup.verbrauch[13] + mealcoup.verbrauch[14] +\
                            mealcoup.verbrauch[15] + mealcoup.verbrauch[16] + mealcoup.verbrauch[17] + mealcoup.verbrauch[18] + mealcoup.verbrauch[19] +\
                            mealcoup.verbrauch[20] + mealcoup.verbrauch[21] + mealcoup.verbrauch[22] + mealcoup.verbrauch[23] + mealcoup.verbrauch[24] +\
                            mealcoup.verbrauch[25] + mealcoup.verbrauch[26] + mealcoup.verbrauch[27] + mealcoup.verbrauch[28] + mealcoup.verbrauch[29] +\
                            mealcoup.verbrauch[30] + mealcoup.verbrauch[31]

                segment = get_cache (Segment, {"segmentcode": [(eq, reservation.segmentcode)]})

                if segment:
                    cl_list.segm = entry(0, segment.bezeich, "$$0")

                if guest.karteityp != 0:
                    cl_list.company = guest.name + ", " + guest.vorname1 + " " + guest.anrede1 + guest.anredefirma
                else:
                    cl_list.company = guest.name + ", " + guest.vorname1 + " " + guest.anrede1 + guest.anredefirma

                if cl_list.nat == "":
                    cl_list.nat = "?"

                if res_line.resstatus == 13 or res_line.zimmerfix:
                    cl_list.qty = 0

                if not split_rsv_print:

                    if incl_gcomment:

                        gbuff = get_cache (Guest, {"gastnr": [(eq, res_line.gastnrmember)]})

                        if gbuff:
                            for i in range(1,length(gbuff.bemerkung)  + 1) :

                                if substring(gbuff.bemerkung, i - 1, 1) == chr_unicode(10):
                                    cl_list.bemerk = cl_list.bemerk + " "
                                else:
                                    cl_list.bemerk = cl_list.bemerk + substring(trim(gbuff.bemerkung) , i - 1, 1)
                        cl_list.bemerk = cl_list.bemerk + " || "

                    if incl_rsvcomment:

                        rbuff = get_cache (Reservation, {"resnr": [(eq, reservation.resnr)]})

                        if rbuff:
                            for j in range(1,length(rbuff.bemerk)  + 1) :

                                if substring(rbuff.bemerk, j - 1, 1) == chr_unicode(10):
                                    cl_list.bemerk1 = cl_list.bemerk1 + " "
                                else:
                                    cl_list.bemerk1 = cl_list.bemerk1 + substring(trim(rbuff.bemerk) , j - 1, 1)
                        cl_list.bemerk = cl_list.bemerk + cl_list.bemerk1 + " || "
                    for i in range(1,length(res_line.bemerk)  + 1) :

                        if substring(res_line.bemerk, i - 1, 1) == chr_unicode(10):
                            cl_list.bemerk = cl_list.bemerk + " "
                        else:
                            cl_list.bemerk = cl_list.bemerk + substring(trim(res_line.bemerk) , i - 1, 1)
                    all_remark = res_line.bemerk
                    all_remark = replace_str(all_remark, chr_unicode(10) , " ")
                    all_remark = replace_str(all_remark, chr_unicode(13) , " ")
                    cl_list.bemerk01 = to_string(substring(all_remark, 0, 225))
                    cl_list.bemerk02 = to_string(substring(all_remark, 225, 225))
                    cl_list.bemerk03 = to_string(substring(all_remark, 450, 225))
                    cl_list.bemerk04 = to_string(substring(all_remark, 675, 225))
                else:
                    for i in range(1,length(res_line.bemerk)  + 1) :
                        cl_list.bemerk = cl_list.bemerk + substring(trim(res_line.bemerk) , i - 1, 1)

                    rbuff = get_cache (Reservation, {"resnr": [(eq, reservation.resnr)]})

                    if rbuff:
                        cl_list.rsv_comment = rbuff.bemerk

                    gbuff = get_cache (Guest, {"gastnr": [(eq, res_line.gastnrmember)]})

                    if gbuff:
                        cl_list.g_comment = gbuff.bemerkung

                    queasy = get_cache (Queasy, {"key": [(eq, 267)],"number1": [(eq, res_line.resnr)],"number2": [(eq, res_line.reslinnr)]})

                    if queasy:
                        cl_list.other_comment = queasy.char1
                cl_list.pax = to_string(cl_list.a, ">9") + "/" + to_string(cl_list.c, "9") + " " + to_string(cl_list.co, "9")

                if cl_list.nat == "":
                    cl_list.nat = "?"
                else:

                    nation = get_cache (Nation, {"kurzbez": [(eq, cl_list.nat)]})

                    if nation:
                        cl_list.nation = nation.bezeich

                zinr_list = query(zinr_list_data, filters=(lambda zinr_list: zinr_list.zinr == res_line.zinr and zinr_list.resnr == res_line.resnr and zinr_list.reslinnr == res_line.reslinnr), first=True)

                if not zinr_list:
                    zinr_list = Zinr_list()
                    zinr_list_data.append(zinr_list)

                    zinr_list.resnr = res_line.resnr
                    zinr_list.reslinnr = res_line.reslinnr
                    zinr_list.zinr = res_line.zinr

                    queasy = get_cache (Queasy, {"key": [(eq, 14)],"char1": [(eq, res_line.zinr)],"date1": [(le, curr_date)],"date2": [(ge, curr_date)]})

                    if zimmer.sleeping and res_line.resstatus != 13:

                        if not queasy:
                            tot_rm = tot_rm + res_line.zimmeranz
                            tot_rmqty = tot_rmqty + res_line.zimmeranz

                        elif queasy and queasy.number3 != res_line.gastnr:
                            tot_rm = tot_rm + res_line.zimmeranz
                            tot_rmqty = tot_rmqty + res_line.zimmeranz

                    if zimmer.sleeping and (res_line.zipreis > 0 or res_line.zipreis == 0) and res_line.resstatus != 13 and res_line.erwachs > 0:

                        if not queasy:
                            tot_payrm = tot_payrm + res_line.zimmeranz

                        elif queasy and queasy.number3 != res_line.gastnr:
                            tot_payrm = tot_payrm + res_line.zimmeranz

                    elif not zimmer.sleeping:

                        if queasy and queasy.number3 != res_line.gastnr and res_line.zipreis > 0:
                            tot_rm = tot_rm + res_line.zimmeranz
                            tot_rmqty = tot_rmqty + res_line.zimmeranz
                        inactive = inactive + 1
                tot_a = tot_a + res_line.erwachs
                tot_c = tot_c + res_line.kind1 + res_line.kind2
                tot_co = tot_co + res_line.gratis

                if exc_compli:
                    tot_co = 0

            if not disp_accompany:

                cl_list = query(cl_list_data, filters=(lambda cl_list: cl_list.rmno == res_line.zinr and cl_list.resnr == res_line.resnr and cl_list.arrive == res_line.ankunft and cl_list.zipreis == 0 and (cl_list.a + cl_list.c) < 1 and cl_list.co < 1), first=True)

                if cl_list:
                    cl_list_data.remove(cl_list)
                    pass

            if exc_compli:

                cl_list = query(cl_list_data, filters=(lambda cl_list: cl_list.rmno == res_line.zinr and cl_list.resnr == res_line.resnr and cl_list.arrive == res_line.ankunft and cl_list.co > 0), first=True)

                if cl_list:
                    cl_list_data.remove(cl_list)
                    pass
                    tot_rm = tot_rm - 1
     
        # Summary s_list
        for cl_list in query(cl_list_data, sort_by=[("nat",False),("bezeich",False)]):

            s_list = query(s_list_data, filters=(lambda s_list: s_list.rmcat == cl_list.kurzbez), first=True)
            if not s_list:
                s_list = query(s_list_data, filters=(lambda s_list: s_list.rmcat == ""), first=True)
                if s_list:
                    s_list.rmcat = cl_list.kurzbez
                    s_list.bezeich = cl_list.bezeich

            if not s_list:
                s_list = S_list()
                s_list_data.append(s_list)

                s_list.rmcat = cl_list.kurzbez
                s_list.bezeich = cl_list.bezeich
            s_list.anz = s_list.anz + cl_list.qty

            s_list = query(s_list_data, filters=(lambda s_list: s_list.nat == cl_list.nat), first=True)
            if not s_list:
                s_list = query(s_list_data, filters=(lambda s_list: s_list.nat == ""), first=True)

                if s_list:
                    s_list.nat = cl_list.nat

            if not s_list:
                s_list = S_list()
                s_list_data.append(s_list)
                s_list.nat = cl_list.nat

            s_list.adult = s_list.adult + cl_list.a + cl_list.co
            s_list.child = s_list.child + cl_list.c
            s_list.rmqty = s_list.rmqty + cl_list.qty

        if (tot_a + tot_co) != 0:

            for s_list in query(s_list_data, filters=(lambda s_list: s_list.nat != "")):

                nation = get_cache (Nation, {"kurzbez": [(eq, s_list.nat)]})

                if nation:
                    s_list.nat = nation.bezeich
                s_list.proz =  to_decimal(s_list.adult) / to_decimal((tot_a) + to_decimal(tot_co)) * to_decimal("100")

        # sort by rmno -> query diatas merubah sort order.-------------------
        for cl_list in query(cl_list_data, sort_by=[("rmno",False)]):
            pass
        #--------------------------------------------------------------------

    def create_genstat_inhouse():

        nonlocal tot_payrm, tot_rm, tot_a, tot_c, tot_co, tot_avail, tot_rmqty, inactive, cl_list_data, s_list_data, t_buff_queasy_data, vipnr1, vipnr2, vipnr3, vipnr4, vipnr5, vipnr6, vipnr7, vipnr8, vipnr9, tot_room, all_room, all_remark, queasy, htparam, zkstat, zinrstat, paramtext, guest, reservation, zimmer, zimkateg, res_line, guestseg, segment, mc_guest, mc_types, nation, waehrung, reslin_queasy, mealcoup, genstat
        nonlocal sorttype, datum, curr_date, curr_gastnr, froom, troom, exc_depart, incl_gcomment, incl_rsvcomment, prog_name, disp_accompany, disp_exclinact, split_rsv_print, exc_compli


        nonlocal setup_list, str_list, cl_list, s_list, zinr_list, t_buff_queasy
        nonlocal setup_list_data, str_list_data, cl_list_data, s_list_data, zinr_list_data, t_buff_queasy_data

        i:int = 0
        j:int = 0
        vip_flag:string = ""
        nr:int = 0
        str:string = ""
        actflag1:int = 0
        actflag2:int = 0
        do_it:bool = False
        gmember = None
        gbuff = None
        rbuff = None
        z:int = 0
        Gmember =  create_buffer("Gmember",Guest)
        Gbuff =  create_buffer("Gbuff",Guest)
        Rbuff =  create_buffer("Rbuff",Reservation)
        zinr_list_data.clear()

        if datum == curr_date:
            actflag1 = 1
            actflag2 = 1
        else:
            actflag1 = 1
            actflag2 = 2
        tot_payrm = 0
        tot_rm = 0
        tot_a = 0
        tot_c = 0
        tot_co = 0
        inactive = 0
        s_list_data.clear()
        cl_list_data.clear()
        str_list_data.clear()
        tot_avail = 0

        for zkstat in db_session.query(Zkstat).filter(
                 (Zkstat.datum == datum)).order_by(Zkstat._recid).all():
            tot_avail = tot_avail + zkstat.anz100

        genstat_obj_list = {}
        genstat = Genstat()
        zimkateg = Zimkateg()
        reservation = Reservation()
        guest = Guest()
        gmember = Guest()
        for genstat.resstatus, genstat.res_date, genstat.resnr, genstat.res_int, genstat.zinr, genstat.zipreis, genstat.erwachs, genstat.kind1, \
            genstat.kind2, genstat.kind3, genstat.gratis, genstat.argt, genstat.segmentcode, genstat.gastnr, genstat._recid, zimkateg.kurzbez, \
            zimkateg.bezeichnung, zimkateg._recid, reservation.segmentcode, reservation.resdat, reservation.useridanlage, reservation.resnr, \
            reservation._recid, guest.name, guest.vorname1, guest.anrede1, guest.anredefirma, guest.gastnr, guest.karteityp, guest._recid, \
            gmember.name, gmember.vorname1, gmember.anrede1, gmember.anredefirma, gmember.gastnr, gmember.karteityp, \
            gmember._recid, gmember.nation1, gmember.nation2, gmember.email_adr, gmember.geburtdatum1, gmember.telefon, gmember.mobil_telefon \
                in db_session.query(Genstat.resstatus, Genstat.res_date, Genstat.resnr, Genstat.res_int, Genstat.zinr, Genstat.zipreis, Genstat.erwachs, \
                                    Genstat.kind1, Genstat.kind2, Genstat.kind3, Genstat.gratis, Genstat.argt, Genstat.segmentcode, Genstat.gastnr, \
                                    Genstat._recid, Zimkateg.kurzbez, Zimkateg.bezeichnung, Zimkateg._recid, Reservation.segmentcode, Reservation.resdat, \
                                    Reservation.useridanlage, Reservation.resnr, Reservation._recid, Guest.name, Guest.vorname1, Guest.anrede1, \
                                    Guest.anredefirma, Guest.gastnr, Guest.karteityp, Guest._recid, Gmember.name, Gmember.vorname1, Gmember.anrede1, \
                                    Gmember.anredefirma, Gmember.gastnr, Gmember.karteityp, Gmember._recid, \
                                    Gmember.nation1, Gmember.nation2, Gmember.email_adr, Gmember.geburtdatum1, Gmember.telefon, Gmember.mobil_telefon)\
                .join(Zimkateg,(Zimkateg.zikatnr == Genstat.zikatnr))\
                .join(Reservation,(Reservation.resnr == Genstat.resnr))\
                .join(Guest,(Guest.gastnr == Genstat.gastnr))\
                .join(Gmember,(Gmember.gastnr == Genstat.gastnrmember))\
                .filter(
                    (Genstat.datum == datum) & 
                    (Genstat.zinr >= (froom).lower()) & 
                    (Genstat.zinr <= (troom).lower()) &
                    (Genstat.datum == datum) & 
                    (Genstat.zinr >= (froom).lower()) & 
                    (Genstat.zinr <= (troom).lower())
                    ) \
                .order_by(Genstat.zinr, Genstat.erwachs.desc(), Gmember.name).all():
        
            if genstat_obj_list.get(genstat._recid):
                continue
            else:
                genstat_obj_list[genstat._recid] = True

            if genstat.res_date[0] < datum and genstat.res_date[1] == datum and genstat.resstatus == 8:
                pass

            elif exc_depart and genstat.res_date[0] <= datum and genstat.res_date[1] == datum and genstat.resstatus == 8:
                pass
            else:

                res_line = get_cache (Res_line, {"resnr": [(eq, genstat.resnr)],"reslinnr": [(eq, genstat.res_int[0])]})

                setup_list = query(setup_list_data, filters=(lambda setup_list: setup_list.nr == res_line.setup + 1), first=True)

                zimmer = get_cache (Zimmer, {"zinr": [(eq, genstat.zinr)]})
                nr = nr + 1
                vip_flag = ""

                guestseg = db_session.query(Guestseg).filter(
                         (Guestseg.gastnr == gmember.gastnr) & ((Guestseg.segmentcode == vipnr1) | (Guestseg.segmentcode == vipnr2) | (Guestseg.segmentcode == vipnr3) | (Guestseg.segmentcode == vipnr4) | (Guestseg.segmentcode == vipnr5) | (Guestseg.segmentcode == vipnr6) | (Guestseg.segmentcode == vipnr7) | (Guestseg.segmentcode == vipnr8) | (Guestseg.segmentcode == vipnr9))).first()

                if guestseg:

                    segment = get_cache (Segment, {"segmentcode": [(eq, guestseg.segmentcode)]})
                    vip_flag = replace_str(segment.bezeich, " ", "")
                cl_list = Cl_list()
                cl_list_data.append(cl_list)

                cl_list.nr = nr
                cl_list.rmcat = zimkateg.kurzbez + setup_list.char
                cl_list.kurzbez = zimkateg.kurzbez
                cl_list.bezeich = zimkateg.bezeichnung
                cl_list.nat = gmember.nation1
                cl_list.resnr = genstat.resnr
                cl_list.vip = vip_flag
                cl_list.name = gmember.name + ", " + gmember.vorname1 +\
                        " " + gmember.anrede1
                cl_list.rmno = genstat.zinr
                cl_list.zipreis =  to_decimal(genstat.zipreis)
                cl_list.arrive = genstat.res_date[0]
                cl_list.depart = genstat.res_date[1]
                cl_list.qty = 1
                cl_list.a = genstat.erwachs
                cl_list.c = genstat.kind1 + genstat.kind2 + genstat.kind3
                cl_list.co = genstat.gratis
                cl_list.argt = genstat.argt
                cl_list.flight = substring(res_line.flight_nr, 11, 6)
                cl_list.etd = substring(res_line.flight_nr, 17, 5)
                cl_list.ci_time = to_string(res_line.ankzeit, "HH:MM")
                cl_list.paym = genstat.segmentcode
                cl_list.created = reservation.resdat
                cl_list.createid = reservation.useridanlage
                cl_list.etage = zimmer.etage
                cl_list.zinr_bez = zimmer.bezeich
                cl_list.birthdate = gmember.geburtdatum1
                cl_list.telefon = gmember.telefon
                cl_list.mobil_tel = gmember.mobil_telefon

                if res_line.resstatus != 11 and res_line.resstatus != 13:
                    cl_list.flag_guest = 1


                else:
                    cl_list.flag_guest = 2

                mc_guest = get_cache (Mc_guest, {"gastnr": [(eq, gmember.gastnr)]})

                if mc_guest:
                    cl_list.telefon = gmember.telefon + ";" + mc_guest.cardnum

                    mc_types = get_cache (Mc_types, {"nr": [(eq, mc_guest.nr)]})

                    if mc_types:
                        cl_list.mobil_tel = gmember.mobil_telefon + ";" + mc_types.bezeich
                    else:
                        cl_list.mobil_tel = gmember.mobil_telefon
                else:
                    cl_list.telefon = gmember.telefon

                nation = get_cache (Nation, {"kurzbez": [(eq, gmember.nation2)]})

                if nation:
                    cl_list.local_reg = nation.bezeich

                waehrung = get_cache (Waehrung, {"waehrungsnr": [(eq, res_line.betriebsnr)]})

                if waehrung:
                    cl_list.curr = waehrung.wabkurz + ";" + gmember.email_adr

                reslin_queasy = get_cache (Reslin_queasy, {"key": [(eq, "specialrequest")],"resnr": [(eq, res_line.resnr)],"reslinnr": [(eq, res_line.reslinnr)]})

                if reslin_queasy:
                    cl_list.spreq = reslin_queasy.char3 + "," + cl_list.spreq

                reslin_queasy = get_cache (Reslin_queasy, {"key": [(eq, "arrangement")],"resnr": [(eq, res_line.resnr)],"reslinnr": [(eq, res_line.reslinnr)],"date1": [(le, datum)],"date2": [(ge, datum)]})

                if reslin_queasy:

                    if reslin_queasy.char2 != "":
                        cl_list.ratecode = reslin_queasy.char2
                    else:
                        for i in range(1,num_entries(res_line.zimmer_wunsch, ";") - 1 + 1) :
                            str = entry(i - 1, res_line.zimmer_wunsch, ";")

                            if substring(str, 0, 6) == ("$CODE$").lower() :
                                cl_list.ratecode = substring(str, 6)
                                break

                segment = get_cache (Segment, {"segmentcode": [(eq, genstat.segmentcode)]})

                if segment:
                    cl_list.segm = entry(0, segment.bezeich, "$$0")

                if guest.karteityp != 0:
                    cl_list.company = guest.name + ", " + guest.vorname1 + " " + guest.anrede1 + guest.anredefirma
                else:
                    cl_list.company = guest.name + ", " + guest.vorname1 + " " + guest.anrede1 + guest.anredefirma

                if cl_list.nat == "":
                    cl_list.nat = "?"

                if genstat.resstatus == 13:
                    cl_list.qty = 0

                if not split_rsv_print:

                    if incl_gcomment:

                        gbuff = get_cache (Guest, {"gastnr": [(eq, res_line.gastnrmember)]})

                        if gbuff:
                            for i in range(1,length(gbuff.bemerkung)  + 1) :

                                if substring(gbuff.bemerkung, i - 1, 1) == chr_unicode(10):
                                    cl_list.bemerk = cl_list.bemerk + " "
                                else:
                                    cl_list.bemerk = cl_list.bemerk + substring(trim(gbuff.bemerkung) , i - 1, 1)
                        cl_list.bemerk = cl_list.bemerk + " || "

                    if incl_rsvcomment:

                        rbuff = get_cache (Reservation, {"resnr": [(eq, reservation.resnr)]})

                        if rbuff:
                            for j in range(1,length(rbuff.bemerk)  + 1) :

                                if substring(rbuff.bemerk, j - 1, 1) == chr_unicode(10):
                                    cl_list.bemerk1 = cl_list.bemerk1 + " "
                                else:
                                    cl_list.bemerk1 = cl_list.bemerk1 + substring(trim(rbuff.bemerk) , j - 1, 1)
                        cl_list.bemerk = cl_list.bemerk + cl_list.bemerk1 + " || "
                    for i in range(1,length(res_line.bemerk)  + 1) :

                        if substring(res_line.bemerk, i - 1, 1) == chr_unicode(10):
                            cl_list.bemerk = cl_list.bemerk + " "
                        else:
                            cl_list.bemerk = cl_list.bemerk + substring(trim(res_line.bemerk) , i - 1, 1)
                    all_remark = res_line.bemerk
                    all_remark = replace_str(all_remark, chr_unicode(10) , " ")
                    all_remark = replace_str(all_remark, chr_unicode(13) , " ")
                    cl_list.bemerk01 = to_string(substring(all_remark, 0, 225))
                    cl_list.bemerk02 = to_string(substring(all_remark, 225, 225))
                    cl_list.bemerk03 = to_string(substring(all_remark, 450, 225))
                    cl_list.bemerk04 = to_string(substring(all_remark, 675, 225))
                else:
                    for i in range(1,length(res_line.bemerk)  + 1) :
                        cl_list.bemerk = cl_list.bemerk + substring(trim(res_line.bemerk) , i - 1, 1)

                    rbuff = get_cache (Reservation, {"resnr": [(eq, reservation.resnr)]})

                    if rbuff:
                        cl_list.rsv_comment = rbuff.bemerk

                    gbuff = get_cache (Guest, {"gastnr": [(eq, res_line.gastnrmember)]})

                    if gbuff:
                        cl_list.g_comment = gbuff.bemerkung

                    queasy = get_cache (Queasy, {"key": [(eq, 267)],"number1": [(eq, res_line.resnr)],"number2": [(eq, res_line.reslinnr)]})

                    if queasy:
                        cl_list.other_comment = queasy.char1
                cl_list.pax = to_string(cl_list.a, ">9") + "/" + to_string(cl_list.c, "9") + " " + to_string(cl_list.co, "9")

                if cl_list.nat == "":
                    cl_list.nat = "?"
                else:

                    nation = get_cache (Nation, {"kurzbez": [(eq, cl_list.nat)]})

                    if nation:
                        cl_list.nation = nation.bezeich

                zinr_list = query(zinr_list_data, filters=(lambda zinr_list: zinr_list.zinr == genstat.zinr and zinr_list.resnr == res_line.resnr and zinr_list.reslinnr == res_line.reslinnr), first=True)

                if not zinr_list:
                    zinr_list = Zinr_list()
                    zinr_list_data.append(zinr_list)

                    zinr_list.resnr = res_line.resnr
                    zinr_list.reslinnr = res_line.reslinnr
                    zinr_list.zinr = genstat.zinr

                    queasy = get_cache (Queasy, {"key": [(eq, 14)],"char1": [(eq, genstat.zinr)],"date1": [(le, curr_date)],"date2": [(ge, curr_date)]})

                    if zimmer.sleeping and genstat.resstatus != 13:

                        if not queasy:
                            tot_rm = tot_rm + 1
                            tot_rmqty = tot_rmqty + 1

                        elif queasy and queasy.number3 != genstat.gastnr:
                            tot_rm = tot_rm + 1
                            tot_rmqty = tot_rmqty + 1

                    if zimmer.sleeping and (genstat.zipreis > 0 or genstat.zipreis == 0) and genstat.erwachs > 0 and genstat.resstatus != 13:
                        z = z + 1

                        if not queasy:
                            tot_payrm = tot_payrm + 1

                        elif queasy and queasy.number3 != genstat.gastnr:
                            tot_payrm = tot_payrm + 1

                    elif not zimmer.sleeping:

                        if queasy and queasy.number3 != genstat.gastnr and genstat.zipreis > 0:
                            tot_rm = tot_rm + 1
                            tot_rmqty = tot_rmqty + 1
                        inactive = inactive + 1
                tot_a = tot_a + genstat.erwachs
                tot_c = tot_c + genstat.kind1 + genstat.kind2 + genstat.kind3
                tot_co = tot_co + genstat.gratis

                if exc_compli:
                    tot_co = 0

            if not disp_accompany:

                cl_list = query(cl_list_data, filters=(lambda cl_list: cl_list.rmno == res_line.zinr and cl_list.resnr == res_line.resnr and cl_list.arrive == res_line.ankunft and cl_list.zipreis == 0 and (cl_list.a + cl_list.c) < 1 and cl_list.co < 1), first=True)

                if cl_list:
                    cl_list_data.remove(cl_list)
                    pass

            if exc_compli:

                cl_list = query(cl_list_data, filters=(lambda cl_list: cl_list.rmno == res_line.zinr and cl_list.resnr == res_line.resnr and cl_list.arrive == res_line.ankunft and cl_list.co > 0), first=True)

                if cl_list:
                    cl_list_data.remove(cl_list)
                    pass
                    tot_rm = tot_rm - 1

        for cl_list in query(cl_list_data, sort_by=[("nation",False),("bezeich",False)]):

            mealcoup = get_cache (Mealcoup, {"name": [(eq, "breakfast")],"resnr": [(eq, cl_list.resnr)],"zinr": [(eq, cl_list.rmno)]})

            if mealcoup:
                cl_list.tot_bfast = mealcoup.verbrauch[0] + mealcoup.verbrauch[1] + mealcoup.verbrauch[2] + mealcoup.verbrauch[3] + mealcoup.verbrauch[4] +\
                        mealcoup.verbrauch[5] + mealcoup.verbrauch[6] + mealcoup.verbrauch[7] + mealcoup.verbrauch[8] + mealcoup.verbrauch[9] +\
                        mealcoup.verbrauch[10] + mealcoup.verbrauch[11] + mealcoup.verbrauch[12] + mealcoup.verbrauch[13] + mealcoup.verbrauch[14] +\
                        mealcoup.verbrauch[15] + mealcoup.verbrauch[16] + mealcoup.verbrauch[17] + mealcoup.verbrauch[18] + mealcoup.verbrauch[19] +\
                        mealcoup.verbrauch[20] + mealcoup.verbrauch[21] + mealcoup.verbrauch[22] + mealcoup.verbrauch[23] + mealcoup.verbrauch[24] +\
                        mealcoup.verbrauch[25] + mealcoup.verbrauch[26] + mealcoup.verbrauch[27] + mealcoup.verbrauch[28] + mealcoup.verbrauch[29] +\
                        mealcoup.verbrauch[30] + mealcoup.verbrauch[31]

            s_list = query(s_list_data, filters=(lambda s_list: s_list.rmcat == cl_list.kurzbez), first=True)

            if not s_list:

                s_list = query(s_list_data, filters=(lambda s_list: s_list.rmcat == ""), first=True)

                if s_list:
                    s_list.rmcat = cl_list.kurzbez
                    s_list.bezeich = cl_list.bezeich

            if not s_list:
                s_list = S_list()
                s_list_data.append(s_list)

                s_list.rmcat = cl_list.kurzbez
                s_list.bezeich = cl_list.bezeich
            s_list.anz = s_list.anz + cl_list.qty

            s_list = query(s_list_data, filters=(lambda s_list: s_list.nat == cl_list.nat), first=True)

            if not s_list:

                s_list = query(s_list_data, filters=(lambda s_list: s_list.nat == ""), first=True)

                if s_list:
                    s_list.nat = cl_list.nat

            if not s_list:
                s_list = S_list()
                s_list_data.append(s_list)


                if s_list:
                    s_list.nat = cl_list.nat
            s_list.adult = s_list.adult + cl_list.a + cl_list.co
            s_list.child = s_list.child + cl_list.c
            s_list.rmqty = s_list.rmqty + cl_list.qty

        if (tot_a + tot_co) != 0:

            for s_list in query(s_list_data, filters=(lambda s_list: s_list.nat != "")):

                nation = get_cache (Nation, {"kurzbez": [(eq, s_list.nat)]})

                if nation:
                    s_list.nat = nation.bezeich
                s_list.proz =  to_decimal(s_list.adult) / to_decimal((tot_a) + to_decimal(tot_co)) * to_decimal("100")

        # sort by rmno -> query diatas merubah sort order.-------------------
        for cl_list in query(cl_list_data, sort_by=[("rmno",False)]):
            pass
        #--------------------------------------------------------------------

    def create_inhouse1():

        nonlocal tot_payrm, tot_rm, tot_a, tot_c, tot_co, tot_avail, tot_rmqty, inactive, cl_list_data, s_list_data, t_buff_queasy_data, vipnr1, vipnr2, vipnr3, vipnr4, vipnr5, vipnr6, vipnr7, vipnr8, vipnr9, tot_room, all_room, all_remark, queasy, htparam, zkstat, zinrstat, paramtext, guest, reservation, zimmer, zimkateg, res_line, guestseg, segment, mc_guest, mc_types, nation, waehrung, reslin_queasy, mealcoup, genstat
        nonlocal sorttype, datum, curr_date, froom, troom, exc_depart, incl_gcomment, incl_rsvcomment, prog_name, disp_accompany, disp_exclinact, split_rsv_print, exc_compli


        nonlocal setup_list, str_list, cl_list, s_list, zinr_list, t_buff_queasy
        nonlocal setup_list_data, str_list_data, cl_list_data, s_list_data, zinr_list_data, t_buff_queasy_data

        i:int = 0
        j:int = 0
        vip_flag:string = ""
        str:string = ""
        nr:int = 0
        curr_gastnr:int = 0
        actflag1:int = 0
        actflag2:int = 0
        gmember = None
        gbuff = None
        rbuff = None
        Gmember =  create_buffer("Gmember",Guest)
        Gbuff =  create_buffer("Gbuff",Guest)
        Rbuff =  create_buffer("Rbuff",Reservation)
        zinr_list_data.clear()

        if datum == curr_date:
            actflag1 = 1
            actflag2 = 1
        else:
            actflag1 = 1
            actflag2 = 2
        tot_payrm = 0
        tot_rm = 0
        tot_a = 0
        tot_c = 0
        tot_co = 0
        inactive = 0
        s_list_data.clear()
        cl_list_data.clear()
        str_list_data.clear()
        tot_avail = 0

        for zimmer in db_session.query(Zimmer).filter(
                 (Zimmer.sleeping)).order_by(Zimmer._recid).all():
            tot_avail = tot_avail + 1

        res_line_obj_list = {}
        res_line = Res_line()
        zimkateg = Zimkateg()
        reservation = Reservation()
        guest = Guest()
        gmember = Guest()
        for res_line.setup, res_line.zinr, res_line.resnr, res_line.name, res_line.zipreis, res_line.ankunft, res_line.abreise, res_line.zimmeranz, res_line.erwachs, \
            res_line.kind1, res_line.kind2, res_line.gratis, res_line.arrangement, res_line.flight_nr, res_line.ankzeit, res_line.resstatus, res_line.betriebsnr, \
            res_line.reslinnr, res_line.zimmer_wunsch, res_line.zimmerfix, res_line.gastnrmember, res_line.bemerk, res_line.gastnr, res_line._recid, zimkateg.kurzbez, \
            zimkateg.bezeichnung, zimkateg._recid, reservation.segmentcode, reservation.resdat, reservation.useridanlage, reservation.resnr, reservation._recid, guest.name, \
            guest.vorname1, guest.anrede1, guest.anredefirma, guest.gastnr, guest.karteityp, guest._recid, gmember.name, gmember.vorname1, gmember.anrede1, gmember.anredefirma, \
            gmember.gastnr, gmember.karteityp, gmember._recid, gmember.nation1, gmember.nation2, gmember.email_adr, gmember.geburtdatum1, gmember.telefon, gmember.mobil_telefon \
                in db_session.query(Res_line.setup, Res_line.zinr, Res_line.resnr, Res_line.name, Res_line.zipreis, Res_line.ankunft, Res_line.abreise, Res_line.zimmeranz,\
                                    Res_line.erwachs, Res_line.kind1, Res_line.kind2, Res_line.gratis, Res_line.arrangement, Res_line.flight_nr, Res_line.ankzeit, \
                                    Res_line.resstatus, Res_line.betriebsnr, Res_line.reslinnr, Res_line.zimmer_wunsch, Res_line.zimmerfix, Res_line.gastnrmember,\
                                    Res_line.bemerk, Res_line.gastnr, Res_line._recid, Zimkateg.kurzbez, Zimkateg.bezeichnung, Zimkateg._recid, \
                                    Reservation.segmentcode, Reservation.resdat, Reservation.useridanlage, Reservation.resnr, Reservation._recid, \
                                    Guest.name, Guest.vorname1, Guest.anrede1, Guest.anredefirma, Guest.gastnr, Guest.karteityp, Guest._recid, \
                                    Gmember.name, Gmember.vorname1, Gmember.anrede1, Gmember.anredefirma, Gmember.gastnr, Gmember.karteityp,\
                                    Gmember._recid, Gmember.nation1, Gmember.nation2, Gmember.email_adr, Gmember.geburtdatum1, Gmember.telefon, Gmember.mobil_telefon)\
                                .join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Guest,(Guest.gastnr == Reservation.gastnr)).join(Gmember,(Gmember.gastnr == Res_line.gastnrmember)).filter(
                 (Res_line.active_flag >= actflag1) & (Res_line.active_flag <= actflag2) & (Res_line.resstatus != 9) & (Res_line.resstatus != 10) & (Res_line.resstatus != 12) & (Res_line.ankunft <= datum) & (Res_line.abreise >= datum) & (Res_line.zinr >= (froom).lower()) & (Res_line.zinr <= (troom).lower())).order_by(Guest.karteityp.desc(), Guest.name, Guest.gastnr, Res_line.name, Res_line.zinr).all():
            if res_line_obj_list.get(res_line._recid):
                continue
            else:
                res_line_obj_list[res_line._recid] = True

            if exc_depart and res_line.abreise == datum:
                pass
            else:

                setup_list = query(setup_list_data, filters=(lambda setup_list: setup_list.nr == res_line.setup + 1), first=True)

                zimmer = get_cache (Zimmer, {"zinr": [(eq, res_line.zinr)]})

                if curr_gastnr != guest.gastnr:
                    nr = 0
                    curr_gastnr = guest.gastnr

                if guest.karteityp > 0:
                    nr = nr + 1
                vip_flag = ""

                guestseg = db_session.query(Guestseg).filter(
                         (Guestseg.gastnr == gmember.gastnr) & ((Guestseg.segmentcode == vipnr1) | (Guestseg.segmentcode == vipnr2) | (Guestseg.segmentcode == vipnr3) | (Guestseg.segmentcode == vipnr4) | (Guestseg.segmentcode == vipnr5) | (Guestseg.segmentcode == vipnr6) | (Guestseg.segmentcode == vipnr7) | (Guestseg.segmentcode == vipnr8) | (Guestseg.segmentcode == vipnr9))).first()

                if guestseg:

                    segment = get_cache (Segment, {"segmentcode": [(eq, guestseg.segmentcode)]})
                    vip_flag = segment.bezeich


                cl_list = Cl_list()
                cl_list_data.append(cl_list)

                cl_list.nr = nr
                cl_list.karteityp = guest.karteityp
                cl_list.rmcat = zimkateg.kurzbez + setup_list.char
                cl_list.kurzbez = zimkateg.kurzbez
                cl_list.bezeich = zimkateg.bezeichnung
                cl_list.nat = gmember.nation1
                cl_list.resnr = res_line.resnr
                cl_list.vip = vip_flag
                cl_list.name = res_line.name
                cl_list.rmno = res_line.zinr
                cl_list.zipreis =  to_decimal(res_line.zipreis)
                cl_list.arrive = res_line.ankunft
                cl_list.depart = res_line.abreise
                cl_list.qty = res_line.zimmeranz
                cl_list.a = res_line.erwachs
                cl_list.c = res_line.kind1 + res_line.kind2
                cl_list.co = res_line.gratis
                cl_list.argt = res_line.arrangement
                cl_list.flight = substring(res_line.flight_nr, 11, 6)
                cl_list.etd = substring(res_line.flight_nr, 17, 5)
                cl_list.ci_time = to_string(res_line.ankzeit, "HH:MM")
                cl_list.paym = reservation.segmentcode
                cl_list.created = reservation.resdat
                cl_list.createid = reservation.useridanlage
                cl_list.etage = zimmer.etage
                cl_list.zinr_bez = zimmer.bezeich
                cl_list.birthdate = gmember.geburtdatum1
                cl_list.telefon = gmember.telefon
                cl_list.mobil_tel = gmember.mobil_telefon

                if res_line.resstatus != 11 and res_line.resstatus != 13:
                    cl_list.flag_guest = 1


                else:
                    cl_list.flag_guest = 2

                mc_guest = get_cache (Mc_guest, {"gastnr": [(eq, gmember.gastnr)]})

                if mc_guest:
                    cl_list.telefon = gmember.telefon + ";" + mc_guest.cardnum

                    mc_types = get_cache (Mc_types, {"nr": [(eq, mc_guest.nr)]})

                    if mc_types:
                        cl_list.mobil_tel = gmember.mobil_telefon + ";" + mc_types.bezeich
                    else:
                        cl_list.mobil_tel = gmember.mobil_telefon
                else:
                    cl_list.telefon = gmember.telefon

                nation = get_cache (Nation, {"kurzbez": [(eq, gmember.nation2)]})

                if nation:
                    cl_list.local_reg = nation.bezeich

                waehrung = get_cache (Waehrung, {"waehrungsnr": [(eq, res_line.betriebsnr)]})

                if waehrung:
                    cl_list.curr = waehrung.wabkurz + ";" + gmember.email_adr

                reslin_queasy = get_cache (Reslin_queasy, {"key": [(eq, "specialrequest")],"resnr": [(eq, res_line.resnr)],"reslinnr": [(eq, res_line.reslinnr)]})

                if reslin_queasy:
                    cl_list.spreq = reslin_queasy.char3 + "," + cl_list.spreq

                reslin_queasy = get_cache (Reslin_queasy, {"key": [(eq, "arrangement")],"resnr": [(eq, res_line.resnr)],"reslinnr": [(eq, res_line.reslinnr)],"date1": [(le, datum)],"date2": [(ge, datum)]})

                if reslin_queasy:

                    if reslin_queasy.char2 != "":
                        cl_list.ratecode = reslin_queasy.char2
                    else:
                        for i in range(1,num_entries(res_line.zimmer_wunsch, ";") - 1 + 1) :
                            str = entry(i - 1, res_line.zimmer_wunsch, ";")

                            if substring(str, 0, 6) == ("$CODE$").lower() :
                                cl_list.ratecode = substring(str, 6)
                                break

                mealcoup = get_cache (Mealcoup, {"name": [(eq, "breakfast")],"resnr": [(eq, res_line.resnr)],"zinr": [(eq, res_line.zinr)]})

                if mealcoup:
                    cl_list.tot_bfast = mealcoup.verbrauch[0] + mealcoup.verbrauch[1] + mealcoup.verbrauch[2] + mealcoup.verbrauch[3] + mealcoup.verbrauch[4] +\
                            mealcoup.verbrauch[5] + mealcoup.verbrauch[6] + mealcoup.verbrauch[7] + mealcoup.verbrauch[8] + mealcoup.verbrauch[9] +\
                            mealcoup.verbrauch[10] + mealcoup.verbrauch[11] + mealcoup.verbrauch[12] + mealcoup.verbrauch[13] + mealcoup.verbrauch[14] +\
                            mealcoup.verbrauch[15] + mealcoup.verbrauch[16] + mealcoup.verbrauch[17] + mealcoup.verbrauch[18] + mealcoup.verbrauch[19] +\
                            mealcoup.verbrauch[20] + mealcoup.verbrauch[21] + mealcoup.verbrauch[22] + mealcoup.verbrauch[23] + mealcoup.verbrauch[24] +\
                            mealcoup.verbrauch[25] + mealcoup.verbrauch[26] + mealcoup.verbrauch[27] + mealcoup.verbrauch[28] + mealcoup.verbrauch[29] +\
                            mealcoup.verbrauch[30] + mealcoup.verbrauch[31]

                segment = get_cache (Segment, {"segmentcode": [(eq, reservation.segmentcode)]})

                if segment:
                    cl_list.segm = entry(0, segment.bezeich, "$$0")

                if guest.karteityp != 0:
                    cl_list.company = guest.name + ", " + guest.vorname1 + " " + guest.anrede1 + guest.anredefirma
                else:
                    cl_list.company = guest.name + ", " + guest.vorname1 + " " + guest.anrede1 + guest.anredefirma

                if cl_list.nat == "":
                    cl_list.nat = "?"

                if res_line.resstatus == 13 or res_line.zimmerfix :
                    cl_list.qty = 0

                if not split_rsv_print:

                    if incl_gcomment:

                        gbuff = get_cache (Guest, {"gastnr": [(eq, res_line.gastnrmember)]})

                        if gbuff:
                            for i in range(1,length(gbuff.bemerkung)  + 1) :

                                if substring(gbuff.bemerkung, i - 1, 1) == chr_unicode(10):
                                    cl_list.bemerk = cl_list.bemerk + " "
                                else:
                                    cl_list.bemerk = cl_list.bemerk + substring(trim(gbuff.bemerkung) , i - 1, 1)
                        cl_list.bemerk = cl_list.bemerk + " || "

                    if incl_rsvcomment:

                        rbuff = get_cache (Reservation, {"resnr": [(eq, reservation.resnr)]})

                        if rbuff:
                            for j in range(1,length(rbuff.bemerk)  + 1) :

                                if substring(rbuff.bemerk, j - 1, 1) == chr_unicode(10):
                                    cl_list.bemerk1 = cl_list.bemerk1 + " "
                                else:
                                    cl_list.bemerk1 = cl_list.bemerk1 + substring(trim(rbuff.bemerk) , j - 1, 1)
                        cl_list.bemerk = cl_list.bemerk + cl_list.bemerk1 + " || "
                    for i in range(1,length(res_line.bemerk)  + 1) :

                        if substring(res_line.bemerk, i - 1, 1) == chr_unicode(10):
                            cl_list.bemerk = cl_list.bemerk + " "
                        else:
                            cl_list.bemerk = cl_list.bemerk + substring(trim(res_line.bemerk) , i - 1, 1)
                    all_remark = res_line.bemerk
                    all_remark = replace_str(all_remark, chr_unicode(10) , " ")
                    all_remark = replace_str(all_remark, chr_unicode(13) , " ")
                    cl_list.bemerk01 = to_string(substring(all_remark, 0, 225))
                    cl_list.bemerk02 = to_string(substring(all_remark, 225, 225))
                    cl_list.bemerk03 = to_string(substring(all_remark, 450, 225))
                    cl_list.bemerk04 = to_string(substring(all_remark, 675, 225))
                else:
                    for i in range(1,length(res_line.bemerk)  + 1) :
                        cl_list.bemerk = cl_list.bemerk + substring(trim(res_line.bemerk) , i - 1, 1)

                    rbuff = get_cache (Reservation, {"resnr": [(eq, reservation.resnr)]})

                    if rbuff:
                        cl_list.rsv_comment = rbuff.bemerk

                    gbuff = get_cache (Guest, {"gastnr": [(eq, res_line.gastnrmember)]})

                    if gbuff:
                        cl_list.g_comment = gbuff.bemerkung

                    queasy = get_cache (Queasy, {"key": [(eq, 267)],"number1": [(eq, res_line.resnr)],"number2": [(eq, res_line.reslinnr)]})

                    if queasy:
                        cl_list.other_comment = queasy.char1
                cl_list.pax = to_string(cl_list.a, ">9") + "/" + to_string(cl_list.c, "9") + " " + to_string(cl_list.co, "9")

                if cl_list.nat == "":
                    cl_list.nat = "?"
                else:

                    nation = get_cache (Nation, {"kurzbez": [(eq, cl_list.nat)]})

                    if nation:
                        cl_list.nation = nation.bezeich

                zinr_list = query(zinr_list_data, filters=(lambda zinr_list: zinr_list.zinr == res_line.zinr and zinr_list.resnr == res_line.resnr and zinr_list.reslinnr == res_line.reslinnr), first=True)

                if not zinr_list:
                    zinr_list = Zinr_list()
                    zinr_list_data.append(zinr_list)

                    zinr_list.resnr = res_line.resnr
                    zinr_list.reslinnr = res_line.reslinnr
                    zinr_list.zinr = res_line.zinr

                    queasy = get_cache (Queasy, {"key": [(eq, 14)],"char1": [(eq, res_line.zinr)],"date1": [(le, curr_date)],"date2": [(ge, curr_date)]})

                    if zimmer.sleeping and res_line.resstatus != 13:

                        if not queasy:
                            tot_rm = tot_rm + res_line.zimmeranz
                            tot_rmqty = tot_rmqty + res_line.zimmeranz

                        elif queasy and queasy.number3 != res_line.gastnr:
                            tot_rm = tot_rm + res_line.zimmeranz
                            tot_rmqty = tot_rmqty + res_line.zimmeranz

                    if zimmer.sleeping and (res_line.zipreis > 0 or res_line.zipreis == 0) and res_line.resstatus != 13 and res_line.erwachs > 0:

                        if not queasy:
                            tot_payrm = tot_payrm + res_line.zimmeranz

                        elif queasy and queasy.number3 != res_line.gastnr:
                            tot_payrm = tot_payrm + res_line.zimmeranz

                    elif not zimmer.sleeping:

                        if queasy and queasy.number3 != res_line.gastnr and res_line.zipreis > 0:
                            tot_rm = tot_rm + res_line.zimmeranz
                            tot_rmqty = tot_rmqty + res_line.zimmeranz
                        inactive = inactive + 1
                tot_a = tot_a + res_line.erwachs
                tot_c = tot_c + res_line.kind1 + res_line.kind2
                tot_co = tot_co + res_line.gratis

                if exc_compli:
                    tot_co = 0

            if not disp_accompany:

                cl_list = query(cl_list_data, filters=(lambda cl_list: cl_list.rmno == res_line.zinr and cl_list.resnr == res_line.resnr and cl_list.arrive == res_line.ankunft and cl_list.zipreis == 0 and (cl_list.a + cl_list.c) < 1 and cl_list.co < 1), first=True)

                if cl_list:
                    cl_list_data.remove(cl_list)
                    pass

            if exc_compli:

                cl_list = query(cl_list_data, filters=(lambda cl_list: cl_list.rmno == res_line.zinr and cl_list.resnr == res_line.resnr and cl_list.arrive == res_line.ankunft and cl_list.co > 0), first=True)

                if cl_list:
                    cl_list_data.remove(cl_list)
                    pass
                    tot_rm = tot_rm - 1

        for cl_list in query(cl_list_data, sort_by=[("nation",False),("bezeich",False)]):

            s_list = query(s_list_data, filters=(lambda s_list: s_list.rmcat == cl_list.kurzbez), first=True)

            if not s_list:

                s_list = query(s_list_data, filters=(lambda s_list: s_list.rmcat == ""), first=True)

                if s_list:
                    s_list.rmcat = cl_list.kurzbez
                    s_list.bezeich = cl_list.bezeich

            if not s_list:
                s_list = S_list()
                s_list_data.append(s_list)

                s_list.rmcat = cl_list.kurzbez
                s_list.bezeich = cl_list.bezeich
            s_list.anz = s_list.anz + cl_list.qty

            s_list = query(s_list_data, filters=(lambda s_list: s_list.nat == cl_list.nat), first=True)

            if not s_list:

                s_list = query(s_list_data, filters=(lambda s_list: s_list.nat == ""), first=True)

                if s_list:
                    s_list.nat = cl_list.nat

            if not s_list:
                s_list = S_list()
                s_list_data.append(s_list)


                if s_list:
                    s_list.nat = cl_list.nat
            s_list.adult = s_list.adult + cl_list.a + cl_list.co
            s_list.child = s_list.child + cl_list.c
            s_list.rmqty = s_list.rmqty + cl_list.qty

        if (tot_a + tot_co) != 0:

            for s_list in query(s_list_data, filters=(lambda s_list: s_list.nat != "")):

                nation = get_cache (Nation, {"kurzbez": [(eq, s_list.nat)]})

                if nation:
                    s_list.nat = nation.bezeich
                s_list.proz =  to_decimal(s_list.adult) / to_decimal((tot_a) + to_decimal(tot_co)) * to_decimal("100")

        # sort by rmno -> query diatas merubah sort order.-------------------
        for cl_list in query(cl_list_data, sort_by=[("rmno",False)]):
            pass
        #--------------------------------------------------------------------

    def create_genstat_inhouse1():
        # sorttype = 2
        nonlocal tot_payrm, tot_rm, tot_a, tot_c, tot_co, tot_avail, tot_rmqty, inactive, cl_list_data, s_list_data, t_buff_queasy_data, vipnr1, vipnr2, vipnr3, vipnr4, vipnr5, vipnr6, vipnr7, vipnr8, vipnr9, tot_room, all_room, all_remark, queasy, htparam, zkstat, zinrstat, paramtext, guest, reservation, zimmer, zimkateg, res_line, guestseg, segment, mc_guest, mc_types, nation, waehrung, reslin_queasy, mealcoup, genstat
        nonlocal sorttype, datum, curr_date, curr_gastnr, froom, troom, exc_depart, incl_gcomment, incl_rsvcomment, prog_name, disp_accompany, disp_exclinact, split_rsv_print, exc_compli


        nonlocal setup_list, str_list, cl_list, s_list, zinr_list, t_buff_queasy
        nonlocal setup_list_data, str_list_data, cl_list_data, s_list_data, zinr_list_data, t_buff_queasy_data

        i:int = 0
        j:int = 0
        vip_flag:string = ""
        nr:int = 0
        str:string = ""
        actflag1:int = 0
        actflag2:int = 0
        do_it:bool = False
        gmember = None
        gbuff = None
        rbuff = None
        Gmember =  create_buffer("Gmember",Guest)
        Gbuff =  create_buffer("Gbuff",Guest)
        Rbuff =  create_buffer("Rbuff",Reservation)
        zinr_list_data.clear()

        if datum == curr_date:
            actflag1 = 1
            actflag2 = 1
        else:
            actflag1 = 1
            actflag2 = 2
        tot_payrm = 0
        tot_rm = 0
        tot_a = 0
        tot_c = 0
        tot_co = 0
        inactive = 0
        s_list_data.clear()
        cl_list_data.clear()
        str_list_data.clear()
        tot_avail = 0

        for zkstat in db_session.query(Zkstat).filter(
                 (Zkstat.datum == datum)).order_by(Zkstat._recid).all():
            tot_avail = tot_avail + zkstat.anz100

        genstat_obj_list = {}
        genstat = Genstat()
        zimkateg = Zimkateg()
        reservation = Reservation()
        guest = Guest()
        gmember = Guest()
        for genstat.resstatus, genstat.res_date, genstat.resnr, genstat.res_int, genstat.zinr, genstat.zipreis, genstat.erwachs, genstat.kind1, genstat.kind2, \
            genstat.kind3, genstat.gratis, genstat.argt, genstat.segmentcode, genstat.gastnr, genstat._recid, zimkateg.kurzbez, zimkateg.bezeichnung, zimkateg._recid, \
            reservation.segmentcode, reservation.resdat, reservation.useridanlage, reservation.resnr, reservation._recid, guest.name, guest.vorname1, guest.anrede1, \
            guest.anredefirma, guest.gastnr, guest.karteityp, guest._recid, gmember.name, gmember.vorname1, gmember.anrede1, gmember.anredefirma, gmember.gastnr, \
            gmember.karteityp, gmember._recid, gmember.nation1, gmember.nation2, gmember.email_adr, gmember.geburtdatum1, gmember.telefon, gmember.mobil_telefon \
            in db_session.query(Genstat.resstatus, Genstat.res_date, Genstat.resnr, Genstat.res_int, Genstat.zinr, Genstat.zipreis, Genstat.erwachs, Genstat.kind1, \
                                Genstat.kind2, Genstat.kind3, Genstat.gratis, Genstat.argt, Genstat.segmentcode, Genstat.gastnr, Genstat._recid, Zimkateg.kurzbez, \
                                Zimkateg.bezeichnung, Zimkateg._recid, Reservation.segmentcode, Reservation.resdat, Reservation.useridanlage, Reservation.resnr, \
                                Reservation._recid, Guest.name, Guest.vorname1, Guest.anrede1, Guest.anredefirma, Guest.gastnr, Guest.karteityp, Guest._recid, \
                                Gmember.name, Gmember.vorname1, Gmember.anrede1, Gmember.anredefirma, Gmember.gastnr, Gmember.karteityp, Gmember._recid, \
                                Gmember.nation1, Gmember.nation2, Gmember.email_adr, Gmember.geburtdatum1, Gmember.telefon, Gmember.mobil_telefon)\
                        .join(Zimkateg,(Zimkateg.zikatnr == Genstat.zikatnr))\
                        .join(Reservation,(Reservation.resnr == Genstat.resnr))\
                        .join(Guest,(Guest.gastnr == Genstat.gastnr))\
                        .join(Gmember,(Gmember.gastnr == Genstat.gastnrmember))\
                        .filter(
                            (Genstat.datum == datum) &  (Genstat.zinr >= (froom).lower()) &  (Genstat.zinr <= (troom).lower()) &
                            (Genstat.datum == datum) & 
                            (Genstat.zinr >= (froom).lower()) & 
                            (Genstat.zinr <= (troom).lower())) \
                        .order_by(Guest.karteityp.desc(), Guest.name, Guest.gastnr, Gmember.name, Genstat.zinr).all():
            if genstat_obj_list.get(genstat._recid):
                continue
            else:
                genstat_obj_list[genstat._recid] = True

            if genstat.res_date[0] < datum and genstat.res_date[1] == datum and genstat.resstatus == 8:
                pass

            elif exc_depart and genstat.res_date[0] <= datum and genstat.res_date[1] == datum and genstat.resstatus == 8:
                pass
            else:

                res_line = get_cache (Res_line, {"resnr": [(eq, genstat.resnr)],"reslinnr": [(eq, genstat.res_int[0])]})

                setup_list = query(setup_list_data, filters=(lambda setup_list: setup_list.nr == res_line.setup + 1), first=True)

                zimmer = get_cache (Zimmer, {"zinr": [(eq, genstat.zinr)]})

                if curr_gastnr != guest.gastnr:
                    nr = 0
                    curr_gastnr = guest.gastnr

                if guest.karteityp > 0:
                    nr = nr + 1
                vip_flag = ""

                guestseg = db_session.query(Guestseg).filter(
                         (Guestseg.gastnr == gmember.gastnr) & ((Guestseg.segmentcode == vipnr1) | (Guestseg.segmentcode == vipnr2) | (Guestseg.segmentcode == vipnr3) | (Guestseg.segmentcode == vipnr4) | (Guestseg.segmentcode == vipnr5) | (Guestseg.segmentcode == vipnr6) | (Guestseg.segmentcode == vipnr7) | (Guestseg.segmentcode == vipnr8) | (Guestseg.segmentcode == vipnr9))).first()

                if guestseg:

                    segment = get_cache (Segment, {"segmentcode": [(eq, guestseg.segmentcode)]})
                    vip_flag = segment.bezeich


                cl_list = Cl_list()
                cl_list_data.append(cl_list)

                cl_list.nr = nr
                cl_list.karteityp = guest.karteityp
                cl_list.rmcat = zimkateg.kurzbez + setup_list.char
                cl_list.kurzbez = zimkateg.kurzbez
                cl_list.bezeich = zimkateg.bezeichnung
                cl_list.nat = gmember.nation1
                cl_list.resnr = genstat.resnr
                cl_list.vip = vip_flag
                cl_list.name = gmember.name + ", " + gmember.vorname1 +\
                        " " + gmember.anrede1
                cl_list.rmno = genstat.zinr
                cl_list.zipreis =  to_decimal(genstat.zipreis)
                cl_list.arrive = genstat.res_date[0]
                cl_list.depart = genstat.res_date[1]
                cl_list.qty = 1
                cl_list.a = genstat.erwachs
                cl_list.c = genstat.kind1 + genstat.kind2 + genstat.kind3
                cl_list.co = genstat.gratis
                cl_list.argt = genstat.argt
                cl_list.flight = substring(res_line.flight_nr, 11, 6)
                cl_list.etd = substring(res_line.flight_nr, 17, 5)
                cl_list.ci_time = to_string(res_line.ankzeit, "HH:MM")
                cl_list.paym = genstat.segmentcode
                cl_list.created = reservation.resdat
                cl_list.createid = reservation.useridanlage
                cl_list.etage = zimmer.etage
                cl_list.zinr_bez = zimmer.bezeich
                cl_list.birthdate = gmember.geburtdatum1
                cl_list.telefon = gmember.telefon
                cl_list.mobil_tel = gmember.mobil_telefon

                if res_line.resstatus != 11 and res_line.resstatus != 13:
                    cl_list.flag_guest = 1


                else:
                    cl_list.flag_guest = 2

                mc_guest = get_cache (Mc_guest, {"gastnr": [(eq, gmember.gastnr)]})

                if mc_guest:
                    cl_list.telefon = gmember.telefon + ";" + mc_guest.cardnum

                    mc_types = get_cache (Mc_types, {"nr": [(eq, mc_guest.nr)]})

                    if mc_types:
                        cl_list.mobil_tel = gmember.mobil_telefon + ";" + mc_types.bezeich
                    else:
                        cl_list.mobil_tel = gmember.mobil_telefon
                else:
                    cl_list.telefon = gmember.telefon

                nation = get_cache (Nation, {"kurzbez": [(eq, gmember.nation2)]})

                if nation:
                    cl_list.local_reg = nation.bezeich

                waehrung = get_cache (Waehrung, {"waehrungsnr": [(eq, res_line.betriebsnr)]})

                if waehrung:
                    cl_list.curr = waehrung.wabkurz + ";" + gmember.email_adr

                reslin_queasy = get_cache (Reslin_queasy, {"key": [(eq, "specialrequest")],"resnr": [(eq, res_line.resnr)],"reslinnr": [(eq, res_line.reslinnr)]})

                if reslin_queasy:
                    cl_list.spreq = reslin_queasy.char3 + "," + cl_list.spreq

                reslin_queasy = get_cache (Reslin_queasy, {"key": [(eq, "arrangement")],"resnr": [(eq, res_line.resnr)],"reslinnr": [(eq, res_line.reslinnr)],"date1": [(le, datum)],"date2": [(ge, datum)]})

                if reslin_queasy:

                    if reslin_queasy.char2 != "":
                        cl_list.ratecode = reslin_queasy.char2
                    else:
                        for i in range(1,num_entries(res_line.zimmer_wunsch, ";") - 1 + 1) :
                            str = entry(i - 1, res_line.zimmer_wunsch, ";")

                            if substring(str, 0, 6) == ("$CODE$").lower() :
                                cl_list.ratecode = substring(str, 6)
                                break

                segment = get_cache (Segment, {"segmentcode": [(eq, genstat.segmentcode)]})

                if segment:
                    cl_list.segm = entry(0, segment.bezeich, "$$0")

                if guest.karteityp != 0:
                    cl_list.company = guest.name + ", " + guest.vorname1 + " " + guest.anrede1 + guest.anredefirma
                else:
                    cl_list.company = guest.name + ", " + guest.vorname1 + " " + guest.anrede1 + guest.anredefirma

                if cl_list.nat == "":
                    cl_list.nat = "?"

                if genstat.resstatus == 13:
                    cl_list.qty = 0

                if not split_rsv_print:

                    if incl_gcomment:

                        gbuff = get_cache (Guest, {"gastnr": [(eq, res_line.gastnrmember)]})

                        if gbuff:
                            for i in range(1,length(gbuff.bemerkung)  + 1) :

                                if substring(gbuff.bemerkung, i - 1, 1) == chr_unicode(10):
                                    cl_list.bemerk = cl_list.bemerk + " "
                                else:
                                    cl_list.bemerk = cl_list.bemerk + substring(trim(gbuff.bemerkung) , i - 1, 1)
                        cl_list.bemerk = cl_list.bemerk + " || "

                    if incl_rsvcomment:

                        rbuff = get_cache (Reservation, {"resnr": [(eq, reservation.resnr)]})

                        if rbuff:
                            for j in range(1,length(rbuff.bemerk)  + 1) :

                                if substring(rbuff.bemerk, j - 1, 1) == chr_unicode(10):
                                    cl_list.bemerk1 = cl_list.bemerk1 + " "
                                else:
                                    cl_list.bemerk1 = cl_list.bemerk1 + substring(trim(rbuff.bemerk) , j - 1, 1)
                        cl_list.bemerk = cl_list.bemerk + cl_list.bemerk1 + " || "
                    for i in range(1,length(res_line.bemerk)  + 1) :

                        if substring(res_line.bemerk, i - 1, 1) == chr_unicode(10):
                            cl_list.bemerk = cl_list.bemerk + " "
                        else:
                            cl_list.bemerk = cl_list.bemerk + substring(trim(res_line.bemerk) , i - 1, 1)
                    all_remark = res_line.bemerk
                    all_remark = replace_str(all_remark, chr_unicode(10) , " ")
                    all_remark = replace_str(all_remark, chr_unicode(13) , " ")
                    cl_list.bemerk01 = to_string(substring(all_remark, 0, 225))
                    cl_list.bemerk02 = to_string(substring(all_remark, 225, 225))
                    cl_list.bemerk03 = to_string(substring(all_remark, 450, 225))
                    cl_list.bemerk04 = to_string(substring(all_remark, 675, 225))
                else:
                    for i in range(1,length(res_line.bemerk)  + 1) :
                        cl_list.bemerk = cl_list.bemerk + substring(trim(res_line.bemerk) , i - 1, 1)

                    rbuff = get_cache (Reservation, {"resnr": [(eq, reservation.resnr)]})

                    if rbuff:
                        cl_list.rsv_comment = rbuff.bemerk

                    gbuff = get_cache (Guest, {"gastnr": [(eq, res_line.gastnrmember)]})

                    if gbuff:
                        cl_list.g_comment = gbuff.bemerkung

                    queasy = get_cache (Queasy, {"key": [(eq, 267)],"number1": [(eq, res_line.resnr)],"number2": [(eq, res_line.reslinnr)]})

                    if queasy:
                        cl_list.other_comment = queasy.char1
                cl_list.pax = to_string(cl_list.a, ">9") + "/" + to_string(cl_list.c, "9") + " " + to_string(cl_list.co, "9")

                if cl_list.nat == "":
                    cl_list.nat = "?"
                else:

                    nation = get_cache (Nation, {"kurzbez": [(eq, cl_list.nat)]})

                    if nation:
                        cl_list.nation = nation.bezeich

                zinr_list = query(zinr_list_data, filters=(lambda zinr_list: zinr_list.zinr == genstat.zinr and zinr_list.resnr == res_line.resnr and zinr_list.reslinnr == res_line.reslinnr), first=True)

                if not zinr_list:
                    zinr_list = Zinr_list()
                    zinr_list_data.append(zinr_list)

                    zinr_list.resnr = res_line.resnr
                    zinr_list.reslinnr = res_line.reslinnr
                    zinr_list.zinr = genstat.zinr

                    queasy = get_cache (Queasy, {"key": [(eq, 14)],"char1": [(eq, genstat.zinr)],"date1": [(le, curr_date)],"date2": [(ge, curr_date)]})

                    if zimmer.sleeping and genstat.resstatus != 13:

                        if not queasy:
                            tot_rm = tot_rm + 1
                            tot_rmqty = tot_rmqty + 1

                        elif queasy and queasy.number3 != genstat.gastnr:
                            tot_rm = tot_rm + 1
                            tot_rmqty = tot_rmqty + 1

                    if zimmer.sleeping and (genstat.zipreis > 0 or genstat.zipreis == 0) and genstat.erwachs > 0 and genstat.resstatus != 13:

                        if not queasy:
                            tot_payrm = tot_payrm + 1

                        elif queasy and queasy.number3 != genstat.gastnr:
                            tot_payrm = tot_payrm + 1

                    elif not zimmer.sleeping:

                        if queasy and queasy.number3 != genstat.gastnr and genstat.zipreis > 0:
                            tot_rm = tot_rm + 1
                            tot_rmqty = tot_rmqty + 1
                        inactive = inactive + 1
                tot_a = tot_a + genstat.erwachs
                tot_c = tot_c + genstat.kind1 + genstat.kind2 + genstat.kind3
                tot_co = tot_co + genstat.gratis

                if exc_compli:
                    tot_co = 0

            if not disp_accompany:

                cl_list = query(cl_list_data, filters=(lambda cl_list: cl_list.rmno == res_line.zinr and cl_list.resnr == res_line.resnr and cl_list.arrive == res_line.ankunft and cl_list.zipreis == 0 and (cl_list.a + cl_list.c) < 1 and cl_list.co < 1), first=True)

                if cl_list:
                    cl_list_data.remove(cl_list)
                    pass

            if exc_compli:

                cl_list = query(cl_list_data, filters=(lambda cl_list: cl_list.rmno == res_line.zinr and cl_list.resnr == res_line.resnr and cl_list.arrive == res_line.ankunft and cl_list.co > 0), first=True)

                if cl_list:
                    cl_list_data.remove(cl_list)
                    pass
                    tot_rm = tot_rm - 1

        for cl_list in query(cl_list_data, sort_by=[("nation",False),("bezeich",False)]):

            mealcoup = get_cache (Mealcoup, {"name": [(eq, "breakfast")],"resnr": [(eq, cl_list.resnr)],"zinr": [(eq, cl_list.rmno)]})

            if mealcoup:
                cl_list.tot_bfast = mealcoup.verbrauch[0] + mealcoup.verbrauch[1] + mealcoup.verbrauch[2] + mealcoup.verbrauch[3] + mealcoup.verbrauch[4] +\
                        mealcoup.verbrauch[5] + mealcoup.verbrauch[6] + mealcoup.verbrauch[7] + mealcoup.verbrauch[8] + mealcoup.verbrauch[9] +\
                        mealcoup.verbrauch[10] + mealcoup.verbrauch[11] + mealcoup.verbrauch[12] + mealcoup.verbrauch[13] + mealcoup.verbrauch[14] +\
                        mealcoup.verbrauch[15] + mealcoup.verbrauch[16] + mealcoup.verbrauch[17] + mealcoup.verbrauch[18] + mealcoup.verbrauch[19] +\
                        mealcoup.verbrauch[20] + mealcoup.verbrauch[21] + mealcoup.verbrauch[22] + mealcoup.verbrauch[23] + mealcoup.verbrauch[24] +\
                        mealcoup.verbrauch[25] + mealcoup.verbrauch[26] + mealcoup.verbrauch[27] + mealcoup.verbrauch[28] + mealcoup.verbrauch[29] +\
                        mealcoup.verbrauch[30] + mealcoup.verbrauch[31]

            s_list = query(s_list_data, filters=(lambda s_list: s_list.bezeich == cl_list.bezeich), first=True)

            if not s_list:

                s_list = query(s_list_data, filters=(lambda s_list: s_list.rmcat == ""), first=True)

                if s_list:
                    s_list.rmcat = cl_list.kurzbez
                    s_list.bezeich = cl_list.bezeich

            if not s_list:
                s_list = S_list()
                s_list_data.append(s_list)

                s_list.rmcat = cl_list.kurzbez
                s_list.bezeich = cl_list.bezeich
            s_list.anz = s_list.anz + cl_list.qty

            s_list = query(s_list_data, filters=(lambda s_list: s_list.nat == cl_list.nat), first=True)

            if not s_list:

                s_list = query(s_list_data, filters=(lambda s_list: s_list.nat == ""), first=True)

                if s_list:
                    s_list.nat = cl_list.nat

            if not s_list:
                s_list = S_list()
                s_list_data.append(s_list)


                if s_list:
                    s_list.nat = cl_list.nat
            s_list.adult = s_list.adult + cl_list.a + cl_list.co
            s_list.child = s_list.child + cl_list.c
            s_list.rmqty = s_list.rmqty + cl_list.qty

        if (tot_a + tot_co) != 0:

            for s_list in query(s_list_data, filters=(lambda s_list: s_list.nat != "")):

                nation = get_cache (Nation, {"kurzbez": [(eq, s_list.nat)]})

                if nation:
                    s_list.nat = nation.bezeich
                s_list.proz =  to_decimal(s_list.adult) / to_decimal((tot_a) + to_decimal(tot_co)) * to_decimal("100")

        # sort by rmno -> query diatas merubah sort order.-------------------
        for cl_list in query(cl_list_data, sort_by=[("rmno",False)]):
            pass
        #--------------------------------------------------------------------

    def create_inhouse2():
        # sorttype = 1
        nonlocal tot_payrm, tot_rm, tot_a, tot_c, tot_co, tot_avail, tot_rmqty, inactive, cl_list_data, s_list_data, t_buff_queasy_data, vipnr1, vipnr2, vipnr3, vipnr4, vipnr5, vipnr6, vipnr7, vipnr8, vipnr9, tot_room, all_room, all_remark, queasy, htparam, zkstat, zinrstat, paramtext, guest, reservation, zimmer, zimkateg, res_line, guestseg, segment, mc_guest, mc_types, nation, waehrung, reslin_queasy, mealcoup, genstat
        nonlocal sorttype, datum, curr_date, curr_gastnr, froom, troom, exc_depart, incl_gcomment, incl_rsvcomment, prog_name, disp_accompany, disp_exclinact, split_rsv_print, exc_compli


        nonlocal setup_list, str_list, cl_list, s_list, zinr_list, t_buff_queasy
        nonlocal setup_list_data, str_list_data, cl_list_data, s_list_data, zinr_list_data, t_buff_queasy_data

        i:int = 0
        j:int = 0
        vip_flag:string = ""
        nr:int = 0
        str:string = ""
        actflag1:int = 0
        actflag2:int = 0
        do_it:bool = False
        gmember = None
        gbuff = None
        rbuff = None
        Gmember =  create_buffer("Gmember",Guest)
        Gbuff =  create_buffer("Gbuff",Guest)
        Rbuff =  create_buffer("Rbuff",Reservation)
        zinr_list_data.clear()

        if datum == curr_date:
            actflag1 = 1
            actflag2 = 1
        else:
            actflag1 = 1
            actflag2 = 2
        tot_payrm = 0
        tot_rm = 0
        tot_a = 0
        tot_c = 0
        tot_co = 0
        inactive = 0
        s_list_data.clear()
        cl_list_data.clear()
        str_list_data.clear()
        tot_avail = 0

        for zimmer in db_session.query(Zimmer).filter(
                 (Zimmer.sleeping)).order_by(Zimmer._recid).all():
            tot_avail = tot_avail + 1

        res_line_obj_list = {}
        res_line = Res_line()
        zimkateg = Zimkateg()
        reservation = Reservation()
        guest = Guest()
        gmember = Guest()
        zimmer = Zimmer()
        for res_line.setup, res_line.zinr, res_line.resnr, res_line.name, res_line.zipreis, res_line.ankunft, res_line.abreise, res_line.zimmeranz, res_line.erwachs, \
            res_line.kind1, res_line.kind2, res_line.gratis, res_line.arrangement, res_line.flight_nr, res_line.ankzeit, res_line.resstatus, res_line.betriebsnr, \
            res_line.reslinnr, res_line.zimmer_wunsch, res_line.zimmerfix, res_line.gastnrmember, res_line.bemerk, res_line.gastnr, res_line._recid, \
            zimkateg.kurzbez, zimkateg.bezeichnung, zimkateg._recid, reservation.segmentcode, reservation.resdat, reservation.useridanlage, reservation.resnr, \
            reservation._recid, guest.name, guest.vorname1, guest.anrede1, guest.anredefirma, guest.gastnr, guest.karteityp, guest._recid, gmember.name, \
            gmember.vorname1, gmember.anrede1, gmember.anredefirma, gmember.gastnr, gmember.karteityp, gmember._recid, zimmer.etage, zimmer.bezeich, \
            zimmer.sleeping, zimmer._recid, gmember.nation1, gmember.nation2, gmember.email_adr, gmember.geburtdatum1, gmember.telefon, gmember.mobil_telefon \
            in db_session.query(Res_line.setup, Res_line.zinr, Res_line.resnr, Res_line.name, Res_line.zipreis, Res_line.ankunft, Res_line.abreise, \
                                Res_line.zimmeranz, Res_line.erwachs, Res_line.kind1, Res_line.kind2, Res_line.gratis, Res_line.arrangement, \
                                Res_line.flight_nr, Res_line.ankzeit, Res_line.resstatus, Res_line.betriebsnr, Res_line.reslinnr, Res_line.zimmer_wunsch, \
                                Res_line.zimmerfix, Res_line.gastnrmember, Res_line.bemerk, Res_line.gastnr, Res_line._recid, Zimkateg.kurzbez, \
                                Zimkateg.bezeichnung, Zimkateg._recid, Reservation.segmentcode, Reservation.resdat, Reservation.useridanlage, \
                                Reservation.resnr, Reservation._recid, Guest.name, Guest.vorname1, Guest.anrede1, Guest.anredefirma, Guest.gastnr, \
                                Guest.karteityp, Guest._recid, Gmember.name, Gmember.vorname1, Gmember.anrede1, Gmember.anredefirma, Gmember.gastnr, \
                                Gmember.karteityp, Gmember._recid, Zimmer.etage, Zimmer.bezeich, Zimmer.sleeping, Zimmer._recid, Gmember.nation1, \
                                    Gmember.nation2, Gmember.email_adr, Gmember.geburtdatum1, Gmember.telefon, Gmember.mobil_telefon)\
                                    .join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).join(Reservation,(Reservation.resnr == Res_line.resnr))\
                                    .join(Guest,(Guest.gastnr == Reservation.gastnr)).join(Gmember,(Gmember.gastnr == Res_line.gastnrmember))\
                                    .join(Zimmer,(Zimmer.zinr == Res_line.zinr) & (Zimmer.sleeping)).filter(
                 (Res_line.active_flag >= actflag1) & (Res_line.active_flag <= actflag2) & (Res_line.resstatus != 9) & (Res_line.resstatus != 10) & 
                 (Res_line.resstatus != 12) & (Res_line.ankunft <= datum) & (Res_line.abreise >= datum) & (Res_line.zinr >= (froom).lower()) & 
                (Res_line.zinr <= (troom).lower())).order_by(Res_line.zinr, Res_line.erwachs.desc(), Res_line.name).all():
            if res_line_obj_list.get(res_line._recid):
                continue
            else:
                res_line_obj_list[res_line._recid] = True

            if exc_depart and res_line.abreise == datum:
                pass
            else:

                setup_list = query(setup_list_data, filters=(lambda setup_list: setup_list.nr == res_line.setup + 1), first=True)
                nr = nr + 1
                vip_flag = ""

                guestseg = db_session.query(Guestseg).filter(
                         (Guestseg.gastnr == gmember.gastnr) & ((Guestseg.segmentcode == vipnr1) | (Guestseg.segmentcode == vipnr2) | (Guestseg.segmentcode == vipnr3) | (Guestseg.segmentcode == vipnr4) | (Guestseg.segmentcode == vipnr5) | (Guestseg.segmentcode == vipnr6) | (Guestseg.segmentcode == vipnr7) | (Guestseg.segmentcode == vipnr8) | (Guestseg.segmentcode == vipnr9))).first()

                if guestseg:

                    segment = get_cache (Segment, {"segmentcode": [(eq, guestseg.segmentcode)]})
                    vip_flag = segment.bezeich


                cl_list = Cl_list()
                cl_list_data.append(cl_list)

                cl_list.nr = nr
                cl_list.rmcat = zimkateg.kurzbez + setup_list.char
                cl_list.kurzbez = zimkateg.kurzbez
                cl_list.bezeich = zimkateg.bezeichnung
                cl_list.nat = gmember.nation1
                cl_list.resnr = res_line.resnr
                cl_list.vip = vip_flag
                cl_list.name = res_line.name
                cl_list.rmno = res_line.zinr
                cl_list.zipreis =  to_decimal(res_line.zipreis)
                cl_list.arrive = res_line.ankunft
                cl_list.depart = res_line.abreise
                cl_list.qty = res_line.zimmeranz
                cl_list.a = res_line.erwachs
                cl_list.c = res_line.kind1 + res_line.kind2
                cl_list.co = res_line.gratis
                cl_list.argt = res_line.arrangement
                cl_list.flight = substring(res_line.flight_nr, 11, 6)
                cl_list.etd = substring(res_line.flight_nr, 17, 5)
                cl_list.ci_time = to_string(res_line.ankzeit, "HH:MM")
                cl_list.paym = reservation.segmentcode
                cl_list.created = reservation.resdat
                cl_list.createid = reservation.useridanlage
                cl_list.etage = zimmer.etage
                cl_list.zinr_bez = zimmer.bezeich
                cl_list.birthdate = gmember.geburtdatum1
                cl_list.telefon = gmember.telefon
                cl_list.mobil_tel = gmember.mobil_telefon

                if res_line.resstatus != 11 and res_line.resstatus != 13:
                    cl_list.flag_guest = 1


                else:
                    cl_list.flag_guest = 2

                mc_guest = get_cache (Mc_guest, {"gastnr": [(eq, gmember.gastnr)]})

                if mc_guest:
                    cl_list.telefon = gmember.telefon + ";" + mc_guest.cardnum

                    mc_types = get_cache (Mc_types, {"nr": [(eq, mc_guest.nr)]})

                    if mc_types:
                        cl_list.mobil_tel = gmember.mobil_telefon + ";" + mc_types.bezeich
                    else:
                        cl_list.mobil_tel = gmember.mobil_telefon
                else:
                    cl_list.telefon = gmember.telefon

                nation = get_cache (Nation, {"kurzbez": [(eq, gmember.nation2)]})

                if nation:
                    cl_list.local_reg = nation.bezeich

                waehrung = get_cache (Waehrung, {"waehrungsnr": [(eq, res_line.betriebsnr)]})

                if waehrung:
                    cl_list.curr = waehrung.wabkurz + ";" + gmember.email_adr

                reslin_queasy = get_cache (Reslin_queasy, {"key": [(eq, "specialrequest")],"resnr": [(eq, res_line.resnr)],"reslinnr": [(eq, res_line.reslinnr)]})

                if reslin_queasy:
                    cl_list.spreq = reslin_queasy.char3 + "," + cl_list.spreq

                reslin_queasy = get_cache (Reslin_queasy, {"key": [(eq, "arrangement")],"resnr": [(eq, res_line.resnr)],"reslinnr": [(eq, res_line.reslinnr)],"date1": [(le, datum)],"date2": [(ge, datum)]})

                if reslin_queasy:

                    if reslin_queasy.char2 != "":
                        cl_list.ratecode = reslin_queasy.char2
                    else:
                        for i in range(1,num_entries(res_line.zimmer_wunsch, ";") - 1 + 1) :
                            str = entry(i - 1, res_line.zimmer_wunsch, ";")

                            if substring(str, 0, 6) == ("$CODE$").lower() :
                                cl_list.ratecode = substring(str, 6)
                                break

                mealcoup = get_cache (Mealcoup, {"name": [(eq, "breakfast")],"resnr": [(eq, res_line.resnr)],"zinr": [(eq, res_line.zinr)]})

                if mealcoup:
                    cl_list.tot_bfast = mealcoup.verbrauch[0] + mealcoup.verbrauch[1] + mealcoup.verbrauch[2] + mealcoup.verbrauch[3] + mealcoup.verbrauch[4] +\
                            mealcoup.verbrauch[5] + mealcoup.verbrauch[6] + mealcoup.verbrauch[7] + mealcoup.verbrauch[8] + mealcoup.verbrauch[9] +\
                            mealcoup.verbrauch[10] + mealcoup.verbrauch[11] + mealcoup.verbrauch[12] + mealcoup.verbrauch[13] + mealcoup.verbrauch[14] +\
                            mealcoup.verbrauch[15] + mealcoup.verbrauch[16] + mealcoup.verbrauch[17] + mealcoup.verbrauch[18] + mealcoup.verbrauch[19] +\
                            mealcoup.verbrauch[20] + mealcoup.verbrauch[21] + mealcoup.verbrauch[22] + mealcoup.verbrauch[23] + mealcoup.verbrauch[24] +\
                            mealcoup.verbrauch[25] + mealcoup.verbrauch[26] + mealcoup.verbrauch[27] + mealcoup.verbrauch[28] + mealcoup.verbrauch[29] +\
                            mealcoup.verbrauch[30] + mealcoup.verbrauch[31]

                segment = get_cache (Segment, {"segmentcode": [(eq, reservation.segmentcode)]})

                if segment:
                    cl_list.segm = entry(0, segment.bezeich, "$$0")

                if guest.karteityp != 0:
                    cl_list.company = guest.name + ", " + guest.vorname1 + " " + guest.anrede1 + guest.anredefirma
                else:
                    cl_list.company = guest.name + ", " + guest.vorname1 + " " + guest.anrede1 + guest.anredefirma

                if cl_list.nat == "":
                    cl_list.nat = "?"

                if res_line.resstatus == 13 or res_line.zimmerfix:
                    cl_list.qty = 0

                if not split_rsv_print:

                    if incl_gcomment:

                        gbuff = get_cache (Guest, {"gastnr": [(eq, res_line.gastnrmember)]})

                        if gbuff:
                            for i in range(1,length(gbuff.bemerkung)  + 1) :

                                if substring(gbuff.bemerkung, i - 1, 1) == chr_unicode(10):
                                    cl_list.bemerk = cl_list.bemerk + " "
                                else:
                                    cl_list.bemerk = cl_list.bemerk + substring(trim(gbuff.bemerkung) , i - 1, 1)
                        cl_list.bemerk = cl_list.bemerk + " || "

                    if incl_rsvcomment:

                        rbuff = get_cache (Reservation, {"resnr": [(eq, reservation.resnr)]})

                        if rbuff:
                            for j in range(1,length(rbuff.bemerk)  + 1) :

                                if substring(rbuff.bemerk, j - 1, 1) == chr_unicode(10):
                                    cl_list.bemerk1 = cl_list.bemerk1 + " "
                                else:
                                    cl_list.bemerk1 = cl_list.bemerk1 + substring(trim(rbuff.bemerk) , j - 1, 1)
                        cl_list.bemerk = cl_list.bemerk + cl_list.bemerk1 + " || "
                    for i in range(1,length(res_line.bemerk)  + 1) :

                        if substring(res_line.bemerk, i - 1, 1) == chr_unicode(10):
                            cl_list.bemerk = cl_list.bemerk + " "
                        else:
                            cl_list.bemerk = cl_list.bemerk + substring(trim(res_line.bemerk) , i - 1, 1)
                    all_remark = res_line.bemerk
                    all_remark = replace_str(all_remark, chr_unicode(10) , " ")
                    all_remark = replace_str(all_remark, chr_unicode(13) , " ")
                    cl_list.bemerk01 = to_string(substring(all_remark, 0, 225))
                    cl_list.bemerk02 = to_string(substring(all_remark, 225, 225))
                    cl_list.bemerk03 = to_string(substring(all_remark, 450, 225))
                    cl_list.bemerk04 = to_string(substring(all_remark, 675, 225))
                else:
                    for i in range(1,length(res_line.bemerk)  + 1) :
                        cl_list.bemerk = cl_list.bemerk + substring(trim(res_line.bemerk) , i - 1, 1)

                    rbuff = get_cache (Reservation, {"resnr": [(eq, reservation.resnr)]})

                    if rbuff:
                        cl_list.rsv_comment = rbuff.bemerk

                    gbuff = get_cache (Guest, {"gastnr": [(eq, res_line.gastnrmember)]})

                    if gbuff:
                        cl_list.g_comment = gbuff.bemerkung

                    queasy = get_cache (Queasy, {"key": [(eq, 267)],"number1": [(eq, res_line.resnr)],"number2": [(eq, res_line.reslinnr)]})

                    if queasy:
                        cl_list.other_comment = queasy.char1
                cl_list.pax = to_string(cl_list.a, ">9") + "/" + to_string(cl_list.c, "9") + " " + to_string(cl_list.co, "9")

                if cl_list.nat == "":
                    cl_list.nat = "?"
                else:

                    nation = get_cache (Nation, {"kurzbez": [(eq, cl_list.nat)]})

                    if nation:
                        cl_list.nation = nation.bezeich

                zinr_list = query(zinr_list_data, filters=(lambda zinr_list: zinr_list.zinr == res_line.zinr and zinr_list.resnr == res_line.resnr and zinr_list.reslinnr == res_line.reslinnr), first=True)

                if not zinr_list:
                    zinr_list = Zinr_list()
                    zinr_list_data.append(zinr_list)

                    zinr_list.resnr = res_line.resnr
                    zinr_list.reslinnr = res_line.reslinnr
                    zinr_list.zinr = res_line.zinr

                    queasy = get_cache (Queasy, {"key": [(eq, 14)],"char1": [(eq, res_line.zinr)],"date1": [(le, curr_date)],"date2": [(ge, curr_date)]})

                    if zimmer.sleeping and res_line.resstatus != 13:

                        if not queasy:
                            tot_rm = tot_rm + res_line.zimmeranz
                            tot_rmqty = tot_rmqty + res_line.zimmeranz

                        elif queasy and queasy.number3 != res_line.gastnr:
                            tot_rm = tot_rm + res_line.zimmeranz
                            tot_rmqty = tot_rmqty + res_line.zimmeranz

                    if zimmer.sleeping and (res_line.zipreis > 0 or res_line.zipreis == 0) and res_line.resstatus != 13 and res_line.erwachs > 0:

                        if not queasy:
                            tot_payrm = tot_payrm + res_line.zimmeranz

                        elif queasy and queasy.number3 != res_line.gastnr:
                            tot_payrm = tot_payrm + res_line.zimmeranz

                    elif not zimmer.sleeping:

                        if queasy and queasy.number3 != res_line.gastnr and res_line.zipreis > 0:
                            tot_rm = tot_rm + res_line.zimmeranz
                            tot_rmqty = tot_rmqty + res_line.zimmeranz
                        inactive = inactive + 1
                tot_a = tot_a + res_line.erwachs
                tot_c = tot_c + res_line.kind1 + res_line.kind2
                tot_co = tot_co + res_line.gratis

                if exc_compli:
                    tot_co = 0

            if not disp_accompany:

                cl_list = query(cl_list_data, filters=(lambda cl_list: cl_list.rmno == res_line.zinr and cl_list.resnr == res_line.resnr and cl_list.arrive == res_line.ankunft and cl_list.zipreis == 0 and (cl_list.a + cl_list.c) < 1 and cl_list.co < 1), first=True)

                if cl_list:
                    cl_list_data.remove(cl_list)
                    pass

            if exc_compli:

                cl_list = query(cl_list_data, filters=(lambda cl_list: cl_list.rmno == res_line.zinr and cl_list.resnr == res_line.resnr and cl_list.arrive == res_line.ankunft and cl_list.co > 0), first=True)

                if cl_list:
                    cl_list_data.remove(cl_list)
                    pass
                    tot_rm = tot_rm - 1

        for cl_list in query(cl_list_data, sort_by=[("nation",False),("bezeich",False)]):

            s_list = query(s_list_data, filters=(lambda s_list: s_list.rmcat == cl_list.kurzbez), first=True)

            if not s_list:

                s_list = query(s_list_data, filters=(lambda s_list: s_list.rmcat == ""), first=True)

                if s_list:
                    s_list.rmcat = cl_list.kurzbez
                    s_list.bezeich = cl_list.bezeich

            if not s_list:
                s_list = S_list()
                s_list_data.append(s_list)

                s_list.rmcat = cl_list.kurzbez
                s_list.bezeich = cl_list.bezeich
            s_list.anz = s_list.anz + cl_list.qty

            s_list = query(s_list_data, filters=(lambda s_list: s_list.nat == cl_list.nat), first=True)

            if not s_list:

                s_list = query(s_list_data, filters=(lambda s_list: s_list.nat == ""), first=True)

                if s_list:
                    s_list.nat = cl_list.nat

            if not s_list:
                s_list = S_list()
                s_list_data.append(s_list)


                if s_list:
                    s_list.nat = cl_list.nat
            s_list.adult = s_list.adult + cl_list.a + cl_list.co
            s_list.child = s_list.child + cl_list.c
            s_list.rmqty = s_list.rmqty + cl_list.qty

        if (tot_a + tot_co) != 0:

            for s_list in query(s_list_data, filters=(lambda s_list: s_list.nat != "")):

                nation = get_cache (Nation, {"kurzbez": [(eq, s_list.nat)]})

                if nation:
                    s_list.nat = nation.bezeich
                s_list.proz =  to_decimal(s_list.adult) / to_decimal((tot_a) + to_decimal(tot_co)) * to_decimal("100")

        # sort by rmno -> query diatas merubah sort order.-------------------
        for cl_list in query(cl_list_data, sort_by=[("rmno",False)]):
            pass
        #--------------------------------------------------------------------

    def create_genstat_inhouse2():
        # sorttype = 1
        nonlocal tot_payrm, tot_rm, tot_a, tot_c, tot_co, tot_avail, tot_rmqty, inactive, cl_list_data, s_list_data, t_buff_queasy_data, vipnr1, vipnr2, vipnr3, vipnr4, vipnr5, vipnr6, vipnr7, vipnr8, vipnr9, tot_room, all_room, all_remark, queasy, htparam, zkstat, zinrstat, paramtext, guest, reservation, zimmer, zimkateg, res_line, guestseg, segment, mc_guest, mc_types, nation, waehrung, reslin_queasy, mealcoup, genstat
        nonlocal sorttype, datum, curr_date, curr_gastnr, froom, troom, exc_depart, incl_gcomment, incl_rsvcomment, prog_name, disp_accompany, disp_exclinact, split_rsv_print, exc_compli


        nonlocal setup_list, str_list, cl_list, s_list, zinr_list, t_buff_queasy
        nonlocal setup_list_data, str_list_data, cl_list_data, s_list_data, zinr_list_data, t_buff_queasy_data

        i:int = 0
        j:int = 0
        vip_flag:string = ""
        nr:int = 0
        str:string = ""
        actflag1:int = 0
        actflag2:int = 0
        do_it:bool = False
        gmember = None
        gbuff = None
        rbuff = None
        z:int = 0
        Gmember =  create_buffer("Gmember",Guest)
        Gbuff =  create_buffer("Gbuff",Guest)
        Rbuff =  create_buffer("Rbuff",Reservation)
        zinr_list_data.clear()

        if datum == curr_date:
            actflag1 = 1
            actflag2 = 1
        else:
            actflag1 = 1
            actflag2 = 2
        tot_payrm = 0
        tot_rm = 0
        tot_a = 0
        tot_c = 0
        tot_co = 0
        inactive = 0
        s_list_data.clear()
        cl_list_data.clear()
        str_list_data.clear()
        tot_avail = 0

        for zkstat in db_session.query(Zkstat).filter(
                 (Zkstat.datum == datum)).order_by(Zkstat._recid).all():
            tot_avail = tot_avail + zkstat.anz100

        genstat_obj_list = {}
        genstat = Genstat()
        zimkateg = Zimkateg()
        reservation = Reservation()
        guest = Guest()
        gmember = Guest()
        zimmer = Zimmer()
        for genstat.resstatus, genstat.res_date, genstat.resnr, genstat.res_int, genstat.zinr, genstat.zipreis, genstat.erwachs, genstat.kind1, genstat.kind2, genstat.kind3, genstat.gratis, \
            genstat.argt, genstat.segmentcode, genstat.gastnr, genstat._recid, zimkateg.kurzbez, zimkateg.bezeichnung, zimkateg._recid, reservation.segmentcode, reservation.resdat, \
            reservation.useridanlage, reservation.resnr, reservation._recid, guest.name, guest.vorname1, guest.anrede1, guest.anredefirma, guest.gastnr, guest.karteityp, guest._recid, \
            gmember.name, gmember.vorname1, gmember.anrede1, gmember.anredefirma, gmember.gastnr, gmember.karteityp, gmember._recid, zimmer.etage, zimmer.bezeich, \
            zimmer.sleeping, zimmer._recid, gmember.nation1, gmember.nation2, gmember.email_adr, gmember.geburtdatum1, gmember.telefon, gmember.mobil_telefon \
            in db_session.query(Genstat.resstatus, Genstat.res_date, Genstat.resnr, Genstat.res_int, Genstat.zinr, Genstat.zipreis, Genstat.erwachs, Genstat.kind1, Genstat.kind2, \
                                Genstat.kind3, Genstat.gratis, Genstat.argt, Genstat.segmentcode, Genstat.gastnr, Genstat._recid, Zimkateg.kurzbez, Zimkateg.bezeichnung, Zimkateg._recid, \
                                Reservation.segmentcode, Reservation.resdat, Reservation.useridanlage, Reservation.resnr, Reservation._recid, Guest.name, Guest.vorname1, Guest.anrede1, \
                                Guest.anredefirma, Guest.gastnr, Guest.karteityp, Guest._recid, Gmember.name, Gmember.vorname1, Gmember.nation2, Gmember.anrede1, Gmember.anredefirma, \
                                Gmember.gastnr, Gmember.karteityp, Gmember._recid, Zimmer.etage, Zimmer.bezeich, Zimmer.sleeping, Zimmer._recid, Gmember.nation1, Gmember.email_adr, Gmember.geburtdatum1, Gmember.telefon, Gmember.mobil_telefon)\
                            .join(Zimkateg,(Zimkateg.zikatnr == Genstat.zikatnr))\
                            .join(Reservation,(Reservation.resnr == Genstat.resnr))\
                            .join(Guest,(Guest.gastnr == Genstat.gastnr))\
                            .join(Gmember,(Gmember.gastnr == Genstat.gastnrmember))\
                            .join(Zimmer,(Zimmer.zinr == Genstat.zinr) & (Zimmer.sleeping))\
                        .filter(
                            (Genstat.datum == datum) & 
                            (Genstat.zinr >= (froom).lower()) & 
                            (Genstat.zinr <= (troom).lower()))\
                        .order_by(Genstat.zinr, Genstat.erwachs.desc(), Gmember.name).all():
            if genstat_obj_list.get(genstat._recid):
                continue
            else:
                genstat_obj_list[genstat._recid] = True

            if genstat.res_date[0] < datum and genstat.res_date[1] == datum and genstat.resstatus == 8:
                pass

            elif exc_depart and genstat.res_date[0] <= datum and genstat.res_date[1] == datum and genstat.resstatus == 8:
                pass
            else:

                res_line = get_cache (Res_line, {"resnr": [(eq, genstat.resnr)],"reslinnr": [(eq, genstat.res_int[0])]})

                setup_list = query(setup_list_data, filters=(lambda setup_list: setup_list.nr == res_line.setup + 1), first=True)
                nr = nr + 1
                vip_flag = ""

                guestseg = db_session.query(Guestseg).filter(
                         (Guestseg.gastnr == gmember.gastnr) & ((Guestseg.segmentcode == vipnr1) | (Guestseg.segmentcode == vipnr2) | (Guestseg.segmentcode == vipnr3) | (Guestseg.segmentcode == vipnr4) | (Guestseg.segmentcode == vipnr5) | (Guestseg.segmentcode == vipnr6) | (Guestseg.segmentcode == vipnr7) | (Guestseg.segmentcode == vipnr8) | (Guestseg.segmentcode == vipnr9))).first()

                if guestseg:

                    segment = get_cache (Segment, {"segmentcode": [(eq, guestseg.segmentcode)]})
                    vip_flag = replace_str(segment.bezeich, " ", "")
                cl_list = Cl_list()
                cl_list_data.append(cl_list)

                cl_list.nr = nr
                cl_list.rmcat = zimkateg.kurzbez + setup_list.char
                cl_list.kurzbez = zimkateg.kurzbez
                cl_list.bezeich = zimkateg.bezeichnung
                cl_list.nat = gmember.nation1
                cl_list.resnr = genstat.resnr
                cl_list.vip = vip_flag
                cl_list.name = gmember.name + ", " + gmember.vorname1 +\
                        " " + gmember.anrede1
                cl_list.rmno = genstat.zinr
                cl_list.zipreis =  to_decimal(genstat.zipreis)
                cl_list.arrive = genstat.res_date[0]
                cl_list.depart = genstat.res_date[1]
                cl_list.qty = 1
                cl_list.a = genstat.erwachs
                cl_list.c = genstat.kind1 + genstat.kind2 + genstat.kind3
                cl_list.co = genstat.gratis
                cl_list.argt = genstat.argt
                cl_list.flight = substring(res_line.flight_nr, 11, 6)
                cl_list.etd = substring(res_line.flight_nr, 17, 5)
                cl_list.ci_time = to_string(res_line.ankzeit, "HH:MM")
                cl_list.paym = genstat.segmentcode
                cl_list.created = reservation.resdat
                cl_list.createid = reservation.useridanlage
                cl_list.etage = zimmer.etage
                cl_list.zinr_bez = zimmer.bezeich
                cl_list.birthdate = gmember.geburtdatum1
                cl_list.telefon = gmember.telefon
                cl_list.mobil_tel = gmember.mobil_telefon

                if res_line.resstatus != 11 and res_line.resstatus != 13:
                    cl_list.flag_guest = 1


                else:
                    cl_list.flag_guest = 2

                mc_guest = get_cache (Mc_guest, {"gastnr": [(eq, gmember.gastnr)]})

                if mc_guest:
                    cl_list.telefon = gmember.telefon + ";" + mc_guest.cardnum

                    mc_types = get_cache (Mc_types, {"nr": [(eq, mc_guest.nr)]})

                    if mc_types:
                        cl_list.mobil_tel = gmember.mobil_telefon + ";" + mc_types.bezeich
                    else:
                        cl_list.mobil_tel = gmember.mobil_telefon
                else:
                    cl_list.telefon = gmember.telefon

                nation = get_cache (Nation, {"kurzbez": [(eq, gmember.nation2)]})

                if nation:
                    cl_list.local_reg = nation.bezeich

                waehrung = get_cache (Waehrung, {"waehrungsnr": [(eq, res_line.betriebsnr)]})

                if waehrung:
                    cl_list.curr = waehrung.wabkurz + ";" + gmember.email_adr

                reslin_queasy = get_cache (Reslin_queasy, {"key": [(eq, "specialrequest")],"resnr": [(eq, res_line.resnr)],"reslinnr": [(eq, res_line.reslinnr)]})

                if reslin_queasy:
                    cl_list.spreq = reslin_queasy.char3 + "," + cl_list.spreq

                reslin_queasy = get_cache (Reslin_queasy, {"key": [(eq, "arrangement")],"resnr": [(eq, res_line.resnr)],"reslinnr": [(eq, res_line.reslinnr)],"date1": [(le, datum)],"date2": [(ge, datum)]})

                if reslin_queasy:

                    if reslin_queasy.char2 != "":
                        cl_list.ratecode = reslin_queasy.char2
                    else:
                        for i in range(1,num_entries(res_line.zimmer_wunsch, ";") - 1 + 1) :
                            str = entry(i - 1, res_line.zimmer_wunsch, ";")

                            if substring(str, 0, 6) == ("$CODE$").lower() :
                                cl_list.ratecode = substring(str, 6)
                                break

                segment = get_cache (Segment, {"segmentcode": [(eq, genstat.segmentcode)]})

                if segment:
                    cl_list.segm = entry(0, segment.bezeich, "$$0")

                if guest.karteityp != 0:
                    cl_list.company = guest.name + ", " + guest.vorname1 + " " + guest.anrede1 + guest.anredefirma
                else:
                    cl_list.company = guest.name + ", " + guest.vorname1 + " " + guest.anrede1 + guest.anredefirma

                if cl_list.nat == "":
                    cl_list.nat = "?"

                if genstat.resstatus == 13:
                    cl_list.qty = 0

                if not split_rsv_print:

                    if incl_gcomment:

                        gbuff = get_cache (Guest, {"gastnr": [(eq, res_line.gastnrmember)]})

                        if gbuff:
                            for i in range(1,length(gbuff.bemerkung)  + 1) :

                                if substring(gbuff.bemerkung, i - 1, 1) == chr_unicode(10):
                                    cl_list.bemerk = cl_list.bemerk + " "
                                else:
                                    cl_list.bemerk = cl_list.bemerk + substring(trim(gbuff.bemerkung) , i - 1, 1)
                        cl_list.bemerk = cl_list.bemerk + " || "

                    if incl_rsvcomment:

                        rbuff = get_cache (Reservation, {"resnr": [(eq, reservation.resnr)]})

                        if rbuff:
                            for j in range(1,length(rbuff.bemerk)  + 1) :

                                if substring(rbuff.bemerk, j - 1, 1) == chr_unicode(10):
                                    cl_list.bemerk1 = cl_list.bemerk1 + " "
                                else:
                                    cl_list.bemerk1 = cl_list.bemerk1 + substring(trim(rbuff.bemerk) , j - 1, 1)
                        cl_list.bemerk = cl_list.bemerk + cl_list.bemerk1 + " || "
                    for i in range(1,length(res_line.bemerk)  + 1) :

                        if substring(res_line.bemerk, i - 1, 1) == chr_unicode(10):
                            cl_list.bemerk = cl_list.bemerk + " "
                        else:
                            cl_list.bemerk = cl_list.bemerk + substring(trim(res_line.bemerk) , i - 1, 1)
                    all_remark = res_line.bemerk
                    all_remark = replace_str(all_remark, chr_unicode(10) , " ")
                    all_remark = replace_str(all_remark, chr_unicode(13) , " ")
                    cl_list.bemerk01 = to_string(substring(all_remark, 0, 225))
                    cl_list.bemerk02 = to_string(substring(all_remark, 225, 225))
                    cl_list.bemerk03 = to_string(substring(all_remark, 450, 225))
                    cl_list.bemerk04 = to_string(substring(all_remark, 675, 225))
                else:
                    for i in range(1,length(res_line.bemerk)  + 1) :
                        cl_list.bemerk = cl_list.bemerk + substring(trim(res_line.bemerk) , i - 1, 1)

                    rbuff = get_cache (Reservation, {"resnr": [(eq, reservation.resnr)]})

                    if rbuff:
                        cl_list.rsv_comment = rbuff.bemerk

                    gbuff = get_cache (Guest, {"gastnr": [(eq, res_line.gastnrmember)]})

                    if gbuff:
                        cl_list.g_comment = gbuff.bemerkung

                    queasy = get_cache (Queasy, {"key": [(eq, 267)],"number1": [(eq, res_line.resnr)],"number2": [(eq, res_line.reslinnr)]})

                    if queasy:
                        cl_list.other_comment = queasy.char1
                cl_list.pax = to_string(cl_list.a, ">9") + "/" + to_string(cl_list.c, "9") + " " + to_string(cl_list.co, "9")

                if cl_list.nat == "":
                    cl_list.nat = "?"
                else:

                    nation = get_cache (Nation, {"kurzbez": [(eq, cl_list.nat)]})

                    if nation:
                        cl_list.nation = nation.bezeich

                zinr_list = query(zinr_list_data, filters=(lambda zinr_list: zinr_list.zinr == genstat.zinr and zinr_list.resnr == res_line.resnr and zinr_list.reslinnr == res_line.reslinnr), first=True)

                if not zinr_list:
                    zinr_list = Zinr_list()
                    zinr_list_data.append(zinr_list)

                    zinr_list.resnr = res_line.resnr
                    zinr_list.reslinnr = res_line.reslinnr
                    zinr_list.zinr = genstat.zinr

                    queasy = get_cache (Queasy, {"key": [(eq, 14)],"char1": [(eq, genstat.zinr)],"date1": [(le, curr_date)],"date2": [(ge, curr_date)]})

                    if zimmer.sleeping and genstat.resstatus != 13:

                        if not queasy:
                            tot_rm = tot_rm + 1
                            tot_rmqty = tot_rmqty + 1

                        elif queasy and queasy.number3 != genstat.gastnr:
                            tot_rm = tot_rm + 1
                            tot_rmqty = tot_rmqty + 1

                    if zimmer.sleeping and (genstat.zipreis > 0 or genstat.zipreis == 0) and genstat.erwachs > 0 and genstat.resstatus != 13:
                        z = z + 1

                        if not queasy:
                            tot_payrm = tot_payrm + 1

                        elif queasy and queasy.number3 != genstat.gastnr:
                            tot_payrm = tot_payrm + 1

                    elif not zimmer.sleeping:

                        if queasy and queasy.number3 != genstat.gastnr and genstat.zipreis > 0:
                            tot_rm = tot_rm + 1
                            tot_rmqty = tot_rmqty + 1
                        inactive = inactive + 1
                tot_a = tot_a + genstat.erwachs
                tot_c = tot_c + genstat.kind1 + genstat.kind2 + genstat.kind3
                tot_co = tot_co + genstat.gratis

                if exc_compli:
                    tot_co = 0

            if not disp_accompany:

                cl_list = query(cl_list_data, filters=(lambda cl_list: cl_list.rmno == res_line.zinr and cl_list.resnr == res_line.resnr and cl_list.arrive == res_line.ankunft and cl_list.zipreis == 0 and (cl_list.a + cl_list.c) < 1 and cl_list.co < 1), first=True)

                if cl_list:
                    cl_list_data.remove(cl_list)
                    pass

            if exc_compli:

                cl_list = query(cl_list_data, filters=(lambda cl_list: cl_list.rmno == res_line.zinr and cl_list.resnr == res_line.resnr and cl_list.arrive == res_line.ankunft and cl_list.co > 0), first=True)

                if cl_list:
                    cl_list_data.remove(cl_list)
                    pass
                    tot_rm = tot_rm - 1

        for cl_list in query(cl_list_data, sort_by=[("nation",False),("bezeich",False)]):

            mealcoup = get_cache (Mealcoup, {"name": [(eq, "breakfast")],"resnr": [(eq, cl_list.resnr)],"zinr": [(eq, cl_list.rmno)]})

            if mealcoup:
                cl_list.tot_bfast = mealcoup.verbrauch[0] + mealcoup.verbrauch[1] + mealcoup.verbrauch[2] + mealcoup.verbrauch[3] + mealcoup.verbrauch[4] +\
                        mealcoup.verbrauch[5] + mealcoup.verbrauch[6] + mealcoup.verbrauch[7] + mealcoup.verbrauch[8] + mealcoup.verbrauch[9] +\
                        mealcoup.verbrauch[10] + mealcoup.verbrauch[11] + mealcoup.verbrauch[12] + mealcoup.verbrauch[13] + mealcoup.verbrauch[14] +\
                        mealcoup.verbrauch[15] + mealcoup.verbrauch[16] + mealcoup.verbrauch[17] + mealcoup.verbrauch[18] + mealcoup.verbrauch[19] +\
                        mealcoup.verbrauch[20] + mealcoup.verbrauch[21] + mealcoup.verbrauch[22] + mealcoup.verbrauch[23] + mealcoup.verbrauch[24] +\
                        mealcoup.verbrauch[25] + mealcoup.verbrauch[26] + mealcoup.verbrauch[27] + mealcoup.verbrauch[28] + mealcoup.verbrauch[29] +\
                        mealcoup.verbrauch[30] + mealcoup.verbrauch[31]

            s_list = query(s_list_data, filters=(lambda s_list: s_list.rmcat == cl_list.kurzbez), first=True)

            if not s_list:

                s_list = query(s_list_data, filters=(lambda s_list: s_list.rmcat == ""), first=True)

                if s_list:
                    s_list.rmcat = cl_list.kurzbez
                    s_list.bezeich = cl_list.bezeich

            if not s_list:
                s_list = S_list()
                s_list_data.append(s_list)

                s_list.rmcat = cl_list.kurzbez
                s_list.bezeich = cl_list.bezeich
            s_list.anz = s_list.anz + cl_list.qty

            s_list = query(s_list_data, filters=(lambda s_list: s_list.nat == cl_list.nat), first=True)

            if not s_list:

                s_list = query(s_list_data, filters=(lambda s_list: s_list.nat == ""), first=True)

                if s_list:
                    s_list.nat = cl_list.nat

            if not s_list:
                s_list = S_list()
                s_list_data.append(s_list)


                if s_list:
                    s_list.nat = cl_list.nat
            s_list.adult = s_list.adult + cl_list.a + cl_list.co
            s_list.child = s_list.child + cl_list.c
            s_list.rmqty = s_list.rmqty + cl_list.qty

        if (tot_a + tot_co) != 0:

            for s_list in query(s_list_data, filters=(lambda s_list: s_list.nat != "")):

                nation = get_cache (Nation, {"kurzbez": [(eq, s_list.nat)]})

                if nation:
                    s_list.nat = nation.bezeich
                s_list.proz =  to_decimal(s_list.adult) / to_decimal((tot_a) + to_decimal(tot_co)) * to_decimal("100")

        # sort by rmno -> query diatas merubah sort order.-------------------
        for cl_list in query(cl_list_data, sort_by=[("rmno",False)]):
            pass
        #--------------------------------------------------------------------

    def create_inhouse3():
        # sorttype = 
        nonlocal tot_payrm, tot_rm, tot_a, tot_c, tot_co, tot_avail, tot_rmqty, inactive, cl_list_data, s_list_data, t_buff_queasy_data, vipnr1, vipnr2, vipnr3, vipnr4, vipnr5, vipnr6, vipnr7, vipnr8, vipnr9, tot_room, all_room, all_remark, queasy, htparam, zkstat, zinrstat, paramtext, guest, reservation, zimmer, zimkateg, res_line, guestseg, segment, mc_guest, mc_types, nation, waehrung, reslin_queasy, mealcoup, genstat
        nonlocal sorttype, datum, curr_date, froom, troom, exc_depart, incl_gcomment, incl_rsvcomment, prog_name, disp_accompany, disp_exclinact, split_rsv_print, exc_compli


        nonlocal setup_list, str_list, cl_list, s_list, zinr_list, t_buff_queasy
        nonlocal setup_list_data, str_list_data, cl_list_data, s_list_data, zinr_list_data, t_buff_queasy_data

        i:int = 0
        j:int = 0
        vip_flag:string = ""
        str:string = ""
        nr:int = 0
        curr_gastnr:int = 0
        actflag1:int = 0
        actflag2:int = 0
        gmember = None
        gbuff = None
        rbuff = None
        Gmember =  create_buffer("Gmember",Guest)
        Gbuff =  create_buffer("Gbuff",Guest)
        Rbuff =  create_buffer("Rbuff",Reservation)
        zinr_list_data.clear()

        if datum == curr_date:
            actflag1 = 1
            actflag2 = 1
        else:
            actflag1 = 1
            actflag2 = 2
        tot_payrm = 0
        tot_rm = 0
        tot_a = 0
        tot_c = 0
        tot_co = 0
        inactive = 0
        s_list_data.clear()
        cl_list_data.clear()
        str_list_data.clear()
        tot_avail = 0

        for zimmer in db_session.query(Zimmer).filter(
                 (Zimmer.sleeping)).order_by(Zimmer._recid).all():
            tot_avail = tot_avail + 1

        res_line_obj_list = {}
        res_line = Res_line()
        zimkateg = Zimkateg()
        reservation = Reservation()
        guest = Guest()
        gmember = Guest()
        zimmer = Zimmer()
        for res_line.setup, res_line.zinr, res_line.resnr, res_line.name, res_line.zipreis, res_line.ankunft, res_line.abreise, res_line.zimmeranz, res_line.erwachs, res_line.kind1, res_line.kind2, \
            res_line.gratis, res_line.arrangement, res_line.flight_nr, res_line.ankzeit, res_line.resstatus, res_line.betriebsnr, res_line.reslinnr, res_line.zimmer_wunsch, res_line.zimmerfix, \
            res_line.gastnrmember, res_line.bemerk, res_line.gastnr, res_line._recid, zimkateg.kurzbez, zimkateg.bezeichnung, zimkateg._recid, reservation.segmentcode, reservation.resdat, \
            reservation.useridanlage, reservation.resnr, reservation._recid, guest.name, guest.vorname1, guest.anrede1, guest.anredefirma, guest.gastnr, guest.karteityp, guest._recid, \
            gmember.name, gmember.vorname1, gmember.anrede1, gmember.anredefirma, gmember.gastnr, gmember.karteityp, gmember._recid, zimmer.etage, zimmer.bezeich, zimmer.sleeping, \
            zimmer._recid, gmember.nation1, gmember.nation2, gmember.email_adr, gmember.geburtdatum1, gmember.telefon, gmember.mobil_telefon \
                in db_session.query(Res_line.setup, Res_line.zinr, Res_line.resnr, Res_line.name, Res_line.zipreis, Res_line.ankunft, Res_line.abreise, Res_line.zimmeranz, Res_line.erwachs, \
                                    Res_line.kind1, Res_line.kind2, Res_line.gratis, Res_line.arrangement, Res_line.flight_nr, Res_line.ankzeit, Res_line.resstatus, Res_line.betriebsnr, \
                                    Res_line.reslinnr, Res_line.zimmer_wunsch, Res_line.zimmerfix, Res_line.gastnrmember, Res_line.bemerk, Res_line.gastnr, Res_line._recid, Zimkateg.kurzbez, \
                                    Zimkateg.bezeichnung, Zimkateg._recid, Reservation.segmentcode, Reservation.resdat, Reservation.useridanlage, Reservation.resnr, Reservation._recid, \
                                    Guest.name, Guest.vorname1, Guest.anrede1, Guest.anredefirma, Guest.gastnr, Guest.karteityp, Guest._recid, Gmember.name, Gmember.vorname1, \
                                    Gmember.anrede1, Gmember.anredefirma, Gmember.gastnr, Gmember.karteityp, Gmember._recid, Zimmer.etage, Zimmer.bezeich, Zimmer.sleeping, \
                                    Zimmer._recid, Gmember.nation1, Gmember.nation2, Gmember.email_adr, Gmember.geburtdatum1, Gmember.telefon, Gmember.mobil_telefon) \
                                .join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Guest,(Guest.gastnr == Reservation.gastnr)).join(Gmember,(Gmember.gastnr == Res_line.gastnrmember)).join(Zimmer,(Zimmer.zinr == Res_line.zinr) & (Zimmer.sleeping)).filter(
                 (Res_line.active_flag >= actflag1) & (Res_line.active_flag <= actflag2) & (Res_line.resstatus != 9) & (Res_line.resstatus != 10) & (Res_line.resstatus != 12) & (Res_line.ankunft <= datum) & (Res_line.abreise >= datum) & (Res_line.zinr >= (froom).lower()) & (Res_line.zinr <= (troom).lower())).order_by(Guest.karteityp.desc(), Guest.name, Guest.gastnr, Res_line.name, Res_line.zinr).all():
            if res_line_obj_list.get(res_line._recid):
                continue
            else:
                res_line_obj_list[res_line._recid] = True

            if exc_depart and res_line.abreise == datum:
                pass
            else:

                setup_list = query(setup_list_data, filters=(lambda setup_list: setup_list.nr == res_line.setup + 1), first=True)

                if curr_gastnr != guest.gastnr:
                    nr = 0
                    curr_gastnr = guest.gastnr

                if guest.karteityp > 0:
                    nr = nr + 1
                vip_flag = ""

                guestseg = db_session.query(Guestseg).filter(
                         (Guestseg.gastnr == gmember.gastnr) & ((Guestseg.segmentcode == vipnr1) | (Guestseg.segmentcode == vipnr2) | (Guestseg.segmentcode == vipnr3) | (Guestseg.segmentcode == vipnr4) | (Guestseg.segmentcode == vipnr5) | (Guestseg.segmentcode == vipnr6) | (Guestseg.segmentcode == vipnr7) | (Guestseg.segmentcode == vipnr8) | (Guestseg.segmentcode == vipnr9))).first()

                if guestseg:

                    segment = get_cache (Segment, {"segmentcode": [(eq, guestseg.segmentcode)]})
                    vip_flag = segment.bezeich


                cl_list = Cl_list()
                cl_list_data.append(cl_list)

                cl_list.nr = nr
                cl_list.karteityp = guest.karteityp
                cl_list.rmcat = zimkateg.kurzbez + setup_list.char
                cl_list.kurzbez = zimkateg.kurzbez
                cl_list.bezeich = zimkateg.bezeichnung
                cl_list.nat = gmember.nation1
                cl_list.resnr = res_line.resnr
                cl_list.vip = vip_flag
                cl_list.name = res_line.name
                cl_list.rmno = res_line.zinr
                cl_list.zipreis =  to_decimal(res_line.zipreis)
                cl_list.arrive = res_line.ankunft
                cl_list.depart = res_line.abreise
                cl_list.qty = res_line.zimmeranz
                cl_list.a = res_line.erwachs
                cl_list.c = res_line.kind1 + res_line.kind2
                cl_list.co = res_line.gratis
                cl_list.argt = res_line.arrangement
                cl_list.flight = substring(res_line.flight_nr, 11, 6)
                cl_list.etd = substring(res_line.flight_nr, 17, 5)
                cl_list.ci_time = to_string(res_line.ankzeit, "HH:MM")
                cl_list.paym = reservation.segmentcode
                cl_list.created = reservation.resdat
                cl_list.createid = reservation.useridanlage
                cl_list.etage = zimmer.etage
                cl_list.zinr_bez = zimmer.bezeich
                cl_list.birthdate = gmember.geburtdatum1
                cl_list.telefon = gmember.telefon
                cl_list.mobil_tel = gmember.mobil_telefon

                if res_line.resstatus != 11 and res_line.resstatus != 13:
                    cl_list.flag_guest = 1


                else:
                    cl_list.flag_guest = 2

                mc_guest = get_cache (Mc_guest, {"gastnr": [(eq, gmember.gastnr)]})

                if mc_guest:
                    cl_list.telefon = gmember.telefon + ";" + mc_guest.cardnum

                    mc_types = get_cache (Mc_types, {"nr": [(eq, mc_guest.nr)]})

                    if mc_types:
                        cl_list.mobil_tel = gmember.mobil_telefon + ";" + mc_types.bezeich
                    else:
                        cl_list.mobil_tel = gmember.mobil_telefon
                else:
                    cl_list.telefon = gmember.telefon

                nation = get_cache (Nation, {"kurzbez": [(eq, gmember.nation2)]})

                if nation:
                    cl_list.local_reg = nation.bezeich

                waehrung = get_cache (Waehrung, {"waehrungsnr": [(eq, res_line.betriebsnr)]})

                if waehrung:
                    cl_list.curr = waehrung.wabkurz + ";" + gmember.email_adr

                reslin_queasy = get_cache (Reslin_queasy, {"key": [(eq, "specialrequest")],"resnr": [(eq, res_line.resnr)],"reslinnr": [(eq, res_line.reslinnr)]})

                if reslin_queasy:
                    cl_list.spreq = reslin_queasy.char3 + "," + cl_list.spreq

                reslin_queasy = get_cache (Reslin_queasy, {"key": [(eq, "arrangement")],"resnr": [(eq, res_line.resnr)],"reslinnr": [(eq, res_line.reslinnr)],"date1": [(le, datum)],"date2": [(ge, datum)]})

                if reslin_queasy:

                    if reslin_queasy.char2 != "":
                        cl_list.ratecode = reslin_queasy.char2
                    else:
                        for i in range(1,num_entries(res_line.zimmer_wunsch, ";") - 1 + 1) :
                            str = entry(i - 1, res_line.zimmer_wunsch, ";")

                            if substring(str, 0, 6) == ("$CODE$").lower() :
                                cl_list.ratecode = substring(str, 6)
                                break

                mealcoup = get_cache (Mealcoup, {"name": [(eq, "breakfast")],"resnr": [(eq, res_line.resnr)],"zinr": [(eq, res_line.zinr)]})

                if mealcoup:
                    cl_list.tot_bfast = mealcoup.verbrauch[0] + mealcoup.verbrauch[1] + mealcoup.verbrauch[2] + mealcoup.verbrauch[3] + mealcoup.verbrauch[4] +\
                            mealcoup.verbrauch[5] + mealcoup.verbrauch[6] + mealcoup.verbrauch[7] + mealcoup.verbrauch[8] + mealcoup.verbrauch[9] +\
                            mealcoup.verbrauch[10] + mealcoup.verbrauch[11] + mealcoup.verbrauch[12] + mealcoup.verbrauch[13] + mealcoup.verbrauch[14] +\
                            mealcoup.verbrauch[15] + mealcoup.verbrauch[16] + mealcoup.verbrauch[17] + mealcoup.verbrauch[18] + mealcoup.verbrauch[19] +\
                            mealcoup.verbrauch[20] + mealcoup.verbrauch[21] + mealcoup.verbrauch[22] + mealcoup.verbrauch[23] + mealcoup.verbrauch[24] +\
                            mealcoup.verbrauch[25] + mealcoup.verbrauch[26] + mealcoup.verbrauch[27] + mealcoup.verbrauch[28] + mealcoup.verbrauch[29] +\
                            mealcoup.verbrauch[30] + mealcoup.verbrauch[31]

                segment = get_cache (Segment, {"segmentcode": [(eq, reservation.segmentcode)]})

                if segment:
                    cl_list.segm = entry(0, segment.bezeich, "$$0")

                if guest.karteityp != 0:
                    cl_list.company = guest.name + ", " + guest.vorname1 + " " + guest.anrede1 + guest.anredefirma
                else:
                    cl_list.company = guest.name + ", " + guest.vorname1 + " " + guest.anrede1 + guest.anredefirma

                if cl_list.nat == "":
                    cl_list.nat = "?"

                if res_line.resstatus == 13 or res_line.zimmerfix :
                    cl_list.qty = 0

                if split_rsv_print:

                    if incl_gcomment:

                        gbuff = get_cache (Guest, {"gastnr": [(eq, res_line.gastnrmember)]})

                        if gbuff:
                            for i in range(1,length(gbuff.bemerkung)  + 1) :

                                if substring(gbuff.bemerkung, i - 1, 1) == chr_unicode(10):
                                    cl_list.bemerk = cl_list.bemerk + " "
                                else:
                                    cl_list.bemerk = cl_list.bemerk + substring(trim(gbuff.bemerkung) , i - 1, 1)
                        cl_list.bemerk = cl_list.bemerk + " || "

                    if incl_rsvcomment:

                        rbuff = get_cache (Reservation, {"resnr": [(eq, reservation.resnr)]})

                        if rbuff:
                            for j in range(1,length(rbuff.bemerk)  + 1) :

                                if substring(rbuff.bemerk, j - 1, 1) == chr_unicode(10):
                                    cl_list.bemerk1 = cl_list.bemerk1 + " "
                                else:
                                    cl_list.bemerk1 = cl_list.bemerk1 + substring(trim(rbuff.bemerk) , j - 1, 1)
                        cl_list.bemerk = cl_list.bemerk + cl_list.bemerk1 + " || "
                    for i in range(1,length(res_line.bemerk)  + 1) :

                        if substring(res_line.bemerk, i - 1, 1) == chr_unicode(10):
                            cl_list.bemerk = cl_list.bemerk + " "
                        else:
                            cl_list.bemerk = cl_list.bemerk + substring(trim(res_line.bemerk) , i - 1, 1)
                    all_remark = res_line.bemerk
                    all_remark = replace_str(all_remark, chr_unicode(10) , " ")
                    all_remark = replace_str(all_remark, chr_unicode(13) , " ")
                    cl_list.bemerk01 = to_string(substring(all_remark, 0, 225))
                    cl_list.bemerk02 = to_string(substring(all_remark, 225, 225))
                    cl_list.bemerk03 = to_string(substring(all_remark, 450, 225))
                    cl_list.bemerk04 = to_string(substring(all_remark, 675, 225))
                else:
                    for i in range(1,length(res_line.bemerk)  + 1) :
                        cl_list.bemerk = cl_list.bemerk + substring(trim(res_line.bemerk) , i - 1, 1)

                    rbuff = get_cache (Reservation, {"resnr": [(eq, reservation.resnr)]})

                    if rbuff:
                        cl_list.rsv_comment = rbuff.bemerk

                    gbuff = get_cache (Guest, {"gastnr": [(eq, res_line.gastnrmember)]})

                    if gbuff:
                        cl_list.g_comment = gbuff.bemerkung

                    queasy = get_cache (Queasy, {"key": [(eq, 267)],"number1": [(eq, res_line.resnr)],"number2": [(eq, res_line.reslinnr)]})

                    if queasy:
                        cl_list.other_comment = queasy.char1
                cl_list.pax = to_string(cl_list.a, ">9") + "/" + to_string(cl_list.c, "9") + " " + to_string(cl_list.co, "9")

                if cl_list.nat == "":
                    cl_list.nat = "?"
                else:

                    nation = get_cache (Nation, {"kurzbez": [(eq, cl_list.nat)]})

                    if nation:
                        cl_list.nation = nation.bezeich

                zinr_list = query(zinr_list_data, filters=(lambda zinr_list: zinr_list.zinr == res_line.zinr and zinr_list.resnr == res_line.resnr and zinr_list.reslinnr == res_line.reslinnr), first=True)

                if not zinr_list:
                    zinr_list = Zinr_list()
                    zinr_list_data.append(zinr_list)

                    zinr_list.resnr = res_line.resnr
                    zinr_list.reslinnr = res_line.reslinnr
                    zinr_list.zinr = res_line.zinr

                    queasy = get_cache (Queasy, {"key": [(eq, 14)],"char1": [(eq, res_line.zinr)],"date1": [(le, curr_date)],"date2": [(ge, curr_date)]})

                    if zimmer.sleeping and res_line.resstatus != 13:

                        if not queasy:
                            tot_rm = tot_rm + res_line.zimmeranz
                            tot_rmqty = tot_rmqty + res_line.zimmeranz

                        elif queasy and queasy.number3 != res_line.gastnr:
                            tot_rm = tot_rm + res_line.zimmeranz
                            tot_rmqty = tot_rmqty + res_line.zimmeranz

                    if zimmer.sleeping and (res_line.zipreis > 0 or res_line.zipreis == 0) and res_line.resstatus != 13 and res_line.erwachs > 0:

                        if not queasy:
                            tot_payrm = tot_payrm + res_line.zimmeranz

                        elif queasy and queasy.number3 != res_line.gastnr:
                            tot_payrm = tot_payrm + res_line.zimmeranz

                    elif not zimmer.sleeping:

                        if queasy and queasy.number3 != res_line.gastnr and res_line.zipreis > 0:
                            tot_rm = tot_rm + res_line.zimmeranz
                            tot_rmqty = tot_rmqty + res_line.zimmeranz
                        inactive = inactive + 1
                tot_a = tot_a + res_line.erwachs
                tot_c = tot_c + res_line.kind1 + res_line.kind2
                tot_co = tot_co + res_line.gratis

                if exc_compli:
                    tot_co = 0

            if not disp_accompany:

                cl_list = query(cl_list_data, filters=(lambda cl_list: cl_list.rmno == res_line.zinr and cl_list.resnr == res_line.resnr and cl_list.arrive == res_line.ankunft and cl_list.zipreis == 0 and (cl_list.a + cl_list.c) < 1 and cl_list.co < 1), first=True)

                if cl_list:
                    cl_list_data.remove(cl_list)
                    pass

            if exc_compli:

                cl_list = query(cl_list_data, filters=(lambda cl_list: cl_list.rmno == res_line.zinr and cl_list.resnr == res_line.resnr and cl_list.arrive == res_line.ankunft and cl_list.co > 0), first=True)

                if cl_list:
                    cl_list_data.remove(cl_list)
                    pass
                    tot_rm = tot_rm - 1

        for cl_list in query(cl_list_data, sort_by=[("nation",False),("bezeich",False)]):

            # summary by room category
            s_list = query(s_list_data, filters=(lambda s_list: s_list.rmcat == cl_list.kurzbez), first=True)
            if not s_list:
                s_list = query(s_list_data, filters=(lambda s_list: s_list.rmcat == ""), first=True)
                if s_list:
                    s_list.rmcat = cl_list.kurzbez
                    s_list.bezeich = cl_list.bezeich

            if not s_list:
                s_list = S_list()
                s_list_data.append(s_list)

                s_list.rmcat = cl_list.kurzbez
                s_list.bezeich = cl_list.bezeich
            s_list.anz = s_list.anz + cl_list.qty

            # summary by nation
            print("Nat:", cl_list.nat)
            s_list = query(s_list_data, filters=(lambda s_list: s_list.nat == cl_list.nat), first=True)
            if not s_list:
                s_list = query(s_list_data, filters=(lambda s_list: s_list.nat == ""), first=True)

                if s_list:
                    s_list.nat = cl_list.nat

            if not s_list:
                s_list = S_list()
                s_list_data.append(s_list)

                if s_list:
                    s_list.nat = cl_list.nat

            s_list.adult = s_list.adult + cl_list.a + cl_list.co
            s_list.child = s_list.child + cl_list.c
            s_list.rmqty = s_list.rmqty + cl_list.qty

        if (tot_a + tot_co) != 0:
            for s_list in query(s_list_data, filters=(lambda s_list: s_list.nat != "")):
                nation = get_cache (Nation, {"kurzbez": [(eq, s_list.nat)]})
                if nation:
                    s_list.nat = nation.bezeich
                s_list.proz =  to_decimal(s_list.adult) / to_decimal((tot_a) + to_decimal(tot_co)) * to_decimal("100")


        # sort by rmno -> query diatas merubah sort order.-------------------
        for cl_list in query(cl_list_data, sort_by=[("rmno",False)]):
            pass
        #--------------------------------------------------------------------

    def create_genstat_inhouse3():

        nonlocal tot_payrm, tot_rm, tot_a, tot_c, tot_co, tot_avail, tot_rmqty, inactive, cl_list_data, s_list_data, t_buff_queasy_data, vipnr1, vipnr2, vipnr3, vipnr4, vipnr5, vipnr6, vipnr7, vipnr8, vipnr9, tot_room, all_room, all_remark, queasy, htparam, zkstat, zinrstat, paramtext, guest, reservation, zimmer, zimkateg, res_line, guestseg, segment, mc_guest, mc_types, nation, waehrung, reslin_queasy, mealcoup, genstat
        nonlocal sorttype, datum, curr_date, curr_gastnr, froom, troom, exc_depart, incl_gcomment, incl_rsvcomment, prog_name, disp_accompany, disp_exclinact, split_rsv_print, exc_compli


        nonlocal setup_list, str_list, cl_list, s_list, zinr_list, t_buff_queasy
        nonlocal setup_list_data, str_list_data, cl_list_data, s_list_data, zinr_list_data, t_buff_queasy_data

        i:int = 0
        j:int = 0
        vip_flag:string = ""
        nr:int = 0
        str:string = ""
        actflag1:int = 0
        actflag2:int = 0
        do_it:bool = False
        gmember = None
        gbuff = None
        rbuff = None
        Gmember =  create_buffer("Gmember",Guest)
        Gbuff =  create_buffer("Gbuff",Guest)
        Rbuff =  create_buffer("Rbuff",Reservation)
        zinr_list_data.clear()

        if datum == curr_date:
            actflag1 = 1
            actflag2 = 1
        else:
            actflag1 = 1
            actflag2 = 2
        tot_payrm = 0
        tot_rm = 0
        tot_a = 0
        tot_c = 0
        tot_co = 0
        inactive = 0
        s_list_data.clear()
        cl_list_data.clear()
        str_list_data.clear()
        tot_avail = 0

        for zkstat in db_session.query(Zkstat).filter(
                 (Zkstat.datum == datum)).order_by(Zkstat._recid).all():
            tot_avail = tot_avail + zkstat.anz100

        genstat_obj_list = {}
        genstat = Genstat()
        zimkateg = Zimkateg()
        reservation = Reservation()
        guest = Guest()
        gmember = Guest()
        zimmer = Zimmer()
        for genstat.resstatus, genstat.res_date, genstat.resnr, genstat.res_int, genstat.zinr, genstat.zipreis, genstat.erwachs, genstat.kind1, genstat.kind2, genstat.kind3, \
            genstat.gratis, genstat.argt, genstat.segmentcode, genstat.gastnr, genstat._recid, zimkateg.kurzbez, zimkateg.bezeichnung, zimkateg._recid, reservation.segmentcode, \
            reservation.resdat, reservation.useridanlage, reservation.resnr, reservation._recid, guest.name, guest.vorname1, guest.anrede1, guest.anredefirma, guest.gastnr, \
            guest.karteityp, guest._recid, gmember.name, gmember.vorname1, gmember.anrede1, gmember.anredefirma, gmember.gastnr, gmember.karteityp, gmember._recid, zimmer.etage, \
            zimmer.bezeich, zimmer.sleeping, zimmer._recid, gmember.nation1, gmember.nation2, gmember.email_adr, gmember.geburtdatum1, gmember.telefon, gmember.mobil_telefon \
                in db_session.query(Genstat.resstatus, Genstat.res_date, Genstat.resnr, Genstat.res_int, Genstat.zinr, Genstat.zipreis, \
                                        Genstat.erwachs, Genstat.kind1, Genstat.kind2, Genstat.kind3, Genstat.gratis, Genstat.argt, \
                                        Genstat.segmentcode, Genstat.gastnr, Genstat._recid, Zimkateg.kurzbez, Zimkateg.bezeichnung, \
                                        Zimkateg._recid, Reservation.segmentcode, Reservation.resdat, Reservation.useridanlage, \
                                        Reservation.resnr, Reservation._recid, Guest.name, Guest.vorname1, Guest.anrede1, \
                                        Guest.anredefirma, Guest.gastnr, Guest.karteityp, Guest._recid, Gmember.name, Gmember.vorname1,\
                                        Gmember.anrede1, Gmember.anredefirma, Gmember.gastnr, Gmember.karteityp, Gmember._recid, \
                                        Zimmer.etage, Zimmer.bezeich, Zimmer.sleeping, Zimmer._recid, Gmember.nation1, Gmember.nation2, Gmember.email_adr,\
                                        Gmember.geburtdatum1, Gmember.telefon, Gmember.mobil_telefon)\
                                .join(Zimkateg,(Zimkateg.zikatnr == Genstat.zikatnr)).join(Reservation,(Reservation.resnr == Genstat.resnr))\
                                .join(Guest,(Guest.gastnr == Genstat.gastnr))\
                                .join(Gmember,(Gmember.gastnr == Genstat.gastnrmember)).join(Zimmer,(Zimmer.zinr == Genstat.zinr) & (Zimmer.sleeping))\
                                .filter(
                                        (Genstat.datum == datum) & 
                                        (Genstat.zinr >= (froom).lower()) & 
                                        (Genstat.zinr <= (troom).lower()))\
                                .order_by(Guest.karteityp.desc(), Guest.name, Guest.gastnr, Gmember.name, Genstat.zinr).all():
            if genstat_obj_list.get(genstat._recid):
                continue
            else:
                genstat_obj_list[genstat._recid] = True

            if genstat.res_date[0] < datum and genstat.res_date[1] == datum and genstat.resstatus == 8:
                pass

            elif exc_depart and genstat.res_date[0] <= datum and genstat.res_date[1] == datum and genstat.resstatus == 8:
                pass
            else:

                res_line = get_cache (Res_line, {"resnr": [(eq, genstat.resnr)],"reslinnr": [(eq, genstat.res_int[0])]})

                setup_list = query(setup_list_data, filters=(lambda setup_list: setup_list.nr == res_line.setup + 1), first=True)

                if curr_gastnr != guest.gastnr:
                    nr = 0
                    curr_gastnr = guest.gastnr

                if guest.karteityp > 0:
                    nr = nr + 1
                vip_flag = ""

                guestseg = db_session.query(Guestseg).filter(
                         (Guestseg.gastnr == gmember.gastnr) & ((Guestseg.segmentcode == vipnr1) | (Guestseg.segmentcode == vipnr2) | (Guestseg.segmentcode == vipnr3) | (Guestseg.segmentcode == vipnr4) | (Guestseg.segmentcode == vipnr5) | (Guestseg.segmentcode == vipnr6) | (Guestseg.segmentcode == vipnr7) | (Guestseg.segmentcode == vipnr8) | (Guestseg.segmentcode == vipnr9))).first()

                if guestseg:

                    segment = get_cache (Segment, {"segmentcode": [(eq, guestseg.segmentcode)]})
                    vip_flag = segment.bezeich


                cl_list = Cl_list()
                cl_list_data.append(cl_list)

                cl_list.nr = nr
                cl_list.karteityp = guest.karteityp
                cl_list.rmcat = zimkateg.kurzbez + setup_list.char
                cl_list.kurzbez = zimkateg.kurzbez
                cl_list.bezeich = zimkateg.bezeichnung
                cl_list.nat = gmember.nation1
                cl_list.resnr = genstat.resnr
                cl_list.vip = vip_flag
                cl_list.name = gmember.name + ", " + gmember.vorname1 +\
                        " " + gmember.anrede1
                cl_list.rmno = genstat.zinr
                cl_list.zipreis =  to_decimal(genstat.zipreis)
                cl_list.arrive = genstat.res_date[0]
                cl_list.depart = genstat.res_date[1]
                cl_list.qty = 1
                cl_list.a = genstat.erwachs
                cl_list.c = genstat.kind1 + genstat.kind2 + genstat.kind3
                cl_list.co = genstat.gratis
                cl_list.argt = genstat.argt
                cl_list.flight = substring(res_line.flight_nr, 11, 6)
                cl_list.etd = substring(res_line.flight_nr, 17, 5)
                cl_list.ci_time = to_string(res_line.ankzeit, "HH:MM")
                cl_list.paym = genstat.segmentcode
                cl_list.created = reservation.resdat
                cl_list.createid = reservation.useridanlage
                cl_list.etage = zimmer.etage
                cl_list.zinr_bez = zimmer.bezeich
                cl_list.birthdate = gmember.geburtdatum1
                cl_list.telefon = gmember.telefon
                cl_list.mobil_tel = gmember.mobil_telefon

                if res_line.resstatus != 11 and res_line.resstatus != 13:
                    cl_list.flag_guest = 1


                else:
                    cl_list.flag_guest = 2

                mc_guest = get_cache (Mc_guest, {"gastnr": [(eq, gmember.gastnr)]})

                if mc_guest:
                    cl_list.telefon = gmember.telefon + ";" + mc_guest.cardnum

                    mc_types = get_cache (Mc_types, {"nr": [(eq, mc_guest.nr)]})

                    if mc_types:
                        cl_list.mobil_tel = gmember.mobil_telefon + ";" + mc_types.bezeich
                    else:
                        cl_list.mobil_tel = gmember.mobil_telefon
                else:
                    cl_list.telefon = gmember.telefon

                nation = get_cache (Nation, {"kurzbez": [(eq, gmember.nation2)]})

                if nation:
                    cl_list.local_reg = nation.bezeich

                waehrung = get_cache (Waehrung, {"waehrungsnr": [(eq, res_line.betriebsnr)]})

                if waehrung:
                    cl_list.curr = waehrung.wabkurz + ";" + gmember.email_adr

                reslin_queasy = get_cache (Reslin_queasy, {"key": [(eq, "specialrequest")],"resnr": [(eq, res_line.resnr)],"reslinnr": [(eq, res_line.reslinnr)]})

                if reslin_queasy:
                    cl_list.spreq = reslin_queasy.char3 + "," + cl_list.spreq

                reslin_queasy = get_cache (Reslin_queasy, {"key": [(eq, "arrangement")],"resnr": [(eq, res_line.resnr)],"reslinnr": [(eq, res_line.reslinnr)],"date1": [(le, datum)],"date2": [(ge, datum)]})

                if reslin_queasy:

                    if reslin_queasy.char2 != "":
                        cl_list.ratecode = reslin_queasy.char2
                    else:
                        for i in range(1,num_entries(res_line.zimmer_wunsch, ";") - 1 + 1) :
                            str = entry(i - 1, res_line.zimmer_wunsch, ";")

                            if substring(str, 0, 6) == ("$CODE$").lower() :
                                cl_list.ratecode = substring(str, 6)
                                break

                segment = get_cache (Segment, {"segmentcode": [(eq, genstat.segmentcode)]})

                if segment:
                    cl_list.segm = entry(0, segment.bezeich, "$$0")

                if guest.karteityp != 0:
                    cl_list.company = guest.name + ", " + guest.vorname1 + " " + guest.anrede1 + guest.anredefirma
                else:
                    cl_list.company = guest.name + ", " + guest.vorname1 + " " + guest.anrede1 + guest.anredefirma

                if cl_list.nat == "":
                    cl_list.nat = "?"

                if genstat.resstatus == 13:
                    cl_list.qty = 0

                if not split_rsv_print:

                    if incl_gcomment:

                        gbuff = get_cache (Guest, {"gastnr": [(eq, res_line.gastnrmember)]})

                        if gbuff:
                            for i in range(1,length(gbuff.bemerkung)  + 1) :

                                if substring(gbuff.bemerkung, i - 1, 1) == chr_unicode(10):
                                    cl_list.bemerk = cl_list.bemerk + " "
                                else:
                                    cl_list.bemerk = cl_list.bemerk + substring(trim(gbuff.bemerkung) , i - 1, 1)
                        cl_list.bemerk = cl_list.bemerk + " || "

                    if incl_rsvcomment:

                        rbuff = get_cache (Reservation, {"resnr": [(eq, reservation.resnr)]})

                        if rbuff:
                            for j in range(1,length(rbuff.bemerk)  + 1) :

                                if substring(rbuff.bemerk, j - 1, 1) == chr_unicode(10):
                                    cl_list.bemerk1 = cl_list.bemerk1 + " "
                                else:
                                    cl_list.bemerk1 = cl_list.bemerk1 + substring(trim(rbuff.bemerk) , j - 1, 1)
                        cl_list.bemerk = cl_list.bemerk + cl_list.bemerk1 + " || "
                    for i in range(1,length(res_line.bemerk)  + 1) :

                        if substring(res_line.bemerk, i - 1, 1) == chr_unicode(10):
                            cl_list.bemerk = cl_list.bemerk + " "
                        else:
                            cl_list.bemerk = cl_list.bemerk + substring(trim(res_line.bemerk) , i - 1, 1)
                    all_remark = res_line.bemerk
                    all_remark = replace_str(all_remark, chr_unicode(10) , " ")
                    all_remark = replace_str(all_remark, chr_unicode(13) , " ")
                    cl_list.bemerk01 = to_string(substring(all_remark, 0, 225))
                    cl_list.bemerk02 = to_string(substring(all_remark, 225, 225))
                    cl_list.bemerk03 = to_string(substring(all_remark, 450, 225))
                    cl_list.bemerk04 = to_string(substring(all_remark, 675, 225))
                else:
                    for i in range(1,length(res_line.bemerk)  + 1) :
                        cl_list.bemerk = cl_list.bemerk + substring(trim(res_line.bemerk) , i - 1, 1)

                    rbuff = get_cache (Reservation, {"resnr": [(eq, reservation.resnr)]})

                    if rbuff:
                        cl_list.rsv_comment = rbuff.bemerk

                    gbuff = get_cache (Guest, {"gastnr": [(eq, res_line.gastnrmember)]})

                    if gbuff:
                        cl_list.g_comment = gbuff.bemerkung

                    queasy = get_cache (Queasy, {"key": [(eq, 267)],"number1": [(eq, res_line.resnr)],"number2": [(eq, res_line.reslinnr)]})

                    if queasy:
                        cl_list.other_comment = queasy.char1
                cl_list.pax = to_string(cl_list.a, ">9") + "/" + to_string(cl_list.c, "9") + " " + to_string(cl_list.co, "9")

                if cl_list.nat == "":
                    cl_list.nat = "?"
                else:

                    nation = get_cache (Nation, {"kurzbez": [(eq, cl_list.nat)]})

                    if nation:
                        cl_list.nation = nation.bezeich

                zinr_list = query(zinr_list_data, filters=(lambda zinr_list: zinr_list.zinr == genstat.zinr and zinr_list.resnr == res_line.resnr and zinr_list.reslinnr == res_line.reslinnr), first=True)

                if not zinr_list:
                    zinr_list = Zinr_list()
                    zinr_list_data.append(zinr_list)

                    zinr_list.resnr = res_line.resnr
                    zinr_list.reslinnr = res_line.reslinnr
                    zinr_list.zinr = genstat.zinr

                    queasy = get_cache (Queasy, {"key": [(eq, 14)],"char1": [(eq, genstat.zinr)],"date1": [(le, curr_date)],"date2": [(ge, curr_date)]})

                    if zimmer.sleeping and genstat.resstatus != 13:

                        if not queasy:
                            tot_rm = tot_rm + 1
                            tot_rmqty = tot_rmqty + 1

                        elif queasy and queasy.number3 != genstat.gastnr:
                            tot_rm = tot_rm + 1
                            tot_rmqty = tot_rmqty + 1

                    if zimmer.sleeping and (genstat.zipreis > 0 or genstat.zipreis == 0) and genstat.erwachs > 0 and genstat.resstatus != 13:

                        if not queasy:
                            tot_payrm = tot_payrm + 1

                        elif queasy and queasy.number3 != genstat.gastnr:
                            tot_payrm = tot_payrm + 1

                    elif not zimmer.sleeping:

                        if queasy and queasy.number3 != genstat.gastnr and genstat.zipreis > 0:
                            tot_rm = tot_rm + 1
                            tot_rmqty = tot_rmqty + 1
                        inactive = inactive + 1
                tot_a = tot_a + genstat.erwachs
                tot_c = tot_c + genstat.kind1 + genstat.kind2 + genstat.kind3
                tot_co = tot_co + genstat.gratis

                if exc_compli:
                    tot_co = 0

            if not disp_accompany:

                cl_list = query(cl_list_data, filters=(lambda cl_list: cl_list.rmno == res_line.zinr and cl_list.resnr == res_line.resnr and cl_list.arrive == res_line.ankunft and cl_list.zipreis == 0 and (cl_list.a + cl_list.c) < 1 and cl_list.co < 1), first=True)

                if cl_list:
                    cl_list_data.remove(cl_list)
                    pass

            if exc_compli:

                cl_list = query(cl_list_data, filters=(lambda cl_list: cl_list.rmno == res_line.zinr and cl_list.resnr == res_line.resnr and cl_list.arrive == res_line.ankunft and cl_list.co > 0), first=True)

                if cl_list:
                    cl_list_data.remove(cl_list)
                    pass
                    tot_rm = tot_rm - 1

        for cl_list in query(cl_list_data, sort_by=[("nation",False),("bezeich",False)]):

            mealcoup = get_cache (Mealcoup, {"name": [(eq, "breakfast")],"resnr": [(eq, cl_list.resnr)],"zinr": [(eq, cl_list.rmno)]})

            if mealcoup:
                cl_list.tot_bfast = mealcoup.verbrauch[0] + mealcoup.verbrauch[1] + mealcoup.verbrauch[2] + mealcoup.verbrauch[3] + mealcoup.verbrauch[4] +\
                        mealcoup.verbrauch[5] + mealcoup.verbrauch[6] + mealcoup.verbrauch[7] + mealcoup.verbrauch[8] + mealcoup.verbrauch[9] +\
                        mealcoup.verbrauch[10] + mealcoup.verbrauch[11] + mealcoup.verbrauch[12] + mealcoup.verbrauch[13] + mealcoup.verbrauch[14] +\
                        mealcoup.verbrauch[15] + mealcoup.verbrauch[16] + mealcoup.verbrauch[17] + mealcoup.verbrauch[18] + mealcoup.verbrauch[19] +\
                        mealcoup.verbrauch[20] + mealcoup.verbrauch[21] + mealcoup.verbrauch[22] + mealcoup.verbrauch[23] + mealcoup.verbrauch[24] +\
                        mealcoup.verbrauch[25] + mealcoup.verbrauch[26] + mealcoup.verbrauch[27] + mealcoup.verbrauch[28] + mealcoup.verbrauch[29] +\
                        mealcoup.verbrauch[30] + mealcoup.verbrauch[31]

            s_list = query(s_list_data, filters=(lambda s_list: s_list.bezeich == cl_list.bezeich), first=True)

            if not s_list:

                s_list = query(s_list_data, filters=(lambda s_list: s_list.rmcat == ""), first=True)

                if s_list:
                    s_list.rmcat = cl_list.kurzbez
                    s_list.bezeich = cl_list.bezeich

            if not s_list:
                s_list = S_list()
                s_list_data.append(s_list)

                s_list.rmcat = cl_list.kurzbez
                s_list.bezeich = cl_list.bezeich
            s_list.anz = s_list.anz + cl_list.qty

            s_list = query(s_list_data, filters=(lambda s_list: s_list.nat == cl_list.nat), first=True)

            if not s_list:

                s_list = query(s_list_data, filters=(lambda s_list: s_list.nat == ""), first=True)

                if s_list:
                    s_list.nat = cl_list.nat

            if not s_list:
                s_list = S_list()
                s_list_data.append(s_list)


                if s_list:
                    s_list.nat = cl_list.nat
            s_list.adult = s_list.adult + cl_list.a + cl_list.co
            s_list.child = s_list.child + cl_list.c
            s_list.rmqty = s_list.rmqty + cl_list.qty

        if (tot_a + tot_co) != 0:

            for s_list in query(s_list_data, filters=(lambda s_list: s_list.nat != "")):

                nation = get_cache (Nation, {"kurzbez": [(eq, s_list.nat)]})

                if nation:
                    s_list.nat = nation.bezeich
                s_list.proz =  to_decimal(s_list.adult) / to_decimal((tot_a) + to_decimal(tot_co)) * to_decimal("100")

        # sort by rmno -> query diatas merubah sort order.-------------------
        for cl_list in query(cl_list_data, sort_by=[("rmno",False)]):
            pass
        #--------------------------------------------------------------------

    def create_buf_queasy():

        nonlocal tot_payrm, tot_rm, tot_a, tot_c, tot_co, tot_avail, tot_rmqty, inactive, cl_list_data, s_list_data, t_buff_queasy_data, vipnr1, vipnr2, vipnr3, vipnr4, vipnr5, vipnr6, vipnr7, vipnr8, vipnr9, tot_room, all_room, all_remark, queasy, htparam, zkstat, zinrstat, paramtext, guest, reservation, zimmer, zimkateg, res_line, guestseg, segment, mc_guest, mc_types, nation, waehrung, reslin_queasy, mealcoup, genstat
        nonlocal sorttype, datum, curr_date, curr_gastnr, froom, troom, exc_depart, incl_gcomment, incl_rsvcomment, prog_name, disp_accompany, disp_exclinact, split_rsv_print, exc_compli


        nonlocal setup_list, str_list, cl_list, s_list, zinr_list, t_buff_queasy
        nonlocal setup_list_data, str_list_data, cl_list_data, s_list_data, zinr_list_data, t_buff_queasy_data


        t_buff_queasy_data.clear()

        for queasy in db_session.query(Queasy).filter(
                 (Queasy.key == 140) & (Queasy.char1 == (prog_name).lower())).order_by(Queasy._recid).all():
            t_buff_queasy = T_buff_queasy()
            t_buff_queasy_data.append(t_buff_queasy)

            buffer_copy(queasy, t_buff_queasy)

    htparam = get_cache (Htparam, {"paramnr": [(eq, 700)]})

    if htparam.finteger != 0:
        vipnr1 = htparam.finteger

    htparam = get_cache (Htparam, {"paramnr": [(eq, 701)]})

    if htparam.finteger != 0:
        vipnr2 = htparam.finteger

    htparam = get_cache (Htparam, {"paramnr": [(eq, 702)]})

    if htparam.finteger != 0:
        vipnr3 = htparam.finteger

    htparam = get_cache (Htparam, {"paramnr": [(eq, 703)]})

    if htparam.finteger != 0:
        vipnr4 = htparam.finteger

    htparam = get_cache (Htparam, {"paramnr": [(eq, 704)]})

    if htparam.finteger != 0:
        vipnr5 = htparam.finteger

    htparam = get_cache (Htparam, {"paramnr": [(eq, 705)]})

    if htparam.finteger != 0:
        vipnr6 = htparam.finteger

    htparam = get_cache (Htparam, {"paramnr": [(eq, 706)]})

    if htparam.finteger != 0:
        vipnr7 = htparam.finteger

    htparam = get_cache (Htparam, {"paramnr": [(eq, 707)]})

    if htparam.finteger != 0:
        vipnr8 = htparam.finteger

    htparam = get_cache (Htparam, {"paramnr": [(eq, 708)]})

    if htparam.finteger != 0:
        vipnr9 = htparam.finteger
    bed_setup()

    if sorttype == 1:
        # by Room
        if disp_exclinact:

            if datum >= curr_date:
                print("create_inhouse2")
                create_inhouse2()
            else:
                print("create_genstat_inhouse2")
                create_genstat_inhouse2()
        else:

            if datum >= curr_date:
                print("create_inhouse")
                create_inhouse()
            else:
                print("create_genstat_inhouse")
                create_genstat_inhouse()
    else:

        if disp_exclinact:

            if datum >= curr_date:
                print("create_inhouse3")
                create_inhouse3()
            else:
                print("create_genstat_inhouse3")
                create_genstat_inhouse3()
        else:

            if datum >= curr_date:
                print("create_inhouse1")
                create_inhouse1()
            else:
                print("create_genstat_inhouse1")
                create_genstat_inhouse1()
    
    create_buf_queasy()

    if datum < curr_date:

        for zkstat in db_session.query(Zkstat).filter(
                 (Zkstat.datum == datum)).order_by(Zkstat._recid).all():
            tot_room = tot_room + zkstat.anz100

        zinrstat = get_cache (Zinrstat, {"zinr": [(eq, "tot-rm")],"datum": [(eq, datum)]})

        if zinrstat:
            all_room = zinrstat.zimmeranz
        inactive = all_room - tot_room

    return generate_output()