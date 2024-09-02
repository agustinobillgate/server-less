from functions.additional_functions import *
import decimal
from datetime import date
from sqlalchemy import func
import re
from functions.get_room_breakdown import get_room_breakdown
from functions.calc_servvat import calc_servvat
from models import Htparam, Zimmer, Zkstat, Zinrstat, Genstat, Segment, Guestseg, Reservation, Res_line, Outorder, Artikel, Umsatz

def rm_drecap2_webbl(pvilanguage:int, opening_date:date, from_date:date, to_date:date, fdate:date, tdate:date, segmtype_exist:bool, mi_mtd_chk:bool, mi_ftd_chk:bool, mi_exchu_chk:bool, mi_exccomp_chk:bool, long_digit:bool):
    cl_list_list = []
    lvcarea:str = "rm_drecap2"
    do_it:bool = False
    droomrev:int = 0
    mroomrev:int = 0
    yroomrev:int = 0
    droomexc:int = 0
    mroomexc:int = 0
    yroomexc:int = 0
    tot_room:int = 0
    all_room:int = 0
    dvacant:int = 0
    dooo:int = 0
    mvacant:int = 0
    mooo:int = 0
    yvacant:int = 0
    yooo:int = 0
    dnoshow:int = 0
    dcancel:int = 0
    mnoshow:int = 0
    mcancel:int = 0
    ynoshow:int = 0
    ycancel:int = 0
    droom:int = 0
    proz1:decimal = 0
    mroom:int = 0
    proz2:int = 0
    dpax:int = 0
    mpax:int = 0
    drate:decimal = 0
    mrate:decimal = 0
    drev:decimal = 0
    mrev:decimal = 0
    yroom:int = 0
    ypax:int = 0
    yrate:decimal = 0
    yrev:decimal = 0
    from_bez:str = ""
    to_bez:str = ""
    inactive:int = 0
    mtd_act:int = 0
    mtd_totrm:int = 0
    ytd_act:int = 0
    ytd_totrm:int = 0
    ncompli:int = 0
    mtd_ncompli:int = 0
    ytd_ncompli:int = 0
    dcompli:int = 0
    mcompli:int = 0
    ycompli:int = 0
    dhu:int = 0
    mhu:int = 0
    yhu:int = 0
    ci_date:date = None
    htparam = zimmer = zkstat = zinrstat = genstat = segment = guestseg = reservation = res_line = outorder = artikel = umsatz = None

    cl_list = bgenstat = None

    cl_list_list, Cl_list = create_model("Cl_list", {"segm":int, "betriebsnr":int, "compli":bool, "bezeich":str, "droom":int, "proz1":decimal, "mroom":int, "proz2":decimal, "dpax":int, "mpax":int, "drate":decimal, "mrate":decimal, "drev":decimal, "mrev":decimal, "yroom":int, "proz3":decimal, "ypax":int, "yrate":decimal, "yrev":decimal, "zero_flag":bool})

    Bgenstat = Genstat

    db_session = local_storage.db_session

    def generate_output():
        nonlocal cl_list_list, lvcarea, do_it, droomrev, mroomrev, yroomrev, droomexc, mroomexc, yroomexc, tot_room, all_room, dvacant, dooo, mvacant, mooo, yvacant, yooo, dnoshow, dcancel, mnoshow, mcancel, ynoshow, ycancel, droom, proz1, mroom, proz2, dpax, mpax, drate, mrate, drev, mrev, yroom, ypax, yrate, yrev, from_bez, to_bez, inactive, mtd_act, mtd_totrm, ytd_act, ytd_totrm, ncompli, mtd_ncompli, ytd_ncompli, dcompli, mcompli, ycompli, dhu, mhu, yhu, ci_date, htparam, zimmer, zkstat, zinrstat, genstat, segment, guestseg, reservation, res_line, outorder, artikel, umsatz
        nonlocal bgenstat


        nonlocal cl_list, bgenstat
        nonlocal cl_list_list
        return {"cl-list": cl_list_list}

    def create_umsatz1():

        nonlocal cl_list_list, lvcarea, do_it, droomrev, mroomrev, yroomrev, droomexc, mroomexc, yroomexc, tot_room, all_room, dvacant, dooo, mvacant, mooo, yvacant, yooo, dnoshow, dcancel, mnoshow, mcancel, ynoshow, ycancel, droom, proz1, mroom, proz2, dpax, mpax, drate, mrate, drev, mrev, yroom, ypax, yrate, yrev, from_bez, to_bez, inactive, mtd_act, mtd_totrm, ytd_act, ytd_totrm, ncompli, mtd_ncompli, ytd_ncompli, dcompli, mcompli, ycompli, dhu, mhu, yhu, ci_date, htparam, zimmer, zkstat, zinrstat, genstat, segment, guestseg, reservation, res_line, outorder, artikel, umsatz
        nonlocal bgenstat


        nonlocal cl_list, bgenstat
        nonlocal cl_list_list

        i:int = 0
        datum:date = None
        black_list:int = 0

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 709)).first()
        black_list = htparam.finteger
        cl_list_list.clear()
        droom = 0
        mroom = 0
        yroom = 0
        dpax = 0
        mpax = 0
        ypax = 0
        drev = 0
        mrev = 0
        yrev = 0
        tot_room = 0
        inactive = 0
        mtd_act = 0
        ytd_act = 0
        mtd_totrm = 0
        ytd_totrm = 0

        for zimmer in db_session.query(Zimmer).filter(
                (not sleeping)).all():
            inactive = inactive + 1

        for zimmer in db_session.query(Zimmer).filter(
                (sleeping)).all():
            tot_room = tot_room + 1
        count_mtd_totrm1()

        if not segmtype_exist:
            cal_umsatz4(1, 12, 15, 49, translateExtended ("Room Revenue", lvcarea, ""), "", True)
            cal_umsatz4(13, 14, 0, 0, translateExtended ("Total Room Occ", lvcarea, ""), translateExtended ("Double Occupancy", lvcarea, ""), False)
        else:
            cal_umsatz4a(0, 0, translateExtended ("Room Revenue", lvcarea, ""), "", True)
            cal_umsatz4b(1, 2, translateExtended ("Total Room Occ", lvcarea, ""), translateExtended ("Double Occupancy", lvcarea, ""), False)
        cal_umsatz5()
        cal_umsatz6()

    def create_umsatz():

        nonlocal cl_list_list, lvcarea, do_it, droomrev, mroomrev, yroomrev, droomexc, mroomexc, yroomexc, tot_room, all_room, dvacant, dooo, mvacant, mooo, yvacant, yooo, dnoshow, dcancel, mnoshow, mcancel, ynoshow, ycancel, droom, proz1, mroom, proz2, dpax, mpax, drate, mrate, drev, mrev, yroom, ypax, yrate, yrev, from_bez, to_bez, inactive, mtd_act, mtd_totrm, ytd_act, ytd_totrm, ncompli, mtd_ncompli, ytd_ncompli, dcompli, mcompli, ycompli, dhu, mhu, yhu, ci_date, htparam, zimmer, zkstat, zinrstat, genstat, segment, guestseg, reservation, res_line, outorder, artikel, umsatz
        nonlocal bgenstat


        nonlocal cl_list, bgenstat
        nonlocal cl_list_list

        i:int = 0
        datum:date = None
        black_list:int = 0

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 709)).first()
        black_list = htparam.finteger
        cl_list_list.clear()
        droom = 0
        mroom = 0
        yroom = 0
        dpax = 0
        mpax = 0
        ypax = 0
        drev = 0
        mrev = 0
        yrev = 0
        tot_room = 0
        inactive = 0
        mtd_act = 0
        ytd_act = 0
        mtd_totrm = 0
        ytd_totrm = 0

        for zimmer in db_session.query(Zimmer).filter(
                (not sleeping)).all():
            inactive = inactive + 1

        if to_date < ci_date:

            for zkstat in db_session.query(Zkstat).filter(
                    (Zkstat.datum == to_date)).all():
                tot_room = tot_room + zkstat.anz100
        else:

            for zimmer in db_session.query(Zimmer).filter(
                    (sleeping)).all():
                tot_room = tot_room + 1
        count_mtd_totrm()

        if not segmtype_exist:
            cal_umsatz1(1, 12, 15, 49, translateExtended ("Room Revenue", lvcarea, ""), "", True)
            cal_umsatz1(13, 14, 0, 0, translateExtended ("Total Room Occ", lvcarea, ""), translateExtended ("Double Occupancy", lvcarea, ""), False)
        else:
            cal_umsatz1a(0, 0, translateExtended ("Room Revenue", lvcarea, ""), "", True)
            cal_umsatz1b(1, 2, translateExtended ("Total Room Occ", lvcarea, ""), translateExtended ("Double Occupancy", lvcarea, ""), False)
        cal_umsatz2()
        cal_umsatz3()
        no_show()

    def count_mtd_totrm1():

        nonlocal cl_list_list, lvcarea, do_it, droomrev, mroomrev, yroomrev, droomexc, mroomexc, yroomexc, tot_room, all_room, dvacant, dooo, mvacant, mooo, yvacant, yooo, dnoshow, dcancel, mnoshow, mcancel, ynoshow, ycancel, droom, proz1, mroom, proz2, dpax, mpax, drate, mrate, drev, mrev, yroom, ypax, yrate, yrev, from_bez, to_bez, inactive, mtd_act, mtd_totrm, ytd_act, ytd_totrm, ncompli, mtd_ncompli, ytd_ncompli, dcompli, mcompli, ycompli, dhu, mhu, yhu, ci_date, htparam, zimmer, zkstat, zinrstat, genstat, segment, guestseg, reservation, res_line, outorder, artikel, umsatz
        nonlocal bgenstat


        nonlocal cl_list, bgenstat
        nonlocal cl_list_list

        datum:date = None
        tot1:int = 0
        glob_tot:int = 0
        mtd_totrm = 0 mtd_act == 0 ytd_act == 0 ytd_totrm == 0

        for zimmer in db_session.query(Zimmer).filter(
                (Zimmer.sleeping)).all():
            glob_tot = glob_tot + 1
        for datum in range(from_date,to_date + 1) :
            tot1 = 0

            for zimmer in db_session.query(Zimmer).filter(
                    (Zimmer.sleeping)).all():
                tot1 = tot1 + 1

            if tot1 == 0:
                tot1 = glob_tot

            if (mi_mtd_chk and get_month(datum) == get_month(to_date)) or (mi_ftd_chk and datum >= fdate and datum <= tdate):
                mtd_act = mtd_act + tot1
            ytd_act = ytd_act + tot1

            for zimmer in db_session.query(Zimmer).all():

                if (mi_mtd_chk and get_month(datum) == get_month(to_date)) or (mi_ftd_chk and datum >= fdate and datum <= tdate):
                    mtd_totrm = mtd_totrm + 1
                ytd_totrm = ytd_totrm + 1

    def count_mtd_totrm():

        nonlocal cl_list_list, lvcarea, do_it, droomrev, mroomrev, yroomrev, droomexc, mroomexc, yroomexc, tot_room, all_room, dvacant, dooo, mvacant, mooo, yvacant, yooo, dnoshow, dcancel, mnoshow, mcancel, ynoshow, ycancel, droom, proz1, mroom, proz2, dpax, mpax, drate, mrate, drev, mrev, yroom, ypax, yrate, yrev, from_bez, to_bez, inactive, mtd_act, mtd_totrm, ytd_act, ytd_totrm, ncompli, mtd_ncompli, ytd_ncompli, dcompli, mcompli, ycompli, dhu, mhu, yhu, ci_date, htparam, zimmer, zkstat, zinrstat, genstat, segment, guestseg, reservation, res_line, outorder, artikel, umsatz
        nonlocal bgenstat


        nonlocal cl_list, bgenstat
        nonlocal cl_list_list

        datum:date = None
        tot1:int = 0
        glob_tot:int = 0
        mtd_totrm = 0 mtd_act == 0 ytd_act == 0 ytd_totrm == 0

        for zimmer in db_session.query(Zimmer).filter(
                (Zimmer.sleeping)).all():
            glob_tot = glob_tot + 1
        for datum in range(from_date,to_date + 1) :
            tot1 = 0

            for zkstat in db_session.query(Zkstat).filter(
                    (Zkstat.datum == datum)).all():
                tot1 = tot1 + zkstat.anz100

            if tot1 == 0:
                tot1 = glob_tot

            if (mi_mtd_chk and get_month(datum) == get_month(to_date)) or (mi_ftd_chk and datum >= fdate and datum <= tdate):
                mtd_act = mtd_act + tot1
            ytd_act = ytd_act + tot1

            zinrstat = db_session.query(Zinrstat).filter(
                    (func.lower(Zinrstat.zinr) == "tot_rm") &  (Zinrstat.datum == datum)).first()

            if zinrstat:

                if (mi_mtd_chk and get_month(datum) == get_month(to_date)) or (mi_ftd_chk and datum >= fdate and datum <= tdate):
                    mtd_totrm = mtd_totrm + zinrstat.zimmeranz
                ytd_totrm = ytd_totrm + zinrstat.zimmeranz
            else:

                if (mi_mtd_chk and get_month(datum) == get_month(to_date)) or (mi_ftd_chk and datum >= fdate and datum <= tdate):
                    mtd_totrm = mtd_totrm + glob_tot + inactive
                ytd_totrm = ytd_totrm + glob_tot + inactive

    def cal_umsatz1(i1:int, i2:int, i3:int, i4:int, rev_title:str, rev_title1:str, show_avrg:bool):

        nonlocal cl_list_list, lvcarea, do_it, droomrev, mroomrev, yroomrev, droomexc, mroomexc, yroomexc, tot_room, all_room, dvacant, dooo, mvacant, mooo, yvacant, yooo, dnoshow, dcancel, mnoshow, mcancel, ynoshow, ycancel, droom, proz1, mroom, proz2, dpax, mpax, drate, mrate, drev, mrev, yroom, ypax, yrate, yrev, from_bez, to_bez, inactive, mtd_act, mtd_totrm, ytd_act, ytd_totrm, ncompli, mtd_ncompli, ytd_ncompli, dcompli, mcompli, ycompli, dhu, mhu, yhu, ci_date, htparam, zimmer, zkstat, zinrstat, genstat, segment, guestseg, reservation, res_line, outorder, artikel, umsatz
        nonlocal bgenstat


        nonlocal cl_list, bgenstat
        nonlocal cl_list_list

        i:int = 0
        datum:date = None
        do_it1:bool = False
        d1:date = None
        d2:date = None
        datum0:date = None
        datum1:date = None
        datum2:date = None
        curr_i:int = 0
        net_lodg:decimal = 0
        fnet_lodg:decimal = 0
        tot_breakfast:decimal = 0
        tot_lunch:decimal = 0
        tot_dinner:decimal = 0
        tot_other:decimal = 0
        tot_rmrev:decimal = 0
        tot_vat:decimal = 0
        tot_service:decimal = 0
        Bgenstat = Genstat
        d1 = from_date

        if to_date < (ci_date - 1):
            d2 = to_date
        else:
            d2 = ci_date - 1

        for segment in db_session.query(Segment).filter(
                (((Segmentcode >= i1) &  (Segmentcode <= i2)) |  ((Segmentcode >= i3) &  (Segmentcode <= i4)))).all():

            bgenstat = db_session.query(Bgenstat).filter(
                    (Bgenstat.segmentcode == segmentcode) &  (Bgenstat.datum >= d1) &  (Bgenstat.datum <= d2) &  (Bgenstat.resstatus != 13) &  (Bgenstat.gratis == 0) &  (Bgenstat.segmentcode != 0) &  (Bgenstat.nationnr != 0) &  (Bgenstat.zinr != "") &  (Bgenstat.res_logic[1])).first()

            if bgenstat:
                do_it1 = True


            else:

                if re.match(".*\$\$0",segment.bezeich):
                    do_it1 = False


                else:
                    do_it1 = True

            if do_it1:
                cl_list = Cl_list()
                cl_list_list.append(cl_list)

                cl_list.segm = segmentcode
                cl_list.bezeich = entry(0, segment.bezeich, "$$0")

                for genstat in db_session.query(Genstat).filter(
                        (Genstat.segmentcode == segmentcode) &  (Genstat.datum >= d1) &  (Genstat.datum <= d2) &  (Genstat.resstatus != 13) &  (Genstat.gratis == 0) &  (Genstat.segmentcode != 0) &  (Genstat.nationnr != 0) &  (Genstat.zinr != "") &  (Genstat.res_logic[1])).all():

                    if genstat.res_date[0] < genstat.datum and genstat.res_date[1] == genstat.datum and genstat.resstatus == 8:
                        1
                    else:

                        if genstat.datum == to_date:
                            droom = droom + 1
                            cl_list.droom = cl_list.droom + 1
                            cl_list.dpax = cl_list.dpax + genstat.erwachs + genstat.kind1 + genstat.kind2 + genstat.gratis
                            cl_list.drev = cl_list.drev + genstat.logis
                            drev = drev + genstat.logis

                        if (mi_mtd_chk and get_month(genstat.datum) == get_month(d2)) or (mi_ftd_chk and genstat.datum >= d1 and genstat.datum <= d2):
                            cl_list.mroom = cl_list.mroom + 1
                            cl_list.mpax = cl_list.mpax + genstat.erwachs + genstat.kind1 + genstat.kind2 + genstat.gratis
                            cl_list.mrev = cl_list.mrev + genstat.logis
                            mroom = mroom + 1
                            mpax = mpax + genstat.erwachs + genstat.kind1 + genstat.kind2 + genstat.gratis
                            mrev = mrev + genstat.logis
                        cl_list.yroom = cl_list.yroom + 1
                        cl_list.ypax = cl_list.ypax + genstat.erwachs +\
                                genstat.kind1 + genstat.kind2 + genstat.gratis
                        cl_list.yrev = cl_list.yrev + genstat.logis
                        yroom = yroom + 1
                        ypax = ypax + genstat.gratis
                        yrev = yrev + genstat.logis

        if do_it:

            for genstat in db_session.query(Genstat).filter(
                    (Genstat.datum >= d1) &  (Genstat.datum <= d2) &  (Genstat.segmentcode != 0) &  (Genstat.nationnr != 0) &  (Genstat.zinr != "") &  (Genstat.resstatus != 13) &  (Genstat.res_logic[1])).all():

                segment = db_session.query(Segment).filter(
                        (Segment.segmentcode == genstat.segmentcode)).first()

                if segment:

                    cl_list = query(cl_list_list, filters=(lambda cl_list :cl_list.segm == segmentcode), first=True)

                    if cl_list:

                        if genstat.datum == to_date:
                            cl_list.drev = cl_list.drev + genstat.res_deci[0]
                            drev = drev + genstat.logis

                        if (mi_mtd_chk and get_month(genstat.datum) == get_month(d2)) or (mi_ftd_chk and genstat.datum >= d1 and genstat.datum <= d2):
                            cl_list.mrev = cl_list.mrev + genstat.res_deci[0]
                            mrev = mrev + genstat.logis
                else:

                    guestseg = db_session.query(Guestseg).filter(
                            (Guestseg.gastnr == genstat.gastnr)).first()

                    if guestseg:

                        if guestseg.reihenfolge == 1:

                            cl_list = query(cl_list_list, filters=(lambda cl_list :cl_list.segm == segmentcode), first=True)

                            if cl_list:

                                if genstat.datum == to_date:
                                    cl_list.drev = cl_list.drev + genstat.res_deci[0]
                                    drev = drev + genstat.logis

                                if (mi_mtd_chk and get_month(genstat.datum) == get_month(d2)) or (mi_ftd_chk and genstat.datum >= d1 and genstat.datum <= d2):
                                    cl_list.mrev = cl_list.mrev + genstat.res_deci[0]
                                    mrev = mrev + genstat.logis
                        else:

                            guestseg = db_session.query(Guestseg).filter(
                                    (Guestseg.reihenfolge == 0)).first()

                            if guestseg:

                                cl_list = query(cl_list_list, filters=(lambda cl_list :cl_list.segm == guestseg.segmentcode), first=True)

                                if cl_list:

                                    if genstat.datum == to_date:
                                        cl_list.drev = cl_list.drev + genstat.res_deci[0]
                                        drev = drev + genstat.logis

                                    if (mi_mtd_chk and get_month(genstat.datum) == get_month(d2)) or (mi_ftd_chk and genstat.datum >= d1 and genstat.datum <= d2):
                                        cl_list.mrev = cl_list.mrev + genstat.res_deci[0]
                                        mrev = mrev + genstat.logis
                    else:

                        segment = db_session.query(Segment).first()

                        if segment:

                            cl_list = query(cl_list_list, filters=(lambda cl_list :cl_list.segm == segmentcode), first=True)

                            if cl_list:

                                if genstat.datum == to_date:
                                    cl_list.drev = cl_list.drev + genstat.res_deci[0]
                                    drev = drev + genstat.logis

                                if (mi_mtd_chk and get_month(genstat.datum) == get_month(d2)) or (mi_ftd_chk and genstat.datum >= d1 and genstat.datum <= d2):
                                    cl_list.mrev = cl_list.mrev + genstat.res_deci[0]
                                    mrev = mrev + genstat.logis

        if to_date >= ci_date:
            d2 = d2 + 1

            res_line_obj_list = []
            for res_line, reservation in db_session.query(Res_line, Reservation).join(Reservation,(Reservation.resnr == Res_line.resnr)).filter(
                    (((Res_line.resstatus <= 13) &  (Res_line.resstatus != 4) &  (Res_line.resstatus != 8) &  (Res_line.resstatus != 9) &  (Res_line.resstatus != 10) &  (Res_line.resstatus != 12) &  (Res_line.active_flag <= 1) &  (not (Res_line.ankunft > to_date)) &  (not (Res_line.abreise < d2)))) |  ((Res_line.resstatus == 8) &  (Res_line.active_flag == 2) &  (Res_line.ankunft == ci_date) &  (Res_line.abreise == ci_date)) &  (Res_line.gastnr > 0) &  (Res_line.l_zuordnung[2] == 0)).all():
                if res_line._recid in res_line_obj_list:
                    continue
                else:
                    res_line_obj_list.append(res_line._recid)


                curr_i = 0

                if res_line.kontignr < 0:
                    do_it1 = True

                    cl_list = query(cl_list_list, filters=(lambda cl_list :cl_list.segm == reservation.segmentcode), first=True)

                    if not cl_list:

                        segment = db_session.query(Segment).filter(
                                (Segment.segmentcode == reservation.segmentcode)).first()

                        if segment and not re.match(".*\$\$0",segment.bezeich):
                            cl_list = Cl_list()
                            cl_list_list.append(cl_list)

                            cl_list.segm = segmentcode
                            cl_list.bezeich = segment.bezeich
                        else:
                            do_it1 = False

                    if do_it1 :
                        datum1 = d2

                        if res_line.ankunft > datum1:
                            datum1 = res_line.ankunft
                        datum2 = to_date

                        if res_line.abreise < datum2:
                            datum2 = res_line.abreise
                        for datum0 in range(datum1,datum2 + 1) :
                            curr_i = curr_i + 1

                            if datum0 == res_line.abreise:
                                1
                            else:
                                net_lodg = 0
                                tot_breakfast = 0
                                tot_lunch = 0
                                tot_dinner = 0
                                tot_other = 0


                                fnet_lodg, net_lodg, tot_breakfast, tot_lunch, tot_dinner, tot_other, tot_rmrev, tot_vat, tot_service = get_output(get_room_breakdown(res_line._recid, datum0, curr_i, from_date))

                                if datum0 == to_date:
                                    droom = droom + res_line.zimmeranz
                                    cl_list.droom = cl_list.droom + res_line.zimmeranz
                                    cl_list.dpax = cl_list.dpax + res_line.erwachs + res_line.kind1 +\
                                            res_line.kind2 + res_line.gratis
                                    cl_list.drev = cl_list.drev + net_lodg
                                    drev = drev + net_lodg

                                if (mi_mtd_chk and get_month(datum0) == get_month(to_date)) or (mi_ftd_chk and datum0 >= d2 and datum0 <= tdate):
                                    cl_list.mroom = cl_list.mroom + res_line.zimmeranz
                                    cl_list.mpax = cl_list.mpax + res_line.erwachs + res_line.kind1 +\
                                            res_line.kind2 + res_line.gratis
                                    cl_list.mrev = cl_list.mrev + net_lodg
                                    mroom = mroom + res_line.zimmeranz
                                    mpax = mpax + res_line.erwachs + res_line.kind1 +\
                                            res_line.kind2 + res_line.gratis
                                    mrev = mrev + net_lodg


                                cl_list.yroom = cl_list.yroom + res_line.zimmeranz
                                cl_list.ypax = cl_list.ypax + res_line.erwachs + res_line.kind1 +\
                                        res_line.kind2 + res_line.gratis
                                cl_list.yrev = cl_list.yrev + net_lodg
                                yroom = yroom + res_line.zimmeranz
                                ypax = ypax + res_line.erwachs + res_line.kind1 +\
                                        res_line.kind2 + res_line.gratis
                                yrev = yrev + net_lodg

        for cl_list in query(cl_list_list, filters=(lambda cl_list :((cl_list.segm >= i1 and cl_list.segm <= i2) or (cl_list.segm >= i3 and cl_list.segm <= i4)))):

            if cl_list.droom != 0:
                cl_list.drate = cl_list.drev / cl_list.droom

            if cl_list.mroom != 0:
                cl_list.mrate = cl_list.mrev / cl_list.mroom

            if cl_list.yroom != 0:
                cl_list.yrate = cl_list.yrev / cl_list.yroom
            cl_list.proz1 = 100.0 * cl_list.droom / tot_room
            cl_list.proz2 = 100.0 * cl_list.mroom / mtd_act
            cl_list.proz3 = 100.0 * cl_list.yroom / ytd_act

            if droom != 0:
                drate = drev / droom

            if mroom != 0:
                mrate = mrev / mroom

            if yroom != 0:
                yrate = yrev / yroom

            if cl_list.proz1 == None:
                cl_list.proz1 = 0

            if cl_list.proz2 == None:
                cl_list.proz2 = 0

            if cl_list.proz3 == None:
                cl_list.proz3 = 0
            dpax = dpax + cl_list.dpax

            if cl_list.drev == 0 and cl_list.mrev == 0 and cl_list.yrev == 0:
                cl_list.zero_flag = True
        cl_list = Cl_list()
        cl_list_list.append(cl_list)

        cl_list = Cl_list()
        cl_list_list.append(cl_list)

        cl_list.bezeich = rev_title
        cl_list.droom = droom
        cl_list.proz1 = droom / tot_room * 100
        cl_list.mroom = mroom
        cl_list.proz2 = mroom / mtd_act * 100
        cl_list.dpax = dpax
        cl_list.mpax = mpax
        cl_list.yroom = yroom
        cl_list.ypax = ypax
        cl_list.proz3 = yroom / ytd_act * 100
        cl_list.drev = drev
        cl_list.mrev = mrev
        cl_list.yrev = yrev

        if show_avrg:

            if droom != 0:
                cl_list.drate = drev / droom
            else:
                cl_list.drate = 0

            if mroom != 0:
                cl_list.mrate = mrev / mroom
            else:
                cl_list.mrate = 0

            if yroom != 0:
                cl_list.yrate = yrev / yroom
            else:
                cl_list.yrate = 0

        if rev_title1 != "":
            cl_list = Cl_list()
            cl_list_list.append(cl_list)

            cl_list.bezeich = rev_title1

            if droom != 0:
                cl_list.proz1 = (dpax - droom) / droom * 100
            else:
                cl_list.proz1 = 0

            if mroom != 0:
                cl_list.proz2 = (mpax - mroom) / mroom * 100
            else:
                cl_list.proz2 = 0

            if yroom != 0:
                cl_list.proz3 = (ypax - yroom) / yroom * 100
            else:
                cl_list.proz3 = 0
        cl_list = Cl_list()
        cl_list_list.append(cl_list)


    def cal_umsatz1a(i1:int, i2:int, rev_title:str, rev_title1:str, show_avrg:bool):

        nonlocal cl_list_list, lvcarea, do_it, droomrev, mroomrev, yroomrev, droomexc, mroomexc, yroomexc, tot_room, all_room, dvacant, dooo, mvacant, mooo, yvacant, yooo, dnoshow, dcancel, mnoshow, mcancel, ynoshow, ycancel, droom, proz1, mroom, proz2, dpax, mpax, drate, mrate, drev, mrev, yroom, ypax, yrate, yrev, from_bez, to_bez, inactive, mtd_act, mtd_totrm, ytd_act, ytd_totrm, ncompli, mtd_ncompli, ytd_ncompli, dcompli, mcompli, ycompli, dhu, mhu, yhu, ci_date, htparam, zimmer, zkstat, zinrstat, genstat, segment, guestseg, reservation, res_line, outorder, artikel, umsatz
        nonlocal bgenstat


        nonlocal cl_list, bgenstat
        nonlocal cl_list_list

        i:int = 0
        tot_proz3:decimal = 0
        inact:bool = False
        do_it1:bool = False
        d1:date = None
        d2:date = None
        datum0:date = None
        datum1:date = None
        datum2:date = None
        curr_i:int = 0
        net_lodg:decimal = 0
        fnet_lodg:decimal = 0
        tot_breakfast:decimal = 0
        tot_lunch:decimal = 0
        tot_dinner:decimal = 0
        tot_other:decimal = 0
        tot_rmrev:decimal = 0
        tot_vat:decimal = 0
        tot_service:decimal = 0
        Bgenstat = Genstat
        d1 = from_date

        if to_date < (ci_date - 1):
            d2 = to_date
        else:
            d2 = ci_date - 1

        for segment in db_session.query(Segment).filter(
                (Segment.betriebsnr == 0)).all():

            bgenstat = db_session.query(Bgenstat).filter(
                    (Bgenstat.segmentcode == segmentcode) &  (Bgenstat.datum >= d1) &  (Bgenstat.datum <= d2) &  (Bgenstat.resstatus != 13) &  (Bgenstat.gratis == 0) &  (Bgenstat.segmentcode != 0) &  (Bgenstat.nationnr != 0) &  (Bgenstat.zinr != "") &  (Bgenstat.res_logic[1])).first()

            if bgenstat:
                do_it1 = True


            else:

                if re.match(".*\$\$0",segment.bezeich):
                    do_it1 = False


                else:
                    do_it1 = True

            if do_it1:
                cl_list = Cl_list()
                cl_list_list.append(cl_list)

                cl_list.segm = segmentcode
                cl_list.bezeich = entry(0, segment.bezeich, "$$0")
                cl_list.betriebsnr = segment.betriebsnr
                cl_list.drev = 0

                for genstat in db_session.query(Genstat).filter(
                        (Genstat.segmentcode == segmentcode) &  (Genstat.datum >= d1) &  (Genstat.datum <= d2) &  (Genstat.resstatus != 13) &  (Genstat.gratis == 0) &  (Genstat.segmentcode != 0) &  (Genstat.nationnr != 0) &  (Genstat.zinr != "") &  (Genstat.res_logic[1])).all():
                    inact = True

                    if genstat.res_date[0] < genstat.datum and genstat.res_date[1] == genstat.datum and genstat.resstatus == 8:
                        1
                    else:

                        if genstat.datum == to_date:
                            droom = droom + 1
                            cl_list.droom = cl_list.droom + 1
                            cl_list.dpax = cl_list.dpax + genstat.erwachs + genstat.kind1 +\
                                    genstat.kind2
                            cl_list.drev = cl_list.drev + genstat.logis
                            drev = drev + genstat.logis

                        if (mi_mtd_chk and get_month(genstat.datum) == get_month(d2)) or (mi_ftd_chk and genstat.datum >= d1 and genstat.datum <= d2):
                            cl_list.mroom = cl_list.mroom + 1
                            cl_list.mpax = cl_list.mpax + genstat.erwachs +\
                                    genstat.kind1 + genstat.kind2


                            cl_list.mrev = cl_list.mrev + genstat.logis
                            mroom = mroom + 1
                            mpax = mpax + genstat.erwachs + genstat.kind1 + genstat.kind2
                            mrev = mrev + genstat.logis
                        cl_list.yroom = cl_list.yroom + 1


                        cl_list.ypax = cl_list.ypax + genstat.erwachs + genstat.kind1 + genstat.kind2
                        cl_list.yrev = cl_list.yrev + genstat.logis
                        yroom = yroom + 1
                        ypax = ypax + genstat.erwachs + genstat.kind1 + genstat.kind2
                        yrev = yrev + genstat.logis

        if do_it:

            for genstat in db_session.query(Genstat).filter(
                    (Genstat.datum >= d1) &  (Genstat.datum <= d2) &  (Genstat.segmentcode != 0) &  (Genstat.nationnr != 0) &  (Genstat.zinr != "") &  (Genstat.resstatus != 13) &  (Genstat.res_logic[1])).all():

                segment = db_session.query(Segment).filter(
                        (Segment.segmentcode == genstat.segmentcode)).first()

                if segment:

                    cl_list = query(cl_list_list, filters=(lambda cl_list :cl_list.segm == segmentcode), first=True)

                    if cl_list:

                        if genstat.datum == to_date:
                            cl_list.drev = cl_list.drev + genstat.res_deci[0]
                            drev = drev + genstat.res_deci[0]

                        if (mi_mtd_chk and get_month(genstat.datum) == get_month(d2)) or (mi_ftd_chk and genstat.datum >= d1 and genstat.datum <= d2):
                            cl_list.mrev = cl_list.mrev + genstat.res_deci[0]
                            mrev = mrev + genstat.res_deci[0]


                else:

                    guestseg = db_session.query(Guestseg).filter(
                            (Guestseg.gastnr == genstat.gastnr)).first()

                    if guestseg:

                        if guestseg.reihenfolge == 1:

                            cl_list = query(cl_list_list, filters=(lambda cl_list :cl_list.segm == segmentcode), first=True)

                            if cl_list:

                                if genstat.datum == to_date:
                                    cl_list.drev = cl_list.drev + genstat.res_deci[0]
                                    drev = drev + genstat.res_deci[0]

                                if (mi_mtd_chk and get_month(genstat.datum) == get_month(d2)) or (mi_ftd_chk and genstat.datum >= d1 and genstat.datum <= d2):
                                    cl_list.mrev = cl_list.mrev + genstat.res_deci[0]
                                    mrev = mrev + genstat.res_deci[0]


                        else:

                            guestseg = db_session.query(Guestseg).filter(
                                    (Guestseg.reihenfolge == 0)).first()

                            if guestseg:

                                cl_list = query(cl_list_list, filters=(lambda cl_list :cl_list.segm == guestseg.segmentcode), first=True)

                                if cl_list:

                                    if genstat.datum == to_date:
                                        cl_list.drev = cl_list.drev + genstat.res_deci[0]
                                        drev = drev + genstat.res_deci[0]

                                    if (mi_mtd_chk and get_month(genstat.datum) == get_month(d2)) or (mi_ftd_chk and genstat.datum >= d1 and genstat.datum <= d2):
                                        cl_list.mrev = cl_list.mrev + genstat.res_deci[0]
                                        mrev = mrev + genstat.res_deci[0]


                    else:

                        segment = db_session.query(Segment).first()

                        if segment:

                            cl_list = query(cl_list_list, filters=(lambda cl_list :cl_list.segm == segmentcode), first=True)

                            if cl_list:

                                if genstat.datum == to_date:
                                    cl_list.drev = cl_list.drev + genstat.res_deci[0]
                                    drev = drev + genstat.res_deci[0]

                                if (mi_mtd_chk and get_month(genstat.datum) == get_month(d2)) or (mi_ftd_chk and genstat.datum >= d1 and genstat.datum <= d2):
                                    cl_list.mrev = cl_list.mrev + genstat.res_deci[0]
                                    mrev = mrev + genstat.res_deci[0]

        if to_date >= ci_date:
            d2 = d2 + 1

            res_line_obj_list = []
            for res_line, reservation in db_session.query(Res_line, Reservation).join(Reservation,(Reservation.resnr == Res_line.resnr)).filter(
                    (((Res_line.resstatus <= 13) &  (Res_line.resstatus != 4) &  (Res_line.resstatus != 8) &  (Res_line.resstatus != 9) &  (Res_line.resstatus != 10) &  (Res_line.resstatus != 12) &  (Res_line.active_flag <= 1) &  (not (Res_line.ankunft > to_date)) &  (not (Res_line.abreise < d2)))) |  ((Res_line.resstatus == 8) &  (Res_line.active_flag == 2) &  (Res_line.ankunft == ci_date) &  (Res_line.abreise == ci_date)) &  (Res_line.gastnr > 0) &  (Res_line.l_zuordnung[2] == 0)).all():
                if res_line._recid in res_line_obj_list:
                    continue
                else:
                    res_line_obj_list.append(res_line._recid)


                curr_i = 0

                if res_line.kontignr < 0:
                    do_it1 = True

                    cl_list = query(cl_list_list, filters=(lambda cl_list :cl_list.segm == reservation.segmentcode), first=True)

                    if not cl_list:

                        segment = db_session.query(Segment).filter(
                                (Segment.segmentcode == reservation.segmentcode)).first()

                        if segment and not re.match(".*\$\$0",segment.bezeich):
                            cl_list = Cl_list()
                            cl_list_list.append(cl_list)

                            cl_list.segm = segmentcode
                            cl_list.bezeich = segment.bezeich
                        else:
                            do_it1 = False

                    if do_it1 :
                        datum1 = d2

                        if res_line.ankunft > datum1:
                            datum1 = res_line.ankunft
                        datum2 = to_date

                        if res_line.abreise < datum2:
                            datum2 = res_line.abreise
                        for datum0 in range(datum1,datum2 + 1) :
                            curr_i = curr_i + 1

                            if datum0 == res_line.abreise:
                                1
                            else:
                                net_lodg = 0
                                tot_breakfast = 0
                                tot_lunch = 0
                                tot_dinner = 0
                                tot_other = 0


                                fnet_lodg, net_lodg, tot_breakfast, tot_lunch, tot_dinner, tot_other, tot_rmrev, tot_vat, tot_service = get_output(get_room_breakdown(res_line._recid, datum0, curr_i, from_date))

                                if datum0 == to_date:
                                    droom = droom + res_line.zimmeranz
                                    cl_list.droom = cl_list.droom + res_line.zimmeranz
                                    cl_list.dpax = cl_list.dpax + res_line.erwachs + res_line.kind1 +\
                                            res_line.kind2 + res_line.gratis
                                    cl_list.drev = cl_list.drev + net_lodg
                                    drev = drev + net_lodg

                                if (mi_mtd_chk and get_month(datum0) == get_month(to_date)) or (mi_ftd_chk and datum0 >= d2 and datum0 <= tdate):
                                    cl_list.mroom = cl_list.mroom + res_line.zimmeranz
                                    cl_list.mpax = cl_list.mpax + res_line.erwachs + res_line.kind1 +\
                                            res_line.kind2 + res_line.gratis
                                    cl_list.mrev = cl_list.mrev + net_lodg
                                    mroom = mroom + res_line.zimmeranz
                                    mpax = mpax + res_line.erwachs + res_line.kind1 +\
                                            res_line.kind2 + res_line.gratis
                                    mrev = mrev + net_lodg


                                cl_list.yroom = cl_list.yroom + res_line.zimmeranz
                                cl_list.ypax = cl_list.ypax + res_line.erwachs + res_line.kind1 +\
                                        res_line.kind2 + res_line.gratis
                                cl_list.yrev = cl_list.yrev + net_lodg
                                yroom = yroom + res_line.zimmeranz
                                ypax = ypax + res_line.erwachs + res_line.kind1 +\
                                        res_line.kind2 + res_line.gratis
                                yrev = yrev + net_lodg

        if inact:

            for cl_list in query(cl_list_list, filters=(lambda cl_list :(cl_list.betriebsnr >= i1 and cl_list.betriebsnr <= i2))):

                if cl_list.droom != 0:
                    cl_list.drate = cl_list.drev / cl_list.droom

                if cl_list.mroom != 0:
                    cl_list.mrate = cl_list.mrev / cl_list.mroom

                if cl_list.yroom != 0:
                    cl_list.yrate = cl_list.yrev / cl_list.yroom
                cl_list.proz1 = 100.0 * cl_list.droom / tot_room
                cl_list.proz2 = 100.0 * cl_list.mroom / mtd_act
                cl_list.proz3 = 100.0 * cl_list.yroom / ytd_act

                if droom != 0:
                    drate = drev / droom

                if mroom != 0:
                    mrate = mrev / mroom

                if yroom != 0:
                    yrate = yrev / yroom

                if cl_list.proz1 == None:
                    cl_list.proz1 = 0

                if cl_list.proz2 == None:
                    cl_list.proz2 = 0

                if cl_list.proz3 == None:
                    cl_list.proz3 = 0
                tot_proz3 = tot_proz3 + cl_list.proz3


                dpax = dpax + cl_list.dpax

                if cl_list.drev == 0 and cl_list.mrev == 0 and cl_list.yrev == 0:
                    cl_list.zero_flag = True
            cl_list = Cl_list()
            cl_list_list.append(cl_list)

        droomexc = droom
        mroomexc = mroom
        yroomexc = yroom
        droomrev = droomexc
        mroomrev = mroomexc
        yroomrev = yroomexc


        cl_list = Cl_list()
        cl_list_list.append(cl_list)

        cl_list = Cl_list()
        cl_list_list.append(cl_list)

        cl_list.bezeich = rev_title
        cl_list.droom = droom
        cl_list.proz1 = droom / tot_room * 100
        cl_list.mroom = mroom
        cl_list.proz2 = mroom / mtd_act * 100
        cl_list.dpax = dpax
        cl_list.mpax = mpax
        cl_list.yroom = yroom
        cl_list.ypax = ypax
        cl_list.proz3 = tot_proz3
        cl_list.drev = drev
        cl_list.mrev = mrev
        cl_list.yrev = yrev

        if show_avrg:

            if droom != 0:
                cl_list.drate = drev / droom
            else:
                cl_list.drate = 0

            if mroom != 0:
                cl_list.mrate = mrev / mroom
            else:
                cl_list.mrate = 0

            if yroom != 0:
                cl_list.yrate = yrev / yroom
            else:
                cl_list.yrate = 0

        if rev_title1 != "":
            cl_list = Cl_list()
            cl_list_list.append(cl_list)

            cl_list.bezeich = rev_title1

            if droom != 0:
                cl_list.proz1 = (dpax - droom) / droom * 100
            else:
                cl_list.proz1 = 0

            if mroom != 0:
                cl_list.proz2 = (mpax - mroom) / mroom * 100
            else:
                cl_list.proz2 = 0

            if yroom != 0:
                cl_list.proz3 = (ypax - yroom) / yroom * 100
            else:
                cl_list.proz3 = 0
        cl_list = Cl_list()
        cl_list_list.append(cl_list)


    def cal_umsatz1b(i1:int, i2:int, rev_title:str, rev_title1:str, show_avrg:bool):

        nonlocal cl_list_list, lvcarea, do_it, droomrev, mroomrev, yroomrev, droomexc, mroomexc, yroomexc, tot_room, all_room, dvacant, dooo, mvacant, mooo, yvacant, yooo, dnoshow, dcancel, mnoshow, mcancel, ynoshow, ycancel, droom, proz1, mroom, proz2, dpax, mpax, drate, mrate, drev, mrev, yroom, ypax, yrate, yrev, from_bez, to_bez, inactive, mtd_act, mtd_totrm, ytd_act, ytd_totrm, ncompli, mtd_ncompli, ytd_ncompli, dcompli, mcompli, ycompli, dhu, mhu, yhu, ci_date, htparam, zimmer, zkstat, zinrstat, genstat, segment, guestseg, reservation, res_line, outorder, artikel, umsatz
        nonlocal bgenstat


        nonlocal cl_list, bgenstat
        nonlocal cl_list_list

        i:int = 0
        datum:date = None
        inact:bool = False
        do_it1:bool = False
        d1:date = None
        d2:date = None
        datum0:date = None
        datum1:date = None
        datum2:date = None
        curr_i:int = 0
        net_lodg:decimal = 0
        fnet_lodg:decimal = 0
        tot_breakfast:decimal = 0
        tot_lunch:decimal = 0
        tot_dinner:decimal = 0
        tot_other:decimal = 0
        tot_rmrev:decimal = 0
        tot_vat:decimal = 0
        tot_service:decimal = 0
        Bgenstat = Genstat
        d1 = from_date

        if to_date < (ci_date - 1):
            d2 = to_date
        else:
            d2 = ci_date - 1

        for segment in db_session.query(Segment).all():

            bgenstat = db_session.query(Bgenstat).filter(
                    (Bgenstat.segmentcode == segmentcode) &  (Bgenstat.datum >= d1) &  (Bgenstat.datum <= d2) &  (Bgenstat.resstatus != 13) &  (Bgenstat.gratis != 0) &  (Bgenstat.segmentcode != 0) &  (Bgenstat.nationnr != 0) &  (Bgenstat.zinr != "") &  (Bgenstat.res_logic[1])).first()

            if bgenstat:
                do_it1 = True


            else:

                if re.match(".*\$\$0",segment.bezeich):
                    do_it1 = False


                else:
                    do_it1 = True

            if do_it1:

                for genstat in db_session.query(Genstat).filter(
                        (Genstat.segmentcode == segmentcode) &  (Genstat.datum >= d1) &  (Genstat.datum <= d2) &  (Genstat.resstatus != 13) &  (Genstat.gratis != 0) &  (Genstat.segmentcode != 0) &  (Genstat.nationnr != 0) &  (Genstat.zinr != "") &  (Genstat.res_logic[1])).all():
                    inact = True

                    cl_list = query(cl_list_list, filters=(lambda cl_list :cl_list.segm == segmentcode and cl_list.compli), first=True)

                    if not cl_list:
                        cl_list = Cl_list()
                        cl_list_list.append(cl_list)

                        cl_list.compli = True
                        cl_list.segm = segmentcode
                        cl_list.bezeich = entry(0, segment.bezeich, "$$0")
                        cl_list.betriebsnr = segment.betriebsnr

                    if genstat.res_date[0] < genstat.datum and genstat.res_date[1] == genstat.datum and genstat.resstatus == 8:
                        1
                    else:

                        if genstat.datum == to_date:
                            droom = droom + 1
                            cl_list.droom = cl_list.droom + 1
                            cl_list.dpax = cl_list.dpax + genstat.erwachs + genstat.kind1 + genstat.kind2 + genstat.gratis

                        if (mi_mtd_chk and get_month(genstat.datum) == get_month(d2)) or (mi_ftd_chk and genstat.datum >= d1 and genstat.datum <= d2):
                            mroom = mroom + 1
                            cl_list.mroom = cl_list.mroom + 1
                            cl_list.mpax = cl_list.mpax + genstat.erwachs + genstat.kind1 + genstat.kind2 + genstat.gratis
                            mpax = mpax + genstat.erwachs + genstat.kind1 + genstat.kind2 + genstat.gratis
                        yroom = yroom + 1
                        cl_list.yroom = cl_list.yroom + 1
                        cl_list.ypax = cl_list.ypax + genstat.erwachs + genstat.kind1 + genstat.kind2 + genstat.gratis
                        ypax = ypax + genstat.erwachs + genstat.kind1 + genstat.kind2 + genstat.gratis

        if to_date >= ci_date:
            d2 = d2 + 1

            res_line_obj_list = []
            for res_line, reservation in db_session.query(Res_line, Reservation).join(Reservation,(Reservation.resnr == Res_line.resnr)).filter(
                    (((Res_line.resstatus <= 13) &  (Res_line.resstatus != 4) &  (Res_line.resstatus != 8) &  (Res_line.resstatus != 9) &  (Res_line.resstatus != 10) &  (Res_line.resstatus != 12) &  (Res_line.active_flag <= 1) &  (not (Res_line.ankunft > to_date)) &  (not (Res_line.abreise < d2)))) |  ((Res_line.resstatus == 8) &  (Res_line.active_flag == 2) &  (Res_line.ankunft == ci_date) &  (Res_line.abreise == ci_date)) &  (Res_line.gastnr > 0) &  (Res_line.l_zuordnung[2] == 0)).all():
                if res_line._recid in res_line_obj_list:
                    continue
                else:
                    res_line_obj_list.append(res_line._recid)


                curr_i = 0

                if res_line.kontignr < 0:
                    do_it1 = True

                    cl_list = query(cl_list_list, filters=(lambda cl_list :cl_list.segm == reservation.segmentcode), first=True)

                    if not cl_list:

                        segment = db_session.query(Segment).filter(
                                (Segment.segmentcode == reservation.segmentcode)).first()

                        if segment and not re.match(".*\$\$0",segment.bezeich):
                            cl_list = Cl_list()
                            cl_list_list.append(cl_list)

                            cl_list.segm = segmentcode
                            cl_list.bezeich = segment.bezeich
                        else:
                            do_it1 = False

                    if do_it1 :
                        datum1 = d2

                        if res_line.ankunft > datum1:
                            datum1 = res_line.ankunft
                        datum2 = to_date

                        if res_line.abreise < datum2:
                            datum2 = res_line.abreise
                        for datum0 in range(datum1,datum2 + 1) :
                            curr_i = curr_i + 1

                            if datum0 == res_line.abreise:
                                1
                            else:
                                net_lodg = 0
                                tot_breakfast = 0
                                tot_lunch = 0
                                tot_dinner = 0
                                tot_other = 0


                                fnet_lodg, net_lodg, tot_breakfast, tot_lunch, tot_dinner, tot_other, tot_rmrev, tot_vat, tot_service = get_output(get_room_breakdown(res_line._recid, datum0, curr_i, from_date))

                                if datum0 == to_date:
                                    droom = droom + res_line.zimmeranz
                                    cl_list.droom = cl_list.droom + res_line.zimmeranz
                                    cl_list.dpax = cl_list.dpax + res_line.erwachs + res_line.kind1 + res_line.kind2 + res_line.gratis
                                    cl_list.drev = cl_list.drev + net_lodg
                                    drev = drev + net_lodg

                                if (mi_mtd_chk and get_month(datum0) == get_month(to_date)) or (mi_ftd_chk and datum0 >= d2 and datum0 <= tdate):
                                    cl_list.mroom = cl_list.mroom + res_line.zimmeranz
                                    cl_list.mpax = cl_list.mpax + res_line.erwachs + res_line.kind1 + res_line.kind2 + res_line.gratis
                                    cl_list.mrev = cl_list.mrev + net_lodg
                                    mroom = mroom + res_line.zimmeranz
                                    mpax = mpax + res_line.erwachs + res_line.kind1 + res_line.kind2 + res_line.gratis
                                    mrev = mrev + net_lodg
                                cl_list.yroom = cl_list.yroom + res_line.zimmeranz
                                cl_list.ypax = cl_list.ypax + res_line.erwachs + res_line.kind1 +\
                                        res_line.kind2 + res_line.gratis
                                cl_list.yrev = cl_list.yrev + net_lodg
                                yroom = yroom + res_line.zimmeranz
                                ypax = ypax + res_line.erwachs + res_line.kind1 +\
                                        res_line.kind2 + res_line.gratis
                                yrev = yrev + net_lodg

        if inact:

            for cl_list in query(cl_list_list, filters=(lambda cl_list :cl_list.compli)):

                if cl_list.droom != 0:
                    cl_list.drate = cl_list.drev / cl_list.droom

                if cl_list.mroom != 0:
                    cl_list.mrate = cl_list.mrev / cl_list.mroom

                if cl_list.yroom != 0:
                    cl_list.yrate = cl_list.yrev / cl_list.yroom
                cl_list.proz1 = 100.0 * cl_list.droom / tot_room
                cl_list.proz2 = 100.0 * cl_list.mroom / mtd_act
                cl_list.proz3 = 100.0 * cl_list.yroom / ytd_act

                if droom != 0:
                    drate = drev / droom

                if mroom != 0:
                    mrate = mrev / mroom

                if yroom != 0:
                    yrate = yrev / yroom

                if cl_list.proz1 == None:
                    cl_list.proz1 = 0

                if cl_list.proz2 == None:
                    cl_list.proz2 = 0

                if cl_list.proz3 == None:
                    cl_list.proz3 = 0
                dpax = dpax + cl_list.dpax
            cl_list = Cl_list()
            cl_list_list.append(cl_list)

        cl_list = Cl_list()
        cl_list_list.append(cl_list)

        cl_list.bezeich = rev_title
        cl_list.droom = droom
        cl_list.proz1 = droom / tot_room * 100
        cl_list.mroom = mroom
        cl_list.proz2 = mroom / mtd_act * 100
        cl_list.dpax = dpax
        cl_list.mpax = mpax
        cl_list.yroom = yroom
        cl_list.ypax = ypax
        cl_list.proz3 = yroom / ytd_act * 100
        cl_list.drev = drev
        cl_list.mrev = mrev
        cl_list.yrev = yrev

        if show_avrg:

            if droom != 0:
                cl_list.drate = drev / droom
            else:
                cl_list.drate = 0

            if mroom != 0:
                cl_list.mrate = mrev / mroom
            else:
                cl_list.mrate = 0

            if yroom != 0:
                cl_list.yrate = yrev / yroom
            else:
                cl_list.yrate = 0

        if rev_title1 != "":
            cl_list = Cl_list()
            cl_list_list.append(cl_list)

            cl_list.bezeich = rev_title1

            if droom != 0:
                cl_list.proz1 = (dpax - droom) / droom * 100
            else:
                cl_list.proz1 = 0

            if mroom != 0:
                cl_list.proz2 = (mpax - mroom) / mroom * 100
            else:
                cl_list.proz2 = 0

            if yroom != 0:
                cl_list.proz3 = (ypax - yroom) / yroom * 100
            else:
                cl_list.proz3 = 0
        cl_list = Cl_list()
        cl_list_list.append(cl_list)


    def cal_umsatz2():

        nonlocal cl_list_list, lvcarea, do_it, droomrev, mroomrev, yroomrev, droomexc, mroomexc, yroomexc, tot_room, all_room, dvacant, dooo, mvacant, mooo, yvacant, yooo, dnoshow, dcancel, mnoshow, mcancel, ynoshow, ycancel, droom, proz1, mroom, proz2, dpax, mpax, drate, mrate, drev, mrev, yroom, ypax, yrate, yrev, from_bez, to_bez, inactive, mtd_act, mtd_totrm, ytd_act, ytd_totrm, ncompli, mtd_ncompli, ytd_ncompli, dcompli, mcompli, ycompli, dhu, mhu, yhu, ci_date, htparam, zimmer, zkstat, zinrstat, genstat, segment, guestseg, reservation, res_line, outorder, artikel, umsatz
        nonlocal bgenstat


        nonlocal cl_list, bgenstat
        nonlocal cl_list_list

        i:int = 0
        datum:date = None
        datum1:date = None
        dooo = 0
        mooo = 0
        yooo = 0
        for datum in range(from_date,to_date + 1) :

            if to_date < ci_date:
                datum1 = to_date


            else:
                datum1 = (ci_date - 1)

            zinrstat = db_session.query(Zinrstat).filter(
                    (Zinrstat.datum == datum) &  (func.lower(Zinrstat.zinr) == "ooo")).first()

            if zinrstat:

                if datum == to_date:
                    dooo = zinrstat.zimmeranz

                if (mi_mtd_chk and get_month(zinrstat.datum) == get_month(datum1)) or (mi_ftd_chk and zinrstat.datum >= fdate and zinrstat.datum <= datum1):
                    mooo = mooo + zinrstat.zimmeranz
                yooo = yooo + zinrstat.zimmeranz

            if datum >= ci_date:

                outorder_obj_list = []
                for outorder, zimmer in db_session.query(Outorder, Zimmer).join(Zimmer,(Zimmer.zinr == Outorder.zinr)).filter(
                        ((Outorder.gespstart >= datum) &  (Outorder.gespstart <= datum)) |  ((Outorder.gespstart <= datum) &  (Outorder.gespende >= datum))).all():
                    if outorder._recid in outorder_obj_list:
                        continue
                    else:
                        outorder_obj_list.append(outorder._recid)

                    if datum == to_date:
                        dooo = dooo + 1

                    if (mi_mtd_chk and get_month(datum) == get_month(to_date)):
                        mooo = mooo + 1
                    yooo = yooo + 1
        dvacant = tot_room - dooo - droom
        mvacant = mtd_act - mooo - mroom
        yvacant = ytd_act - yooo - yroom

        if to_date == opening_date:
            mvacant = dvacant
            yvacant = dvacant
            mooo = dooo
            yooo = dooo
        cl_list = Cl_list()
        cl_list_list.append(cl_list)

        cl_list.bezeich = "V A C A N T"
        cl_list.droom = dvacant
        cl_list.proz1 = dvacant / tot_room * 100
        cl_list.mroom = mvacant
        cl_list.proz2 = mvacant / mtd_act * 100
        cl_list.yroom = yvacant
        cl_list.proz3 = yvacant / ytd_act * 100


        cl_list = Cl_list()
        cl_list_list.append(cl_list)

        cl_list.bezeich = "Out Of Order"
        cl_list.droom = dooo
        cl_list.proz1 = dooo / tot_room * 100
        cl_list.mroom = mooo
        cl_list.proz2 = mooo / mtd_act * 100
        cl_list.yroom = yooo
        cl_list.proz3 = yooo / ytd_act * 100


        cl_list = Cl_list()
        cl_list_list.append(cl_list)


        if to_date < ci_date:

            zinrstat = db_session.query(Zinrstat).filter(
                    (func.lower(Zinrstat.zinr) == "tot_rm") &  (Zinrstat.datum == to_date)).first()

            if zinrstat:
                all_room = zinrstat.zimmeranz
        else:

            for zimmer in db_session.query(Zimmer).all():
                all_room = all_room + 1


        cl_list = Cl_list()
        cl_list_list.append(cl_list)

        cl_list.bezeich = "# Active Rooms"
        cl_list.droom = tot_room
        cl_list.proz1 = 100
        cl_list.mroom = mtd_act
        cl_list.proz2 = 100
        cl_list.yroom = ytd_act
        cl_list.proz3 = 100


        cl_list = Cl_list()
        cl_list_list.append(cl_list)

        cl_list.bezeich = "inactive Rooms"
        cl_list.droom = all_room - tot_room
        cl_list.mroom = mtd_totrm - mtd_act
        cl_list.yroom = ytd_totrm - ytd_act


        cl_list = Cl_list()
        cl_list_list.append(cl_list)

        cl_list.bezeich = "Total Rooms"
        cl_list.droom = all_room
        cl_list.mroom = mtd_totrm
        cl_list.yroom = ytd_totrm


        cl_list = Cl_list()
        cl_list_list.append(cl_list)


    def cal_umsatz3():

        nonlocal cl_list_list, lvcarea, do_it, droomrev, mroomrev, yroomrev, droomexc, mroomexc, yroomexc, tot_room, all_room, dvacant, dooo, mvacant, mooo, yvacant, yooo, dnoshow, dcancel, mnoshow, mcancel, ynoshow, ycancel, droom, proz1, mroom, proz2, dpax, mpax, drate, mrate, drev, mrev, yroom, ypax, yrate, yrev, from_bez, to_bez, inactive, mtd_act, mtd_totrm, ytd_act, ytd_totrm, ncompli, mtd_ncompli, ytd_ncompli, dcompli, mcompli, ycompli, dhu, mhu, yhu, ci_date, htparam, zimmer, zkstat, zinrstat, genstat, segment, guestseg, reservation, res_line, outorder, artikel, umsatz
        nonlocal bgenstat


        nonlocal cl_list, bgenstat
        nonlocal cl_list_list

        i:int = 0
        max_i:int = 0
        datum:date = None
        art_list:[int] = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        serv_vat:bool = False
        fact:decimal = 0
        serv:decimal = 0
        vat:decimal = 0
        drev_droom:decimal = 0
        mrev_mroom:decimal = 0
        drev_droom1:decimal = 0
        mrev_mroom1:decimal = 0

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 479)).first()
        serv_vat = htparam.flogical

        for artikel in db_session.query(Artikel).filter(
                (Artikel.departement == 0) &  (Artikel.artart == 0) &  (Artikel.umsatzart == 1)).all():
            max_i = max_i + 1
            art_list[max_i - 1] = artikel.artnr

        if do_it:
            pass
        else:
            for i in range(1,max_i + 1) :

                artikel = db_session.query(Artikel).filter(
                        (Artikel.artnr == art_list[i - 1]) &  (Artikel.departement == 0)).first()

                if artikel:
                    cl_list = Cl_list()
                    cl_list_list.append(cl_list)

                    cl_list.segm = 9999999

                    if i >= 10:
                        cl_list.bezeich = translateExtended ("Other RmRev", lvcarea, "")
                    else:
                        cl_list.bezeich = artikel.bezeich
                    for datum in range(from_date,to_date + 1) :
                        serv = 0
                        vat = 0

                        for umsatz in db_session.query(Umsatz).filter(
                                (Umsatz.artnr == artikel.artnr) &  (Umsatz.departement == artikel.departement) &  (Umsatz.datum == datum)).all():
                            serv, vat = get_output(calc_servvat(umsatz.departement, umsatz.artnr, umsatz.datum, artikel.service_code, artikel.mwst_code))
                            fact = 1.00 + serv + vat

                            if datum == to_date:
                                drev = drev + umsatz.betrag / fact
                                cl_list.drev = umsatz.betrag / fact

                            if (mi_mtd_chk and get_month(datum) == get_month(to_date)) or (mi_ftd_chk and datum >= fdate and datum <= tdate):
                                mrev = mrev + umsatz.betrag / fact
                                cl_list.mrev = cl_list.mrev + umsatz.betrag / fact
                            yrev = yrev + umsatz.betrag / fact


                            cl_list.yrev = cl_list.yrev + umsatz.betrag / fact

                    if cl_list.mrev == 0:
                        cl_list.bezeich = "Deleted"
            cl_list = Cl_list()
            cl_list_list.append(cl_list)


        if mi_exchu_chk :
            ncompli = ncompli - dhu
            mtd_ncompli = mtd_ncompli - mhu
            ytd_ncompli = ytd_ncompli - yhu

        if mi_exccomp_chk :
            ncompli = ncompli - dcompli
            mtd_ncompli = mtd_ncompli - mcompli
            ytd_ncompli = ytd_ncompli - ycompli


        drev_droom = drev / droom
        drev_droom1 = drev / droomrev

        if drev_droom == None:
            drev_droom = 0

        if drev_droom1 == None:
            drev_droom1 = 0
        mrev_mroom = mrev / mroom
        mrev_mroom1 = mrev / mroomrev

        if mrev_mroom == None:
            mrev_mroom = 0

        if mrev_mroom1 == None:
            mrev_mroom1 = 0

        if not long_digit:
            cl_list = Cl_list()
            cl_list_list.append(cl_list)

            cl_list.bezeich = "RmRev Inc Comp"
            cl_list.drate = drev_droom
            cl_list.mrate = mrev_mroom
            cl_list.drev = drev
            cl_list.mrev = mrev
            cl_list.yrev = yrev

            if yroom != 0:
                cl_list.yrate = yrev / yroom
            cl_list = Cl_list()
            cl_list_list.append(cl_list)

            cl_list.bezeich = "RmRev Exc Comp"
            cl_list.drate = drev_droom1
            cl_list.mrate = mrev_mroom1
            cl_list.drev = drev
            cl_list.mrev = mrev
            cl_list.yrev = yrev

            if yroomrev != 0:
                cl_list.yrate = yrev / yroomrev
        else:
            cl_list = Cl_list()
            cl_list_list.append(cl_list)

            cl_list.bezeich = "Total RmRevenue (comp guest)"
            cl_list.drate = drev_droom
            cl_list.mrate = mrev_mroom
            cl_list.drev = drev
            cl_list.mrev = mrev
            cl_list.yrev = yrev


            cl_list = Cl_list()
            cl_list_list.append(cl_list)

            cl_list.bezeich = "Total RmRevenue (Paying Guest)"
            cl_list.drate = drev_droom1
            cl_list.mrate = mrev_mroom1
            cl_list.drev = drev
            cl_list.mrev = mrev
            cl_list.yrev = yrev


        cl_list = Cl_list()
        cl_list_list.append(cl_list)


    def no_show():

        nonlocal cl_list_list, lvcarea, do_it, droomrev, mroomrev, yroomrev, droomexc, mroomexc, yroomexc, tot_room, all_room, dvacant, dooo, mvacant, mooo, yvacant, yooo, dnoshow, dcancel, mnoshow, mcancel, ynoshow, ycancel, droom, proz1, mroom, proz2, dpax, mpax, drate, mrate, drev, mrev, yroom, ypax, yrate, yrev, from_bez, to_bez, inactive, mtd_act, mtd_totrm, ytd_act, ytd_totrm, ncompli, mtd_ncompli, ytd_ncompli, dcompli, mcompli, ycompli, dhu, mhu, yhu, ci_date, htparam, zimmer, zkstat, zinrstat, genstat, segment, guestseg, reservation, res_line, outorder, artikel, umsatz
        nonlocal bgenstat


        nonlocal cl_list, bgenstat
        nonlocal cl_list_list

        i:int = 0
        dnoshow = 0
        dcancel = 0
        mnoshow = 0
        mcancel = 0

        for zinrstat in db_session.query(Zinrstat).filter(
                (func.lower(Zinrstat.zinr) == "No_Show") &  (Zinrstat.datum >= from_date) &  (Zinrstat.datum <= to_date)).all():

            if zinrstat.datum == to_date:
                dnoshow = dnoshow + zinrstat.zimmeranz

            if (mi_mtd_chk and get_month(datum) == get_month(to_date)) or (mi_ftd_chk and datum >= fdate and datum <= tdate):
                mnoshow = mnoshow + zinrstat.zimmeranz
            ynoshow = ynoshow + zinrstat.zimmeranz

        for zinrstat in db_session.query(Zinrstat).filter(
                (func.lower(Zinrstat.zinr) == "CancRes") &  (Zinrstat.datum >= from_date) &  (Zinrstat.datum <= to_date)).all():

            if zinrstat.datum == to_date:
                dcancel = dcancel + zinrstat.zimmeranz

            if get_month(datum) == get_month(to_date):
                mcancel = mcancel + zinrstat.zimmeranz


            ycancel = ycancel + zinrstat.zimmeranz
        cl_list = Cl_list()
        cl_list_list.append(cl_list)

        cl_list.bezeich = "NO SHOW"
        cl_list.droom = dnoshow
        cl_list.mroom = mnoshow
        cl_list.yroom = ynoshow


        cl_list = Cl_list()
        cl_list_list.append(cl_list)

        cl_list.bezeich = "C A N C E L"
        cl_list.droom = dcancel
        cl_list.mroom = mcancel
        cl_list.yroom = ycancel


        cl_list = Cl_list()
        cl_list_list.append(cl_list)


    def cal_umsatz4(i1:int, i2:int, i3:int, i4:int, rev_title:str, rev_title1:str, show_avrg:bool):

        nonlocal cl_list_list, lvcarea, do_it, droomrev, mroomrev, yroomrev, droomexc, mroomexc, yroomexc, tot_room, all_room, dvacant, dooo, mvacant, mooo, yvacant, yooo, dnoshow, dcancel, mnoshow, mcancel, ynoshow, ycancel, droom, proz1, mroom, proz2, dpax, mpax, drate, mrate, drev, mrev, yroom, ypax, yrate, yrev, from_bez, to_bez, inactive, mtd_act, mtd_totrm, ytd_act, ytd_totrm, ncompli, mtd_ncompli, ytd_ncompli, dcompli, mcompli, ycompli, dhu, mhu, yhu, ci_date, htparam, zimmer, zkstat, zinrstat, genstat, segment, guestseg, reservation, res_line, outorder, artikel, umsatz
        nonlocal bgenstat


        nonlocal cl_list, bgenstat
        nonlocal cl_list_list

        i:int = 0
        datum:date = None
        do_it1:bool = False
        d1:date = None
        d2:date = None
        datum0:date = None
        datum1:date = None
        datum2:date = None
        curr_i:int = 0
        net_lodg:decimal = 0
        fnet_lodg:decimal = 0
        tot_breakfast:decimal = 0
        tot_lunch:decimal = 0
        tot_dinner:decimal = 0
        tot_other:decimal = 0
        tot_rmrev:decimal = 0
        tot_vat:decimal = 0
        tot_service:decimal = 0
        Bgenstat = Genstat
        d2 = from_date

        res_line_obj_list = []
        for res_line, reservation in db_session.query(Res_line, Reservation).join(Reservation,(Reservation.resnr == Res_line.resnr)).filter(
                    (((Res_line.resstatus <= 13) &  (Res_line.resstatus != 4) &  (Res_line.resstatus != 8) &  (Res_line.resstatus != 9) &  (Res_line.resstatus != 10) &  (Res_line.resstatus != 12) &  (Res_line.active_flag <= 1) &  (not (Res_line.ankunft > to_date)) &  (not (Res_line.abreise < d2)))) |  ((Res_line.resstatus == 8) &  (Res_line.active_flag == 2) &  (Res_line.ankunft == ci_date) &  (Res_line.abreise == ci_date)) &  (Res_line.gastnr > 0) &  (Res_line.l_zuordnung[2] == 0)).all():
            if res_line._recid in res_line_obj_list:
                continue
            else:
                res_line_obj_list.append(res_line._recid)


            curr_i = 0

            if res_line.kontignr < 0:
                do_it1 = True

                cl_list = query(cl_list_list, filters=(lambda cl_list :cl_list.segm == reservation.segmentcode), first=True)

                if not cl_list:

                    segment = db_session.query(Segment).filter(
                                (Segment.segmentcode == reservation.segmentcode)).first()

                    if segment and not re.match(".*\$\$0",segment.bezeich):
                        cl_list = Cl_list()
                        cl_list_list.append(cl_list)

                        cl_list.segm = segmentcode
                        cl_list.bezeich = segment.bezeich
                    else:
                        do_it1 = False

                if do_it1 :
                    datum1 = d2

                    if res_line.ankunft > datum1:
                        datum1 = res_line.ankunft
                    datum2 = to_date

                    if res_line.abreise < datum2:
                        datum2 = res_line.abreise
                    for datum0 in range(datum1,datum2 + 1) :
                        curr_i = curr_i + 1

                        if datum0 == res_line.abreise:
                            1
                        else:
                            net_lodg = 0
                            tot_breakfast = 0
                            tot_lunch = 0
                            tot_dinner = 0
                            tot_other = 0


                            fnet_lodg, net_lodg, tot_breakfast, tot_lunch, tot_dinner, tot_other, tot_rmrev, tot_vat, tot_service = get_output(get_room_breakdown(res_line._recid, datum0, curr_i, from_date))

                            if datum0 == to_date:
                                droom = droom + res_line.zimmeranz
                                cl_list.droom = cl_list.droom + res_line.zimmeranz
                                cl_list.dpax = cl_list.dpax + res_line.erwachs + res_line.kind1 + res_line.kind2 + res_line.gratis
                                cl_list.drev = cl_list.drev + net_lodg
                                drev = drev + net_lodg

                            if (mi_mtd_chk and get_month(datum0) == get_month(to_date)) or (mi_ftd_chk and datum0 >= d2 and datum0 <= tdate):
                                cl_list.mroom = cl_list.mroom + res_line.zimmeranz
                                cl_list.mpax = cl_list.mpax + res_line.erwachs + res_line.kind1 + res_line.kind2 + res_line.gratis
                                cl_list.mrev = cl_list.mrev + net_lodg
                                mroom = mroom + res_line.zimmeranz
                                mpax = mpax + res_line.erwachs + res_line.kind1 + res_line.kind2 + res_line.gratis
                                mrev = mrev + net_lodg
                            cl_list.yroom = cl_list.yroom + res_line.zimmeranz
                            cl_list.ypax = cl_list.ypax + res_line.erwachs + res_line.kind1 +\
                                    res_line.kind2 + res_line.gratis
                            cl_list.yrev = cl_list.yrev + net_lodg
                            yroom = yroom + res_line.zimmeranz
                            ypax = ypax + res_line.erwachs + res_line.kind1 +\
                                    res_line.kind2 + res_line.gratis
                            yrev = yrev + net_lodg

        for cl_list in query(cl_list_list, filters=(lambda cl_list :((cl_list.segm >= i1 and cl_list.segm <= i2) or (cl_list.segm >= i3 and cl_list.segm <= i4)))):

            if cl_list.droom != 0:
                cl_list.drate = cl_list.drev / cl_list.droom

            if cl_list.mroom != 0:
                cl_list.mrate = cl_list.mrev / cl_list.mroom
            cl_list.proz1 = 100.0 * cl_list.droom / tot_room
            cl_list.proz2 = 100.0 * cl_list.mroom / mtd_act
            cl_list.proz3 = 100.0 * cl_list.yroom / ytd_act

            if droom != 0:
                drate = drev / droom

            if mroom != 0:
                mrate = mrev / mroom

            if yroom != 0:
                yrate = yrev / yroom

            if cl_list.proz1 == None:
                cl_list.proz1 = 0

            if cl_list.proz2 == None:
                cl_list.proz2 = 0

            if cl_list.proz3 == None:
                cl_list.proz3 = 0
            dpax = dpax + cl_list.dpax

            if cl_list.drev == 0 and cl_list.mrev == 0 and cl_list.yrev == 0:
                cl_list.zero_flag = True
        cl_list = Cl_list()
        cl_list_list.append(cl_list)

        cl_list = Cl_list()
        cl_list_list.append(cl_list)

        cl_list.bezeich = to_string(rev_title, "x(16)")
        cl_list.droom = droom
        cl_list.proz1 = droom / tot_room * 100
        cl_list.mroom = mroom
        cl_list.proz2 = mroom / mtd_act * 100
        cl_list.dpax = dpax
        cl_list.mpax = mpax
        cl_list.yroom = yroom
        cl_list.ypax = ypax
        cl_list.proz3 = ytd_act * 100
        cl_list.drev = drev
        cl_list.mrev = mrev
        cl_list.yrev = yrev

        if show_avrg:

            if droom != 0:
                cl_list.drate = drev / droom
            else:
                cl_list.drate = 0

            if mroom != 0:
                cl_list.mrate = mrev / mroom
            else:
                cl_list.mrate = 0

            if yroom != 0:
                cl_list.yrate = yrev / yroom
            else:
                cl_list.yrate = 0

        if rev_title1 != "":
            cl_list = Cl_list()
            cl_list_list.append(cl_list)

            cl_list.bezeich = rev_title1

            if droom != 0:
                cl_list.proz1 = (dpax - droom) / droom * 100
            else:
                cl_list.proz1 = 0

            if mroom != 0:
                cl_list.proz2 = (mpax - mroom) / mroom * 100
            else:
                cl_list.proz2 = 0

            if yroom != 0:
                cl_list.proz3 = (ypax - yroom) / yroom * 100
            else:
                cl_list.proz3 = 0
        cl_list = Cl_list()
        cl_list_list.append(cl_list)


    def cal_umsatz4a(i1:int, i2:int, rev_title:str, rev_title1:str, show_avrg:bool):

        nonlocal cl_list_list, lvcarea, do_it, droomrev, mroomrev, yroomrev, droomexc, mroomexc, yroomexc, tot_room, all_room, dvacant, dooo, mvacant, mooo, yvacant, yooo, dnoshow, dcancel, mnoshow, mcancel, ynoshow, ycancel, droom, proz1, mroom, proz2, dpax, mpax, drate, mrate, drev, mrev, yroom, ypax, yrate, yrev, from_bez, to_bez, inactive, mtd_act, mtd_totrm, ytd_act, ytd_totrm, ncompli, mtd_ncompli, ytd_ncompli, dcompli, mcompli, ycompli, dhu, mhu, yhu, ci_date, htparam, zimmer, zkstat, zinrstat, genstat, segment, guestseg, reservation, res_line, outorder, artikel, umsatz
        nonlocal bgenstat


        nonlocal cl_list, bgenstat
        nonlocal cl_list_list

        i:int = 0
        tot_proz3:decimal = 0
        inact:bool = False
        do_it1:bool = False
        d1:date = None
        d2:date = None
        datum0:date = None
        datum1:date = None
        datum2:date = None
        curr_i:int = 0
        net_lodg:decimal = 0
        fnet_lodg:decimal = 0
        tot_breakfast:decimal = 0
        tot_lunch:decimal = 0
        tot_dinner:decimal = 0
        tot_other:decimal = 0
        tot_rmrev:decimal = 0
        tot_vat:decimal = 0
        tot_service:decimal = 0
        Bgenstat = Genstat
        d2 = from_date

        res_line_obj_list = []
        for res_line, reservation in db_session.query(Res_line, Reservation).join(Reservation,(Reservation.resnr == Res_line.resnr)).filter(
                    (((Res_line.resstatus <= 13) &  (Res_line.resstatus != 4) &  (Res_line.resstatus != 8) &  (Res_line.resstatus != 9) &  (Res_line.resstatus != 10) &  (Res_line.resstatus != 12) &  (Res_line.active_flag <= 1) &  (not (Res_line.ankunft > to_date)) &  (not (Res_line.abreise < d2)))) |  ((Res_line.resstatus == 8) &  (Res_line.active_flag == 2) &  (Res_line.ankunft == ci_date) &  (Res_line.abreise == ci_date)) &  (Res_line.gastnr > 0) &  (Res_line.l_zuordnung[2] == 0)).all():
            if res_line._recid in res_line_obj_list:
                continue
            else:
                res_line_obj_list.append(res_line._recid)


            curr_i = 0

            if res_line.kontignr < 0:
                do_it1 = True

                cl_list = query(cl_list_list, filters=(lambda cl_list :cl_list.segm == reservation.segmentcode), first=True)

                if not cl_list:

                    segment = db_session.query(Segment).filter(
                                (Segment.segmentcode == reservation.segmentcode)).first()

                    if segment and not re.match(".*\$\$0",segment.bezeich):
                        cl_list = Cl_list()
                        cl_list_list.append(cl_list)

                        cl_list.segm = segmentcode
                        cl_list.bezeich = segment.bezeich
                    else:
                        do_it1 = False

                if do_it1 :
                    datum1 = d2

                    if res_line.ankunft > datum1:
                        datum1 = res_line.ankunft
                    datum2 = to_date

                    if res_line.abreise < datum2:
                        datum2 = res_line.abreise
                    for datum0 in range(datum1,datum2 + 1) :
                        curr_i = curr_i + 1

                        if datum0 == res_line.abreise:
                            1
                        else:
                            net_lodg = 0
                            tot_breakfast = 0
                            tot_lunch = 0
                            tot_dinner = 0
                            tot_other = 0


                            fnet_lodg, net_lodg, tot_breakfast, tot_lunch, tot_dinner, tot_other, tot_rmrev, tot_vat, tot_service = get_output(get_room_breakdown(res_line._recid, datum0, curr_i, from_date))

                            if datum0 == to_date:
                                droom = droom + res_line.zimmeranz
                                cl_list.droom = cl_list.droom + res_line.zimmeranz
                                cl_list.dpax = cl_list.dpax + res_line.erwachs + res_line.kind1 + res_line.kind2 + res_line.gratis
                                cl_list.drev = cl_list.drev + net_lodg
                                drev = drev + net_lodg

                            if (mi_mtd_chk and get_month(datum0) == get_month(to_date)) or (mi_ftd_chk and datum0 >= d2 and datum0 <= tdate):
                                cl_list.mroom = cl_list.mroom + res_line.zimmeranz
                                cl_list.mpax = cl_list.mpax + res_line.erwachs + res_line.kind1 + res_line.kind2 + res_line.gratis
                                cl_list.mrev = cl_list.mrev + net_lodg
                                mroom = mroom + res_line.zimmeranz
                                mpax = mpax + res_line.erwachs + res_line.kind1 + res_line.kind2 + res_line.gratis
                                mrev = mrev + net_lodg
                            cl_list.yroom = cl_list.yroom + res_line.zimmeranz
                            cl_list.ypax = cl_list.ypax + res_line.erwachs + res_line.kind1 +\
                                    res_line.kind2 + res_line.gratis
                            cl_list.yrev = cl_list.yrev + net_lodg
                            yroom = yroom + res_line.zimmeranz
                            ypax = ypax + res_line.erwachs + res_line.kind1 +\
                                    res_line.kind2 + res_line.gratis
                            yrev = yrev + net_lodg

        if inact:

            for cl_list in query(cl_list_list, filters=(lambda cl_list :(cl_list.betriebsnr >= i1 and cl_list.betriebsnr <= i2))):

                if cl_list.droom != 0:
                    cl_list.drate = cl_list.drev / cl_list.droom

                if cl_list.mroom != 0:
                    cl_list.mrate = cl_list.mrev / cl_list.mroom

                if cl_list.yroom != 0:
                    cl_list.yrate = cl_list.yrev / cl_list.yroom
                cl_list.proz1 = 100.0 * cl_list.droom / tot_room
                cl_list.proz2 = 100.0 * cl_list.mroom / mtd_act
                cl_list.proz3 = 100.0 * cl_list.yroom / ytd_act

                if droom != 0:
                    drate = drev / droom

                if mroom != 0:
                    mrate = mrev / mroom

                if yroom != 0:
                    yrate = yrev / yroom

                if cl_list.proz1 == None:
                    cl_list.proz1 = 0

                if cl_list.proz2 == None:
                    cl_list.proz2 = 0

                if cl_list.proz3 == None:
                    cl_list.proz3 = 0
                tot_proz3 = tot_proz3 + cl_list.proz3


                dpax = dpax + cl_list.dpax

                if cl_list.drev == 0 and cl_list.mrev == 0 and cl_list.yrev == 0:
                    cl_list.zero_flag = True
            cl_list = Cl_list()
            cl_list_list.append(cl_list)

        droomexc = droom
        mroomexc = mroom
        yroomexc = yroom
        droomrev = droomexc
        mroomrev = mroomexc
        yroomrev = yroomexc


        cl_list = Cl_list()
        cl_list_list.append(cl_list)

        cl_list.bezeich = rev_title
        cl_list.droom = droom
        cl_list.proz1 = droom / tot_room * 100
        cl_list.mroom = mroom
        cl_list.proz2 = mroom / mtd_act * 100
        cl_list.dpax = dpax
        cl_list.mpax = mpax
        cl_list.yroom = yroom
        cl_list.ypax = ypax
        cl_list.proz3 = tot_proz3
        cl_list.drev = drev
        cl_list.mrev = mrev
        cl_list.yrev = yrev

        if show_avrg:

            if droom != 0:
                cl_list.drate = drev / droom
            else:
                cl_list.drate = 0

            if mroom != 0:
                cl_list.mrate = mrev / mroom
            else:
                cl_list.mrate = 0

            if yroom != 0:
                cl_list.yrate = yrev / yroom
            else:
                cl_list.yrate = 0

        if rev_title1 != "":
            cl_list = Cl_list()
            cl_list_list.append(cl_list)

            cl_list.bezeich = rev_title1

            if droom != 0:
                cl_list.proz1 = (dpax - droom) / droom * 100
            else:
                cl_list.proz1 = 0

            if mroom != 0:
                cl_list.proz2 = (mpax - mroom) / mroom * 100
            else:
                cl_list.proz2 = 0

            if yroom != 0:
                cl_list.proz3 = (ypax - yroom) / yroom * 100
            else:
                cl_list.proz3 = 0
        cl_list = Cl_list()
        cl_list_list.append(cl_list)


    def cal_umsatz4b(i1:int, i2:int, rev_title:str, rev_title1:str, show_avrg:bool):

        nonlocal cl_list_list, lvcarea, do_it, droomrev, mroomrev, yroomrev, droomexc, mroomexc, yroomexc, tot_room, all_room, dvacant, dooo, mvacant, mooo, yvacant, yooo, dnoshow, dcancel, mnoshow, mcancel, ynoshow, ycancel, droom, proz1, mroom, proz2, dpax, mpax, drate, mrate, drev, mrev, yroom, ypax, yrate, yrev, from_bez, to_bez, inactive, mtd_act, mtd_totrm, ytd_act, ytd_totrm, ncompli, mtd_ncompli, ytd_ncompli, dcompli, mcompli, ycompli, dhu, mhu, yhu, ci_date, htparam, zimmer, zkstat, zinrstat, genstat, segment, guestseg, reservation, res_line, outorder, artikel, umsatz
        nonlocal bgenstat


        nonlocal cl_list, bgenstat
        nonlocal cl_list_list

        i:int = 0
        datum:date = None
        inact:bool = False
        do_it1:bool = False
        d1:date = None
        d2:date = None
        datum0:date = None
        datum1:date = None
        datum2:date = None
        curr_i:int = 0
        net_lodg:decimal = 0
        fnet_lodg:decimal = 0
        tot_breakfast:decimal = 0
        tot_lunch:decimal = 0
        tot_dinner:decimal = 0
        tot_other:decimal = 0
        tot_rmrev:decimal = 0
        tot_vat:decimal = 0
        tot_service:decimal = 0
        Bgenstat = Genstat
        d2 = from_date

        res_line_obj_list = []
        for res_line, reservation in db_session.query(Res_line, Reservation).join(Reservation,(Reservation.resnr == Res_line.resnr)).filter(
                    (((Res_line.resstatus <= 13) &  (Res_line.resstatus != 4) &  (Res_line.resstatus != 8) &  (Res_line.resstatus != 9) &  (Res_line.resstatus != 10) &  (Res_line.resstatus != 12) &  (Res_line.active_flag <= 1) &  (not (Res_line.ankunft > to_date)) &  (not (Res_line.abreise < d2)))) |  ((Res_line.resstatus == 8) &  (Res_line.active_flag == 2) &  (Res_line.ankunft == ci_date) &  (Res_line.abreise == ci_date)) &  (Res_line.gastnr > 0) &  (Res_line.l_zuordnung[2] == 0)).all():
            if res_line._recid in res_line_obj_list:
                continue
            else:
                res_line_obj_list.append(res_line._recid)


            curr_i = 0

            if res_line.kontignr < 0:
                do_it1 = True

                cl_list = query(cl_list_list, filters=(lambda cl_list :cl_list.segm == reservation.segmentcode), first=True)

                if not cl_list:

                    segment = db_session.query(Segment).filter(
                                (Segment.segmentcode == reservation.segmentcode)).first()

                    if segment and not re.match(".*\$\$0",segment.bezeich):
                        cl_list = Cl_list()
                        cl_list_list.append(cl_list)

                        cl_list.segm = segmentcode
                        cl_list.bezeich = segment.bezeich
                    else:
                        do_it1 = False

                if do_it1 :
                    datum1 = d2

                    if res_line.ankunft > datum1:
                        datum1 = res_line.ankunft
                    datum2 = to_date

                    if res_line.abreise < datum2:
                        datum2 = res_line.abreise
                    for datum0 in range(datum1,datum2 + 1) :
                        curr_i = curr_i + 1

                        if datum0 == res_line.abreise:
                            1
                        else:
                            net_lodg = 0
                            tot_breakfast = 0
                            tot_lunch = 0
                            tot_dinner = 0
                            tot_other = 0


                            fnet_lodg, net_lodg, tot_breakfast, tot_lunch, tot_dinner, tot_other, tot_rmrev, tot_vat, tot_service = get_output(get_room_breakdown(res_line._recid, datum0, curr_i, from_date))

                            if datum0 == to_date:
                                droom = droom + res_line.zimmeranz
                                cl_list.droom = cl_list.droom + res_line.zimmeranz
                                cl_list.dpax = cl_list.dpax + res_line.erwachs + res_line.kind1 + res_line.kind2 + res_line.gratis
                                cl_list.drev = cl_list.drev + net_lodg
                                drev = drev + net_lodg

                            if (mi_mtd_chk and get_month(datum0) == get_month(to_date)) or (mi_ftd_chk and datum0 >= d2 and datum0 <= tdate):
                                cl_list.mroom = cl_list.mroom + res_line.zimmeranz
                                cl_list.mpax = cl_list.mpax + res_line.erwachs + res_line.kind1 + res_line.kind2 + res_line.gratis
                                cl_list.mrev = cl_list.mrev + net_lodg
                                mroom = mroom + res_line.zimmeranz
                                mpax = mpax + res_line.erwachs + res_line.kind1 + res_line.kind2 + res_line.gratis
                                mrev = mrev + net_lodg
                            cl_list.yroom = cl_list.yroom + res_line.zimmeranz
                            cl_list.ypax = cl_list.ypax + res_line.erwachs + res_line.kind1 +\
                                    res_line.kind2 + res_line.gratis
                            cl_list.yrev = cl_list.yrev + net_lodg
                            yroom = yroom + res_line.zimmeranz
                            ypax = ypax + res_line.erwachs + res_line.kind1 +\
                                    res_line.kind2 + res_line.gratis
                            yrev = yrev + net_lodg

        if inact:

            for cl_list in query(cl_list_list, filters=(lambda cl_list :cl_list.compli)):

                if cl_list.droom != 0:
                    cl_list.drate = cl_list.drev / cl_list.droom

                if cl_list.mroom != 0:
                    cl_list.mrate = cl_list.mrev / cl_list.mroom

                if cl_list.yroom != 0:
                    cl_list.yrate = cl_list.yrev / cl_list.yroom
                cl_list.proz1 = 100.0 * cl_list.droom / tot_room
                cl_list.proz2 = 100.0 * cl_list.mroom / mtd_act
                cl_list.proz3 = 100.0 * cl_list.yroom / ytd_act

                if droom != 0:
                    drate = drev / droom

                if mroom != 0:
                    mrate = mrev / mroom

                if yroom != 0:
                    yrate = yrev / yroom

                if cl_list.proz1 == None:
                    cl_list.proz1 = 0

                if cl_list.proz2 == None:
                    cl_list.proz2 = 0

                if cl_list.proz3 == None:
                    cl_list.proz3 = 0
                dpax = dpax + cl_list.dpax
            cl_list = Cl_list()
            cl_list_list.append(cl_list)

        cl_list = Cl_list()
        cl_list_list.append(cl_list)

        cl_list.bezeich = rev_title
        cl_list.droom = droom
        cl_list.proz1 = droom / tot_room * 100
        cl_list.mroom = mroom
        cl_list.proz2 = mroom / mtd_act * 100
        cl_list.dpax = dpax
        cl_list.mpax = mpax
        cl_list.yroom = yroom
        cl_list.ypax = ypax
        cl_list.proz3 = yroom / ytd_act * 100
        cl_list.drev = drev
        cl_list.mrev = mrev
        cl_list.yrev = yrev

        if show_avrg:

            if droom != 0:
                cl_list.drate = drev / droom
            else:
                cl_list.drate = 0

            if mroom != 0:
                cl_list.mrate = mrev / mroom
            else:
                cl_list.mrate = 0

            if yroom != 0:
                cl_list.yrate = yrev / yroom
            else:
                cl_list.yrate = 0

        if rev_title1 != "":
            cl_list = Cl_list()
            cl_list_list.append(cl_list)

            cl_list.bezeich = rev_title1

            if droom != 0:
                cl_list.proz1 = (dpax - droom) / droom * 100
            else:
                cl_list.proz1 = 0

            if mroom != 0:
                cl_list.proz2 = (mpax - mroom) / mroom * 100
            else:
                cl_list.proz2 = 0

            if yroom != 0:
                cl_list.proz3 = (ypax - yroom) / yroom * 100
            else:
                cl_list.proz3 = 0
        cl_list = Cl_list()
        cl_list_list.append(cl_list)


    def cal_umsatz5():

        nonlocal cl_list_list, lvcarea, do_it, droomrev, mroomrev, yroomrev, droomexc, mroomexc, yroomexc, tot_room, all_room, dvacant, dooo, mvacant, mooo, yvacant, yooo, dnoshow, dcancel, mnoshow, mcancel, ynoshow, ycancel, droom, proz1, mroom, proz2, dpax, mpax, drate, mrate, drev, mrev, yroom, ypax, yrate, yrev, from_bez, to_bez, inactive, mtd_act, mtd_totrm, ytd_act, ytd_totrm, ncompli, mtd_ncompli, ytd_ncompli, dcompli, mcompli, ycompli, dhu, mhu, yhu, ci_date, htparam, zimmer, zkstat, zinrstat, genstat, segment, guestseg, reservation, res_line, outorder, artikel, umsatz
        nonlocal bgenstat


        nonlocal cl_list, bgenstat
        nonlocal cl_list_list

        i:int = 0
        datum:date = None
        datum1:date = None
        dooo = 0
        mooo = 0
        yooo = 0
        for datum in range(from_date,to_date + 1) :

            outorder_obj_list = []
            for outorder, zimmer in db_session.query(Outorder, Zimmer).join(Zimmer,(Zimmer.zinr == Outorder.zinr)).filter(
                    ((Outorder.gespstart >= datum) &  (Outorder.gespstart <= datum)) |  ((Outorder.gespstart <= datum) &  (Outorder.gespende >= datum))).all():
                if outorder._recid in outorder_obj_list:
                    continue
                else:
                    outorder_obj_list.append(outorder._recid)

                if datum == to_date:
                    dooo = dooo + 1

                if (mi_mtd_chk and get_month(datum) == get_month(to_date)):
                    mooo = mooo + 1
                yooo = yooo + 1
        dvacant = tot_room - dooo - droom
        mvacant = mtd_act - mooo - mroom
        yvacant = ytd_act - yooo - yroom

        if to_date == opening_date:
            mvacant = dvacant
            yvacant = dvacant
            mooo = dooo
            yooo = dooo
        cl_list = Cl_list()
        cl_list_list.append(cl_list)

        cl_list.bezeich = "V A C A N T"
        cl_list.droom = dvacant
        cl_list.proz1 = dvacant / tot_room * 100
        cl_list.mroom = mvacant
        cl_list.proz2 = mvacant / mtd_act * 100
        cl_list.yroom = yvacant
        cl_list.proz3 = yvacant / ytd_act * 100


        cl_list = Cl_list()
        cl_list_list.append(cl_list)

        cl_list.bezeich = "Out Of Order"
        cl_list.droom = dooo
        cl_list.proz1 = dooo / tot_room * 100
        cl_list.mroom = mooo
        cl_list.proz2 = mooo / mtd_act * 100
        cl_list.yroom = yooo
        cl_list.proz3 = yooo / ytd_act * 100


        cl_list = Cl_list()
        cl_list_list.append(cl_list)


        if to_date < ci_date:

            zinrstat = db_session.query(Zinrstat).filter(
                    (func.lower(Zinrstat.zinr) == "tot_rm") &  (Zinrstat.datum == to_date)).first()

            if zinrstat:
                all_room = zinrstat.zimmeranz
        else:

            for zimmer in db_session.query(Zimmer).all():
                all_room = all_room + 1


        cl_list = Cl_list()
        cl_list_list.append(cl_list)

        cl_list.bezeich = "# Active Rooms"
        cl_list.droom = tot_room
        cl_list.proz1 = 100
        cl_list.mroom = mtd_act
        cl_list.proz2 = 100
        cl_list.yroom = ytd_act
        cl_list.proz3 = 100


        cl_list = Cl_list()
        cl_list_list.append(cl_list)

        cl_list.bezeich = "inactive Rooms"
        cl_list.droom = all_room - tot_room
        cl_list.mroom = mtd_totrm - mtd_act
        cl_list.yroom = ytd_totrm - ytd_act


        cl_list = Cl_list()
        cl_list_list.append(cl_list)

        cl_list.bezeich = "Total Rooms"
        cl_list.droom = all_room
        cl_list.mroom = mtd_totrm
        cl_list.yroom = ytd_totrm


        cl_list = Cl_list()
        cl_list_list.append(cl_list)


    def cal_umsatz6():

        nonlocal cl_list_list, lvcarea, do_it, droomrev, mroomrev, yroomrev, droomexc, mroomexc, yroomexc, tot_room, all_room, dvacant, dooo, mvacant, mooo, yvacant, yooo, dnoshow, dcancel, mnoshow, mcancel, ynoshow, ycancel, droom, proz1, mroom, proz2, dpax, mpax, drate, mrate, drev, mrev, yroom, ypax, yrate, yrev, from_bez, to_bez, inactive, mtd_act, mtd_totrm, ytd_act, ytd_totrm, ncompli, mtd_ncompli, ytd_ncompli, dcompli, mcompli, ycompli, dhu, mhu, yhu, ci_date, htparam, zimmer, zkstat, zinrstat, genstat, segment, guestseg, reservation, res_line, outorder, artikel, umsatz
        nonlocal bgenstat


        nonlocal cl_list, bgenstat
        nonlocal cl_list_list

        i:int = 0
        max_i:int = 0
        datum:date = None
        art_list:[int] = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        serv_vat:bool = False
        fact:decimal = 0
        serv:decimal = 0
        vat:decimal = 0
        drev_droom:decimal = 0
        mrev_mroom:decimal = 0
        drev_droom1:decimal = 0
        mrev_mroom1:decimal = 0

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 479)).first()
        serv_vat = htparam.flogical

        for artikel in db_session.query(Artikel).filter(
                (Artikel.departement == 0) &  (Artikel.artart == 0) &  (Artikel.umsatzart == 1)).all():
            max_i = max_i + 1
            art_list[max_i - 1] = artikel.artnr

        if do_it:
            pass
        else:
            for i in range(1,max_i + 1) :

                artikel = db_session.query(Artikel).filter(
                        (Artikel.artnr == art_list[i - 1]) &  (Artikel.departement == 0)).first()

                if artikel:
                    cl_list = Cl_list()
                    cl_list_list.append(cl_list)

                    cl_list.segm = 9999999

                    if i >= 10:
                        cl_list.bezeich = translateExtended ("Other RmRev", lvcarea, "")
                    else:
                        cl_list.bezeich = artikel.bezeich
                    for datum in range(from_date,to_date + 1) :
                        serv = 0
                        vat = 0

                        for umsatz in db_session.query(Umsatz).filter(
                                (Umsatz.artnr == artikel.artnr) &  (Umsatz.departement == artikel.departement) &  (Umsatz.datum == datum)).all():
                            serv, vat = get_output(calc_servvat(umsatz.departement, umsatz.artnr, umsatz.datum, artikel.service_code, artikel.mwst_code))
                            fact = 1.00 + serv + vat

                            if datum == to_date:
                                drev = drev + umsatz.betrag / fact
                                cl_list.drev = umsatz.betrag / fact

                            if (mi_mtd_chk and get_month(datum) == get_month(to_date)) or (mi_ftd_chk and datum >= fdate and datum <= tdate):
                                mrev = mrev + umsatz.betrag / fact
                                cl_list.mrev = cl_list.mrev + umsatz.betrag / fact
                            yrev = yrev + umsatz.betrag / fact


                            cl_list.yrev = cl_list.yrev + umsatz.betrag / fact

                    if cl_list.mrev == 0:
                        cl_list.bezeich = "Deleted"
            cl_list = Cl_list()
            cl_list_list.append(cl_list)


        if mi_exchu_chk :
            ncompli = ncompli - dhu
            mtd_ncompli = mtd_ncompli - mhu
            ytd_ncompli = ytd_ncompli - yhu

        if mi_exccomp_chk :
            ncompli = ncompli - dcompli
            mtd_ncompli = mtd_ncompli - mcompli
            ytd_ncompli = ytd_ncompli - ycompli


        drev_droom = drev / droom
        drev_droom1 = drev / droomrev

        if drev_droom == None:
            drev_droom = 0

        if drev_droom1 == None:
            drev_droom1 = 0
        mrev_mroom = mrev / mroom
        mrev_mroom1 = mrev / mroomrev

        if mrev_mroom == None:
            mrev_mroom = 0

        if mrev_mroom1 == None:
            mrev_mroom1 = 0

        if not long_digit:
            cl_list = Cl_list()
            cl_list_list.append(cl_list)

            cl_list.bezeich = "RmRev Inc Comp"
            cl_list.drate = drev_droom
            cl_list.mrate = mrev_mroom
            cl_list.drev = drev
            cl_list.mrev = mrev
            cl_list.yrev = yrev

            if yroom != 0:
                cl_list.yrate = yrev / yroom
            cl_list = Cl_list()
            cl_list_list.append(cl_list)

            cl_list.bezeich = "RmRev Exc Comp"
            cl_list.drate = drev_droom1
            cl_list.mrate = mrev_mroom1
            cl_list.drev = drev
            cl_list.mrev = mrev
            cl_list.yrev = yrev

            if yroomrev != 0:
                cl_list.yrate = yrev / yroomrev
        else:
            cl_list = Cl_list()
            cl_list_list.append(cl_list)

            cl_list.bezeich = "Total RmRevenue (comp guest)"
            cl_list.drate = drev_droom
            cl_list.mrate = mrev_mroom
            cl_list.drev = drev
            cl_list.mrev = mrev
            cl_list.yrev = yrev


            cl_list = Cl_list()
            cl_list_list.append(cl_list)

            cl_list.bezeich = "Total RmRevenue (Paying Guest)"
            cl_list.drate = drev_droom1
            cl_list.mrate = mrev_mroom1
            cl_list.drev = drev
            cl_list.mrev = mrev
            cl_list.yrev = yrev


        cl_list = Cl_list()
        cl_list_list.append(cl_list)


    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 186)).first()
    opening_date = htparam.fdate

    if get_month(to_date) == get_month(opening_date) and get_year(to_date) == get_year(opening_date):
        from_date = opening_date

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 87)).first()
    ci_date = htparam.fdate

    if from_date < ci_date:
        create_umsatz()
    else:
        create_umsatz1()

    for cl_list in query(cl_list_list, filters=(lambda cl_list :cl_list.bezeich.lower()  == "Deleted")):
        cl_list_list.remove(cl_list)

    return generate_output()