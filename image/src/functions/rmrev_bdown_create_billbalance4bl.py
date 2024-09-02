from functions.additional_functions import *
import decimal
from datetime import date
from functions.calc_servtaxesbl import calc_servtaxesbl
import re
from sqlalchemy import func
from models import Argt_line, Waehrung, Guest, Artikel, Htparam, Res_line, Zimmer, Genstat, Arrangement, Exrate, Reservation, Billjournal, Bill, Zimkateg, Reslin_queasy

def rmrev_bdown_create_billbalance4bl(exc_taxserv:bool, pvilanguage:int, new_contrate:bool, foreign_rate:bool, price_decimal:int, fdate:date, tdate:date, srttype:int):
    cl_list_list = []
    currency_list_list = []
    sum_list_list = []
    s_list_list = []
    argt_list_list = []
    exchg_rate:decimal = 1
    frate:decimal = 0
    post_it:bool = False
    total_rev:decimal = 0
    lvcarea:str = "rmrev_bdown"
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
    argt_line = waehrung = guest = artikel = htparam = res_line = zimmer = genstat = arrangement = exrate = reservation = billjournal = bill = zimkateg = reslin_queasy = None

    sum_list = currency_list = cl_list = s_list = argt_list = t_argt_line = waehrung1 = cc_list = member1 = rguest = artikel1 = argtline = argtline1 = None

    sum_list_list, Sum_list = create_model("Sum_list", {"bezeich":str, "pax":int, "adult":int, "ch1":int, "ch2":int, "comch":int, "com":int, "lodging":decimal, "bfast":decimal, "lunch":decimal, "dinner":decimal, "misc":decimal, "fixcost":decimal, "t_rev":decimal})
    currency_list_list, Currency_list = create_model("Currency_list", {"code":str})
    cl_list_list, Cl_list = create_model("Cl_list", {"zipreis":decimal, "localrate":decimal, "lodging":decimal, "bfast":decimal, "lunch":decimal, "dinner":decimal, "misc":decimal, "fixcost":decimal, "t_rev":decimal, "c_zipreis":str, "c_localrate":str, "c_lodging":str, "c_bfast":str, "c_lunch":str, "c_dinner":str, "c_misc":str, "c_fixcost":str, "ct_rev":str, "res_recid":int, "sleeping":bool, "row_disp":int, "flag":str, "zinr":str, "rstatus":int, "argt":str, "currency":str, "ratecode":str, "pax":int, "com":int, "ankunft":date, "abreise":date, "rechnr":int, "name":str, "ex_rate":str, "fix_rate":str, "adult":int, "ch1":int, "ch2":int, "comch":int, "age1":int, "age2":str, "rmtype":str, "resnr":int, "resname":str}, {"sleeping": True})
    s_list_list, S_list = create_model("S_list", {"artnr":int, "dept":int, "bezeich":str, "curr":str, "anzahl":int, "betrag":decimal, "l_betrag":decimal, "f_betrag":decimal})
    argt_list_list, Argt_list = create_model("Argt_list", {"argtnr":int, "argtcode":str, "bezeich":str, "room":int, "pax":int, "qty":int, "bfast":decimal})
    t_argt_line_list, T_argt_line = create_model_like(Argt_line)

    Waehrung1 = Waehrung
    Cc_list = Cl_list
    cc_list_list = cl_list_list

    Member1 = Guest
    Rguest = Guest
    Artikel1 = Artikel
    Argtline = Argt_line
    Argtline1 = Argt_line

    db_session = local_storage.db_session

    def generate_output():
        nonlocal cl_list_list, currency_list_list, sum_list_list, s_list_list, argt_list_list, exchg_rate, frate, post_it, total_rev, lvcarea, curr_code, curr_rate, curr_local, curr_bfast, curr_lodge, curr_lunch, curr_dinner, curr_misc, curr_fcost, curr_trev, curr_pax, curr_com, curr_rm, curr_adult, curr_ch1, curr_ch2, curr_comch, argt_line, waehrung, guest, artikel, htparam, res_line, zimmer, genstat, arrangement, exrate, reservation, billjournal, bill, zimkateg, reslin_queasy
        nonlocal waehrung1, cc_list, member1, rguest, artikel1, argtline, argtline1


        nonlocal sum_list, currency_list, cl_list, s_list, argt_list, t_argt_line, waehrung1, cc_list, member1, rguest, artikel1, argtline, argtline1
        nonlocal sum_list_list, currency_list_list, cl_list_list, s_list_list, argt_list_list, t_argt_line_list
        return {"cl-list": cl_list_list, "currency-list": currency_list_list, "sum-list": sum_list_list, "s-list": s_list_list, "argt-list": argt_list_list}

    def create_billbalance1():

        nonlocal cl_list_list, currency_list_list, sum_list_list, s_list_list, argt_list_list, exchg_rate, frate, post_it, total_rev, lvcarea, curr_code, curr_rate, curr_local, curr_bfast, curr_lodge, curr_lunch, curr_dinner, curr_misc, curr_fcost, curr_trev, curr_pax, curr_com, curr_rm, curr_adult, curr_ch1, curr_ch2, curr_comch, argt_line, waehrung, guest, artikel, htparam, res_line, zimmer, genstat, arrangement, exrate, reservation, billjournal, bill, zimkateg, reslin_queasy
        nonlocal waehrung1, cc_list, member1, rguest, artikel1, argtline, argtline1


        nonlocal sum_list, currency_list, cl_list, s_list, argt_list, t_argt_line, waehrung1, cc_list, member1, rguest, artikel1, argtline, argtline1
        nonlocal sum_list_list, currency_list_list, cl_list_list, s_list_list, argt_list_list, t_argt_line_list

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
        vat1:decimal = 0
        service1:decimal = 0
        serv1:decimal = 0
        serv2:decimal = 0
        vat2:decimal = 0
        vat3:decimal = 0
        vat4:decimal = 0
        fact:decimal = 0
        fact1:decimal = 0
        fact2:decimal = 0
        cr_code:str = ""
        loopi:int = 0
        str1:str = ""
        curr_zikatnr:int = 0
        bill_rechnr:int = 0
        bill_master:int = 0
        serv_1:decimal = 0
        vat_1:decimal = 0
        vat_2:decimal = 0
        fact_1:decimal = 0
        serv_2:decimal = 0
        vat_3:decimal = 0
        vat_4:decimal = 0
        fact_2:decimal = 0
        bill_flag1:str = ""
        bill_flag2:str = ""
        deposit_art:int = 0
        i:int = 0
        n:int = 0
        j:int = 0
        m:int = 0
        Member1 = Guest
        Rguest = Guest
        Artikel1 = Artikel

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 125)).first()
        bfast_art = finteger

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 126)).first()
        fb_dept = finteger

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 227)).first()
        lunch_art = finteger

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 228)).first()
        dinner_art = finteger

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 229)).first()
        lundin_art = finteger

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 120)).first()
        deposit_art = finteger

        artikel = db_session.query(Artikel).filter(
                (Artikel.zwkum == bfast_art) &  (Artikel.departement == fb_dept)).first()

        if not artikel and bfast_art != 0:

            return

        artikel = db_session.query(Artikel).filter(
                (Artikel.zwkum == lunch_art) &  (Artikel.departement == fb_dept)).first()

        if not artikel and lunch_art != 0:

            return

        artikel = db_session.query(Artikel).filter(
                (Artikel.zwkum == dinner_art) &  (Artikel.departement == fb_dept)).first()

        if not artikel and dinner_art != 0:

            return

        artikel = db_session.query(Artikel).filter(
                (Artikel.zwkum == lundin_art) &  (Artikel.departement == fb_dept)).first()

        if not artikel and lundin_art != 0:

            return
        s_list_list.clear()
        cl_list_list.clear()
        currency_list_list.clear()
        sum_list_list.clear()
        sum_list = Sum_list()
        sum_list_list.append(sum_list)

        r_qty = 0
        lodge_betrag = 0

        if srttype == 2:

            genstat_obj_list = []
            for genstat, res_line, zimmer in db_session.query(Genstat, Res_line, Zimmer).join(Res_line,(Res_line.resnr == Genstat.resnr) &  (Res_line.reslinnr == Genstat.res_int[0]) &  (Res_line.l_zuordnung[2] == 0)).join(Zimmer,(Zimmer.zinr == Genstat.zinr)).filter(
                    (Genstat.zinr != "") &  (Genstat.datum >= fdate) &  (Genstat.datum <= tdate) &  (Genstat.res_logic[1])).all():
                if genstat._recid in genstat_obj_list:
                    continue
                else:
                    genstat_obj_list.append(genstat._recid)


                serv1 = 0
                vat1 = 0
                vat2 = 0
                fact1 = 0

                arrangement = db_session.query(Arrangement).filter(
                        (Arrangement == genstat.argt)).first()

                artikel = db_session.query(Artikel).filter(
                        (Artikel.artnr == arrangement.argt_artikelnr) &  (Artikel.departement == 0)).first()
                serv1, vat1, vat2, fact1 = get_output(calc_servtaxesbl(1, artikel.artnr, artikel.departement, genstat.datum))

                waehrung1 = db_session.query(Waehrung1).filter(
                        (Waehrung1.waehrungsnr == res_line.betriebsnr)).first()

                exrate = db_session.query(Exrate).filter(
                        (Exrate.datum >= fdate) &  (Exrate.datum <= tdate) &  (Exrate.artnr == waehrung1.waehrungsnr)).first()
                exchg_rate = exrate.betrag

                if res_line.reserve_dec != 0:
                    frate = res_line.reserve_dec
                else:
                    frate = exchg_rate

                if genstat.zipreis != 0:
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

                for billjournal in db_session.query(Billjournal).filter(
                        (Billjournal.bill_datum == genstat.datum) &  (Billjournal.zinr == genstat.zinr)).all():
                    bill_flag1 = ""

                    bill = db_session.query(Bill).filter(
                            (Bill.resnr == genstat.resnr) &  (Bill.reslinnr == 0)).first()

                    if bill:
                        bill_master = bill.rechnr
                        bill_flag1 = "Master Bill"

                    if bill_flag1.lower()  == "Master Bill":
                        break

                bill = db_session.query(Bill).filter(
                        (Bill.resnr == genstat.resnr) &  (Bill.reslinnr == genstat.res_int[0])).first()

                if bill:
                    bill_rechnr = bill.rechnr
                    bill_flag2 = "Guest Bill"
                sum_list.pax = sum_list.pax + genstat.erwachs + genstat.kind1 + genstat.kind2
                sum_list.adult = sum_list.adult + genstat.erwachs
                sum_list.com = sum_list.com + genstat.gratis + genstat.kind3


                cl_list = Cl_list()
                cl_list_list.append(cl_list)

                cl_list.res_recid = res_line._recid
                cl_list.zinr = genstat.zinr
                cl_list.rstatus = genstat.resstatus
                cl_list.sleeping = zimmer.sleeping
                cl_list.argt = genstat.argt
                cl_list.name = res_line.name + "-"
                cl_list.com = genstat.gratis
                cl_list.ankunft = res_line.ankunft
                cl_list.abreise = res_line.abreise
                cl_list.resnr = res_line.resnr
                cl_list.resname = res_line.resname

                if not exc_taxserv:
                    cl_list.zipreis = genstat.zipreis
                    cl_list.localrate = genstat.rateLocal
                    cl_list.t_rev = genstat.zipreis
                    cl_list.lodging = genstat.logis * (1 + vat1 + vat2 + serv1)
                    cl_list.fixcost = genstat.res_deci[5] * (1 + vat1 + vat2 + serv1)


                else:
                    cl_list.zipreis = round((genstat.zipreis / (1 + vat1 + vat2 + serv1)) , price_decimal)
                    cl_list.localrate = round((genstat.rateLocal / (1 + vat1 + vat2 + serv1)) , price_decimal)
                    cl_list.t_rev = round((genstat.zipreis / (1 + vat1 + vat2 + serv1)) , price_decimal)
                    cl_list.lodging = round(genstat.logis, price_decimal)
                    cl_list.fixcost = round(genstat.res_deci[5], price_decimal)


                sum_list.lodging = sum_list.lodging + cl_list.lodging
                sum_list.t_rev = sum_list.t_rev + genstat.zipreis
                sum_list.fixcost = sum_list.fixcost + cl_list.fixcost

                if bill_flag1.lower()  == "Master Bill":

                    billjournal = db_session.query(Billjournal).filter(
                            (Billjournal.rechnr == bill_master) &  (Billjournal.bill_datum == genstat.datum)).first()

                    if billjournal:
                        cl_list.rechnr = bill_master

                if bill_flag2.lower()  == "Guest Bill":

                    billjournal = db_session.query(Billjournal).filter(
                            (Billjournal.rechnr == bill_rechnr) &  (Billjournal.bill_datum == genstat.datum)).first()

                    if billjournal:
                        cl_list.rechnr = bill_rechnr

                if genstat.gratis != 0:
                    cl_list.rechnr = 0
                cl_list.adult = genstat.erwachs
                cl_list.ch1 = genstat.kind1
                cl_list.ch2 = genstat.kind2
                cl_list.comch = genstat.kind3

                if cl_list.zipreis == 0 and cl_list.adult == 0:
                    cl_list.pax = cl_list.com + cl_list.comch


                else:
                    cl_list.pax = genstat.erwachs + genstat.kind1 + genstat.kind2 + cl_list.com + cl_list.comch

                zimkateg = db_session.query(Zimkateg).filter(
                        (Zimkateg.zikatnr == genstat.zikatnr)).first()

                if zimkateg:
                    cl_list.rmtype = zimkateg.kurzbez

                if guest:
                    cl_list.name = cl_list.name + guest.name + ", " + guest.vorname1 + "-" + guest.adresse1
                    cl_list.rechnr = bill_rechnr
                    cl_list.currency = waehrung1.wabkurz

                argt_list = query(argt_list_list, filters=(lambda argt_list :argt_list.argtnr == arrangement.argtnr), first=True)

                if not argt_list:
                    argt_list = Argt_list()
                    argt_list_list.append(argt_list)

                    argt_list.argtnr = arrangement.argtnr
                    argt_list.argtcode = arrangement
                    argt_list.bezeich = argt_bez
                    argt_list.room = 1
                    argt_list.pax = genstat.erwachs + genstat.kind1 + genstat.kind2 + cl_list.com + cl_list.comch


                else:
                    argt_list.room = argt_list.room + 1
                    argt_list.pax = argt_list.pax + (genstat.erwachs + genstat.gratis)

                if guest.geburtdatum1 != None and guest.geburtdatum2 != None:

                    if guest.geburtdatum1 < guest.geburtdatum2:
                        cl_list.age1 = get_year(guest.geburtdatum2) - get_year(guest.geburtdatum1)

                if re.match(".*ChAge.*",res_line.zimmer_wunsch):
                    for loopi in range(1,num_entries(res_line.zimmer_wunsch, ";") - 1 + 1) :
                        str1 = entry(loopi - 1, res_line.zimmer_wunsch, ";")

                        if substring(str1, 0, 5) == "ChAge":
                            cl_list.age2 = substring(str1, 5)
                serv2 = 0
                vat3 = 0
                vat4 = 0
                fact2 = 0


                for loopi in range(1,num_entries(genstat.res_char[1], ";") - 1 + 1) :
                    str1 = entry(loopi - 1, genstat.res_char[1], ";")

                    if substring(str1, 0, 6) == "$CODE$":
                        cr_code = substring(str1, 6)

                if genstat.zipreis != 0:

                    argt_line_obj_list = []
                    for argt_line, artikel in db_session.query(Argt_line, Artikel).join(Artikel,(Artikel.artnr == Argt_line.argt_artnr) &  (Artikel.departement == Argt_line.departement)).filter(
                            (Argt_line.argtnr == arrangement.argtnr) &  (not Argt_line.kind2) &  (Argt_line.kind1)).all():
                        if argt_line._recid in argt_line_obj_list:
                            continue
                        else:
                            argt_line_obj_list.append(argt_line._recid)


                        Argtline = Argt_line
                        take_it, f_betrag, argt_betrag, qty = get_argtline_rate(contcode, argt_line._recid)
                        serv2, vat3, vat4, fact2 = get_output(calc_servtaxesbl(1, artikel.artnr, artikel.departement, genstat.datum))
                        vat3 = vat3 + vat4

                        if artikel.zwkum == bfast_art and (artikel.umsatzart == 3 or artikel.umsatzart >= 5):

                            if not exc_taxserv:
                                cl_list.bfast = genstat.res_deci[1] * (1 + vat3 + serv2)
                                sum_list.bfast = sum_list.bfast + cl_list.bfast


                            else:
                                cl_list.bfast = round(genstat.res_deci[1], price_decimal)
                                sum_list.bfast = round(sum_list.bfast + cl_list.bfast, price_decimal)

                        elif artikel.zwkum == lunch_art and (artikel.umsatzart == 3 or artikel.umsatzart >= 5):

                            if not exc_taxserv:
                                cl_list.lunch = genstat.res_deci[2] * (1 + vat3 + serv2)
                                sum_list.lunch = sum_list.lunch + cl_list.lunch


                            else:
                                cl_list.lunch = round(genstat.res_deci[2], price_decimal)
                                sum_list.lunch = round(sum_list.lunch + cl_list.lunch, price_decimal)

                        elif artikel.zwkum == dinner_art and (artikel.umsatzart == 3 or artikel.umsatzart >= 5):

                            if not exc_taxserv:
                                cl_list.dinner = genstat.res_deci[3] * (1 + vat3 + serv2)
                                sum_list.dinner = sum_list.dinner + cl_list.dinner


                            else:
                                cl_list.dinner = round(genstat.res_deci[3], price_decimal)
                                sum_list.dinner = round(sum_list.dinner + cl_list.dinner, price_decimal)

                        elif artikel.zwkum == lundin_art and (artikel.umsatzart == 3 or artikel.umsatzart >= 5):

                            if not exc_taxserv:
                                cl_list.lunch = genstat.res_deci[2] * (1 + vat3 + serv2)
                                sum_list.lunch = sum_list.lunch + cl_list.lunch


                            else:
                                cl_list.lunch = round(genstat.res_deci[2], price_decimal)
                                sum_list.lunch = round(sum_list.lunch + cl_list.lunch, price_decimal)


                        else:

                            if argt_betrag != 0:
                                pass

                    if not exc_taxserv:
                        cl_list.misc = cl_list.localrate - (cl_list.lodging + cl_list.bfast + cl_list.lunch + cl_list.dinner)
                        sum_list.misc = sum_list.misc + cl_list.misc


                    else:
                        cl_list.misc = genstat.res_deci[4]
                        sum_list.misc = sum_list.misc + cl_list.misc

                    if cl_list.misc < 0 and cl_list.misc > -1:
                        cl_list.misc = 0.00

                htparam = db_session.query(Htparam).filter(
                        (Htparam.paramnr == 127)).first()

                if htparam.flogical and not exc_taxserv:
                    cl_list.zipreis = round(cl_list.zipreis, price_decimal)
                    cl_list.lodging = round(cl_list.lodging, price_decimal)
                    cl_list.bfast = round(cl_list.bfast, price_decimal)
                    cl_list.lunch = round(cl_list.lunch, price_decimal)
                    cl_list.dinner = round(cl_list.dinner, price_decimal)
                    cl_list.misc = round(cl_list.misc , price_decimal)
                    cl_list.fixcost = round(cl_list.fixcost, price_decimal)
                    cl_list.localrate = round(cl_list.localrate, price_decimal)
                    cl_list.t_rev = round(cl_list.t_rev, price_decimal)

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
                        (func.lower(Reslin_queasy.key) == "arrangement") &  (Reslin_queasy.resnr == res_line.resnr) &  (Reslin_queasy.reslinnr == res_line.reslinnr) &  (Reslin_queasy.tdate >= Reslin_queasy.date1) &  (Reslin_queasy.fdate <= Reslin_queasy.date2)).first()

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

                for argt_line in db_session.query(Argt_line).filter(
                        (Argt_line.argtnr == arrangement.argtnr) &  (not Argt_line.kind2) &  (Argt_line.kind1)).all():

                    t_argt_line = query(t_argt_line_list, filters=(lambda t_argt_line :t_argt_line.argt_artnr == argt_line.argt_artnr and t_argt_line.argtnr == arrangement.argtnr and t_argt_line.departement == argt_line.departement), first=True)

                    if not t_argt_line:
                        t_argt_line = T_argt_line()
                        t_argt_line_list.append(t_argt_line)

                        buffer_copy(argt_line, t_argt_line)

                if genstat.zipreis != 0:

                    if bill_flag1.lower()  == "Master Bill":

                        billjournal_obj_list = []
                        for billjournal, artikel in db_session.query(Billjournal, Artikel).join(Artikel,(Artikel.artnr == Billjournal.artnr) &  (Artikel.departement == Billjournal.departement) &  (Artikel.artart != 9)).filter(
                                (Billjournal.rechnr == bill_master) &  (Billjournal.bill_datum == genstat.datum) &  (Billjournal.zinr == genstat.zinr) &  (Billjournal.betrag != 0) &  (Billjournal.anzahl != 0) &  (not Billjournal.kassarapport) &  (func.lower(Billjournal.userinit) == "$$")).all():
                            if billjournal._recid in billjournal_obj_list:
                                continue
                            else:
                                billjournal_obj_list.append(billjournal._recid)

                            if billjournal.artnr != deposit_art:

                                s_list = query(s_list_list, filters=(lambda s_list :s_list.artnr == billjournal.artnr and s_list.dept == billjournal.departement and s_list.curr == waehrung1.wabkurz), first=True)

                                if not s_list:
                                    s_list = S_list()
                                    s_list_list.append(s_list)

                                    s_list.artnr = billjournal.artnr
                                    s_list.dept = billjournal.departement
                                    s_list.bezeich = billjournal.bezeich
                                    s_list.curr = waehrung1.wabkurz


                                s_list.f_betrag = s_list.f_betrag + billjournal.fremdwaehrng
                                s_list.l_betrag = s_list.l_betrag + billjournal.betrag


                        bill_master = -1

                    if bill_flag2.lower()  == "Guest Bill":

                        billjournal_obj_list = []
                        for billjournal, artikel in db_session.query(Billjournal, Artikel).join(Artikel,(Artikel.artnr == Billjournal.artnr) &  (Artikel.departement == Billjournal.departement) &  (Artikel.artart != 9)).filter(
                                (Billjournal.rechnr == bill_rechnr) &  (Billjournal.bill_datum == genstat.datum) &  (Billjournal.zinr == genstat.zinr) &  (Billjournal.betrag != 0) &  (Billjournal.anzahl != 0) &  (not Billjournal.kassarapport) &  (func.lower(Billjournal.userinit) == "$$")).all():
                            if billjournal._recid in billjournal_obj_list:
                                continue
                            else:
                                billjournal_obj_list.append(billjournal._recid)

                            if billjournal.artnr != deposit_art:

                                s_list = query(s_list_list, filters=(lambda s_list :s_list.artnr == billjournal.artnr and s_list.dept == billjournal.departement and s_list.curr == waehrung1.wabkurz), first=True)

                                if not s_list:
                                    s_list = S_list()
                                    s_list_list.append(s_list)

                                    s_list.artnr = billjournal.artnr
                                    s_list.dept = billjournal.departement
                                    s_list.bezeich = billjournal.bezeich
                                    s_list.curr = waehrung1.wabkurz


                                s_list.f_betrag = s_list.f_betrag + billjournal.fremdwaehrng
                                s_list.l_betrag = s_list.l_betrag + billjournal.betrag


                        bill_rechnr = -1

                if res_line.adrflag:
                    ltot_lodging = ltot_lodging + cl_list.lodging
                else:
                    tot_lodging = tot_lodging + cl_list.lodging
                lodge_betrag = cl_list.lodging

                if foreign_rate and price_decimal == 0 and not res_line.adrflag:

                    htparam = db_session.query(Htparam).filter(
                            (Htparam.paramnr == 145)).first()

                    if htparam.finteger != 0:
                        n = 1
                        for i in range(1,finteger + 1) :
                            n = n * 10
                        lodge_betrag = round(lodge_betrag / n, 0) * n

                if curr_zinr != res_line.zinr or curr_resnr != res_line.resnr:

                    if res_line.adrflag:
                        ltot_rm = ltot_rm + 1
                    else:
                        tot_rm = tot_rm + 1
                curr_zinr = res_line.zinr
                curr_resnr = res_line.resnr
        else DO:

        genstat_obj_list = []
        for genstat, res_line, zimmer in db_session.query(Genstat, Res_line, Zimmer).join(Res_line,(Res_line.resnr == Genstat.resnr) &  (Res_line.reslinnr == Genstat.res_int[0]) &  (Res_line.l_zuordnung[2] == 0)).join(Zimmer,(Zimmer.zinr == Genstat.zinr)).filter(
                (Genstat.zinr != "") &  (Genstat.datum >= fdate) &  (Genstat.datum <= tdate) &  (Genstat.res_logic[1])).all():
            if genstat._recid in genstat_obj_list:
                continue
            else:
                genstat_obj_list.append(genstat._recid)


            serv1 = 0
            vat1 = 0
            vat2 = 0
            fact1 = 0

            arrangement = db_session.query(Arrangement).filter(
                    (Arrangement == genstat.argt)).first()

            artikel = db_session.query(Artikel).filter(
                    (Artikel.artnr == arrangement.argt_artikelnr) &  (Artikel.departement == 0)).first()
            serv1, vat1, vat2, fact1 = get_output(calc_servtaxesbl(1, artikel.artnr, artikel.departement, genstat.datum))

            waehrung1 = db_session.query(Waehrung1).filter(
                    (Waehrung1.waehrungsnr == res_line.betriebsnr)).first()

            exrate = db_session.query(Exrate).filter(
                    (Exrate.datum >= fdate) &  (Exrate.datum <= tdate) &  (Exrate.artnr == waehrung1.waehrungsnr)).first()
            exchg_rate = exrate.betrag

            if res_line.reserve_dec != 0:
                frate = res_line.reserve_dec
            else:
                frate = exchg_rate

            if genstat.zipreis != 0:
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

            for billjournal in db_session.query(Billjournal).filter(
                    (Billjournal.bill_datum == genstat.datum) &  (Billjournal.zinr == genstat.zinr)).all():
                bill_flag1 = ""

                bill = db_session.query(Bill).filter(
                        (Bill.resnr == genstat.resnr) &  (Bill.reslinnr == 0)).first()

                if bill:
                    bill_master = bill.rechnr
                    bill_flag1 = "Master Bill"

                if bill_flag1.lower()  == "Master Bill":
                    break

            bill = db_session.query(Bill).filter(
                    (Bill.resnr == genstat.resnr) &  (Bill.reslinnr == genstat.res_int[0])).first()

            if bill:
                bill_rechnr = bill.rechnr
                bill_flag2 = "Guest Bill"
            sum_list.pax = sum_list.pax + genstat.erwachs + genstat.kind1 + genstat.kind2
            sum_list.adult = sum_list.adult + genstat.erwachs
            sum_list.com = sum_list.com + genstat.gratis + genstat.kind3


            cl_list = Cl_list()
            cl_list_list.append(cl_list)

            cl_list.res_recid = res_line._recid
            cl_list.zinr = genstat.zinr
            cl_list.rstatus = genstat.resstatus
            cl_list.sleeping = zimmer.sleeping
            cl_list.argt = genstat.argt
            cl_list.name = res_line.name + "-"
            cl_list.com = genstat.gratis
            cl_list.ankunft = res_line.ankunft
            cl_list.abreise = res_line.abreise
            cl_list.resnr = res_line.resnr
            cl_list.resname = res_line.resname

            if not exc_taxserv:
                cl_list.zipreis = genstat.zipreis
                cl_list.localrate = genstat.rateLocal
                cl_list.t_rev = genstat.zipreis
                cl_list.lodging = genstat.logis * (1 + vat1 + vat2 + serv1)
                cl_list.fixcost = genstat.res_deci[5] * (1 + vat1 + vat2 + serv1)


            else:
                cl_list.zipreis = round((genstat.zipreis / (1 + vat1 + vat2 + serv1)) , price_decimal)
                cl_list.localrate = round((genstat.rateLocal / (1 + vat1 + vat2 + serv1)) , price_decimal)
                cl_list.t_rev = round((genstat.zipreis / (1 + vat1 + vat2 + serv1)) , price_decimal)
                cl_list.lodging = round(genstat.logis, price_decimal)
                cl_list.fixcost = round(genstat.res_deci[5], price_decimal)


            sum_list.lodging = sum_list.lodging + cl_list.lodging
            sum_list.t_rev = sum_list.t_rev + genstat.zipreis
            sum_list.fixcost = sum_list.fixcost + cl_list.fixcost

            if bill_flag1.lower()  == "Master Bill":

                billjournal = db_session.query(Billjournal).filter(
                        (Billjournal.rechnr == bill_master) &  (Billjournal.bill_datum == genstat.datum)).first()

                if billjournal:
                    cl_list.rechnr = bill_master

            if bill_flag2.lower()  == "Guest Bill":

                billjournal = db_session.query(Billjournal).filter(
                        (Billjournal.rechnr == bill_rechnr) &  (Billjournal.bill_datum == genstat.datum)).first()

                if billjournal:
                    cl_list.rechnr = bill_rechnr

            if genstat.gratis != 0:
                cl_list.rechnr = 0
            cl_list.adult = genstat.erwachs
            cl_list.ch1 = genstat.kind1
            cl_list.ch2 = genstat.kind2
            cl_list.comch = genstat.kind3

            if cl_list.zipreis == 0 and cl_list.adult == 0:
                cl_list.pax = cl_list.com + cl_list.comch


            else:
                cl_list.pax = genstat.erwachs + genstat.kind1 + genstat.kind2 + cl_list.com + cl_list.comch

            zimkateg = db_session.query(Zimkateg).filter(
                    (Zimkateg.zikatnr == genstat.zikatnr)).first()

            if zimkateg:
                cl_list.rmtype = zimkateg.kurzbez

            if guest:
                cl_list.name = cl_list.name + guest.name + ", " + guest.vorname1 + "-" + guest.adresse1
                cl_list.rechnr = bill_rechnr
                cl_list.currency = waehrung1.wabkurz

            argt_list = query(argt_list_list, filters=(lambda argt_list :argt_list.argtnr == arrangement.argtnr), first=True)

            if not argt_list:
                argt_list = Argt_list()
                argt_list_list.append(argt_list)

                argt_list.argtnr = arrangement.argtnr
                argt_list.argtcode = arrangement
                argt_list.bezeich = argt_bez
                argt_list.room = 1
                argt_list.pax = genstat.erwachs + genstat.kind1 + genstat.kind2 + cl_list.com + cl_list.comch


            else:
                argt_list.room = argt_list.room + 1
                argt_list.pax = argt_list.pax + (genstat.erwachs + genstat.gratis)

            if guest.geburtdatum1 != None and guest.geburtdatum2 != None:

                if guest.geburtdatum1 < guest.geburtdatum2:
                    cl_list.age1 = get_year(guest.geburtdatum2) - get_year(guest.geburtdatum1)

            if re.match(".*ChAge.*",res_line.zimmer_wunsch):
                for loopi in range(1,num_entries(res_line.zimmer_wunsch, ";") - 1 + 1) :
                    str1 = entry(loopi - 1, res_line.zimmer_wunsch, ";")

                    if substring(str1, 0, 5) == "ChAge":
                        cl_list.age2 = substring(str1, 5)
            serv2 = 0
            vat3 = 0
            vat4 = 0
            fact2 = 0


            for loopi in range(1,num_entries(genstat.res_char[1], ";") - 1 + 1) :
                str1 = entry(loopi - 1, genstat.res_char[1], ";")

                if substring(str1, 0, 6) == "$CODE$":
                    cr_code = substring(str1, 6)

            if genstat.zipreis != 0:

                argt_line_obj_list = []
                for argt_line, artikel in db_session.query(Argt_line, Artikel).join(Artikel,(Artikel.artnr == Argt_line.argt_artnr) &  (Artikel.departement == Argt_line.departement)).filter(
                        (Argt_line.argtnr == arrangement.argtnr) &  (not Argt_line.kind2) &  (Argt_line.kind1)).all():
                    if argt_line._recid in argt_line_obj_list:
                        continue
                    else:
                        argt_line_obj_list.append(argt_line._recid)


                    Argtline1 = Argt_line
                    take_it, f_betrag, argt_betrag, qty = get_argtline_rate(contcode, argt_line._recid)
                    serv2, vat3, vat4, fact2 = get_output(calc_servtaxesbl(1, artikel.artnr, artikel.departement, genstat.datum))
                    vat3 = vat3 + vat4

                    if artikel.zwkum == bfast_art and (artikel.umsatzart == 3 or artikel.umsatzart >= 5):

                        if not exc_taxserv:
                            cl_list.bfast = genstat.res_deci[1] * (1 + vat3 + serv2)
                            sum_list.bfast = sum_list.bfast + cl_list.bfast


                        else:
                            cl_list.bfast = round(genstat.res_deci[1], price_decimal)
                            sum_list.bfast = round(sum_list.bfast + cl_list.bfast, price_decimal)

                    elif artikel.zwkum == lunch_art and (artikel.umsatzart == 3 or artikel.umsatzart >= 5):

                        if not exc_taxserv:
                            cl_list.lunch = genstat.res_deci[2] * (1 + vat3 + serv2)
                            sum_list.lunch = sum_list.lunch + cl_list.lunch


                        else:
                            cl_list.lunch = round(genstat.res_deci[2], price_decimal)
                            sum_list.lunch = round(sum_list.lunch + cl_list.lunch, price_decimal)

                    elif artikel.zwkum == dinner_art and (artikel.umsatzart == 3 or artikel.umsatzart >= 5):

                        if not exc_taxserv:
                            cl_list.dinner = genstat.res_deci[3] * (1 + vat3 + serv2)
                            sum_list.dinner = sum_list.dinner + cl_list.dinner


                        else:
                            cl_list.dinner = round(genstat.res_deci[3], price_decimal)
                            sum_list.dinner = round(sum_list.dinner + cl_list.dinner, price_decimal)

                    elif artikel.zwkum == lundin_art and (artikel.umsatzart == 3 or artikel.umsatzart >= 5):

                        if not exc_taxserv:
                            cl_list.lunch = genstat.res_deci[2] * (1 + vat3 + serv2)
                            sum_list.lunch = sum_list.lunch + cl_list.lunch


                        else:
                            cl_list.lunch = round(genstat.res_deci[2], price_decimal)
                            sum_list.lunch = round(sum_list.lunch + cl_list.lunch, price_decimal)


                    else:

                        if argt_betrag != 0:
                            pass

                if not exc_taxserv:
                    cl_list.misc = cl_list.localrate - (cl_list.lodging + cl_list.bfast + cl_list.lunch + cl_list.dinner)
                    sum_list.misc = sum_list.misc + cl_list.misc


                else:
                    cl_list.misc = genstat.res_deci[4]
                    sum_list.misc = sum_list.misc + cl_list.misc

                if cl_list.misc < 0 and cl_list.misc > -1:
                    cl_list.misc = 0.00

            htparam = db_session.query(Htparam).filter(
                    (Htparam.paramnr == 127)).first()

            if htparam.flogical and not exc_taxserv:
                cl_list.zipreis = round(cl_list.zipreis, price_decimal)
                cl_list.lodging = round(cl_list.lodging, price_decimal)
                cl_list.bfast = round(cl_list.bfast, price_decimal)
                cl_list.lunch = round(cl_list.lunch, price_decimal)
                cl_list.dinner = round(cl_list.dinner, price_decimal)
                cl_list.misc = round(cl_list.misc , price_decimal)
                cl_list.fixcost = round(cl_list.fixcost, price_decimal)
                cl_list.localrate = round(cl_list.localrate, price_decimal)
                cl_list.t_rev = round(cl_list.t_rev, price_decimal)

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
                    (func.lower(Reslin_queasy.key) == "arrangement") &  (Reslin_queasy.resnr == res_line.resnr) &  (Reslin_queasy.reslinnr == res_line.reslinnr) &  (Reslin_queasy.tdate >= Reslin_queasy.date1) &  (Reslin_queasy.fdate <= Reslin_queasy.date2)).first()

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

            for argt_line in db_session.query(Argt_line).filter(
                    (Argt_line.argtnr == arrangement.argtnr) &  (not Argt_line.kind2) &  (Argt_line.kind1)).all():

                t_argt_line = query(t_argt_line_list, filters=(lambda t_argt_line :t_argt_line.argt_artnr == argt_line.argt_artnr and t_argt_line.argtnr == arrangement.argtnr and t_argt_line.departement == argt_line.departement), first=True)

                if not t_argt_line:
                    t_argt_line = T_argt_line()
                    t_argt_line_list.append(t_argt_line)

                    buffer_copy(argt_line, t_argt_line)

            if genstat.zipreis != 0:

                if bill_flag1.lower()  == "Master Bill":

                    billjournal_obj_list = []
                    for billjournal, artikel in db_session.query(Billjournal, Artikel).join(Artikel,(Artikel.artnr == Billjournal.artnr) &  (Artikel.departement == Billjournal.departement) &  (Artikel.artart != 9)).filter(
                            (Billjournal.rechnr == bill_master) &  (Billjournal.bill_datum == genstat.datum) &  (Billjournal.zinr == genstat.zinr) &  (Billjournal.betrag != 0) &  (Billjournal.anzahl != 0) &  (not Billjournal.kassarapport) &  (func.lower(Billjournal.userinit) == "$$")).all():
                        if billjournal._recid in billjournal_obj_list:
                            continue
                        else:
                            billjournal_obj_list.append(billjournal._recid)

                        if billjournal.artnr != deposit_art:

                            s_list = query(s_list_list, filters=(lambda s_list :s_list.artnr == billjournal.artnr and s_list.dept == billjournal.departement and s_list.curr == waehrung1.wabkurz), first=True)

                            if not s_list:
                                s_list = S_list()
                                s_list_list.append(s_list)

                                s_list.artnr = billjournal.artnr
                                s_list.dept = billjournal.departement
                                s_list.bezeich = billjournal.bezeich
                                s_list.curr = waehrung1.wabkurz


                            s_list.f_betrag = s_list.f_betrag + billjournal.fremdwaehrng
                            s_list.l_betrag = s_list.l_betrag + billjournal.betrag


                    bill_master = -1

                if bill_flag2.lower()  == "Guest Bill":

                    billjournal_obj_list = []
                    for billjournal, artikel in db_session.query(Billjournal, Artikel).join(Artikel,(Artikel.artnr == Billjournal.artnr) &  (Artikel.departement == Billjournal.departement) &  (Artikel.artart != 9)).filter(
                            (Billjournal.rechnr == bill_rechnr) &  (Billjournal.bill_datum == genstat.datum) &  (Billjournal.zinr == genstat.zinr) &  (Billjournal.betrag != 0) &  (Billjournal.anzahl != 0) &  (not Billjournal.kassarapport) &  (func.lower(Billjournal.userinit) == "$$")).all():
                        if billjournal._recid in billjournal_obj_list:
                            continue
                        else:
                            billjournal_obj_list.append(billjournal._recid)

                        if billjournal.artnr != deposit_art:

                            s_list = query(s_list_list, filters=(lambda s_list :s_list.artnr == billjournal.artnr and s_list.dept == billjournal.departement and s_list.curr == waehrung1.wabkurz), first=True)

                            if not s_list:
                                s_list = S_list()
                                s_list_list.append(s_list)

                                s_list.artnr = billjournal.artnr
                                s_list.dept = billjournal.departement
                                s_list.bezeich = billjournal.bezeich
                                s_list.curr = waehrung1.wabkurz


                            s_list.f_betrag = s_list.f_betrag + billjournal.fremdwaehrng
                            s_list.l_betrag = s_list.l_betrag + billjournal.betrag


                    bill_rechnr = -1

            if res_line.adrflag:
                ltot_lodging = ltot_lodging + cl_list.lodging
            else:
                tot_lodging = tot_lodging + cl_list.lodging
            lodge_betrag = cl_list.lodging

            if foreign_rate and price_decimal == 0 and not res_line.adrflag:

                htparam = db_session.query(Htparam).filter(
                        (Htparam.paramnr == 145)).first()

                if htparam.finteger != 0:
                    m = 1
                    for j in range(1,finteger + 1) :
                        m = m * 10
                    lodge_betrag = round(lodge_betrag / n, 0) * n

            if curr_zinr != res_line.zinr or curr_resnr != res_line.resnr:

                if res_line.adrflag:
                    ltot_rm = ltot_rm + 1
                else:
                    tot_rm = tot_rm + 1
            curr_zinr = res_line.zinr
            curr_resnr = res_line.resnr

    def get_argtline_rate(contcode:str, argt_recid:int):

        nonlocal cl_list_list, currency_list_list, sum_list_list, s_list_list, argt_list_list, exchg_rate, frate, post_it, total_rev, lvcarea, curr_code, curr_rate, curr_local, curr_bfast, curr_lodge, curr_lunch, curr_dinner, curr_misc, curr_fcost, curr_trev, curr_pax, curr_com, curr_rm, curr_adult, curr_ch1, curr_ch2, curr_comch, argt_line, waehrung, guest, artikel, htparam, res_line, zimmer, genstat, arrangement, exrate, reservation, billjournal, bill, zimkateg, reslin_queasy
        nonlocal waehrung1, cc_list, member1, rguest, artikel1, argtline, argtline1


        nonlocal sum_list, currency_list, cl_list, s_list, argt_list, t_argt_line, waehrung1, cc_list, member1, rguest, artikel1, argtline, argtline1
        nonlocal sum_list_list, currency_list_list, cl_list_list, s_list_list, argt_list_list, t_argt_line_list

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
                qty = genstat.erwachs
            else:
                qty = argt_line.betriebsnr

        elif argt_line.vt_percnt == 1:
            qty = genstat.kind1

        elif argt_line.vt_percnt == 2:
            qty = genstat.kind2

        if qty > 0:

            if argtline.fakt_modus == 1:
                add_it = True

            elif argtline.fakt_modus == 2:

                if (res_line.ankunft == genstat.datum):
                    add_it = True

            elif argtline.fakt_modus == 3:

                if (res_line.ankunft + 1) == genstat.datum:
                    add_it = True

            elif argtline.fakt_modus == 4 and (get_day(genstat.datum) == 1):
                add_it = True

            elif argtline.fakt_modus == 5 and (get_day(genstat.datum + 1) == 1):
                add_it = True

            elif argtline.fakt_modus == 6:

                if (res_line.ankunft + (argtline.intervall - 1)) >= genstat.datum:
                    add_it = True

        if add_it:

            reslin_queasy = db_session.query(Reslin_queasy).filter(
                    (func.lower(Reslin_queasy.key) == "fargt_line") &  (Reslin_queasy.char1 == "") &  (Reslin_queasy.resnr == res_line.resnr) &  (Reslin_queasy.reslinnr == res_line.reslinnr) &  (Reslin_queasy.number1 == argtline.departement) &  (Reslin_queasy.number2 == argtline.argtnr) &  (Reslin_queasy.number3 == argtline.argt_artnr) &  (Reslin_queasy.tdate >= Reslin_queasy.date1) &  (Reslin_queasy.fdate <= Reslin_queasy.date2)).first()

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
                        (func.lower(Reslin_queasy.key) == "argt_line") &  (func.lower(Reslin_queasy.char1) == (contcode).lower()) &  (Reslin_queasy.number1 == res_line.reserve_int) &  (Reslin_queasy.number2 == arrangement.argtnr) &  (Reslin_queasy.number3 == argtline.argt_artnr) &  (Reslin_queasy.resnr == argtline.departement) &  (Reslin_queasy.reslinnr == curr_zikatnr) &  (Reslin_queasy.tdate >= Reslin_queasy.date1) &  (Reslin_queasy.fdate <= Reslin_queasy.date2)).first()

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
            argt_betrag = argt_betrag * qty

            if argt_betrag == 0:
                add_it = False


        return generate_inner_output()

    def get_genstat_argt_betrag(frate:decimal, argt_betrag:decimal):

        nonlocal cl_list_list, currency_list_list, sum_list_list, s_list_list, argt_list_list, exchg_rate, frate, post_it, total_rev, lvcarea, curr_code, curr_rate, curr_local, curr_bfast, curr_lodge, curr_lunch, curr_dinner, curr_misc, curr_fcost, curr_trev, curr_pax, curr_com, curr_rm, curr_adult, curr_ch1, curr_ch2, curr_comch, argt_line, waehrung, guest, artikel, htparam, res_line, zimmer, genstat, arrangement, exrate, reservation, billjournal, bill, zimkateg, reslin_queasy
        nonlocal waehrung1, cc_list, member1, rguest, artikel1, argtline, argtline1


        nonlocal sum_list, currency_list, cl_list, s_list, argt_list, t_argt_line, waehrung1, cc_list, member1, rguest, artikel1, argtline, argtline1
        nonlocal sum_list_list, currency_list_list, cl_list_list, s_list_list, argt_list_list, t_argt_line_list

        tokcounter:int = 0
        mestoken:str = ""
        curr_artnr:int = 0
        curr_dept:int = 0
        a_betrag:decimal = 0
        x_betrag:decimal = 0

        if genstat.res_char[3] == "":

            return
        for tokcounter in range(1,num_entries(genstat.res_char[3], ";")  + 1) :
            mestoken = trim(entry(tokcounter - 1, genstat.res_char[3], ";"))

            if mestoken != "":
                curr_artnr = to_int(entry(0, mestoken, ","))
                curr_dept = to_int(entry(1, mestoken, ","))
                a_betrag = decimal.Decimal(entry(2, mestoken, ",")) * 0.01
                x_betrag = decimal.Decimal(entry(3, mestoken, ",")) * 0.01

                if curr_artnr == argt_line.argt_artnr and curr_dept == argt_line.departement:
                    argt_betrag = a_betrag * x_betrag / frate

                    return

    def check_fixleist_posted(artnr:int, dept:int, fakt_modus:int, intervall:int, lfakt:date):

        nonlocal cl_list_list, currency_list_list, sum_list_list, s_list_list, argt_list_list, exchg_rate, frate, post_it, total_rev, lvcarea, curr_code, curr_rate, curr_local, curr_bfast, curr_lodge, curr_lunch, curr_dinner, curr_misc, curr_fcost, curr_trev, curr_pax, curr_com, curr_rm, curr_adult, curr_ch1, curr_ch2, curr_comch, argt_line, waehrung, guest, artikel, htparam, res_line, zimmer, genstat, arrangement, exrate, reservation, billjournal, bill, zimkateg, reslin_queasy
        nonlocal waehrung1, cc_list, member1, rguest, artikel1, argtline, argtline1


        nonlocal sum_list, currency_list, cl_list, s_list, argt_list, t_argt_line, waehrung1, cc_list, member1, rguest, artikel1, argtline, argtline1
        nonlocal sum_list_list, currency_list_list, cl_list_list, s_list_list, argt_list_list, t_argt_line_list

        post_it = False
        delta:int = 0
        start_date:date = None

        def generate_inner_output():
            return post_it

        if fakt_modus == 1:
            post_it = True

        elif fakt_modus == 2:

            if (res_line.ankunft == genstat.datum):
                post_it = True

        elif fakt_modus == 3:

            if ((res_line.ankunft + 1) == genstat.datum):
                post_it = True

        elif fakt_modus == 4:

            if (get_day(genstat.datum) == 1):
                post_it = True

        elif fakt_modus == 5:

            if (get_day(genstat.datum + 1) == 1):
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

            if tdate <= (start_date + (intervall - 1)):
                post_it = True

            if tdate < start_date:
                post_it = False


        return generate_inner_output()

    create_billbalance1()
    cl_list = Cl_list()
    cl_list_list.append(cl_list)

    cl_list.flag = "*"
    cl_list.zinr = ""
    cl_list.c_zipreis = "s U m m A R Y:"


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

        if cl_list.lodging < 0:
            cl_list.c_lodging = to_string(cl_list.lodging, "->>,>>>,>>>,>>9.99")
        else:
            cl_list.c_lodging = to_string(cl_list.lodging, ">>>,>>>,>>>,>>9.99")
        cl_list.c_zipreis = to_string(cl_list.zipreis, ">>>,>>>,>>>,>>9.99")
        cl_list.c_localrate = to_string(cl_list.localrate, ">>>,>>>,>>>,>>9.99")
        cl_list.c_bfast = to_string(cl_list.bfast, "->,>>>,>>>,>>9.99")
        cl_list.c_lunch = to_string(cl_list.lunch, "->,>>>,>>>,>>9.99")
        cl_list.c_dinner = to_string(cl_list.dinner, "->,>>>,>>>,>>9.99")
        cl_list.c_misc = to_string(cl_list.misc, "->,>>>,>>>,>>9.99")
        cl_list.c_fixcost = to_string(cl_list.fixcost, "->>>,>>>,>>9.99")
        cl_list.ct_rev = to_string(cl_list.t_rev, ">>>,>>>,>>>,>>9.99")

        argt_list = query(argt_list_list, filters=(lambda argt_list :argt_list.argtcode == cl_list.argt), first=True)

        if argt_list:
            argt_list.bfast = argt_list.bfast + cl_list.bfast

    if exc_taxserv:

        for s_list in query(s_list_list):
            s_list.f_betrag = round((s_list.f_betrag / (1 + vat1 + vat2 + serv1)) , price_decimal)
            s_list.l_betrag = round((s_list.l_betrag / (1 + vat1 + vat2 + serv1)) , price_decimal)

        for sum_list in query(sum_list_list):
            sum_list.lodging = round((sum_list.lodging / (1 + vat1 + vat2 + serv1)) , price_decimal)
            sum_list.bfast = round((sum_list.bfast / (1 + vat1 + vat2 + serv1)) , price_decimal)
            sum_list.lunch = round((sum_list.lunch / (1 + vat1 + vat2 + serv1)) , price_decimal)
            sum_list.dinner = round((sum_list.dinner / (1 + vat1 + vat2 + serv1)) , price_decimal)
            sum_list.misc = round((sum_list.misc / (1 + vat1 + vat2 + serv1)) , price_decimal)
            sum_list.fixcost = round((sum_list.fixcost / (1 + vat1 + vat2 + serv1)) , price_decimal)
            sum_list.t_rev = round((sum_list.t_rev / (1 + vat1 + vat2 + serv1)) , price_decimal)


    total_rev = tot_rate

    return generate_output()