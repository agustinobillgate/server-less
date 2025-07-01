#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from functions.get_room_breakdown import get_room_breakdown
from models import Guest, Segment, Htparam, Genstat, Reservation, Res_line

def prepare_rm_stat2_1bl(gastno:int, segmcode:int, from_date:date, to_date:date, mi_ftd:bool):

    prepare_cache ([Guest, Segment, Htparam, Genstat, Res_line])

    avail_guest = False
    f_tittle = ""
    t_list_list = []
    ci_date:date = None
    guest = segment = htparam = genstat = reservation = res_line = None

    t_list = None

    t_list_list, T_list = create_model("T_list", {"gastnr":int, "mgastnr":int, "gname":string, "resnr":int, "reslinnr":int, "fdate":date, "tdate":date, "ankunft":date, "abreise":date, "zimmeranz":int, "dlodge":Decimal, "dnite":int, "drate":Decimal, "mlodge":Decimal, "mnite":int, "mrate":Decimal, "ylodge":Decimal, "ynite":int, "yrate":Decimal}, {"fdate": get_current_date(), "tdate": date_mdy(1, 1, 1900), "ankunft": None, "abreise": None})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal avail_guest, f_tittle, t_list_list, ci_date, guest, segment, htparam, genstat, reservation, res_line
        nonlocal gastno, segmcode, from_date, to_date, mi_ftd


        nonlocal t_list
        nonlocal t_list_list

        return {"avail_guest": avail_guest, "f_tittle": f_tittle, "t-list": t_list_list}

    def create_list(f_date:date, t_date:date):

        nonlocal avail_guest, f_tittle, t_list_list, ci_date, guest, segment, htparam, genstat, reservation, res_line
        nonlocal gastno, segmcode, from_date, to_date, mi_ftd


        nonlocal t_list
        nonlocal t_list_list

        for genstat in db_session.query(Genstat).filter(
                 (Genstat.gastnr == gastno) & (Genstat.datum >= f_date) & (Genstat.datum <= t_date) & (Genstat.segmentcode == segmcode) & (Genstat.res_logic[inc_value(1)]) & ((Genstat.erwachs + Genstat.kind1) > 0)).order_by(Genstat._recid).all():

            t_list = query(t_list_list, filters=(lambda t_list: t_list.resnr == genstat.resnr), first=True)

            if not t_list:
                t_list = T_list()
                t_list_list.append(t_list)

                t_list.resnr = genstat.resnr
                t_list.reslinnr = genstat.res_int[0]
                t_list.mgastnr = genstat.gastnrmember
                t_list.gastnr = genstat.gastnr

                if guest:
                    t_list.gname = guest.name + ", " + guest.vorname1 + ", " + guest.anrede1 + guest.anredefirma

            if t_list.ankunft == None or t_list.ankunft > genstat.res_date[0]:
                t_list.ankunft = genstat.res_date[0]

            if t_list.abreise == None or t_list.abreise < genstat.res_date[1]:
                t_list.abreise = genstat.res_date[1]

            if t_list.fdate > genstat.datum:
                t_list.fdate = genstat.datum

            if t_list.tdate < genstat.datum:
                t_list.tdate = genstat.datum

            if mi_ftd and f_date < ci_date:

                if genstat.datum == f_date:
                    t_list.dlodge =  to_decimal(t_list.dlodge) + to_decimal(genstat.logis)

                    if genstat.resstatus != 13:
                        t_list.dnite = t_list.dnite + 1

                if get_month(genstat.datum) == get_month(t_date) and get_year(genstat.datum) == get_year(t_date):
                    t_list.mlodge =  to_decimal(t_list.mlodge) + to_decimal(genstat.logis)

                    if genstat.resstatus != 13:
                        t_list.mnite = t_list.mnite + 1

                if genstat.datum >= f_date and genstat.datum <= t_date:
                    t_list.ylodge =  to_decimal(t_list.ylodge) + to_decimal(genstat.logis)

                    if genstat.resstatus != 13:
                        t_list.ynite = t_list.ynite + 1

            elif not mi_ftd and f_date < ci_date:

                if genstat.datum == to_date:
                    t_list.dlodge =  to_decimal(t_list.dlodge) + to_decimal(genstat.logis)

                    if genstat.resstatus != 13:
                        t_list.dnite = t_list.dnite + 1

                if get_year(genstat.datum) == get_year(t_date):

                    if get_month(genstat.datum) == get_month(t_date):
                        t_list.mlodge =  to_decimal(t_list.mlodge) + to_decimal(genstat.logis)

                        if genstat.resstatus != 13:
                            t_list.mnite = t_list.mnite + 1


                    t_list.ylodge =  to_decimal(t_list.ylodge) + to_decimal(genstat.logis)

                    if genstat.resstatus != 13:
                        t_list.ynite = t_list.ynite + 1

        for t_list in query(t_list_list):

            if t_list.dnite != 0:
                t_list.drate =  to_decimal(t_list.dlodge) / to_decimal(t_list.dnite)

            if t_list.mnite != 0:
                t_list.mrate =  to_decimal(t_list.mlodge) / to_decimal(t_list.mnite)

            if t_list.ynite != 0:
                t_list.yrate =  to_decimal(t_list.ylodge) / to_decimal(t_list.ynite)


    def create_list2(f_date:date, t_date:date):

        nonlocal avail_guest, f_tittle, t_list_list, ci_date, guest, segment, htparam, genstat, reservation, res_line
        nonlocal gastno, segmcode, from_date, to_date, mi_ftd


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
        for res_line, reservation in db_session.query(Res_line, Reservation).join(Reservation,(Reservation.resnr == Res_line.resnr) & (Reservation.segmentcode == segmcode)).filter(
                 ((Res_line.active_flag <= 1) & (Res_line.resstatus <= 13) & (Res_line.resstatus != 4) & (Res_line.resstatus != 8) & (Res_line.resstatus != 9) & (Res_line.resstatus != 10) & (Res_line.resstatus != 12) & (Res_line.active_flag <= 1) & (not_ (Res_line.ankunft > t_date)) & (not_ (Res_line.abreise < f_date))) | ((Res_line.active_flag == 2) & (Res_line.resstatus == 8) & (Res_line.ankunft == ci_date) & (Res_line.abreise == ci_date)) & (Res_line.gastnr == gastnr) & (Res_line.l_zuordnung[inc_value(2)] == 0)).order_by(Res_line._recid).all():
            if res_line_obj_list.get(res_line._recid):
                continue
            else:
                res_line_obj_list[res_line._recid] = True

            t_list = query(t_list_list, filters=(lambda t_list: t_list.resnr == res_line.resnr), first=True)

            if not t_list:
                t_list = T_list()
                t_list_list.append(t_list)

                t_list.resnr = res_line.resnr
                t_list.reslinnr = res_line.reslinnr
                t_list.mgastnr = res_line.gastnrmember
                t_list.gastnr = res_line.gastnr

                if guest:
                    t_list.gname = guest.name + ", " + guest.vorname1 + ", " + guest.anrede1 + guest.anredefirma

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

                if t_list.fdate > datum:
                    t_list.fdate = datum

                if t_list.tdate < datum:
                    t_list.tdate = datum


                net_lodg, local_net_lodg, tot_breakfast, tot_lunch, tot_dinner, tot_other, tot_rmrev, tot_vat, tot_service = get_output(get_room_breakdown(res_line._recid, datum, 0, f_date))

                if tot_rmrev == 0:
                    local_net_lodg =  to_decimal("0")
                    net_lodg =  to_decimal("0")

                if mi_ftd:

                    if datum == f_date and from_date >= f_date:
                        t_list.dlodge =  to_decimal(t_list.dlodge) + to_decimal(local_net_lodg)

                        if res_line.resstatus != 13:
                            t_list.dnite = t_list.dnite + res_line.zimmeranz

                    if get_month(datum) == get_month(t_date):
                        t_list.mlodge =  to_decimal(t_list.mlodge) + to_decimal(local_net_lodg)

                        if res_line.resstatus != 13:
                            t_list.mnite = t_list.mnite + res_line.zimmeranz

                    if datum >= f_date and datum <= t_date:
                        t_list.ylodge =  to_decimal(t_list.ylodge) + to_decimal(local_net_lodg)

                        if res_line.resstatus != 13:
                            t_list.ynite = t_list.ynite + res_line.zimmeranz

                elif not mi_ftd:

                    if datum == t_date and from_date >= f_date:
                        t_list.dlodge =  to_decimal(t_list.dlodge) + to_decimal(local_net_lodg)

                        if res_line.resstatus != 13:
                            t_list.dnite = t_list.dnite + res_line.zimmeranz

                    if get_year(datum) == get_year(t_date):

                        if get_month(datum) == get_month(t_date):
                            t_list.mlodge =  to_decimal(t_list.mlodge) + to_decimal(local_net_lodg)

                            if res_line.resstatus != 13:
                                t_list.mnite = t_list.mnite + res_line.zimmeranz
                        t_list.ylodge =  to_decimal(t_list.ylodge) + to_decimal(local_net_lodg)

                        if res_line.resstatus != 13:
                            t_list.ynite = t_list.ynite + res_line.zimmeranz

        for t_list in query(t_list_list):

            if t_list.dnite != 0:
                t_list.drate =  to_decimal(t_list.dlodge) / to_decimal(t_list.dnite)

            if t_list.mnite != 0:
                t_list.mrate =  to_decimal(t_list.mlodge) / to_decimal(t_list.mnite)

            if t_list.ynite != 0:
                t_list.yrate =  to_decimal(t_list.ylodge) / to_decimal(t_list.ynite)


    guest = get_cache (Guest, {"gastnr": [(eq, gastno)]})

    if not guest:

        return generate_output()
    else:
        avail_guest = True

    segment = get_cache (Segment, {"segmentcode": [(eq, segmcode)]})

    if segment:
        f_tittle = ": " + entry(0, segment.bezeich, "$$0") + " - " + guest.name

    htparam = get_cache (Htparam, {"paramnr": [(eq, 87)]})
    ci_date = htparam.fdate

    if (from_date < ci_date) and (to_date < ci_date):
        create_list(from_date, to_date)

    if (from_date < ci_date) and (to_date >= ci_date):
        create_list(from_date, ci_date - 1)
        create_list2(ci_date, to_date)

    if (from_date >= ci_date) and (to_date >= ci_date):
        create_list2(from_date, to_date)

    return generate_output()