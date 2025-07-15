from functions.additional_functions import *
import decimal
from datetime import date
from sqlalchemy import func
from functions.calc_servtaxesbl import calc_servtaxesbl
from functions.argt_betrag import argt_betrag
from functions.ratecode_compli import ratecode_compli
from models import Paramtext, Htparam, Waehrung, Nightaudit, Nitestor, Res_line, Artikel, Zimmer, Zimkateg, Bill_line, Arrangement, Bill, Guest, Reservation, Nation, Segmentstat, Zinrstat, Argt_line, Reslin_queasy, Guest_pr

def nt_pjrmrecap():
    bill_date:date = None
    tot_rev:decimal = to_decimal("0.0")
    domestic:str = ""
    tot_inactive:int = 0
    walk_in:int = 0
    anz_win:int = 0
    anz_rsv:int = 0
    anz_nos:int = 0
    anz_can:int = 0
    anz_dom:int = 0
    anz_for:int = 0
    anz_comadult:int = 0
    anz_comchild:int = 0
    anz_rmci:int = 0
    anz_rmco:int = 0
    anz_adci:int = 0
    anz_adco:int = 0
    anz_chci:int = 0
    anz_chco:int = 0
    anz_cmci:int = 0
    anz_cmco:int = 0
    anz_cmchci:int = 0
    anz_cmchco:int = 0
    lodg_betrag:decimal = to_decimal("0.0")
    rate:decimal = to_decimal("0.0")
    frate:decimal = 1
    exchg_rate:decimal = 1
    service:decimal = to_decimal("0.0")
    vat:decimal = to_decimal("0.0")
    vat2:decimal = to_decimal("0.0")
    fact:decimal = to_decimal("0.0")
    argt_betrag:decimal = to_decimal("0.0")
    ex_rate:decimal = to_decimal("0.0")
    grate:decimal = to_decimal("0.0")
    tot_lodging:decimal = to_decimal("0.0")
    price_decimal:int = 0
    foreign_rate:bool = False
    rm_serv:bool = False
    new_contrate:bool = False
    progname:str = "nt-PJrmrecap.p"
    night_type:int = 0
    reihenfolge:int = 0
    line_nr:int = 0
    line:str = ""
    p_width:int = 83
    p_length:int = 59
    htl_name:str = ""
    htl_adr:str = ""
    htl_tel:str = ""
    long_digit:bool = False
    paramtext = htparam = waehrung = nightaudit = nitestor = res_line = artikel = zimmer = zimkateg = bill_line = arrangement = bill = guest = reservation = nation = segmentstat = zinrstat = argt_line = reslin_queasy = guest_pr = None

    occ_list = zk_list = nat_list = argt_list = segm_list = None

    occ_list_list, Occ_list = create_model("Occ_list", {"nr":int, "rm":int})
    zk_list_list, Zk_list = create_model("Zk_list", {"zikatnr":int, "bezeich":str, "anz100":int, "inactive":int, "zimmeranz":int, "anz_pax":int, "anz_child1":int, "anz_child2":int, "dayuse":int, "du_pax":int, "du_child1":int, "du_child2":int, "vacant":int, "ooo":int, "co_rm":int, "cb_rm":int, "co_pax":int, "cb_pax":int})
    nat_list_list, Nat_list = create_model("Nat_list", {"bezeich":str, "nat":str, "adult":int, "proz":decimal, "child":int})
    argt_list_list, Argt_list = create_model("Argt_list", {"bezeich":str, "anz_rm":int, "adult":int})
    segm_list_list, Segm_list = create_model("Segm_list", {"nr":int, "bezeich":str, "anz_rm":int, "adult":int})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal bill_date, tot_rev, domestic, tot_inactive, walk_in, anz_win, anz_rsv, anz_nos, anz_can, anz_dom, anz_for, anz_comadult, anz_comchild, anz_rmci, anz_rmco, anz_adci, anz_adco, anz_chci, anz_chco, anz_cmci, anz_cmco, anz_cmchci, anz_cmchco, lodg_betrag, rate, frate, exchg_rate, service, vat, vat2, fact, argt_betrag, ex_rate, grate, tot_lodging, price_decimal, foreign_rate, rm_serv, new_contrate, progname, night_type, reihenfolge, line_nr, line, p_width, p_length, htl_name, htl_adr, htl_tel, long_digit, paramtext, htparam, waehrung, nightaudit, nitestor, res_line, artikel, zimmer, zimkateg, bill_line, arrangement, bill, guest, reservation, nation, segmentstat, zinrstat, argt_line, reslin_queasy, guest_pr


        nonlocal occ_list, zk_list, nat_list, argt_list, segm_list
        nonlocal occ_list_list, zk_list_list, nat_list_list, argt_list_list, segm_list_list

        return {}

    def create_zkstat():

        nonlocal bill_date, tot_rev, domestic, tot_inactive, walk_in, anz_win, anz_rsv, anz_nos, anz_can, anz_dom, anz_for, anz_comadult, anz_comchild, anz_rmci, anz_rmco, anz_adci, anz_adco, anz_chci, anz_chco, anz_cmci, anz_cmco, anz_cmchci, anz_cmchco, lodg_betrag, rate, exchg_rate, service, vat, vat2, fact, argt_betrag, ex_rate, grate, tot_lodging, price_decimal, foreign_rate, rm_serv, new_contrate, progname, night_type, reihenfolge, line_nr, line, p_width, p_length, htl_name, htl_adr, htl_tel, long_digit, paramtext, htparam, waehrung, nightaudit, nitestor, res_line, artikel, zimmer, zimkateg, bill_line, arrangement, bill, guest, reservation, nation, segmentstat, zinrstat, argt_line, reslin_queasy, guest_pr


        nonlocal occ_list, zk_list, nat_list, argt_list, segm_list
        nonlocal occ_list_list, zk_list_list, nat_list_list, argt_list_list, segm_list_list

        dayuse:bool = False
        do_it:bool = False
        co_flag:bool = False
        cb_flag:bool = False
        extra_bed:decimal = to_decimal("0.0")
        frate:decimal = to_decimal("0.0")
        eb_artnr:int = 0
        rline = None
        paxnum:int = 0
        rbuff = None
        Rline =  create_buffer("Rline",Res_line)
        occ_list_list.clear()
        occ_list = Occ_list()
        occ_list_list.append(occ_list)

        occ_list.nr = 1
        occ_list = Occ_list()
        occ_list_list.append(occ_list)

        occ_list.nr = 2
        occ_list = Occ_list()
        occ_list_list.append(occ_list)

        occ_list.nr = 3

        artikel = db_session.query(Artikel).filter(
                 (Artikel.departement == 0) & (func.lower(Artikel.bezeich) == ("Extra Bed").lower())).first()

        if artikel:
            eb_artnr = artikel.artnr

        for zimmer in db_session.query(Zimmer).order_by(Zimmer.zikatnr).all():

            zk_list = query(zk_list_list, filters=(lambda zk_list: zk_list.zikatnr == zimmer.zikatnr), first=True)

            if not zk_list:

                zimkateg = db_session.query(Zimkateg).filter(
                         (Zimkateg.zikatnr == zimmer.zikatnr)).first()
                zk_list = Zk_list()
                zk_list_list.append(zk_list)

                zk_list.zikatnr = zimmer.zikatnr
                zk_list.bezeich = zimkateg.bezeichnung

            if zimmer.sleeping:
                zk_list.anz100 = zk_list.anz100 + 1
            else:
                zk_list.inactive = zk_list.inactive + 1

            if zimmer.zistatus == 6 and zimmer.sleeping:
                zk_list.ooo = zk_list.ooo + 1

        for bill_line in db_session.query(Bill_line).filter(
                 (Bill_line.rechnr > 0) & (Bill_line.bill_datum == bill_date) & (Bill_line.zeit >= 0) & (Bill_line.departement == 0)).order_by(Bill_line.rechnr).all():

            artikel = db_session.query(Artikel).filter(
                     (Artikel.artnr == bill_line.artnr) & (Artikel.departement == bill_line.departement)).first()

            if artikel.umsatzart == 1 or artikel.artart == 9:
                do_it = True

                if artikel.artart == 9:

                    arrangement = db_session.query(Arrangement).filter(
                             (Arrangement.argt_artikelnr == artikel.artnr) & (Arrangement.arrangement != "")).first()
                    do_it = None != arrangement

                if do_it:
                    tot_rev =  to_decimal(tot_rev) + to_decimal(bill_line.betrag)

        res_line_obj_list = []
        for res_line, zimmer in db_session.query(Res_line, Zimmer).join(Zimmer,(Zimmer.zinr == Res_line.zinr) & (Zimmer.sleeping)).filter(
                 ((Res_line.active_flag == 1) & (Res_line.resstatus != 12)) | ((Res_line.active_flag == 2) & (Res_line.resstatus == 8) & (Res_line.ankunft <= bill_date) & (Res_line.abreise == bill_date)) & (Res_line.l_zuordnung[inc_value(2)] == 0)).order_by(Res_line.resnr).all():
            if res_line._recid in res_line_obj_list:
                continue
            else:
                res_line_obj_list.append(res_line._recid)


            dayuse = False
            do_it = False
            co_flag = False
            cb_flag = False

            if res_line.active_flag == 2 and (res_line.ankunft == res_line.abreise):

                bill = db_session.query(Bill).filter(
                         (Bill.resnr == res_line.resnr) & (Bill.reslinnr == res_line.reslinnr)).first()

                if bill and bill.argtumsatz > 0:
                    do_it = True
                    dayuse = True

                    if not res_line.zimmerfix:
                        anz_rmco = anz_rmco + 1
                    anz_adco = anz_adco + res_line.erwachs
                    anz_chco = anz_chco + res_line.kind1 + res_line.kind2
                    anz_cmco = anz_cmco + res_line.gratis
                    anz_cmchco = anz_cmchco + res_line.l_zuordnung[3]

                    if not res_line.zimmerfix:
                        anz_rmci = anz_rmci + 1
                    anz_adci = anz_adci + res_line.erwachs
                    anz_chci = anz_chci + res_line.kind1 + res_line.kind2
                    anz_cmci = anz_cmci + res_line.gratis
                    anz_cmchci = anz_cmchci + res_line.l_zuordnung[3]

            elif res_line.active_flag == 2 and (res_line.ankunft < res_line.abreise) and res_line.abreise == bill_date:

                if (res_line.erwachs + res_line.gratis) > 0:

                    if not res_line.zimmerfix:
                        anz_rmco = anz_rmco + 1
                    anz_adco = anz_adco + res_line.erwachs
                    anz_chco = anz_chco + res_line.kind1 + res_line.kind2
                    anz_cmco = anz_cmco + res_line.gratis
                    anz_cmchco = anz_cmchco + res_line.l_zuordnung[3]

            if res_line.active_flag == 1:

                if res_line.resstatus == 13:

                    rline = db_session.query(Rline).filter(
                             (Rline.active_flag == 1) & (Rline.resstatus == 6) & (Rline.zinr == res_line.zinr)).first()
                anz_comadult = anz_comadult + res_line.gratis
                anz_comchild = anz_comchild + res_line.l_zuordnung[3]


                do_it = True

                if res_line.zipreis == 0 and res_line.gratis > 0 and res_line.resstatus == 6:
                    co_flag = True

                elif res_line.zipreis == 0 and res_line.gratis == 0 and res_line.resstatus == 6 and res_line.erwachs > 0:
                    cb_flag = True

                if res_line.ankunft == bill_date:

                    if res_line.resstatus == 6:
                        anz_rmci = anz_rmci + 1

                    elif res_line.resstatus == 13 and not rline:
                        anz_rmci = anz_rmci + 1
                    anz_adci = anz_adci + res_line.erwachs
                    anz_chci = anz_chci + res_line.kind1 + res_line.kind2
                    anz_cmci = anz_cmci + res_line.gratis
                    anz_cmchci = anz_cmchci + res_line.l_zuordnung[3]

            if do_it and ((res_line.resstatus == 6) or (res_line.resstatus == 13) or (res_line.resstatus == 8 and not res_line.zimmerfix)):
                Rbuff =  create_buffer("Rbuff",Res_line)
                paxnum = 0

                if res_line.resstatus == 6:
                    paxnum = res_line.erwachs

                    for rbuff in db_session.query(Rbuff).filter(
                             (Rbuff.active_flag == 1) & (Rbuff.zinr == res_line.zinr) & (Rbuff.resstatus == 13)).order_by(Rbuff._recid).all():
                        paxnum = paxnum + rbuff.erwachs

                elif res_line.resstatus == 8:
                    paxnum = res_line.erwachs

                if paxnum == 1:

                    occ_list = query(occ_list_list, filters=(lambda occ_list: occ_list.nr == 1), first=True)
                    occ_list.rm = occ_list.rm + res_line.zimmeranz

                elif paxnum == 2:

                    occ_list = query(occ_list_list, filters=(lambda occ_list: occ_list.nr == 2), first=True)
                    occ_list.rm = occ_list.rm + res_line.zimmeranz

                elif paxnum == 3:

                    occ_list = query(occ_list_list, filters=(lambda occ_list: occ_list.nr == 3), first=True)
                    occ_list.rm = occ_list.rm + res_line.zimmeranz

                guest = db_session.query(Guest).filter(
                         (Guest.gastnr == res_line.gastnrmember)).first()

                reservation = db_session.query(Reservation).filter(
                         (Reservation.resnr == res_line.resnr)).first()

                if res_line.reserve_dec != 0:
                    frate =  to_decimal(res_line.reserve_dec)
                else:

                    waehrung = db_session.query(Waehrung).filter(
                             (Waehrung.waehrungsnr == res_line.betriebsnr)).first()
                    frate =  to_decimal(waehrung.ankauf) / to_decimal(waehrung.einheit)

                zk_list = query(zk_list_list, filters=(lambda zk_list: zk_list.zikatnr == res_line.zikatnr), first=True)

                argt_list = query(argt_list_list, filters=(lambda argt_list: argt_list.bezeich == res_line.arrangement), first=True)

                if not argt_list:
                    argt_list = Argt_list()
                    argt_list_list.append(argt_list)

                    argt_list.bezeich = res_line.arrangement

                if not dayuse and not co_flag and not cb_flag:

                    if (res_line.resstatus == 6) or (res_line.resstatus == 13 and not rline):
                        zk_list.zimmeranz = zk_list.zimmeranz + 1
                        argt_list.anz_rm = argt_list.anz_rm + 1

                        if res_line.ankunft == bill_date:

                            if reservation.segmentcode == walk_in:
                                anz_win = anz_win + 1
                            else:
                                anz_rsv = anz_rsv + 1
                    zk_list.anz_pax = zk_list.anz_pax + res_line.erwachs
                    zk_list.anz_child1 = zk_list.anz_child1 + res_line.kind1
                    zk_list.anz_child2 = zk_list.anz_child2 + res_line.kind2

                    if guest.nation1.lower()  == (domestic).lower() :
                        anz_dom = anz_dom + res_line.erwachs
                    else:
                        anz_for = anz_for + res_line.erwachs

                    nat_list = query(nat_list_list, filters=(lambda nat_list: nat_list.nat == trim(guest.nation1)), first=True)

                    if not nat_list:

                        nation = db_session.query(Nation).filter(
                                 (Nation.kurzbez == guest.nation1)).first()
                        nat_list = Nat_list()
                        nat_list_list.append(nat_list)


                        if nation:
                            nat_list.nat = trim(guest.nation1)

                        if not nation:

                            if trim(guest.nation1) == "":
                                nat_list.bezeich = "UNKNOWN"
                            else:
                                nat_list.bezeich = guest.nation1 + "- " + "UNKNOWN"
                        else:
                            nat_list.bezeich = nation.bezeich
                    nat_list.adult = nat_list.adult + res_line.erwachs
                    nat_list.child = nat_list.child + res_line.kind1 + res_line.kind2
                    argt_list.adult = argt_list.adult + res_line.erwachs

                if dayuse:

                    if not res_line.zimmerfix:
                        zk_list.dayuse = zk_list.dayuse + 1
                        argt_list.anz_rm = argt_list.anz_rm + 1

                        if res_line.ankunft == bill_date:

                            if reservation.segmentcode == walk_in:
                                anz_win = anz_win + 1
                            else:
                                anz_rsv = anz_rsv + 1
                    zk_list.du_pax = zk_list.du_pax + res_line.erwachs
                    zk_list.du_child1 = zk_list.du_child1 + res_line.kind1
                    zk_list.du_child2 = zk_list.du_child2 + res_line.kind2

                    if guest.nation1.lower()  == (domestic).lower() :
                        anz_dom = anz_dom + res_line.erwachs
                    else:
                        anz_for = anz_for + res_line.erwachs

                    nat_list = query(nat_list_list, filters=(lambda nat_list: nat_list.nat == trim(guest.nation1)), first=True)

                    if not nat_list:

                        nation = db_session.query(Nation).filter(
                                 (Nation.kurzbez == guest.nation1)).first()
                        nat_list = Nat_list()
                        nat_list_list.append(nat_list)


                        if nation:
                            nat_list.nat = trim(guest.nation1)

                        if not nation:

                            if trim(guest.nation1) == "":
                                nat_list.bezeich = "UNKNOWN"
                            else:
                                nat_list.bezeich = guest.nation1 + "- " + "UNKNOWN"
                        else:
                            nat_list.bezeich = nation.bezeich
                    nat_list.adult = nat_list.adult + res_line.erwachs
                    nat_list.child = nat_list.child + res_line.kind1 + res_line.kind2
                    argt_list.adult = argt_list.adult + res_line.erwachs

                if co_flag:

                    if (res_line.resstatus == 6) or (res_line.resstatus == 13 and not rline):
                        zk_list.co_rm = zk_list.co_rm + 1
                        argt_list.anz_rm = argt_list.anz_rm + 1

                        if res_line.ankunft == bill_date:

                            if reservation.segmentcode == walk_in:
                                anz_win = anz_win + 1
                            else:
                                anz_rsv = anz_rsv + 1
                    zk_list.co_pax = zk_list.co_pax + res_line.gratis

                    if guest.nation1.lower()  == (domestic).lower() :
                        anz_dom = anz_dom + res_line.gratis
                    else:
                        anz_for = anz_for + res_line.gratis

                    nat_list = query(nat_list_list, filters=(lambda nat_list: nat_list.nat == trim(guest.nation1)), first=True)

                    if not nat_list:

                        nation = db_session.query(Nation).filter(
                                 (Nation.kurzbez == guest.nation1)).first()
                        nat_list = Nat_list()
                        nat_list_list.append(nat_list)


                        if nation:
                            nat_list.nat = trim(guest.nation1)

                        if not nation:

                            if trim(guest.nation1) == "":
                                nat_list.bezeich = "UNKNOWN"
                            else:
                                nat_list.bezeich = guest.nation1 + "- " + "UNKNOWN"
                        else:
                            nat_list.bezeich = nation.bezeich
                    nat_list.adult = nat_list.adult + res_line.gratis
                    argt_list.adult = argt_list.adult + res_line.gratis

                if cb_flag:

                    if (res_line.resstatus == 6) or (res_line.resstatus == 13 and not rline):
                        zk_list.cb_rm = zk_list.cb_rm + 1
                        argt_list.anz_rm = argt_list.anz_rm + 1

                        if res_line.ankunft == bill_date:

                            if reservation.segmentcode == walk_in:
                                anz_win = anz_win + 1
                            else:
                                anz_rsv = anz_rsv + 1
                    zk_list.cb_pax = zk_list.cb_pax + res_line.erwachs
                    zk_list.anz_child1 = zk_list.anz_child1 + res_line.kind1
                    zk_list.anz_child2 = zk_list.anz_child2 + res_line.kind2

                    if guest.nation1.lower()  == (domestic).lower() :
                        anz_dom = anz_dom + res_line.erwachs
                    else:
                        anz_for = anz_for + res_line.erwachs

                    nat_list = query(nat_list_list, filters=(lambda nat_list: nat_list.nat == trim(guest.nation1)), first=True)

                    if not nat_list:

                        nation = db_session.query(Nation).filter(
                                 (Nation.kurzbez == guest.nation1)).first()
                        nat_list = Nat_list()
                        nat_list_list.append(nat_list)


                        if nation:
                            nat_list.nat = trim(guest.nation1)

                        if not nation:

                            if trim(guest.nation1) == "":
                                nat_list.bezeich = "UNKNOWN"
                            else:
                                nat_list.bezeich = guest.nation1 + "- " + "UNKNOWN"
                        else:
                            nat_list.bezeich = nation.bezeich
                    nat_list.adult = nat_list.adult + res_line.erwachs
                    nat_list.child = nat_list.child + res_line.kind1 + res_line.kind2
                    argt_list.adult = argt_list.adult + res_line.erwachs
                rate =  to_decimal("0")
                count_lodging()
                tot_lodging =  to_decimal(tot_lodging) + to_decimal(lodg_betrag)
        tot_lodging =  to_decimal("0")

        for segmentstat in db_session.query(Segmentstat).filter(
                 (Segmentstat.datum == bill_date)).order_by(Segmentstat._recid).all():
            tot_lodging =  to_decimal(tot_lodging) + to_decimal(segmentstat.logis)

        for zk_list in query(zk_list_list):
            zk_list.vacant = zk_list.anz100 - zk_list.zimmeranz - zk_list.co_rm - zk_list.cb_rm - zk_list.ooo

            if zk_list.vacant < 0:
                zk_list.vacant = 0

        zinrstat = db_session.query(Zinrstat).filter(
                 (func.lower(Zinrstat.zinr) == ("CancRes").lower()) & (Zinrstat.datum == bill_date)).first()

        if zinrstat:
            anz_can = anz_can + zinrstat.zimmeranz

        for res_line in db_session.query(Res_line).filter(
                 (Res_line.active_flag == 2) & (Res_line.resstatus == 10) & (Res_line.ankunft == bill_date)).order_by(Res_line._recid).all():
            anz_nos = anz_nos + res_line.zimmeranz


    def zkstat_list():

        nonlocal bill_date, tot_rev, domestic, tot_inactive, walk_in, anz_win, anz_rsv, anz_nos, anz_can, anz_dom, anz_for, anz_comadult, anz_comchild, anz_rmci, anz_rmco, anz_adci, anz_adco, anz_chci, anz_chco, anz_cmci, anz_cmco, anz_cmchci, anz_cmchco, lodg_betrag, rate, frate, exchg_rate, service, vat, vat2, fact, argt_betrag, ex_rate, grate, tot_lodging, price_decimal, foreign_rate, rm_serv, new_contrate, progname, night_type, reihenfolge, line_nr, line, p_width, p_length, htl_name, htl_adr, htl_tel, long_digit, paramtext, htparam, waehrung, nightaudit, nitestor, res_line, artikel, zimmer, zimkateg, bill_line, arrangement, bill, guest, reservation, nation, segmentstat, zinrstat, argt_line, reslin_queasy, guest_pr


        nonlocal occ_list, zk_list, nat_list, argt_list, segm_list
        nonlocal occ_list_list, zk_list_list, nat_list_list, argt_list_list, segm_list_list

        i:int = 0
        str1:str = ""
        str2:str = ""
        it_exist:bool = False
        curr_grp:str = ""
        tot_rm:int = 0
        tot_payrm:int = 0
        tot_occ:int = 0
        tot_occ1:int = 0
        tot_pax:int = 0
        tot_adult:int = 0
        tot_paypax:int = 0
        tot_child1:int = 0
        tot_child2:int = 0
        tot_du:int = 0
        tot_co:int = 0
        tot_cb:int = 0
        tot_dupax:int = 0
        tot_copax:int = 0
        tot_cbpax:int = 0
        tot_vc:int = 0
        tot_oo:int = 0
        tot_ia:int = 0
        nat_adult:int = 0
        nat_child:int = 0
        nat_proz:decimal = to_decimal("0.0")
        curr_nr:int = 0
        for i in range(1,p_width + 1) :
            str1 = str1 + "="
            str2 = str2 + "-"
        line = to_string(p_width) + "," + to_string(p_length)
        add_line(line)
        add_line("##header")
        line = to_string(htl_name, "x(40)")
        for i in range(1,18 + 1) :
            line = line + " "
        line = line + "Date/Time : " + to_string(get_current_date()) + " " + to_string(time, "HH:MM")
        add_line(line)
        line = to_string(htl_adr, "x(40)")
        add_line(line)
        line = "Tel" + " " + to_string(htl_tel, "x(36)")
        for i in range(1,18 + 1) :
            line = line + " "
        line = line + "Page : " + "##page"
        add_line(line)
        add_line(" ")
        line = "ROOM RECAPITULATION" + " - " + to_string(bill_date)
        add_line(line)
        add_line(str1)
        add_line(" ")
        add_line("##end-header")
        line = "R O O M SALEABLE OCCUPIED dayuse COMPL C.B" + " "
        line = line + "VACANT O-O-0"
        add_line(line)
        add_line(" ")

        for zk_list in query(zk_list_list):
            tot_rm = tot_rm + zk_list.anz100
            tot_payrm = tot_payrm + zk_list.zimmeranz + zk_list.cb_rm + zk_list.dayuse
            tot_occ = tot_occ + zk_list.zimmeranz
            tot_pax = tot_pax + zk_list.anz_pax
            tot_du = tot_du + zk_list.dayuse
            tot_co = tot_co + zk_list.co_rm
            tot_cb = tot_cb + zk_list.cb_rm
            tot_vc = tot_vc + zk_list.vacant
            tot_oo = tot_oo + zk_list.ooo
            tot_ia = tot_ia + zk_list.inactive
            tot_dupax = tot_dupax + zk_list.du_pax
            tot_copax = tot_copax + zk_list.co_pax
            tot_cbpax = tot_cbpax + zk_list.cb_pax
            tot_child1 = tot_child1 + zk_list.anz_child1 + zk_list.du_child1
            tot_child2 = tot_child2 + zk_list.anz_child2 + zk_list.du_child2
            tot_adult = tot_adult + zk_list.anz_pax + zk_list.du_pax + zk_list.co_pax + zk_list.cb_pax
            tot_paypax = tot_paypax + zk_list.anz_pax + zk_list.du_pax + zk_list.cb_pax
            tot_occ1 = tot_occ1 + zk_list.zimmeranz + zk_list.dayuse + zk_list.co_rm + zk_list.cb_rm
            tot_inactive = tot_inactive + zk_list.inactive
            line = to_string(zk_list.bezeich, "x(16) ") + to_string(zk_list.anz100, ">>>>>>>9 ") + to_string(zk_list.zimmeranz, ">>>>>>>> ") + to_string(zk_list.dayuse, ">>>>>> ") + to_string(zk_list.co_rm, ">>>>> ") + to_string(zk_list.cb_rm, ">>> ") + to_string(zk_list.vacant, ">>>>>> ") + to_string(zk_list.ooo, ">>>>>")
            add_line(line)
        add_line(str2)
        line = to_string("T O T A L", "x(16) ") + to_string(tot_rm, ">>>>>>>9 ") + to_string(tot_occ, ">>>>>>>> ") + to_string(tot_du, ">>>>>> ") + to_string(tot_co, ">>>>> ") + to_string(tot_cb, ">>> ") + to_string(tot_vc, ">>>>>> ") + to_string(tot_oo, ">>>>>")
        add_line(line)
        line = to_string("% Percentage", "x(16) ") + to_string(100, " >>9.99 ") + to_string(tot_occ / tot_rm * 100, " >>9.99 ") + to_string(tot_du / tot_rm * 100, ">>9.99 ") + to_string(tot_co / tot_rm * 100, ">>9.99 ") + to_string(tot_cb / tot_rm * 100, ">>9.99 ") + to_string(tot_vc / tot_rm * 100, ">>9.99 ") + to_string(tot_oo / tot_rm * 100, ">>9.99")
        add_line(line)
        add_line(" ")
        add_line(" ")
        line = to_string("Occupied", "x(16) ")

        if tot_occ > 0:
            line = line + to_string(tot_occ, ">>>>>>>> ") + to_string(tot_occ / tot_rm * 100, " >>9.99 % ") + to_string(tot_pax, ">>>>>>")
        line = to_string(line, "x(55)") + to_string("Walk In", "x(16)") + to_string(anz_win, ">>9 ") + "Rooms"
        add_line(line)
        line = to_string("Day Use", "x(16) ")

        if tot_du > 0:
            line = line + to_string(tot_du, ">>>>>>>> ") + to_string(tot_du / tot_rm * 100, " >>9.99 % ") + to_string(tot_dupax, ">>>>>> ")
        line = to_string(line, "x(55)") + to_string("Reserved", "x(16)") + to_string(anz_rsv, ">>9 ") + "Rooms"
        add_line(line)
        line = to_string("Compliment", "x(16) ")

        if tot_co > 0:
            line = line + to_string(tot_co, ">>>>>>>9 ") + to_string(tot_co / tot_rm * 100, " >>9.99 % ") + to_string(tot_copax, ">>>>>> ")
        line = to_string(line, "x(55)") + to_string("No SHow", "x(16)") + to_string(anz_nos, ">>9 ") + "Rooms"
        add_line(line)
        line = to_string("Compliment-B", "x(16) ")

        if tot_cb > 0:
            line = line + to_string(tot_cb, ">>>>>>>9 ") + to_string(tot_cb / tot_rm * 100, " >>9.99 % ") + to_string(tot_cbpax, ">>>>>> ")
        line = to_string(line, "x(55)") + to_string("Cancelled", "x(16)") + to_string(anz_can, ">>9 ") + "Rooms"
        add_line(line)
        line = to_string("Total Occ+Comp", "x(16) ") + to_string(tot_occ1, ">>>>>>>9 ") + to_string(tot_occ1 / tot_rm * 100, " >>9.99 % ") + to_string(tot_adult, ">>>>>> ")
        line = to_string(line, "x(55)") + to_string("Child (02-12)", "x(16)") + to_string(tot_child1, ">>9 ") + "Pax"
        add_line(line)
        line = to_string("Vacant", "x(16) ")

        if tot_vc > 0:
            line = line + to_string(tot_vc, ">>>>>>>9 ") + to_string(tot_vc / tot_rm * 100, " >>9.99 % ") + to_string(0, ">>>>>> ")
        line = to_string(line, "x(55)") + to_string("Junior (13-16)", "x(16)") + to_string(tot_child2, ">>9 ") + "Pax"
        add_line(line)
        line = to_string("Out-of-order", "x(16) ")

        if tot_oo > 0:
            line = line + to_string(tot_oo, ">>>>>>>9 ") + to_string(tot_oo / tot_rm * 100, " >>9.99 % ") + to_string(0, ">>>>>> ")
        line = to_string(line, "x(55)") + to_string("Adult", "x(16)") + to_string(tot_adult, ">>9 ") + "Pax"
        add_line(line)
        line = to_string(" ", "x(55)") + to_string("Comp Child", "x(16)") + to_string(anz_comchild, ">>9 ") + "Pax"
        add_line(line)
        line = to_string(" ", "x(55)") + to_string("Comp Adult", "x(16)") + to_string(anz_comadult, ">>9 ") + "Pax"
        add_line(line)
        line = to_string(" ", "x(55)") + to_string("domestic", "x(16)") + to_string(anz_dom, ">>9 ") + "Pax"
        add_line(line)
        line = to_string("Total Active Room", "x(18)") + to_string(tot_rm, ">>>>>>>9 ") + to_string(100, " >>9.99 % ")
        line = to_string(line, "x(55)") + to_string("Foreigner", "x(16)") + to_string(anz_for, ">>9 ") + "Pax"
        add_line(line)
        line = to_string("Inactive Room", "x(16) ")

        if tot_inactive > 0:
            line = line + to_string(tot_inactive, ">>>>>>>9 ")
        line = to_string(line, "x(55)") + to_string("Double Occ", "x(16)") + to_string((tot_adult - tot_occ1) , ">>9 ") + "Pax"
        add_line(line)
        line = to_string(" ", "x(55)") + to_string("Percentage", "x(16)") + to_string((tot_adult - tot_occ1) / tot_occ1 * 100, ">>9.99 ") + "%"
        add_line(line)
        line = to_string("Average Guest/Room", "x(18) ") + to_string(tot_paypax / tot_payrm, " >>9.99")
        add_line(line)

        if not long_digit:
            line = to_string("Average rate/Room", "x(18) ") + to_string(tot_rev / tot_payrm, ">,>>>,>>>,>>9.99")
            line = to_string(line, "x(55)") + to_string("Tot Room Rev" + " ", "x(14)") + trim(to_string(tot_rev, ">>>,>>>,>>9"))
        else:
            line = to_string("Average rate/Room", "x(18) ") + to_string(tot_rev / tot_payrm, ">>>>,>>>,>>9")
            line = to_string(line, "x(55)") + to_string("Tot Room Rev" + " ", "x(14)") + trim(to_string(tot_rev, ">>>,>>>,>>>,>>9"))
        add_line(line)

        if not long_digit:
            line = to_string("Average rate/Guest", "x(18) ") + to_string(tot_rev / tot_paypax, ">,>>>,>>>,>>9.99")
        else:
            line = to_string("Average rate/Guest", "x(18) ") + to_string(tot_rev / tot_paypax, ">>>>,>>>,>>9")
        add_line(line)

        if not long_digit:
            line = to_string("Average Lodging/Room", "x(18) ") + to_string(tot_lodging / tot_payrm, ">,>>>,>>>,>>9.99")
            line = to_string(line, "x(55)") + to_string("Tot Room Rev" + " ", "x(14)") + trim(to_string(tot_lodging, ">>>,>>>,>>9"))
        else:
            line = to_string("Average Lodging/Room", "x(18) ") + to_string(tot_lodging / tot_payrm, ">>>>,>>>,>>9")
            line = to_string(line, "x(55)") + to_string("Tot Room Rev" + " ", "x(14)") + trim(to_string(tot_lodging, ">>>,>>>,>>>,>>9"))
        add_line(line)

        if not long_digit:
            line = to_string("Average Lodging/Guest", "x(18) ") + to_string(tot_lodging / tot_paypax, ">,>>>,>>>,>>9.99")
        else:
            line = to_string("Average Lodging/Guest", "x(18) ") + to_string(tot_lodging / tot_paypax, ">>>>,>>>,>>9")
        add_line(line)
        add_line(" ")
        add_line(" ")
        line = "Actual-Arrival Room" + " " + to_string(anz_rmci, ">>9") + " / " + "Adult" + " " + to_string(anz_adci, ">>9") + " / " + "Child" + " " + to_string(anz_chci, ">9") + " / " + "Comp" + " " + to_string(anz_cmci, ">9") + " / " + "CompChild" + " " + to_string(anz_cmchci, ">9")
        add_line(line)
        line = "Actual-Departure Room" + " " + to_string(anz_rmco, ">>9") + " / " + "Adult" + " " + to_string(anz_adco, ">>9") + " / " + "Child" + " " + to_string(anz_chco, ">9") + " / " + "Comp" + " " + to_string(anz_cmco, ">9") + " / " + "CompChild" + " " + to_string(anz_cmchco, ">9")
        add_line(line)
        add_line(" ")
        add_line(" ")

        for nat_list in query(nat_list_list, sort_by=[("bezeich",False)]):
            nat_list.proz =  to_decimal(nat_list.adult) / to_decimal(tot_adult) * to_decimal("100")

            argt_list = query(argt_list_list, filters=(lambda argt_list: argt_list.bezeich != ""), first=True)

            if argt_list:

                arrangement = db_session.query(Arrangement).filter(
                         (Arrangement.arrangement == argt_list.bezeich)).first()
                line = to_string(arrangement.argt_bez, "x(24) ") + to_string(argt_list.anz_rm, ">>9 ") + "Rm" + " " + to_string(argt_list.adult, ">>>>9 ") + "Pax" + " " + to_string(nat_list.bezeich, "x(16) ") + to_string(nat_list.adult, ">>> ") + to_string(nat_list.proz, ">>9.99") + "% " + to_string(nat_list.child, ">>>")
                argt_list_list.remove(argt_list)
            else:

                if curr_nr == 0:
                    line = to_string(" ", "x(45)") + to_string(nat_list.bezeich, "x(16) ") + to_string(nat_list.adult, ">>> ") + to_string(nat_list.proz, ">>9.99") + "% " + to_string(nat_list.child, ">>>")
                    curr_nr = 1

                elif curr_nr == 1:

                    occ_list = query(occ_list_list, filters=(lambda occ_list: occ_list.nr == 1), first=True)
                    line = "Single Adult Occupancy" + " " + to_string(occ_list.rm, ">>>>9") + " " + "Rm" + " " + to_string(nat_list.bezeich, "x(16) ") + to_string(nat_list.adult, ">>> ") + to_string(nat_list.proz, ">>9.99") + "% " + to_string(nat_list.child, ">>>")
                    curr_nr = 2

                elif curr_nr == 2:

                    occ_list = query(occ_list_list, filters=(lambda occ_list: occ_list.nr == 2), first=True)
                    line = "Double Adult Occupancy" + " " + to_string(occ_list.rm, ">>>>9") + " " + "Rm" + " " + to_string(nat_list.bezeich, "x(16) ") + to_string(nat_list.adult, ">>> ") + to_string(nat_list.proz, ">>9.99") + "% " + to_string(nat_list.child, ">>>")
                    curr_nr = 3

                elif curr_nr == 3:

                    occ_list = query(occ_list_list, filters=(lambda occ_list: occ_list.nr == 3), first=True)
                    line = "Triple Adult Occupancy" + " " + to_string(occ_list.rm, ">>>>9") + " " + "Rm" + " " + to_string(nat_list.bezeich, "x(16) ") + to_string(nat_list.adult, ">>> ") + to_string(nat_list.proz, ">>9.99") + "% " + to_string(nat_list.child, ">>>")
                    curr_nr = 4
                else:
                    line = to_string(" ", "x(45)") + to_string(nat_list.bezeich, "x(16) ") + to_string(nat_list.adult, ">>> ") + to_string(nat_list.proz, ">>9.99") + "% " + to_string(nat_list.child, ">>>")
            add_line(line)
            nat_adult = nat_adult + nat_list.adult
            nat_child = nat_child + nat_list.child
            nat_proz =  to_decimal(nat_proz) + to_decimal(nat_list.proz)

        argt_list = query(argt_list_list, filters=(lambda argt_list: argt_list.bezeich != ""), first=True)
        while None != argt_list:

            arrangement = db_session.query(Arrangement).filter(
                     (Arrangement.arrangement == argt_list.bezeich)).first()
            line = to_string(arrangement.argt_bez, "x(24) ") + to_string(argt_list.anz_rm, ">>9 ") + "Rm" + " " + to_string(argt_list.adult, ">>>>9 ") + " " + "Pax" + " "
            add_line(line)

            argt_list = query(argt_list_list, filters=(lambda argt_list: argt_list.bezeich != ""), next=True)

        if curr_nr == 0:
            line = ""
            add_line(line)
            curr_nr = 1

        if curr_nr == 1:

            occ_list = query(occ_list_list, filters=(lambda occ_list: occ_list.nr == 1), first=True)
            line = "Single Adult Occupancy" + " " + to_string(occ_list.rm, ">>>>9") + " " + "Rm"
            add_line(line)
            curr_nr = 2

        if curr_nr == 2:

            occ_list = query(occ_list_list, filters=(lambda occ_list: occ_list.nr == 2), first=True)
            line = "Double Adult Occupancy" + " " + to_string(occ_list.rm, ">>>>9") + " " + "Rm"
            add_line(line)
            curr_nr = 3

        if curr_nr == 3:

            occ_list = query(occ_list_list, filters=(lambda occ_list: occ_list.nr == 3), first=True)
            line = "Triple Adult Occupancy" + " " + to_string(occ_list.rm, ">>>>9") + " " + "Rm"
            add_line(line)
        add_line(str1)
        line = to_string(" " + "T O T A L", "x(45)") + to_string(" ", "x(16) ") + to_string(nat_adult, ">>> ") + to_string(nat_proz, ">>9.99") + "% " + to_string(nat_child, ">>>")
        add_line(line)
        add_line("##end-of-file")


    def add_line(s:str):

        nonlocal bill_date, tot_rev, domestic, tot_inactive, walk_in, anz_win, anz_rsv, anz_nos, anz_can, anz_dom, anz_for, anz_comadult, anz_comchild, anz_rmci, anz_rmco, anz_adci, anz_adco, anz_chci, anz_chco, anz_cmci, anz_cmco, anz_cmchci, anz_cmchco, lodg_betrag, rate, frate, exchg_rate, service, vat, vat2, fact, argt_betrag, ex_rate, grate, tot_lodging, price_decimal, foreign_rate, rm_serv, new_contrate, progname, night_type, reihenfolge, line_nr, line, p_width, p_length, htl_name, htl_adr, htl_tel, long_digit, paramtext, htparam, waehrung, nightaudit, nitestor, res_line, artikel, zimmer, zimkateg, bill_line, arrangement, bill, guest, reservation, nation, segmentstat, zinrstat, argt_line, reslin_queasy, guest_pr


        nonlocal occ_list, zk_list, nat_list, argt_list, segm_list
        nonlocal occ_list_list, zk_list_list, nat_list_list, argt_list_list, segm_list_list

        nitestor = db_session.query(Nitestor).filter(
                 (Nitestor.night_type == night_type) & (Nitestor.reihenfolge == reihenfolge) & (Nitestor.line_nr == line_nr)).first()

        if not nitestor:
            nitestor = Nitestor()
            db_session.add(nitestor)

            nitestor.night_type = night_type
            nitestor.reihenfolge = reihenfolge
            nitestor.line_nr = line_nr
        nitestor.line = s
        line_nr = line_nr + 1


    def count_lodging():

        nonlocal bill_date, tot_rev, domestic, tot_inactive, walk_in, anz_win, anz_rsv, anz_nos, anz_can, anz_dom, anz_for, anz_comadult, anz_comchild, anz_rmci, anz_rmco, anz_adci, anz_adco, anz_chci, anz_chco, anz_cmci, anz_cmco, anz_cmchci, anz_cmchco, lodg_betrag, rate, frate, exchg_rate, service, vat, vat2, fact, argt_betrag, ex_rate, grate, tot_lodging, price_decimal, foreign_rate, rm_serv, new_contrate, progname, night_type, reihenfolge, line_nr, line, p_width, p_length, htl_name, htl_adr, htl_tel, long_digit, paramtext, htparam, waehrung, nightaudit, nitestor, res_line, artikel, zimmer, zimkateg, bill_line, arrangement, bill, guest, reservation, nation, segmentstat, zinrstat, argt_line, reslin_queasy, guest_pr


        nonlocal occ_list, zk_list, nat_list, argt_list, segm_list
        nonlocal occ_list_list, zk_list_list, nat_list_list, argt_list_list, segm_list_list

        bonus:bool = False
        n:int = 0
        i:int = 0

        htparam = db_session.query(Htparam).filter(
                 (Htparam.paramnr == 491)).first()
        price_decimal = htparam.finteger

        htparam = db_session.query(Htparam).filter(
                 (Htparam.paramnr == 143)).first()
        foreign_rate = htparam.flogical
        bonus = check_bonus()

        if (res_line.zipreis > 0 or bonus):

            if res_line.reserve_dec != 0:
                frate =  to_decimal(res_line.reserve_dec)
            else:

                waehrung = db_session.query(Waehrung).filter(
                         (Waehrung.waehrungsnr == res_line.betriebsnr)).first()

                if waehrung:
                    frate =  to_decimal(waehrung.ankauf) / to_decimal(waehrung.einheit)
            rate =  to_decimal(res_line.zipreis)

            artikel = db_session.query(Artikel).filter(
                     (Artikel.artnr == arrangement.artnr_logis) & (Artikel.departement == 0)).first()
            service, vat, vat2, fact = get_output(calc_servtaxesbl(1, artikel.artnr, artikel.departement, bill_date))
            lodg_betrag =  to_decimal(rate) * to_decimal(frate)

            if rate > 0:

                for argt_line in db_session.query(Argt_line).filter(
                         (Argt_line.argtnr == arrangement.argtnr) & (not Argt_line.kind2)).order_by(Argt_line._recid).all():

                    artikel = db_session.query(Artikel).filter(
                             (Artikel.artnr == argt_line.argt_artnr) & (Artikel.departement == argt_line.departement)).first()
                    argt_betrag, ex_rate = get_output(argt_betrag(res_line._recid, argt_line._recid))
                    lodg_betrag =  to_decimal(lodg_betrag) - to_decimal(argt_betrag) * to_decimal(ex_rate)

        lodg_betrag = to_decimal(round(lodg_betrag , price_decimal))
        rate = to_decimal(round(rate * frate , price_decimal))

        if foreign_rate and price_decimal == 0:

            htparam = db_session.query(Htparam).filter(
                     (Htparam.paramnr == 145)).first()

            if htparam.finteger != 0:
                n = 1
                for i in range(1,htparam.finteger + 1) :
                    n = n * 10
                rate = to_decimal(round(rate / n , 0) * n)

        if rm_serv:
            grate =  to_decimal(rate) * to_decimal(fact)
        else:
            grate =  to_decimal(rate)
            rate =  to_decimal(rate) / to_decimal(fact)
            lodg_betrag =  to_decimal(lodg_betrag) / to_decimal(fact)


    def check_bonus():

        nonlocal bill_date, tot_rev, domestic, tot_inactive, walk_in, anz_win, anz_rsv, anz_nos, anz_can, anz_dom, anz_for, anz_comadult, anz_comchild, anz_rmci, anz_rmco, anz_adci, anz_adco, anz_chci, anz_chco, anz_cmci, anz_cmco, anz_cmchci, anz_cmchco, lodg_betrag, rate, frate, exchg_rate, service, vat, vat2, fact, argt_betrag, ex_rate, grate, tot_lodging, price_decimal, foreign_rate, rm_serv, new_contrate, progname, night_type, reihenfolge, line_nr, line, p_width, p_length, htl_name, htl_adr, htl_tel, long_digit, paramtext, htparam, waehrung, nightaudit, nitestor, res_line, artikel, zimmer, zimkateg, bill_line, arrangement, bill, guest, reservation, nation, segmentstat, zinrstat, argt_line, reslin_queasy, guest_pr


        nonlocal occ_list, zk_list, nat_list, argt_list, segm_list
        nonlocal occ_list_list, zk_list_list, nat_list_list, argt_list_list, segm_list_list

        bonus = False
        bonus_array:List[bool] = create_empty_list(999, False)
        i:int = 0
        j:int = 1
        k:int = 0
        n:int = 0
        stay:int = 0
        pay:int = 0
        num_bonus:int = 0
        curr_zikatnr:int = 0
        rmcat = None

        def generate_inner_output():
            return (bonus)

        Rmcat =  create_buffer("Rmcat",Zimkateg)

        reslin_queasy = db_session.query(Reslin_queasy).filter(
                 (func.lower(Reslin_queasy.key) == ("arrangement").lower()) & (Reslin_queasy.resnr == res_line.resnr) & (Reslin_queasy.reslinnr == res_line.reslinnr) & (Reslin_queasy.bill_date >= Reslin_queasy.date1) & (Reslin_queasy.bill_date <= Reslin_queasy.date2)).first()

        if reslin_queasy:

            return generate_inner_output()

        guest_pr = db_session.query(Guest_pr).filter(
                 (Guest_pr.gastnr == res_line.gastnr)).first()

        if res_line.l_zuordnung[0] != 0:

            rmcat = db_session.query(Rmcat).filter(
                     (Rmcat.zikatnr == res_line.l_zuordnung[0])).first()
            curr_zikatnr = rmcat.zikatnr
        else:
            curr_zikatnr = res_line.zikatnr

        if new_contrate and guest_pr:
            bonus = get_output(ratecode_compli(res_line.resnr, res_line.reslinnr, guest_pr.code, curr_zikatnr, bill_date))

            return generate_inner_output()

        arrangement = db_session.query(Arrangement).filter(
                 (Arrangement.arrangement == res_line.arrangement)).first()

        if len(arrangement.OPTIONS) != 16:

            return generate_inner_output()
        j = 1
        for i in range(1,4 + 1) :
            stay = 0
            pay = 0
            stay = to_int(substring(options, j - 1, 2))
            pay = to_int(substring(options, j + 2 - 1, 2))

            if (stay - pay) > 0:
                n = num_bonus + pay + 1
                for k in range(n,stay + 1) :
                    bonus_array[k - 1] = True
                num_bonus = stay - pay
            j = j + 4
        n = bill_date - res_line.ankunft + 1
        bonus = False

        if n <= 999:
            bonus = bonus_array[n - 1]

        return generate_inner_output()


    paramtext = db_session.query(Paramtext).filter(
             (Paramtext.txtnr == 200)).first()
    htl_name = paramtext.ptexte

    paramtext = db_session.query(Paramtext).filter(
             (Paramtext.txtnr == 201)).first()
    htl_adr = paramtext.ptexte

    paramtext = db_session.query(Paramtext).filter(
             (Paramtext.txtnr == 204)).first()
    htl_tel = paramtext.ptexte

    htparam = db_session.query(Htparam).filter(
             (Htparam.paramnr == 246)).first()
    long_digit = htparam.flogical

    htparam = db_session.query(Htparam).filter(
             (Htparam.paramnr == 110)).first()
    bill_date = htparam.fdate

    htparam = db_session.query(Htparam).filter(
             (Htparam.paramnr == 48)).first()
    walk_in = htparam.finteger

    htparam = db_session.query(Htparam).filter(
             (Htparam.paramnr == 276)).first()
    domestic = htparam.fchar

    htparam = db_session.query(Htparam).filter(
             (Htparam.paramnr == 550)).first()

    if htparam.feldtyp == 4:
        new_contrate = htparam.flogical
    exchg_rate =  to_decimal("1")

    htparam = db_session.query(Htparam).filter(
             (Htparam.paramnr == 143)).first()

    if htparam.flogical:

        htparam = db_session.query(Htparam).filter(
                 (Htparam.paramnr == 144)).first()

        waehrung = db_session.query(Waehrung).filter(
                 (Waehrung.wabkurz == htparam.fchar)).first()

        if waehrung:
            exchg_rate =  to_decimal(waehrung.ankauf) / to_decimal(waehrung.einheit)

    nightaudit = db_session.query(Nightaudit).filter(
             (func.lower(Nightaudit.programm) == (progname).lower())).first()

    if nightaudit:

        if nightaudit.hogarest == 0:
            night_type = 0
        else:
            night_type = 2
        reihenfolge = nightaudit.reihenfolge

        for nitestor in db_session.query(Nitestor).filter(
                 (Nitestor.night_type == night_type) & (Nitestor.reihenfolge == reihenfolge)).order_by(Nitestor._recid).all():
            db_session.delete(nitestor)
        create_zkstat()
        zkstat_list()

    return generate_output()