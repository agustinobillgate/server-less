from functions.additional_functions import *
import decimal
from datetime import date
import re
from sqlalchemy import func
from functions.ratecode_rate import ratecode_rate
from functions.pricecod_rate import pricecod_rate
from models import Htparam, Segment, Guest, Genstat, Zimkateg, Reservation, Res_line, Guestseg, Guest_pr, Arrangement, Reslin_queasy, Queasy

def compli_glist_1bl(pvilanguage:int, from_date:date, to_date:date, sorttype:int, bonus_flag:int, segmentcode:int):
    complig_list_list = []
    do_it:bool = False
    last_sort:str = ""
    int_sort:int = 0
    t_anz:int = 0
    t_pax:int = 0
    tot_anz:int = 0
    tot_pax:int = 0
    ci_date:date = None
    datum:date = None
    new_contrate:bool = False
    bonus_array:[bool] = [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None]
    vip_nr:[int] = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    lvcarea:str = "compli_glist"
    htparam = segment = guest = genstat = zimkateg = reservation = res_line = guestseg = guest_pr = arrangement = reslin_queasy = queasy = None

    complig_list = cl_list = gbuff = None

    complig_list_list, Complig_list = create_model("Complig_list", {"resnr":int, "reslinnr":int, "datum":date, "zinr":str, "reserve_nm":str, "name":str, "zimmeranz":int, "pax":int, "ankunft":date, "abreise":date, "segm":str, "rstatus":str, "remark":str, "rname":str, "fsort":int, "fdatum":date, "vip":str, "nat":str, "rmtype":str, "rm_rate":decimal, "rate_code":str, "argt":str, "bill_detail":str, "usr_id":str, "gratis":int})
    cl_list_list, Cl_list = create_model("Cl_list", {"segm":int, "bezeich":str, "zimmeranz":int, "pax":int})

    Gbuff = Guest

    db_session = local_storage.db_session

    def generate_output():
        nonlocal complig_list_list, do_it, last_sort, int_sort, t_anz, t_pax, tot_anz, tot_pax, ci_date, datum, new_contrate, bonus_array, vip_nr, lvcarea, htparam, segment, guest, genstat, zimkateg, reservation, res_line, guestseg, guest_pr, arrangement, reslin_queasy, queasy
        nonlocal gbuff


        nonlocal complig_list, cl_list, gbuff
        nonlocal complig_list_list, cl_list_list
        return {"complig-list": complig_list_list}

    def create_list2():

        nonlocal complig_list_list, do_it, last_sort, int_sort, t_anz, t_pax, tot_anz, tot_pax, ci_date, datum, new_contrate, bonus_array, vip_nr, lvcarea, htparam, segment, guest, genstat, zimkateg, reservation, res_line, guestseg, guest_pr, arrangement, reslin_queasy, queasy
        nonlocal gbuff


        nonlocal complig_list, cl_list, gbuff
        nonlocal complig_list_list, cl_list_list

        loopi:int = 0
        s:str = ""
        Gbuff = Guest
        complig_list = Complig_list()
        complig_list_list.append(complig_list)

        complig_list.datum = genstat.datum
        complig_list.zinr = genstat.zinr
        complig_list.pax = genstat.erwachs + genstat.gratis
        complig_list.ankunft = genstat.res_date[0]
        complig_list.abreise = genstat.res_date[1]
        complig_list.segm = segment.bezeich
        complig_list.gratis = genstat.gratis
        t_pax = t_pax + genstat.erwachs + genstat.gratis
        complig_list.fsort = int_sort
        complig_list.resnr = genstat.resnr


        complig_list.rm_rate = genstat.zipreis
        complig_list.argt = genstat.argt

        if re.match(".*\$CODE\$.*",genstat.res_char[1]):
            s = substring(genstat.res_char[1], (1 + get_index(res_char[1], "$CODE$") + 6) - 1)
            complig_list.rate_code = trim(entry(0, s, ";"))
        else:
            complig_list.rate_code = "UNKNOWN"

        reservation = db_session.query(Reservation).filter(
                (Reservation.resnr == genstat.resnr)).first()

        if reservation:
            complig_list.usr_id = reservation.useridanlage

        guest = db_session.query(Guest).filter(
                (Guest.gastnr == genstat.gastnrmember)).first()

        if guest:

            guestseg = db_session.query(Guestseg).filter(
                    (Guestseg.gastnr == guest.gastnr) &  ((Guestseg.segmentcode == vip_nr[0]) |  (Guestseg.segmentcode == vip_nr[1]) |  (Guestseg.segmentcode == vip_nr[2]) |  (Guestseg.segmentcode == vip_nr[3]) |  (Guestseg.segmentcode == vip_nr[4]) |  (Guestseg.segmentcode == vip_nr[5]) |  (Guestseg.segmentcode == vip_nr[6]) |  (Guestseg.segmentcode == vip_nr[7]) |  (Guestseg.segmentcode == vip_nr[8]) |  (Guestseg.segmentcode == vip_nr[9]))).first()

            if guestseg:

                segment = db_session.query(Segment).filter(
                        (Segment.segmentcode == guestseg.segmentcode)).first()

                if segment:
                    complig_list.vip = segment.bezeich


            complig_list.nat = guest.nation1

        zimkateg = db_session.query(Zimkateg).filter(
                (Zimkateg.zikatnr == genstat.zikatnr)).first()

        if zimkateg:
            complig_list.rmtype = zimkateg.kurzbez

        if genstat.resstatus == 6:
            complig_list.zimmeranz = 1
            t_anz = t_anz + 1

        if genstat.resstatus == 6:
            complig_list.rstatus = translateExtended ("In_House", lvcarea, "")

        elif genstat.resstatus == 13:
            complig_list.rstatus = translateExtended ("Rm Sharer", lvcarea, "")
        else:
            complig_list.rstatus = translateExtended ("Departed", lvcarea, "")

        res_line = db_session.query(Res_line).filter(
                (Res_line.resnr == genstat.resnr) &  (Res_line.reslinnr == genstat.res_int[0])).first()

        if res_line:
            for loopi in range(1,len(res_line.bemerk)  + 1) :

                if substring(res_line.bemerk, loopi - 1, 1) != chr(10):
                    complig_list.remark = complig_list.remark + substring(res_line.bemerk, loopi - 1, 1)
                else:
                    complig_list.remark = complig_list.remark + " "

        gbuff = db_session.query(Gbuff).filter(
                (Gbuff.gastnr == genstat.gastnrmember)).first()

        if gbuff:
            complig_list.name = gbuff.name + ", " + gbuff.vorname1 + gbuff.anredefirma + " " + gbuff.anrede1

        reservation = db_session.query(Reservation).filter(
                (Reservation.resnr == genstat.resnr)).first()

        if reservation:
            complig_list.reserve_nm = reservation.name

        cl_list = query(cl_list_list, filters=(lambda cl_list :cl_list.segm == genstat.segmentcode), first=True)

        if not cl_list:
            cl_list = Cl_list()
            cl_list_list.append(cl_list)

            cl_list.segm = genstat.segmentcode
            cl_list.bezeich = entry(0, segment.bezeich, "$$0")

        if genstat.resstatus == 6:
            cl_list.zimmeranz = cl_list.zimmeranz + 1
        cl_list.pax = cl_list.pax + genstat.erwachs + genstat.gratis

    def create_list1():

        nonlocal complig_list_list, do_it, last_sort, int_sort, t_anz, t_pax, tot_anz, tot_pax, ci_date, datum, new_contrate, bonus_array, vip_nr, lvcarea, htparam, segment, guest, genstat, zimkateg, reservation, res_line, guestseg, guest_pr, arrangement, reslin_queasy, queasy
        nonlocal gbuff


        nonlocal complig_list, cl_list, gbuff
        nonlocal complig_list_list, cl_list_list

        fixed_rate:bool = False
        rate_found:bool = False
        ebdisc_flag:bool = False
        kbdisc_flag:bool = False
        early_flag:bool = False
        kback_flag:bool = False
        rate:decimal = 0
        do_it:bool = False
        it_exist:bool = False
        pax:int = 0
        curr_zikatnr:int = 0
        i:int = 0
        curr_i:int = 0
        rm_rate:decimal = 0
        loopi:int = 0
        str:str = ""
        fixed_rate = False
        rate_found = False
        ebdisc_flag = re.match(".*ebdisc.*",res_line.zimmer_wunsch)
        kbdisc_flag = re.match(".*kbdisc.*",res_line.zimmer_wunsch)

        if res_line.l_zuordnung[0] != 0:
            curr_zikatnr = res_line.l_zuordnung[0]
        else:
            curr_zikatnr = res_line.zikatnr

        guest_pr = db_session.query(Guest_pr).filter(
                (Guest_pr.gastnr == res_line.gastnr)).first()

        arrangement = db_session.query(Arrangement).filter(
                (Arrangement == res_line.arrangement)).first()
        check_bonus()
        curr_i = datum - res_line.ankunft + 1
        rm_rate = res_line.zipreis

        reslin_queasy = db_session.query(Reslin_queasy).filter(
                (func.lower(Reslin_queasy.key) == "arrangement") &  (Reslin_queasy.resnr == res_line.resnr) &  (Reslin_queasy.reslinnr == res_line.reslinnr) &  (Reslin_queasy.datum >= Reslin_queasy.date1) &  (Reslin_queasy.datum <= Reslin_queasy.date2)).first()

        if reslin_queasy:
            fixed_rate = True
            rm_rate = reslin_queasy.deci1

            if reslin_queasy.number3 != 0:
                pax = reslin_queasy.number3

            if reslin_queasy.char1 != "":

                arrangement = db_session.query(Arrangement).filter(
                        (Arrangement == reslin_queasy.char1)).first()
                check_bonus()
        else:

            if not it_exist:

                if guest_pr:

                    queasy = db_session.query(Queasy).filter(
                            (Queasy.key == 18) &  (Queasy.number1 == res_line.reserve_int)).first()

                    if new_contrate:
                        rate_found, rate, early_flag, kback_flag = get_output(ratecode_rate(ebdisc_flag, kbdisc_flag, res_line.resnr, res_line.reslinnr, guest_pr.CODE, None, datum, res_line.ankunft, res_line.abreise, res_line.reserve_int, arrangement.argtnr, curr_zikatnr, res_line.erwachs, res_line.kind1, res_line.kind2, res_line.reserve_dec, res_line.betriebsnr))

                        if rate_found:
                            rm_rate = rate
                    else:
                        rate, rate_found = get_output(pricecod_rate(res_line.resnr, res_line.reslinnr, guest_pr.CODE, datum, res_line.ankunft, res_line.abreise, res_line.reserve_int, arrangement.argtnr, curr_zikatnr, res_line.erwachs, res_line.kind1, res_line.kind2, res_line.reserve_dec, res_line.betriebsnr))

                        if it_exist:
                            rate_found = True

                        if rate_found:
                            rm_rate = rate

                        if not it_exist and bonus_array[curr_i - 1] :
                            rm_rate = 0

                if not rate_found:

                    if bonus_array[curr_i - 1] :
                        rm_rate = 0

        if bonus_flag == 0:
            do_it = (rm_rate == 0) and (res_line.gratis > 0)

        elif bonus_flag == 1:
            do_it = (rm_rate == 0)

        elif bonus_flag == 2:
            do_it = (rm_rate == 0) and (res_line.erwachs > 0)

        if do_it:
            complig_list = Complig_list()
            complig_list_list.append(complig_list)

            complig_list.resnr = res_line.resnr
            complig_list.reslinnr = res_line.reslinnr
            complig_list.datum = datum
            complig_list.zinr = res_line.zinr
            complig_list.name = res_line.name
            complig_list.pax = res_line.erwachs + res_line.gratis
            complig_list.ankunft = res_line.ankunft
            complig_list.abreise = res_line.abreise
            complig_list.segm = entry(0, segment.bezeich, "$$0")
            complig_list.fsort = int_sort
            complig_list.gratis = res_line.gratis


            complig_list.rm_rate = res_line.zipreis
            complig_list.argt = res_line.arrangement


            for loopi in range(1,num_entries(res_line.zimmer_wunsch, ";") - 1 + 1) :
                str = entry(loopi - 1, res_line.zimmer_wunsch, ";")

                if substring(str, 0, 6) == "$CODE$":
                    complig_list.rate_code = substring(str, 6)
                    return

            reservation = db_session.query(Reservation).filter(
                    (Reservation.resnr == res_line.resnr)).first()

            if reservation:
                complig_list.usr_id = reservation.useridanlage
                complig_list.reserve_nm = reservation.name

            guest = db_session.query(Guest).filter(
                    (Guest.gastnr == res_line.gastnrmember)).first()

            if guest:

                guestseg = db_session.query(Guestseg).filter(
                        (Guestseg.gastnr == guest.gastnr) &  ((Guestseg.segmentcode == vip_nr[0]) |  (Guestseg.segmentcode == vip_nr[1]) |  (Guestseg.segmentcode == vip_nr[2]) |  (Guestseg.segmentcode == vip_nr[3]) |  (Guestseg.segmentcode == vip_nr[4]) |  (Guestseg.segmentcode == vip_nr[5]) |  (Guestseg.segmentcode == vip_nr[6]) |  (Guestseg.segmentcode == vip_nr[7]) |  (Guestseg.segmentcode == vip_nr[8]) |  (Guestseg.segmentcode == vip_nr[9]))).first()

                if guestseg:

                    segment = db_session.query(Segment).filter(
                            (Segment.segmentcode == guestseg.segmentcode)).first()

                    if segment:
                        complig_list.vip = segment.bezeich


                complig_list.nat = guest.nation1

            zimkateg = db_session.query(Zimkateg).filter(
                    (Zimkateg.zikatnr == res_line.zikatnr)).first()

            if zimkateg:
                complig_list.rmtype = zimkateg.kurzbez

            if res_line.resstatus != 11 and res_line.resstatus != 13:
                complig_list.zimmeranz = res_line.zimmeranz

            guest = db_session.query(Guest).filter(
                    (Guest.gastnr == res_line.gastnr)).first()
            for i in range(1,len(res_line.bemerk)  + 1) :

                if substring(res_line.bemerk, i - 1, 1) != chr(10):
                    complig_list.remark = complig_list.remark + substring(res_line.bemerk, i - 1, 1)
                else:
                    complig_list.remark = complig_list.remark + " "

            if res_line.active_flag == 1:
                complig_list.rstatus = "In_House"

            elif res_line.active_flag == 0:
                complig_list.rstatus = "Arival"
            else:
                complig_list.rstatus = "Departed"

            cl_list = query(cl_list_list, filters=(lambda cl_list :cl_list.segm == reservation.segmentcode), first=True)

            if not cl_list:
                cl_list = Cl_list()
                cl_list_list.append(cl_list)

                cl_list.segm = reservation.segmentcode
                cl_list.bezeich = entry(0, segment.bezeich, "$$0")

            if (res_line.abreise > datum) or ((res_line.abreise == datum) and (res_line.active_flag == 1)):
                cl_list.zimmeranz = cl_list.zimmeranz + 1
                cl_list.pax = cl_list.pax + res_line.erwachs + res_line.gratis
                t_anz = t_anz + 1
                t_pax = t_pax + res_line.erwachs + res_line.gratis

    def check_bonus():

        nonlocal complig_list_list, do_it, last_sort, int_sort, t_anz, t_pax, tot_anz, tot_pax, ci_date, datum, new_contrate, bonus_array, vip_nr, lvcarea, htparam, segment, guest, genstat, zimkateg, reservation, res_line, guestseg, guest_pr, arrangement, reslin_queasy, queasy
        nonlocal gbuff


        nonlocal complig_list, cl_list, gbuff
        nonlocal complig_list_list, cl_list_list

        i:int = 0
        j:int = 1
        k:int = 0
        n:int = 0
        stay:int = 0
        pay:int = 0
        num_bonus:int = 0
        for i in range(1,99 + 1) :
            bonus_array[i - 1] = False
        j = 1
        for i in range(1,4 + 1) :
            stay = to_int(substring(arrangement.options, j - 1, 2))
            pay = to_int(substring(arrangement.options, j + 2 - 1, 2))

            if (stay - pay) > 0:
                n = num_bonus + pay + 1
                for k in range(n,stay + 1) :
                    bonus_array[k - 1] = True
                num_bonus = stay - pay
            j = j + 4


    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 87)).first()
    ci_date = htparam.fdate

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 700)).first()
    vip_nr[0] = htparam.finteger

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 701)).first()
    vip_nr[1] = htparam.finteger

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 702)).first()
    vip_nr[2] = htparam.finteger

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 703)).first()
    vip_nr[3] = htparam.finteger

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 704)).first()
    vip_nr[4] = htparam.finteger

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 705)).first()
    vip_nr[5] = htparam.finteger

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 706)).first()
    vip_nr[6] = htparam.finteger

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 707)).first()
    vip_nr[7] = htparam.finteger

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 708)).first()
    vip_nr[8] = htparam.finteger

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 712)).first()
    vip_nr[9] = htparam.finteger
    int_sort = 0
    complig_list_list.clear()
    cl_list_list.clear()
    tot_anz = 0
    tot_pax = 0


    for datum in range(from_date,to_date + 1) :
        t_anz = 0
        t_pax = 0

        if datum < ci_date:

            if segmentcode != 0:

                if sorttype == 0:

                    genstat_obj_list = []
                    for genstat, segment, guest in db_session.query(Genstat, Segment, Guest).join(Segment,(Segment.segmentcode == Genstat.segmentcode)).join(Guest,(Guest.gastnr == Genstat.gastnr)).filter(
                            (Genstat.datum == datum) &  (Genstat.zipreis == 0) &  (Genstat.resstatus == 6) &  (Genstat.res_logic[1]) &  (Genstat.segmentcode == segmentcode)).all():
                        if genstat._recid in genstat_obj_list:
                            continue
                        else:
                            genstat_obj_list.append(genstat._recid)

                        if bonus_flag == 0:
                            do_it = not genstat.res_logic[2]

                        elif bonus_flag == 1:
                            do_it = True

                        elif bonus_flag == 2:
                            do_it = genstat.res_logic[2]

                        if do_it:
                            create_list2()

                else:

                    genstat_obj_list = []
                    for genstat, segment, guest in db_session.query(Genstat, Segment, Guest).join(Segment,(Segment.segmentcode == Genstat.segmentcode)).join(Guest,(Guest.gastnr == Genstat.gastnrmember)).filter(
                            (Genstat.datum == datum) &  (Genstat.zipreis == 0) &  (Genstat.resstatus == 6) &  (Genstat.res_logic[1]) &  (Genstat.segmentcode == segmentcode)).all():
                        if genstat._recid in genstat_obj_list:
                            continue
                        else:
                            genstat_obj_list.append(genstat._recid)

                        if bonus_flag == 0:
                            do_it = not genstat.res_logic[2]

                        elif bonus_flag == 1:
                            do_it = True

                        elif bonus_flag == 2:
                            do_it = genstat.res_logic[2]

                        if do_it:
                            create_list2()


                if sorttype == 3:

                    genstat_obj_list = []
                    for genstat, segment, guest, zimkateg in db_session.query(Genstat, Segment, Guest, Zimkateg).join(Segment,(Segment.segmentcode == Genstat.segmentcode)).join(Guest,(Guest.gastnr == Genstat.gastnr)).join(Zimkateg,(Zimkateg.zikatnr == Genstat.zikatnr)).filter(
                            (Genstat.datum == datum) &  (Genstat.zipreis == 0) &  (Genstat.resstatus == 6) &  (Genstat.res_logic[1]) &  (Genstat.segmentcode == segmentcode)).all():
                        if genstat._recid in genstat_obj_list:
                            continue
                        else:
                            genstat_obj_list.append(genstat._recid)

                        if bonus_flag == 0:
                            do_it = not genstat.res_logic[2]

                        elif bonus_flag == 1:
                            do_it = True

                        elif bonus_flag == 2:
                            do_it = genstat.res_logic[2]

                        if do_it:
                            create_list2()

            else:

                if sorttype == 0:

                    genstat_obj_list = []
                    for genstat, segment, guest in db_session.query(Genstat, Segment, Guest).join(Segment,(Segment.segmentcode == Genstat.segmentcode)).join(Guest,(Guest.gastnr == Genstat.gastnr)).filter(
                            (Genstat.datum == datum) &  (Genstat.zipreis == 0) &  (Genstat.resstatus == 6) &  (Genstat.res_logic[1])).all():
                        if genstat._recid in genstat_obj_list:
                            continue
                        else:
                            genstat_obj_list.append(genstat._recid)

                        if bonus_flag == 0:
                            do_it = not genstat.res_logic[2]

                        elif bonus_flag == 1:
                            do_it = True

                        elif bonus_flag == 2:
                            do_it = genstat.res_logic[2]

                        if do_it:
                            create_list2()

                else:

                    genstat_obj_list = []
                    for genstat, segment, guest in db_session.query(Genstat, Segment, Guest).join(Segment,(Segment.segmentcode == Genstat.segmentcode)).join(Guest,(Guest.gastnr == Genstat.gastnrmember)).filter(
                            (Genstat.datum == datum) &  (Genstat.zipreis == 0) &  (Genstat.resstatus == 6) &  (Genstat.res_logic[1])).all():
                        if genstat._recid in genstat_obj_list:
                            continue
                        else:
                            genstat_obj_list.append(genstat._recid)

                        if bonus_flag == 0:
                            do_it = not genstat.res_logic[2]

                        elif bonus_flag == 1:
                            do_it = True

                        elif bonus_flag == 2:
                            do_it = genstat.res_logic[2]

                        if do_it:
                            create_list2()


                if sorttype == 3:

                    genstat_obj_list = []
                    for genstat, segment, guest, zimkateg in db_session.query(Genstat, Segment, Guest, Zimkateg).join(Segment,(Segment.segmentcode == Genstat.segmentcode)).join(Guest,(Guest.gastnr == Genstat.gastnr)).join(Zimkateg,(Zimkateg.zikatnr == Genstat.zikatnr)).filter(
                            (Genstat.datum == datum) &  (Genstat.zipreis == 0) &  (Genstat.resstatus == 6) &  (Genstat.res_logic[1])).all():
                        if genstat._recid in genstat_obj_list:
                            continue
                        else:
                            genstat_obj_list.append(genstat._recid)

                        if bonus_flag == 0:
                            do_it = not genstat.res_logic[2]

                        elif bonus_flag == 1:
                            do_it = True

                        elif bonus_flag == 2:
                            do_it = genstat.res_logic[2]

                        if do_it:
                            create_list2()

        else:

            if segmentcode != 0:

                if sorttype == 0:

                    res_line_obj_list = []
                    for res_line, reservation, segment, guest in db_session.query(Res_line, Reservation, Segment, Guest).join(Reservation,(Reservation.resnr == Res_line.resnr) &  (Reservation.segmentcode == segmentcode)).join(Segment,(Segment.segmentcode == reservation.segmentcode)).join(Guest,(Guest.gastnr == Res_line.gastnr)).filter(
                            (Res_line.active_flag <= 1) &  ((Res_line.resstatus <= 2) |  (Res_line.resstatus == 5) |  (Res_line.resstatus == 6)) &  (Res_line.ankunft <= datum) &  (Res_line.abreise > datum)).all():
                        if res_line._recid in res_line_obj_list:
                            continue
                        else:
                            res_line_obj_list.append(res_line._recid)


                        create_list1()
                else:

                    res_line_obj_list = []
                    for res_line, reservation, segment, guest in db_session.query(Res_line, Reservation, Segment, Guest).join(Reservation,(Reservation.resnr == Res_line.resnr) &  (Reservation.segmentcode == segmentcode)).join(Segment,(Segment.segmentcode == reservation.segmentcode)).join(Guest,(Guest.gastnr == Res_line.gastnr)).filter(
                            (Res_line.active_flag <= 1) &  ((Res_line.resstatus <= 2) |  (Res_line.resstatus == 5) |  (Res_line.resstatus == 6)) &  (Res_line.ankunft <= datum) &  (Res_line.abreise > datum)).all():
                        if res_line._recid in res_line_obj_list:
                            continue
                        else:
                            res_line_obj_list.append(res_line._recid)


                        create_list1()

            else:

                if sorttype == 0:

                    res_line_obj_list = []
                    for res_line, reservation, segment, guest in db_session.query(Res_line, Reservation, Segment, Guest).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Segment,(Segment.segmentcode == reservation.segmentcode)).join(Guest,(Guest.gastnr == Res_line.gastnr)).filter(
                            (Res_line.active_flag <= 1) &  ((Res_line.resstatus <= 2) |  (Res_line.resstatus == 5) |  (Res_line.resstatus == 6)) &  (Res_line.ankunft <= datum) &  (Res_line.abreise > datum)).all():
                        if res_line._recid in res_line_obj_list:
                            continue
                        else:
                            res_line_obj_list.append(res_line._recid)


                        create_list1()
                else:

                    res_line_obj_list = []
                    for res_line, reservation, segment, guest in db_session.query(Res_line, Reservation, Segment, Guest).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Segment,(Segment.segmentcode == reservation.segmentcode)).join(Guest,(Guest.gastnr == Res_line.gastnr)).filter(
                            (Res_line.active_flag <= 1) &  ((Res_line.resstatus <= 2) |  (Res_line.resstatus == 5) |  (Res_line.resstatus == 6)) &  (Res_line.ankunft <= datum) &  (Res_line.abreise > datum)).all():
                        if res_line._recid in res_line_obj_list:
                            continue
                        else:
                            res_line_obj_list.append(res_line._recid)


                        create_list1()

        int_sort = int_sort + 1

        if t_anz != 0 and t_pax != 0:
            complig_list = Complig_list()
            complig_list_list.append(complig_list)

            complig_list.name = "T O T A L"
            complig_list.zimmeranz = t_anz
            complig_list.pax = t_pax
            complig_list.fdatum = datum
            complig_list.fsort = int_sort
            complig_list.zinr = ""


        int_sort = int_sort + 1
    int_sort = int_sort + 1
    complig_list = Complig_list()
    complig_list_list.append(complig_list)

    complig_list.name = translateExtended ("SUMMARY BY segmentcode", lvcarea, "")
    complig_list.rname = "SUMMARY BY segmentcode"
    complig_list.fsort = int_sort
    complig_list.zinr = ""

    for cl_list in query(cl_list_list):
        int_sort = int_sort + 1
        complig_list = Complig_list()
        complig_list_list.append(complig_list)

        complig_list.name = cl_list.bezeich
        complig_list.zimmeranz = cl_list.zimmeranz
        complig_list.pax = cl_list.pax
        tot_anz = tot_anz + cl_list.zimmeranz
        tot_pax = tot_pax + cl_list.pax
        complig_list.fsort = int_sort
        complig_list.zinr = ""
    int_sort = int_sort + 1
    complig_list = Complig_list()
    complig_list_list.append(complig_list)

    complig_list.name = "TOTAL"
    complig_list.zimmeranz = tot_anz
    complig_list.pax = tot_pax
    complig_list.fsort = int_sort
    complig_list.zinr = ""

    return generate_output()