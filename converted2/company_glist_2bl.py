#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from functions.htpdate import htpdate
from functions.calc_servtaxesbl import calc_servtaxesbl
from models import Bill, Guest, Htparam, Artikel, Res_line, Waehrung, Zimkateg, Genstat, Guest_pr, Arrangement, Argt_line, Fixleist, Reslin_queasy

def company_glist_2bl(sort_rmcat:bool, fr_date:date, to_date:date, curr_gastnr:int):

    prepare_cache ([Bill, Guest, Htparam, Artikel, Res_line, Waehrung, Zimkateg, Genstat, Guest_pr, Arrangement, Argt_line, Fixleist, Reslin_queasy])

    output_list_data = []
    curr_date:date = None
    datum:date = None
    todate:date = None
    zikatnr:int = 0
    tot_nr:int = 0
    tot_zipreis:Decimal = to_decimal("0.0")
    tot_amount:Decimal = to_decimal("0.0")
    tot_night:int = 0
    tot_lodging:Decimal = to_decimal("0.0")
    tot_bfast:Decimal = to_decimal("0.0")
    tot_adroom:Decimal = to_decimal("0.0")
    tot_exbed:Decimal = to_decimal("0.0")
    gr_zipreis:Decimal = to_decimal("0.0")
    gr_amount:Decimal = to_decimal("0.0")
    gr_night:int = 0
    gr_lodging:Decimal = to_decimal("0.0")
    gr_bfast:Decimal = to_decimal("0.0")
    gr_adroom:Decimal = to_decimal("0.0")
    gr_exbed:Decimal = to_decimal("0.0")
    ct:string = ""
    take_it:bool = False
    contcode:string = ""
    f_betrag:Decimal = to_decimal("0.0")
    argt_betrag:Decimal = to_decimal("0.0")
    qty:int = 0
    bfast_art:int = 0
    lunch_art:int = 0
    dinner_art:int = 0
    lundin_art:int = 0
    fb_dept:int = 0
    exchg_rate:Decimal = 1
    frate:Decimal = to_decimal("0.0")
    argt_rate:Decimal = to_decimal("0.0")
    add_it:bool = False
    delta:int = 0
    start_date:date = None
    actflag1:int = 0
    actflag2:int = 0
    serv2:Decimal = to_decimal("0.0")
    vat2:Decimal = to_decimal("0.0")
    vat3:Decimal = to_decimal("0.0")
    vat4:Decimal = to_decimal("0.0")
    fact2:Decimal = to_decimal("0.0")
    find__code:string = ""
    pr_code:string = ""
    i:int = 0
    a:Decimal = to_decimal("0.0")
    bill = guest = htparam = artikel = res_line = waehrung = zimkateg = genstat = guest_pr = arrangement = argt_line = fixleist = reslin_queasy = None

    output_list = t_output = tbill = rguest = argtline = None

    output_list_data, Output_list = create_model("Output_list", {"ankunft":date, "abreise":date, "zinr":string, "resnr":int, "regno":int, "gname":string, "night":int, "zipreis":Decimal, "amount":Decimal, "str":string, "nr":int, "rmcat":string, "verstat":int, "bill_no":int, "lodging":Decimal, "bfast":Decimal, "lunch":Decimal, "dinner":Decimal, "ex_bed":Decimal, "add_room":Decimal, "pr_code":string})

    T_output = Output_list
    t_output_data = output_list_data

    Tbill = create_buffer("Tbill",Bill)
    Rguest = create_buffer("Rguest",Guest)
    Argtline = create_buffer("Argtline",Argt_line)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal output_list_data, curr_date, datum, todate, zikatnr, tot_nr, tot_zipreis, tot_amount, tot_night, tot_lodging, tot_bfast, tot_adroom, tot_exbed, gr_zipreis, gr_amount, gr_night, gr_lodging, gr_bfast, gr_adroom, gr_exbed, ct, take_it, contcode, f_betrag, argt_betrag, qty, bfast_art, lunch_art, dinner_art, lundin_art, fb_dept, exchg_rate, frate, argt_rate, add_it, delta, start_date, actflag1, actflag2, serv2, vat2, vat3, vat4, fact2, find__code, pr_code, i, a, bill, guest, htparam, artikel, res_line, waehrung, zimkateg, genstat, guest_pr, arrangement, argt_line, fixleist, reslin_queasy
        nonlocal sort_rmcat, fr_date, to_date, curr_gastnr
        nonlocal t_output, tbill, rguest, argtline


        nonlocal output_list, t_output, tbill, rguest, argtline
        nonlocal output_list_data

        return {"output-list": output_list_data}

    def get_argtline_rate(contcode:string, argt_recid:int):

        nonlocal output_list_data, curr_date, datum, todate, zikatnr, tot_nr, tot_zipreis, tot_amount, tot_night, tot_lodging, tot_bfast, tot_adroom, tot_exbed, gr_zipreis, gr_amount, gr_night, gr_lodging, gr_bfast, gr_adroom, gr_exbed, ct, take_it, f_betrag, argt_betrag, qty, bfast_art, lunch_art, dinner_art, lundin_art, fb_dept, exchg_rate, frate, argt_rate, add_it, delta, start_date, actflag1, actflag2, serv2, vat2, vat3, vat4, fact2, find__code, pr_code, i, a, bill, guest, htparam, artikel, res_line, waehrung, zimkateg, genstat, guest_pr, arrangement, argt_line, fixleist, reslin_queasy
        nonlocal sort_rmcat, fr_date, to_date, curr_gastnr
        nonlocal t_output, tbill, rguest, argtline


        nonlocal output_list, t_output, tbill, rguest, argtline
        nonlocal output_list_data

        add_it = False
        argt_betrag = to_decimal("0.0")
        qty = 0
        curr_zikatnr:int = 0
        argtline = None

        def generate_inner_output():
            return (add_it, argt_betrag, qty)

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

                if argt_betrag == 0:
                    add_it = False

                return generate_inner_output()

            if contcode != "":

                reslin_queasy = get_cache (Reslin_queasy, {"key": [(eq, "argt-line")],"char1": [(eq, contcode)],"number1": [(eq, res_line.reserve_int)],"number2": [(eq, arrangement.argtnr)],"number3": [(eq, argtline.argt_artnr)],"resnr": [(eq, argtline.departement)],"reslinnr": [(eq, curr_zikatnr)],"date1": [(le, curr_date)],"date2": [(ge, curr_date)]})

                if reslin_queasy:
                    argt_betrag =  to_decimal(reslin_queasy.deci1) * to_decimal(qty)

                    if argt_betrag == 0:
                        add_it = False

                    return generate_inner_output()
            argt_betrag =  to_decimal(argt_line.betrag)

            arrangement = get_cache (Arrangement, {"argtnr": [(eq, argt_line.argtnr)]})

            waehrung = get_cache (Waehrung, {"waehrungsnr": [(eq, arrangement.betriebsnr)]})

            if res_line.betriebsnr != arrangement.betriebsnr:
                argt_betrag =  to_decimal(argt_betrag) * to_decimal((waehrung.ankauf) / to_decimal(waehrung.einheit)) / to_decimal(frate)
            argt_betrag =  to_decimal(argt_betrag) * to_decimal(qty)

            if argt_betrag == 0:
                add_it = False

        return generate_inner_output()


    def get_genstat_argtline_rate(contcode:string, argt_recid:int):

        nonlocal output_list_data, curr_date, datum, todate, zikatnr, tot_nr, tot_zipreis, tot_amount, tot_night, tot_lodging, tot_bfast, tot_adroom, tot_exbed, gr_zipreis, gr_amount, gr_night, gr_lodging, gr_bfast, gr_adroom, gr_exbed, ct, take_it, f_betrag, argt_betrag, qty, bfast_art, lunch_art, dinner_art, lundin_art, fb_dept, exchg_rate, frate, argt_rate, add_it, delta, start_date, actflag1, actflag2, serv2, vat2, vat3, vat4, fact2, find__code, pr_code, i, a, bill, guest, htparam, artikel, res_line, waehrung, zimkateg, genstat, guest_pr, arrangement, argt_line, fixleist, reslin_queasy
        nonlocal sort_rmcat, fr_date, to_date, curr_gastnr
        nonlocal t_output, tbill, rguest, argtline


        nonlocal output_list, t_output, tbill, rguest, argtline
        nonlocal output_list_data

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
                argt_betrag =  to_decimal(reslin_queasy.deci1) * to_decimal(qty)

                if argt_betrag == 0:
                    add_it = False

                return generate_inner_output()

            if contcode != "":

                reslin_queasy = get_cache (Reslin_queasy, {"key": [(eq, "argt-line")],"char1": [(eq, contcode)],"number1": [(eq, res_line.reserve_int)],"number2": [(eq, arrangement.argtnr)],"number3": [(eq, argtline.argt_artnr)],"resnr": [(eq, argtline.departement)],"reslinnr": [(eq, curr_zikatnr)],"date1": [(le, curr_date)],"date2": [(ge, curr_date)]})

                if reslin_queasy:
                    argt_betrag =  to_decimal(reslin_queasy.deci1) * to_decimal(qty)

                    if argt_betrag == 0:
                        add_it = False

                    return generate_inner_output()
            argt_betrag =  to_decimal(argt_line.betrag)

            arrangement = get_cache (Arrangement, {"argtnr": [(eq, argt_line.argtnr)]})

            waehrung = get_cache (Waehrung, {"waehrungsnr": [(eq, arrangement.betriebsnr)]})

            if res_line.betriebsnr != arrangement.betriebsnr:
                argt_betrag =  to_decimal(argt_betrag) * to_decimal((waehrung.ankauf) / to_decimal(waehrung.einheit)) / to_decimal(frate)
            argt_betrag =  to_decimal(argt_betrag) * to_decimal(qty)

            if argt_betrag == 0:
                add_it = False

        return generate_inner_output()


    htparam = get_cache (Htparam, {"paramnr": [(eq, 125)]})
    bfast_art = htparam.finteger

    htparam = get_cache (Htparam, {"paramnr": [(eq, 126)]})
    fb_dept = htparam.finteger

    artikel = get_cache (Artikel, {"zwkum": [(eq, bfast_art)],"departement": [(eq, fb_dept)]})

    if not artikel and bfast_art != 0:

        return generate_output()

    htparam = get_cache (Htparam, {"paramnr": [(eq, 227)]})
    lunch_art = htparam.finteger

    artikel = get_cache (Artikel, {"zwkum": [(eq, lunch_art)],"departement": [(eq, fb_dept)]})

    if not artikel and lunch_art != 0:

        return generate_output()

    htparam = get_cache (Htparam, {"paramnr": [(eq, 228)]})
    dinner_art = htparam.finteger

    artikel = get_cache (Artikel, {"zwkum": [(eq, dinner_art)],"departement": [(eq, fb_dept)]})

    if not artikel and dinner_art != 0:

        return generate_output()

    htparam = get_cache (Htparam, {"paramnr": [(eq, 229)]})
    lundin_art = htparam.finteger

    artikel = get_cache (Artikel, {"zwkum": [(eq, lundin_art)],"departement": [(eq, fb_dept)]})

    if not artikel and lundin_art != 0:

        return generate_output()
    curr_date = get_output(htpdate(87))

    if fr_date == curr_date and to_date == curr_date:
        actflag1 = 1
        actflag2 = 1
    else:
        actflag1 = 1
        actflag2 = 2

    if sort_rmcat :

        if fr_date >= curr_date:

            for res_line in db_session.query(Res_line).filter(
                     (Res_line.gastnr == curr_gastnr) & (Res_line.active_flag >= actflag1) & (Res_line.active_flag <= actflag2) & (Res_line.resstatus != 9) & (Res_line.resstatus != 10) & (Res_line.resstatus != 12) & (Res_line.ankunft <= fr_date) & (Res_line.abreise >= to_date)).order_by(Res_line.zikatnr).all():

                waehrung = get_cache (Waehrung, {"waehrungsnr": [(eq, res_line.betriebsnr)]})
                exchg_rate =  to_decimal(waehrung.ankauf) / to_decimal(waehrung.einheit)

                if res_line.reserve_dec != 0:
                    frate =  to_decimal(reserve_dec)
                else:
                    frate =  to_decimal(exchg_rate)

                if res_line.zikatnr != zikatnr and zikatnr != 0:
                    output_list = Output_list()
                    output_list_data.append(output_list)

                    output_list.ankunft = None
                    output_list.abreise = None
                    output_list.zinr = " "
                    output_list.gname = "T O T a L"
                    output_list.resnr = 0
                    output_list.night = tot_night
                    output_list.zipreis =  to_decimal(tot_zipreis)
                    output_list.amount =  to_decimal(tot_amount)
                    output_list.lodging =  to_decimal(tot_lodging)
                    output_list.bfast =  to_decimal(tot_bfast)
                    output_list.add_room =  to_decimal(tot_adroom)
                    output_list.ex_bed =  to_decimal(tot_exbed)
                    output_list.regno = 0
                    output_list.nr = tot_nr
                    tot_zipreis =  to_decimal("0")
                    tot_night = 0
                    tot_amount =  to_decimal("0")
                    output_list.bill_no = 0


                    output_list = Output_list()
                    output_list_data.append(output_list)

                    output_list.ankunft = None
                    output_list.abreise = None
                    output_list.zinr = " "
                    output_list.gname = " "
                    output_list.resnr = 0
                    output_list.night = 0
                    output_list.zipreis =  to_decimal("0")
                    output_list.amount =  to_decimal("0")
                    output_list.lodging =  to_decimal("0")
                    output_list.bfast =  to_decimal("0")
                    output_list.add_room =  to_decimal("0")
                    output_list.ex_bed =  to_decimal("0")
                    output_list.amount =  to_decimal("0")
                    output_list.regno = 0
                    output_list.bill_no = 0


                output_list = Output_list()
                output_list_data.append(output_list)

                output_list.ankunft = res_line.ankunft
                output_list.abreise = res_line.abreise
                output_list.zinr = res_line.zinr
                output_list.gname = res_line.name
                output_list.resnr = res_line.resnr
                output_list.nr = tot_nr

                if res_line.abreise == res_line.ankunft:
                    output_list.night = 1
                else:
                    output_list.night = (res_line.abreise - res_line.ankunft).days

                zimkateg = get_cache (Zimkateg, {"zikatnr": [(eq, res_line.zikatnr)]})

                if zimkateg:
                    output_list.rmcat = zimkateg.kurzbez

                if res_line.ankunft >= curr_date:
                    output_list.zipreis =  to_decimal(res_line.zipreis)
                    output_list.amount =  to_decimal(res_line.zipreis) * to_decimal(res_line.zimmeranz) * to_decimal((res_line.abreise) - to_decimal(res_line.ankunft))
                else:

                    for genstat in db_session.query(Genstat).filter(
                             (Genstat.datum == res_line.ankunft) & (Genstat.resnr == res_line.resnr)).order_by(Genstat._recid).all():
                        output_list.zipreis =  to_decimal(genstat.zipreis)
                        output_list.amount =  to_decimal(genstat.zipreis) * to_decimal(res_line.zimmeranz) * to_decimal((res_line.abreise) - to_decimal(res_line.ankunft))

                    if output_list.zipreis == 0 and res_line.gratis == 0:
                        output_list.zipreis =  to_decimal(res_line.zipreis)
                        output_list.amount =  to_decimal(res_line.zipreis) * to_decimal(res_line.zimmeranz) * to_decimal((res_line.abreise) - to_decimal(res_line.ankunft))

                if output_list.zipreis != 0:
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

                    arrangement = get_cache (Arrangement, {"arrangement": [(eq, res_line.arrangement)]})

                    for argt_line in db_session.query(Argt_line).filter(
                             (Argt_line.argtnr == arrangement.argtnr) & not_ (Argt_line.kind2)).order_by(Argt_line._recid).all():

                        artikel = get_cache (Artikel, {"artnr": [(eq, argt_line.argt_artnr)],"departement": [(eq, argt_line.departement)]})

                        if not artikel:
                            take_it = False
                        else:
                            take_it, argt_betrag, qty = get_argtline_rate(contcode, argt_line._recid)

                        if artikel.zwkum == bfast_art and (artikel.umsatzart == 3 or artikel.umsatzart >= 5):
                            output_list.bfast =  to_decimal(output_list.bfast) + to_decimal(argt_betrag)
                            output_list.lodging =  to_decimal(output_list.zipreis) - to_decimal(argt_betrag)

                        elif artikel.zwkum == lunch_art and (artikel.umsatzart == 3 or artikel.umsatzart >= 5):
                            output_list.lunch =  to_decimal(output_list.lunch) + to_decimal(argt_betrag)
                            output_list.lodging =  to_decimal(output_list.zipreis) - to_decimal(argt_betrag)

                        elif artikel.zwkum == dinner_art and (artikel.umsatzart == 3 or artikel.umsatzart >= 5):
                            output_list.dinner =  to_decimal(output_list.dinner) + to_decimal(argt_betrag)
                            output_list.lodging =  to_decimal(output_list.zipreis) - to_decimal(argt_betrag)
                        else:
                            output_list.lodging =  to_decimal(output_list.zipreis) - to_decimal(argt_betrag)
                        output_list.lodging =  to_decimal(output_list.zipreis) - to_decimal(output_list.bfast) - to_decimal(output_list.lunch) - to_decimal(output_list.dinner)

                for fixleist in db_session.query(Fixleist).filter(
                         (Fixleist.resnr == res_line.resnr) & (Fixleist.reslinnr == res_line.reslinnr)).order_by(Fixleist._recid).all():

                    if fixleist:
                        add_it = False
                        argt_rate =  to_decimal("0")

                        if fixleist.sequenz == 1:
                            add_it = True

                        elif fixleist.sequenz == 2 or fixleist.sequenz == 3:

                            if res_line.ankunft == datum:
                                add_it = True

                        elif fixleist.sequenz == 4 and get_day(datum) == 1:
                            add_it = True

                        elif fixleist.sequenz == 5 and get_day(datum + 1) == 1:
                            add_it = True

                        elif fixleist.sequenz == 6:

                            if fixleist.lfakt == None:
                                delta = 0
                            else:
                                delta = fixleist.lfakt - res_line.ankunft

                                if delta < 0:
                                    delta = 0
                            start_date = res_line.ankunft + timedelta(days=delta)

                            if (res_line.abreise - start_date) < fixleist.dekade:
                                start_date = res_line.ankunft

                            if datum <= (start_date + timedelta(days=(fixleist.dekade - 1))):
                                add_it = True

                            if datum < start_date:
                                add_it = False

                        if add_it:

                            artikel = get_cache (Artikel, {"artnr": [(eq, fixleist.artnr)],"departement": [(eq, fixleist.departement)]})
                            argt_rate =  to_decimal(fixleist.betrag) * to_decimal(fixleist.number)

                            if artikel and artikel.artnr == 110 and argt_rate != 0:
                                output_list.ex_bed =  to_decimal(argt_rate)

                            elif artikel and artikel.artnr == 112 and argt_rate != 0:
                                output_list.add_room =  to_decimal(argt_rate)

                bill = get_cache (Bill, {"resnr": [(eq, res_line.resnr)],"reslinnr": [(eq, res_line.reslinnr)]})

                if bill:
                    output_list.regno = bill.rechnr2
                    output_list.bill_no = bill.rechnr

                tbill = get_cache (Bill, {"resnr": [(eq, output_list.resnr)],"reslinnr": [(eq, 0)]})

                if tbill:
                    output_list.verstat = tbill.rechnr
                zikatnr = res_line.zikatnr
                tot_nr = tot_nr + 1
                tot_zipreis =  to_decimal(tot_zipreis) + to_decimal(output_list.zipreis)
                tot_amount =  to_decimal(tot_amount) + to_decimal(output_list.amount)
                tot_night = tot_night + output_list.night
                tot_lodging =  to_decimal(tot_lodging) + to_decimal(output_list.lodging)
                tot_bfast =  to_decimal(tot_bfast) + to_decimal(output_list.bfast)
                tot_adroom =  to_decimal(tot_adroom) + to_decimal(output_list.add_room)
                tot_exbed =  to_decimal(tot_exbed) + to_decimal(output_list.ex_bed)


        else:

            genstat_obj_list = {}
            genstat = Genstat()
            res_line = Res_line()
            guest = Guest()
            for genstat.erwachs, genstat.kind1, genstat.kind2, genstat.zipreis, genstat.res_date, genstat.zinr, genstat.resnr, genstat.zikatnr, genstat.gratis, genstat.res_int, genstat.argt, genstat.logis, genstat.res_deci, genstat._recid, res_line.l_zuordnung, res_line.zikatnr, res_line.erwachs, res_line.kind1, res_line.kind2, res_line.resnr, res_line.reslinnr, res_line.reserve_int, res_line.betriebsnr, res_line.ankunft, res_line.abreise, res_line.zinr, res_line.name, res_line.zipreis, res_line.zimmeranz, res_line.gratis, res_line.gastnr, res_line.zimmer_wunsch, res_line.arrangement, res_line.reserve_dec, res_line.active_flag, res_line._recid, guest.name, guest._recid, guest.gastnr in db_session.query(Genstat.erwachs, Genstat.kind1, Genstat.kind2, Genstat.zipreis, Genstat.res_date, Genstat.zinr, Genstat.resnr, Genstat.zikatnr, Genstat.gratis, Genstat.res_int, Genstat.argt, Genstat.logis, Genstat.res_deci, Genstat._recid, Res_line.l_zuordnung, Res_line.zikatnr, Res_line.erwachs, Res_line.kind1, Res_line.kind2, Res_line.resnr, Res_line.reslinnr, Res_line.reserve_int, Res_line.betriebsnr, Res_line.ankunft, Res_line.abreise, Res_line.zinr, Res_line.name, Res_line.zipreis, Res_line.zimmeranz, Res_line.gratis, Res_line.gastnr, Res_line.zimmer_wunsch, Res_line.arrangement, Res_line.reserve_dec, Res_line.active_flag, Res_line._recid, Guest.name, Guest._recid, Guest.gastnr).join(Res_line,(Res_line.resnr == Genstat.resnr) & (Res_line.reslinnr == Genstat.res_int[inc_value(0)]) & (Res_line.l_zuordnung[inc_value(2)] == 0)).join(Guest,(Guest.gastnr == Genstat.gastnrmember)).filter(
                     (Genstat.datum >= fr_date) & (Genstat.datum <= to_date) & (Genstat.gastnr == curr_gastnr)).order_by(Genstat.zikatnr).all():
                if genstat_obj_list.get(genstat._recid):
                    continue
                else:
                    genstat_obj_list[genstat._recid] = True

                if genstat.zikatnr != zikatnr and zikatnr != 0:
                    output_list = Output_list()
                    output_list_data.append(output_list)

                    output_list.ankunft = None
                    output_list.abreise = None
                    output_list.zinr = " "
                    output_list.gname = "T O T a L"
                    output_list.resnr = 0
                    output_list.night = tot_night
                    output_list.zipreis =  to_decimal(tot_zipreis)
                    output_list.amount =  to_decimal(tot_amount)
                    output_list.lodging =  to_decimal(tot_lodging)
                    output_list.bfast =  to_decimal(tot_bfast)
                    output_list.add_room =  to_decimal(tot_adroom)
                    output_list.ex_bed =  to_decimal(tot_exbed)
                    output_list.regno = 0
                    output_list.nr = tot_nr
                    tot_zipreis =  to_decimal("0")
                    tot_night = 0
                    tot_amount =  to_decimal("0")
                    output_list.bill_no = 0


                    output_list = Output_list()
                    output_list_data.append(output_list)

                    output_list.ankunft = None
                    output_list.abreise = None
                    output_list.zinr = " "
                    output_list.gname = " "
                    output_list.resnr = 0
                    output_list.night = 0
                    output_list.zipreis =  to_decimal("0")
                    output_list.amount =  to_decimal("0")
                    output_list.lodging =  to_decimal("0")
                    output_list.bfast =  to_decimal("0")
                    output_list.add_room =  to_decimal("0")
                    output_list.ex_bed =  to_decimal("0")
                    output_list.amount =  to_decimal("0")
                    output_list.regno = 0
                    output_list.bill_no = 0


                output_list = Output_list()
                output_list_data.append(output_list)

                output_list.ankunft = genstat.res_date[0]
                output_list.abreise = genstat.res_date[1]
                output_list.zinr = genstat.zinr
                output_list.gname = guest.name
                output_list.resnr = genstat.resnr
                output_list.night = (genstat.res_date[1] - genstat.res_date[0]).days
                output_list.nr = tot_nr

                if genstat.res_date[1] == genstat.res_date[0]:
                    output_list.night = 1
                else:
                    output_list.night = (genstat.res_date[1] - genstat.res_date[0]).days

                if matches(res_line.zimmer_wunsch,r"*PromotionCode*"):
                    for i in range(1,num_entries(res_line.zimmer_wunsch, ";")  + 1) :
                        find__code = entry(i - 1, res_line.zimmer_wunsch, ";")

                        if matches(find__code,r"*$PRCODE$*"):
                            output_list.pr_code = trim (substring(find__code, 6))

                zimkateg = get_cache (Zimkateg, {"zikatnr": [(eq, genstat.zikatnr)]})

                if zimkateg:
                    output_list.rmcat = zimkateg.kurzbez

                if res_line.ankunft >= curr_date:
                    output_list.zipreis =  to_decimal(res_line.zipreis)
                else:
                    output_list.zipreis =  to_decimal(genstat.zipreis)

                if output_list.zipreis == 0 and genstat.gratis == 0:
                    output_list.zipreis =  to_decimal(genstat.zipreis)

                reslin_queasy = get_cache (Reslin_queasy, {"key": [(eq, "arrangement")],"resnr": [(eq, res_line.resnr)],"reslinnr": [(eq, res_line.reslinnr)]})

                if reslin_queasy:

                    if res_line.ankunft == res_line.abreise:
                        todate = res_line.abreise
                    else:
                        todate = res_line.abreise - timedelta(days=1)
                    for datum in date_range(res_line.ankunft,todate) :

                        reslin_queasy = db_session.query(Reslin_queasy).filter(
                                 (Reslin_queasy.key == ("arrangement").lower()) & (Reslin_queasy.resnr == res_line.resnr) & (Reslin_queasy.reslinnr == res_line.reslinnr) & ((Reslin_queasy.date1 == datum) | (Reslin_queasy.date2 == datum))).first()

                        if reslin_queasy:
                            output_list.amount =  to_decimal(output_list.amount) + to_decimal(reslin_queasy.deci1)
                    output_list.amount =  to_decimal(output_list.amount) * to_decimal(res_line.zimmeranz)

                elif not reslin_queasy:
                    output_list.amount =  to_decimal(res_line.zipreis) * to_decimal(res_line.zimmeranz) * to_decimal((res_line.abreise) - to_decimal(res_line.ankunft))

                bill = get_cache (Bill, {"resnr": [(eq, genstat.resnr)],"reslinnr": [(eq, genstat.res_int[0])]})

                if bill:
                    output_list.regno = bill.rechnr2
                    output_list.bill_no = bill.rechnr

                tbill = get_cache (Bill, {"resnr": [(eq, output_list.resnr)],"reslinnr": [(eq, 0)]})

                if tbill:
                    output_list.verstat = tbill.rechnr

                arrangement = get_cache (Arrangement, {"arrangement": [(eq, genstat.argt)]})

                if output_list.zipreis != 0:

                    argt_line_obj_list = {}
                    argt_line = Argt_line()
                    artikel = Artikel()
                    for argt_line.betriebsnr, argt_line.betrag, argt_line.argtnr, argt_line.argt_artnr, argt_line.departement, argt_line._recid, argt_line.vt_percnt, argt_line.fakt_modus, argt_line.intervall, artikel.umsatzart, artikel.artnr, artikel.departement, artikel.zwkum, artikel._recid in db_session.query(Argt_line.betriebsnr, Argt_line.betrag, Argt_line.argtnr, Argt_line.argt_artnr, Argt_line.departement, Argt_line._recid, Argt_line.vt_percnt, Argt_line.fakt_modus, Argt_line.intervall, Artikel.umsatzart, Artikel.artnr, Artikel.departement, Artikel.zwkum, Artikel._recid).join(Artikel,(Artikel.artnr == Argt_line.argt_artnr) & (Artikel.departement == Argt_line.departement)).filter(
                             (Argt_line.argtnr == arrangement.argtnr) & not_ (Argt_line.kind2) & (Argt_line.kind1)).order_by(Argt_line._recid).all():
                        if argt_line_obj_list.get(argt_line._recid):
                            continue
                        else:
                            argt_line_obj_list[argt_line._recid] = True


                        take_it, f_betrag, argt_betrag, qty = get_genstat_argtline_rate(contcode, argt_line._recid)

                        if artikel.zwkum == bfast_art and (artikel.umsatzart == 3 or artikel.umsatzart >= 5):
                            output_list.bfast =  to_decimal(output_list.bfast) + to_decimal(argt_betrag)

                        elif artikel.zwkum == lunch_art and (artikel.umsatzart == 3 or artikel.umsatzart >= 5):
                            output_list.lunch =  to_decimal(output_list.lunch) + to_decimal(argt_betrag)

                        elif artikel.zwkum == dinner_art and (artikel.umsatzart == 3 or artikel.umsatzart >= 5):
                            output_list.dinner =  to_decimal(output_list.dinner) + to_decimal(argt_betrag)

                        elif artikel.zwkum == lundin_art and (artikel.umsatzart == 3 or artikel.umsatzart >= 5):
                            output_list.dinner =  to_decimal(output_list.dinner) + to_decimal(argt_betrag)

                for fixleist in db_session.query(Fixleist).filter(
                         (Fixleist.resnr == res_line.resnr) & (Fixleist.reslinnr == res_line.reslinnr)).order_by(Fixleist._recid).all():

                    if fixleist:
                        add_it = False
                        argt_rate =  to_decimal("0")

                        if fixleist.sequenz == 1:
                            add_it = True

                        elif fixleist.sequenz == 2 or fixleist.sequenz == 3:

                            if res_line.ankunft == datum:
                                add_it = True

                        elif fixleist.sequenz == 4 and get_day(datum) == 1:
                            add_it = True

                        elif fixleist.sequenz == 5 and get_day(datum + 1) == 1:
                            add_it = True

                        elif fixleist.sequenz == 6:

                            if fixleist.lfakt == None:
                                delta = 0
                            else:
                                delta = fixleist.lfakt - res_line.ankunft

                                if delta < 0:
                                    delta = 0
                            start_date = res_line.ankunft + timedelta(days=delta)

                            if (res_line.abreise - start_date) < fixleist.dekade:
                                start_date = res_line.ankunft

                            if datum <= (start_date + timedelta(days=(fixleist.dekade - 1))):
                                add_it = True

                            if datum < start_date:
                                add_it = False

                        if add_it:

                            artikel = get_cache (Artikel, {"artnr": [(eq, fixleist.artnr)],"departement": [(eq, fixleist.departement)]})
                            argt_rate =  to_decimal(fixleist.betrag) * to_decimal(fixleist.number)

                            if artikel and artikel.artnr == 110 and argt_rate != 0:
                                output_list.ex_bed =  to_decimal(argt_rate)

                            elif artikel and artikel.artnr == 112 and argt_rate != 0:
                                output_list.add_room =  to_decimal(argt_rate)
                output_list.lodging =  to_decimal(output_list.lodging) + to_decimal(genstat.logis)
                zikatnr = res_line.zikatnr
                tot_nr = tot_nr + 1
                tot_zipreis =  to_decimal(tot_zipreis) + to_decimal(output_list.zipreis)
                tot_amount =  to_decimal(tot_amount) + to_decimal(output_list.amount)
                tot_night = tot_night + output_list.night
                tot_lodging =  to_decimal(tot_lodging) + to_decimal(output_list.lodging)
                tot_bfast =  to_decimal(tot_bfast) + to_decimal(output_list.bfast)
                tot_adroom =  to_decimal(tot_adroom) + to_decimal(output_list.add_room)
                tot_exbed =  to_decimal(tot_exbed) + to_decimal(output_list.ex_bed)


        output_list = Output_list()
        output_list_data.append(output_list)

        output_list.ankunft = None
        output_list.abreise = None
        output_list.zinr = " "
        output_list.gname = "T O T a L"
        output_list.resnr = 0
        output_list.night = tot_night
        output_list.zipreis =  to_decimal(tot_zipreis)
        output_list.amount =  to_decimal(tot_amount)
        output_list.lodging =  to_decimal(tot_lodging)
        output_list.bfast =  to_decimal(tot_bfast)
        output_list.add_room =  to_decimal(tot_adroom)
        output_list.ex_bed =  to_decimal(tot_exbed)
        output_list.regno = 0
        output_list.nr = tot_nr
        output_list.bill_no = 0

        for output_list in query(output_list_data):

            if output_list.gname.lower()  == ("T O T a L").lower() :
                gr_zipreis =  to_decimal(gr_zipreis) + to_decimal(output_list.zipreis)
                gr_amount =  to_decimal(gr_amount) + to_decimal(output_list.amount)
                gr_night = gr_night + output_list.night
                gr_lodging =  to_decimal(gr_lodging) + to_decimal(output_list.lodging)
                gr_bfast =  to_decimal(gr_bfast) + to_decimal(output_list.bfast)
                gr_adroom =  to_decimal(gr_adroom) + to_decimal(output_list.add_room)
                gr_exbed =  to_decimal(gr_exbed) + to_decimal(output_list.ex_bed)


        output_list = Output_list()
        output_list_data.append(output_list)

        output_list.ankunft = None
        output_list.abreise = None
        output_list.zinr = " "
        output_list.gname = "GRAND TOTAL"
        output_list.resnr = 0
        output_list.night = gr_night
        output_list.zipreis =  to_decimal(gr_zipreis)
        output_list.amount =  to_decimal(gr_amount)
        output_list.lodging =  to_decimal(gr_lodging)
        output_list.bfast =  to_decimal(gr_bfast)
        output_list.add_room =  to_decimal(gr_adroom)
        output_list.ex_bed =  to_decimal(gr_exbed)
        output_list.regno = 0
        output_list.nr = tot_nr + 1
        output_list.bill_no = 0


    else:

        if fr_date >= curr_date:

            for res_line in db_session.query(Res_line).filter(
                     (Res_line.gastnr == curr_gastnr) & (Res_line.active_flag >= actflag1) & (Res_line.active_flag <= actflag2) & (Res_line.resstatus != 9) & (Res_line.resstatus != 10) & (Res_line.resstatus != 12) & (Res_line.ankunft <= fr_date) & (Res_line.abreise >= to_date)).order_by(Res_line.ankunft).all():

                if res_line.active_flag >= 1:

                    bill = get_cache (Bill, {"resnr": [(eq, res_line.resnr)],"reslinnr": [(eq, res_line.reslinnr)]})
                output_list = Output_list()
                output_list_data.append(output_list)

                output_list.ankunft = res_line.ankunft
                output_list.abreise = res_line.abreise
                output_list.zinr = res_line.zinr
                output_list.gname = res_line.name
                output_list.resnr = res_line.resnr
                output_list.night = (res_line.abreise - res_line.ankunft).days

                if res_line.abreise == res_line.ankunft:
                    output_list.night = 1
                else:
                    output_list.night = (res_line.abreise - res_line.ankunft).days

                if matches(res_line.zimmer_wunsch,r"*PromotionCode*"):
                    for i in range(1,num_entries(res_line.zimmer_wunsch, ";")  + 1) :
                        find__code = entry(i - 1, res_line.zimmer_wunsch, ";")

                        if matches(find__code,r"*$PRCODE$*"):
                            output_list.pr_code = trim (substring(find__code, 6))

                zimkateg = get_cache (Zimkateg, {"zikatnr": [(eq, res_line.zikatnr)]})

                if zimkateg:
                    output_list.rmcat = zimkateg.kurzbez

                if res_line.ankunft >= curr_date:
                    output_list.zipreis =  to_decimal(res_line.zipreis)
                    output_list.amount =  to_decimal(res_line.zipreis) * to_decimal(res_line.zimmeranz) * to_decimal((res_line.abreise) - to_decimal(res_line.ankunft))
                else:

                    for genstat in db_session.query(Genstat).filter(
                             (Genstat.datum == res_line.ankunft) & (res_line.resnr == Genstat.resnr)).order_by(Genstat._recid).all():
                        output_list.zipreis =  to_decimal(genstat.zipreis)
                        output_list.amount =  to_decimal(genstat.zipreis) * to_decimal(res_line.zimmeranz) * to_decimal((res_line.abreise) - to_decimal(res_line.ankunft))

                    if output_list.zipreis == 0 and res_line.gratis == 0:
                        output_list.zipreis =  to_decimal(res_line.zipreis)
                        output_list.amount =  to_decimal(res_line.zipreis) * to_decimal(res_line.zimmeranz) * to_decimal((res_line.abreise) - to_decimal(res_line.ankunft))

                if output_list.zipreis != 0:
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

                    arrangement = get_cache (Arrangement, {"arrangement": [(eq, res_line.arrangement)]})

                    for argt_line in db_session.query(Argt_line).filter(
                             (Argt_line.argtnr == arrangement.argtnr) & not_ (Argt_line.kind2)).order_by(Argt_line._recid).all():

                        artikel = get_cache (Artikel, {"artnr": [(eq, argt_line.argt_artnr)],"departement": [(eq, argt_line.departement)]})

                        if not artikel:
                            take_it = False
                        else:
                            take_it, argt_betrag, qty = get_argtline_rate(contcode, argt_line._recid)

                        if artikel.zwkum == bfast_art and (artikel.umsatzart == 3 or artikel.umsatzart >= 5):
                            output_list.bfast =  to_decimal(output_list.bfast) + to_decimal(argt_betrag)
                            output_list.lodging =  to_decimal(output_list.zipreis) - to_decimal(argt_betrag)

                        elif artikel.zwkum == lunch_art and (artikel.umsatzart == 3 or artikel.umsatzart >= 5):
                            output_list.lunch =  to_decimal(output_list.lunch) + to_decimal(argt_betrag)
                            output_list.lodging =  to_decimal(output_list.zipreis) - to_decimal(argt_betrag)

                        elif artikel.zwkum == dinner_art and (artikel.umsatzart == 3 or artikel.umsatzart >= 5):
                            output_list.dinner =  to_decimal(output_list.dinner) + to_decimal(argt_betrag)
                            output_list.lodging =  to_decimal(output_list.zipreis) - to_decimal(argt_betrag)
                        else:
                            output_list.lodging =  to_decimal(output_list.zipreis) - to_decimal(argt_betrag)
                        output_list.lodging =  to_decimal(output_list.zipreis) - to_decimal(output_list.bfast) - to_decimal(output_list.lunch) - to_decimal(output_list.dinner)

                for fixleist in db_session.query(Fixleist).filter(
                         (Fixleist.resnr == res_line.resnr) & (Fixleist.reslinnr == res_line.reslinnr)).order_by(Fixleist._recid).all():

                    if fixleist:
                        add_it = False
                        argt_rate =  to_decimal("0")

                        if fixleist.sequenz == 1:
                            add_it = True

                        elif fixleist.sequenz == 2 or fixleist.sequenz == 3:

                            if res_line.ankunft == datum:
                                add_it = True

                        elif fixleist.sequenz == 4 and get_day(datum) == 1:
                            add_it = True

                        elif fixleist.sequenz == 5 and get_day(datum + 1) == 1:
                            add_it = True

                        elif fixleist.sequenz == 6:

                            if fixleist.lfakt == None:
                                delta = 0
                            else:
                                delta = fixleist.lfakt - res_line.ankunft

                                if delta < 0:
                                    delta = 0
                            start_date = res_line.ankunft + timedelta(days=delta)

                            if (res_line.abreise - start_date) < fixleist.dekade:
                                start_date = res_line.ankunft

                            if datum <= (start_date + timedelta(days=(fixleist.dekade - 1))):
                                add_it = True

                            if datum < start_date:
                                add_it = False

                        if add_it:

                            artikel = get_cache (Artikel, {"artnr": [(eq, fixleist.artnr)],"departement": [(eq, fixleist.departement)]})
                            argt_rate =  to_decimal(fixleist.betrag) * to_decimal(fixleist.number)

                            if artikel and artikel.artnr == 110 and argt_rate != 0:
                                output_list.ex_bed =  to_decimal(argt_rate)

                            elif artikel and artikel.artnr == 112 and argt_rate != 0:
                                output_list.add_room =  to_decimal(argt_rate)

                bill = get_cache (Bill, {"resnr": [(eq, res_line.resnr)],"reslinnr": [(eq, res_line.reslinnr)]})

                if bill:
                    output_list.regno = bill.rechnr2
                    output_list.bill_no = bill.rechnr

                tbill = get_cache (Bill, {"resnr": [(eq, output_list.resnr)],"reslinnr": [(eq, 0)]})

                if tbill:
                    output_list.verstat = tbill.rechnr
                zikatnr = res_line.zikatnr
                tot_nr = tot_nr + 1
                tot_zipreis =  to_decimal(tot_zipreis) + to_decimal(output_list.zipreis)
                tot_amount =  to_decimal(tot_amount) + to_decimal(output_list.amount)
                tot_night = tot_night + output_list.night
                tot_lodging =  to_decimal(tot_lodging) + to_decimal(output_list.lodging)
                tot_bfast =  to_decimal(tot_bfast) + to_decimal(output_list.bfast)
                tot_adroom =  to_decimal(tot_adroom) + to_decimal(output_list.add_room)
                tot_exbed =  to_decimal(tot_exbed) + to_decimal(output_list.ex_bed)


        else:

            genstat_obj_list = {}
            genstat = Genstat()
            res_line = Res_line()
            guest = Guest()
            for genstat.erwachs, genstat.kind1, genstat.kind2, genstat.zipreis, genstat.res_date, genstat.zinr, genstat.resnr, genstat.zikatnr, genstat.gratis, genstat.res_int, genstat.argt, genstat.logis, genstat.res_deci, genstat._recid, res_line.l_zuordnung, res_line.zikatnr, res_line.erwachs, res_line.kind1, res_line.kind2, res_line.resnr, res_line.reslinnr, res_line.reserve_int, res_line.betriebsnr, res_line.ankunft, res_line.abreise, res_line.zinr, res_line.name, res_line.zipreis, res_line.zimmeranz, res_line.gratis, res_line.gastnr, res_line.zimmer_wunsch, res_line.arrangement, res_line.reserve_dec, res_line.active_flag, res_line._recid, guest.name, guest._recid, guest.gastnr in db_session.query(Genstat.erwachs, Genstat.kind1, Genstat.kind2, Genstat.zipreis, Genstat.res_date, Genstat.zinr, Genstat.resnr, Genstat.zikatnr, Genstat.gratis, Genstat.res_int, Genstat.argt, Genstat.logis, Genstat.res_deci, Genstat._recid, Res_line.l_zuordnung, Res_line.zikatnr, Res_line.erwachs, Res_line.kind1, Res_line.kind2, Res_line.resnr, Res_line.reslinnr, Res_line.reserve_int, Res_line.betriebsnr, Res_line.ankunft, Res_line.abreise, Res_line.zinr, Res_line.name, Res_line.zipreis, Res_line.zimmeranz, Res_line.gratis, Res_line.gastnr, Res_line.zimmer_wunsch, Res_line.arrangement, Res_line.reserve_dec, Res_line.active_flag, Res_line._recid, Guest.name, Guest._recid, Guest.gastnr).join(Res_line,(Res_line.resnr == Genstat.resnr) & (Res_line.reslinnr == Genstat.res_int[inc_value(0)]) & (Res_line.l_zuordnung[inc_value(2)] == 0)).join(Guest,(Guest.gastnr == Genstat.gastnrmember)).filter(
                     (Genstat.datum >= fr_date) & (Genstat.datum <= to_date) & (Genstat.gastnr == curr_gastnr)).order_by(Genstat.res_date[inc_value(0)]).all():
                if genstat_obj_list.get(genstat._recid):
                    continue
                else:
                    genstat_obj_list[genstat._recid] = True


                output_list = Output_list()
                output_list_data.append(output_list)

                output_list.ankunft = genstat.res_date[0]
                output_list.abreise = genstat.res_date[1]
                output_list.zinr = genstat.zinr
                output_list.gname = guest.name
                output_list.resnr = genstat.resnr
                output_list.night = (genstat.res_date[1] - genstat.res_date[0]).days

                if genstat.res_date[1] == genstat.res_date[0]:
                    output_list.night = 1
                else:
                    output_list.night = (genstat.res_date[1] - genstat.res_date[0]).days

                zimkateg = get_cache (Zimkateg, {"zikatnr": [(eq, genstat.zikatnr)]})

                if zimkateg:
                    output_list.rmcat = zimkateg.kurzbez

                if res_line.ankunft >= curr_date:
                    output_list.zipreis =  to_decimal(res_line.zipreis)
                else:
                    output_list.zipreis =  to_decimal(genstat.zipreis)

                if output_list.zipreis == 0 and genstat.gratis == 0:
                    output_list.zipreis =  to_decimal(genstat.zipreis)

                if matches(res_line.zimmer_wunsch,r"*PromotionCode*"):
                    for i in range(1,num_entries(res_line.zimmer_wunsch, ";")  + 1) :
                        find__code = entry(i - 1, res_line.zimmer_wunsch, ";")

                        if matches(find__code,r"*$PRCODE$*"):
                            output_list.pr_code = trim (substring(find__code, 8))

                reslin_queasy = get_cache (Reslin_queasy, {"key": [(eq, "arrangement")],"resnr": [(eq, res_line.resnr)],"reslinnr": [(eq, res_line.reslinnr)]})

                if reslin_queasy:

                    if res_line.ankunft == res_line.abreise:
                        todate = res_line.abreise
                    else:
                        todate = res_line.abreise - timedelta(days=1)
                    for datum in date_range(res_line.ankunft,todate) :

                        reslin_queasy = db_session.query(Reslin_queasy).filter(
                                 (Reslin_queasy.key == ("arrangement").lower()) & (Reslin_queasy.resnr == res_line.resnr) & (Reslin_queasy.reslinnr == res_line.reslinnr) & ((Reslin_queasy.date1 == datum) | (Reslin_queasy.date2 == datum))).first()

                        if reslin_queasy:
                            output_list.amount =  to_decimal(output_list.amount) + to_decimal(reslin_queasy.deci1)
                    output_list.amount =  to_decimal(output_list.amount) * to_decimal(res_line.zimmeranz)

                elif not reslin_queasy:
                    output_list.amount =  to_decimal(res_line.zipreis) * to_decimal(res_line.zimmeranz) * to_decimal((res_line.abreise) - to_decimal(res_line.ankunft))

                bill = get_cache (Bill, {"resnr": [(eq, genstat.resnr)],"reslinnr": [(eq, genstat.res_int[0])]})

                if bill:
                    output_list.regno = bill.rechnr2
                    output_list.bill_no = bill.rechnr

                tbill = get_cache (Bill, {"resnr": [(eq, output_list.resnr)],"reslinnr": [(eq, 0)]})

                if tbill:
                    output_list.verstat = tbill.rechnr

                arrangement = get_cache (Arrangement, {"arrangement": [(eq, genstat.argt)]})

                if output_list.zipreis != 0:

                    argt_line_obj_list = {}
                    argt_line = Argt_line()
                    artikel = Artikel()
                    for argt_line.betriebsnr, argt_line.betrag, argt_line.argtnr, argt_line.argt_artnr, argt_line.departement, argt_line._recid, argt_line.vt_percnt, argt_line.fakt_modus, argt_line.intervall, artikel.umsatzart, artikel.artnr, artikel.departement, artikel.zwkum, artikel._recid in db_session.query(Argt_line.betriebsnr, Argt_line.betrag, Argt_line.argtnr, Argt_line.argt_artnr, Argt_line.departement, Argt_line._recid, Argt_line.vt_percnt, Argt_line.fakt_modus, Argt_line.intervall, Artikel.umsatzart, Artikel.artnr, Artikel.departement, Artikel.zwkum, Artikel._recid).join(Artikel,(Artikel.artnr == Argt_line.argt_artnr) & (Artikel.departement == Argt_line.departement)).filter(
                             (Argt_line.argtnr == arrangement.argtnr) & not_ (Argt_line.kind2) & (Argt_line.kind1)).order_by(Argt_line._recid).all():
                        if argt_line_obj_list.get(argt_line._recid):
                            continue
                        else:
                            argt_line_obj_list[argt_line._recid] = True


                        take_it, f_betrag, argt_betrag, qty = get_genstat_argtline_rate(contcode, argt_line._recid)
                        serv2, vat3, vat4, fact2 = get_output(calc_servtaxesbl(1, artikel.artnr, artikel.departement, curr_date))
                        vat3 =  to_decimal(vat3) + to_decimal(vat4)

                        if artikel.zwkum == bfast_art and (artikel.umsatzart == 3 or artikel.umsatzart >= 5):
                            output_list.bfast =  to_decimal(genstat.res_deci[1]) * to_decimal((1) + to_decimal(vat3) + to_decimal(serv2) )

                        elif artikel.zwkum == lunch_art and (artikel.umsatzart == 3 or artikel.umsatzart >= 5):
                            output_list.lunch =  to_decimal(genstat.res_deci[2]) * to_decimal((1) + to_decimal(vat3) + to_decimal(serv2) )

                        elif artikel.zwkum == dinner_art and (artikel.umsatzart == 3 or artikel.umsatzart >= 5):
                            output_list.dinner =  to_decimal(genstat.res_deci[3]) * to_decimal((1) + to_decimal(vat3) + to_decimal(serv2) )

                        elif artikel.zwkum == lundin_art and (artikel.umsatzart == 3 or artikel.umsatzart >= 5):
                            output_list.lunch =  to_decimal(genstat.res_deci[2]) * to_decimal((1) + to_decimal(vat3) + to_decimal(serv2) )


                        else:
                            a =  to_decimal(a) + to_decimal(argt_betrag)

                for fixleist in db_session.query(Fixleist).filter(
                         (Fixleist.resnr == genstat.resnr) & (Fixleist.reslinnr == genstat.res_int[0])).order_by(Fixleist._recid).all():

                    if fixleist:
                        add_it = False
                        argt_rate =  to_decimal("0")

                        if fixleist.sequenz == 1:
                            add_it = True

                        elif fixleist.sequenz == 2 or fixleist.sequenz == 3:

                            if genstat.res_date[0] == datum:
                                add_it = True

                        elif fixleist.sequenz == 4 and get_day(datum) == 1:
                            add_it = True

                        elif fixleist.sequenz == 5 and get_day(datum + 1) == 1:
                            add_it = True

                        elif fixleist.sequenz == 6:

                            if fixleist.lfakt == None:
                                delta = 0
                            else:
                                delta = fixleist.lfakt - genstat.res_date[0]

                                if delta < 0:
                                    delta = 0
                            start_date = genstat.res_date[0] + timedelta(days=delta)

                            if (genstat.res_date[1] - start_date) < fixleist.dekade:
                                start_date = genstat.res_date[0]

                            if datum <= (start_date + timedelta(days=(fixleist.dekade - 1))):
                                add_it = True

                            if datum < start_date:
                                add_it = False

                        if add_it:

                            artikel = get_cache (Artikel, {"artnr": [(eq, fixleist.artnr)],"departement": [(eq, fixleist.departement)]})
                            argt_rate =  to_decimal(fixleist.betrag) * to_decimal(fixleist.number)

                            if artikel and artikel.artnr == 110 and argt_rate != 0:
                                output_list.ex_bed =  to_decimal(argt_rate)

                            elif artikel and artikel.artnr == 112 and argt_rate != 0:
                                output_list.add_room =  to_decimal(argt_rate)
                output_list.lodging =  to_decimal(output_list.lodging) + to_decimal(genstat.logis)
                zikatnr = res_line.zikatnr
                tot_nr = tot_nr + 1
                tot_zipreis =  to_decimal(tot_zipreis) + to_decimal(output_list.zipreis)
                tot_amount =  to_decimal(tot_amount) + to_decimal(output_list.amount)
                tot_night = tot_night + output_list.night
                tot_lodging =  to_decimal(tot_lodging) + to_decimal(output_list.lodging)
                tot_bfast =  to_decimal(tot_bfast) + to_decimal(output_list.bfast)
                tot_adroom =  to_decimal(tot_adroom) + to_decimal(output_list.add_room)
                tot_exbed =  to_decimal(tot_exbed) + to_decimal(output_list.ex_bed)


        output_list = Output_list()
        output_list_data.append(output_list)

        output_list.ankunft = None
        output_list.abreise = None
        output_list.zinr = " "
        output_list.gname = "T O T a L"
        output_list.resnr = 0
        output_list.night = tot_night
        output_list.zipreis =  to_decimal(tot_zipreis)
        output_list.amount =  to_decimal(tot_amount)
        output_list.lodging =  to_decimal(tot_lodging)
        output_list.bfast =  to_decimal(tot_bfast)
        output_list.add_room =  to_decimal(tot_adroom)
        output_list.ex_bed =  to_decimal(tot_exbed)
        output_list.regno = 0
        output_list.nr = tot_nr
        output_list.bill_no = 0

        for output_list in query(output_list_data):

            if output_list.gname.lower()  == ("T O T a L").lower() :
                gr_zipreis =  to_decimal(gr_zipreis) + to_decimal(output_list.zipreis)
                gr_amount =  to_decimal(gr_amount) + to_decimal(output_list.amount)
                gr_night = gr_night + output_list.night
                gr_lodging =  to_decimal(gr_lodging) + to_decimal(output_list.lodging)
                gr_bfast =  to_decimal(gr_bfast) + to_decimal(output_list.bfast)
                gr_adroom =  to_decimal(gr_adroom) + to_decimal(output_list.add_room)
                gr_exbed =  to_decimal(gr_exbed) + to_decimal(output_list.ex_bed)


        output_list = Output_list()
        output_list_data.append(output_list)

        output_list.ankunft = None
        output_list.abreise = None
        output_list.zinr = " "
        output_list.gname = "GRAND TOTAL"
        output_list.resnr = 0
        output_list.night = gr_night
        output_list.zipreis =  to_decimal(gr_zipreis)
        output_list.amount =  to_decimal(gr_amount)
        output_list.lodging =  to_decimal(gr_lodging)
        output_list.bfast =  to_decimal(gr_bfast)
        output_list.add_room =  to_decimal(gr_adroom)
        output_list.ex_bed =  to_decimal(gr_exbed)
        output_list.regno = 0
        output_list.nr = tot_nr + 1
        output_list.bill_no = 0

    return generate_output()