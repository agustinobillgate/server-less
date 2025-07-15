#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from sqlalchemy import func
from models import Queasy, Nation, Genstat, Reservation

def orges_natbl(fdate:date, to_date:date, show_ytd:bool):

    prepare_cache ([Queasy, Nation, Genstat, Reservation])

    out_list_data = []
    out_list1_data = []
    tot_b_individual:int = 0
    tot_b_grup:int = 0
    tot_l_individual:int = 0
    tot_l_grup:int = 0
    mtdtot_b_individual:int = 0
    mtdtot_b_grup:int = 0
    mtdtot_l_individual:int = 0
    mtdtot_l_grup:int = 0
    ytdtot_b_individual:int = 0
    ytdtot_b_grup:int = 0
    ytdtot_l_individual:int = 0
    ytdtot_l_grup:int = 0
    subtot_b:int = 0
    subtot_l:int = 0
    ytdsubtot_b:int = 0
    ytdsubtot_l:int = 0
    mtdsubtot_b:int = 0
    mtdsubtot_l:int = 0
    subtot_date:int = 0
    subtot_mtd:int = 0
    subtot_ytd:int = 0
    pmtd_btotrmnights:Decimal = to_decimal("0.0")
    pmtd_bgrouprmnights:Decimal = to_decimal("0.0")
    pmtd_bindividualrmnights:Decimal = to_decimal("0.0")
    pmtd_ltotrmnights:Decimal = to_decimal("0.0")
    pmtd_lgrouprmnights:Decimal = to_decimal("0.0")
    pmtd_lindividualrmnights:Decimal = to_decimal("0.0")
    pytd_btotrmnights:Decimal = to_decimal("0.0")
    pytd_bgrouprmnights:Decimal = to_decimal("0.0")
    pytd_bindividualrmnights:Decimal = to_decimal("0.0")
    pytd_ltotrmnights:Decimal = to_decimal("0.0")
    pytd_lgrouprmnights:Decimal = to_decimal("0.0")
    pytd_lindividualrmnights:Decimal = to_decimal("0.0")
    psubtotal_date:Decimal = to_decimal("0.0")
    psubtotal_mtd:Decimal = to_decimal("0.0")
    psubtotal_ytd:Decimal = to_decimal("0.0")
    segm__purcode:int = 0
    i:int = 0
    str:string = ""
    from_date:date = None
    jan1:date = None
    mtd1:date = None
    queasy = nation = genstat = reservation = None

    orges_list = region_list = out_list = out_list1 = None

    orges_list_data, Orges_list = create_model("Orges_list", {"region_nr":int, "nationnr":int, "nationality":string, "b_totrmnights":int, "b_grouprmnights":int, "b_individualrmnights":int, "l_totrmnights":int, "l_grouprmnights":int, "l_individualrmnights":int, "ytd_btotrmnights":int, "ytd_bgrouprmnights":int, "ytd_bindividualrmnights":int, "ytd_ltotrmnights":int, "ytd_lgrouprmnights":int, "ytd_lindividualrmnights":int, "mtd_btotrmnights":int, "mtd_bgrouprmnights":int, "mtd_bindividualrmnights":int, "mtd_ltotrmnights":int, "mtd_lgrouprmnights":int, "mtd_lindividualrmnights":int, "pmtd_btotrmnights":Decimal, "pmtd_bgrouprmnights":Decimal, "pmtd_bindividualrmnights":Decimal, "pmtd_ltotrmnights":Decimal, "pmtd_lgrouprmnights":Decimal, "pmtd_lindividualrmnights":Decimal, "pytd_btotrmnights":Decimal, "pytd_bgrouprmnights":Decimal, "pytd_bindividualrmnights":Decimal, "pytd_ltotrmnights":Decimal, "pytd_lgrouprmnights":Decimal, "pytd_lindividualrmnights":Decimal, "subtotal_date":int, "subtotal_mtd":int, "subtotal_ytd":int, "psubtotal_date":Decimal, "psubtotal_mtd":Decimal, "psubtotal_ytd":Decimal})
    region_list_data, Region_list = create_model_like(Orges_list)
    out_list_data, Out_list = create_model("Out_list", {"str":string, "num":int, "nationnr":int, "region_nr":int})
    out_list1_data, Out_list1 = create_model("Out_list1", {"str":string, "num":int, "nationnr":int, "region_nr":int})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal out_list_data, out_list1_data, tot_b_individual, tot_b_grup, tot_l_individual, tot_l_grup, mtdtot_b_individual, mtdtot_b_grup, mtdtot_l_individual, mtdtot_l_grup, ytdtot_b_individual, ytdtot_b_grup, ytdtot_l_individual, ytdtot_l_grup, subtot_b, subtot_l, ytdsubtot_b, ytdsubtot_l, mtdsubtot_b, mtdsubtot_l, subtot_date, subtot_mtd, subtot_ytd, pmtd_btotrmnights, pmtd_bgrouprmnights, pmtd_bindividualrmnights, pmtd_ltotrmnights, pmtd_lgrouprmnights, pmtd_lindividualrmnights, pytd_btotrmnights, pytd_bgrouprmnights, pytd_bindividualrmnights, pytd_ltotrmnights, pytd_lgrouprmnights, pytd_lindividualrmnights, psubtotal_date, psubtotal_mtd, psubtotal_ytd, segm__purcode, i, str, from_date, jan1, mtd1, queasy, nation, genstat, reservation
        nonlocal fdate, to_date, show_ytd


        nonlocal orges_list, region_list, out_list, out_list1
        nonlocal orges_list_data, region_list_data, out_list_data, out_list1_data

        return {"out-list": out_list_data, "out-list1": out_list1_data}

    def create_list():

        nonlocal out_list_data, out_list1_data, tot_b_individual, tot_b_grup, tot_l_individual, tot_l_grup, mtdtot_b_individual, mtdtot_b_grup, mtdtot_l_individual, mtdtot_l_grup, ytdtot_b_individual, ytdtot_b_grup, ytdtot_l_individual, ytdtot_l_grup, subtot_b, subtot_l, ytdsubtot_b, ytdsubtot_l, mtdsubtot_b, mtdsubtot_l, subtot_date, subtot_mtd, subtot_ytd, pmtd_btotrmnights, pmtd_bgrouprmnights, pmtd_bindividualrmnights, pmtd_ltotrmnights, pmtd_lgrouprmnights, pmtd_lindividualrmnights, pytd_btotrmnights, pytd_bgrouprmnights, pytd_bindividualrmnights, pytd_ltotrmnights, pytd_lgrouprmnights, pytd_lindividualrmnights, psubtotal_date, psubtotal_mtd, psubtotal_ytd, segm__purcode, i, str, from_date, jan1, mtd1, queasy, nation, genstat, reservation
        nonlocal fdate, to_date, show_ytd


        nonlocal orges_list, region_list, out_list, out_list1
        nonlocal orges_list_data, region_list_data, out_list_data, out_list1_data


        out_list_data.clear()
        out_list1_data.clear()
        region_list_data.clear()
        orges_list_data.clear()
        tot_b_individual = 0
        tot_b_grup = 0
        tot_l_individual = 0
        tot_l_grup = 0
        mtdtot_b_individual = 0
        mtdtot_b_grup = 0
        mtdtot_l_individual = 0
        mtdtot_l_grup = 0
        ytdtot_b_individual = 0
        ytdtot_b_grup = 0
        ytdtot_l_individual = 0
        ytdtot_l_grup = 0
        subtot_b = 0
        subtot_l = 0
        mtdsubtot_b = 0
        mtdsubtot_l = 0
        ytdsubtot_b = 0
        ytdsubtot_l = 0
        subtot_date = 0
        subtot_mtd = 0
        subtot_ytd = 0
        pmtd_btotrmnights =  to_decimal("0")
        pmtd_bgrouprmnights =  to_decimal("0")
        pmtd_bindividualrmnights =  to_decimal("0")
        pmtd_ltotrmnights =  to_decimal("0")
        pmtd_lgrouprmnights =  to_decimal("0")
        pmtd_lindividualrmnights =  to_decimal("0")
        pytd_btotrmnights =  to_decimal("0")
        pytd_bgrouprmnights =  to_decimal("0")
        pytd_bindividualrmnights =  to_decimal("0")
        pytd_ltotrmnights =  to_decimal("0")
        pytd_lgrouprmnights =  to_decimal("0")
        pytd_lindividualrmnights =  to_decimal("0")
        psubtotal_date =  to_decimal("0")
        psubtotal_mtd =  to_decimal("0")
        psubtotal_ytd =  to_decimal("0")

        for queasy in db_session.query(Queasy).filter(
                 (Queasy.key == 6)).order_by(Queasy._recid).all():
            region_list = Region_list()
            region_list_data.append(region_list)

            region_list.nationality = queasy.char1
            region_list.region_nr = queasy.number1

        genstat_obj_list = {}
        for genstat, nation in db_session.query(Genstat, Nation).join(Nation,(Nation.nationnr == Genstat.nationnr)).filter(
                 (Genstat.datum >= from_date) & (Genstat.datum <= to_date) & (Genstat.resstatus != 13) & (Genstat.segmentcode != 0) & (Genstat.nationnr != 0) & (Genstat.zinr != "") & (Genstat.res_logic[inc_value(1)]) & (matches(Genstat.res_char[inc_value(1)],("*SEGM_PUR*")))).order_by(Genstat._recid).all():
            region_list = query(region_list_data, (lambda region_list: region_list.region_nr == nation.untergruppe), first=True)
            if not region_list:
                continue

            if genstat_obj_list.get(genstat._recid):
                continue
            else:
                genstat_obj_list[genstat._recid] = True

            orges_list = query(orges_list_data, filters=(lambda orges_list: orges_list.nationnr == nation.nationnr), first=True)

            if not orges_list:
                orges_list = Orges_list()
                orges_list_data.append(orges_list)

                orges_list.region_nr = region_list.region_nr
                orges_list.nationnr = nation.nationnr
                orges_list.nationality = nation.bezeich


            for i in range(1,num_entries(genstat.res_char[1], ";") - 1 + 1) :
                str = entry(i - 1, genstat.res_char[1], ";")

                if substring(str, 0, 8) == ("SEGM_PUR").lower() :
                    segm__purcode = to_int(substring(str, 8))

            queasy = get_cache (Queasy, {"key": [(eq, 143)],"number1": [(eq, segm__purcode)]})

            if matches(queasy.char1,r"BS"):

                if genstat.datum >= fdate and genstat.datum <= to_date:
                    region_list.b_totrmnights = region_list.b_totrmnights + 1
                    orges_list.b_totrmnights = orges_list.b_totrmnights + 1

                    reservation = get_cache (Reservation, {"resnr": [(eq, genstat.resnr)]})

                    if reservation and (to_int(reservation.grpflag) + 1) == 2:
                        region_list.b_grouprmnights = region_list.b_grouprmnights + 1
                        orges_list.b_grouprmnights = orges_list.b_grouprmnights + 1
                        tot_b_grup = tot_b_grup + 1
                    else:
                        region_list.b_individualrmnights = region_list.b_individualrmnights + 1
                        orges_list.b_individualrmnights = orges_list.b_individualrmnights + 1
                        tot_b_individual = tot_b_individual + 1

                if get_month(genstat.datum) == get_month(to_date):
                    region_list.mtd_btotrmnights = region_list.mtd_btotrmnights + 1
                    orges_list.mtd_btotrmnights = orges_list.mtd_btotrmnights + 1

                    reservation = get_cache (Reservation, {"resnr": [(eq, genstat.resnr)]})

                    if reservation and (to_int(reservation.grpflag) + 1) == 2:
                        region_list.mtd_bgrouprmnights = region_list.mtd_bgrouprmnights + 1
                        orges_list.mtd_bgrouprmnights = orges_list.mtd_bgrouprmnights + 1
                        mtdtot_b_grup = mtdtot_b_grup + 1
                    else:
                        region_list.mtd_bindividualrmnights = region_list.mtd_bindividualrmnights + 1
                        orges_list.mtd_bindividualrmnights = orges_list.mtd_bindividualrmnights + 1
                        mtdtot_b_individual = mtdtot_b_individual + 1

            elif matches(queasy.char1,r"LS"):

                if genstat.datum >= fdate and genstat.datum <= to_date:
                    region_list.l_totrmnights = region_list.l_totrmnights + 1
                    orges_list.l_totrmnights = orges_list.l_totrmnights + 1

                    reservation = get_cache (Reservation, {"resnr": [(eq, genstat.resnr)]})

                    if reservation and (to_int(reservation.grpflag) + 1) == 2:
                        region_list.l_grouprmnights = region_list.l_grouprmnights + 1
                        orges_list.l_grouprmnights = orges_list.l_grouprmnights + 1
                        tot_l_grup = tot_l_grup + 1
                    else:
                        region_list.l_individualrmnights = region_list.l_individualrmnights + 1
                        orges_list.l_individualrmnights = orges_list.l_individualrmnights + 1
                        tot_l_individual = tot_l_individual + 1

                if get_month(genstat.datum) == get_month(to_date):
                    region_list.mtd_ltotrmnights = region_list.mtd_ltotrmnights + 1
                    orges_list.mtd_ltotrmnights = orges_list.mtd_ltotrmnights + 1

                    reservation = get_cache (Reservation, {"resnr": [(eq, genstat.resnr)]})

                    if reservation and (to_int(reservation.grpflag) + 1) == 2:
                        region_list.mtd_lgrouprmnights = region_list.mtd_lgrouprmnights + 1
                        orges_list.mtd_lgrouprmnights = orges_list.mtd_lgrouprmnights + 1
                        mtdtot_l_grup = mtdtot_l_grup + 1
                    else:
                        region_list.mtd_lindividualrmnights = region_list.mtd_lindividualrmnights + 1
                        orges_list.mtd_lindividualrmnights = orges_list.mtd_lindividualrmnights + 1
                        mtdtot_l_individual = mtdtot_l_individual + 1
        subtot_b = tot_b_grup + tot_b_individual
        subtot_l = tot_l_grup + tot_l_individual
        mtdsubtot_b = mtdtot_b_grup + mtdtot_b_individual
        mtdsubtot_l = mtdtot_l_grup + mtdtot_l_individual
        subtot_date = subtot_b + subtot_l
        subtot_mtd = mtdsubtot_b + mtdsubtot_l

        for orges_list in query(orges_list_data, sort_by=[("region_nr",False)]):
            region_list = query(region_list_data, (lambda region_list: region_list.region_nr == orges_list.region_nr), first=True)
            if not region_list:
                continue

            region_list.subtotal_date = region_list.B_totRmNights + region_list.L_totRmNights
            region_list.subtotal_mtd = region_list.MTD_BtotRmNights + region_list.MTD_LtotRmNights
            orges_list.subtotal_date = orges_list.B_totRmNights + orges_list.L_totRmNights
            orges_list.subtotal_mtd = orges_list.MTD_BtotRmNights + orges_list.MTD_LtotRmNights
            region_list.pmtd_btotrmnights = ( to_decimal(region_list.MTD_BtotRmNights) / to_decimal(mtdsubtot_b)) * to_decimal(100.00)
            region_list.pmtd_bgrouprmnights = ( to_decimal(region_list.MTD_BgroupRmNights) / to_decimal(mtdtot_b_grup)) * to_decimal(100.00)
            region_list.pmtd_bindividualrmnights = ( to_decimal(region_list.MTD_BindividualRmNights) / to_decimal(mtdtot_b_individual)) * to_decimal(100.00)
            region_list.pmtd_ltotrmnights = ( to_decimal(region_list.MTD_LtotRmNights) / to_decimal(mtdsubtot_l)) * to_decimal(100.00)
            region_list.pmtd_lgrouprmnights = ( to_decimal(region_list.MTD_LgroupRmNights) / to_decimal(mtdtot_l_grup)) * to_decimal(100.00)
            region_list.pmtd_lindividualrmnights = ( to_decimal(region_list.MTD_LindividualRmNights) / to_decimal(mtdtot_l_individual)) * to_decimal(100.00)
            region_list.psubtotal_date = ( to_decimal(region_list.subtotal_date) / to_decimal(subtot_date)) * to_decimal(100.00)
            region_list.psubtotal_mtd = ( to_decimal(region_list.subtotal_MTD) / to_decimal(subtot_mtd)) * to_decimal(100.00)
            orges_list.pmtd_btotrmnights = ( to_decimal(orges_list.MTD_BtotRmNights) / to_decimal(mtdsubtot_b)) * to_decimal(100.00)
            orges_list.pmtd_bgrouprmnights = ( to_decimal(orges_list.MTD_BgroupRmNights) / to_decimal(mtdtot_b_grup)) * to_decimal(100.00)
            orges_list.pmtd_bindividualrmnights = ( to_decimal(orges_list.MTD_BindividualRmNights) / to_decimal(mtdtot_b_individual)) * to_decimal(100.00)
            orges_list.pmtd_ltotrmnights = ( to_decimal(orges_list.MTD_LtotRmNights) / to_decimal(mtdsubtot_l)) * to_decimal(100.00)
            orges_list.pmtd_lgrouprmnights = ( to_decimal(orges_list.MTD_LgroupRmNights) / to_decimal(mtdtot_l_grup)) * to_decimal(100.00)
            orges_list.pmtd_lindividualrmnights = ( to_decimal(orges_list.MTD_LindividualRmNights) / to_decimal(mtdtot_l_individual)) * to_decimal(100.00)
            orges_list.psubtotal_date = ( to_decimal(orges_list.subtotal_date) / to_decimal(subtot_date)) * to_decimal(100.00)
            orges_list.psubtotal_mtd = ( to_decimal(orges_list.subtotal_MTD) / to_decimal(subtot_mtd)) * to_decimal(100.00)

            if region_list.pmtd_btotrmnights == None:
                region_list.pmtd_btotrmnights =  to_decimal(0.00)

            if region_list.pmtd_bgrouprmnights == None:
                region_list.pmtd_bgrouprmnights =  to_decimal(0.00)

            if region_list.pmtd_bindividualrmnights == None:
                region_list.pmtd_bindividualrmnights =  to_decimal(0.00)

            if region_list.pmtd_ltotrmnights == None:
                region_list.pmtd_ltotrmnights =  to_decimal(0.00)

            if region_list.pmtd_lgrouprmnights == None:
                region_list.pmtd_lgrouprmnights =  to_decimal(0.00)

            if region_list.pmtd_lindividualrmnights == None:
                region_list.pmtd_lindividualrmnights =  to_decimal(0.00)

            if region_list.psubtotal_date == None:
                region_list.psubtotal_date =  to_decimal(0.00)

            if region_list.psubtotal_mtd == None:
                region_list.psubtotal_mtd =  to_decimal(0.00)

            if orges_list.pmtd_btotrmnights == None:
                orges_list.pmtd_btotrmnights =  to_decimal(0.00)

            if orges_list.pmtd_bgrouprmnights == None:
                orges_list.pmtd_bgrouprmnights =  to_decimal(0.00)

            if orges_list.pmtd_bindividualrmnights == None:
                orges_list.pmtd_bindividualrmnights =  to_decimal(0.00)

            if orges_list.pmtd_ltotrmnights == None:
                orges_list.pmtd_ltotrmnights =  to_decimal(0.00)

            if orges_list.pmtd_lgrouprmnights == None:
                orges_list.pmtd_lgrouprmnights =  to_decimal(0.00)

            if orges_list.pmtd_lindividualrmnights == None:
                orges_list.pmtd_lindividualrmnights =  to_decimal(0.00)

            if orges_list.psubtotal_date == None:
                orges_list.psubtotal_date =  to_decimal(0.00)

            if orges_list.psubtotal_mtd == None:
                orges_list.psubtotal_mtd =  to_decimal(0.00)

            out_list = query(out_list_data, filters=(lambda out_list: out_list.num == 999 and out_list.region_nr == orges_list.region_nr), first=True)

            if not out_list:
                out_list = Out_list()
                out_list_data.append(out_list)

                out_list.num = 999
                out_list.region_nr = region_list.region_nr


                out_list.str = out_list.str + to_string("** " + region_list.nationality + " **", "x(30)") + to_string(region_list.B_totRmNights, " >>>>9") + to_string(region_list.B_groupRmNights, " >>>>9") + to_string(region_list.B_individualRmNights, " >>>>9") + to_string(region_list.L_totRmNights, " >>>>9") + to_string(region_list.L_groupRmNights, " >>>>9") + to_string(region_list.L_individualRmNights, " >>>>9") + to_string(region_list.MTD_BtotRmNights, " >>>>9") + to_string(region_list.MTD_BgroupRmNights, " >>>>9") + to_string(region_list.MTD_BindividualRmNights, " >>>>9") + to_string(region_list.MTD_LtotRmNights, " >>>>9") + to_string(region_list.MTD_LgroupRmNights, " >>>>9") + to_string(region_list.MTD_LindividualRmNights, " >>>>9") + to_string(region_list.pmtd_btotrmnights, " >>9.99") + to_string(region_list.pmtd_bgrouprmnights, " >>9.99") + to_string(region_list.pmtd_bindividualrmnights, " >>9.99") + to_string(region_list.pmtd_ltotrmnights, " >>9.99") + to_string(region_list.pmtd_lgrouprmnights, " >>9.99") + to_string(region_list.pmtd_lindividualrmnights, " >>9.99") + to_string(region_list.subtotal_date, " >>>>9") + to_string(region_list.subtotal_MTD, " >>>>9") + to_string(region_list.psubtotal_date, " >>9.99") + to_string(region_list.psubtotal_mtd, " >>9.99")
                out_list = Out_list()
                out_list_data.append(out_list)

                out_list.num = 9999
                out_list.region_nr = region_list.region_nr


            pmtd_btotrmnights =  to_decimal(pmtd_btotrmnights) + to_decimal(orges_list.pmtd_btotrmnights)
            pmtd_bgrouprmnights =  to_decimal(pmtd_bgrouprmnights) + to_decimal(orges_list.pmtd_bgrouprmnights)
            pmtd_bindividualrmnights =  to_decimal(pmtd_bindividualrmnights) + to_decimal(orges_list.pmtd_bindividualrmnights)
            pmtd_ltotrmnights =  to_decimal(pmtd_ltotrmnights) + to_decimal(orges_list.pmtd_ltotrmnights)
            pmtd_lgrouprmnights =  to_decimal(pmtd_lgrouprmnights) + to_decimal(orges_list.pmtd_lgrouprmnights)
            pmtd_lindividualrmnights =  to_decimal(pmtd_lindividualrmnights) + to_decimal(orges_list.pmtd_lindividualrmnights)
            psubtotal_date =  to_decimal(psubtotal_date) + to_decimal(orges_list.psubtotal_date)
            psubtotal_mtd =  to_decimal(psubtotal_mtd) + to_decimal(orges_list.psubtotal_mtd)


            out_list = Out_list()
            out_list_data.append(out_list)

            out_list.num = 1
            out_list.region_nr = orges_list.region_nr
            out_list.str = out_list.str + to_string(orges_list.nationality, "x(30)") +\
                    to_string(orges_list.B_totRmNights, " >>>>9") +\
                    to_string(orges_list.B_groupRmNights, " >>>>9") +\
                    to_string(orges_list.B_individualRmNights, " >>>>9") +\
                    to_string(orges_list.L_totRmNights, " >>>>9") +\
                    to_string(orges_list.L_groupRmNights, " >>>>9") +\
                    to_string(orges_list.L_individualRmNights, " >>>>9") +\
                    to_string(orges_list.MTD_BtotRmNights, " >>>>9") +\
                    to_string(orges_list.MTD_BgroupRmNights, " >>>>9") +\
                    to_string(orges_list.MTD_BindividualRmNights, " >>>>9") +\
                    to_string(orges_list.MTD_LtotRmNights, " >>>>9") +\
                    to_string(orges_list.MTD_LgroupRmNights, " >>>>9") +\
                    to_string(orges_list.MTD_LindividualRmNights, " >>>>9") +\
                    to_string(orges_list.pmtd_btotrmnights, " >>9.99") +\
                    to_string(orges_list.pmtd_bgrouprmnights, " >>9.99") +\
                    to_string(orges_list.pmtd_bindividualrmnights, " >>9.99") +\
                    to_string(orges_list.pmtd_ltotrmnights, " >>9.99") +\
                    to_string(orges_list.pmtd_lgrouprmnights, " >>9.99") +\
                    to_string(orges_list.pmtd_lindividualrmnights, " >>9.99") +\
                    to_string(orges_list.subtotal_date, " >>>>9") +\
                    to_string(orges_list.subtotal_MTD, " >>>>9") +\
                    to_string(orges_list.psubtotal_date, " >>9.99") +\
                    to_string(orges_list.psubtotal_mtd, " >>9.99")


        out_list = Out_list()
        out_list_data.append(out_list)

        out_list.num = 9999
        out_list.region_nr = 999
        out_list.str = out_list.str + to_string("SUB TOTAL", "x(30)") +\
                to_string(subtot_b, " >>>>9") +\
                to_string(tot_b_grup, " >>>>9") +\
                to_string(tot_b_individual, " >>>>9") +\
                to_string(subtot_l, " >>>>9") +\
                to_string(tot_l_grup, " >>>>9") +\
                to_string(tot_l_individual, " >>>>9") +\
                to_string(mtdsubtot_b, " >>>>9") +\
                to_string(mtdtot_b_grup, " >>>>9") +\
                to_string(mtdtot_b_individual, " >>>>9") +\
                to_string(mtdsubtot_l, " >>>>9") +\
                to_string(mtdtot_l_grup, " >>>>9") +\
                to_string(mtdtot_l_individual, " >>>>9") +\
                to_string(pmtd_btotrmnights, " >>9.99") +\
                to_string(pmtd_bgrouprmnights, " >>9.99") +\
                to_string(pmtd_bindividualrmnights, " >>9.99") +\
                to_string(pmtd_ltotrmnights, " >>9.99") +\
                to_string(pmtd_lgrouprmnights, " >>9.99") +\
                to_string(pmtd_lindividualrmnights, " >>9.99") +\
                to_string(subtot_date, " >>>>9") +\
                to_string(subtot_mtd, " >>>>9") +\
                to_string(psubtotal_date, " >>9.99") +\
                to_string(psubtotal_mtd, " >>9.99")


        out_list = Out_list()
        out_list_data.append(out_list)

        out_list.num = 9999
        out_list.region_nr = 9999
        out_list.str = out_list.str + to_string("G. TOTAL of ROOM NIGHTS : " + to_string(to_int(subtot_b + subtot_l)) , "x(30)")


    def create_list1():

        nonlocal out_list_data, out_list1_data, tot_b_individual, tot_b_grup, tot_l_individual, tot_l_grup, mtdtot_b_individual, mtdtot_b_grup, mtdtot_l_individual, mtdtot_l_grup, ytdtot_b_individual, ytdtot_b_grup, ytdtot_l_individual, ytdtot_l_grup, subtot_b, subtot_l, ytdsubtot_b, ytdsubtot_l, mtdsubtot_b, mtdsubtot_l, subtot_date, subtot_mtd, subtot_ytd, pmtd_btotrmnights, pmtd_bgrouprmnights, pmtd_bindividualrmnights, pmtd_ltotrmnights, pmtd_lgrouprmnights, pmtd_lindividualrmnights, pytd_btotrmnights, pytd_bgrouprmnights, pytd_bindividualrmnights, pytd_ltotrmnights, pytd_lgrouprmnights, pytd_lindividualrmnights, psubtotal_date, psubtotal_mtd, psubtotal_ytd, segm__purcode, i, str, from_date, jan1, mtd1, queasy, nation, genstat, reservation
        nonlocal fdate, to_date, show_ytd


        nonlocal orges_list, region_list, out_list, out_list1
        nonlocal orges_list_data, region_list_data, out_list_data, out_list1_data


        out_list_data.clear()
        out_list1_data.clear()
        region_list_data.clear()
        orges_list_data.clear()
        tot_b_individual = 0
        tot_b_grup = 0
        tot_l_individual = 0
        tot_l_grup = 0
        mtdtot_b_individual = 0
        mtdtot_b_grup = 0
        mtdtot_l_individual = 0
        mtdtot_l_grup = 0
        ytdtot_b_individual = 0
        ytdtot_b_grup = 0
        ytdtot_l_individual = 0
        ytdtot_l_grup = 0
        subtot_b = 0
        subtot_l = 0
        mtdsubtot_b = 0
        mtdsubtot_l = 0
        ytdsubtot_b = 0
        ytdsubtot_l = 0
        subtot_date = 0
        subtot_mtd = 0
        subtot_ytd = 0
        pmtd_btotrmnights =  to_decimal("0")
        pmtd_bgrouprmnights =  to_decimal("0")
        pmtd_bindividualrmnights =  to_decimal("0")
        pmtd_ltotrmnights =  to_decimal("0")
        pmtd_lgrouprmnights =  to_decimal("0")
        pmtd_lindividualrmnights =  to_decimal("0")
        pytd_btotrmnights =  to_decimal("0")
        pytd_bgrouprmnights =  to_decimal("0")
        pytd_bindividualrmnights =  to_decimal("0")
        pytd_ltotrmnights =  to_decimal("0")
        pytd_lgrouprmnights =  to_decimal("0")
        pytd_lindividualrmnights =  to_decimal("0")
        psubtotal_date =  to_decimal("0")
        psubtotal_mtd =  to_decimal("0")
        psubtotal_ytd =  to_decimal("0")

        for queasy in db_session.query(Queasy).filter(
                 (Queasy.key == 6)).order_by(Queasy._recid).all():
            region_list = Region_list()
            region_list_data.append(region_list)

            region_list.nationality = queasy.char1
            region_list.region_nr = queasy.number1

        genstat_obj_list = {}
        for genstat, nation in db_session.query(Genstat, Nation).join(Nation,(Nation.nationnr == Genstat.nationnr)).filter(
                 (Genstat.datum >= from_date) & (Genstat.datum <= to_date) & (Genstat.resstatus != 13) & (Genstat.segmentcode != 0) & (Genstat.nationnr != 0) & (Genstat.zinr != "") & (Genstat.res_logic[inc_value(1)]) & (matches(Genstat.res_char[inc_value(1)],("*SEGM_PUR*")))).order_by(Genstat._recid).all():
            region_list = query(region_list_data, (lambda region_list: region_list.region_nr == nation.untergruppe), first=True)
            if not region_list:
                continue

            if genstat_obj_list.get(genstat._recid):
                continue
            else:
                genstat_obj_list[genstat._recid] = True

            orges_list = query(orges_list_data, filters=(lambda orges_list: orges_list.nationnr == nation.nationnr), first=True)

            if not orges_list:
                orges_list = Orges_list()
                orges_list_data.append(orges_list)

                orges_list.region_nr = region_list.region_nr
                orges_list.nationnr = nation.nationnr
                orges_list.nationality = nation.bezeich


            for i in range(1,num_entries(genstat.res_char[1], ";") - 1 + 1) :
                str = entry(i - 1, genstat.res_char[1], ";")

                if substring(str, 0, 8) == ("SEGM_PUR").lower() :
                    segm__purcode = to_int(substring(str, 8))

            queasy = get_cache (Queasy, {"key": [(eq, 143)],"number1": [(eq, segm__purcode)]})

            if matches(queasy.char1,r"BS"):

                if genstat.datum >= fdate and genstat.datum <= to_date:
                    region_list.b_totrmnights = region_list.b_totrmnights + 1
                    orges_list.b_totrmnights = orges_list.b_totrmnights + 1

                    reservation = get_cache (Reservation, {"resnr": [(eq, genstat.resnr)]})

                    if reservation and (to_int(reservation.grpflag) + 1) == 2:
                        region_list.b_grouprmnights = region_list.b_grouprmnights + 1
                        orges_list.b_grouprmnights = orges_list.b_grouprmnights + 1
                        tot_b_grup = tot_b_grup + 1
                    else:
                        region_list.b_individualrmnights = region_list.b_individualrmnights + 1
                        orges_list.b_individualrmnights = orges_list.b_individualrmnights + 1
                        tot_b_individual = tot_b_individual + 1

                if get_month(genstat.datum) == get_month(to_date):
                    region_list.mtd_btotrmnights = region_list.mtd_btotrmnights + 1
                    orges_list.mtd_btotrmnights = orges_list.mtd_btotrmnights + 1

                    reservation = get_cache (Reservation, {"resnr": [(eq, genstat.resnr)]})

                    if reservation and (to_int(reservation.grpflag) + 1) == 2:
                        region_list.mtd_bgrouprmnights = region_list.mtd_bgrouprmnights + 1
                        orges_list.mtd_bgrouprmnights = orges_list.mtd_bgrouprmnights + 1
                        mtdtot_b_grup = mtdtot_b_grup + 1
                    else:
                        region_list.mtd_bindividualrmnights = region_list.mtd_bindividualrmnights + 1
                        orges_list.mtd_bindividualrmnights = orges_list.mtd_bindividualrmnights + 1
                        mtdtot_b_individual = mtdtot_b_individual + 1

                if genstat.datum >= jan1 and genstat.datum <= to_date:
                    region_list.ytd_btotrmnights = region_list.ytd_btotrmnights + 1
                    orges_list.ytd_btotrmnights = orges_list.ytd_btotrmnights + 1

                    reservation = get_cache (Reservation, {"resnr": [(eq, genstat.resnr)]})

                    if reservation and (to_int(reservation.grpflag) + 1) == 2:
                        region_list.ytd_bgrouprmnights = region_list.ytd_bgrouprmnights + 1
                        orges_list.ytd_bgrouprmnights = orges_list.ytd_bgrouprmnights + 1
                        ytdtot_b_grup = ytdtot_b_grup + 1
                    else:
                        region_list.ytd_bindividualrmnights = region_list.ytd_bindividualrmnights + 1
                        orges_list.ytd_bindividualrmnights = orges_list.ytd_bindividualrmnights + 1
                        ytdtot_b_individual = ytdtot_b_individual + 1

            elif matches(queasy.char1,r"LS"):

                if genstat.datum >= fdate and genstat.datum <= to_date:
                    region_list.l_totrmnights = region_list.l_totrmnights + 1
                    orges_list.l_totrmnights = orges_list.l_totrmnights + 1

                    reservation = get_cache (Reservation, {"resnr": [(eq, genstat.resnr)]})

                    if reservation and (to_int(reservation.grpflag) + 1) == 2:
                        region_list.l_grouprmnights = region_list.l_grouprmnights + 1
                        orges_list.l_grouprmnights = orges_list.l_grouprmnights + 1
                        tot_l_grup = tot_l_grup + 1
                    else:
                        region_list.l_individualrmnights = region_list.l_individualrmnights + 1
                        orges_list.l_individualrmnights = orges_list.l_individualrmnights + 1
                        tot_l_individual = tot_l_individual + 1

                if get_month(genstat.datum) == get_month(to_date):
                    region_list.mtd_ltotrmnights = region_list.mtd_ltotrmnights + 1
                    orges_list.mtd_ltotrmnights = orges_list.mtd_ltotrmnights + 1

                    reservation = get_cache (Reservation, {"resnr": [(eq, genstat.resnr)]})

                    if reservation and (to_int(reservation.grpflag) + 1) == 2:
                        region_list.mtd_lgrouprmnights = region_list.mtd_lgrouprmnights + 1
                        orges_list.mtd_lgrouprmnights = orges_list.mtd_lgrouprmnights + 1
                        mtdtot_l_grup = mtdtot_l_grup + 1
                    else:
                        region_list.mtd_lindividualrmnights = region_list.mtd_lindividualrmnights + 1
                        orges_list.mtd_lindividualrmnights = orges_list.mtd_lindividualrmnights + 1
                        mtdtot_l_individual = mtdtot_l_individual + 1

                if genstat.datum >= jan1 and genstat.datum <= to_date:
                    region_list.ytd_ltotrmnights = region_list.ytd_ltotrmnights + 1
                    orges_list.ytd_ltotrmnights = orges_list.ytd_ltotrmnights + 1

                    reservation = get_cache (Reservation, {"resnr": [(eq, genstat.resnr)]})

                    if reservation and (to_int(reservation.grpflag) + 1) == 2:
                        region_list.ytd_lgrouprmnights = region_list.ytd_lgrouprmnights + 1
                        orges_list.ytd_lgrouprmnights = orges_list.ytd_lgrouprmnights + 1
                        ytdtot_l_grup = ytdtot_l_grup + 1
                    else:
                        region_list.ytd_lindividualrmnights = region_list.ytd_lindividualrmnights + 1
                        orges_list.ytd_lindividualrmnights = orges_list.ytd_lindividualrmnights + 1
                        ytdtot_l_individual = ytdtot_l_individual + 1
        subtot_b = tot_b_grup + tot_b_individual
        subtot_l = tot_l_grup + tot_l_individual
        mtdsubtot_b = mtdtot_b_grup + mtdtot_b_individual
        mtdsubtot_l = mtdtot_l_grup + mtdtot_l_individual
        ytdsubtot_b = ytdtot_b_grup + ytdtot_b_individual
        ytdsubtot_l = ytdtot_l_grup + ytdtot_l_individual
        subtot_date = subtot_b + subtot_l
        subtot_mtd = mtdsubtot_b + mtdsubtot_l
        subtot_ytd = ytdsubtot_b + ytdsubtot_l

        for orges_list in query(orges_list_data, sort_by=[("region_nr",False)]):
            region_list = query(region_list_data, (lambda region_list: region_list.region_nr == orges_list.region_nr), first=True)
            if not region_list:
                continue

            region_list.subtotal_date = region_list.B_totRmNights + region_list.L_totRmNights
            region_list.subtotal_mtd = region_list.MTD_BtotRmNights + region_list.MTD_LtotRmNights
            region_list.subtotal_ytd = region_list.YTD_BtotRmNights + region_list.YTD_LtotRmNights
            orges_list.subtotal_date = orges_list.B_totRmNights + orges_list.L_totRmNights
            orges_list.subtotal_mtd = orges_list.MTD_BtotRmNights + orges_list.MTD_LtotRmNights
            orges_list.subtotal_ytd = orges_list.YTD_BtotRmNights + orges_list.YTD_LtotRmNights
            region_list.pmtd_btotrmnights = ( to_decimal(region_list.MTD_BtotRmNights) / to_decimal(mtdsubtot_b)) * to_decimal(100.00)
            region_list.pmtd_bgrouprmnights = ( to_decimal(region_list.MTD_BgroupRmNights) / to_decimal(mtdtot_b_grup)) * to_decimal(100.00)
            region_list.pmtd_bindividualrmnights = ( to_decimal(region_list.MTD_BindividualRmNights) / to_decimal(mtdtot_b_individual)) * to_decimal(100.00)
            region_list.pmtd_ltotrmnights = ( to_decimal(region_list.MTD_LtotRmNights) / to_decimal(mtdsubtot_l)) * to_decimal(100.00)
            region_list.pmtd_lgrouprmnights = ( to_decimal(region_list.MTD_LgroupRmNights) / to_decimal(mtdtot_l_grup)) * to_decimal(100.00)
            region_list.pmtd_lindividualrmnights = ( to_decimal(region_list.MTD_LindividualRmNights) / to_decimal(mtdtot_l_individual)) * to_decimal(100.00)
            region_list.psubtotal_date = ( to_decimal(region_list.subtotal_date) / to_decimal(subtot_date)) * to_decimal(100.00)
            region_list.psubtotal_mtd = ( to_decimal(region_list.subtotal_MTD) / to_decimal(subtot_mtd)) * to_decimal(100.00)
            orges_list.pmtd_btotrmnights = ( to_decimal(orges_list.MTD_BtotRmNights) / to_decimal(mtdsubtot_b)) * to_decimal(100.00)
            orges_list.pmtd_bgrouprmnights = ( to_decimal(orges_list.MTD_BgroupRmNights) / to_decimal(mtdtot_b_grup)) * to_decimal(100.00)
            orges_list.pmtd_bindividualrmnights = ( to_decimal(orges_list.MTD_BindividualRmNights) / to_decimal(mtdtot_b_individual)) * to_decimal(100.00)
            orges_list.pmtd_ltotrmnights = ( to_decimal(orges_list.MTD_LtotRmNights) / to_decimal(mtdsubtot_l)) * to_decimal(100.00)
            orges_list.pmtd_lgrouprmnights = ( to_decimal(orges_list.MTD_LgroupRmNights) / to_decimal(mtdtot_l_grup)) * to_decimal(100.00)
            orges_list.pmtd_lindividualrmnights = ( to_decimal(orges_list.MTD_LindividualRmNights) / to_decimal(mtdtot_l_individual)) * to_decimal(100.00)
            orges_list.psubtotal_date = ( to_decimal(orges_list.subtotal_date) / to_decimal(subtot_date)) * to_decimal(100.00)
            orges_list.psubtotal_mtd = ( to_decimal(orges_list.subtotal_MTD) / to_decimal(subtot_mtd)) * to_decimal(100.00)
            region_list.pytd_btotrmnights = ( to_decimal(region_list.YTD_BtotRmNights) / to_decimal(ytdsubtot_b)) * to_decimal(100.00)
            region_list.pytd_bgrouprmnights = ( to_decimal(region_list.YTD_BgroupRmNights) / to_decimal(ytdtot_b_grup)) * to_decimal(100.00)
            region_list.pytd_bindividualrmnights = ( to_decimal(region_list.YTD_BindividualRmNights) / to_decimal(ytdtot_b_individual)) * to_decimal(100.00)
            region_list.pytd_ltotrmnights = ( to_decimal(region_list.YTD_LtotRmNights) / to_decimal(ytdsubtot_l)) * to_decimal(100.00)
            region_list.pytd_lgrouprmnights = ( to_decimal(region_list.YTD_LgroupRmNights) / to_decimal(ytdtot_l_grup)) * to_decimal(100.00)
            region_list.pytd_lindividualrmnights = ( to_decimal(region_list.YTD_LindividualRmNights) / to_decimal(ytdtot_l_individual)) * to_decimal(100.00)
            region_list.psubtotal_ytd = ( to_decimal(region_list.subtotal_YTD) / to_decimal(subtot_ytd)) * to_decimal(100.00)
            orges_list.pytd_btotrmnights = ( to_decimal(orges_list.YTD_BtotRmNights) / to_decimal(ytdsubtot_b)) * to_decimal(100.00)
            orges_list.pytd_bgrouprmnights = ( to_decimal(orges_list.YTD_BgroupRmNights) / to_decimal(ytdtot_b_grup)) * to_decimal(100.00)
            orges_list.pytd_bindividualrmnights = ( to_decimal(orges_list.YTD_BindividualRmNights) / to_decimal(ytdtot_b_individual)) * to_decimal(100.00)
            orges_list.pytd_ltotrmnights = ( to_decimal(orges_list.YTD_LtotRmNights) / to_decimal(ytdsubtot_l)) * to_decimal(100.00)
            orges_list.pytd_lgrouprmnights = ( to_decimal(orges_list.YTD_LgroupRmNights) / to_decimal(ytdtot_l_grup)) * to_decimal(100.00)
            orges_list.pytd_lindividualrmnights = ( to_decimal(orges_list.YTD_LindividualRmNights) / to_decimal(ytdtot_l_individual)) * to_decimal(100.00)
            orges_list.psubtotal_ytd = ( to_decimal(orges_list.subtotal_YTD) / to_decimal(subtot_ytd)) * to_decimal(100.00)

            if region_list.pmtd_btotrmnights == None:
                region_list.pmtd_btotrmnights =  to_decimal(0.00)

            if region_list.pmtd_bgrouprmnights == None:
                region_list.pmtd_bgrouprmnights =  to_decimal(0.00)

            if region_list.pmtd_bindividualrmnights == None:
                region_list.pmtd_bindividualrmnights =  to_decimal(0.00)

            if region_list.pmtd_ltotrmnights == None:
                region_list.pmtd_ltotrmnights =  to_decimal(0.00)

            if region_list.pmtd_lgrouprmnights == None:
                region_list.pmtd_lgrouprmnights =  to_decimal(0.00)

            if region_list.pmtd_lindividualrmnights == None:
                region_list.pmtd_lindividualrmnights =  to_decimal(0.00)

            if region_list.psubtotal_date == None:
                region_list.psubtotal_date =  to_decimal(0.00)

            if region_list.psubtotal_mtd == None:
                region_list.psubtotal_mtd =  to_decimal(0.00)

            if orges_list.pmtd_btotrmnights == None:
                orges_list.pmtd_btotrmnights =  to_decimal(0.00)

            if orges_list.pmtd_bgrouprmnights == None:
                orges_list.pmtd_bgrouprmnights =  to_decimal(0.00)

            if orges_list.pmtd_bindividualrmnights == None:
                orges_list.pmtd_bindividualrmnights =  to_decimal(0.00)

            if orges_list.pmtd_ltotrmnights == None:
                orges_list.pmtd_ltotrmnights =  to_decimal(0.00)

            if orges_list.pmtd_lgrouprmnights == None:
                orges_list.pmtd_lgrouprmnights =  to_decimal(0.00)

            if orges_list.pmtd_lindividualrmnights == None:
                orges_list.pmtd_lindividualrmnights =  to_decimal(0.00)

            if orges_list.psubtotal_date == None:
                orges_list.psubtotal_date =  to_decimal(0.00)

            if orges_list.psubtotal_mtd == None:
                orges_list.psubtotal_mtd =  to_decimal(0.00)

            if region_list.pytd_btotrmnights == None:
                region_list.pytd_btotrmnights =  to_decimal(0.00)

            if region_list.pytd_bgrouprmnights == None:
                region_list.pytd_bgrouprmnights =  to_decimal(0.00)

            if region_list.pytd_bindividualrmnights == None:
                region_list.pytd_bindividualrmnights =  to_decimal(0.00)

            if region_list.pytd_ltotrmnights == None:
                region_list.pytd_ltotrmnights =  to_decimal(0.00)

            if region_list.pytd_lgrouprmnights == None:
                region_list.pytd_lgrouprmnights =  to_decimal(0.00)

            if region_list.pytd_lindividualrmnights == None:
                region_list.pytd_lindividualrmnights =  to_decimal(0.00)

            if region_list.psubtotal_ytd == None:
                region_list.psubtotal_ytd =  to_decimal(0.00)

            if orges_list.pytd_btotrmnights == None:
                orges_list.pytd_btotrmnights =  to_decimal(0.00)

            if orges_list.pytd_bgrouprmnights == None:
                orges_list.pytd_bgrouprmnights =  to_decimal(0.00)

            if orges_list.pytd_bindividualrmnights == None:
                orges_list.pytd_bindividualrmnights =  to_decimal(0.00)

            if orges_list.pytd_ltotrmnights == None:
                orges_list.pytd_ltotrmnights =  to_decimal(0.00)

            if orges_list.pytd_lgrouprmnights == None:
                orges_list.pytd_lgrouprmnights =  to_decimal(0.00)

            if orges_list.pytd_lindividualrmnights == None:
                orges_list.pytd_lindividualrmnights =  to_decimal(0.00)

            if orges_list.psubtotal_ytd == None:
                orges_list.psubtotal_ytd =  to_decimal(0.00)

            out_list1 = query(out_list1_data, filters=(lambda out_list1: out_list1.num == 999 and out_list1.region_nr == orges_list.region_nr), first=True)

            if not out_list1:
                out_list1 = Out_list1()
                out_list1_data.append(out_list1)

                out_list1.num = 999
                out_list1.region_nr = region_list.region_nr


                out_list1.str = out_list1.str + to_string("** " + region_list.nationality + " **", "x(30)") + to_string(region_list.B_totRmNights, " >>>>9") + to_string(region_list.B_groupRmNights, " >>>>9") + to_string(region_list.B_individualRmNights, " >>>>9") + to_string(region_list.L_totRmNights, " >>>>9") + to_string(region_list.L_groupRmNights, " >>>>9") + to_string(region_list.L_individualRmNights, " >>>>9") + to_string(region_list.MTD_BtotRmNights, " >>>>9") + to_string(region_list.MTD_BgroupRmNights, " >>>>9") + to_string(region_list.MTD_BindividualRmNights, " >>>>9") + to_string(region_list.MTD_LtotRmNights, " >>>>9") + to_string(region_list.MTD_LgroupRmNights, " >>>>9") + to_string(region_list.MTD_LindividualRmNights, " >>>>9") + to_string(region_list.pmtd_btotrmnights, " >>9.99") + to_string(region_list.pmtd_bgrouprmnights, " >>9.99") + to_string(region_list.pmtd_bindividualrmnights, " >>9.99") + to_string(region_list.pmtd_ltotrmnights, " >>9.99") + to_string(region_list.pmtd_lgrouprmnights, " >>9.99") + to_string(region_list.pmtd_lindividualrmnights, " >>9.99") + to_string(region_list.subtotal_date, " >>>>9") + to_string(region_list.subtotal_MTD, " >>>>9") + to_string(region_list.psubtotal_date, " >>9.99") + to_string(region_list.psubtotal_ytd, " >>9.99") + to_string(region_list.YTD_BtotRmNights, " >>>>9") + to_string(region_list.YTD_BgroupRmNights, " >>>>9") + to_string(region_list.YTD_BindividualRmNights, " >>>>9") + to_string(region_list.YTD_LtotRmNights, " >>>>9") + to_string(region_list.YTD_LgroupRmNights, " >>>>9") + to_string(region_list.YTD_LindividualRmNights, " >>>>9") + to_string(region_list.pytd_btotrmnights, " >>9.99") + to_string(region_list.pytd_bgrouprmnights, " >>9.99") + to_string(region_list.pytd_bindividualrmnights, " >>9.99") + to_string(region_list.pytd_ltotrmnights, " >>9.99") + to_string(region_list.pytd_lgrouprmnights, " >>9.99") + to_string(region_list.pytd_lindividualrmnights, " >>9.99") + to_string(region_list.subtotal_YTD, " >>>>9") + to_string(region_list.psubtotal_ytd, " >>9.99")
                out_list1 = Out_list1()
                out_list1_data.append(out_list1)

                out_list1.num = 9999
                out_list1.region_nr = region_list.region_nr


            pmtd_btotrmnights =  to_decimal(pmtd_btotrmnights) + to_decimal(orges_list.pmtd_btotrmnights)
            pmtd_bgrouprmnights =  to_decimal(pmtd_bgrouprmnights) + to_decimal(orges_list.pmtd_bgrouprmnights)
            pmtd_bindividualrmnights =  to_decimal(pmtd_bindividualrmnights) + to_decimal(orges_list.pmtd_bindividualrmnights)
            pmtd_ltotrmnights =  to_decimal(pmtd_ltotrmnights) + to_decimal(orges_list.pmtd_ltotrmnights)
            pmtd_lgrouprmnights =  to_decimal(pmtd_lgrouprmnights) + to_decimal(orges_list.pmtd_lgrouprmnights)
            pmtd_lindividualrmnights =  to_decimal(pmtd_lindividualrmnights) + to_decimal(orges_list.pmtd_lindividualrmnights)
            pytd_btotrmnights =  to_decimal(pytd_btotrmnights) + to_decimal(orges_list.pytd_btotrmnights)
            pytd_bgrouprmnights =  to_decimal(pytd_bgrouprmnights) + to_decimal(orges_list.pytd_bgrouprmnights)
            pytd_bindividualrmnights =  to_decimal(pytd_bindividualrmnights) + to_decimal(orges_list.pytd_bindividualrmnights)
            pytd_ltotrmnights =  to_decimal(pytd_ltotrmnights) + to_decimal(orges_list.pytd_ltotrmnights)
            pytd_lgrouprmnights =  to_decimal(pytd_lgrouprmnights) + to_decimal(orges_list.pytd_lgrouprmnights)
            pytd_lindividualrmnights =  to_decimal(pytd_lindividualrmnights) + to_decimal(orges_list.pytd_lindividualrmnights)
            psubtotal_date =  to_decimal(psubtotal_date) + to_decimal(orges_list.psubtotal_date)
            psubtotal_mtd =  to_decimal(psubtotal_mtd) + to_decimal(orges_list.psubtotal_mtd)
            psubtotal_ytd =  to_decimal(psubtotal_ytd) + to_decimal(orges_list.psubtotal_ytd)


            out_list1 = Out_list1()
            out_list1_data.append(out_list1)

            out_list1.num = 1
            out_list1.region_nr = orges_list.region_nr
            out_list1.str = out_list1.str + to_string(orges_list.nationality, "x(30)") +\
                    to_string(orges_list.B_totRmNights, " >>>>9") +\
                    to_string(orges_list.B_groupRmNights, " >>>>9") +\
                    to_string(orges_list.B_individualRmNights, " >>>>9") +\
                    to_string(orges_list.L_totRmNights, " >>>>9") +\
                    to_string(orges_list.L_groupRmNights, " >>>>9") +\
                    to_string(orges_list.L_individualRmNights, " >>>>9") +\
                    to_string(orges_list.MTD_BtotRmNights, " >>>>9") +\
                    to_string(orges_list.MTD_BgroupRmNights, " >>>>9") +\
                    to_string(orges_list.MTD_BindividualRmNights, " >>>>9") +\
                    to_string(orges_list.MTD_LtotRmNights, " >>>>9") +\
                    to_string(orges_list.MTD_LgroupRmNights, " >>>>9") +\
                    to_string(orges_list.MTD_LindividualRmNights, " >>>>9") +\
                    to_string(orges_list.pmtd_btotrmnights, " >>9.99") +\
                    to_string(orges_list.pmtd_bgrouprmnights, " >>9.99") +\
                    to_string(orges_list.pmtd_bindividualrmnights, " >>9.99") +\
                    to_string(orges_list.pmtd_ltotrmnights, " >>9.99") +\
                    to_string(orges_list.pmtd_lgrouprmnights, " >>9.99") +\
                    to_string(orges_list.pmtd_lindividualrmnights, " >>9.99") +\
                    to_string(orges_list.subtotal_date, " >>>>9") +\
                    to_string(orges_list.subtotal_MTD, " >>>>9") +\
                    to_string(orges_list.psubtotal_date, " >>9.99") +\
                    to_string(orges_list.psubtotal_mtd, " >>9.99") +\
                    to_string(orges_list.YTD_BtotRmNights, " >>>>9") +\
                    to_string(orges_list.YTD_BgroupRmNights, " >>>>9") +\
                    to_string(orges_list.YTD_BindividualRmNights, " >>>>9") +\
                    to_string(orges_list.YTD_LtotRmNights, " >>>>9") +\
                    to_string(orges_list.YTD_LgroupRmNights, " >>>>9") +\
                    to_string(orges_list.YTD_LindividualRmNights, " >>>>9") +\
                    to_string(orges_list.pytd_btotrmnights, " >>9.99") +\
                    to_string(orges_list.pytd_bgrouprmnights, " >>9.99") +\
                    to_string(orges_list.pytd_bindividualrmnights, " >>9.99") +\
                    to_string(orges_list.pytd_ltotrmnights, " >>9.99") +\
                    to_string(orges_list.pytd_lgrouprmnights, " >>9.99") +\
                    to_string(orges_list.pytd_lindividualrmnights, " >>9.99") +\
                    to_string(orges_list.subtotal_YTD, " >>>>9") +\
                    to_string(orges_list.psubtotal_ytd, " >>9.99")


        out_list1 = Out_list1()
        out_list1_data.append(out_list1)

        out_list1.num = 9999
        out_list1.region_nr = 999
        out_list1.str = out_list1.str + to_string("SUB TOTAL", "x(30)") +\
                to_string(subtot_b, " >>>>9") +\
                to_string(tot_b_grup, " >>>>9") +\
                to_string(tot_b_individual, " >>>>9") +\
                to_string(subtot_l, " >>>>9") +\
                to_string(tot_l_grup, " >>>>9") +\
                to_string(tot_l_individual, " >>>>9") +\
                to_string(mtdsubtot_b, " >>>>9") +\
                to_string(mtdtot_b_grup, " >>>>9") +\
                to_string(mtdtot_b_individual, " >>>>9") +\
                to_string(mtdsubtot_l, " >>>>9") +\
                to_string(mtdtot_l_grup, " >>>>9") +\
                to_string(mtdtot_l_individual, " >>>>9") +\
                to_string(pmtd_btotrmnights, " >>9.99") +\
                to_string(pmtd_bgrouprmnights, " >>9.99") +\
                to_string(pmtd_bindividualrmnights, " >>9.99") +\
                to_string(pmtd_ltotrmnights, " >>9.99") +\
                to_string(pmtd_lgrouprmnights, " >>9.99") +\
                to_string(pmtd_lindividualrmnights, " >>9.99") +\
                to_string(subtot_date, " >>>>9") +\
                to_string(subtot_mtd, " >>>>9") +\
                to_string(psubtotal_date, " >>9.99") +\
                to_string(psubtotal_mtd, " >>9.99") +\
                to_string(ytdsubtot_b, " >>>>9") +\
                to_string(ytdtot_b_grup, " >>>>9") +\
                to_string(ytdtot_b_individual, " >>>>9") +\
                to_string(ytdsubtot_l, " >>>>9") +\
                to_string(ytdtot_l_grup, " >>>>9") +\
                to_string(ytdtot_l_individual, " >>>>9") +\
                to_string(pytd_btotrmnights, " >>9.99") +\
                to_string(pytd_bgrouprmnights, " >>9.99") +\
                to_string(pytd_bindividualrmnights, " >>9.99") +\
                to_string(pytd_ltotrmnights, " >>9.99") +\
                to_string(pytd_lgrouprmnights, " >>9.99") +\
                to_string(pytd_lindividualrmnights, " >>9.99") +\
                to_string(subtot_ytd, " >>>>9") +\
                to_string(psubtotal_ytd, " >>9.99")


        out_list1 = Out_list1()
        out_list1_data.append(out_list1)

        out_list1.num = 9999
        out_list1.region_nr = 9999
        out_list1.str = out_list1.str + to_string("G. TOTAL of ROOM NIGHTS : " + to_string(to_int(subtot_b + subtot_l)) , "x(30)")


    jan1 = date_mdy(1, 1, get_year(to_date))
    mtd1 = date_mdy(get_month(to_date) , 1, get_year(to_date))

    if show_ytd:
        from_date = jan1
        create_list1()
    else:
        from_date = fdate
        create_list()

    return generate_output()