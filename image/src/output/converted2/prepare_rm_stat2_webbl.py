#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Guest, Segment, Genstat

def prepare_rm_stat2_webbl(gastno:int, segmcode:int, jan_date:date, to_date:date):

    prepare_cache ([Guest, Segment, Genstat])

    avail_guest = False
    f_tittle = ""
    t_list_list = []
    guest = segment = genstat = None

    t_list = None

    t_list_list, T_list = create_model("T_list", {"gastnr":int, "mgastnr":int, "gname":string, "resnr":int, "reslinnr":int, "fdate":date, "tdate":date, "ankunft":date, "abreise":date, "zimmeranz":int, "dlodge":Decimal, "dnite":int, "drate":Decimal, "mlodge":Decimal, "mnite":int, "mrate":Decimal, "ylodge":Decimal, "ynite":int, "yrate":Decimal, "zinr":string}, {"fdate": get_current_date(), "tdate": date_mdy(1, 1, 1900), "ankunft": None, "abreise": None})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal avail_guest, f_tittle, t_list_list, guest, segment, genstat
        nonlocal gastno, segmcode, jan_date, to_date


        nonlocal t_list
        nonlocal t_list_list

        return {"avail_guest": avail_guest, "f_tittle": f_tittle, "t-list": t_list_list}

    def create_list():

        nonlocal avail_guest, f_tittle, t_list_list, guest, segment, genstat
        nonlocal gastno, segmcode, jan_date, to_date


        nonlocal t_list
        nonlocal t_list_list

        for genstat in db_session.query(Genstat).filter(
                 (Genstat.gastnr == gastno) & (Genstat.datum >= jan_date) & (Genstat.datum <= to_date) & (Genstat.segmentcode == segmcode) & (Genstat.res_logic[inc_value(1)]) & ((Genstat.erwachs + Genstat.kind1) > 0)).order_by(Genstat._recid).all():

            t_list = query(t_list_list, filters=(lambda t_list: t_list.resnr == genstat.resnr), first=True)

            guest = get_cache (Guest, {"gastnr": [(eq, genstat.gastnrmember)]})
            t_list = T_list()
            t_list_list.append(t_list)

            t_list.resnr = genstat.resnr
            t_list.reslinnr = genstat.res_int[0]
            t_list.mgastnr = genstat.gastnrmember
            t_list.gastnr = genstat.gastnr
            t_list.zinr = genstat.zinr

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

            if genstat.datum == to_date:
                t_list.dlodge =  to_decimal(t_list.dlodge) + to_decimal(genstat.logis)

                if genstat.resstatus != 13:
                    t_list.dnite = t_list.dnite + 1

            if get_month(genstat.datum) == get_month(to_date):
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


    guest = get_cache (Guest, {"gastnr": [(eq, gastno)]})

    if not guest:

        return generate_output()
    else:
        avail_guest = True

    segment = get_cache (Segment, {"segmentcode": [(eq, segmcode)]})
    f_tittle = ": " + entry(0, segment.bezeich, "$$0") + " - " + guest.name
    create_list()

    return generate_output()