#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from functions.get_room_breakdown import get_room_breakdown
from models import Htparam, Genstat, Guest, Waehrung, Reservation, Res_line

def rm_stat3_1bl(segmno:int, gastno:int, fr_date:date, to_date:date):

    prepare_cache ([Htparam, Genstat, Guest, Waehrung, Res_line])

    t_list_list = []
    ci_date:date = None
    htparam = genstat = guest = waehrung = reservation = res_line = None

    t_list = None

    t_list_list, T_list = create_model("T_list", {"gastnr":int, "gname":string, "nat":string, "zinr":string, "erwachs":int, "kind1":int, "gratis":int, "zipreis":Decimal, "curr":string, "resnr":int, "reslinnr":int, "ankunft":date, "abreise":date, "dlodge":Decimal, "drate":Decimal}, {"ankunft": None, "abreise": None})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal t_list_list, ci_date, htparam, genstat, guest, waehrung, reservation, res_line
        nonlocal segmno, gastno, fr_date, to_date


        nonlocal t_list
        nonlocal t_list_list

        return {"t-list": t_list_list}

    def create_list(f_date:date, t_date:date):

        nonlocal t_list_list, ci_date, htparam, genstat, guest, waehrung, reservation, res_line
        nonlocal segmno, gastno, fr_date, to_date


        nonlocal t_list
        nonlocal t_list_list

        for genstat in db_session.query(Genstat).filter(
                 (Genstat.gastnr == gastno) & (Genstat.datum >= f_date) & (Genstat.datum <= t_date) & (Genstat.segmentcode == segmno) & ((Genstat.erwachs + Genstat.kind1) > 0) & (Genstat.gastnr > 0) & (Genstat.res_logic[inc_value(1)])).order_by(Genstat._recid).all():

            t_list = query(t_list_list, filters=(lambda t_list: t_list.resnr == genstat.resnr and t_list.reslinnr == genstat.res_int[0]), first=True)

            if not t_list:

                guest = get_cache (Guest, {"gastnr": [(eq, genstat.gastnrmember)]})

                waehrung = get_cache (Waehrung, {"waehrungsnr": [(eq, genstat.wahrungsnr)]})
                t_list = T_list()
                t_list_list.append(t_list)

                t_list.resnr = genstat.resnr
                t_list.reslinnr = genstat.res_int[0]
                t_list.gastnr = genstat.gastnrmember
                t_list.nat = guest.nation1
                t_list.zinr = genstat.zinr
                t_list.zipreis =  to_decimal(genstat.zipreis)
                t_list.erwachs = genstat.erwachs
                t_list.kind1 = genstat.kind1
                t_list.gratis = genstat.gratis

                if guest:
                    t_list.gname = guest.name + ", " + guest.vorname1 + ", " + guest.anrede1 + guest.anredefirma

                if waehrung:
                    t_list.curr = waehrung.wabkurz

            if t_list.ankunft == None or t_list.ankunft > genstat.res_date[0]:
                t_list.ankunft = genstat.res_date[0]

            if t_list.abreise == None or t_list.abreise < genstat.res_date[1]:
                t_list.abreise = genstat.res_date[1]
            t_list.dlodge =  to_decimal(t_list.dlodge) + to_decimal(genstat.logis)


    def create_list2(f_date:date, t_date:date):

        nonlocal t_list_list, ci_date, htparam, genstat, guest, waehrung, reservation, res_line
        nonlocal segmno, gastno, fr_date, to_date


        nonlocal t_list
        nonlocal t_list_list

        datum:date = None
        datum1:date = None
        datum2:date = None
        local_net_lodg:Decimal = to_decimal("0.0")
        net_lodg:Decimal = to_decimal("0.0")
        tot_breakfast:Decimal = to_decimal("0.0")
        tot_lunch:Decimal = to_decimal("0.0")
        tot_dinner:Decimal = to_decimal("0.0")
        tot_other:Decimal = to_decimal("0.0")
        tot_rmrev:Decimal = to_decimal("0.0")
        tot_vat:Decimal = to_decimal("0.0")
        tot_service:Decimal = to_decimal("0.0")

        res_line_obj_list = {}
        for res_line, reservation in db_session.query(Res_line, Reservation).join(Reservation,(Reservation.resnr == Res_line.resnr) & (Reservation.segmentcode == segmno)).filter(
                 ((Res_line.active_flag <= 1) & (Res_line.resstatus <= 13) & (Res_line.resstatus != 4) & (Res_line.resstatus != 8) & (Res_line.resstatus != 9) & (Res_line.resstatus != 10) & (Res_line.resstatus != 12) & (Res_line.active_flag <= 1) & (not_ (Res_line.ankunft > t_date)) & (not_ (Res_line.abreise < f_date))) | ((Res_line.active_flag == 2) & (Res_line.resstatus == 8) & (Res_line.ankunft == ci_date) & (Res_line.abreise == ci_date)) & (Res_line.gastnr == gastnr) & (Res_line.l_zuordnung[inc_value(2)] == 0)).order_by(Res_line._recid).all():
            if res_line_obj_list.get(res_line._recid):
                continue
            else:
                res_line_obj_list[res_line._recid] = True

            t_list = query(t_list_list, filters=(lambda t_list: t_list.resnr == res_line.resnr and t_list.reslinnr == res_line.reslinnr), first=True)

            if not t_list:

                guest = get_cache (Guest, {"gastnr": [(eq, res_line.gastnrmember)]})

                waehrung = get_cache (Waehrung, {"waehrungsnr": [(eq, res_line.betriebsnr)]})
                t_list = T_list()
                t_list_list.append(t_list)

                t_list.resnr = res_line.resnr
                t_list.reslinnr = res_line.reslinnr
                t_list.gastnr = res_line.gastnrmember
                t_list.zinr = res_line.zinr
                t_list.zipreis =  to_decimal(res_line.zipreis)
                t_list.erwachs = res_line.erwachs
                t_list.kind1 = res_line.kind1
                t_list.gratis = res_line.gratis

                if guest:
                    t_list.gname = guest.name + ", " + guest.vorname1 + ", " +\
                            guest.anrede1 + guest.anredefirma
                    t_list.nat = guest.nation1

                if waehrung:
                    t_list.curr = waehrung.wabkurz

            if t_list.ankunft == None or t_list.ankunft > res_line.ankunft:
                t_list.ankunft = res_line.ankunft

            if t_list.abreise == None or t_list.abreise < res_line.abreise:
                t_list.abreise = res_line.abreise

            if res_line.ankunft >= f_date:
                datum1 = res_line.ankunft
            else:
                datum1 = f_date

            if res_line.abreise <= t_date:
                datum2 = res_line.abreise - timedelta(days=1)
            else:
                datum2 = t_date
            for datum in date_range(datum1,datum2) :
                local_net_lodg =  to_decimal("0")
                net_lodg =  to_decimal("0")
                net_lodg, local_net_lodg, tot_breakfast, tot_lunch, tot_dinner, tot_other, tot_rmrev, tot_vat, tot_service = get_output(get_room_breakdown(res_line._recid, datum, 0, f_date))

                if tot_rmrev == 0:
                    local_net_lodg =  to_decimal("0")
                    net_lodg =  to_decimal("0")


                t_list.dlodge =  to_decimal(t_list.dlodge) + to_decimal(local_net_lodg)


    htparam = get_cache (Htparam, {"paramnr": [(eq, 87)]})
    ci_date = htparam.fdate

    if (fr_date < ci_date) and (to_date < ci_date):
        create_list(fr_date, to_date)

    if (fr_date < ci_date) and (to_date >= ci_date):
        create_list(fr_date, ci_date - 1)
        create_list2(ci_date, to_date)

    if (fr_date >= ci_date) and (to_date >= ci_date):
        create_list2(fr_date, to_date)

    return generate_output()