#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from functions.calc_servtaxesbl import calc_servtaxesbl
from functions.ratecode_seek import ratecode_seek
from models import Res_line, Waehrung, Guest, Artikel, Queasy, Nation, Reservation, Kontline, Zimkateg, Htparam, Zimmer, Arrangement, Genstat, Exrate, Bill, Reslin_queasy, Guest_pr, Pricecod, Argt_line, Fixleist

reslin_list_data, Reslin_list = create_model_like(Res_line)

def closingscriptbl(reslin_list_data:[Reslin_list], pvilanguage:int):

    prepare_cache ([Res_line, Waehrung, Guest, Artikel, Queasy, Nation, Reservation, Kontline, Zimkateg, Htparam, Zimmer, Arrangement, Genstat, Exrate, Bill, Reslin_queasy, Guest_pr, Pricecod, Argt_line, Fixleist])

    ausweis_nr2 = ""
    karteityp = 0
    msg_str = ""
    msg_warning = ""
    cl_list_data = []
    output_list_data = []
    exchg_rate:Decimal = 1
    frate:Decimal = to_decimal("0.0")
    post_it:bool = False
    total_rev:Decimal = to_decimal("0.0")
    new_contrate:bool = False
    foreign_rate:bool = False
    price_decimal:int = 0
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
    curr_zikatnr:int = 0
    co_date:date = None
    datum:date = None
    curr_date:date = None
    i:int = 0
    str:string = ""
    segm__purcode:int = 0
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
    lvcarea:string = "rmrev-bdown"
    rstat_list:List[string] = create_empty_list(13,"")
    res_line = waehrung = guest = artikel = queasy = nation = reservation = kontline = zimkateg = htparam = zimmer = arrangement = genstat = exrate = bill = reslin_queasy = guest_pr = pricecod = argt_line = fixleist = None

    reslin_list = cl_list = output_list = waehrung1 = cc_list = member1 = rguest = artikel1 = queasy1 = nation1 = bres = None

    cl_list_data, Cl_list = create_model("Cl_list", {"zinr":string, "zipreis":Decimal, "localrate":Decimal, "lodging":Decimal, "bfast":Decimal, "lunch":Decimal, "dinner":Decimal, "misc":Decimal, "fixcost":Decimal, "t_rev":Decimal, "res_recid":int, "sleeping":bool, "row_disp":int, "flag":string, "rstatus":int, "argt":string, "currency":string, "ratecode":string, "pax":int, "com":int, "ankunft":date, "abreise":date, "rechnr":int, "name":string, "ex_rate":string, "fix_rate":string, "fdate":date, "tdate":date, "datum":date, "dt_rate":string}, {"sleeping": True})
    output_list_data, Output_list = create_model("Output_list", {"ci":string, "co":string, "guest":string, "rmcat":string, "card":string, "grpname":string, "res_status":string, "night":string, "adult":string, "child1":string, "child2":string, "com":string, "rmqty":string, "rmno":string, "memo_zinr":string, "voucher":string, "argt":string, "allot":string, "ratecode":string, "rmrate":string, "currency":string, "bill_reciv":string, "purpose":string, "bill_instruct":string, "deposit":string, "pay1":string, "pay2":string, "contcode":string, "email_adr":string, "nat":string, "country":string, "restatus":int, "lzuordnung3":int})

    Waehrung1 = create_buffer("Waehrung1",Waehrung)
    Cc_list = Cl_list
    cc_list_data = cl_list_data

    Member1 = create_buffer("Member1",Guest)
    Rguest = create_buffer("Rguest",Guest)
    Artikel1 = create_buffer("Artikel1",Artikel)
    Queasy1 = create_buffer("Queasy1",Queasy)
    Nation1 = create_buffer("Nation1",Nation)
    Bres = create_buffer("Bres",Res_line)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal ausweis_nr2, karteityp, msg_str, msg_warning, cl_list_data, output_list_data, exchg_rate, frate, post_it, total_rev, new_contrate, foreign_rate, price_decimal, fcost, tot_pax, tot_com, tot_rm, tot_rate, tot_lrate, tot_lodging, tot_bfast, tot_lunch, tot_dinner, tot_misc, tot_fix, ltot_rm, ltot_pax, ltot_rate, ltot_lodging, ltot_bfast, ltot_lunch, ltot_dinner, ltot_misc, ltot_fix, curr_zinr, curr_resnr, bfast_art, lunch_art, dinner_art, lundin_art, fb_dept, argt_betrag, take_it, prcode, qty, r_qty, lodge_betrag, f_betrag, s, ct, contcode, vat, service, curr_zikatnr, co_date, datum, curr_date, i, str, segm__purcode, vat1, service1, serv1, serv2, vat2, vat3, vat4, fact, fact1, fact2, lvcarea, rstat_list, res_line, waehrung, guest, artikel, queasy, nation, reservation, kontline, zimkateg, htparam, zimmer, arrangement, genstat, exrate, bill, reslin_queasy, guest_pr, pricecod, argt_line, fixleist
        nonlocal pvilanguage
        nonlocal waehrung1, cc_list, member1, rguest, artikel1, queasy1, nation1, bres


        nonlocal reslin_list, cl_list, output_list, waehrung1, cc_list, member1, rguest, artikel1, queasy1, nation1, bres
        nonlocal cl_list_data, output_list_data

        return {"ausweis_nr2": ausweis_nr2, "karteityp": karteityp, "msg_str": msg_str, "msg_warning": msg_warning, "cl-list": cl_list_data, "output-list": output_list_data}

    def cal_revenue():

        nonlocal ausweis_nr2, karteityp, msg_str, msg_warning, cl_list_data, output_list_data, exchg_rate, frate, post_it, total_rev, new_contrate, foreign_rate, price_decimal, fcost, tot_pax, tot_com, tot_rm, tot_rate, tot_lrate, tot_lodging, tot_bfast, tot_lunch, tot_dinner, tot_misc, tot_fix, ltot_rm, ltot_pax, ltot_rate, ltot_lodging, ltot_bfast, ltot_lunch, ltot_dinner, ltot_misc, ltot_fix, curr_zinr, curr_resnr, bfast_art, lunch_art, dinner_art, lundin_art, fb_dept, argt_betrag, take_it, prcode, qty, r_qty, lodge_betrag, f_betrag, s, ct, contcode, vat, service, curr_zikatnr, co_date, datum, curr_date, i, str, segm__purcode, vat1, service1, serv1, serv2, vat2, vat3, vat4, fact, fact1, fact2, lvcarea, rstat_list, res_line, waehrung, guest, artikel, queasy, nation, reservation, kontline, zimkateg, htparam, zimmer, arrangement, genstat, exrate, bill, reslin_queasy, guest_pr, pricecod, argt_line, fixleist
        nonlocal pvilanguage
        nonlocal waehrung1, cc_list, member1, rguest, artikel1, queasy1, nation1, bres


        nonlocal reslin_list, cl_list, output_list, waehrung1, cc_list, member1, rguest, artikel1, queasy1, nation1, bres
        nonlocal cl_list_data, output_list_data


        cl_list_data.clear()

        htparam = get_cache (Htparam, {"paramnr": [(eq, 125)]})
        bfast_art = htparam.finteger

        htparam = get_cache (Htparam, {"paramnr": [(eq, 126)]})
        fb_dept = htparam.finteger

        htparam = get_cache (Htparam, {"paramnr": [(eq, 87)]})
        curr_date = htparam.fdate

        htparam = get_cache (Htparam, {"paramnr": [(eq, 240)]})
        foreign_rate = htparam.flogical

        if not foreign_rate:

            htparam = get_cache (Htparam, {"paramnr": [(eq, 143)]})
            foreign_rate = htparam.flogical

        htparam = get_cache (Htparam, {"paramnr": [(eq, 491)]})
        price_decimal = htparam.finteger

        htparam = get_cache (Htparam, {"paramnr": [(eq, 550)]})

        if htparam.feldtyp == 4:
            new_contrate = htparam.flogical

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
        r_qty = 0
        lodge_betrag =  to_decimal("0")

        reslin_list = query(reslin_list_data, first=True)

        if reslin_list:

            zimmer = get_cache (Zimmer, {"zinr": [(eq, reslin_list.zinr)]})

            arrangement = get_cache (Arrangement, {"arrangement": [(eq, reslin_list.arrangement)]})

            if reslin_list.abreise > reslin_list.ankunft:
                co_date = reslin_list.abreise - timedelta(days=1)
            else:
                co_date = reslin_list.abreise
            for datum in date_range(reslin_list.ankunft,co_date) :

                if datum < curr_date:
                    read_genstat()
                else:
                    read_resline()


    def read_genstat():

        nonlocal ausweis_nr2, karteityp, msg_str, msg_warning, cl_list_data, output_list_data, exchg_rate, frate, post_it, total_rev, new_contrate, foreign_rate, price_decimal, fcost, tot_pax, tot_com, tot_rm, tot_rate, tot_lrate, tot_lodging, tot_bfast, tot_lunch, tot_dinner, tot_misc, tot_fix, ltot_rm, ltot_pax, ltot_rate, ltot_lodging, ltot_bfast, ltot_lunch, ltot_dinner, ltot_misc, ltot_fix, curr_zinr, curr_resnr, bfast_art, lunch_art, dinner_art, lundin_art, fb_dept, argt_betrag, take_it, prcode, qty, r_qty, lodge_betrag, f_betrag, s, ct, contcode, vat, service, curr_zikatnr, co_date, datum, curr_date, str, segm__purcode, vat1, service1, serv1, serv2, vat2, vat3, vat4, fact, fact1, fact2, lvcarea, rstat_list, res_line, waehrung, guest, artikel, queasy, nation, reservation, kontline, zimkateg, htparam, zimmer, arrangement, genstat, exrate, bill, reslin_queasy, guest_pr, pricecod, argt_line, fixleist
        nonlocal pvilanguage
        nonlocal waehrung1, cc_list, member1, rguest, artikel1, queasy1, nation1, bres


        nonlocal reslin_list, cl_list, output_list, waehrung1, cc_list, member1, rguest, artikel1, queasy1, nation1, bres
        nonlocal cl_list_data, output_list_data

        i:int = 0
        n:int = 0

        genstat = get_cache (Genstat, {"zinr": [(ne, "")],"datum": [(eq, datum)],"res_logic[1]": [(eq, True)],"resnr": [(eq, reslin_list.resnr)],"res_int[0]": [(eq, reslin_list.reslinnr)]})

        if genstat:

            artikel = get_cache (Artikel, {"artnr": [(eq, arrangement.argt_artikelnr)],"departement": [(eq, 0)]})
            service =  to_decimal("0")
            vat =  to_decimal("0")
            serv1 =  to_decimal("0")
            vat1 =  to_decimal("0")
            vat2 =  to_decimal("0")
            fact1 =  to_decimal("0")


            serv1, vat1, vat2, fact1 = get_output(calc_servtaxesbl(1, artikel.artnr, artikel.departement, curr_date))

            waehrung1 = get_cache (Waehrung, {"waehrungsnr": [(eq, reslin_list.betriebsnr)]})

            if waehrung1:

                exrate = get_cache (Exrate, {"datum": [(eq, curr_date)],"artnr": [(eq, waehrung1.waehrungsnr)]})

                if exrate:
                    exchg_rate =  to_decimal(exrate.betrag)

            if reslin_list.reserve_dec != 0:
                frate =  to_decimal(reslin_list.reserve_dec)
            else:
                frate =  to_decimal(exchg_rate)

            if genstat.zipreis != 0:
                r_qty = r_qty + 1

            guest = get_cache (Guest, {"gastnr": [(eq, reslin_list.gastnrpay)]})

            member1 = get_cache (Guest, {"gastnr": [(eq, reslin_list.gastnrmember)]})

            reservation = get_cache (Reservation, {"resnr": [(eq, reslin_list.resnr)]})

            if reslin_list.l_zuordnung[0] != 0:
                curr_zikatnr = reslin_list.l_zuordnung[0]
            else:
                curr_zikatnr = reslin_list.zikatnr

            bill = get_cache (Bill, {"resnr": [(eq, reslin_list.resnr)],"reslinnr": [(eq, reslin_list.reslinnr)],"zinr": [(eq, reslin_list.zinr)]})

            if not bill:

                bill = get_cache (Bill, {"resnr": [(eq, reslin_list.resnr)],"reslinnr": [(eq, reslin_list.reslinnr)]})

            if not bill:
                msg_str = translateExtended ("Bill not found: RmNo ", lvcarea, "") + reslin_list.zinr + " - " + reslin_list.name
            cl_list = Cl_list()
            cl_list_data.append(cl_list)

            cl_list.res_recid = reslin_list._recid
            cl_list.zinr = genstat.zinr
            cl_list.rstatus = genstat.resstatus
            cl_list.sleeping = zimmer.sleeping
            cl_list.argt = genstat.argt
            cl_list.name = reslin_list.name
            cl_list.pax = genstat.erwachs + genstat.kind1 + genstat.kind2
            cl_list.com = genstat.gratis + genstat.kind3
            cl_list.ankunft = reslin_list.ankunft
            cl_list.abreise = reslin_list.abreise
            cl_list.zipreis =  to_decimal(genstat.zipreis)
            cl_list.localrate =  to_decimal(genstat.ratelocal)
            cl_list.rechnr = bill.rechnr
            cl_list.t_rev =  to_decimal(genstat.zipreis)
            cl_list.currency = waehrung1.wabkurz
            cl_list.lodging =  to_decimal(genstat.logis)
            cl_list.bfast =  to_decimal(genstat.res_deci[1]) * to_decimal((1) + to_decimal(vat1) + to_decimal(vat2) + to_decimal(serv1) )
            cl_list.lunch =  to_decimal(genstat.res_deci[2]) * to_decimal((1) + to_decimal(vat1) + to_decimal(vat2) + to_decimal(serv1) )
            cl_list.dinner =  to_decimal(genstat.res_deci[3]) * to_decimal((1) + to_decimal(vat1) + to_decimal(vat2) + to_decimal(serv1) )
            cl_list.misc =  to_decimal(genstat.res_deci[4]) * to_decimal((1) + to_decimal(vat1) + to_decimal(vat2) + to_decimal(serv1) )
            cl_list.fixcost =  to_decimal(genstat.res_deci[5]) * to_decimal((1) + to_decimal(vat1) + to_decimal(vat2) + to_decimal(serv1) )
            cl_list.datum = datum

            htparam = get_cache (Htparam, {"paramnr": [(eq, 127)]})

            if htparam.flogical:
                cl_list.lodging = to_decimal(round((cl_list.lodging * (1 + vat1 + vat2 + serv1)) , price_decimal))

            if matches(reslin_list.zimmer_wunsch,r"*$CODE$*"):
                s = substring(reslin_list.zimmer_wunsch, (get_index(reslin_list.zimmer_wunsch, "$CODE$") + 6) - 1)
                cl_list.ratecode = trim(entry(0, s, ";"))

            if frate == 1:
                cl_list.ex_rate = to_string(frate, " >>9.99")

            elif frate <= 999:
                cl_list.ex_rate = to_string(frate, " >>9.9999")

            elif frate <= 99999:
                cl_list.ex_rate = to_string(frate, ">>,>>9.99")
            else:
                cl_list.ex_rate = to_string(frate, ">,>>>,>>9")

            reslin_queasy = get_cache (Reslin_queasy, {"key": [(eq, "arrangement")],"resnr": [(eq, reslin_list.resnr)],"reslinnr": [(eq, reslin_list.reslinnr)],"date1": [(le, datum)],"date2": [(ge, datum)]})

            if reslin_queasy:
                cl_list.fix_rate = "YES"
                cl_list.fdate = reslin_queasy.date1
                cl_list.tdate = reslin_queasy.date2


            else:
                cl_list.fix_rate = "NO"

            if cl_list.fdate != None:
                cl_list.dt_rate = to_string(cl_list.fdate, "99/99/99") + " - " + to_string(cl_list.tdate, "99/99/99")


            tot_rate =  to_decimal(tot_rate) + to_decimal(cl_list.zipreis)
            tot_lrate =  to_decimal(tot_lrate) + to_decimal(cl_list.localrate)

            if not reslin_list.adrflag:
                tot_pax = tot_pax + cl_list.pax
            else:
                ltot_pax = ltot_pax + cl_list.pax
            tot_com = tot_com + cl_list.com

            if reslin_list.adrflag:
                ltot_lodging =  to_decimal(ltot_lodging) + to_decimal(cl_list.lodging)
            else:
                tot_lodging =  to_decimal(tot_lodging) + to_decimal(cl_list.lodging)
            lodge_betrag =  to_decimal(cl_list.lodging)

            if foreign_rate and price_decimal == 0 and not reslin_list.adrflag:

                htparam = get_cache (Htparam, {"paramnr": [(eq, 145)]})

                if htparam.finteger != 0:
                    n = 1
                    for i in range(1,htparam.finteger + 1) :
                        n = n * 10
                    lodge_betrag = to_decimal(round(lodge_betrag / n , 0) * n)

            if curr_zinr != reslin_list.zinr or curr_resnr != reslin_list.resnr:

                if reslin_list.adrflag:
                    ltot_rm = ltot_rm + 1
                else:
                    tot_rm = tot_rm + 1
            curr_zinr = reslin_list.zinr


            curr_resnr = reslin_list.resnr


    def read_resline():

        nonlocal ausweis_nr2, karteityp, msg_str, msg_warning, cl_list_data, output_list_data, exchg_rate, frate, post_it, total_rev, new_contrate, foreign_rate, price_decimal, fcost, tot_pax, tot_com, tot_rm, tot_rate, tot_lrate, tot_lodging, tot_bfast, tot_lunch, tot_dinner, tot_misc, tot_fix, ltot_rm, ltot_pax, ltot_rate, ltot_lodging, ltot_bfast, ltot_lunch, ltot_dinner, ltot_misc, ltot_fix, curr_zinr, curr_resnr, bfast_art, lunch_art, dinner_art, lundin_art, fb_dept, argt_betrag, take_it, prcode, qty, r_qty, lodge_betrag, f_betrag, s, ct, contcode, vat, service, curr_zikatnr, co_date, datum, curr_date, str, segm__purcode, vat1, service1, serv1, serv2, vat2, vat3, vat4, fact, fact1, fact2, lvcarea, rstat_list, res_line, waehrung, guest, artikel, queasy, nation, reservation, kontline, zimkateg, htparam, zimmer, arrangement, genstat, exrate, bill, reslin_queasy, guest_pr, pricecod, argt_line, fixleist
        nonlocal pvilanguage
        nonlocal waehrung1, cc_list, member1, rguest, artikel1, queasy1, nation1, bres


        nonlocal reslin_list, cl_list, output_list, waehrung1, cc_list, member1, rguest, artikel1, queasy1, nation1, bres
        nonlocal cl_list_data, output_list_data

        i:int = 0
        n:int = 0
        service =  to_decimal("0")
        vat =  to_decimal("0")
        serv1 =  to_decimal("0")
        vat1 =  to_decimal("0")
        vat2 =  to_decimal("0")
        fact1 =  to_decimal("0")

        artikel = get_cache (Artikel, {"artnr": [(eq, arrangement.argt_artikelnr)],"departement": [(eq, 0)]})

        if artikel:
            serv1, vat1, vat2, fact1 = get_output(calc_servtaxesbl(1, artikel.artnr, artikel.departement, curr_date))

        waehrung1 = get_cache (Waehrung, {"waehrungsnr": [(eq, reslin_list.betriebsnr)]})

        if waehrung1:
            exchg_rate =  to_decimal(waehrung1.ankauf) / to_decimal(waehrung1.einheit)

        if reslin_list.reserve_dec != 0:
            frate =  to_decimal(reslin_list.reserve_dec)
        else:
            frate =  to_decimal(exchg_rate)

        if reslin_list.zipreis != 0:
            r_qty = r_qty + 1

        guest = get_cache (Guest, {"gastnr": [(eq, reslin_list.gastnrpay)]})

        member1 = get_cache (Guest, {"gastnr": [(eq, reslin_list.gastnrmember)]})

        reservation = get_cache (Reservation, {"resnr": [(eq, reslin_list.resnr)]})

        if reslin_list.l_zuordnung[0] != 0:
            curr_zikatnr = reslin_list.l_zuordnung[0]
        else:
            curr_zikatnr = reslin_list.zikatnr

        bill = get_cache (Bill, {"resnr": [(eq, reslin_list.resnr)],"reslinnr": [(eq, reslin_list.reslinnr)],"zinr": [(eq, reslin_list.zinr)]})

        if not bill:

            bill = get_cache (Bill, {"resnr": [(eq, reslin_list.resnr)],"reslinnr": [(eq, reslin_list.reslinnr)]})

        if not bill:
            msg_warning = "&W" + translateExtended ("Bill not found: RmNo ", lvcarea, "") + reslin_list.zinr + " - " + reslin_list.name
        cl_list = Cl_list()
        cl_list_data.append(cl_list)

        cl_list.res_recid = reslin_list._recid
        cl_list.zinr = reslin_list.zinr
        cl_list.rstatus = reslin_list.resstatus
        cl_list.argt = reslin_list.arrangement
        cl_list.name = reslin_list.name
        cl_list.pax = reslin_list.erwachs + reslin_list.kind1 + reslin_list.kind2
        cl_list.com = reslin_list.gratis + reslin_list.l_zuordnung[3]
        cl_list.ankunft = reslin_list.ankunft
        cl_list.abreise = reslin_list.abreise
        cl_list.currency = waehrung1.wabkurz
        cl_list.datum = datum

        if bill:
            cl_list.rechnr = bill.rechnr

        if zimmer:
            cl_list.sleeping = zimmer.sleeping

        if frate == 1:
            cl_list.ex_rate = to_string(frate, " >>9.99")

        elif frate <= 999:
            cl_list.ex_rate = to_string(frate, " >>9.9999")

        elif frate <= 99999:
            cl_list.ex_rate = to_string(frate, ">>,>>9.99")
        else:
            cl_list.ex_rate = to_string(frate, ">,>>>,>>9")

        reslin_queasy = get_cache (Reslin_queasy, {"key": [(eq, "arrangement")],"resnr": [(eq, reslin_list.resnr)],"reslinnr": [(eq, reslin_list.reslinnr)],"date1": [(le, datum)],"date2": [(ge, datum)]})

        if reslin_queasy:
            cl_list.fix_rate = "YES"
            cl_list.zipreis =  to_decimal(reslin_queasy.deci1)
            cl_list.localrate =  to_decimal(reslin_queasy.deci1) * to_decimal(frate)
            cl_list.t_rev =  to_decimal(reslin_queasy.deci1)
            cl_list.fdate = reslin_queasy.date1
            cl_list.tdate = reslin_queasy.date2


        else:
            cl_list.fix_rate = "NO"
            cl_list.zipreis =  to_decimal(reslin_list.zipreis)
            cl_list.localrate =  to_decimal(reslin_list.zipreis) * to_decimal(frate)
            cl_list.t_rev =  to_decimal(reslin_list.zipreis)

        if cl_list.fdate != None:
            cl_list.dt_rate = to_string(cl_list.fdate, "99/99/99") + "-" + to_string(cl_list.tdate, "99/99/99")


        tot_rate =  to_decimal(tot_rate) + to_decimal(cl_list.zipreis)
        tot_lrate =  to_decimal(tot_lrate) + to_decimal(cl_list.localrate)

        if not reslin_list.adrflag:
            tot_pax = tot_pax + cl_list.pax
        else:
            ltot_pax = ltot_pax + cl_list.pax
        tot_com = tot_com + cl_list.com


        cl_list.lodging =  to_decimal(cl_list.zipreis)

        if cl_list.lodging != 0:
            prcode = 0
            contcode = ""

            rguest = get_cache (Guest, {"gastnr": [(eq, reslin_list.gastnr)]})

            if reslin_list.reserve_int != 0:

                guest_pr = get_cache (Guest_pr, {"gastnr": [(eq, rguest.gastnr)]})

            if guest_pr:
                contcode = guest_pr.code
                ct = reslin_list.zimmer_wunsch

                if matches(ct,r"*$CODE$*"):
                    ct = substring(ct, get_index(ct, "$CODE$") + 6 - 1)
                    contcode = substring(ct, 0, get_index(ct, ";") - 1)

                if new_contrate:
                    prcode = get_output(ratecode_seek(reslin_list.resnr, reslin_list.reslinnr, contcode, curr_date))
                else:

                    pricecod = get_cache (Pricecod, {"code": [(eq, contcode)],"marknr": [(eq, reslin_list.reserve_int)],"argtnr": [(eq, arrangement.argtnr)],"zikatnr": [(eq, curr_zikatnr)],"startperiode": [(le, curr_date)],"endperiode": [(ge, curr_date)]})

                    if pricecod:
                        prcode = pricecod._recid

            for argt_line in db_session.query(Argt_line).filter(
                     (Argt_line.argtnr == arrangement.argtnr) & not_ (Argt_line.kind2)).order_by(Argt_line._recid).all():

                artikel = get_cache (Artikel, {"artnr": [(eq, argt_line.argt_artnr)],"departement": [(eq, argt_line.departement)]})

                if not artikel:
                    take_it = False
                else:
                    take_it, f_betrag, argt_betrag, qty = get_argtline_rate(contcode, argt_line._recid)

                if take_it:

                    if artikel.zwkum == bfast_art and (artikel.umsatzart == 3 or artikel.umsatzart >= 5):
                        cl_list.bfast =  to_decimal(cl_list.bfast) + to_decimal(argt_betrag)

                        if reslin_list.adrflag:
                            ltot_bfast =  to_decimal(ltot_bfast) + to_decimal(argt_betrag)
                        else:
                            tot_bfast =  to_decimal(tot_bfast) + to_decimal(argt_betrag)
                        cl_list.lodging =  to_decimal(cl_list.lodging) - to_decimal(argt_betrag)

                    elif artikel.zwkum == lunch_art and (artikel.umsatzart == 3 or artikel.umsatzart >= 5):
                        cl_list.lunch =  to_decimal(cl_list.lunch) + to_decimal(argt_betrag)

                        if reslin_list.adrflag:
                            ltot_lunch =  to_decimal(ltot_lunch) + to_decimal(argt_betrag)
                        else:
                            tot_lunch =  to_decimal(tot_lunch) + to_decimal(argt_betrag)
                        cl_list.lodging =  to_decimal(cl_list.lodging) - to_decimal(argt_betrag)

                    elif artikel.zwkum == dinner_art and (artikel.umsatzart == 3 or artikel.umsatzart >= 5):
                        cl_list.dinner =  to_decimal(cl_list.dinner) + to_decimal(argt_betrag)

                        if reslin_list.adrflag:
                            ltot_dinner =  to_decimal(ltot_dinner) + to_decimal(argt_betrag)
                        else:
                            tot_dinner =  to_decimal(tot_dinner) + to_decimal(argt_betrag)
                        cl_list.lodging =  to_decimal(cl_list.lodging) - to_decimal(argt_betrag)

                    elif artikel.zwkum == lundin_art and (artikel.umsatzart == 3 or artikel.umsatzart >= 5):
                        cl_list.lunch =  to_decimal(cl_list.lunch) + to_decimal(argt_betrag)

                        if reslin_list.adrflag:
                            ltot_lunch =  to_decimal(ltot_lunch) + to_decimal(argt_betrag)
                        else:
                            tot_lunch =  to_decimal(tot_lunch) + to_decimal(argt_betrag)
                        cl_list.lodging =  to_decimal(cl_list.lodging) - to_decimal(argt_betrag)


                    else:
                        cl_list.misc =  to_decimal(cl_list.misc) + to_decimal(argt_betrag)

                        if reslin_list.adrflag:
                            ltot_misc =  to_decimal(ltot_misc) + to_decimal(argt_betrag)
                        else:
                            tot_misc =  to_decimal(tot_misc) + to_decimal(argt_betrag)
                        cl_list.lodging =  to_decimal(cl_list.lodging) - to_decimal(argt_betrag)

        if reslin_list.adrflag:
            ltot_lodging =  to_decimal(ltot_lodging) + to_decimal(cl_list.lodging)
        else:
            tot_lodging =  to_decimal(tot_lodging) + to_decimal(cl_list.lodging)
        lodge_betrag =  to_decimal(cl_list.lodging) * to_decimal(frate)

        if foreign_rate and price_decimal == 0 and not reslin_list.adrflag:

            htparam = get_cache (Htparam, {"paramnr": [(eq, 145)]})

            if htparam.finteger != 0:
                n = 1
                for i in range(1,htparam.finteger + 1) :
                    n = n * 10
                lodge_betrag = to_decimal(round(lodge_betrag / n , 0) * n)

        artikel1 = get_cache (Artikel, {"artnr": [(eq, arrangement.artnr_logis)],"departement": [(eq, 0)]})

        for fixleist in db_session.query(Fixleist).filter(
                 (Fixleist.resnr == reslin_list.resnr) & (Fixleist.reslinnr == reslin_list.reslinnr)).order_by(Fixleist._recid).all():
            post_it = check_fixleist_posted(fixleist.artnr, fixleist.departement, fixleist.sequenz, fixleist.dekade, fixleist.lfakt)

            if post_it:
                fcost =  to_decimal(fixleist.betrag) * to_decimal(fixleist.number)
                cl_list.t_rev =  to_decimal(cl_list.t_rev) + to_decimal(fcost)

                if reslin_list.adrflag:
                    ltot_rate =  to_decimal(ltot_rate) + to_decimal(fcost)
                else:
                    tot_rate =  to_decimal(tot_rate) + to_decimal(fcost)

                artikel = get_cache (Artikel, {"artnr": [(eq, fixleist.artnr)],"departement": [(eq, fixleist.departement)]})

                if (artikel.zwkum == bfast_art and artikel.departement == fb_dept):
                    cl_list.bfast =  to_decimal(cl_list.bfast) + to_decimal(fcost)

                    if reslin_list.adrflag:
                        ltot_bfast =  to_decimal(ltot_bfast) + to_decimal(fcost) * to_decimal(frate)
                    else:
                        tot_bfast =  to_decimal(tot_bfast) + to_decimal(fcost)

                elif (artikel.zwkum == lunch_art and artikel.departement == fb_dept):
                    cl_list.lunch =  to_decimal(cl_list.lunch) + to_decimal(fcost)

                    if reslin_list.adrflag:
                        ltot_lunch =  to_decimal(ltot_lunch) + to_decimal(fcost) * to_decimal(frate)
                    else:
                        tot_lunch =  to_decimal(tot_lunch) + to_decimal(fcost)

                elif (artikel.zwkum == dinner_art and artikel.departement == fb_dept):
                    cl_list.dinner =  to_decimal(cl_list.dinner) + to_decimal(fcost)

                    if reslin_list.adrflag:
                        ltot_dinner =  to_decimal(ltot_dinner) + to_decimal(fcost) * to_decimal(frate)
                    else:
                        tot_dinner =  to_decimal(tot_dinner) + to_decimal(fcost)
                else:
                    cl_list.fixcost =  to_decimal(cl_list.fixcost) + to_decimal(fcost)

                    if reslin_list.adrflag:
                        ltot_fix =  to_decimal(ltot_fix) + to_decimal(fcost)
                    else:
                        tot_fix =  to_decimal(tot_fix) + to_decimal(fcost)

        if curr_zinr != reslin_list.zinr or curr_resnr != reslin_list.resnr:

            if reslin_list.adrflag:
                ltot_rm = ltot_rm + 1
            else:
                tot_rm = tot_rm + 1
        curr_zinr = reslin_list.zinr
        curr_resnr = reslin_list.resnr


    def check_fixleist_posted(artnr:int, dept:int, fakt_modus:int, intervall:int, lfakt:date):

        nonlocal ausweis_nr2, karteityp, msg_str, msg_warning, cl_list_data, output_list_data, exchg_rate, frate, post_it, total_rev, new_contrate, foreign_rate, price_decimal, fcost, tot_pax, tot_com, tot_rm, tot_rate, tot_lrate, tot_lodging, tot_bfast, tot_lunch, tot_dinner, tot_misc, tot_fix, ltot_rm, ltot_pax, ltot_rate, ltot_lodging, ltot_bfast, ltot_lunch, ltot_dinner, ltot_misc, ltot_fix, curr_zinr, curr_resnr, bfast_art, lunch_art, dinner_art, lundin_art, fb_dept, argt_betrag, take_it, prcode, qty, r_qty, lodge_betrag, f_betrag, s, ct, contcode, vat, service, curr_zikatnr, co_date, datum, curr_date, i, str, segm__purcode, vat1, service1, serv1, serv2, vat2, vat3, vat4, fact, fact1, fact2, lvcarea, rstat_list, res_line, waehrung, guest, artikel, queasy, nation, reservation, kontline, zimkateg, htparam, zimmer, arrangement, genstat, exrate, bill, reslin_queasy, guest_pr, pricecod, argt_line, fixleist
        nonlocal pvilanguage
        nonlocal waehrung1, cc_list, member1, rguest, artikel1, queasy1, nation1, bres


        nonlocal reslin_list, cl_list, output_list, waehrung1, cc_list, member1, rguest, artikel1, queasy1, nation1, bres
        nonlocal cl_list_data, output_list_data

        post_it = False
        delta:int = 0
        start_date:date = None

        def generate_inner_output():
            return (post_it)


        if fakt_modus == 1:
            post_it = True

        elif fakt_modus == 2:

            if reslin_list.ankunft == curr_date:
                post_it = True

        elif fakt_modus == 3:

            if (reslin_list.ankunft + 1) == curr_date:
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
                delta = (lfakt - reslin_list.ankunft).days

                if delta < 0:
                    delta = 0
            start_date = reslin_list.ankunft + timedelta(days=delta)

            if (reslin_list.abreise - start_date) < intervall:
                start_date = reslin_list.ankunft

            if curr_date <= (start_date + timedelta(days=(intervall - 1))):
                post_it = True

            if curr_date < start_date:
                post_it = False

        return generate_inner_output()


    def get_argtline_rate(contcode:string, argt_recid:int):

        nonlocal ausweis_nr2, karteityp, msg_str, msg_warning, cl_list_data, output_list_data, exchg_rate, frate, post_it, total_rev, new_contrate, foreign_rate, price_decimal, fcost, tot_pax, tot_com, tot_rm, tot_rate, tot_lrate, tot_lodging, tot_bfast, tot_lunch, tot_dinner, tot_misc, tot_fix, ltot_rm, ltot_pax, ltot_rate, ltot_lodging, ltot_bfast, ltot_lunch, ltot_dinner, ltot_misc, ltot_fix, curr_zinr, curr_resnr, bfast_art, lunch_art, dinner_art, lundin_art, fb_dept, argt_betrag, take_it, prcode, qty, r_qty, lodge_betrag, f_betrag, s, ct, vat, service, co_date, datum, curr_date, i, str, segm__purcode, vat1, service1, serv1, serv2, vat2, vat3, vat4, fact, fact1, fact2, lvcarea, rstat_list, res_line, waehrung, guest, artikel, queasy, nation, reservation, kontline, zimkateg, htparam, zimmer, arrangement, genstat, exrate, bill, reslin_queasy, guest_pr, pricecod, argt_line, fixleist
        nonlocal pvilanguage
        nonlocal waehrung1, cc_list, member1, rguest, artikel1, queasy1, nation1, bres


        nonlocal reslin_list, cl_list, output_list, waehrung1, cc_list, member1, rguest, artikel1, queasy1, nation1, bres
        nonlocal cl_list_data, output_list_data

        add_it = False
        f_betrag = to_decimal("0.0")
        argt_betrag = to_decimal("0.0")
        qty = 0
        curr_zikatnr:int = 0
        argtline = None

        def generate_inner_output():
            return (add_it, f_betrag, argt_betrag, qty)

        Argtline =  create_buffer("Argtline",Argt_line)

        if reslin_list.l_zuordnung[0] != 0:
            curr_zikatnr = reslin_list.l_zuordnung[0]
        else:
            curr_zikatnr = reslin_list.zikatnr

        argtline = get_cache (Argt_line, {"_recid": [(eq, argt_recid)]})

        if argt_line.vt_percnt == 0:

            if argt_line.betriebsnr == 0:
                qty = reslin_list.erwachs
            else:
                qty = argt_line.betriebsnr

        elif argt_line.vt_percnt == 1:
            qty = reslin_list.kind1

        elif argt_line.vt_percnt == 2:
            qty = reslin_list.kind2

        if qty > 0:

            if argtline.fakt_modus == 1:
                add_it = True

            elif argtline.fakt_modus == 2:

                if reslin_list.ankunft == curr_date:
                    add_it = True

            elif argtline.fakt_modus == 3:

                if (reslin_list.ankunft + 1) == curr_date:
                    add_it = True

            elif argtline.fakt_modus == 4 and get_day(curr_date) == 1:
                add_it = True

            elif argtline.fakt_modus == 5 and get_day(curr_date + 1) == 1:
                add_it = True

            elif argtline.fakt_modus == 6:

                if (reslin_list.ankunft + (argtline.intervall - 1)) >= curr_date:
                    add_it = True

        if add_it:

            reslin_queasy = get_cache (Reslin_queasy, {"key": [(eq, "fargt-line")],"char1": [(eq, "")],"resnr": [(eq, reslin_list.resnr)],"reslinnr": [(eq, reslin_list.reslinnr)],"number1": [(eq, argtline.departement)],"number2": [(eq, argtline.argtnr)],"number3": [(eq, argtline.argt_artnr)],"date1": [(le, curr_date)],"date2": [(ge, curr_date)]})

            if reslin_queasy:
                argt_betrag =  to_decimal(reslin_queasy.deci1) * to_decimal(qty)
                f_betrag =  to_decimal(argt_betrag)

                waehrung = get_cache (Waehrung, {"_recid": [(eq, waehrung1._recid)]})

                if argt_betrag == 0:
                    add_it = False

                return generate_inner_output()

            if contcode != "":

                reslin_queasy = get_cache (Reslin_queasy, {"key": [(eq, "argt-line")],"char1": [(eq, contcode)],"number1": [(eq, reslin_list.reserve_int)],"number2": [(eq, arrangement.argtnr)],"number3": [(eq, argtline.argt_artnr)],"resnr": [(eq, argtline.departement)],"reslinnr": [(eq, curr_zikatnr)],"date1": [(le, curr_date)],"date2": [(ge, curr_date)]})

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

            if reslin_list.betriebsnr != arrangement.betriebsnr:
                argt_betrag =  to_decimal(argt_betrag) * to_decimal((waehrung.ankauf) / to_decimal(waehrung.einheit)) / to_decimal(frate)
            argt_betrag =  to_decimal(argt_betrag) * to_decimal(qty)

            if argt_betrag == 0:
                add_it = False

        return generate_inner_output()

    rstat_list[0] = translateExtended ("Guaranted", lvcarea, "")
    rstat_list[1] = translateExtended ("6 PM", lvcarea, "")
    rstat_list[2] = translateExtended ("Tentative", lvcarea, "")
    rstat_list[3] = translateExtended ("WaitList", lvcarea, "")
    rstat_list[4] = translateExtended ("Verbal Confirm", lvcarea, "")
    rstat_list[5] = translateExtended ("Main Guest", lvcarea, "")
    rstat_list[6] = ""
    rstat_list[7] = translateExtended ("Departed", lvcarea, "")
    rstat_list[8] = translateExtended ("Cancelled", lvcarea, "")
    rstat_list[9] = translateExtended ("NoShow", lvcarea, "")
    rstat_list[10] = translateExtended ("ResSharer", lvcarea, "")
    rstat_list[11] = ""
    rstat_list[12] = translateExtended ("RmSharer", lvcarea, "")

    reslin_list = query(reslin_list_data, first=True)

    if reslin_list:
        output_list = Output_list()
        output_list_data.append(output_list)

        output_list.night = to_string(reslin_list.anztage)
        output_list.adult = to_string(reslin_list.erwachs)
        output_list.child1 = to_string(reslin_list.kind1)
        output_list.child2 = to_string(reslin_list.kind2)
        output_list.com = to_string(reslin_list.gratis)
        output_list.rmqty = to_string(reslin_list.zimmeranz)
        output_list.ci = to_string(reslin_list.ankunft, "99/99/9999")
        output_list.co = to_string(reslin_list.abreise, "99/99/9999")
        output_list.rmno = reslin_list.zinr
        output_list.argt = reslin_list.arrangement

        if reslin_list.zipreis != 0:
            output_list.rmrate = to_string(reslin_list.zipreis, ">,>>>,>>>,>>9.99")


        else:
            output_list.rmrate = "0.00"

        guest = get_cache (Guest, {"gastnr": [(eq, reslin_list.gastnrmember)]})

        if guest:
            output_list.guest = guest.name + ", " + guest.vorname1 + guest.anredefirma +\
                    " " + guest.anrede1
            output_list.email_adr = guest.email_adr
            ausweis_nr2 = guest.ausweis_nr2
            karteityp = guest.karteityp

        nation = get_cache (Nation, {"kurzbez": [(eq, guest.nation1)]})

        if nation:

            if matches(nation.bezeich,r"*;*"):
                output_list.nat = entry(0, nation.bezeich, ";")


            else:
                output_list.nat = nation.bezeich

        nation1 = get_cache (Nation, {"kurzbez": [(eq, guest.land)]})

        if nation1:

            if matches(nation1.bezeich,r"*;*"):
                output_list.country = entry(0, nation1.bezeich, ";")


            else:
                output_list.country = nation1.bezeich

        reservation = get_cache (Reservation, {"resnr": [(eq, reslin_list.resnr)]})

        if reservation:
            output_list.grpname = reservation.groupname

            if reservation.depositgef != 0:
                output_list.deposit = to_string(reservation.depositgef, ">,>>>,>>>,>>9.99")

            if reservation.depositbez != 0:
                output_list.pay1 = to_string(reservation.depositbez, ">,>>>,>>>,>>9.99")

            if reservation.depositbez2 != 0:
                output_list.pay2 = to_string(reservation.depositbez2, ">,>>>,>>>,>>9.99")

        res_line = get_cache (Res_line, {"resnr": [(eq, reslin_list.resnr)],"reslinnr": [(eq, reslin_list.reslinnr)]})

        if res_line:
            output_list.res_status = rstat_list[reslin_list.resstatus - 1]
            output_list.restat = res_line.resstatus
            output_list.lzuordnung3 = res_line.l_zuordnung[2]

            if matches(res_line.memozinr,r"*;*"):
                output_list.memo_zinr = entry(1, res_line.memozinr, ";")


            else:
                output_list.memo_zinr = res_line.memozinr

            guest = get_cache (Guest, {"gastnr": [(eq, res_line.gastnrpay)]})

            if guest:
                output_list.bill_reciv = guest.name + ", " + guest.vorname1 + guest.anredefirma +\
                    " " + guest.anrede1


            for i in range(1,num_entries(reslin_list.zimmer_wunsch, ";") - 1 + 1) :
                str = entry(i - 1, reslin_list.zimmer_wunsch, ";")

                if substring(str, 0, 8) == ("SEGM_PUR").lower() :
                    segm__purcode = to_int(substring(str, 8))

                elif substring(str, 0, 6) == ("$CODE$").lower() :
                    output_list.contcode = substring(str, 6)

            queasy1 = get_cache (Queasy, {"key": [(eq, 143)],"number1": [(eq, segm__purcode)]})

            if queasy1:
                output_list.purpose = queasy1.char3

            queasy = get_cache (Queasy, {"key": [(eq, 9)],"number1": [(eq, to_int(reslin_list.code))]})

            if queasy:
                output_list.bill_instruct = queasy.char1

        if reslin_list.kontignr > 0:

            kontline = get_cache (Kontline, {"kontignr": [(eq, reslin_list.kontignr)],"kontstatus": [(eq, 1)]})
        else:

            kontline = get_cache (Kontline, {"kontignr": [(eq, - reslin_list.kontignr)],"betriebsnr": [(eq, 1)],"kontstatus": [(eq, 1)]})

        if kontline:
            output_list.allot = kontline.kontcode

        if output_list.contcode != "":

            queasy = get_cache (Queasy, {"key": [(eq, 2)],"char1": [(eq, output_list.contcode)]})

            if queasy:
                output_list.ratecode = queasy.char1

        waehrung1 = get_cache (Waehrung, {"waehrungsnr": [(eq, reslin_list.betriebsnr)]})

        if waehrung1:
            output_list.currency = waehrung1.wabkurz

        zimkateg = get_cache (Zimkateg, {"zikatnr": [(eq, reslin_list.zikatnr)]})

        if zimkateg:
            output_list.rmcat = zimkateg.bezeichnung

        if res_line.kontakt_nr != 0 and res_line.resstatus <= 6:

            for bres in db_session.query(Bres).filter(
                     (Bres.resnr == reslin_list.resnr) & (Bres.reslinnr != reslin_list.reslinnr) & (Bres.kontakt_nr == reslin_list.reslinnr) & (Bres.resstatus != 9) & (Bres.resstatus != 10) & (Bres.resstatus != 12)).order_by(Bres.l_zuordnung[inc_value(2)], Bres.resstatus, Bres.name).all():

                guest = get_cache (Guest, {"gastnr": [(eq, bres.gastnrmember)]})

                if guest:
                    output_list = Output_list()
                    output_list_data.append(output_list)

                    output_list.guest = guest.name + ", " + guest.vorname1 + guest.anredefirma +\
                            " " + guest.anrede1
                    output_list.restat = bres.resstatus
                    output_list.lzuordnung3 = bres.l_zuordnung[2]


        elif res_line.kontakt_nr != 0 and res_line.resstatus > 6:

            bres = get_cache (Res_line, {"resnr": [(eq, res_line.resnr)],"reslinnr": [(eq, res_line.kontakt_nr)],"resstatus": [(ne, 9),(ne, 10),(ne, 12)]})

            if bres:

                guest = get_cache (Guest, {"gastnr": [(eq, bres.gastnrmember)]})

                if guest:
                    output_list = Output_list()
                    output_list_data.append(output_list)

                    output_list.guest = guest.name + ", " + guest.vorname1 + guest.anredefirma +\
                            " " + guest.anrede1
                    output_list.restat = bres.resstatus
                    output_list.lzuordnung3 = bres.l_zuordnung[2]


    cal_revenue()

    return generate_output()