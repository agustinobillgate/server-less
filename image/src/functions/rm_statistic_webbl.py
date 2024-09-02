from functions.additional_functions import *
import decimal
from datetime import date
from sqlalchemy import func
from models import Htparam, Segment, Zinrstat, Genstat

def rm_statistic_webbl(pvilanguage:int, call_from:int, txt_file:str, to_date:date, grp_flag:bool, show_ytd:bool, show_other:bool):
    rm_statistic_list_list = []
    rm_statistic_list1_list = []
    lnldelimeter:str = ""
    long_digit:bool = False
    droom:int = 0
    proz1:decimal = 0
    mroom:int = 0
    proz2:int = 0
    yroom:int = 0
    proz3:int = 0
    dpax:int = 0
    mpax:int = 0
    ypax:int = 0
    drate:decimal = 0
    mrate:decimal = 0
    yrate:decimal = 0
    drev:decimal = 0
    mrev:decimal = 0
    yrev:decimal = 0
    lodg:decimal = 0
    olodg:decimal = 0
    dgroom:int = 0
    gproz1:decimal = 0
    mgroom:int = 0
    gproz2:int = 0
    ygroom:int = 0
    gproz3:int = 0
    dgpax:int = 0
    mgpax:int = 0
    ygpax:int = 0
    dgrate:decimal = 0
    mgrate:decimal = 0
    ygrate:decimal = 0
    dgrev:decimal = 0
    mgrev:decimal = 0
    ygrev:decimal = 0
    dgroom1:int = 0
    mgroom1:int = 0
    ygroom1:int = 0
    dgpax1:int = 0
    mgpax1:int = 0
    ygpax1:int = 0
    dgrate1:decimal = 0
    mgrate1:decimal = 0
    ygrate1:decimal = 0
    dgrev1:decimal = 0
    mgrev1:decimal = 0
    ygrev1:decimal = 0
    ttrev:decimal = 0
    ttmrev:decimal = 0
    ttyrev:decimal = 0
    from_date:date = None
    period_str:str = ""
    comp_room:str = ""
    curr_grup:int = 0
    tot_droom:int = 0
    tot_proz1:int = 0
    tot_mroom:int = 0
    tot_proz2:int = 0
    tot_yroom:int = 0
    tot_proz3:int = 0
    tot_dpax:int = 0
    tot_mpax:int = 0
    tot_ypax:int = 0
    tot_drate:decimal = 0
    tot_mrate:decimal = 0
    tot_yrate:decimal = 0
    tot_drev:decimal = 0
    tot_mrev:decimal = 0
    tot_yrev:decimal = 0
    lvcarea:str = "rm_statistic_web"
    htparam = segment = zinrstat = genstat = None

    rm_statistic_list = rm_statistic_list1 = cl_list = other_list = s_list = r_list = r_list1 = None

    rm_statistic_list_list, Rm_statistic_list = create_model("Rm_statistic_list", {"grpflag":bool, "flag":str, "segm":str, "bezeich":str, "dgroom":str, "proz1":str, "mgroom":str, "proz2":str, "ygroom":str, "proz3":str, "dgpax":str, "mgpax":str, "ygpax":str, "dgrate":str, "mgrate":str, "ygrate":str, "dgrev":str, "mgrev":str, "ygrev":str})
    rm_statistic_list1_list, Rm_statistic_list1 = create_model("Rm_statistic_list1", {"grpflag":bool, "flag":str, "segm":str, "bezeich":str, "droom":str, "proz1":str, "mroom":str, "proz2":str, "yroom":str, "proz3":str, "dpax":str, "mpax":str, "ypax":str, "drate":str, "mrate":str, "yrate":str, "drev":str, "mrev":str, "yrev":str})
    cl_list_list, Cl_list = create_model("Cl_list", {"grpflag":bool, "flag":str, "segm":int, "bezeich":str, "droom":int, "tot_droom":int, "proz1":decimal, "mroom":int, "proz2":decimal, "yroom":int, "proz3":decimal, "dpax":int, "tot_dpax":int, "mpax":int, "ypax":int, "drate":decimal, "mrate":decimal, "yrate":decimal, "drev":decimal, "mrev":decimal, "yrev":decimal, "orev":decimal, "flag_comp":bool, "flag_temp":bool, "segm_grup":int})
    other_list_list, Other_list = create_model("Other_list", {"flag":str, "segm":int, "bezeich":str, "orev":decimal, "morev":decimal, "yorev":decimal})
    s_list_list, S_list = create_model("S_list", {"nr":int, "bezeich":str, "droom":int, "mroom":int, "yroom":int, "dpax":int, "mpax":int, "ypax":int})

    R_list = Rm_statistic_list
    r_list_list = rm_statistic_list_list

    R_list1 = Rm_statistic_list1
    r_list1_list = rm_statistic_list1_list


    db_session = local_storage.db_session

    def generate_output():
        nonlocal rm_statistic_list_list, rm_statistic_list1_list, lnldelimeter, long_digit, droom, proz1, mroom, proz2, yroom, proz3, dpax, mpax, ypax, drate, mrate, yrate, drev, mrev, yrev, lodg, olodg, dgroom, gproz1, mgroom, gproz2, ygroom, gproz3, dgpax, mgpax, ygpax, dgrate, mgrate, ygrate, dgrev, mgrev, ygrev, dgroom1, mgroom1, ygroom1, dgpax1, mgpax1, ygpax1, dgrate1, mgrate1, ygrate1, dgrev1, mgrev1, ygrev1, ttrev, ttmrev, ttyrev, from_date, period_str, comp_room, curr_grup, tot_droom, tot_proz1, tot_mroom, tot_proz2, tot_yroom, tot_proz3, tot_dpax, tot_mpax, tot_ypax, tot_drate, tot_mrate, tot_yrate, tot_drev, tot_mrev, tot_yrev, lvcarea, htparam, segment, zinrstat, genstat
        nonlocal r_list, r_list1


        nonlocal rm_statistic_list, rm_statistic_list1, cl_list, other_list, s_list, r_list, r_list1
        nonlocal rm_statistic_list_list, rm_statistic_list1_list, cl_list_list, other_list_list, s_list_list
        return {"rm-statistic-list": rm_statistic_list_list, "rm-statistic-list1": rm_statistic_list1_list}

    def create_other():

        nonlocal rm_statistic_list_list, rm_statistic_list1_list, lnldelimeter, long_digit, droom, proz1, mroom, proz2, yroom, proz3, dpax, mpax, ypax, drate, mrate, yrate, drev, mrev, yrev, lodg, olodg, dgroom, gproz1, mgroom, gproz2, ygroom, gproz3, dgpax, mgpax, ygpax, dgrate, mgrate, ygrate, dgrev, mgrev, ygrev, dgroom1, mgroom1, ygroom1, dgpax1, mgpax1, ygpax1, dgrate1, mgrate1, ygrate1, dgrev1, mgrev1, ygrev1, ttrev, ttmrev, ttyrev, from_date, period_str, comp_room, curr_grup, tot_droom, tot_proz1, tot_mroom, tot_proz2, tot_yroom, tot_proz3, tot_dpax, tot_mpax, tot_ypax, tot_drate, tot_mrate, tot_yrate, tot_drev, tot_mrev, tot_yrev, lvcarea, htparam, segment, zinrstat, genstat
        nonlocal r_list, r_list1


        nonlocal rm_statistic_list, rm_statistic_list1, cl_list, other_list, s_list, r_list, r_list1
        nonlocal rm_statistic_list_list, rm_statistic_list1_list, cl_list_list, other_list_list, s_list_list

        black_list:int = 0

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 709)).first()
        black_list = htparam.finteger
        other_list_list.clear()

        zinrstat_obj_list = []
        for zinrstat, segment in db_session.query(Zinrstat, Segment).join(Segment,(Segment.segmentcode == Zinrstat.betriebsnr) &  (Segmentcode != black_list) &  (Segmentgrup <= 99)).filter(
                (Zinrstat.datum >= from_date) &  (Zinrstat.datum <= to_date) &  (func.lower(Zinrstat.zinr) == "SEGM")).all():
            if zinrstat._recid in zinrstat_obj_list:
                continue
            else:
                zinrstat_obj_list.append(zinrstat._recid)

            other_list = query(other_list_list, filters=(lambda other_list :other_list.segm == segmentcode), first=True)

            if not other_list:
                other_list = Other_list()
                other_list_list.append(other_list)

                other_list.segm = segmentcode

            if zinrstat.datum == to_date:
                other_list.orev = zinrstat.logisumsatz

            if get_month(zinrstat.datum) == get_month(to_date):
                other_list.morev = other_list.morev + zinrstat.logisumsatz

            if show_ytd:
                other_list.yorev = other_list.yorev + zinrstat.logisumsatz

    def create_umsatz2():

        nonlocal rm_statistic_list_list, rm_statistic_list1_list, lnldelimeter, long_digit, droom, proz1, mroom, proz2, yroom, proz3, dpax, mpax, ypax, drate, mrate, yrate, drev, mrev, yrev, lodg, olodg, dgroom, gproz1, mgroom, gproz2, ygroom, gproz3, dgpax, mgpax, ygpax, dgrate, mgrate, ygrate, dgrev, mgrev, ygrev, dgroom1, mgroom1, ygroom1, dgpax1, mgpax1, ygpax1, dgrate1, mgrate1, ygrate1, dgrev1, mgrev1, ygrev1, ttrev, ttmrev, ttyrev, from_date, period_str, comp_room, curr_grup, tot_droom, tot_proz1, tot_mroom, tot_proz2, tot_yroom, tot_proz3, tot_dpax, tot_mpax, tot_ypax, tot_drate, tot_mrate, tot_yrate, tot_drev, tot_mrev, tot_yrev, lvcarea, htparam, segment, zinrstat, genstat
        nonlocal r_list, r_list1


        nonlocal rm_statistic_list, rm_statistic_list1, cl_list, other_list, s_list, r_list, r_list1
        nonlocal rm_statistic_list_list, rm_statistic_list1_list, cl_list_list, other_list_list, s_list_list

        black_list:int = 0
        fl_comp:bool = False
        i:int = 0
        curr_grp:int = -1
        curr_segm:int = 0
        aa:int = 0
        xx:int = 0
        tot_slist_dpax:decimal = 0
        flag_temp:bool = False

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 709)).first()
        black_list = htparam.finteger
        rm_statistic_list_list.clear()
        rm_statistic_list1_list.clear()
        cl_list_list.clear()
        s_list_list.clear()
        droom = 0
        mroom = 0
        yroom = 0
        dpax = 0
        mpax = 0
        ypax = 0
        drate = 0
        mrate = 0
        yrate = 0
        drev = 0
        mrev = 0
        yrev = 0
        dgroom = 0
        mgroom = 0
        ygroom = 0
        dgpax = 0
        mgpax = 0
        ygpax = 0
        dgrate = 0
        mgrate = 0
        ygrate = 0
        dgrev = 0
        mgrev = 0
        ygrev = 0
        dgroom1 = 0
        mgroom1 = 0
        ygroom1 = 0
        dgpax1 = 0
        mgpax1 = 0
        ygpax1 = 0
        dgrate1 = 0
        mgrate1 = 0
        ygrate1 = 0
        dgrev1 = 0
        mgrev1 = 0
        ygrev1 = 0
        tot_droom = 0
        tot_proz1 = 0
        tot_mroom = 0
        tot_proz2 = 0
        tot_yroom = 0
        tot_proz3 = 0
        tot_dpax = 0
        tot_mpax = 0
        tot_ypax = 0
        tot_drate = 0
        tot_mrate = 0
        tot_yrate = 0
        tot_drev = 0
        tot_mrev = 0
        tot_yrev = 0


        from_date = date_mdy(1, 1, get_year(to_date))

        if show_other:
            create_other()

        genstat_obj_list = []
        for genstat, segment in db_session.query(Genstat, Segment).join(Segment,(Segment.segmentcode == Genstat.segmentcode) &  (Segmentcode != black_list) &  (Segmentgrup <= 99)).filter(
                (Genstat.datum >= from_date) &  (Genstat.datum <= to_date) &  (Genstat.segmentcode != 0) &  (Genstat.nationnr != 0) &  (Genstat.res_logic[1])).all():
            if genstat._recid in genstat_obj_list:
                continue
            else:
                genstat_obj_list.append(genstat._recid)

            if genstat.zipreis == 0 and genstat.resstatus == 6 and genstat.gratis != 0:
                fl_comp = True
            else:
                fl_comp = False

            cl_list = query(cl_list_list, filters=(lambda cl_list :cl_list.segm == genstat.segmentcode and cl_list.flag_comp == fl_comp and not cl_list.grpflag), first=True)

            if not cl_list:
                cl_list = Cl_list()
                cl_list_list.append(cl_list)

                cl_list.segm = genstat.segmentcode
                cl_list.bezeich = segment.bezeich
                cl_list.flag_comp = fl_comp
                cl_list.segm_grup = segmentgrup

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

                elif genstat.resstatus != 13 and genstat.gratis == 0:

                    if genstat.datum == to_date:
                        cl_list.drev = genstat.logis
                        cl_list.droom = cl_list.droom + 1
                        cl_list.dpax = cl_list.dpax + genstat.erwachs +\
                                genstat.kind1 + genstat.kind2 + genstat.kind3
                        dgroom = dgroom + 1
                        dgpax = dgpax + genstat.erwachs +\
                                genstat.kind1 + genstat.kind2 + genstat.kind3
                        dgrev = dgrev + genstat.logis
                        cl_list.drate = cl_list.drate + (cl_list.drev / cl_list.droom)
                        dgrate = dgrev / dgroom
                        droom = droom + 1

                    if get_month(genstat.datum) == get_month(to_date):
                        cl_list.mrev = genstat.logis
                        cl_list.mroom = cl_list.mroom + 1
                        cl_list.mpax = cl_list.mpax + genstat.erwachs +\
                                genstat.kind1 + genstat.kind2 + genstat.kind3
                        mgroom = mgroom + 1
                        mgpax = mgpax + genstat.erwachs + genstat.kind1 +\
                                genstat.kind2 + genstat.kind3
                        mgrev = mgrev + genstat.logis
                        cl_list.mrate = cl_list.mrate + (cl_list.mrev / cl_list.mroom)
                        mgrate = mgrev / mgroom
                        mroom = mroom + 1


                    cl_list.yrev = genstat.logis
                    cl_list.yroom = cl_list.yroom + 1
                    cl_list.ypax = cl_list.ypax + genstat.erwachs +\
                            genstat.kind1 + genstat.kind2 + genstat.kind3
                    ygroom = ygroom + 1
                    ygpax = ygpax + genstat.erwachs + genstat.kind1 +\
                            genstat.kind2 + genstat.kind3
                    ygrev = ygrev + genstat.logis
                    cl_list.yrate = cl_list.yrate + (cl_list.yrev / cl_list.yroom)
                    ygrate = ygrev / ygroom
                    yroom = yroom + 1


            else:

                if genstat.zipreis == 0 and genstat.resstatus != 13 and genstat.resstatus == 6 and genstat.gratis != 0:

                    if genstat.datum == to_date:
                        cl_list.droom = cl_list.droom + 1 cl_list.dpax == cl_list.dpax + genstat.gratis droom == droom + 1

                    if get_month(genstat.datum) == get_month(to_date):
                        cl_list.mroom = cl_list.mroom + 1 cl_list.mpax == cl_list.mpax + genstat.gratis mroom == mroom + 1
                    cl_list.yroom = cl_list.yroom + 1 cl_list.ypax == cl_list.ypax + genstat.gratis yroom == yroom + 1

                elif genstat.resstatus != 13 and genstat.gratis == 0:

                    if genstat.datum == to_date:
                        cl_list.drev = cl_list.drev + genstat.logis
                        cl_list.droom = cl_list.droom + 1
                        cl_list.dpax = cl_list.dpax + genstat.erwachs +\
                                genstat.kind1 + genstat.kind2 + genstat.kind3
                        dgroom = dgroom + 1
                        dgpax = dgpax + genstat.erwachs + genstat.kind1 + genstat.kind2 + genstat.kind3
                        dgrev = dgrev + genstat.logis
                        cl_list.drate = cl_list.drev / cl_list.droom
                        dgrate = dgrev / dgroom
                        droom = droom + 1

                    if get_month(genstat.datum) == get_month(to_date):
                        cl_list.mrev = cl_list.mrev + genstat.logis
                        cl_list.mroom = cl_list.mroom + 1
                        cl_list.mpax = cl_list.mpax + genstat.erwachs + genstat.kind1 +\
                                genstat.kind2 + genstat.kind3
                        mgroom = mgroom + 1
                        mgpax = mgpax + genstat.erwachs + genstat.kind1 + genstat.kind2 + genstat.kind3
                        mgrev = mgrev + genstat.logis
                        cl_list.mrate = cl_list.mrev / cl_list.mroom
                        mgrate = mgrev / mgroom
                        mroom = mroom + 1


                    cl_list.yroom = cl_list.yroom + 1
                    ygroom = ygroom + 1
                    cl_list.yrev = cl_list.yrev + genstat.logis
                    ygrev = ygrev + genstat.logis
                    cl_list.yrate = cl_list.yrev / cl_list.yroom
                    ygrate = ygrev / ygroom
                    cl_list.ypax = cl_list.ypax + genstat.erwachs + genstat.kind1 + genstat.kind2
                    ygpax = ygpax + genstat.erwachs + genstat.kind1 + genstat.kind2
                    yroom = yroom + 1

        for cl_list in query(cl_list_list, filters=(lambda cl_list :not cl_list.flag_comp)):

            if cl_list.droom == 0:
                cl_list.dpax = 0

            if cl_list.mroom == 0:
                cl_list.mpax = 0

            if cl_list.yroom == 0:
                cl_list.ypax = 0

            if cl_list.droom != 0:
                cl_list.drate = cl_list.drev / cl_list.droom

            if cl_list.mroom != 0:
                cl_list.mrate = cl_list.mrev / cl_list.mroom

            if droom != 0:
                cl_list.proz1 = 100.0 * cl_list.droom / droom

            if mroom != 0:
                cl_list.proz2 = 100.0 * cl_list.mroom / mroom

            if droom != 0:
                drate = drev / droom

            if mroom != 0:
                mrate = mrev / mroom

            if show_ytd:

                if cl_list.yroom != 0:
                    cl_list.yrate = cl_list.yrev / cl_list.yroom

                if yroom != 0:
                    cl_list.proz3 = 100.0 * cl_list.yroom / yroom

                if yroom != 0:
                    yrate = yrev / yroom

            if grp_flag and not cl_list.grpflag:

                if cl_list.segm_grup != curr_grup and curr_grup != 0:
                    rm_statistic_list1 = Rm_statistic_list1()
                    rm_statistic_list1_list.append(rm_statistic_list1)

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


                    rm_statistic_list1 = Rm_statistic_list1()
                    rm_statistic_list1_list.append(rm_statistic_list1)

                    tot_droom = 0
                    tot_proz1 = 0
                    tot_mroom = 0
                    tot_proz2 = 0
                    tot_yroom = 0
                    tot_proz3 = 0
                    tot_dpax = 0
                    tot_mpax = 0
                    tot_ypax = 0
                    tot_drate = 0
                    tot_mrate = 0
                    tot_yrate = 0
                    tot_drev = 0
                    tot_mrev = 0
                    tot_yrev = 0
                    tot_droom = tot_droom + cl_list.droom
                    tot_proz1 = tot_proz1 + cl_list.proz1
                    tot_mroom = tot_mroom + cl_list.mroom
                    tot_proz2 = tot_proz2 + cl_list.proz2
                    tot_yroom = tot_yroom + cl_list.yroom
                    tot_proz3 = tot_proz3 + cl_list.proz3
                    tot_dpax = tot_dpax + cl_list.dpax
                    tot_mpax = tot_mpax + cl_list.mpax
                    tot_ypax = tot_ypax + cl_list.ypax
                    tot_drate = tot_drate + cl_list.drate
                    tot_mrate = tot_mrate + cl_list.mrate
                    tot_yrate = tot_yrate + cl_list.yrate
                    tot_drev = tot_drev + cl_list.drev
                    tot_mrev = tot_mrev + cl_list.mrev
                    tot_yrev = tot_yrev + cl_list.yrev


                else:
                    tot_droom = tot_droom + cl_list.droom
                    tot_proz1 = tot_proz1 + cl_list.proz1
                    tot_mroom = tot_mroom + cl_list.mroom
                    tot_proz2 = tot_proz2 + cl_list.proz2
                    tot_yroom = tot_yroom + cl_list.yroom
                    tot_proz3 = tot_proz3 + cl_list.proz3
                    tot_dpax = tot_dpax + cl_list.dpax
                    tot_mpax = tot_mpax + cl_list.mpax
                    tot_ypax = tot_ypax + cl_list.ypax
                    tot_drate = tot_drate + cl_list.drate
                    tot_mrate = tot_mrate + cl_list.mrate
                    tot_yrate = tot_yrate + cl_list.yrate
                    tot_drev = tot_drev + cl_list.drev
                    tot_mrev = tot_mrev + cl_list.mrev
                    tot_yrev = tot_yrev + cl_list.yrev


                curr_grup = cl_list.segm_grup


            rm_statistic_list1 = Rm_statistic_list1()
            rm_statistic_list1_list.append(rm_statistic_list1)


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

            if show_other:

                other_list = query(other_list_list, filters=(lambda other_list :other_list.segm == cl_list.segm), first=True)

                if other_list:
                    ttrev = cl_list.drev + other_list.orev
                    ttmrev = cl_list.mrev + other_list.morev
                    ttyrev = cl_list.yrev + other_list.yorev


                    rm_statistic_list1 = Rm_statistic_list1()
                    rm_statistic_list1_list.append(rm_statistic_list1)


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
                    rm_statistic_list1_list.append(rm_statistic_list1)


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
                    rm_statistic_list1_list.append(rm_statistic_list1)


        if grp_flag:
            rm_statistic_list1 = Rm_statistic_list1()
            rm_statistic_list1_list.append(rm_statistic_list1)

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


            rm_statistic_list1 = Rm_statistic_list1()
            rm_statistic_list1_list.append(rm_statistic_list1)


        if not show_ytd:
            rm_statistic_list = Rm_statistic_list()
            rm_statistic_list_list.append(rm_statistic_list)


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


        else:
            rm_statistic_list1 = Rm_statistic_list1()
            rm_statistic_list1_list.append(rm_statistic_list1)

            rm_statistic_list1 = Rm_statistic_list1()
            rm_statistic_list1_list.append(rm_statistic_list1)


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
                rm_statistic_list1.ypax = to_string(ygpax, ">>,>>9")
                rm_statistic_list1.drate = to_string(dgrate, "->>,>>>,>>>,>>>,>>9")
                rm_statistic_list1.mrate = to_string(mgrate, "->>,>>>,>>>,>>>,>>9")
                rm_statistic_list1.yrate = to_string(ygrate, "->>,>>>,>>>,>>>,>>9")
                rm_statistic_list1.drev = to_string(dgrev, "->>,>>>,>>>,>>>,>>9")
                rm_statistic_list1.mrev = to_string(mgrev, "->>,>>>,>>>,>>>,>>9")
                rm_statistic_list1.yrev = to_string(ygrev, "->>,>>>,>>>,>>>,>>9")


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
                rm_statistic_list1.ypax = to_string(ygpax, ">>,>>9")
                rm_statistic_list1.drate = to_string(dgrate, "->>>,>>>,>>>,>>9.99")
                rm_statistic_list1.mrate = to_string(mgrate, "->>>,>>>,>>>,>>9.99")
                rm_statistic_list1.yrate = to_string(ygrate, "->>>,>>>,>>>,>>9.99")
                rm_statistic_list1.drev = to_string(dgrev, "->>>,>>>,>>>,>>9.99")
                rm_statistic_list1.mrev = to_string(mgrev, "->>>,>>>,>>>,>>9.99")
                rm_statistic_list1.yrev = to_string(ygrev, "->>>,>>>,>>>,>>9.99")

        cl_list = query(cl_list_list, filters=(lambda cl_list :cl_list.flag_comp), first=True)

        if cl_list:
            rm_statistic_list1 = Rm_statistic_list1()
            rm_statistic_list1_list.append(rm_statistic_list1)

            rm_statistic_list1 = Rm_statistic_list1()
            rm_statistic_list1_list.append(rm_statistic_list1)

            rm_statistic_list1 = Rm_statistic_list1()
            rm_statistic_list1_list.append(rm_statistic_list1)

            rm_statistic_list1.bezeich = translateExtended ("Compliment Rooms", lvcarea, "")

            for cl_list in query(cl_list_list, filters=(lambda cl_list :cl_list.flag_comp)):
                rm_statistic_list1 = Rm_statistic_list1()
                rm_statistic_list1_list.append(rm_statistic_list1)

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


                pass

    def create_umsatz():

        nonlocal rm_statistic_list_list, rm_statistic_list1_list, lnldelimeter, long_digit, droom, proz1, mroom, proz2, yroom, proz3, dpax, mpax, ypax, drate, mrate, yrate, drev, mrev, yrev, lodg, olodg, dgroom, gproz1, mgroom, gproz2, ygroom, gproz3, dgpax, mgpax, ygpax, dgrate, mgrate, ygrate, dgrev, mgrev, ygrev, dgroom1, mgroom1, ygroom1, dgpax1, mgpax1, ygpax1, dgrate1, mgrate1, ygrate1, dgrev1, mgrev1, ygrev1, ttrev, ttmrev, ttyrev, from_date, period_str, comp_room, curr_grup, tot_droom, tot_proz1, tot_mroom, tot_proz2, tot_yroom, tot_proz3, tot_dpax, tot_mpax, tot_ypax, tot_drate, tot_mrate, tot_yrate, tot_drev, tot_mrev, tot_yrev, lvcarea, htparam, segment, zinrstat, genstat
        nonlocal r_list, r_list1


        nonlocal rm_statistic_list, rm_statistic_list1, cl_list, other_list, s_list, r_list, r_list1
        nonlocal rm_statistic_list_list, rm_statistic_list1_list, cl_list_list, other_list_list, s_list_list

        black_list:int = 0
        fl_comp:bool = False
        dgroom:int = 0
        i:int = 0
        flag_temp:bool = False

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 709)).first()
        black_list = htparam.finteger
        rm_statistic_list_list.clear()
        rm_statistic_list1_list.clear()
        cl_list_list.clear()
        s_list_list.clear()
        droom = 0
        mroom = 0
        yroom = 0
        dpax = 0
        mpax = 0
        ypax = 0
        drate = 0
        mrate = 0
        yrate = 0
        drev = 0
        mrev = 0
        yrev = 0
        dgroom = 0
        mgroom = 0
        ygroom = 0
        dgpax = 0
        mgpax = 0
        ygpax = 0
        dgrate = 0
        mgrate = 0
        ygrate = 0
        dgrev = 0
        mgrev = 0
        ygrev = 0
        tot_droom = 0
        tot_proz1 = 0
        tot_mroom = 0
        tot_proz2 = 0
        tot_yroom = 0
        tot_proz3 = 0
        tot_dpax = 0
        tot_mpax = 0
        tot_ypax = 0
        tot_drate = 0
        tot_mrate = 0
        tot_yrate = 0
        tot_drev = 0
        tot_mrev = 0
        tot_yrev = 0


        from_date = date_mdy(get_month(to_date) , 1, get_year(to_date))

        if show_other:
            create_other()

        genstat_obj_list = []
        for genstat, segment in db_session.query(Genstat, Segment).join(Segment,(Segment.segmentcode == Genstat.segmentcode) &  (Segmentcode != black_list) &  (Segmentgrup <= 99)).filter(
                (Genstat.datum >= from_date) &  (Genstat.datum <= to_date) &  (Genstat.segmentcode != 0) &  (Genstat.nationnr != 0)).all():
            if genstat._recid in genstat_obj_list:
                continue
            else:
                genstat_obj_list.append(genstat._recid)

            if genstat.zipreis == 0 and genstat.resstatus == 6 and genstat.gratis != 0:
                fl_comp = True
            else:
                fl_comp = False

            cl_list = query(cl_list_list, filters=(lambda cl_list :cl_list.segm == genstat.segmentcode and cl_list.flag_comp == fl_comp), first=True)

            if not cl_list:
                cl_list = Cl_list()
                cl_list_list.append(cl_list)

                cl_list.segm = genstat.segmentcode
                cl_list.bezeich = segment.bezeich
                cl_list.flag_comp = fl_comp
                cl_list.segm_grup = segmentgrup

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
                        cl_list.drev = genstat.logis
                        cl_list.droom = cl_list.droom + 1
                        cl_list.dpax = cl_list.dpax + genstat.erwachs +\
                                genstat.kind1 + genstat.kind2 + genstat.kind3
                        dgroom = dgroom + 1
                        dgpax = dgpax + genstat.erwachs +\
                                genstat.kind1 + genstat.kind2 + genstat.kind3
                        dgrev = dgrev + genstat.logis
                        cl_list.drate = cl_list.drate + (cl_list.drev / cl_list.droom)
                        dgrate = dgrev / dgroom
                        droom = droom + 1

                    if get_month(genstat.datum) == get_month(to_date):
                        cl_list.mrev = genstat.logis
                        cl_list.mroom = cl_list.mroom + 1
                        cl_list.mpax = cl_list.mpax + genstat.erwachs +\
                                genstat.kind1 + genstat.kind2 + genstat.kind3
                        mgroom = mgroom + 1
                        mgpax = mgpax + genstat.erwachs + genstat.kind1 +\
                                genstat.kind2 + genstat.kind3
                        mgrev = mgrev + genstat.logis
                        cl_list.mrate = cl_list.mrate + (cl_list.mrev / cl_list.mroom)
                        mgrate = mgrev / mgroom
                        mroom = mroom + 1


            else:

                if genstat.zipreis == 0 and genstat.resstatus == 6 and genstat.gratis != 0:

                    if genstat.datum == to_date:
                        cl_list.droom = cl_list.droom + 1 cl_list.dpax == cl_list.dpax + genstat.gratis droom == droom + 1

                    if get_month(genstat.datum) == get_month(to_date):
                        cl_list.mroom = cl_list.mroom + 1 cl_list.mpax == cl_list.mpax + genstat.gratis mroom == mroom + 1

                elif genstat.resstatus != 13:

                    if genstat.datum == to_date:
                        cl_list.drev = cl_list.drev + genstat.logis
                        cl_list.droom = cl_list.droom + 1
                        cl_list.dpax = cl_list.dpax + genstat.erwachs +\
                                genstat.kind1 + genstat.kind2 + genstat.kind3
                        dgroom = dgroom + 1
                        dgpax = dgpax + genstat.erwachs +\
                                genstat.kind1 + genstat.kind2 + genstat.kind3
                        dgrev = dgrev + genstat.logis
                        cl_list.drate = cl_list.drev / cl_list.droom
                        dgrate = dgrev / dgroom
                        droom = droom + 1

                    if get_month(genstat.datum) == get_month(to_date):
                        cl_list.mroom = cl_list.mroom + 1
                        cl_list.mpax = cl_list.mpax + genstat.erwachs + genstat.kind1 +\
                                genstat.kind2 + genstat.kind3
                        cl_list.mrev = cl_list.mrev + genstat.logis
                        mgroom = mgroom + 1
                        mgpax = mgpax + genstat.erwachs + genstat.kind1 + genstat.kind2 + genstat.kind3
                        mgrev = mgrev + genstat.logis
                        cl_list.mrate = cl_list.mrev / cl_list.mroom
                        mgrate = mgrev / mgroom
                        mroom = mroom + 1

        for cl_list in query(cl_list_list, filters=(lambda cl_list :not flag_comp)):

            if cl_list.droom == 0:
                cl_list.dpax = 0

            if cl_list.mroom == 0:
                cl_list.mpax = 0

            if cl_list.yroom == 0:
                cl_list.ypax = 0

            if cl_list.droom != 0:
                cl_list.drate = cl_list.drev / cl_list.droom

            if cl_list.mroom != 0:
                cl_list.mrate = cl_list.mrev / cl_list.mroom

            if droom != 0:
                cl_list.proz1 = 100.0 * cl_list.droom / droom

            if mroom != 0:
                cl_list.proz2 = 100.0 * cl_list.mroom / mroom

            if droom != 0:
                drate = drev / droom

            if mroom != 0:
                mrate = mrev / mroom

            if not show_ytd:

                if grp_flag and not cl_list.grpflag:

                    if cl_list.segm_grup != curr_grup and curr_grup != 0:
                        rm_statistic_list = Rm_statistic_list()
                        rm_statistic_list_list.append(rm_statistic_list)

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


                        rm_statistic_list = Rm_statistic_list()
                        rm_statistic_list_list.append(rm_statistic_list)

                        tot_droom = 0
                        tot_proz1 = 0
                        tot_mroom = 0
                        tot_proz2 = 0
                        tot_yroom = 0
                        tot_proz3 = 0
                        tot_dpax = 0
                        tot_mpax = 0
                        tot_ypax = 0
                        tot_drate = 0
                        tot_mrate = 0
                        tot_yrate = 0
                        tot_drev = 0
                        tot_mrev = 0
                        tot_yrev = 0
                        tot_droom = tot_droom + cl_list.droom
                        tot_proz1 = tot_proz1 + cl_list.proz1
                        tot_mroom = tot_mroom + cl_list.mroom
                        tot_proz2 = tot_proz2 + cl_list.proz2
                        tot_yroom = tot_yroom + cl_list.yroom
                        tot_proz3 = tot_proz3 + cl_list.proz3
                        tot_dpax = tot_dpax + cl_list.dpax
                        tot_mpax = tot_mpax + cl_list.mpax
                        tot_ypax = tot_ypax + cl_list.ypax
                        tot_drate = tot_drate + cl_list.drate
                        tot_mrate = tot_mrate + cl_list.mrate
                        tot_yrate = tot_yrate + cl_list.yrate
                        tot_drev = tot_drev + cl_list.drev
                        tot_mrev = tot_mrev + cl_list.mrev
                        tot_yrev = tot_yrev + cl_list.yrev


                    else:
                        tot_droom = tot_droom + cl_list.droom
                        tot_proz1 = tot_proz1 + cl_list.proz1
                        tot_mroom = tot_mroom + cl_list.mroom
                        tot_proz2 = tot_proz2 + cl_list.proz2
                        tot_yroom = tot_yroom + cl_list.yroom
                        tot_proz3 = tot_proz3 + cl_list.proz3
                        tot_dpax = tot_dpax + cl_list.dpax
                        tot_mpax = tot_mpax + cl_list.mpax
                        tot_ypax = tot_ypax + cl_list.ypax
                        tot_drate = tot_drate + cl_list.drate
                        tot_mrate = tot_mrate + cl_list.mrate
                        tot_yrate = tot_yrate + cl_list.yrate
                        tot_drev = tot_drev + cl_list.drev
                        tot_mrev = tot_mrev + cl_list.mrev
                        tot_yrev = tot_yrev + cl_list.yrev


                    curr_grup = cl_list.segm_grup


                rm_statistic_list = Rm_statistic_list()
                rm_statistic_list_list.append(rm_statistic_list)


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

                if cl_list.grpflag:
                    rm_statistic_list = Rm_statistic_list()
                rm_statistic_list_list.append(rm_statistic_list)

            else:

                if grp_flag and not cl_list.grpflag:

                    if cl_list.segm_grup != curr_grup and curr_grup != 0:
                        rm_statistic_list = Rm_statistic_list()
                        rm_statistic_list_list.append(rm_statistic_list)

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


                        rm_statistic_list = Rm_statistic_list()
                        rm_statistic_list_list.append(rm_statistic_list)

                        tot_droom = 0
                        tot_proz1 = 0
                        tot_mroom = 0
                        tot_proz2 = 0
                        tot_yroom = 0
                        tot_proz3 = 0
                        tot_dpax = 0
                        tot_mpax = 0
                        tot_ypax = 0
                        tot_drate = 0
                        tot_mrate = 0
                        tot_yrate = 0
                        tot_drev = 0
                        tot_mrev = 0
                        tot_yrev = 0
                        tot_droom = tot_droom + cl_list.droom
                        tot_proz1 = tot_proz1 + cl_list.proz1
                        tot_mroom = tot_mroom + cl_list.mroom
                        tot_proz2 = tot_proz2 + cl_list.proz2
                        tot_yroom = tot_yroom + cl_list.yroom
                        tot_proz3 = tot_proz3 + cl_list.proz3
                        tot_dpax = tot_dpax + cl_list.dpax
                        tot_mpax = tot_mpax + cl_list.mpax
                        tot_ypax = tot_ypax + cl_list.ypax
                        tot_drate = tot_drate + cl_list.drate
                        tot_mrate = tot_mrate + cl_list.mrate
                        tot_yrate = tot_yrate + cl_list.yrate
                        tot_drev = tot_drev + cl_list.drev
                        tot_mrev = tot_mrev + cl_list.mrev
                        tot_yrev = tot_yrev + cl_list.yrev


                    else:
                        tot_droom = tot_droom + cl_list.droom
                        tot_proz1 = tot_proz1 + cl_list.proz1
                        tot_mroom = tot_mroom + cl_list.mroom
                        tot_proz2 = tot_proz2 + cl_list.proz2
                        tot_yroom = tot_yroom + cl_list.yroom
                        tot_proz3 = tot_proz3 + cl_list.proz3
                        tot_dpax = tot_dpax + cl_list.dpax
                        tot_mpax = tot_mpax + cl_list.mpax
                        tot_ypax = tot_ypax + cl_list.ypax
                        tot_drate = tot_drate + cl_list.drate
                        tot_mrate = tot_mrate + cl_list.mrate
                        tot_yrate = tot_yrate + cl_list.yrate
                        tot_drev = tot_drev + cl_list.drev
                        tot_mrev = tot_mrev + cl_list.mrev
                        tot_yrev = tot_yrev + cl_list.yrev


                    curr_grup = cl_list.segm_grup


                rm_statistic_list1 = Rm_statistic_list1()
                rm_statistic_list1_list.append(rm_statistic_list1)


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

                if show_other:

                    other_list = query(other_list_list, filters=(lambda other_list :other_list.segm == cl_list.segm), first=True)

                    if other_list:
                        ttrev = cl_list.drev + other_list.orev
                        ttmrev = cl_list.mrev + other_list.morev
                        ttyrev = cl_list.yrev + other_list.yorev


                        rm_statistic_list1 = Rm_statistic_list1()
                        rm_statistic_list1_list.append(rm_statistic_list1)


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
                        rm_statistic_list1_list.append(rm_statistic_list1)


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
                        rm_statistic_list1_list.append(rm_statistic_list1)


        if grp_flag:
            rm_statistic_list = Rm_statistic_list()
            rm_statistic_list_list.append(rm_statistic_list)


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


                rm_statistic_list = Rm_statistic_list()
                rm_statistic_list_list.append(rm_statistic_list)


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


                pass
                rm_statistic_list = Rm_statistic_list()
                rm_statistic_list_list.append(rm_statistic_list)


        if not show_ytd:
            rm_statistic_list = Rm_statistic_list()
            rm_statistic_list_list.append(rm_statistic_list)

            rm_statistic_list = Rm_statistic_list()
            rm_statistic_list_list.append(rm_statistic_list)


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

        cl_list = query(cl_list_list, filters=(lambda cl_list :cl_list.flag_comp), first=True)

        if cl_list:
            rm_statistic_list = Rm_statistic_list()
            rm_statistic_list_list.append(rm_statistic_list)

            rm_statistic_list = Rm_statistic_list()
            rm_statistic_list_list.append(rm_statistic_list)

            rm_statistic_list = Rm_statistic_list()
            rm_statistic_list_list.append(rm_statistic_list)

            rm_statistic_list.bezeich = translateExtended ("Compliment Rooms", lvcarea, "")

            for cl_list in query(cl_list_list, filters=(lambda cl_list :flag_comp)):
                rm_statistic_list = Rm_statistic_list()
                rm_statistic_list_list.append(rm_statistic_list)

                rm_statistic_list.segm = to_string(cl_list.segm, ">>9")
                rm_statistic_list.bezeich = cl_list.bezeich
                rm_statistic_list.dgroom = to_string(cl_list.droom, ">>,>>9")
                rm_statistic_list.proz1 = ""
                rm_statistic_list.mgroom = to_string(cl_list.mroom, ">>,>>9")
                rm_statistic_list.proz2 = ""
                rm_statistic_list.dgpax = to_string(cl_list.dpax, ">>,>>9")
                rm_statistic_list.mgpax = to_string(cl_list.mpax, ">>,>>9")

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 246)).first()
    long_digit = htparam.flogical
    comp_room = translateExtended ("Compliment Rooms" , lvcarea, "")

    if show_ytd:
        create_umsatz2()
    else:
        create_umsatz()

    return generate_output()