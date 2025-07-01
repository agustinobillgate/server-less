#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from functions.calc_servvat import calc_servvat
from models import Htparam, Zimmer, Zkstat, Zinrstat, Genstat, Segment, Guestseg, Artikel, Umsatz

def rm_drecap2bl(pvilanguage:int, opening_date:date, from_date:date, to_date:date, fdate:date, tdate:date, segmtype_exist:bool, mi_mtd_chk:bool, mi_ftd_chk:bool, mi_exchu_chk:bool, mi_exccomp_chk:bool, long_digit:bool):

    prepare_cache ([Htparam, Zkstat, Zinrstat, Genstat, Segment, Guestseg, Artikel, Umsatz])

    output_list_list = []
    lvcarea:string = "rm-drecap2"
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
    from_bez:string = ""
    to_bez:string = ""
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
    htparam = zimmer = zkstat = zinrstat = genstat = segment = guestseg = artikel = umsatz = None

    cl_list = output_list = None

    cl_list_list, Cl_list = create_model("Cl_list", {"flag":string, "segm":int, "betriebsnr":int, "compli":bool, "bezeich":string, "droom":int, "proz1":Decimal, "mroom":int, "proz2":Decimal, "dpax":int, "mpax":int, "drate":Decimal, "mrate":Decimal, "drev":Decimal, "mrev":Decimal, "yroom":int, "proz3":Decimal, "ypax":int, "yrate":Decimal, "yrev":Decimal})
    output_list_list, Output_list = create_model("Output_list", {"segno":int, "flag":string, "str":string, "yroom":string, "proz3":string, "ypax":string, "yrate":string, "yrev":string, "zero_flag":bool})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal output_list_list, lvcarea, do_it, droomrev, mroomrev, yroomrev, droomexc, mroomexc, yroomexc, tot_room, all_room, dvacant, dooo, mvacant, mooo, yvacant, yooo, dnoshow, dcancel, mnoshow, mcancel, ynoshow, ycancel, droom, proz1, mroom, proz2, dpax, mpax, drate, mrate, drev, mrev, yroom, ypax, yrate, yrev, from_bez, to_bez, inactive, mtd_act, mtd_totrm, ytd_act, ytd_totrm, ncompli, mtd_ncompli, ytd_ncompli, dcompli, mcompli, ycompli, dhu, mhu, yhu, htparam, zimmer, zkstat, zinrstat, genstat, segment, guestseg, artikel, umsatz
        nonlocal pvilanguage, opening_date, from_date, to_date, fdate, tdate, segmtype_exist, mi_mtd_chk, mi_ftd_chk, mi_exchu_chk, mi_exccomp_chk, long_digit


        nonlocal cl_list, output_list
        nonlocal cl_list_list, output_list_list

        return {"output-list": output_list_list}

    def create_umsatz():

        nonlocal output_list_list, lvcarea, do_it, droomrev, mroomrev, yroomrev, droomexc, mroomexc, yroomexc, tot_room, all_room, dvacant, dooo, mvacant, mooo, yvacant, yooo, dnoshow, dcancel, mnoshow, mcancel, ynoshow, ycancel, droom, proz1, mroom, proz2, dpax, mpax, drate, mrate, drev, mrev, yroom, ypax, yrate, yrev, from_bez, to_bez, inactive, mtd_act, mtd_totrm, ytd_act, ytd_totrm, ncompli, mtd_ncompli, ytd_ncompli, dcompli, mcompli, ycompli, dhu, mhu, yhu, htparam, zimmer, zkstat, zinrstat, genstat, segment, guestseg, artikel, umsatz
        nonlocal pvilanguage, opening_date, from_date, to_date, fdate, tdate, segmtype_exist, mi_mtd_chk, mi_ftd_chk, mi_exchu_chk, mi_exccomp_chk, long_digit


        nonlocal cl_list, output_list
        nonlocal cl_list_list, output_list_list

        i:int = 0
        datum:date = None
        black_list:int = 0

        htparam = get_cache (Htparam, {"paramnr": [(eq, 709)]})
        black_list = htparam.finteger
        output_list_list.clear()
        cl_list_list.clear()
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

        for zkstat in db_session.query(Zkstat).filter(
                 (Zkstat.datum == to_date)).order_by(Zkstat._recid).all():
            tot_room = tot_room + zkstat.anz100
        create_lbl()
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


    def create_lbl():

        nonlocal output_list_list, lvcarea, do_it, droomrev, mroomrev, yroomrev, droomexc, mroomexc, yroomexc, tot_room, all_room, dvacant, dooo, mvacant, mooo, yvacant, yooo, dnoshow, dcancel, mnoshow, mcancel, ynoshow, ycancel, droom, proz1, mroom, proz2, dpax, mpax, drate, mrate, drev, mrev, yroom, ypax, yrate, yrev, from_bez, to_bez, inactive, mtd_act, mtd_totrm, ytd_act, ytd_totrm, ncompli, mtd_ncompli, ytd_ncompli, dcompli, mcompli, ycompli, dhu, mhu, yhu, htparam, zimmer, zkstat, zinrstat, genstat, segment, guestseg, artikel, umsatz
        nonlocal pvilanguage, opening_date, from_date, to_date, fdate, tdate, segmtype_exist, mi_mtd_chk, mi_ftd_chk, mi_exchu_chk, mi_exccomp_chk, long_digit


        nonlocal cl_list, output_list
        nonlocal cl_list_list, output_list_list

        n:int = 0
        output_list = Output_list()
        output_list_list.append(output_list)

        output_list.flag = "header"
        output_list.str = fill("=", 165)
        output_list.yroom = fill("=", 10)
        output_list.proz3 = fill("=", 6)
        output_list.ypax = fill("=", 10)
        output_list.yrate = fill("=", 13)
        output_list.yrev = fill("=", 19)


        output_list = Output_list()
        output_list_list.append(output_list)

        output_list.flag = "header"

        if mi_mtd_chk:
            output_list.str = translateExtended ("SNoGuest Segment #Rm (%) MTD (%) Pax MTD Avrg-Rate MTD-AvrgRate Room-Revenue MTD-RmRevenue", lvcarea, "")
        else:
            output_list.str = translateExtended ("SNoGuest Segment #Rm (%) FTD (%) Pax FTD Avrg-Rate FTD-AvrgRate Room-Revenue FTD-RmRevenue", lvcarea, "")
        output_list.yroom = translateExtended (" YTD", lvcarea, "")
        output_list.proz3 = translateExtended (" (%)", lvcarea, "")
        output_list.ypax = translateExtended (" YTDPax", lvcarea, "")
        output_list.yrate = translateExtended (" YTD-AvrgRate", lvcarea, "")
        output_list.yrev = translateExtended (" YTDRoomRevenue", lvcarea, "")


        output_list = Output_list()
        output_list_list.append(output_list)

        output_list.flag = "header"
        output_list.str = fill("=", 165)
        output_list.str = fill("=", 165)
        output_list.yroom = fill("=", 10)
        output_list.proz3 = fill("=", 6)
        output_list.ypax = fill("=", 10)
        output_list.yrate = fill("=", 13)
        output_list.yrev = fill("=", 19)


    def count_mtd_totrm():

        nonlocal output_list_list, lvcarea, do_it, droomrev, mroomrev, yroomrev, droomexc, mroomexc, yroomexc, tot_room, all_room, dvacant, dooo, mvacant, mooo, yvacant, yooo, dnoshow, dcancel, mnoshow, mcancel, ynoshow, ycancel, droom, proz1, mroom, proz2, dpax, mpax, drate, mrate, drev, mrev, yroom, ypax, yrate, yrev, from_bez, to_bez, inactive, mtd_act, mtd_totrm, ytd_act, ytd_totrm, ncompli, mtd_ncompli, ytd_ncompli, dcompli, mcompli, ycompli, dhu, mhu, yhu, htparam, zimmer, zkstat, zinrstat, genstat, segment, guestseg, artikel, umsatz
        nonlocal pvilanguage, opening_date, from_date, to_date, fdate, tdate, segmtype_exist, mi_mtd_chk, mi_ftd_chk, mi_exchu_chk, mi_exccomp_chk, long_digit


        nonlocal cl_list, output_list
        nonlocal cl_list_list, output_list_list

        datum:date = None
        tot1:int = 0
        glob_tot:int = 0
        mtd_totrm = 0 mtd_act == 0 ytd_act == 0 ytd_totrm == 0

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

        nonlocal output_list_list, lvcarea, do_it, droomrev, mroomrev, yroomrev, droomexc, mroomexc, yroomexc, tot_room, all_room, dvacant, dooo, mvacant, mooo, yvacant, yooo, dnoshow, dcancel, mnoshow, mcancel, ynoshow, ycancel, droom, proz1, mroom, proz2, dpax, mpax, drate, mrate, drev, mrev, yroom, ypax, yrate, yrev, from_bez, to_bez, inactive, mtd_act, mtd_totrm, ytd_act, ytd_totrm, ncompli, mtd_ncompli, ytd_ncompli, dcompli, mcompli, ycompli, dhu, mhu, yhu, htparam, zimmer, zkstat, zinrstat, genstat, segment, guestseg, artikel, umsatz
        nonlocal pvilanguage, opening_date, from_date, to_date, fdate, tdate, segmtype_exist, mi_mtd_chk, mi_ftd_chk, mi_exchu_chk, mi_exccomp_chk, long_digit


        nonlocal cl_list, output_list
        nonlocal cl_list_list, output_list_list

        i:int = 0
        datum:date = None
        do_it1:bool = False
        bgenstat = None
        Bgenstat =  create_buffer("Bgenstat",Genstat)

        for segment in db_session.query(Segment).filter(
                 (((Segment.segmentcode >= i1) & (Segment.segmentcode <= i2)) | ((Segment.segmentcode >= i3) & (Segment.segmentcode <= i4)))).order_by(Segment.segmentcode).all():

            bgenstat = db_session.query(Bgenstat).filter(
                     (Bgenstat.segmentcode == segment.segmentcode) & (Bgenstat.datum >= from_date) & (Bgenstat.datum <= to_date) & (Bgenstat.resstatus != 13) & (Bgenstat.gratis == 0) & (Bgenstat.segmentcode != 0) & (Bgenstat.nationnr != 0) & (Bgenstat.zinr != "") & (Bgenstat.res_logic[inc_value(1)])).first()

            if bgenstat:
                do_it1 = True


            else:

                if matches(segment.bezeich,r"*$$0"):
                    do_it1 = False


                else:
                    do_it1 = True

            if do_it1:
                cl_list = Cl_list()
                cl_list_list.append(cl_list)

                cl_list.segm = segment.segmentcode
                cl_list.bezeich = entry(0, segment.bezeich, "$$0")

                for genstat in db_session.query(Genstat).filter(
                         (Genstat.segmentcode == segment.segmentcode) & (Genstat.datum >= from_date) & (Genstat.datum <= to_date) & (Genstat.resstatus != 13) & (Genstat.gratis == 0) & (Genstat.segmentcode != 0) & (Genstat.nationnr != 0) & (Genstat.zinr != "") & (Genstat.res_logic[inc_value(1)])).order_by(Genstat._recid).all():

                    if genstat.res_date[0] < genstat.datum and genstat.res_date[1] == genstat.datum and genstat.resstatus == 8:
                        pass
                    else:

                        if genstat.datum == to_date:
                            droom = droom + 1
                            cl_list.droom = cl_list.droom + 1
                            cl_list.dpax = cl_list.dpax + genstat.erwachs + genstat.kind1 + genstat.kind2 + genstat.gratis
                            cl_list.drev =  to_decimal(cl_list.drev) + to_decimal(genstat.logis)
                            drev =  to_decimal(drev) + to_decimal(genstat.logis)

                        if (mi_mtd_chk and get_month(genstat.datum) == get_month(to_date)) or (mi_ftd_chk and genstat.datum >= fdate and genstat.datum <= tdate):
                            cl_list.mroom = cl_list.mroom + 1
                            cl_list.mpax = cl_list.mpax + genstat.erwachs + genstat.kind1 + genstat.kind2 + genstat.gratis
                            cl_list.mrev =  to_decimal(cl_list.mrev) + to_decimal(genstat.logis)
                            mroom = mroom + 1
                            mpax = mpax + genstat.erwachs + genstat.kind1 + genstat.kind2 + genstat.gratis
                            mrev =  to_decimal(mrev) + to_decimal(genstat.logis)
                        cl_list.yroom = cl_list.yroom + 1
                        cl_list.ypax = cl_list.ypax + genstat.erwachs +\
                                genstat.kind1 + genstat.kind2 + genstat.gratis
                        cl_list.yrev =  to_decimal(cl_list.yrev) + to_decimal(genstat.logis)
                        yroom = yroom + 1
                        ypax = ypax + genstat.gratis
                        yrev =  to_decimal(yrev) + to_decimal(genstat.logis)

        if do_it:

            for genstat in db_session.query(Genstat).filter(
                     (Genstat.datum >= from_date) & (Genstat.datum <= to_date) & (Genstat.segmentcode != 0) & (Genstat.nationnr != 0) & (Genstat.zinr != "") & (Genstat.resstatus != 13) & (Genstat.res_logic[inc_value(1)])).order_by(Genstat._recid).all():

                segment = get_cache (Segment, {"segmentcode": [(eq, genstat.segmentcode)]})

                if segment:

                    cl_list = query(cl_list_list, filters=(lambda cl_list: cl_list.segm == segment.segmentcode), first=True)

                    if cl_list:

                        if genstat.datum == to_date:
                            cl_list.drev =  to_decimal(cl_list.drev) + to_decimal(genstat.res_deci[0])
                            drev =  to_decimal(drev) + to_decimal(genstat.logis)

                        if (mi_mtd_chk and get_month(genstat.datum) == get_month(to_date)) or (mi_ftd_chk and genstat.datum >= fdate and genstat.datum <= tdate):
                            cl_list.mrev =  to_decimal(cl_list.mrev) + to_decimal(genstat.res_deci[0])
                            mrev =  to_decimal(mrev) + to_decimal(genstat.logis)
                else:

                    guestseg = get_cache (Guestseg, {"gastnr": [(eq, genstat.gastnr)]})

                    if guestseg:

                        if guestseg.reihenfolge == 1:

                            cl_list = query(cl_list_list, filters=(lambda cl_list: cl_list.segm == segment.segmentcode), first=True)

                            if cl_list:

                                if genstat.datum == to_date:
                                    cl_list.drev =  to_decimal(cl_list.drev) + to_decimal(genstat.res_deci[0])
                                    drev =  to_decimal(drev) + to_decimal(genstat.logis)

                                if (mi_mtd_chk and get_month(genstat.datum) == get_month(to_date)) or (mi_ftd_chk and genstat.datum >= fdate and genstat.datum <= tdate):
                                    cl_list.mrev =  to_decimal(cl_list.mrev) + to_decimal(genstat.res_deci[0])
                                    mrev =  to_decimal(mrev) + to_decimal(genstat.logis)
                        else:

                            guestseg = get_cache (Guestseg, {"reihenfolge": [(eq, 0)]})

                            if guestseg:

                                cl_list = query(cl_list_list, filters=(lambda cl_list: cl_list.segm == guestseg.segmentcode), first=True)

                                if cl_list:

                                    if genstat.datum == to_date:
                                        cl_list.drev =  to_decimal(cl_list.drev) + to_decimal(genstat.res_deci[0])
                                        drev =  to_decimal(drev) + to_decimal(genstat.logis)

                                    if (mi_mtd_chk and get_month(genstat.datum) == get_month(to_date)) or (mi_ftd_chk and genstat.datum >= fdate and genstat.datum <= tdate):
                                        cl_list.mrev =  to_decimal(cl_list.mrev) + to_decimal(genstat.res_deci[0])
                                        mrev =  to_decimal(mrev) + to_decimal(genstat.logis)
                    else:

                        segment = db_session.query(Segment).first()

                        if segment:

                            cl_list = query(cl_list_list, filters=(lambda cl_list: cl_list.segm == segment.segmentcode), first=True)

                            if cl_list:

                                if genstat.datum == to_date:
                                    cl_list.drev =  to_decimal(cl_list.drev) + to_decimal(genstat.res_deci[0])
                                    drev =  to_decimal(drev) + to_decimal(genstat.logis)

                                if (mi_mtd_chk and get_month(genstat.datum) == get_month(to_date)) or (mi_ftd_chk and genstat.datum >= fdate and genstat.datum <= tdate):
                                    cl_list.mrev =  to_decimal(cl_list.mrev) + to_decimal(genstat.res_deci[0])
                                    mrev =  to_decimal(mrev) + to_decimal(genstat.logis)

        for cl_list in query(cl_list_list, filters=(lambda cl_list:((cl_list.segm >= i1 and cl_list.segm <= i2) or (cl_list.segm >= i3 and cl_list.segm <= i4)))):

            if cl_list.droom != 0:
                cl_list.drate =  to_decimal(cl_list.drev) / to_decimal(cl_list.droom)

            if cl_list.mroom != 0:
                cl_list.mrate =  to_decimal(cl_list.mrev) / to_decimal(cl_list.mroom)
            cl_list.proz1 =  to_decimal(100.0) * to_decimal(cl_list.droom) / to_decimal(tot_room)
            cl_list.proz2 =  to_decimal(100.0) * to_decimal(cl_list.mroom) / to_decimal(mtd_act)
            cl_list.proz3 =  to_decimal(100.0) * to_decimal(cl_list.yroom) / to_decimal(ytd_act)

            if droom != 0:
                drate =  to_decimal(drev) / to_decimal(droom)

            if mroom != 0:
                mrate =  to_decimal(mrev) / to_decimal(mroom)

            if yroom != 0:
                yrate =  to_decimal(yrev) / to_decimal(yroom)

            if cl_list.proz1 == None:
                cl_list.proz1 =  to_decimal("0")

            if cl_list.proz2 == None:
                cl_list.proz2 =  to_decimal("0")

            if cl_list.proz3 == None:
                cl_list.proz3 =  to_decimal("0")
            dpax = dpax + cl_list.dpax
            output_list = Output_list()
            output_list_list.append(output_list)

            output_list.segno = cl_list.segm
            output_list.str = to_string(cl_list.segm, ">>>") +\
                    to_string(cl_list.bezeich, "x(16)") +\
                    to_string(cl_list.droom, "->9") +\
                    to_string(cl_list.proz1, "->>9.99") +\
                    to_string(cl_list.mroom, "->>>>9 ") +\
                    to_string(cl_list.proz2, "->>9.99") +\
                    to_string(cl_list.dpax, "->9") +\
                    to_string(cl_list.mpax, "->,>>9") +\
                    to_string(cl_list.drate, "->,>>>,>>9.99") +\
                    to_string(cl_list.mrate, "->,>>>,>>9.99") +\
                    to_string(cl_list.drev, "->>,>>>,>>9.99") +\
                    to_string(cl_list.mrev, ">>>,>>>,>>>,>>9.99")
            output_list.yroom = to_string(cl_list.yroom, "->,>>>,>>9")
            output_list.ypax = to_string(cl_list.ypax, "->,>>>,>>9")
            output_list.proz3 = to_string(cl_list.proz3, "->>9.99")
            output_list.yrev = to_string(cl_list.yrev, "->>>,>>>,>>>,>>9.99")


            output_list.yrate = to_string(cl_list.yrate, "->,>>>,>>9.99")

            if cl_list.drev == 0 and cl_list.mrev == 0 and cl_list.yrev == 0:
                output_list.zero_flag = True
        output_list = Output_list()
        output_list_list.append(output_list)

        output_list.str = " "
        output_list.yroom = fill("-", 10)
        output_list.proz3 = fill("-", 6)
        output_list.ypax = fill("-", 10)
        output_list.yrate = fill("-", 13)
        output_list.yrev = fill("-", 19)


        for i in range(1,96 + 1) :
            output_list.str = output_list.str + "----"
        output_list = Output_list()
        output_list_list.append(output_list)

        output_list.str = " " + to_string(rev_title, "x(16)") +\
                to_string(droom, "->9") +\
                to_string(droom / tot_room * 100, "->>9.99") +\
                to_string(mroom, "->>>>9") +\
                to_string(mroom / mtd_act * 100, "->>9.99") +\
                to_string(dpax, "->9") +\
                to_string(mpax, "->,>>9")
        output_list.yroom = to_string(yroom, "->,>>>,>>9")
        output_list.ypax = to_string(ypax, "->,>>>,>>9")
        output_list.proz3 = to_string(ytd_act * 100 , "->,>>9")

        if show_avrg:

            if droom != 0:
                output_list.str = output_list.str + to_string(drev / droom, "->,>>>,>>9.99")
            else:
                output_list.str = output_list.str + to_string(0, ">,>>>,>>9.99")

            if mroom != 0:
                output_list.str = output_list.str + to_string(mrev / mroom, "->,>>>,>>9.99")
            else:
                output_list.str = output_list.str + to_string(0, ">,>>>,>>9.99")

            if yroom != 0:
                output_list.yrate = to_string(yrev / yroom, "->,>>>,>>9.99")
            else:
                output_list.yrate = to_string(0, "->,>>>,>>9.99")
        else:
            output_list.str = output_list.str + to_string(0, ">>>>>>>>>>>>>") + to_string(0, ">>>>>>>>>>>>>")
        output_list.str = output_list.str +\
                to_string(drev, ">>>,>>>,>>9.99") +\
                to_string(mrev, ">>>,>>>,>>>,>>9.99")
        output_list.yrev = to_string(yrev, "->>>,>>>,>>>,>>9.99")

        if rev_title1 != "":
            output_list = Output_list()
            output_list_list.append(output_list)

            output_list.str = " " + to_string(rev_title1, "x(16)") + to_string(0, ">>>")

            if droom != 0:
                output_list.str = output_list.str + to_string((dpax - droom) / droom * 100, "->>9.99") + to_string(0, ">,>>>")
            else:
                output_list.str = output_list.str + to_string(0, "->>9.99") + to_string(0, ">,>>>")

            if mroom != 0:
                output_list.str = output_list.str + to_string((mpax - mroom) / mroom * 100, "->>9.99")
            else:
                output_list.str = output_list.str + to_string(0, "->>9.99")
            output_list.str = output_list.str + to_string(0, ">>>") + to_string(0, ">>,>>>")

            if yroom != 0:
                output_list.proz3 = to_string((ypax - yroom) / yroom * 100, "->>9.99")
            else:
                output_list.proz3 = to_string(0, "->>9.99")
        output_list = Output_list()
        output_list_list.append(output_list)

        output_list.str = " "
        output_list.yroom = fill("-", 10)
        output_list.proz3 = fill("-", 6)
        output_list.ypax = fill("-", 10)
        output_list.yrate = fill("-", 13)
        output_list.yrev = fill("-", 19)


        for i in range(1,96 + 1) :
            output_list.str = output_list.str + "----"


    def cal_umsatz1a(i1:int, i2:int, rev_title:string, rev_title1:string, show_avrg:bool):

        nonlocal output_list_list, lvcarea, do_it, droomrev, mroomrev, yroomrev, droomexc, mroomexc, yroomexc, tot_room, all_room, dvacant, dooo, mvacant, mooo, yvacant, yooo, dnoshow, dcancel, mnoshow, mcancel, ynoshow, ycancel, droom, proz1, mroom, proz2, dpax, mpax, drate, mrate, drev, mrev, yroom, ypax, yrate, yrev, from_bez, to_bez, inactive, mtd_act, mtd_totrm, ytd_act, ytd_totrm, ncompli, mtd_ncompli, ytd_ncompli, dcompli, mcompli, ycompli, dhu, mhu, yhu, htparam, zimmer, zkstat, zinrstat, genstat, segment, guestseg, artikel, umsatz
        nonlocal pvilanguage, opening_date, from_date, to_date, fdate, tdate, segmtype_exist, mi_mtd_chk, mi_ftd_chk, mi_exchu_chk, mi_exccomp_chk, long_digit


        nonlocal cl_list, output_list
        nonlocal cl_list_list, output_list_list

        i:int = 0
        tot_proz3:Decimal = to_decimal("0.0")
        inact:bool = False
        do_it1:bool = False
        bgenstat = None
        Bgenstat =  create_buffer("Bgenstat",Genstat)

        for segment in db_session.query(Segment).filter(
                 (Segment.betriebsnr == 0)).order_by(Segment.segmentcode).all():

            bgenstat = db_session.query(Bgenstat).filter(
                     (Bgenstat.segmentcode == segment.segmentcode) & (Bgenstat.datum >= from_date) & (Bgenstat.datum <= to_date) & (Bgenstat.resstatus != 13) & (Bgenstat.gratis == 0) & (Bgenstat.segmentcode != 0) & (Bgenstat.nationnr != 0) & (Bgenstat.zinr != "") & (Bgenstat.res_logic[inc_value(1)])).first()

            if bgenstat:
                do_it1 = True


            else:

                if matches(segment.bezeich,r"*$$0"):
                    do_it1 = False


                else:
                    do_it1 = True

            if do_it1:
                cl_list = Cl_list()
                cl_list_list.append(cl_list)

                cl_list.segm = segment.segmentcode
                cl_list.bezeich = entry(0, segment.bezeich, "$$0")
                cl_list.betriebsnr = segment.betriebsnr
                cl_list.drev =  to_decimal("0")

                for genstat in db_session.query(Genstat).filter(
                         (Genstat.segmentcode == segment.segmentcode) & (Genstat.datum >= from_date) & (Genstat.datum <= to_date) & (Genstat.resstatus != 13) & (Genstat.gratis == 0) & (Genstat.segmentcode != 0) & (Genstat.nationnr != 0) & (Genstat.zinr != "") & (Genstat.res_logic[inc_value(1)])).order_by(Genstat._recid).all():
                    inact = True

                    if genstat.res_date[0] < genstat.datum and genstat.res_date[1] == genstat.datum and genstat.resstatus == 8:
                        pass
                    else:

                        if genstat.datum == to_date:
                            droom = droom + 1
                            cl_list.droom = cl_list.droom + 1
                            cl_list.dpax = cl_list.dpax + genstat.erwachs + genstat.kind1 + genstat.kind2
                            cl_list.drev =  to_decimal(cl_list.drev) + to_decimal(genstat.logis)
                            drev =  to_decimal(drev) + to_decimal(genstat.logis)

                        if (mi_mtd_chk and get_month(genstat.datum) == get_month(to_date)) or (mi_ftd_chk and genstat.datum >= fdate and genstat.datum <= tdate):
                            cl_list.mroom = cl_list.mroom + 1
                            cl_list.mpax = cl_list.mpax + genstat.erwachs + genstat.kind1 + genstat.kind2
                            cl_list.mrev =  to_decimal(cl_list.mrev) + to_decimal(genstat.logis)
                            mroom = mroom + 1
                            mpax = mpax + genstat.erwachs + genstat.kind1 + genstat.kind2
                            mrev =  to_decimal(mrev) + to_decimal(genstat.logis)
                        cl_list.yroom = cl_list.yroom + 1


                        cl_list.ypax = cl_list.ypax + genstat.erwachs + genstat.kind1 + genstat.kind2
                        cl_list.yrev =  to_decimal(cl_list.yrev) + to_decimal(genstat.logis)
                        yroom = yroom + 1
                        ypax = ypax + genstat.erwachs + genstat.kind1 + genstat.kind2
                        yrev =  to_decimal(yrev) + to_decimal(genstat.logis)

        if do_it:

            for genstat in db_session.query(Genstat).filter(
                     (Genstat.datum >= from_date) & (Genstat.datum <= to_date) & (Genstat.segmentcode != 0) & (Genstat.nationnr != 0) & (Genstat.zinr != "") & (Genstat.resstatus != 13) & (Genstat.res_logic[inc_value(1)])).order_by(Genstat._recid).all():

                segment = get_cache (Segment, {"segmentcode": [(eq, genstat.segmentcode)]})

                if segment:

                    cl_list = query(cl_list_list, filters=(lambda cl_list: cl_list.segm == segment.segmentcode), first=True)

                    if cl_list:

                        if genstat.datum == to_date:
                            cl_list.drev =  to_decimal(cl_list.drev) + to_decimal(genstat.res_deci[0])
                            drev =  to_decimal(drev) + to_decimal(genstat.res_deci[0])

                        if (mi_mtd_chk and get_month(genstat.datum) == get_month(to_date)) or (mi_ftd_chk and genstat.datum >= fdate and genstat.datum <= tdate):
                            cl_list.mrev =  to_decimal(cl_list.mrev) + to_decimal(genstat.res_deci[0])
                            mrev =  to_decimal(mrev) + to_decimal(genstat.res_deci[0])


                else:

                    guestseg = get_cache (Guestseg, {"gastnr": [(eq, genstat.gastnr)]})

                    if guestseg:

                        if guestseg.reihenfolge == 1:

                            cl_list = query(cl_list_list, filters=(lambda cl_list: cl_list.segm == segment.segmentcode), first=True)

                            if cl_list:

                                if genstat.datum == to_date:
                                    cl_list.drev =  to_decimal(cl_list.drev) + to_decimal(genstat.res_deci[0])
                                    drev =  to_decimal(drev) + to_decimal(genstat.res_deci[0])

                                if (mi_mtd_chk and get_month(genstat.datum) == get_month(to_date)) or (mi_ftd_chk and genstat.datum >= fdate and genstat.datum <= tdate):
                                    cl_list.mrev =  to_decimal(cl_list.mrev) + to_decimal(genstat.res_deci[0])
                                    mrev =  to_decimal(mrev) + to_decimal(genstat.res_deci[0])


                        else:

                            guestseg = get_cache (Guestseg, {"reihenfolge": [(eq, 0)]})

                            if guestseg:

                                cl_list = query(cl_list_list, filters=(lambda cl_list: cl_list.segm == guestseg.segmentcode), first=True)

                                if cl_list:

                                    if genstat.datum == to_date:
                                        cl_list.drev =  to_decimal(cl_list.drev) + to_decimal(genstat.res_deci[0])
                                        drev =  to_decimal(drev) + to_decimal(genstat.res_deci[0])

                                    if (mi_mtd_chk and get_month(genstat.datum) == get_month(to_date)) or (mi_ftd_chk and genstat.datum >= fdate and genstat.datum <= tdate):
                                        cl_list.mrev =  to_decimal(cl_list.mrev) + to_decimal(genstat.res_deci[0])
                                        mrev =  to_decimal(mrev) + to_decimal(genstat.res_deci[0])


                    else:

                        segment = db_session.query(Segment).first()

                        if segment:

                            cl_list = query(cl_list_list, filters=(lambda cl_list: cl_list.segm == segment.segmentcode), first=True)

                            if cl_list:

                                if genstat.datum == to_date:
                                    cl_list.drev =  to_decimal(cl_list.drev) + to_decimal(genstat.res_deci[0])
                                    drev =  to_decimal(drev) + to_decimal(genstat.res_deci[0])

                                if (mi_mtd_chk and get_month(genstat.datum) == get_month(to_date)) or (mi_ftd_chk and genstat.datum >= fdate and genstat.datum <= tdate):
                                    cl_list.mrev =  to_decimal(cl_list.mrev) + to_decimal(genstat.res_deci[0])
                                    mrev =  to_decimal(mrev) + to_decimal(genstat.res_deci[0])

        if inact:

            for cl_list in query(cl_list_list, filters=(lambda cl_list:(cl_list.betriebsnr >= i1 and cl_list.betriebsnr <= i2))):

                if cl_list.droom != 0:
                    cl_list.drate =  to_decimal(cl_list.drev) / to_decimal(cl_list.droom)

                if cl_list.mroom != 0:
                    cl_list.mrate =  to_decimal(cl_list.mrev) / to_decimal(cl_list.mroom)

                if cl_list.yroom != 0:
                    cl_list.yrate =  to_decimal(cl_list.yrev) / to_decimal(cl_list.yroom)
                cl_list.proz1 =  to_decimal(100.0) * to_decimal(cl_list.droom) / to_decimal(tot_room)
                cl_list.proz2 =  to_decimal(100.0) * to_decimal(cl_list.mroom) / to_decimal(mtd_act)
                cl_list.proz3 =  to_decimal(100.0) * to_decimal(cl_list.yroom) / to_decimal(ytd_act)

                if droom != 0:
                    drate =  to_decimal(drev) / to_decimal(droom)

                if mroom != 0:
                    mrate =  to_decimal(mrev) / to_decimal(mroom)

                if yroom != 0:
                    yrate =  to_decimal(yrev) / to_decimal(yroom)

                if cl_list.proz1 == None:
                    cl_list.proz1 =  to_decimal("0")

                if cl_list.proz2 == None:
                    cl_list.proz2 =  to_decimal("0")

                if cl_list.proz3 == None:
                    cl_list.proz3 =  to_decimal("0")
                tot_proz3 =  to_decimal(tot_proz3) + to_decimal(cl_list.proz3)


                dpax = dpax + cl_list.dpax
                output_list = Output_list()
                output_list_list.append(output_list)

                output_list.segno = cl_list.segm

                if not long_digit:
                    output_list.str = to_string(cl_list.segm, ">>>") +\
                            to_string(cl_list.bezeich, "x(16)") +\
                            to_string(cl_list.droom, "->9") +\
                            to_string(cl_list.proz1, "->>9.99") +\
                            to_string(cl_list.mroom, "->>>>9") +\
                            to_string(cl_list.proz2, "->>9.99") +\
                            to_string(cl_list.dpax, "->9") +\
                            to_string(cl_list.mpax, "->,>>9") +\
                            to_string(cl_list.drate, "->,>>>,>>9.99") +\
                            to_string(cl_list.mrate, "->,>>>,>>9.99") +\
                            to_string(cl_list.drev, "->>,>>>,>>9.99") +\
                            to_string(cl_list.mrev, ">>>,>>>,>>>,>>9.99")
                    output_list.yroom = to_string(cl_list.yroom, "->,>>>,>>9")
                    output_list.ypax = to_string(cl_list.ypax, "->,>>>,>>9")
                    output_list.yrate = to_string(cl_list.yrate, "->,>>>,>>9.99")
                    output_list.yrev = to_string(cl_list.yrev, "->>>,>>>,>>>,>>9.99")
                    output_list.proz3 = to_string(cl_list.proz3, "->>9.99")


                else:
                    output_list.str = to_string(cl_list.segm, ">>>") +\
                            to_string(cl_list.bezeich, "x(16)") +\
                            to_string(cl_list.droom, "->9") +\
                            to_string(cl_list.proz1, "->>9.99") +\
                            to_string(cl_list.mroom, "->>>>9") +\
                            to_string(cl_list.proz2, "->>9.99") +\
                            to_string(cl_list.dpax, "->9") +\
                            to_string(cl_list.mpax, "->,>>9") +\
                            to_string(cl_list.drate, "->>>,>>>,>>9") +\
                            to_string(cl_list.mrate, "->>>,>>>,>>9") +\
                            to_string(cl_list.drev, "->,>>>,>>>,>>9") +\
                            to_string(cl_list.mrev, "->>>,>>>,>>>,>>9")
                    output_list.yroom = to_string(cl_list.yroom, "->,>>>,>>9")
                    output_list.ypax = to_string(cl_list.ypax, "->>>>9")
                    output_list.yrate = to_string(cl_list.yrate, "->>>,>>>,>>9")
                    output_list.yrev = to_string(cl_list.yrev, "->>>>,>>>,>>>,>>9")
                    output_list.proz3 = to_string(cl_list.proz3, "->>9.99")

                if cl_list.drev == 0 and cl_list.mrev == 0 and cl_list.yrev == 0:
                    output_list.zero_flag = True
            output_list = Output_list()
            output_list_list.append(output_list)

            output_list.str = " "
            output_list.yroom = fill("-", 10)
            output_list.proz3 = fill("-", 6)
            output_list.ypax = fill("-", 10)
            output_list.yrate = fill("-", 13)
            output_list.yrev = fill("-", 19)


            for i in range(1,96 + 1) :
                output_list.str = output_list.str + "----"
        droomexc = droom
        mroomexc = mroom
        yroomexc = yroom
        droomrev = droomexc
        mroomrev = mroomexc
        yroomrev = yroomexc


        output_list = Output_list()
        output_list_list.append(output_list)

        output_list.str = " " + to_string(rev_title, "x(16)") +\
                to_string(droom, "->9") +\
                to_string(droom / tot_room * 100, "->>9.99") +\
                to_string(mroom, "->>>>9") +\
                to_string(mroom / mtd_act * 100, "->>9.99") +\
                to_string(dpax, "->9") +\
                to_string(mpax, "->,>>9")


        output_list.yroom = to_string(yroom, "->,>>>,>>9")
        output_list.ypax = to_string(ypax, "->,>>>,>>9")
        output_list.proz3 = to_string(tot_proz3, "->>9.99")

        if show_avrg:

            if not long_digit:

                if droom != 0:
                    output_list.str = output_list.str + to_string(drev / droom, "->,>>>,>>9.99")
                else:
                    output_list.str = output_list.str + to_string(0, "->,>>>,>>9.99")

                if mroom != 0:
                    output_list.str = output_list.str + to_string(mrev / mroom, "->,>>>,>>9.99")
                else:
                    output_list.str = output_list.str + to_string(0, "->,>>>,>>9.99")

                if yroom != 0:
                    output_list.yrate = to_string(yrev / yroom, "->,>>>,>>9.99")
                else:
                    output_list.yrate = to_string(0, "->,>>>,>>9.99")
            else:

                if droom != 0:
                    output_list.str = output_list.str + to_string(drev / droom, "->>>,>>>,>>9")
                else:
                    output_list.str = output_list.str + to_string(0, "->>>,>>>,>>9")

                if mroom != 0:
                    output_list.str = output_list.str + to_string(mrev / mroom, "->>>,>>>,>>9")
                else:
                    output_list.str = output_list.str + to_string(0, "->>>,>>>,>>9")

                if yroom != 0:
                    output_list.yrate = to_string(yrev / yroom, "->>>,>>>,>>9")
                else:
                    output_list.yrate = to_string(0, "->,>>>,>>>,>>9")
        else:
            output_list.str = output_list.str + to_string(0, ">>>>>>>>>>>>>") + to_string(0, ">>>>>>>>>>>>>")

        if not long_digit:
            output_list.str = output_list.str +\
                    to_string(drev, ">>>,>>>,>>9.99") +\
                    to_string(mrev, ">>>,>>>,>>>,>>9.99")
            output_list.yrev = to_string(yrev, "->>>,>>>,>>>,>>9.99")


        else:
            output_list.str = output_list.str +\
                    to_string(drev, ">>,>>>,>>>,>>9") +\
                    to_string(mrev, ">>>>,>>>,>>>,>>9")
            output_list.yrev = to_string(yrev, "->>>,>>>,>>>,>>9.99")

        if rev_title1 != "":
            output_list = Output_list()
            output_list_list.append(output_list)

            output_list.str = " " + to_string(rev_title1, "x(16)") + to_string(0, ">>>")

            if droom != 0:
                output_list.str = output_list.str + to_string((dpax - droom) / droom * 100, "->>9.99") + to_string(0, ">,>>>")
            else:
                output_list.str = output_list.str + to_string(0, "->>9.99") + to_string(0, ">,>>>")

            if mroom != 0:
                output_list.str = output_list.str + to_string((mpax - mroom) / mroom * 100, "->>9.99")
            else:
                output_list.str = output_list.str + to_string(0, "->>9.99")
            output_list.str = output_list.str + to_string(0, ">>>") + to_string(0, ">>,>>>")

            if yroom != 0:
                output_list.proz3 = to_string((ypax - yroom) / yroom * 100, "->>9.99")
            else:
                output_list.proz3 = to_string(0, "->>9.99")
        output_list = Output_list()
        output_list_list.append(output_list)

        output_list.str = " "
        output_list.yroom = fill("-", 10)
        output_list.proz3 = fill("-", 6)
        output_list.ypax = fill("-", 10)
        output_list.yrate = fill("-", 13)
        output_list.yrev = fill("-", 19)


        for i in range(1,96 + 1) :
            output_list.str = output_list.str + "----"


    def cal_umsatz1b(i1:int, i2:int, rev_title:string, rev_title1:string, show_avrg:bool):

        nonlocal output_list_list, lvcarea, do_it, droomrev, mroomrev, yroomrev, droomexc, mroomexc, yroomexc, tot_room, all_room, dvacant, dooo, mvacant, mooo, yvacant, yooo, dnoshow, dcancel, mnoshow, mcancel, ynoshow, ycancel, droom, proz1, mroom, proz2, dpax, mpax, drate, mrate, drev, mrev, yroom, ypax, yrate, yrev, from_bez, to_bez, inactive, mtd_act, mtd_totrm, ytd_act, ytd_totrm, ncompli, mtd_ncompli, ytd_ncompli, dcompli, mcompli, ycompli, dhu, mhu, yhu, htparam, zimmer, zkstat, zinrstat, genstat, segment, guestseg, artikel, umsatz
        nonlocal pvilanguage, opening_date, from_date, to_date, fdate, tdate, segmtype_exist, mi_mtd_chk, mi_ftd_chk, mi_exchu_chk, mi_exccomp_chk, long_digit


        nonlocal cl_list, output_list
        nonlocal cl_list_list, output_list_list

        i:int = 0
        datum:date = None
        inact:bool = False
        do_it1:bool = False
        bgenstat = None
        Bgenstat =  create_buffer("Bgenstat",Genstat)

        for segment in db_session.query(Segment).order_by(Segment.segmentcode).all():

            bgenstat = db_session.query(Bgenstat).filter(
                     (Bgenstat.segmentcode == segment.segmentcode) & (Bgenstat.datum >= from_date) & (Bgenstat.datum <= to_date) & (Bgenstat.resstatus != 13) & (Bgenstat.gratis != 0) & (Bgenstat.segmentcode != 0) & (Bgenstat.nationnr != 0) & (Bgenstat.zinr != "") & (Bgenstat.res_logic[inc_value(1)])).first()

            if bgenstat:
                do_it1 = True


            else:

                if matches(segment.bezeich,r"*$$0"):
                    do_it1 = False


                else:
                    do_it1 = True

            if do_it1:

                for genstat in db_session.query(Genstat).filter(
                         (Genstat.segmentcode == segment.segmentcode) & (Genstat.datum >= from_date) & (Genstat.datum <= to_date) & (Genstat.resstatus != 13) & (Genstat.gratis != 0) & (Genstat.segmentcode != 0) & (Genstat.nationnr != 0) & (Genstat.zinr != "") & (Genstat.res_logic[inc_value(1)])).order_by(Genstat._recid).all():
                    inact = True

                    cl_list = query(cl_list_list, filters=(lambda cl_list: cl_list.segm == segment.segmentcode and cl_list.compli), first=True)

                    if not cl_list:
                        cl_list = Cl_list()
                        cl_list_list.append(cl_list)

                        cl_list.compli = True
                        cl_list.segm = segment.segmentcode
                        cl_list.bezeich = entry(0, segment.bezeich, "$$0")
                        cl_list.betriebsnr = segment.betriebsnr

                    if genstat.res_date[0] < genstat.datum and genstat.res_date[1] == genstat.datum and genstat.resstatus == 8:
                        pass
                    else:

                        if genstat.datum == to_date:
                            droom = droom + 1
                            cl_list.droom = cl_list.droom + 1
                            cl_list.dpax = cl_list.dpax + genstat.erwachs + genstat.kind1 + genstat.kind2 + genstat.gratis

                        if (mi_mtd_chk and get_month(genstat.datum) == get_month(to_date)) or (mi_ftd_chk and genstat.datum >= fdate and genstat.datum <= tdate):
                            mroom = mroom + 1
                            cl_list.mroom = cl_list.mroom + 1
                            cl_list.mpax = cl_list.mpax + genstat.erwachs + genstat.kind1 + genstat.kind2 + genstat.gratis
                            mpax = mpax + genstat.erwachs + genstat.kind1 + genstat.kind2 + genstat.gratis
                        yroom = yroom + 1
                        cl_list.yroom = cl_list.yroom + 1
                        cl_list.ypax = cl_list.ypax + genstat.erwachs + genstat.kind1 + genstat.kind2 + genstat.gratis
                        ypax = ypax + genstat.erwachs + genstat.kind1 + genstat.kind2 + genstat.gratis

        if inact:

            for cl_list in query(cl_list_list, filters=(lambda cl_list: cl_list.compli)):

                if cl_list.droom != 0:
                    cl_list.drate =  to_decimal(cl_list.drev) / to_decimal(cl_list.droom)

                if cl_list.mroom != 0:
                    cl_list.mrate =  to_decimal(cl_list.mrev) / to_decimal(cl_list.mroom)

                if cl_list.yroom != 0:
                    cl_list.yrate =  to_decimal(cl_list.yrev) / to_decimal(cl_list.yroom)
                cl_list.proz1 =  to_decimal(100.0) * to_decimal(cl_list.droom) / to_decimal(tot_room)
                cl_list.proz2 =  to_decimal(100.0) * to_decimal(cl_list.mroom) / to_decimal(mtd_act)
                cl_list.proz3 =  to_decimal(100.0) * to_decimal(cl_list.yroom) / to_decimal(ytd_act)

                if droom != 0:
                    drate =  to_decimal(drev) / to_decimal(droom)

                if mroom != 0:
                    mrate =  to_decimal(mrev) / to_decimal(mroom)

                if yroom != 0:
                    yrate =  to_decimal(yrev) / to_decimal(yroom)

                if cl_list.proz1 == None:
                    cl_list.proz1 =  to_decimal("0")

                if cl_list.proz2 == None:
                    cl_list.proz2 =  to_decimal("0")

                if cl_list.proz3 == None:
                    cl_list.proz3 =  to_decimal("0")
                dpax = dpax + cl_list.dpax
                output_list = Output_list()
                output_list_list.append(output_list)

                output_list.segno = cl_list.segm

                if not long_digit:
                    output_list.str = to_string(cl_list.segm, ">>>") +\
                            to_string(cl_list.bezeich, "x(16)") +\
                            to_string(cl_list.droom, "->9") +\
                            to_string(cl_list.proz1, "->>9.99") +\
                            to_string(cl_list.mroom, "->>>>9") +\
                            to_string(cl_list.proz2, "->>9.99") +\
                            to_string(cl_list.dpax, "->9") +\
                            to_string(cl_list.mpax, "->,>>9") +\
                            to_string(cl_list.drate, "->,>>>,>>9.99") +\
                            to_string(cl_list.mrate, "->,>>>,>>9.99") +\
                            to_string(cl_list.drev, "->>,>>>,>>9.99") +\
                            to_string(cl_list.mrev, ">>>,>>>,>>>,>>9.99")
                    output_list.yroom = to_string(cl_list.yroom, "->,>>>,>>9")
                    output_list.ypax = to_string(cl_list.ypax, "->,>>>,>>9")
                    output_list.yrate = to_string(cl_list.yrate, "->,>>>,>>9.99")
                    output_list.yrev = to_string(cl_list.yrev, "->>>,>>>,>>>,>>9.99")
                    output_list.proz3 = to_string(cl_list.proz3, "->>9.99")


                else:
                    output_list.str = to_string(cl_list.segm, ">>>") +\
                            to_string(cl_list.bezeich, "x(16)") +\
                            to_string(cl_list.droom, "->9") +\
                            to_string(cl_list.proz1, "->>9.99") +\
                            to_string(cl_list.mroom, "->>>>9") +\
                            to_string(cl_list.proz2, "->>9.99") +\
                            to_string(cl_list.dpax, "->9") +\
                            to_string(cl_list.mpax, "->,>>9") +\
                            to_string(cl_list.drate, "->>>,>>>,>>9") +\
                            to_string(cl_list.mrate, "->>>,>>>,>>9") +\
                            to_string(cl_list.drev, "->,>>>,>>>,>>9") +\
                            to_string(cl_list.mrev, "->>>,>>>,>>>,>>9")
                    output_list.yroom = to_string(cl_list.yroom, "->,>>>,>>9")
                    output_list.ypax = to_string(cl_list.ypax, "->,>>>,>>9")
                    output_list.yrate = to_string(cl_list.yrate, "->>>,>>>,>>9")
                    output_list.yrev = to_string(cl_list.yrev, " ->>>,>>>,>>>,>>9")
                    output_list.proz3 = to_string(cl_list.proz3, "->>9.99")


            output_list = Output_list()
            output_list_list.append(output_list)

            output_list.str = " "
            output_list.yroom = fill("-", 10)
            output_list.proz3 = fill("-", 6)
            output_list.ypax = fill("-", 10)
            output_list.yrate = fill("-", 13)
            output_list.yrev = fill("-", 19)


            for i in range(1,96 + 1) :
                output_list.str = output_list.str + "----"
        output_list = Output_list()
        output_list_list.append(output_list)

        output_list.str = " " + to_string(rev_title, "x(16)") +\
                to_string(droom, "->9") +\
                to_string(droom / tot_room * 100, "->>9.99") +\
                to_string(mroom, "->>>>9") +\
                to_string(mroom / mtd_act * 100, "->>9.99") +\
                to_string(dpax, "->9") +\
                to_string(mpax, "->,>>9")
        output_list.yroom = to_string(yroom, "->,>>>,>>9")
        output_list.ypax = to_string(ypax, "->,>>>,>>9")
        output_list.proz3 = to_string(yroom / ytd_act * 100, "->>9.99")

        if show_avrg:

            if not long_digit:

                if droom != 0:
                    output_list.str = output_list.str + to_string(drev / droom, "->,>>>,>>9.99")
                else:
                    output_list.str = output_list.str + to_string(0, "->,>>>,>>9.99")

                if mroom != 0:
                    output_list.str = output_list.str + to_string(mrev / mroom, "->,>>>,>>9.99")
                else:
                    output_list.str = output_list.str + to_string(0, "->,>>>,>>9.99")

                if yroom != 0:
                    output_list.yrate = to_string(yrev / yroom, "->,>>>,>>9.99")
                else:
                    output_list.yrate = to_string(0, "->,>>>,>>9.99")
            else:

                if droom != 0:
                    output_list.str = output_list.str + to_string(drev / droom, "->>>,>>>,>>9")
                else:
                    output_list.str = output_list.str + to_string(0, "->>>,>>>,>>9")

                if mroom != 0:
                    output_list.str = output_list.str + to_string(mrev / mroom, "->>>,>>>,>>9")
                else:
                    output_list.str = output_list.str + to_string(0, "->>>,>>>,>>9")

                if yroom != 0:
                    output_list.yrate = to_string(yrev / yroom, "->>>,>>>,>>9")
                else:
                    output_list.yrate = to_string(0, "->,>>>,>>>,>>9")
        else:
            output_list.str = output_list.str + to_string(" ", "x(13)") + to_string(" ", "x(13)")

        if not long_digit:
            output_list.str = output_list.str +\
                    to_string(drev, "->>,>>>,>>9.99") +\
                    to_string(mrev, ">>>,>>>,>>>,>>9.99")
            output_list.yrev = to_string(yrev, "->>>,>>>,>>>,>>9.99")


        else:
            output_list.str = output_list.str +\
                    to_string(drev, "->>>,>>>,>>9") +\
                    to_string(mrev, "->>>,>>>,>>>,>>9")
            output_list.yrev = to_string(yrev, "->>>>,>>>,>>>,>>9")

        if rev_title1 != "":
            output_list = Output_list()
            output_list_list.append(output_list)

            output_list.str = " " + to_string(rev_title1, "x(16)") + to_string(0, ">>>")

            if droom != 0:
                output_list.str = output_list.str + to_string((dpax - droom) / droom * 100, "->>9.99") + to_string(0, ">,>>>")
            else:
                output_list.str = output_list.str + to_string(0, "->>9.99") + to_string(0, ">,>>>")

            if mroom != 0:
                output_list.str = output_list.str + to_string((mpax - mroom) / mroom * 100, "->>9.99")
            else:
                output_list.str = output_list.str + to_string(0, "->>9.99")
            output_list.str = output_list.str + to_string(0, ">>>") + to_string(0, ">>,>>>")

            if yroom != 0:
                output_list.proz3 = to_string((ypax - yroom) / yroom * 100, "->>9.99")
            else:
                output_list.proz3 = to_string(0, "->>9.99")
        output_list = Output_list()
        output_list_list.append(output_list)

        output_list.str = " "
        output_list.yroom = fill("-", 10)
        output_list.proz3 = fill("-", 6)
        output_list.ypax = fill("-", 10)
        output_list.yrate = fill("-", 13)
        output_list.yrev = fill("-", 17)


        for i in range(1,96 + 1) :
            output_list.str = output_list.str + "----"


    def cal_umsatz2():

        nonlocal output_list_list, lvcarea, do_it, droomrev, mroomrev, yroomrev, droomexc, mroomexc, yroomexc, tot_room, all_room, dvacant, dooo, mvacant, mooo, yvacant, yooo, dnoshow, dcancel, mnoshow, mcancel, ynoshow, ycancel, droom, proz1, mroom, proz2, dpax, mpax, drate, mrate, drev, mrev, yroom, ypax, yrate, yrev, from_bez, to_bez, inactive, mtd_act, mtd_totrm, ytd_act, ytd_totrm, ncompli, mtd_ncompli, ytd_ncompli, dcompli, mcompli, ycompli, dhu, mhu, yhu, htparam, zimmer, zkstat, zinrstat, genstat, segment, guestseg, artikel, umsatz
        nonlocal pvilanguage, opening_date, from_date, to_date, fdate, tdate, segmtype_exist, mi_mtd_chk, mi_ftd_chk, mi_exchu_chk, mi_exccomp_chk, long_digit


        nonlocal cl_list, output_list
        nonlocal cl_list_list, output_list_list

        i:int = 0
        datum:date = None
        dooo = 0
        mooo = 0
        yooo = 0
        for datum in date_range(from_date,to_date) :

            zinrstat = get_cache (Zinrstat, {"datum": [(eq, datum)],"zinr": [(eq, "ooo")]})

            if zinrstat:

                if datum == to_date:
                    dooo = zinrstat.zimmeranz

                if (mi_mtd_chk and get_month(zinrstat.datum) == get_month(to_date)) or (mi_ftd_chk and zinrstat.datum >= fdate and zinrstat.datum <= tdate):
                    mooo = mooo + zinrstat.zimmeranz
                yooo = yooo + zinrstat.zimmeranz
        dvacant = tot_room - dooo - droom
        mvacant = mtd_act - mooo - mroom
        yvacant = ytd_act - yooo - yroom

        if to_date == opening_date:
            mvacant = dvacant
            yvacant = dvacant
            mooo = dooo
            yooo = dooo
        output_list = Output_list()
        output_list_list.append(output_list)

        output_list.str = " " + to_string(translateExtended ("V A C A n T", lvcarea, "") , "x(16)") +\
                to_string(dvacant, "->9") +\
                to_string(dvacant / tot_room * 100, "->>9.99") +\
                to_string(mvacant, "->,>>9") +\
                to_string(mvacant / mtd_act * 100, "->>9.99") +\
                to_string(0, ">>>") +\
                to_string(0, ">>>>>>") +\
                to_string("", "x(13)") +\
                to_string("", "x(13)") +\
                to_string(0, ">>>>>>>>>>>>>>") +\
                to_string(0, ">>>>>>>>>>>>>>>>")
        output_list.yroom = to_string(yvacant, "->,>>>,>>9")
        output_list.proz3 = to_string(yvacant / ytd_act * 100, "->>9.99")


        output_list = Output_list()
        output_list_list.append(output_list)

        output_list.str = " " + to_string(translateExtended ("Out Of Order", lvcarea, "") , "x(16)") +\
                to_string(dooo, ">>9") +\
                to_string(dooo / tot_room * 100, "->>9.99") +\
                to_string(mooo, ">>,>>9") +\
                to_string(mooo / mtd_act * 100, "->>9.99") +\
                to_string(0, ">>>") +\
                to_string(0, ">>>>>>") +\
                to_string("", "x(13)") +\
                to_string("", "x(13)") +\
                to_string(0, ">>>>>>>>>>>>>>") +\
                to_string(0, ">>>>>>>>>>>>>>>>")
        output_list.yroom = to_string(yooo, "->,>>>,>>9")
        output_list.proz3 = to_string(yooo / ytd_act * 100, "->>9.99")


        output_list = Output_list()
        output_list_list.append(output_list)

        output_list.str = " "
        output_list.yroom = fill("-", 10)
        output_list.proz3 = fill("-", 6)
        output_list.ypax = fill("-", 10)
        output_list.yrate = fill("-", 13)
        output_list.yrev = fill("-", 19)


        for i in range(1,96 + 1) :
            output_list.str = output_list.str + "----"

        zinrstat = get_cache (Zinrstat, {"zinr": [(eq, "tot-rm")],"datum": [(eq, to_date)]})

        if zinrstat:
            all_room = zinrstat.zimmeranz
        output_list = Output_list()
        output_list_list.append(output_list)

        output_list.str = " " + to_string(translateExtended ("# Active Rooms", lvcarea, "") , "x(16)") +\
                to_string(tot_room, ">>9") +\
                to_string(100, "->>9.99") +\
                to_string(mtd_act, ">>,>>9") +\
                to_string(100, "->>9.99") +\
                to_string(0, ">>>") +\
                to_string(0, ">>>>>>") +\
                to_string(0, ">>>>>>>>>>>>>") +\
                to_string(0, ">>>>>>>>>>>>>") +\
                to_string(0, ">>>>>>>>>>>>>>") +\
                to_string(0, ">>>>>>>>>>>>>>>>")
        output_list.yroom = to_string(ytd_act, "->,>>>,>>9")


        output_list = Output_list()
        output_list_list.append(output_list)

        output_list.str = " " + to_string(translateExtended ("inactive Rooms", lvcarea, "") , "x(16)") +\
                to_string(all_room - tot_room, ">>9") +\
                to_string("", ">>>>>>") +\
                to_string((mtd_totrm - mtd_act) , ">>>>>>") +\
                to_string("", ">>>>>>") +\
                to_string(0, ">>>") +\
                to_string(0, ">>>>>>") +\
                to_string(0, ">>>>>>>>>>>>>") +\
                to_string(0, ">>>>>>>>>>>>>") +\
                to_string(0, ">>>>>>>>>>>>>>") +\
                to_string(0, ">>>>>>>>>>>>>>>>")
        output_list.yroom = to_string(ytd_totrm - ytd_act, "->,>>>,>>9")


        output_list = Output_list()
        output_list_list.append(output_list)

        output_list.str = " " + to_string(translateExtended ("Total Rooms", lvcarea, "") , "x(16)") +\
                to_string(all_room, ">>9") +\
                to_string("", ">>>>>>") +\
                to_string(mtd_totrm, ">>>>>>") +\
                to_string("", ">>>>>>") +\
                to_string(0, ">>>") +\
                to_string(0, ">>>>>>") +\
                to_string(0, ">>>>>>>>>>>>>") +\
                to_string(0, ">>>>>>>>>>>>>") +\
                to_string(0, ">>>>>>>>>>>>>>") +\
                to_string(0, ">>>>>>>>>>>>>>>>>")
        output_list.yroom = to_string(ytd_totrm , "->,>>>,>>9")


        output_list = Output_list()
        output_list_list.append(output_list)

        output_list.str = " "
        output_list.yroom = fill("-", 10)
        output_list.proz3 = fill("-", 6)
        output_list.ypax = fill("-", 10)
        output_list.yrate = fill("-", 13)
        output_list.yrev = fill("-", 17)


        for i in range(1,96 + 1) :
            output_list.str = output_list.str + "----"


    def cal_umsatz3():

        nonlocal output_list_list, lvcarea, do_it, droomrev, mroomrev, yroomrev, droomexc, mroomexc, yroomexc, tot_room, all_room, dvacant, dooo, mvacant, mooo, yvacant, yooo, dnoshow, dcancel, mnoshow, mcancel, ynoshow, ycancel, droom, proz1, mroom, proz2, dpax, mpax, drate, mrate, drev, mrev, yroom, ypax, yrate, yrev, from_bez, to_bez, inactive, mtd_act, mtd_totrm, ytd_act, ytd_totrm, ncompli, mtd_ncompli, ytd_ncompli, dcompli, mcompli, ycompli, dhu, mhu, yhu, htparam, zimmer, zkstat, zinrstat, genstat, segment, guestseg, artikel, umsatz
        nonlocal pvilanguage, opening_date, from_date, to_date, fdate, tdate, segmtype_exist, mi_mtd_chk, mi_ftd_chk, mi_exchu_chk, mi_exccomp_chk, long_digit


        nonlocal cl_list, output_list
        nonlocal cl_list_list, output_list_list

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
        drev_droom1:Decimal = to_decimal("0.0")
        mrev_mroom1:Decimal = to_decimal("0.0")

        htparam = get_cache (Htparam, {"paramnr": [(eq, 479)]})
        serv_vat = htparam.flogical

        for artikel in db_session.query(Artikel).filter(
                 (Artikel.departement == 0) & (Artikel.artart == 0) & (Artikel.umsatzart == 1)).order_by(Artikel.artnr).all():
            max_i = max_i + 1
            art_list[max_i - 1] = artikel.artnr

        if do_it:
            pass
        else:
            for i in range(1,max_i + 1) :

                artikel = get_cache (Artikel, {"artnr": [(eq, art_list[i - 1])],"departement": [(eq, 0)]})

                if artikel:
                    cl_list = Cl_list()
                    cl_list_list.append(cl_list)

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
                                drev =  to_decimal(drev) + to_decimal(umsatz.betrag) / to_decimal(fact)
                                cl_list.drev =  to_decimal(umsatz.betrag) / to_decimal(fact)

                            if (mi_mtd_chk and get_month(datum) == get_month(to_date)) or (mi_ftd_chk and datum >= fdate and datum <= tdate):
                                mrev =  to_decimal(mrev) + to_decimal(umsatz.betrag) / to_decimal(fact)
                                cl_list.mrev =  to_decimal(cl_list.mrev) + to_decimal(umsatz.betrag) / to_decimal(fact)
                            yrev =  to_decimal(yrev) + to_decimal(umsatz.betrag) / to_decimal(fact)


                            cl_list.yrev =  to_decimal(cl_list.yrev) + to_decimal(umsatz.betrag) / to_decimal(fact)

                    if cl_list.mrev != 0:
                        output_list = Output_list()
                        output_list_list.append(output_list)


                        if not long_digit:
                            output_list.str = " " + to_string(cl_list.bezeich, "x(16)") + to_string(0, ">>>") + to_string(0, ">>>>>>") + to_string(0, ">>>>>>") + to_string(0, ">>>>>>") + to_string(0, ">>>") + to_string(0, ">>>>>>") + to_string("", "x(13)") + to_string("", "x(13)") + to_string(cl_list.drev, "->>,>>>,>>9.99") + to_string(cl_list.mrev, "->>>>,>>>,>>9.99")
                        else:
                            output_list.str = " " + to_string(cl_list.bezeich, "x(16)") + to_string(0, ">>>") + to_string(0, ">>>>>>") + to_string(0, ">>>>>>") + to_string(0, ">>>>>>") + to_string(0, ">>>") + to_string(0, ">>>>>>") + to_string(0, ">>>>>>>>>>>>>") + to_string(0, ">>>>>>>>>>>>>") + to_string(cl_list.drev, ">>,>>>,>>>,>>9") + to_string(cl_list.mrev, ">>>>,>>>,>>>,>>9")
            output_list = Output_list()
            output_list_list.append(output_list)

            output_list.str = " "
            output_list.yroom = fill("-", 10)
            output_list.proz3 = fill("-", 6)
            output_list.ypax = fill("-", 10)
            output_list.yrate = fill("-", 13)
            output_list.yrev = fill("-", 17)


            for i in range(1,96 + 1) :
                output_list.str = output_list.str + "----"

        if mi_exchu_chk :
            ncompli = ncompli - dhu
            mtd_ncompli = mtd_ncompli - mhu
            ytd_ncompli = ytd_ncompli - yhu

        if mi_exccomp_chk :
            ncompli = ncompli - dcompli
            mtd_ncompli = mtd_ncompli - mcompli
            ytd_ncompli = ytd_ncompli - ycompli


        drev_droom =  to_decimal(drev) / to_decimal(droom)
        drev_droom1 =  to_decimal(drev) / to_decimal(droomrev)

        if drev_droom == None:
            drev_droom =  to_decimal("0")

        if drev_droom1 == None:
            drev_droom1 =  to_decimal("0")
        mrev_mroom =  to_decimal(mrev) / to_decimal(mroom)
        mrev_mroom1 =  to_decimal(mrev) / to_decimal(mroomrev)

        if mrev_mroom == None:
            mrev_mroom =  to_decimal("0")

        if mrev_mroom1 == None:
            mrev_mroom1 =  to_decimal("0")

        if not long_digit:
            output_list = Output_list()
            output_list_list.append(output_list)

            output_list.str = " " + to_string(translateExtended ("RmRev Inc Comp", lvcarea, "") , "x(16)") +\
                    to_string(0, ">>>") +\
                    to_string(0, ">>>>>>") +\
                    to_string(0, ">>>>>>") +\
                    to_string(0, ">>>>>>") +\
                    to_string(0, ">>>") +\
                    to_string(0, ">>>>>>") +\
                    to_string(drev_droom, "->,>>>,>>9.99") +\
                    to_string(mrev_mroom, "->,>>>,>>9.99") +\
                    to_string(drev, ">>>,>>>,>>9.99") +\
                    to_string(mrev, ">>>,>>>,>>>,>>9.99")
            output_list.yrev = to_string(yrev, "->>>,>>>,>>>,>>9.99")

            if yroom != 0:
                output_list.yrate = to_string(yrev / yroom, "->,>>>,>>9.99")
            output_list = Output_list()
            output_list_list.append(output_list)

            output_list.str = " " + to_string(translateExtended ("RmRev Exc Comp", lvcarea, "") , "x(16)") +\
                    to_string(0, ">>>") +\
                    to_string(0, ">>>>>>") +\
                    to_string(0, ">>>>>>") +\
                    to_string(0, ">>>>>>") +\
                    to_string(0, ">>>") +\
                    to_string(0, ">>>>>>") +\
                    to_string(drev_droom1, "->,>>>,>>9.99") +\
                    to_string(mrev_mroom1, "->,>>>,>>9.99") +\
                    to_string(drev, ">>>,>>>,>>9.99") +\
                    to_string(mrev, ">>>,>>>,>>>,>>9.99")
            output_list.yrev = to_string(yrev, "->>>,>>>,>>>,>>9.99")

            if yroomrev != 0:
                output_list.yrate = to_string(yrev / yroomrev, "->,>>>,>>9.99")
        else:
            output_list = Output_list()
            output_list_list.append(output_list)

            output_list.str = " " + to_string(translateExtended ("Total RmRevenue (comp guest)", lvcarea, "") , "x(30)") +\
                    to_string(0, ">>>") +\
                    to_string(0, ">>>>>>") +\
                    to_string(0, ">>>>>>") +\
                    to_string(0, ">>>>>>") +\
                    to_string(0, ">>>") +\
                    to_string(0, ">>>>>>") +\
                    to_string(drev_droom, "->>>,>>>,>>>") +\
                    to_string(mrev_mroom, "->>>,>>>,>>>") +\
                    to_string(drev, ">>,>>>,>>>,>>9") +\
                    to_string(mrev, ">>>>,>>>,>>>,>>9")
            output_list.yrev = to_string(yrev, "->>>,>>>,>>>,>>>,>>9")


            output_list = Output_list()
            output_list_list.append(output_list)

            output_list.str = " " + to_string(translateExtended ("Total RmRevenue (paying guest)", lvcarea, "") , "x(30)") +\
                    to_string(0, ">>>") +\
                    to_string(0, ">>>>>>") +\
                    to_string(0, ">>>>>>") +\
                    to_string(0, ">>>>>>") +\
                    to_string(0, ">>>") +\
                    to_string(0, ">>>>>>") +\
                    to_string(drev_droom1, "->>>,>>>,>>>") +\
                    to_string(mrev_mroom1, "->>>,>>>,>>>") +\
                    to_string(drev, ">>,>>>,>>>,>>9") +\
                    to_string(mrev, ">>>>,>>>,>>>,>>9")
            output_list.yrev = to_string(yrev, "->>>>,>>>,>>>,>>9")


        output_list = Output_list()
        output_list_list.append(output_list)

        output_list.str = " "
        output_list.yroom = fill("-", 10)
        output_list.proz3 = fill("-", 6)
        output_list.ypax = fill("-", 10)
        output_list.yrate = fill("-", 13)
        output_list.yrev = fill("-", 19)


        for i in range(1,96 + 1) :
            output_list.str = output_list.str + "----"


    def no_show():

        nonlocal output_list_list, lvcarea, do_it, droomrev, mroomrev, yroomrev, droomexc, mroomexc, yroomexc, tot_room, all_room, dvacant, dooo, mvacant, mooo, yvacant, yooo, dnoshow, dcancel, mnoshow, mcancel, ynoshow, ycancel, droom, proz1, mroom, proz2, dpax, mpax, drate, mrate, drev, mrev, yroom, ypax, yrate, yrev, from_bez, to_bez, inactive, mtd_act, mtd_totrm, ytd_act, ytd_totrm, ncompli, mtd_ncompli, ytd_ncompli, dcompli, mcompli, ycompli, dhu, mhu, yhu, htparam, zimmer, zkstat, zinrstat, genstat, segment, guestseg, artikel, umsatz
        nonlocal pvilanguage, opening_date, from_date, to_date, fdate, tdate, segmtype_exist, mi_mtd_chk, mi_ftd_chk, mi_exchu_chk, mi_exccomp_chk, long_digit


        nonlocal cl_list, output_list
        nonlocal cl_list_list, output_list_list

        i:int = 0
        dnoshow = 0
        dcancel = 0
        mnoshow = 0
        mcancel = 0

        for zinrstat in db_session.query(Zinrstat).filter(
                 (Zinrstat.zinr == ("No-Show").lower()) & (Zinrstat.datum >= from_date) & (Zinrstat.datum <= to_date)).order_by(Zinrstat._recid).all():

            if zinrstat.datum == to_date:
                dnoshow = dnoshow + zinrstat.zimmeranz

            if (mi_mtd_chk and get_month(datum) == get_month(to_date)) or (mi_ftd_chk and datum >= fdate and datum <= tdate):
                mnoshow = mnoshow + zinrstat.zimmeranz
            ynoshow = ynoshow + zinrstat.zimmeranz

        for zinrstat in db_session.query(Zinrstat).filter(
                 (Zinrstat.zinr == ("CancRes").lower()) & (Zinrstat.datum >= from_date) & (Zinrstat.datum <= to_date)).order_by(Zinrstat._recid).all():

            if zinrstat.datum == to_date:
                dcancel = dcancel + zinrstat.zimmeranz

            if get_month(datum) == get_month(to_date):
                mcancel = mcancel + zinrstat.zimmeranz


            ycancel = ycancel + zinrstat.zimmeranz
        output_list = Output_list()
        output_list_list.append(output_list)

        output_list.str = " " + to_string(translateExtended ("NO SHOW", lvcarea, "") , "x(16)") +\
                to_string(dnoshow, ">>9") +\
                to_string(0, "->>9.99") +\
                to_string(mnoshow, ">>,>>9") +\
                to_string(0, ">>>>>>") +\
                to_string(0, ">>>") +\
                to_string(0, ">>>>>>") +\
                to_string(0, ">>>>>>>>>>>>>") +\
                to_string(0, ">>>>>>>>>>>>>") +\
                to_string(0, ">>>>>>>>>>>>>>") +\
                to_string(0, ">>>>>>>>>>>>>>>>")
        output_list.yroom = to_string(ynoshow, "->,>>>,>>9")


        output_list = Output_list()
        output_list_list.append(output_list)

        output_list.str = " " + to_string(translateExtended ("C A n C E L", lvcarea, "") , "x(16)") +\
                to_string(dcancel, ">>9") +\
                to_string(0, "->>9.99") +\
                to_string(mcancel, ">>,>>9") +\
                to_string(0, ">>>>>>") +\
                to_string(0, ">>>") +\
                to_string(0, ">>>>>>") +\
                to_string(0, ">>>>>>>>>>>>>") +\
                to_string(0, ">>>>>>>>>>>>>") +\
                to_string(0, ">>>>>>>>>>>>>>") +\
                to_string(0, ">>>>>>>>>>>>>>>>")
        output_list.yroom = to_string(ycancel, "->,>>>,>>9")


        output_list = Output_list()
        output_list_list.append(output_list)

        output_list.str = " "
        output_list.yroom = fill("-", 10)
        output_list.proz3 = fill("-", 6)
        output_list.ypax = fill("-", 10)
        output_list.yrate = fill("-", 13)
        output_list.yrev = fill("-", 17)


        for i in range(1,96 + 1) :
            output_list.str = output_list.str + "----"

    htparam = get_cache (Htparam, {"paramnr": [(eq, 186)]})
    opening_date = htparam.fdate

    if get_month(to_date) == get_month(opening_date) and get_year(to_date) == get_year(opening_date):
        from_date = opening_date
    create_umsatz()

    return generate_output()