#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from functions.calc_servtaxesbl import calc_servtaxesbl
from models import Argt_line, Waehrung, Guest, Artikel, Htparam, Res_line, Zimmer, Genstat, Arrangement, Exrate, Reservation, Billjournal, Bill, Zimkateg, Segment, Reslin_queasy

def rmrev_bdown_create_billbalance1_4a_webbl(exc_taxserv:bool, pvilanguage:int, new_contrate:bool, foreign_rate:bool, price_decimal:int, curr_date:date, srttype:int):

    prepare_cache ([Waehrung, Guest, Artikel, Htparam, Res_line, Zimmer, Genstat, Arrangement, Exrate, Reservation, Billjournal, Bill, Zimkateg, Segment, Reslin_queasy])

    cl_list_data = []
    currency_list_data = []
    sum_list_data = []
    s_list_data = []
    argt_list_data = []
    exchg_rate:Decimal = 1
    frate:Decimal = to_decimal("0.0")
    post_it:bool = False
    total_rev:Decimal = to_decimal("0.0")
    rm_rate:Decimal = to_decimal("0.0")
    temptotjur:Decimal = to_decimal("0.0")
    lvcarea:string = "rmrev-bdown"
    argt_line = waehrung = guest = artikel = htparam = res_line = zimmer = genstat = arrangement = exrate = reservation = billjournal = bill = zimkateg = segment = reslin_queasy = None

    sum_list = currency_list = cl_list = s_list = argt_list = t_argt_line = waehrung1 = cc_list = None

    sum_list_data, Sum_list = create_model("Sum_list", {"bezeich":string, "pax":int, "adult":int, "ch1":int, "ch2":int, "comch":int, "com":int, "lodging":Decimal, "bfast":Decimal, "lunch":Decimal, "dinner":Decimal, "misc":Decimal, "fixcost":Decimal, "t_rev":Decimal})
    currency_list_data, Currency_list = create_model("Currency_list", {"code":string})
    cl_list_data, Cl_list = create_model("Cl_list", {"zipreis":Decimal, "localrate":Decimal, "lodging":Decimal, "bfast":Decimal, "lunch":Decimal, "dinner":Decimal, "misc":Decimal, "fixcost":Decimal, "t_rev":Decimal, "c_zipreis":string, "c_localrate":string, "c_lodging":string, "c_bfast":string, "c_lunch":string, "c_dinner":string, "c_misc":string, "c_fixcost":string, "ct_rev":string, "res_recid":int, "sleeping":bool, "row_disp":int, "flag":string, "zinr":string, "rstatus":int, "argt":string, "currency":string, "ratecode":string, "pax":int, "com":int, "ankunft":date, "abreise":date, "rechnr":int, "name":string, "ex_rate":string, "fix_rate":string, "adult":int, "ch1":int, "ch2":int, "comch":int, "age1":int, "age2":string, "rmtype":string, "resnr":int, "resname":string, "segm_desc":string, "nation":string}, {"sleeping": True})
    s_list_data, S_list = create_model("S_list", {"artnr":int, "dept":int, "bezeich":string, "curr":string, "anzahl":int, "betrag":Decimal, "l_betrag":Decimal, "f_betrag":Decimal})
    argt_list_data, Argt_list = create_model("Argt_list", {"argtnr":int, "argtcode":string, "bezeich":string, "room":int, "pax":int, "qty":int, "bfast":Decimal})
    t_argt_line_data, T_argt_line = create_model_like(Argt_line)

    Waehrung1 = create_buffer("Waehrung1",Waehrung)
    Cc_list = Cl_list
    cc_list_data = cl_list_data

    db_session = local_storage.db_session

    def generate_output():
        nonlocal cl_list_data, currency_list_data, sum_list_data, s_list_data, argt_list_data, exchg_rate, frate, post_it, total_rev, rm_rate, temptotjur, lvcarea, argt_line, waehrung, guest, artikel, htparam, res_line, zimmer, genstat, arrangement, exrate, reservation, billjournal, bill, zimkateg, segment, reslin_queasy
        nonlocal exc_taxserv, pvilanguage, new_contrate, foreign_rate, price_decimal, curr_date, srttype
        nonlocal waehrung1, cc_list


        nonlocal sum_list, currency_list, cl_list, s_list, argt_list, t_argt_line, waehrung1, cc_list
        nonlocal sum_list_data, currency_list_data, cl_list_data, s_list_data, argt_list_data, t_argt_line_data

        return {"cl-list": cl_list_data, "currency-list": currency_list_data, "sum-list": sum_list_data, "s-list": s_list_data, "argt-list": argt_list_data}

    def create_billbalance1():

        nonlocal cl_list_data, currency_list_data, sum_list_data, s_list_data, argt_list_data, exchg_rate, frate, post_it, total_rev, rm_rate, temptotjur, lvcarea, argt_line, waehrung, guest, artikel, htparam, res_line, zimmer, genstat, arrangement, exrate, reservation, billjournal, bill, zimkateg, segment, reslin_queasy
        nonlocal exc_taxserv, pvilanguage, new_contrate, foreign_rate, price_decimal, curr_date, srttype
        nonlocal waehrung1, cc_list


        nonlocal sum_list, currency_list, cl_list, s_list, argt_list, t_argt_line, waehrung1, cc_list
        nonlocal sum_list_data, currency_list_data, cl_list_data, s_list_data, argt_list_data, t_argt_line_data

        member1 = None
        rguest = None
        fcost:Decimal = to_decimal("0.0")
        tot_pax:int = 0
        tot_com:int = 0
        tot_rm:int = 0
        tot_rate:Decimal = to_decimal("0.0")
        tot_lrate:Decimal = to_decimal("0.0")
        tot_lodging:Decimal = to_decimal("0.0")
        tot_bfast:Decimal = to_decimal("0.0")
        tot_lunch:Decimal = to_decimal("0.0")
        tot_dinner:Decimal = to_decimal("0.0")
        tot_misc:Decimal = to_decimal("0.0")
        tot_fix:Decimal = to_decimal("0.0")
        tot_adult:int = 0
        tot_ch1:int = 0
        tot_ch2:int = 0
        tot_comch:int = 0
        ltot_rm:int = 0
        ltot_pax:int = 0
        ltot_rate:Decimal = to_decimal("0.0")
        ltot_lodging:Decimal = to_decimal("0.0")
        ltot_bfast:Decimal = to_decimal("0.0")
        ltot_lunch:Decimal = to_decimal("0.0")
        ltot_dinner:Decimal = to_decimal("0.0")
        ltot_misc:Decimal = to_decimal("0.0")
        ltot_fix:Decimal = to_decimal("0.0")
        curr_zinr:string = ""
        curr_resnr:int = 0
        bfast_art:int = 0
        lunch_art:int = 0
        dinner_art:int = 0
        lundin_art:int = 0
        fb_dept:int = 0
        argt_betrag:Decimal = to_decimal("0.0")
        take_it:bool = False
        prcode:int = 0
        qty:int = 0
        r_qty:int = 0
        lodge_betrag:Decimal = to_decimal("0.0")
        f_betrag:Decimal = to_decimal("0.0")
        s:string = ""
        ct:string = ""
        contcode:string = ""
        vat:Decimal = to_decimal("0.0")
        service:Decimal = to_decimal("0.0")
        vat1:Decimal = to_decimal("0.0")
        service1:Decimal = to_decimal("0.0")
        serv1:Decimal = to_decimal("0.0")
        serv2:Decimal = to_decimal("0.0")
        vat2:Decimal = to_decimal("0.0")
        vat3:Decimal = to_decimal("0.0")
        vat4:Decimal = to_decimal("0.0")
        fact:Decimal = to_decimal("0.0")
        fact1:Decimal = to_decimal("0.0")
        fact2:Decimal = to_decimal("0.0")
        cr_code:string = ""
        loopi:int = 0
        str1:string = ""
        curr_zikatnr:int = 0
        artikel1 = None
        bill_rechnr:int = 0
        bill_master:int = 0
        serv_1:Decimal = to_decimal("0.0")
        vat_1:Decimal = to_decimal("0.0")
        vat_2:Decimal = to_decimal("0.0")
        fact_1:Decimal = to_decimal("0.0")
        serv_2:Decimal = to_decimal("0.0")
        vat_3:Decimal = to_decimal("0.0")
        vat_4:Decimal = to_decimal("0.0")
        fact_2:Decimal = to_decimal("0.0")
        bill_flag1:string = ""
        bill_flag2:string = ""
        deposit_art:int = 0
        argtline = None
        i:int = 0
        n:int = 0
        argtline1 = None
        j:int = 0
        m:int = 0
        curr_code:string = ""
        curr_rate:Decimal = to_decimal("0.0")
        curr_local:Decimal = to_decimal("0.0")
        curr_bfast:Decimal = to_decimal("0.0")
        curr_lodge:Decimal = to_decimal("0.0")
        curr_lunch:Decimal = to_decimal("0.0")
        curr_dinner:Decimal = to_decimal("0.0")
        curr_misc:Decimal = to_decimal("0.0")
        curr_fcost:Decimal = to_decimal("0.0")
        curr_trev:Decimal = to_decimal("0.0")
        curr_pax:int = 0
        curr_com:int = 0
        curr_rm:int = 0
        curr_adult:int = 0
        curr_ch1:int = 0
        curr_ch2:int = 0
        curr_comch:int = 0
        Member1 =  create_buffer("Member1",Guest)
        Rguest =  create_buffer("Rguest",Guest)
        Artikel1 =  create_buffer("Artikel1",Artikel)

        htparam = get_cache (Htparam, {"paramnr": [(eq, 125)]})
        bfast_art = htparam.finteger

        htparam = get_cache (Htparam, {"paramnr": [(eq, 126)]})
        fb_dept = htparam.finteger

        htparam = get_cache (Htparam, {"paramnr": [(eq, 227)]})
        lunch_art = htparam.finteger

        htparam = get_cache (Htparam, {"paramnr": [(eq, 228)]})
        dinner_art = htparam.finteger

        htparam = get_cache (Htparam, {"paramnr": [(eq, 229)]})
        lundin_art = htparam.finteger

        htparam = get_cache (Htparam, {"paramnr": [(eq, 120)]})
        deposit_art = htparam.finteger

        artikel = get_cache (Artikel, {"zwkum": [(eq, bfast_art)],"departement": [(eq, fb_dept)]})

        if not artikel and bfast_art != 0:

            return

        artikel = get_cache (Artikel, {"zwkum": [(eq, lunch_art)],"departement": [(eq, fb_dept)]})

        if not artikel and lunch_art != 0:

            return

        artikel = get_cache (Artikel, {"zwkum": [(eq, dinner_art)],"departement": [(eq, fb_dept)]})

        if not artikel and dinner_art != 0:

            return

        artikel = get_cache (Artikel, {"zwkum": [(eq, lundin_art)],"departement": [(eq, fb_dept)]})

        if not artikel and lundin_art != 0:

            return
        s_list_data.clear()
        cl_list_data.clear()
        currency_list_data.clear()
        sum_list_data.clear()
        sum_list = Sum_list()
        sum_list_data.append(sum_list)

        r_qty = 0
        lodge_betrag =  to_decimal("0")

        if srttype == 2:

            genstat_obj_list = {}
            genstat = Genstat()
            res_line = Res_line()
            zimmer = Zimmer()
            for genstat.argt, genstat.datum, genstat.zinr, genstat.resnr, genstat.res_int, genstat.erwachs, genstat.kind1, genstat.kind2, genstat.gratis, genstat.kind3, genstat.resstatus, genstat.zipreis, genstat.ratelocal, genstat.logis, genstat.res_deci, genstat.zikatnr, genstat.res_char, genstat._recid, res_line.betriebsnr, res_line.reserve_dec, res_line.gastnrpay, res_line.gastnrmember, res_line.resnr, res_line.l_zuordnung, res_line.zikatnr, res_line._recid, res_line.name, res_line.ankunft, res_line.abreise, res_line.resname, res_line.zimmer_wunsch, res_line.reslinnr, res_line.adrflag, res_line.zinr, res_line.zipreis, res_line.reserve_int, zimmer.sleeping, zimmer._recid in db_session.query(Genstat.argt, Genstat.datum, Genstat.zinr, Genstat.resnr, Genstat.res_int, Genstat.erwachs, Genstat.kind1, Genstat.kind2, Genstat.gratis, Genstat.kind3, Genstat.resstatus, Genstat.zipreis, Genstat.ratelocal, Genstat.logis, Genstat.res_deci, Genstat.zikatnr, Genstat.res_char, Genstat._recid, Res_line.betriebsnr, Res_line.reserve_dec, Res_line.gastnrpay, Res_line.gastnrmember, Res_line.resnr, Res_line.l_zuordnung, Res_line.zikatnr, Res_line._recid, Res_line.name, Res_line.ankunft, Res_line.abreise, Res_line.resname, Res_line.zimmer_wunsch, Res_line.reslinnr, Res_line.adrflag, Res_line.zinr, Res_line.zipreis, Res_line.reserve_int, Zimmer.sleeping, Zimmer._recid).join(Res_line,(Res_line.resnr == Genstat.resnr) & (Res_line.reslinnr == Genstat.res_int[inc_value(0)]) & (Res_line.l_zuordnung[inc_value(2)] == 0)).join(Zimmer,(Zimmer.zinr == Genstat.zinr)).filter(
                     (Genstat.zinr != "") & (Genstat.datum == curr_date) & (Genstat.res_logic[inc_value(1)])).order_by(Res_line.resname).all():
                if genstat_obj_list.get(genstat._recid):
                    continue
                else:
                    genstat_obj_list[genstat._recid] = True


                serv1 =  to_decimal("0")
                vat1 =  to_decimal("0")
                vat2 =  to_decimal("0")
                fact1 =  to_decimal("0")

                arrangement = get_cache (Arrangement, {"arrangement": [(eq, genstat.argt)]})

                artikel = get_cache (Artikel, {"artnr": [(eq, arrangement.argt_artikelnr)],"departement": [(eq, 0)]})
                serv1, vat1, vat2, fact1 = get_output(calc_servtaxesbl(1, artikel.artnr, artikel.departement, curr_date))

                waehrung1 = get_cache (Waehrung, {"waehrungsnr": [(eq, res_line.betriebsnr)]})

                exrate = get_cache (Exrate, {"datum": [(eq, curr_date)],"artnr": [(eq, waehrung1.waehrungsnr)]})
                exchg_rate =  to_decimal(exrate.betrag)

                if res_line.reserve_dec != 0:
                    frate =  to_decimal(res_line.reserve_dec)
                else:
                    frate =  to_decimal(exchg_rate)

                if genstat.zipreis != 0:
                    r_qty = r_qty + 1

                guest = get_cache (Guest, {"gastnr": [(eq, res_line.gastnrpay)]})

                member1 = get_cache (Guest, {"gastnr": [(eq, res_line.gastnrmember)]})

                reservation = get_cache (Reservation, {"resnr": [(eq, res_line.resnr)]})

                if res_line.l_zuordnung[0] != 0:
                    curr_zikatnr = res_line.l_zuordnung[0]
                else:
                    curr_zikatnr = res_line.zikatnr

                for billjournal in db_session.query(Billjournal).filter(
                         (Billjournal.bill_datum == genstat.datum) & (Billjournal.zinr == genstat.zinr)).order_by(Billjournal._recid).yield_per(100):
                    bill_flag1 = ""

                    bill = get_cache (Bill, {"rechnr": [(eq, billjournal.rechnr)],"resnr": [(eq, genstat.resnr)],"reslinnr": [(eq, 0)]})

                    if bill:
                        bill_master = bill.rechnr
                        bill_flag1 = "Master Bill"

                    if bill_flag1.lower()  == ("Master Bill").lower() :
                        break

                bill = get_cache (Bill, {"resnr": [(eq, genstat.resnr)],"reslinnr": [(eq, genstat.res_int[0])]})

                if bill:
                    bill_rechnr = bill.rechnr
                    bill_flag2 = "Guest Bill"
                sum_list.pax = sum_list.pax + genstat.erwachs + genstat.kind1 + genstat.kind2
                sum_list.adult = sum_list.adult + genstat.erwachs
                sum_list.com = sum_list.com + genstat.gratis + genstat.kind3


                cl_list = Cl_list()
                cl_list_data.append(cl_list)

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
                    cl_list.zipreis =  to_decimal(genstat.zipreis)
                    cl_list.localrate =  to_decimal(genstat.ratelocal)
                    cl_list.t_rev =  to_decimal(genstat.zipreis)
                    cl_list.lodging =  to_decimal(genstat.logis) * to_decimal((1) + to_decimal(vat1) + to_decimal(vat2) + to_decimal(serv1) )
                    cl_list.fixcost =  to_decimal(genstat.res_deci[5]) * to_decimal((1) + to_decimal(vat1) + to_decimal(vat2) + to_decimal(serv1) )


                else:
                    cl_list.zipreis = to_decimal(round((genstat.zipreis / (1 + vat1 + vat2 + serv1)) , price_decimal))
                    cl_list.localrate = to_decimal(round((genstat.ratelocal / (1 + vat1 + vat2 + serv1)) , price_decimal))
                    cl_list.t_rev = to_decimal(round((genstat.zipreis / (1 + vat1 + vat2 + serv1)) , price_decimal))
                    cl_list.lodging = to_decimal(round(genstat.logis , price_decimal))
                    cl_list.fixcost = to_decimal(round(genstat.res_deci[5] , price_decimal))


                sum_list.lodging =  to_decimal(sum_list.lodging) + to_decimal(cl_list.lodging)
                sum_list.t_rev =  to_decimal(sum_list.t_rev) + to_decimal(genstat.zipreis)
                sum_list.fixcost =  to_decimal(sum_list.fixcost) + to_decimal(cl_list.fixcost)

                if bill_flag1.lower()  == ("Master Bill").lower() :

                    billjournal = get_cache (Billjournal, {"rechnr": [(eq, bill_master)],"bill_datum": [(eq, genstat.datum)]})

                    if billjournal:
                        cl_list.rechnr = bill_master

                if bill_flag2.lower()  == ("Guest Bill").lower() :

                    billjournal = get_cache (Billjournal, {"rechnr": [(eq, bill_rechnr)],"bill_datum": [(eq, genstat.datum)]})

                    if billjournal:
                        cl_list.rechnr = bill_rechnr

                if genstat.gratis != 0:
                    cl_list.rechnr = 0
                cl_list.adult = genstat.erwachs
                cl_list.ch1 = genstat.kind1
                cl_list.ch2 = genstat.kind2
                cl_list.comch = genstat.kind3

                zimkateg = get_cache (Zimkateg, {"zikatnr": [(eq, genstat.zikatnr)]})

                if zimkateg:
                    cl_list.rmtype = zimkateg.kurzbez

                segment = get_cache (Segment, {"segmentcode": [(eq, reservation.segmentcode)]})

                if segment:
                    cl_list.segm_desc = segment.bezeich

                if member1.nation1 != "":
                    cl_list.nation = member1.nation1

                if cl_list.zipreis == 0 and cl_list.adult == 0:
                    cl_list.pax = cl_list.com + cl_list.comch


                else:
                    cl_list.pax = genstat.erwachs + genstat.kind1 + genstat.kind2 + cl_list.com + cl_list.comch

                if guest:
                    cl_list.name = cl_list.name + guest.name + ", " + guest.vorname1 + "-" + guest.adresse1
                    cl_list.currency = waehrung1.wabkurz

                argt_list = query(argt_list_data, filters=(lambda argt_list: argt_list.argtnr == arrangement.argtnr), first=True)

                if not argt_list:
                    argt_list = Argt_list()
                    argt_list_data.append(argt_list)

                    argt_list.argtnr = arrangement.argtnr
                    argt_list.argtcode = arrangement.arrangement
                    argt_list.bezeich = arrangement.argt_bez
                    argt_list.room = 1

                    if cl_list.zipreis == 0 and cl_list.adult == 0:
                        argt_list.pax = cl_list.com + cl_list.comch


                    else:
                        argt_list.pax = genstat.erwachs + genstat.kind1 + genstat.kind2 + cl_list.com + cl_list.comch
                else:
                    argt_list.room = argt_list.room + 1

                    if cl_list.zipreis == 0 and cl_list.adult == 0:
                        argt_list.pax = argt_list.pax + cl_list.com + cl_list.comch


                    else:
                        argt_list.pax = argt_list.pax + genstat.erwachs + genstat.kind1 + genstat.kind2 + cl_list.com + cl_list.comch

                if guest.geburtdatum1 != None and guest.geburtdatum2 != None:

                    if guest.geburtdatum1 < guest.geburtdatum2:
                        cl_list.age1 = get_year(guest.geburtdatum2) - get_year(guest.geburtdatum1)

                if matches(res_line.zimmer_wunsch,r"*ChAge*"):
                    for loopi in range(1,num_entries(res_line.zimmer_wunsch, ";") - 1 + 1) :
                        str1 = entry(loopi - 1, res_line.zimmer_wunsch, ";")

                        if substring(str1, 0, 5) == ("ChAge").lower() :
                            cl_list.age2 = substring(str1, 5)
                serv2 =  to_decimal("0")
                vat3 =  to_decimal("0")
                vat4 =  to_decimal("0")
                fact2 =  to_decimal("0")


                for loopi in range(1,num_entries(genstat.res_char[1], ";") - 1 + 1) :
                    str1 = entry(loopi - 1, genstat.res_char[1], ";")

                    if substring(str1, 0, 6) == ("$CODE$").lower() :
                        cr_code = substring(str1, 6)

                if genstat.zipreis != 0:
                    rm_rate =  to_decimal(genstat.zipreis)

                    argt_line_obj_list = {}
                    for argt_line, artikel in db_session.query(Argt_line, Artikel).join(Artikel,(Artikel.artnr == Argt_line.argt_artnr) & (Artikel.departement == Argt_line.departement)).filter(
                             (Argt_line.argtnr == arrangement.argtnr) & not_ (Argt_line.kind2) & (Argt_line.kind1)).order_by(Argt_line._recid).all():
                        if argt_line_obj_list.get(argt_line._recid):
                            continue
                        else:
                            argt_line_obj_list[argt_line._recid] = True


                        Argtline =  create_buffer("Argtline",Argt_line)
                        take_it, f_betrag, argt_betrag, qty = get_argtline_rate(contcode, argt_line._recid)
                        serv2, vat3, vat4, fact2 = get_output(calc_servtaxesbl(1, artikel.artnr, artikel.departement, curr_date))
                        vat3 =  to_decimal(vat3) + to_decimal(vat4)

                        if artikel.zwkum == bfast_art and (artikel.umsatzart == 3 or artikel.umsatzart >= 5):

                            if not exc_taxserv:
                                cl_list.bfast =  to_decimal(genstat.res_deci[1]) * to_decimal((1) + to_decimal(vat3) + to_decimal(serv2) )
                                sum_list.bfast =  to_decimal(sum_list.bfast) + to_decimal(cl_list.bfast)


                            else:
                                cl_list.bfast =  to_decimal(genstat.res_deci[1])
                                sum_list.bfast =  to_decimal(sum_list.bfast) + to_decimal(cl_list.bfast)

                        elif artikel.zwkum == lunch_art and (artikel.umsatzart == 3 or artikel.umsatzart >= 5):

                            if not exc_taxserv:
                                cl_list.lunch =  to_decimal(genstat.res_deci[2]) * to_decimal((1) + to_decimal(vat3) + to_decimal(serv2) )
                                sum_list.lunch =  to_decimal(sum_list.lunch) + to_decimal(cl_list.lunch)


                            else:
                                cl_list.lunch =  to_decimal(genstat.res_deci[2])
                                sum_list.lunch =  to_decimal(sum_list.lunch) + to_decimal(cl_list.lunch)

                        elif artikel.zwkum == dinner_art and (artikel.umsatzart == 3 or artikel.umsatzart >= 5):

                            if not exc_taxserv:
                                cl_list.dinner =  to_decimal(genstat.res_deci[3]) * to_decimal((1) + to_decimal(vat3) + to_decimal(serv2) )
                                sum_list.dinner =  to_decimal(sum_list.dinner) + to_decimal(cl_list.dinner)


                            else:
                                cl_list.dinner =  to_decimal(genstat.res_deci[3])
                                sum_list.dinner =  to_decimal(sum_list.dinner) + to_decimal(cl_list.dinner)

                        elif artikel.zwkum == lundin_art and (artikel.umsatzart == 3 or artikel.umsatzart >= 5):

                            if not exc_taxserv:
                                cl_list.lunch =  to_decimal(genstat.res_deci[2]) * to_decimal((1) + to_decimal(vat3) + to_decimal(serv2) )
                                sum_list.lunch =  to_decimal(sum_list.lunch) + to_decimal(cl_list.lunch)


                            else:
                                cl_list.lunch =  to_decimal(genstat.res_deci[2])
                                sum_list.lunch =  to_decimal(sum_list.lunch) + to_decimal(cl_list.lunch)


                        else:

                            if argt_betrag != 0:
                                pass

                    if not exc_taxserv:
                        cl_list.misc =  to_decimal(cl_list.localrate) - to_decimal((cl_list.lodging) + to_decimal(cl_list.bfast) + to_decimal(cl_list.lunch) + to_decimal(cl_list.dinner) )
                        sum_list.misc =  to_decimal(sum_list.misc) + to_decimal(cl_list.misc)


                    else:
                        cl_list.misc =  to_decimal(genstat.res_deci[4])
                        sum_list.misc =  to_decimal(sum_list.misc) + to_decimal(cl_list.misc)

                    if cl_list.misc < 0 and cl_list.misc > -1:
                        cl_list.misc =  to_decimal(0.00)

                htparam = get_cache (Htparam, {"paramnr": [(eq, 127)]})

                if htparam.flogical and not exc_taxserv:
                    cl_list.zipreis = to_decimal(round(cl_list.zipreis , price_decimal))
                    cl_list.lodging = to_decimal(round(cl_list.lodging , price_decimal))
                    cl_list.bfast = to_decimal(round(cl_list.bfast , price_decimal))
                    cl_list.lunch = to_decimal(round(cl_list.lunch , price_decimal))
                    cl_list.dinner = to_decimal(round(cl_list.dinner , price_decimal))
                    cl_list.misc = to_decimal(round(cl_list.misc , price_decimal))
                    cl_list.fixcost = to_decimal(round(cl_list.fixcost , price_decimal))
                    cl_list.localrate = to_decimal(round(cl_list.localrate , price_decimal))
                    cl_list.t_rev = to_decimal(round(cl_list.t_rev , price_decimal))

                if matches(res_line.zimmer_wunsch,r"*$CODE$*"):
                    s = substring(res_line.zimmer_wunsch, (get_index(res_line.zimmer_wunsch, "$CODE$") + 6) - 1)
                    cl_list.ratecode = trim(entry(0, s, ";"))

                if frate == 1:
                    cl_list.ex_rate = to_string(frate, " >>9.99")

                elif frate <= 999:
                    cl_list.ex_rate = to_string(frate, " >>9.9999")

                elif frate <= 99999:
                    cl_list.ex_rate = to_string(frate, ">>,>>9.99")
                else:
                    cl_list.ex_rate = to_string(frate, ">,>>>,>>9")

                reslin_queasy = get_cache (Reslin_queasy, {"key": [(eq, "arrangement")],"resnr": [(eq, res_line.resnr)],"reslinnr": [(eq, res_line.reslinnr)],"date1": [(le, curr_date)],"date2": [(ge, curr_date)]})

                if reslin_queasy:
                    cl_list.fix_rate = "F"


                tot_rate =  to_decimal(tot_rate) + to_decimal(cl_list.zipreis)
                tot_lrate =  to_decimal(tot_lrate) + to_decimal(cl_list.localrate)

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
                         (Argt_line.argtnr == arrangement.argtnr) & not_ (Argt_line.kind2) & (Argt_line.kind1)).order_by(Argt_line.argtnr, Argt_line.argt_artnr).all():

                    t_argt_line = query(t_argt_line_data, filters=(lambda t_argt_line: t_argt_line.argt_artnr == argt_line.argt_artnr and t_argt_line.argtnr == arrangement.argtnr and t_argt_line.departement == argt_line.departement), first=True)

                    if not t_argt_line:
                        t_argt_line = T_argt_line()
                        t_argt_line_data.append(t_argt_line)

                        buffer_copy(argt_line, t_argt_line)

                if genstat.zipreis != 0:

                    if bill_flag1.lower()  == ("Master Bill").lower() :

                        billjournal_obj_list = {}
                        billjournal = Billjournal()
                        artikel = Artikel()
                        for billjournal.rechnr, billjournal.artnr, billjournal.departement, billjournal.bezeich, billjournal.fremdwaehrng, billjournal.betrag, billjournal._recid, artikel.artnr, artikel.departement, artikel.umsatzart, artikel.zwkum, artikel._recid in db_session.query(Billjournal.rechnr, Billjournal.artnr, Billjournal.departement, Billjournal.bezeich, Billjournal.fremdwaehrng, Billjournal.betrag, Billjournal._recid, Artikel.artnr, Artikel.departement, Artikel.umsatzart, Artikel.zwkum, Artikel._recid).join(Artikel,(Artikel.artnr == Billjournal.artnr) & (Artikel.departement == Billjournal.departement) & (Artikel.artart != 9)).filter(
                                 (Billjournal.rechnr == bill_master) & (Billjournal.bill_datum == genstat.datum) & (Billjournal.zinr == genstat.zinr) & (Billjournal.betrag != 0) & (Billjournal.anzahl != 0) & not_ (Billjournal.kassarapport) & (Billjournal.userinit == ("$$").lower())).order_by(Billjournal.sysdate, Billjournal.bill_datum, Billjournal.zinr).all():
                            if billjournal_obj_list.get(billjournal._recid):
                                continue
                            else:
                                billjournal_obj_list[billjournal._recid] = True

                            if billjournal.artnr != deposit_art:

                                s_list = query(s_list_data, filters=(lambda s_list: s_list.artnr == billjournal.artnr and s_list.dept == billjournal.departement and s_list.curr == waehrung1.wabkurz), first=True)

                                if not s_list:
                                    s_list = S_list()
                                    s_list_data.append(s_list)

                                    s_list.artnr = billjournal.artnr
                                    s_list.dept = billjournal.departement
                                    s_list.bezeich = billjournal.bezeich
                                    s_list.curr = waehrung1.wabkurz


                                s_list.f_betrag =  to_decimal(s_list.f_betrag) + to_decimal(billjournal.fremdwaehrng)
                                s_list.l_betrag =  to_decimal(s_list.l_betrag) + to_decimal(billjournal.betrag)


                        bill_master = -1

                    if bill_flag2.lower()  == ("Guest Bill").lower() :

                        billjournal_obj_list = {}
                        billjournal = Billjournal()
                        artikel = Artikel()
                        for billjournal.rechnr, billjournal.artnr, billjournal.departement, billjournal.bezeich, billjournal.fremdwaehrng, billjournal.betrag, billjournal._recid, artikel.artnr, artikel.departement, artikel.umsatzart, artikel.zwkum, artikel._recid in db_session.query(Billjournal.rechnr, Billjournal.artnr, Billjournal.departement, Billjournal.bezeich, Billjournal.fremdwaehrng, Billjournal.betrag, Billjournal._recid, Artikel.artnr, Artikel.departement, Artikel.umsatzart, Artikel.zwkum, Artikel._recid).join(Artikel,(Artikel.artnr == Billjournal.artnr) & (Artikel.departement == Billjournal.departement) & (Artikel.artart != 9)).filter(
                                 (Billjournal.rechnr == bill_rechnr) & (Billjournal.bill_datum == genstat.datum) & (Billjournal.zinr == genstat.zinr) & (Billjournal.betrag != 0) & (Billjournal.anzahl != 0) & not_ (Billjournal.kassarapport) & (Billjournal.userinit == ("$$").lower())).order_by(Billjournal.sysdate, Billjournal.bill_datum, Billjournal.zinr).all():
                            if billjournal_obj_list.get(billjournal._recid):
                                continue
                            else:
                                billjournal_obj_list[billjournal._recid] = True

                            if billjournal.artnr != deposit_art:

                                s_list = query(s_list_data, filters=(lambda s_list: s_list.artnr == billjournal.artnr and s_list.dept == billjournal.departement and s_list.curr == waehrung1.wabkurz), first=True)

                                if not s_list:
                                    s_list = S_list()
                                    s_list_data.append(s_list)

                                    s_list.artnr = billjournal.artnr
                                    s_list.dept = billjournal.departement
                                    s_list.bezeich = billjournal.bezeich
                                    s_list.curr = waehrung1.wabkurz


                                s_list.f_betrag =  to_decimal(s_list.f_betrag) + to_decimal(billjournal.fremdwaehrng)
                                s_list.l_betrag =  to_decimal(s_list.l_betrag) + to_decimal(billjournal.betrag)


                        bill_rechnr = -1

                if res_line.adrflag:
                    ltot_lodging =  to_decimal(ltot_lodging) + to_decimal(cl_list.lodging)
                else:
                    tot_lodging =  to_decimal(tot_lodging) + to_decimal(cl_list.lodging)
                lodge_betrag =  to_decimal(cl_list.lodging)

                if foreign_rate and price_decimal == 0 and not res_line.adrflag:

                    htparam = get_cache (Htparam, {"paramnr": [(eq, 145)]})

                    if htparam.finteger != 0:
                        n = 1
                        for i in range(1,htparam.finteger + 1) :
                            n = n * 10
                        lodge_betrag = to_decimal(round(lodge_betrag / n , 0) * n)

                if curr_zinr != res_line.zinr or curr_resnr != res_line.resnr:

                    if res_line.adrflag:
                        ltot_rm = ltot_rm + 1
                    else:
                        tot_rm = tot_rm + 1
                curr_zinr = res_line.zinr
                curr_resnr = res_line.resnr
        else:

            genstat_obj_list = {}
            genstat = Genstat()
            res_line = Res_line()
            zimmer = Zimmer()
            for genstat.argt, genstat.datum, genstat.zinr, genstat.resnr, genstat.res_int, genstat.erwachs, genstat.kind1, genstat.kind2, genstat.gratis, genstat.kind3, genstat.resstatus, genstat.zipreis, genstat.ratelocal, genstat.logis, genstat.res_deci, genstat.zikatnr, genstat.res_char, genstat._recid, res_line.betriebsnr, res_line.reserve_dec, res_line.gastnrpay, res_line.gastnrmember, res_line.resnr, res_line.l_zuordnung, res_line.zikatnr, res_line._recid, res_line.name, res_line.ankunft, res_line.abreise, res_line.resname, res_line.zimmer_wunsch, res_line.reslinnr, res_line.adrflag, res_line.zinr, res_line.zipreis, res_line.reserve_int, zimmer.sleeping, zimmer._recid in db_session.query(Genstat.argt, Genstat.datum, Genstat.zinr, Genstat.resnr, Genstat.res_int, Genstat.erwachs, Genstat.kind1, Genstat.kind2, Genstat.gratis, Genstat.kind3, Genstat.resstatus, Genstat.zipreis, Genstat.ratelocal, Genstat.logis, Genstat.res_deci, Genstat.zikatnr, Genstat.res_char, Genstat._recid, Res_line.betriebsnr, Res_line.reserve_dec, Res_line.gastnrpay, Res_line.gastnrmember, Res_line.resnr, Res_line.l_zuordnung, Res_line.zikatnr, Res_line._recid, Res_line.name, Res_line.ankunft, Res_line.abreise, Res_line.resname, Res_line.zimmer_wunsch, Res_line.reslinnr, Res_line.adrflag, Res_line.zinr, Res_line.zipreis, Res_line.reserve_int, Zimmer.sleeping, Zimmer._recid).join(Res_line,(Res_line.resnr == Genstat.resnr) & (Res_line.reslinnr == Genstat.res_int[inc_value(0)]) & (Res_line.l_zuordnung[inc_value(2)] == 0)).join(Zimmer,(Zimmer.zinr == Genstat.zinr)).filter(
                     (Genstat.zinr != "") & (Genstat.datum == curr_date) & (Genstat.res_logic[inc_value(1)])).order_by(Genstat.zinr, Genstat.resnr).all():
                if genstat_obj_list.get(genstat._recid):
                    continue
                else:
                    genstat_obj_list[genstat._recid] = True


                serv1 =  to_decimal("0")
                vat1 =  to_decimal("0")
                vat2 =  to_decimal("0")
                fact1 =  to_decimal("0")

                arrangement = get_cache (Arrangement, {"arrangement": [(eq, genstat.argt)]})

                artikel = get_cache (Artikel, {"artnr": [(eq, arrangement.argt_artikelnr)],"departement": [(eq, 0)]})
                serv1, vat1, vat2, fact1 = get_output(calc_servtaxesbl(1, artikel.artnr, artikel.departement, curr_date))

                waehrung1 = get_cache (Waehrung, {"waehrungsnr": [(eq, res_line.betriebsnr)]})

                exrate = get_cache (Exrate, {"datum": [(eq, curr_date)],"artnr": [(eq, waehrung1.waehrungsnr)]})
                exchg_rate =  to_decimal(exrate.betrag)

                if res_line.reserve_dec != 0:
                    frate =  to_decimal(res_line.reserve_dec)
                else:
                    frate =  to_decimal(exchg_rate)

                if genstat.zipreis != 0:
                    r_qty = r_qty + 1

                guest = get_cache (Guest, {"gastnr": [(eq, res_line.gastnrpay)]})

                member1 = get_cache (Guest, {"gastnr": [(eq, res_line.gastnrmember)]})

                reservation = get_cache (Reservation, {"resnr": [(eq, res_line.resnr)]})

                if res_line.l_zuordnung[0] != 0:
                    curr_zikatnr = res_line.l_zuordnung[0]
                else:
                    curr_zikatnr = res_line.zikatnr

                for billjournal in db_session.query(Billjournal).filter(
                         (Billjournal.bill_datum == genstat.datum) & (Billjournal.zinr == genstat.zinr)).order_by(Billjournal._recid).yield_per(100):
                    bill_flag1 = ""

                    bill = get_cache (Bill, {"rechnr": [(eq, billjournal.rechnr)],"resnr": [(eq, genstat.resnr)],"reslinnr": [(eq, 0)]})

                    if bill:
                        bill_master = bill.rechnr
                        bill_flag1 = "Master Bill"

                    if bill_flag1.lower()  == ("Master Bill").lower() :
                        break

                bill = get_cache (Bill, {"resnr": [(eq, genstat.resnr)],"reslinnr": [(eq, genstat.res_int[0])]})

                if bill:
                    bill_rechnr = bill.rechnr
                    bill_flag2 = "Guest Bill"
                sum_list.pax = sum_list.pax + genstat.erwachs + genstat.kind1 + genstat.kind2
                sum_list.adult = sum_list.adult + genstat.erwachs
                sum_list.com = sum_list.com + genstat.gratis + genstat.kind3


                cl_list = Cl_list()
                cl_list_data.append(cl_list)

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
                    cl_list.zipreis =  to_decimal(genstat.zipreis)
                    cl_list.localrate =  to_decimal(genstat.ratelocal)
                    cl_list.t_rev =  to_decimal(genstat.zipreis)
                    cl_list.lodging =  to_decimal(genstat.logis) * to_decimal((1) + to_decimal(vat1) + to_decimal(vat2) + to_decimal(serv1) )
                    cl_list.fixcost =  to_decimal(genstat.res_deci[5]) * to_decimal((1) + to_decimal(vat1) + to_decimal(vat2) + to_decimal(serv1) )


                else:
                    cl_list.zipreis = to_decimal(round((genstat.zipreis / (1 + vat1 + vat2 + serv1)) , price_decimal))
                    cl_list.localrate = to_decimal(round((genstat.ratelocal / (1 + vat1 + vat2 + serv1)) , price_decimal))
                    cl_list.t_rev = to_decimal(round((genstat.zipreis / (1 + vat1 + vat2 + serv1)) , price_decimal))
                    cl_list.lodging = to_decimal(round(genstat.logis , price_decimal))
                    cl_list.fixcost = to_decimal(round(genstat.res_deci[5] , price_decimal))


                sum_list.lodging =  to_decimal(sum_list.lodging) + to_decimal(cl_list.lodging)
                sum_list.t_rev =  to_decimal(sum_list.t_rev) + to_decimal(genstat.zipreis)
                sum_list.fixcost =  to_decimal(sum_list.fixcost) + to_decimal(cl_list.fixcost)

                if bill_flag1.lower()  == ("Master Bill").lower() :

                    billjournal = get_cache (Billjournal, {"rechnr": [(eq, bill_master)],"bill_datum": [(eq, genstat.datum)]})

                    if billjournal:
                        cl_list.rechnr = bill_master

                if bill_flag2.lower()  == ("Guest Bill").lower() :

                    billjournal = get_cache (Billjournal, {"rechnr": [(eq, bill_rechnr)],"bill_datum": [(eq, genstat.datum)]})

                    if billjournal:
                        cl_list.rechnr = bill_rechnr

                if genstat.gratis != 0:
                    cl_list.rechnr = 0
                cl_list.adult = genstat.erwachs
                cl_list.ch1 = genstat.kind1
                cl_list.ch2 = genstat.kind2
                cl_list.comch = genstat.kind3

                zimkateg = get_cache (Zimkateg, {"zikatnr": [(eq, genstat.zikatnr)]})

                if zimkateg:
                    cl_list.rmtype = zimkateg.kurzbez

                segment = get_cache (Segment, {"segmentcode": [(eq, reservation.segmentcode)]})

                if segment:
                    cl_list.segm_desc = segment.bezeich

                if member1.nation1 != "":
                    cl_list.nation = member1.nation1

                if cl_list.zipreis == 0 and cl_list.adult == 0:
                    cl_list.pax = cl_list.com + cl_list.comch


                else:
                    cl_list.pax = genstat.erwachs + genstat.kind1 + genstat.kind2 + cl_list.com + cl_list.comch

                if guest:
                    cl_list.name = cl_list.name + guest.name + ", " + guest.vorname1 + "-" + guest.adresse1
                    cl_list.currency = waehrung1.wabkurz

                argt_list = query(argt_list_data, filters=(lambda argt_list: argt_list.argtnr == arrangement.argtnr), first=True)

                if not argt_list:
                    argt_list = Argt_list()
                    argt_list_data.append(argt_list)

                    argt_list.argtnr = arrangement.argtnr
                    argt_list.argtcode = arrangement.arrangement
                    argt_list.bezeich = arrangement.argt_bez
                    argt_list.room = 1

                    if cl_list.zipreis == 0 and cl_list.adult == 0:
                        argt_list.pax = cl_list.com + cl_list.comch


                    else:
                        argt_list.pax = genstat.erwachs + genstat.kind1 + genstat.kind2 + cl_list.com + cl_list.comch
                else:
                    argt_list.room = argt_list.room + 1

                    if cl_list.zipreis == 0 and cl_list.adult == 0:
                        argt_list.pax = argt_list.pax + cl_list.com + cl_list.comch


                    else:
                        argt_list.pax = argt_list.pax + genstat.erwachs + genstat.kind1 + genstat.kind2 + cl_list.com + cl_list.comch

                if guest.geburtdatum1 != None and guest.geburtdatum2 != None:

                    if guest.geburtdatum1 < guest.geburtdatum2:
                        cl_list.age1 = get_year(guest.geburtdatum2) - get_year(guest.geburtdatum1)

                if matches(res_line.zimmer_wunsch,r"*ChAge*"):
                    for loopi in range(1,num_entries(res_line.zimmer_wunsch, ";") - 1 + 1) :
                        str1 = entry(loopi - 1, res_line.zimmer_wunsch, ";")

                        if substring(str1, 0, 5) == ("ChAge").lower() :
                            cl_list.age2 = substring(str1, 5)
                serv2 =  to_decimal("0")
                vat3 =  to_decimal("0")
                vat4 =  to_decimal("0")
                fact2 =  to_decimal("0")


                for loopi in range(1,num_entries(genstat.res_char[1], ";") - 1 + 1) :
                    str1 = entry(loopi - 1, genstat.res_char[1], ";")

                    if substring(str1, 0, 6) == ("$CODE$").lower() :
                        cr_code = substring(str1, 6)

                if genstat.zipreis != 0:

                    argt_line_obj_list = {}
                    for argt_line, artikel in db_session.query(Argt_line, Artikel).join(Artikel,(Artikel.artnr == Argt_line.argt_artnr) & (Artikel.departement == Argt_line.departement)).filter(
                             (Argt_line.argtnr == arrangement.argtnr) & not_ (Argt_line.kind2) & (Argt_line.kind1)).order_by(Argt_line._recid).all():
                        if argt_line_obj_list.get(argt_line._recid):
                            continue
                        else:
                            argt_line_obj_list[argt_line._recid] = True


                        Argtline1 =  create_buffer("Argtline1",Argt_line)
                        take_it, f_betrag, argt_betrag, qty = get_argtline_rate(contcode, argt_line._recid)
                        serv2, vat3, vat4, fact2 = get_output(calc_servtaxesbl(1, artikel.artnr, artikel.departement, curr_date))
                        vat3 =  to_decimal(vat3) + to_decimal(vat4)

                        if artikel.zwkum == bfast_art and (artikel.umsatzart == 3 or artikel.umsatzart >= 5):

                            if not exc_taxserv:
                                cl_list.bfast =  to_decimal(genstat.res_deci[1]) * to_decimal((1) + to_decimal(vat3) + to_decimal(serv2) )
                                sum_list.bfast =  to_decimal(sum_list.bfast) + to_decimal(cl_list.bfast)


                            else:
                                cl_list.bfast =  to_decimal(genstat.res_deci[1])
                                sum_list.bfast =  to_decimal(sum_list.bfast) + to_decimal(cl_list.bfast)

                        elif artikel.zwkum == lunch_art and (artikel.umsatzart == 3 or artikel.umsatzart >= 5):

                            if not exc_taxserv:
                                cl_list.lunch =  to_decimal(genstat.res_deci[2]) * to_decimal((1) + to_decimal(vat3) + to_decimal(serv2) )
                                sum_list.lunch =  to_decimal(sum_list.lunch) + to_decimal(cl_list.lunch)


                            else:
                                cl_list.lunch =  to_decimal(genstat.res_deci[2])
                                sum_list.lunch =  to_decimal(sum_list.lunch) + to_decimal(cl_list.lunch)

                        elif artikel.zwkum == dinner_art and (artikel.umsatzart == 3 or artikel.umsatzart >= 5):

                            if not exc_taxserv:
                                cl_list.dinner =  to_decimal(genstat.res_deci[3]) * to_decimal((1) + to_decimal(vat3) + to_decimal(serv2) )
                                sum_list.dinner =  to_decimal(sum_list.dinner) + to_decimal(cl_list.dinner)


                            else:
                                cl_list.dinner =  to_decimal(genstat.res_deci[3])
                                sum_list.dinner =  to_decimal(sum_list.dinner) + to_decimal(cl_list.dinner)

                        elif artikel.zwkum == lundin_art and (artikel.umsatzart == 3 or artikel.umsatzart >= 5):

                            if not exc_taxserv:
                                cl_list.lunch =  to_decimal(genstat.res_deci[2]) * to_decimal((1) + to_decimal(vat3) + to_decimal(serv2) )
                                sum_list.lunch =  to_decimal(sum_list.lunch) + to_decimal(cl_list.lunch)


                            else:
                                cl_list.lunch =  to_decimal(genstat.res_deci[2])
                                sum_list.lunch =  to_decimal(sum_list.lunch) + to_decimal(cl_list.lunch)


                        else:

                            if argt_betrag != 0:
                                pass

                    if not exc_taxserv:
                        cl_list.misc =  to_decimal(cl_list.localrate) - to_decimal((cl_list.lodging) + to_decimal(cl_list.bfast) + to_decimal(cl_list.lunch) + to_decimal(cl_list.dinner) )
                        sum_list.misc =  to_decimal(sum_list.misc) + to_decimal(cl_list.misc)


                    else:
                        cl_list.misc =  to_decimal(genstat.res_deci[4])
                        sum_list.misc =  to_decimal(sum_list.misc) + to_decimal(cl_list.misc)

                    if cl_list.misc < 0 and cl_list.misc > -1:
                        cl_list.misc =  to_decimal(0.00)

                htparam = get_cache (Htparam, {"paramnr": [(eq, 127)]})

                if htparam.flogical and not exc_taxserv:
                    cl_list.zipreis = to_decimal(round(cl_list.zipreis , price_decimal))
                    cl_list.lodging = to_decimal(round(cl_list.lodging , price_decimal))
                    cl_list.bfast = to_decimal(round(cl_list.bfast , price_decimal))
                    cl_list.lunch = to_decimal(round(cl_list.lunch , price_decimal))
                    cl_list.dinner = to_decimal(round(cl_list.dinner , price_decimal))
                    cl_list.misc = to_decimal(round(cl_list.misc , price_decimal))
                    cl_list.fixcost = to_decimal(round(cl_list.fixcost , price_decimal))
                    cl_list.localrate = to_decimal(round(cl_list.localrate , price_decimal))
                    cl_list.t_rev = to_decimal(round(cl_list.t_rev , price_decimal))

                if matches(res_line.zimmer_wunsch,r"*$CODE$*"):
                    s = substring(res_line.zimmer_wunsch, (get_index(res_line.zimmer_wunsch, "$CODE$") + 6) - 1)
                    cl_list.ratecode = trim(entry(0, s, ";"))

                if frate == 1:
                    cl_list.ex_rate = to_string(frate, " >>9.99")

                elif frate <= 999:
                    cl_list.ex_rate = to_string(frate, " >>9.9999")

                elif frate <= 99999:
                    cl_list.ex_rate = to_string(frate, ">>,>>9.99")
                else:
                    cl_list.ex_rate = to_string(frate, ">,>>>,>>9")

                reslin_queasy = get_cache (Reslin_queasy, {"key": [(eq, "arrangement")],"resnr": [(eq, res_line.resnr)],"reslinnr": [(eq, res_line.reslinnr)],"date1": [(le, curr_date)],"date2": [(ge, curr_date)]})

                if reslin_queasy:
                    cl_list.fix_rate = "F"


                tot_rate =  to_decimal(tot_rate) + to_decimal(cl_list.zipreis)
                tot_lrate =  to_decimal(tot_lrate) + to_decimal(cl_list.localrate)

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
                         (Argt_line.argtnr == arrangement.argtnr) & not_ (Argt_line.kind2) & (Argt_line.kind1)).order_by(Argt_line.argtnr, Argt_line.argt_artnr).all():

                    t_argt_line = query(t_argt_line_data, filters=(lambda t_argt_line: t_argt_line.argt_artnr == argt_line.argt_artnr and t_argt_line.argtnr == arrangement.argtnr and t_argt_line.departement == argt_line.departement), first=True)

                    if not t_argt_line:
                        t_argt_line = T_argt_line()
                        t_argt_line_data.append(t_argt_line)

                        buffer_copy(argt_line, t_argt_line)

                if genstat.zipreis != 0:

                    if bill_flag1.lower()  == ("Master Bill").lower() :

                        billjournal_obj_list = {}
                        billjournal = Billjournal()
                        artikel = Artikel()
                        for billjournal.rechnr, billjournal.artnr, billjournal.departement, billjournal.bezeich, billjournal.fremdwaehrng, billjournal.betrag, billjournal._recid, artikel.artnr, artikel.departement, artikel.umsatzart, artikel.zwkum, artikel._recid in db_session.query(Billjournal.rechnr, Billjournal.artnr, Billjournal.departement, Billjournal.bezeich, Billjournal.fremdwaehrng, Billjournal.betrag, Billjournal._recid, Artikel.artnr, Artikel.departement, Artikel.umsatzart, Artikel.zwkum, Artikel._recid).join(Artikel,(Artikel.artnr == Billjournal.artnr) & (Artikel.departement == Billjournal.departement) & (Artikel.artart != 9)).filter(
                                 (Billjournal.rechnr == bill_master) & (Billjournal.bill_datum == genstat.datum) & (Billjournal.zinr == genstat.zinr) & (Billjournal.betrag != 0) & (Billjournal.anzahl != 0) & not_ (Billjournal.kassarapport) & (Billjournal.userinit == ("$$").lower())).order_by(Billjournal.sysdate, Billjournal.bill_datum, Billjournal.zinr).all():
                            if billjournal_obj_list.get(billjournal._recid):
                                continue
                            else:
                                billjournal_obj_list[billjournal._recid] = True

                            if billjournal.artnr != deposit_art:

                                s_list = query(s_list_data, filters=(lambda s_list: s_list.artnr == billjournal.artnr and s_list.dept == billjournal.departement and s_list.curr == waehrung1.wabkurz), first=True)

                                if not s_list:
                                    s_list = S_list()
                                    s_list_data.append(s_list)

                                    s_list.artnr = billjournal.artnr
                                    s_list.dept = billjournal.departement
                                    s_list.bezeich = billjournal.bezeich
                                    s_list.curr = waehrung1.wabkurz


                                s_list.f_betrag =  to_decimal(s_list.f_betrag) + to_decimal(billjournal.fremdwaehrng)
                                s_list.l_betrag =  to_decimal(s_list.l_betrag) + to_decimal(billjournal.betrag)


                        bill_master = -1

                    if bill_flag2.lower()  == ("Guest Bill").lower() :

                        billjournal_obj_list = {}
                        billjournal = Billjournal()
                        artikel = Artikel()
                        for billjournal.rechnr, billjournal.artnr, billjournal.departement, billjournal.bezeich, billjournal.fremdwaehrng, billjournal.betrag, billjournal._recid, artikel.artnr, artikel.departement, artikel.umsatzart, artikel.zwkum, artikel._recid in db_session.query(Billjournal.rechnr, Billjournal.artnr, Billjournal.departement, Billjournal.bezeich, Billjournal.fremdwaehrng, Billjournal.betrag, Billjournal._recid, Artikel.artnr, Artikel.departement, Artikel.umsatzart, Artikel.zwkum, Artikel._recid).join(Artikel,(Artikel.artnr == Billjournal.artnr) & (Artikel.departement == Billjournal.departement) & (Artikel.artart != 9)).filter(
                                 (Billjournal.rechnr == bill_rechnr) & (Billjournal.bill_datum == genstat.datum) & (Billjournal.zinr == genstat.zinr) & (Billjournal.betrag != 0) & (Billjournal.anzahl != 0) & not_ (Billjournal.kassarapport) & (Billjournal.userinit == ("$$").lower())).order_by(Billjournal.sysdate, Billjournal.bill_datum, Billjournal.zinr).all():
                            if billjournal_obj_list.get(billjournal._recid):
                                continue
                            else:
                                billjournal_obj_list[billjournal._recid] = True

                            if billjournal.artnr != deposit_art:

                                s_list = query(s_list_data, filters=(lambda s_list: s_list.artnr == billjournal.artnr and s_list.dept == billjournal.departement and s_list.curr == waehrung1.wabkurz), first=True)

                                if not s_list:
                                    s_list = S_list()
                                    s_list_data.append(s_list)

                                    s_list.artnr = billjournal.artnr
                                    s_list.dept = billjournal.departement
                                    s_list.bezeich = billjournal.bezeich
                                    s_list.curr = waehrung1.wabkurz


                                s_list.f_betrag =  to_decimal(s_list.f_betrag) + to_decimal(billjournal.fremdwaehrng)
                                s_list.l_betrag =  to_decimal(s_list.l_betrag) + to_decimal(billjournal.betrag)


                        bill_rechnr = -1

                if res_line.adrflag:
                    ltot_lodging =  to_decimal(ltot_lodging) + to_decimal(cl_list.lodging)
                else:
                    tot_lodging =  to_decimal(tot_lodging) + to_decimal(cl_list.lodging)
                lodge_betrag =  to_decimal(cl_list.lodging)

                if foreign_rate and price_decimal == 0 and not res_line.adrflag:

                    htparam = get_cache (Htparam, {"paramnr": [(eq, 145)]})

                    if htparam.finteger != 0:
                        m = 1
                        for j in range(1,htparam.finteger + 1) :
                            m = m * 10
                        lodge_betrag = to_decimal(round(lodge_betrag / m , 0) * m)

                if curr_zinr != res_line.zinr or curr_resnr != res_line.resnr:

                    if res_line.adrflag:
                        ltot_rm = ltot_rm + 1
                    else:
                        tot_rm = tot_rm + 1
                curr_zinr = res_line.zinr
                curr_resnr = res_line.resnr
        cl_list = Cl_list()
        cl_list_data.append(cl_list)

        cl_list.flag = "*"
        cl_list.zinr = ""
        cl_list.c_zipreis = "s U m m A R Y:"


        curr_code = ""
        curr_rate =  to_decimal("0")
        curr_local =  to_decimal("0")
        curr_lodge =  to_decimal("0")
        curr_bfast =  to_decimal("0")
        curr_lunch =  to_decimal("0")
        curr_dinner =  to_decimal("0")
        curr_misc =  to_decimal("0")
        curr_fcost =  to_decimal("0")
        curr_trev =  to_decimal("0")
        curr_pax = 0
        curr_com = 0
        curr_rm = 0
        curr_adult = 0
        curr_ch1 = 0
        curr_ch2 = 0
        curr_comch = 0

        for cc_list in query(cc_list_data, filters=(lambda cc_list: cc_list.flag == ""), sort_by=[("currency",False)]):

            if curr_code != cc_list.currency:

                if curr_code != "":
                    cl_list.zipreis =  to_decimal(curr_rate)
                    cl_list.localrate =  to_decimal(curr_local)
                    cl_list.lodging =  to_decimal(curr_lodge)
                    cl_list.bfast =  to_decimal(curr_bfast)
                    cl_list.lunch =  to_decimal(curr_lunch)
                    cl_list.dinner =  to_decimal(curr_dinner)
                    cl_list.misc =  to_decimal(curr_misc)
                    cl_list.fixcost =  to_decimal(curr_fcost)
                    cl_list.t_rev =  to_decimal(curr_trev)
                    cl_list.pax = curr_pax
                    cl_list.com = curr_com
                    cl_list.zinr = to_string(curr_rm, ">>>9")
                    cl_list.adult = curr_adult
                    cl_list.ch1 = curr_ch1
                    cl_list.ch2 = curr_ch2
                    cl_list.comch = curr_comch

                waehrung = get_cache (Waehrung, {"wabkurz": [(eq, cc_list.currency)]})

                if (waehrung.ankauf / waehrung.einheit) != 1:
                    currency_list = Currency_list()
                    currency_list_data.append(currency_list)

                    currency_list.code = cc_list.currency
                cl_list = Cl_list()
                cl_list_data.append(cl_list)

                cl_list.flag = "**"
                cl_list.currency = cc_list.currency
                curr_code = cc_list.currency
                curr_rate =  to_decimal("0")
                curr_local =  to_decimal("0")
                curr_lodge =  to_decimal("0")
                curr_bfast =  to_decimal("0")
                curr_lunch =  to_decimal("0")
                curr_dinner =  to_decimal("0")
                curr_misc =  to_decimal("0")
                curr_fcost =  to_decimal("0")
                curr_trev =  to_decimal("0")
                curr_pax = 0
                curr_com = 0
                curr_rm = 0
                curr_adult = 0
                curr_ch1 = 0
                curr_ch2 = 0
                curr_comch = 0
            curr_rate =  to_decimal(curr_rate) + to_decimal(cc_list.zipreis)
            curr_local =  to_decimal(curr_local) + to_decimal(cc_list.localrate)
            curr_lodge =  to_decimal(curr_lodge) + to_decimal(cc_list.lodging)
            curr_bfast =  to_decimal(curr_bfast) + to_decimal(cc_list.bfast)
            curr_lunch =  to_decimal(curr_lunch) + to_decimal(cc_list.lunch)
            curr_dinner =  to_decimal(curr_dinner) + to_decimal(cc_list.dinner)
            curr_misc =  to_decimal(curr_misc) + to_decimal(cc_list.misc)
            curr_fcost =  to_decimal(curr_fcost) + to_decimal(cc_list.fixcost)
            curr_trev =  to_decimal(curr_trev) + to_decimal(cc_list.t_rev)
            curr_pax = curr_pax + cc_list.pax
            curr_com = curr_com + cc_list.com
            curr_adult = curr_adult + cc_list.adult
            curr_ch1 = curr_ch1 + cc_list.ch1
            curr_ch2 = curr_ch2 + cc_list.ch2
            curr_comch = curr_comch + cc_list.comch

            if cc_list.rstatus != 13:
                curr_rm = curr_rm + 1
        cl_list.zipreis =  to_decimal(curr_rate)
        cl_list.localrate =  to_decimal(curr_local)
        cl_list.lodging =  to_decimal(curr_lodge)
        cl_list.bfast =  to_decimal(curr_bfast)
        cl_list.lunch =  to_decimal(curr_lunch)
        cl_list.dinner =  to_decimal(curr_dinner)
        cl_list.misc =  to_decimal(curr_misc)
        cl_list.fixcost =  to_decimal(curr_fcost)
        cl_list.t_rev =  to_decimal(curr_trev)
        cl_list.pax = curr_pax
        cl_list.com = curr_com
        cl_list.zinr = to_string(curr_rm, ">>>9")
        cl_list.adult = curr_adult
        cl_list.ch1 = curr_ch1
        cl_list.ch2 = curr_ch2
        cl_list.comch = curr_comch

        for cl_list in query(cl_list_data, filters=(lambda cl_list: cl_list.flag.lower()  != ("*").lower())):

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

            argt_list = query(argt_list_data, filters=(lambda argt_list: argt_list.argtcode == cl_list.argt), first=True)

            if argt_list:
                argt_list.bfast =  to_decimal(argt_list.bfast) + to_decimal(cl_list.bfast)

        if exc_taxserv:

            for s_list in query(s_list_data):
                s_list.f_betrag = to_decimal(round((s_list.f_betrag / (1 + vat1 + vat2 + serv1)) , price_decimal))
                s_list.l_betrag = to_decimal(round((s_list.l_betrag / (1 + vat1 + vat2 + serv1)) , price_decimal))

            for sum_list in query(sum_list_data):
                sum_list.lodging = to_decimal(round((sum_list.lodging / (1 + vat1 + vat2 + serv1)) , price_decimal))
                sum_list.bfast = to_decimal(round((sum_list.bfast / (1 + vat1 + vat2 + serv1)) , price_decimal))
                sum_list.lunch = to_decimal(round((sum_list.lunch / (1 + vat1 + vat2 + serv1)) , price_decimal))
                sum_list.dinner = to_decimal(round((sum_list.dinner / (1 + vat1 + vat2 + serv1)) , price_decimal))
                sum_list.misc = to_decimal(round((sum_list.misc / (1 + vat1 + vat2 + serv1)) , price_decimal))
                sum_list.fixcost = to_decimal(round((sum_list.fixcost / (1 + vat1 + vat2 + serv1)) , price_decimal))
                sum_list.t_rev = to_decimal(round((sum_list.t_rev / (1 + vat1 + vat2 + serv1)) , price_decimal))


        total_rev =  to_decimal(tot_rate)


    def get_argtline_rate(contcode:string, argt_recid:int):

        nonlocal cl_list_data, currency_list_data, sum_list_data, s_list_data, argt_list_data, exchg_rate, frate, post_it, total_rev, rm_rate, temptotjur, lvcarea, argt_line, waehrung, guest, artikel, htparam, res_line, zimmer, genstat, arrangement, exrate, reservation, billjournal, bill, zimkateg, segment, reslin_queasy
        nonlocal exc_taxserv, pvilanguage, new_contrate, foreign_rate, price_decimal, curr_date, srttype
        nonlocal waehrung1, cc_list


        nonlocal sum_list, currency_list, cl_list, s_list, argt_list, t_argt_line, waehrung1, cc_list
        nonlocal sum_list_data, currency_list_data, cl_list_data, s_list_data, argt_list_data, t_argt_line_data

        add_it = False
        f_betrag = to_decimal("0.0")
        argt_betrag = to_decimal("0.0")
        qty = 0
        curr_zikatnr:int = 0
        argtline = None

        def generate_inner_output():
            return (add_it, f_betrag, argt_betrag, qty)

        Argtline =  create_buffer("Argtline",Argt_line)

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

            reslin_queasy = get_cache (Reslin_queasy, {"key": [(eq, "fargt-line")],"char1": [(eq, "")],"resnr": [(eq, res_line.resnr)],"reslinnr": [(eq, res_line.reslinnr)],"number1": [(eq, argtline.departement)],"number2": [(eq, argtline.argtnr)],"number3": [(eq, argtline.argt_artnr)],"date1": [(le, curr_date)],"date2": [(ge, curr_date)]})

            if reslin_queasy:

                if argtline.vt_percnt == 0:
                    query = db_session.query(Reslin_queasy).filter((Reslin_queasy.key == 'fargt-line') & (Reslin_queasy.char1 == '') & (Reslin_queasy.number1 == argtline.departement) & (Reslin_queasy.number2 == argtline.argtnr) & (Reslin_queasy.resnr == res_line.resnr) & (Reslin_queasy.reslinnr == res_line.reslinnr) & (Reslin_queasy.number3 == argtline.argt_artnr) & (Reslin_queasy.date1 <= curr_date) & (Reslin_queasy.date2 >= curr_date) & (Reslin_queasy.deci1 != 0))

                elif argtline.vt_percnt == 1:
                    query = db_session.query(Reslin_queasy).filter((Reslin_queasy.key == 'fargt-line') & (Reslin_queasy.char1 == '') & (Reslin_queasy.number1 == argtline.departement) & (Reslin_queasy.number2 == argtline.argtnr) & (Reslin_queasy.resnr == res_line.resnr) & (Reslin_queasy.reslinnr == res_line.reslinnr) & (Reslin_queasy.number3 == argtline.argt_artnr) & (Reslin_queasy.date1 <= curr_date) & (Reslin_queasy.date2 >= curr_date) & (Reslin_queasy.deci2 != 0))

                elif argtline.vt_percnt == 2:
                    query = db_session.query(Reslin_queasy).filter((Reslin_queasy.key == 'fargt-line') & (Reslin_queasy.char1 == '') & (Reslin_queasy.number1 == argtline.departement) & (Reslin_queasy.number2 == argtline.argtnr) & (Reslin_queasy.resnr == res_line.resnr) & (Reslin_queasy.reslinnr == res_line.reslinnr) & (Reslin_queasy.number3 == argtline.argt_artnr) & (Reslin_queasy.date1 <= curr_date) & (Reslin_queasy.date2 >= curr_date) & (Reslin_queasy.deci3 != 0))

                for reslin_queasy in query.all():
                    if reslin_queasy.char2.lower()  != "" and reslin_queasy.char2.lower()  != ("0").lower() :
                        argt_betrag = ( to_decimal(res_line.zipreis) * to_decimal(to_int(reslin_queasy.char2)) / to_decimal(100)) * to_decimal(qty)
                    else:
                        if argt_line.vt_percnt == 0:
                            argt_betrag =  to_decimal(reslin_queasy.deci1) * to_decimal(qty)

                        elif argt_line.vt_percnt == 1:
                            argt_betrag =  to_decimal(reslin_queasy.deci2) * to_decimal(qty)

                        elif argt_line.vt_percnt == 2:
                            argt_betrag =  to_decimal(reslin_queasy.deci3) * to_decimal(qty)

                    f_betrag =  to_decimal(argt_betrag)

                    waehrung = get_cache (Waehrung, {"_recid": [(eq, waehrung1._recid)]})

                    if argt_betrag == 0:
                        add_it = False
                    else:
                        return generate_inner_output()

            if contcode != "":

                reslin_queasy = get_cache (Reslin_queasy, {"key": [(eq, "argt-line")],"char1": [(eq, contcode)],"number1": [(eq, res_line.reserve_int)],"number2": [(eq, arrangement.argtnr)],"number3": [(eq, argtline.argt_artnr)],"resnr": [(eq, argtline.departement)],"reslinnr": [(eq, curr_zikatnr)],"date1": [(le, curr_date)],"date2": [(ge, curr_date)]})

                if reslin_queasy:
                    if argt_line.vt_percnt == 0:
                        query = db_session.query(Reslin_queasy).filter((Reslin_queasy.key == 'argt-line') & (Reslin_queasy.char1 == contcode) & (Reslin_queasy.number1 == res_line.reserve_int) & (Reslin_queasy.number2 == arrangement.argtnr) & (Reslin_queasy.number3 == argtline.argt_artnr) & (Reslin_queasy.resnr == argtline.departement) & (Reslin_queasy.reslinnr == curr_zikatnr) & (Reslin_queasy.date1 <= curr_date) & (Reslin_queasy.date2 >= curr_date) & (Reslin_queasy.deci1 != 0))

                    elif argt_line.vt_percnt == 1:
                        query = db_session.query(Reslin_queasy).filter((Reslin_queasy.key == 'argt-line') & (Reslin_queasy.char1 == contcode) & (Reslin_queasy.number1 == res_line.reserve_int) & (Reslin_queasy.number2 == arrangement.argtnr) & (Reslin_queasy.number3 == argtline.argt_artnr) & (Reslin_queasy.resnr == argtline.departement) & (Reslin_queasy.reslinnr == curr_zikatnr) & (Reslin_queasy.date1 <= curr_date) & (Reslin_queasy.date2 >= curr_date) & (Reslin_queasy.deci2 != 0))

                    elif argt_line.vt_percnt == 2:
                        query = db_session.query(Reslin_queasy).filter((Reslin_queasy.key == 'argt-line') & (Reslin_queasy.char1 == contcode) & (Reslin_queasy.number1 == res_line.reserve_int) & (Reslin_queasy.number2 == arrangement.argtnr) & (Reslin_queasy.number3 == argtline.argt_artnr) & (Reslin_queasy.resnr == argtline.departement) & (Reslin_queasy.reslinnr == curr_zikatnr) & (Reslin_queasy.date1 <= curr_date) & (Reslin_queasy.date2 >= curr_date) & (Reslin_queasy.deci3 != 0))

                    for reslin_queasy in query.all():
                        if argt_line.vt_percnt == 0:
                            argt_betrag =  to_decimal(reslin_queasy.deci1) * to_decimal(qty)

                        elif argt_line.vt_percnt == 1:
                            argt_betrag =  to_decimal(reslin_queasy.deci2) * to_decimal(qty)

                        elif argt_line.vt_percnt == 2:
                            argt_betrag =  to_decimal(reslin_queasy.deci3) * to_decimal(qty)
                        f_betrag =  to_decimal(argt_betrag)

                        waehrung = get_cache (Waehrung, {"_recid": [(eq, waehrung1._recid)]})

                        if argt_betrag == 0:
                            add_it = False
                        else:
                            return generate_inner_output()

            argt_betrag =  to_decimal(argt_line.betrag)

            arrangement = get_cache (Arrangement, {"argtnr": [(eq, argt_line.argtnr)]})

            waehrung = get_cache (Waehrung, {"waehrungsnr": [(eq, arrangement.betriebsnr)]})
            f_betrag =  to_decimal(argt_betrag) * to_decimal(qty)

            if res_line.betriebsnr != arrangement.betriebsnr:
                argt_betrag =  to_decimal(argt_betrag) * to_decimal((waehrung.ankauf) / to_decimal(waehrung.einheit)) / to_decimal(frate)

            if argt_betrag > 0:
                argt_betrag =  to_decimal(argt_betrag) * to_decimal(qty)
            else:
                argt_betrag = ( to_decimal(rm_rate) * to_decimal((argt_betrag) / to_decimal(100))) * to_decimal(qty)
                argt_betrag =  -1 * to_decimal(argt_betrag)

            if argt_betrag != 0:
                add_it = True

        return generate_inner_output()


    def get_genstat_argt_betrag(f_rate:Decimal, argt_betrag:Decimal):

        nonlocal cl_list_data, currency_list_data, sum_list_data, s_list_data, argt_list_data, exchg_rate, frate, post_it, total_rev, rm_rate, temptotjur, lvcarea, argt_line, waehrung, guest, artikel, htparam, res_line, zimmer, genstat, arrangement, exrate, reservation, billjournal, bill, zimkateg, segment, reslin_queasy
        nonlocal exc_taxserv, pvilanguage, new_contrate, foreign_rate, price_decimal, curr_date, srttype
        nonlocal waehrung1, cc_list


        nonlocal sum_list, currency_list, cl_list, s_list, argt_list, t_argt_line, waehrung1, cc_list
        nonlocal sum_list_data, currency_list_data, cl_list_data, s_list_data, argt_list_data, t_argt_line_data

        tokcounter:int = 0
        mestoken:string = ""
        curr_artnr:int = 0
        curr_dept:int = 0
        a_betrag:Decimal = to_decimal("0.0")
        x_betrag:Decimal = to_decimal("0.0")

        def generate_inner_output():
            return (argt_betrag)


        if genstat.res_char[3] == "":

            return generate_inner_output()
        for tokcounter in range(1,num_entries(genstat.res_char[3], ";")  + 1) :
            mestoken = trim(entry(tokcounter - 1, genstat.res_char[3], ";"))

            if mestoken != "":
                curr_artnr = to_int(entry(0, mestoken, ","))
                curr_dept = to_int(entry(1, mestoken, ","))
                a_betrag =  to_decimal(to_decimal(entry(2 , mestoken , ","))) * to_decimal(0.01)
                x_betrag =  to_decimal(to_decimal(entry(3 , mestoken , ","))) * to_decimal(0.01)

                if curr_artnr == argt_line.argt_artnr and curr_dept == argt_line.departement:
                    argt_betrag =  to_decimal(a_betrag) * to_decimal(x_betrag) / to_decimal(f_rate)

                    return generate_inner_output()

        return generate_inner_output()


    def check_fixleist_posted(artnr:int, dept:int, fakt_modus:int, intervall:int, lfakt:date):

        nonlocal cl_list_data, currency_list_data, sum_list_data, s_list_data, argt_list_data, exchg_rate, frate, post_it, total_rev, rm_rate, temptotjur, lvcarea, argt_line, waehrung, guest, artikel, htparam, res_line, zimmer, genstat, arrangement, exrate, reservation, billjournal, bill, zimkateg, segment, reslin_queasy
        nonlocal exc_taxserv, pvilanguage, new_contrate, foreign_rate, price_decimal, curr_date, srttype
        nonlocal waehrung1, cc_list


        nonlocal sum_list, currency_list, cl_list, s_list, argt_list, t_argt_line, waehrung1, cc_list
        nonlocal sum_list_data, currency_list_data, cl_list_data, s_list_data, argt_list_data, t_argt_line_data

        post_it = False
        delta:int = 0
        start_date:date = None

        def generate_inner_output():
            return (post_it)


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
                delta = (lfakt - res_line.ankunft).days

                if delta < 0:
                    delta = 0
            start_date = res_line.ankunft + timedelta(days=delta)

            if (res_line.abreise - start_date) < intervall:
                start_date = res_line.ankunft

            if curr_date <= (start_date + timedelta(days=(intervall - 1))):
                post_it = True

            if curr_date < start_date:
                post_it = False

        return generate_inner_output()


    create_billbalance1()

    return generate_output()