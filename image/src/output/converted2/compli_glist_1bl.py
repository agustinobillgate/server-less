#using conversion tools version: 1.0.0.112

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
import re
from functions.ratecode_rate import ratecode_rate
from functions.pricecod_rate import pricecod_rate
from models import Htparam, Segment, Guest, Genstat, Zimkateg, Reservation, Res_line, Guestseg, Guest_pr, Arrangement, Reslin_queasy, Queasy

def compli_glist_1bl(pvilanguage:int, from_date:date, to_date:date, sorttype:int, bonus_flag:int, segmentcode:int):

    prepare_cache ([Htparam, Segment, Genstat, Zimkateg, Reservation, Res_line, Guestseg, Guest_pr, Arrangement, Reslin_queasy])

    complig_list_list = []
    do_it:bool = False
    last_sort:string = ""
    int_sort:int = 0
    t_anz:int = 0
    t_pax:int = 0
    tot_anz:int = 0
    tot_pax:int = 0
    ci_date:date = None
    datum:date = None
    new_contrate:bool = False
    bonus_array:List[bool] = create_empty_list(2500, False)
    vip_nr:List[int] = create_empty_list(10,0)
    lvcarea:string = "compli-glist"
    htparam = segment = guest = genstat = zimkateg = reservation = res_line = guestseg = guest_pr = arrangement = reslin_queasy = queasy = None

    complig_list = cl_list = None

    complig_list_list, Complig_list = create_model("Complig_list", {"resnr":int, "reslinnr":int, "datum":date, "zinr":string, "reserve_nm":string, "name":string, "zimmeranz":int, "pax":int, "ankunft":date, "abreise":date, "segm":string, "rstatus":string, "remark":string, "rname":string, "fsort":int, "fdatum":date, "vip":string, "nat":string, "rmtype":string, "rm_rate":Decimal, "rate_code":string, "argt":string, "bill_detail":string, "usr_id":string, "gratis":int})
    cl_list_list, Cl_list = create_model("Cl_list", {"segm":int, "bezeich":string, "zimmeranz":int, "pax":int})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal complig_list_list, do_it, last_sort, int_sort, t_anz, t_pax, tot_anz, tot_pax, ci_date, datum, new_contrate, bonus_array, vip_nr, lvcarea, htparam, segment, guest, genstat, zimkateg, reservation, res_line, guestseg, guest_pr, arrangement, reslin_queasy, queasy
        nonlocal pvilanguage, from_date, to_date, sorttype, bonus_flag, segmentcode


        nonlocal complig_list, cl_list
        nonlocal complig_list_list, cl_list_list

        return {"complig-list": complig_list_list}

    def create_list2():

        nonlocal complig_list_list, do_it, last_sort, int_sort, t_anz, t_pax, tot_anz, tot_pax, ci_date, datum, new_contrate, bonus_array, vip_nr, lvcarea, htparam, segment, guest, genstat, zimkateg, reservation, res_line, guestseg, guest_pr, arrangement, reslin_queasy, queasy
        nonlocal pvilanguage, from_date, to_date, sorttype, bonus_flag, segmentcode


        nonlocal complig_list, cl_list
        nonlocal complig_list_list, cl_list_list

        loopi:int = 0
        gbuff = None
        buf_guest = None
        s:string = ""
        Gbuff =  create_buffer("Gbuff",Guest)
        Buf_guest =  create_buffer("Buf_guest",Guest)
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


        complig_list.rm_rate =  to_decimal(genstat.zipreis)
        complig_list.argt = genstat.argt

        if matches(genstat.res_char[1],r"*$CODE$*"):
            s = substring(genstat.res_char[1], (get_index(genstat.res_char[1], "$CODE$") + 6) - 1)
            complig_list.rate_code = trim(entry(0, s, ";"))
        else:
            complig_list.rate_code = "UNKNOWN"

        reservation = get_cache (Reservation, {"resnr": [(eq, genstat.resnr)]})

        if reservation:
            complig_list.usr_id = reservation.useridanlage

        buf_guest = db_session.query(Buf_guest).filter(
                 (Buf_guest.gastnr == genstat.gastnrmember)).first()

        if buf_guest:

            guestseg = db_session.query(Guestseg).filter(
                     (Guestseg.gastnr == buf_guest.gastnr) & ((Guestseg.segmentcode == vip_nr[0]) | (Guestseg.segmentcode == vip_nr[1]) | (Guestseg.segmentcode == vip_nr[2]) | (Guestseg.segmentcode == vip_nr[3]) | (Guestseg.segmentcode == vip_nr[4]) | (Guestseg.segmentcode == vip_nr[5]) | (Guestseg.segmentcode == vip_nr[6]) | (Guestseg.segmentcode == vip_nr[7]) | (Guestseg.segmentcode == vip_nr[8]) | (Guestseg.segmentcode == vip_nr[9]))).first()

            if guestseg:

                segment = get_cache (Segment, {"segmentcode": [(eq, guestseg.segmentcode)]})

                if segment:
                    complig_list.vip = segment.bezeich


            complig_list.nat = buf_guest.nation1

        zimkateg = get_cache (Zimkateg, {"zikatnr": [(eq, genstat.zikatnr)]})

        if zimkateg:
            complig_list.rmtype = zimkateg.kurzbez

        if genstat.resstatus == 6:
            complig_list.zimmeranz = 1
            t_anz = t_anz + 1

        if genstat.resstatus == 6:
            complig_list.rstatus = translateExtended ("In-House", lvcarea, "")

        elif genstat.resstatus == 13:
            complig_list.rstatus = translateExtended ("Rm Sharer", lvcarea, "")
        else:
            complig_list.rstatus = translateExtended ("Departed", lvcarea, "")

        res_line = get_cache (Res_line, {"resnr": [(eq, genstat.resnr)],"reslinnr": [(eq, genstat.res_int[0])]})

        if res_line:
            for loopi in range(1,length(res_line.bemerk)  + 1) :

                if substring(res_line.bemerk, loopi - 1, 1) != chr_unicode(10):
                    complig_list.remark = complig_list.remark + substring(res_line.bemerk, loopi - 1, 1)
                else:
                    complig_list.remark = complig_list.remark + " "

        gbuff = db_session.query(Gbuff).filter(
                 (Gbuff.gastnr == genstat.gastnrmember)).first()

        if gbuff:
            complig_list.name = gbuff.name + ", " + gbuff.vorname1 + gbuff.anredefirma + " " + gbuff.anrede1

        reservation = get_cache (Reservation, {"resnr": [(eq, genstat.resnr)]})

        if reservation:
            complig_list.reserve_nm = reservation.name

        cl_list = query(cl_list_list, filters=(lambda cl_list: cl_list.segm == genstat.segmentcode), first=True)

        if not cl_list:
            cl_list = Cl_list()
            cl_list_list.append(cl_list)

            cl_list.segm = genstat.segmentcode
            cl_list.bezeich = entry(0, segment.bezeich, "$$0")

        if genstat.resstatus == 6:
            cl_list.zimmeranz = cl_list.zimmeranz + 1
        cl_list.pax = cl_list.pax + genstat.erwachs + genstat.gratis


    def create_list1():

        nonlocal complig_list_list, last_sort, int_sort, t_anz, t_pax, tot_anz, tot_pax, ci_date, datum, new_contrate, bonus_array, vip_nr, lvcarea, htparam, segment, guest, genstat, zimkateg, reservation, res_line, guestseg, guest_pr, arrangement, reslin_queasy, queasy
        nonlocal pvilanguage, from_date, to_date, sorttype, bonus_flag, segmentcode


        nonlocal complig_list, cl_list
        nonlocal complig_list_list, cl_list_list

        fixed_rate:bool = False
        rate_found:bool = False
        ebdisc_flag:bool = False
        kbdisc_flag:bool = False
        early_flag:bool = False
        kback_flag:bool = False
        rate:Decimal = to_decimal("0.0")
        do_it:bool = False
        it_exist:bool = False
        pax:int = 0
        curr_zikatnr:int = 0
        i:int = 0
        curr_i:int = 0
        rm_rate:Decimal = to_decimal("0.0")
        datum_ankunft:int = 0
        loopi:int = 0
        str:string = ""
        buf_guest = None
        Buf_guest =  create_buffer("Buf_guest",Guest)
        fixed_rate = False
        rate_found = False
        ebdisc_flag = matches(res_line.zimmer_wunsch, ("*ebdisc*"))
        kbdisc_flag = matches(res_line.zimmer_wunsch, ("*kbdisc*"))

        if res_line.l_zuordnung[0] != 0:
            curr_zikatnr = res_line.l_zuordnung[0]
        else:
            curr_zikatnr = res_line.zikatnr

        guest_pr = get_cache (Guest_pr, {"gastnr": [(eq, res_line.gastnr)]})
        datum_ankunft = (datum - res_line.ankunft).days

        arrangement = get_cache (Arrangement, {"arrangement": [(eq, res_line.arrangement)]})

        if arrangement:
            check_bonus()
            curr_i = datum_ankunft + 1
            rm_rate =  to_decimal(res_line.zipreis)

        reslin_queasy = get_cache (Reslin_queasy, {"key": [(eq, "arrangement")],"resnr": [(eq, res_line.resnr)],"reslinnr": [(eq, res_line.reslinnr)],"date1": [(le, datum)],"date2": [(ge, datum)]})

        if reslin_queasy:
            fixed_rate = True
            rm_rate =  to_decimal(reslin_queasy.deci1)

            if reslin_queasy.number3 != 0:
                pax = reslin_queasy.number3

            if reslin_queasy.char1 != "":

                arrangement = get_cache (Arrangement, {"arrangement": [(eq, reslin_queasy.char1)]})

                if arrangement:
                    check_bonus()
        else:

            if not it_exist:

                if guest_pr:

                    queasy = get_cache (Queasy, {"key": [(eq, 18)],"number1": [(eq, res_line.reserve_int)]})

                    if new_contrate:
                        rate_found, rate, early_flag, kback_flag = get_output(ratecode_rate(ebdisc_flag, kbdisc_flag, res_line.resnr, res_line.reslinnr, guest_pr.code, None, datum, res_line.ankunft, res_line.abreise, res_line.reserve_int, arrangement.argtnr, curr_zikatnr, res_line.erwachs, res_line.kind1, res_line.kind2, res_line.reserve_dec, res_line.betriebsnr))

                        if rate_found:
                            rm_rate =  to_decimal(rate)
                    else:
                        rate, rate_found = get_output(pricecod_rate(res_line.resnr, res_line.reslinnr, guest_pr.code, datum, res_line.ankunft, res_line.abreise, res_line.reserve_int, arrangement.argtnr, curr_zikatnr, res_line.erwachs, res_line.kind1, res_line.kind2, res_line.reserve_dec, res_line.betriebsnr))

                        if it_exist:
                            rate_found = True

                        if rate_found:
                            rm_rate =  to_decimal(rate)

                        if not it_exist and bonus_array[curr_i - 1] :
                            rm_rate =  to_decimal("0")

                if not rate_found:

                    if bonus_array[curr_i - 1] :
                        rm_rate =  to_decimal("0")

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


            complig_list.rm_rate =  to_decimal(res_line.zipreis)
            complig_list.argt = res_line.arrangement


            for loopi in range(1,num_entries(res_line.zimmer_wunsch, ";") - 1 + 1) :
                str = entry(loopi - 1, res_line.zimmer_wunsch, ";")

                if substring(str, 0, 6) == ("$CODE$").lower() :
                    complig_list.rate_code = substring(str, 6)
                    return

            reservation = get_cache (Reservation, {"resnr": [(eq, res_line.resnr)]})

            if reservation:
                complig_list.usr_id = reservation.useridanlage
                complig_list.reserve_nm = reservation.name

            buf_guest = db_session.query(Buf_guest).filter(
                     (Buf_guest.gastnr == res_line.gastnrmember)).first()

            if buf_guest:

                guestseg = db_session.query(Guestseg).filter(
                         (Guestseg.gastnr == buf_guest.gastnr) & ((Guestseg.segmentcode == vip_nr[0]) | (Guestseg.segmentcode == vip_nr[1]) | (Guestseg.segmentcode == vip_nr[2]) | (Guestseg.segmentcode == vip_nr[3]) | (Guestseg.segmentcode == vip_nr[4]) | (Guestseg.segmentcode == vip_nr[5]) | (Guestseg.segmentcode == vip_nr[6]) | (Guestseg.segmentcode == vip_nr[7]) | (Guestseg.segmentcode == vip_nr[8]) | (Guestseg.segmentcode == vip_nr[9]))).first()

                if guestseg:

                    segment = get_cache (Segment, {"segmentcode": [(eq, guestseg.segmentcode)]})

                    if segment:
                        complig_list.vip = segment.bezeich


                complig_list.nat = buf_guest.nation1

            zimkateg = get_cache (Zimkateg, {"zikatnr": [(eq, res_line.zikatnr)]})

            if zimkateg:
                complig_list.rmtype = zimkateg.kurzbez

            if res_line.resstatus != 11 and res_line.resstatus != 13:
                complig_list.zimmeranz = res_line.zimmeranz
            for i in range(1,length(res_line.bemerk)  + 1) :

                if substring(res_line.bemerk, i - 1, 1) != chr_unicode(10):
                    complig_list.remark = complig_list.remark + substring(res_line.bemerk, i - 1, 1)
                else:
                    complig_list.remark = complig_list.remark + " "

            if res_line.active_flag == 1:
                complig_list.rstatus = "In-House"

            elif res_line.active_flag == 0:
                complig_list.rstatus = "Arival"
            else:
                complig_list.rstatus = "Departed"

            cl_list = query(cl_list_list, filters=(lambda cl_list: cl_list.segm == reservation.segmentcode), first=True)

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
        nonlocal pvilanguage, from_date, to_date, sorttype, bonus_flag, segmentcode


        nonlocal complig_list, cl_list
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

    htparam = get_cache (Htparam, {"paramnr": [(eq, 87)]})
    ci_date = htparam.fdate

    htparam = get_cache (Htparam, {"paramnr": [(eq, 700)]})
    vip_nr[0] = htparam.finteger

    htparam = get_cache (Htparam, {"paramnr": [(eq, 701)]})
    vip_nr[1] = htparam.finteger

    htparam = get_cache (Htparam, {"paramnr": [(eq, 702)]})
    vip_nr[2] = htparam.finteger

    htparam = get_cache (Htparam, {"paramnr": [(eq, 703)]})
    vip_nr[3] = htparam.finteger

    htparam = get_cache (Htparam, {"paramnr": [(eq, 704)]})
    vip_nr[4] = htparam.finteger

    htparam = get_cache (Htparam, {"paramnr": [(eq, 705)]})
    vip_nr[5] = htparam.finteger

    htparam = get_cache (Htparam, {"paramnr": [(eq, 706)]})
    vip_nr[6] = htparam.finteger

    htparam = get_cache (Htparam, {"paramnr": [(eq, 707)]})
    vip_nr[7] = htparam.finteger

    htparam = get_cache (Htparam, {"paramnr": [(eq, 708)]})
    vip_nr[8] = htparam.finteger

    htparam = get_cache (Htparam, {"paramnr": [(eq, 712)]})
    vip_nr[9] = htparam.finteger
    int_sort = 0
    complig_list_list.clear()
    cl_list_list.clear()
    tot_anz = 0
    tot_pax = 0


    for datum in date_range(from_date,to_date) :
        t_anz = 0
        t_pax = 0

        if datum < ci_date:

            if segmentcode != 0:

                if sorttype == 0:

                    genstat_obj_list = {}
                    for genstat, segment, guest in db_session.query(Genstat, Segment, Guest).join(Segment,(Segment.segmentcode == Genstat.segmentcode)).join(Guest,(Guest.gastnr == Genstat.gastnr)).filter(
                             (Genstat.datum == datum) & (Genstat.zipreis == 0) & (Genstat.resstatus == 6) & (Genstat.res_logic[inc_value(1)]) & (Genstat.segmentcode == segmentcode)).order_by(Guest.name, Genstat.zinr, Genstat.resstatus).all():
                        if genstat_obj_list.get(genstat._recid):
                            continue
                        else:
                            genstat_obj_list[genstat._recid] = True

                        if bonus_flag == 0:
                            do_it = not genstat.res_logic[2]

                        elif bonus_flag == 1:
                            do_it = True

                        elif bonus_flag == 2:
                            do_it = genstat.res_logic[2]

                        if do_it:
                            create_list2()


                elif sorttype == 1:

                    genstat_obj_list = {}
                    for genstat, segment, guest in db_session.query(Genstat, Segment, Guest).join(Segment,(Segment.segmentcode == Genstat.segmentcode)).join(Guest,(Guest.gastnr == Genstat.gastnrmember)).filter(
                             (Genstat.datum == datum) & (Genstat.zipreis == 0) & (Genstat.resstatus == 6) & (Genstat.res_logic[inc_value(1)]) & (Genstat.segmentcode == segmentcode)).order_by(Guest.name).all():
                        if genstat_obj_list.get(genstat._recid):
                            continue
                        else:
                            genstat_obj_list[genstat._recid] = True

                        if bonus_flag == 0:
                            do_it = not genstat.res_logic[2]

                        elif bonus_flag == 1:
                            do_it = True

                        elif bonus_flag == 2:
                            do_it = genstat.res_logic[2]

                        if do_it:
                            create_list2()


                elif sorttype == 2:

                    genstat_obj_list = {}
                    for genstat, segment, guest, zimkateg in db_session.query(Genstat, Segment, Guest, Zimkateg).join(Segment,(Segment.segmentcode == Genstat.segmentcode)).join(Guest,(Guest.gastnr == Genstat.gastnr)).join(Zimkateg,(Zimkateg.zikatnr == Genstat.zikatnr)).filter(
                             (Genstat.datum == datum) & (Genstat.zipreis == 0) & (Genstat.resstatus == 6) & (Genstat.res_logic[inc_value(1)]) & (Genstat.segmentcode == segmentcode)).order_by(Genstat.zikatnr, Guest.name, Genstat.zinr, Genstat.resstatus).all():
                        if genstat_obj_list.get(genstat._recid):
                            continue
                        else:
                            genstat_obj_list[genstat._recid] = True

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

                    genstat_obj_list = {}
                    for genstat, segment, guest in db_session.query(Genstat, Segment, Guest).join(Segment,(Segment.segmentcode == Genstat.segmentcode)).join(Guest,(Guest.gastnr == Genstat.gastnr)).filter(
                             (Genstat.datum == datum) & (Genstat.zipreis == 0) & (Genstat.resstatus == 6) & (Genstat.res_logic[inc_value(1)])).order_by(Guest.name, Genstat.zinr, Genstat.resstatus).all():
                        if genstat_obj_list.get(genstat._recid):
                            continue
                        else:
                            genstat_obj_list[genstat._recid] = True

                        if bonus_flag == 0:
                            do_it = not genstat.res_logic[2]

                        elif bonus_flag == 1:
                            do_it = True

                        elif bonus_flag == 2:
                            do_it = genstat.res_logic[2]

                        if do_it:
                            create_list2()


                elif sorttype == 1:

                    genstat_obj_list = {}
                    for genstat, segment, guest in db_session.query(Genstat, Segment, Guest).join(Segment,(Segment.segmentcode == Genstat.segmentcode)).join(Guest,(Guest.gastnr == Genstat.gastnrmember)).filter(
                             (Genstat.datum == datum) & (Genstat.zipreis == 0) & (Genstat.resstatus == 6) & (Genstat.res_logic[inc_value(1)])).order_by(Guest.name).all():
                        if genstat_obj_list.get(genstat._recid):
                            continue
                        else:
                            genstat_obj_list[genstat._recid] = True

                        if bonus_flag == 0:
                            do_it = not genstat.res_logic[2]

                        elif bonus_flag == 1:
                            do_it = True

                        elif bonus_flag == 2:
                            do_it = genstat.res_logic[2]

                        if do_it:
                            create_list2()


                elif sorttype == 2:

                    genstat_obj_list = {}
                    for genstat, segment, guest, zimkateg in db_session.query(Genstat, Segment, Guest, Zimkateg).join(Segment,(Segment.segmentcode == Genstat.segmentcode)).join(Guest,(Guest.gastnr == Genstat.gastnr)).join(Zimkateg,(Zimkateg.zikatnr == Genstat.zikatnr)).filter(
                             (Genstat.datum == datum) & (Genstat.zipreis == 0) & (Genstat.resstatus == 6) & (Genstat.res_logic[inc_value(1)])).order_by(Genstat.zikatnr, Guest.name, Genstat.zinr, Genstat.resstatus).all():
                        if genstat_obj_list.get(genstat._recid):
                            continue
                        else:
                            genstat_obj_list[genstat._recid] = True

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

                    res_line_obj_list = {}
                    for res_line, reservation, segment, guest in db_session.query(Res_line, Reservation, Segment, Guest).join(Reservation,(Reservation.resnr == Res_line.resnr) & (Reservation.segmentcode == segmentcode)).join(Segment,(Segment.segmentcode == Reservation.segmentcode)).join(Guest,(Guest.gastnr == Res_line.gastnr)).filter(
                             (Res_line.active_flag <= 1) & ((Res_line.resstatus <= 2) | (Res_line.resstatus == 5) | (Res_line.resstatus == 6)) & (Res_line.ankunft <= datum) & (Res_line.abreise > datum)).order_by(Guest.name).all():
                        if res_line_obj_list.get(res_line._recid):
                            continue
                        else:
                            res_line_obj_list[res_line._recid] = True


                        create_list1()
                else:

                    res_line_obj_list = {}
                    for res_line, reservation, segment, guest in db_session.query(Res_line, Reservation, Segment, Guest).join(Reservation,(Reservation.resnr == Res_line.resnr) & (Reservation.segmentcode == segmentcode)).join(Segment,(Segment.segmentcode == Reservation.segmentcode)).join(Guest,(Guest.gastnr == Res_line.gastnr)).filter(
                             (Res_line.active_flag <= 1) & ((Res_line.resstatus <= 2) | (Res_line.resstatus == 5) | (Res_line.resstatus == 6)) & (Res_line.ankunft <= datum) & (Res_line.abreise > datum)).order_by(Res_line.name).all():
                        if res_line_obj_list.get(res_line._recid):
                            continue
                        else:
                            res_line_obj_list[res_line._recid] = True


                        create_list1()

            else:

                if sorttype == 0:

                    res_line_obj_list = {}
                    for res_line, reservation, segment, guest in db_session.query(Res_line, Reservation, Segment, Guest).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Segment,(Segment.segmentcode == Reservation.segmentcode)).join(Guest,(Guest.gastnr == Res_line.gastnr)).filter(
                             (Res_line.active_flag <= 1) & ((Res_line.resstatus <= 2) | (Res_line.resstatus == 5) | (Res_line.resstatus == 6)) & (Res_line.ankunft <= datum) & (Res_line.abreise > datum)).order_by(Guest.name).all():
                        if res_line_obj_list.get(res_line._recid):
                            continue
                        else:
                            res_line_obj_list[res_line._recid] = True


                        create_list1()
                else:

                    res_line_obj_list = {}
                    for res_line, reservation, segment, guest in db_session.query(Res_line, Reservation, Segment, Guest).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Segment,(Segment.segmentcode == Reservation.segmentcode)).join(Guest,(Guest.gastnr == Res_line.gastnr)).filter(
                             (Res_line.active_flag <= 1) & ((Res_line.resstatus <= 2) | (Res_line.resstatus == 5) | (Res_line.resstatus == 6)) & (Res_line.ankunft <= datum) & (Res_line.abreise > datum)).order_by(Res_line.name).all():
                        if res_line_obj_list.get(res_line._recid):
                            continue
                        else:
                            res_line_obj_list[res_line._recid] = True


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