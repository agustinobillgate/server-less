#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from functions.htpdate import htpdate
from functions.argt_betrag import argt_betrag
from models import Htparam, Zimmer, Reservation, Arrangement, Res_line, Waehrung, Segment, Argt_line, Artikel, Zinrstat, Genstat, Zimkateg

payload_list_data, Payload_list = create_model("Payload_list", {"show_breakdown_comphu":bool})

def rm_revenue_3_webbl(m_ftd:bool, m_ytd:bool, f_date:date, t_date:date, to_date:date, rm_no:string, sorttype:int, lod__rev:bool, excl_compl:bool, payload_list_data:[Payload_list]):

    prepare_cache ([Htparam, Zimmer, Reservation, Arrangement, Res_line, Waehrung, Segment, Argt_line, Zinrstat, Genstat, Zimkateg])

    output_list_data = []
    i:int = 0
    anz:int = 0
    manz:int = 0
    yanz:int = 0
    com_anz:int = 0
    com_manz:int = 0
    com_yanz:int = 0
    hu_anz:int = 0
    hu_manz:int = 0
    hu_yanz:int = 0
    pax:int = 0
    mpax:int = 0
    ypax:int = 0
    com_pax:int = 0
    com_mpax:int = 0
    com_ypax:int = 0
    hu_pax:int = 0
    hu_mpax:int = 0
    hu_ypax:int = 0
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
    t_com_anz:int = 0
    t_com_pax:int = 0
    t_com_manz:int = 0
    t_com_mpax:int = 0
    t_com_yanz:int = 0
    t_com_ypax:int = 0
    t_hu_anz:int = 0
    t_hu_pax:int = 0
    t_hu_manz:int = 0
    t_hu_mpax:int = 0
    t_hu_yanz:int = 0
    t_hu_ypax:int = 0
    from_bez:string = ""
    to_bez:string = ""
    price_decimal:int = 0
    from_date:date = None
    curr_zeit:int = 0
    ci_date:date = None
    do_it:bool = False
    compli_flag:bool = False
    hu_flag:bool = False
    htparam = zimmer = reservation = arrangement = res_line = waehrung = segment = argt_line = artikel = zinrstat = genstat = zimkateg = None

    output_list = cl_list = payload_list = None

    output_list_data, Output_list = create_model("Output_list", {"rmno":string, "flag":string, "str":string, "rmno1":string, "rmtype":string, "rm":int, "pax":int, "com_rm":int, "com_pax":int, "hu_rm":int, "hu_pax":int, "rm_rev":Decimal, "percent":Decimal, "mtdrm":int, "pax1":int, "com_mtdrm":int, "com_pax1":int, "hu_mtdrm":int, "hu_pax1":int, "rm_rev1":Decimal, "percent1":Decimal, "ftdrm":int, "pax2":int, "com_ftdrm":int, "com_pax2":int, "hu_ftdrm":int, "hu_pax2":int, "rm_rev2":Decimal, "percent3":Decimal})
    cl_list_data, Cl_list = create_model("Cl_list", {"flag":string, "zinr":string, "rmcat":string, "anz":int, "pax":int, "com_anz":int, "com_pax":int, "hu_anz":int, "hu_pax":int, "net":Decimal, "proz":Decimal, "manz":int, "mpax":int, "com_manz":int, "com_mpax":int, "hu_manz":int, "hu_mpax":int, "mnet":Decimal, "proz1":Decimal, "yanz":int, "ypax":int, "com_yanz":int, "com_ypax":int, "hu_yanz":int, "hu_ypax":int, "ynet":Decimal, "proz2":Decimal})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal output_list_data, i, anz, manz, yanz, com_anz, com_manz, com_yanz, hu_anz, hu_manz, hu_yanz, pax, mpax, ypax, com_pax, com_mpax, com_ypax, hu_pax, hu_mpax, hu_ypax, mnet, ynet, net, t_anz, t_manz, t_yanz, t_pax, t_mpax, t_ypax, t_net, t_mnet, t_ynet, t_com_anz, t_com_pax, t_com_manz, t_com_mpax, t_com_yanz, t_com_ypax, t_hu_anz, t_hu_pax, t_hu_manz, t_hu_mpax, t_hu_yanz, t_hu_ypax, from_bez, to_bez, price_decimal, from_date, curr_zeit, ci_date, do_it, compli_flag, hu_flag, htparam, zimmer, reservation, arrangement, res_line, waehrung, segment, argt_line, artikel, zinrstat, genstat, zimkateg
        nonlocal m_ftd, m_ytd, f_date, t_date, to_date, rm_no, sorttype, lod__rev, excl_compl


        nonlocal output_list, cl_list, payload_list
        nonlocal output_list_data, cl_list_data

        return {"output-list": output_list_data}

    def create_resline():

        nonlocal output_list_data, i, anz, manz, yanz, com_anz, com_manz, com_yanz, hu_anz, hu_manz, hu_yanz, pax, mpax, ypax, com_pax, com_mpax, com_ypax, hu_pax, hu_mpax, hu_ypax, mnet, ynet, net, t_anz, t_manz, t_yanz, t_pax, t_mpax, t_ypax, t_net, t_mnet, t_ynet, t_com_anz, t_com_pax, t_com_manz, t_com_mpax, t_com_yanz, t_com_ypax, t_hu_anz, t_hu_pax, t_hu_manz, t_hu_mpax, t_hu_yanz, t_hu_ypax, from_bez, to_bez, from_date, curr_zeit, ci_date, do_it, compli_flag, hu_flag, htparam, zimmer, reservation, arrangement, res_line, waehrung, segment, argt_line, artikel, zinrstat, genstat, zimkateg
        nonlocal m_ftd, m_ytd, f_date, t_date, to_date, rm_no, sorttype, lod__rev, excl_compl


        nonlocal output_list, cl_list, payload_list
        nonlocal output_list_data, cl_list_data

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
            cl_list_data.append(cl_list)

            cl_list.zinr = rm_no

            zimmer = get_cache (Zimmer, {"zinr": [(eq, rm_no)]})

            if zimmer:
                cl_list.rmcat = zimmer.kbezeich

            res_line_obj_list = {}
            res_line = Res_line()
            reservation = Reservation()
            arrangement = Arrangement()
            zimmer = Zimmer()
            for res_line.reserve_dec, res_line.betriebsnr, res_line.ankunft, res_line.abreise, res_line.zipreis, res_line._recid, res_line.zimmeranz, res_line.erwachs, res_line.gratis, res_line.kind1, res_line.kind2, res_line.zinr, res_line.zikatnr, reservation.segmentcode, reservation._recid, arrangement.argtnr, arrangement._recid, zimmer.kbezeich, zimmer.zikatnr, zimmer.zinr, zimmer._recid in db_session.query(Res_line.reserve_dec, Res_line.betriebsnr, Res_line.ankunft, Res_line.abreise, Res_line.zipreis, Res_line._recid, Res_line.zimmeranz, Res_line.erwachs, Res_line.gratis, Res_line.kind1, Res_line.kind2, Res_line.zinr, Res_line.zikatnr, Reservation.segmentcode, Reservation._recid, Arrangement.argtnr, Arrangement._recid, Zimmer.kbezeich, Zimmer.zikatnr, Zimmer.zinr, Zimmer._recid).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Arrangement,(Arrangement.arrangement == Res_line.arrangement)).join(Zimmer,(Zimmer.zinr == Res_line.zinr)).filter(
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
                do_it = True

                if excl_compl:

                    segment = db_session.query(Segment).filter(
                             (Segment.segmentcode == reservation.segmentcode) & ((Segment.betriebsnr == 1) | (Segment.betriebsnr == 2))).first()

                    if segment:
                        do_it = False

                if do_it:
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
                reservation = Reservation()
                arrangement = Arrangement()
                zimmer = Zimmer()
                for res_line.reserve_dec, res_line.betriebsnr, res_line.ankunft, res_line.abreise, res_line.zipreis, res_line._recid, res_line.zimmeranz, res_line.erwachs, res_line.gratis, res_line.kind1, res_line.kind2, res_line.zinr, res_line.zikatnr, reservation.segmentcode, reservation._recid, arrangement.argtnr, arrangement._recid, zimmer.kbezeich, zimmer.zikatnr, zimmer.zinr, zimmer._recid in db_session.query(Res_line.reserve_dec, Res_line.betriebsnr, Res_line.ankunft, Res_line.abreise, Res_line.zipreis, Res_line._recid, Res_line.zimmeranz, Res_line.erwachs, Res_line.gratis, Res_line.kind1, Res_line.kind2, Res_line.zinr, Res_line.zikatnr, Reservation.segmentcode, Reservation._recid, Arrangement.argtnr, Arrangement._recid, Zimmer.kbezeich, Zimmer.zikatnr, Zimmer.zinr, Zimmer._recid).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Arrangement,(Arrangement.arrangement == Res_line.arrangement)).join(Zimmer,(Zimmer.zinr == Res_line.zinr)).filter(
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

                    cl_list = query(cl_list_data, filters=(lambda cl_list: cl_list.zinr == res_line.zinr and cl_list.rmcat == zimmer.kbezeich), first=True)

                    if not cl_list:
                        cl_list = Cl_list()
                        cl_list_data.append(cl_list)

                        cl_list.zinr = res_line.zinr
                        cl_list.rmcat = zimmer.kbezeich
                    do_it = True

                    if excl_compl:

                        segment = db_session.query(Segment).filter(
                                 (Segment.segmentcode == reservation.segmentcode) & ((Segment.betriebsnr == 1) | (Segment.betriebsnr == 2))).first()

                        if segment:
                            do_it = False

                    if do_it:
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
                reservation = Reservation()
                arrangement = Arrangement()
                zimmer = Zimmer()
                for res_line.reserve_dec, res_line.betriebsnr, res_line.ankunft, res_line.abreise, res_line.zipreis, res_line._recid, res_line.zimmeranz, res_line.erwachs, res_line.gratis, res_line.kind1, res_line.kind2, res_line.zinr, res_line.zikatnr, reservation.segmentcode, reservation._recid, arrangement.argtnr, arrangement._recid, zimmer.kbezeich, zimmer.zikatnr, zimmer.zinr, zimmer._recid in db_session.query(Res_line.reserve_dec, Res_line.betriebsnr, Res_line.ankunft, Res_line.abreise, Res_line.zipreis, Res_line._recid, Res_line.zimmeranz, Res_line.erwachs, Res_line.gratis, Res_line.kind1, Res_line.kind2, Res_line.zinr, Res_line.zikatnr, Reservation.segmentcode, Reservation._recid, Arrangement.argtnr, Arrangement._recid, Zimmer.kbezeich, Zimmer.zikatnr, Zimmer.zinr, Zimmer._recid).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Arrangement,(Arrangement.arrangement == Res_line.arrangement)).join(Zimmer,(Zimmer.zinr == Res_line.zinr)).filter(
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
                            cl_list_data.append(cl_list)

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
                        cl_list_data.append(cl_list)

                        cl_list.zinr = res_line.zinr
                        cl_list.rmcat = zimmer.kbezeich
                        last_zikatnr = res_line.zikatnr
                        last_zinr = res_line.zinr
                    do_it = True

                    if excl_compl:

                        segment = db_session.query(Segment).filter(
                                 (Segment.segmentcode == reservation.segmentcode) & ((Segment.betriebsnr == 1) | (Segment.betriebsnr == 2))).first()

                        if segment:
                            do_it = False

                    if do_it:
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
                cl_list_data.append(cl_list)

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

        for cl_list in query(cl_list_data):

            if net != 0:
                cl_list.proz =  to_decimal(cl_list.net) / to_decimal(net) * to_decimal("100")

            if mnet != 0:
                cl_list.proz1 =  to_decimal(cl_list.mnet) / to_decimal(mnet) * to_decimal("100")
        cl_list = Cl_list()
        cl_list_data.append(cl_list)

        cl_list.flag = "*"
        cl_list.zinr = ""
        cl_list = Cl_list()
        cl_list_data.append(cl_list)

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

        for cl_list in query(cl_list_data):
            output_list = Output_list()
            output_list_data.append(output_list)

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

        nonlocal output_list_data, i, anz, manz, yanz, com_anz, com_manz, com_yanz, hu_anz, hu_manz, hu_yanz, pax, mpax, ypax, com_pax, com_mpax, com_ypax, hu_pax, hu_mpax, hu_ypax, mnet, ynet, net, t_anz, t_manz, t_yanz, t_pax, t_mpax, t_ypax, t_net, t_mnet, t_ynet, t_com_anz, t_com_pax, t_com_manz, t_com_mpax, t_com_yanz, t_com_ypax, t_hu_anz, t_hu_pax, t_hu_manz, t_hu_mpax, t_hu_yanz, t_hu_ypax, from_bez, to_bez, price_decimal, from_date, curr_zeit, ci_date, do_it, compli_flag, hu_flag, htparam, zimmer, reservation, arrangement, res_line, waehrung, segment, argt_line, artikel, zinrstat, genstat, zimkateg
        nonlocal m_ftd, m_ytd, f_date, t_date, to_date, rm_no, sorttype, lod__rev, excl_compl


        nonlocal output_list, cl_list, payload_list
        nonlocal output_list_data, cl_list_data

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
        output_list_data.clear()
        cl_list_data.clear()

        if rm_no != "":

            zimmer = get_cache (Zimmer, {"zinr": [(eq, rm_no)]})

            if zimmer:
                cl_list = Cl_list()
                cl_list_data.append(cl_list)

                cl_list.zinr = rm_no
                cl_list.rmcat = zimmer.kbezeich
                for datum in date_range(from_date,to_date) :

                    zinrstat = get_cache (Zinrstat, {"zinr": [(eq, rm_no)],"datum": [(eq, datum)],"zimmeranz": [(gt, 0)]})

                    if zinrstat:
                        do_it = True

                        if excl_compl:

                            genstat = db_session.query(Genstat).filter(
                                     (Genstat.datum == datum) & (Genstat.zikatnr == zimmer.zikatnr) & (Genstat.zinr == zimmer.zinr) & (Genstat.zipreis == 0) & (Genstat.gratis != 0) & (Genstat.resstatus == 6) & (Genstat.res_logic[inc_value(1)])).first()

                            if genstat:

                                segment = db_session.query(Segment).filter(
                                         (Segment.segmentcode == genstat.segmentcode) & ((Segment.betriebsnr == 1) | (Segment.betriebsnr == 2))).first()

                                if segment:
                                    do_it = False

                        if do_it:

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
                for zimmer.kbezeich, zimmer.zikatnr, zimmer.zinr, zimmer._recid, zimkateg.kurzbez, zimkateg._recid in db_session.query(Zimmer.kbezeich, Zimmer.zikatnr, Zimmer.zinr, Zimmer._recid, Zimkateg.kurzbez, Zimkateg._recid).join(Zimkateg,(Zimkateg.zikatnr == Zimmer.zikatnr)).order_by(Zimmer.zinr).all():
                    if zimmer_obj_list.get(zimmer._recid):
                        continue
                    else:
                        zimmer_obj_list[zimmer._recid] = True


                    cl_list = Cl_list()
                    cl_list_data.append(cl_list)

                    cl_list.zinr = zimmer.zinr
                    cl_list.rmcat = zimkateg.kurzbez
                    for datum in date_range(from_date,to_date) :

                        zinrstat = get_cache (Zinrstat, {"zinr": [(eq, zimmer.zinr)],"datum": [(eq, datum)],"zimmeranz": [(gt, 0)]})

                        if zinrstat:
                            do_it = True

                            if excl_compl:

                                genstat = db_session.query(Genstat).filter(
                                         (Genstat.datum == datum) & (Genstat.zikatnr == zimmer.zikatnr) & (Genstat.zinr == zimmer.zinr) & (Genstat.zipreis == 0) & (Genstat.gratis != 0) & (Genstat.resstatus == 6) & (Genstat.res_logic[inc_value(1)])).first()

                                if genstat:

                                    segment = db_session.query(Segment).filter(
                                             (Segment.segmentcode == genstat.segmentcode) & ((Segment.betriebsnr == 1) | (Segment.betriebsnr == 2))).first()

                                    if segment:
                                        do_it = False

                            if do_it:

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
                for zimmer.kbezeich, zimmer.zikatnr, zimmer.zinr, zimmer._recid, zimkateg.kurzbez, zimkateg._recid in db_session.query(Zimmer.kbezeich, Zimmer.zikatnr, Zimmer.zinr, Zimmer._recid, Zimkateg.kurzbez, Zimkateg._recid).join(Zimkateg,(Zimkateg.zikatnr == Zimmer.zikatnr)).order_by(Zimkateg.zikatnr, Zimmer.zinr).all():
                    if zimmer_obj_list.get(zimmer._recid):
                        continue
                    else:
                        zimmer_obj_list[zimmer._recid] = True

                    if last_zikatnr == 0:
                        last_zikatnr = zimmer.zikatnr

                    if last_zikatnr != zimmer.zikatnr:
                        cl_list = Cl_list()
                        cl_list_data.append(cl_list)

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
                    cl_list_data.append(cl_list)

                    cl_list.zinr = zimmer.zinr
                    cl_list.rmcat = zimkateg.kurzbez
                    for datum in date_range(from_date,to_date) :

                        zinrstat = get_cache (Zinrstat, {"zinr": [(eq, zimmer.zinr)],"datum": [(eq, datum)],"zimmeranz": [(gt, 0)]})

                        if zinrstat:
                            do_it = True

                            if excl_compl:

                                genstat = db_session.query(Genstat).filter(
                                         (Genstat.datum == datum) & (Genstat.zikatnr == zimmer.zikatnr) & (Genstat.zinr == zimmer.zinr) & (Genstat.zipreis == 0) & (Genstat.gratis != 0) & (Genstat.resstatus == 6) & (Genstat.res_logic[inc_value(1)])).first()

                                if genstat:

                                    segment = db_session.query(Segment).filter(
                                             (Segment.segmentcode == genstat.segmentcode) & ((Segment.betriebsnr == 1) | (Segment.betriebsnr == 2))).first()

                                    if segment:
                                        do_it = False

                            if do_it:

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
                cl_list_data.append(cl_list)

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

        for cl_list in query(cl_list_data):

            if net != 0:
                cl_list.proz =  to_decimal(cl_list.net) / to_decimal(net) * to_decimal("100")

            if mnet != 0:
                cl_list.proz1 =  to_decimal(cl_list.mnet) / to_decimal(mnet) * to_decimal("100")

            if ynet != 0:
                cl_list.proz2 =  to_decimal(cl_list.ynet) / to_decimal(ynet) * to_decimal("100")
        cl_list = Cl_list()
        cl_list_data.append(cl_list)

        cl_list.flag = "*"
        cl_list = Cl_list()
        cl_list_data.append(cl_list)

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

        for cl_list in query(cl_list_data):
            output_list = Output_list()
            output_list_data.append(output_list)

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
                    output_list_data.append(output_list)

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

        nonlocal output_list_data, i, anz, manz, yanz, com_anz, com_manz, com_yanz, hu_anz, hu_manz, hu_yanz, pax, mpax, ypax, com_pax, com_mpax, com_ypax, hu_pax, hu_mpax, hu_ypax, mnet, ynet, net, t_anz, t_manz, t_yanz, t_pax, t_mpax, t_ypax, t_net, t_mnet, t_ynet, t_com_anz, t_com_pax, t_com_manz, t_com_mpax, t_com_yanz, t_com_ypax, t_hu_anz, t_hu_pax, t_hu_manz, t_hu_mpax, t_hu_yanz, t_hu_ypax, from_bez, to_bez, price_decimal, from_date, curr_zeit, ci_date, do_it, compli_flag, hu_flag, htparam, zimmer, reservation, arrangement, res_line, waehrung, segment, argt_line, artikel, zinrstat, genstat, zimkateg
        nonlocal m_ftd, m_ytd, f_date, t_date, to_date, rm_no, sorttype, lod__rev, excl_compl


        nonlocal output_list, cl_list, payload_list
        nonlocal output_list_data, cl_list_data

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
        output_list_data.clear()
        output_list_data.clear()

        if rm_no != "":

            zimmer = get_cache (Zimmer, {"zinr": [(eq, rm_no)]})

            if zimmer:
                cl_list = Cl_list()
                cl_list_data.append(cl_list)

                cl_list.zinr = rm_no
                cl_list.rmcat = zimmer.kbezeich
                for datum in date_range(from_date,to_date) :

                    for genstat in db_session.query(Genstat).filter(
                             (Genstat.zinr == (rm_no).lower()) & (Genstat.datum == datum) & ((Genstat.resstatus == 6) | (Genstat.resstatus == 8))).order_by(Genstat._recid).all():
                        do_it = True

                        if excl_compl:

                            segment = db_session.query(Segment).filter(
                                     (Segment.segmentcode == genstat.segmentcode) & ((Segment.betriebsnr == 1) | (Segment.betriebsnr == 2))).first()

                            if segment:
                                do_it = False
                            else:

                                if genstat.zipreis == 0 and genstat.gratis != 0 and genstat.resstatus == 6 and genstat.res_logic[1] :
                                    do_it = False

                        if do_it:

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
                for zimmer.kbezeich, zimmer.zikatnr, zimmer.zinr, zimmer._recid, zimkateg.kurzbez, zimkateg._recid in db_session.query(Zimmer.kbezeich, Zimmer.zikatnr, Zimmer.zinr, Zimmer._recid, Zimkateg.kurzbez, Zimkateg._recid).join(Zimkateg,(Zimkateg.zikatnr == Zimmer.zikatnr)).order_by(Zimmer.zinr).all():
                    if zimmer_obj_list.get(zimmer._recid):
                        continue
                    else:
                        zimmer_obj_list[zimmer._recid] = True


                    cl_list = Cl_list()
                    cl_list_data.append(cl_list)

                    cl_list.zinr = zimmer.zinr
                    cl_list.rmcat = zimkateg.kurzbez
                    for datum in date_range(from_date,to_date) :

                        for genstat in db_session.query(Genstat).filter(
                                 (Genstat.zinr == zimmer.zinr) & (Genstat.datum == datum) & ((Genstat.resstatus == 6) | (Genstat.resstatus == 8))).order_by(Genstat._recid).all():
                            do_it = True

                            if excl_compl:

                                segment = db_session.query(Segment).filter(
                                         (Segment.segmentcode == genstat.segmentcode) & ((Segment.betriebsnr == 1) | (Segment.betriebsnr == 2))).first()

                                if segment:
                                    do_it = False
                                else:

                                    if genstat.zipreis == 0 and genstat.gratis != 0 and genstat.resstatus == 6 and genstat.res_logic[1] :
                                        do_it = False

                            if do_it:

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
                for zimmer.kbezeich, zimmer.zikatnr, zimmer.zinr, zimmer._recid, zimkateg.kurzbez, zimkateg._recid in db_session.query(Zimmer.kbezeich, Zimmer.zikatnr, Zimmer.zinr, Zimmer._recid, Zimkateg.kurzbez, Zimkateg._recid).join(Zimkateg,(Zimkateg.zikatnr == Zimmer.zikatnr)).order_by(Zimkateg.zikatnr, Zimmer.zinr).all():
                    if zimmer_obj_list.get(zimmer._recid):
                        continue
                    else:
                        zimmer_obj_list[zimmer._recid] = True

                    if last_zikatnr == 0:
                        last_zikatnr = zimmer.zikatnr

                    if last_zikatnr != zimmer.zikatnr:
                        cl_list = Cl_list()
                        cl_list_data.append(cl_list)

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
                    cl_list_data.append(cl_list)

                    cl_list.zinr = zimmer.zinr
                    cl_list.rmcat = zimkateg.kurzbez
                    for datum in date_range(from_date,to_date) :

                        for genstat in db_session.query(Genstat).filter(
                                 (Genstat.zinr == zimmer.zinr) & (Genstat.datum == datum) & ((Genstat.resstatus == 6) | (Genstat.resstatus == 8))).order_by(Genstat._recid).all():
                            do_it = True

                            if excl_compl:

                                segment = db_session.query(Segment).filter(
                                         (Segment.segmentcode == genstat.segmentcode) & ((Segment.betriebsnr == 1) | (Segment.betriebsnr == 2))).first()

                                if segment:
                                    do_it = False
                                else:

                                    if genstat.zipreis == 0 and genstat.gratis != 0 and genstat.resstatus == 6 and genstat.res_logic[1] :
                                        do_it = False

                            if do_it:

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
                cl_list_data.append(cl_list)

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

        for cl_list in query(cl_list_data):

            if net != 0:
                cl_list.proz =  to_decimal(cl_list.net) / to_decimal(net) * to_decimal("100")

            if mnet != 0:
                cl_list.proz1 =  to_decimal(cl_list.mnet) / to_decimal(mnet) * to_decimal("100")

            if ynet != 0:
                cl_list.proz2 =  to_decimal(cl_list.ynet) / to_decimal(ynet) * to_decimal("100")
        cl_list = Cl_list()
        cl_list_data.append(cl_list)

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

        for cl_list in query(cl_list_data):
            output_list = Output_list()
            output_list_data.append(output_list)

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


    def create_resline2():

        nonlocal output_list_data, i, anz, manz, yanz, com_anz, com_manz, com_yanz, hu_anz, hu_manz, hu_yanz, pax, mpax, ypax, com_pax, com_mpax, com_ypax, hu_pax, hu_mpax, hu_ypax, mnet, ynet, net, t_anz, t_manz, t_yanz, t_pax, t_mpax, t_ypax, t_net, t_mnet, t_ynet, t_com_anz, t_com_pax, t_com_manz, t_com_mpax, t_com_yanz, t_com_ypax, t_hu_anz, t_hu_pax, t_hu_manz, t_hu_mpax, t_hu_yanz, t_hu_ypax, from_bez, to_bez, from_date, curr_zeit, ci_date, do_it, compli_flag, hu_flag, htparam, zimmer, reservation, arrangement, res_line, waehrung, segment, argt_line, artikel, zinrstat, genstat, zimkateg
        nonlocal m_ftd, m_ytd, f_date, t_date, to_date, rm_no, sorttype, lod__rev, excl_compl


        nonlocal output_list, cl_list, payload_list
        nonlocal output_list_data, cl_list_data

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
        anz = 0
        pax = 0
        net =  to_decimal("0")
        manz = 0
        mpax = 0
        mnet =  to_decimal("0")
        yanz = 0
        ypax = 0
        ynet =  to_decimal("0")
        com_anz = 0
        com_manz = 0
        com_yanz = 0
        hu_anz = 0
        hu_manz = 0
        hu_yanz = 0
        com_pax = 0
        com_mpax = 0
        com_ypax = 0
        hu_pax = 0
        hu_mpax = 0
        hu_ypax = 0
        t_anz = 0
        t_pax = 0
        t_manz = 0
        t_mpax = 0
        t_mnet =  to_decimal("0")
        t_yanz = 0
        t_ypax = 0
        t_ynet =  to_decimal("0")
        t_com_anz = 0
        t_com_pax = 0
        t_com_manz = 0
        t_com_mpax = 0
        t_com_yanz = 0
        t_com_ypax = 0
        t_hu_anz = 0
        t_hu_pax = 0
        t_hu_manz = 0
        t_hu_mpax = 0
        t_hu_yanz = 0
        t_hu_ypax = 0

        htparam = get_cache (Htparam, {"paramnr": [(eq, 491)]})
        price_decimal = htparam.finteger

        if rm_no != "":
            cl_list = Cl_list()
            cl_list_data.append(cl_list)

            cl_list.zinr = rm_no

            zimmer = get_cache (Zimmer, {"zinr": [(eq, rm_no)]})

            if zimmer:
                cl_list.rmcat = zimmer.kbezeich

            res_line_obj_list = {}
            res_line = Res_line()
            reservation = Reservation()
            arrangement = Arrangement()
            zimmer = Zimmer()
            for res_line.reserve_dec, res_line.betriebsnr, res_line.ankunft, res_line.abreise, res_line.zipreis, res_line._recid, res_line.zimmeranz, res_line.erwachs, res_line.gratis, res_line.kind1, res_line.kind2, res_line.zinr, res_line.zikatnr, reservation.segmentcode, reservation._recid, arrangement.argtnr, arrangement._recid, zimmer.kbezeich, zimmer.zikatnr, zimmer.zinr, zimmer._recid in db_session.query(Res_line.reserve_dec, Res_line.betriebsnr, Res_line.ankunft, Res_line.abreise, Res_line.zipreis, Res_line._recid, Res_line.zimmeranz, Res_line.erwachs, Res_line.gratis, Res_line.kind1, Res_line.kind2, Res_line.zinr, Res_line.zikatnr, Reservation.segmentcode, Reservation._recid, Arrangement.argtnr, Arrangement._recid, Zimmer.kbezeich, Zimmer.zikatnr, Zimmer.zinr, Zimmer._recid).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Arrangement,(Arrangement.arrangement == Res_line.arrangement)).join(Zimmer,(Zimmer.zinr == Res_line.zinr)).filter(
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
                do_it = True

                if do_it:
                    compli_flag = False
                    hu_flag = False

                    segment = db_session.query(Segment).filter(
                             (Segment.segmentcode == reservation.segmentcode) & ((Segment.betriebsnr == 1) | (Segment.betriebsnr == 2))).first()

                    if segment:

                        if segment.betriebsnr == 1:
                            compli_flag = True

                        elif segment.betriebsnr == 2:
                            hu_flag = True
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

                            if compli_flag:
                                cl_list.com_anz = cl_list.com_anz + res_line.zimmeranz
                                cl_list.com_pax = cl_list.com_pax + res_line.erwachs + res_line.gratis + res_line.kind1 + res_line.kind2
                                com_anz = com_anz + res_line.zimmeranz
                                com_pax = com_pax + res_line.erwachs + res_line.gratis + res_line.kind1 + res_line.kind2

                            elif hu_flag:
                                cl_list.hu_anz = cl_list.hu_anz + res_line.zimmeranz
                                cl_list.hu_pax = cl_list.hu_pax + res_line.erwachs + res_line.gratis + res_line.kind1 + res_line.kind2
                                hu_anz = hu_anz + res_line.zimmeranz
                                hu_pax = hu_pax + res_line.erwachs + res_line.gratis + res_line.kind1 + res_line.kind2
                            else:
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

                        if compli_flag:
                            cl_list.com_manz = cl_list.com_manz + res_line.zimmeranz
                            cl_list.com_mpax = cl_list.com_mpax + res_line.erwachs + res_line.gratis + res_line.kind1 + res_line.kind2
                            com_manz = com_manz + res_line.zimmeranz
                            com_mpax = com_mpax + res_line.erwachs + res_line.gratis + res_line.kind1 + res_line.kind2

                        elif hu_flag:
                            cl_list.hu_manz = cl_list.hu_manz + res_line.zimmeranz
                            cl_list.hu_mpax = cl_list.hu_mpax + res_line.erwachs + res_line.gratis + res_line.kind1 + res_line.kind2
                            hu_manz = hu_manz + res_line.zimmeranz
                            hu_mpax = hu_mpax + res_line.erwachs + res_line.gratis + res_line.kind1 + res_line.kind2
                        else:
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
                reservation = Reservation()
                arrangement = Arrangement()
                zimmer = Zimmer()
                for res_line.reserve_dec, res_line.betriebsnr, res_line.ankunft, res_line.abreise, res_line.zipreis, res_line._recid, res_line.zimmeranz, res_line.erwachs, res_line.gratis, res_line.kind1, res_line.kind2, res_line.zinr, res_line.zikatnr, reservation.segmentcode, reservation._recid, arrangement.argtnr, arrangement._recid, zimmer.kbezeich, zimmer.zikatnr, zimmer.zinr, zimmer._recid in db_session.query(Res_line.reserve_dec, Res_line.betriebsnr, Res_line.ankunft, Res_line.abreise, Res_line.zipreis, Res_line._recid, Res_line.zimmeranz, Res_line.erwachs, Res_line.gratis, Res_line.kind1, Res_line.kind2, Res_line.zinr, Res_line.zikatnr, Reservation.segmentcode, Reservation._recid, Arrangement.argtnr, Arrangement._recid, Zimmer.kbezeich, Zimmer.zikatnr, Zimmer.zinr, Zimmer._recid).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Arrangement,(Arrangement.arrangement == Res_line.arrangement)).join(Zimmer,(Zimmer.zinr == Res_line.zinr)).filter(
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

                    cl_list = query(cl_list_data, filters=(lambda cl_list: cl_list.zinr == res_line.zinr and cl_list.rmcat == zimmer.kbezeich), first=True)

                    if not cl_list:
                        cl_list = Cl_list()
                        cl_list_data.append(cl_list)

                        cl_list.zinr = res_line.zinr
                        cl_list.rmcat = zimmer.kbezeich
                    do_it = True

                    if do_it:
                        compli_flag = False
                        hu_flag = False

                        segment = db_session.query(Segment).filter(
                                 (Segment.segmentcode == reservation.segmentcode) & ((Segment.betriebsnr == 1) | (Segment.betriebsnr == 2))).first()

                        if segment:

                            if segment.betriebsnr == 1:
                                compli_flag = True

                            elif segment.betriebsnr == 2:
                                hu_flag = True
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

                                if compli_flag:
                                    cl_list.com_anz = cl_list.com_anz + res_line.zimmeranz
                                    cl_list.com_pax = cl_list.com_pax + res_line.erwachs + res_line.gratis + res_line.kind1 + res_line.kind2
                                    com_anz = com_anz + res_line.zimmeranz
                                    com_pax = com_pax + res_line.erwachs + res_line.gratis + res_line.kind1 + res_line.kind2

                                elif hu_flag:
                                    cl_list.hu_anz = cl_list.hu_anz + res_line.zimmeranz
                                    cl_list.hu_pax = cl_list.hu_pax + res_line.erwachs + res_line.gratis + res_line.kind1 + res_line.kind2
                                    hu_anz = hu_anz + res_line.zimmeranz
                                    hu_pax = hu_pax + res_line.erwachs + res_line.gratis + res_line.kind1 + res_line.kind2
                                else:
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

                            if compli_flag:
                                cl_list.com_manz = cl_list.com_manz + res_line.zimmeranz
                                cl_list.com_mpax = cl_list.com_mpax + res_line.erwachs + res_line.gratis + res_line.kind1 + res_line.kind2
                                com_manz = com_manz + res_line.zimmeranz
                                com_mpax = com_mpax + res_line.erwachs + res_line.gratis + res_line.kind1 + res_line.kind2

                            elif hu_flag:
                                cl_list.hu_manz = cl_list.hu_manz + res_line.zimmeranz
                                cl_list.hu_mpax = cl_list.hu_mpax + res_line.erwachs + res_line.gratis + res_line.kind1 + res_line.kind2
                                hu_manz = hu_manz + res_line.zimmeranz
                                hu_mpax = hu_mpax + res_line.erwachs + res_line.gratis + res_line.kind1 + res_line.kind2
                            else:
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
                reservation = Reservation()
                arrangement = Arrangement()
                zimmer = Zimmer()
                for res_line.reserve_dec, res_line.betriebsnr, res_line.ankunft, res_line.abreise, res_line.zipreis, res_line._recid, res_line.zimmeranz, res_line.erwachs, res_line.gratis, res_line.kind1, res_line.kind2, res_line.zinr, res_line.zikatnr, reservation.segmentcode, reservation._recid, arrangement.argtnr, arrangement._recid, zimmer.kbezeich, zimmer.zikatnr, zimmer.zinr, zimmer._recid in db_session.query(Res_line.reserve_dec, Res_line.betriebsnr, Res_line.ankunft, Res_line.abreise, Res_line.zipreis, Res_line._recid, Res_line.zimmeranz, Res_line.erwachs, Res_line.gratis, Res_line.kind1, Res_line.kind2, Res_line.zinr, Res_line.zikatnr, Reservation.segmentcode, Reservation._recid, Arrangement.argtnr, Arrangement._recid, Zimmer.kbezeich, Zimmer.zikatnr, Zimmer.zinr, Zimmer._recid).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Arrangement,(Arrangement.arrangement == Res_line.arrangement)).join(Zimmer,(Zimmer.zinr == Res_line.zinr)).filter(
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
                            cl_list_data.append(cl_list)

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
                            cl_list.com_anz = t_com_anz
                            cl_list.com_pax = t_com_pax
                            cl_list.hu_anz = t_hu_anz
                            cl_list.hu_pax = t_hu_pax
                            cl_list.com_manz = t_com_manz
                            cl_list.com_mpax = t_com_mpax
                            cl_list.hu_manz = t_hu_manz
                            cl_list.hu_mpax = t_hu_mpax
                            cl_list.com_yanz = t_com_manz
                            cl_list.com_ypax = t_com_mpax
                            cl_list.hu_yanz = t_hu_manz
                            cl_list.hu_ypax = t_hu_mpax
                            t_anz = 0
                            t_pax = 0
                            t_net =  to_decimal("0")
                            t_manz = 0
                            t_mnet =  to_decimal("0")
                            t_mpax = 0
                            t_yanz = 0
                            t_ynet =  to_decimal("0")
                            t_ypax = 0
                            t_com_anz = 0
                            t_com_pax = 0
                            t_com_manz = 0
                            t_com_mpax = 0
                            t_com_yanz = 0
                            t_com_ypax = 0
                            t_hu_anz = 0
                            t_hu_pax = 0
                            t_hu_manz = 0
                            t_hu_mpax = 0
                            t_hu_yanz = 0
                            t_hu_ypax = 0


                        cl_list = Cl_list()
                        cl_list_data.append(cl_list)

                        cl_list.zinr = res_line.zinr
                        cl_list.rmcat = zimmer.kbezeich
                        last_zikatnr = res_line.zikatnr
                        last_zinr = res_line.zinr
                    do_it = True

                    if do_it:
                        compli_flag = False
                        hu_flag = False

                        segment = db_session.query(Segment).filter(
                                 (Segment.segmentcode == reservation.segmentcode) & ((Segment.betriebsnr == 1) | (Segment.betriebsnr == 2))).first()

                        if segment:

                            if segment.betriebsnr == 1:
                                compli_flag = True

                            elif segment.betriebsnr == 2:
                                hu_flag = True
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

                                if compli_flag:
                                    cl_list.com_anz = cl_list.com_anz + res_line.zimmeranz
                                    cl_list.com_pax = cl_list.com_pax + res_line.erwachs + res_line.gratis + res_line.kind1 + res_line.kind2
                                    t_com_anz = t_com_anz + res_line.zimmeranz
                                    t_com_pax = t_com_pax + res_line.erwachs + res_line.gratis + res_line.kind1 + res_line.kind2
                                    com_anz = com_anz + res_line.zimmeranz
                                    com_pax = com_pax + res_line.erwachs + res_line.gratis + res_line.kind1 + res_line.kind2

                                elif hu_flag:
                                    cl_list.hu_anz = cl_list.hu_anz + res_line.zimmeranz
                                    cl_list.hu_pax = cl_list.hu_pax + res_line.erwachs + res_line.gratis + res_line.kind1 + res_line.kind2
                                    t_hu_anz = t_hu_anz + res_line.zimmeranz
                                    t_hu_pax = t_hu_pax + res_line.erwachs + res_line.gratis + res_line.kind1 + res_line.kind2
                                    hu_anz = hu_anz + res_line.zimmeranz
                                    hu_pax = hu_pax + res_line.erwachs + res_line.gratis + res_line.kind1 + res_line.kind2
                                else:
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

                            if compli_flag:
                                cl_list.com_manz = cl_list.com_manz + res_line.zimmeranz
                                cl_list.com_mpax = cl_list.com_mpax + res_line.erwachs + res_line.gratis + res_line.kind1 + res_line.kind2
                                t_com_manz = t_com_manz + res_line.zimmeranz
                                t_com_mpax = t_com_mpax + res_line.erwachs + res_line.gratis + res_line.kind1 + res_line.kind2
                                com_manz = com_manz + res_line.zimmeranz
                                com_mpax = com_mpax + res_line.erwachs + res_line.gratis + res_line.kind1 + res_line.kind2

                            elif hu_flag:
                                cl_list.hu_manz = cl_list.hu_manz + res_line.zimmeranz
                                cl_list.hu_mpax = cl_list.hu_mpax + res_line.erwachs + res_line.gratis + res_line.kind1 + res_line.kind2
                                t_hu_manz = t_hu_manz + res_line.zimmeranz
                                t_hu_mpax = t_hu_mpax + res_line.erwachs + res_line.gratis + res_line.kind1 + res_line.kind2
                                hu_manz = hu_manz + res_line.zimmeranz
                                hu_mpax = hu_mpax + res_line.erwachs + res_line.gratis + res_line.kind1 + res_line.kind2
                            else:
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
                cl_list_data.append(cl_list)

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
                cl_list.com_anz = t_com_anz
                cl_list.com_pax = t_com_pax
                cl_list.hu_anz = t_hu_anz
                cl_list.hu_pax = t_hu_pax
                cl_list.com_manz = t_com_manz
                cl_list.com_mpax = t_com_mpax
                cl_list.hu_manz = t_hu_manz
                cl_list.hu_mpax = t_hu_mpax
                cl_list.com_yanz = t_com_manz
                cl_list.com_ypax = t_com_mpax
                cl_list.hu_yanz = t_hu_manz
                cl_list.hu_ypax = t_hu_mpax
                t_anz = 0
                t_pax = 0
                t_net =  to_decimal("0")
                t_manz = 0
                t_mnet =  to_decimal("0")
                t_mpax = 0
                t_yanz = 0
                t_ynet =  to_decimal("0")
                t_ypax = 0
                t_com_anz = 0
                t_com_pax = 0
                t_com_manz = 0
                t_com_mpax = 0
                t_com_yanz = 0
                t_com_ypax = 0
                t_hu_anz = 0
                t_hu_pax = 0
                t_hu_manz = 0
                t_hu_mpax = 0
                t_hu_yanz = 0
                t_hu_ypax = 0

        for cl_list in query(cl_list_data):

            if net != 0:
                cl_list.proz =  to_decimal(cl_list.net) / to_decimal(net) * to_decimal("100")

            if mnet != 0:
                cl_list.proz1 =  to_decimal(cl_list.mnet) / to_decimal(mnet) * to_decimal("100")
        cl_list = Cl_list()
        cl_list_data.append(cl_list)

        cl_list.flag = "*"
        cl_list.zinr = ""
        cl_list = Cl_list()
        cl_list_data.append(cl_list)

        cl_list.zinr = ""
        cl_list.rmcat = "GTOTAL"
        cl_list.anz = anz
        cl_list.pax = pax
        cl_list.net =  to_decimal(net)
        cl_list.com_anz = com_anz
        cl_list.com_pax = com_pax
        cl_list.hu_anz = hu_anz
        cl_list.hu_pax = hu_pax

        if net != 0:
            cl_list.proz =  to_decimal("100")
        cl_list.manz = manz
        cl_list.mpax = mpax
        cl_list.mnet =  to_decimal(mnet)
        cl_list.com_manz = com_manz
        cl_list.com_mpax = com_mpax
        cl_list.hu_manz = hu_manz
        cl_list.hu_mpax = hu_mpax

        if mnet != 0:
            cl_list.proz1 =  to_decimal("100")
        cl_list.yanz = manz
        cl_list.ypax = mpax
        cl_list.ynet =  to_decimal(mnet)
        cl_list.com_manz = com_manz
        cl_list.com_mpax = com_mpax
        cl_list.hu_manz = hu_manz
        cl_list.hu_mpax = hu_mpax

        if mnet != 0:
            cl_list.proz2 =  to_decimal("100")

        for cl_list in query(cl_list_data):
            output_list = Output_list()
            output_list_data.append(output_list)

            output_list.flag = cl_list.flag
            output_list.rmno = cl_list.zinr
            output_list.rmno1 = to_string(cl_list.zinr)
            output_list.rmtype = to_string(cl_list.rmcat)
            output_list.rm = cl_list.anz
            output_list.pax = cl_list.pax
            output_list.com_rm = cl_list.com_anz
            output_list.com_pax = cl_list.com_pax
            output_list.hu_rm = cl_list.hu_anz
            output_list.hu_pax = cl_list.hu_pax
            output_list.rm_rev =  to_decimal(cl_list.net)
            output_list.percent =  to_decimal(cl_list.proz)
            output_list.mtdrm = cl_list.manz
            output_list.pax1 = cl_list.mpax
            output_list.com_mtdrm = cl_list.com_manz
            output_list.com_pax1 = cl_list.com_mpax
            output_list.hu_mtdrm = cl_list.hu_manz
            output_list.hu_pax1 = cl_list.hu_mpax
            output_list.rm_rev1 =  to_decimal(cl_list.mnet)
            output_list.percent1 =  to_decimal(cl_list.proz1)
            output_list.ftdrm = cl_list.manz
            output_list.pax2 = cl_list.mpax
            output_list.com_mtdrm = cl_list.com_manz
            output_list.com_pax1 = cl_list.com_mpax
            output_list.hu_mtdrm = cl_list.hu_manz
            output_list.hu_pax1 = cl_list.hu_mpax
            output_list.rm_rev2 =  to_decimal(cl_list.mnet)
            output_list.percent3 =  to_decimal(cl_list.proz1)


    def create_zinrstat2():

        nonlocal output_list_data, i, anz, manz, yanz, com_anz, com_manz, com_yanz, hu_anz, hu_manz, hu_yanz, pax, mpax, ypax, com_pax, com_mpax, com_ypax, hu_pax, hu_mpax, hu_ypax, mnet, ynet, net, t_anz, t_manz, t_yanz, t_pax, t_mpax, t_ypax, t_net, t_mnet, t_ynet, t_com_anz, t_com_pax, t_com_manz, t_com_mpax, t_com_yanz, t_com_ypax, t_hu_anz, t_hu_pax, t_hu_manz, t_hu_mpax, t_hu_yanz, t_hu_ypax, from_bez, to_bez, price_decimal, from_date, curr_zeit, ci_date, do_it, compli_flag, hu_flag, htparam, zimmer, reservation, arrangement, res_line, waehrung, segment, argt_line, artikel, zinrstat, genstat, zimkateg
        nonlocal m_ftd, m_ytd, f_date, t_date, to_date, rm_no, sorttype, lod__rev, excl_compl


        nonlocal output_list, cl_list, payload_list
        nonlocal output_list_data, cl_list_data

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
        com_anz = 0
        com_manz = 0
        com_yanz = 0
        hu_anz = 0
        hu_manz = 0
        hu_yanz = 0
        com_pax = 0
        com_mpax = 0
        com_ypax = 0
        hu_pax = 0
        hu_mpax = 0
        hu_ypax = 0
        t_anz = 0
        t_pax = 0
        t_manz = 0
        t_mpax = 0
        t_mnet =  to_decimal("0")
        t_yanz = 0
        t_ypax = 0
        t_ynet =  to_decimal("0")
        t_com_anz = 0
        t_com_pax = 0
        t_com_manz = 0
        t_com_mpax = 0
        t_com_yanz = 0
        t_com_ypax = 0
        t_hu_anz = 0
        t_hu_pax = 0
        t_hu_manz = 0
        t_hu_mpax = 0
        t_hu_yanz = 0
        t_hu_ypax = 0

        if m_ftd  and m_ytd == False:
            from_date = f_date
            to_date = t_date
            mm = get_month(to_date)
            yy = get_year(to_date)

        elif m_ftd == False and m_ytd :
            mm = get_month(to_date)
            yy = get_year(to_date)
            from_date = date_mdy(1, 1, yy)
        output_list_data.clear()
        cl_list_data.clear()

        if rm_no != "":

            zimmer = get_cache (Zimmer, {"zinr": [(eq, rm_no)]})

            if zimmer:
                cl_list = Cl_list()
                cl_list_data.append(cl_list)

                cl_list.zinr = rm_no
                cl_list.rmcat = zimmer.kbezeich
                for datum in date_range(from_date,to_date) :

                    zinrstat = get_cache (Zinrstat, {"zinr": [(eq, rm_no)],"datum": [(eq, datum)],"zimmeranz": [(gt, 0)]})

                    if zinrstat:
                        do_it = True

                        if do_it:
                            compli_flag = False
                            hu_flag = False

                            genstat = db_session.query(Genstat).filter(
                                     (Genstat.datum == datum) & (Genstat.zikatnr == zimmer.zikatnr) & (Genstat.zinr == zimmer.zinr) & (Genstat.zipreis == 0) & (Genstat.gratis != 0) & (Genstat.res_logic[inc_value(1)])).first()

                            if genstat:

                                segment = db_session.query(Segment).filter(
                                         (Segment.segmentcode == genstat.segmentcode) & ((Segment.betriebsnr == 1) | (Segment.betriebsnr == 2))).first()

                                if segment:

                                    if segment.betriebsnr == 1:
                                        compli_flag = True

                                    elif segment.betriebsnr == 2:
                                        hu_flag = True

                            if datum == to_date:

                                if compli_flag:
                                    cl_list.com_anz = cl_list.com_anz + zinrstat.zimmeranz
                                    cl_list.com_pax = cl_list.com_pax + zinrstat.person
                                    com_anz = com_anz + zinrstat.zimmeranz
                                    com_pax = com_pax + zinrstat.person

                                elif hu_flag:
                                    cl_list.hu_anz = cl_list.hu_anz + zinrstat.zimmeranz
                                    cl_list.hu_pax = cl_list.hu_pax + zinrstat.person
                                    hu_anz = hu_anz + zinrstat.zimmeranz
                                    hu_pax = hu_pax + zinrstat.person
                                else:
                                    cl_list.anz = cl_list.anz + zinrstat.zimmeranz
                                    cl_list.net =  to_decimal(cl_list.net) + to_decimal(zinrstat.argtumsatz)
                                    cl_list.pax = cl_list.pax + zinrstat.person
                                    anz = anz + zinrstat.zimmeranz
                                    pax = pax + zinrstat.person
                                    net =  to_decimal(net) + to_decimal(zinrstat.argtumsatz)

                            if get_month(zinrstat.datum) == mm and get_year(zinrstat.datum) == yy:

                                if compli_flag:
                                    cl_list.com_manz = cl_list.com_manz + zinrstat.zimmeranz
                                    cl_list.com_mpax = cl_list.com_mpax + zinrstat.person
                                    com_manz = com_manz + zinrstat.zimmeranz
                                    com_mpax = com_mpax + zinrstat.person

                                elif hu_flag:
                                    cl_list.hu_manz = cl_list.hu_manz + zinrstat.zimmeranz
                                    cl_list.hu_mpax = cl_list.hu_mpax + zinrstat.person
                                    hu_manz = hu_manz + zinrstat.zimmeranz
                                    hu_mpax = hu_mpax + zinrstat.person
                                else:
                                    cl_list.manz = cl_list.manz + zinrstat.zimmeranz
                                    cl_list.mnet =  to_decimal(cl_list.mnet) + to_decimal(zinrstat.argtumsatz)
                                    cl_list.mpax = cl_list.mpax + zinrstat.person
                                    manz = manz + zinrstat.zimmeranz
                                    mpax = mpax + zinrstat.person
                                    mnet =  to_decimal(mnet) + to_decimal(zinrstat.argtumsatz)

                            if compli_flag:
                                cl_list.com_yanz = cl_list.com_yanz + zinrstat.zimmeranz
                                cl_list.com_ypax = cl_list.com_ypax + zinrstat.person
                                com_yanz = com_yanz + zinrstat.zimmeranz
                                com_ypax = com_ypax + zinrstat.person

                            elif hu_flag:
                                cl_list.hu_yanz = cl_list.hu_yanz + zinrstat.zimmeranz
                                cl_list.hu_ypax = cl_list.hu_ypax + zinrstat.person
                                hu_yanz = hu_yanz + zinrstat.zimmeranz
                                hu_ypax = hu_ypax + zinrstat.person
                            else:
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
                for zimmer.kbezeich, zimmer.zikatnr, zimmer.zinr, zimmer._recid, zimkateg.kurzbez, zimkateg._recid in db_session.query(Zimmer.kbezeich, Zimmer.zikatnr, Zimmer.zinr, Zimmer._recid, Zimkateg.kurzbez, Zimkateg._recid).join(Zimkateg,(Zimkateg.zikatnr == Zimmer.zikatnr)).order_by(Zimmer.zinr).all():
                    if zimmer_obj_list.get(zimmer._recid):
                        continue
                    else:
                        zimmer_obj_list[zimmer._recid] = True


                    cl_list = Cl_list()
                    cl_list_data.append(cl_list)

                    cl_list.zinr = zimmer.zinr
                    cl_list.rmcat = zimkateg.kurzbez
                    for datum in date_range(from_date,to_date) :

                        zinrstat = get_cache (Zinrstat, {"zinr": [(eq, zimmer.zinr)],"datum": [(eq, datum)],"zimmeranz": [(gt, 0)]})

                        if zinrstat:
                            do_it = True

                            if do_it:
                                compli_flag = False
                                hu_flag = False

                                genstat = db_session.query(Genstat).filter(
                                         (Genstat.datum == datum) & (Genstat.zikatnr == zimmer.zikatnr) & (Genstat.zinr == zimmer.zinr) & (Genstat.zipreis == 0) & (Genstat.gratis != 0) & (Genstat.res_logic[inc_value(1)])).first()

                                if genstat:

                                    segment = db_session.query(Segment).filter(
                                             (Segment.segmentcode == genstat.segmentcode) & ((Segment.betriebsnr == 1) | (Segment.betriebsnr == 2))).first()

                                    if segment:

                                        if segment.betriebsnr == 1:
                                            compli_flag = True

                                        elif segment.betriebsnr == 2:
                                            hu_flag = True

                                if datum == to_date:

                                    if compli_flag:
                                        cl_list.com_anz = cl_list.com_anz + zinrstat.zimmeranz
                                        cl_list.com_pax = cl_list.com_pax + zinrstat.person
                                        com_anz = com_anz + zinrstat.zimmeranz
                                        com_pax = com_pax + zinrstat.person

                                    elif hu_flag:
                                        cl_list.hu_anz = cl_list.hu_anz + zinrstat.zimmeranz
                                        cl_list.hu_pax = cl_list.hu_pax + zinrstat.person
                                        hu_anz = hu_anz + zinrstat.zimmeranz
                                        hu_pax = hu_pax + zinrstat.person
                                    else:
                                        cl_list.anz = cl_list.anz + zinrstat.zimmeranz
                                        cl_list.net =  to_decimal(cl_list.net) + to_decimal(zinrstat.argtumsatz)
                                        cl_list.pax = cl_list.pax + zinrstat.person
                                        anz = anz + zinrstat.zimmeranz
                                        pax = pax + zinrstat.person
                                        net =  to_decimal(net) + to_decimal(zinrstat.argtumsatz)

                                if get_month(zinrstat.datum) == mm and get_year(zinrstat.datum) == yy:

                                    if compli_flag:
                                        cl_list.com_manz = cl_list.com_manz + zinrstat.zimmeranz
                                        cl_list.com_mpax = cl_list.com_mpax + zinrstat.person
                                        com_manz = com_manz + zinrstat.zimmeranz
                                        com_mpax = com_mpax + zinrstat.person

                                    elif hu_flag:
                                        cl_list.hu_manz = cl_list.hu_manz + zinrstat.zimmeranz
                                        cl_list.hu_mpax = cl_list.hu_mpax + zinrstat.person
                                        hu_manz = hu_manz + zinrstat.zimmeranz
                                        hu_mpax = hu_mpax + zinrstat.person
                                    else:
                                        cl_list.manz = cl_list.manz + zinrstat.zimmeranz
                                        cl_list.mnet =  to_decimal(cl_list.mnet) + to_decimal(zinrstat.argtumsatz)
                                        cl_list.mpax = cl_list.mpax + zinrstat.person
                                        manz = manz + zinrstat.zimmeranz
                                        mpax = mpax + zinrstat.person
                                        mnet =  to_decimal(mnet) + to_decimal(zinrstat.argtumsatz)

                                if compli_flag:
                                    cl_list.com_yanz = cl_list.com_yanz + zinrstat.zimmeranz
                                    cl_list.com_ypax = cl_list.com_ypax + zinrstat.person
                                    com_yanz = com_yanz + zinrstat.zimmeranz
                                    com_ypax = com_ypax + zinrstat.person

                                elif hu_flag:
                                    cl_list.hu_yanz = cl_list.hu_yanz + zinrstat.zimmeranz
                                    cl_list.hu_ypax = cl_list.hu_ypax + zinrstat.person
                                    hu_yanz = hu_yanz + zinrstat.zimmeranz
                                    hu_ypax = hu_ypax + zinrstat.person
                                else:
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
                for zimmer.kbezeich, zimmer.zikatnr, zimmer.zinr, zimmer._recid, zimkateg.kurzbez, zimkateg._recid in db_session.query(Zimmer.kbezeich, Zimmer.zikatnr, Zimmer.zinr, Zimmer._recid, Zimkateg.kurzbez, Zimkateg._recid).join(Zimkateg,(Zimkateg.zikatnr == Zimmer.zikatnr)).order_by(Zimkateg.zikatnr, Zimmer.zinr).all():
                    if zimmer_obj_list.get(zimmer._recid):
                        continue
                    else:
                        zimmer_obj_list[zimmer._recid] = True

                    if last_zikatnr == 0:
                        last_zikatnr = zimmer.zikatnr

                    if last_zikatnr != zimmer.zikatnr:
                        cl_list = Cl_list()
                        cl_list_data.append(cl_list)

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
                        cl_list.com_anz = t_com_anz
                        cl_list.com_pax = t_com_pax
                        cl_list.hu_anz = t_hu_anz
                        cl_list.hu_pax = t_hu_pax
                        cl_list.com_manz = t_com_manz
                        cl_list.com_mpax = t_com_mpax
                        cl_list.hu_manz = t_hu_manz
                        cl_list.hu_mpax = t_hu_mpax
                        cl_list.com_yanz = t_com_yanz
                        cl_list.com_ypax = t_com_ypax
                        cl_list.hu_yanz = t_hu_yanz
                        cl_list.hu_ypax = t_hu_ypax


                        t_anz = 0
                        t_pax = 0
                        t_net =  to_decimal("0")
                        t_manz = 0
                        t_mnet =  to_decimal("0")
                        t_mpax = 0
                        t_yanz = 0
                        t_ynet =  to_decimal("0")
                        t_ypax = 0
                        t_com_anz = 0
                        t_com_pax = 0
                        t_com_manz = 0
                        t_com_mpax = 0
                        t_com_yanz = 0
                        t_com_ypax = 0
                        t_hu_anz = 0
                        t_hu_pax = 0
                        t_hu_manz = 0
                        t_hu_mpax = 0
                        t_hu_yanz = 0
                        t_hu_ypax = 0
                        last_zikatnr = zimmer.zikatnr


                    cl_list = Cl_list()
                    cl_list_data.append(cl_list)

                    cl_list.zinr = zimmer.zinr
                    cl_list.rmcat = zimkateg.kurzbez
                    for datum in date_range(from_date,to_date) :

                        zinrstat = get_cache (Zinrstat, {"zinr": [(eq, zimmer.zinr)],"datum": [(eq, datum)],"zimmeranz": [(gt, 0)]})

                        if zinrstat:
                            do_it = True

                            if do_it:
                                compli_flag = False
                                hu_flag = False

                                genstat = db_session.query(Genstat).filter(
                                         (Genstat.datum == datum) & (Genstat.zikatnr == zimmer.zikatnr) & (Genstat.zinr == zimmer.zinr) & (Genstat.zipreis == 0) & (Genstat.gratis != 0) & (Genstat.res_logic[inc_value(1)])).first()

                                if genstat:

                                    segment = db_session.query(Segment).filter(
                                             (Segment.segmentcode == genstat.segmentcode) & ((Segment.betriebsnr == 1) | (Segment.betriebsnr == 2))).first()

                                    if segment:

                                        if segment.betriebsnr == 1:
                                            compli_flag = True

                                        elif segment.betriebsnr == 2:
                                            hu_flag = True

                                if datum == to_date:

                                    if compli_flag:
                                        cl_list.com_anz = cl_list.com_anz + zinrstat.zimmeranz
                                        cl_list.com_pax = cl_list.com_pax + zinrstat.person
                                        t_com_anz = t_com_anz + zinrstat.zimmeranz
                                        t_com_pax = t_com_pax + zinrstat.person
                                        com_anz = com_anz + zinrstat.zimmeranz
                                        com_pax = com_pax + zinrstat.person

                                    elif hu_flag:
                                        cl_list.hu_anz = cl_list.hu_anz + zinrstat.zimmeranz
                                        cl_list.hu_pax = cl_list.hu_pax + zinrstat.person
                                        t_hu_anz = t_hu_anz + zinrstat.zimmeranz
                                        t_hu_pax = t_hu_pax + zinrstat.person
                                        hu_anz = hu_anz + zinrstat.zimmeranz
                                        hu_pax = hu_pax + zinrstat.person
                                    else:
                                        cl_list.anz = cl_list.anz + zinrstat.zimmeranz
                                        cl_list.net =  to_decimal(cl_list.net) + to_decimal(zinrstat.argtumsatz)
                                        cl_list.pax = cl_list.pax + zinrstat.person
                                        anz = anz + zinrstat.zimmeranz
                                        pax = pax + zinrstat.person
                                        net =  to_decimal(net) + to_decimal(zinrstat.argtumsatz)
                                        t_anz = t_anz + zinrstat.zimmeranz
                                        t_pax = t_pax + zinrstat.person
                                        t_net =  to_decimal(t_net) + to_decimal(zinrstat.argtumsatz)

                                if get_month(zinrstat.datum) == mm and get_year(zinrstat.datum) == yy:

                                    if compli_flag:
                                        cl_list.com_manz = cl_list.com_manz + zinrstat.zimmeranz
                                        cl_list.com_mpax = cl_list.com_mpax + zinrstat.person
                                        t_com_manz = t_com_manz + zinrstat.zimmeranz
                                        t_com_mpax = t_com_mpax + zinrstat.person
                                        com_manz = com_manz + zinrstat.zimmeranz
                                        com_mpax = com_mpax + zinrstat.person

                                    elif hu_flag:
                                        cl_list.hu_manz = cl_list.hu_manz + zinrstat.zimmeranz
                                        cl_list.hu_mpax = cl_list.hu_mpax + zinrstat.person
                                        t_hu_manz = t_hu_manz + zinrstat.zimmeranz
                                        t_hu_mpax = t_hu_mpax + zinrstat.person
                                        hu_manz = hu_manz + zinrstat.zimmeranz
                                        hu_mpax = hu_mpax + zinrstat.person
                                    else:
                                        cl_list.manz = cl_list.manz + zinrstat.zimmeranz
                                        cl_list.mnet =  to_decimal(cl_list.mnet) + to_decimal(zinrstat.argtumsatz)
                                        cl_list.mpax = cl_list.mpax + zinrstat.person
                                        manz = manz + zinrstat.zimmeranz
                                        mpax = mpax + zinrstat.person
                                        mnet =  to_decimal(mnet) + to_decimal(zinrstat.argtumsatz)
                                        t_manz = t_manz + zinrstat.zimmeranz
                                        t_mpax = t_mpax + zinrstat.person
                                        t_mnet =  to_decimal(t_mnet) + to_decimal(zinrstat.argtumsatz)

                                if compli_flag:
                                    cl_list.com_yanz = cl_list.com_yanz + zinrstat.zimmeranz
                                    cl_list.com_ypax = cl_list.com_ypax + zinrstat.person
                                    t_com_yanz = t_com_yanz + zinrstat.zimmeranz
                                    t_com_ypax = t_com_ypax + zinrstat.person
                                    com_yanz = com_yanz + zinrstat.zimmeranz
                                    com_ypax = com_ypax + zinrstat.person

                                elif hu_flag:
                                    cl_list.hu_yanz = cl_list.hu_yanz + zinrstat.zimmeranz
                                    cl_list.hu_ypax = cl_list.hu_ypax + zinrstat.person
                                    t_hu_yanz = t_hu_yanz + zinrstat.zimmeranz
                                    t_hu_ypax = t_hu_ypax + zinrstat.person
                                    hu_yanz = hu_yanz + zinrstat.zimmeranz
                                    hu_ypax = hu_ypax + zinrstat.person
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
                cl_list_data.append(cl_list)

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
                cl_list.com_anz = t_com_anz
                cl_list.com_pax = t_com_pax
                cl_list.hu_anz = t_hu_anz
                cl_list.hu_pax = t_hu_pax
                cl_list.com_manz = t_com_manz
                cl_list.com_mpax = t_com_mpax
                cl_list.hu_manz = t_hu_manz
                cl_list.hu_mpax = t_hu_mpax
                cl_list.com_yanz = t_com_yanz
                cl_list.com_ypax = t_com_ypax
                cl_list.hu_yanz = t_hu_yanz
                cl_list.hu_ypax = t_hu_ypax


                t_anz = 0
                t_pax = 0
                t_net =  to_decimal("0")
                t_manz = 0
                t_mnet =  to_decimal("0")
                t_mpax = 0
                t_yanz = 0
                t_ynet =  to_decimal("0")
                t_ypax = 0
                t_com_anz = 0
                t_com_pax = 0
                t_com_manz = 0
                t_com_mpax = 0
                t_com_yanz = 0
                t_com_ypax = 0
                t_hu_anz = 0
                t_hu_pax = 0
                t_hu_manz = 0
                t_hu_mpax = 0
                t_hu_yanz = 0
                t_hu_ypax = 0

        for cl_list in query(cl_list_data):

            if net != 0:
                cl_list.proz =  to_decimal(cl_list.net) / to_decimal(net) * to_decimal("100")

            if mnet != 0:
                cl_list.proz1 =  to_decimal(cl_list.mnet) / to_decimal(mnet) * to_decimal("100")

            if ynet != 0:
                cl_list.proz2 =  to_decimal(cl_list.ynet) / to_decimal(ynet) * to_decimal("100")
        cl_list = Cl_list()
        cl_list_data.append(cl_list)

        cl_list.flag = "*"
        cl_list = Cl_list()
        cl_list_data.append(cl_list)

        cl_list.zinr = ""
        cl_list.rmcat = "GTOTAL"
        cl_list.anz = anz
        cl_list.pax = pax
        cl_list.net =  to_decimal(net)
        cl_list.com_anz = com_anz
        cl_list.com_pax = com_pax
        cl_list.hu_anz = hu_anz
        cl_list.hu_pax = hu_pax

        if net != 0:
            cl_list.proz =  to_decimal("100")
        cl_list.manz = manz
        cl_list.mpax = mpax
        cl_list.mnet =  to_decimal(mnet)
        cl_list.com_manz = com_manz
        cl_list.com_mpax = com_mpax
        cl_list.hu_manz = hu_manz
        cl_list.hu_mpax = hu_mpax

        if mnet != 0:
            cl_list.proz1 =  to_decimal("100")
        cl_list.yanz = yanz
        cl_list.ypax = ypax
        cl_list.ynet =  to_decimal(ynet)
        cl_list.com_yanz = com_yanz
        cl_list.com_ypax = com_ypax
        cl_list.hu_yanz = hu_yanz
        cl_list.hu_ypax = hu_ypax

        if ynet != 0:
            cl_list.proz2 =  to_decimal("100")

        for cl_list in query(cl_list_data):
            output_list = Output_list()
            output_list_data.append(output_list)

            output_list.flag = cl_list.flag
            output_list.rmno = cl_list.zinr

            if cl_list.flag.lower()  == ("*").lower() :
                pass
            else:
                output_list.rmno1 = to_string(cl_list.zinr)
                output_list.rmtype = to_string(cl_list.rmcat)
                output_list.rm = cl_list.anz
                output_list.pax = cl_list.pax
                output_list.com_rm = cl_list.com_anz
                output_list.com_pax = cl_list.com_pax
                output_list.hu_rm = cl_list.hu_anz
                output_list.hu_pax = cl_list.hu_pax
                output_list.rm_rev =  to_decimal(cl_list.net)
                output_list.percent =  to_decimal(cl_list.proz)
                output_list.mtdrm = cl_list.manz
                output_list.pax1 = cl_list.mpax
                output_list.com_mtdrm = cl_list.com_manz
                output_list.com_pax1 = cl_list.com_mpax
                output_list.hu_mtdrm = cl_list.hu_manz
                output_list.hu_pax1 = cl_list.hu_mpax
                output_list.rm_rev1 =  to_decimal(cl_list.mnet)
                output_list.percent1 =  to_decimal(cl_list.proz1)
                output_list.ftdrm = cl_list.yanz
                output_list.pax2 = cl_list.ypax
                output_list.com_ftdrm = cl_list.com_yanz
                output_list.com_pax2 = cl_list.com_ypax
                output_list.hu_ftdrm = cl_list.hu_yanz
                output_list.hu_pax2 = cl_list.hu_ypax
                output_list.rm_rev2 =  to_decimal(cl_list.ynet)
                output_list.percent3 =  to_decimal(cl_list.proz2)


    def create_genstat2():

        nonlocal output_list_data, i, anz, manz, yanz, com_anz, com_manz, com_yanz, hu_anz, hu_manz, hu_yanz, pax, mpax, ypax, com_pax, com_mpax, com_ypax, hu_pax, hu_mpax, hu_ypax, mnet, ynet, net, t_anz, t_manz, t_yanz, t_pax, t_mpax, t_ypax, t_net, t_mnet, t_ynet, t_com_anz, t_com_pax, t_com_manz, t_com_mpax, t_com_yanz, t_com_ypax, t_hu_anz, t_hu_pax, t_hu_manz, t_hu_mpax, t_hu_yanz, t_hu_ypax, from_bez, to_bez, price_decimal, from_date, curr_zeit, ci_date, do_it, compli_flag, hu_flag, htparam, zimmer, reservation, arrangement, res_line, waehrung, segment, argt_line, artikel, zinrstat, genstat, zimkateg
        nonlocal m_ftd, m_ytd, f_date, t_date, to_date, rm_no, sorttype, lod__rev, excl_compl


        nonlocal output_list, cl_list, payload_list
        nonlocal output_list_data, cl_list_data

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
        com_anz = 0
        com_manz = 0
        com_yanz = 0
        hu_anz = 0
        hu_manz = 0
        hu_yanz = 0
        com_pax = 0
        com_mpax = 0
        com_ypax = 0
        hu_pax = 0
        hu_mpax = 0
        hu_ypax = 0
        t_anz = 0
        t_pax = 0
        t_manz = 0
        t_mpax = 0
        t_mnet =  to_decimal("0")
        t_yanz = 0
        t_ypax = 0
        t_ynet =  to_decimal("0")
        t_com_anz = 0
        t_com_pax = 0
        t_com_manz = 0
        t_com_mpax = 0
        t_com_yanz = 0
        t_com_ypax = 0
        t_hu_anz = 0
        t_hu_pax = 0
        t_hu_manz = 0
        t_hu_mpax = 0
        t_hu_yanz = 0
        t_hu_ypax = 0

        if m_ftd :
            from_date = f_date
            to_date = t_date
            mm = get_month(to_date)
            yy = get_year(to_date)
        else:
            mm = get_month(to_date)
            yy = get_year(to_date)
            from_date = date_mdy(1, 1, yy)
        output_list_data.clear()
        output_list_data.clear()

        if rm_no != "":

            zimmer = get_cache (Zimmer, {"zinr": [(eq, rm_no)]})

            if zimmer:
                cl_list = Cl_list()
                cl_list_data.append(cl_list)

                cl_list.zinr = rm_no
                cl_list.rmcat = zimmer.kbezeich
                for datum in date_range(from_date,to_date) :

                    for genstat in db_session.query(Genstat).filter(
                             (Genstat.zinr == (rm_no).lower()) & (Genstat.datum == datum) & ((Genstat.resstatus == 6) | (Genstat.resstatus == 8))).order_by(Genstat._recid).all():
                        do_it = True

                        if do_it:
                            compli_flag = False
                            hu_flag = False

                            if genstat.zikatnr == zimmer.zikatnr and genstat.zipreis == 0 and genstat.gratis != 0:

                                segment = db_session.query(Segment).filter(
                                         (Segment.segmentcode == genstat.segmentcode) & ((Segment.betriebsnr == 1) | (Segment.betriebsnr == 2))).first()

                                if segment:

                                    if segment.betriebsnr == 1:
                                        compli_flag = True

                                    elif segment.betriebsnr == 2:
                                        hu_flag = True

                            if datum == to_date:

                                if compli_flag:
                                    cl_list.com_anz = cl_list.com_anz + 1
                                    cl_list.com_pax = cl_list.com_pax + genstat.erwachs + genstat.gratis + genstat.kind1 + genstat.kind2 + genstat.kind3
                                    com_anz = cl_list.com_anz + 1
                                    com_pax = cl_list.com_pax + genstat.erwachs + genstat.gratis + genstat.kind1 + genstat.kind2 + genstat.kind3

                                elif hu_flag:
                                    cl_list.hu_anz = cl_list.hu_anz + 1
                                    cl_list.hu_pax = cl_list.hu_pax + genstat.erwachs + genstat.gratis + genstat.kind1 + genstat.kind2 + genstat.kind3
                                    hu_anz = hu_anz + 1
                                    hu_pax = hu_pax + genstat.erwachs + genstat.gratis + genstat.kind1 + genstat.kind2 + genstat.kind3
                                else:
                                    cl_list.anz = cl_list.anz + 1
                                    cl_list.net =  to_decimal(cl_list.net) + to_decimal(genstat.logis)
                                    cl_list.pax = cl_list.pax + genstat.erwachs + genstat.gratis + genstat.kind1 + genstat.kind2 + genstat.kind3
                                    anz = anz + 1
                                    pax = pax + genstat.erwachs + genstat.gratis + genstat.kind1 + genstat.kind2 + genstat.kind3
                                    net =  to_decimal(net) + to_decimal(genstat.logis)

                            if get_month(genstat.datum) == mm and get_year(genstat.datum) == yy:

                                if compli_flag:
                                    cl_list.com_manz = cl_list.com_manz + 1
                                    cl_list.com_mpax = cl_list.com_mpax + genstat.erwachs + genstat.gratis + genstat.kind1 + genstat.kind2 + genstat.kind3
                                    com_manz = com_manz + 1
                                    com_mpax = com_mpax + genstat.erwachs + genstat.gratis + genstat.kind1 + genstat.kind2 + genstat.kind3

                                elif hu_flag:
                                    cl_list.hu_manz = cl_list.hu_manz + 1
                                    cl_list.hu_mpax = cl_list.hu_mpax + genstat.erwachs + genstat.gratis + genstat.kind1 + genstat.kind2 + genstat.kind3
                                    hu_manz = hu_manz + 1
                                    hu_mpax = hu_mpax + genstat.erwachs + genstat.gratis + genstat.kind1 + genstat.kind2 + genstat.kind3
                                else:
                                    cl_list.manz = cl_list.manz + 1
                                    cl_list.mnet =  to_decimal(cl_list.mnet) + to_decimal(genstat.logis)
                                    cl_list.mpax = cl_list.mpax + genstat.erwachs + genstat.gratis + genstat.kind1 + genstat.kind2 + genstat.kind3
                                    manz = manz + 1
                                    mpax = mpax + genstat.erwachs + genstat.gratis + genstat.kind1 + genstat.kind2 + genstat.kind3
                                    mnet =  to_decimal(mnet) + to_decimal(genstat.logis)

                            if compli_flag:
                                cl_list.com_yanz = cl_list.com_yanz + 1
                                cl_list.com_ypax = cl_list.com_ypax + genstat.erwachs + genstat.gratis + genstat.kind1 + genstat.kind2 + genstat.kind3
                                com_yanz = com_yanz + 1
                                com_ypax = com_ypax + genstat.erwachs + genstat.gratis + genstat.kind1 + genstat.kind2 + genstat.kind3

                            elif hu_flag:
                                cl_list.hu_yanz = cl_list.hu_yanz + 1
                                cl_list.hu_ypax = cl_list.hu_ypax + genstat.erwachs + genstat.gratis + genstat.kind1 + genstat.kind2 + genstat.kind3
                                hu_yanz = hu_yanz + 1
                                hu_ypax = hu_ypax + genstat.erwachs + genstat.gratis + genstat.kind1 + genstat.kind2 + genstat.kind3
                            else:
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
                for zimmer.kbezeich, zimmer.zikatnr, zimmer.zinr, zimmer._recid, zimkateg.kurzbez, zimkateg._recid in db_session.query(Zimmer.kbezeich, Zimmer.zikatnr, Zimmer.zinr, Zimmer._recid, Zimkateg.kurzbez, Zimkateg._recid).join(Zimkateg,(Zimkateg.zikatnr == Zimmer.zikatnr)).order_by(Zimmer.zinr).all():
                    if zimmer_obj_list.get(zimmer._recid):
                        continue
                    else:
                        zimmer_obj_list[zimmer._recid] = True


                    cl_list = Cl_list()
                    cl_list_data.append(cl_list)

                    cl_list.zinr = zimmer.zinr
                    cl_list.rmcat = zimkateg.kurzbez
                    for datum in date_range(from_date,to_date) :

                        for genstat in db_session.query(Genstat).filter(
                                 (Genstat.zinr == zimmer.zinr) & (Genstat.datum == datum) & ((Genstat.resstatus == 6) | (Genstat.resstatus == 8))).order_by(Genstat._recid).all():
                            do_it = True

                            if do_it:
                                compli_flag = False
                                hu_flag = False

                                if genstat.zikatnr == zimmer.zikatnr and genstat.zipreis == 0 and genstat.gratis != 0:

                                    segment = db_session.query(Segment).filter(
                                             (Segment.segmentcode == genstat.segmentcode) & ((Segment.betriebsnr == 1) | (Segment.betriebsnr == 2))).first()

                                    if segment:

                                        if segment.betriebsnr == 1:
                                            compli_flag = True

                                        elif segment.betriebsnr == 2:
                                            hu_flag = True

                                if datum == to_date:

                                    if compli_flag:
                                        cl_list.com_anz = cl_list.com_anz + 1
                                        cl_list.com_pax = cl_list.com_pax + genstat.erwachs + genstat.gratis + genstat.kind1 + genstat.kind2 + genstat.kind3
                                        com_anz = cl_list.com_anz + 1
                                        com_pax = cl_list.com_pax + genstat.erwachs + genstat.gratis + genstat.kind1 + genstat.kind2 + genstat.kind3

                                    elif hu_flag:
                                        cl_list.hu_anz = cl_list.hu_anz + 1
                                        cl_list.hu_pax = cl_list.hu_pax + genstat.erwachs + genstat.gratis + genstat.kind1 + genstat.kind2 + genstat.kind3
                                        hu_anz = hu_anz + 1
                                        hu_pax = hu_pax + genstat.erwachs + genstat.gratis + genstat.kind1 + genstat.kind2 + genstat.kind3
                                    else:
                                        cl_list.anz = cl_list.anz + 1
                                        cl_list.net =  to_decimal(cl_list.net) + to_decimal(genstat.logis)
                                        cl_list.pax = cl_list.pax + genstat.erwachs + genstat.gratis +\
                                                genstat.kind1 + genstat.kind2 + genstat.kind3
                                        anz = anz + 1
                                        pax = pax + genstat.erwachs + genstat.gratis +\
                                                genstat.kind1 + genstat.kind2 + genstat.kind3


                                        net =  to_decimal(net) + to_decimal(genstat.logis)

                                if get_month(genstat.datum) == mm and get_year(genstat.datum) == yy:

                                    if compli_flag:
                                        cl_list.com_manz = cl_list.com_manz + 1
                                        cl_list.com_mpax = cl_list.com_mpax + genstat.erwachs + genstat.gratis + genstat.kind1 + genstat.kind2 + genstat.kind3
                                        com_manz = com_manz + 1
                                        com_mpax = com_mpax + genstat.erwachs + genstat.gratis + genstat.kind1 + genstat.kind2 + genstat.kind3

                                    elif hu_flag:
                                        cl_list.hu_manz = cl_list.hu_manz + 1
                                        cl_list.hu_mpax = cl_list.hu_mpax + genstat.erwachs + genstat.gratis + genstat.kind1 + genstat.kind2 + genstat.kind3
                                        hu_manz = hu_manz + 1
                                        hu_mpax = hu_mpax + genstat.erwachs + genstat.gratis + genstat.kind1 + genstat.kind2 + genstat.kind3
                                    else:
                                        cl_list.manz = cl_list.manz + 1
                                        cl_list.mnet =  to_decimal(cl_list.mnet) + to_decimal(genstat.logis)
                                        cl_list.mpax = cl_list.mpax + genstat.erwachs + genstat.gratis +\
                                                genstat.kind1 + genstat.kind2 + genstat.kind3
                                        manz = manz + 1
                                        mpax = mpax + genstat.erwachs + genstat.gratis +\
                                                genstat.kind1 + genstat.kind2 + genstat.kind3
                                        mnet =  to_decimal(mnet) + to_decimal(genstat.logis)

                                if compli_flag:
                                    cl_list.com_yanz = cl_list.com_yanz + 1
                                    cl_list.com_ypax = cl_list.com_ypax + genstat.erwachs + genstat.gratis + genstat.kind1 + genstat.kind2 + genstat.kind3
                                    com_yanz = com_yanz + 1
                                    com_ypax = com_ypax + genstat.erwachs + genstat.gratis + genstat.kind1 + genstat.kind2 + genstat.kind3

                                elif hu_flag:
                                    cl_list.hu_yanz = cl_list.hu_yanz + 1
                                    cl_list.hu_ypax = cl_list.hu_ypax + genstat.erwachs + genstat.gratis + genstat.kind1 + genstat.kind2 + genstat.kind3
                                    hu_yanz = hu_yanz + 1
                                    hu_ypax = hu_ypax + genstat.erwachs + genstat.gratis + genstat.kind1 + genstat.kind2 + genstat.kind3
                                else:
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
                for zimmer.kbezeich, zimmer.zikatnr, zimmer.zinr, zimmer._recid, zimkateg.kurzbez, zimkateg._recid in db_session.query(Zimmer.kbezeich, Zimmer.zikatnr, Zimmer.zinr, Zimmer._recid, Zimkateg.kurzbez, Zimkateg._recid).join(Zimkateg,(Zimkateg.zikatnr == Zimmer.zikatnr)).order_by(Zimkateg.zikatnr, Zimmer.zinr).all():
                    if zimmer_obj_list.get(zimmer._recid):
                        continue
                    else:
                        zimmer_obj_list[zimmer._recid] = True

                    if last_zikatnr == 0:
                        last_zikatnr = zimmer.zikatnr

                    if last_zikatnr != zimmer.zikatnr:
                        cl_list = Cl_list()
                        cl_list_data.append(cl_list)

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
                        cl_list.com_anz = t_com_anz
                        cl_list.com_pax = t_com_pax
                        cl_list.hu_anz = t_hu_anz
                        cl_list.hu_pax = t_hu_pax
                        cl_list.com_manz = t_com_manz
                        cl_list.com_mpax = t_com_mpax
                        cl_list.hu_manz = t_hu_manz
                        cl_list.hu_mpax = t_hu_mpax
                        cl_list.com_yanz = t_com_yanz
                        cl_list.com_ypax = t_com_ypax
                        cl_list.hu_yanz = t_hu_yanz
                        cl_list.hu_ypax = t_hu_ypax
                        t_anz = 0
                        t_pax = 0
                        t_net =  to_decimal("0")
                        t_manz = 0
                        t_mnet =  to_decimal("0")
                        t_mpax = 0
                        t_yanz = 0
                        t_ynet =  to_decimal("0")
                        t_ypax = 0
                        t_com_anz = 0
                        t_com_pax = 0
                        t_com_manz = 0
                        t_com_mpax = 0
                        t_com_yanz = 0
                        t_com_ypax = 0
                        t_hu_anz = 0
                        t_hu_pax = 0
                        t_hu_manz = 0
                        t_hu_mpax = 0
                        t_hu_yanz = 0
                        t_hu_ypax = 0
                        last_zikatnr = zimmer.zikatnr


                    cl_list = Cl_list()
                    cl_list_data.append(cl_list)

                    cl_list.zinr = zimmer.zinr
                    cl_list.rmcat = zimkateg.kurzbez
                    for datum in date_range(from_date,to_date) :

                        for genstat in db_session.query(Genstat).filter(
                                 (Genstat.zinr == zimmer.zinr) & (Genstat.datum == datum) & ((Genstat.resstatus == 6) | (Genstat.resstatus == 8))).order_by(Genstat._recid).all():
                            do_it = True

                            if do_it:
                                compli_flag = False
                                hu_flag = False

                                if genstat.zikatnr == zimmer.zikatnr and genstat.zipreis == 0 and genstat.gratis != 0:

                                    segment = db_session.query(Segment).filter(
                                             (Segment.segmentcode == genstat.segmentcode) & ((Segment.betriebsnr == 1) | (Segment.betriebsnr == 2))).first()

                                    if segment:

                                        if segment.betriebsnr == 1:
                                            compli_flag = True

                                        elif segment.betriebsnr == 2:
                                            hu_flag = True

                                if datum == to_date:

                                    if compli_flag:
                                        cl_list.com_anz = cl_list.com_anz + 1
                                        cl_list.com_pax = cl_list.com_pax + genstat.erwachs + genstat.gratis + genstat.kind1 + genstat.kind2 + genstat.kind3
                                        t_com_anz = t_com_anz + 1
                                        t_com_pax = t_com_pax + genstat.erwachs + genstat.gratis + genstat.kind1 + genstat.kind2 + genstat.kind3
                                        com_anz = com_anz + 1
                                        com_pax = com_pax + genstat.erwachs + genstat.gratis + genstat.kind1 + genstat.kind2 + genstat.kind3

                                    elif hu_flag:
                                        cl_list.hu_anz = cl_list.hu_anz + 1
                                        cl_list.hu_pax = cl_list.hu_pax + genstat.erwachs + genstat.gratis + genstat.kind1 + genstat.kind2 + genstat.kind3
                                        t_hu_anz = t_hu_anz + 1
                                        t_hu_pax = t_hu_pax + genstat.erwachs + genstat.gratis + genstat.kind1 + genstat.kind2 + genstat.kind3
                                        hu_anz = hu_anz + 1
                                        hu_pax = hu_pax + genstat.erwachs + genstat.gratis + genstat.kind1 + genstat.kind2 + genstat.kind3
                                    else:
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

                                if get_month(genstat.datum) == mm and get_year(genstat.datum) == yy:

                                    if compli_flag:
                                        cl_list.com_manz = cl_list.com_manz + 1
                                        cl_list.com_mpax = cl_list.com_mpax + genstat.erwachs + genstat.gratis + genstat.kind1 + genstat.kind2 + genstat.kind3
                                        t_com_manz = t_com_manz + 1
                                        t_com_mpax = t_com_mpax + genstat.erwachs + genstat.gratis + genstat.kind1 + genstat.kind2 + genstat.kind3
                                        com_manz = com_manz + 1
                                        com_mpax = com_mpax + genstat.erwachs + genstat.gratis + genstat.kind1 + genstat.kind2 + genstat.kind3

                                    elif hu_flag:
                                        cl_list.hu_manz = cl_list.hu_manz + 1
                                        cl_list.hu_mpax = cl_list.hu_mpax + genstat.erwachs + genstat.gratis + genstat.kind1 + genstat.kind2 + genstat.kind3
                                        t_hu_manz = t_hu_manz + 1
                                        t_hu_mpax = t_hu_mpax + genstat.erwachs + genstat.gratis + genstat.kind1 + genstat.kind2 + genstat.kind3
                                        hu_manz = hu_manz + 1
                                        hu_mpax = hu_mpax + genstat.erwachs + genstat.gratis + genstat.kind1 + genstat.kind2 + genstat.kind3
                                    else:
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

                                if compli_flag:
                                    cl_list.com_yanz = cl_list.com_yanz + 1
                                    cl_list.com_ypax = cl_list.com_ypax + genstat.erwachs + genstat.gratis + genstat.kind1 + genstat.kind2 + genstat.kind3
                                    t_com_yanz = t_com_yanz + 1
                                    t_com_ypax = t_com_ypax + genstat.erwachs + genstat.gratis + genstat.kind1 + genstat.kind2 + genstat.kind3
                                    com_yanz = com_yanz + 1
                                    com_ypax = com_ypax + genstat.erwachs + genstat.gratis + genstat.kind1 + genstat.kind2 + genstat.kind3

                                elif hu_flag:
                                    cl_list.hu_yanz = cl_list.hu_yanz + 1
                                    cl_list.hu_ypax = cl_list.hu_ypax + genstat.erwachs + genstat.gratis + genstat.kind1 + genstat.kind2 + genstat.kind3
                                    t_hu_yanz = t_hu_yanz + 1
                                    t_hu_ypax = t_hu_ypax + genstat.erwachs + genstat.gratis + genstat.kind1 + genstat.kind2 + genstat.kind3
                                    hu_yanz = hu_yanz + 1
                                    hu_ypax = hu_ypax + genstat.erwachs + genstat.gratis + genstat.kind1 + genstat.kind2 + genstat.kind3
                                else:
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
                cl_list_data.append(cl_list)

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
                cl_list.com_anz = t_com_anz
                cl_list.com_pax = t_com_pax
                cl_list.hu_anz = t_hu_anz
                cl_list.hu_pax = t_hu_pax
                cl_list.com_manz = t_com_manz
                cl_list.com_mpax = t_com_mpax
                cl_list.hu_manz = t_hu_manz
                cl_list.hu_mpax = t_hu_mpax
                cl_list.com_yanz = t_com_yanz
                cl_list.com_ypax = t_com_ypax
                cl_list.hu_yanz = t_hu_yanz
                cl_list.hu_ypax = t_hu_ypax


                t_anz = 0
                t_pax = 0
                t_net =  to_decimal("0")
                t_manz = 0
                t_mnet =  to_decimal("0")
                t_mpax = 0
                t_yanz = 0
                t_ynet =  to_decimal("0")
                t_ypax = 0
                t_com_anz = 0
                t_com_pax = 0
                t_com_manz = 0
                t_com_mpax = 0
                t_com_yanz = 0
                t_com_ypax = 0
                t_hu_anz = 0
                t_hu_pax = 0
                t_hu_manz = 0
                t_hu_mpax = 0
                t_hu_yanz = 0
                t_hu_ypax = 0

        for cl_list in query(cl_list_data):

            if net != 0:
                cl_list.proz =  to_decimal(cl_list.net) / to_decimal(net) * to_decimal("100")

            if mnet != 0:
                cl_list.proz1 =  to_decimal(cl_list.mnet) / to_decimal(mnet) * to_decimal("100")

            if ynet != 0:
                cl_list.proz2 =  to_decimal(cl_list.ynet) / to_decimal(ynet) * to_decimal("100")
        cl_list = Cl_list()
        cl_list_data.append(cl_list)

        cl_list.zinr = ""
        cl_list.rmcat = "GTOTAL"
        cl_list.anz = anz
        cl_list.pax = pax
        cl_list.net =  to_decimal(net)
        cl_list.com_anz = com_anz
        cl_list.com_pax = com_pax
        cl_list.hu_anz = hu_anz
        cl_list.hu_pax = hu_pax

        if net != 0:
            cl_list.proz =  to_decimal("100")
        cl_list.manz = manz
        cl_list.mpax = mpax
        cl_list.mnet =  to_decimal(mnet)
        cl_list.com_manz = com_manz
        cl_list.com_mpax = com_mpax
        cl_list.hu_manz = hu_manz
        cl_list.hu_mpax = hu_mpax

        if mnet != 0:
            cl_list.proz1 =  to_decimal("100")
        cl_list.yanz = yanz
        cl_list.ypax = ypax
        cl_list.ynet =  to_decimal(ynet)
        cl_list.com_yanz = com_yanz
        cl_list.com_ypax = com_ypax
        cl_list.hu_yanz = hu_yanz
        cl_list.hu_ypax = hu_ypax

        if ynet != 0:
            cl_list.proz2 =  to_decimal("100")

        for cl_list in query(cl_list_data):
            output_list = Output_list()
            output_list_data.append(output_list)

            output_list.rmno1 = to_string(cl_list.zinr)
            output_list.rmtype = to_string(cl_list.rmcat)
            output_list.rm = cl_list.anz
            output_list.pax = cl_list.pax
            output_list.com_rm = cl_list.com_anz
            output_list.com_pax = cl_list.com_pax
            output_list.hu_rm = cl_list.hu_anz
            output_list.hu_pax = cl_list.hu_pax
            output_list.rm_rev =  to_decimal(cl_list.net)
            output_list.percent =  to_decimal(cl_list.proz)
            output_list.mtdrm = cl_list.manz
            output_list.pax1 = cl_list.mpax
            output_list.com_mtdrm = cl_list.com_manz
            output_list.com_pax1 = cl_list.com_mpax
            output_list.hu_mtdrm = cl_list.hu_manz
            output_list.hu_pax1 = cl_list.hu_mpax
            output_list.rm_rev1 =  to_decimal(cl_list.mnet)
            output_list.percent1 =  to_decimal(cl_list.proz1)
            output_list.ftdrm = cl_list.yanz
            output_list.pax2 = cl_list.ypax
            output_list.com_ftdrm = cl_list.com_yanz
            output_list.com_pax2 = cl_list.com_ypax
            output_list.hu_ftdrm = cl_list.hu_yanz
            output_list.hu_pax2 = cl_list.hu_ypax
            output_list.rm_rev2 =  to_decimal(cl_list.ynet)
            output_list.percent3 =  to_decimal(cl_list.proz2)

    ci_date = get_output(htpdate(87))

    payload_list = query(payload_list_data, first=True)

    if payload_list:

        if payload_list.show_breakdown_comphu == None:
            payload_list.show_breakdown_comphu = False

        if excl_compl:
            payload_list.show_breakdown_comphu = False

        if payload_list.show_breakdown_comphu:
            excl_compl = False

    if (not excl_compl and not payload_list.show_breakdown_comphu) or excl_compl and not payload_list.show_breakdown_comphu:

        if m_ftd and f_date >= ci_date and t_date >= ci_date:
            create_resline()
        else:

            if lod__rev :
                create_genstat()
            else:
                create_zinrstat()

    elif not excl_compl and payload_list.show_breakdown_comphu:

        if m_ftd and f_date >= ci_date and t_date >= ci_date:
            create_resline2()
        else:

            if lod__rev :
                create_genstat2()
            else:
                create_zinrstat2()

    return generate_output()