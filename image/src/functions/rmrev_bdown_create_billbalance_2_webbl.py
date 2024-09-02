from functions.additional_functions import *
import decimal
from datetime import date
from functions.calc_servtaxesbl import calc_servtaxesbl
import re
from sqlalchemy import func
from functions.ratecode_seek import ratecode_seek
from models import Waehrung, Guest, Artikel, Htparam, Zimmer, Res_line, Arrangement, Reservation, Bill, Segment, Reslin_queasy, Guest_pr, Pricecod, Argt_line, Fixleist

def rmrev_bdown_create_billbalance_2_webbl(exc_taxserv:bool, pvilanguage:int, new_contrate:bool, foreign_rate:bool, price_decimal:int, curr_date:date):
    msg_str = ""
    msg_warning = ""
    cl_list_list = []
    currency_list_list = []
    sum_list_list = []
    s_list_list = []
    exchg_rate:decimal = 1
    frate:decimal = 0
    post_it:bool = False
    total_rev:decimal = 0
    rm_rate:decimal = 0
    lvcarea:str = "rmrev_bdown"
    waehrung = guest = artikel = htparam = zimmer = res_line = arrangement = reservation = bill = segment = reslin_queasy = guest_pr = pricecod = argt_line = fixleist = None

    sum_list = currency_list = cl_list = s_list = waehrung1 = cc_list = member1 = rguest = artikel1 = argtline = None

    sum_list_list, Sum_list = create_model("Sum_list", {"bezeich":str, "pax":int, "adult":int, "ch1":int, "ch2":int, "comch":int, "com":int, "lodging":decimal, "bfast":decimal, "lunch":decimal, "dinner":decimal, "misc":decimal, "fixcost":decimal, "t_rev":decimal})
    currency_list_list, Currency_list = create_model("Currency_list", {"code":str})
    cl_list_list, Cl_list = create_model("Cl_list", {"zipreis":decimal, "localrate":decimal, "lodging":decimal, "bfast":decimal, "lunch":decimal, "dinner":decimal, "misc":decimal, "fixcost":decimal, "t_rev":decimal, "c_zipreis":str, "c_localrate":str, "c_lodging":str, "c_bfast":str, "c_lunch":str, "c_dinner":str, "c_misc":str, "c_fixcost":str, "ct_rev":str, "res_recid":int, "sleeping":bool, "row_disp":int, "flag":str, "zinr":str, "rstatus":int, "argt":str, "currency":str, "ratecode":str, "pax":int, "com":int, "ankunft":date, "abreise":date, "rechnr":int, "name":str, "ex_rate":str, "fix_rate":str, "adult":int, "ch1":int, "ch2":int, "comch":int, "age1":int, "age2":str, "rmtype":str, "resnr":int, "resname":str, "segm_desc":str, "nation":str}, {"sleeping": True})
    s_list_list, S_list = create_model("S_list", {"artnr":int, "dept":int, "bezeich":str, "curr":str, "anzahl":int, "betrag":decimal, "l_betrag":decimal, "f_betrag":decimal})

    Waehrung1 = Waehrung
    Cc_list = Cl_list
    cc_list_list = cl_list_list

    Member1 = Guest
    Rguest = Guest
    Artikel1 = Artikel
    Argtline = Argt_line

    db_session = local_storage.db_session

    def generate_output():
        nonlocal msg_str, msg_warning, cl_list_list, currency_list_list, sum_list_list, s_list_list, exchg_rate, frate, post_it, total_rev, rm_rate, lvcarea, waehrung, guest, artikel, htparam, zimmer, res_line, arrangement, reservation, bill, segment, reslin_queasy, guest_pr, pricecod, argt_line, fixleist
        nonlocal waehrung1, cc_list, member1, rguest, artikel1, argtline


        nonlocal sum_list, currency_list, cl_list, s_list, waehrung1, cc_list, member1, rguest, artikel1, argtline
        nonlocal sum_list_list, currency_list_list, cl_list_list, s_list_list
        return {"msg_str": msg_str, "msg_warning": msg_warning, "cl-list": cl_list_list, "currency-list": currency_list_list, "sum-list": sum_list_list, "s-list": s_list_list}

    def create_billbalance():

        nonlocal msg_str, msg_warning, cl_list_list, currency_list_list, sum_list_list, s_list_list, exchg_rate, frate, post_it, total_rev, rm_rate, lvcarea, waehrung, guest, artikel, htparam, zimmer, res_line, arrangement, reservation, bill, segment, reslin_queasy, guest_pr, pricecod, argt_line, fixleist
        nonlocal waehrung1, cc_list, member1, rguest, artikel1, argtline


        nonlocal sum_list, currency_list, cl_list, s_list, waehrung1, cc_list, member1, rguest, artikel1, argtline
        nonlocal sum_list_list, currency_list_list, cl_list_list, s_list_list

        fcost:decimal = 0
        tot_pax:int = 0
        tot_com:int = 0
        tot_rm:int = 0
        tot_rate:decimal = 0
        tot_lrate:decimal = 0
        tot_lodging:decimal = 0
        tot_bfast:decimal = 0
        tot_lunch:decimal = 0
        tot_dinner:decimal = 0
        tot_misc:decimal = 0
        tot_fix:decimal = 0
        tot_adult:int = 0
        tot_ch1:int = 0
        tot_ch2:int = 0
        tot_comch:int = 0
        ltot_rm:int = 0
        ltot_pax:int = 0
        ltot_rate:decimal = 0
        ltot_lodging:decimal = 0
        ltot_bfast:decimal = 0
        ltot_lunch:decimal = 0
        ltot_dinner:decimal = 0
        ltot_misc:decimal = 0
        ltot_fix:decimal = 0
        curr_zinr:str = ""
        curr_resnr:int = 0
        bfast_art:int = 0
        lunch_art:int = 0
        dinner_art:int = 0
        lundin_art:int = 0
        fb_dept:int = 0
        argt_betrag:decimal = 0
        take_it:bool = False
        prcode:int = 0
        qty:int = 0
        r_qty:int = 0
        lodge_betrag:decimal = 0
        f_betrag:decimal = 0
        s:str = ""
        ct:str = ""
        contcode:str = ""
        vat:decimal = 0
        service:decimal = 0
        serv:decimal = 0
        vat2:decimal = 0
        fact:decimal = 0
        curr_zikatnr:int = 0
        loopi:int = 0
        i:int = 0
        n:int = 0
        curr_code:str = ""
        curr_rate:decimal = 0
        curr_local:decimal = 0
        curr_bfast:decimal = 0
        curr_lodge:decimal = 0
        curr_lunch:decimal = 0
        curr_dinner:decimal = 0
        curr_misc:decimal = 0
        curr_fcost:decimal = 0
        curr_trev:decimal = 0
        curr_pax:int = 0
        curr_com:int = 0
        curr_rm:int = 0
        curr_adult:int = 0
        curr_ch1:int = 0
        curr_ch2:int = 0
        curr_comch:int = 0
        Member1 = Guest
        Rguest = Guest
        Artikel1 = Artikel

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 125)).first()
        bfast_art = finteger

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 126)).first()
        fb_dept = finteger

        artikel = db_session.query(Artikel).filter(
                (Artikel.zwkum == bfast_art) &  (Artikel.departement == fb_dept)).first()

        if not artikel and bfast_art != 0:
            msg_str = translateExtended ("B'fast SubGrp not yed defined (Grp 7)", lvcarea, "")

            return

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 227)).first()
        lunch_art = finteger

        artikel = db_session.query(Artikel).filter(
                (Artikel.zwkum == lunch_art) &  (Artikel.departement == fb_dept)).first()

        if not artikel and lunch_art != 0:
            msg_str = translateExtended ("Lunch SubGrp not yed defined (Grp 7)", lvcarea, "")

            return

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 228)).first()
        dinner_art = finteger

        artikel = db_session.query(Artikel).filter(
                (Artikel.zwkum == dinner_art) &  (Artikel.departement == fb_dept)).first()

        if not artikel and dinner_art != 0:
            msg_str = translateExtended ("Dinner SubGrp not yed defined (Grp 7)", lvcarea, "")

            return

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 229)).first()
        lundin_art = finteger

        artikel = db_session.query(Artikel).filter(
                (Artikel.zwkum == lundin_art) &  (Artikel.departement == fb_dept)).first()

        if not artikel and lundin_art != 0:
            msg_str = translateExtended ("HalfBoard SubGrp not yed defined (Grp 7)", lvcarea, "")

            return
        s_list_list.clear()
        cl_list_list.clear()
        currency_list_list.clear()

        if sum_list:
            sum_list_list.remove(sum_list)
        sum_list = Sum_list()
        sum_list_list.append(sum_list)

        r_qty = 0
        lodge_betrag = 0

        res_line_obj_list = []
        for res_line, zimmer in db_session.query(Res_line, Zimmer).join(Zimmer,(Zimmer.zinr == Res_line.zinr)).filter(
                ((Res_line.active_flag == 1) &  (Res_line.resstatus == 6)) &  (Res_line.l_zuordnung[2] == 0)).all():
            if res_line._recid in res_line_obj_list:
                continue
            else:
                res_line_obj_list.append(res_line._recid)

            arrangement = db_session.query(Arrangement).filter(
                    (Arrangement == res_line.arrangement)).first()

            artikel = db_session.query(Artikel).filter(
                    (Artikel.artnr == arrangement.argt_artikelnr) &  (Artikel.departement == 0)).first()
            serv = 0
            vat = 0
            vat2 = 0
            fact = 0


            service, vat, vat2, fact = get_output(calc_servtaxesbl(1, artikel.artnr, artikel.departement, curr_date))

            waehrung1 = db_session.query(Waehrung1).filter(
                    (Waehrung1.waehrungsnr == res_line.betriebsnr)).first()
            exchg_rate = waehrung1.ankauf / waehrung1.einheit

            if res_line.reserve_dec != 0:
                frate = reserve_dec
            else:
                frate = exchg_rate

            if res_line.zipreis != 0:
                r_qty = r_qty + 1

            guest = db_session.query(Guest).filter(
                    (Guest.gastnr == res_line.gastnrpay)).first()

            member1 = db_session.query(Member1).filter(
                    (Member1.gastnr == res_line.gastnrmember)).first()

            reservation = db_session.query(Reservation).filter(
                    (Reservation.resnr == res_line.resnr)).first()

            if res_line.l_zuordnung[0] != 0:
                curr_zikatnr = res_line.l_zuordnung[0]
            else:
                curr_zikatnr = res_line.zikatnr

            bill = db_session.query(Bill).filter(
                    (Bill.resnr == res_line.resnr) &  (Bill.reslinnr == res_line.reslinnr) &  (Bill.zinr == res_line.zinr)).first()

            if not bill:

                bill = db_session.query(Bill).filter(
                        (Bill.resnr == res_line.resnr) &  (Bill.reslinnr == res_line.reslinnr)).first()

                if not bill:
                    msg_warning = "&W" + translateExtended ("Bill not found: RmNo ", lvcarea, "") + res_line.zinr + " - " + res_line.name
            sum_list.pax = sum_list.pax +\
                    res_line.erwachs + res_line.kind1 + res_line.kind2
            sum_list.adult = sum_list.adult + res_line.erwachs
            sum_list.com = sum_list.com + res_line.gratis


            cl_list = Cl_list()
            cl_list_list.append(cl_list)

            cl_list.res_recid = res_line._recid
            cl_list.zinr = res_line.zinr
            cl_list.rstatus = res_line.resstatus
            cl_list.sleeping = zimmer.sleeping
            cl_list.argt = res_line.arrangement
            cl_list.name = res_line.name
            cl_list.com = res_line.gratis
            cl_list.ankunft = res_line.ankunft
            cl_list.abreise = res_line.abreise
            cl_list.zipreis = res_line.zipreis
            cl_list.localrate = res_line.zipreis * frate
            cl_list.t_rev = res_line.zipreis
            cl_list.resnr = res_line.resnr
            cl_list.resname = res_line.resname


            cl_list.adult = res_line.erwachs
            cl_list.ch1 = res_line.kind1
            cl_list.ch2 = res_line.kind2
            cl_list.comch = res_line.l_zuordnung[3]

            if cl_list.zipreis == 0:
                cl_list.pax = res_line.gratis + cl_list.comch


            else:
                cl_list.pax = res_line.erwachs + res_line.kind1 + res_line.kind2 + res_line.gratis + cl_list.comch

            segment = db_session.query(Segment).filter(
                    (Segment.segmentcode == reservation.segmentcode)).first()

            if segment:
                cl_list.segm_desc = segment.bezeich

            if member1.nation1 != "":
                cl_list.nation = member1.nation1

            if guest:
                cl_list.name = cl_list.name + guest.name + ", " + guest.vorname1 + "-" + guest.adresse1
                cl_list.rechnr = bill.rechnr
                cl_list.currency = waehrung1.wabkurz

            if guest.geburtdatum1 != None and guest.geburtdatum2 != None:

                if guest.geburtdatum1 < guest.geburtdatum2:
                    cl_list.age1 = get_year(guest.geburtdatum2) - get_year(guest.geburtdatum1)

            if re.match(".*ChAge.*",res_line.zimmer_wunsch):
                for loopi in range(1,num_entries(res_line.zimmer_wunsch, ";") - 1 + 1) :
                    s = entry(loopi - 1, res_line.zimmer_wunsch, ";")

                    if substring(s, 0, 5) == "ChAge":
                        cl_list.age2 = substring(s, 5)

            if re.match(".*\$CODE\$.*",res_line.zimmer_wunsch):
                s = substring(res_line.zimmer_wunsch, (1 + get_index(res_line.zimmer_wunsch, "$CODE$") + 6) - 1)
                cl_list.ratecode = trim(entry(0, s, ";"))

            if frate == 1:
                cl_list.ex_rate = to_string(frate, "   >>9.99")

            elif frate <= 999:
                cl_list.ex_rate = to_string(frate, " >>9.9999")

            elif frate <= 99999:
                cl_list.ex_rate = to_string(frate, ">>,>>9.99")
            else:
                cl_list.ex_rate = to_string(frate, ">,>>>,>>9")

            reslin_queasy = db_session.query(Reslin_queasy).filter(
                    (func.lower(Reslin_queasy.key) == "arrangement") &  (Reslin_queasy.resnr == res_line.resnr) &  (Reslin_queasy.reslinnr == res_line.reslinnr) &  (Reslin_queasy.curr_date >= Reslin_queasy.date1) &  (Reslin_queasy.curr_date <= Reslin_queasy.date2)).first()

            if reslin_queasy:
                cl_list.fix_rate = "F"


            tot_rate = tot_rate + cl_list.zipreis
            tot_lrate = tot_lrate + cl_list.localrate

            if not res_line.adrflag:
                tot_pax = tot_pax + cl_list.pax
            else:
                ltot_pax = ltot_pax + cl_list.pax
            tot_com = tot_com + cl_list.com
            tot_adult = tot_adult + cl_list.adult
            tot_ch1 = tot_ch1 + cl_list.ch1
            tot_ch2 = tot_ch2 + cl_list.ch2
            tot_comch = tot_comch + cl_list.comch
            cl_list.lodging = cl_list.zipreis

            if cl_list.lodging != 0:
                prcode = 0
                contcode = ""

                rguest = db_session.query(Rguest).filter(
                        (Rguest.gastnr == res_line.gastnr)).first()

                if res_line.reserve_int != 0:

                    guest_pr = db_session.query(Guest_pr).filter(
                            (Guest_pr.gastnr == rguest.gastnr)).first()

                if guest_pr:
                    contcode = guest_pr.CODE
                    ct = res_line.zimmer_wunsch

                    if re.match(".*\$CODE\$.*",ct):
                        ct = substring(ct,0 + get_index(ct, "$CODE$") + 6)
                        contcode = substring(ct, 0,1 + get_index(ct, ";") - 1)

                    if new_contrate:
                        prcode = get_output(ratecode_seek(res_line.resnr, res_line.reslinnr, contcode, curr_date))
                    else:

                        pricecod = db_session.query(Pricecod).filter(
                                (func.lower(Pricecod.code) == (contcode).lower()) &  (Pricecod.marknr == res_line.reserve_int) &  (Pricecod.argtnr == arrangement.argtnr) &  (Pricecod.zikatnr == curr_zikatnr) &  (Pricecod.curr_date >= Pricecod.startperiode) &  (Pricecod.curr_date <= Pricecod.endperiode)).first()

                        if pricecod:
                            prcode = pricecod._recid
                rm_rate = res_line.zipreis

                for argt_line in db_session.query(Argt_line).filter(
                        (Argt_line.argtnr == arrangement.argtnr) &  (not Argt_line.kind2)).all():

                    artikel = db_session.query(Artikel).filter(
                            (Artikel.artnr == argt_line.argt_artnr) &  (Artikel.departement == argt_line.departement)).first()

                    if not artikel:
                        take_it = False
                    else:
                        take_it, f_betrag, argt_betrag, qty = get_argtline_rate(contcode, argt_line._recid)

                    if take_it:

                        s_list = query(s_list_list, filters=(lambda s_list :s_list.artnr == argt_line.argt_artnr and s_list.dept == argt_line.departement and s_list.curr == waehrung.wabkurz), first=True)

                        if not s_list:
                            s_list = S_list()
                            s_list_list.append(s_list)

                            s_list.artnr = argt_line.argt_artnr
                            s_list.dept = argt_line.departement
                            s_list.bezeich = artikel.bezeich
                            s_list.curr = waehrung.wabkurz


                        s_list.f_betrag = s_list.f_betrag + f_betrag
                        s_list.l_betrag = s_list.l_betrag + argt_betrag * frate
                        s_list.anzahl = s_list.anzahl + qty


                        sum_list.t_rev = sum_list.t_rev + argt_betrag * frate

                        if artikel.zwkum == bfast_art and (artikel.umsatzart == 3 or artikel.umsatzart >= 5):
                            sum_list.bfast = sum_list.bfast + argt_betrag * frate
                            cl_list.bfast = cl_list.bfast + argt_betrag

                            if res_line.adrflag:
                                ltot_bfast = ltot_bfast + argt_betrag
                            else:
                                tot_bfast = tot_bfast + argt_betrag
                            cl_list.lodging = cl_list.lodging - argt_betrag

                        elif artikel.zwkum == lunch_art and (artikel.umsatzart == 3 or artikel.umsatzart >= 5):
                            sum_list.lunch = sum_list.lunch + argt_betrag * frate
                            cl_list.lunch = cl_list.lunch + argt_betrag

                            if res_line.adrflag:
                                ltot_lunch = ltot_lunch + argt_betrag
                            else:
                                tot_lunch = tot_lunch + argt_betrag
                            cl_list.lodging = cl_list.lodging - argt_betrag

                        elif artikel.zwkum == dinner_art and (artikel.umsatzart == 3 or artikel.umsatzart >= 5):
                            sum_list.dinner = sum_list.dinner + argt_betrag * frate
                            cl_list.dinner = cl_list.dinner + argt_betrag

                            if res_line.adrflag:
                                ltot_dinner = ltot_dinner + argt_betrag
                            else:
                                tot_dinner = tot_dinner + argt_betrag
                            cl_list.lodging = cl_list.lodging - argt_betrag

                        elif artikel.zwkum == lundin_art and (artikel.umsatzart == 3 or artikel.umsatzart >= 5):
                            sum_list.lunch = sum_list.lunch + argt_betrag * frate
                            cl_list.lunch = cl_list.lunch + argt_betrag

                            if res_line.adrflag:
                                ltot_lunch = ltot_lunch + argt_betrag
                            else:
                                tot_lunch = tot_lunch + argt_betrag
                            cl_list.lodging = cl_list.lodging - argt_betrag
                        else:
                            sum_list.misc = sum_list.misc + argt_betrag * frate
                            cl_list.misc = cl_list.misc + argt_betrag

                            if res_line.adrflag:
                                ltot_misc = ltot_misc + argt_betrag
                            else:
                                tot_misc = tot_misc + argt_betrag
                            cl_list.lodging = cl_list.lodging - argt_betrag

            if res_line.adrflag:
                ltot_lodging = ltot_lodging + cl_list.lodging
            else:
                tot_lodging = tot_lodging + cl_list.lodging
            lodge_betrag = cl_list.lodging * frate

            if foreign_rate and price_decimal == 0 and not res_line.adrflag:

                htparam = db_session.query(Htparam).filter(
                        (Htparam.paramnr == 145)).first()

                if htparam.finteger != 0:
                    n = 1
                    for i in range(1,finteger + 1) :
                        n = n * 10
                    lodge_betrag = round(lodge_betrag / n, 0) * n

            artikel1 = db_session.query(Artikel1).filter(
                    (Artikel1.artnr == arrangement.artnr_logis) &  (Artikel1.departement == 0)).first()

            s_list = query(s_list_list, filters=(lambda s_list :s_list.artnr == artikel1.artnr and s_list.dept == artikel1.departement and s_list.curr == waehrung1.wabkurz), first=True)

            if not s_list:
                s_list = S_list()
                s_list_list.append(s_list)

                s_list.artnr = artikel1.artnr
                s_list.dept = artikel1.departement
                s_list.bezeich = artikel1.bezeich
                s_list.curr = waehrung1.wabkurz


            s_list.f_betrag = s_list.f_betrag + lodge_betrag / frate
            s_list.l_betrag = s_list.l_betrag + lodge_betrag
            s_list.anzahl = s_list.anzahl + 1


            sum_list.lodging = sum_list.lodging + lodge_betrag
            sum_list.t_rev = sum_list.t_rev + lodge_betrag

            for fixleist in db_session.query(Fixleist).filter(
                    (Fixleist.resnr == res_line.resnr) &  (Fixleist.reslinnr == res_line.reslinnr)).all():
                post_it = check_fixleist_posted(fixleist.artnr, fixleist.departement, fixleist.sequenz, fixleist.dekade, fixleist.lfakt)

                if post_it:
                    fcost = fixleist.betrag * fixleist.number
                    cl_list.t_rev = cl_list.t_rev + fcost
                    sum_list.t_rev = sum_list.t_rev + fcost * frate

                    if res_line.adrflag:
                        ltot_rate = ltot_rate + fcost
                    else:
                        tot_rate = tot_rate + fcost

                    artikel = db_session.query(Artikel).filter(
                            (Artikel.artnr == fixleist.artnr) &  (Artikel.departement == fixleist.departement)).first()

                    s_list = query(s_list_list, filters=(lambda s_list :s_list.artnr == artikel.artnr and s_list.dept == artikel.departement and s_list.curr == waehrung1.wabkurz), first=True)

                    if not s_list:
                        s_list = S_list()
                        s_list_list.append(s_list)

                        s_list.artnr = artikel.artnr
                        s_list.dept = artikel.departement
                        s_list.bezeich = artikel.bezeich
                        s_list.curr = waehrung1.wabkurz

                    if (artikel.zwkum == bfast_art and artikel.departement == fb_dept):
                        s_list.f_betrag = s_list.f_betrag + fcost
                        s_list.l_betrag = s_list.l_betrag + fcost * frate
                        s_list.anzahl = s_list.anzahl + fixleist.number
                        cl_list.bfast = cl_list.bfast + fcost
                        sum_list.bfast = sum_list.bfast + fcost * frate

                        if res_line.adrflag:
                            ltot_bfast = ltot_bfast + fcost * frate
                        else:
                            tot_bfast = tot_bfast + fcost

                    elif (artikel.zwkum == lunch_art and artikel.departement == fb_dept):
                        s_list.f_betrag = s_list.f_betrag + fcost
                        s_list.l_betrag = s_list.l_betrag + fcost * frate
                        s_list.anzahl = s_list.anzahl + fixleist.number
                        cl_list.lunch = cl_list.lunch + fcost
                        sum_list.lunch = sum_list.lunch + fcost * frate

                        if res_line.adrflag:
                            ltot_lunch = ltot_lunch + fcost * frate
                        else:
                            tot_lunch = tot_lunch + fcost

                    elif (artikel.zwkum == dinner_art and artikel.departement == fb_dept):
                        s_list.f_betrag = s_list.f_betrag + fcost
                        s_list.l_betrag = s_list.l_betrag + fcost * frate
                        s_list.anzahl = s_list.anzahl + fixleist.number
                        cl_list.dinner = cl_list.dinner + fcost
                        sum_list.dinner = sum_list.dinner + fcost * frate

                        if res_line.adrflag:
                            ltot_dinner = ltot_dinner + fcost * frate
                        else:
                            tot_dinner = tot_dinner + fcost
                    else:
                        s_list.f_betrag = s_list.f_betrag + fcost
                        s_list.l_betrag = s_list.l_betrag + fcost * frate
                        s_list.anzahl = s_list.anzahl + fixleist.number
                        cl_list.fixcost = cl_list.fixcost + fcost
                        sum_list.fixcost = sum_list.fixcost + fcost * frate

                        if res_line.adrflag:
                            ltot_fix = ltot_fix + fcost
                        else:
                            tot_fix = tot_fix + fcost

            if curr_zinr != res_line.zinr or curr_resnr != res_line.resnr:

                if res_line.adrflag:
                    ltot_rm = ltot_rm + 1
                else:
                    tot_rm = tot_rm + 1
            curr_zinr = res_line.zinr
            curr_resnr = res_line.resnr

        if exc_taxserv:

            for s_list in query(s_list_list):
                s_list.f_betrag = round((s_list.f_betrag / (1 + vat + service)) , price_decimal)
                s_list.l_betrag = round((s_list.l_betrag / (1 + vat + service)) , price_decimal)

            for sum_list in query(sum_list_list):
                sum_list.lodging = round((sum_list.lodging / (1 + vat + service)) , price_decimal)
                sum_list.bfast = round((sum_list.bfast / (1 + vat + service)) , price_decimal)
                sum_list.lunch = round((sum_list.lunch / (1 + vat + service)) , price_decimal)
                sum_list.dinner = round((sum_list.dinner / (1 + vat + service)) , price_decimal)
                sum_list.misc = round((sum_list.misc / (1 + vat + service)) , price_decimal)
                sum_list.fixcost = round((sum_list.fixcost / (1 + vat + service)) , price_decimal)
                sum_list.t_rev = round((sum_list.t_rev / (1 + vat + service)) , price_decimal)


        cl_list = Cl_list()
        cl_list_list.append(cl_list)

        cl_list.flag = "*"
        cl_list.zinr = " "
        curr_code = ""
        curr_rate = 0
        curr_local = 0
        curr_lodge = 0
        curr_bfast = 0
        curr_lunch = 0
        curr_dinner = 0
        curr_misc = 0
        curr_fcost = 0
        curr_trev = 0
        curr_pax = 0
        curr_com = 0
        curr_rm = 0
        curr_adult = 0
        curr_ch1 = 0
        curr_ch2 = 0
        curr_comch = 0

        for cc_list in query(cc_list_list, filters=(lambda cc_list :cc_list.flag == "")):

            if curr_code != cc_list.currency:

                if curr_code != "":
                    cl_list.zipreis = curr_rate
                    cl_list.localrate = curr_local
                    cl_list.lodging = curr_lodge
                    cl_list.bfast = curr_bfast
                    cl_list.lunch = curr_lunch
                    cl_list.dinner = curr_dinner
                    cl_list.misc = curr_misc
                    cl_list.fixcost = curr_fcost
                    cl_list.t_rev = curr_trev
                    cl_list.pax = curr_pax
                    cl_list.com = curr_com
                    cl_list.zinr = to_string(curr_rm, ">>>9")
                    cl_list.adult = curr_adult
                    cl_list.ch1 = curr_ch1
                    cl_list.ch2 = curr_ch2
                    cl_list.comch = curr_comch

                waehrung = db_session.query(Waehrung).filter(
                        (Waehrung.wabkurz == cc_list.currency)).first()

                if (waehrung.ankauf / waehrung.einheit) != 1:
                    currency_list = Currency_list()
                    currency_list_list.append(currency_list)

                    currency_list.code = cc_list.currency
                cl_list = Cl_list()
                cl_list_list.append(cl_list)

                cl_list.flag = "**"
                cl_list.currency = cc_list.currency
                curr_code = cc_list.currency
                curr_rate = 0
                curr_local = 0
                curr_lodge = 0
                curr_bfast = 0
                curr_lunch = 0
                curr_dinner = 0
                curr_misc = 0
                curr_fcost = 0
                curr_trev = 0
                curr_pax = 0
                curr_com = 0
                curr_rm = 0
                curr_rm = 0
                curr_adult = 0
                curr_ch1 = 0
                curr_ch2 = 0
                curr_comch = 0
            curr_rate = curr_rate + cc_list.zipreis
            curr_local = curr_local + cc_list.localrate
            curr_lodge = curr_lodge + cc_list.lodging
            curr_bfast = curr_bfast + cc_list.bfast
            curr_lunch = curr_lunch + cc_list.lunch
            curr_dinner = curr_dinner + cc_list.dinner
            curr_misc = curr_misc + cc_list.misc
            curr_fcost = curr_fcost + cc_list.fixcost
            curr_trev = curr_trev + cc_list.t_rev
            curr_pax = curr_pax + cc_list.pax
            curr_com = curr_com + cc_list.com
            curr_adult = curr_adult + cc_list.adult
            curr_ch1 = curr_ch1 + cc_list.ch1
            curr_ch2 = curr_ch2 + cc_list.ch2
            curr_comch = curr_comch + cc_list.comch

            if cc_list.rstatus != 13:
                curr_rm = curr_rm + 1
        cl_list.zipreis = curr_rate
        cl_list.localrate = curr_local
        cl_list.lodging = curr_lodge
        cl_list.bfast = curr_bfast
        cl_list.lunch = curr_lunch
        cl_list.dinner = curr_dinner
        cl_list.misc = curr_misc
        cl_list.fixcost = curr_fcost
        cl_list.t_rev = curr_trev
        cl_list.pax = curr_pax
        cl_list.com = curr_com
        cl_list.zinr = to_string(curr_rm, ">>>9")
        cl_list.adult = curr_adult
        cl_list.ch1 = curr_ch1
        cl_list.ch2 = curr_ch2
        cl_list.comch = curr_comch

        for cl_list in query(cl_list_list, filters=(lambda cl_list :cl_list.flag.lower()  != "*")):

            if exc_taxserv:
                cl_list.zipreis = round((cl_list.zipreis / (1 + vat + service)) , price_decimal)
                cl_list.localrate = round((cl_list.localrate / (1 + vat + service)) , price_decimal)
                cl_list.lodging = round((cl_list.lodging / (1 + vat + service)) , price_decimal)
                cl_list.bfast = round((cl_list.bfast / (1 + vat + service)) , price_decimal)
                cl_list.lunch = round((cl_list.lunch / (1 + vat + service)) , price_decimal)
                cl_list.dinner = round((cl_list.dinner / (1 + vat + service)) , price_decimal)
                cl_list.misc = round((cl_list.misc / (1 + vat + service)) , price_decimal)
                cl_list.fixcost = round((cl_list.fixcost / (1 + vat + service)) , price_decimal)
                cl_list.t_rev = round((cl_list.t_rev / (1 + vat + service)) , price_decimal)


            cl_list.c_zipreis = to_string(cl_list.zipreis, ">>>,>>>,>>>,>>9.99")
            cl_list.c_localrate = to_string(cl_list.localrate, ">>>,>>>,>>>,>>9.99")

            if cl_list.lodging < 0:
                cl_list.c_lodging = to_string(cl_list.lodging, "->>,>>>,>>>,>>9.99")
            else:
                cl_list.c_lodging = to_string(cl_list.lodging, ">>>,>>>,>>>,>>9.99")
            cl_list.c_bfast = to_string(cl_list.bfast, ">>,>>>,>>>,>>9.99")
            cl_list.c_lunch = to_string(cl_list.lunch, ">>,>>>,>>>,>>9.99")
            cl_list.c_dinner = to_string(cl_list.dinner, ">>,>>>,>>>,>>9.99")
            cl_list.c_misc = to_string(cl_list.misc, ">>,>>>,>>>,>>9.99")
            cl_list.c_fixcost = to_string(cl_list.fixcost, "->>>,>>>,>>9.99")
            cl_list.ct_rev = to_string(cl_list.t_rev, ">>>,>>>,>>>,>>9.99")
        total_rev = tot_rate

    def check_fixleist_posted(artnr:int, dept:int, fakt_modus:int, intervall:int, lfakt:date):

        nonlocal msg_str, msg_warning, cl_list_list, currency_list_list, sum_list_list, s_list_list, exchg_rate, frate, post_it, total_rev, rm_rate, lvcarea, waehrung, guest, artikel, htparam, zimmer, res_line, arrangement, reservation, bill, segment, reslin_queasy, guest_pr, pricecod, argt_line, fixleist
        nonlocal waehrung1, cc_list, member1, rguest, artikel1, argtline


        nonlocal sum_list, currency_list, cl_list, s_list, waehrung1, cc_list, member1, rguest, artikel1, argtline
        nonlocal sum_list_list, currency_list_list, cl_list_list, s_list_list

        post_it = False
        delta:int = 0
        start_date:date = None

        def generate_inner_output():
            return post_it

        if fakt_modus == 1:
            post_it = True

        elif fakt_modus == 2:

            if res_line.ankunft == curr_date:
                post_it = True

        elif fakt_modus == 3:

            if (res_line.ankunft + 1) == curr_date:
                post_it = True

        elif fakt_modus == 4:

            if get_day(curr_date) == 1:
                post_it = True

        elif fakt_modus == 5:

            if get_day(curr_date + 1) == 1:
                post_it = True

        elif fakt_modus == 6:

            if lfakt == None:
                delta = 0
            else:
                delta = lfakt - res_line.ankunft

                if delta < 0:
                    delta = 0
            start_date = res_line.ankunft + delta

            if (res_line.abreise - start_date) < intervall:
                start_date = res_line.ankunft

            if curr_date <= (start_date + (intervall - 1)):
                post_it = True

            if curr_date < start_date:
                post_it = False


        return generate_inner_output()

    def get_argtline_rate(contcode:str, argt_recid:int):

        nonlocal msg_str, msg_warning, cl_list_list, currency_list_list, sum_list_list, s_list_list, exchg_rate, frate, post_it, total_rev, rm_rate, lvcarea, waehrung, guest, artikel, htparam, zimmer, res_line, arrangement, reservation, bill, segment, reslin_queasy, guest_pr, pricecod, argt_line, fixleist
        nonlocal waehrung1, cc_list, member1, rguest, artikel1, argtline


        nonlocal sum_list, currency_list, cl_list, s_list, waehrung1, cc_list, member1, rguest, artikel1, argtline
        nonlocal sum_list_list, currency_list_list, cl_list_list, s_list_list

        add_it = False
        f_betrag = 0
        argt_betrag = 0
        qty = 0
        curr_zikatnr:int = 0

        def generate_inner_output():
            return add_it, f_betrag, argt_betrag, qty
        Argtline = Argt_line

        if res_line.l_zuordnung[0] != 0:
            curr_zikatnr = res_line.l_zuordnung[0]
        else:
            curr_zikatnr = res_line.zikatnr

        argtline = db_session.query(Argtline).filter(
                (Argtline._recid == argt_recid)).first()

        if argt_line.vt_percnt == 0:

            if argt_line.betriebsnr == 0:
                qty = res_line.erwachs
            else:
                qty = argt_line.betriebsnr

        elif argt_line.vt_percnt == 1:
            qty = res_line.kind1

        elif argt_line.vt_percnt == 2:
            qty = res_line.kind2

        if qty > 0:

            if argtline.fakt_modus == 1:
                add_it = True

            elif argtline.fakt_modus == 2:

                if res_line.ankunft == curr_date:
                    add_it = True

            elif argtline.fakt_modus == 3:

                if (res_line.ankunft + 1) == curr_date:
                    add_it = True

            elif argtline.fakt_modus == 4 and get_day(curr_date) == 1:
                add_it = True

            elif argtline.fakt_modus == 5 and get_day(curr_date + 1) == 1:
                add_it = True

            elif argtline.fakt_modus == 6:

                if (res_line.ankunft + (argtline.intervall - 1)) >= curr_date:
                    add_it = True

        if add_it:

            reslin_queasy = db_session.query(Reslin_queasy).filter(
                    (func.lower(Reslin_queasy.key) == "fargt_line") &  (Reslin_queasy.char1 == "") &  (Reslin_queasy.resnr == res_line.resnr) &  (Reslin_queasy.reslinnr == res_line.reslinnr) &  (Reslin_queasy.number1 == argtline.departement) &  (Reslin_queasy.number2 == argtline.argtnr) &  (Reslin_queasy.number3 == argtline.argt_artnr) &  (Reslin_queasy.curr_date >= Reslin_queasy.date1) &  (Reslin_queasy.curr_date <= Reslin_queasy.date2)).first()

            if reslin_queasy:

                if reslin_queasy.char2.lower()  != "" and reslin_queasy.char2.lower()  != "0":
                    argt_betrag = (res_line.zipreis * to_int(reslin_queasy.char2) / 100) * qty
                else:
                    argt_betrag = reslin_queasy.deci1 * qty
                f_betrag = argt_betrag

                waehrung = db_session.query(Waehrung).filter(
                        (Waehrung._recid == waehrung1._recid)).first()

                if argt_betrag == 0:
                    add_it = False

                return generate_inner_output()

            if contcode != "":

                reslin_queasy = db_session.query(Reslin_queasy).filter(
                        (func.lower(Reslin_queasy.key) == "argt_line") &  (func.lower(Reslin_queasy.char1) == (contcode).lower()) &  (Reslin_queasy.number1 == res_line.reserve_int) &  (Reslin_queasy.number2 == arrangement.argtnr) &  (Reslin_queasy.number3 == argtline.argt_artnr) &  (Reslin_queasy.resnr == argtline.departement) &  (Reslin_queasy.reslinnr == curr_zikatnr) &  (Reslin_queasy.curr_date >= Reslin_queasy.date1) &  (Reslin_queasy.curr_date <= Reslin_queasy.date2)).first()

                if reslin_queasy:
                    argt_betrag = reslin_queasy.deci1 * qty
                    f_betrag = argt_betrag

                    waehrung = db_session.query(Waehrung).filter(
                            (Waehrung._recid == waehrung1._recid)).first()

                    if argt_betrag == 0:
                        add_it = False

                    return generate_inner_output()
            argt_betrag = argt_line.betrag

            arrangement = db_session.query(Arrangement).filter(
                    (Arrangement.argtnr == argt_line.argtnr)).first()

            waehrung = db_session.query(Waehrung).filter(
                    (Waehrungsnr == arrangement.betriebsnr)).first()
            f_betrag = argt_betrag * qty

            if res_line.betriebsnr != arrangement.betriebsnr:
                argt_betrag = argt_betrag * (waehrung.ankauf / waehrung.einheit) / frate

            if argt_betrag > 0:
                argt_betrag = argt_betrag * qty
            else:
                argt_betrag = (rm_rate * (- argt_betrag / 100)) * qty

            if argt_betrag == 0:
                add_it = False


        return generate_inner_output()

    sum_list = Sum_list()
    sum_list_list.append(sum_list)

    create_billbalance()

    return generate_output()