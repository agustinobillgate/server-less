#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Genstat, Segment

def rm_rev1bl(pvilanguage:int, from_date:date, to_date:date, rmno:string):

    prepare_cache ([Genstat, Segment])

    msg_str = ""
    t_list_data = []
    lvcarea:string = "rm-rev1"
    genstat = segment = None

    t_list = None

    t_list_data, T_list = create_model("T_list", {"flag":int, "bezeich":string, "anz":int, "pax":int, "net":Decimal, "proz":Decimal, "manz":int, "mpax":int, "mnet":Decimal, "proz1":Decimal, "yanz":int, "ypax":int, "ynet":Decimal, "proz2":Decimal})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal msg_str, t_list_data, lvcarea, genstat, segment
        nonlocal pvilanguage, from_date, to_date, rmno


        nonlocal t_list
        nonlocal t_list_data

        return {"msg_str": msg_str, "t-list": t_list_data}

    def create_list():

        nonlocal msg_str, t_list_data, lvcarea, genstat, segment
        nonlocal pvilanguage, from_date, to_date, rmno


        nonlocal t_list
        nonlocal t_list_data

        tot_dlodge:Decimal = to_decimal("0.0")
        tot_mlodge:Decimal = to_decimal("0.0")
        tot_ylodge:Decimal = to_decimal("0.0")
        tot_dnite:int = 0
        tot_mnite:int = 0
        tot_ynite:int = 0
        tot_drate:Decimal = to_decimal("0.0")
        tot_mrate:Decimal = to_decimal("0.0")
        tot_yrate:Decimal = to_decimal("0.0")
        tot_dpax:int = 0
        tot_mpax:int = 0
        tot_ypax:int = 0
        fdate:date = None
        t_genstat = None
        T_genstat =  create_buffer("T_genstat",Genstat)
        htparam.fdate = date_mdy(1, 1, get_year(to_date))

        for genstat in db_session.query(Genstat).filter(
                 (Genstat.datum >= from_date) & (Genstat.datum <= to_date) & (Genstat.zinr == rmno) & (Genstat.res_logic[inc_value(1)])).order_by(Genstat._recid).all():

            segment = get_cache (Segment, {"segmentcode": [(eq, genstat.segmentcode)]})

            if segment:

                if segment.betriebsnr == 2:

                    t_list = query(t_list_data, filters=(lambda t_list: t_list.flag == 3), first=True)

                    if not t_list:
                        t_list = T_list()
                        t_list_data.append(t_list)

                        t_list.flag = 3
                        t_list.bezeich = translateExtended ("House Use", lvcarea, "")

                elif segment.betriebsnr == 1 or (genstat.zipreis == 0 and (genstat.gratis > 0 or (genstat.erwachs + genstat.kind1 + genstat.kind2 + genstat.gratis == 0))):

                    t_list = query(t_list_data, filters=(lambda t_list: t_list.flag == 2), first=True)

                    if not t_list:
                        t_list = T_list()
                        t_list_data.append(t_list)

                        t_list.flag = 2
                        t_list.bezeich = translateExtended ("Compliment", lvcarea, "")


                else:

                    t_list = query(t_list_data, filters=(lambda t_list: t_list.flag == 1), first=True)

                    if not t_list:
                        t_list = T_list()
                        t_list_data.append(t_list)

                        t_list.flag = 1
                        t_list.bezeich = translateExtended ("Paying", lvcarea, "")


            else:
                msg_str = msg_str + chr_unicode(2) + "&W" + translateExtended ("Unable to find segmentcode ", lvcarea, "") + to_string(genstat.segmentcode)

                if (genstat.zipreis == 0 and (genstat.gratis > 0 or (genstat.erwachs + genstat.kind1 + genstat.kind2 + genstat.gratis == 0))):

                    t_list = query(t_list_data, filters=(lambda t_list: t_list.flag == 2), first=True)

                    if not t_list:
                        t_list = T_list()
                        t_list_data.append(t_list)

                        t_list.flag = 2
                        t_list.bezeich = translateExtended ("Compliment", lvcarea, "")


                else:

                    t_list = query(t_list_data, filters=(lambda t_list: t_list.flag == 1), first=True)

                    if not t_list:
                        t_list = T_list()
                        t_list_data.append(t_list)

                        t_list.flag = 1
                        t_list.bezeich = translateExtended ("Paying", lvcarea, "")

            if genstat.datum == to_date:
                t_list.anz = t_list.anz + 1
                t_list.pax = t_list.pax + genstat.erwachs + genstat.gratis +\
                        genstat.kind1 + genstat.kind2 + genstat.kind3
                t_list.net =  to_decimal(t_list.net) + to_decimal(genstat.logis)
                tot_dnite = tot_dnite + 1
                tot_dlodge =  to_decimal(tot_dlodge) + to_decimal(genstat.logis)
                tot_dpax = tot_dpax + genstat.erwachs + genstat.gratis +\
                        genstat.kind1 + genstat.kind2 + genstat.kind3

            if get_month(genstat.datum) == get_month(to_date) and get_year(genstat.datum) == get_year(to_date):
                t_list.manz = t_list.manz + 1
                t_list.mpax = t_list.mpax + genstat.erwachs + genstat.gratis +\
                        genstat.kind1 + genstat.kind2 + genstat.kind3
                t_list.mnet =  to_decimal(t_list.mnet) + to_decimal(genstat.logis)
                tot_mnite = tot_mnite + 1
                tot_mlodge =  to_decimal(tot_mlodge) + to_decimal(genstat.logis)
                tot_mpax = tot_mpax + genstat.erwachs + genstat.gratis +\
                        genstat.kind1 + genstat.kind2 + genstat.kind3


            t_list.yanz = t_list.yanz + 1
            t_list.ypax = t_list.ypax + genstat.erwachs + genstat.gratis +\
                    genstat.kind1 + genstat.kind2 + genstat.kind3
            t_list.ynet =  to_decimal(t_list.ynet) + to_decimal(genstat.logis)
            tot_ynite = tot_ynite + 1
            tot_ylodge =  to_decimal(tot_ylodge) + to_decimal(genstat.logis)
            tot_ypax = tot_ypax + genstat.erwachs + genstat.gratis +\
                    genstat.kind1 + genstat.kind2 + genstat.kind3

        for t_list in query(t_list_data):

            if t_list.anz != 0:
                t_list.proz =  to_decimal(t_list.net) / to_decimal(tot_dlodge) * to_decimal("100")

            if t_list.manz != 0:
                t_list.proz1 =  to_decimal(t_list.mnet) / to_decimal(tot_mlodge) * to_decimal("100")

            if t_list.yanz != 0:
                t_list.proz2 =  to_decimal(t_list.ynet) / to_decimal(tot_ylodge) * to_decimal("100")


        t_list = T_list()
        t_list_data.append(t_list)

        t_list.bezeich = translateExtended ("T O T A L", lvcarea, "")
        t_list.flag = 4
        t_list.anz = tot_dnite
        t_list.pax = tot_dpax
        t_list.net =  to_decimal(tot_dlodge)
        t_list.manz = tot_mnite
        t_list.mpax = tot_mpax
        t_list.mnet =  to_decimal(tot_mlodge)
        t_list.yanz = tot_ynite
        t_list.ypax = tot_ypax
        t_list.ynet =  to_decimal(tot_ylodge)
        t_list.proz =  to_decimal("100")
        t_list.proz1 =  to_decimal("100")
        t_list.proz2 =  to_decimal("100")

    create_list()

    return generate_output()