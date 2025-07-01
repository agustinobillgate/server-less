#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from functions.htpdate import htpdate
from functions.argt_betrag import argt_betrag
from models import Htparam, Zimmer, Arrangement, Res_line, Waehrung, Argt_line, Artikel, Zinrstat, Zimkateg, Genstat

def rm_revenue_1_webbl(m_ftd:bool, m_ytd:bool, f_date:date, t_date:date, to_date:date, rm_no:string, sorttype:int, lod__rev:bool):

    prepare_cache ([Htparam, Zimmer, Arrangement, Res_line, Waehrung, Argt_line, Zinrstat, Zimkateg, Genstat])

    output_list_list = []
    i:int = 0
    anz:int = 0
    manz:int = 0
    yanz:int = 0
    pax:int = 0
    mpax:int = 0
    ypax:int = 0
    mnet:Decimal = to_decimal("0.0")
    ynet:Decimal = to_decimal("0.0")
    net:Decimal = to_decimal("0.0")
    t_anz:int = 0
    t_manz:int = 0
    t_yanz:int = 0
    t_pax:int = 0
    t_mpax:int = 0
    t_ypax:int = 0
    t_net:Decimal = to_decimal("0.0")
    t_mnet:Decimal = to_decimal("0.0")
    t_ynet:Decimal = to_decimal("0.0")
    from_bez:string = ""
    to_bez:string = ""
    price_decimal:int = 0
    from_date:date = None
    curr_zeit:int = 0
    ci_date:date = None
    htparam = zimmer = arrangement = res_line = waehrung = argt_line = artikel = zinrstat = zimkateg = genstat = None

    output_list = cl_list = None

    output_list_list, Output_list = create_model("Output_list", {"rmno":string, "flag":string, "str":string, "rmno1":string, "rmtype":string, "rm":int, "pax":int, "rm_rev":Decimal, "percent":Decimal, "mtdrm":int, "pax1":int, "rm_rev1":Decimal, "percent1":Decimal, "ftdrm":int, "pax2":int, "rm_rev2":Decimal, "percent3":Decimal})
    cl_list_list, Cl_list = create_model("Cl_list", {"flag":string, "zinr":string, "rmcat":string, "anz":int, "pax":int, "net":Decimal, "proz":Decimal, "manz":int, "mpax":int, "mnet":Decimal, "proz1":Decimal, "yanz":int, "ypax":int, "ynet":Decimal, "proz2":Decimal})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal output_list_list, i, anz, manz, yanz, pax, mpax, ypax, mnet, ynet, net, t_anz, t_manz, t_yanz, t_pax, t_mpax, t_ypax, t_net, t_mnet, t_ynet, from_bez, to_bez, price_decimal, from_date, curr_zeit, ci_date, htparam, zimmer, arrangement, res_line, waehrung, argt_line, artikel, zinrstat, zimkateg, genstat
        nonlocal m_ftd, m_ytd, f_date, t_date, to_date, rm_no, sorttype, lod__rev


        nonlocal output_list, cl_list
        nonlocal output_list_list, cl_list_list

        return {"output-list": output_list_list}

    def create_resline():

        nonlocal output_list_list, i, anz, manz, yanz, pax, mpax, ypax, mnet, ynet, net, t_anz, t_manz, t_yanz, t_pax, t_mpax, t_ypax, t_net, t_mnet, t_ynet, from_bez, to_bez, from_date, curr_zeit, ci_date, htparam, zimmer, arrangement, res_line, waehrung, argt_line, artikel, zinrstat, zimkateg, genstat
        nonlocal m_ftd, m_ytd, f_date, t_date, to_date, rm_no, sorttype, lod__rev


        nonlocal output_list, cl_list
        nonlocal output_list_list, cl_list_list

        datum:date = None
        s_datum:date = None
        e_datum:date = None
        amount_rmrev:Decimal = to_decimal("0.0")
        amount_rmargt:Decimal = to_decimal("0.0")
        frate:Decimal = 1
        price_decimal:int = 0
        argt_betrag:Decimal = to_decimal("0.0")
        ex_rate:Decimal = to_decimal("0.0")
        last_zikatnr:int = 0
        found_zikatnr:bool = False
        count_k:int = 0
        last_zinr:string = ""
        last_rmtype:string = ""

        htparam = get_cache (Htparam, {"paramnr": [(eq, 491)]})
        price_decimal = htparam.finteger

        if rm_no != "":
            cl_list = Cl_list()
            cl_list_list.append(cl_list)

            cl_list.zinr = rm_no

            zimmer = get_cache (Zimmer, {"zinr": [(eq, rm_no)]})

            if zimmer:
                cl_list.rmcat = zimmer.kbezeich

            res_line_obj_list = {}
            res_line = Res_line()
            arrangement = Arrangement()
            zimmer = Zimmer()
            for res_line.reserve_dec, res_line.betriebsnr, res_line.ankunft, res_line.abreise, res_line.zipreis, res_line._recid, res_line.zimmeranz, res_line.erwachs, res_line.gratis, res_line.kind1, res_line.kind2, res_line.zinr, res_line.zikatnr, arrangement.argtnr, arrangement._recid, zimmer.kbezeich, zimmer.zinr, zimmer.zikatnr, zimmer._recid in db_session.query(Res_line.reserve_dec, Res_line.betriebsnr, Res_line.ankunft, Res_line.abreise, Res_line.zipreis, Res_line._recid, Res_line.zimmeranz, Res_line.erwachs, Res_line.gratis, Res_line.kind1, Res_line.kind2, Res_line.zinr, Res_line.zikatnr, Arrangement.argtnr, Arrangement._recid, Zimmer.kbezeich, Zimmer.zinr, Zimmer.zikatnr, Zimmer._recid).join(Arrangement,(Arrangement.arrangement == Res_line.arrangement)).join(Zimmer,(Zimmer.zinr == Res_line.zinr)).filter(
                     ((Res_line.active_flag <= 1) & (Res_line.resstatus != 12) & (Res_line.resstatus <= 13) & (Res_line.resstatus != 4) & (not_ (Res_line.ankunft > t_date)) & (not_ (Res_line.abreise < f_date))) & (Res_line.l_zuordnung[inc_value(2)] == 0) & (Res_line.zinr == (rm_no).lower()) & (Res_line.zipreis != 0)).order_by(Res_line.zinr).all():
                if res_line_obj_list.get(res_line._recid):
                    continue
                else:
                    res_line_obj_list[res_line._recid] = True


                amount_rmrev =  to_decimal("0")
                amount_rmargt =  to_decimal("0")

                if res_line.reserve_dec != 0:
                    frate =  to_decimal(res_line.reserve_dec)
                else:

                    waehrung = get_cache (Waehrung, {"waehrungsnr": [(eq, res_line.betriebsnr)]})

                    if waehrung:
                        frate =  to_decimal(waehrung.ankauf) / to_decimal(waehrung.einheit)

                if res_line.ankunft >= f_date:
                    s_datum = res_line.ankunft
                else:
                    s_datum = f_date

                if res_line.abreise <= t_date:
                    e_datum = res_line.abreise - timedelta(days=1)
                else:
                    e_datum = t_date
                for datum in date_range(s_datum,e_datum) :
                    amount_rmrev =  to_decimal(res_line.zipreis) * to_decimal(frate)
                    amount_rmargt = to_decimal(round(res_line.zipreis * frate , price_decimal))

                    for argt_line in db_session.query(Argt_line).filter(
                             (Argt_line.argtnr == arrangement.argtnr) & not_ (Argt_line.kind2)).order_by(Argt_line._recid).all():

                        artikel = get_cache (Artikel, {"artnr": [(eq, argt_line.argt_artnr)],"departement": [(eq, argt_line.departement)]})
                        argt_betrag, ex_rate = get_output(argt_betrag(res_line._recid, argt_line._recid))
                        amount_rmrev =  to_decimal(amount_rmrev) - to_decimal(argt_betrag) * to_decimal(ex_rate)
                    amount_rmrev = to_decimal(round(amount_rmrev , price_decimal))

                    if datum == e_datum:
                        cl_list.anz = cl_list.anz + res_line.zimmeranz
                        cl_list.pax = cl_list.pax + res_line.erwachs + res_line.gratis + res_line.kind1 + res_line.kind2
                        anz = anz + res_line.zimmeranz
                        pax = pax + res_line.erwachs + res_line.gratis + res_line.kind1 + res_line.kind2

                        if lod__rev:
                            cl_list.net =  to_decimal(cl_list.net) + to_decimal(amount_rmrev)
                            net =  to_decimal(net) + to_decimal(amount_rmrev)
                        else:
                            cl_list.net =  to_decimal(cl_list.net) + to_decimal(amount_rmargt)
                            net =  to_decimal(net) + to_decimal(amount_rmargt)
                    cl_list.manz = cl_list.manz + res_line.zimmeranz
                    cl_list.mpax = cl_list.mpax + res_line.erwachs + res_line.gratis + res_line.kind1 + res_line.kind2
                    manz = manz + res_line.zimmeranz
                    mpax = mpax + res_line.erwachs + res_line.gratis + res_line.kind1 + res_line.kind2

                    if lod__rev:
                        cl_list.mnet =  to_decimal(cl_list.mnet) + to_decimal(amount_rmrev)
                        mnet =  to_decimal(mnet) + to_decimal(amount_rmrev)
                    else:
                        cl_list.mnet =  to_decimal(cl_list.mnet) + to_decimal(amount_rmargt)
                        mnet =  to_decimal(mnet) + to_decimal(amount_rmargt)
        else:

            if sorttype == 1:

                res_line_obj_list = {}
                res_line = Res_line()
                arrangement = Arrangement()
                zimmer = Zimmer()
                for res_line.reserve_dec, res_line.betriebsnr, res_line.ankunft, res_line.abreise, res_line.zipreis, res_line._recid, res_line.zimmeranz, res_line.erwachs, res_line.gratis, res_line.kind1, res_line.kind2, res_line.zinr, res_line.zikatnr, arrangement.argtnr, arrangement._recid, zimmer.kbezeich, zimmer.zinr, zimmer.zikatnr, zimmer._recid in db_session.query(Res_line.reserve_dec, Res_line.betriebsnr, Res_line.ankunft, Res_line.abreise, Res_line.zipreis, Res_line._recid, Res_line.zimmeranz, Res_line.erwachs, Res_line.gratis, Res_line.kind1, Res_line.kind2, Res_line.zinr, Res_line.zikatnr, Arrangement.argtnr, Arrangement._recid, Zimmer.kbezeich, Zimmer.zinr, Zimmer.zikatnr, Zimmer._recid).join(Arrangement,(Arrangement.arrangement == Res_line.arrangement)).join(Zimmer,(Zimmer.zinr == Res_line.zinr)).filter(
                         ((Res_line.active_flag <= 1) & (Res_line.resstatus != 12) & (Res_line.resstatus <= 13) & (Res_line.resstatus != 4) & (not_ (Res_line.ankunft > t_date)) & (not_ (Res_line.abreise < f_date))) & (Res_line.l_zuordnung[inc_value(2)] == 0) & (Res_line.zinr != "") & (Res_line.zipreis != 0)).order_by(Res_line.zinr).all():
                    if res_line_obj_list.get(res_line._recid):
                        continue
                    else:
                        res_line_obj_list[res_line._recid] = True


                    amount_rmrev =  to_decimal("0")
                    amount_rmargt =  to_decimal("0")

                    if res_line.reserve_dec != 0:
                        frate =  to_decimal(res_line.reserve_dec)
                    else:

                        waehrung = get_cache (Waehrung, {"waehrungsnr": [(eq, res_line.betriebsnr)]})

                        if waehrung:
                            frate =  to_decimal(waehrung.ankauf) / to_decimal(waehrung.einheit)

                    if res_line.ankunft >= f_date:
                        s_datum = res_line.ankunft
                    else:
                        s_datum = f_date

                    if res_line.abreise <= t_date:
                        e_datum = res_line.abreise - timedelta(days=1)
                    else:
                        e_datum = t_date

                    cl_list = query(cl_list_list, filters=(lambda cl_list: cl_list.zinr == res_line.zinr and cl_list.rmcat == zimmer.kbezeich), first=True)

                    if not cl_list:
                        cl_list = Cl_list()
                        cl_list_list.append(cl_list)

                        cl_list.zinr = res_line.zinr
                        cl_list.rmcat = zimmer.kbezeich
                    for datum in date_range(s_datum,e_datum) :
                        amount_rmrev =  to_decimal(res_line.zipreis) * to_decimal(frate)
                        amount_rmargt = to_decimal(round(res_line.zipreis * frate , price_decimal))

                        for argt_line in db_session.query(Argt_line).filter(
                                 (Argt_line.argtnr == arrangement.argtnr) & not_ (Argt_line.kind2)).order_by(Argt_line._recid).all():

                            artikel = get_cache (Artikel, {"artnr": [(eq, argt_line.argt_artnr)],"departement": [(eq, argt_line.departement)]})
                            argt_betrag, ex_rate = get_output(argt_betrag(res_line._recid, argt_line._recid))
                            amount_rmrev =  to_decimal(amount_rmrev) - to_decimal(argt_betrag) * to_decimal(ex_rate)
                        amount_rmrev = to_decimal(round(amount_rmrev , price_decimal))

                        if datum == e_datum:
                            cl_list.anz = cl_list.anz + res_line.zimmeranz
                            cl_list.pax = cl_list.pax + res_line.erwachs + res_line.gratis + res_line.kind1 + res_line.kind2
                            anz = anz + res_line.zimmeranz
                            pax = pax + res_line.erwachs + res_line.gratis + res_line.kind1 + res_line.kind2

                            if lod__rev:
                                cl_list.net =  to_decimal(cl_list.net) + to_decimal(amount_rmrev)
                                net =  to_decimal(net) + to_decimal(amount_rmrev)
                            else:
                                cl_list.net =  to_decimal(cl_list.net) + to_decimal(amount_rmargt)
                                net =  to_decimal(net) + to_decimal(amount_rmargt)
                        cl_list.manz = cl_list.manz + res_line.zimmeranz
                        cl_list.mpax = cl_list.mpax + res_line.erwachs + res_line.gratis + res_line.kind1 + res_line.kind2
                        manz = manz + res_line.zimmeranz
                        mpax = mpax + res_line.erwachs + res_line.gratis + res_line.kind1 + res_line.kind2

                        if lod__rev:
                            cl_list.mnet =  to_decimal(cl_list.mnet) + to_decimal(amount_rmrev)
                            mnet =  to_decimal(mnet) + to_decimal(amount_rmrev)
                        else:
                            cl_list.mnet =  to_decimal(cl_list.mnet) + to_decimal(amount_rmargt)
                            mnet =  to_decimal(mnet) + to_decimal(amount_rmargt)

            elif sorttype == 2:

                res_line_obj_list = {}
                res_line = Res_line()
                arrangement = Arrangement()
                zimmer = Zimmer()
                for res_line.reserve_dec, res_line.betriebsnr, res_line.ankunft, res_line.abreise, res_line.zipreis, res_line._recid, res_line.zimmeranz, res_line.erwachs, res_line.gratis, res_line.kind1, res_line.kind2, res_line.zinr, res_line.zikatnr, arrangement.argtnr, arrangement._recid, zimmer.kbezeich, zimmer.zinr, zimmer.zikatnr, zimmer._recid in db_session.query(Res_line.reserve_dec, Res_line.betriebsnr, Res_line.ankunft, Res_line.abreise, Res_line.zipreis, Res_line._recid, Res_line.zimmeranz, Res_line.erwachs, Res_line.gratis, Res_line.kind1, Res_line.kind2, Res_line.zinr, Res_line.zikatnr, Arrangement.argtnr, Arrangement._recid, Zimmer.kbezeich, Zimmer.zinr, Zimmer.zikatnr, Zimmer._recid).join(Arrangement,(Arrangement.arrangement == Res_line.arrangement)).join(Zimmer,(Zimmer.zinr == Res_line.zinr)).filter(
                         ((Res_line.active_flag <= 1) & (Res_line.resstatus != 12) & (Res_line.resstatus <= 13) & (Res_line.resstatus != 4) & (not_ (Res_line.ankunft > t_date)) & (not_ (Res_line.abreise < f_date))) & (Res_line.l_zuordnung[inc_value(2)] == 0) & (Res_line.zinr != "") & (Res_line.zipreis != 0)).order_by(Res_line.zikatnr, Res_line.zinr).all():
                    if res_line_obj_list.get(res_line._recid):
                        continue
                    else:
                        res_line_obj_list[res_line._recid] = True


                    amount_rmrev =  to_decimal("0")
                    amount_rmargt =  to_decimal("0")

                    if res_line.reserve_dec != 0:
                        frate =  to_decimal(res_line.reserve_dec)
                    else:

                        waehrung = get_cache (Waehrung, {"waehrungsnr": [(eq, res_line.betriebsnr)]})

                        if waehrung:
                            frate =  to_decimal(waehrung.ankauf) / to_decimal(waehrung.einheit)

                    if res_line.ankunft >= f_date:
                        s_datum = res_line.ankunft
                    else:
                        s_datum = f_date

                    if res_line.abreise <= t_date:
                        e_datum = res_line.abreise - timedelta(days=1)
                    else:
                        e_datum = t_date

                    if last_zikatnr != res_line.zikatnr or last_zinr != res_line.zinr:
                        count_k = count_k + 1

                        if count_k > 1 and last_zikatnr != res_line.zikatnr:
                            cl_list = Cl_list()
                            cl_list_list.append(cl_list)

                            cl_list.flag = "*"
                            cl_list.rmcat = "Total"
                            cl_list.anz = t_anz
                            cl_list.pax = t_pax
                            cl_list.net =  to_decimal(t_net)
                            cl_list.manz = t_manz
                            cl_list.mnet =  to_decimal(t_mnet)
                            cl_list.mpax = t_mpax
                            cl_list.yanz = t_manz
                            cl_list.ypax = t_mnet
                            cl_list.ynet =  to_decimal(t_mpax)
                            t_anz = 0
                            t_pax = 0
                            t_net =  to_decimal("0")
                            t_manz = 0
                            t_mnet =  to_decimal("0")
                            t_mpax = 0
                            t_yanz = 0
                            t_ynet =  to_decimal("0")
                            t_ypax = 0


                        cl_list = Cl_list()
                        cl_list_list.append(cl_list)

                        cl_list.zinr = res_line.zinr
                        cl_list.rmcat = zimmer.kbezeich
                        last_zikatnr = res_line.zikatnr
                        last_zinr = res_line.zinr
                    for datum in date_range(s_datum,e_datum) :
                        amount_rmrev =  to_decimal(res_line.zipreis) * to_decimal(frate)
                        amount_rmargt = to_decimal(round(res_line.zipreis * frate , price_decimal))

                        for argt_line in db_session.query(Argt_line).filter(
                                 (Argt_line.argtnr == arrangement.argtnr) & not_ (Argt_line.kind2)).order_by(Argt_line._recid).all():

                            artikel = get_cache (Artikel, {"artnr": [(eq, argt_line.argt_artnr)],"departement": [(eq, argt_line.departement)]})
                            argt_betrag, ex_rate = get_output(argt_betrag(res_line._recid, argt_line._recid))
                            amount_rmrev =  to_decimal(amount_rmrev) - to_decimal(argt_betrag) * to_decimal(ex_rate)
                        amount_rmrev = to_decimal(round(amount_rmrev , price_decimal))

                        if datum == e_datum:
                            cl_list.anz = cl_list.anz + res_line.zimmeranz
                            cl_list.pax = cl_list.pax + res_line.erwachs + res_line.gratis + res_line.kind1 + res_line.kind2
                            anz = anz + res_line.zimmeranz
                            pax = pax + res_line.erwachs + res_line.gratis + res_line.kind1 + res_line.kind2
                            t_anz = t_anz + res_line.zimmeranz
                            t_pax = t_pax + res_line.erwachs + res_line.gratis + res_line.kind1 + res_line.kind2

                            if lod__rev:
                                cl_list.net =  to_decimal(cl_list.net) + to_decimal(amount_rmrev)
                                net =  to_decimal(net) + to_decimal(amount_rmrev)
                                t_net =  to_decimal(t_net) + to_decimal(amount_rmrev)
                            else:
                                cl_list.net =  to_decimal(cl_list.net) + to_decimal(amount_rmargt)
                                net =  to_decimal(net) + to_decimal(amount_rmargt)
                                t_net =  to_decimal(t_net) + to_decimal(amount_rmargt)
                        cl_list.manz = cl_list.manz + res_line.zimmeranz
                        cl_list.mpax = cl_list.mpax + res_line.erwachs + res_line.gratis + res_line.kind1 + res_line.kind2
                        manz = manz + res_line.zimmeranz
                        mpax = mpax + res_line.erwachs + res_line.gratis + res_line.kind1 + res_line.kind2
                        t_manz = t_manz + res_line.zimmeranz
                        t_mpax = t_mpax + res_line.erwachs + res_line.gratis + res_line.kind1 + res_line.kind2

                        if lod__rev:
                            cl_list.mnet =  to_decimal(cl_list.mnet) + to_decimal(amount_rmrev)
                            mnet =  to_decimal(mnet) + to_decimal(amount_rmrev)
                            t_mnet =  to_decimal(t_mnet) + to_decimal(amount_rmrev)
                        else:
                            cl_list.mnet =  to_decimal(cl_list.mnet) + to_decimal(amount_rmargt)
                            mnet =  to_decimal(mnet) + to_decimal(amount_rmargt)
                            t_mnet =  to_decimal(t_mnet) + to_decimal(amount_rmargt)

            if sorttype == 2:
                cl_list = Cl_list()
                cl_list_list.append(cl_list)

                cl_list.flag = "*"
                cl_list.rmcat = "Total"
                cl_list.anz = t_anz
                cl_list.pax = t_pax
                cl_list.net =  to_decimal(t_net)
                cl_list.manz = t_manz
                cl_list.mnet =  to_decimal(t_mnet)
                cl_list.mpax = t_mpax
                cl_list.yanz = t_manz
                cl_list.ypax = t_mnet
                cl_list.ynet =  to_decimal(t_mpax)
                t_anz = 0
                t_pax = 0
                t_net =  to_decimal("0")
                t_manz = 0
                t_mnet =  to_decimal("0")
                t_mpax = 0
                t_yanz = 0
                t_ynet =  to_decimal("0")
                t_ypax = 0

        for cl_list in query(cl_list_list):

            if net != 0:
                cl_list.proz =  to_decimal(cl_list.net) / to_decimal(net) * to_decimal("100")

            if mnet != 0:
                cl_list.proz1 =  to_decimal(cl_list.mnet) / to_decimal(mnet) * to_decimal("100")
        cl_list = Cl_list()
        cl_list_list.append(cl_list)

        cl_list.flag = "*"
        cl_list.zinr = ""
        cl_list = Cl_list()
        cl_list_list.append(cl_list)

        cl_list.zinr = ""
        cl_list.rmcat = "GTOTAL"
        cl_list.anz = anz
        cl_list.pax = pax
        cl_list.net =  to_decimal(net)

        if net != 0:
            cl_list.proz =  to_decimal("100")
        cl_list.manz = manz
        cl_list.mpax = mpax
        cl_list.mnet =  to_decimal(mnet)

        if mnet != 0:
            cl_list.proz1 =  to_decimal("100")
        cl_list.yanz = manz
        cl_list.ypax = mpax
        cl_list.ynet =  to_decimal(mnet)

        if mnet != 0:
            cl_list.proz2 =  to_decimal("100")

        for cl_list in query(cl_list_list):
            output_list = Output_list()
            output_list_list.append(output_list)

            output_list.flag = cl_list.flag
            output_list.rmno = cl_list.zinr
            output_list.rmno1 = to_string(cl_list.zinr)
            output_list.rmtype = to_string(cl_list.rmcat)
            output_list.rm = cl_list.anz
            output_list.pax = cl_list.pax
            output_list.rm_rev =  to_decimal(cl_list.net)
            output_list.percent =  to_decimal(cl_list.proz)
            output_list.mtdrm = cl_list.manz
            output_list.pax1 = cl_list.mpax
            output_list.rm_rev1 =  to_decimal(cl_list.mnet)
            output_list.percent1 =  to_decimal(cl_list.proz1)
            output_list.ftdrm = cl_list.manz
            output_list.pax2 = cl_list.mpax
            output_list.rm_rev2 =  to_decimal(cl_list.mnet)
            output_list.percent3 =  to_decimal(cl_list.proz1)


    def create_zinrstat():

        nonlocal output_list_list, i, anz, manz, yanz, pax, mpax, ypax, mnet, ynet, net, t_anz, t_manz, t_yanz, t_pax, t_mpax, t_ypax, t_net, t_mnet, t_ynet, from_bez, to_bez, price_decimal, from_date, curr_zeit, ci_date, htparam, zimmer, arrangement, res_line, waehrung, argt_line, artikel, zinrstat, zimkateg, genstat
        nonlocal m_ftd, m_ytd, f_date, t_date, to_date, rm_no, sorttype, lod__rev


        nonlocal output_list, cl_list
        nonlocal output_list_list, cl_list_list

        mm:int = 0
        yy:int = 0
        datum:date = None
        last_zikatnr:int = 0
        anz = 0
        pax = 0
        net =  to_decimal("0")
        manz = 0
        mpax = 0
        mnet =  to_decimal("0")
        yanz = 0
        ypax = 0
        ynet =  to_decimal("0")
        t_anz = 0
        t_pax = 0
        t_manz = 0
        t_mpax = 0
        t_mnet =  to_decimal("0")
        t_yanz = 0
        t_ypax = 0
        t_ynet =  to_decimal("0")

        if m_ftd  and m_ytd == False:
            from_date = f_date
            to_date = t_date
            mm = get_month(to_date)
            yy = get_year(to_date)

        elif m_ftd == False and m_ytd :
            mm = get_month(to_date)
            yy = get_year(to_date)
            from_date = date_mdy(1, 1, yy)
        output_list_list.clear()
        cl_list_list.clear()

        if rm_no != "":

            zimmer = get_cache (Zimmer, {"zinr": [(eq, rm_no)]})

            if zimmer:
                cl_list = Cl_list()
                cl_list_list.append(cl_list)

                cl_list.zinr = rm_no
                cl_list.rmcat = zimmer.kbezeich
                for datum in date_range(from_date,to_date) :

                    zinrstat = get_cache (Zinrstat, {"zinr": [(eq, rm_no)],"datum": [(eq, datum)],"zimmeranz": [(gt, 0)]})

                    if zinrstat:

                        if datum == to_date:
                            cl_list.anz = cl_list.anz + zinrstat.zimmeranz
                            cl_list.net =  to_decimal(cl_list.net) + to_decimal(zinrstat.argtumsatz)
                            cl_list.pax = cl_list.pax + zinrstat.person
                            anz = anz + zinrstat.zimmeranz
                            pax = pax + zinrstat.person
                            net =  to_decimal(net) + to_decimal(zinrstat.argtumsatz)

                        if get_month(zinrstat.datum) == mm and get_year(zinrstat.datum) == yy:
                            cl_list.manz = cl_list.manz + zinrstat.zimmeranz
                            cl_list.mnet =  to_decimal(cl_list.mnet) + to_decimal(zinrstat.argtumsatz)
                            cl_list.mpax = cl_list.mpax + zinrstat.person
                            manz = manz + zinrstat.zimmeranz
                            mpax = mpax + zinrstat.person
                            mnet =  to_decimal(mnet) + to_decimal(zinrstat.argtumsatz)
                        cl_list.yanz = cl_list.yanz + zinrstat.zimmeranz
                        cl_list.ypax = cl_list.ypax + zinrstat.person
                        cl_list.ynet =  to_decimal(cl_list.ynet) + to_decimal(zinrstat.argtumsatz)
                        yanz = yanz + zinrstat.zimmeranz
                        ypax = ypax + zinrstat.person
                        ynet =  to_decimal(ynet) + to_decimal(zinrstat.argtumsatz)
        else:
            rm_no = ""

            if sorttype == 1:

                zimmer_obj_list = {}
                zimmer = Zimmer()
                zimkateg = Zimkateg()
                for zimmer.kbezeich, zimmer.zinr, zimmer.zikatnr, zimmer._recid, zimkateg.kurzbez, zimkateg._recid in db_session.query(Zimmer.kbezeich, Zimmer.zinr, Zimmer.zikatnr, Zimmer._recid, Zimkateg.kurzbez, Zimkateg._recid).join(Zimkateg,(Zimkateg.zikatnr == Zimmer.zikatnr)).order_by(Zimmer.zinr).all():
                    if zimmer_obj_list.get(zimmer._recid):
                        continue
                    else:
                        zimmer_obj_list[zimmer._recid] = True


                    cl_list = Cl_list()
                    cl_list_list.append(cl_list)

                    cl_list.zinr = zimmer.zinr
                    cl_list.rmcat = zimkateg.kurzbez
                    for datum in date_range(from_date,to_date) :

                        zinrstat = get_cache (Zinrstat, {"zinr": [(eq, zimmer.zinr)],"datum": [(eq, datum)],"zimmeranz": [(gt, 0)]})

                        if zinrstat:

                            if datum == to_date:
                                cl_list.anz = cl_list.anz + zinrstat.zimmeranz
                                cl_list.net =  to_decimal(cl_list.net) + to_decimal(zinrstat.argtumsatz)
                                cl_list.pax = cl_list.pax + zinrstat.person
                                anz = anz + zinrstat.zimmeranz
                                pax = pax + zinrstat.person
                                net =  to_decimal(net) + to_decimal(zinrstat.argtumsatz)

                            if get_month(zinrstat.datum) == mm and get_year(zinrstat.datum) == yy:
                                cl_list.manz = cl_list.manz + zinrstat.zimmeranz
                                cl_list.mnet =  to_decimal(cl_list.mnet) + to_decimal(zinrstat.argtumsatz)
                                cl_list.mpax = cl_list.mpax + zinrstat.person
                                manz = manz + zinrstat.zimmeranz
                                mpax = mpax + zinrstat.person
                                mnet =  to_decimal(mnet) + to_decimal(zinrstat.argtumsatz)
                            cl_list.yanz = cl_list.yanz + zinrstat.zimmeranz
                            cl_list.ypax = cl_list.ypax + zinrstat.person
                            cl_list.ynet =  to_decimal(cl_list.ynet) + to_decimal(zinrstat.argtumsatz)
                            yanz = yanz + zinrstat.zimmeranz
                            ypax = ypax + zinrstat.person
                            ynet =  to_decimal(ynet) + to_decimal(zinrstat.argtumsatz)

            elif sorttype == 2:

                zimmer_obj_list = {}
                zimmer = Zimmer()
                zimkateg = Zimkateg()
                for zimmer.kbezeich, zimmer.zinr, zimmer.zikatnr, zimmer._recid, zimkateg.kurzbez, zimkateg._recid in db_session.query(Zimmer.kbezeich, Zimmer.zinr, Zimmer.zikatnr, Zimmer._recid, Zimkateg.kurzbez, Zimkateg._recid).join(Zimkateg,(Zimkateg.zikatnr == Zimmer.zikatnr)).order_by(Zimkateg.zikatnr, Zimmer.zinr).all():
                    if zimmer_obj_list.get(zimmer._recid):
                        continue
                    else:
                        zimmer_obj_list[zimmer._recid] = True

                    if last_zikatnr == 0:
                        last_zikatnr = zimmer.zikatnr

                    if last_zikatnr != zimmer.zikatnr:
                        cl_list = Cl_list()
                        cl_list_list.append(cl_list)

                        cl_list.rmcat = "Total"
                        cl_list.anz = t_anz
                        cl_list.pax = t_pax
                        cl_list.net =  to_decimal(t_net)
                        cl_list.manz = t_manz
                        cl_list.mnet =  to_decimal(t_mnet)
                        cl_list.mpax = t_mpax
                        cl_list.yanz = t_yanz
                        cl_list.ypax = t_ypax
                        cl_list.ynet =  to_decimal(t_ynet)
                        t_anz = 0
                        t_pax = 0
                        t_net =  to_decimal("0")
                        t_manz = 0
                        t_mnet =  to_decimal("0")
                        t_mpax = 0
                        t_yanz = 0
                        t_ynet =  to_decimal("0")
                        t_ypax = 0
                        last_zikatnr = zimmer.zikatnr


                    cl_list = Cl_list()
                    cl_list_list.append(cl_list)

                    cl_list.zinr = zimmer.zinr
                    cl_list.rmcat = zimkateg.kurzbez
                    for datum in date_range(from_date,to_date) :

                        zinrstat = get_cache (Zinrstat, {"zinr": [(eq, zimmer.zinr)],"datum": [(eq, datum)],"zimmeranz": [(gt, 0)]})

                        if zinrstat:

                            if datum == to_date:
                                cl_list.anz = cl_list.anz + zinrstat.zimmeranz
                                cl_list.net =  to_decimal(cl_list.net) + to_decimal(zinrstat.argtumsatz)
                                cl_list.pax = cl_list.pax + zinrstat.person
                                anz = anz + zinrstat.zimmeranz
                                pax = pax + zinrstat.person
                                net =  to_decimal(net) + to_decimal(zinrstat.argtumsatz)
                                t_anz = t_anz + zinrstat.zimmeranz
                                t_pax = t_pax + zinrstat.person
                                t_net =  to_decimal(t_net) + to_decimal(zinrstat.argtumsatz)

                            if get_month(zinrstat.datum) == mm:
                                cl_list.manz = cl_list.manz + zinrstat.zimmeranz
                                cl_list.mnet =  to_decimal(cl_list.mnet) + to_decimal(zinrstat.argtumsatz)
                                cl_list.mpax = cl_list.mpax + zinrstat.person
                                manz = manz + zinrstat.zimmeranz
                                mpax = mpax + zinrstat.person
                                mnet =  to_decimal(mnet) + to_decimal(zinrstat.argtumsatz)
                                t_manz = t_manz + zinrstat.zimmeranz
                                t_mpax = t_mpax + zinrstat.person
                                t_mnet =  to_decimal(t_mnet) + to_decimal(zinrstat.argtumsatz)
                            cl_list.yanz = cl_list.yanz + zinrstat.zimmeranz
                            cl_list.ypax = cl_list.ypax + zinrstat.person
                            cl_list.ynet =  to_decimal(cl_list.ynet) + to_decimal(zinrstat.argtumsatz)
                            yanz = yanz + zinrstat.zimmeranz
                            ypax = ypax + zinrstat.person
                            ynet =  to_decimal(ynet) + to_decimal(zinrstat.argtumsatz)
                            t_yanz = t_yanz + zinrstat.zimmeranz
                            t_ypax = t_ypax + zinrstat.person
                            t_ynet =  to_decimal(t_ynet) + to_decimal(zinrstat.argtumsatz)

            if sorttype == 2:
                cl_list = Cl_list()
                cl_list_list.append(cl_list)

                cl_list.rmcat = "Total"
                cl_list.anz = t_anz
                cl_list.pax = t_pax
                cl_list.net =  to_decimal(t_net)
                cl_list.manz = t_manz
                cl_list.mnet =  to_decimal(t_mnet)
                cl_list.mpax = t_mpax
                cl_list.yanz = t_yanz
                cl_list.ypax = t_ypax
                cl_list.ynet =  to_decimal(t_ynet)


                t_anz = 0
                t_pax = 0
                t_net =  to_decimal("0")
                t_manz = 0
                t_mnet =  to_decimal("0")
                t_mpax = 0
                t_yanz = 0
                t_ynet =  to_decimal("0")
                t_ypax = 0

        for cl_list in query(cl_list_list):

            if net != 0:
                cl_list.proz =  to_decimal(cl_list.net) / to_decimal(net) * to_decimal("100")

            if mnet != 0:
                cl_list.proz1 =  to_decimal(cl_list.mnet) / to_decimal(mnet) * to_decimal("100")

            if ynet != 0:
                cl_list.proz2 =  to_decimal(cl_list.ynet) / to_decimal(ynet) * to_decimal("100")
        cl_list = Cl_list()
        cl_list_list.append(cl_list)

        cl_list.flag = "*"
        cl_list = Cl_list()
        cl_list_list.append(cl_list)

        cl_list.zinr = ""
        cl_list.rmcat = "GTOTAL"
        cl_list.anz = anz
        cl_list.pax = pax
        cl_list.net =  to_decimal(net)

        if net != 0:
            cl_list.proz =  to_decimal("100")
        cl_list.manz = manz
        cl_list.mpax = mpax
        cl_list.mnet =  to_decimal(mnet)

        if mnet != 0:
            cl_list.proz1 =  to_decimal("100")
        cl_list.yanz = yanz
        cl_list.ypax = ypax
        cl_list.ynet =  to_decimal(ynet)

        if ynet != 0:
            cl_list.proz2 =  to_decimal("100")

        for cl_list in query(cl_list_list):
            output_list = Output_list()
            output_list_list.append(output_list)

            output_list.flag = cl_list.flag
            output_list.rmno = cl_list.zinr

            if cl_list.flag.lower()  == ("*").lower() :
                pass
            else:

                if price_decimal == 0:
                    output_list.rmno1 = to_string(cl_list.zinr)
                    output_list.rmtype = to_string(cl_list.rmcat)
                    output_list.rm = cl_list.anz
                    output_list.pax = cl_list.pax
                    output_list.rm_rev =  to_decimal(cl_list.net)
                    output_list.percent =  to_decimal(cl_list.proz)
                    output_list.mtdrm = cl_list.manz
                    output_list.pax1 = cl_list.mpax
                    output_list.rm_rev1 =  to_decimal(cl_list.mnet)
                    output_list.percent1 =  to_decimal(cl_list.proz1)
                    output_list.ftdrm = cl_list.yanz
                    output_list.pax2 = cl_list.ypax
                    output_list.rm_rev2 =  to_decimal(cl_list.ynet)
                    output_list.percent3 =  to_decimal(cl_list.proz2)


                else:
                    output_list = Output_list()
                    output_list_list.append(output_list)

                    output_list.rmno1 = to_string(cl_list.zinr)
                    output_list.rmtype = to_string(cl_list.rmcat)
                    output_list.rm = cl_list.anz
                    output_list.pax = cl_list.pax
                    output_list.rm_rev =  to_decimal(cl_list.net)
                    output_list.percent =  to_decimal(cl_list.proz)
                    output_list.mtdrm = cl_list.manz
                    output_list.pax1 = cl_list.mpax
                    output_list.rm_rev1 =  to_decimal(cl_list.mnet)
                    output_list.percent1 =  to_decimal(cl_list.proz1)
                    output_list.ftdrm = cl_list.yanz
                    output_list.pax2 = cl_list.ypax
                    output_list.rm_rev2 =  to_decimal(cl_list.ynet)
                    output_list.percent3 =  to_decimal(cl_list.proz2)


    def create_genstat():

        nonlocal output_list_list, i, anz, manz, yanz, pax, mpax, ypax, mnet, ynet, net, t_anz, t_manz, t_yanz, t_pax, t_mpax, t_ypax, t_net, t_mnet, t_ynet, from_bez, to_bez, price_decimal, from_date, curr_zeit, ci_date, htparam, zimmer, arrangement, res_line, waehrung, argt_line, artikel, zinrstat, zimkateg, genstat
        nonlocal m_ftd, m_ytd, f_date, t_date, to_date, rm_no, sorttype, lod__rev


        nonlocal output_list, cl_list
        nonlocal output_list_list, cl_list_list

        mm:int = 0
        yy:int = 0
        datum:date = None
        last_zikatnr:int = 0
        anz = 0
        pax = 0
        net =  to_decimal("0")
        manz = 0
        mpax = 0
        mnet =  to_decimal("0")
        yanz = 0
        ypax = 0
        ynet =  to_decimal("0")
        t_anz = 0
        t_pax = 0
        t_manz = 0
        t_mpax = 0
        t_mnet =  to_decimal("0")
        t_yanz = 0
        t_ypax = 0
        t_ynet =  to_decimal("0")

        if m_ftd :
            from_date = f_date
            to_date = t_date
            mm = get_month(to_date)
            yy = get_year(to_date)
        else:
            mm = get_month(to_date)
            yy = get_year(to_date)
            from_date = date_mdy(1, 1, yy)
        output_list_list.clear()
        output_list_list.clear()

        if rm_no != "":

            zimmer = get_cache (Zimmer, {"zinr": [(eq, rm_no)]})

            if zimmer:
                cl_list = Cl_list()
                cl_list_list.append(cl_list)

                cl_list.zinr = rm_no
                cl_list.rmcat = zimmer.kbezeich
                for datum in date_range(from_date,to_date) :

                    for genstat in db_session.query(Genstat).filter(
                             (Genstat.zinr == (rm_no).lower()) & (Genstat.datum == datum) & ((Genstat.resstatus == 6) | (Genstat.resstatus == 8))).order_by(Genstat._recid).all():

                        if datum == to_date:
                            cl_list.anz = cl_list.anz + 1
                            cl_list.net =  to_decimal(cl_list.net) + to_decimal(genstat.logis)
                            cl_list.pax = cl_list.pax + genstat.erwachs + genstat.gratis + genstat.kind1 + genstat.kind2 + genstat.kind3
                            anz = anz + 1
                            pax = pax + genstat.erwachs + genstat.gratis + genstat.kind1 + genstat.kind2 + genstat.kind3
                            net =  to_decimal(net) + to_decimal(genstat.logis)

                        if get_month(genstat.datum) == mm and get_year(genstat.datum) == yy:
                            cl_list.manz = cl_list.manz + 1
                            cl_list.mnet =  to_decimal(cl_list.mnet) + to_decimal(genstat.logis)
                            cl_list.mpax = cl_list.mpax + genstat.erwachs + genstat.gratis + genstat.kind1 + genstat.kind2 + genstat.kind3
                            manz = manz + 1
                            mpax = mpax + genstat.erwachs + genstat.gratis + genstat.kind1 + genstat.kind2 + genstat.kind3
                            mnet =  to_decimal(mnet) + to_decimal(genstat.logis)
                        cl_list.yanz = cl_list.yanz + 1
                        cl_list.ypax = cl_list.ypax + genstat.erwachs + genstat.gratis + genstat.kind1 + genstat.kind2 + genstat.kind3
                        cl_list.ynet =  to_decimal(cl_list.ynet) + to_decimal(genstat.logis)
                        yanz = yanz + 1
                        ypax = ypax + genstat.erwachs + genstat.gratis + genstat.kind1 + genstat.kind2 + genstat.kind3
                        ynet =  to_decimal(ynet) + to_decimal(genstat.logis)
        else:
            rm_no = ""

            if sorttype == 1:

                zimmer_obj_list = {}
                zimmer = Zimmer()
                zimkateg = Zimkateg()
                for zimmer.kbezeich, zimmer.zinr, zimmer.zikatnr, zimmer._recid, zimkateg.kurzbez, zimkateg._recid in db_session.query(Zimmer.kbezeich, Zimmer.zinr, Zimmer.zikatnr, Zimmer._recid, Zimkateg.kurzbez, Zimkateg._recid).join(Zimkateg,(Zimkateg.zikatnr == Zimmer.zikatnr)).order_by(Zimmer.zinr).all():
                    if zimmer_obj_list.get(zimmer._recid):
                        continue
                    else:
                        zimmer_obj_list[zimmer._recid] = True


                    cl_list = Cl_list()
                    cl_list_list.append(cl_list)

                    cl_list.zinr = zimmer.zinr
                    cl_list.rmcat = zimkateg.kurzbez
                    for datum in date_range(from_date,to_date) :

                        for genstat in db_session.query(Genstat).filter(
                                 (Genstat.zinr == zimmer.zinr) & (Genstat.datum == datum) & ((Genstat.resstatus == 6) | (Genstat.resstatus == 8))).order_by(Genstat._recid).all():

                            if datum == to_date:
                                cl_list.anz = cl_list.anz + 1
                                cl_list.net =  to_decimal(cl_list.net) + to_decimal(genstat.logis)
                                cl_list.pax = cl_list.pax + genstat.erwachs + genstat.gratis +\
                                        genstat.kind1 + genstat.kind2 + genstat.kind3
                                anz = anz + 1
                                pax = pax + genstat.erwachs + genstat.gratis +\
                                        genstat.kind1 + genstat.kind2 + genstat.kind3


                                net =  to_decimal(net) + to_decimal(genstat.logis)

                            if get_month(genstat.datum) == mm and get_year(genstat.datum) == yy:
                                cl_list.manz = cl_list.manz + 1
                                cl_list.mnet =  to_decimal(cl_list.mnet) + to_decimal(genstat.logis)
                                cl_list.mpax = cl_list.mpax + genstat.erwachs + genstat.gratis +\
                                        genstat.kind1 + genstat.kind2 + genstat.kind3
                                manz = manz + 1
                                mpax = mpax + genstat.erwachs + genstat.gratis +\
                                        genstat.kind1 + genstat.kind2 + genstat.kind3
                                mnet =  to_decimal(mnet) + to_decimal(genstat.logis)


                            cl_list.yanz = cl_list.yanz + 1
                            cl_list.ypax = cl_list.ypax + genstat.erwachs + genstat.gratis +\
                                    genstat.kind1 + genstat.kind2 + genstat.kind3
                            cl_list.ynet =  to_decimal(cl_list.ynet) + to_decimal(genstat.logis)
                            yanz = yanz + 1
                            ypax = ypax + genstat.erwachs + genstat.gratis +\
                                    genstat.kind1 + genstat.kind2 + genstat.kind3
                            ynet =  to_decimal(ynet) + to_decimal(genstat.logis)

            elif sorttype == 2:

                zimmer_obj_list = {}
                zimmer = Zimmer()
                zimkateg = Zimkateg()
                for zimmer.kbezeich, zimmer.zinr, zimmer.zikatnr, zimmer._recid, zimkateg.kurzbez, zimkateg._recid in db_session.query(Zimmer.kbezeich, Zimmer.zinr, Zimmer.zikatnr, Zimmer._recid, Zimkateg.kurzbez, Zimkateg._recid).join(Zimkateg,(Zimkateg.zikatnr == Zimmer.zikatnr)).order_by(Zimkateg.zikatnr, Zimmer.zinr).all():
                    if zimmer_obj_list.get(zimmer._recid):
                        continue
                    else:
                        zimmer_obj_list[zimmer._recid] = True

                    if last_zikatnr == 0:
                        last_zikatnr = zimmer.zikatnr

                    if last_zikatnr != zimmer.zikatnr:
                        cl_list = Cl_list()
                        cl_list_list.append(cl_list)

                        cl_list.rmcat = "Total"
                        cl_list.anz = t_anz
                        cl_list.pax = t_pax
                        cl_list.net =  to_decimal(t_net)
                        cl_list.manz = t_manz
                        cl_list.mnet =  to_decimal(t_mnet)
                        cl_list.mpax = t_mpax
                        cl_list.yanz = t_yanz
                        cl_list.ypax = t_ypax
                        cl_list.ynet =  to_decimal(t_ynet)
                        t_anz = 0
                        t_pax = 0
                        t_net =  to_decimal("0")
                        t_manz = 0
                        t_mnet =  to_decimal("0")
                        t_mpax = 0
                        t_yanz = 0
                        t_ynet =  to_decimal("0")
                        t_ypax = 0


                        last_zikatnr = zimmer.zikatnr
                    cl_list = Cl_list()
                    cl_list_list.append(cl_list)

                    cl_list.zinr = zimmer.zinr
                    cl_list.rmcat = zimkateg.kurzbez
                    for datum in date_range(from_date,to_date) :

                        for genstat in db_session.query(Genstat).filter(
                                 (Genstat.zinr == zimmer.zinr) & (Genstat.datum == datum) & ((Genstat.resstatus == 6) | (Genstat.resstatus == 8))).order_by(Genstat._recid).all():

                            if datum == to_date:
                                cl_list.anz = cl_list.anz + 1
                                cl_list.net =  to_decimal(cl_list.net) + to_decimal(genstat.logis)
                                cl_list.pax = cl_list.pax + genstat.erwachs + genstat.gratis +\
                                        genstat.kind1 + genstat.kind2 + genstat.kind3
                                anz = anz + 1
                                pax = pax + genstat.erwachs + genstat.gratis +\
                                        genstat.kind1 + genstat.kind2 + genstat.kind3
                                net =  to_decimal(net) + to_decimal(genstat.logis)
                                t_anz = t_anz + 1
                                t_pax = t_pax + genstat.erwachs + genstat.gratis +\
                                        genstat.kind1 + genstat.kind2 + genstat.kind3
                                t_net =  to_decimal(t_net) + to_decimal(genstat.logis)

                            if get_month(genstat.datum) == mm:
                                cl_list.manz = cl_list.manz + 1
                                cl_list.mnet =  to_decimal(cl_list.mnet) + to_decimal(genstat.logis)
                                cl_list.mpax = cl_list.mpax + genstat.erwachs + genstat.gratis +\
                                        genstat.kind1 + genstat.kind2 + genstat.kind3
                                manz = manz + 1
                                mpax = mpax + genstat.erwachs + genstat.gratis +\
                                        genstat.kind1 + genstat.kind2 + genstat.kind3
                                mnet =  to_decimal(mnet) + to_decimal(genstat.logis)
                                t_manz = t_manz + 1
                                t_mpax = t_mpax + genstat.erwachs + genstat.gratis +\
                                        genstat.kind1 + genstat.kind2 + genstat.kind3
                                t_mnet =  to_decimal(t_mnet) + to_decimal(genstat.logis)


                            cl_list.yanz = cl_list.yanz + 1
                            cl_list.ypax = cl_list.ypax + genstat.erwachs + genstat.gratis +\
                                    genstat.kind1 + genstat.kind2 + genstat.kind3
                            cl_list.ynet =  to_decimal(cl_list.ynet) + to_decimal(genstat.logis)
                            yanz = yanz + 1
                            ypax = ypax + genstat.erwachs + genstat.gratis +\
                                    genstat.kind1 + genstat.kind2 + genstat.kind3
                            ynet =  to_decimal(ynet) + to_decimal(genstat.logis)
                            t_yanz = t_yanz + 1
                            t_ypax = t_ypax + genstat.erwachs + genstat.gratis +\
                                    genstat.kind1 + genstat.kind2 + genstat.kind3
                            t_ynet =  to_decimal(t_ynet) + to_decimal(genstat.logis)

            if sorttype == 2:
                cl_list = Cl_list()
                cl_list_list.append(cl_list)

                cl_list.rmcat = "Total"
                cl_list.anz = t_anz
                cl_list.pax = t_pax
                cl_list.net =  to_decimal(t_net)
                cl_list.manz = t_manz
                cl_list.mnet =  to_decimal(t_mnet)
                cl_list.mpax = t_mpax
                cl_list.yanz = t_yanz
                cl_list.ypax = t_ypax
                cl_list.ynet =  to_decimal(t_ynet)


                t_anz = 0
                t_pax = 0
                t_net =  to_decimal("0")
                t_manz = 0
                t_mnet =  to_decimal("0")
                t_mpax = 0
                t_yanz = 0
                t_ynet =  to_decimal("0")
                t_ypax = 0

        for cl_list in query(cl_list_list):

            if net != 0:
                cl_list.proz =  to_decimal(cl_list.net) / to_decimal(net) * to_decimal("100")

            if mnet != 0:
                cl_list.proz1 =  to_decimal(cl_list.mnet) / to_decimal(mnet) * to_decimal("100")

            if ynet != 0:
                cl_list.proz2 =  to_decimal(cl_list.ynet) / to_decimal(ynet) * to_decimal("100")
        cl_list = Cl_list()
        cl_list_list.append(cl_list)

        cl_list.zinr = ""
        cl_list.rmcat = "GTOTAL"
        cl_list.anz = anz
        cl_list.pax = pax
        cl_list.net =  to_decimal(net)

        if net != 0:
            cl_list.proz =  to_decimal("100")
        cl_list.manz = manz
        cl_list.mpax = mpax
        cl_list.mnet =  to_decimal(mnet)

        if mnet != 0:
            cl_list.proz1 =  to_decimal("100")
        cl_list.yanz = yanz
        cl_list.ypax = ypax
        cl_list.ynet =  to_decimal(ynet)

        if ynet != 0:
            cl_list.proz2 =  to_decimal("100")

        for cl_list in query(cl_list_list):
            output_list = Output_list()
            output_list_list.append(output_list)

            output_list.rmno1 = to_string(cl_list.zinr)
            output_list.rmtype = to_string(cl_list.rmcat)
            output_list.rm = cl_list.anz
            output_list.pax = cl_list.pax
            output_list.rm_rev =  to_decimal(cl_list.net)
            output_list.percent =  to_decimal(cl_list.proz)
            output_list.mtdrm = cl_list.manz
            output_list.pax1 = cl_list.mpax
            output_list.rm_rev1 =  to_decimal(cl_list.mnet)
            output_list.percent1 =  to_decimal(cl_list.proz1)
            output_list.ftdrm = cl_list.yanz
            output_list.pax2 = cl_list.ypax
            output_list.rm_rev2 =  to_decimal(cl_list.ynet)
            output_list.percent3 =  to_decimal(cl_list.proz2)


    ci_date = get_output(htpdate(87))

    if m_ftd and f_date >= ci_date and t_date >= ci_date:
        create_resline()
    else:

        if lod__rev :
            create_genstat()
        else:
            create_zinrstat()

    return generate_output()