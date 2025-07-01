#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from functions.calc_servtaxesbl import calc_servtaxesbl
from functions.ratecode_seek import ratecode_seek
from models import Waehrung, Guest, Artikel, Htparam, Zimmer, Res_line, Arrangement, Reservation, Bill, Reslin_queasy, Guest_pr, Pricecod, Argt_line, Fixleist

def rmrev_bdown_create_billbalance_1bl(exc_taxserv:bool, pvilanguage:int, new_contrate:bool, foreign_rate:bool, price_decimal:int, curr_date:date):

    prepare_cache ([Waehrung, Guest, Artikel, Htparam, Zimmer, Res_line, Arrangement, Bill, Reslin_queasy, Guest_pr, Pricecod, Argt_line, Fixleist])

    msg_str = ""
    msg_warning = ""
    cl_list_list = []
    currency_list_list = []
    sum_list_list = []
    s_list_list = []
    exchg_rate:Decimal = 1
    frate:Decimal = to_decimal("0.0")
    post_it:bool = False
    total_rev:Decimal = to_decimal("0.0")
    rm_rate:Decimal = to_decimal("0.0")
    lvcarea:string = "rmrev-bdown"
    waehrung = guest = artikel = htparam = zimmer = res_line = arrangement = reservation = bill = reslin_queasy = guest_pr = pricecod = argt_line = fixleist = None

    sum_list = currency_list = cl_list = s_list = waehrung1 = cc_list = None

    sum_list_list, Sum_list = create_model("Sum_list", {"bezeich":string, "pax":int, "adult":int, "ch1":int, "ch2":int, "comch":int, "com":int, "lodging":Decimal, "bfast":Decimal, "lunch":Decimal, "dinner":Decimal, "misc":Decimal, "fixcost":Decimal, "t_rev":Decimal})
    currency_list_list, Currency_list = create_model("Currency_list", {"code":string})
    cl_list_list, Cl_list = create_model("Cl_list", {"zipreis":Decimal, "localrate":Decimal, "lodging":Decimal, "bfast":Decimal, "lunch":Decimal, "dinner":Decimal, "misc":Decimal, "fixcost":Decimal, "t_rev":Decimal, "c_zipreis":string, "c_localrate":string, "c_lodging":string, "c_bfast":string, "c_lunch":string, "c_dinner":string, "c_misc":string, "c_fixcost":string, "ct_rev":string, "res_recid":int, "sleeping":bool, "row_disp":int, "flag":string, "zinr":string, "rstatus":int, "argt":string, "currency":string, "ratecode":string, "pax":int, "com":int, "ankunft":date, "abreise":date, "rechnr":int, "name":string, "ex_rate":string, "fix_rate":string, "adult":int, "ch1":int, "ch2":int, "comch":int, "age1":int, "age2":string, "rmtype":string}, {"sleeping": True})
    s_list_list, S_list = create_model("S_list", {"artnr":int, "dept":int, "bezeich":string, "curr":string, "anzahl":int, "betrag":Decimal, "l_betrag":Decimal, "f_betrag":Decimal})

    Waehrung1 = create_buffer("Waehrung1",Waehrung)
    Cc_list = Cl_list
    cc_list_list = cl_list_list

    db_session = local_storage.db_session

    def generate_output():
        nonlocal msg_str, msg_warning, cl_list_list, currency_list_list, sum_list_list, s_list_list, exchg_rate, frate, post_it, total_rev, rm_rate, lvcarea, waehrung, guest, artikel, htparam, zimmer, res_line, arrangement, reservation, bill, reslin_queasy, guest_pr, pricecod, argt_line, fixleist
        nonlocal exc_taxserv, pvilanguage, new_contrate, foreign_rate, price_decimal, curr_date
        nonlocal waehrung1, cc_list


        nonlocal sum_list, currency_list, cl_list, s_list, waehrung1, cc_list
        nonlocal sum_list_list, currency_list_list, cl_list_list, s_list_list

        return {"msg_str": msg_str, "msg_warning": msg_warning, "cl-list": cl_list_list, "currency-list": currency_list_list, "sum-list": sum_list_list, "s-list": s_list_list}

    def create_billbalance():

        nonlocal msg_str, msg_warning, cl_list_list, currency_list_list, sum_list_list, s_list_list, exchg_rate, frate, post_it, total_rev, rm_rate, lvcarea, waehrung, guest, artikel, htparam, zimmer, res_line, arrangement, reservation, bill, reslin_queasy, guest_pr, pricecod, argt_line, fixleist
        nonlocal exc_taxserv, pvilanguage, new_contrate, foreign_rate, price_decimal, curr_date
        nonlocal waehrung1, cc_list


        nonlocal sum_list, currency_list, cl_list, s_list, waehrung1, cc_list
        nonlocal sum_list_list, currency_list_list, cl_list_list, s_list_list

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
        serv:Decimal = to_decimal("0.0")
        vat2:Decimal = to_decimal("0.0")
        fact:Decimal = to_decimal("0.0")
        curr_zikatnr:int = 0
        artikel1 = None
        loopi:int = 0
        i:int = 0
        n:int = 0
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

        artikel = get_cache (Artikel, {"zwkum": [(eq, bfast_art)],"departement": [(eq, fb_dept)]})

        if not artikel and bfast_art != 0:
            msg_str = translateExtended ("B'fast SubGrp not yed defined (Grp 7)", lvcarea, "")

            return

        htparam = get_cache (Htparam, {"paramnr": [(eq, 227)]})
        lunch_art = htparam.finteger

        artikel = get_cache (Artikel, {"zwkum": [(eq, lunch_art)],"departement": [(eq, fb_dept)]})

        if not artikel and lunch_art != 0:
            msg_str = translateExtended ("Lunch SubGrp not yed defined (Grp 7)", lvcarea, "")

            return

        htparam = get_cache (Htparam, {"paramnr": [(eq, 228)]})
        dinner_art = htparam.finteger

        artikel = get_cache (Artikel, {"zwkum": [(eq, dinner_art)],"departement": [(eq, fb_dept)]})

        if not artikel and dinner_art != 0:
            msg_str = translateExtended ("Dinner SubGrp not yed defined (Grp 7)", lvcarea, "")

            return

        htparam = get_cache (Htparam, {"paramnr": [(eq, 229)]})
        lundin_art = htparam.finteger

        artikel = get_cache (Artikel, {"zwkum": [(eq, lundin_art)],"departement": [(eq, fb_dept)]})

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
        lodge_betrag =  to_decimal("0")

        res_line_obj_list = {}
        res_line = Res_line()
        zimmer = Zimmer()
        for res_line.arrangement, res_line.betriebsnr, res_line.gastnrpay, res_line.gastnrmember, res_line.resnr, res_line.l_zuordnung, res_line.zikatnr, res_line.reslinnr, res_line.zinr, res_line.name, res_line.erwachs, res_line.gratis, res_line._recid, res_line.resstatus, res_line.ankunft, res_line.abreise, res_line.zipreis, res_line.kind1, res_line.kind2, res_line.zimmer_wunsch, res_line.gastnr, res_line.reserve_int, res_line.adrflag, res_line.reserve_dec, zimmer.sleeping, zimmer._recid in db_session.query(Res_line.arrangement, Res_line.betriebsnr, Res_line.gastnrpay, Res_line.gastnrmember, Res_line.resnr, Res_line.l_zuordnung, Res_line.zikatnr, Res_line.reslinnr, Res_line.zinr, Res_line.name, Res_line.erwachs, Res_line.gratis, Res_line._recid, Res_line.resstatus, Res_line.ankunft, Res_line.abreise, Res_line.zipreis, Res_line.kind1, Res_line.kind2, Res_line.zimmer_wunsch, Res_line.gastnr, Res_line.reserve_int, Res_line.adrflag, Res_line.reserve_dec, Zimmer.sleeping, Zimmer._recid).join(Zimmer,(Zimmer.zinr == Res_line.zinr)).filter(
                 ((Res_line.active_flag == 1) & (Res_line.resstatus == 6)) & (Res_line.l_zuordnung[inc_value(2)] == 0)).order_by(Res_line.zinr, Res_line.resnr).all():
            if res_line_obj_list.get(res_line._recid):
                continue
            else:
                res_line_obj_list[res_line._recid] = True

            arrangement = get_cache (Arrangement, {"arrangement": [(eq, res_line.arrangement)]})

            artikel = get_cache (Artikel, {"artnr": [(eq, arrangement.argt_artikelnr)],"departement": [(eq, 0)]})
            serv =  to_decimal("0")
            vat =  to_decimal("0")
            vat2 =  to_decimal("0")
            fact =  to_decimal("0")


            service, vat, vat2, fact = get_output(calc_servtaxesbl(1, artikel.artnr, artikel.departement, curr_date))

            waehrung1 = get_cache (Waehrung, {"waehrungsnr": [(eq, res_line.betriebsnr)]})
            exchg_rate =  to_decimal(waehrung1.ankauf) / to_decimal(waehrung1.einheit)

            if res_line.reserve_dec != 0:
                frate =  to_decimal(reserve_dec)
            else:
                frate =  to_decimal(exchg_rate)

            if res_line.zipreis != 0:
                r_qty = r_qty + 1

            guest = get_cache (Guest, {"gastnr": [(eq, res_line.gastnrpay)]})

            member1 = get_cache (Guest, {"gastnr": [(eq, res_line.gastnrmember)]})

            reservation = get_cache (Reservation, {"resnr": [(eq, res_line.resnr)]})

            if res_line.l_zuordnung[0] != 0:
                curr_zikatnr = res_line.l_zuordnung[0]
            else:
                curr_zikatnr = res_line.zikatnr

            bill = get_cache (Bill, {"resnr": [(eq, res_line.resnr)],"reslinnr": [(eq, res_line.reslinnr)],"zinr": [(eq, res_line.zinr)]})

            if not bill:

                bill = get_cache (Bill, {"resnr": [(eq, res_line.resnr)],"reslinnr": [(eq, res_line.reslinnr)]})

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
            cl_list.zipreis =  to_decimal(res_line.zipreis)
            cl_list.localrate =  to_decimal(res_line.zipreis) * to_decimal(frate)
            cl_list.t_rev =  to_decimal(res_line.zipreis)


            cl_list.adult = res_line.erwachs
            cl_list.ch1 = res_line.kind1
            cl_list.ch2 = res_line.kind2
            cl_list.comch = res_line.l_zuordnung[3]

            if cl_list.zipreis == 0:
                cl_list.pax = res_line.gratis + cl_list.comch


            else:
                cl_list.pax = res_line.erwachs + res_line.kind1 + res_line.kind2 + res_line.gratis + cl_list.comch

            if guest:
                cl_list.name = cl_list.name + guest.name + ", " + guest.vorname1 + "-" + guest.adresse1
                cl_list.rechnr = bill.rechnr
                cl_list.currency = waehrung1.wabkurz

            if guest.geburtdatum1 != None and guest.geburtdatum2 != None:

                if guest.geburtdatum1 < guest.geburtdatum2:
                    cl_list.age1 = get_year(guest.geburtdatum2) - get_year(guest.geburtdatum1)

            if matches(res_line.zimmer_wunsch,r"*ChAge*"):
                for loopi in range(1,num_entries(res_line.zimmer_wunsch, ";") - 1 + 1) :
                    s = entry(loopi - 1, res_line.zimmer_wunsch, ";")

                    if substring(s, 0, 5) == ("ChAge").lower() :
                        cl_list.age2 = substring(s, 5)

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
            cl_list.lodging =  to_decimal(cl_list.zipreis)

            if cl_list.lodging != 0:
                prcode = 0
                contcode = ""

                rguest = get_cache (Guest, {"gastnr": [(eq, res_line.gastnr)]})

                if res_line.reserve_int != 0:

                    guest_pr = get_cache (Guest_pr, {"gastnr": [(eq, rguest.gastnr)]})

                if guest_pr:
                    contcode = guest_pr.code
                    ct = res_line.zimmer_wunsch

                    if matches(ct,r"*$CODE$*"):
                        ct = substring(ct, get_index(ct, "$CODE$") + 6 - 1)
                        contcode = substring(ct, 0, get_index(ct, ";") - 1)

                    if new_contrate:
                        prcode = get_output(ratecode_seek(res_line.resnr, res_line.reslinnr, contcode, curr_date))
                    else:

                        pricecod = get_cache (Pricecod, {"code": [(eq, contcode)],"marknr": [(eq, res_line.reserve_int)],"argtnr": [(eq, arrangement.argtnr)],"zikatnr": [(eq, curr_zikatnr)],"startperiode": [(le, curr_date)],"endperiode": [(ge, curr_date)]})

                        if pricecod:
                            prcode = pricecod._recid
                rm_rate =  to_decimal(res_line.zipreis)

                for argt_line in db_session.query(Argt_line).filter(
                         (Argt_line.argtnr == arrangement.argtnr) & not_ (Argt_line.kind2)).order_by(Argt_line._recid).all():

                    artikel = get_cache (Artikel, {"artnr": [(eq, argt_line.argt_artnr)],"departement": [(eq, argt_line.departement)]})

                    if not artikel:
                        take_it = False
                    else:
                        take_it, f_betrag, argt_betrag, qty = get_argtline_rate(contcode, argt_line._recid)

                    if take_it:

                        s_list = query(s_list_list, filters=(lambda s_list: s_list.artnr == argt_line.argt_artnr and s_list.dept == argt_line.departement and s_list.curr == waehrung.wabkurz), first=True)

                        if not s_list:
                            s_list = S_list()
                            s_list_list.append(s_list)

                            s_list.artnr = argt_line.argt_artnr
                            s_list.dept = argt_line.departement
                            s_list.bezeich = artikel.bezeich
                            s_list.curr = waehrung.wabkurz


                        s_list.f_betrag =  to_decimal(s_list.f_betrag) + to_decimal(f_betrag)
                        s_list.l_betrag =  to_decimal(s_list.l_betrag) + to_decimal(argt_betrag) * to_decimal(frate)
                        s_list.anzahl = s_list.anzahl + qty


                        sum_list.t_rev =  to_decimal(sum_list.t_rev) + to_decimal(argt_betrag) * to_decimal(frate)

                        if artikel.zwkum == bfast_art and (artikel.umsatzart == 3 or artikel.umsatzart >= 5):
                            sum_list.bfast =  to_decimal(sum_list.bfast) + to_decimal(argt_betrag) * to_decimal(frate)
                            cl_list.bfast =  to_decimal(cl_list.bfast) + to_decimal(argt_betrag)

                            if res_line.adrflag:
                                ltot_bfast =  to_decimal(ltot_bfast) + to_decimal(argt_betrag)
                            else:
                                tot_bfast =  to_decimal(tot_bfast) + to_decimal(argt_betrag)
                            cl_list.lodging =  to_decimal(cl_list.lodging) - to_decimal(argt_betrag)

                        elif artikel.zwkum == lunch_art and (artikel.umsatzart == 3 or artikel.umsatzart >= 5):
                            sum_list.lunch =  to_decimal(sum_list.lunch) + to_decimal(argt_betrag) * to_decimal(frate)
                            cl_list.lunch =  to_decimal(cl_list.lunch) + to_decimal(argt_betrag)

                            if res_line.adrflag:
                                ltot_lunch =  to_decimal(ltot_lunch) + to_decimal(argt_betrag)
                            else:
                                tot_lunch =  to_decimal(tot_lunch) + to_decimal(argt_betrag)
                            cl_list.lodging =  to_decimal(cl_list.lodging) - to_decimal(argt_betrag)

                        elif artikel.zwkum == dinner_art and (artikel.umsatzart == 3 or artikel.umsatzart >= 5):
                            sum_list.dinner =  to_decimal(sum_list.dinner) + to_decimal(argt_betrag) * to_decimal(frate)
                            cl_list.dinner =  to_decimal(cl_list.dinner) + to_decimal(argt_betrag)

                            if res_line.adrflag:
                                ltot_dinner =  to_decimal(ltot_dinner) + to_decimal(argt_betrag)
                            else:
                                tot_dinner =  to_decimal(tot_dinner) + to_decimal(argt_betrag)
                            cl_list.lodging =  to_decimal(cl_list.lodging) - to_decimal(argt_betrag)

                        elif artikel.zwkum == lundin_art and (artikel.umsatzart == 3 or artikel.umsatzart >= 5):
                            sum_list.lunch =  to_decimal(sum_list.lunch) + to_decimal(argt_betrag) * to_decimal(frate)
                            cl_list.lunch =  to_decimal(cl_list.lunch) + to_decimal(argt_betrag)

                            if res_line.adrflag:
                                ltot_lunch =  to_decimal(ltot_lunch) + to_decimal(argt_betrag)
                            else:
                                tot_lunch =  to_decimal(tot_lunch) + to_decimal(argt_betrag)
                            cl_list.lodging =  to_decimal(cl_list.lodging) - to_decimal(argt_betrag)
                        else:
                            sum_list.misc =  to_decimal(sum_list.misc) + to_decimal(argt_betrag) * to_decimal(frate)
                            cl_list.misc =  to_decimal(cl_list.misc) + to_decimal(argt_betrag)

                            if res_line.adrflag:
                                ltot_misc =  to_decimal(ltot_misc) + to_decimal(argt_betrag)
                            else:
                                tot_misc =  to_decimal(tot_misc) + to_decimal(argt_betrag)
                            cl_list.lodging =  to_decimal(cl_list.lodging) - to_decimal(argt_betrag)

            if res_line.adrflag:
                ltot_lodging =  to_decimal(ltot_lodging) + to_decimal(cl_list.lodging)
            else:
                tot_lodging =  to_decimal(tot_lodging) + to_decimal(cl_list.lodging)
            lodge_betrag =  to_decimal(cl_list.lodging) * to_decimal(frate)

            if foreign_rate and price_decimal == 0 and not res_line.adrflag:

                htparam = get_cache (Htparam, {"paramnr": [(eq, 145)]})

                if htparam.finteger != 0:
                    n = 1
                    for i in range(1,htparam.finteger + 1) :
                        n = n * 10
                    lodge_betrag = to_decimal(round(lodge_betrag / n , 0) * n)

            artikel1 = get_cache (Artikel, {"artnr": [(eq, arrangement.artnr_logis)],"departement": [(eq, 0)]})

            s_list = query(s_list_list, filters=(lambda s_list: s_list.artnr == artikel1.artnr and s_list.dept == artikel1.departement and s_list.curr == waehrung1.wabkurz), first=True)

            if not s_list:
                s_list = S_list()
                s_list_list.append(s_list)

                s_list.artnr = artikel1.artnr
                s_list.dept = artikel1.departement
                s_list.bezeich = artikel1.bezeich
                s_list.curr = waehrung1.wabkurz


            s_list.f_betrag =  to_decimal(s_list.f_betrag) + to_decimal(lodge_betrag) / to_decimal(frate)
            s_list.l_betrag =  to_decimal(s_list.l_betrag) + to_decimal(lodge_betrag)
            s_list.anzahl = s_list.anzahl + 1


            sum_list.lodging =  to_decimal(sum_list.lodging) + to_decimal(lodge_betrag)
            sum_list.t_rev =  to_decimal(sum_list.t_rev) + to_decimal(lodge_betrag)

            for fixleist in db_session.query(Fixleist).filter(
                     (Fixleist.resnr == res_line.resnr) & (Fixleist.reslinnr == res_line.reslinnr)).order_by(Fixleist._recid).all():
                post_it = check_fixleist_posted(fixleist.artnr, fixleist.departement, fixleist.sequenz, fixleist.dekade, fixleist.lfakt)

                if post_it:
                    fcost =  to_decimal(fixleist.betrag) * to_decimal(fixleist.number)
                    cl_list.t_rev =  to_decimal(cl_list.t_rev) + to_decimal(fcost)
                    sum_list.t_rev =  to_decimal(sum_list.t_rev) + to_decimal(fcost) * to_decimal(frate)

                    if res_line.adrflag:
                        ltot_rate =  to_decimal(ltot_rate) + to_decimal(fcost)
                    else:
                        tot_rate =  to_decimal(tot_rate) + to_decimal(fcost)

                    artikel = get_cache (Artikel, {"artnr": [(eq, fixleist.artnr)],"departement": [(eq, fixleist.departement)]})

                    s_list = query(s_list_list, filters=(lambda s_list: s_list.artnr == artikel.artnr and s_list.dept == artikel.departement and s_list.curr == waehrung1.wabkurz), first=True)

                    if not s_list:
                        s_list = S_list()
                        s_list_list.append(s_list)

                        s_list.artnr = artikel.artnr
                        s_list.dept = artikel.departement
                        s_list.bezeich = artikel.bezeich
                        s_list.curr = waehrung1.wabkurz

                    if (artikel.zwkum == bfast_art and artikel.departement == fb_dept):
                        s_list.f_betrag =  to_decimal(s_list.f_betrag) + to_decimal(fcost)
                        s_list.l_betrag =  to_decimal(s_list.l_betrag) + to_decimal(fcost) * to_decimal(frate)
                        s_list.anzahl = s_list.anzahl + fixleist.number
                        cl_list.bfast =  to_decimal(cl_list.bfast) + to_decimal(fcost)
                        sum_list.bfast =  to_decimal(sum_list.bfast) + to_decimal(fcost) * to_decimal(frate)

                        if res_line.adrflag:
                            ltot_bfast =  to_decimal(ltot_bfast) + to_decimal(fcost) * to_decimal(frate)
                        else:
                            tot_bfast =  to_decimal(tot_bfast) + to_decimal(fcost)

                    elif (artikel.zwkum == lunch_art and artikel.departement == fb_dept):
                        s_list.f_betrag =  to_decimal(s_list.f_betrag) + to_decimal(fcost)
                        s_list.l_betrag =  to_decimal(s_list.l_betrag) + to_decimal(fcost) * to_decimal(frate)
                        s_list.anzahl = s_list.anzahl + fixleist.number
                        cl_list.lunch =  to_decimal(cl_list.lunch) + to_decimal(fcost)
                        sum_list.lunch =  to_decimal(sum_list.lunch) + to_decimal(fcost) * to_decimal(frate)

                        if res_line.adrflag:
                            ltot_lunch =  to_decimal(ltot_lunch) + to_decimal(fcost) * to_decimal(frate)
                        else:
                            tot_lunch =  to_decimal(tot_lunch) + to_decimal(fcost)

                    elif (artikel.zwkum == dinner_art and artikel.departement == fb_dept):
                        s_list.f_betrag =  to_decimal(s_list.f_betrag) + to_decimal(fcost)
                        s_list.l_betrag =  to_decimal(s_list.l_betrag) + to_decimal(fcost) * to_decimal(frate)
                        s_list.anzahl = s_list.anzahl + fixleist.number
                        cl_list.dinner =  to_decimal(cl_list.dinner) + to_decimal(fcost)
                        sum_list.dinner =  to_decimal(sum_list.dinner) + to_decimal(fcost) * to_decimal(frate)

                        if res_line.adrflag:
                            ltot_dinner =  to_decimal(ltot_dinner) + to_decimal(fcost) * to_decimal(frate)
                        else:
                            tot_dinner =  to_decimal(tot_dinner) + to_decimal(fcost)
                    else:
                        s_list.f_betrag =  to_decimal(s_list.f_betrag) + to_decimal(fcost)
                        s_list.l_betrag =  to_decimal(s_list.l_betrag) + to_decimal(fcost) * to_decimal(frate)
                        s_list.anzahl = s_list.anzahl + fixleist.number
                        cl_list.fixcost =  to_decimal(cl_list.fixcost) + to_decimal(fcost)
                        sum_list.fixcost =  to_decimal(sum_list.fixcost) + to_decimal(fcost) * to_decimal(frate)

                        if res_line.adrflag:
                            ltot_fix =  to_decimal(ltot_fix) + to_decimal(fcost)
                        else:
                            tot_fix =  to_decimal(tot_fix) + to_decimal(fcost)

            if curr_zinr != res_line.zinr or curr_resnr != res_line.resnr:

                if res_line.adrflag:
                    ltot_rm = ltot_rm + 1
                else:
                    tot_rm = tot_rm + 1
            curr_zinr = res_line.zinr
            curr_resnr = res_line.resnr

        if exc_taxserv:

            for s_list in query(s_list_list):
                s_list.f_betrag = to_decimal(round((s_list.f_betrag / (1 + vat + service)) , price_decimal))
                s_list.l_betrag = to_decimal(round((s_list.l_betrag / (1 + vat + service)) , price_decimal))

            for sum_list in query(sum_list_list):
                sum_list.lodging = to_decimal(round((sum_list.lodging / (1 + vat + service)) , price_decimal))
                sum_list.bfast = to_decimal(round((sum_list.bfast / (1 + vat + service)) , price_decimal))
                sum_list.lunch = to_decimal(round((sum_list.lunch / (1 + vat + service)) , price_decimal))
                sum_list.dinner = to_decimal(round((sum_list.dinner / (1 + vat + service)) , price_decimal))
                sum_list.misc = to_decimal(round((sum_list.misc / (1 + vat + service)) , price_decimal))
                sum_list.fixcost = to_decimal(round((sum_list.fixcost / (1 + vat + service)) , price_decimal))
                sum_list.t_rev = to_decimal(round((sum_list.t_rev / (1 + vat + service)) , price_decimal))


        cl_list = Cl_list()
        cl_list_list.append(cl_list)

        cl_list.flag = "*"
        cl_list.zinr = " "
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

        for cc_list in query(cc_list_list, filters=(lambda cc_list: cc_list.flag == ""), sort_by=[("currency",False)]):

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
                    currency_list_list.append(currency_list)

                    currency_list.code = cc_list.currency
                cl_list = Cl_list()
                cl_list_list.append(cl_list)

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

        for cl_list in query(cl_list_list, filters=(lambda cl_list: cl_list.flag.lower()  != ("*").lower())):

            if exc_taxserv:
                cl_list.zipreis = to_decimal(round((cl_list.zipreis / (1 + vat + service)) , price_decimal))
                cl_list.localrate = to_decimal(round((cl_list.localrate / (1 + vat + service)) , price_decimal))
                cl_list.lodging = to_decimal(round((cl_list.lodging / (1 + vat + service)) , price_decimal))
                cl_list.bfast = to_decimal(round((cl_list.bfast / (1 + vat + service)) , price_decimal))
                cl_list.lunch = to_decimal(round((cl_list.lunch / (1 + vat + service)) , price_decimal))
                cl_list.dinner = to_decimal(round((cl_list.dinner / (1 + vat + service)) , price_decimal))
                cl_list.misc = to_decimal(round((cl_list.misc / (1 + vat + service)) , price_decimal))
                cl_list.fixcost = to_decimal(round((cl_list.fixcost / (1 + vat + service)) , price_decimal))
                cl_list.t_rev = to_decimal(round((cl_list.t_rev / (1 + vat + service)) , price_decimal))


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
        total_rev =  to_decimal(tot_rate)


    def check_fixleist_posted(artnr:int, dept:int, fakt_modus:int, intervall:int, lfakt:date):

        nonlocal msg_str, msg_warning, cl_list_list, currency_list_list, sum_list_list, s_list_list, exchg_rate, frate, post_it, total_rev, rm_rate, lvcarea, waehrung, guest, artikel, htparam, zimmer, res_line, arrangement, reservation, bill, reslin_queasy, guest_pr, pricecod, argt_line, fixleist
        nonlocal exc_taxserv, pvilanguage, new_contrate, foreign_rate, price_decimal, curr_date
        nonlocal waehrung1, cc_list


        nonlocal sum_list, currency_list, cl_list, s_list, waehrung1, cc_list
        nonlocal sum_list_list, currency_list_list, cl_list_list, s_list_list

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


    def get_argtline_rate(contcode:string, argt_recid:int):

        nonlocal msg_str, msg_warning, cl_list_list, currency_list_list, sum_list_list, s_list_list, exchg_rate, frate, post_it, total_rev, rm_rate, lvcarea, waehrung, guest, artikel, htparam, zimmer, res_line, arrangement, reservation, bill, reslin_queasy, guest_pr, pricecod, argt_line, fixleist
        nonlocal exc_taxserv, pvilanguage, new_contrate, foreign_rate, price_decimal, curr_date
        nonlocal waehrung1, cc_list


        nonlocal sum_list, currency_list, cl_list, s_list, waehrung1, cc_list
        nonlocal sum_list_list, currency_list_list, cl_list_list, s_list_list

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

        argtline = get_cache (Argt_line, {"_recid": [(eq, argt_recid)]})

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

            reslin_queasy = get_cache (Reslin_queasy, {"key": [(eq, "fargt-line")],"char1": [(eq, "")],"resnr": [(eq, res_line.resnr)],"reslinnr": [(eq, res_line.reslinnr)],"number1": [(eq, argtline.departement)],"number2": [(eq, argtline.argtnr)],"number3": [(eq, argtline.argt_artnr)],"date1": [(le, curr_date)],"date2": [(ge, curr_date)]})

            if reslin_queasy:
                argt_betrag =  to_decimal(reslin_queasy.deci1) * to_decimal(qty)
                f_betrag =  to_decimal(argt_betrag)

                waehrung = get_cache (Waehrung, {"_recid": [(eq, waehrung1._recid)]})

                if argt_betrag == 0:
                    add_it = False

                return generate_inner_output()

            if contcode != "":

                reslin_queasy = get_cache (Reslin_queasy, {"key": [(eq, "argt-line")],"char1": [(eq, contcode)],"number1": [(eq, res_line.reserve_int)],"number2": [(eq, arrangement.argtnr)],"number3": [(eq, argtline.argt_artnr)],"resnr": [(eq, argtline.departement)],"reslinnr": [(eq, curr_zikatnr)],"date1": [(le, curr_date)],"date2": [(ge, curr_date)]})

                if reslin_queasy:
                    argt_betrag =  to_decimal(reslin_queasy.deci1) * to_decimal(qty)
                    f_betrag =  to_decimal(argt_betrag)

                    waehrung = get_cache (Waehrung, {"_recid": [(eq, waehrung1._recid)]})

                    if argt_betrag == 0:
                        add_it = False

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
                argt_betrag = ( to_decimal(rm_rate) * to_decimal(- to_decimal(argt_betrag) / to_decimal(100))) * to_decimal(qty)

            if argt_betrag == 0:
                add_it = False

        return generate_inner_output()


    sum_list = Sum_list()
    sum_list_list.append(sum_list)

    create_billbalance()

    return generate_output()