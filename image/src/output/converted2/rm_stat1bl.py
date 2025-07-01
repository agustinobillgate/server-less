#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Genstat, Guest

def rm_stat1bl(pvilanguage:int, segmcode:int, jan_date:date, to_date:date):

    prepare_cache ([Genstat, Guest])

    t_list_list = []
    lvcarea:string = "rm-stat1"
    genstat = guest = None

    t_list = None

    t_list_list, T_list = create_model("T_list", {"flag":bool, "gastnr":int, "gname":string, "dlodge":Decimal, "mlodge":Decimal, "ylodge":Decimal, "dnite":int, "mnite":int, "ynite":int, "drate":Decimal, "mrate":Decimal, "yrate":Decimal})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal t_list_list, lvcarea, genstat, guest
        nonlocal pvilanguage, segmcode, jan_date, to_date


        nonlocal t_list
        nonlocal t_list_list

        return {"t-list": t_list_list}

    def create_list():

        nonlocal t_list_list, lvcarea, genstat, guest
        nonlocal pvilanguage, segmcode, jan_date, to_date


        nonlocal t_list
        nonlocal t_list_list

        tot_dlodge:Decimal = to_decimal("0.0")
        tot_mlodge:Decimal = to_decimal("0.0")
        tot_ylodge:Decimal = to_decimal("0.0")
        tot_dnite:int = 0
        tot_mnite:int = 0
        tot_ynite:int = 0
        tot_drate:Decimal = to_decimal("0.0")
        tot_mrate:Decimal = to_decimal("0.0")
        tot_yrate:Decimal = to_decimal("0.0")

        for genstat in db_session.query(Genstat).filter(
                 (Genstat.datum >= jan_date) & (Genstat.datum <= to_date) & (Genstat.segmentcode == segmcode) & (Genstat.resstatus != 13) & (Genstat.nationnr != 0) & (Genstat.zinr != "") & (Genstat.gastnr > 0) & (Genstat.res_logic[inc_value(1)])).order_by(Genstat._recid).all():

            t_list = query(t_list_list, filters=(lambda t_list: t_list.gastnr == genstat.gastnr), first=True)

            if not t_list:

                guest = get_cache (Guest, {"gastnr": [(eq, genstat.gastnr)]})
                t_list = T_list()
                t_list_list.append(t_list)

                t_list.gastnr = genstat.gastnr

                if guest:
                    t_list.gname = guest.name + ", " + guest.vorname1 + ", " + guest.anrede1 + guest.anredefirma

            if genstat.datum == to_date:
                t_list.dlodge =  to_decimal(t_list.dlodge) + to_decimal(genstat.logis)
                tot_dlodge =  to_decimal(tot_dlodge) + to_decimal(genstat.logis)

                if genstat.resstatus != 13:
                    t_list.dnite = t_list.dnite + 1
                    tot_dnite = tot_dnite + 1

            if get_month(genstat.datum) == get_month(to_date):
                t_list.mlodge =  to_decimal(t_list.mlodge) + to_decimal(genstat.logis)
                tot_mlodge =  to_decimal(tot_mlodge) + to_decimal(genstat.logis)

                if genstat.resstatus != 13:
                    t_list.mnite = t_list.mnite + 1
                    tot_mnite = tot_mnite + 1


            t_list.ylodge =  to_decimal(t_list.ylodge) + to_decimal(genstat.logis)
            tot_ylodge =  to_decimal(tot_ylodge) + to_decimal(genstat.logis)

            if genstat.resstatus != 13:
                t_list.ynite = t_list.ynite + 1
                tot_ynite = tot_ynite + 1


        t_list = T_list()
        t_list_list.append(t_list)

        t_list.gname = translateExtended ("T O T A L", lvcarea, "")
        t_list.flag = True
        t_list.dlodge =  to_decimal(tot_dlodge)
        t_list.mlodge =  to_decimal(tot_mlodge)
        t_list.ylodge =  to_decimal(tot_ylodge)
        t_list.dnite = tot_dnite
        t_list.mnite = tot_mnite
        t_list.ynite = tot_ynite
        t_list.drate =  to_decimal(tot_drate)
        t_list.mrate =  to_decimal(tot_mrate)
        t_list.yrate =  to_decimal(tot_yrate)

        for t_list in query(t_list_list):

            if t_list.dnite != 0:
                t_list.drate =  to_decimal(t_list.dlodge) / to_decimal(t_list.dnite)

            if t_list.mnite != 0:
                t_list.mrate =  to_decimal(t_list.mlodge) / to_decimal(t_list.mnite)

            if t_list.ynite != 0:
                t_list.yrate =  to_decimal(t_list.ylodge) / to_decimal(t_list.ynite)

    create_list()

    return generate_output()