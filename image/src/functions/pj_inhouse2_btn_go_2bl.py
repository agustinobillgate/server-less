from functions.additional_functions import *
import decimal
from datetime import date
from sqlalchemy import func
from models import Queasy, Htparam, Zkstat, Zinrstat, Paramtext, Guest, Reservation, Zimmer, Zimkateg, Res_line, Guestseg, Segment, Mc_guest, Mc_types, Nation, Waehrung, Reslin_queasy, Mealcoup, Genstat

def pj_inhouse2_btn_go_2bl(sorttype:int, datum:date, curr_date:date, curr_gastnr:int, froom:str, troom:str, exc_depart:bool, incl_gcomment:bool, incl_rsvcomment:bool, prog_name:str, disp_accompany:bool, disp_exclinact:bool):
    tot_payrm = 0
    tot_rm = 0
    tot_a = 0
    tot_c = 0
    tot_co = 0
    tot_avail = 0
    tot_rmqty = 0
    inactive = 0
    cl_list_list = []
    s_list_list = []
    t_buff_queasy_list = []
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
    all_remark:str = ""
    queasy = htparam = zkstat = zinrstat = paramtext = guest = reservation = zimmer = zimkateg = res_line = guestseg = segment = mc_guest = mc_types = nation = waehrung = reslin_queasy = mealcoup = genstat = None

    setup_list = str_list = cl_list = s_list = zinr_list = t_buff_queasy = gmember = gbuff = rbuff = None

    setup_list_list, Setup_list = create_model("Setup_list", {"nr":int, "char":str})
    str_list_list, Str_list = create_model("Str_list", {"flag":int, "rflag":bool, "line1":str, "line2":str, "line3":str, "company":str}, {"rflag": True})
    cl_list_list, Cl_list = create_model("Cl_list", {"flag":int, "karteityp":int, "nr":int, "vip":str, "resnr":int, "name":str, "groupname":str, "rmno":str, "qty":int, "arrive":date, "depart":date, "rmcat":str, "ratecode":str, "zipreis":decimal, "kurzbez":str, "bezeich":str, "a":int, "c":int, "co":int, "pax":str, "nat":str, "nation":str, "argt":str, "company":str, "flight":str, "etd":str, "paym":int, "segm":str, "telefon":str, "mobil_tel":str, "created":date, "createid":str, "bemerk":str, "bemerk01":str, "bemerk02":str, "bemerk03":str, "bemerk04":str, "bemerk05":str, "bemerk06":str, "bemerk07":str, "bemerk08":str, "bemerk1":str, "ci_time":str, "curr":str, "spreq":str, "tot_bfast":int, "local_reg":str})
    s_list_list, S_list = create_model("S_list", {"rmcat":str, "bezeich":str, "nat":str, "anz":int, "adult":int, "proz":decimal, "child":int, "rmqty":int})
    zinr_list_list, Zinr_list = create_model("Zinr_list", {"resnr":int, "reslinnr":int, "zinr":str})
    t_buff_queasy_list, T_buff_queasy = create_model_like(Queasy)

    Gmember = Guest
    Gbuff = Guest
    Rbuff = Reservation

    db_session = local_storage.db_session

    def generate_output():
        nonlocal tot_payrm, tot_rm, tot_a, tot_c, tot_co, tot_avail, tot_rmqty, inactive, cl_list_list, s_list_list, t_buff_queasy_list, vipnr1, vipnr2, vipnr3, vipnr4, vipnr5, vipnr6, vipnr7, vipnr8, vipnr9, tot_room, all_room, all_remark, queasy, htparam, zkstat, zinrstat, paramtext, guest, reservation, zimmer, zimkateg, res_line, guestseg, segment, mc_guest, mc_types, nation, waehrung, reslin_queasy, mealcoup, genstat
        nonlocal gmember, gbuff, rbuff


        nonlocal setup_list, str_list, cl_list, s_list, zinr_list, t_buff_queasy, gmember, gbuff, rbuff
        nonlocal setup_list_list, str_list_list, cl_list_list, s_list_list, zinr_list_list, t_buff_queasy_list
        return {"tot_payrm": tot_payrm, "tot_rm": tot_rm, "tot_a": tot_a, "tot_c": tot_c, "tot_co": tot_co, "tot_avail": tot_avail, "tot_rmqty": tot_rmqty, "inactive": inactive, "cl-list": cl_list_list, "s-list": s_list_list, "t-buff-queasy": t_buff_queasy_list}

    def bed_setup():

        nonlocal tot_payrm, tot_rm, tot_a, tot_c, tot_co, tot_avail, tot_rmqty, inactive, cl_list_list, s_list_list, t_buff_queasy_list, vipnr1, vipnr2, vipnr3, vipnr4, vipnr5, vipnr6, vipnr7, vipnr8, vipnr9, tot_room, all_room, all_remark, queasy, htparam, zkstat, zinrstat, paramtext, guest, reservation, zimmer, zimkateg, res_line, guestseg, segment, mc_guest, mc_types, nation, waehrung, reslin_queasy, mealcoup, genstat
        nonlocal gmember, gbuff, rbuff


        nonlocal setup_list, str_list, cl_list, s_list, zinr_list, t_buff_queasy, gmember, gbuff, rbuff
        nonlocal setup_list_list, str_list_list, cl_list_list, s_list_list, zinr_list_list, t_buff_queasy_list


        setup_list = Setup_list()
        setup_list_list.append(setup_list)

        setup_list.nr = 1
        setup_list.char = " "

        for paramtext in db_session.query(Paramtext).filter(
                (Paramtext.txtnr >= 9201) &  (Paramtext.txtnr <= 9299)).all():
            setup_list = Setup_list()
            setup_list_list.append(setup_list)

            setup_list.nr = paramtext.txtnr - 9199
            setup_list.char = substring(paramtext.notes, 0, 1)

    def create_inhouse():

        nonlocal tot_payrm, tot_rm, tot_a, tot_c, tot_co, tot_avail, tot_rmqty, inactive, cl_list_list, s_list_list, t_buff_queasy_list, vipnr1, vipnr2, vipnr3, vipnr4, vipnr5, vipnr6, vipnr7, vipnr8, vipnr9, tot_room, all_room, all_remark, queasy, htparam, zkstat, zinrstat, paramtext, guest, reservation, zimmer, zimkateg, res_line, guestseg, segment, mc_guest, mc_types, nation, waehrung, reslin_queasy, mealcoup, genstat
        nonlocal gmember, gbuff, rbuff


        nonlocal setup_list, str_list, cl_list, s_list, zinr_list, t_buff_queasy, gmember, gbuff, rbuff
        nonlocal setup_list_list, str_list_list, cl_list_list, s_list_list, zinr_list_list, t_buff_queasy_list

        i:int = 0
        j:int = 0
        vip_flag:str = ""
        nr:int = 0
        str:str = ""
        actflag1:int = 0
        actflag2:int = 0
        do_it:bool = False
        Gmember = Guest
        Gbuff = Guest
        Rbuff = Reservation
        zinr_list_list.clear()

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
        s_list_list.clear()
        cl_list_list.clear()
        str_list_list.clear()
        tot_avail = 0

        for zimmer in db_session.query(Zimmer).filter(
                (Zimmer.sleeping)).all():
            tot_avail = tot_avail + 1

        res_line_obj_list = []
        for res_line, zimkateg, reservation, guest, gmember in db_session.query(Res_line, Zimkateg, Reservation, Guest, Gmember).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Guest,(Guest.gastnr == reservation.gastnr)).join(Gmember,(Gmember.gastnr == Res_line.gastnrmember)).filter(
                (Res_line.active_flag >= actflag1) &  (Res_line.active_flag <= actflag2) &  (Res_line.resstatus != 9) &  (Res_line.resstatus != 10) &  (Res_line.resstatus != 12) &  (Res_line.ankunft <= datum) &  (Res_line.abreise >= datum) &  (func.lower(Res_line.zinr) >= (froom).lower()) &  (func.lower(Res_line.zinr) <= (troom).lower())).all():
            if res_line._recid in res_line_obj_list:
                continue
            else:
                res_line_obj_list.append(res_line._recid)

            if exc_depart and res_line.abreise == datum:
                1
            else:

                setup_list = query(setup_list_list, filters=(lambda setup_list :setup_list.nr == res_line.setup + 1), first=True)

                zimmer = db_session.query(Zimmer).filter(
                        (Zimmer.zinr == res_line.zinr)).first()
                nr = nr + 1
                vip_flag = ""

                guestseg = db_session.query(Guestseg).filter(
                        (Guestseg.gastnr == gmember.gastnr) &  ((Guestseg.segmentcode == vipnr1) |  (Guestseg.segmentcode == vipnr2) |  (Guestseg.segmentcode == vipnr3) |  (Guestseg.segmentcode == vipnr4) |  (Guestseg.segmentcode == vipnr5) |  (Guestseg.segmentcode == vipnr6) |  (Guestseg.segmentcode == vipnr7) |  (Guestseg.segmentcode == vipnr8) |  (Guestseg.segmentcode == vipnr9))).first()

                if guestseg:

                    segment = db_session.query(Segment).filter(
                            (Segment.segmentcode == guestseg.segmentcode)).first()
                    vip_flag = segment.bezeich


                cl_list = Cl_list()
                cl_list_list.append(cl_list)

                cl_list.nr = nr
                cl_list.rmcat = zimkateg.kurzbez + setup_list.char
                cl_list.kurzbez = zimkateg.kurzbez
                cl_list.bezeich = zimkateg.bezeich
                cl_list.nat = gmember.nation1
                cl_list.resnr = res_line.resnr
                cl_list.vip = vip_flag
                cl_list.name = res_line.name
                cl_list.rmno = res_line.zinr
                cl_list.zipreis = res_line.zipreis
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
                cl_list.createID = reservation.useridanlage

                mc_guest = db_session.query(Mc_guest).filter(
                        (Mc_guest.gastnr == gmember.gastnr)).first()

                if mc_guest:
                    cl_list.telefon = gmember.telefon + ";" + mc_guest.cardnum
                else:
                    cl_list.telefon = gmember.telefon

                mc_types = db_session.query(Mc_types).filter(
                        (Mc_types.nr == mc_guest.nr)).first()

                if mc_types:
                    cl_list.mobil_tel = gmember.mobil_telefon + ";" + mc_types.bezeich
                else:
                    cl_list.mobil_tel = gmember.mobil_telefon

                nation = db_session.query(Nation).filter(
                        (Nation.kurzbez == gmember.nation2)).first()

                if nation:
                    cl_list.local_reg = nation.bezeich

                waehrung = db_session.query(Waehrung).filter(
                        (Waehrungsnr == res_line.betriebsnr)).first()

                if waehrung:
                    cl_list.curr = waehrung.wabkurz + ";" + gmember.email_adr

                reslin_queasy = db_session.query(Reslin_queasy).filter(
                        (func.lower(Reslin_queasy.key) == "specialRequest") &  (Reslin_queasy.resnr == res_line.resnr) &  (Reslin_queasy.reslinnr == res_line.reslinnr)).first()

                if reslin_queasy:
                    cl_list.spreq = reslin_queasy.char3 + "," + cl_list.spreq

                reslin_queasy = db_session.query(Reslin_queasy).filter(
                        (func.lower(Reslin_queasy.key) == "arrangement") &  (Reslin_queasy.resnr == res_line.resnr) &  (Reslin_queasy.reslinnr == res_line.reslinnr) &  (Reslin_queasy.datum >= Reslin_queasy.date1) &  (Reslin_queasy.datum <= Reslin_queasy.date2)).first()

                if reslin_queasy:

                    if reslin_queasy.char2 != "":
                        cl_list.ratecode = reslin_queasy.char2
                    else:
                        for i in range(1,num_entries(res_line.zimmer_wunsch, ";") - 1 + 1) :
                            str = entry(i - 1, res_line.zimmer_wunsch, ";")

                            if substring(str, 0, 6) == "$CODE$":
                                cl_list.ratecode = substring(str, 6)
                                break

                mealcoup = db_session.query(Mealcoup).filter(
                        (func.lower(Mealcoup.name) == "Breakfast") &  (Mealcoup.resnr == res_line.resnr) &  (Mealcoup.zinr == res_line.zinr)).first()

                if mealcoup:
                    cl_list.tot_bfast = mealcoup.verbrauch[0] + mealcoup.verbrauch[1] + mealcoup.verbrauch[2] + mealcoup.verbrauch[3] + mealcoup.verbrauch[4] +\
                            mealcoup.verbrauch[5] + mealcoup.verbrauch[6] + mealcoup.verbrauch[7] + mealcoup.verbrauch[8] + mealcoup.verbrauch[9] +\
                            mealcoup.verbrauch[10] + mealcoup.verbrauch[11] + mealcoup.verbrauch[12] + mealcoup.verbrauch[13] + mealcoup.verbrauch[14] +\
                            mealcoup.verbrauch[15] + mealcoup.verbrauch[16] + mealcoup.verbrauch[17] + mealcoup.verbrauch[18] + mealcoup.verbrauch[19] +\
                            mealcoup.verbrauch[20] + mealcoup.verbrauch[21] + mealcoup.verbrauch[22] + mealcoup.verbrauch[23] + mealcoup.verbrauch[24] +\
                            mealcoup.verbrauch[25] + mealcoup.verbrauch[26] + mealcoup.verbrauch[27] + mealcoup.verbrauch[28] + mealcoup.verbrauch[29] +\
                            mealcoup.verbrauch[30] + mealcoup.verbrauch[31]

                segment = db_session.query(Segment).filter(
                        (Segment.segmentcode == reservation.segmentcode)).first()

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

                if incl_gcomment:

                    gbuff = db_session.query(Gbuff).filter(
                            (Gbuff.gastnr == res_line.gastnrmember)).first()

                    if gbuff:
                        for i in range(1,len(gbuff.bemerk)  + 1) :

                            if substring(gbuff.bemerk, i - 1, 1) == chr(10):
                                cl_list.bemerk = cl_list.bemerk + " "
                            else:
                                cl_list.bemerk = cl_list.bemerk + substring(trim(gbuff.bemerk) , i - 1, 1)
                    cl_list.bemerk = cl_list.bemerk + " || "

                if incl_rsvcomment:

                    rbuff = db_session.query(Rbuff).filter(
                            (Rbuff.gastnr == reservation.gastnr)).first()

                    if rbuff:
                        for j in range(1,len(rbuff.bemerk)  + 1) :

                            if substring(rbuff.bemerk, j - 1, 1) == chr(10):
                                cl_list.bemerk1 = cl_list.bemerk1 + " "
                            else:
                                cl_list.bemerk1 = cl_list.bemerk1 + substring(trim(rbuff.bemerk) , j - 1, 1)
                    cl_list.bemerk = cl_list.bemerk + cl_list.bemerk1 + " || "
                for i in range(1,len(res_line.bemerk)  + 1) :

                    if substring(res_line.bemerk, i - 1, 1) == chr (10):
                        cl_list.bemerk = cl_list.bemerk + " "
                    else:
                        cl_list.bemerk = cl_list.bemerk + substring(trim(res_line.bemerk) , i - 1, 1)
                all_remark = res_line.bemerk
                all_remark = replace_str(all_remark, chr(10) , " ")
                all_remark = replace_str(all_remark, chr(13) , " ")
                cl_list.bemerk01 = to_string(substring(all_remark, 0, 225))
                cl_list.bemerk02 = to_string(substring(all_remark, 225, 225))
                cl_list.bemerk03 = to_string(substring(all_remark, 450, 225))
                cl_list.bemerk04 = to_string(substring(all_remark, 675, 225))
                cl_list.pax = to_string(cl_list.a, ">9") + "/" + to_string(cl_list.c, "9") + " " + to_string(cl_list.co, "9")

                if cl_list.nat == "":
                    cl_list.nat = "?"
                else:

                    nation = db_session.query(Nation).filter(
                            (Nation.kurzbez == cl_list.nat)).first()

                    if nation:
                        cl_list.nation = nation.bezeich

                zinr_list = query(zinr_list_list, filters=(lambda zinr_list :zinr_list.zinr == res_line.zinr and zinr_list.resnr == res_line.resnr and zinr_list.reslinnr == res_line.reslinnr), first=True)

                if not zinr_list:
                    zinr_list = Zinr_list()
                    zinr_list_list.append(zinr_list)

                    zinr_list.resnr = res_line.resnr
                    zinr_list.reslinnr = res_line.reslinnr
                    zinr_list.zinr = res_line.zinr

                    queasy = db_session.query(Queasy).filter(
                            (Queasy.key == 14) &  (Queasy.char1 == res_line.zinr) &  (Queasy.date1 <= curr_date) &  (Queasy.date2 >= curr_date)).first()

                    if zimmer.sleeping and res_line.resstatus != 13:

                        if not queasy:
                            tot_rm = tot_rm + res_line.zimmeranz
                            tot_rmqty = tot_rmqty + res_line.zimmeranz

                        elif queasy and queasy.number3 != res_line.gastnr:
                            tot_rm = tot_rm + res_line.zimmeranz
                            tot_rmqty = tot_rmqty + res_line.zimmeranz

                    if zimmer.sleeping and res_line.zipreis > 0 and res_line.resstatus != 13:

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

            if not disp_accompany:

                cl_list = query(cl_list_list, filters=(lambda cl_list :cl_list.rmno == res_line.zinr and cl_list.resnr == res_line.resnr and cl_list.arrive == res_line.ankunft and cl_list.zipreis == 0 and (cl_list.a + cl_list.c) < 1 and cl_list.co < 1), first=True)

                if cl_list:
                    cl_list_list.remove(cl_list)

                    nr = nr - 1

        for cl_list in query(cl_list_list):

            s_list = query(s_list_list, filters=(lambda s_list :s_list.rmcat == cl_list.kurzbez), first=True)

            if not s_list:

                s_list = query(s_list_list, filters=(lambda s_list :s_list.rmcat == ""), first=True)

                if s_list:
                    s_list.rmcat = cl_list.kurzbez
                    s_list.bezeich = cl_list.bezeich

            if not s_list:
                s_list = S_list()
                s_list_list.append(s_list)

                s_list.rmcat = cl_list.kurzbez
                s_list.bezeich = cl_list.bezeich
            s_list.anz = s_list.anz + cl_list.qty

            s_list = query(s_list_list, filters=(lambda s_list :s_list.nat == cl_list.nat), first=True)

            if not s_list:

                s_list = query(s_list_list, filters=(lambda s_list :s_list.nat == ""), first=True)

                if s_list:
                    s_list.nat = cl_list.nat

            if not s_list:
                s_list = S_list()
                s_list_list.append(s_list)


                if s_list:
                    s_list.nat = cl_list.nat
            s_list.adult = s_list.adult + cl_list.a + cl_list.co
            s_list.child = s_list.child + cl_list.c
            s_list.rmqty = s_list.rmqty + cl_list.qty

        if (tot_a + tot_co) != 0:

            for s_list in query(s_list_list, filters=(lambda s_list :s_list.nat != "")):

                nation = db_session.query(Nation).filter(
                        (Nation.kurzbez == s_list.nat)).first()

                if nation:
                    s_list.nat = nation.bezeich
                s_list.proz = s_list.adult / (tot_a + tot_co) * 100


    def create_genstat_inhouse():

        nonlocal tot_payrm, tot_rm, tot_a, tot_c, tot_co, tot_avail, tot_rmqty, inactive, cl_list_list, s_list_list, t_buff_queasy_list, vipnr1, vipnr2, vipnr3, vipnr4, vipnr5, vipnr6, vipnr7, vipnr8, vipnr9, tot_room, all_room, all_remark, queasy, htparam, zkstat, zinrstat, paramtext, guest, reservation, zimmer, zimkateg, res_line, guestseg, segment, mc_guest, mc_types, nation, waehrung, reslin_queasy, mealcoup, genstat
        nonlocal gmember, gbuff, rbuff


        nonlocal setup_list, str_list, cl_list, s_list, zinr_list, t_buff_queasy, gmember, gbuff, rbuff
        nonlocal setup_list_list, str_list_list, cl_list_list, s_list_list, zinr_list_list, t_buff_queasy_list

        i:int = 0
        j:int = 0
        vip_flag:str = ""
        nr:int = 0
        str:str = ""
        actflag1:int = 0
        actflag2:int = 0
        do_it:bool = False
        z:int = 0
        Gmember = Guest
        Gbuff = Guest
        Rbuff = Reservation
        zinr_list_list.clear()

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
        s_list_list.clear()
        cl_list_list.clear()
        str_list_list.clear()
        tot_avail = 0

        for zkstat in db_session.query(Zkstat).filter(
                (Zkstat.datum == datum)).all():
            tot_avail = tot_avail + zkstat.anz100

        genstat_obj_list = []
        for genstat, zimkateg, reservation, guest, gmember in db_session.query(Genstat, Zimkateg, Reservation, Guest, Gmember).join(Zimkateg,(Zimkateg.zikatnr == Genstat.zikatnr)).join(Reservation,(Reservation.resnr == Genstat.resnr)).join(Guest,(Guest.gastnr == Genstat.gastnr)).join(Gmember,(Gmember.gastnr == Genstat.gastnrmember)).filter(
                (Genstat.datum == datum) &  (func.lower(Genstat.zinr) >= (froom).lower()) &  (func.lower(Genstat.zinr) <= (troom).lower())).all():
            if genstat._recid in genstat_obj_list:
                continue
            else:
                genstat_obj_list.append(genstat._recid)

            if genstat.res_date[0] < datum and genstat.res_date[1] == datum and genstat.resstatus == 8:
                1

            elif exc_depart and genstat.res_date[0] <= datum and genstat.res_date[1] == datum and genstat.resstatus == 8:
                1
            else:

                res_line = db_session.query(Res_line).filter(
                        (Res_line.resnr == genstat.resnr) &  (Res_line.reslinnr == genstat.res_int[0])).first()

                setup_list = query(setup_list_list, filters=(lambda setup_list :setup_list.nr == res_line.setup + 1), first=True)

                zimmer = db_session.query(Zimmer).filter(
                        (Zimmer.zinr == genstat.zinr)).first()
                nr = nr + 1
                vip_flag = ""

                guestseg = db_session.query(Guestseg).filter(
                        (Guestseg.gastnr == gmember.gastnr) &  ((Guestseg.segmentcode == vipnr1) |  (Guestseg.segmentcode == vipnr2) |  (Guestseg.segmentcode == vipnr3) |  (Guestseg.segmentcode == vipnr4) |  (Guestseg.segmentcode == vipnr5) |  (Guestseg.segmentcode == vipnr6) |  (Guestseg.segmentcode == vipnr7) |  (Guestseg.segmentcode == vipnr8) |  (Guestseg.segmentcode == vipnr9))).first()

                if guestseg:

                    segment = db_session.query(Segment).filter(
                            (Segment.segmentcode == guestseg.segmentcode)).first()
                    vip_flag = replace_str(segment.bezeich, " ", "")
                cl_list = Cl_list()
                cl_list_list.append(cl_list)

                cl_list.nr = nr
                cl_list.rmcat = zimkateg.kurzbez + setup_list.char
                cl_list.kurzbez = zimkateg.kurzbez
                cl_list.bezeich = zimkateg.bezeich
                cl_list.nat = gmember.nation1
                cl_list.resnr = genstat.resnr
                cl_list.vip = vip_flag
                cl_list.name = gmember.name + ", " + gmember.vorname1 +\
                        " " + gmember.anrede1
                cl_list.rmno = genstat.zinr
                cl_list.zipreis = genstat.zipreis
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
                cl_list.createID = reservation.useridanlage

                mc_guest = db_session.query(Mc_guest).filter(
                        (Mc_guest.gastnr == gmember.gastnr)).first()

                if mc_guest:
                    cl_list.telefon = gmember.telefon + ";" + mc_guest.cardnum
                else:
                    cl_list.telefon = gmember.telefon

                mc_types = db_session.query(Mc_types).filter(
                        (Mc_types.nr == mc_guest.nr)).first()

                if mc_types:
                    cl_list.mobil_tel = gmember.mobil_telefon + ";" + mc_types.bezeich
                else:
                    cl_list.mobil_tel = gmember.mobil_telefon

                nation = db_session.query(Nation).filter(
                        (Nation.kurzbez == gmember.nation2)).first()

                if nation:
                    cl_list.local_reg = nation.bezeich

                waehrung = db_session.query(Waehrung).filter(
                        (Waehrungsnr == res_line.betriebsnr)).first()

                if waehrung:
                    cl_list.curr = waehrung.wabkurz + ";" + gmember.email_adr

                reslin_queasy = db_session.query(Reslin_queasy).filter(
                        (func.lower(Reslin_queasy.key) == "specialRequest") &  (Reslin_queasy.resnr == res_line.resnr) &  (Reslin_queasy.reslinnr == res_line.reslinnr)).first()

                if reslin_queasy:
                    cl_list.spreq = reslin_queasy.char3 + "," + cl_list.spreq

                reslin_queasy = db_session.query(Reslin_queasy).filter(
                        (func.lower(Reslin_queasy.key) == "arrangement") &  (Reslin_queasy.resnr == res_line.resnr) &  (Reslin_queasy.reslinnr == res_line.reslinnr) &  (Reslin_queasy.datum >= Reslin_queasy.date1) &  (Reslin_queasy.datum <= Reslin_queasy.date2)).first()

                if reslin_queasy:

                    if reslin_queasy.char2 != "":
                        cl_list.ratecode = reslin_queasy.char2
                    else:
                        for i in range(1,num_entries(res_line.zimmer_wunsch, ";") - 1 + 1) :
                            str = entry(i - 1, res_line.zimmer_wunsch, ";")

                            if substring(str, 0, 6) == "$CODE$":
                                cl_list.ratecode = substring(str, 6)
                                break

                segment = db_session.query(Segment).filter(
                        (Segment.segmentcode == genstat.segmentcode)).first()

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

                if incl_gcomment:

                    gbuff = db_session.query(Gbuff).filter(
                            (Gbuff.gastnr == res_line.gastnrmember)).first()

                    if gbuff:
                        for i in range(1,len(gbuff.bemerk)  + 1) :

                            if substring(gbuff.bemerk, i - 1, 1) == chr(10):
                                cl_list.bemerk = cl_list.bemerk + " "
                            else:
                                cl_list.bemerk = cl_list.bemerk + substring(trim(gbuff.bemerk) , i - 1, 1)
                    cl_list.bemerk = cl_list.bemerk + " || "

                if incl_rsvcomment:

                    rbuff = db_session.query(Rbuff).filter(
                            (Rbuff.gastnr == reservation.gastnr)).first()

                    if rbuff:
                        for j in range(1,len(rbuff.bemerk)  + 1) :

                            if substring(rbuff.bemerk, j - 1, 1) == chr(10):
                                cl_list.bemerk1 = cl_list.bemerk1 + " "
                            else:
                                cl_list.bemerk1 = cl_list.bemerk1 + substring(trim(rbuff.bemerk) , j - 1, 1)
                    cl_list.bemerk = cl_list.bemerk + cl_list.bemerk1 + " || "
                for i in range(1,len(res_line.bemerk)  + 1) :

                    if substring(res_line.bemerk, i - 1, 1) == chr (10):
                        cl_list.bemerk = cl_list.bemerk + " "
                    else:
                        cl_list.bemerk = cl_list.bemerk + substring(trim(res_line.bemerk) , i - 1, 1)
                all_remark = res_line.bemerk
                all_remark = replace_str(all_remark, chr(10) , " ")
                all_remark = replace_str(all_remark, chr(13) , " ")
                cl_list.bemerk01 = to_string(substring(all_remark, 0, 225))
                cl_list.bemerk02 = to_string(substring(all_remark, 225, 225))
                cl_list.bemerk03 = to_string(substring(all_remark, 450, 225))
                cl_list.bemerk04 = to_string(substring(all_remark, 675, 225))
                cl_list.pax = to_string(cl_list.a, ">9") + "/" + to_string(cl_list.c, "9") + " " + to_string(cl_list.co, "9")

                if cl_list.nat == "":
                    cl_list.nat = "?"
                else:

                    nation = db_session.query(Nation).filter(
                            (Nation.kurzbez == cl_list.nat)).first()

                    if nation:
                        cl_list.nation = nation.bezeich

                zinr_list = query(zinr_list_list, filters=(lambda zinr_list :zinr_list.zinr == genstat.zinr and zinr_list.resnr == res_line.resnr and zinr_list.reslinnr == res_line.reslinnr), first=True)

                if not zinr_list:
                    zinr_list = Zinr_list()
                    zinr_list_list.append(zinr_list)

                    zinr_list.resnr = res_line.resnr
                    zinr_list.reslinnr = res_line.reslinnr
                    zinr_list.zinr = genstat.zinr

                    queasy = db_session.query(Queasy).filter(
                            (Queasy.key == 14) &  (Queasy.char1 == genstat.zinr) &  (Queasy.date1 <= curr_date) &  (Queasy.date2 >= curr_date)).first()

                    if zimmer.sleeping and genstat.resstatus != 13:

                        if not queasy:
                            tot_rm = tot_rm + 1
                            tot_rmqty = tot_rmqty + 1

                        elif queasy and queasy.number3 != genstat.gastnr:
                            tot_rm = tot_rm + 1
                            tot_rmqty = tot_rmqty + 1

                    if zimmer.sleeping and genstat.zipreis > 0 and genstat.resstatus != 13:
                        DO: z = z + 1

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

        if not disp_accompany:

            cl_list = query(cl_list_list, filters=(lambda cl_list :cl_list.rmno == res_line.zinr and cl_list.resnr == res_line.resnr and cl_list.arrive == res_line.ankunft and cl_list.zipreis == 0 and (cl_list.a + cl_list.c) < 1 and cl_list.co < 1), first=True)

            if cl_list:
                cl_list_list.remove(cl_list)

                nr = nr - 1

    def create_inhouse1():

        nonlocal tot_payrm, tot_rm, tot_a, tot_c, tot_co, tot_avail, tot_rmqty, inactive, cl_list_list, s_list_list, t_buff_queasy_list, vipnr1, vipnr2, vipnr3, vipnr4, vipnr5, vipnr6, vipnr7, vipnr8, vipnr9, tot_room, all_room, all_remark, queasy, htparam, zkstat, zinrstat, paramtext, guest, reservation, zimmer, zimkateg, res_line, guestseg, segment, mc_guest, mc_types, nation, waehrung, reslin_queasy, mealcoup, genstat
        nonlocal gmember, gbuff, rbuff


        nonlocal setup_list, str_list, cl_list, s_list, zinr_list, t_buff_queasy, gmember, gbuff, rbuff
        nonlocal setup_list_list, str_list_list, cl_list_list, s_list_list, zinr_list_list, t_buff_queasy_list

        i:int = 0
        j:int = 0
        vip_flag:str = ""
        str:str = ""
        nr:int = 0
        curr_gastnr:int = 0
        actflag1:int = 0
        actflag2:int = 0
        Gmember = Guest
        Gbuff = Guest
        Rbuff = Reservation
        zinr_list_list.clear()

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
        s_list_list.clear()
        cl_list_list.clear()
        str_list_list.clear()
        tot_avail = 0

        for zimmer in db_session.query(Zimmer).filter(
                (Zimmer.sleeping)).all():
            tot_avail = tot_avail + 1

        res_line_obj_list = []
        for res_line, zimkateg, reservation, guest, gmember in db_session.query(Res_line, Zimkateg, Reservation, Guest, Gmember).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Guest,(Guest.gastnr == reservation.gastnr)).join(Gmember,(Gmember.gastnr == Res_line.gastnrmember)).filter(
                (Res_line.active_flag >= actflag1) &  (Res_line.active_flag <= actflag2) &  (Res_line.resstatus != 9) &  (Res_line.resstatus != 10) &  (Res_line.resstatus != 12) &  (Res_line.ankunft <= datum) &  (Res_line.abreise >= datum) &  (func.lower(Res_line.zinr) >= (froom).lower()) &  (func.lower(Res_line.zinr) <= (troom).lower())).all():
            if res_line._recid in res_line_obj_list:
                continue
            else:
                res_line_obj_list.append(res_line._recid)

            if exc_depart and res_line.abreise == datum:
                pass
            else:

                setup_list = query(setup_list_list, filters=(lambda setup_list :setup_list.nr == res_line.setup + 1), first=True)

                zimmer = db_session.query(Zimmer).filter(
                        (Zimmer.zinr == res_line.zinr)).first()

                if curr_gastnr != guest.gastnr:
                    nr = 0
                    curr_gastnr = guest.gastnr

                if guest.karteityp > 0:
                    nr = nr + 1
                vip_flag = ""

                guestseg = db_session.query(Guestseg).filter(
                        (Guestseg.gastnr == gmember.gastnr) &  ((Guestseg.segmentcode == vipnr1) |  (Guestseg.segmentcode == vipnr2) |  (Guestseg.segmentcode == vipnr3) |  (Guestseg.segmentcode == vipnr4) |  (Guestseg.segmentcode == vipnr5) |  (Guestseg.segmentcode == vipnr6) |  (Guestseg.segmentcode == vipnr7) |  (Guestseg.segmentcode == vipnr8) |  (Guestseg.segmentcode == vipnr9))).first()

                if guestseg:

                    segment = db_session.query(Segment).filter(
                            (Segment.segmentcode == guestseg.segmentcode)).first()
                    vip_flag = segment.bezeich


                cl_list = Cl_list()
                cl_list_list.append(cl_list)

                cl_list.nr = nr
                cl_list.karteityp = guest.karteityp
                cl_list.rmcat = zimkateg.kurzbez + setup_list.char
                cl_list.kurzbez = zimkateg.kurzbez
                cl_list.bezeich = zimkateg.bezeich
                cl_list.nat = gmember.nation1
                cl_list.resnr = res_line.resnr
                cl_list.vip = vip_flag
                cl_list.name = res_line.name
                cl_list.rmno = res_line.zinr
                cl_list.zipreis = res_line.zipreis
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
                cl_list.createID = reservation.useridanlage

                mc_guest = db_session.query(Mc_guest).filter(
                        (Mc_guest.gastnr == gmember.gastnr)).first()

                if mc_guest:
                    cl_list.telefon = gmember.telefon + ";" + mc_guest.cardnum
                else:
                    cl_list.telefon = gmember.telefon

                mc_types = db_session.query(Mc_types).filter(
                        (Mc_types.nr == mc_guest.nr)).first()

                if mc_types:
                    cl_list.mobil_tel = gmember.mobil_telefon + ";" + mc_types.bezeich
                else:
                    cl_list.mobil_tel = gmember.mobil_telefon

                nation = db_session.query(Nation).filter(
                        (Nation.kurzbez == gmember.nation2)).first()

                if nation:
                    cl_list.local_reg = nation.bezeich

                waehrung = db_session.query(Waehrung).filter(
                        (Waehrungsnr == res_line.betriebsnr)).first()

                if waehrung:
                    cl_list.curr = waehrung.wabkurz + ";" + gmember.email_adr

                reslin_queasy = db_session.query(Reslin_queasy).filter(
                        (func.lower(Reslin_queasy.key) == "specialRequest") &  (Reslin_queasy.resnr == res_line.resnr) &  (Reslin_queasy.reslinnr == res_line.reslinnr)).first()

                if reslin_queasy:
                    cl_list.spreq = reslin_queasy.char3 + "," + cl_list.spreq

                reslin_queasy = db_session.query(Reslin_queasy).filter(
                        (func.lower(Reslin_queasy.key) == "arrangement") &  (Reslin_queasy.resnr == res_line.resnr) &  (Reslin_queasy.reslinnr == res_line.reslinnr) &  (Reslin_queasy.datum >= Reslin_queasy.date1) &  (Reslin_queasy.datum <= Reslin_queasy.date2)).first()

                if reslin_queasy:

                    if reslin_queasy.char2 != "":
                        cl_list.ratecode = reslin_queasy.char2
                    else:
                        for i in range(1,num_entries(res_line.zimmer_wunsch, ";") - 1 + 1) :
                            str = entry(i - 1, res_line.zimmer_wunsch, ";")

                            if substring(str, 0, 6) == "$CODE$":
                                cl_list.ratecode = substring(str, 6)
                                break

                mealcoup = db_session.query(Mealcoup).filter(
                        (func.lower(Mealcoup.name) == "Breakfast") &  (Mealcoup.resnr == res_line.resnr) &  (Mealcoup.zinr == res_line.zinr)).first()

                if mealcoup:
                    cl_list.tot_bfast = mealcoup.verbrauch[0] + mealcoup.verbrauch[1] + mealcoup.verbrauch[2] + mealcoup.verbrauch[3] + mealcoup.verbrauch[4] +\
                            mealcoup.verbrauch[5] + mealcoup.verbrauch[6] + mealcoup.verbrauch[7] + mealcoup.verbrauch[8] + mealcoup.verbrauch[9] +\
                            mealcoup.verbrauch[10] + mealcoup.verbrauch[11] + mealcoup.verbrauch[12] + mealcoup.verbrauch[13] + mealcoup.verbrauch[14] +\
                            mealcoup.verbrauch[15] + mealcoup.verbrauch[16] + mealcoup.verbrauch[17] + mealcoup.verbrauch[18] + mealcoup.verbrauch[19] +\
                            mealcoup.verbrauch[20] + mealcoup.verbrauch[21] + mealcoup.verbrauch[22] + mealcoup.verbrauch[23] + mealcoup.verbrauch[24] +\
                            mealcoup.verbrauch[25] + mealcoup.verbrauch[26] + mealcoup.verbrauch[27] + mealcoup.verbrauch[28] + mealcoup.verbrauch[29] +\
                            mealcoup.verbrauch[30] + mealcoup.verbrauch[31]

                segment = db_session.query(Segment).filter(
                        (Segment.segmentcode == reservation.segmentcode)).first()

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

                if incl_gcomment:

                    gbuff = db_session.query(Gbuff).filter(
                            (Gbuff.gastnr == res_line.gastnrmember)).first()

                    if gbuff:
                        for i in range(1,len(gbuff.bemerk)  + 1) :

                            if substring(gbuff.bemerk, i - 1, 1) == chr(10):
                                cl_list.bemerk = cl_list.bemerk + " "
                            else:
                                cl_list.bemerk = cl_list.bemerk + substring(trim(gbuff.bemerk) , i - 1, 1)
                    cl_list.bemerk = cl_list.bemerk + " || "

                if incl_rsvcomment:

                    rbuff = db_session.query(Rbuff).filter(
                            (Rbuff.gastnr == reservation.gastnr)).first()

                    if rbuff:
                        for j in range(1,len(rbuff.bemerk)  + 1) :

                            if substring(rbuff.bemerk, j - 1, 1) == chr(10):
                                cl_list.bemerk1 = cl_list.bemerk1 + " "
                            else:
                                cl_list.bemerk1 = cl_list.bemerk1 + substring(trim(rbuff.bemerk) , j - 1, 1)
                    cl_list.bemerk = cl_list.bemerk + cl_list.bemerk1 + " || "
                for i in range(1,len(res_line.bemerk)  + 1) :

                    if substring(res_line.bemerk, i - 1, 1) == chr (10):
                        cl_list.bemerk = cl_list.bemerk + " "
                    else:
                        cl_list.bemerk = cl_list.bemerk + substring(trim(res_line.bemerk) , i - 1, 1)
                all_remark = res_line.bemerk
                all_remark = replace_str(all_remark, chr(10) , " ")
                all_remark = replace_str(all_remark, chr(13) , " ")
                cl_list.bemerk01 = to_string(substring(all_remark, 0, 225))
                cl_list.bemerk02 = to_string(substring(all_remark, 225, 225))
                cl_list.bemerk03 = to_string(substring(all_remark, 450, 225))
                cl_list.bemerk04 = to_string(substring(all_remark, 675, 225))
                cl_list.pax = to_string(cl_list.a, ">9") + "/" + to_string(cl_list.c, "9") + " " + to_string(cl_list.co, "9")

                if cl_list.nat == "":
                    cl_list.nat = "?"
                else:

                    nation = db_session.query(Nation).filter(
                            (Nation.kurzbez == cl_list.nat)).first()

                    if nation:
                        cl_list.nation = nation.bezeich

                zinr_list = query(zinr_list_list, filters=(lambda zinr_list :zinr_list.zinr == res_line.zinr and zinr_list.resnr == res_line.resnr and zinr_list.reslinnr == res_line.reslinnr), first=True)

                if not zinr_list:
                    zinr_list = Zinr_list()
                    zinr_list_list.append(zinr_list)

                    zinr_list.resnr = res_line.resnr
                    zinr_list.reslinnr = res_line.reslinnr
                    zinr_list.zinr = res_line.zinr

                    queasy = db_session.query(Queasy).filter(
                            (Queasy.key == 14) &  (Queasy.char1 == res_line.zinr) &  (Queasy.date1 <= curr_date) &  (Queasy.date2 >= curr_date)).first()

                    if zimmer.sleeping and res_line.resstatus != 13:

                        if not queasy:
                            tot_rm = tot_rm + res_line.zimmeranz
                            tot_rmqty = tot_rmqty + res_line.zimmeranz

                        elif queasy and queasy.number3 != res_line.gastnr:
                            tot_rm = tot_rm + res_line.zimmeranz
                            tot_rmqty = tot_rmqty + res_line.zimmeranz

                    if zimmer.sleeping and res_line.zipreis > 0 and res_line.resstatus != 13:

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

            if not disp_accompany:

                cl_list = query(cl_list_list, filters=(lambda cl_list :cl_list.rmno == res_line.zinr and cl_list.resnr == res_line.resnr and cl_list.arrive == res_line.ankunft and cl_list.zipreis == 0 and (cl_list.a + cl_list.c) < 1 and cl_list.co < 1), first=True)

                if cl_list:
                    cl_list_list.remove(cl_list)

                    nr = nr - 1

        for cl_list in query(cl_list_list):

            s_list = query(s_list_list, filters=(lambda s_list :s_list.rmcat == cl_list.kurzbez), first=True)

            if not s_list:

                s_list = query(s_list_list, filters=(lambda s_list :s_list.rmcat == ""), first=True)

                if s_list:
                    s_list.rmcat = cl_list.kurzbez
                    s_list.bezeich = cl_list.bezeich

            if not s_list:
                s_list = S_list()
                s_list_list.append(s_list)

                s_list.rmcat = cl_list.kurzbez
                s_list.bezeich = cl_list.bezeich
            s_list.anz = s_list.anz + cl_list.qty

            s_list = query(s_list_list, filters=(lambda s_list :s_list.nat == cl_list.nat), first=True)

            if not s_list:

                s_list = query(s_list_list, filters=(lambda s_list :s_list.nat == ""), first=True)

                if s_list:
                    s_list.nat = cl_list.nat

            if not s_list:
                s_list = S_list()
                s_list_list.append(s_list)


                if s_list:
                    s_list.nat = cl_list.nat
            s_list.adult = s_list.adult + cl_list.a + cl_list.co
            s_list.child = s_list.child + cl_list.c
            s_list.rmqty = s_list.rmqty + cl_list.qty

        if (tot_a + tot_co) != 0:

            for s_list in query(s_list_list, filters=(lambda s_list :s_list.nat != "")):

                nation = db_session.query(Nation).filter(
                        (Nation.kurzbez == s_list.nat)).first()

                if nation:
                    s_list.nat = nation.bezeich
                s_list.proz = s_list.adult / (tot_a + tot_co) * 100


    def create_genstat_inhouse1():

        nonlocal tot_payrm, tot_rm, tot_a, tot_c, tot_co, tot_avail, tot_rmqty, inactive, cl_list_list, s_list_list, t_buff_queasy_list, vipnr1, vipnr2, vipnr3, vipnr4, vipnr5, vipnr6, vipnr7, vipnr8, vipnr9, tot_room, all_room, all_remark, queasy, htparam, zkstat, zinrstat, paramtext, guest, reservation, zimmer, zimkateg, res_line, guestseg, segment, mc_guest, mc_types, nation, waehrung, reslin_queasy, mealcoup, genstat
        nonlocal gmember, gbuff, rbuff


        nonlocal setup_list, str_list, cl_list, s_list, zinr_list, t_buff_queasy, gmember, gbuff, rbuff
        nonlocal setup_list_list, str_list_list, cl_list_list, s_list_list, zinr_list_list, t_buff_queasy_list

        i:int = 0
        j:int = 0
        vip_flag:str = ""
        nr:int = 0
        str:str = ""
        actflag1:int = 0
        actflag2:int = 0
        do_it:bool = False
        Gmember = Guest
        Gbuff = Guest
        Rbuff = Reservation
        zinr_list_list.clear()

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
        s_list_list.clear()
        cl_list_list.clear()
        str_list_list.clear()
        tot_avail = 0

        for zkstat in db_session.query(Zkstat).filter(
                (Zkstat.datum == datum)).all():
            tot_avail = tot_avail + zkstat.anz100

        genstat_obj_list = []
        for genstat, zimkateg, reservation, guest, gmember in db_session.query(Genstat, Zimkateg, Reservation, Guest, Gmember).join(Zimkateg,(Zimkateg.zikatnr == Genstat.zikatnr)).join(Reservation,(Reservation.resnr == Genstat.resnr)).join(Guest,(Guest.gastnr == Genstat.gastnr)).join(Gmember,(Gmember.gastnr == Genstat.gastnrmember)).filter(
                (Genstat.datum == datum) &  (func.lower(Genstat.zinr) >= (froom).lower()) &  (func.lower(Genstat.zinr) <= (troom).lower())).all():
            if genstat._recid in genstat_obj_list:
                continue
            else:
                genstat_obj_list.append(genstat._recid)

            if genstat.res_date[0] < datum and genstat.res_date[1] == datum and genstat.resstatus == 8:
                1

            elif exc_depart and genstat.res_date[0] <= datum and genstat.res_date[1] == datum and genstat.resstatus == 8:
                1
            else:

                res_line = db_session.query(Res_line).filter(
                        (Res_line.resnr == genstat.resnr) &  (Res_line.reslinnr == genstat.res_int[0])).first()

                setup_list = query(setup_list_list, filters=(lambda setup_list :setup_list.nr == res_line.setup + 1), first=True)

                zimmer = db_session.query(Zimmer).filter(
                        (Zimmer.zinr == genstat.zinr)).first()

                if curr_gastnr != guest.gastnr:
                    nr = 0
                    curr_gastnr = guest.gastnr

                if guest.karteityp > 0:
                    nr = nr + 1
                vip_flag = ""

                guestseg = db_session.query(Guestseg).filter(
                        (Guestseg.gastnr == gmember.gastnr) &  ((Guestseg.segmentcode == vipnr1) |  (Guestseg.segmentcode == vipnr2) |  (Guestseg.segmentcode == vipnr3) |  (Guestseg.segmentcode == vipnr4) |  (Guestseg.segmentcode == vipnr5) |  (Guestseg.segmentcode == vipnr6) |  (Guestseg.segmentcode == vipnr7) |  (Guestseg.segmentcode == vipnr8) |  (Guestseg.segmentcode == vipnr9))).first()

                if guestseg:

                    segment = db_session.query(Segment).filter(
                            (Segment.segmentcode == guestseg.segmentcode)).first()
                    vip_flag = segment.bezeich


                cl_list = Cl_list()
                cl_list_list.append(cl_list)

                cl_list.nr = nr
                cl_list.karteityp = guest.karteityp
                cl_list.rmcat = zimkateg.kurzbez + setup_list.char
                cl_list.kurzbez = zimkateg.kurzbez
                cl_list.bezeich = zimkateg.bezeich
                cl_list.nat = gmember.nation1
                cl_list.resnr = genstat.resnr
                cl_list.vip = vip_flag
                cl_list.name = gmember.name + ", " + gmember.vorname1 +\
                        " " + gmember.anrede1
                cl_list.rmno = genstat.zinr
                cl_list.zipreis = genstat.zipreis
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
                cl_list.createID = reservation.useridanlage

                mc_guest = db_session.query(Mc_guest).filter(
                        (Mc_guest.gastnr == gmember.gastnr)).first()

                if mc_guest:
                    cl_list.telefon = gmember.telefon + ";" + mc_guest.cardnum
                else:
                    cl_list.telefon = gmember.telefon

                mc_types = db_session.query(Mc_types).filter(
                        (Mc_types.nr == mc_guest.nr)).first()

                if mc_types:
                    cl_list.mobil_tel = gmember.mobil_telefon + ";" + mc_types.bezeich
                else:
                    cl_list.mobil_tel = gmember.mobil_telefon

                nation = db_session.query(Nation).filter(
                        (Nation.kurzbez == gmember.nation2)).first()

                if nation:
                    cl_list.local_reg = nation.bezeich

                waehrung = db_session.query(Waehrung).filter(
                        (Waehrungsnr == res_line.betriebsnr)).first()

                if waehrung:
                    cl_list.curr = waehrung.wabkurz + ";" + gmember.email_adr

                reslin_queasy = db_session.query(Reslin_queasy).filter(
                        (func.lower(Reslin_queasy.key) == "specialRequest") &  (Reslin_queasy.resnr == res_line.resnr) &  (Reslin_queasy.reslinnr == res_line.reslinnr)).first()

                if reslin_queasy:
                    cl_list.spreq = reslin_queasy.char3 + "," + cl_list.spreq

                reslin_queasy = db_session.query(Reslin_queasy).filter(
                        (func.lower(Reslin_queasy.key) == "arrangement") &  (Reslin_queasy.resnr == res_line.resnr) &  (Reslin_queasy.reslinnr == res_line.reslinnr) &  (Reslin_queasy.datum >= Reslin_queasy.date1) &  (Reslin_queasy.datum <= Reslin_queasy.date2)).first()

                if reslin_queasy:

                    if reslin_queasy.char2 != "":
                        cl_list.ratecode = reslin_queasy.char2
                    else:
                        for i in range(1,num_entries(res_line.zimmer_wunsch, ";") - 1 + 1) :
                            str = entry(i - 1, res_line.zimmer_wunsch, ";")

                            if substring(str, 0, 6) == "$CODE$":
                                cl_list.ratecode = substring(str, 6)
                                break

                segment = db_session.query(Segment).filter(
                        (Segment.segmentcode == genstat.segmentcode)).first()

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

                if incl_gcomment:

                    gbuff = db_session.query(Gbuff).filter(
                            (Gbuff.gastnr == res_line.gastnrmember)).first()

                    if gbuff:
                        for i in range(1,len(gbuff.bemerk)  + 1) :

                            if substring(gbuff.bemerk, i - 1, 1) == chr(10):
                                cl_list.bemerk = cl_list.bemerk + " "
                            else:
                                cl_list.bemerk = cl_list.bemerk + substring(trim(gbuff.bemerk) , i - 1, 1)
                    cl_list.bemerk = cl_list.bemerk + " || "

                if incl_rsvcomment:

                    rbuff = db_session.query(Rbuff).filter(
                            (Rbuff.gastnr == reservation.gastnr)).first()

                    if rbuff:
                        for j in range(1,len(rbuff.bemerk)  + 1) :

                            if substring(rbuff.bemerk, j - 1, 1) == chr(10):
                                cl_list.bemerk1 = cl_list.bemerk1 + " "
                            else:
                                cl_list.bemerk1 = cl_list.bemerk1 + substring(trim(rbuff.bemerk) , j - 1, 1)
                    cl_list.bemerk = cl_list.bemerk + cl_list.bemerk1 + " || "
                for i in range(1,len(res_line.bemerk)  + 1) :

                    if substring(res_line.bemerk, i - 1, 1) == chr (10):
                        cl_list.bemerk = cl_list.bemerk + " "
                    else:
                        cl_list.bemerk = cl_list.bemerk + substring(trim(res_line.bemerk) , i - 1, 1)
                all_remark = res_line.bemerk
                all_remark = replace_str(all_remark, chr(10) , " ")
                all_remark = replace_str(all_remark, chr(13) , " ")
                cl_list.bemerk01 = to_string(substring(all_remark, 0, 225))
                cl_list.bemerk02 = to_string(substring(all_remark, 225, 225))
                cl_list.bemerk03 = to_string(substring(all_remark, 450, 225))
                cl_list.bemerk04 = to_string(substring(all_remark, 675, 225))
                cl_list.pax = to_string(cl_list.a, ">9") + "/" + to_string(cl_list.c, "9") + " " + to_string(cl_list.co, "9")

                if cl_list.nat == "":
                    cl_list.nat = "?"
                else:

                    nation = db_session.query(Nation).filter(
                            (Nation.kurzbez == cl_list.nat)).first()

                    if nation:
                        cl_list.nation = nation.bezeich

                zinr_list = query(zinr_list_list, filters=(lambda zinr_list :zinr_list.zinr == genstat.zinr and zinr_list.resnr == res_line.resnr and zinr_list.reslinnr == res_line.reslinnr), first=True)

                if not zinr_list:
                    zinr_list = Zinr_list()
                    zinr_list_list.append(zinr_list)

                    zinr_list.resnr = res_line.resnr
                    zinr_list.reslinnr = res_line.reslinnr
                    zinr_list.zinr = genstat.zinr

                    queasy = db_session.query(Queasy).filter(
                            (Queasy.key == 14) &  (Queasy.char1 == genstat.zinr) &  (Queasy.date1 <= curr_date) &  (Queasy.date2 >= curr_date)).first()

                    if zimmer.sleeping and genstat.resstatus != 13:

                        if not queasy:
                            tot_rm = tot_rm + 1
                            tot_rmqty = tot_rmqty + 1

                        elif queasy and queasy.number3 != genstat.gastnr:
                            tot_rm = tot_rm + 1
                            tot_rmqty = tot_rmqty + 1

                    if zimmer.sleeping and genstat.zipreis > 0 and genstat.resstatus != 13:

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

            if not disp_accompany:

                cl_list = query(cl_list_list, filters=(lambda cl_list :cl_list.rmno == res_line.zinr and cl_list.resnr == res_line.resnr and cl_list.arrive == res_line.ankunft and cl_list.zipreis == 0 and (cl_list.a + cl_list.c) < 1 and cl_list.co < 1), first=True)

                if cl_list:
                    cl_list_list.remove(cl_list)

                    nr = nr - 1

        for cl_list in query(cl_list_list):

            mealcoup = db_session.query(Mealcoup).filter(
                    (func.lower(Mealcoup.name) == "Breakfast") &  (Mealcoup.resnr == cl_list.resnr) &  (Mealcoup.zinr == cl_list.rmno)).first()

            if mealcoup:
                cl_list.tot_bfast = mealcoup.verbrauch[0] + mealcoup.verbrauch[1] + mealcoup.verbrauch[2] + mealcoup.verbrauch[3] + mealcoup.verbrauch[4] +\
                        mealcoup.verbrauch[5] + mealcoup.verbrauch[6] + mealcoup.verbrauch[7] + mealcoup.verbrauch[8] + mealcoup.verbrauch[9] +\
                        mealcoup.verbrauch[10] + mealcoup.verbrauch[11] + mealcoup.verbrauch[12] + mealcoup.verbrauch[13] + mealcoup.verbrauch[14] +\
                        mealcoup.verbrauch[15] + mealcoup.verbrauch[16] + mealcoup.verbrauch[17] + mealcoup.verbrauch[18] + mealcoup.verbrauch[19] +\
                        mealcoup.verbrauch[20] + mealcoup.verbrauch[21] + mealcoup.verbrauch[22] + mealcoup.verbrauch[23] + mealcoup.verbrauch[24] +\
                        mealcoup.verbrauch[25] + mealcoup.verbrauch[26] + mealcoup.verbrauch[27] + mealcoup.verbrauch[28] + mealcoup.verbrauch[29] +\
                        mealcoup.verbrauch[30] + mealcoup.verbrauch[31]

            s_list = query(s_list_list, filters=(lambda s_list :s_list.bezeich == cl_list.bezeich), first=True)

            if not s_list:

                s_list = query(s_list_list, filters=(lambda s_list :s_list.rmcat == ""), first=True)

                if s_list:
                    s_list.rmcat = cl_list.kurzbez
                    s_list.bezeich = cl_list.bezeich

            if not s_list:
                s_list = S_list()
                s_list_list.append(s_list)

                s_list.rmcat = cl_list.kurzbez
                s_list.bezeich = cl_list.bezeich
            s_list.anz = s_list.anz + cl_list.qty

            s_list = query(s_list_list, filters=(lambda s_list :s_list.nat == cl_list.nat), first=True)

            if not s_list:

                s_list = query(s_list_list, filters=(lambda s_list :s_list.nat == ""), first=True)

                if s_list:
                    s_list.nat = cl_list.nat

            if not s_list:
                s_list = S_list()
                s_list_list.append(s_list)


                if s_list:
                    s_list.nat = cl_list.nat
            s_list.adult = s_list.adult + cl_list.a + cl_list.co
            s_list.child = s_list.child + cl_list.c
            s_list.rmqty = s_list.rmqty + cl_list.qty

        if (tot_a + tot_co) != 0:

            for s_list in query(s_list_list, filters=(lambda s_list :s_list.nat != "")):

                nation = db_session.query(Nation).filter(
                        (Nation.kurzbez == s_list.nat)).first()

                if nation:
                    s_list.nat = nation.bezeich
                s_list.proz = s_list.adult / (tot_a + tot_co) * 100


    def create_inhouse2():

        nonlocal tot_payrm, tot_rm, tot_a, tot_c, tot_co, tot_avail, tot_rmqty, inactive, cl_list_list, s_list_list, t_buff_queasy_list, vipnr1, vipnr2, vipnr3, vipnr4, vipnr5, vipnr6, vipnr7, vipnr8, vipnr9, tot_room, all_room, all_remark, queasy, htparam, zkstat, zinrstat, paramtext, guest, reservation, zimmer, zimkateg, res_line, guestseg, segment, mc_guest, mc_types, nation, waehrung, reslin_queasy, mealcoup, genstat
        nonlocal gmember, gbuff, rbuff


        nonlocal setup_list, str_list, cl_list, s_list, zinr_list, t_buff_queasy, gmember, gbuff, rbuff
        nonlocal setup_list_list, str_list_list, cl_list_list, s_list_list, zinr_list_list, t_buff_queasy_list

        i:int = 0
        j:int = 0
        vip_flag:str = ""
        nr:int = 0
        str:str = ""
        actflag1:int = 0
        actflag2:int = 0
        do_it:bool = False
        Gmember = Guest
        Gbuff = Guest
        Rbuff = Reservation
        zinr_list_list.clear()

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
        s_list_list.clear()
        cl_list_list.clear()
        str_list_list.clear()
        tot_avail = 0

        for zimmer in db_session.query(Zimmer).filter(
                (Zimmer.sleeping)).all():
            tot_avail = tot_avail + 1

        res_line_obj_list = []
        for res_line, zimkateg, reservation, guest, gmember, zimmer in db_session.query(Res_line, Zimkateg, Reservation, Guest, Gmember, Zimmer).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Guest,(Guest.gastnr == reservation.gastnr)).join(Gmember,(Gmember.gastnr == Res_line.gastnrmember)).join(Zimmer,(Zimmer.zinr == Res_line.zinr) &  (Zimmer.sleeping)).filter(
                (Res_line.active_flag >= actflag1) &  (Res_line.active_flag <= actflag2) &  (Res_line.resstatus != 9) &  (Res_line.resstatus != 10) &  (Res_line.resstatus != 12) &  (Res_line.ankunft <= datum) &  (Res_line.abreise >= datum) &  (func.lower(Res_line.zinr) >= (froom).lower()) &  (func.lower(Res_line.zinr) <= (troom).lower())).all():
            if res_line._recid in res_line_obj_list:
                continue
            else:
                res_line_obj_list.append(res_line._recid)

            if exc_depart and res_line.abreise == datum:
                1
            else:

                setup_list = query(setup_list_list, filters=(lambda setup_list :setup_list.nr == res_line.setup + 1), first=True)
                nr = nr + 1
                vip_flag = ""

                guestseg = db_session.query(Guestseg).filter(
                        (Guestseg.gastnr == gmember.gastnr) &  ((Guestseg.segmentcode == vipnr1) |  (Guestseg.segmentcode == vipnr2) |  (Guestseg.segmentcode == vipnr3) |  (Guestseg.segmentcode == vipnr4) |  (Guestseg.segmentcode == vipnr5) |  (Guestseg.segmentcode == vipnr6) |  (Guestseg.segmentcode == vipnr7) |  (Guestseg.segmentcode == vipnr8) |  (Guestseg.segmentcode == vipnr9))).first()

                if guestseg:

                    segment = db_session.query(Segment).filter(
                            (Segment.segmentcode == guestseg.segmentcode)).first()
                    vip_flag = segment.bezeich


                cl_list = Cl_list()
                cl_list_list.append(cl_list)

                cl_list.nr = nr
                cl_list.rmcat = zimkateg.kurzbez + setup_list.char
                cl_list.kurzbez = zimkateg.kurzbez
                cl_list.bezeich = zimkateg.bezeich
                cl_list.nat = gmember.nation1
                cl_list.resnr = res_line.resnr
                cl_list.vip = vip_flag
                cl_list.name = res_line.name
                cl_list.rmno = res_line.zinr
                cl_list.zipreis = res_line.zipreis
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
                cl_list.createID = reservation.useridanlage

                mc_guest = db_session.query(Mc_guest).filter(
                        (Mc_guest.gastnr == gmember.gastnr)).first()

                if mc_guest:
                    cl_list.telefon = gmember.telefon + ";" + mc_guest.cardnum
                else:
                    cl_list.telefon = gmember.telefon

                mc_types = db_session.query(Mc_types).filter(
                        (Mc_types.nr == mc_guest.nr)).first()

                if mc_types:
                    cl_list.mobil_tel = gmember.mobil_telefon + ";" + mc_types.bezeich
                else:
                    cl_list.mobil_tel = gmember.mobil_telefon

                nation = db_session.query(Nation).filter(
                        (Nation.kurzbez == gmember.nation2)).first()

                if nation:
                    cl_list.local_reg = nation.bezeich

                waehrung = db_session.query(Waehrung).filter(
                        (Waehrungsnr == res_line.betriebsnr)).first()

                if waehrung:
                    cl_list.curr = waehrung.wabkurz + ";" + gmember.email_adr

                reslin_queasy = db_session.query(Reslin_queasy).filter(
                        (func.lower(Reslin_queasy.key) == "specialRequest") &  (Reslin_queasy.resnr == res_line.resnr) &  (Reslin_queasy.reslinnr == res_line.reslinnr)).first()

                if reslin_queasy:
                    cl_list.spreq = reslin_queasy.char3 + "," + cl_list.spreq

                reslin_queasy = db_session.query(Reslin_queasy).filter(
                        (func.lower(Reslin_queasy.key) == "arrangement") &  (Reslin_queasy.resnr == res_line.resnr) &  (Reslin_queasy.reslinnr == res_line.reslinnr) &  (Reslin_queasy.datum >= Reslin_queasy.date1) &  (Reslin_queasy.datum <= Reslin_queasy.date2)).first()

                if reslin_queasy:

                    if reslin_queasy.char2 != "":
                        cl_list.ratecode = reslin_queasy.char2
                    else:
                        for i in range(1,num_entries(res_line.zimmer_wunsch, ";") - 1 + 1) :
                            str = entry(i - 1, res_line.zimmer_wunsch, ";")

                            if substring(str, 0, 6) == "$CODE$":
                                cl_list.ratecode = substring(str, 6)
                                break

                mealcoup = db_session.query(Mealcoup).filter(
                        (func.lower(Mealcoup.name) == "Breakfast") &  (Mealcoup.resnr == res_line.resnr) &  (Mealcoup.zinr == res_line.zinr)).first()

                if mealcoup:
                    cl_list.tot_bfast = mealcoup.verbrauch[0] + mealcoup.verbrauch[1] + mealcoup.verbrauch[2] + mealcoup.verbrauch[3] + mealcoup.verbrauch[4] +\
                            mealcoup.verbrauch[5] + mealcoup.verbrauch[6] + mealcoup.verbrauch[7] + mealcoup.verbrauch[8] + mealcoup.verbrauch[9] +\
                            mealcoup.verbrauch[10] + mealcoup.verbrauch[11] + mealcoup.verbrauch[12] + mealcoup.verbrauch[13] + mealcoup.verbrauch[14] +\
                            mealcoup.verbrauch[15] + mealcoup.verbrauch[16] + mealcoup.verbrauch[17] + mealcoup.verbrauch[18] + mealcoup.verbrauch[19] +\
                            mealcoup.verbrauch[20] + mealcoup.verbrauch[21] + mealcoup.verbrauch[22] + mealcoup.verbrauch[23] + mealcoup.verbrauch[24] +\
                            mealcoup.verbrauch[25] + mealcoup.verbrauch[26] + mealcoup.verbrauch[27] + mealcoup.verbrauch[28] + mealcoup.verbrauch[29] +\
                            mealcoup.verbrauch[30] + mealcoup.verbrauch[31]

                segment = db_session.query(Segment).filter(
                        (Segment.segmentcode == reservation.segmentcode)).first()

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

                if incl_gcomment:

                    gbuff = db_session.query(Gbuff).filter(
                            (Gbuff.gastnr == res_line.gastnrmember)).first()

                    if gbuff:
                        for i in range(1,len(gbuff.bemerk)  + 1) :

                            if substring(gbuff.bemerk, i - 1, 1) == chr(10):
                                cl_list.bemerk = cl_list.bemerk + " "
                            else:
                                cl_list.bemerk = cl_list.bemerk + substring(trim(gbuff.bemerk) , i - 1, 1)
                    cl_list.bemerk = cl_list.bemerk + " || "

                if incl_rsvcomment:

                    rbuff = db_session.query(Rbuff).filter(
                            (Rbuff.gastnr == reservation.gastnr)).first()

                    if rbuff:
                        for j in range(1,len(rbuff.bemerk)  + 1) :

                            if substring(rbuff.bemerk, j - 1, 1) == chr(10):
                                cl_list.bemerk1 = cl_list.bemerk1 + " "
                            else:
                                cl_list.bemerk1 = cl_list.bemerk1 + substring(trim(rbuff.bemerk) , j - 1, 1)
                    cl_list.bemerk = cl_list.bemerk + cl_list.bemerk1 + " || "
                for i in range(1,len(res_line.bemerk)  + 1) :

                    if substring(res_line.bemerk, i - 1, 1) == chr (10):
                        cl_list.bemerk = cl_list.bemerk + " "
                    else:
                        cl_list.bemerk = cl_list.bemerk + substring(trim(res_line.bemerk) , i - 1, 1)
                all_remark = res_line.bemerk
                all_remark = replace_str(all_remark, chr(10) , " ")
                all_remark = replace_str(all_remark, chr(13) , " ")
                cl_list.bemerk01 = to_string(substring(all_remark, 0, 225))
                cl_list.bemerk02 = to_string(substring(all_remark, 225, 225))
                cl_list.bemerk03 = to_string(substring(all_remark, 450, 225))
                cl_list.bemerk04 = to_string(substring(all_remark, 675, 225))
                cl_list.pax = to_string(cl_list.a, ">9") + "/" + to_string(cl_list.c, "9") + " " + to_string(cl_list.co, "9")

                if cl_list.nat == "":
                    cl_list.nat = "?"
                else:

                    nation = db_session.query(Nation).filter(
                            (Nation.kurzbez == cl_list.nat)).first()

                    if nation:
                        cl_list.nation = nation.bezeich

                zinr_list = query(zinr_list_list, filters=(lambda zinr_list :zinr_list.zinr == res_line.zinr and zinr_list.resnr == res_line.resnr and zinr_list.reslinnr == res_line.reslinnr), first=True)

                if not zinr_list:
                    zinr_list = Zinr_list()
                    zinr_list_list.append(zinr_list)

                    zinr_list.resnr = res_line.resnr
                    zinr_list.reslinnr = res_line.reslinnr
                    zinr_list.zinr = res_line.zinr

                    queasy = db_session.query(Queasy).filter(
                            (Queasy.key == 14) &  (Queasy.char1 == res_line.zinr) &  (Queasy.date1 <= curr_date) &  (Queasy.date2 >= curr_date)).first()

                    if zimmer.sleeping and res_line.resstatus != 13:

                        if not queasy:
                            tot_rm = tot_rm + res_line.zimmeranz
                            tot_rmqty = tot_rmqty + res_line.zimmeranz

                        elif queasy and queasy.number3 != res_line.gastnr:
                            tot_rm = tot_rm + res_line.zimmeranz
                            tot_rmqty = tot_rmqty + res_line.zimmeranz

                    if zimmer.sleeping and res_line.zipreis > 0 and res_line.resstatus != 13:

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

            if not disp_accompany:

                cl_list = query(cl_list_list, filters=(lambda cl_list :cl_list.rmno == res_line.zinr and cl_list.resnr == res_line.resnr and cl_list.arrive == res_line.ankunft and cl_list.zipreis == 0 and (cl_list.a + cl_list.c) < 1 and cl_list.co < 1), first=True)

                if cl_list:
                    cl_list_list.remove(cl_list)

                    nr = nr - 1

        for cl_list in query(cl_list_list):

            s_list = query(s_list_list, filters=(lambda s_list :s_list.rmcat == cl_list.kurzbez), first=True)

            if not s_list:

                s_list = query(s_list_list, filters=(lambda s_list :s_list.rmcat == ""), first=True)

                if s_list:
                    s_list.rmcat = cl_list.kurzbez
                    s_list.bezeich = cl_list.bezeich

            if not s_list:
                s_list = S_list()
                s_list_list.append(s_list)

                s_list.rmcat = cl_list.kurzbez
                s_list.bezeich = cl_list.bezeich
            s_list.anz = s_list.anz + cl_list.qty

            s_list = query(s_list_list, filters=(lambda s_list :s_list.nat == cl_list.nat), first=True)

            if not s_list:

                s_list = query(s_list_list, filters=(lambda s_list :s_list.nat == ""), first=True)

                if s_list:
                    s_list.nat = cl_list.nat

            if not s_list:
                s_list = S_list()
                s_list_list.append(s_list)


                if s_list:
                    s_list.nat = cl_list.nat
            s_list.adult = s_list.adult + cl_list.a + cl_list.co
            s_list.child = s_list.child + cl_list.c
            s_list.rmqty = s_list.rmqty + cl_list.qty

        if (tot_a + tot_co) != 0:

            for s_list in query(s_list_list, filters=(lambda s_list :s_list.nat != "")):

                nation = db_session.query(Nation).filter(
                        (Nation.kurzbez == s_list.nat)).first()

                if nation:
                    s_list.nat = nation.bezeich
                s_list.proz = s_list.adult / (tot_a + tot_co) * 100


    def create_genstat_inhouse2():

        nonlocal tot_payrm, tot_rm, tot_a, tot_c, tot_co, tot_avail, tot_rmqty, inactive, cl_list_list, s_list_list, t_buff_queasy_list, vipnr1, vipnr2, vipnr3, vipnr4, vipnr5, vipnr6, vipnr7, vipnr8, vipnr9, tot_room, all_room, all_remark, queasy, htparam, zkstat, zinrstat, paramtext, guest, reservation, zimmer, zimkateg, res_line, guestseg, segment, mc_guest, mc_types, nation, waehrung, reslin_queasy, mealcoup, genstat
        nonlocal gmember, gbuff, rbuff


        nonlocal setup_list, str_list, cl_list, s_list, zinr_list, t_buff_queasy, gmember, gbuff, rbuff
        nonlocal setup_list_list, str_list_list, cl_list_list, s_list_list, zinr_list_list, t_buff_queasy_list

        i:int = 0
        j:int = 0
        vip_flag:str = ""
        nr:int = 0
        str:str = ""
        actflag1:int = 0
        actflag2:int = 0
        do_it:bool = False
        z:int = 0
        Gmember = Guest
        Gbuff = Guest
        Rbuff = Reservation
        zinr_list_list.clear()

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
        s_list_list.clear()
        cl_list_list.clear()
        str_list_list.clear()
        tot_avail = 0

        for zkstat in db_session.query(Zkstat).filter(
                (Zkstat.datum == datum)).all():
            tot_avail = tot_avail + zkstat.anz100

        genstat_obj_list = []
        for genstat, zimkateg, reservation, guest, gmember, zimmer in db_session.query(Genstat, Zimkateg, Reservation, Guest, Gmember, Zimmer).join(Zimkateg,(Zimkateg.zikatnr == Genstat.zikatnr)).join(Reservation,(Reservation.resnr == Genstat.resnr)).join(Guest,(Guest.gastnr == Genstat.gastnr)).join(Gmember,(Gmember.gastnr == Genstat.gastnrmember)).join(Zimmer,(Zimmer.zinr == Genstat.zinr) &  (Zimmer.sleeping)).filter(
                (Genstat.datum == datum) &  (func.lower(Genstat.zinr) >= (froom).lower()) &  (func.lower(Genstat.zinr) <= (troom).lower())).all():
            if genstat._recid in genstat_obj_list:
                continue
            else:
                genstat_obj_list.append(genstat._recid)

            if genstat.res_date[0] < datum and genstat.res_date[1] == datum and genstat.resstatus == 8:
                1

            elif exc_depart and genstat.res_date[0] <= datum and genstat.res_date[1] == datum and genstat.resstatus == 8:
                1
            else:

                res_line = db_session.query(Res_line).filter(
                        (Res_line.resnr == genstat.resnr) &  (Res_line.reslinnr == genstat.res_int[0])).first()

                setup_list = query(setup_list_list, filters=(lambda setup_list :setup_list.nr == res_line.setup + 1), first=True)
                nr = nr + 1
                vip_flag = ""

                guestseg = db_session.query(Guestseg).filter(
                        (Guestseg.gastnr == gmember.gastnr) &  ((Guestseg.segmentcode == vipnr1) |  (Guestseg.segmentcode == vipnr2) |  (Guestseg.segmentcode == vipnr3) |  (Guestseg.segmentcode == vipnr4) |  (Guestseg.segmentcode == vipnr5) |  (Guestseg.segmentcode == vipnr6) |  (Guestseg.segmentcode == vipnr7) |  (Guestseg.segmentcode == vipnr8) |  (Guestseg.segmentcode == vipnr9))).first()

                if guestseg:

                    segment = db_session.query(Segment).filter(
                            (Segment.segmentcode == guestseg.segmentcode)).first()
                    vip_flag = replace_str(segment.bezeich, " ", "")
                cl_list = Cl_list()
                cl_list_list.append(cl_list)

                cl_list.nr = nr
                cl_list.rmcat = zimkateg.kurzbez + setup_list.char
                cl_list.kurzbez = zimkateg.kurzbez
                cl_list.bezeich = zimkateg.bezeich
                cl_list.nat = gmember.nation1
                cl_list.resnr = genstat.resnr
                cl_list.vip = vip_flag
                cl_list.name = gmember.name + ", " + gmember.vorname1 +\
                        " " + gmember.anrede1
                cl_list.rmno = genstat.zinr
                cl_list.zipreis = genstat.zipreis
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
                cl_list.createID = reservation.useridanlage

                mc_guest = db_session.query(Mc_guest).filter(
                        (Mc_guest.gastnr == gmember.gastnr)).first()

                if mc_guest:
                    cl_list.telefon = gmember.telefon + ";" + mc_guest.cardnum
                else:
                    cl_list.telefon = gmember.telefon

                mc_types = db_session.query(Mc_types).filter(
                        (Mc_types.nr == mc_guest.nr)).first()

                if mc_types:
                    cl_list.mobil_tel = gmember.mobil_telefon + ";" + mc_types.bezeich
                else:
                    cl_list.mobil_tel = gmember.mobil_telefon

                nation = db_session.query(Nation).filter(
                        (Nation.kurzbez == gmember.nation2)).first()

                if nation:
                    cl_list.local_reg = nation.bezeich

                waehrung = db_session.query(Waehrung).filter(
                        (Waehrungsnr == res_line.betriebsnr)).first()

                if waehrung:
                    cl_list.curr = waehrung.wabkurz + ";" + gmember.email_adr

                reslin_queasy = db_session.query(Reslin_queasy).filter(
                        (func.lower(Reslin_queasy.key) == "specialRequest") &  (Reslin_queasy.resnr == res_line.resnr) &  (Reslin_queasy.reslinnr == res_line.reslinnr)).first()

                if reslin_queasy:
                    cl_list.spreq = reslin_queasy.char3 + "," + cl_list.spreq

                reslin_queasy = db_session.query(Reslin_queasy).filter(
                        (func.lower(Reslin_queasy.key) == "arrangement") &  (Reslin_queasy.resnr == res_line.resnr) &  (Reslin_queasy.reslinnr == res_line.reslinnr) &  (Reslin_queasy.datum >= Reslin_queasy.date1) &  (Reslin_queasy.datum <= Reslin_queasy.date2)).first()

                if reslin_queasy:

                    if reslin_queasy.char2 != "":
                        cl_list.ratecode = reslin_queasy.char2
                    else:
                        for i in range(1,num_entries(res_line.zimmer_wunsch, ";") - 1 + 1) :
                            str = entry(i - 1, res_line.zimmer_wunsch, ";")

                            if substring(str, 0, 6) == "$CODE$":
                                cl_list.ratecode = substring(str, 6)
                                break

                segment = db_session.query(Segment).filter(
                        (Segment.segmentcode == genstat.segmentcode)).first()

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

                if incl_gcomment:

                    gbuff = db_session.query(Gbuff).filter(
                            (Gbuff.gastnr == res_line.gastnrmember)).first()

                    if gbuff:
                        for i in range(1,len(gbuff.bemerk)  + 1) :

                            if substring(gbuff.bemerk, i - 1, 1) == chr(10):
                                cl_list.bemerk = cl_list.bemerk + " "
                            else:
                                cl_list.bemerk = cl_list.bemerk + substring(trim(gbuff.bemerk) , i - 1, 1)
                    cl_list.bemerk = cl_list.bemerk + " || "

                if incl_rsvcomment:

                    rbuff = db_session.query(Rbuff).filter(
                            (Rbuff.gastnr == reservation.gastnr)).first()

                    if rbuff:
                        for j in range(1,len(rbuff.bemerk)  + 1) :

                            if substring(rbuff.bemerk, j - 1, 1) == chr(10):
                                cl_list.bemerk1 = cl_list.bemerk1 + " "
                            else:
                                cl_list.bemerk1 = cl_list.bemerk1 + substring(trim(rbuff.bemerk) , j - 1, 1)
                    cl_list.bemerk = cl_list.bemerk + cl_list.bemerk1 + " || "
                for i in range(1,len(res_line.bemerk)  + 1) :

                    if substring(res_line.bemerk, i - 1, 1) == chr (10):
                        cl_list.bemerk = cl_list.bemerk + " "
                    else:
                        cl_list.bemerk = cl_list.bemerk + substring(trim(res_line.bemerk) , i - 1, 1)
                all_remark = res_line.bemerk
                all_remark = replace_str(all_remark, chr(10) , " ")
                all_remark = replace_str(all_remark, chr(13) , " ")
                cl_list.bemerk01 = to_string(substring(all_remark, 0, 225))
                cl_list.bemerk02 = to_string(substring(all_remark, 225, 225))
                cl_list.bemerk03 = to_string(substring(all_remark, 450, 225))
                cl_list.bemerk04 = to_string(substring(all_remark, 675, 225))
                cl_list.pax = to_string(cl_list.a, ">9") + "/" + to_string(cl_list.c, "9") + " " + to_string(cl_list.co, "9")

                if cl_list.nat == "":
                    cl_list.nat = "?"
                else:

                    nation = db_session.query(Nation).filter(
                            (Nation.kurzbez == cl_list.nat)).first()

                    if nation:
                        cl_list.nation = nation.bezeich

                zinr_list = query(zinr_list_list, filters=(lambda zinr_list :zinr_list.zinr == genstat.zinr and zinr_list.resnr == res_line.resnr and zinr_list.reslinnr == res_line.reslinnr), first=True)

                if not zinr_list:
                    zinr_list = Zinr_list()
                    zinr_list_list.append(zinr_list)

                    zinr_list.resnr = res_line.resnr
                    zinr_list.reslinnr = res_line.reslinnr
                    zinr_list.zinr = genstat.zinr

                    queasy = db_session.query(Queasy).filter(
                            (Queasy.key == 14) &  (Queasy.char1 == genstat.zinr) &  (Queasy.date1 <= curr_date) &  (Queasy.date2 >= curr_date)).first()

                    if zimmer.sleeping and genstat.resstatus != 13:

                        if not queasy:
                            tot_rm = tot_rm + 1
                            tot_rmqty = tot_rmqty + 1

                        elif queasy and queasy.number3 != genstat.gastnr:
                            tot_rm = tot_rm + 1
                            tot_rmqty = tot_rmqty + 1

                    if zimmer.sleeping and genstat.zipreis > 0 and genstat.resstatus != 13:
                        DO: z = z + 1

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

        if not disp_accompany:

            cl_list = query(cl_list_list, filters=(lambda cl_list :cl_list.rmno == res_line.zinr and cl_list.resnr == res_line.resnr and cl_list.arrive == res_line.ankunft and cl_list.zipreis == 0 and (cl_list.a + cl_list.c) < 1 and cl_list.co < 1), first=True)

            if cl_list:
                cl_list_list.remove(cl_list)

                nr = nr - 1

    def create_inhouse3():

        nonlocal tot_payrm, tot_rm, tot_a, tot_c, tot_co, tot_avail, tot_rmqty, inactive, cl_list_list, s_list_list, t_buff_queasy_list, vipnr1, vipnr2, vipnr3, vipnr4, vipnr5, vipnr6, vipnr7, vipnr8, vipnr9, tot_room, all_room, all_remark, queasy, htparam, zkstat, zinrstat, paramtext, guest, reservation, zimmer, zimkateg, res_line, guestseg, segment, mc_guest, mc_types, nation, waehrung, reslin_queasy, mealcoup, genstat
        nonlocal gmember, gbuff, rbuff


        nonlocal setup_list, str_list, cl_list, s_list, zinr_list, t_buff_queasy, gmember, gbuff, rbuff
        nonlocal setup_list_list, str_list_list, cl_list_list, s_list_list, zinr_list_list, t_buff_queasy_list

        i:int = 0
        j:int = 0
        vip_flag:str = ""
        str:str = ""
        nr:int = 0
        curr_gastnr:int = 0
        actflag1:int = 0
        actflag2:int = 0
        Gmember = Guest
        Gbuff = Guest
        Rbuff = Reservation
        zinr_list_list.clear()

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
        s_list_list.clear()
        cl_list_list.clear()
        str_list_list.clear()
        tot_avail = 0

        for zimmer in db_session.query(Zimmer).filter(
                (Zimmer.sleeping)).all():
            tot_avail = tot_avail + 1

        res_line_obj_list = []
        for res_line, zimkateg, reservation, guest, gmember, zimmer in db_session.query(Res_line, Zimkateg, Reservation, Guest, Gmember, Zimmer).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Guest,(Guest.gastnr == reservation.gastnr)).join(Gmember,(Gmember.gastnr == Res_line.gastnrmember)).join(Zimmer,(Zimmer.zinr == Res_line.zinr) &  (Zimmer.sleeping)).filter(
                (Res_line.active_flag >= actflag1) &  (Res_line.active_flag <= actflag2) &  (Res_line.resstatus != 9) &  (Res_line.resstatus != 10) &  (Res_line.resstatus != 12) &  (Res_line.ankunft <= datum) &  (Res_line.abreise >= datum) &  (func.lower(Res_line.zinr) >= (froom).lower()) &  (func.lower(Res_line.zinr) <= (troom).lower())).all():
            if res_line._recid in res_line_obj_list:
                continue
            else:
                res_line_obj_list.append(res_line._recid)

            if exc_depart and res_line.abreise == datum:
                pass
            else:

                setup_list = query(setup_list_list, filters=(lambda setup_list :setup_list.nr == res_line.setup + 1), first=True)

                if curr_gastnr != guest.gastnr:
                    nr = 0
                    curr_gastnr = guest.gastnr

                if guest.karteityp > 0:
                    nr = nr + 1
                vip_flag = ""

                guestseg = db_session.query(Guestseg).filter(
                        (Guestseg.gastnr == gmember.gastnr) &  ((Guestseg.segmentcode == vipnr1) |  (Guestseg.segmentcode == vipnr2) |  (Guestseg.segmentcode == vipnr3) |  (Guestseg.segmentcode == vipnr4) |  (Guestseg.segmentcode == vipnr5) |  (Guestseg.segmentcode == vipnr6) |  (Guestseg.segmentcode == vipnr7) |  (Guestseg.segmentcode == vipnr8) |  (Guestseg.segmentcode == vipnr9))).first()

                if guestseg:

                    segment = db_session.query(Segment).filter(
                            (Segment.segmentcode == guestseg.segmentcode)).first()
                    vip_flag = segment.bezeich


                cl_list = Cl_list()
                cl_list_list.append(cl_list)

                cl_list.nr = nr
                cl_list.karteityp = guest.karteityp
                cl_list.rmcat = zimkateg.kurzbez + setup_list.char
                cl_list.kurzbez = zimkateg.kurzbez
                cl_list.bezeich = zimkateg.bezeich
                cl_list.nat = gmember.nation1
                cl_list.resnr = res_line.resnr
                cl_list.vip = vip_flag
                cl_list.name = res_line.name
                cl_list.rmno = res_line.zinr
                cl_list.zipreis = res_line.zipreis
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
                cl_list.createID = reservation.useridanlage

                mc_guest = db_session.query(Mc_guest).filter(
                        (Mc_guest.gastnr == gmember.gastnr)).first()

                if mc_guest:
                    cl_list.telefon = gmember.telefon + ";" + mc_guest.cardnum
                else:
                    cl_list.telefon = gmember.telefon

                mc_types = db_session.query(Mc_types).filter(
                        (Mc_types.nr == mc_guest.nr)).first()

                if mc_types:
                    cl_list.mobil_tel = gmember.mobil_telefon + ";" + mc_types.bezeich
                else:
                    cl_list.mobil_tel = gmember.mobil_telefon

                nation = db_session.query(Nation).filter(
                        (Nation.kurzbez == gmember.nation2)).first()

                if nation:
                    cl_list.local_reg = nation.bezeich

                waehrung = db_session.query(Waehrung).filter(
                        (Waehrungsnr == res_line.betriebsnr)).first()

                if waehrung:
                    cl_list.curr = waehrung.wabkurz + ";" + gmember.email_adr

                reslin_queasy = db_session.query(Reslin_queasy).filter(
                        (func.lower(Reslin_queasy.key) == "specialRequest") &  (Reslin_queasy.resnr == res_line.resnr) &  (Reslin_queasy.reslinnr == res_line.reslinnr)).first()

                if reslin_queasy:
                    cl_list.spreq = reslin_queasy.char3 + "," + cl_list.spreq

                reslin_queasy = db_session.query(Reslin_queasy).filter(
                        (func.lower(Reslin_queasy.key) == "arrangement") &  (Reslin_queasy.resnr == res_line.resnr) &  (Reslin_queasy.reslinnr == res_line.reslinnr) &  (Reslin_queasy.datum >= Reslin_queasy.date1) &  (Reslin_queasy.datum <= Reslin_queasy.date2)).first()

                if reslin_queasy:

                    if reslin_queasy.char2 != "":
                        cl_list.ratecode = reslin_queasy.char2
                    else:
                        for i in range(1,num_entries(res_line.zimmer_wunsch, ";") - 1 + 1) :
                            str = entry(i - 1, res_line.zimmer_wunsch, ";")

                            if substring(str, 0, 6) == "$CODE$":
                                cl_list.ratecode = substring(str, 6)
                                break

                mealcoup = db_session.query(Mealcoup).filter(
                        (func.lower(Mealcoup.name) == "Breakfast") &  (Mealcoup.resnr == res_line.resnr) &  (Mealcoup.zinr == res_line.zinr)).first()

                if mealcoup:
                    cl_list.tot_bfast = mealcoup.verbrauch[0] + mealcoup.verbrauch[1] + mealcoup.verbrauch[2] + mealcoup.verbrauch[3] + mealcoup.verbrauch[4] +\
                            mealcoup.verbrauch[5] + mealcoup.verbrauch[6] + mealcoup.verbrauch[7] + mealcoup.verbrauch[8] + mealcoup.verbrauch[9] +\
                            mealcoup.verbrauch[10] + mealcoup.verbrauch[11] + mealcoup.verbrauch[12] + mealcoup.verbrauch[13] + mealcoup.verbrauch[14] +\
                            mealcoup.verbrauch[15] + mealcoup.verbrauch[16] + mealcoup.verbrauch[17] + mealcoup.verbrauch[18] + mealcoup.verbrauch[19] +\
                            mealcoup.verbrauch[20] + mealcoup.verbrauch[21] + mealcoup.verbrauch[22] + mealcoup.verbrauch[23] + mealcoup.verbrauch[24] +\
                            mealcoup.verbrauch[25] + mealcoup.verbrauch[26] + mealcoup.verbrauch[27] + mealcoup.verbrauch[28] + mealcoup.verbrauch[29] +\
                            mealcoup.verbrauch[30] + mealcoup.verbrauch[31]

                segment = db_session.query(Segment).filter(
                        (Segment.segmentcode == reservation.segmentcode)).first()

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

                if incl_gcomment:

                    gbuff = db_session.query(Gbuff).filter(
                            (Gbuff.gastnr == res_line.gastnrmember)).first()

                    if gbuff:
                        for i in range(1,len(gbuff.bemerk)  + 1) :

                            if substring(gbuff.bemerk, i - 1, 1) == chr(10):
                                cl_list.bemerk = cl_list.bemerk + " "
                            else:
                                cl_list.bemerk = cl_list.bemerk + substring(trim(gbuff.bemerk) , i - 1, 1)
                    cl_list.bemerk = cl_list.bemerk + " || "

                if incl_rsvcomment:

                    rbuff = db_session.query(Rbuff).filter(
                            (Rbuff.gastnr == reservation.gastnr)).first()

                    if rbuff:
                        for j in range(1,len(rbuff.bemerk)  + 1) :

                            if substring(rbuff.bemerk, j - 1, 1) == chr(10):
                                cl_list.bemerk1 = cl_list.bemerk1 + " "
                            else:
                                cl_list.bemerk1 = cl_list.bemerk1 + substring(trim(rbuff.bemerk) , j - 1, 1)
                    cl_list.bemerk = cl_list.bemerk + cl_list.bemerk1 + " || "
                for i in range(1,len(res_line.bemerk)  + 1) :

                    if substring(res_line.bemerk, i - 1, 1) == chr (10):
                        cl_list.bemerk = cl_list.bemerk + " "
                    else:
                        cl_list.bemerk = cl_list.bemerk + substring(trim(res_line.bemerk) , i - 1, 1)
                all_remark = res_line.bemerk
                all_remark = replace_str(all_remark, chr(10) , " ")
                all_remark = replace_str(all_remark, chr(13) , " ")
                cl_list.bemerk01 = to_string(substring(all_remark, 0, 225))
                cl_list.bemerk02 = to_string(substring(all_remark, 225, 225))
                cl_list.bemerk03 = to_string(substring(all_remark, 450, 225))
                cl_list.bemerk04 = to_string(substring(all_remark, 675, 225))
                cl_list.pax = to_string(cl_list.a, ">9") + "/" + to_string(cl_list.c, "9") + " " + to_string(cl_list.co, "9")

                if cl_list.nat == "":
                    cl_list.nat = "?"
                else:

                    nation = db_session.query(Nation).filter(
                            (Nation.kurzbez == cl_list.nat)).first()

                    if nation:
                        cl_list.nation = nation.bezeich

                zinr_list = query(zinr_list_list, filters=(lambda zinr_list :zinr_list.zinr == res_line.zinr and zinr_list.resnr == res_line.resnr and zinr_list.reslinnr == res_line.reslinnr), first=True)

                if not zinr_list:
                    zinr_list = Zinr_list()
                    zinr_list_list.append(zinr_list)

                    zinr_list.resnr = res_line.resnr
                    zinr_list.reslinnr = res_line.reslinnr
                    zinr_list.zinr = res_line.zinr

                    queasy = db_session.query(Queasy).filter(
                            (Queasy.key == 14) &  (Queasy.char1 == res_line.zinr) &  (Queasy.date1 <= curr_date) &  (Queasy.date2 >= curr_date)).first()

                    if zimmer.sleeping and res_line.resstatus != 13:

                        if not queasy:
                            tot_rm = tot_rm + res_line.zimmeranz
                            tot_rmqty = tot_rmqty + res_line.zimmeranz

                        elif queasy and queasy.number3 != res_line.gastnr:
                            tot_rm = tot_rm + res_line.zimmeranz
                            tot_rmqty = tot_rmqty + res_line.zimmeranz

                    if zimmer.sleeping and res_line.zipreis > 0 and res_line.resstatus != 13:

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

            if not disp_accompany:

                cl_list = query(cl_list_list, filters=(lambda cl_list :cl_list.rmno == res_line.zinr and cl_list.resnr == res_line.resnr and cl_list.arrive == res_line.ankunft and cl_list.zipreis == 0 and (cl_list.a + cl_list.c) < 1 and cl_list.co < 1), first=True)

                if cl_list:
                    cl_list_list.remove(cl_list)

                    nr = nr - 1

        for cl_list in query(cl_list_list):

            s_list = query(s_list_list, filters=(lambda s_list :s_list.rmcat == cl_list.kurzbez), first=True)

            if not s_list:

                s_list = query(s_list_list, filters=(lambda s_list :s_list.rmcat == ""), first=True)

                if s_list:
                    s_list.rmcat = cl_list.kurzbez
                    s_list.bezeich = cl_list.bezeich

            if not s_list:
                s_list = S_list()
                s_list_list.append(s_list)

                s_list.rmcat = cl_list.kurzbez
                s_list.bezeich = cl_list.bezeich
            s_list.anz = s_list.anz + cl_list.qty

            s_list = query(s_list_list, filters=(lambda s_list :s_list.nat == cl_list.nat), first=True)

            if not s_list:

                s_list = query(s_list_list, filters=(lambda s_list :s_list.nat == ""), first=True)

                if s_list:
                    s_list.nat = cl_list.nat

            if not s_list:
                s_list = S_list()
                s_list_list.append(s_list)


                if s_list:
                    s_list.nat = cl_list.nat
            s_list.adult = s_list.adult + cl_list.a + cl_list.co
            s_list.child = s_list.child + cl_list.c
            s_list.rmqty = s_list.rmqty + cl_list.qty

        if (tot_a + tot_co) != 0:

            for s_list in query(s_list_list, filters=(lambda s_list :s_list.nat != "")):

                nation = db_session.query(Nation).filter(
                        (Nation.kurzbez == s_list.nat)).first()

                if nation:
                    s_list.nat = nation.bezeich
                s_list.proz = s_list.adult / (tot_a + tot_co) * 100


    def create_genstat_inhouse3():

        nonlocal tot_payrm, tot_rm, tot_a, tot_c, tot_co, tot_avail, tot_rmqty, inactive, cl_list_list, s_list_list, t_buff_queasy_list, vipnr1, vipnr2, vipnr3, vipnr4, vipnr5, vipnr6, vipnr7, vipnr8, vipnr9, tot_room, all_room, all_remark, queasy, htparam, zkstat, zinrstat, paramtext, guest, reservation, zimmer, zimkateg, res_line, guestseg, segment, mc_guest, mc_types, nation, waehrung, reslin_queasy, mealcoup, genstat
        nonlocal gmember, gbuff, rbuff


        nonlocal setup_list, str_list, cl_list, s_list, zinr_list, t_buff_queasy, gmember, gbuff, rbuff
        nonlocal setup_list_list, str_list_list, cl_list_list, s_list_list, zinr_list_list, t_buff_queasy_list

        i:int = 0
        j:int = 0
        vip_flag:str = ""
        nr:int = 0
        str:str = ""
        actflag1:int = 0
        actflag2:int = 0
        do_it:bool = False
        Gmember = Guest
        Gbuff = Guest
        Rbuff = Reservation
        zinr_list_list.clear()

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
        s_list_list.clear()
        cl_list_list.clear()
        str_list_list.clear()
        tot_avail = 0

        for zkstat in db_session.query(Zkstat).filter(
                (Zkstat.datum == datum)).all():
            tot_avail = tot_avail + zkstat.anz100

        genstat_obj_list = []
        for genstat, zimkateg, reservation, guest, gmember, zimmer in db_session.query(Genstat, Zimkateg, Reservation, Guest, Gmember, Zimmer).join(Zimkateg,(Zimkateg.zikatnr == Genstat.zikatnr)).join(Reservation,(Reservation.resnr == Genstat.resnr)).join(Guest,(Guest.gastnr == Genstat.gastnr)).join(Gmember,(Gmember.gastnr == Genstat.gastnrmember)).join(Zimmer,(Zimmer.zinr == Genstat.zinr) &  (Zimmer.sleeping)).filter(
                (Genstat.datum == datum) &  (func.lower(Genstat.zinr) >= (froom).lower()) &  (func.lower(Genstat.zinr) <= (troom).lower())).all():
            if genstat._recid in genstat_obj_list:
                continue
            else:
                genstat_obj_list.append(genstat._recid)

            if genstat.res_date[0] < datum and genstat.res_date[1] == datum and genstat.resstatus == 8:
                1

            elif exc_depart and genstat.res_date[0] <= datum and genstat.res_date[1] == datum and genstat.resstatus == 8:
                1
            else:

                res_line = db_session.query(Res_line).filter(
                        (Res_line.resnr == genstat.resnr) &  (Res_line.reslinnr == genstat.res_int[0])).first()

                setup_list = query(setup_list_list, filters=(lambda setup_list :setup_list.nr == res_line.setup + 1), first=True)

                if curr_gastnr != guest.gastnr:
                    nr = 0
                    curr_gastnr = guest.gastnr

                if guest.karteityp > 0:
                    nr = nr + 1
                vip_flag = ""

                guestseg = db_session.query(Guestseg).filter(
                        (Guestseg.gastnr == gmember.gastnr) &  ((Guestseg.segmentcode == vipnr1) |  (Guestseg.segmentcode == vipnr2) |  (Guestseg.segmentcode == vipnr3) |  (Guestseg.segmentcode == vipnr4) |  (Guestseg.segmentcode == vipnr5) |  (Guestseg.segmentcode == vipnr6) |  (Guestseg.segmentcode == vipnr7) |  (Guestseg.segmentcode == vipnr8) |  (Guestseg.segmentcode == vipnr9))).first()

                if guestseg:

                    segment = db_session.query(Segment).filter(
                            (Segment.segmentcode == guestseg.segmentcode)).first()
                    vip_flag = segment.bezeich


                cl_list = Cl_list()
                cl_list_list.append(cl_list)

                cl_list.nr = nr
                cl_list.karteityp = guest.karteityp
                cl_list.rmcat = zimkateg.kurzbez + setup_list.char
                cl_list.kurzbez = zimkateg.kurzbez
                cl_list.bezeich = zimkateg.bezeich
                cl_list.nat = gmember.nation1
                cl_list.resnr = genstat.resnr
                cl_list.vip = vip_flag
                cl_list.name = gmember.name + ", " + gmember.vorname1 +\
                        " " + gmember.anrede1
                cl_list.rmno = genstat.zinr
                cl_list.zipreis = genstat.zipreis
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
                cl_list.createID = reservation.useridanlage

                mc_guest = db_session.query(Mc_guest).filter(
                        (Mc_guest.gastnr == gmember.gastnr)).first()

                if mc_guest:
                    cl_list.telefon = gmember.telefon + ";" + mc_guest.cardnum
                else:
                    cl_list.telefon = gmember.telefon

                mc_types = db_session.query(Mc_types).filter(
                        (Mc_types.nr == mc_guest.nr)).first()

                if mc_types:
                    cl_list.mobil_tel = gmember.mobil_telefon + ";" + mc_types.bezeich
                else:
                    cl_list.mobil_tel = gmember.mobil_telefon

                nation = db_session.query(Nation).filter(
                        (Nation.kurzbez == gmember.nation2)).first()

                if nation:
                    cl_list.local_reg = nation.bezeich

                waehrung = db_session.query(Waehrung).filter(
                        (Waehrungsnr == res_line.betriebsnr)).first()

                if waehrung:
                    cl_list.curr = waehrung.wabkurz + ";" + gmember.email_adr

                reslin_queasy = db_session.query(Reslin_queasy).filter(
                        (func.lower(Reslin_queasy.key) == "specialRequest") &  (Reslin_queasy.resnr == res_line.resnr) &  (Reslin_queasy.reslinnr == res_line.reslinnr)).first()

                if reslin_queasy:
                    cl_list.spreq = reslin_queasy.char3 + "," + cl_list.spreq

                reslin_queasy = db_session.query(Reslin_queasy).filter(
                        (func.lower(Reslin_queasy.key) == "arrangement") &  (Reslin_queasy.resnr == res_line.resnr) &  (Reslin_queasy.reslinnr == res_line.reslinnr) &  (Reslin_queasy.datum >= Reslin_queasy.date1) &  (Reslin_queasy.datum <= Reslin_queasy.date2)).first()

                if reslin_queasy:

                    if reslin_queasy.char2 != "":
                        cl_list.ratecode = reslin_queasy.char2
                    else:
                        for i in range(1,num_entries(res_line.zimmer_wunsch, ";") - 1 + 1) :
                            str = entry(i - 1, res_line.zimmer_wunsch, ";")

                            if substring(str, 0, 6) == "$CODE$":
                                cl_list.ratecode = substring(str, 6)
                                break

                segment = db_session.query(Segment).filter(
                        (Segment.segmentcode == genstat.segmentcode)).first()

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

                if incl_gcomment:

                    gbuff = db_session.query(Gbuff).filter(
                            (Gbuff.gastnr == res_line.gastnrmember)).first()

                    if gbuff:
                        for i in range(1,len(gbuff.bemerk)  + 1) :

                            if substring(gbuff.bemerk, i - 1, 1) == chr(10):
                                cl_list.bemerk = cl_list.bemerk + " "
                            else:
                                cl_list.bemerk = cl_list.bemerk + substring(trim(gbuff.bemerk) , i - 1, 1)
                    cl_list.bemerk = cl_list.bemerk + " || "

                if incl_rsvcomment:

                    rbuff = db_session.query(Rbuff).filter(
                            (Rbuff.gastnr == reservation.gastnr)).first()

                    if rbuff:
                        for j in range(1,len(rbuff.bemerk)  + 1) :

                            if substring(rbuff.bemerk, j - 1, 1) == chr(10):
                                cl_list.bemerk1 = cl_list.bemerk1 + " "
                            else:
                                cl_list.bemerk1 = cl_list.bemerk1 + substring(trim(rbuff.bemerk) , j - 1, 1)
                    cl_list.bemerk = cl_list.bemerk + cl_list.bemerk1 + " || "
                for i in range(1,len(res_line.bemerk)  + 1) :

                    if substring(res_line.bemerk, i - 1, 1) == chr (10):
                        cl_list.bemerk = cl_list.bemerk + " "
                    else:
                        cl_list.bemerk = cl_list.bemerk + substring(trim(res_line.bemerk) , i - 1, 1)
                all_remark = res_line.bemerk
                all_remark = replace_str(all_remark, chr(10) , " ")
                all_remark = replace_str(all_remark, chr(13) , " ")
                cl_list.bemerk01 = to_string(substring(all_remark, 0, 225))
                cl_list.bemerk02 = to_string(substring(all_remark, 225, 225))
                cl_list.bemerk03 = to_string(substring(all_remark, 450, 225))
                cl_list.bemerk04 = to_string(substring(all_remark, 675, 225))
                cl_list.pax = to_string(cl_list.a, ">9") + "/" + to_string(cl_list.c, "9") + " " + to_string(cl_list.co, "9")

                if cl_list.nat == "":
                    cl_list.nat = "?"
                else:

                    nation = db_session.query(Nation).filter(
                            (Nation.kurzbez == cl_list.nat)).first()

                    if nation:
                        cl_list.nation = nation.bezeich

                zinr_list = query(zinr_list_list, filters=(lambda zinr_list :zinr_list.zinr == genstat.zinr and zinr_list.resnr == res_line.resnr and zinr_list.reslinnr == res_line.reslinnr), first=True)

                if not zinr_list:
                    zinr_list = Zinr_list()
                    zinr_list_list.append(zinr_list)

                    zinr_list.resnr = res_line.resnr
                    zinr_list.reslinnr = res_line.reslinnr
                    zinr_list.zinr = genstat.zinr

                    queasy = db_session.query(Queasy).filter(
                            (Queasy.key == 14) &  (Queasy.char1 == genstat.zinr) &  (Queasy.date1 <= curr_date) &  (Queasy.date2 >= curr_date)).first()

                    if zimmer.sleeping and genstat.resstatus != 13:

                        if not queasy:
                            tot_rm = tot_rm + 1
                            tot_rmqty = tot_rmqty + 1

                        elif queasy and queasy.number3 != genstat.gastnr:
                            tot_rm = tot_rm + 1
                            tot_rmqty = tot_rmqty + 1

                    if zimmer.sleeping and genstat.zipreis > 0 and genstat.resstatus != 13:

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

            if not disp_accompany:

                cl_list = query(cl_list_list, filters=(lambda cl_list :cl_list.rmno == res_line.zinr and cl_list.resnr == res_line.resnr and cl_list.arrive == res_line.ankunft and cl_list.zipreis == 0 and (cl_list.a + cl_list.c) < 1 and cl_list.co < 1), first=True)

                if cl_list:
                    cl_list_list.remove(cl_list)

                    nr = nr - 1

        for cl_list in query(cl_list_list):

            mealcoup = db_session.query(Mealcoup).filter(
                    (func.lower(Mealcoup.name) == "Breakfast") &  (Mealcoup.resnr == cl_list.resnr) &  (Mealcoup.zinr == cl_list.rmno)).first()

            if mealcoup:
                cl_list.tot_bfast = mealcoup.verbrauch[0] + mealcoup.verbrauch[1] + mealcoup.verbrauch[2] + mealcoup.verbrauch[3] + mealcoup.verbrauch[4] +\
                        mealcoup.verbrauch[5] + mealcoup.verbrauch[6] + mealcoup.verbrauch[7] + mealcoup.verbrauch[8] + mealcoup.verbrauch[9] +\
                        mealcoup.verbrauch[10] + mealcoup.verbrauch[11] + mealcoup.verbrauch[12] + mealcoup.verbrauch[13] + mealcoup.verbrauch[14] +\
                        mealcoup.verbrauch[15] + mealcoup.verbrauch[16] + mealcoup.verbrauch[17] + mealcoup.verbrauch[18] + mealcoup.verbrauch[19] +\
                        mealcoup.verbrauch[20] + mealcoup.verbrauch[21] + mealcoup.verbrauch[22] + mealcoup.verbrauch[23] + mealcoup.verbrauch[24] +\
                        mealcoup.verbrauch[25] + mealcoup.verbrauch[26] + mealcoup.verbrauch[27] + mealcoup.verbrauch[28] + mealcoup.verbrauch[29] +\
                        mealcoup.verbrauch[30] + mealcoup.verbrauch[31]

            s_list = query(s_list_list, filters=(lambda s_list :s_list.bezeich == cl_list.bezeich), first=True)

            if not s_list:

                s_list = query(s_list_list, filters=(lambda s_list :s_list.rmcat == ""), first=True)

                if s_list:
                    s_list.rmcat = cl_list.kurzbez
                    s_list.bezeich = cl_list.bezeich

            if not s_list:
                s_list = S_list()
                s_list_list.append(s_list)

                s_list.rmcat = cl_list.kurzbez
                s_list.bezeich = cl_list.bezeich
            s_list.anz = s_list.anz + cl_list.qty

            s_list = query(s_list_list, filters=(lambda s_list :s_list.nat == cl_list.nat), first=True)

            if not s_list:

                s_list = query(s_list_list, filters=(lambda s_list :s_list.nat == ""), first=True)

                if s_list:
                    s_list.nat = cl_list.nat

            if not s_list:
                s_list = S_list()
                s_list_list.append(s_list)


                if s_list:
                    s_list.nat = cl_list.nat
            s_list.adult = s_list.adult + cl_list.a + cl_list.co
            s_list.child = s_list.child + cl_list.c
            s_list.rmqty = s_list.rmqty + cl_list.qty

        if (tot_a + tot_co) != 0:

            for s_list in query(s_list_list, filters=(lambda s_list :s_list.nat != "")):

                nation = db_session.query(Nation).filter(
                        (Nation.kurzbez == s_list.nat)).first()

                if nation:
                    s_list.nat = nation.bezeich
                s_list.proz = s_list.adult / (tot_a + tot_co) * 100


    def create_buf_queasy():

        nonlocal tot_payrm, tot_rm, tot_a, tot_c, tot_co, tot_avail, tot_rmqty, inactive, cl_list_list, s_list_list, t_buff_queasy_list, vipnr1, vipnr2, vipnr3, vipnr4, vipnr5, vipnr6, vipnr7, vipnr8, vipnr9, tot_room, all_room, all_remark, queasy, htparam, zkstat, zinrstat, paramtext, guest, reservation, zimmer, zimkateg, res_line, guestseg, segment, mc_guest, mc_types, nation, waehrung, reslin_queasy, mealcoup, genstat
        nonlocal gmember, gbuff, rbuff


        nonlocal setup_list, str_list, cl_list, s_list, zinr_list, t_buff_queasy, gmember, gbuff, rbuff
        nonlocal setup_list_list, str_list_list, cl_list_list, s_list_list, zinr_list_list, t_buff_queasy_list


        t_buff_queasy_list.clear()

        for queasy in db_session.query(Queasy).filter(
                (Queasy.key == 140) &  (func.lower(Queasy.char1) == (prog_name).lower())).all():
            t_buff_queasy = T_buff_queasy()
            t_buff_queasy_list.append(t_buff_queasy)

            buffer_copy(queasy, t_buff_queasy)


    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 700)).first()

    if htparam.finteger != 0:
        vipnr1 = htparam.finteger

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 701)).first()

    if htparam.finteger != 0:
        vipnr2 = htparam.finteger

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 702)).first()

    if htparam.finteger != 0:
        vipnr3 = htparam.finteger

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 703)).first()

    if htparam.finteger != 0:
        vipnr4 = htparam.finteger

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 704)).first()

    if htparam.finteger != 0:
        vipnr5 = htparam.finteger

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 705)).first()

    if htparam.finteger != 0:
        vipnr6 = htparam.finteger

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 706)).first()

    if htparam.finteger != 0:
        vipnr7 = htparam.finteger

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 707)).first()

    if htparam.finteger != 0:
        vipnr8 = htparam.finteger

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 708)).first()

    if htparam.finteger != 0:
        vipnr9 = htparam.finteger
    bed_setup()

    if sorttype == 1:

        if disp_exclinact:

            if datum >= curr_date:
                create_inhouse2()
            else:
                create_genstat_inhouse2()
        else:

            if datum >= curr_date:
                create_inhouse()
            else:
                create_genstat_inhouse()
    else:

        if disp_exclinact:

            if datum >= curr_date:
                create_inhouse3()
            else:
                create_genstat_inhouse3()
        else:

            if datum >= curr_date:
                create_inhouse1()
            else:
                create_genstat_inhouse1()
    create_buf_queasy()

    if datum < curr_date:

        for zkstat in db_session.query(Zkstat).filter(
                (Zkstat.datum == datum)).all():
            tot_room = tot_room + zkstat.anz100

        zinrstat = db_session.query(Zinrstat).filter(
                (func.lower(Zinrstat.zinr) == "tot_rm") &  (Zinrstat.datum == datum)).first()

        if zinrstat:
            all_room = zinrstat.zimmeranz
        inactive = all_room - tot_room

    for cl_list in query(cl_list_list):

        mealcoup = db_session.query(Mealcoup).filter(
                (func.lower(Mealcoup.name) == "Breakfast") &  (Mealcoup.resnr == cl_list.resnr) &  (Mealcoup.zinr == cl_list.rmno)).first()

        if mealcoup:
            cl_list.tot_bfast = mealcoup.verbrauch[0] + mealcoup.verbrauch[1] + mealcoup.verbrauch[2] + mealcoup.verbrauch[3] + mealcoup.verbrauch[4] +\
                    mealcoup.verbrauch[5] + mealcoup.verbrauch[6] + mealcoup.verbrauch[7] + mealcoup.verbrauch[8] + mealcoup.verbrauch[9] +\
                    mealcoup.verbrauch[10] + mealcoup.verbrauch[11] + mealcoup.verbrauch[12] + mealcoup.verbrauch[13] + mealcoup.verbrauch[14] +\
                    mealcoup.verbrauch[15] + mealcoup.verbrauch[16] + mealcoup.verbrauch[17] + mealcoup.verbrauch[18] + mealcoup.verbrauch[19] +\
                    mealcoup.verbrauch[20] + mealcoup.verbrauch[21] + mealcoup.verbrauch[22] + mealcoup.verbrauch[23] + mealcoup.verbrauch[24] +\
                    mealcoup.verbrauch[25] + mealcoup.verbrauch[26] + mealcoup.verbrauch[27] + mealcoup.verbrauch[28] + mealcoup.verbrauch[29] +\
                    mealcoup.verbrauch[30] + mealcoup.verbrauch[31]

        s_list = query(s_list_list, filters=(lambda s_list :s_list.rmcat == cl_list.kurzbez), first=True)

        if not s_list:

            s_list = query(s_list_list, filters=(lambda s_list :s_list.rmcat == ""), first=True)

            if s_list:
                s_list.rmcat = cl_list.kurzbez
                s_list.bezeich = cl_list.bezeich

        if not s_list:
            s_list = S_list()
            s_list_list.append(s_list)

            s_list.rmcat = cl_list.kurzbez
            s_list.bezeich = cl_list.bezeich
        s_list.anz = s_list.anz + cl_list.qty

        s_list = query(s_list_list, filters=(lambda s_list :s_list.nat == cl_list.nat), first=True)

        if not s_list:

            s_list = query(s_list_list, filters=(lambda s_list :s_list.nat == ""), first=True)

            if s_list:
                s_list.nat = cl_list.nat

        if not s_list:
            s_list = S_list()
            s_list_list.append(s_list)


            if s_list:
                s_list.nat = cl_list.nat
        s_list.adult = s_list.adult + cl_list.a + cl_list.co
        s_list.child = s_list.child + cl_list.c
        s_list.rmqty = s_list.rmqty + cl_list.qty

    if (tot_a + tot_co) != 0:

        for s_list in query(s_list_list, filters=(lambda s_list :s_list.nat != "")):

            nation = db_session.query(Nation).filter(
                    (Nation.kurzbez == s_list.nat)).first()

            if nation:
                s_list.nat = nation.bezeich
            s_list.proz = s_list.adult / (tot_a + tot_co) * 100


    for cl_list in query(cl_list_list):

        mealcoup = db_session.query(Mealcoup).filter(
                (func.lower(Mealcoup.name) == "Breakfast") &  (Mealcoup.resnr == cl_list.resnr) &  (Mealcoup.zinr == cl_list.rmno)).first()

        if mealcoup:
            cl_list.tot_bfast = mealcoup.verbrauch[0] + mealcoup.verbrauch[1] + mealcoup.verbrauch[2] + mealcoup.verbrauch[3] + mealcoup.verbrauch[4] +\
                    mealcoup.verbrauch[5] + mealcoup.verbrauch[6] + mealcoup.verbrauch[7] + mealcoup.verbrauch[8] + mealcoup.verbrauch[9] +\
                    mealcoup.verbrauch[10] + mealcoup.verbrauch[11] + mealcoup.verbrauch[12] + mealcoup.verbrauch[13] + mealcoup.verbrauch[14] +\
                    mealcoup.verbrauch[15] + mealcoup.verbrauch[16] + mealcoup.verbrauch[17] + mealcoup.verbrauch[18] + mealcoup.verbrauch[19] +\
                    mealcoup.verbrauch[20] + mealcoup.verbrauch[21] + mealcoup.verbrauch[22] + mealcoup.verbrauch[23] + mealcoup.verbrauch[24] +\
                    mealcoup.verbrauch[25] + mealcoup.verbrauch[26] + mealcoup.verbrauch[27] + mealcoup.verbrauch[28] + mealcoup.verbrauch[29] +\
                    mealcoup.verbrauch[30] + mealcoup.verbrauch[31]

        s_list = query(s_list_list, filters=(lambda s_list :s_list.rmcat == cl_list.kurzbez), first=True)

        if not s_list:

            s_list = query(s_list_list, filters=(lambda s_list :s_list.rmcat == ""), first=True)

            if s_list:
                s_list.rmcat = cl_list.kurzbez
                s_list.bezeich = cl_list.bezeich

        if not s_list:
            s_list = S_list()
            s_list_list.append(s_list)

            s_list.rmcat = cl_list.kurzbez
            s_list.bezeich = cl_list.bezeich
        s_list.anz = s_list.anz + cl_list.qty

        s_list = query(s_list_list, filters=(lambda s_list :s_list.nat == cl_list.nat), first=True)

        if not s_list:

            s_list = query(s_list_list, filters=(lambda s_list :s_list.nat == ""), first=True)

            if s_list:
                s_list.nat = cl_list.nat

        if not s_list:
            s_list = S_list()
            s_list_list.append(s_list)


            if s_list:
                s_list.nat = cl_list.nat
        s_list.adult = s_list.adult + cl_list.a + cl_list.co
        s_list.child = s_list.child + cl_list.c
        s_list.rmqty = s_list.rmqty + cl_list.qty

    if (tot_a + tot_co) != 0:

        for s_list in query(s_list_list, filters=(lambda s_list :s_list.nat != "")):

            nation = db_session.query(Nation).filter(
                    (Nation.kurzbez == s_list.nat)).first()

            if nation:
                s_list.nat = nation.bezeich
            s_list.proz = s_list.adult / (tot_a + tot_co) * 100


    return generate_output()