from functions.additional_functions import *
import decimal
from datetime import date
from models import Genstat, Segment

def rm_rev1bl(pvilanguage:int, from_date:date, to_date:date, rmno:str):
    msg_str = ""
    t_list_list = []
    lvcarea:str = "rm_rev1"
    genstat = segment = None

    t_list = t_genstat = None

    t_list_list, T_list = create_model("T_list", {"flag":int, "bezeich":str, "anz":int, "pax":int, "net":decimal, "proz":decimal, "manz":int, "mpax":int, "mnet":decimal, "proz1":decimal, "yanz":int, "ypax":int, "ynet":decimal, "proz2":decimal})

    T_genstat = Genstat

    db_session = local_storage.db_session

    def generate_output():
        nonlocal msg_str, t_list_list, lvcarea, genstat, segment
        nonlocal t_genstat


        nonlocal t_list, t_genstat
        nonlocal t_list_list
        return {"msg_str": msg_str, "t-list": t_list_list}

    def create_list():

        nonlocal msg_str, t_list_list, lvcarea, genstat, segment
        nonlocal t_genstat


        nonlocal t_list, t_genstat
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
        tot_dpax:int = 0
        tot_mpax:int = 0
        tot_ypax:int = 0
        fdate:date = None
        T_genstat = Genstat
        fdate = date_mdy(1, 1, get_year(to_date))

        for genstat in db_session.query(Genstat).filter(
                (Genstat.datum >= from_date) &  (Genstat.datum <= to_date) &  (Genstat.zinr == rmno) &  (Genstat.res_logic[1])).all():

            segment = db_session.query(Segment).filter(
                    (Segment.segmentcode == genstat.segmentcode)).first()

            if segment:

                if segment.betriebsnr == 2:

                    t_list = query(t_list_list, filters=(lambda t_list :t_list.flag == 3), first=True)

                    if not t_list:
                        t_list = T_list()
                        t_list_list.append(t_list)

                        t_list.flag = 3
                        t_list.bezeich = translateExtended ("House Use", lvcarea, "")

                elif segment.betriebsnr == 1 or (genstat.zipreis == 0 and (genstat.gratis > 0 or (genstat.erwachs + genstat.kind1 + genstat.kind2 + genstat.gratis == 0))):

                    t_list = query(t_list_list, filters=(lambda t_list :t_list.flag == 2), first=True)

                    if not t_list:
                        t_list = T_list()
                        t_list_list.append(t_list)

                        t_list.flag = 2
                        t_list.bezeich = translateExtended ("Compliment", lvcarea, "")


                else:

                    t_list = query(t_list_list, filters=(lambda t_list :t_list.flag == 1), first=True)

                    if not t_list:
                        t_list = T_list()
                        t_list_list.append(t_list)

                        t_list.flag = 1
                        t_list.bezeich = translateExtended ("Paying", lvcarea, "")


            else:
                msg_str = msg_str + chr(2) + "&W" + translateExtended ("Unable to find segmentcode ", lvcarea, "") + to_string(genstat.segmentcode)

                if (genstat.zipreis == 0 and (genstat.gratis > 0 or (genstat.erwachs + genstat.kind1 + genstat.kind2 + genstat.gratis == 0))):

                    t_list = query(t_list_list, filters=(lambda t_list :t_list.flag == 2), first=True)

                    if not t_list:
                        t_list = T_list()
                        t_list_list.append(t_list)

                        t_list.flag = 2
                        t_list.bezeich = translateExtended ("Compliment", lvcarea, "")


                else:

                    t_list = query(t_list_list, filters=(lambda t_list :t_list.flag == 1), first=True)

                    if not t_list:
                        t_list = T_list()
                        t_list_list.append(t_list)

                        t_list.flag = 1
                        t_list.bezeich = translateExtended ("Paying", lvcarea, "")

            if genstat.datum == to_date:
                t_list.anz = t_list.anz + 1
                t_list.pax = t_list.pax + genstat.erwachs + genstat.gratis +\
                        genstat.kind1 + genstat.kind2 + genstat.kind3
                t_list.net = t_list.net + genstat.logis
                tot_dnite = tot_dnite + 1
                tot_dlodge = tot_dlodge + genstat.logis
                tot_dpax = tot_dpax + genstat.erwachs + genstat.gratis +\
                        genstat.kind1 + genstat.kind2 + genstat.kind3

            if get_month(genstat.datum) == get_month(to_date) and get_year(genstat.datum) == get_year(to_date):
                t_list.manz = t_list.manz + 1
                t_list.mpax = t_list.mpax + genstat.erwachs + genstat.gratis +\
                        genstat.kind1 + genstat.kind2 + genstat.kind3
                t_list.mnet = t_list.mnet + genstat.logis
                tot_mnite = tot_mnite + 1
                tot_mlodge = tot_mlodge + genstat.logis
                tot_mpax = tot_mpax + genstat.erwachs + genstat.gratis +\
                        genstat.kind1 + genstat.kind2 + genstat.kind3


            t_list.yanz = t_list.yanz + 1
            t_list.ypax = t_list.ypax + genstat.erwachs + genstat.gratis +\
                    genstat.kind1 + genstat.kind2 + genstat.kind3
            t_list.ynet = t_list.ynet + genstat.logis
            tot_ynite = tot_ynite + 1
            tot_ylodge = tot_ylodge + genstat.logis
            tot_ypax = tot_ypax + genstat.erwachs + genstat.gratis +\
                    genstat.kind1 + genstat.kind2 + genstat.kind3

        for t_list in query(t_list_list):

            if t_list.anz != 0:
                t_list.proz = t_list.net / tot_dlodge * 100

            if t_list.manz != 0:
                t_list.proz1 = t_list.mnet / tot_mlodge * 100

            if t_list.yanz != 0:
                t_list.proz2 = t_list.ynet / tot_ylodge * 100


        t_list = T_list()
        t_list_list.append(t_list)

        t_list.bezeich = translateExtended ("T O T A L", lvcarea, "")
        t_list.flag = 4
        t_list.anz = tot_dnite
        t_list.pax = tot_dpax
        t_list.net = tot_dlodge
        t_list.manz = tot_mnite
        t_list.mpax = tot_mpax
        t_list.mnet = tot_mlodge
        t_list.yanz = tot_ynite
        t_list.ypax = tot_ypax
        t_list.ynet = tot_ylodge
        t_list.proz = 100
        t_list.proz1 = 100
        t_list.proz2 = 100


    create_list()

    return generate_output()