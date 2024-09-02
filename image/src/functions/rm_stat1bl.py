from functions.additional_functions import *
import decimal
from datetime import date
from models import Genstat, Guest

def rm_stat1bl(pvilanguage:int, segmcode:int, jan_date:date, to_date:date):
    t_list_list = []
    lvcarea:str = "rm_stat1"
    genstat = guest = None

    t_list = None

    t_list_list, T_list = create_model("T_list", {"flag":bool, "gastnr":int, "gname":str, "dlodge":decimal, "mlodge":decimal, "ylodge":decimal, "dnite":int, "mnite":int, "ynite":int, "drate":decimal, "mrate":decimal, "yrate":decimal})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal t_list_list, lvcarea, genstat, guest


        nonlocal t_list
        nonlocal t_list_list
        return {"t-list": t_list_list}

    def create_list():

        nonlocal t_list_list, lvcarea, genstat, guest


        nonlocal t_list
        nonlocal t_list_list

        tot_dlodge:decimal = 0
        tot_mlodge:decimal = 0
        tot_ylodge:decimal = 0
        tot_dnite:int = 0
        tot_mnite:int = 0
        tot_ynite:int = 0
        tot_drate:decimal = 0
        tot_mrate:decimal = 0
        tot_yrate:decimal = 0

        for genstat in db_session.query(Genstat).filter(
                (Genstat.datum >= jan_date) &  (Genstat.datum <= to_date) &  (Genstat.segmentcode == segmcode) &  (Genstat.resstatus != 13) &  (Genstat.nationnr != 0) &  (Genstat.zinr != "") &  (Genstat.gastnr > 0) &  (Genstat.res_logic[1])).all():

            t_list = query(t_list_list, filters=(lambda t_list :t_list.gastnr == genstat.gastnr), first=True)

            if not t_list:

                guest = db_session.query(Guest).filter(
                        (Guest.gastnr == genstat.gastnr)).first()
                t_list = T_list()
                t_list_list.append(t_list)

                t_list.gastnr = genstat.gastnr

                if guest:
                    t_list.gname = guest.name + ", " + guest.vorname1 + ", " + guest.anrede1 + guest.anredefirma

            if genstat.datum == to_date:
                t_list.dlodge = t_list.dlodge + genstat.logis
                tot_dlodge = tot_dlodge + genstat.logis

                if genstat.resstatus != 13:
                    t_list.dnite = t_list.dnite + 1
                    tot_dnite = tot_dnite + 1

            if get_month(genstat.datum) == get_month(to_date):
                t_list.mlodge = t_list.mlodge + genstat.logis
                tot_mlodge = tot_mlodge + genstat.logis

                if genstat.resstatus != 13:
                    t_list.mnite = t_list.mnite + 1
                    tot_mnite = tot_mnite + 1


            t_list.ylodge = t_list.ylodge + genstat.logis
            tot_ylodge = tot_ylodge + genstat.logis

            if genstat.resstatus != 13:
                t_list.ynite = t_list.ynite + 1
                tot_ynite = tot_ynite + 1


        t_list = T_list()
        t_list_list.append(t_list)

        t_list.gname = translateExtended ("T O T A L", lvcarea, "")
        t_list.flag = True
        t_list.dlodge = tot_dlodge
        t_list.mlodge = tot_mlodge
        t_list.ylodge = tot_ylodge
        t_list.dnite = tot_dnite
        t_list.mnite = tot_mnite
        t_list.ynite = tot_ynite
        t_list.drate = tot_drate
        t_list.mrate = tot_mrate
        t_list.yrate = tot_yrate

        for t_list in query(t_list_list):

            if t_list.dnite != 0:
                t_list.drate = t_list.dlodge / t_list.dnite

            if t_list.mnite != 0:
                t_list.mrate = t_list.mlodge / t_list.mnite

            if t_list.ynite != 0:
                t_list.yrate = t_list.ylodge / t_list.ynite


    create_list()

    return generate_output()