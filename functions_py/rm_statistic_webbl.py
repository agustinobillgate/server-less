#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Htparam, Segment, Zinrstat, Genstat, Queasy

def rm_statistic_webbl(pvilanguage:int, call_from:int, txt_file:string, to_date:date, grp_flag:bool, show_ytd:bool, show_other:bool):

    prepare_cache ([Htparam, Segment, Zinrstat, Genstat, Queasy])

    rm_statistic_list_data = []
    rm_statistic_list1_data = []
    lnldelimeter:string = ""
    long_digit:bool = False
    droom:int = 0
    proz1:Decimal = to_decimal("0.0")
    mroom:int = 0
    proz2:Decimal = to_decimal("0.0")
    yroom:int = 0
    proz3:Decimal = to_decimal("0.0")
    dpax:int = 0
    mpax:int = 0
    ypax:int = 0
    drate:Decimal = to_decimal("0.0")
    mrate:Decimal = to_decimal("0.0")
    yrate:Decimal = to_decimal("0.0")
    drev:Decimal = to_decimal("0.0")
    mrev:Decimal = to_decimal("0.0")
    yrev:Decimal = to_decimal("0.0")
    lodg:Decimal = to_decimal("0.0")
    olodg:Decimal = to_decimal("0.0")
    dgroom:int = 0
    gproz1:Decimal = to_decimal("0.0")
    mgroom:int = 0
    gproz2:int = 0
    ygroom:int = 0
    gproz3:int = 0
    dgpax:int = 0
    mgpax:int = 0
    ygpax:int = 0
    dgrate:Decimal = to_decimal("0.0")
    mgrate:Decimal = to_decimal("0.0")
    ygrate:Decimal = to_decimal("0.0")
    dgrev:Decimal = to_decimal("0.0")
    mgrev:Decimal = to_decimal("0.0")
    ygrev:Decimal = to_decimal("0.0")
    dgroom1:int = 0
    mgroom1:int = 0
    ygroom1:int = 0
    dgpax1:int = 0
    mgpax1:int = 0
    ygpax1:int = 0
    dgrate1:Decimal = to_decimal("0.0")
    mgrate1:Decimal = to_decimal("0.0")
    ygrate1:Decimal = to_decimal("0.0")
    dgrev1:Decimal = to_decimal("0.0")
    mgrev1:Decimal = to_decimal("0.0")
    ygrev1:Decimal = to_decimal("0.0")
    ttrev:Decimal = to_decimal("0.0")
    ttmrev:Decimal = to_decimal("0.0")
    ttyrev:Decimal = to_decimal("0.0")
    from_date:date = None
    period_str:string = ""
    comp_room:string = ""
    curr_grup:int = 0
    tot_droom:int = 0
    tot_proz1:Decimal = to_decimal("0.0")
    tot_mroom:int = 0
    tot_proz2:Decimal = to_decimal("0.0")
    tot_yroom:int = 0
    tot_proz3:Decimal = to_decimal("0.0")
    tot_dpax:int = 0
    tot_mpax:int = 0
    tot_ypax:int = 0
    tot_drate:Decimal = to_decimal("0.0")
    tot_mrate:Decimal = to_decimal("0.0")
    tot_yrate:Decimal = to_decimal("0.0")
    tot_drev:Decimal = to_decimal("0.0")
    tot_mrev:Decimal = to_decimal("0.0")
    tot_yrev:Decimal = to_decimal("0.0")
    lvcarea:string = "rm-statistic-web"
    htparam = segment = zinrstat = genstat = queasy = None

    rm_statistic_list = rm_statistic_list1 = cl_list = other_list = s_list = r_list = r_list1 = None

    rm_statistic_list_data, Rm_statistic_list = create_model("Rm_statistic_list", {"grpflag":bool, "flag":string, "segm":string, "bezeich":string, "dgroom":string, "proz1":string, "mgroom":string, "proz2":string, "ygroom":string, "proz3":string, "dgpax":string, "mgpax":string, "ygpax":string, "dgrate":string, "mgrate":string, "ygrate":string, "dgrev":string, "mgrev":string, "ygrev":string, "segm_descr":string})
    rm_statistic_list1_data, Rm_statistic_list1 = create_model("Rm_statistic_list1", {"grpflag":bool, "flag":string, "segm":string, "bezeich":string, "droom":string, "proz1":string, "mroom":string, "proz2":string, "yroom":string, "proz3":string, "dpax":string, "mpax":string, "ypax":string, "drate":string, "mrate":string, "yrate":string, "drev":string, "mrev":string, "yrev":string, "segm_descr":string})
    cl_list_data, Cl_list = create_model("Cl_list", {"grpflag":bool, "flag":string, "segm":int, "bezeich":string, "droom":int, "tot_droom":int, "proz1":Decimal, "mroom":int, "proz2":Decimal, "yroom":int, "proz3":Decimal, "dpax":int, "tot_dpax":int, "mpax":int, "ypax":int, "drate":Decimal, "mrate":Decimal, "yrate":Decimal, "drev":Decimal, "mrev":Decimal, "yrev":Decimal, "orev":Decimal, "flag_comp":bool, "flag_temp":bool, "segm_grup":int, "segm_descr":string})
    other_list_data, Other_list = create_model("Other_list", {"flag":string, "segm":int, "bezeich":string, "orev":Decimal, "morev":Decimal, "yorev":Decimal})
    s_list_data, S_list = create_model("S_list", {"nr":int, "bezeich":string, "droom":int, "mroom":int, "yroom":int, "dpax":int, "mpax":int, "ypax":int})

    R_list = Rm_statistic_list
    r_list_data = rm_statistic_list_data

    R_list1 = Rm_statistic_list1
    r_list1_data = rm_statistic_list1_data

    db_session = local_storage.db_session

    def generate_output():
        nonlocal rm_statistic_list_data, rm_statistic_list1_data, lnldelimeter, long_digit, droom, proz1, mroom, proz2, yroom, proz3, dpax, mpax, ypax, drate, mrate, yrate, drev, mrev, yrev, lodg, olodg, dgroom, gproz1, mgroom, gproz2, ygroom, gproz3, dgpax, mgpax, ygpax, dgrate, mgrate, ygrate, dgrev, mgrev, ygrev, dgroom1, mgroom1, ygroom1, dgpax1, mgpax1, ygpax1, dgrate1, mgrate1, ygrate1, dgrev1, mgrev1, ygrev1, ttrev, ttmrev, ttyrev, from_date, period_str, comp_room, curr_grup, tot_droom, tot_proz1, tot_mroom, tot_proz2, tot_yroom, tot_proz3, tot_dpax, tot_mpax, tot_ypax, tot_drate, tot_mrate, tot_yrate, tot_drev, tot_mrev, tot_yrev, lvcarea, htparam, segment, zinrstat, genstat, queasy
        nonlocal pvilanguage, call_from, txt_file, to_date, grp_flag, show_ytd, show_other
        nonlocal r_list, r_list1


        nonlocal rm_statistic_list, rm_statistic_list1, cl_list, other_list, s_list, r_list, r_list1
        nonlocal rm_statistic_list_data, rm_statistic_list1_data, cl_list_data, other_list_data, s_list_data

        return {"rm-statistic-list": rm_statistic_list_data, "rm-statistic-list1": rm_statistic_list1_data}

    def create_other():

        nonlocal rm_statistic_list_data, rm_statistic_list1_data, lnldelimeter, long_digit, droom, proz1, mroom, proz2, yroom, proz3, dpax, mpax, ypax, drate, mrate, yrate, drev, mrev, yrev, lodg, olodg, dgroom, gproz1, mgroom, gproz2, ygroom, gproz3, dgpax, mgpax, ygpax, dgrate, mgrate, ygrate, dgrev, mgrev, ygrev, dgroom1, mgroom1, ygroom1, dgpax1, mgpax1, ygpax1, dgrate1, mgrate1, ygrate1, dgrev1, mgrev1, ygrev1, ttrev, ttmrev, ttyrev, from_date, period_str, comp_room, curr_grup, tot_droom, tot_proz1, tot_mroom, tot_proz2, tot_yroom, tot_proz3, tot_dpax, tot_mpax, tot_ypax, tot_drate, tot_mrate, tot_yrate, tot_drev, tot_mrev, tot_yrev, lvcarea, htparam, segment, zinrstat, genstat, queasy
        nonlocal pvilanguage, call_from, txt_file, to_date, grp_flag, show_ytd, show_other
        nonlocal r_list, r_list1


        nonlocal rm_statistic_list, rm_statistic_list1, cl_list, other_list, s_list, r_list, r_list1
        nonlocal rm_statistic_list_data, rm_statistic_list1_data, cl_list_data, other_list_data, s_list_data

        black_list:int = 0

        htparam = get_cache (Htparam, {"paramnr": [(eq, 709)]})
        black_list = htparam.finteger
        other_list_data.clear()

        zinrstat_obj_list = {}
        zinrstat = Zinrstat()
        segment = Segment()
        for zinrstat.logisumsatz, zinrstat.datum, zinrstat._recid, segment.segmentcode, segment.bezeich, segment.segmentgrup, segment._recid in db_session.query(Zinrstat.logisumsatz, Zinrstat.datum, Zinrstat._recid, Segment.segmentcode, Segment.bezeich, Segment.segmentgrup, Segment._recid).join(Segment,(Segment.segmentcode == Zinrstat.betriebsnr) & (Segment.segmentcode != black_list) & (Segment.segmentgrup <= 99)).filter(
                 (Zinrstat.datum >= from_date) & (Zinrstat.datum <= to_date) & (Zinrstat.zinr == ("SEGM").lower())).order_by(Segment.segmentgrup, Segment.segmentcode).all():
            if zinrstat_obj_list.get(zinrstat._recid):
                continue
            else:
                zinrstat_obj_list[zinrstat._recid] = True

            other_list = query(other_list_data, filters=(lambda other_list: other_list.segm == segment.segmentcode), first=True)

            if not other_list:
                other_list = Other_list()
                other_list_data.append(other_list)

                other_list.segm = segment.segmentcode

            if zinrstat.datum == to_date:
                other_list.orev =  to_decimal(zinrstat.logisumsatz)

            if get_month(zinrstat.datum) == get_month(to_date):
                other_list.morev =  to_decimal(other_list.morev) + to_decimal(zinrstat.logisumsatz)

            if show_ytd:
                other_list.yorev =  to_decimal(other_list.yorev) + to_decimal(zinrstat.logisumsatz)


    def create_umsatz2():

        nonlocal rm_statistic_list_data, rm_statistic_list1_data, lnldelimeter, long_digit, droom, proz1, mroom, proz2, yroom, proz3, dpax, mpax, ypax, drate, mrate, yrate, drev, mrev, yrev, lodg, olodg, dgroom, gproz1, mgroom, gproz2, ygroom, gproz3, dgpax, mgpax, ygpax, dgrate, mgrate, ygrate, dgrev, mgrev, ygrev, dgroom1, mgroom1, ygroom1, dgpax1, mgpax1, ygpax1, dgrate1, mgrate1, ygrate1, dgrev1, mgrev1, ygrev1, ttrev, ttmrev, ttyrev, from_date, period_str, comp_room, curr_grup, tot_droom, tot_proz1, tot_mroom, tot_proz2, tot_yroom, tot_proz3, tot_dpax, tot_mpax, tot_ypax, tot_drate, tot_mrate, tot_yrate, tot_drev, tot_mrev, tot_yrev, lvcarea, htparam, segment, zinrstat, genstat, queasy
        nonlocal pvilanguage, call_from, txt_file, to_date, grp_flag, show_ytd, show_other
        nonlocal r_list, r_list1


        nonlocal rm_statistic_list, rm_statistic_list1, cl_list, other_list, s_list, r_list, r_list1
        nonlocal rm_statistic_list_data, rm_statistic_list1_data, cl_list_data, other_list_data, s_list_data

        black_list:int = 0
        fl_comp:bool = False
        i:int = 0
        curr_grp:int = -1
        curr_segm:int = 0
        aa:int = 0
        xx:int = 0
        tot_slist_dpax:Decimal = to_decimal("0.0")
        flag_temp:bool = False

        htparam = get_cache (Htparam, {"paramnr": [(eq, 709)]})
        black_list = htparam.finteger
        rm_statistic_list_data.clear()
        rm_statistic_list1_data.clear()
        cl_list_data.clear()
        s_list_data.clear()
        droom = 0
        mroom = 0
        yroom = 0
        dpax = 0
        mpax = 0
        ypax = 0
        drate =  to_decimal("0")
        mrate =  to_decimal("0")
        yrate =  to_decimal("0")
        drev =  to_decimal("0")
        mrev =  to_decimal("0")
        yrev =  to_decimal("0")
        dgroom = 0
        mgroom = 0
        ygroom = 0
        dgpax = 0
        mgpax = 0
        ygpax = 0
        dgrate =  to_decimal("0")
        mgrate =  to_decimal("0")
        ygrate =  to_decimal("0")
        dgrev =  to_decimal("0")
        mgrev =  to_decimal("0")
        ygrev =  to_decimal("0")
        dgroom1 = 0
        mgroom1 = 0
        ygroom1 = 0
        dgpax1 = 0
        mgpax1 = 0
        ygpax1 = 0
        dgrate1 =  to_decimal("0")
        mgrate1 =  to_decimal("0")
        ygrate1 =  to_decimal("0")
        dgrev1 =  to_decimal("0")
        mgrev1 =  to_decimal("0")
        ygrev1 =  to_decimal("0")
        tot_droom = 0
        tot_proz1 =  to_decimal("0")
        tot_mroom = 0
        tot_proz2 =  to_decimal("0")
        tot_yroom = 0
        tot_proz3 = 0
        tot_dpax = 0
        tot_mpax = 0
        tot_ypax = 0
        tot_drate =  to_decimal("0")
        tot_mrate =  to_decimal("0")
        tot_yrate =  to_decimal("0")
        tot_drev =  to_decimal("0")
        tot_mrev =  to_decimal("0")
        tot_yrev =  to_decimal("0")


        from_date = date_mdy(1, 1, get_year(to_date))

        if show_other:
            create_other()

        genstat_obj_list = {}
        genstat = Genstat()
        segment = Segment()

        for genstat.resstatus, genstat.gratis, genstat.segmentcode, genstat.logis, genstat.erwachs, genstat.kind1, genstat.kind2, genstat.kind3, genstat.zipreis, genstat.datum, genstat._recid, segment.segmentcode, segment.bezeich, segment.segmentgrup, segment._recid in db_session.query(Genstat.resstatus, Genstat.gratis, Genstat.segmentcode, Genstat.logis, Genstat.erwachs, Genstat.kind1, Genstat.kind2, Genstat.kind3, Genstat.zipreis, Genstat.datum, Genstat._recid, Segment.segmentcode, Segment.bezeich, Segment.segmentgrup, Segment._recid).join(Segment,(Segment.segmentcode == Genstat.segmentcode) & (Segment.segmentcode != black_list)).filter((Genstat.datum >= from_date) & (Genstat.datum <= to_date) & (Genstat.segmentcode != 0) & (Genstat.nationnr != 0) & (Genstat.zinr != "") & (Genstat.res_logic[inc_value(1)])).order_by(Genstat.segmentcode).all():

            # if genstat_obj_list.get(genstat._recid):
            #     continue
            # else:
            #     genstat_obj_list[genstat._recid] = True

            if genstat.zipreis == 0 and genstat.resstatus == 6 and genstat.gratis != 0:
                fl_comp = True
            else:
                fl_comp = False

            cl_list = query(cl_list_data, filters=(lambda cl_list: cl_list.segm == genstat.segmentcode and cl_list.flag_comp == fl_comp and not cl_list.grpflag), first=True)

            if not cl_list:
                cl_list = Cl_list()
                cl_list_data.append(cl_list)

                cl_list.segm = genstat.segmentcode
                cl_list.bezeich = segment.bezeich
                cl_list.flag_comp = fl_comp
                cl_list.segm_grup = segment.segmentgrup

                queasy = get_cache (Queasy, {"key": [(eq, 26)],"number1": [(eq, segment.segmentgrup)]})

                if queasy:
                    cl_list.segm_descr = queasy.char3

                if genstat.zipreis == 0 and genstat.resstatus != 13 and genstat.resstatus == 6 and genstat.gratis != 0:

                    if genstat.datum == to_date:
                        cl_list.droom = 1
                        cl_list.dpax = cl_list.dpax + genstat.gratis
                        droom = droom + 1

                    if get_month(genstat.datum) == get_month(to_date):
                        cl_list.mroom = 1
                        cl_list.mpax = cl_list.mpax + genstat.gratis
                        mroom = mroom + 1


                    cl_list.yroom = cl_list.yroom + 1
                    cl_list.ypax = cl_list.ypax + genstat.gratis
                    yroom = yroom + 1

                elif genstat.resstatus != 13:

                    if genstat.datum == to_date:
                        cl_list.drev =  to_decimal(genstat.logis)
                        cl_list.droom = cl_list.droom + 1
                        cl_list.dpax = cl_list.dpax + genstat.erwachs +\
                                genstat.kind1 + genstat.kind2 + genstat.kind3
                        dgroom = dgroom + 1
                        dgpax = dgpax + genstat.erwachs +\
                                genstat.kind1 + genstat.kind2 + genstat.kind3
                        dgrev =  to_decimal(dgrev) + to_decimal(genstat.logis)
                        cl_list.drate =  to_decimal(cl_list.drate) + to_decimal((cl_list.drev) / to_decimal(cl_list.droom) )
                        dgrate =  to_decimal(dgrev) / to_decimal(dgroom)
                        droom = droom + 1

                    if get_month(genstat.datum) == get_month(to_date):
                        cl_list.mrev =  to_decimal(genstat.logis)
                        cl_list.mroom = cl_list.mroom + 1
                        cl_list.mpax = cl_list.mpax + genstat.erwachs +\
                                genstat.kind1 + genstat.kind2 + genstat.kind3
                        mgroom = mgroom + 1
                        mgpax = mgpax + genstat.erwachs + genstat.kind1 +\
                                genstat.kind2 + genstat.kind3
                        mgrev =  to_decimal(mgrev) + to_decimal(genstat.logis)
                        cl_list.mrate =  to_decimal(cl_list.mrate) + to_decimal((cl_list.mrev) / to_decimal(cl_list.mroom) )
                        mgrate =  to_decimal(mgrev) / to_decimal(mgroom)
                        mroom = mroom + 1


                    cl_list.yrev =  to_decimal(genstat.logis)
                    cl_list.yroom = cl_list.yroom + 1
                    cl_list.ypax = cl_list.ypax + genstat.erwachs +\
                            genstat.kind1 + genstat.kind2 + genstat.kind3
                    ygroom = ygroom + 1
                    ygpax = ygpax + genstat.erwachs + genstat.kind1 +\
                            genstat.kind2 + genstat.kind3
                    ygrev =  to_decimal(ygrev) + to_decimal(genstat.logis)
                    cl_list.yrate =  to_decimal(cl_list.yrate) + to_decimal((cl_list.yrev) / to_decimal(cl_list.yroom) )
                    ygrate =  to_decimal(ygrev) / to_decimal(ygroom)
                    yroom = yroom + 1


            else:

                if genstat.zipreis == 0 and genstat.resstatus != 13 and genstat.resstatus == 6 and genstat.gratis != 0:

                    if genstat.datum == to_date:
                        cl_list.droom = cl_list.droom + 1
                        cl_list.dpax = cl_list.dpax + genstat.gratis
                        droom = droom + 1

                    if get_month(genstat.datum) == get_month(to_date):
                        cl_list.mroom = cl_list.mroom + 1
                        cl_list.mpax = cl_list.mpax + genstat.gratis
                        mroom = mroom + 1


                    cl_list.yroom = cl_list.yroom + 1
                    cl_list.ypax = cl_list.ypax + genstat.gratis
                    yroom = yroom + 1

                elif genstat.resstatus != 13:

                    if genstat.datum == to_date:
                        cl_list.drev =  to_decimal(cl_list.drev) + to_decimal(genstat.logis)
                        cl_list.droom = cl_list.droom + 1
                        cl_list.dpax = cl_list.dpax + genstat.erwachs +\
                                genstat.kind1 + genstat.kind2 + genstat.kind3
                        dgroom = dgroom + 1
                        dgpax = dgpax + genstat.erwachs + genstat.kind1 + genstat.kind2 + genstat.kind3
                        dgrev =  to_decimal(dgrev) + to_decimal(genstat.logis)
                        cl_list.drate =  to_decimal(cl_list.drev) / to_decimal(cl_list.droom)
                        dgrate =  to_decimal(dgrev) / to_decimal(dgroom)
                        droom = droom + 1

                    if get_month(genstat.datum) == get_month(to_date):
                        cl_list.mrev =  to_decimal(cl_list.mrev) + to_decimal(genstat.logis)
                        cl_list.mroom = cl_list.mroom + 1
                        cl_list.mpax = cl_list.mpax + genstat.erwachs + genstat.kind1 +\
                                genstat.kind2 + genstat.kind3
                        mgroom = mgroom + 1
                        mgpax = mgpax + genstat.erwachs + genstat.kind1 + genstat.kind2 + genstat.kind3
                        mgrev =  to_decimal(mgrev) + to_decimal(genstat.logis)
                        cl_list.mrate =  to_decimal(cl_list.mrev) / to_decimal(cl_list.mroom)
                        mgrate =  to_decimal(mgrev) / to_decimal(mgroom)
                        mroom = mroom + 1


                    cl_list.yroom = cl_list.yroom + 1
                    ygroom = ygroom + 1
                    cl_list.yrev =  to_decimal(cl_list.yrev) + to_decimal(genstat.logis)
                    ygrev =  to_decimal(ygrev) + to_decimal(genstat.logis)
                    cl_list.yrate =  to_decimal(cl_list.yrev) / to_decimal(cl_list.yroom)
                    ygrate =  to_decimal(ygrev) / to_decimal(ygroom)
                    cl_list.ypax = cl_list.ypax + genstat.erwachs + genstat.kind1 + genstat.kind2
                    ygpax = ygpax + genstat.erwachs + genstat.kind1 + genstat.kind2
                    yroom = yroom + 1

        for cl_list in query(cl_list_data, filters=(lambda cl_list: not cl_list.flag_comp)):

            if cl_list.droom == 0:
                cl_list.dpax = 0

            if cl_list.mroom == 0:
                cl_list.mpax = 0

            if cl_list.yroom == 0:
                cl_list.ypax = 0

            if cl_list.droom != 0:
                cl_list.drate =  to_decimal(cl_list.drev) / to_decimal(cl_list.droom)

            if cl_list.mroom != 0:
                cl_list.mrate =  to_decimal(cl_list.mrev) / to_decimal(cl_list.mroom)

            if droom != 0:
                cl_list.proz1 =  to_decimal(100.0) * to_decimal(cl_list.droom) / to_decimal(droom)

            if mroom != 0:
                cl_list.proz2 =  to_decimal(100.0) * to_decimal(cl_list.mroom) / to_decimal(mroom)

            if yroom != 0:
                cl_list.proz3 =  to_decimal(100.0) * to_decimal(cl_list.yroom) / to_decimal(yroom)

            if droom != 0:
                drate =  to_decimal(drev) / to_decimal(droom)

            if mroom != 0:
                mrate =  to_decimal(mrev) / to_decimal(mroom)

            if show_ytd:

                if cl_list.yroom != 0:
                    cl_list.yrate =  to_decimal(cl_list.yrev) / to_decimal(cl_list.yroom)

                if yroom != 0:
                    cl_list.proz3 =  to_decimal(100.0) * to_decimal(cl_list.yroom) / to_decimal(yroom)

                if yroom != 0:
                    yrate =  to_decimal(yrev) / to_decimal(yroom)

            if grp_flag and not cl_list.grpflag:

                if cl_list.segm_grup != curr_grup and curr_grup != 0:
                    rm_statistic_list1 = Rm_statistic_list1()
                    rm_statistic_list1_data.append(rm_statistic_list1)

                    rm_statistic_list1.segm = ""
                    rm_statistic_list1.bezeich = "T O T A L"
                    rm_statistic_list1.droom = to_string(tot_droom, ">>,>>9")
                    rm_statistic_list1.proz1 = to_string(tot_proz1, ">>9.99")
                    rm_statistic_list1.mroom = to_string(tot_mroom, ">>,>>9")
                    rm_statistic_list1.proz2 = to_string(tot_proz2, ">>9.99")
                    rm_statistic_list1.yroom = to_string(tot_yroom, ">>,>>9")
                    rm_statistic_list1.proz3 = to_string(tot_proz3, ">>9.99")
                    rm_statistic_list1.dpax = to_string(tot_dpax, ">>,>>9")
                    rm_statistic_list1.mpax = to_string(tot_mpax, ">>,>>9")
                    rm_statistic_list1.ypax = to_string(tot_ypax, ">>,>>9")
                    rm_statistic_list1.drate = to_string(tot_drate, "->>>,>>>,>>>,>>9.99")
                    rm_statistic_list1.mrate = to_string(tot_mrate, "->>>,>>>,>>>,>>9.99")
                    rm_statistic_list1.yrate = to_string(tot_yrate, "->>>,>>>,>>>,>>9.99")
                    rm_statistic_list1.drev = to_string(tot_drev, "->>>,>>>,>>>,>>9.99")
                    rm_statistic_list1.mrev = to_string(tot_mrev, "->>>,>>>,>>>,>>9.99")
                    rm_statistic_list1.yrev = to_string(tot_yrev, "->>>,>>>,>>>,>>9.99")
                    rm_statistic_list1.segm_descr = ""


                    rm_statistic_list1 = Rm_statistic_list1()
                    rm_statistic_list1_data.append(rm_statistic_list1)

                    tot_droom = 0
                    tot_proz1 =  to_decimal("0")
                    tot_mroom = 0
                    tot_proz2 =  to_decimal("0")
                    tot_yroom = 0
                    tot_proz3 = 0
                    tot_dpax = 0
                    tot_mpax = 0
                    tot_ypax = 0
                    tot_drate =  to_decimal("0")
                    tot_mrate =  to_decimal("0")
                    tot_yrate =  to_decimal("0")
                    tot_drev =  to_decimal("0")
                    tot_mrev =  to_decimal("0")
                    tot_yrev =  to_decimal("0")
                    tot_droom = tot_droom + cl_list.droom
                    tot_proz1 =  to_decimal(tot_proz1) + to_decimal(cl_list.proz1)
                    tot_mroom = tot_mroom + cl_list.mroom
                    tot_proz2 =  to_decimal(tot_proz2) + to_decimal(cl_list.proz2)
                    tot_yroom = tot_yroom + cl_list.yroom
                    tot_proz3 = tot_proz3 + cl_list.proz3
                    tot_dpax = tot_dpax + cl_list.dpax
                    tot_mpax = tot_mpax + cl_list.mpax
                    tot_ypax = tot_ypax + cl_list.ypax
                    tot_drate =  to_decimal(tot_drate) + to_decimal(cl_list.drate)
                    tot_mrate =  to_decimal(tot_mrate) + to_decimal(cl_list.mrate)
                    tot_yrate =  to_decimal(tot_yrate) + to_decimal(cl_list.yrate)
                    tot_drev =  to_decimal(tot_drev) + to_decimal(cl_list.drev)
                    tot_mrev =  to_decimal(tot_mrev) + to_decimal(cl_list.mrev)
                    tot_yrev =  to_decimal(tot_yrev) + to_decimal(cl_list.yrev)


                else:
                    tot_droom = tot_droom + cl_list.droom
                    tot_proz1 =  to_decimal(tot_proz1) + to_decimal(cl_list.proz1)
                    tot_mroom = tot_mroom + cl_list.mroom
                    tot_proz2 =  to_decimal(tot_proz2) + to_decimal(cl_list.proz2)
                    tot_yroom = tot_yroom + cl_list.yroom
                    tot_proz3 = tot_proz3 + cl_list.proz3
                    tot_dpax = tot_dpax + cl_list.dpax
                    tot_mpax = tot_mpax + cl_list.mpax
                    tot_ypax = tot_ypax + cl_list.ypax
                    tot_drate =  to_decimal(tot_drate) + to_decimal(cl_list.drate)
                    tot_mrate =  to_decimal(tot_mrate) + to_decimal(cl_list.mrate)
                    tot_yrate =  to_decimal(tot_yrate) + to_decimal(cl_list.yrate)
                    tot_drev =  to_decimal(tot_drev) + to_decimal(cl_list.drev)
                    tot_mrev =  to_decimal(tot_mrev) + to_decimal(cl_list.mrev)
                    tot_yrev =  to_decimal(tot_yrev) + to_decimal(cl_list.yrev)


                curr_grup = cl_list.segm_grup


            rm_statistic_list1 = Rm_statistic_list1()
            rm_statistic_list1_data.append(rm_statistic_list1)


            if long_digit:
                rm_statistic_list1.segm = to_string(cl_list.segm, ">>>")
                rm_statistic_list1.bezeich = cl_list.bezeich
                rm_statistic_list1.droom = to_string(cl_list.droom, ">>,>>9")
                rm_statistic_list1.proz1 = to_string(cl_list.proz1, ">>9.99")
                rm_statistic_list1.mroom = to_string(cl_list.mroom, ">>,>>9")
                rm_statistic_list1.proz2 = to_string(cl_list.proz2, ">>9.99")
                rm_statistic_list1.yroom = to_string(cl_list.yroom, ">>,>>9")
                rm_statistic_list1.proz3 = to_string(cl_list.proz3, ">>9.99")
                rm_statistic_list1.dpax = to_string(cl_list.dpax, ">>,>>9")
                rm_statistic_list1.mpax = to_string(cl_list.mpax, ">>,>>9")
                rm_statistic_list1.ypax = to_string(cl_list.ypax, ">>,>>9")
                rm_statistic_list1.drate = to_string(cl_list.drate, "->>,>>>,>>>,>>>,>>9")
                rm_statistic_list1.mrate = to_string(cl_list.mrate, "->>,>>>,>>>,>>>,>>9")
                rm_statistic_list1.yrate = to_string(cl_list.yrate, "->>,>>>,>>>,>>>,>>9")
                rm_statistic_list1.drev = to_string(cl_list.drev, "->>,>>>,>>>,>>>,>>9")
                rm_statistic_list1.mrev = to_string(cl_list.mrev, "->>,>>>,>>>,>>>,>>9")
                rm_statistic_list1.yrev = to_string(cl_list.yrev, "->>,>>>,>>>,>>>,>>9")
                rm_statistic_list1.segm_descr = cl_list.segm_descr


            else:
                rm_statistic_list1.segm = to_string(cl_list.segm, ">>>")
                rm_statistic_list1.bezeich = cl_list.bezeich
                rm_statistic_list1.droom = to_string(cl_list.droom, ">>,>>9")
                rm_statistic_list1.proz1 = to_string(cl_list.proz1, ">>9.99")
                rm_statistic_list1.mroom = to_string(cl_list.mroom, ">>,>>9")
                rm_statistic_list1.proz2 = to_string(cl_list.proz2, ">>9.99")
                rm_statistic_list1.yroom = to_string(cl_list.yroom, ">>,>>9")
                rm_statistic_list1.proz3 = to_string(cl_list.proz3, ">>9.99")
                rm_statistic_list1.dpax = to_string(cl_list.dpax, ">>,>>9")
                rm_statistic_list1.mpax = to_string(cl_list.mpax, ">>,>>9")
                rm_statistic_list1.ypax = to_string(cl_list.ypax, ">>,>>9")
                rm_statistic_list1.drate = to_string(cl_list.drate, "->>>,>>>,>>>,>>9.99")
                rm_statistic_list1.mrate = to_string(cl_list.mrate, "->>>,>>>,>>>,>>9.99")
                rm_statistic_list1.yrate = to_string(cl_list.yrate, "->>>,>>>,>>>,>>9.99")
                rm_statistic_list1.drev = to_string(cl_list.drev, "->>>,>>>,>>>,>>9.99")
                rm_statistic_list1.mrev = to_string(cl_list.mrev, "->>>,>>>,>>>,>>9.99")
                rm_statistic_list1.yrev = to_string(cl_list.yrev, "->>>,>>>,>>>,>>9.99")
                rm_statistic_list1.segm_descr = cl_list.segm_descr

            if show_other:

                other_list = query(other_list_data, filters=(lambda other_list: other_list.segm == cl_list.segm), first=True)

                if other_list:
                    ttrev =  to_decimal(cl_list.drev) + to_decimal(other_list.orev)
                    ttmrev =  to_decimal(cl_list.mrev) + to_decimal(other_list.morev)
                    ttyrev =  to_decimal(cl_list.yrev) + to_decimal(other_list.yorev)


                    rm_statistic_list1 = Rm_statistic_list1()
                    rm_statistic_list1_data.append(rm_statistic_list1)


                    if long_digit:
                        rm_statistic_list1.flag = "Orev"
                        rm_statistic_list1.bezeich = translateExtended ("Other Revenue", lvcarea, "")
                        rm_statistic_list1.drev = to_string(other_list.orev, "->>,>>>,>>>,>>>,>>9")
                        rm_statistic_list1.mrev = to_string(other_list.morev, "->>,>>>,>>>,>>>,>>9")
                        rm_statistic_list1.yrev = to_string(other_list.yorev, "->>,>>>,>>>,>>>,>>9")


                    else:
                        rm_statistic_list1.flag = "Orev"
                        rm_statistic_list1.bezeich = translateExtended ("Other Revenue", lvcarea, "")
                        rm_statistic_list1.drev = to_string(other_list.orev, "->>>,>>>,>>>,>>9.99")
                        rm_statistic_list1.mrev = to_string(other_list.morev, "->>>,>>>,>>>,>>9.99")
                        rm_statistic_list1.yrev = to_string(other_list.yorev, "->>>,>>>,>>>,>>9.99")


                    rm_statistic_list1 = Rm_statistic_list1()
                    rm_statistic_list1_data.append(rm_statistic_list1)


                    if long_digit:
                        rm_statistic_list1.flag = "Trev"
                        rm_statistic_list1.bezeich = translateExtended ("Total Revenue", lvcarea, "")
                        rm_statistic_list1.drev = to_string(ttrev, "->>,>>>,>>>,>>>,>>9")
                        rm_statistic_list1.mrev = to_string(ttmrev, "->>,>>>,>>>,>>>,>>9")
                        rm_statistic_list1.yrev = to_string(ttyrev, "->>,>>>,>>>,>>>,>>9")


                    else:
                        rm_statistic_list1.flag = "Trev"
                        rm_statistic_list1.bezeich = translateExtended ("Total Revenue", lvcarea, "")
                        rm_statistic_list1.drev = to_string(ttrev, "->>>,>>>,>>>,>>9.99")
                        rm_statistic_list1.mrev = to_string(ttmrev, "->>>,>>>,>>>,>>9.99")
                        rm_statistic_list1.yrev = to_string(ttyrev, "->>>,>>>,>>>,>>9.99")


                    rm_statistic_list1 = Rm_statistic_list1()
                    rm_statistic_list1_data.append(rm_statistic_list1)


        if grp_flag:
            rm_statistic_list1 = Rm_statistic_list1()
            rm_statistic_list1_data.append(rm_statistic_list1)

            rm_statistic_list1.segm = ""
            rm_statistic_list1.bezeich = "T O T A L"
            rm_statistic_list1.droom = to_string(tot_droom, ">>,>>9")
            rm_statistic_list1.proz1 = to_string(tot_proz1, ">>9.99")
            rm_statistic_list1.mroom = to_string(tot_mroom, ">>,>>9")
            rm_statistic_list1.proz2 = to_string(tot_proz2, ">>9.99")
            rm_statistic_list1.yroom = to_string(tot_yroom, ">>,>>9")
            rm_statistic_list1.proz3 = to_string(tot_proz3, ">>9.99")
            rm_statistic_list1.dpax = to_string(tot_dpax, ">>,>>9")
            rm_statistic_list1.mpax = to_string(tot_mpax, ">>,>>9")
            rm_statistic_list1.ypax = to_string(tot_ypax, ">>,>>9")
            rm_statistic_list1.drate = to_string(tot_drate, "->>>,>>>,>>>,>>9.99")
            rm_statistic_list1.mrate = to_string(tot_mrate, "->>>,>>>,>>>,>>9.99")
            rm_statistic_list1.yrate = to_string(tot_yrate, "->>>,>>>,>>>,>>9.99")
            rm_statistic_list1.drev = to_string(tot_drev, "->>>,>>>,>>>,>>9.99")
            rm_statistic_list1.mrev = to_string(tot_mrev, "->>>,>>>,>>>,>>9.99")
            rm_statistic_list1.yrev = to_string(tot_yrev, "->>>,>>>,>>>,>>9.99")
            rm_statistic_list1.segm_descr = ""


            rm_statistic_list1 = Rm_statistic_list1()
            rm_statistic_list1_data.append(rm_statistic_list1)


        if not show_ytd:
            rm_statistic_list = Rm_statistic_list()
            rm_statistic_list_data.append(rm_statistic_list)


            if long_digit:
                rm_statistic_list.segm = ""
                rm_statistic_list.bezeich = translateExtended ("Total Revenue Room", lvcarea, "")
                rm_statistic_list.dgroom = to_string(dgroom, ">>,>>9")
                rm_statistic_list.proz1 = to_string(100, ">>9.99")
                rm_statistic_list.mgroom = to_string(mgroom, ">>,>>9")
                rm_statistic_list.proz2 = to_string(100, ">>9.99")
                rm_statistic_list.dgpax = to_string(dgpax, ">>,>>9")
                rm_statistic_list.mgpax = to_string(mgpax, ">>,>>9")
                rm_statistic_list.dgrate = to_string(dgrate, "->>,>>>,>>>,>>>,>>9")
                rm_statistic_list.mgrate = to_string(mgrate, "->>,>>>,>>>,>>>,>>9")
                rm_statistic_list.dgrev = to_string(dgrev, "->>,>>>,>>>,>>>,>>9")
                rm_statistic_list.mgrev = to_string(mgrev, "->>,>>>,>>>,>>>,>>9")
                rm_statistic_list.segm_descr = ""


            else:
                rm_statistic_list.segm = ""
                rm_statistic_list.bezeich = translateExtended ("Total Revenue Room", lvcarea, "")
                rm_statistic_list.dgroom = to_string(dgroom, ">>,>>9")
                rm_statistic_list.proz1 = to_string(100, ">>9.99")
                rm_statistic_list.mgroom = to_string(mgroom, ">>,>>9")
                rm_statistic_list.proz2 = to_string(100, ">>9.99")
                rm_statistic_list.dgpax = to_string(dgpax, ">>,>>9")
                rm_statistic_list.mgpax = to_string(mgpax, ">>,>>9")
                rm_statistic_list.dgrate = to_string(dgrate, "->>>,>>>,>>>,>>9.99")
                rm_statistic_list.mgrate = to_string(mgrate, "->>>,>>>,>>>,>>9.99")
                rm_statistic_list.dgrev = to_string(dgrev, "->>>,>>>,>>>,>>9.99")
                rm_statistic_list.mgrev = to_string(mgrev, "->>>,>>>,>>>,>>9.99")
                rm_statistic_list.segm_descr = cl_list.segm_descr


        else:
            rm_statistic_list1 = Rm_statistic_list1()
            rm_statistic_list1_data.append(rm_statistic_list1)

            rm_statistic_list1 = Rm_statistic_list1()
            rm_statistic_list1_data.append(rm_statistic_list1)


            if long_digit:
                rm_statistic_list1.segm = ""
                rm_statistic_list1.bezeich = translateExtended ("Total Revenue Room", lvcarea, "")
                rm_statistic_list1.droom = to_string(dgroom, ">>,>>9")
                rm_statistic_list1.proz1 = to_string(100, ">>9.99")
                rm_statistic_list1.mroom = to_string(mgroom, ">>,>>9")
                rm_statistic_list1.proz2 = to_string(100, ">>9.99")
                rm_statistic_list1.yroom = to_string(ygroom, ">>,>>9")
                rm_statistic_list1.proz3 = to_string(100, ">>9.99")
                rm_statistic_list1.dpax = to_string(dgpax, ">>,>>9")
                rm_statistic_list1.mpax = to_string(mgpax, ">>,>>9")
                rm_statistic_list1.ypax = to_string(ygpax, ">>>,>>9")
                rm_statistic_list1.drate = to_string(dgrate, "->>,>>>,>>>,>>>,>>9")
                rm_statistic_list1.mrate = to_string(mgrate, "->>,>>>,>>>,>>>,>>9")
                rm_statistic_list1.yrate = to_string(ygrate, "->>,>>>,>>>,>>>,>>9")
                rm_statistic_list1.drev = to_string(dgrev, "->>,>>>,>>>,>>>,>>9")
                rm_statistic_list1.mrev = to_string(mgrev, "->>,>>>,>>>,>>>,>>9")
                rm_statistic_list1.yrev = to_string(ygrev, "->>,>>>,>>>,>>>,>>9")
                rm_statistic_list1.segm_descr = ""


            else:
                rm_statistic_list1.segm = ""
                rm_statistic_list1.bezeich = translateExtended ("Total Revenue Room", lvcarea, "")
                rm_statistic_list1.droom = to_string(dgroom, ">>,>>9")
                rm_statistic_list1.proz1 = to_string(100, ">>9.99")
                rm_statistic_list1.mroom = to_string(mgroom, ">>,>>9")
                rm_statistic_list1.proz2 = to_string(100, ">>9.99")
                rm_statistic_list1.yroom = to_string(ygroom, ">>,>>9")
                rm_statistic_list1.proz3 = to_string(100, ">>9.99")
                rm_statistic_list1.dpax = to_string(dgpax, ">>,>>9")
                rm_statistic_list1.mpax = to_string(mgpax, ">>,>>9")
                rm_statistic_list1.ypax = to_string(ygpax, ">>>,>>9")
                rm_statistic_list1.drate = to_string(dgrate, "->>>,>>>,>>>,>>9.99")
                rm_statistic_list1.mrate = to_string(mgrate, "->>>,>>>,>>>,>>9.99")
                rm_statistic_list1.yrate = to_string(ygrate, "->>>,>>>,>>>,>>9.99")
                rm_statistic_list1.drev = to_string(dgrev, "->>>,>>>,>>>,>>9.99")
                rm_statistic_list1.mrev = to_string(mgrev, "->>>,>>>,>>>,>>9.99")
                rm_statistic_list1.yrev = to_string(ygrev, "->>>,>>>,>>>,>>9.99")
                rm_statistic_list1.segm_descr = ""

        cl_list = query(cl_list_data, filters=(lambda cl_list: cl_list.flag_comp), first=True)

        if cl_list:
            rm_statistic_list1 = Rm_statistic_list1()
            rm_statistic_list1_data.append(rm_statistic_list1)

            rm_statistic_list1 = Rm_statistic_list1()
            rm_statistic_list1_data.append(rm_statistic_list1)

            rm_statistic_list1 = Rm_statistic_list1()
            rm_statistic_list1_data.append(rm_statistic_list1)

            rm_statistic_list1.bezeich = translateExtended ("Compliment Rooms", lvcarea, "")

            for cl_list in query(cl_list_data, filters=(lambda cl_list: cl_list.flag_comp)):
                rm_statistic_list1 = Rm_statistic_list1()
                rm_statistic_list1_data.append(rm_statistic_list1)

                rm_statistic_list1.segm = to_string(cl_list.segm, ">>9")
                rm_statistic_list1.bezeich = cl_list.bezeich
                rm_statistic_list1.droom = to_string(cl_list.droom, ">>,>>9")
                rm_statistic_list1.proz1 = ""
                rm_statistic_list1.mroom = to_string(cl_list.mroom, ">>,>>9")
                rm_statistic_list1.proz2 = ""
                rm_statistic_list1.yroom = to_string(cl_list.yroom, ">>,>>9")
                rm_statistic_list1.proz3 = ""
                rm_statistic_list1.dpax = to_string(cl_list.dpax, ">>,>>9")
                rm_statistic_list1.mpax = to_string(cl_list.mpax, ">>,>>9")
                rm_statistic_list1.ypax = to_string(cl_list.ypax, ">>,>>9")


                rm_statistic_list1.segm_descr = cl_list.segm_descr


    def create_umsatz():

        nonlocal rm_statistic_list_data, rm_statistic_list1_data, lnldelimeter, long_digit, droom, proz1, mroom, proz2, yroom, proz3, dpax, mpax, ypax, drate, mrate, yrate, drev, mrev, yrev, lodg, olodg, gproz1, mgroom, gproz2, ygroom, gproz3, dgpax, mgpax, ygpax, dgrate, mgrate, ygrate, dgrev, mgrev, ygrev, dgroom1, mgroom1, ygroom1, dgpax1, mgpax1, ygpax1, dgrate1, mgrate1, ygrate1, dgrev1, mgrev1, ygrev1, ttrev, ttmrev, ttyrev, from_date, period_str, comp_room, curr_grup, tot_droom, tot_proz1, tot_mroom, tot_proz2, tot_yroom, tot_proz3, tot_dpax, tot_mpax, tot_ypax, tot_drate, tot_mrate, tot_yrate, tot_drev, tot_mrev, tot_yrev, lvcarea, htparam, segment, zinrstat, genstat, queasy
        nonlocal pvilanguage, call_from, txt_file, to_date, grp_flag, show_ytd, show_other
        nonlocal r_list, r_list1


        nonlocal rm_statistic_list, rm_statistic_list1, cl_list, other_list, s_list, r_list, r_list1
        nonlocal rm_statistic_list_data, rm_statistic_list1_data, cl_list_data, other_list_data, s_list_data

        black_list:int = 0
        fl_comp:bool = False
        dgroom:int = 0
        i:int = 0
        flag_temp:bool = False

        htparam = get_cache (Htparam, {"paramnr": [(eq, 709)]})
        black_list = htparam.finteger
        rm_statistic_list_data.clear()
        rm_statistic_list1_data.clear()
        cl_list_data.clear()
        s_list_data.clear()
        droom = 0
        mroom = 0
        yroom = 0
        dpax = 0
        mpax = 0
        ypax = 0
        drate =  to_decimal("0")
        mrate =  to_decimal("0")
        yrate =  to_decimal("0")
        drev =  to_decimal("0")
        mrev =  to_decimal("0")
        yrev =  to_decimal("0")
        dgroom = 0
        mgroom = 0
        ygroom = 0
        dgpax = 0
        mgpax = 0
        ygpax = 0
        dgrate =  to_decimal("0")
        mgrate =  to_decimal("0")
        ygrate =  to_decimal("0")
        dgrev =  to_decimal("0")
        mgrev =  to_decimal("0")
        ygrev =  to_decimal("0")
        tot_droom = 0
        tot_proz1 =  to_decimal("0")
        tot_mroom = 0
        tot_proz2 =  to_decimal("0")
        tot_yroom = 0
        tot_proz3 = 0
        tot_dpax = 0
        tot_mpax = 0
        tot_ypax = 0
        tot_drate =  to_decimal("0")
        tot_mrate =  to_decimal("0")
        tot_yrate =  to_decimal("0")
        tot_drev =  to_decimal("0")
        tot_mrev =  to_decimal("0")
        tot_yrev =  to_decimal("0")


        from_date = date_mdy(get_month(to_date) , 1, get_year(to_date))

        if show_other:
            create_other()

        genstat_obj_list = {}
        genstat = Genstat()
        segment = Segment()
        for genstat.resstatus, genstat.gratis, genstat.segmentcode, genstat.logis, genstat.erwachs, genstat.kind1, genstat.kind2, genstat.kind3, genstat.zipreis, genstat.datum, genstat._recid, segment.segmentcode, segment.bezeich, segment.segmentgrup, segment._recid in db_session.query(Genstat.resstatus, Genstat.gratis, Genstat.segmentcode, Genstat.logis, Genstat.erwachs, Genstat.kind1, Genstat.kind2, Genstat.kind3, Genstat.zipreis, Genstat.datum, Genstat._recid, Segment.segmentcode, Segment.bezeich, Segment.segmentgrup, Segment._recid).join(Segment,(Segment.segmentcode == Genstat.segmentcode) & (Segment.segmentcode != black_list) & (Segment.segmentgrup <= 99)).filter(
                 (Genstat.datum >= from_date) & (Genstat.datum <= to_date) & (Genstat.segmentcode != 0) & (Genstat.nationnr != 0)).order_by(Genstat._recid).all():
            if genstat_obj_list.get(genstat._recid):
                continue
            else:
                genstat_obj_list[genstat._recid] = True

            if genstat.zipreis == 0 and genstat.resstatus == 6 and genstat.gratis != 0:
                fl_comp = True
            else:
                fl_comp = False

            cl_list = query(cl_list_data, filters=(lambda cl_list: cl_list.segm == genstat.segmentcode and cl_list.flag_comp == fl_comp), first=True)

            if not cl_list:
                cl_list = Cl_list()
                cl_list_data.append(cl_list)

                cl_list.segm = genstat.segmentcode
                cl_list.bezeich = segment.bezeich
                cl_list.flag_comp = fl_comp
                cl_list.segm_grup = segment.segmentgrup

                queasy = get_cache (Queasy, {"key": [(eq, 26)],"number1": [(eq, segment.segmentgrup)]})

                if queasy:
                    cl_list.segm_descr = queasy.char3

                if genstat.zipreis == 0 and genstat.resstatus == 6 and genstat.gratis != 0:

                    if genstat.datum == to_date:
                        cl_list.droom = 1
                        cl_list.dpax = cl_list.dpax + genstat.gratis
                        droom = droom + 1

                    if get_month(genstat.datum) == get_month(to_date):
                        cl_list.mroom = 1
                        cl_list.mpax = cl_list.mpax + genstat.gratis
                        mroom = mroom + 1

                elif genstat.resstatus != 13:

                    if genstat.datum == to_date:
                        cl_list.drev =  to_decimal(genstat.logis)
                        cl_list.droom = cl_list.droom + 1
                        cl_list.dpax = cl_list.dpax + genstat.erwachs +\
                                genstat.kind1 + genstat.kind2 + genstat.kind3
                        dgroom = dgroom + 1
                        dgpax = dgpax + genstat.erwachs +\
                                genstat.kind1 + genstat.kind2 + genstat.kind3
                        dgrev =  to_decimal(dgrev) + to_decimal(genstat.logis)
                        cl_list.drate =  to_decimal(cl_list.drate) + to_decimal((cl_list.drev) / to_decimal(cl_list.droom) )
                        dgrate =  to_decimal(dgrev) / to_decimal(dgroom)
                        droom = droom + 1

                    if get_month(genstat.datum) == get_month(to_date):
                        cl_list.mrev =  to_decimal(genstat.logis)
                        cl_list.mroom = cl_list.mroom + 1
                        cl_list.mpax = cl_list.mpax + genstat.erwachs +\
                                genstat.kind1 + genstat.kind2 + genstat.kind3
                        mgroom = mgroom + 1
                        mgpax = mgpax + genstat.erwachs + genstat.kind1 +\
                                genstat.kind2 + genstat.kind3
                        mgrev =  to_decimal(mgrev) + to_decimal(genstat.logis)
                        cl_list.mrate =  to_decimal(cl_list.mrate) + to_decimal((cl_list.mrev) / to_decimal(cl_list.mroom) )
                        mgrate =  to_decimal(mgrev) / to_decimal(mgroom)
                        mroom = mroom + 1


            else:

                if genstat.zipreis == 0 and genstat.resstatus == 6 and genstat.gratis != 0:

                    if genstat.datum == to_date:
                        cl_list.droom = cl_list.droom + 1
                        cl_list.dpax = cl_list.dpax + genstat.gratis
                        droom = droom + 1

                    if get_month(genstat.datum) == get_month(to_date):
                        cl_list.mroom = cl_list.mroom + 1
                        cl_list.mpax = cl_list.mpax + genstat.gratis
                        mroom = mroom + 1

                elif genstat.resstatus != 13:

                    if genstat.datum == to_date:
                        cl_list.drev =  to_decimal(cl_list.drev) + to_decimal(genstat.logis)
                        cl_list.droom = cl_list.droom + 1
                        cl_list.dpax = cl_list.dpax + genstat.erwachs +\
                                genstat.kind1 + genstat.kind2 + genstat.kind3
                        dgroom = dgroom + 1
                        dgpax = dgpax + genstat.erwachs +\
                                genstat.kind1 + genstat.kind2 + genstat.kind3
                        dgrev =  to_decimal(dgrev) + to_decimal(genstat.logis)
                        cl_list.drate =  to_decimal(cl_list.drev) / to_decimal(cl_list.droom)
                        dgrate =  to_decimal(dgrev) / to_decimal(dgroom)
                        droom = droom + 1

                    if get_month(genstat.datum) == get_month(to_date):
                        cl_list.mroom = cl_list.mroom + 1
                        cl_list.mpax = cl_list.mpax + genstat.erwachs + genstat.kind1 +\
                                genstat.kind2 + genstat.kind3
                        cl_list.mrev =  to_decimal(cl_list.mrev) + to_decimal(genstat.logis)
                        mgroom = mgroom + 1
                        mgpax = mgpax + genstat.erwachs + genstat.kind1 + genstat.kind2 + genstat.kind3
                        mgrev =  to_decimal(mgrev) + to_decimal(genstat.logis)
                        cl_list.mrate =  to_decimal(cl_list.mrev) / to_decimal(cl_list.mroom)
                        mgrate =  to_decimal(mgrev) / to_decimal(mgroom)
                        mroom = mroom + 1

        for cl_list in query(cl_list_data, filters=(lambda cl_list: not cl_list.flag_comp), sort_by=[("segm_grup",False)]):

            if cl_list.droom == 0:
                cl_list.dpax = 0

            if cl_list.mroom == 0:
                cl_list.mpax = 0

            if cl_list.yroom == 0:
                cl_list.ypax = 0

            if cl_list.droom != 0:
                cl_list.drate =  to_decimal(cl_list.drev) / to_decimal(cl_list.droom)

            if cl_list.mroom != 0:
                cl_list.mrate =  to_decimal(cl_list.mrev) / to_decimal(cl_list.mroom)

            if droom != 0:
                cl_list.proz1 =  to_decimal(100.0) * to_decimal(cl_list.droom) / to_decimal(dgroom)

            if mroom != 0:
                cl_list.proz2 =  to_decimal(100.0) * to_decimal(cl_list.mroom) / to_decimal(mgroom)

            if droom != 0:
                drate =  to_decimal(drev) / to_decimal(droom)

            if mroom != 0:
                mrate =  to_decimal(mrev) / to_decimal(mroom)

            if not show_ytd:

                if grp_flag and not cl_list.grpflag:

                    if cl_list.segm_grup != curr_grup and curr_grup != 0:
                        rm_statistic_list = Rm_statistic_list()
                        rm_statistic_list_data.append(rm_statistic_list)

                        rm_statistic_list.segm = ""
                        rm_statistic_list.bezeich = translateExtended ("T O T A L", lvcarea, "")
                        rm_statistic_list.dgroom = to_string(tot_droom, ">>,>>9")
                        rm_statistic_list.proz1 = to_string(tot_proz1, ">>9.99")
                        rm_statistic_list.mgroom = to_string(tot_mroom, ">>,>>9")
                        rm_statistic_list.proz2 = to_string(tot_proz2, ">>9.99")
                        rm_statistic_list.dgpax = to_string(tot_dpax, ">>,>>9")
                        rm_statistic_list.mgpax = to_string(tot_mpax, ">>,>>9")
                        rm_statistic_list.dgrate = to_string(tot_drate, "->>>,>>>,>>>,>>9.99")
                        rm_statistic_list.mgrate = to_string(tot_mrate, "->>>,>>>,>>>,>>9.99")
                        rm_statistic_list.dgrev = to_string(tot_drev, "->>>,>>>,>>>,>>9.99")
                        rm_statistic_list.mgrev = to_string(tot_mrev, "->>>,>>>,>>>,>>9.99")
                        rm_statistic_list.segm_descr = ""


                        rm_statistic_list = Rm_statistic_list()
                        rm_statistic_list_data.append(rm_statistic_list)

                        tot_droom = 0
                        tot_proz1 =  to_decimal("0")
                        tot_mroom = 0
                        tot_proz2 =  to_decimal("0")
                        tot_yroom = 0
                        tot_proz3 = 0
                        tot_dpax = 0
                        tot_mpax = 0
                        tot_ypax = 0
                        tot_drate =  to_decimal("0")
                        tot_mrate =  to_decimal("0")
                        tot_yrate =  to_decimal("0")
                        tot_drev =  to_decimal("0")
                        tot_mrev =  to_decimal("0")
                        tot_yrev =  to_decimal("0")
                        tot_droom = tot_droom + cl_list.droom
                        tot_proz1 =  to_decimal(tot_proz1) + to_decimal(cl_list.proz1)
                        tot_mroom = tot_mroom + cl_list.mroom
                        tot_proz2 =  to_decimal(tot_proz2) + to_decimal(cl_list.proz2)
                        tot_yroom = tot_yroom + cl_list.yroom
                        tot_proz3 = tot_proz3 + cl_list.proz3
                        tot_dpax = tot_dpax + cl_list.dpax
                        tot_mpax = tot_mpax + cl_list.mpax
                        tot_ypax = tot_ypax + cl_list.ypax
                        tot_drate =  to_decimal(tot_drate) + to_decimal(cl_list.drate)
                        tot_mrate =  to_decimal(tot_mrate) + to_decimal(cl_list.mrate)
                        tot_yrate =  to_decimal(tot_yrate) + to_decimal(cl_list.yrate)
                        tot_drev =  to_decimal(tot_drev) + to_decimal(cl_list.drev)
                        tot_mrev =  to_decimal(tot_mrev) + to_decimal(cl_list.mrev)
                        tot_yrev =  to_decimal(tot_yrev) + to_decimal(cl_list.yrev)


                    else:
                        tot_droom = tot_droom + cl_list.droom
                        tot_proz1 =  to_decimal(tot_proz1) + to_decimal(cl_list.proz1)
                        tot_mroom = tot_mroom + cl_list.mroom
                        tot_proz2 =  to_decimal(tot_proz2) + to_decimal(cl_list.proz2)
                        tot_yroom = tot_yroom + cl_list.yroom
                        tot_proz3 = tot_proz3 + cl_list.proz3
                        tot_dpax = tot_dpax + cl_list.dpax
                        tot_mpax = tot_mpax + cl_list.mpax
                        tot_ypax = tot_ypax + cl_list.ypax
                        tot_drate =  to_decimal(tot_drate) + to_decimal(cl_list.drate)
                        tot_mrate =  to_decimal(tot_mrate) + to_decimal(cl_list.mrate)
                        tot_yrate =  to_decimal(tot_yrate) + to_decimal(cl_list.yrate)
                        tot_drev =  to_decimal(tot_drev) + to_decimal(cl_list.drev)
                        tot_mrev =  to_decimal(tot_mrev) + to_decimal(cl_list.mrev)
                        tot_yrev =  to_decimal(tot_yrev) + to_decimal(cl_list.yrev)


                    curr_grup = cl_list.segm_grup


                rm_statistic_list = Rm_statistic_list()
                rm_statistic_list_data.append(rm_statistic_list)


                if long_digit:
                    rm_statistic_list.segm = to_string(cl_list.segm, ">>>")
                    rm_statistic_list.bezeich = cl_list.bezeich
                    rm_statistic_list.dgroom = to_string(cl_list.droom, ">>,>>9")
                    rm_statistic_list.proz1 = to_string(cl_list.proz1, ">>9.99")
                    rm_statistic_list.mgroom = to_string(cl_list.mroom, ">>,>>9")
                    rm_statistic_list.proz2 = to_string(cl_list.proz2, ">>9.99")
                    rm_statistic_list.dgpax = to_string(cl_list.dpax, ">>,>>9")
                    rm_statistic_list.mgpax = to_string(cl_list.mpax, ">>,>>9")
                    rm_statistic_list.dgrate = to_string(cl_list.drate, "->>,>>>,>>>,>>>,>>9")
                    rm_statistic_list.mgrate = to_string(cl_list.mrate, "->>,>>>,>>>,>>>,>>9")
                    rm_statistic_list.dgrev = to_string(cl_list.drev, "->>,>>>,>>>,>>>,>>9")
                    rm_statistic_list.mgrev = to_string(cl_list.mrev, "->>,>>>,>>>,>>>,>>9")
                    rm_statistic_list.segm_descr = cl_list.segm_descr


                else:
                    rm_statistic_list.segm = to_string(cl_list.segm, ">>>")
                    rm_statistic_list.bezeich = cl_list.bezeich
                    rm_statistic_list.dgroom = to_string(cl_list.droom, ">>,>>9")
                    rm_statistic_list.proz1 = to_string(cl_list.proz1, ">>9.99")
                    rm_statistic_list.mgroom = to_string(cl_list.mroom, ">>,>>9")
                    rm_statistic_list.proz2 = to_string(cl_list.proz2, ">>9.99")
                    rm_statistic_list.dgpax = to_string(cl_list.dpax, ">>,>>9")
                    rm_statistic_list.mgpax = to_string(cl_list.mpax, ">>,>>9")
                    rm_statistic_list.dgrate = to_string(cl_list.drate, "->>>,>>>,>>>,>>9.99")
                    rm_statistic_list.mgrate = to_string(cl_list.mrate, "->>>,>>>,>>>,>>9.99")
                    rm_statistic_list.dgrev = to_string(cl_list.drev, "->>>,>>>,>>>,>>9.99")
                    rm_statistic_list.mgrev = to_string(cl_list.mrev, "->>>,>>>,>>>,>>9.99")
                    rm_statistic_list.segm_descr = cl_list.segm_descr

                if cl_list.grpflag:
                    rm_statistic_list = Rm_statistic_list()
                    rm_statistic_list_data.append(rm_statistic_list)

            else:

                if grp_flag and not cl_list.grpflag:

                    if cl_list.segm_grup != curr_grup and curr_grup != 0:
                        rm_statistic_list = Rm_statistic_list()
                        rm_statistic_list_data.append(rm_statistic_list)

                        rm_statistic_list.segm = ""
                        rm_statistic_list.bezeich = translateExtended ("T O T A L", lvcarea, "")
                        rm_statistic_list.dgroom = to_string(tot_droom, ">>,>>9")
                        rm_statistic_list.proz1 = to_string(tot_proz1, ">>9.99")
                        rm_statistic_list.mgroom = to_string(tot_mroom, ">>,>>9")
                        rm_statistic_list.proz2 = to_string(tot_proz2, ">>9.99")
                        rm_statistic_list.ygroom = to_string(tot_yroom, ">>,>>9")
                        rm_statistic_list.proz3 = to_string(tot_proz3, ">>9.99")
                        rm_statistic_list.dgpax = to_string(tot_dpax, ">>,>>9")
                        rm_statistic_list.mgpax = to_string(tot_mpax, ">>,>>9")
                        rm_statistic_list.ygpax = to_string(tot_ypax, ">>,>>9")
                        rm_statistic_list.dgrate = to_string(tot_drate, "->>>,>>>,>>>,>>9.99")
                        rm_statistic_list.mgrate = to_string(tot_mrate, "->>>,>>>,>>>,>>9.99")
                        rm_statistic_list.ygrate = to_string(tot_yrate, "->>>,>>>,>>>,>>9.99")
                        rm_statistic_list.dgrev = to_string(tot_drev, "->>>,>>>,>>>,>>9.99")
                        rm_statistic_list.mgrev = to_string(tot_mrev, "->>>,>>>,>>>,>>9.99")
                        rm_statistic_list.ygrev = to_string(tot_yrev, "->>>,>>>,>>>,>>9.99")
                        rm_statistic_list.segm_descr = ""


                        rm_statistic_list = Rm_statistic_list()
                        rm_statistic_list_data.append(rm_statistic_list)

                        tot_droom = 0
                        tot_proz1 =  to_decimal("0")
                        tot_mroom = 0
                        tot_proz2 =  to_decimal("0")
                        tot_yroom = 0
                        tot_proz3 = 0
                        tot_dpax = 0
                        tot_mpax = 0
                        tot_ypax = 0
                        tot_drate =  to_decimal("0")
                        tot_mrate =  to_decimal("0")
                        tot_yrate =  to_decimal("0")
                        tot_drev =  to_decimal("0")
                        tot_mrev =  to_decimal("0")
                        tot_yrev =  to_decimal("0")
                        tot_droom = tot_droom + cl_list.droom
                        tot_proz1 =  to_decimal(tot_proz1) + to_decimal(cl_list.proz1)
                        tot_mroom = tot_mroom + cl_list.mroom
                        tot_proz2 =  to_decimal(tot_proz2) + to_decimal(cl_list.proz2)
                        tot_yroom = tot_yroom + cl_list.yroom
                        tot_proz3 = tot_proz3 + cl_list.proz3
                        tot_dpax = tot_dpax + cl_list.dpax
                        tot_mpax = tot_mpax + cl_list.mpax
                        tot_ypax = tot_ypax + cl_list.ypax
                        tot_drate =  to_decimal(tot_drate) + to_decimal(cl_list.drate)
                        tot_mrate =  to_decimal(tot_mrate) + to_decimal(cl_list.mrate)
                        tot_yrate =  to_decimal(tot_yrate) + to_decimal(cl_list.yrate)
                        tot_drev =  to_decimal(tot_drev) + to_decimal(cl_list.drev)
                        tot_mrev =  to_decimal(tot_mrev) + to_decimal(cl_list.mrev)
                        tot_yrev =  to_decimal(tot_yrev) + to_decimal(cl_list.yrev)


                    else:
                        tot_droom = tot_droom + cl_list.droom
                        tot_proz1 =  to_decimal(tot_proz1) + to_decimal(cl_list.proz1)
                        tot_mroom = tot_mroom + cl_list.mroom
                        tot_proz2 =  to_decimal(tot_proz2) + to_decimal(cl_list.proz2)
                        tot_yroom = tot_yroom + cl_list.yroom
                        tot_proz3 = tot_proz3 + cl_list.proz3
                        tot_dpax = tot_dpax + cl_list.dpax
                        tot_mpax = tot_mpax + cl_list.mpax
                        tot_ypax = tot_ypax + cl_list.ypax
                        tot_drate =  to_decimal(tot_drate) + to_decimal(cl_list.drate)
                        tot_mrate =  to_decimal(tot_mrate) + to_decimal(cl_list.mrate)
                        tot_yrate =  to_decimal(tot_yrate) + to_decimal(cl_list.yrate)
                        tot_drev =  to_decimal(tot_drev) + to_decimal(cl_list.drev)
                        tot_mrev =  to_decimal(tot_mrev) + to_decimal(cl_list.mrev)
                        tot_yrev =  to_decimal(tot_yrev) + to_decimal(cl_list.yrev)


                    curr_grup = cl_list.segm_grup


                rm_statistic_list1 = Rm_statistic_list1()
                rm_statistic_list1_data.append(rm_statistic_list1)


                if long_digit:
                    rm_statistic_list1.segm = to_string(cl_list.segm, ">>>")
                    rm_statistic_list1.bezeich = cl_list.bezeich
                    rm_statistic_list1.droom = to_string(cl_list.droom, ">>,>>9")
                    rm_statistic_list1.proz1 = to_string(cl_list.proz1, ">>9.99")
                    rm_statistic_list1.mroom = to_string(cl_list.mroom, ">>,>>9")
                    rm_statistic_list1.proz2 = to_string(cl_list.proz2, ">>9.99")
                    rm_statistic_list1.yroom = to_string(cl_list.yroom, ">>,>>9")
                    rm_statistic_list1.proz3 = to_string(cl_list.proz3, ">>9.99")
                    rm_statistic_list1.dpax = to_string(cl_list.dpax, ">>,>>9")
                    rm_statistic_list1.mpax = to_string(cl_list.mpax, ">>,>>9")
                    rm_statistic_list1.ypax = to_string(cl_list.ypax, ">>,>>9")
                    rm_statistic_list1.drate = to_string(cl_list.drate, "->>,>>>,>>>,>>>,>>9")
                    rm_statistic_list1.mrate = to_string(cl_list.mrate, "->>,>>>,>>>,>>>,>>9")
                    rm_statistic_list1.yrate = to_string(cl_list.yrate, "->>,>>>,>>>,>>>,>>9")
                    rm_statistic_list1.drev = to_string(cl_list.drev, "->>,>>>,>>>,>>>,>>9")
                    rm_statistic_list1.mrev = to_string(cl_list.mrev, "->>,>>>,>>>,>>>,>>9")
                    rm_statistic_list1.yrev = to_string(cl_list.yrev, "->>,>>>,>>>,>>>,>>9")
                    rm_statistic_list1.segm_descr = cl_list.segm_descr


                else:
                    rm_statistic_list1.segm = to_string(cl_list.segm, ">>>")
                    rm_statistic_list1.bezeich = cl_list.bezeich
                    rm_statistic_list1.droom = to_string(cl_list.droom, ">>,>>9")
                    rm_statistic_list1.proz1 = to_string(cl_list.proz1, ">>9.99")
                    rm_statistic_list1.mroom = to_string(cl_list.mroom, ">>,>>9")
                    rm_statistic_list1.proz2 = to_string(cl_list.proz2, ">>9.99")
                    rm_statistic_list1.yroom = to_string(cl_list.yroom, ">>,>>9")
                    rm_statistic_list1.proz3 = to_string(cl_list.proz3, ">>9.99")
                    rm_statistic_list1.dpax = to_string(cl_list.dpax, ">>,>>9")
                    rm_statistic_list1.mpax = to_string(cl_list.mpax, ">>,>>9")
                    rm_statistic_list1.ypax = to_string(cl_list.ypax, ">>,>>9")
                    rm_statistic_list1.drate = to_string(cl_list.drate, "->>>,>>>,>>>,>>9.99")
                    rm_statistic_list1.mrate = to_string(cl_list.mrate, "->>>,>>>,>>>,>>9.99")
                    rm_statistic_list1.yrate = to_string(cl_list.yrate, "->>>,>>>,>>>,>>9.99")
                    rm_statistic_list1.drev = to_string(cl_list.drev, "->>>,>>>,>>>,>>9.99")
                    rm_statistic_list1.mrev = to_string(cl_list.mrev, "->>>,>>>,>>>,>>9.99")
                    rm_statistic_list1.yrev = to_string(cl_list.yrev, "->>>,>>>,>>>,>>9.99")
                    rm_statistic_list1.segm_descr = cl_list.segm_descr

                if show_other:

                    other_list = query(other_list_data, filters=(lambda other_list: other_list.segm == cl_list.segm), first=True)

                    if other_list:
                        ttrev =  to_decimal(cl_list.drev) + to_decimal(other_list.orev)
                        ttmrev =  to_decimal(cl_list.mrev) + to_decimal(other_list.morev)
                        ttyrev =  to_decimal(cl_list.yrev) + to_decimal(other_list.yorev)


                        rm_statistic_list1 = Rm_statistic_list1()
                        rm_statistic_list1_data.append(rm_statistic_list1)


                        if long_digit:
                            rm_statistic_list1.flag = "Orev"
                            rm_statistic_list1.bezeich = translateExtended ("Other Revenue", lvcarea, "")
                            rm_statistic_list1.drev = to_string(other_list.orev, "->>,>>>,>>>,>>>,>>9")
                            rm_statistic_list1.mrev = to_string(other_list.morev, "->>,>>>,>>>,>>>,>>9")
                            rm_statistic_list1.yrev = to_string(other_list.yorev, "->>,>>>,>>>,>>>,>>9")


                        else:
                            rm_statistic_list1.flag = "Orev"
                            rm_statistic_list1.bezeich = translateExtended ("Other Revenue", lvcarea, "")
                            rm_statistic_list1.drev = to_string(other_list.orev, "->>>,>>>,>>>,>>9.99")
                            rm_statistic_list1.mrev = to_string(other_list.morev, "->>>,>>>,>>>,>>9.99")
                            rm_statistic_list1.yrev = to_string(other_list.yorev, "->>>,>>>,>>>,>>9.99")


                        rm_statistic_list1 = Rm_statistic_list1()
                        rm_statistic_list1_data.append(rm_statistic_list1)


                        if long_digit:
                            rm_statistic_list1.flag = "Trev"
                            rm_statistic_list1.bezeich = translateExtended ("Total Revenue", lvcarea, "")
                            rm_statistic_list1.drev = to_string(ttrev, "->>,>>>,>>>,>>>,>>9")
                            rm_statistic_list1.mrev = to_string(ttmrev, "->>,>>>,>>>,>>>,>>9")
                            rm_statistic_list1.yrev = to_string(ttyrev, "->>,>>>,>>>,>>>,>>9")


                        else:
                            rm_statistic_list1.flag = "Trev"
                            rm_statistic_list1.bezeich = translateExtended ("Total Revenue", lvcarea, "")
                            rm_statistic_list1.drev = to_string(ttrev, "->>>,>>>,>>>,>>9.99")
                            rm_statistic_list1.mrev = to_string(ttmrev, "->>>,>>>,>>>,>>9.99")
                            rm_statistic_list1.yrev = to_string(ttyrev, "->>>,>>>,>>>,>>9.99")


                        rm_statistic_list1 = Rm_statistic_list1()
                        rm_statistic_list1_data.append(rm_statistic_list1)


        if grp_flag:
            rm_statistic_list = Rm_statistic_list()
            rm_statistic_list_data.append(rm_statistic_list)


            if not show_ytd:
                rm_statistic_list.segm = ""
                rm_statistic_list.bezeich = translateExtended ("T O T A L", lvcarea, "")
                rm_statistic_list.dgroom = to_string(tot_droom, ">>,>>9")
                rm_statistic_list.proz1 = to_string(tot_proz1, ">>9.99")
                rm_statistic_list.mgroom = to_string(tot_mroom, ">>,>>9")
                rm_statistic_list.proz2 = to_string(tot_proz2, ">>9.99")
                rm_statistic_list.dgpax = to_string(tot_dpax, ">>,>>9")
                rm_statistic_list.mgpax = to_string(tot_mpax, ">>,>>9")
                rm_statistic_list.dgrate = to_string(tot_drate, "->>>,>>>,>>>,>>9.99")
                rm_statistic_list.mgrate = to_string(tot_mrate, "->>>,>>>,>>>,>>9.99")
                rm_statistic_list.dgrev = to_string(tot_drev, "->>>,>>>,>>>,>>9.99")
                rm_statistic_list.mgrev = to_string(tot_mrev, "->>>,>>>,>>>,>>9.99")
                rm_statistic_list.segm_descr = ""


                rm_statistic_list = Rm_statistic_list()
                rm_statistic_list_data.append(rm_statistic_list)


            elif show_ytd:
                rm_statistic_list.segm = ""
                rm_statistic_list.bezeich = translateExtended ("T O T A L", lvcarea, "")
                rm_statistic_list.dgroom = to_string(tot_droom, ">>9")
                rm_statistic_list.proz1 = to_string(tot_proz1, ">>9.99")
                rm_statistic_list.mgroom = to_string(tot_mroom, ">,>>9")
                rm_statistic_list.proz2 = to_string(tot_proz2, ">>9.99")
                rm_statistic_list.ygroom = to_string(tot_yroom, ">>,>>9")
                rm_statistic_list.proz3 = to_string(tot_proz3, ">>9.99")
                rm_statistic_list.dgpax = to_string(tot_dpax, ">>9")
                rm_statistic_list.mgpax = to_string(tot_mpax, ">>,>>9")
                rm_statistic_list.ygpax = to_string(tot_ypax, ">>,>>9")
                rm_statistic_list.dgrate = to_string(tot_drate, "->>>,>>>,>>9.99")
                rm_statistic_list.mgrate = to_string(tot_mrate, "->>>,>>>,>>9.99")
                rm_statistic_list.ygrate = to_string(tot_yrate, "->>>,>>>,>>9.99")
                rm_statistic_list.dgrev = to_string(tot_drev, "->>,>>>,>>>,>>9.99")
                rm_statistic_list.mgrev = to_string(tot_mrev, "->>>,>>>,>>>,>>9.99")
                rm_statistic_list.ygrev = to_string(tot_yrev, "->>>,>>>,>>>,>>9.99")
                rm_statistic_list.segm_descr = ""


                rm_statistic_list = Rm_statistic_list()
                rm_statistic_list_data.append(rm_statistic_list)


        if not show_ytd:
            rm_statistic_list = Rm_statistic_list()
            rm_statistic_list_data.append(rm_statistic_list)

            rm_statistic_list = Rm_statistic_list()
            rm_statistic_list_data.append(rm_statistic_list)


            if long_digit:
                rm_statistic_list.segm = ""
                rm_statistic_list.bezeich = translateExtended ("Total Revenue Room", lvcarea, "")
                rm_statistic_list.dgroom = to_string(dgroom, ">>,>>9")
                rm_statistic_list.proz1 = to_string(100, ">>9.99")
                rm_statistic_list.mgroom = to_string(mgroom, ">>,>>9")
                rm_statistic_list.proz2 = to_string(100, ">>9.99")
                rm_statistic_list.dgpax = to_string(dgpax, ">>,>>9")
                rm_statistic_list.mgpax = to_string(mgpax, ">>,>>9")
                rm_statistic_list.dgrate = to_string(dgrate, "->>,>>>,>>>,>>>,>>9")
                rm_statistic_list.mgrate = to_string(mgrate, "->>,>>>,>>>,>>>,>>9")
                rm_statistic_list.dgrev = to_string(dgrev, "->>,>>>,>>>,>>>,>>9")
                rm_statistic_list.mgrev = to_string(mgrev, "->>,>>>,>>>,>>>,>>9")
                rm_statistic_list.segm_descr = ""


            else:
                rm_statistic_list.segm = ""
                rm_statistic_list.bezeich = translateExtended ("Total Revenue Room", lvcarea, "")
                rm_statistic_list.dgroom = to_string(dgroom, ">>,>>9")
                rm_statistic_list.proz1 = to_string(100, ">>9.99")
                rm_statistic_list.mgroom = to_string(mgroom, ">>,>>9")
                rm_statistic_list.proz2 = to_string(100, ">>9.99")
                rm_statistic_list.dgpax = to_string(dgpax, ">>,>>9")
                rm_statistic_list.mgpax = to_string(mgpax, ">>,>>9")
                rm_statistic_list.dgrate = to_string(dgrate, "->>>,>>>,>>>,>>9.99")
                rm_statistic_list.mgrate = to_string(mgrate, "->>>,>>>,>>>,>>9.99")
                rm_statistic_list.dgrev = to_string(dgrev, "->>>,>>>,>>>,>>9.99")
                rm_statistic_list.mgrev = to_string(mgrev, "->>>,>>>,>>>,>>9.99")
                rm_statistic_list.segm_descr = ""

        cl_list = query(cl_list_data, filters=(lambda cl_list: cl_list.flag_comp), first=True)

        if cl_list:
            rm_statistic_list = Rm_statistic_list()
            rm_statistic_list_data.append(rm_statistic_list)

            rm_statistic_list = Rm_statistic_list()
            rm_statistic_list_data.append(rm_statistic_list)

            rm_statistic_list = Rm_statistic_list()
            rm_statistic_list_data.append(rm_statistic_list)

            rm_statistic_list.bezeich = translateExtended ("Compliment Rooms", lvcarea, "")

            for cl_list in query(cl_list_data, filters=(lambda cl_list: cl_list.flag_comp), sort_by=[("segm",False)]):
                rm_statistic_list = Rm_statistic_list()
                rm_statistic_list_data.append(rm_statistic_list)

                rm_statistic_list.segm = to_string(cl_list.segm, ">>9")
                rm_statistic_list.bezeich = cl_list.bezeich
                rm_statistic_list.dgroom = to_string(cl_list.droom, ">>,>>9")
                rm_statistic_list.proz1 = ""
                rm_statistic_list.mgroom = to_string(cl_list.mroom, ">>,>>9")
                rm_statistic_list.proz2 = ""
                rm_statistic_list.dgpax = to_string(cl_list.dpax, ">>,>>9")
                rm_statistic_list.mgpax = to_string(cl_list.mpax, ">>,>>9")
                rm_statistic_list.segm_descr = cl_list.segm_descr


    htparam = get_cache (Htparam, {"paramnr": [(eq, 246)]})
    long_digit = htparam.flogical
    comp_room = translateExtended ("Compliment Rooms" , lvcarea, "")

    if show_ytd:
        create_umsatz2()
    else:
        create_umsatz()

    return generate_output()