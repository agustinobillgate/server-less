#using conversion tools version: 1.0.0.117
#-----------------------------------------
# Rd, 29/7/2025
# gitlab: 111
# error konversi, # mtd_totrm = 0 mtd_act == 0 ytd_act == 0 ytd_totrm == 0
#-----------------------------------------
from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from functions.get_room_breakdown import get_room_breakdown
from functions.calc_servvat import calc_servvat
from models import Htparam, Zimmer, Zkstat, Zinrstat, Genstat, Segment, Guestseg, Reservation, Res_line, Outorder, Artikel, Umsatz

def rm_drecap2_webbl(pvilanguage:int, opening_date:date, from_date:date, to_date:date, fdate:date, tdate:date, segmtype_exist:bool, mi_mtd_chk:bool, mi_ftd_chk:bool, mi_exchu_chk:bool, mi_exccomp_chk:bool, long_digit:bool):

    prepare_cache ([Htparam, Zkstat, Zinrstat, Genstat, Segment, Guestseg, Reservation, Res_line, Outorder, Artikel, Umsatz])

    cl_list_data = []
    lvcarea:string = "rm-drecap2"
    do_it:bool = False
    droomrev:int = 0
    mroomrev:int = 0
    yroomrev:int = 0
    drevrev:Decimal = to_decimal("0.0")
    mrevrev:Decimal = to_decimal("0.0")
    yrevrev:Decimal = to_decimal("0.0")
    dpaxrev:int = 0
    mpaxrev:int = 0
    ypaxrev:int = 0
    draterev:Decimal = to_decimal("0.0")
    mraterev:Decimal = to_decimal("0.0")
    yraterev:Decimal = to_decimal("0.0")
    droomcomp:int = 0
    mroomcomp:int = 0
    yroomcomp:int = 0
    dpaxcomp:int = 0
    mpaxcomp:int = 0
    ypaxcomp:int = 0
    droomhu:int = 0
    mroomhu:int = 0
    yroomhu:int = 0
    dpaxhu:int = 0
    mpaxhu:int = 0
    ypaxhu:int = 0
    tot_room:int = 0
    all_room:int = 0
    dvacant:int = 0
    mvacant:int = 0
    yvacant:int = 0
    dooo:int = 0
    mooo:int = 0
    yooo:int = 0
    dnoshow:int = 0
    mnoshow:int = 0
    ynoshow:int = 0
    dcancel:int = 0
    mcancel:int = 0
    ycancel:int = 0
    cal_umsatz1_called:bool = False
    cal_umsatz4_called:bool = False
    droom:int = 0
    proz1:Decimal = to_decimal("0.0")
    mroom:int = 0
    proz2:int = 0
    dpax:int = 0
    mpax:int = 0
    drate:Decimal = to_decimal("0.0")
    mrate:Decimal = to_decimal("0.0")
    drev:Decimal = to_decimal("0.0")
    mrev:Decimal = to_decimal("0.0")
    yroom:int = 0
    ypax:int = 0
    yrate:Decimal = to_decimal("0.0")
    yrev:Decimal = to_decimal("0.0")
    inactive:int = 0
    mtd_act:int = 0
    mtd_totrm:int = 0
    ytd_act:int = 0
    ytd_totrm:int = 0
    ci_date:date = None
    htparam = zimmer = zkstat = zinrstat = genstat = segment = guestseg = reservation = res_line = outorder = artikel = umsatz = None

    cl_list = om_list = None

    cl_list_data, Cl_list = create_model("Cl_list", {"segm":int, "betriebsnr":int, "compli":bool, "bezeich":string, "droom":int, "proz1":Decimal, "mroom":int, "proz2":Decimal, "dpax":int, "mpax":int, "drate":Decimal, "mrate":Decimal, "drev":Decimal, "mrev":Decimal, "yroom":int, "proz3":Decimal, "ypax":int, "yrate":Decimal, "yrev":Decimal, "zero_flag":bool})
    om_list_data, Om_list = create_model("Om_list", {"zinr":string, "userinit":string, "ind":int, "reason":string, "gespstart":date, "gespende":date})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal cl_list_data, lvcarea, do_it, droomrev, mroomrev, yroomrev, drevrev, mrevrev, yrevrev, dpaxrev, mpaxrev, ypaxrev, draterev, mraterev, yraterev, droomcomp, mroomcomp, yroomcomp, dpaxcomp, mpaxcomp, ypaxcomp, droomhu, mroomhu, yroomhu, dpaxhu, mpaxhu, ypaxhu, tot_room, all_room, dvacant, mvacant, yvacant, dooo, mooo, yooo, dnoshow, mnoshow, ynoshow, dcancel, mcancel, ycancel, cal_umsatz1_called, cal_umsatz4_called, droom, proz1, mroom, proz2, dpax, mpax, drate, mrate, drev, mrev, yroom, ypax, yrate, yrev, inactive, mtd_act, mtd_totrm, ytd_act, ytd_totrm, ci_date, htparam, zimmer, zkstat, zinrstat, genstat, segment, guestseg, reservation, res_line, outorder, artikel, umsatz
        nonlocal pvilanguage, opening_date, from_date, to_date, fdate, tdate, segmtype_exist, mi_mtd_chk, mi_ftd_chk, mi_exchu_chk, mi_exccomp_chk, long_digit


        nonlocal cl_list, om_list
        nonlocal cl_list_data, om_list_data

        return {"cl-list": cl_list_data}

    def create_umsatz1():

        nonlocal cl_list_data, lvcarea, do_it, droomrev, mroomrev, yroomrev, drevrev, mrevrev, yrevrev, dpaxrev, mpaxrev, ypaxrev, draterev, mraterev, yraterev, droomcomp, mroomcomp, yroomcomp, dpaxcomp, mpaxcomp, ypaxcomp, droomhu, mroomhu, yroomhu, dpaxhu, mpaxhu, ypaxhu, tot_room, all_room, dvacant, mvacant, yvacant, dooo, mooo, yooo, dnoshow, mnoshow, ynoshow, dcancel, mcancel, ycancel, cal_umsatz1_called, cal_umsatz4_called, droom, proz1, mroom, proz2, dpax, mpax, drate, mrate, drev, mrev, yroom, ypax, yrate, yrev, inactive, mtd_act, mtd_totrm, ytd_act, ytd_totrm, ci_date, htparam, zimmer, zkstat, zinrstat, genstat, segment, guestseg, reservation, res_line, outorder, artikel, umsatz
        nonlocal pvilanguage, opening_date, from_date, to_date, fdate, tdate, segmtype_exist, mi_mtd_chk, mi_ftd_chk, mi_exchu_chk, mi_exccomp_chk, long_digit


        nonlocal cl_list, om_list
        nonlocal cl_list_data, om_list_data

        i:int = 0
        datum:date = None
        black_list:int = 0

        htparam = get_cache (Htparam, {"paramnr": [(eq, 709)]})
        black_list = htparam.finteger
        cl_list_data.clear()
        droom = 0
        mroom = 0
        yroom = 0
        dpax = 0
        mpax = 0
        ypax = 0
        drev =  to_decimal("0")
        mrev =  to_decimal("0")
        yrev =  to_decimal("0")
        tot_room = 0
        inactive = 0
        mtd_act = 0
        ytd_act = 0
        mtd_totrm = 0
        ytd_totrm = 0

        for zimmer in db_session.query(Zimmer).filter(
                 not_ (Zimmer.sleeping)).order_by(Zimmer._recid).all():
            inactive = inactive + 1

        for zimmer in db_session.query(Zimmer).filter(
                 (Zimmer.sleeping)).order_by(Zimmer._recid).all():
            tot_room = tot_room + 1
        count_mtd_totrm1()

        if not segmtype_exist:
            cal_umsatz4(1, 12, 15, 49, translateExtended ("Room Revenue", lvcarea, ""), "", True)
            cal_umsatz4(13, 14, 0, 0, translateExtended ("Total Room Occ", lvcarea, ""), translateExtended (" Double Occupancy", lvcarea, ""), False)
        else:
            cal_umsatz4a(0, 0, translateExtended ("Room Revenue", lvcarea, ""), "", True)
            cal_umsatz4b(1, 2, translateExtended ("Total Room Occ", lvcarea, ""), translateExtended (" Double Occupancy", lvcarea, ""), False)
        cal_umsatz5()
        cal_umsatz6()


    def create_umsatz():

        nonlocal cl_list_data, lvcarea, do_it, droomrev, mroomrev, yroomrev, drevrev, mrevrev, yrevrev, dpaxrev, mpaxrev, ypaxrev, draterev, mraterev, yraterev, droomcomp, mroomcomp, yroomcomp, dpaxcomp, mpaxcomp, ypaxcomp, droomhu, mroomhu, yroomhu, dpaxhu, mpaxhu, ypaxhu, tot_room, all_room, dvacant, mvacant, yvacant, dooo, mooo, yooo, dnoshow, mnoshow, ynoshow, dcancel, mcancel, ycancel, cal_umsatz1_called, cal_umsatz4_called, droom, proz1, mroom, proz2, dpax, mpax, drate, mrate, drev, mrev, yroom, ypax, yrate, yrev, inactive, mtd_act, mtd_totrm, ytd_act, ytd_totrm, ci_date, htparam, zimmer, zkstat, zinrstat, genstat, segment, guestseg, reservation, res_line, outorder, artikel, umsatz
        nonlocal pvilanguage, opening_date, from_date, to_date, fdate, tdate, segmtype_exist, mi_mtd_chk, mi_ftd_chk, mi_exchu_chk, mi_exccomp_chk, long_digit


        nonlocal cl_list, om_list
        nonlocal cl_list_data, om_list_data

        i:int = 0
        datum:date = None
        black_list:int = 0

        htparam = get_cache (Htparam, {"paramnr": [(eq, 709)]})
        black_list = htparam.finteger
        cl_list_data.clear()
        droom = 0
        mroom = 0
        yroom = 0
        dpax = 0
        mpax = 0
        ypax = 0
        drev =  to_decimal("0")
        mrev =  to_decimal("0")
        yrev =  to_decimal("0")
        tot_room = 0
        inactive = 0
        mtd_act = 0
        ytd_act = 0
        mtd_totrm = 0
        ytd_totrm = 0

        for zimmer in db_session.query(Zimmer).filter(
                 not_ (Zimmer.sleeping)).order_by(Zimmer._recid).all():
            inactive = inactive + 1

        if to_date < ci_date:

            for zkstat in db_session.query(Zkstat).filter(
                     (Zkstat.datum == to_date)).order_by(Zkstat._recid).all():
                tot_room = tot_room + zkstat.anz100
        else:

            for zimmer in db_session.query(Zimmer).filter(
                     (Zimmer.sleeping)).order_by(Zimmer._recid).all():
                tot_room = tot_room + 1
        count_mtd_totrm()

        if not segmtype_exist:
            cal_umsatz1(1, 12, 15, 49, translateExtended ("Room Revenue", lvcarea, ""), "", True)
            cal_umsatz1(13, 14, 0, 0, translateExtended ("Total Room Occ", lvcarea, ""), translateExtended (" Double Occupancy", lvcarea, ""), False)
        else:
            cal_umsatz1a(0, 0, translateExtended ("Room Revenue", lvcarea, ""), "", True)
            cal_umsatz1b(1, 2, translateExtended ("Total Room Occ", lvcarea, ""), translateExtended (" Double Occupancy", lvcarea, ""), False)
        cal_umsatz2()
        cal_umsatz3()
        no_show()


    def count_mtd_totrm1():

        nonlocal cl_list_data, lvcarea, do_it, droomrev, mroomrev, yroomrev, drevrev, mrevrev, yrevrev, dpaxrev, mpaxrev, ypaxrev, draterev, mraterev, yraterev, droomcomp, mroomcomp, yroomcomp, dpaxcomp, mpaxcomp, ypaxcomp, droomhu, mroomhu, yroomhu, dpaxhu, mpaxhu, ypaxhu, tot_room, all_room, dvacant, mvacant, yvacant, dooo, mooo, yooo, dnoshow, mnoshow, ynoshow, dcancel, mcancel, ycancel, cal_umsatz1_called, cal_umsatz4_called, droom, proz1, mroom, proz2, dpax, mpax, drate, mrate, drev, mrev, yroom, ypax, yrate, yrev, inactive, mtd_act, mtd_totrm, ytd_act, ytd_totrm, ci_date, htparam, zimmer, zkstat, zinrstat, genstat, segment, guestseg, reservation, res_line, outorder, artikel, umsatz
        nonlocal pvilanguage, opening_date, from_date, to_date, fdate, tdate, segmtype_exist, mi_mtd_chk, mi_ftd_chk, mi_exchu_chk, mi_exccomp_chk, long_digit


        nonlocal cl_list, om_list
        nonlocal cl_list_data, om_list_data

        datum:date = None
        tot1:int = 0
        glob_tot:int = 0

        # Rd 29/7/2025
        # mtd_totrm = 0 mtd_act == 0 ytd_act == 0 ytd_totrm == 0
        mtd_totrm = mtd_act = ytd_act = ytd_totrm == 0

        for zimmer in db_session.query(Zimmer).filter(
                 (Zimmer.sleeping)).order_by(Zimmer._recid).all():
            glob_tot = glob_tot + 1
        for datum in date_range(from_date,to_date) :
            tot1 = 0

            for zimmer in db_session.query(Zimmer).filter(
                     (Zimmer.sleeping)).order_by(Zimmer._recid).all():
                tot1 = tot1 + 1

            if tot1 == 0:
                tot1 = glob_tot

            if (mi_mtd_chk and get_month(datum) == get_month(to_date)) or (mi_ftd_chk and (datum >= fdate and datum <= tdate)):
                mtd_act = mtd_act + tot1
            ytd_act = ytd_act + tot1

            for zimmer in db_session.query(Zimmer).order_by(Zimmer._recid).all():

                if (mi_mtd_chk and get_month(datum) == get_month(to_date)) or (mi_ftd_chk and datum >= fdate and datum <= tdate):
                    mtd_totrm = mtd_totrm + 1
                ytd_totrm = ytd_totrm + 1


    def count_mtd_totrm():

        nonlocal cl_list_data, lvcarea, do_it, droomrev, mroomrev, yroomrev, drevrev, mrevrev, yrevrev, dpaxrev, mpaxrev, ypaxrev, draterev, mraterev, yraterev, droomcomp, mroomcomp, yroomcomp, dpaxcomp, mpaxcomp, ypaxcomp, droomhu, mroomhu, yroomhu, dpaxhu, mpaxhu, ypaxhu, tot_room, all_room, dvacant, mvacant, yvacant, dooo, mooo, yooo, dnoshow, mnoshow, ynoshow, dcancel, mcancel, ycancel, cal_umsatz1_called, cal_umsatz4_called, droom, proz1, mroom, proz2, dpax, mpax, drate, mrate, drev, mrev, yroom, ypax, yrate, yrev, inactive, mtd_act, mtd_totrm, ytd_act, ytd_totrm, ci_date, htparam, zimmer, zkstat, zinrstat, genstat, segment, guestseg, reservation, res_line, outorder, artikel, umsatz
        nonlocal pvilanguage, opening_date, from_date, to_date, fdate, tdate, segmtype_exist, mi_mtd_chk, mi_ftd_chk, mi_exchu_chk, mi_exccomp_chk, long_digit


        nonlocal cl_list, om_list
        nonlocal cl_list_data, om_list_data

        datum:date = None
        tot1:int = 0
        glob_tot:int = 0

        # Rd 29/7/2025
        # mtd_totrm = 0 mtd_act == 0 ytd_act == 0 ytd_totrm == 0
        mtd_totrm = mtd_act = ytd_act = ytd_totrm == 0

        for zimmer in db_session.query(Zimmer).filter(
                 (Zimmer.sleeping)).order_by(Zimmer._recid).all():
            glob_tot = glob_tot + 1
        for datum in date_range(from_date,to_date) :
            tot1 = 0

            for zkstat in db_session.query(Zkstat).filter(
                     (Zkstat.datum == datum)).order_by(Zkstat._recid).all():
                tot1 = tot1 + zkstat.anz100

            if tot1 == 0:
                tot1 = glob_tot

            if (mi_mtd_chk and get_month(datum) == get_month(to_date)) or (mi_ftd_chk and datum >= fdate and datum <= tdate):
                mtd_act = mtd_act + tot1
            ytd_act = ytd_act + tot1

            zinrstat = get_cache (Zinrstat, {"zinr": [(eq, "tot-rm")],"datum": [(eq, datum)]})

            if zinrstat:

                if (mi_mtd_chk and get_month(datum) == get_month(to_date)) or (mi_ftd_chk and datum >= fdate and datum <= tdate):
                    mtd_totrm = mtd_totrm + zinrstat.zimmeranz
                ytd_totrm = ytd_totrm + zinrstat.zimmeranz
            else:

                if (mi_mtd_chk and get_month(datum) == get_month(to_date)) or (mi_ftd_chk and datum >= fdate and datum <= tdate):
                    mtd_totrm = mtd_totrm + glob_tot + inactive
                ytd_totrm = ytd_totrm + glob_tot + inactive


    def cal_umsatz1(i1:int, i2:int, i3:int, i4:int, rev_title:string, rev_title1:string, show_avrg:bool):

        nonlocal cl_list_data, lvcarea, do_it, droomrev, mroomrev, yroomrev, drevrev, mrevrev, yrevrev, dpaxrev, mpaxrev, ypaxrev, draterev, mraterev, yraterev, droomcomp, mroomcomp, yroomcomp, dpaxcomp, mpaxcomp, ypaxcomp, droomhu, mroomhu, yroomhu, dpaxhu, mpaxhu, ypaxhu, tot_room, all_room, dvacant, mvacant, yvacant, dooo, mooo, yooo, dnoshow, mnoshow, ynoshow, dcancel, mcancel, ycancel, cal_umsatz1_called, cal_umsatz4_called, droom, proz1, mroom, proz2, dpax, mpax, drate, mrate, drev, mrev, yroom, ypax, yrate, yrev, inactive, mtd_act, mtd_totrm, ytd_act, ytd_totrm, ci_date, htparam, zimmer, zkstat, zinrstat, genstat, segment, guestseg, reservation, res_line, outorder, artikel, umsatz
        nonlocal pvilanguage, opening_date, from_date, to_date, fdate, tdate, segmtype_exist, mi_mtd_chk, mi_ftd_chk, mi_exchu_chk, mi_exccomp_chk, long_digit


        nonlocal cl_list, om_list
        nonlocal cl_list_data, om_list_data

        i:int = 0
        datum:date = None
        do_it1:bool = False
        d1:date = None
        d2:date = None
        datum0:date = None
        datum1:date = None
        datum2:date = None
        curr_i:int = 0
        net_lodg:Decimal = to_decimal("0.0")
        fnet_lodg:Decimal = to_decimal("0.0")
        tot_breakfast:Decimal = to_decimal("0.0")
        tot_lunch:Decimal = to_decimal("0.0")
        tot_dinner:Decimal = to_decimal("0.0")
        tot_other:Decimal = to_decimal("0.0")
        tot_rmrev:Decimal = to_decimal("0.0")
        tot_vat:Decimal = to_decimal("0.0")
        tot_service:Decimal = to_decimal("0.0")
        bgenstat = None
        Bgenstat =  create_buffer("Bgenstat",Genstat)
        d1 = from_date

        if to_date < (ci_date - timedelta(days=1)):
            d2 = to_date
        else:
            d2 = ci_date - timedelta(days=1)

        for segment in db_session.query(Segment).filter(
                 (((Segment.segmentcode >= i1) & (Segment.segmentcode <= i2)) | ((Segment.segmentcode >= i3) & (Segment.segmentcode <= i4)))).order_by(Segment.segmentcode).all():

            bgenstat = db_session.query(Bgenstat).filter(
                     (Bgenstat.segmentcode == segment.segmentcode) & (Bgenstat.datum >= d1) & (Bgenstat.datum <= d2) & (Bgenstat.resstatus != 13) & (Bgenstat.gratis == 0) & (Bgenstat.segmentcode != 0) & (Bgenstat.nationnr != 0) & (Bgenstat.zinr != "") & (Bgenstat.res_logic[inc_value(1)])).first()

            if bgenstat:
                do_it1 = True


            else:

                if matches(segment.bezeich,r"*$$0"):
                    do_it1 = False


                else:
                    do_it1 = True

            if do_it1:
                cl_list = Cl_list()
                cl_list_data.append(cl_list)

                cl_list.segm = segment.segmentcode
                cl_list.bezeich = entry(0, segment.bezeich, "$$0")

                for genstat in db_session.query(Genstat).filter(
                         (Genstat.segmentcode == segment.segmentcode) & (Genstat.datum >= d1) & (Genstat.datum <= d2) & (Genstat.resstatus != 13) & (Genstat.gratis == 0) & (Genstat.segmentcode != 0) & (Genstat.nationnr != 0) & (Genstat.zinr != "") & (Genstat.res_logic[inc_value(1)])).order_by(Genstat._recid).all():

                    if genstat.datum == to_date:
                        cl_list.droom = cl_list.droom + 1
                        cl_list.dpax = cl_list.dpax + genstat.erwachs + genstat.kind1 + genstat.kind2 + genstat.gratis
                        cl_list.drev =  to_decimal(cl_list.drev) + to_decimal(genstat.logis)
                        droomrev = droomrev + 1
                        dpaxrev = dpaxrev + genstat.erwachs + genstat.kind1 + genstat.kind2 + genstat.gratis
                        drevrev =  to_decimal(drevrev) + to_decimal(genstat.logis)

                    if (mi_mtd_chk and get_month(genstat.datum) == get_month(d2)) or (mi_ftd_chk and genstat.datum >= d1 and genstat.datum <= d2):
                        cl_list.mroom = cl_list.mroom + 1
                        cl_list.mpax = cl_list.mpax + genstat.erwachs + genstat.kind1 + genstat.kind2 + genstat.gratis
                        cl_list.mrev =  to_decimal(cl_list.mrev) + to_decimal(genstat.logis)
                        mroomrev = mroomrev + 1
                        mpaxrev = mpaxrev + genstat.erwachs + genstat.kind1 + genstat.kind2 + genstat.gratis
                        mrevrev =  to_decimal(mrevrev) + to_decimal(genstat.logis)
                    cl_list.yroom = cl_list.yroom + 1
                    cl_list.ypax = cl_list.ypax + genstat.erwachs + genstat.kind1 + genstat.kind2 + genstat.gratis
                    cl_list.yrev =  to_decimal(cl_list.yrev) + to_decimal(genstat.logis)
                    yroomrev = yroomrev + 1
                    ypaxrev = ypaxrev + genstat.erwachs + genstat.kind1 + genstat.kind2 + genstat.gratis


                    yrevrev =  to_decimal(yrevrev) + to_decimal(genstat.logis)

        if do_it:

            for genstat in db_session.query(Genstat).filter(
                     (Genstat.datum >= d1) & (Genstat.datum <= d2) & (Genstat.segmentcode != 0) & (Genstat.nationnr != 0) & (Genstat.zinr != "") & (Genstat.resstatus != 13) & (Genstat.res_logic[inc_value(1)])).order_by(Genstat._recid).all():

                segment = get_cache (Segment, {"segmentcode": [(eq, genstat.segmentcode)]})

                if segment:

                    cl_list = query(cl_list_data, filters=(lambda cl_list: cl_list.segm == segment.segmentcode), first=True)

                    if cl_list:

                        if genstat.datum == to_date:
                            cl_list.drev =  to_decimal(cl_list.drev) + to_decimal(genstat.res_deci[0])
                            drevrev =  to_decimal(drevrev) + to_decimal(genstat.logis)

                        if (mi_mtd_chk and get_month(genstat.datum) == get_month(d2)) or (mi_ftd_chk and genstat.datum >= d1 and genstat.datum <= d2):
                            cl_list.mrev =  to_decimal(cl_list.mrev) + to_decimal(genstat.res_deci[0])
                            mrevrev =  to_decimal(mrevrev) + to_decimal(genstat.logis)
                else:

                    guestseg = get_cache (Guestseg, {"gastnr": [(eq, genstat.gastnr)]})

                    if guestseg:

                        if guestseg.reihenfolge == 1:

                            cl_list = query(cl_list_data, filters=(lambda cl_list: cl_list.segm == segment.segmentcode), first=True)

                            if cl_list:

                                if genstat.datum == to_date:
                                    cl_list.drev =  to_decimal(cl_list.drev) + to_decimal(genstat.res_deci[0])
                                    drevrev =  to_decimal(drevrev) + to_decimal(genstat.logis)

                                if (mi_mtd_chk and get_month(genstat.datum) == get_month(d2)) or (mi_ftd_chk and genstat.datum >= d1 and genstat.datum <= d2):
                                    cl_list.mrev =  to_decimal(cl_list.mrev) + to_decimal(genstat.res_deci[0])
                                    mrevrev =  to_decimal(mrevrev) + to_decimal(genstat.logis)
                        else:

                            guestseg = get_cache (Guestseg, {"reihenfolge": [(eq, 0)]})

                            if guestseg:

                                cl_list = query(cl_list_data, filters=(lambda cl_list: cl_list.segm == guestseg.segmentcode), first=True)

                                if cl_list:

                                    if genstat.datum == to_date:
                                        cl_list.drev =  to_decimal(cl_list.drev) + to_decimal(genstat.res_deci[0])
                                        drevrev =  to_decimal(drevrev) + to_decimal(genstat.logis)

                                    if (mi_mtd_chk and get_month(genstat.datum) == get_month(d2)) or (mi_ftd_chk and genstat.datum >= d1 and genstat.datum <= d2):
                                        cl_list.mrev =  to_decimal(cl_list.mrev) + to_decimal(genstat.res_deci[0])
                                        mrevrev =  to_decimal(mrevrev) + to_decimal(genstat.logis)

        if (not cal_umsatz1_called) and (to_date >= ci_date):
            d2 = d2 + timedelta(days=1)

            res_line_obj_list = {}
            res_line = Res_line()
            reservation = Reservation()
            for res_line.ankunft, res_line.abreise, res_line._recid, res_line.zimmeranz, res_line.erwachs, res_line.kind1, res_line.kind2, res_line.gratis, res_line.kontignr, reservation.segmentcode, reservation._recid in db_session.query(Res_line.ankunft, Res_line.abreise, Res_line._recid, Res_line.zimmeranz, Res_line.erwachs, Res_line.kind1, Res_line.kind2, Res_line.gratis, Res_line.kontignr, Reservation.segmentcode, Reservation._recid).join(Reservation,(Reservation.resnr == Res_line.resnr)).filter(
                     (((Res_line.resstatus <= 13) & (Res_line.resstatus != 4) & (Res_line.resstatus != 8) & (Res_line.resstatus != 9) & (Res_line.resstatus != 10) & (Res_line.resstatus != 12) & (Res_line.active_flag <= 1) & (not_ (Res_line.ankunft > to_date)) & (not_ (Res_line.abreise < d2)))) | ((Res_line.resstatus == 8) & (Res_line.active_flag == 2) & (Res_line.ankunft == ci_date) & (Res_line.abreise == ci_date)) & (Res_line.gastnr > 0) & (Res_line.l_zuordnung[inc_value(2)] == 0)).order_by(Res_line.resnr, Res_line.reslinnr.desc()).all():
                if res_line_obj_list.get(res_line._recid):
                    continue
                else:
                    res_line_obj_list[res_line._recid] = True


                curr_i = 0

                if res_line.kontignr < 0:
                    do_it1 = True

                    cl_list = query(cl_list_data, filters=(lambda cl_list: cl_list.segm == reservation.segmentcode), first=True)

                    if not cl_list:

                        segment = get_cache (Segment, {"segmentcode": [(eq, reservation.segmentcode)]})

                        if segment and not matches(segment.bezeich,r"*$$0"):

                            if segment.betriebsnr != 1 and segment.betriebsnr != 2:
                                cl_list = Cl_list()
                                cl_list_data.append(cl_list)

                                cl_list.compli = False
                                cl_list.segm = segment.segmentcode
                                cl_list.bezeich = segment.bezeich
                                cl_list.betriebsnr = segment.betriebsnr
                            else:
                                cl_list = Cl_list()
                                cl_list_data.append(cl_list)

                                cl_list.compli = True
                                cl_list.segm = segment.segmentcode
                                cl_list.bezeich = segment.bezeich
                                cl_list.betriebsnr = segment.betriebsnr
                        else:
                            do_it1 = False

                    if do_it1 :
                        datum1 = d2

                        if res_line.ankunft > datum1:
                            datum1 = res_line.ankunft
                        datum2 = to_date

                        if res_line.abreise < datum2:
                            datum2 = res_line.abreise
                        for datum0 in date_range(datum1,datum2) :
                            curr_i = curr_i + 1

                            if datum0 == res_line.abreise:
                                pass
                            else:
                                net_lodg =  to_decimal("0")
                                tot_breakfast =  to_decimal("0")
                                tot_lunch =  to_decimal("0")
                                tot_dinner =  to_decimal("0")
                                tot_other =  to_decimal("0")


                                fnet_lodg, net_lodg, tot_breakfast, tot_lunch, tot_dinner, tot_other, tot_rmrev, tot_vat, tot_service = get_output(get_room_breakdown(res_line._recid, datum0, curr_i, from_date))

                                if datum0 == to_date:
                                    cl_list.droom = cl_list.droom + res_line.zimmeranz
                                    cl_list.dpax = cl_list.dpax + res_line.erwachs + res_line.kind1 + res_line.kind2 + res_line.gratis
                                    cl_list.drev =  to_decimal(cl_list.drev) + to_decimal(net_lodg)

                                    if cl_list.betriebsnr != 1 and cl_list.betriebsnr != 2:
                                        droomrev = droomrev + res_line.zimmeranz
                                        dpaxrev = dpaxrev + res_line.erwachs + res_line.kind1 + res_line.kind2 + res_line.gratis
                                        drevrev =  to_decimal(drevrev) + to_decimal(net_lodg)

                                    if cl_list.betriebsnr == 1:
                                        droomcomp = droomcomp + res_line.zimmeranz
                                        dpaxcomp = dpaxcomp + res_line.erwachs + res_line.kind1 + res_line.kind2 + res_line.gratis

                                    if cl_list.betriebsnr == 2:
                                        droomhu = droomhu + res_line.zimmeranz
                                        dpaxhu = dpaxhu + res_line.erwachs + res_line.kind1 + res_line.kind2 + res_line.gratis

                                if (mi_mtd_chk and get_month(datum0) == get_month(to_date)) or (mi_ftd_chk and datum0 >= d2 and datum0 <= tdate):
                                    cl_list.mroom = cl_list.mroom + res_line.zimmeranz
                                    cl_list.mpax = cl_list.mpax + res_line.erwachs + res_line.kind1 + res_line.kind2 + res_line.gratis
                                    cl_list.mrev =  to_decimal(cl_list.mrev) + to_decimal(net_lodg)

                                    if cl_list.betriebsnr != 1 and cl_list.betriebsnr != 2:
                                        mroomrev = mroomrev + res_line.zimmeranz
                                        mpaxrev = mpaxrev + res_line.erwachs + res_line.kind1 + res_line.kind2 + res_line.gratis
                                        mrevrev =  to_decimal(mrevrev) + to_decimal(net_lodg)

                                    if cl_list.betriebsnr == 1:
                                        mroomcomp = mroomcomp + res_line.zimmeranz
                                        mpaxcomp = mpaxcomp + res_line.erwachs + res_line.kind1 + res_line.kind2 + res_line.gratis

                                    if cl_list.betriebsnr == 2:
                                        mroomhu = mroomhu + res_line.zimmeranz
                                        mpaxhu = mpaxhu + res_line.erwachs + res_line.kind1 + res_line.kind2 + res_line.gratis
                                cl_list.yroom = cl_list.yroom + res_line.zimmeranz
                                cl_list.ypax = cl_list.ypax + res_line.erwachs + res_line.kind1 + res_line.kind2 + res_line.gratis
                                cl_list.yrev =  to_decimal(cl_list.yrev) + to_decimal(net_lodg)

                                if cl_list.betriebsnr != 1 and cl_list.betriebsnr != 2:
                                    yroomrev = yroomrev + res_line.zimmeranz
                                    ypaxrev = ypaxrev + res_line.erwachs + res_line.kind1 + res_line.kind2 + res_line.gratis
                                    yrevrev =  to_decimal(yrevrev) + to_decimal(net_lodg)

                                if cl_list.betriebsnr == 1:
                                    yroomcomp = yroomcomp + res_line.zimmeranz
                                    ypaxcomp = ypaxcomp + res_line.erwachs + res_line.kind1 + res_line.kind2 + res_line.gratis

                                if cl_list.betriebsnr == 2:
                                    yroomhu = yroomhu + res_line.zimmeranz
                                    ypaxhu = ypaxhu + res_line.erwachs + res_line.kind1 + res_line.kind2 + res_line.gratis
            cal_umsatz1_called = True

        for cl_list in query(cl_list_data, filters=(lambda cl_list:((cl_list.segm >= i1 and cl_list.segm <= i2) or (cl_list.segm >= i3 and cl_list.segm <= i4)))):

            if cl_list.droom != 0:
                cl_list.drate =  to_decimal(cl_list.drev) / to_decimal(cl_list.droom)

            if cl_list.mroom != 0:
                cl_list.mrate =  to_decimal(cl_list.mrev) / to_decimal(cl_list.mroom)
            cl_list.proz1 =  to_decimal(100.0) * to_decimal(cl_list.droom) / to_decimal(tot_room)
            cl_list.proz2 =  to_decimal(100.0) * to_decimal(cl_list.mroom) / to_decimal(mtd_act)
            cl_list.proz3 =  to_decimal(100.0) * to_decimal(cl_list.yroom) / to_decimal(ytd_act)

            if droomrev != 0:
                draterev =  to_decimal(drevrev) / to_decimal(droomrev)

            if mroomrev != 0:
                mraterev =  to_decimal(mrevrev) / to_decimal(mroomrev)

            if yroomrev != 0:
                yraterev =  to_decimal(yrevrev) / to_decimal(yroomrev)

            if cl_list.proz1 == None:
                cl_list.proz1 =  to_decimal("0")

            if cl_list.proz2 == None:
                cl_list.proz2 =  to_decimal("0")

            if cl_list.proz3 == None:
                cl_list.proz3 =  to_decimal("0")

            if cl_list.drev == 0 and cl_list.mrev == 0 and cl_list.yrev == 0:
                cl_list.zero_flag = True
        cl_list = Cl_list()
        cl_list_data.append(cl_list)

        cl_list = Cl_list()
        cl_list_data.append(cl_list)

        cl_list.bezeich = rev_title
        cl_list.droom = droomrev
        cl_list.proz1 =  to_decimal(droomrev) / to_decimal(tot_room) * to_decimal("100")
        cl_list.mroom = mroomrev
        cl_list.proz2 =  to_decimal(mroomrev) / to_decimal(mtd_act) * to_decimal("100")
        cl_list.dpax = dpaxrev
        cl_list.mpax = mpaxrev
        cl_list.yroom = yroomrev
        cl_list.ypax = ypaxrev
        cl_list.proz3 =  to_decimal(ytd_act) * to_decimal("100")
        cl_list.drev =  to_decimal(drevrev)
        cl_list.mrev =  to_decimal(mrevrev)
        cl_list.yrev =  to_decimal(yrevrev)

        if show_avrg:

            if droomrev != 0:
                cl_list.drate =  to_decimal(drevrev) / to_decimal(droomrev)
            else:
                cl_list.drate =  to_decimal("0")

            if mroomrev != 0:
                cl_list.mrate =  to_decimal(mrevrev) / to_decimal(mroomrev)
            else:
                cl_list.mrate =  to_decimal("0")

            if yroomrev != 0:
                cl_list.yrate =  to_decimal(yrevrev) / to_decimal(yroomrev)
            else:
                cl_list.yrate =  to_decimal("0")

        if rev_title1 != "":
            cl_list = Cl_list()
            cl_list_data.append(cl_list)

            cl_list.bezeich = rev_title1

            if droomrev != 0:
                cl_list.proz1 = ( to_decimal(dpaxrev) - to_decimal(droomrev)) / to_decimal(droomrev) * to_decimal("100")
            else:
                cl_list.proz1 =  to_decimal("0")

            if mroomrev != 0:
                cl_list.proz2 = ( to_decimal(mpaxrev) - to_decimal(mroomrev)) / to_decimal(mroomrev) * to_decimal("100")
            else:
                cl_list.proz2 =  to_decimal("0")

            if yroomrev != 0:
                cl_list.proz3 = ( to_decimal(ypaxrev) - to_decimal(yroomrev)) / to_decimal(yroomrev) * to_decimal("100")
            else:
                cl_list.proz3 =  to_decimal("0")
        cl_list = Cl_list()
        cl_list_data.append(cl_list)

    def cal_umsatz1a(i1:int, i2:int, rev_title:string, rev_title1:string, show_avrg:bool):

        nonlocal cl_list_data, lvcarea, do_it, droomrev, mroomrev, yroomrev, drevrev, mrevrev, yrevrev, dpaxrev, mpaxrev, ypaxrev, draterev, mraterev, yraterev, droomcomp, mroomcomp, yroomcomp, dpaxcomp, mpaxcomp, ypaxcomp, droomhu, mroomhu, yroomhu, dpaxhu, mpaxhu, ypaxhu, tot_room, all_room, dvacant, mvacant, yvacant, dooo, mooo, yooo, dnoshow, mnoshow, ynoshow, dcancel, mcancel, ycancel, cal_umsatz1_called, cal_umsatz4_called, droom, proz1, mroom, proz2, dpax, mpax, drate, mrate, drev, mrev, yroom, ypax, yrate, yrev, inactive, mtd_act, mtd_totrm, ytd_act, ytd_totrm, ci_date, htparam, zimmer, zkstat, zinrstat, genstat, segment, guestseg, reservation, res_line, outorder, artikel, umsatz
        nonlocal pvilanguage, opening_date, from_date, to_date, fdate, tdate, segmtype_exist, mi_mtd_chk, mi_ftd_chk, mi_exchu_chk, mi_exccomp_chk, long_digit


        nonlocal cl_list, om_list
        nonlocal cl_list_data, om_list_data

        i:int = 0
        tot_proz3:Decimal = to_decimal("0.0")
        inact:bool = False
        do_it1:bool = False
        d1:date = None
        d2:date = None
        datum0:date = None
        datum1:date = None
        datum2:date = None
        curr_i:int = 0
        net_lodg:Decimal = to_decimal("0.0")
        fnet_lodg:Decimal = to_decimal("0.0")
        tot_breakfast:Decimal = to_decimal("0.0")
        tot_lunch:Decimal = to_decimal("0.0")
        tot_dinner:Decimal = to_decimal("0.0")
        tot_other:Decimal = to_decimal("0.0")
        tot_rmrev:Decimal = to_decimal("0.0")
        tot_vat:Decimal = to_decimal("0.0")
        tot_service:Decimal = to_decimal("0.0")
        bgenstat = None
        Bgenstat =  create_buffer("Bgenstat",Genstat)
        d1 = from_date

        if to_date < (ci_date - timedelta(days=1)):
            d2 = to_date
        else:
            d2 = ci_date - timedelta(days=1)

        for segment in db_session.query(Segment).filter(
                 (Segment.betriebsnr == 0)).order_by(Segment.segmentcode).all():

            bgenstat = db_session.query(Bgenstat).filter(
                     (Bgenstat.segmentcode == segment.segmentcode) & (Bgenstat.datum >= d1) & (Bgenstat.datum <= d2) & (Bgenstat.resstatus != 13) & (Bgenstat.gratis == 0) & (Bgenstat.segmentcode != 0) & (Bgenstat.nationnr != 0) & (Bgenstat.zinr != "") & (Bgenstat.res_logic[inc_value(1)])).first()

            if bgenstat:
                do_it1 = True


            else:

                if matches(segment.bezeich,r"*$$0"):
                    do_it1 = False


                else:
                    do_it1 = True

            if do_it1:
                cl_list = Cl_list()
                cl_list_data.append(cl_list)

                cl_list.segm = segment.segmentcode
                cl_list.bezeich = entry(0, segment.bezeich, "$$0")
                cl_list.betriebsnr = segment.betriebsnr
                cl_list.drev =  to_decimal("0")

                for genstat in db_session.query(Genstat).filter(
                         (Genstat.segmentcode == segment.segmentcode) & (Genstat.datum >= d1) & (Genstat.datum <= d2) & (Genstat.resstatus != 13) & (Genstat.gratis == 0) & (Genstat.segmentcode != 0) & (Genstat.nationnr != 0) & (Genstat.zinr != "") & (Genstat.res_logic[inc_value(1)])).order_by(Genstat._recid).all():
                    inact = True

                    if genstat.datum == to_date:
                        cl_list.droom = cl_list.droom + 1
                        cl_list.dpax = cl_list.dpax + genstat.erwachs + genstat.kind1 + genstat.kind2
                        cl_list.drev =  to_decimal(cl_list.drev) + to_decimal(genstat.logis)
                        droomrev = droomrev + 1
                        dpaxrev = dpaxrev + genstat.erwachs + genstat.kind1 + genstat.kind2 + genstat.gratis


                        drevrev =  to_decimal(drevrev) + to_decimal(genstat.logis)

                    if (mi_mtd_chk and get_month(genstat.datum) == get_month(d2)) or (mi_ftd_chk and genstat.datum >= d1 and genstat.datum <= d2):
                        cl_list.mroom = cl_list.mroom + 1
                        cl_list.mpax = cl_list.mpax + genstat.erwachs + genstat.kind1 + genstat.kind2


                        cl_list.mrev =  to_decimal(cl_list.mrev) + to_decimal(genstat.logis)
                        mroomrev = mroomrev + 1
                        mpaxrev = mpaxrev + genstat.erwachs + genstat.kind1 + genstat.kind2
                        mrevrev =  to_decimal(mrevrev) + to_decimal(genstat.logis)
                    cl_list.yroom = cl_list.yroom + 1


                    cl_list.ypax = cl_list.ypax + genstat.erwachs + genstat.kind1 + genstat.kind2
                    cl_list.yrev =  to_decimal(cl_list.yrev) + to_decimal(genstat.logis)
                    yroomrev = yroomrev + 1
                    ypaxrev = ypaxrev + genstat.erwachs + genstat.kind1 + genstat.kind2
                    yrevrev =  to_decimal(yrevrev) + to_decimal(genstat.logis)

        if do_it:

            for genstat in db_session.query(Genstat).filter(
                     (Genstat.datum >= d1) & (Genstat.datum <= d2) & (Genstat.segmentcode != 0) & (Genstat.nationnr != 0) & (Genstat.zinr != "") & (Genstat.resstatus != 13) & (Genstat.res_logic[inc_value(1)])).order_by(Genstat._recid).all():

                segment = get_cache (Segment, {"segmentcode": [(eq, genstat.segmentcode)]})

                if segment:

                    cl_list = query(cl_list_data, filters=(lambda cl_list: cl_list.segm == segment.segmentcode), first=True)

                    if cl_list:

                        if genstat.datum == to_date:
                            cl_list.drev =  to_decimal(cl_list.drev) + to_decimal(genstat.res_deci[0])
                            drevrev =  to_decimal(drevrev) + to_decimal(genstat.res_deci[0])

                        if (mi_mtd_chk and get_month(genstat.datum) == get_month(d2)) or (mi_ftd_chk and genstat.datum >= d1 and genstat.datum <= d2):
                            cl_list.mrev =  to_decimal(cl_list.mrev) + to_decimal(genstat.res_deci[0])
                            mrevrev =  to_decimal(mrevrev) + to_decimal(genstat.res_deci[0])


                else:

                    guestseg = get_cache (Guestseg, {"gastnr": [(eq, genstat.gastnr)]})

                    if guestseg:

                        if guestseg.reihenfolge == 1:

                            cl_list = query(cl_list_data, filters=(lambda cl_list: cl_list.segm == segment.segmentcode), first=True)

                            if cl_list:

                                if genstat.datum == to_date:
                                    cl_list.drev =  to_decimal(cl_list.drev) + to_decimal(genstat.res_deci[0])
                                    drevrev =  to_decimal(drevrev) + to_decimal(genstat.res_deci[0])

                                if (mi_mtd_chk and get_month(genstat.datum) == get_month(d2)) or (mi_ftd_chk and genstat.datum >= d1 and genstat.datum <= d2):
                                    cl_list.mrev =  to_decimal(cl_list.mrev) + to_decimal(genstat.res_deci[0])
                                    mrevrev =  to_decimal(mrevrev) + to_decimal(genstat.res_deci[0])


                        else:

                            guestseg = get_cache (Guestseg, {"reihenfolge": [(eq, 0)]})

                            if guestseg:

                                cl_list = query(cl_list_data, filters=(lambda cl_list: cl_list.segm == guestseg.segmentcode), first=True)

                                if cl_list:

                                    if genstat.datum == to_date:
                                        cl_list.drev =  to_decimal(cl_list.drev) + to_decimal(genstat.res_deci[0])
                                        drevrev =  to_decimal(drevrev) + to_decimal(genstat.res_deci[0])

                                    if (mi_mtd_chk and get_month(genstat.datum) == get_month(d2)) or (mi_ftd_chk and genstat.datum >= d1 and genstat.datum <= d2):
                                        cl_list.mrev =  to_decimal(cl_list.mrev) + to_decimal(genstat.res_deci[0])
                                        mrevrev =  to_decimal(mrevrev) + to_decimal(genstat.res_deci[0])

        if to_date >= ci_date:
            d2 = d2 + timedelta(days=1)

            res_line_obj_list = {}
            res_line = Res_line()
            reservation = Reservation()
            for res_line.ankunft, res_line.abreise, res_line._recid, res_line.zimmeranz, res_line.erwachs, res_line.kind1, res_line.kind2, res_line.gratis, res_line.kontignr, reservation.segmentcode, reservation._recid in db_session.query(Res_line.ankunft, Res_line.abreise, Res_line._recid, Res_line.zimmeranz, Res_line.erwachs, Res_line.kind1, Res_line.kind2, Res_line.gratis, Res_line.kontignr, Reservation.segmentcode, Reservation._recid).join(Reservation,(Reservation.resnr == Res_line.resnr)).filter(
                     (((Res_line.resstatus <= 13) & (Res_line.resstatus != 4) & (Res_line.resstatus != 8) & (Res_line.resstatus != 9) & (Res_line.resstatus != 10) & (Res_line.resstatus != 12) & (Res_line.active_flag <= 1) & (not_ (Res_line.ankunft > to_date)) & (not_ (Res_line.abreise < d2)))) | ((Res_line.resstatus == 8) & (Res_line.active_flag == 2) & (Res_line.ankunft == ci_date) & (Res_line.abreise == ci_date)) & (Res_line.gastnr > 0) & (Res_line.l_zuordnung[inc_value(2)] == 0)).order_by(Res_line.resnr, Res_line.reslinnr.desc()).all():
                if res_line_obj_list.get(res_line._recid):
                    continue
                else:
                    res_line_obj_list[res_line._recid] = True


                curr_i = 0

                if res_line.kontignr < 0:
                    do_it1 = True

                    cl_list = query(cl_list_data, filters=(lambda cl_list: cl_list.segm == reservation.segmentcode), first=True)

                    if not cl_list:

                        segment = get_cache (Segment, {"segmentcode": [(eq, reservation.segmentcode)]})

                        if segment and not matches(segment.bezeich,r"*$$0"):

                            if segment.betriebsnr != 1 and segment.betriebsnr != 2:
                                inact = True
                                cl_list = Cl_list()
                                cl_list_data.append(cl_list)

                                cl_list.compli = False
                                cl_list.segm = segment.segmentcode
                                cl_list.bezeich = segment.bezeich
                                cl_list.betriebsnr = segment.betriebsnr
                            else:
                                cl_list = Cl_list()
                                cl_list_data.append(cl_list)

                                cl_list.compli = True
                                cl_list.segm = segment.segmentcode
                                cl_list.bezeich = segment.bezeich
                                cl_list.betriebsnr = segment.betriebsnr
                        else:
                            do_it1 = False

                    if do_it1 :
                        datum1 = d2

                        if res_line.ankunft > datum1:
                            datum1 = res_line.ankunft
                        datum2 = to_date

                        if res_line.abreise < datum2:
                            datum2 = res_line.abreise
                        for datum0 in date_range(datum1,datum2) :
                            curr_i = curr_i + 1

                            if datum0 != res_line.abreise:
                                net_lodg =  to_decimal("0")
                                tot_breakfast =  to_decimal("0")
                                tot_lunch =  to_decimal("0")
                                tot_dinner =  to_decimal("0")
                                tot_other =  to_decimal("0")


                                fnet_lodg, net_lodg, tot_breakfast, tot_lunch, tot_dinner, tot_other, tot_rmrev, tot_vat, tot_service = get_output(get_room_breakdown(res_line._recid, datum0, curr_i, from_date))

                                if datum0 == to_date:
                                    cl_list.droom = cl_list.droom + res_line.zimmeranz
                                    cl_list.dpax = cl_list.dpax + res_line.erwachs + res_line.kind1 + res_line.kind2 + res_line.gratis
                                    cl_list.drev =  to_decimal(cl_list.drev) + to_decimal(net_lodg)

                                    if cl_list.betriebsnr != 1 and cl_list.betriebsnr != 2:
                                        droomrev = droomrev + res_line.zimmeranz
                                        dpaxrev = dpaxrev + res_line.erwachs + res_line.kind1 + res_line.kind2 + res_line.gratis
                                        drevrev =  to_decimal(drevrev) + to_decimal(net_lodg)

                                    if cl_list.betriebsnr == 1:
                                        droomcomp = droomcomp + res_line.zimmeranz
                                        dpaxcomp = dpaxcomp + res_line.erwachs + res_line.kind1 + res_line.kind2 + res_line.gratis

                                    if cl_list.betriebsnr == 2:
                                        droomhu = droomhu + res_line.zimmeranz
                                        dpaxhu = dpaxhu + res_line.erwachs + res_line.kind1 + res_line.kind2 + res_line.gratis

                                if (mi_mtd_chk and get_month(datum0) == get_month(to_date)) or (mi_ftd_chk and datum0 >= d2 and datum0 <= tdate):
                                    cl_list.mroom = cl_list.mroom + res_line.zimmeranz
                                    cl_list.mpax = cl_list.mpax + res_line.erwachs + res_line.kind1 + res_line.kind2 + res_line.gratis
                                    cl_list.mrev =  to_decimal(cl_list.mrev) + to_decimal(net_lodg)

                                    if cl_list.betriebsnr != 1 and cl_list.betriebsnr != 2:
                                        mroomrev = mroomrev + res_line.zimmeranz
                                        mpaxrev = mpaxrev + res_line.erwachs + res_line.kind1 + res_line.kind2 + res_line.gratis
                                        mrevrev =  to_decimal(mrevrev) + to_decimal(net_lodg)

                                    if cl_list.betriebsnr == 1:
                                        mroomcomp = mroomcomp + res_line.zimmeranz
                                        mpaxcomp = mpaxcomp + res_line.erwachs + res_line.kind1 + res_line.kind2 + res_line.gratis

                                    if cl_list.betriebsnr == 2:
                                        mroomhu = mroomhu + res_line.zimmeranz
                                        mpaxhu = mpaxhu + res_line.erwachs + res_line.kind1 + res_line.kind2 + res_line.gratis
                                cl_list.yroom = cl_list.yroom + res_line.zimmeranz


                                cl_list.ypax = cl_list.ypax + res_line.erwachs + res_line.kind1 + res_line.kind2 + res_line.gratis
                                cl_list.yrev =  to_decimal(cl_list.yrev) + to_decimal(net_lodg)

                                if cl_list.betriebsnr != 1 and cl_list.betriebsnr != 2:
                                    yroomrev = yroomrev + res_line.zimmeranz
                                    ypaxrev = ypaxrev + res_line.erwachs + res_line.kind1 + res_line.kind2 + res_line.gratis
                                    yrevrev =  to_decimal(yrevrev) + to_decimal(net_lodg)

                                if cl_list.betriebsnr == 1:
                                    yroomcomp = yroomcomp + res_line.zimmeranz
                                    ypaxcomp = ypaxcomp + res_line.erwachs + res_line.kind1 + res_line.kind2 + res_line.gratis

                                if cl_list.betriebsnr == 2:
                                    yroomhu = yroomhu + res_line.zimmeranz
                                    ypaxhu = ypaxhu + res_line.erwachs + res_line.kind1 + res_line.kind2 + res_line.gratis

        if inact:

            for cl_list in query(cl_list_data, filters=(lambda cl_list:(cl_list.betriebsnr >= i1 and cl_list.betriebsnr <= i2))):

                if cl_list.droom != 0:
                    cl_list.drate =  to_decimal(cl_list.drev) / to_decimal(cl_list.droom)

                if cl_list.mroom != 0:
                    cl_list.mrate =  to_decimal(cl_list.mrev) / to_decimal(cl_list.mroom)

                if cl_list.yroom != 0:
                    cl_list.yrate =  to_decimal(cl_list.yrev) / to_decimal(cl_list.yroom)
                cl_list.proz1 =  to_decimal(100.0) * to_decimal(cl_list.droom) / to_decimal(tot_room)
                cl_list.proz2 =  to_decimal(100.0) * to_decimal(cl_list.mroom) / to_decimal(mtd_act)
                cl_list.proz3 =  to_decimal(100.0) * to_decimal(cl_list.yroom) / to_decimal(ytd_act)

                if droomrev != 0:
                    draterev =  to_decimal(drevrev) / to_decimal(droomrev)

                if mroomrev != 0:
                    mraterev =  to_decimal(mrevrev) / to_decimal(mroomrev)

                if yroomrev != 0:
                    yraterev =  to_decimal(yrevrev) / to_decimal(yroomrev)

                if cl_list.proz1 == None:
                    cl_list.proz1 =  to_decimal("0")

                if cl_list.proz2 == None:
                    cl_list.proz2 =  to_decimal("0")

                if cl_list.proz3 == None:
                    cl_list.proz3 =  to_decimal("0")
                tot_proz3 =  to_decimal(tot_proz3) + to_decimal(cl_list.proz3)

                if cl_list.drev == 0 and cl_list.mrev == 0 and cl_list.yrev == 0:
                    cl_list.zero_flag = True
            cl_list = Cl_list()
            cl_list_data.append(cl_list)

        cl_list = Cl_list()
        cl_list_data.append(cl_list)

        cl_list = Cl_list()
        cl_list_data.append(cl_list)

        cl_list.bezeich = rev_title
        cl_list.droom = droomrev
        cl_list.proz1 =  to_decimal(droomrev) / to_decimal(tot_room) * to_decimal("100")
        cl_list.mroom = mroomrev
        cl_list.proz2 =  to_decimal(mroomrev) / to_decimal(mtd_act) * to_decimal("100")
        cl_list.dpax = dpaxrev
        cl_list.mpax = mpaxrev
        cl_list.yroom = yroomrev
        cl_list.ypax = ypaxrev
        cl_list.proz3 =  to_decimal(tot_proz3)
        cl_list.drev =  to_decimal(drevrev)
        cl_list.mrev =  to_decimal(mrevrev)
        cl_list.yrev =  to_decimal(yrevrev)

        if show_avrg:

            if droomrev != 0:
                cl_list.drate =  to_decimal(drevrev) / to_decimal(droomrev)
            else:
                cl_list.drate =  to_decimal("0")

            if mroomrev != 0:
                cl_list.mrate =  to_decimal(mrevrev) / to_decimal(mroomrev)
            else:
                cl_list.mrate =  to_decimal("0")

            if yroomrev != 0:
                cl_list.yrate =  to_decimal(yrevrev) / to_decimal(yroomrev)
            else:
                cl_list.yrate =  to_decimal("0")

        if rev_title1 != "":
            cl_list = Cl_list()
            cl_list_data.append(cl_list)

            cl_list.bezeich = rev_title1

            if droomrev != 0:
                cl_list.proz1 = ( to_decimal(dpaxrev) - to_decimal(droomrev)) / to_decimal(droomrev) * to_decimal("100")
            else:
                cl_list.proz1 =  to_decimal("0")

            if mroomrev != 0:
                cl_list.proz2 = ( to_decimal(mpaxrev) - to_decimal(mroomrev)) / to_decimal(mroomrev) * to_decimal("100")
            else:
                cl_list.proz2 =  to_decimal("0")

            if yroomrev != 0:
                cl_list.proz3 = ( to_decimal(ypaxrev) - to_decimal(yroomrev)) / to_decimal(yroomrev) * to_decimal("100")
            else:
                cl_list.proz3 =  to_decimal("0")
        cl_list = Cl_list()
        cl_list_data.append(cl_list)

    def cal_umsatz1b(i1:int, i2:int, rev_title:string, rev_title1:string, show_avrg:bool):

        nonlocal cl_list_data, lvcarea, do_it, droomrev, mroomrev, yroomrev, drevrev, mrevrev, yrevrev, dpaxrev, mpaxrev, ypaxrev, draterev, mraterev, yraterev, droomcomp, mroomcomp, yroomcomp, dpaxcomp, mpaxcomp, ypaxcomp, droomhu, mroomhu, yroomhu, dpaxhu, mpaxhu, ypaxhu, tot_room, all_room, dvacant, mvacant, yvacant, dooo, mooo, yooo, dnoshow, mnoshow, ynoshow, dcancel, mcancel, ycancel, cal_umsatz1_called, cal_umsatz4_called, droom, proz1, mroom, proz2, dpax, mpax, drate, mrate, drev, mrev, yroom, ypax, yrate, yrev, inactive, mtd_act, mtd_totrm, ytd_act, ytd_totrm, ci_date, htparam, zimmer, zkstat, zinrstat, genstat, segment, guestseg, reservation, res_line, outorder, artikel, umsatz
        nonlocal pvilanguage, opening_date, from_date, to_date, fdate, tdate, segmtype_exist, mi_mtd_chk, mi_ftd_chk, mi_exchu_chk, mi_exccomp_chk, long_digit


        nonlocal cl_list, om_list
        nonlocal cl_list_data, om_list_data

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
        net_lodg:Decimal = to_decimal("0.0")
        fnet_lodg:Decimal = to_decimal("0.0")
        tot_breakfast:Decimal = to_decimal("0.0")
        tot_lunch:Decimal = to_decimal("0.0")
        tot_dinner:Decimal = to_decimal("0.0")
        tot_other:Decimal = to_decimal("0.0")
        tot_rmrev:Decimal = to_decimal("0.0")
        tot_vat:Decimal = to_decimal("0.0")
        tot_service:Decimal = to_decimal("0.0")
        bgenstat = None
        Bgenstat =  create_buffer("Bgenstat",Genstat)
        d1 = from_date

        if to_date < (ci_date - timedelta(days=1)):
            d2 = to_date
        else:
            d2 = ci_date - timedelta(days=1)

        for segment in db_session.query(Segment).order_by(Segment.segmentcode).all():

            bgenstat = db_session.query(Bgenstat).filter(
                     (Bgenstat.segmentcode == segment.segmentcode) & (Bgenstat.datum >= d1) & (Bgenstat.datum <= d2) & (Bgenstat.resstatus != 13) & (Bgenstat.gratis != 0) & (Bgenstat.segmentcode != 0) & (Bgenstat.nationnr != 0) & (Bgenstat.zinr != "") & (Bgenstat.res_logic[inc_value(1)])).first()

            if bgenstat:
                do_it1 = True


            else:

                if matches(segment.bezeich,r"*$$0"):
                    do_it1 = False


                else:
                    do_it1 = True

            if do_it1:

                for genstat in db_session.query(Genstat).filter(
                         (Genstat.segmentcode == segment.segmentcode) & (Genstat.datum >= d1) & (Genstat.datum <= d2) & (Genstat.resstatus != 13) & (Genstat.gratis != 0) & (Genstat.segmentcode != 0) & (Genstat.nationnr != 0) & (Genstat.zinr != "") & (Genstat.res_logic[inc_value(1)])).order_by(Genstat._recid).all():
                    inact = True

                    cl_list = query(cl_list_data, filters=(lambda cl_list: cl_list.segm == segment.segmentcode and cl_list.compli), first=True)

                    if not cl_list:
                        cl_list = Cl_list()
                        cl_list_data.append(cl_list)

                        cl_list.compli = True
                        cl_list.segm = segment.segmentcode
                        cl_list.bezeich = entry(0, segment.bezeich, "$$0")
                        cl_list.betriebsnr = segment.betriebsnr

                    if genstat.datum == to_date:
                        cl_list.droom = cl_list.droom + 1
                        cl_list.dpax = cl_list.dpax + genstat.erwachs + genstat.kind1 + genstat.kind2 + genstat.gratis

                        if cl_list.betriebsnr != 1 and cl_list.betriebsnr != 2:
                            droomrev = droomrev + 1
                            dpaxrev = dpaxrev + genstat.erwachs + genstat.kind1 + genstat.kind2 + genstat.gratis

                        if cl_list.betriebsnr == 1:
                            droomcomp = droomcomp + 1
                            dpaxcomp = dpaxcomp + genstat.erwachs + genstat.kind1 + genstat.kind2 + genstat.gratis

                        if cl_list.betriebsnr == 2:
                            droomhu = droomhu + 1
                            dpaxhu = dpaxhu + genstat.erwachs + genstat.kind1 + genstat.kind2 + genstat.gratis

                    if (mi_mtd_chk and get_month(genstat.datum) == get_month(d2)) or (mi_ftd_chk and genstat.datum >= d1 and genstat.datum <= d2):
                        cl_list.mroom = cl_list.mroom + 1
                        cl_list.mpax = cl_list.mpax + genstat.erwachs + genstat.kind1 + genstat.kind2 + genstat.gratis

                        if cl_list.betriebsnr != 1 and cl_list.betriebsnr != 2:
                            mroomrev = mroomrev + 1
                            mpaxrev = mpaxrev + genstat.erwachs + genstat.kind1 + genstat.kind2 + genstat.gratis

                        if cl_list.betriebsnr == 1:
                            mroomcomp = mroomcomp + 1
                            mpaxcomp = mpaxcomp + genstat.erwachs + genstat.kind1 + genstat.kind2 + genstat.gratis

                        if cl_list.betriebsnr == 2:
                            mroomhu = mroomhu + 1
                            mpaxhu = mpaxhu + genstat.erwachs + genstat.kind1 + genstat.kind2 + genstat.gratis
                    cl_list.yroom = cl_list.yroom + 1
                    cl_list.ypax = cl_list.ypax + genstat.erwachs + genstat.kind1 + genstat.kind2 + genstat.gratis

                    if cl_list.betriebsnr != 1 and cl_list.betriebsnr != 2:
                        yroomrev = yroomrev + 1
                        ypaxrev = ypaxrev + genstat.erwachs + genstat.kind1 + genstat.kind2 + genstat.gratis

                    if cl_list.betriebsnr == 1:
                        yroomcomp = yroomcomp + 1
                        ypaxcomp = ypaxcomp + genstat.erwachs + genstat.kind1 + genstat.kind2 + genstat.gratis

                    if cl_list.betriebsnr == 2:
                        yroomhu = yroomhu + 1
                        ypaxhu = ypaxhu + genstat.erwachs + genstat.kind1 + genstat.kind2 + genstat.gratis

        if inact:

            for cl_list in query(cl_list_data, filters=(lambda cl_list: cl_list.compli)):

                if cl_list.droom != 0:
                    cl_list.drate =  to_decimal(cl_list.drev) / to_decimal(cl_list.droom)

                if cl_list.mroom != 0:
                    cl_list.mrate =  to_decimal(cl_list.mrev) / to_decimal(cl_list.mroom)

                if cl_list.yroom != 0:
                    cl_list.yrate =  to_decimal(cl_list.yrev) / to_decimal(cl_list.yroom)
                cl_list.proz1 =  to_decimal(100.0) * to_decimal(cl_list.droom) / to_decimal(tot_room)
                cl_list.proz2 =  to_decimal(100.0) * to_decimal(cl_list.mroom) / to_decimal(mtd_act)
                cl_list.proz3 =  to_decimal(100.0) * to_decimal(cl_list.yroom) / to_decimal(ytd_act)

                if cl_list.proz1 == None:
                    cl_list.proz1 =  to_decimal("0")

                if cl_list.proz2 == None:
                    cl_list.proz2 =  to_decimal("0")

                if cl_list.proz3 == None:
                    cl_list.proz3 =  to_decimal("0")
            cl_list = Cl_list()
            cl_list_data.append(cl_list)

        cl_list = Cl_list()
        cl_list_data.append(cl_list)

        cl_list.bezeich = rev_title
        cl_list.droom = droomrev + droomcomp + droomhu
        cl_list.proz1 = ( to_decimal(droomrev) + to_decimal(droomcomp) + to_decimal(droomhu)) / to_decimal(tot_room) * to_decimal("100")
        cl_list.mroom = mroomrev + mroomcomp + mroomhu
        cl_list.proz2 = ( to_decimal(mroomrev) + to_decimal(mroomcomp) + to_decimal(mroomhu)) / to_decimal(mtd_act) * to_decimal("100")
        cl_list.dpax = dpaxrev + dpaxcomp + dpaxhu
        cl_list.mpax = mpaxrev + mpaxcomp + mpaxhu
        cl_list.yroom = yroomrev + yroomcomp + yroomhu
        cl_list.ypax = ypaxrev + ypaxcomp + ypaxhu
        cl_list.proz3 = ( to_decimal(yroomrev) + to_decimal(yroomcomp) + to_decimal(yroomhu)) / to_decimal(ytd_act) * to_decimal("100")
        cl_list.drev =  to_decimal(drevrev)
        cl_list.mrev =  to_decimal(mrevrev)
        cl_list.yrev =  to_decimal(yrevrev)

        if show_avrg:

            if (droomrev + droomcomp + droomhu) != 0:
                cl_list.drate =  to_decimal(drevrev) / to_decimal((droomrev) + to_decimal(droomcomp) + to_decimal(droomhu))
            else:
                cl_list.drate =  to_decimal("0")

            if (mroomrev + mroomcomp + mroomhu) != 0:
                cl_list.mrate =  to_decimal(mrevrev) / to_decimal((mroomrev) + to_decimal(mroomcomp) + to_decimal(mroomhu))
            else:
                cl_list.mrate =  to_decimal("0")

            if (yroomrev + yroomcomp + yroomhu) != 0:
                cl_list.yrate =  to_decimal(yrevrev) / to_decimal((yroomrev) + to_decimal(yroomcomp) + to_decimal(yroomhu))
            else:
                cl_list.yrate =  to_decimal("0")

        if rev_title1 != "":
            cl_list = Cl_list()
            cl_list_data.append(cl_list)

            cl_list.bezeich = rev_title1

            if (droomrev + droomcomp + droomhu) != 0:
                cl_list.proz1 = ( to_decimal((dpaxrev) + to_decimal(dpaxcomp) + to_decimal(dpaxhu)) - to_decimal((droomrev) + to_decimal(droomcomp) + to_decimal(droomhu))) / to_decimal((droomrev) + to_decimal(droomcomp) + to_decimal(droomhu)) * to_decimal("100")
            else:
                cl_list.proz1 =  to_decimal("0")

            if (mroomrev + mroomcomp + mroomhu) != 0:
                cl_list.proz2 = ( to_decimal((mpaxrev) + to_decimal(mpaxcomp) + to_decimal(mpaxhu)) - to_decimal((mroomrev) + to_decimal(mroomcomp) + to_decimal(mroomhu))) / to_decimal((mroomrev) + to_decimal(mroomcomp) + to_decimal(mroomhu)) * to_decimal("100")
            else:
                cl_list.proz2 =  to_decimal("0")

            if (yroomrev + yroomcomp + yroomhu) != 0:
                cl_list.proz3 = ( to_decimal((ypaxrev) + to_decimal(ypaxcomp) + to_decimal(ypaxhu)) - to_decimal((yroomrev) + to_decimal(yroomcomp) + to_decimal(yroomhu))) / to_decimal((yroomrev) + to_decimal(yroomcomp) + to_decimal(yroomhu)) * to_decimal("100")
            else:
                cl_list.proz3 =  to_decimal("0")
        cl_list = Cl_list()
        cl_list_data.append(cl_list)

    def cal_umsatz2():

        nonlocal cl_list_data, lvcarea, do_it, droomrev, mroomrev, yroomrev, drevrev, mrevrev, yrevrev, dpaxrev, mpaxrev, ypaxrev, draterev, mraterev, yraterev, droomcomp, mroomcomp, yroomcomp, dpaxcomp, mpaxcomp, ypaxcomp, droomhu, mroomhu, yroomhu, dpaxhu, mpaxhu, ypaxhu, tot_room, all_room, dvacant, mvacant, yvacant, dooo, mooo, yooo, dnoshow, mnoshow, ynoshow, dcancel, mcancel, ycancel, cal_umsatz1_called, cal_umsatz4_called, droom, proz1, mroom, proz2, dpax, mpax, drate, mrate, drev, mrev, yroom, ypax, yrate, yrev, inactive, mtd_act, mtd_totrm, ytd_act, ytd_totrm, ci_date, htparam, zimmer, zkstat, zinrstat, genstat, segment, guestseg, reservation, res_line, outorder, artikel, umsatz
        nonlocal pvilanguage, opening_date, from_date, to_date, fdate, tdate, segmtype_exist, mi_mtd_chk, mi_ftd_chk, mi_exchu_chk, mi_exccomp_chk, long_digit


        nonlocal cl_list, om_list
        nonlocal cl_list_data, om_list_data

        i:int = 0
        datum:date = None
        datum1:date = None
        dooo = 0
        mooo = 0
        yooo = 0
        for datum in date_range(from_date,to_date) :

            if to_date < ci_date:
                datum1 = to_date


            else:
                datum1 = (ci_date - timedelta(days=1))

            zinrstat = get_cache (Zinrstat, {"datum": [(eq, datum)],"zinr": [(eq, "ooo")]})

            if zinrstat:

                if datum == to_date:
                    dooo = zinrstat.zimmeranz

                if (mi_mtd_chk and get_month(zinrstat.datum) == get_month(datum1)) or (mi_ftd_chk and zinrstat.datum >= fdate and zinrstat.datum <= datum1):
                    mooo = mooo + zinrstat.zimmeranz
                yooo = yooo + zinrstat.zimmeranz

            if datum >= ci_date:

                outorder_obj_list = {}
                for outorder, zimmer in db_session.query(Outorder, Zimmer).join(Zimmer,(Zimmer.zinr == Outorder.zinr)).filter(
                         ((Outorder.gespstart >= datum) & (Outorder.gespstart <= datum) & (Outorder.betriebsnr <= 1)) | ((Outorder.gespstart <= datum) & (Outorder.gespende >= datum) & (Outorder.betriebsnr <= 1))).order_by(Outorder._recid).all():
                    if outorder_obj_list.get(outorder._recid):
                        continue
                    else:
                        outorder_obj_list[outorder._recid] = True

                    if datum == to_date:
                        dooo = dooo + 1

                    om_list = query(om_list_data, filters=(lambda om_list: om_list.zinr == outorder.zinr and om_list.gespstart == outorder.gespstart and om_list.gespende == outorder.gespende), first=True)

                    if not om_list:
                        om_list = Om_list()
                        om_list_data.append(om_list)

                        om_list.zinr = outorder.zinr
                        om_list.gespstart = outorder.gespstart
                        om_list.gespende = outorder.gespende
                        mooo = mooo + 1
                        yooo = yooo + 1
        dvacant = tot_room - dooo - (droomrev + droomcomp + droomhu)
        mvacant = mtd_act - mooo - (mroomrev + mroomcomp + mroomhu)
        yvacant = ytd_act - yooo - (yroomrev + yroomcomp + yroomhu)

        if to_date == opening_date:
            mvacant = dvacant
            yvacant = dvacant
            mooo = dooo
            yooo = dooo
        cl_list = Cl_list()
        cl_list_data.append(cl_list)

        cl_list.bezeich = "V A C A N T"
        cl_list.droom = dvacant
        cl_list.proz1 =  to_decimal(dvacant) / to_decimal(tot_room) * to_decimal("100")
        cl_list.mroom = mvacant
        cl_list.proz2 =  to_decimal(mvacant) / to_decimal(mtd_act) * to_decimal("100")
        cl_list.yroom = yvacant
        cl_list.proz3 =  to_decimal(yvacant) / to_decimal(ytd_act) * to_decimal("100")


        cl_list = Cl_list()
        cl_list_data.append(cl_list)

        cl_list.bezeich = "Out Of Order"
        cl_list.droom = dooo
        cl_list.proz1 =  to_decimal(dooo) / to_decimal(tot_room) * to_decimal("100")
        cl_list.mroom = mooo
        cl_list.proz2 =  to_decimal(mooo) / to_decimal(mtd_act) * to_decimal("100")
        cl_list.yroom = yooo
        cl_list.proz3 =  to_decimal(yooo) / to_decimal(ytd_act) * to_decimal("100")


        cl_list = Cl_list()
        cl_list_data.append(cl_list)


        if to_date < ci_date:

            zinrstat = get_cache (Zinrstat, {"zinr": [(eq, "tot-rm")],"datum": [(eq, to_date)]})

            if zinrstat:
                all_room = zinrstat.zimmeranz
        else:

            for zimmer in db_session.query(Zimmer).order_by(Zimmer._recid).all():
                all_room = all_room + 1


        cl_list = Cl_list()
        cl_list_data.append(cl_list)

        cl_list.bezeich = "# Active Rooms"
        cl_list.droom = tot_room
        cl_list.proz1 =  to_decimal("100")
        cl_list.mroom = mtd_act
        cl_list.proz2 =  to_decimal("100")
        cl_list.yroom = ytd_act
        cl_list.proz3 =  to_decimal("100")


        cl_list = Cl_list()
        cl_list_data.append(cl_list)

        cl_list.bezeich = "inactive Rooms"
        cl_list.droom = all_room - tot_room
        cl_list.mroom = mtd_totrm - mtd_act
        cl_list.yroom = ytd_totrm - ytd_act


        cl_list = Cl_list()
        cl_list_data.append(cl_list)

        cl_list.bezeich = "Total Rooms"
        cl_list.droom = all_room
        cl_list.mroom = mtd_totrm
        cl_list.yroom = ytd_totrm


        cl_list = Cl_list()
        cl_list_data.append(cl_list)

    def cal_umsatz3():

        nonlocal cl_list_data, lvcarea, do_it, droomrev, mroomrev, yroomrev, drevrev, mrevrev, yrevrev, dpaxrev, mpaxrev, ypaxrev, draterev, mraterev, yraterev, droomcomp, mroomcomp, yroomcomp, dpaxcomp, mpaxcomp, ypaxcomp, droomhu, mroomhu, yroomhu, dpaxhu, mpaxhu, ypaxhu, tot_room, all_room, dvacant, mvacant, yvacant, dooo, mooo, yooo, dnoshow, mnoshow, ynoshow, dcancel, mcancel, ycancel, cal_umsatz1_called, cal_umsatz4_called, droom, proz1, mroom, proz2, dpax, mpax, drate, mrate, drev, mrev, yroom, ypax, yrate, yrev, inactive, mtd_act, mtd_totrm, ytd_act, ytd_totrm, ci_date, htparam, zimmer, zkstat, zinrstat, genstat, segment, guestseg, reservation, res_line, outorder, artikel, umsatz
        nonlocal pvilanguage, opening_date, from_date, to_date, fdate, tdate, segmtype_exist, mi_mtd_chk, mi_ftd_chk, mi_exchu_chk, mi_exccomp_chk, long_digit


        nonlocal cl_list, om_list
        nonlocal cl_list_data, om_list_data

        i:int = 0
        max_i:int = 0
        datum:date = None
        art_list:List[int] = create_empty_list(150,0)
        serv_vat:bool = False
        fact:Decimal = to_decimal("0.0")
        serv:Decimal = to_decimal("0.0")
        vat:Decimal = to_decimal("0.0")
        drev_droom:Decimal = to_decimal("0.0")
        mrev_mroom:Decimal = to_decimal("0.0")
        yrev_yroom:Decimal = to_decimal("0.0")
        drev_droom1:Decimal = to_decimal("0.0")
        mrev_mroom1:Decimal = to_decimal("0.0")
        yrev_yroom1:Decimal = to_decimal("0.0")
        compli_count:Decimal = to_decimal("0.0")
        state_str:string = ""

        htparam = get_cache (Htparam, {"paramnr": [(eq, 479)]})
        serv_vat = htparam.flogical

        for artikel in db_session.query(Artikel).filter(
                 (Artikel.departement == 0) & (Artikel.artart == 0) & (Artikel.umsatzart == 1)).order_by(Artikel.artnr).all():
            max_i = max_i + 1
            art_list[max_i - 1] = artikel.artnr
        do_it = True

        if do_it:
            for i in range(1,max_i + 1) :

                artikel = get_cache (Artikel, {"artnr": [(eq, art_list[i - 1])],"departement": [(eq, 0)]})

                if artikel:
                    cl_list = Cl_list()
                    cl_list_data.append(cl_list)

                    cl_list.segm = artikel.artnr

                    if i >= 10:
                        cl_list.bezeich = translateExtended ("Other RmRev", lvcarea, "")
                    else:
                        cl_list.bezeich = artikel.bezeich
                    for datum in date_range(from_date,to_date) :
                        serv =  to_decimal("0")
                        vat =  to_decimal("0")

                        for umsatz in db_session.query(Umsatz).filter(
                                 (Umsatz.artnr == artikel.artnr) & (Umsatz.departement == artikel.departement) & (Umsatz.datum == datum)).order_by(Umsatz._recid).all():
                            serv, vat = get_output(calc_servvat(umsatz.departement, umsatz.artnr, umsatz.datum, artikel.service_code, artikel.mwst_code))
                            fact =  to_decimal(1.00) + to_decimal(serv) + to_decimal(vat)

                            if datum == to_date:
                                drevrev =  to_decimal(drevrev) + to_decimal(umsatz.betrag) / to_decimal(fact)
                                cl_list.drev =  to_decimal(umsatz.betrag) / to_decimal(fact)

                            if (mi_mtd_chk and get_month(datum) == get_month(to_date)) or (mi_ftd_chk and datum >= fdate and datum <= tdate):
                                mrevrev =  to_decimal(mrevrev) + to_decimal(umsatz.betrag) / to_decimal(fact)
                                cl_list.mrev =  to_decimal(cl_list.mrev) + to_decimal(umsatz.betrag) / to_decimal(fact)
                            yrevrev =  to_decimal(yrevrev) + to_decimal(umsatz.betrag) / to_decimal(fact)


                            cl_list.yrev =  to_decimal(cl_list.yrev) + to_decimal(umsatz.betrag) / to_decimal(fact)

                    if cl_list.mrev == 0:
                        cl_list.bezeich = "Deleted"
            cl_list = Cl_list()
            cl_list_data.append(cl_list)

        drev_droom =  to_decimal(drevrev) / to_decimal((droomrev) + to_decimal(droomhu) + to_decimal(droomcomp))

        if drev_droom == None:
            drev_droom =  to_decimal("0")
        mrev_mroom =  to_decimal(mrevrev) / to_decimal((mroomrev) + to_decimal(mroomhu) + to_decimal(mroomcomp))

        if mrev_mroom == None:
            mrev_mroom =  to_decimal("0")
        yrev_yroom =  to_decimal(yrevrev) / to_decimal((yroomrev) + to_decimal(yroomhu) + to_decimal(yroomcomp))

        if yrev_yroom == None:
            yrev_yroom =  to_decimal("0")

        if not mi_exchu_chk:
            droomrev = droomrev + droomhu
            mroomrev = mroomrev + mroomhu
            yroomrev = yroomrev + yroomhu

        if not mi_exccomp_chk:
            droomrev = droomrev + droomcomp
            mroomrev = mroomrev + mroomcomp
            yroomrev = yroomrev + yroomcomp


        drev_droom1 =  to_decimal(drevrev) / to_decimal(droomrev)

        if drev_droom1 == None:
            drev_droom1 =  to_decimal("0")
        mrev_mroom1 =  to_decimal(mrevrev) / to_decimal(mroomrev)

        if mrev_mroom1 == None:
            mrev_mroom1 =  to_decimal("0")
        yrev_yroom1 =  to_decimal(yrevrev) / to_decimal(yroomrev)

        if yrev_yroom1 == None:
            yrev_yroom1 =  to_decimal("0")

        if mi_exchu_chk and mi_exccomp_chk:
            state_str = translateExtended ("RmRev Exc Comp&HU", lvcarea, "")

        elif mi_exchu_chk:
            state_str = translateExtended ("RmRev Exc HU", lvcarea, "")

        elif mi_exccomp_chk:
            state_str = translateExtended ("RmRev Exc Comp", lvcarea, "")
        else:
            state_str = ""

        if not long_digit:
            cl_list = Cl_list()
            cl_list_data.append(cl_list)

            cl_list.bezeich = "RmRev Inc All"
            cl_list.drate =  to_decimal(drev_droom)
            cl_list.mrate =  to_decimal(mrev_mroom)
            cl_list.drev =  to_decimal(drevrev)
            cl_list.mrev =  to_decimal(mrevrev)
            cl_list.yrev =  to_decimal(yrevrev)
            cl_list.yrate =  to_decimal(yrev_yroom)


            cl_list = Cl_list()
            cl_list_data.append(cl_list)


            if mi_exchu_chk or mi_exccomp_chk:
                cl_list.bezeich = state_str
                cl_list.drate =  to_decimal(drev_droom1)
                cl_list.mrate =  to_decimal(mrev_mroom1)
                cl_list.drev =  to_decimal(drevrev)
                cl_list.mrev =  to_decimal(mrevrev)
                cl_list.yrev =  to_decimal(yrevrev)
                cl_list.yrate =  to_decimal(yrev_yroom1)


        else:
            cl_list = Cl_list()
            cl_list_data.append(cl_list)

            cl_list.bezeich = "RmRev Inc All"
            cl_list.drate =  to_decimal(drev_droom)
            cl_list.mrate =  to_decimal(mrev_mroom)
            cl_list.drev =  to_decimal(drevrev)
            cl_list.mrev =  to_decimal(mrevrev)
            cl_list.yrev =  to_decimal(yrevrev)
            cl_list.yrate =  to_decimal(yrev_yroom)


            cl_list = Cl_list()
            cl_list_data.append(cl_list)


            if mi_exchu_chk or mi_exccomp_chk:
                cl_list.bezeich = state_str
                cl_list.drate =  to_decimal(drev_droom1)
                cl_list.mrate =  to_decimal(mrev_mroom1)
                cl_list.drev =  to_decimal(drevrev)
                cl_list.mrev =  to_decimal(mrevrev)
                cl_list.yrev =  to_decimal(yrevrev)
                cl_list.yrate =  to_decimal(yrev_yroom1)


        cl_list = Cl_list()
        cl_list_data.append(cl_list)

    def no_show():

        nonlocal cl_list_data, lvcarea, do_it, droomrev, mroomrev, yroomrev, drevrev, mrevrev, yrevrev, dpaxrev, mpaxrev, ypaxrev, draterev, mraterev, yraterev, droomcomp, mroomcomp, yroomcomp, dpaxcomp, mpaxcomp, ypaxcomp, droomhu, mroomhu, yroomhu, dpaxhu, mpaxhu, ypaxhu, tot_room, all_room, dvacant, mvacant, yvacant, dooo, mooo, yooo, dnoshow, mnoshow, ynoshow, dcancel, mcancel, ycancel, cal_umsatz1_called, cal_umsatz4_called, droom, proz1, mroom, proz2, dpax, mpax, drate, mrate, drev, mrev, yroom, ypax, yrate, yrev, inactive, mtd_act, mtd_totrm, ytd_act, ytd_totrm, ci_date, htparam, zimmer, zkstat, zinrstat, genstat, segment, guestseg, reservation, res_line, outorder, artikel, umsatz
        nonlocal pvilanguage, opening_date, from_date, to_date, fdate, tdate, segmtype_exist, mi_mtd_chk, mi_ftd_chk, mi_exchu_chk, mi_exccomp_chk, long_digit


        nonlocal cl_list, om_list
        nonlocal cl_list_data, om_list_data

        i:int = 0
        dnoshow = 0
        dcancel = 0
        mnoshow = 0
        mcancel = 0

        for zinrstat in db_session.query(Zinrstat).filter(
                 (Zinrstat.zinr == ("No-Show").lower()) & (Zinrstat.datum >= from_date) & (Zinrstat.datum <= to_date)).order_by(Zinrstat._recid).all():

            if zinrstat.datum == to_date:
                dnoshow = dnoshow + zinrstat.zimmeranz

            if (mi_mtd_chk and get_month(zinrstat.datum) == get_month(to_date)) or (mi_ftd_chk and zinrstat.datum >= fdate and zinrstat.datum <= tdate):
                mnoshow = mnoshow + zinrstat.zimmeranz
            ynoshow = ynoshow + zinrstat.zimmeranz

        for zinrstat in db_session.query(Zinrstat).filter(
                 (Zinrstat.zinr == ("CancRes").lower()) & (Zinrstat.datum >= from_date) & (Zinrstat.datum <= to_date)).order_by(Zinrstat._recid).all():

            if zinrstat.datum == to_date:
                dcancel = dcancel + zinrstat.zimmeranz

            if get_month(zinrstat.datum) == get_month(to_date):
                mcancel = mcancel + zinrstat.zimmeranz


            ycancel = ycancel + zinrstat.zimmeranz
        cl_list = Cl_list()
        cl_list_data.append(cl_list)

        cl_list.bezeich = "NO SHOW"
        cl_list.droom = dnoshow
        cl_list.mroom = mnoshow
        cl_list.yroom = ynoshow


        cl_list = Cl_list()
        cl_list_data.append(cl_list)

        cl_list.bezeich = "C A N C E L"
        cl_list.droom = dcancel
        cl_list.mroom = mcancel
        cl_list.yroom = ycancel


        cl_list = Cl_list()
        cl_list_data.append(cl_list)

    def cal_umsatz4(i1:int, i2:int, i3:int, i4:int, rev_title:string, rev_title1:string, show_avrg:bool):

        nonlocal cl_list_data, lvcarea, do_it, droomrev, mroomrev, yroomrev, drevrev, mrevrev, yrevrev, dpaxrev, mpaxrev, ypaxrev, draterev, mraterev, yraterev, droomcomp, mroomcomp, yroomcomp, dpaxcomp, mpaxcomp, ypaxcomp, droomhu, mroomhu, yroomhu, dpaxhu, mpaxhu, ypaxhu, tot_room, all_room, dvacant, mvacant, yvacant, dooo, mooo, yooo, dnoshow, mnoshow, ynoshow, dcancel, mcancel, ycancel, cal_umsatz1_called, cal_umsatz4_called, droom, proz1, mroom, proz2, dpax, mpax, drate, mrate, drev, mrev, yroom, ypax, yrate, yrev, inactive, mtd_act, mtd_totrm, ytd_act, ytd_totrm, ci_date, htparam, zimmer, zkstat, zinrstat, genstat, segment, guestseg, reservation, res_line, outorder, artikel, umsatz
        nonlocal pvilanguage, opening_date, from_date, to_date, fdate, tdate, segmtype_exist, mi_mtd_chk, mi_ftd_chk, mi_exchu_chk, mi_exccomp_chk, long_digit


        nonlocal cl_list, om_list
        nonlocal cl_list_data, om_list_data

        i:int = 0
        datum:date = None
        do_it1:bool = False
        d1:date = None
        d2:date = None
        datum0:date = None
        datum1:date = None
        datum2:date = None
        curr_i:int = 0
        net_lodg:Decimal = to_decimal("0.0")
        fnet_lodg:Decimal = to_decimal("0.0")
        tot_breakfast:Decimal = to_decimal("0.0")
        tot_lunch:Decimal = to_decimal("0.0")
        tot_dinner:Decimal = to_decimal("0.0")
        tot_other:Decimal = to_decimal("0.0")
        tot_rmrev:Decimal = to_decimal("0.0")
        tot_vat:Decimal = to_decimal("0.0")
        tot_service:Decimal = to_decimal("0.0")
        bgenstat = None
        Bgenstat =  create_buffer("Bgenstat",Genstat)

        if not cal_umsatz4_called:
            d2 = from_date

            res_line_obj_list = {}
            res_line = Res_line()
            reservation = Reservation()
            for res_line.ankunft, res_line.abreise, res_line._recid, res_line.zimmeranz, res_line.erwachs, res_line.kind1, res_line.kind2, res_line.gratis, res_line.kontignr, reservation.segmentcode, reservation._recid in db_session.query(Res_line.ankunft, Res_line.abreise, Res_line._recid, Res_line.zimmeranz, Res_line.erwachs, Res_line.kind1, Res_line.kind2, Res_line.gratis, Res_line.kontignr, Reservation.segmentcode, Reservation._recid).join(Reservation,(Reservation.resnr == Res_line.resnr)).filter(
                     (((Res_line.resstatus <= 13) & (Res_line.resstatus != 4) & (Res_line.resstatus != 8) & (Res_line.resstatus != 9) & (Res_line.resstatus != 10) & (Res_line.resstatus != 12) & (Res_line.active_flag <= 1) & (not_ (Res_line.ankunft > to_date)) & (not_ (Res_line.abreise < d2)))) | ((Res_line.resstatus == 8) & (Res_line.active_flag == 2) & (Res_line.ankunft == ci_date) & (Res_line.abreise == ci_date)) & (Res_line.gastnr > 0) & (Res_line.l_zuordnung[inc_value(2)] == 0)).order_by(Res_line.resnr, Res_line.reslinnr.desc()).all():
                if res_line_obj_list.get(res_line._recid):
                    continue
                else:
                    res_line_obj_list[res_line._recid] = True


                curr_i = 0

                if res_line.kontignr < 0:
                    do_it1 = True

                    cl_list = query(cl_list_data, filters=(lambda cl_list: cl_list.segm == reservation.segmentcode), first=True)

                    if not cl_list:

                        segment = get_cache (Segment, {"segmentcode": [(eq, reservation.segmentcode)]})

                        if segment and not matches(segment.bezeich,r"*$$0"):

                            if segment.betriebsnr != 1 and segment.betriebsnr != 2:
                                cl_list = Cl_list()
                                cl_list_data.append(cl_list)

                                cl_list.compli = False
                                cl_list.segm = segment.segmentcode
                                cl_list.bezeich = segment.bezeich
                                cl_list.betriebsnr = segment.betriebsnr
                            else:
                                cl_list = Cl_list()
                                cl_list_data.append(cl_list)

                                cl_list.compli = True
                                cl_list.segm = segment.segmentcode
                                cl_list.bezeich = segment.bezeich
                                cl_list.betriebsnr = segment.betriebsnr
                        else:
                            do_it1 = False

                    if do_it1 :
                        datum1 = d2

                        if res_line.ankunft > datum1:
                            datum1 = res_line.ankunft
                        datum2 = to_date

                        if res_line.abreise < datum2:
                            datum2 = res_line.abreise
                        for datum0 in date_range(datum1,datum2) :
                            curr_i = curr_i + 1

                            if datum0 == res_line.abreise:
                                pass
                            else:
                                net_lodg =  to_decimal("0")
                                tot_breakfast =  to_decimal("0")
                                tot_lunch =  to_decimal("0")
                                tot_dinner =  to_decimal("0")
                                tot_other =  to_decimal("0")


                                fnet_lodg, net_lodg, tot_breakfast, tot_lunch, tot_dinner, tot_other, tot_rmrev, tot_vat, tot_service = get_output(get_room_breakdown(res_line._recid, datum0, curr_i, from_date))

                                if datum0 == to_date:
                                    cl_list.droom = cl_list.droom + res_line.zimmeranz
                                    cl_list.dpax = cl_list.dpax + res_line.erwachs + res_line.kind1 + res_line.kind2 + res_line.gratis
                                    cl_list.drev =  to_decimal(cl_list.drev) + to_decimal(net_lodg)

                                    if cl_list.betriebsnr != 1 and cl_list.betriebsnr != 2:
                                        droomrev = droomrev + res_line.zimmeranz
                                        dpaxrev = dpaxrev + res_line.erwachs + res_line.kind1 + res_line.kind2 + res_line.gratis
                                        drevrev =  to_decimal(drevrev) + to_decimal(net_lodg)

                                    if cl_list.betriebsnr == 1:
                                        droomcomp = droomcomp + res_line.zimmeranz
                                        dpaxcomp = dpaxcomp + res_line.erwachs + res_line.kind1 + res_line.kind2 + res_line.gratis

                                    if cl_list.betriebsnr == 2:
                                        droomhu = droomhu + res_line.zimmeranz
                                        dpaxhu = dpaxhu + res_line.erwachs + res_line.kind1 + res_line.kind2 + res_line.gratis

                                if (mi_mtd_chk and get_month(datum0) == get_month(to_date)) or (mi_ftd_chk and datum0 >= d2 and datum0 <= tdate):
                                    cl_list.mroom = cl_list.mroom + res_line.zimmeranz
                                    cl_list.mpax = cl_list.mpax + res_line.erwachs + res_line.kind1 + res_line.kind2 + res_line.gratis
                                    cl_list.mrev =  to_decimal(cl_list.mrev) + to_decimal(net_lodg)

                                    if cl_list.betriebsnr != 1 and cl_list.betriebsnr != 2:
                                        mroomrev = mroomrev + res_line.zimmeranz
                                        mpaxrev = mpaxrev + res_line.erwachs + res_line.kind1 + res_line.kind2 + res_line.gratis
                                        mrevrev =  to_decimal(mrevrev) + to_decimal(net_lodg)

                                    if cl_list.betriebsnr == 1:
                                        mroomcomp = mroomcomp + res_line.zimmeranz
                                        mpaxcomp = mpaxcomp + res_line.erwachs + res_line.kind1 + res_line.kind2 + res_line.gratis

                                    if cl_list.betriebsnr == 2:
                                        mroomhu = mroomhu + res_line.zimmeranz
                                        mpaxhu = mpaxhu + res_line.erwachs + res_line.kind1 + res_line.kind2 + res_line.gratis
                                cl_list.yroom = cl_list.yroom + res_line.zimmeranz


                                cl_list.ypax = cl_list.ypax + res_line.erwachs + res_line.kind1 + res_line.kind2 + res_line.gratis
                                cl_list.yrev =  to_decimal(cl_list.yrev) + to_decimal(net_lodg)

                                if cl_list.betriebsnr != 1 and cl_list.betriebsnr != 2:
                                    yroomrev = yroomrev + res_line.zimmeranz
                                    ypaxrev = ypaxrev + res_line.erwachs + res_line.kind1 + res_line.kind2 + res_line.gratis
                                    yrevrev =  to_decimal(yrevrev) + to_decimal(net_lodg)

                                if cl_list.betriebsnr == 1:
                                    yroomcomp = yroomcomp + res_line.zimmeranz
                                    ypaxcomp = ypaxcomp + res_line.erwachs + res_line.kind1 + res_line.kind2 + res_line.gratis

                                if cl_list.betriebsnr == 2:
                                    yroomhu = yroomhu + res_line.zimmeranz
                                    ypaxhu = ypaxhu + res_line.erwachs + res_line.kind1 + res_line.kind2 + res_line.gratis
            cal_umsatz4_called = True

        for cl_list in query(cl_list_data, filters=(lambda cl_list:((cl_list.segm >= i1 and cl_list.segm <= i2) or (cl_list.segm >= i3 and cl_list.segm <= i4)))):

            if cl_list.droom != 0:
                cl_list.drate =  to_decimal(cl_list.drev) / to_decimal(cl_list.droom)

            if cl_list.mroom != 0:
                cl_list.mrate =  to_decimal(cl_list.mrev) / to_decimal(cl_list.mroom)
            cl_list.proz1 =  to_decimal(100.0) * to_decimal(cl_list.droom) / to_decimal(tot_room)
            cl_list.proz2 =  to_decimal(100.0) * to_decimal(cl_list.mroom) / to_decimal(mtd_act)
            cl_list.proz3 =  to_decimal(100.0) * to_decimal(cl_list.yroom) / to_decimal(ytd_act)

            if droomrev != 0:
                draterev =  to_decimal(drevrev) / to_decimal(droomrev)

            if mroomrev != 0:
                mraterev =  to_decimal(mrevrev) / to_decimal(mroomrev)

            if yroomrev != 0:
                yraterev =  to_decimal(yrevrev) / to_decimal(yroomrev)

            if cl_list.proz1 == None:
                cl_list.proz1 =  to_decimal("0")

            if cl_list.proz2 == None:
                cl_list.proz2 =  to_decimal("0")

            if cl_list.proz3 == None:
                cl_list.proz3 =  to_decimal("0")

            if cl_list.drev == 0 and cl_list.mrev == 0 and cl_list.yrev == 0:
                cl_list.zero_flag = True
        cl_list = Cl_list()
        cl_list_data.append(cl_list)

        cl_list = Cl_list()
        cl_list_data.append(cl_list)

        cl_list.bezeich = to_string(rev_title, "x(16)")
        cl_list.droom = droomrev
        cl_list.proz1 =  to_decimal(droomrev) / to_decimal(tot_room) * to_decimal("100")
        cl_list.mroom = mroomrev
        cl_list.proz2 =  to_decimal(mroomrev) / to_decimal(mtd_act) * to_decimal("100")
        cl_list.dpax = dpaxrev
        cl_list.mpax = mpaxrev
        cl_list.yroom = yroomrev
        cl_list.ypax = ypaxrev
        cl_list.proz3 =  to_decimal(ytd_act) * to_decimal("100")
        cl_list.drev =  to_decimal(drevrev)
        cl_list.mrev =  to_decimal(mrevrev)
        cl_list.yrev =  to_decimal(yrevrev)

        if show_avrg:

            if droomrev != 0:
                cl_list.drate =  to_decimal(drevrev) / to_decimal(droomrev)
            else:
                cl_list.drate =  to_decimal("0")

            if mroomrev != 0:
                cl_list.mrate =  to_decimal(mrevrev) / to_decimal(mroomrev)
            else:
                cl_list.mrate =  to_decimal("0")

            if yroomrev != 0:
                cl_list.yrate =  to_decimal(yrevrev) / to_decimal(yroomrev)
            else:
                cl_list.yrate =  to_decimal("0")

        if rev_title1 != "":
            cl_list = Cl_list()
            cl_list_data.append(cl_list)

            cl_list.bezeich = rev_title1

            if droomrev != 0:
                cl_list.proz1 = ( to_decimal(dpaxrev) - to_decimal(droomrev)) / to_decimal(droomrev) * to_decimal("100")
            else:
                cl_list.proz1 =  to_decimal("0")

            if mroomrev != 0:
                cl_list.proz2 = ( to_decimal(mpaxrev) - to_decimal(mroomrev)) / to_decimal(mroomrev) * to_decimal("100")
            else:
                cl_list.proz2 =  to_decimal("0")

            if yroomrev != 0:
                cl_list.proz3 = ( to_decimal(ypaxrev) - to_decimal(yroomrev)) / to_decimal(yroomrev) * to_decimal("100")
            else:
                cl_list.proz3 =  to_decimal("0")
        cl_list = Cl_list()
        cl_list_data.append(cl_list)

    def cal_umsatz4a(i1:int, i2:int, rev_title:string, rev_title1:string, show_avrg:bool):

        nonlocal cl_list_data, lvcarea, do_it, droomrev, mroomrev, yroomrev, drevrev, mrevrev, yrevrev, dpaxrev, mpaxrev, ypaxrev, draterev, mraterev, yraterev, droomcomp, mroomcomp, yroomcomp, dpaxcomp, mpaxcomp, ypaxcomp, droomhu, mroomhu, yroomhu, dpaxhu, mpaxhu, ypaxhu, tot_room, all_room, dvacant, mvacant, yvacant, dooo, mooo, yooo, dnoshow, mnoshow, ynoshow, dcancel, mcancel, ycancel, cal_umsatz1_called, cal_umsatz4_called, droom, proz1, mroom, proz2, dpax, mpax, drate, mrate, drev, mrev, yroom, ypax, yrate, yrev, inactive, mtd_act, mtd_totrm, ytd_act, ytd_totrm, ci_date, htparam, zimmer, zkstat, zinrstat, genstat, segment, guestseg, reservation, res_line, outorder, artikel, umsatz
        nonlocal pvilanguage, opening_date, from_date, to_date, fdate, tdate, segmtype_exist, mi_mtd_chk, mi_ftd_chk, mi_exchu_chk, mi_exccomp_chk, long_digit


        nonlocal cl_list, om_list
        nonlocal cl_list_data, om_list_data

        i:int = 0
        tot_proz3:Decimal = to_decimal("0.0")
        inact:bool = False
        do_it1:bool = False
        d1:date = None
        d2:date = None
        datum0:date = None
        datum1:date = None
        datum2:date = None
        curr_i:int = 0
        net_lodg:Decimal = to_decimal("0.0")
        fnet_lodg:Decimal = to_decimal("0.0")
        tot_breakfast:Decimal = to_decimal("0.0")
        tot_lunch:Decimal = to_decimal("0.0")
        tot_dinner:Decimal = to_decimal("0.0")
        tot_other:Decimal = to_decimal("0.0")
        tot_rmrev:Decimal = to_decimal("0.0")
        tot_vat:Decimal = to_decimal("0.0")
        tot_service:Decimal = to_decimal("0.0")
        bgenstat = None
        Bgenstat =  create_buffer("Bgenstat",Genstat)
        d2 = from_date

        res_line_obj_list = {}
        res_line = Res_line()
        reservation = Reservation()
        for res_line.ankunft, res_line.abreise, res_line._recid, res_line.zimmeranz, res_line.erwachs, res_line.kind1, res_line.kind2, res_line.gratis, res_line.kontignr, reservation.segmentcode, reservation._recid in db_session.query(Res_line.ankunft, Res_line.abreise, Res_line._recid, Res_line.zimmeranz, Res_line.erwachs, Res_line.kind1, Res_line.kind2, Res_line.gratis, Res_line.kontignr, Reservation.segmentcode, Reservation._recid).join(Reservation,(Reservation.resnr == Res_line.resnr)).filter(
                     (((Res_line.resstatus <= 13) & (Res_line.resstatus != 4) & (Res_line.resstatus != 8) & (Res_line.resstatus != 9) & (Res_line.resstatus != 10) & (Res_line.resstatus != 12) & (Res_line.active_flag <= 1) & (not_ (Res_line.ankunft > to_date)) & (not_ (Res_line.abreise < d2)))) | ((Res_line.resstatus == 8) & (Res_line.active_flag == 2) & (Res_line.ankunft == ci_date) & (Res_line.abreise == ci_date)) & (Res_line.gastnr > 0) & (Res_line.l_zuordnung[inc_value(2)] == 0)).order_by(Res_line.resnr, Res_line.reslinnr.desc()).all():
            if res_line_obj_list.get(res_line._recid):
                continue
            else:
                res_line_obj_list[res_line._recid] = True


            curr_i = 0

            if res_line.kontignr < 0:
                do_it1 = True

                cl_list = query(cl_list_data, filters=(lambda cl_list: cl_list.segm == reservation.segmentcode), first=True)

                if not cl_list:

                    segment = get_cache (Segment, {"segmentcode": [(eq, reservation.segmentcode)]})

                    if segment and not matches(segment.bezeich,r"*$$0"):

                        if segment.betriebsnr != 1 and segment.betriebsnr != 2:
                            cl_list = Cl_list()
                            cl_list_data.append(cl_list)

                            cl_list.compli = False
                            cl_list.segm = segment.segmentcode
                            cl_list.bezeich = segment.bezeich
                            cl_list.betriebsnr = segment.betriebsnr
                        else:
                            cl_list = Cl_list()
                            cl_list_data.append(cl_list)

                            cl_list.compli = True
                            cl_list.segm = segment.segmentcode
                            cl_list.bezeich = segment.bezeich
                            cl_list.betriebsnr = segment.betriebsnr
                    else:
                        do_it1 = False

                if do_it1 :
                    datum1 = d2

                    if res_line.ankunft > datum1:
                        datum1 = res_line.ankunft
                    datum2 = to_date

                    if res_line.abreise < datum2:
                        datum2 = res_line.abreise
                    for datum0 in date_range(datum1,datum2) :
                        curr_i = curr_i + 1

                        if datum0 != res_line.abreise:
                            net_lodg =  to_decimal("0")
                            tot_breakfast =  to_decimal("0")
                            tot_lunch =  to_decimal("0")
                            tot_dinner =  to_decimal("0")
                            tot_other =  to_decimal("0")


                            fnet_lodg, net_lodg, tot_breakfast, tot_lunch, tot_dinner, tot_other, tot_rmrev, tot_vat, tot_service = get_output(get_room_breakdown(res_line._recid, datum0, curr_i, from_date))

                            if datum0 == to_date:
                                cl_list.droom = cl_list.droom + res_line.zimmeranz
                                cl_list.dpax = cl_list.dpax + res_line.erwachs + res_line.kind1 + res_line.kind2 + res_line.gratis
                                cl_list.drev =  to_decimal(cl_list.drev) + to_decimal(net_lodg)

                                if cl_list.betriebsnr != 1 and cl_list.betriebsnr != 2:
                                    droomrev = droomrev + res_line.zimmeranz
                                    dpaxrev = dpaxrev + res_line.erwachs + res_line.kind1 + res_line.kind2 + res_line.gratis
                                    drevrev =  to_decimal(drevrev) + to_decimal(net_lodg)

                                if cl_list.betriebsnr == 1:
                                    droomcomp = droomcomp + res_line.zimmeranz
                                    dpaxcomp = dpaxcomp + res_line.erwachs + res_line.kind1 + res_line.kind2 + res_line.gratis

                                if cl_list.betriebsnr == 2:
                                    droomhu = droomhu + res_line.zimmeranz
                                    dpaxhu = dpaxhu + res_line.erwachs + res_line.kind1 + res_line.kind2 + res_line.gratis

                            if (mi_mtd_chk and get_month(datum0) == get_month(to_date)) or (mi_ftd_chk and datum0 >= d2 and datum0 <= tdate):
                                cl_list.mroom = cl_list.mroom + res_line.zimmeranz
                                cl_list.mpax = cl_list.mpax + res_line.erwachs + res_line.kind1 + res_line.kind2 + res_line.gratis
                                cl_list.mrev =  to_decimal(cl_list.mrev) + to_decimal(net_lodg)

                                if cl_list.betriebsnr != 1 and cl_list.betriebsnr != 2:
                                    mroomrev = mroomrev + res_line.zimmeranz
                                    mpaxrev = mpaxrev + res_line.erwachs + res_line.kind1 + res_line.kind2 + res_line.gratis
                                    mrevrev =  to_decimal(mrevrev) + to_decimal(net_lodg)

                                if cl_list.betriebsnr == 1:
                                    mroomcomp = mroomcomp + res_line.zimmeranz
                                    mpaxcomp = mpaxcomp + res_line.erwachs + res_line.kind1 + res_line.kind2 + res_line.gratis

                                if cl_list.betriebsnr == 2:
                                    mroomhu = mroomhu + res_line.zimmeranz
                                    mpaxhu = mpaxhu + res_line.erwachs + res_line.kind1 + res_line.kind2 + res_line.gratis
                            cl_list.yroom = cl_list.yroom + res_line.zimmeranz


                            cl_list.ypax = cl_list.ypax + res_line.erwachs + res_line.kind1 + res_line.kind2 + res_line.gratis
                            cl_list.yrev =  to_decimal(cl_list.yrev) + to_decimal(net_lodg)

                            if cl_list.betriebsnr != 1 and cl_list.betriebsnr != 2:
                                yroomrev = yroomrev + res_line.zimmeranz
                                ypaxrev = ypaxrev + res_line.erwachs + res_line.kind1 + res_line.kind2 + res_line.gratis
                                yrevrev =  to_decimal(yrevrev) + to_decimal(net_lodg)

                            if cl_list.betriebsnr == 1:
                                yroomcomp = yroomcomp + res_line.zimmeranz
                                ypaxcomp = ypaxcomp + res_line.erwachs + res_line.kind1 + res_line.kind2 + res_line.gratis

                            if cl_list.betriebsnr == 2:
                                yroomhu = yroomhu + res_line.zimmeranz
                                ypaxhu = ypaxhu + res_line.erwachs + res_line.kind1 + res_line.kind2 + res_line.gratis

        if inact:

            for cl_list in query(cl_list_data, filters=(lambda cl_list:(cl_list.betriebsnr >= i1 and cl_list.betriebsnr <= i2))):

                if cl_list.droom != 0:
                    cl_list.drate =  to_decimal(cl_list.drev) / to_decimal(cl_list.droom)

                if cl_list.mroom != 0:
                    cl_list.mrate =  to_decimal(cl_list.mrev) / to_decimal(cl_list.mroom)

                if cl_list.yroom != 0:
                    cl_list.yrate =  to_decimal(cl_list.yrev) / to_decimal(cl_list.yroom)
                cl_list.proz1 =  to_decimal(100.0) * to_decimal(cl_list.droom) / to_decimal(tot_room)
                cl_list.proz2 =  to_decimal(100.0) * to_decimal(cl_list.mroom) / to_decimal(mtd_act)
                cl_list.proz3 =  to_decimal(100.0) * to_decimal(cl_list.yroom) / to_decimal(ytd_act)

                if droomrev != 0:
                    draterev =  to_decimal(drevrev) / to_decimal(droomrev)

                if mroomrev != 0:
                    mraterev =  to_decimal(mrevrev) / to_decimal(mroomrev)

                if yroomrev != 0:
                    yraterev =  to_decimal(yrevrev) / to_decimal(yroomrev)

                if cl_list.proz1 == None:
                    cl_list.proz1 =  to_decimal("0")

                if cl_list.proz2 == None:
                    cl_list.proz2 =  to_decimal("0")

                if cl_list.proz3 == None:
                    cl_list.proz3 =  to_decimal("0")
                tot_proz3 =  to_decimal(tot_proz3) + to_decimal(cl_list.proz3)

                if cl_list.drev == 0 and cl_list.mrev == 0 and cl_list.yrev == 0:
                    cl_list.zero_flag = True
            cl_list = Cl_list()
            cl_list_data.append(cl_list)

        cl_list = Cl_list()
        cl_list_data.append(cl_list)

        cl_list.bezeich = rev_title
        cl_list.droom = droomrev
        cl_list.proz1 =  to_decimal(droomrev) / to_decimal(tot_room) * to_decimal("100")
        cl_list.mroom = mroomrev
        cl_list.proz2 =  to_decimal(mroomrev) / to_decimal(mtd_act) * to_decimal("100")
        cl_list.dpax = dpaxrev
        cl_list.mpax = mpaxrev
        cl_list.yroom = yroomrev
        cl_list.ypax = ypaxrev
        cl_list.proz3 =  to_decimal(tot_proz3)
        cl_list.drev =  to_decimal(drevrev)
        cl_list.mrev =  to_decimal(mrevrev)
        cl_list.yrev =  to_decimal(yrevrev)

        if show_avrg:

            if droomrev != 0:
                cl_list.drate =  to_decimal(drevrev) / to_decimal(droomrev)
            else:
                cl_list.drate =  to_decimal("0")

            if mroomrev != 0:
                cl_list.mrate =  to_decimal(mrevrev) / to_decimal(mroomrev)
            else:
                cl_list.mrate =  to_decimal("0")

            if yroomrev != 0:
                cl_list.yrate =  to_decimal(yrevrev) / to_decimal(yroomrev)
            else:
                cl_list.yrate =  to_decimal("0")
        cl_list = Cl_list()
        cl_list_data.append(cl_list)

    def cal_umsatz4b(i1:int, i2:int, rev_title:string, rev_title1:string, show_avrg:bool):

        nonlocal cl_list_data, lvcarea, do_it, droomrev, mroomrev, yroomrev, drevrev, mrevrev, yrevrev, dpaxrev, mpaxrev, ypaxrev, draterev, mraterev, yraterev, droomcomp, mroomcomp, yroomcomp, dpaxcomp, mpaxcomp, ypaxcomp, droomhu, mroomhu, yroomhu, dpaxhu, mpaxhu, ypaxhu, tot_room, all_room, dvacant, mvacant, yvacant, dooo, mooo, yooo, dnoshow, mnoshow, ynoshow, dcancel, mcancel, ycancel, cal_umsatz1_called, cal_umsatz4_called, droom, proz1, mroom, proz2, dpax, mpax, drate, mrate, drev, mrev, yroom, ypax, yrate, yrev, inactive, mtd_act, mtd_totrm, ytd_act, ytd_totrm, ci_date, htparam, zimmer, zkstat, zinrstat, genstat, segment, guestseg, reservation, res_line, outorder, artikel, umsatz
        nonlocal pvilanguage, opening_date, from_date, to_date, fdate, tdate, segmtype_exist, mi_mtd_chk, mi_ftd_chk, mi_exchu_chk, mi_exccomp_chk, long_digit


        nonlocal cl_list, om_list
        nonlocal cl_list_data, om_list_data

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
        net_lodg:Decimal = to_decimal("0.0")
        fnet_lodg:Decimal = to_decimal("0.0")
        tot_breakfast:Decimal = to_decimal("0.0")
        tot_lunch:Decimal = to_decimal("0.0")
        tot_dinner:Decimal = to_decimal("0.0")
        tot_other:Decimal = to_decimal("0.0")
        tot_rmrev:Decimal = to_decimal("0.0")
        tot_vat:Decimal = to_decimal("0.0")
        tot_service:Decimal = to_decimal("0.0")
        bgenstat = None
        Bgenstat =  create_buffer("Bgenstat",Genstat)

        if inact:

            for cl_list in query(cl_list_data, filters=(lambda cl_list: cl_list.compli)):

                if cl_list.droom != 0:
                    cl_list.drate =  to_decimal(cl_list.drev) / to_decimal(cl_list.droom)

                if cl_list.mroom != 0:
                    cl_list.mrate =  to_decimal(cl_list.mrev) / to_decimal(cl_list.mroom)

                if cl_list.yroom != 0:
                    cl_list.yrate =  to_decimal(cl_list.yrev) / to_decimal(cl_list.yroom)
                cl_list.proz1 =  to_decimal(100.0) * to_decimal(cl_list.droom) / to_decimal(tot_room)
                cl_list.proz2 =  to_decimal(100.0) * to_decimal(cl_list.mroom) / to_decimal(mtd_act)
                cl_list.proz3 =  to_decimal(100.0) * to_decimal(cl_list.yroom) / to_decimal(ytd_act)

                if cl_list.proz1 == None:
                    cl_list.proz1 =  to_decimal("0")

                if cl_list.proz2 == None:
                    cl_list.proz2 =  to_decimal("0")

                if cl_list.proz3 == None:
                    cl_list.proz3 =  to_decimal("0")
            cl_list = Cl_list()
            cl_list_data.append(cl_list)

        cl_list = Cl_list()
        cl_list_data.append(cl_list)

        cl_list.bezeich = rev_title
        cl_list.droom = droomrev + droomcomp + droomhu
        cl_list.proz1 = ( to_decimal(droomrev) + to_decimal(droomcomp) + to_decimal(droomhu)) / to_decimal(tot_room) * to_decimal("100")
        cl_list.mroom = mroomrev + mroomcomp + mroomhu
        cl_list.proz2 = ( to_decimal(mroomrev) + to_decimal(mroomcomp) + to_decimal(mroomhu)) / to_decimal(mtd_act) * to_decimal("100")
        cl_list.dpax = dpaxrev + dpaxcomp + dpaxhu
        cl_list.mpax = mpaxrev + mpaxcomp + mpaxhu
        cl_list.yroom = yroomrev + yroomcomp + yroomhu
        cl_list.ypax = ypaxrev + ypaxcomp + ypaxhu
        cl_list.proz3 = ( to_decimal(yroomrev) + to_decimal(yroomcomp) + to_decimal(yroomhu)) / to_decimal(ytd_act) * to_decimal("100")
        cl_list.drev =  to_decimal(drevrev)
        cl_list.mrev =  to_decimal(mrevrev)
        cl_list.yrev =  to_decimal(yrevrev)

        if show_avrg:

            if (droomrev + droomcomp + droomhu) != 0:
                cl_list.drate =  to_decimal(drevrev) / to_decimal((droomrev) + to_decimal(droomcomp) + to_decimal(droomhu))
            else:
                cl_list.drate =  to_decimal("0")

            if (mroomrev + mroomcomp + mroomhu) != 0:
                cl_list.mrate =  to_decimal(mrevrev) / to_decimal((mroomrev) + to_decimal(mroomcomp) + to_decimal(mroomhu))
            else:
                cl_list.mrate =  to_decimal("0")

            if (yroomrev + yroomcomp + yroomhu) != 0:
                cl_list.yrate =  to_decimal(yrevrev) / to_decimal((yroomrev) + to_decimal(yroomcomp) + to_decimal(yroomhu))
            else:
                cl_list.yrate =  to_decimal("0")

        if rev_title1 != "":
            cl_list = Cl_list()
            cl_list_data.append(cl_list)

            cl_list.bezeich = rev_title1

            if (droomrev + droomcomp + droomhu) != 0:
                cl_list.proz1 = ( to_decimal((dpaxrev) + to_decimal(dpaxcomp) + to_decimal(dpaxhu)) - to_decimal((droomrev) + to_decimal(droomcomp) + to_decimal(droomhu))) / to_decimal((droomrev) + to_decimal(droomcomp) + to_decimal(droomhu)) * to_decimal("100")
            else:
                cl_list.proz1 =  to_decimal("0")

            if (mroomrev + mroomcomp + mroomhu) != 0:
                cl_list.proz2 = ( to_decimal((mpaxrev) + to_decimal(mpaxcomp) + to_decimal(mpaxhu)) - to_decimal((mroomrev) + to_decimal(mroomcomp) + to_decimal(mroomhu))) / to_decimal((mroomrev) + to_decimal(mroomcomp) + to_decimal(mroomhu)) * to_decimal("100")
            else:
                cl_list.proz2 =  to_decimal("0")

            if (yroomrev + yroomcomp + yroomhu) != 0:
                cl_list.proz3 = ( to_decimal((ypaxrev) + to_decimal(ypaxcomp) + to_decimal(ypaxhu)) - to_decimal((yroomrev) + to_decimal(yroomcomp) + to_decimal(yroomhu))) / to_decimal((yroomrev) + to_decimal(yroomcomp) + to_decimal(yroomhu)) * to_decimal("100")
            else:
                cl_list.proz3 =  to_decimal("0")
        cl_list = Cl_list()
        cl_list_data.append(cl_list)

    def cal_umsatz5():

        nonlocal cl_list_data, lvcarea, do_it, droomrev, mroomrev, yroomrev, drevrev, mrevrev, yrevrev, dpaxrev, mpaxrev, ypaxrev, draterev, mraterev, yraterev, droomcomp, mroomcomp, yroomcomp, dpaxcomp, mpaxcomp, ypaxcomp, droomhu, mroomhu, yroomhu, dpaxhu, mpaxhu, ypaxhu, tot_room, all_room, dvacant, mvacant, yvacant, dooo, mooo, yooo, dnoshow, mnoshow, ynoshow, dcancel, mcancel, ycancel, cal_umsatz1_called, cal_umsatz4_called, droom, proz1, mroom, proz2, dpax, mpax, drate, mrate, drev, mrev, yroom, ypax, yrate, yrev, inactive, mtd_act, mtd_totrm, ytd_act, ytd_totrm, ci_date, htparam, zimmer, zkstat, zinrstat, genstat, segment, guestseg, reservation, res_line, outorder, artikel, umsatz
        nonlocal pvilanguage, opening_date, from_date, to_date, fdate, tdate, segmtype_exist, mi_mtd_chk, mi_ftd_chk, mi_exchu_chk, mi_exccomp_chk, long_digit


        nonlocal cl_list, om_list
        nonlocal cl_list_data, om_list_data

        i:int = 0
        datum:date = None
        datum1:date = None
        dooo = 0
        mooo = 0
        yooo = 0
        for datum in date_range(from_date,to_date) :

            outorder_obj_list = {}
            for outorder, zimmer in db_session.query(Outorder, Zimmer).join(Zimmer,(Zimmer.zinr == Outorder.zinr)).filter(
                     ((Outorder.gespstart >= datum) & (Outorder.gespstart <= datum)) | ((Outorder.gespstart <= datum) & (Outorder.gespende >= datum))).order_by(Outorder._recid).all():
                if outorder_obj_list.get(outorder._recid):
                    continue
                else:
                    outorder_obj_list[outorder._recid] = True

                if datum == to_date:
                    dooo = dooo + 1

                om_list = query(om_list_data, filters=(lambda om_list: om_list.zinr == outorder.zinr and om_list.gespstart == outorder.gespstart and om_list.gespende == outorder.gespende), first=True)

                if not om_list:
                    om_list = Om_list()
                    om_list_data.append(om_list)

                    om_list.zinr = outorder.zinr
                    om_list.gespstart = outorder.gespstart
                    om_list.gespende = outorder.gespende
                    mooo = mooo + 1
                yooo = yooo + 1
        dvacant = tot_room - dooo - (droomrev + droomcomp + droomhu)
        mvacant = mtd_act - mooo - (mroomrev + mroomcomp + mroomhu)
        yvacant = ytd_act - yooo - (yroomrev + yroomcomp + yroomhu)

        if to_date == opening_date:
            mvacant = dvacant
            yvacant = dvacant
            mooo = dooo
            yooo = dooo
        cl_list = Cl_list()
        cl_list_data.append(cl_list)

        cl_list.bezeich = "V A C A N T"
        cl_list.droom = dvacant
        cl_list.proz1 =  to_decimal(dvacant) / to_decimal(tot_room) * to_decimal("100")
        cl_list.mroom = mvacant
        cl_list.proz2 =  to_decimal(mvacant) / to_decimal(mtd_act) * to_decimal("100")
        cl_list.yroom = yvacant
        cl_list.proz3 =  to_decimal(yvacant) / to_decimal(ytd_act) * to_decimal("100")


        cl_list = Cl_list()
        cl_list_data.append(cl_list)

        cl_list.bezeich = "Out Of Order"
        cl_list.droom = dooo
        cl_list.proz1 =  to_decimal(dooo) / to_decimal(tot_room) * to_decimal("100")
        cl_list.mroom = mooo
        cl_list.proz2 =  to_decimal(mooo) / to_decimal(mtd_act) * to_decimal("100")
        cl_list.yroom = yooo
        cl_list.proz3 =  to_decimal(yooo) / to_decimal(ytd_act) * to_decimal("100")


        cl_list = Cl_list()
        cl_list_data.append(cl_list)


        if to_date < ci_date:

            zinrstat = get_cache (Zinrstat, {"zinr": [(eq, "tot-rm")],"datum": [(eq, to_date)]})

            if zinrstat:
                all_room = zinrstat.zimmeranz
        else:

            for zimmer in db_session.query(Zimmer).order_by(Zimmer._recid).all():
                all_room = all_room + 1


        cl_list = Cl_list()
        cl_list_data.append(cl_list)

        cl_list.bezeich = "# Active Rooms"
        cl_list.droom = tot_room
        cl_list.proz1 =  to_decimal("100")
        cl_list.mroom = mtd_act
        cl_list.proz2 =  to_decimal("100")
        cl_list.yroom = ytd_act
        cl_list.proz3 =  to_decimal("100")


        cl_list = Cl_list()
        cl_list_data.append(cl_list)

        cl_list.bezeich = "inactive Rooms"
        cl_list.droom = all_room - tot_room
        cl_list.mroom = mtd_totrm - mtd_act
        cl_list.yroom = ytd_totrm - ytd_act


        cl_list = Cl_list()
        cl_list_data.append(cl_list)

        cl_list.bezeich = "Total Rooms"
        cl_list.droom = all_room
        cl_list.mroom = mtd_totrm
        cl_list.yroom = ytd_totrm


        cl_list = Cl_list()
        cl_list_data.append(cl_list)

    def cal_umsatz6():

        nonlocal cl_list_data, lvcarea, do_it, droomrev, mroomrev, yroomrev, drevrev, mrevrev, yrevrev, dpaxrev, mpaxrev, ypaxrev, draterev, mraterev, yraterev, droomcomp, mroomcomp, yroomcomp, dpaxcomp, mpaxcomp, ypaxcomp, droomhu, mroomhu, yroomhu, dpaxhu, mpaxhu, ypaxhu, tot_room, all_room, dvacant, mvacant, yvacant, dooo, mooo, yooo, dnoshow, mnoshow, ynoshow, dcancel, mcancel, ycancel, cal_umsatz1_called, cal_umsatz4_called, droom, proz1, mroom, proz2, dpax, mpax, drate, mrate, drev, mrev, yroom, ypax, yrate, yrev, inactive, mtd_act, mtd_totrm, ytd_act, ytd_totrm, ci_date, htparam, zimmer, zkstat, zinrstat, genstat, segment, guestseg, reservation, res_line, outorder, artikel, umsatz
        nonlocal pvilanguage, opening_date, from_date, to_date, fdate, tdate, segmtype_exist, mi_mtd_chk, mi_ftd_chk, mi_exchu_chk, mi_exccomp_chk, long_digit


        nonlocal cl_list, om_list
        nonlocal cl_list_data, om_list_data

        i:int = 0
        max_i:int = 0
        datum:date = None
        art_list:List[int] = create_empty_list(150,0)
        serv_vat:bool = False
        fact:Decimal = to_decimal("0.0")
        serv:Decimal = to_decimal("0.0")
        vat:Decimal = to_decimal("0.0")
        drev_droom:Decimal = to_decimal("0.0")
        mrev_mroom:Decimal = to_decimal("0.0")
        yrev_yroom:Decimal = to_decimal("0.0")
        drev_droom1:Decimal = to_decimal("0.0")
        mrev_mroom1:Decimal = to_decimal("0.0")
        yrev_yroom1:Decimal = to_decimal("0.0")
        compli_count:Decimal = to_decimal("0.0")
        state_str:string = ""

        htparam = get_cache (Htparam, {"paramnr": [(eq, 479)]})
        serv_vat = htparam.flogical

        for artikel in db_session.query(Artikel).filter(
                 (Artikel.departement == 0) & (Artikel.artart == 0) & (Artikel.umsatzart == 1)).order_by(Artikel.artnr).all():
            max_i = max_i + 1
            art_list[max_i - 1] = artikel.artnr
        do_it = True

        if do_it:
            for i in range(1,max_i + 1) :

                artikel = get_cache (Artikel, {"artnr": [(eq, art_list[i - 1])],"departement": [(eq, 0)]})

                if artikel:
                    cl_list = Cl_list()
                    cl_list_data.append(cl_list)

                    cl_list.segm = artikel.artnr

                    if i >= 10:
                        cl_list.bezeich = translateExtended ("Other RmRev", lvcarea, "")
                    else:
                        cl_list.bezeich = artikel.bezeich
                    for datum in date_range(from_date,to_date) :
                        serv =  to_decimal("0")
                        vat =  to_decimal("0")

                        for umsatz in db_session.query(Umsatz).filter(
                                 (Umsatz.artnr == artikel.artnr) & (Umsatz.departement == artikel.departement) & (Umsatz.datum == datum)).order_by(Umsatz._recid).all():
                            serv, vat = get_output(calc_servvat(umsatz.departement, umsatz.artnr, umsatz.datum, artikel.service_code, artikel.mwst_code))
                            fact =  to_decimal(1.00) + to_decimal(serv) + to_decimal(vat)

                            if datum == to_date:
                                drevrev =  to_decimal(drevrev) + to_decimal(umsatz.betrag) / to_decimal(fact)
                                cl_list.drev =  to_decimal(umsatz.betrag) / to_decimal(fact)

                            if (mi_mtd_chk and get_month(datum) == get_month(to_date)) or (mi_ftd_chk and datum >= fdate and datum <= tdate):
                                mrevrev =  to_decimal(mrevrev) + to_decimal(umsatz.betrag) / to_decimal(fact)
                                cl_list.mrev =  to_decimal(cl_list.mrev) + to_decimal(umsatz.betrag) / to_decimal(fact)
                            yrevrev =  to_decimal(yrevrev) + to_decimal(umsatz.betrag) / to_decimal(fact)


                            cl_list.yrev =  to_decimal(cl_list.yrev) + to_decimal(umsatz.betrag) / to_decimal(fact)

                    if cl_list.mrev == 0:
                        cl_list.bezeich = "Deleted"
            cl_list = Cl_list()
            cl_list_data.append(cl_list)

        drev_droom =  to_decimal(drevrev) / to_decimal((droomrev) + to_decimal(droomhu) + to_decimal(droomcomp))

        if drev_droom == None:
            drev_droom =  to_decimal("0")
        mrev_mroom =  to_decimal(mrevrev) / to_decimal((mroomrev) + to_decimal(mroomhu) + to_decimal(mroomcomp))

        if mrev_mroom == None:
            mrev_mroom =  to_decimal("0")
        yrev_yroom =  to_decimal(yrevrev) / to_decimal((yroomrev) + to_decimal(yroomhu) + to_decimal(yroomcomp))

        if yrev_yroom == None:
            yrev_yroom =  to_decimal("0")

        if not mi_exchu_chk:
            droomrev = droomrev + droomhu
            mroomrev = mroomrev + mroomhu
            yroomrev = yroomrev + yroomhu

        if not mi_exccomp_chk:
            droomrev = droomrev + droomcomp
            mroomrev = mroomrev + mroomcomp
            yroomrev = yroomrev + yroomcomp


        drev_droom1 =  to_decimal(drevrev) / to_decimal(droomrev)

        if drev_droom1 == None:
            drev_droom1 =  to_decimal("0")
        mrev_mroom1 =  to_decimal(mrevrev) / to_decimal(mroomrev)

        if mrev_mroom1 == None:
            mrev_mroom1 =  to_decimal("0")
        yrev_yroom1 =  to_decimal(yrevrev) / to_decimal(yroomrev)

        if yrev_yroom1 == None:
            yrev_yroom1 =  to_decimal("0")

        if mi_exchu_chk and mi_exccomp_chk:
            state_str = translateExtended ("RmRev Exc Comp&HU", lvcarea, "")

        elif mi_exchu_chk:
            state_str = translateExtended ("RmRev Exc HU", lvcarea, "")

        elif mi_exccomp_chk:
            state_str = translateExtended ("RmRev Exc Comp", lvcarea, "")
        else:
            state_str = ""

        if not long_digit:
            cl_list = Cl_list()
            cl_list_data.append(cl_list)

            cl_list.bezeich = "RmRev Inc All"
            cl_list.drate =  to_decimal(drev_droom)
            cl_list.mrate =  to_decimal(mrev_mroom)
            cl_list.drev =  to_decimal(drevrev)
            cl_list.mrev =  to_decimal(mrevrev)
            cl_list.yrev =  to_decimal(yrevrev)
            cl_list.yrate =  to_decimal(yrev_yroom)

            if mi_exchu_chk or mi_exccomp_chk:
                cl_list = Cl_list()
                cl_list_data.append(cl_list)

                cl_list.bezeich = state_str
                cl_list.drate =  to_decimal(drev_droom1)
                cl_list.mrate =  to_decimal(mrev_mroom1)
                cl_list.drev =  to_decimal(drevrev)
                cl_list.mrev =  to_decimal(mrevrev)
                cl_list.yrev =  to_decimal(yrevrev)
                cl_list.yrate =  to_decimal(yrev_yroom1)


        else:
            cl_list = Cl_list()
            cl_list_data.append(cl_list)

            cl_list.bezeich = "RmRev Inc All"
            cl_list.drate =  to_decimal(drev_droom)
            cl_list.mrate =  to_decimal(mrev_mroom)
            cl_list.drev =  to_decimal(drevrev)
            cl_list.mrev =  to_decimal(mrevrev)
            cl_list.yrev =  to_decimal(yrevrev)
            cl_list.yrate =  to_decimal(yrev_yroom)

            if mi_exchu_chk or mi_exccomp_chk:
                cl_list = Cl_list()
                cl_list_data.append(cl_list)

                cl_list.bezeich = state_str
                cl_list.drate =  to_decimal(drev_droom1)
                cl_list.mrate =  to_decimal(mrev_mroom1)
                cl_list.drev =  to_decimal(drevrev)
                cl_list.mrev =  to_decimal(mrevrev)
                cl_list.yrev =  to_decimal(yrevrev)
                cl_list.yrate =  to_decimal(yrev_yroom1)

    htparam = get_cache (Htparam, {"paramnr": [(eq, 186)]})
    opening_date = htparam.fdate

    if get_month(to_date) == get_month(opening_date) and get_year(to_date) == get_year(opening_date):
        from_date = opening_date

    htparam = get_cache (Htparam, {"paramnr": [(eq, 87)]})
    ci_date = htparam.fdate

    if from_date < ci_date:
        create_umsatz()
    else:
        create_umsatz1()

    for cl_list in query(cl_list_data, filters=(lambda cl_list: cl_list.bezeich.lower()  == ("Deleted").lower())):
        cl_list_data.remove(cl_list)

    return generate_output()