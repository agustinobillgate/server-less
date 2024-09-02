from functions.additional_functions import *
import decimal
from datetime import date
from sqlalchemy import func
from models import Guest, Htparam, Reservation, Sourccod, Res_line, Guestseg, Segment, Nation, Mc_guest, Mc_types, Reslin_queasy, Zimkateg, History, Paramtext

def pj_arrive_12bl(pvilanguage:int, from_date:date, to_date:date, ci_date:date, disptype:int, incl_tentative:bool, sorttype:int, comment_type:int, incl_accompany:bool, zikat_list:[Zikat_list]):
    tot_rm = 0
    tot_a = 0
    tot_c = 0
    tot_co = 0
    cl_list_list = []
    s_list_list = []
    lvcarea:str = "PJ_arrive"
    curr_date:date = None
    vipnr1:int = 999999999
    vipnr2:int = 999999999
    vipnr3:int = 999999999
    vipnr4:int = 999999999
    vipnr5:int = 999999999
    vipnr6:int = 999999999
    vipnr7:int = 999999999
    vipnr8:int = 999999999
    vipnr9:int = 999999999
    ol_gastnr:int = 0
    sms_gastnr:int = 0
    wg_gastnr:int = 0
    indi_gastnr:int = 0
    nr:int = 0
    vip_flag:str = ""
    i:int = 0
    dummy_flag:bool = False
    do_it:bool = False
    last_gcf:int = 0
    tentres:int = 3
    all_remark:str = ""
    stat_list:[str] = ["", "", "", "", "", "", "", "", "", "", "", "", "", "", ""]
    guest = htparam = reservation = sourccod = res_line = guestseg = segment = nation = mc_guest = mc_types = reslin_queasy = zimkateg = history = paramtext = None

    setup_list = cl_list = s_list = zikat_list = gmember = gbuff = None

    setup_list_list, Setup_list = create_model("Setup_list", {"nr":int, "char":str})
    cl_list_list, Cl_list = create_model("Cl_list", {"ci_id":str, "stat_flag":str, "datum":date, "flag":int, "nr":int, "vip":str, "gastnr":int, "resnr":int, "name":str, "groupname":str, "zimmeranz":int, "rmno":str, "qty":int, "zipreis":str, "arrival":str, "depart":str, "rmcat":str, "kurzbez":str, "bezeich":str, "a":int, "c":int, "co":int, "pax":str, "nat":str, "nation":str, "argt":str, "company":str, "flight":str, "etd":str, "stay":int, "segment":str, "rate_code":str, "eta":str, "e_mail":str, "bemerk":str, "bemerk01":str, "bemerk02":str, "bemerk03":str, "bemerk04":str, "bemerk05":str, "bemerk06":str, "bemerk07":str, "bemerk08":str, "spreq":str, "memberno":str, "resdate":str, "sob":str, "created_by":str, "ci_time":str, "city":str, "res_stat":int, "res_stat_str":str, "nation2":str, "birthdate":date})
    s_list_list, S_list = create_model("S_list", {"rmcat":str, "bezeich":str, "nat":str, "anz":int, "adult":int, "proz":decimal, "child":int})
    zikat_list_list, Zikat_list = create_model("Zikat_list", {"selected":bool, "zikatnr":int, "kurzbez":str, "bezeich":str})

    Gmember = Guest
    Gbuff = Guest

    db_session = local_storage.db_session

    def generate_output():
        nonlocal tot_rm, tot_a, tot_c, tot_co, cl_list_list, s_list_list, lvcarea, curr_date, vipnr1, vipnr2, vipnr3, vipnr4, vipnr5, vipnr6, vipnr7, vipnr8, vipnr9, ol_gastnr, sms_gastnr, wg_gastnr, indi_gastnr, nr, vip_flag, i, dummy_flag, do_it, last_gcf, tentres, all_remark, stat_list, guest, htparam, reservation, sourccod, res_line, guestseg, segment, nation, mc_guest, mc_types, reslin_queasy, zimkateg, history, paramtext
        nonlocal gmember, gbuff


        nonlocal setup_list, cl_list, s_list, zikat_list, gmember, gbuff
        nonlocal setup_list_list, cl_list_list, s_list_list, zikat_list_list
        return {"tot_rm": tot_rm, "tot_a": tot_a, "tot_c": tot_c, "tot_co": tot_co, "cl-list": cl_list_list, "s-list": s_list_list}

    def create_arrival(curr_date:date):

        nonlocal tot_rm, tot_a, tot_c, tot_co, cl_list_list, s_list_list, lvcarea, curr_date, vipnr1, vipnr2, vipnr3, vipnr4, vipnr5, vipnr6, vipnr7, vipnr8, vipnr9, ol_gastnr, sms_gastnr, wg_gastnr, indi_gastnr, nr, vip_flag, i, dummy_flag, do_it, last_gcf, tentres, all_remark, stat_list, guest, htparam, reservation, sourccod, res_line, guestseg, segment, nation, mc_guest, mc_types, reslin_queasy, zimkateg, history, paramtext
        nonlocal gmember, gbuff


        nonlocal setup_list, cl_list, s_list, zikat_list, gmember, gbuff
        nonlocal setup_list_list, cl_list_list, s_list_list, zikat_list_list

        if incl_tentative:
            tentres = 12
        vip_flag = ""
        do_it = False
        last_gcf = 0


        nr = 0

        if sorttype == 1:

            res_line_obj_list = []
            for res_line, zikat_list, reservation, sourccod, guest, gmember in db_session.query(Res_line, Zikat_list, Reservation, Sourccod, Guest, Gmember).join(Zikat_list,(Zikat_list.zikatnr == Res_line.zikatnr) &  (Zikat_list.SELECTED)).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Sourccod,(Sourccod.source_code == reservation.resart)).join(Guest,(Guest.gastnr == reservation.gastnr)).join(Gmember,(Gmember.gastnr == Res_line.gastnrmember)).filter(
                    (Res_line.active_flag <= 1) &  (Res_line.resstatus != 12) &  (Res_line.resstatus != tentres) &  (Res_line.ankunft == curr_date)).all():
                if res_line._recid in res_line_obj_list:
                    continue
                else:
                    res_line_obj_list.append(res_line._recid)


                add_cllist()

                if not incl_accompany:

                    cl_list = query(cl_list_list, filters=(lambda cl_list :cl_list.rmno == res_line.zinr and cl_list.resnr == res_line.resnr and date_mdy(cl_list.arrival) == res_line.ankunft and decimal.Decimal(cl_list.zipreis) == 0 and cl_list.co < 1), first=True)

                    if cl_list:
                        cl_list_list.remove(cl_list)

                        nr = nr - 1


        elif sorttype == 2:

            res_line_obj_list = []
            for res_line, zikat_list, reservation, sourccod, guest, gmember in db_session.query(Res_line, Zikat_list, Reservation, Sourccod, Guest, Gmember).join(Zikat_list,(Zikat_list.zikatnr == Res_line.zikatnr) &  (Zikat_list.SELECTED)).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Sourccod,(Sourccod.source_code == reservation.resart)).join(Guest,(Guest.gastnr == reservation.gastnr)).join(Gmember,(Gmember.gastnr == Res_line.gastnrmember)).filter(
                    (Res_line.active_flag <= 1) &  (Res_line.resstatus != 12) &  (Res_line.resstatus != tentres) &  (Res_line.ankunft == curr_date)).all():
                if res_line._recid in res_line_obj_list:
                    continue
                else:
                    res_line_obj_list.append(res_line._recid)


                add_cllist()

                if not incl_accompany:

                    cl_list = query(cl_list_list, filters=(lambda cl_list :cl_list.rmno == res_line.zinr and cl_list.resnr == res_line.resnr and date_mdy(cl_list.arrival) == res_line.ankunft and decimal.Decimal(cl_list.zipreis) == 0 and cl_list.co < 1), first=True)

                    if cl_list:
                        cl_list_list.remove(cl_list)

                        nr = nr - 1


        elif sorttype == 3:

            res_line_obj_list = []
            for res_line, zikat_list, reservation, sourccod, guest, gmember in db_session.query(Res_line, Zikat_list, Reservation, Sourccod, Guest, Gmember).join(Zikat_list,(Zikat_list.zikatnr == Res_line.zikatnr) &  (Zikat_list.SELECTED)).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Sourccod,(Sourccod.source_code == reservation.resart)).join(Guest,(Guest.gastnr == reservation.gastnr)).join(Gmember,(Gmember.gastnr == Res_line.gastnrmember)).filter(
                    (Res_line.active_flag <= 1) &  (Res_line.resstatus != 12) &  (Res_line.resstatus != tentres) &  (Res_line.ankunft == curr_date)).all():
                if res_line._recid in res_line_obj_list:
                    continue
                else:
                    res_line_obj_list.append(res_line._recid)


                add_cllist()

                if not incl_accompany:

                    cl_list = query(cl_list_list, filters=(lambda cl_list :cl_list.rmno == res_line.zinr and cl_list.resnr == res_line.resnr and date_mdy(cl_list.arrival) == res_line.ankunft and decimal.Decimal(cl_list.zipreis) == 0 and cl_list.co < 1), first=True)

                    if cl_list:
                        cl_list_list.remove(cl_list)

                        nr = nr - 1


        elif sorttype == 4:

            res_line_obj_list = []
            for res_line, zikat_list, reservation, sourccod, guest, gmember in db_session.query(Res_line, Zikat_list, Reservation, Sourccod, Guest, Gmember).join(Zikat_list,(Zikat_list.zikatnr == Res_line.zikatnr) &  (Zikat_list.SELECTED)).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Sourccod,(Sourccod.source_code == reservation.resart)).join(Guest,(Guest.gastnr == reservation.gastnr)).join(Gmember,(Gmember.gastnr == Res_line.gastnrmember)).filter(
                    (Res_line.active_flag <= 1) &  (Res_line.resstatus != 12) &  (Res_line.resstatus != tentres) &  (Res_line.ankunft == curr_date)).all():
                if res_line._recid in res_line_obj_list:
                    continue
                else:
                    res_line_obj_list.append(res_line._recid)


                add_cllist()

                if not incl_accompany:

                    cl_list = query(cl_list_list, filters=(lambda cl_list :cl_list.rmno == res_line.zinr and cl_list.resnr == res_line.resnr and date_mdy(cl_list.arrival) == res_line.ankunft and decimal.Decimal(cl_list.zipreis) == 0 and cl_list.co < 1), first=True)

                    if cl_list:
                        cl_list_list.remove(cl_list)

                        nr = nr - 1

        else:

            res_line_obj_list = []
            for res_line, zikat_list, reservation, sourccod, guest, gmember in db_session.query(Res_line, Zikat_list, Reservation, Sourccod, Guest, Gmember).join(Zikat_list,(Zikat_list.zikatnr == Res_line.zikatnr) &  (Zikat_list.SELECTED)).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Sourccod,(Sourccod.source_code == reservation.resart)).join(Guest,(Guest.gastnr == reservation.gastnr)).join(Gmember,(Gmember.gastnr == Res_line.gastnrmember)).filter(
                    (Res_line.active_flag <= 1) &  (Res_line.resstatus != 12) &  (Res_line.resstatus != tentres) &  (Res_line.ankunft == curr_date)).all():
                if res_line._recid in res_line_obj_list:
                    continue
                else:
                    res_line_obj_list.append(res_line._recid)


                add_cllist()

                if not incl_accompany:

                    cl_list = query(cl_list_list, filters=(lambda cl_list :cl_list.rmno == res_line.zinr and cl_list.resnr == res_line.resnr and date_mdy(cl_list.arrival) == res_line.ankunft and decimal.Decimal(cl_list.zipreis) == 0 and cl_list.co < 1), first=True)

                    if cl_list:
                        cl_list_list.remove(cl_list)

                        nr = nr - 1


    def add_cllist():

        nonlocal tot_rm, tot_a, tot_c, tot_co, cl_list_list, s_list_list, lvcarea, curr_date, vipnr1, vipnr2, vipnr3, vipnr4, vipnr5, vipnr6, vipnr7, vipnr8, vipnr9, ol_gastnr, sms_gastnr, wg_gastnr, indi_gastnr, nr, vip_flag, i, dummy_flag, do_it, last_gcf, tentres, all_remark, stat_list, guest, htparam, reservation, sourccod, res_line, guestseg, segment, nation, mc_guest, mc_types, reslin_queasy, zimkateg, history, paramtext
        nonlocal gmember, gbuff


        nonlocal setup_list, cl_list, s_list, zikat_list, gmember, gbuff
        nonlocal setup_list_list, cl_list_list, s_list_list, zikat_list_list

        loop_i:int = 0
        str_rsv:str = ""
        contcode:str = ""
        segmentcode:str = ""
        dummy_flag = False

        if res_line.gastnr == ol_gastnr or res_line.gastnr == wg_gastnr or res_line.gastnr == indi_gastnr or res_line.gastnr == sms_gastnr:
            dummy_flag = True

        setup_list = query(setup_list_list, filters=(lambda setup_list :setup_list.nr == res_line.setup + 1), first=True)
        nr = nr + 1
        vip_flag = ""

        guestseg = db_session.query(Guestseg).filter(
                (Guestseg.gastnr == gmember.gastnr) &  ((Guestseg.segmentcode == vipnr1) |  (Guestseg.segmentcode == vipnr2) |  (Guestseg.segmentcode == vipnr3) |  (Guestseg.segmentcode == vipnr4) |  (Guestseg.segmentcode == vipnr5) |  (Guestseg.segmentcode == vipnr6) |  (Guestseg.segmentcode == vipnr7) |  (Guestseg.segmentcode == vipnr8) |  (Guestseg.segmentcode == vipnr9))).first()

        if guestseg:

            segment = db_session.query(Segment).filter(
                    (Segment.segmentcode == guestseg.segmentcode)).first()
            vip_flag = replace_str(segment.bezeich, " ", "")

        segment = db_session.query(Segment).filter(
                (Segment.segmentcode == reservation.segmentcode)).first()

        if segment:
            segmentcode = segment.bezeich
        for loop_i in range(1,num_entries(res_line.zimmer_wunsch, ";") - 1 + 1) :
            str_rsv = entry(loop_i - 1, res_line.zimmer_wunsch, ";")

            if substring(str_rsv, 0, 6) == "$CODE$":
                contcode = substring(str_rsv, 6)
        cl_list = Cl_list()
        cl_list_list.append(cl_list)

        cl_list.nr = nr
        cl_list.datum = res_line.ankunft
        cl_list.groupname = reservation.groupname
        cl_list.rmcat = zikat_list.kurzbez + setup_list.char
        cl_list.kurzbez = zikat_list.kurzbez
        cl_list.bezeich = zikat_list.bezeich
        cl_list.nat = gmember.nation1
        cl_list.gastnr = res_line.gastnr
        cl_list.resnr = res_line.resnr
        cl_list.vip = vip_flag
        cl_list.name = res_line.name
        cl_list.zipreis = to_string(res_line.zipreis, " >>>,>>>,>>9.99")
        cl_list.zimmeranz = res_line.zimmeranz
        cl_list.rmno = res_line.zinr
        cl_list.arrival = to_string(res_line.ankunft, "99/99/99")
        cl_list.depart = to_string(res_line.abreise, "99/99/99")
        cl_list.a = res_line.erwachs
        cl_list.c = res_line.kind1 + res_line.kind2
        cl_list.co = res_line.gratis
        cl_list.argt = res_line.arrangement
        cl_list.flight = substring(res_line.flight_nr, 0, 6)
        cl_list.eta = substring(res_line.flight_nr, 6, 4)
        cl_list.etd = substring(res_line.flight_nr, 17, 4)
        cl_list.rate_code = contcode
        cl_list.segment = segmentcode
        cl_list.stay = gmember.aufenthalte
        cl_list.E_Mail = gmember.email_adr
        cl_list.sob = sourccod.bezeich
        cl_list.ci_id = res_line.cancelled_id
        cl_list.ci_time = to_string(res_line.ankzeit, "HH:MM")
        cl_list.city = gmember.wohnort
        cl_list.res_stat = res_line.resstatus
        cl_list.res_stat_str = to_string(cl_list.res_stat) + " - " + stat_list[res_line.resstatus - 1]
        cl_list.birthdate = gmember.geburtdatum1

        if guest.karteityp != 0:
            cl_list.company = guest.name + ", " + guest.vorname1 + " " + guest.anrede1 + guest.anredefirma

        if gmember.telefon != "":
            cl_list.company = cl_list.company + ";" + gmember.telefon

        if cl_list.nat == "":
            cl_list.nat = "?"
        else:

            nation = db_session.query(Nation).filter(
                    (Nation.kurzbez == cl_list.nat)).first()

            if nation:
                cl_list.nation = nation.bezeich

        nation = db_session.query(Nation).filter(
                (Nation.kurzbez == gmember.nation2) &  (Nation.natcode > 0)).first()

        if nation:
            cl_list.nation2 = nation.bezeich

        if res_line.resstatus != 11 and res_line.resstatus != 13:
            cl_list.qty = res_line.zimmeranz
            tot_rm = tot_rm + res_line.zimmeranz

        mc_guest = db_session.query(Mc_guest).filter(
                (Mc_guest.gastnr == gmember.gastnr)).first()

        if mc_guest:
            cl_list.memberno = mc_guest.cardnum

            mc_types = db_session.query(Mc_types).filter(
                    (Mc_types.nr == mc_guest.nr)).first()

            if mc_types:
                cl_list.memberno = mc_guest.cardnum + ";" + mc_types.bezeich
        cl_list.resdate = to_string(reservation.resdat, "99/99/99")
        cl_list.created_by = reservation.useridanlage

        if comment_type == 0:
            for i in range(1,len(res_line.bemerk)  + 1) :

                if substring(res_line.bemerk, i - 1, 1) == chr (10):
                    cl_list.bemerk = cl_list.bemerk + " "
                else:
                    cl_list.bemerk = cl_list.bemerk + substring(trim(res_line.bemerk) , i - 1, 1)
            all_remark = res_line.bemerk
            all_remark = replace_str(all_remark, chr(10) , " ")
            all_remark = replace_str(all_remark, chr(13) , " ")
            cl_list.bemerk01 = to_string(substring(all_remark, 0, 255))
            cl_list.bemerk02 = to_string(substring(all_remark, 255, 255))
            cl_list.bemerk03 = to_string(substring(all_remark, 510, 255))
            cl_list.bemerk04 = to_string(substring(all_remark, 765, 255))
            cl_list.bemerk05 = to_string(substring(all_remark, 1020, 255))
            cl_list.bemerk06 = to_string(substring(all_remark, 1275, 255))
            cl_list.bemerk07 = to_string(substring(all_remark, 1530, 255))
            cl_list.bemerk08 = to_string(substring(all_remark, 1785, 255))
        else:

            if dummy_flag or guest.bemerk == "":

                gbuff = db_session.query(Gbuff).filter(
                        (Gbuff.gastnr == res_line.gastnrmember)).first()

                if gbuff:
                    for i in range(1,len(gbuff.bemerk)  + 1) :

                        if substring(gbuff.bemerk, i - 1, 1) == chr (10):
                            cl_list.bemerk = cl_list.bemerk + " "
                        else:
                            cl_list.bemerk = cl_list.bemerk + substring(gbuff.bemerk, i - 1, 1)
            else:
                for i in range(1,len(guest.bemerk)  + 1) :

                    if substring(guest.bemerk, i - 1, 1) == chr (10):
                        cl_list.bemerk = cl_list.bemerk + " "
                    else:
                        cl_list.bemerk = cl_list.bemerk + substring(guest.bemerk, i - 1, 1)

        if cl_list.rmno == "" and cl_list.qty > 1:
            cl_list.rmno = to_string(cl_list.qty, ">>>9")

        if res_line.resstatus == 3:

            if cl_list.qty <= 9:
                cl_list.rmno = "  T" + to_string(cl_list.qty, "9")

            elif cl_list.qty <= 99:
                cl_list.rmno = " T" + to_string(cl_list.qty, "99")

            elif cl_list.qty <= 999:
                cl_list.rmno = "T" + to_string(cl_list.qty, "999")

        elif res_line.resstatus == 4:

            if cl_list.qty <= 9:
                cl_list.rmno = "  W" + to_string(cl_list.qty, "9")

            elif cl_list.qty <= 99:
                cl_list.rmno = " W" + to_string(cl_list.qty, "99")

            elif cl_list.qty <= 999:
                cl_list.rmno = "W" + to_string(cl_list.qty, "999")
        cl_list.pax = to_string(cl_list.a, "9") + "/" + to_string(cl_list.c, "9")

        reslin_queasy = db_session.query(Reslin_queasy).filter(
                (func.lower(Reslin_queasy.key) == "specialRequest") &  (Reslin_queasy.resnr == res_line.resnr) &  (Reslin_queasy.reslinnr == res_line.reslinnr)).first()

        if reslin_queasy:
            cl_list.spreq = reslin_queasy.char3


        tot_a = tot_a + res_line.erwachs * res_line.zimmeranz
        tot_c = tot_c + (res_line.kind1 + res_line.kind2) * res_line.zimmeranz
        tot_co = tot_co + res_line.gratis * res_line.zimmeranz

    def create_actual(curr_date:date):

        nonlocal tot_rm, tot_a, tot_c, tot_co, cl_list_list, s_list_list, lvcarea, curr_date, vipnr1, vipnr2, vipnr3, vipnr4, vipnr5, vipnr6, vipnr7, vipnr8, vipnr9, ol_gastnr, sms_gastnr, wg_gastnr, indi_gastnr, nr, vip_flag, i, dummy_flag, do_it, last_gcf, tentres, all_remark, stat_list, guest, htparam, reservation, sourccod, res_line, guestseg, segment, nation, mc_guest, mc_types, reslin_queasy, zimkateg, history, paramtext
        nonlocal gmember, gbuff


        nonlocal setup_list, cl_list, s_list, zikat_list, gmember, gbuff
        nonlocal setup_list_list, cl_list_list, s_list_list, zikat_list_list


        vip_flag = ""
        do_it = False
        last_gcf = 0


        nr = 0

        if sorttype == 1:

            res_line_obj_list = []
            for res_line, zikat_list, reservation, sourccod, guest, gmember in db_session.query(Res_line, Zikat_list, Reservation, Sourccod, Guest, Gmember).join(Zikat_list,(Zikat_list.zikatnr == Res_line.zikatnr) &  (Zikat_list.SELECTED)).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Sourccod,(Sourccod.source_code == reservation.resart)).join(Guest,(Guest.gastnr == reservation.gastnr)).join(Gmember,(Gmember.gastnr == Res_line.gastnrmember)).filter(
                    (Res_line.active_flag == 1) &  ((Res_line.resstatus == 6) |  (Res_line.resstatus == 13)) &  (Res_line.ankunft == curr_date)).all():
                if res_line._recid in res_line_obj_list:
                    continue
                else:
                    res_line_obj_list.append(res_line._recid)


                add_cllist()

                if not incl_accompany:

                    cl_list = query(cl_list_list, filters=(lambda cl_list :cl_list.rmno == res_line.zinr and cl_list.resnr == res_line.resnr and date_mdy(cl_list.arrival) == res_line.ankunft and decimal.Decimal(cl_list.zipreis) == 0 and cl_list.co < 1), first=True)

                    if cl_list:
                        cl_list_list.remove(cl_list)

                        nr = nr - 1


        elif sorttype == 2:

            res_line_obj_list = []
            for res_line, zikat_list, reservation, sourccod, guest, gmember in db_session.query(Res_line, Zikat_list, Reservation, Sourccod, Guest, Gmember).join(Zikat_list,(Zikat_list.zikatnr == Res_line.zikatnr) &  (Zikat_list.SELECTED)).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Sourccod,(Sourccod.source_code == reservation.resart)).join(Guest,(Guest.gastnr == reservation.gastnr)).join(Gmember,(Gmember.gastnr == Res_line.gastnrmember)).filter(
                    (Res_line.active_flag == 1) &  ((Res_line.resstatus == 6) |  (Res_line.resstatus == 13)) &  (Res_line.ankunft == curr_date)).all():
                if res_line._recid in res_line_obj_list:
                    continue
                else:
                    res_line_obj_list.append(res_line._recid)


                add_cllist()

                if not incl_accompany:

                    cl_list = query(cl_list_list, filters=(lambda cl_list :cl_list.rmno == res_line.zinr and cl_list.resnr == res_line.resnr and date_mdy(cl_list.arrival) == res_line.ankunft and decimal.Decimal(cl_list.zipreis) == 0 and cl_list.co < 1), first=True)

                    if cl_list:
                        cl_list_list.remove(cl_list)

                        nr = nr - 1


        elif sorttype == 3:

            res_line_obj_list = []
            for res_line, zimkateg, zikat_list, sourccod, guest, gmember in db_session.query(Res_line, Zimkateg, Zikat_list, Sourccod, Guest, Gmember).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).join(Zikat_list,(Zikat_list.zikatnr == Res_line.zikatnr) &  (Zikat_list.SELECTED)).join(Sourccod,(Sourccod.source_code == reservation.resart)).join(Guest,(Guest.gastnr == reservation.gastnr)).join(Gmember,(Gmember.gastnr == Res_line.gastnrmember)).filter(
                    (Res_line.active_flag == 1) &  ((Res_line.resstatus == 6) |  (Res_line.resstatus == 13)) &  (Res_line.ankunft == curr_date)).all():
                if res_line._recid in res_line_obj_list:
                    continue
                else:
                    res_line_obj_list.append(res_line._recid)


                add_cllist()

                if not incl_accompany:

                    cl_list = query(cl_list_list, filters=(lambda cl_list :cl_list.rmno == res_line.zinr and cl_list.resnr == res_line.resnr and date_mdy(cl_list.arrival) == res_line.ankunft and decimal.Decimal(cl_list.zipreis) == 0 and cl_list.co < 1), first=True)

                    if cl_list:
                        cl_list_list.remove(cl_list)

                        nr = nr - 1


        elif sorttype == 4:

            res_line_obj_list = []
            for res_line, zimkateg, zikat_list, sourccod, guest, gmember in db_session.query(Res_line, Zimkateg, Zikat_list, Sourccod, Guest, Gmember).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).join(Zikat_list,(Zikat_list.zikatnr == Res_line.zikatnr) &  (Zikat_list.SELECTED)).join(Sourccod,(Sourccod.source_code == reservation.resart)).join(Guest,(Guest.gastnr == reservation.gastnr)).join(Gmember,(Gmember.gastnr == Res_line.gastnrmember)).filter(
                    (Res_line.active_flag == 1) &  ((Res_line.resstatus == 6) |  (Res_line.resstatus == 13)) &  (Res_line.ankunft == curr_date)).all():
                if res_line._recid in res_line_obj_list:
                    continue
                else:
                    res_line_obj_list.append(res_line._recid)


                add_cllist()

                if not incl_accompany:

                    cl_list = query(cl_list_list, filters=(lambda cl_list :cl_list.rmno == res_line.zinr and cl_list.resnr == res_line.resnr and date_mdy(cl_list.arrival) == res_line.ankunft and decimal.Decimal(cl_list.zipreis) == 0 and cl_list.co < 1), first=True)

                    if cl_list:
                        cl_list_list.remove(cl_list)

                        nr = nr - 1

        else:

            res_line_obj_list = []
            for res_line, zimkateg, zikat_list, sourccod, guest, gmember in db_session.query(Res_line, Zimkateg, Zikat_list, Sourccod, Guest, Gmember).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).join(Zikat_list,(Zikat_list.zikatnr == Res_line.zikatnr) &  (Zikat_list.SELECTED)).join(Sourccod,(Sourccod.source_code == reservation.resart)).join(Guest,(Guest.gastnr == reservation.gastnr)).join(Gmember,(Gmember.gastnr == Res_line.gastnrmember)).filter(
                    (Res_line.active_flag == 1) &  ((Res_line.resstatus == 6) |  (Res_line.resstatus == 13)) &  (Res_line.ankunft == curr_date)).all():
                if res_line._recid in res_line_obj_list:
                    continue
                else:
                    res_line_obj_list.append(res_line._recid)


                add_cllist()

                if not incl_accompany:

                    cl_list = query(cl_list_list, filters=(lambda cl_list :cl_list.rmno == res_line.zinr and cl_list.resnr == res_line.resnr and date_mdy(cl_list.arrival) == res_line.ankunft and decimal.Decimal(cl_list.zipreis) == 0 and cl_list.co < 1), first=True)

                    if cl_list:
                        cl_list_list.remove(cl_list)

                        nr = nr - 1


    def create_expected(curr_date:date):

        nonlocal tot_rm, tot_a, tot_c, tot_co, cl_list_list, s_list_list, lvcarea, curr_date, vipnr1, vipnr2, vipnr3, vipnr4, vipnr5, vipnr6, vipnr7, vipnr8, vipnr9, ol_gastnr, sms_gastnr, wg_gastnr, indi_gastnr, nr, vip_flag, i, dummy_flag, do_it, last_gcf, tentres, all_remark, stat_list, guest, htparam, reservation, sourccod, res_line, guestseg, segment, nation, mc_guest, mc_types, reslin_queasy, zimkateg, history, paramtext
        nonlocal gmember, gbuff


        nonlocal setup_list, cl_list, s_list, zikat_list, gmember, gbuff
        nonlocal setup_list_list, cl_list_list, s_list_list, zikat_list_list


        tentres = 3

        if incl_tentative:
            tentres = 12
        vip_flag = ""
        do_it = False
        last_gcf = 0


        nr = 0

        if sorttype == 1:

            res_line_obj_list = []
            for res_line, zikat_list, reservation, sourccod, guest, gmember in db_session.query(Res_line, Zikat_list, Reservation, Sourccod, Guest, Gmember).join(Zikat_list,(Zikat_list.zikatnr == Res_line.zikatnr) &  (Zikat_list.SELECTED)).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Sourccod,(Sourccod.source_code == reservation.resart)).join(Guest,(Guest.gastnr == reservation.gastnr)).join(Gmember,(Gmember.gastnr == Res_line.gastnrmember)).filter(
                    (Res_line.active_flag == 0) &  (Res_line.resstatus != tentres) &  (Res_line.ankunft == curr_date)).all():
                if res_line._recid in res_line_obj_list:
                    continue
                else:
                    res_line_obj_list.append(res_line._recid)


                add_cllist()

                if not incl_accompany:

                    cl_list = query(cl_list_list, filters=(lambda cl_list :cl_list.rmno == res_line.zinr and cl_list.resnr == res_line.resnr and date_mdy(cl_list.arrival) == res_line.ankunft and decimal.Decimal(cl_list.zipreis) == 0 and cl_list.co < 1), first=True)

                    if cl_list:
                        cl_list_list.remove(cl_list)

                        nr = nr - 1


        elif sorttype == 2:

            res_line_obj_list = []
            for res_line, zikat_list, reservation, sourccod, guest, gmember in db_session.query(Res_line, Zikat_list, Reservation, Sourccod, Guest, Gmember).join(Zikat_list,(Zikat_list.zikatnr == Res_line.zikatnr) &  (Zikat_list.SELECTED)).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Sourccod,(Sourccod.source_code == reservation.resart)).join(Guest,(Guest.gastnr == reservation.gastnr)).join(Gmember,(Gmember.gastnr == Res_line.gastnrmember)).filter(
                    (Res_line.active_flag == 0) &  (Res_line.resstatus != tentres) &  (Res_line.ankunft == curr_date)).all():
                if res_line._recid in res_line_obj_list:
                    continue
                else:
                    res_line_obj_list.append(res_line._recid)


                add_cllist()

                if not incl_accompany:

                    cl_list = query(cl_list_list, filters=(lambda cl_list :cl_list.rmno == res_line.zinr and cl_list.resnr == res_line.resnr and date_mdy(cl_list.arrival) == res_line.ankunft and decimal.Decimal(cl_list.zipreis) == 0 and cl_list.co < 1), first=True)

                    if cl_list:
                        cl_list_list.remove(cl_list)

                        nr = nr - 1


        elif sorttype == 3:

            res_line_obj_list = []
            for res_line, zikat_list, reservation, sourccod, guest, gmember in db_session.query(Res_line, Zikat_list, Reservation, Sourccod, Guest, Gmember).join(Zikat_list,(Zikat_list.zikatnr == Res_line.zikatnr) &  (Zikat_list.SELECTED)).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Sourccod,(Sourccod.source_code == reservation.resart)).join(Guest,(Guest.gastnr == reservation.gastnr)).join(Gmember,(Gmember.gastnr == Res_line.gastnrmember)).filter(
                    (Res_line.active_flag == 0) &  (Res_line.resstatus != tentres) &  (Res_line.ankunft == curr_date)).all():
                if res_line._recid in res_line_obj_list:
                    continue
                else:
                    res_line_obj_list.append(res_line._recid)


                add_cllist()

                if not incl_accompany:

                    cl_list = query(cl_list_list, filters=(lambda cl_list :cl_list.rmno == res_line.zinr and cl_list.resnr == res_line.resnr and date_mdy(cl_list.arrival) == res_line.ankunft and decimal.Decimal(cl_list.zipreis) == 0 and cl_list.co < 1), first=True)

                    if cl_list:
                        cl_list_list.remove(cl_list)

                        nr = nr - 1


        elif sorttype == 4:

            res_line_obj_list = []
            for res_line, zikat_list, reservation, sourccod, guest, gmember in db_session.query(Res_line, Zikat_list, Reservation, Sourccod, Guest, Gmember).join(Zikat_list,(Zikat_list.zikatnr == Res_line.zikatnr) &  (Zikat_list.SELECTED)).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Sourccod,(Sourccod.source_code == reservation.resart)).join(Guest,(Guest.gastnr == reservation.gastnr)).join(Gmember,(Gmember.gastnr == Res_line.gastnrmember)).filter(
                    (Res_line.active_flag == 0) &  (Res_line.resstatus != tentres) &  (Res_line.ankunft == curr_date)).all():
                if res_line._recid in res_line_obj_list:
                    continue
                else:
                    res_line_obj_list.append(res_line._recid)


                add_cllist()

                if not incl_accompany:

                    cl_list = query(cl_list_list, filters=(lambda cl_list :cl_list.rmno == res_line.zinr and cl_list.resnr == res_line.resnr and date_mdy(cl_list.arrival) == res_line.ankunft and decimal.Decimal(cl_list.zipreis) == 0 and cl_list.co < 1), first=True)

                    if cl_list:
                        cl_list_list.remove(cl_list)

                        nr = nr - 1

        else:

            res_line_obj_list = []
            for res_line, zikat_list, reservation, sourccod, guest, gmember in db_session.query(Res_line, Zikat_list, Reservation, Sourccod, Guest, Gmember).join(Zikat_list,(Zikat_list.zikatnr == Res_line.zikatnr) &  (Zikat_list.SELECTED)).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Sourccod,(Sourccod.source_code == reservation.resart)).join(Guest,(Guest.gastnr == reservation.gastnr)).join(Gmember,(Gmember.gastnr == Res_line.gastnrmember)).filter(
                    (Res_line.active_flag == 0) &  (Res_line.resstatus != tentres) &  (Res_line.ankunft == curr_date)).all():
                if res_line._recid in res_line_obj_list:
                    continue
                else:
                    res_line_obj_list.append(res_line._recid)


                add_cllist()

                if not incl_accompany:

                    cl_list = query(cl_list_list, filters=(lambda cl_list :cl_list.rmno == res_line.zinr and cl_list.resnr == res_line.resnr and date_mdy(cl_list.arrival) == res_line.ankunft and decimal.Decimal(cl_list.zipreis) == 0 and cl_list.co < 1), first=True)

                    if cl_list:
                        cl_list_list.remove(cl_list)

                        nr = nr - 1


    def create_summary():

        nonlocal tot_rm, tot_a, tot_c, tot_co, cl_list_list, s_list_list, lvcarea, curr_date, vipnr1, vipnr2, vipnr3, vipnr4, vipnr5, vipnr6, vipnr7, vipnr8, vipnr9, ol_gastnr, sms_gastnr, wg_gastnr, indi_gastnr, nr, vip_flag, i, dummy_flag, do_it, last_gcf, tentres, all_remark, stat_list, guest, htparam, reservation, sourccod, res_line, guestseg, segment, nation, mc_guest, mc_types, reslin_queasy, zimkateg, history, paramtext
        nonlocal gmember, gbuff


        nonlocal setup_list, cl_list, s_list, zikat_list, gmember, gbuff
        nonlocal setup_list_list, cl_list_list, s_list_list, zikat_list_list

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
            s_list.adult = s_list.adult + (cl_list.a + cl_list.co) * cl_list.qty
            s_list.child = s_list.child + cl_list.c * cl_list.qty

        if (tot_a + tot_co) != 0:

            for s_list in query(s_list_list, filters=(lambda s_list :s_list.nat != "")):

                nation = db_session.query(Nation).filter(
                        (Nation.kurzbez == s_list.nat)).first()

                if nation:
                    s_list.nat = nation.bezeich
                else:
                    s_list.nat = translateExtended ("UNKNOWN", lvcarea, "")
                s_list.proz = s_list.adult / (tot_a + tot_co) * 100


    def create_arrival1(curr_date:date):

        nonlocal tot_rm, tot_a, tot_c, tot_co, cl_list_list, s_list_list, lvcarea, curr_date, vipnr1, vipnr2, vipnr3, vipnr4, vipnr5, vipnr6, vipnr7, vipnr8, vipnr9, ol_gastnr, sms_gastnr, wg_gastnr, indi_gastnr, nr, vip_flag, i, dummy_flag, do_it, last_gcf, tentres, all_remark, stat_list, guest, htparam, reservation, sourccod, res_line, guestseg, segment, nation, mc_guest, mc_types, reslin_queasy, zimkateg, history, paramtext
        nonlocal gmember, gbuff


        nonlocal setup_list, cl_list, s_list, zikat_list, gmember, gbuff
        nonlocal setup_list_list, cl_list_list, s_list_list, zikat_list_list


        vip_flag = ""
        do_it = False
        last_gcf = 0


        nr = 0

        if sorttype == 1:

            res_line_obj_list = []
            for res_line, zikat_list, reservation, sourccod, guest, gmember in db_session.query(Res_line, Zikat_list, Reservation, Sourccod, Guest, Gmember).join(Zikat_list,(Zikat_list.zikatnr == Res_line.zikatnr) &  (Zikat_list.SELECTED)).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Sourccod,(Sourccod.source_code == reservation.resart)).join(Guest,(Guest.gastnr == reservation.gastnr)).join(Gmember,(Gmember.gastnr == Res_line.gastnrmember)).filter(
                    ((Res_line.resstatus == 6) |  (Res_line.resstatus == 8) |  (Res_line.resstatus == 13)) &  (Res_line.ankunft == curr_date)).all():
                if res_line._recid in res_line_obj_list:
                    continue
                else:
                    res_line_obj_list.append(res_line._recid)


                do_it = True

                if (res_line.ankunft == res_line.abreise) and res_line.resstatus == 8:

                    history = db_session.query(History).filter(
                            (History.resnr == res_line.resnr) &  (History.reslinnr == res_line.reslinnr) &  (History.gesamtumsatz > 0)).first()

                    if not history:
                        do_it = False

                if do_it:
                    add_cllist1()

                    if not incl_accompany:

                        cl_list = query(cl_list_list, filters=(lambda cl_list :cl_list.rmno == res_line.zinr and cl_list.resnr == res_line.resnr and date_mdy(cl_list.arrival) == res_line.ankunft and decimal.Decimal(cl_list.zipreis) == 0 and cl_list.co < 1), first=True)

                        if cl_list:
                            cl_list_list.remove(cl_list)

                            nr = nr - 1


        elif sorttype == 2:

            res_line_obj_list = []
            for res_line, zikat_list, reservation, sourccod, guest, gmember in db_session.query(Res_line, Zikat_list, Reservation, Sourccod, Guest, Gmember).join(Zikat_list,(Zikat_list.zikatnr == Res_line.zikatnr) &  (Zikat_list.SELECTED)).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Sourccod,(Sourccod.source_code == reservation.resart)).join(Guest,(Guest.gastnr == reservation.gastnr)).join(Gmember,(Gmember.gastnr == Res_line.gastnrmember)).filter(
                    ((Res_line.resstatus == 6) |  (Res_line.resstatus == 8) |  (Res_line.resstatus == 13)) &  (Res_line.ankunft == curr_date)).all():
                if res_line._recid in res_line_obj_list:
                    continue
                else:
                    res_line_obj_list.append(res_line._recid)


                do_it = True

                if (res_line.ankunft == res_line.abreise) and res_line.resstatus == 8:

                    history = db_session.query(History).filter(
                            (History.resnr == res_line.resnr) &  (History.reslinnr == res_line.reslinnr) &  (History.gesamtumsatz > 0)).first()

                    if not history:
                        do_it = False

                if do_it:
                    add_cllist1()

                    if not incl_accompany:

                        cl_list = query(cl_list_list, filters=(lambda cl_list :cl_list.rmno == res_line.zinr and cl_list.resnr == res_line.resnr and date_mdy(cl_list.arrival) == res_line.ankunft and decimal.Decimal(cl_list.zipreis) == 0 and cl_list.co < 1), first=True)

                        if cl_list:
                            cl_list_list.remove(cl_list)

                            nr = nr - 1


        elif sorttype == 3:

            res_line_obj_list = []
            for res_line, zikat_list, reservation, sourccod, guest, gmember in db_session.query(Res_line, Zikat_list, Reservation, Sourccod, Guest, Gmember).join(Zikat_list,(Zikat_list.zikatnr == Res_line.zikatnr) &  (Zikat_list.SELECTED)).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Sourccod,(Sourccod.source_code == reservation.resart)).join(Guest,(Guest.gastnr == reservation.gastnr)).join(Gmember,(Gmember.gastnr == Res_line.gastnrmember)).filter(
                    ((Res_line.resstatus == 6) |  (Res_line.resstatus == 8) |  (Res_line.resstatus == 13)) &  (Res_line.ankunft == curr_date)).all():
                if res_line._recid in res_line_obj_list:
                    continue
                else:
                    res_line_obj_list.append(res_line._recid)


                do_it = True

                if (res_line.ankunft == res_line.abreise) and res_line.resstatus == 8:

                    history = db_session.query(History).filter(
                            (History.resnr == res_line.resnr) &  (History.reslinnr == res_line.reslinnr) &  (History.gesamtumsatz > 0)).first()

                    if not history:
                        do_it = False

                if do_it:
                    add_cllist1()

                    if not incl_accompany:

                        cl_list = query(cl_list_list, filters=(lambda cl_list :cl_list.rmno == res_line.zinr and cl_list.resnr == res_line.resnr and date_mdy(cl_list.arrival) == res_line.ankunft and decimal.Decimal(cl_list.zipreis) == 0 and cl_list.co < 1), first=True)

                        if cl_list:
                            cl_list_list.remove(cl_list)

                            nr = nr - 1


        elif sorttype == 4:

            res_line_obj_list = []
            for res_line, zikat_list, reservation, sourccod, guest, gmember in db_session.query(Res_line, Zikat_list, Reservation, Sourccod, Guest, Gmember).join(Zikat_list,(Zikat_list.zikatnr == Res_line.zikatnr) &  (Zikat_list.SELECTED)).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Sourccod,(Sourccod.source_code == reservation.resart)).join(Guest,(Guest.gastnr == reservation.gastnr)).join(Gmember,(Gmember.gastnr == Res_line.gastnrmember)).filter(
                    ((Res_line.resstatus == 6) |  (Res_line.resstatus == 8) |  (Res_line.resstatus == 13)) &  (Res_line.ankunft == curr_date)).all():
                if res_line._recid in res_line_obj_list:
                    continue
                else:
                    res_line_obj_list.append(res_line._recid)


                do_it = True

                if (res_line.ankunft == res_line.abreise) and res_line.resstatus == 8:

                    history = db_session.query(History).filter(
                            (History.resnr == res_line.resnr) &  (History.reslinnr == res_line.reslinnr) &  (History.gesamtumsatz > 0)).first()

                    if not history:
                        do_it = False

                if do_it:
                    add_cllist1()

                    if not incl_accompany:

                        cl_list = query(cl_list_list, filters=(lambda cl_list :cl_list.rmno == res_line.zinr and cl_list.resnr == res_line.resnr and date_mdy(cl_list.arrival) == res_line.ankunft and decimal.Decimal(cl_list.zipreis) == 0 and cl_list.co < 1), first=True)

                        if cl_list:
                            cl_list_list.remove(cl_list)

                            nr = nr - 1

        else:

            res_line_obj_list = []
            for res_line, zikat_list, reservation, sourccod, guest, gmember in db_session.query(Res_line, Zikat_list, Reservation, Sourccod, Guest, Gmember).join(Zikat_list,(Zikat_list.zikatnr == Res_line.zikatnr) &  (Zikat_list.SELECTED)).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Sourccod,(Sourccod.source_code == reservation.resart)).join(Guest,(Guest.gastnr == reservation.gastnr)).join(Gmember,(Gmember.gastnr == Res_line.gastnrmember)).filter(
                    ((Res_line.resstatus == 6) |  (Res_line.resstatus == 8) |  (Res_line.resstatus == 13)) &  (Res_line.ankunft == curr_date)).all():
                if res_line._recid in res_line_obj_list:
                    continue
                else:
                    res_line_obj_list.append(res_line._recid)


                do_it = True

                if (res_line.ankunft == res_line.abreise) and res_line.resstatus == 8:

                    history = db_session.query(History).filter(
                            (History.resnr == res_line.resnr) &  (History.reslinnr == res_line.reslinnr) &  (History.gesamtumsatz > 0)).first()

                    if not history:
                        do_it = False

                if do_it:
                    add_cllist1()

                    if not incl_accompany:

                        cl_list = query(cl_list_list, filters=(lambda cl_list :cl_list.rmno == res_line.zinr and cl_list.resnr == res_line.resnr and date_mdy(cl_list.arrival) == res_line.ankunft and decimal.Decimal(cl_list.zipreis) == 0 and cl_list.co < 1), first=True)

                        if cl_list:
                            cl_list_list.remove(cl_list)

                            nr = nr - 1


    def add_cllist1():

        nonlocal tot_rm, tot_a, tot_c, tot_co, cl_list_list, s_list_list, lvcarea, curr_date, vipnr1, vipnr2, vipnr3, vipnr4, vipnr5, vipnr6, vipnr7, vipnr8, vipnr9, ol_gastnr, sms_gastnr, wg_gastnr, indi_gastnr, nr, vip_flag, i, dummy_flag, do_it, last_gcf, tentres, all_remark, stat_list, guest, htparam, reservation, sourccod, res_line, guestseg, segment, nation, mc_guest, mc_types, reslin_queasy, zimkateg, history, paramtext
        nonlocal gmember, gbuff


        nonlocal setup_list, cl_list, s_list, zikat_list, gmember, gbuff
        nonlocal setup_list_list, cl_list_list, s_list_list, zikat_list_list


        dummy_flag = False

        if res_line.gastnr == ol_gastnr or res_line.gastnr == wg_gastnr or res_line.gastnr == indi_gastnr or res_line.gastnr == sms_gastnr:
            dummy_flag = True

        setup_list = query(setup_list_list, filters=(lambda setup_list :setup_list.nr == res_line.setup + 1), first=True)
        nr = nr + 1
        vip_flag = ""

        guestseg = db_session.query(Guestseg).filter(
                (Guestseg.gastnr == gmember.gastnr) &  ((Guestseg.segmentcode == vipnr1) |  (Guestseg.segmentcode == vipnr2) |  (Guestseg.segmentcode == vipnr3) |  (Guestseg.segmentcode == vipnr4) |  (Guestseg.segmentcode == vipnr5) |  (Guestseg.segmentcode == vipnr6) |  (Guestseg.segmentcode == vipnr7) |  (Guestseg.segmentcode == vipnr8) |  (Guestseg.segmentcode == vipnr9))).first()

        if guestseg:
            vip_flag = "VIP"
        cl_list = Cl_list()
        cl_list_list.append(cl_list)

        cl_list.nr = nr
        cl_list.datum = res_line.ankunft
        cl_list.groupname = reservation.groupname
        cl_list.rmcat = zikat_list.kurzbez + setup_list.char
        cl_list.kurzbez = zikat_list.kurzbez
        cl_list.bezeich = zikat_list.bezeich
        cl_list.nat = gmember.nation1
        cl_list.gastnr = res_line.gastnr
        cl_list.resnr = res_line.resnr
        cl_list.vip = vip_flag
        cl_list.name = res_line.name
        cl_list.zipreis = to_string(res_line.zipreis, " >>>,>>>,>>9.99")
        cl_list.zimmeranz = res_line.zimmeranz
        cl_list.rmno = res_line.zinr
        cl_list.arrival = to_string(res_line.ankunft, "99/99/99")
        cl_list.depart = to_string(res_line.abreise, "99/99/99")
        cl_list.a = res_line.erwachs
        cl_list.c = res_line.kind1 + res_line.kind2
        cl_list.co = res_line.gratis
        cl_list.argt = res_line.arrangement
        cl_list.flight = substring(res_line.flight_nr, 0, 6)
        cl_list.eta = substring(res_line.flight_nr, 6, 4)
        cl_list.etd = substring(res_line.flight_nr, 17, 4)
        cl_list.stay = gmember.aufenthalte
        cl_list.E_Mail = gmember.email_adr
        cl_list.sob = sourccod.bezeich
        cl_list.ci_id = res_line.cancelled_id
        cl_list.ci_time = to_string(res_line.ankzeit, "HH:MM")
        cl_list.city = gmember.wohnort
        cl_list.res_stat = res_line.resstatus
        cl_list.res_stat_str = to_string(cl_list.res_stat) + " - " + stat_list[res_line.resstatus - 1]
        cl_list.birthdate = gmember.geburtdatum1

        if guest.karteityp != 0:
            cl_list.company = guest.name + ", " + guest.vorname1 + " " + guest.anrede1 + guest.anredefirma

        if gmember.telefon != "":
            cl_list.company = cl_list.company + ";" + gmember.telefon

        if cl_list.nat == "":
            cl_list.nat = "?"
        else:

            nation = db_session.query(Nation).filter(
                    (Nation.kurzbez == cl_list.nat)).first()

            if nation:
                cl_list.nation = nation.bezeich

        nation = db_session.query(Nation).filter(
                (Nation.kurzbez == gmember.nation2) &  (Nation.natcode > 0)).first()

        if nation:
            cl_list.nation2 = nation.bezeich

        mc_guest = db_session.query(Mc_guest).filter(
                (Mc_guest.gastnr == gmember.gastnr)).first()

        if mc_guest:
            cl_list.memberno = mc_guest.cardnum

            mc_types = db_session.query(Mc_types).filter(
                    (Mc_types.nr == mc_guest.nr)).first()

            if mc_types:
                cl_list.memberno = mc_guest.cardnum + ";" + mc_types.bezeich
        cl_list.resdate = to_string(reservation.resdat, "99/99/99")
        cl_list.created_by = reservation.useridanlage

        if res_line.resstatus == 6:
            tot_rm = tot_rm + res_line.zimmeranz
            cl_list.qty = res_line.zimmeranz

        elif res_line.resstatus == 8 and (res_line.erwachs + res_line.gratis) > 0:
            tot_rm = tot_rm + res_line.zimmeranz
            cl_list.qty = res_line.zimmeranz

        if comment_type == 0:
            for i in range(1,len(res_line.bemerk)  + 1) :

                if substring(res_line.bemerk, i - 1, 1) == chr (10):
                    cl_list.bemerk = cl_list.bemerk + " "
                else:
                    cl_list.bemerk = cl_list.bemerk + substring(trim(res_line.bemerk) , i - 1, 1)
            all_remark = res_line.bemerk
            all_remark = replace_str(all_remark, chr(10) , " ")
            all_remark = replace_str(all_remark, chr(13) , " ")
            cl_list.bemerk01 = to_string(substring(all_remark, 0, 255))
            cl_list.bemerk02 = to_string(substring(all_remark, 255, 255))
            cl_list.bemerk03 = to_string(substring(all_remark, 510, 255))
            cl_list.bemerk04 = to_string(substring(all_remark, 765, 255))
            cl_list.bemerk05 = to_string(substring(all_remark, 1020, 255))
            cl_list.bemerk06 = to_string(substring(all_remark, 1275, 255))
            cl_list.bemerk07 = to_string(substring(all_remark, 1530, 255))
            cl_list.bemerk08 = to_string(substring(all_remark, 1785, 255))

        elif comment_type == 1:

            if dummy_flag or guest.bemerk == "":

                gbuff = db_session.query(Gbuff).filter(
                        (Gbuff.gastnr == res_line.gastnrmember)).first()

                if gbuff:
                    for i in range(1,len(gbuff.bemerk)  + 1) :

                        if substring(gbuff.bemerk, i - 1, 1) == chr (10):
                            cl_list.bemerk = cl_list.bemerk + " "
                        else:
                            cl_list.bemerk = cl_list.bemerk + substring(trim(gbuff.bemerk) , i - 1, 1)
            else:
                for i in range(1,len(guest.bemerk)  + 1) :

                    if substring(guest.bemerk, i - 1, 1) == chr (10):
                        cl_list.bemerk = guest.bemerk + " "
                    else:
                        cl_list.bemerk = guest.bemerk + substring(trim(guest.bemerk) , i - 1, 1)
        else:

            if dummy_flag or guest.bemerk == "":

                gbuff = db_session.query(Gbuff).filter(
                        (Gbuff.gastnr == res_line.gastnrmember)).first()

                if gbuff:
                    for i in range(1,len(gbuff.bemerk)  + 1) :

                        if substring(gbuff.bemerk, i - 1, 1) == chr(10):
                            cl_list.bemerk = cl_list.bemerk + " "
                        else:
                            cl_list.bemerk = cl_list.bemerk + substring(trim(gbuff.bemerk) , i - 1, 1)
            else:
                for i in range(1,len(guest.bemerk)  + 1) :

                    if substring(guest.bemerk, i - 1, 1) == chr(10):
                        cl_list.bemerk = cl_list.bemerk + " "
                    else:
                        cl_list.bemerk = cl_list.bemerk + substring(trim(guest.bemerk) , i - 1, 1)
            cl_list.bemerk = cl_list.bemerk + " || "
            for i in range(1,len(res_line.bemerk)  + 1) :

                if substring(res_line.bemerk, i - 1, 1) == chr (10):
                    cl_list.bemerk = cl_list.bemerk + " "
                else:
                    cl_list.bemerk = cl_list.bemerk + substring(trim(res_line.bemerk) , i - 1, 1)

        if cl_list.rmno == "" and cl_list.qty > 1:
            cl_list.rmno = to_string(cl_list.qty, ">>>>>9")

        if res_line.resstatus == 3:

            if cl_list.qty <= 9:
                cl_list.rmno = "    T" + to_string(cl_list.qty, "9")

            elif cl_list.qty <= 99:
                cl_list.rmno = "   T" + to_string(cl_list.qty, "99")

            elif cl_list.qty <= 999:
                cl_list.rmno = "  T" + to_string(cl_list.qty, "999")

        elif res_line.resstatus == 4:

            if cl_list.qty <= 9:
                cl_list.rmno = "    W" + to_string(cl_list.qty, "9")

            elif cl_list.qty <= 99:
                cl_list.rmno = "   W" + to_string(cl_list.qty, "99")

            elif cl_list.qty <= 999:
                cl_list.rmno = "  W" + to_string(cl_list.qty, "999")
        cl_list.pax = to_string(cl_list.a, "9") + "/" + to_string(cl_list.c, "9")

        reslin_queasy = db_session.query(Reslin_queasy).filter(
                (func.lower(Reslin_queasy.key) == "specialRequest") &  (Reslin_queasy.resnr == res_line.resnr) &  (Reslin_queasy.reslinnr == res_line.reslinnr)).first()

        if reslin_queasy:
            cl_list.spreq = reslin_queasy.char3


        tot_a = tot_a + res_line.erwachs * res_line.zimmeranz
        tot_c = tot_c + (res_line.kind1 + res_line.kind2) * res_line.zimmeranz
        tot_co = tot_co + res_line.gratis * res_line.zimmeranz

    def bed_setup():

        nonlocal tot_rm, tot_a, tot_c, tot_co, cl_list_list, s_list_list, lvcarea, curr_date, vipnr1, vipnr2, vipnr3, vipnr4, vipnr5, vipnr6, vipnr7, vipnr8, vipnr9, ol_gastnr, sms_gastnr, wg_gastnr, indi_gastnr, nr, vip_flag, i, dummy_flag, do_it, last_gcf, tentres, all_remark, stat_list, guest, htparam, reservation, sourccod, res_line, guestseg, segment, nation, mc_guest, mc_types, reslin_queasy, zimkateg, history, paramtext
        nonlocal gmember, gbuff


        nonlocal setup_list, cl_list, s_list, zikat_list, gmember, gbuff
        nonlocal setup_list_list, cl_list_list, s_list_list, zikat_list_list


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

    stat_list[0] = translateExtended ("Guaranteed", lvcarea, "")
    stat_list[1] = translateExtended ("6 PM", lvcarea, "")
    stat_list[2] = translateExtended ("Tentative", lvcarea, "")
    stat_list[3] = translateExtended ("WaitList", lvcarea, "")
    stat_list[4] = translateExtended ("Verbal Confirm", lvcarea, "")
    stat_list[5] = translateExtended ("Inhouse", lvcarea, "")
    stat_list[6] = ""
    stat_list[7] = translateExtended ("Departed", lvcarea, "")
    stat_list[8] = translateExtended ("Cancelled", lvcarea, "")
    stat_list[9] = translateExtended ("NoShow", lvcarea, "")
    stat_list[10] = translateExtended ("ShareRes", lvcarea, "")
    stat_list[11] = translateExtended ("AccGuest", lvcarea, "")
    stat_list[12] = translateExtended ("RmSharer", lvcarea, "")
    stat_list[13] = translateExtended ("AccGuest", lvcarea, "")

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

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 39)).first()
    ol_gastnr = htparam.finteger

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 109)).first()
    wg_gastnr = htparam.finteger

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 123)).first()
    indi_gastnr = htparam.finteger

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 577)).first()
    sms_gastnr = htparam.finteger
    for curr_date in range(from_date,to_date + 1) :

        if (curr_date > ci_date):
            create_arrival(curr_date)

        elif curr_date < ci_date:
            create_arrival1(curr_date)

        elif curr_date == ci_date:

            if disptype == 1:
                create_arrival(curr_date)

            elif disptype == 2:
                create_actual(curr_date)

            elif disptype == 3:
                create_expected(curr_date)
    create_summary()

    return generate_output()