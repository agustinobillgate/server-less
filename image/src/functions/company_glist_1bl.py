from functions.additional_functions import *
import decimal
from datetime import date
from functions.htpdate import htpdate
import re
from sqlalchemy import func
from functions.calc_servtaxesbl import calc_servtaxesbl
from models import Bill, Guest, Htparam, Artikel, Res_line, Waehrung, Zimkateg, Genstat, Guest_pr, Arrangement, Argt_line, Fixleist, Reslin_queasy

def company_glist_1bl(sort_rmcat:bool, fr_date:date, to_date:date, curr_gastnr:int):
    output_list_list = []
    curr_date:date = None
    datum:date = None
    todate:date = None
    zikatnr:int = 0
    tot_nr:int = 0
    tot_zipreis:decimal = 0
    tot_amount:decimal = 0
    tot_night:int = 0
    tot_lodging:decimal = 0
    tot_bfast:decimal = 0
    tot_adroom:decimal = 0
    tot_exbed:decimal = 0
    gr_zipreis:decimal = 0
    gr_amount:decimal = 0
    gr_night:int = 0
    gr_lodging:decimal = 0
    gr_bfast:decimal = 0
    gr_adroom:decimal = 0
    gr_exbed:decimal = 0
    ct:str = ""
    take_it:bool = False
    contcode:str = ""
    f_betrag:decimal = 0
    argt_betrag:decimal = 0
    qty:int = 0
    bfast_art:int = 0
    lunch_art:int = 0
    dinner_art:int = 0
    lundin_art:int = 0
    fb_dept:int = 0
    exchg_rate:decimal = 1
    frate:decimal = 0
    argt_rate:decimal = 0
    add_it:bool = False
    delta:int = 0
    start_date:date = None
    actflag1:int = 0
    actflag2:int = 0
    serv2:decimal = 0
    vat2:decimal = 0
    vat3:decimal = 0
    vat4:decimal = 0
    fact2:decimal = 0
    a:decimal = 0
    bill = guest = htparam = artikel = res_line = waehrung = zimkateg = genstat = guest_pr = arrangement = argt_line = fixleist = reslin_queasy = None

    output_list = t_output = tbill = rguest = argtline = None

    output_list_list, Output_list = create_model("Output_list", {"ankunft":date, "abreise":date, "zinr":str, "resnr":int, "regno":int, "gname":str, "night":int, "zipreis":decimal, "amount":decimal, "str":str, "nr":int, "rmcat":str, "verstat":int, "bill_no":int, "lodging":decimal, "bfast":decimal, "lunch":decimal, "dinner":decimal, "ex_bed":decimal, "add_room":decimal})

    T_output = Output_list
    t_output_list = output_list_list

    Tbill = Bill
    Rguest = Guest
    Argtline = Argt_line

    db_session = local_storage.db_session

    def generate_output():
        nonlocal output_list_list, curr_date, datum, todate, zikatnr, tot_nr, tot_zipreis, tot_amount, tot_night, tot_lodging, tot_bfast, tot_adroom, tot_exbed, gr_zipreis, gr_amount, gr_night, gr_lodging, gr_bfast, gr_adroom, gr_exbed, ct, take_it, contcode, f_betrag, argt_betrag, qty, bfast_art, lunch_art, dinner_art, lundin_art, fb_dept, exchg_rate, frate, argt_rate, add_it, delta, start_date, actflag1, actflag2, serv2, vat2, vat3, vat4, fact2, a, bill, guest, htparam, artikel, res_line, waehrung, zimkateg, genstat, guest_pr, arrangement, argt_line, fixleist, reslin_queasy
        nonlocal t_output, tbill, rguest, argtline


        nonlocal output_list, t_output, tbill, rguest, argtline
        nonlocal output_list_list
        return {"output-list": output_list_list}

    def get_argtline_rate(contcode:str, argt_recid:int):

        nonlocal output_list_list, curr_date, datum, todate, zikatnr, tot_nr, tot_zipreis, tot_amount, tot_night, tot_lodging, tot_bfast, tot_adroom, tot_exbed, gr_zipreis, gr_amount, gr_night, gr_lodging, gr_bfast, gr_adroom, gr_exbed, ct, take_it, contcode, f_betrag, argt_betrag, qty, bfast_art, lunch_art, dinner_art, lundin_art, fb_dept, exchg_rate, frate, argt_rate, add_it, delta, start_date, actflag1, actflag2, serv2, vat2, vat3, vat4, fact2, a, bill, guest, htparam, artikel, res_line, waehrung, zimkateg, genstat, guest_pr, arrangement, argt_line, fixleist, reslin_queasy
        nonlocal t_output, tbill, rguest, argtline


        nonlocal output_list, t_output, tbill, rguest, argtline
        nonlocal output_list_list

        add_it = False
        argt_betrag = 0
        qty = 0
        curr_zikatnr:int = 0

        def generate_inner_output():
            return add_it, argt_betrag, qty
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
                argt_betrag = reslin_queasy.deci1 * qty

                if argt_betrag == 0:
                    add_it = False

                return generate_inner_output()

            if contcode != "":

                reslin_queasy = db_session.query(Reslin_queasy).filter(
                        (func.lower(Reslin_queasy.key) == "argt_line") &  (func.lower(Reslin_queasy.char1) == (contcode).lower()) &  (Reslin_queasy.number1 == res_line.reserve_int) &  (Reslin_queasy.number2 == arrangement.argtnr) &  (Reslin_queasy.number3 == argtline.argt_artnr) &  (Reslin_queasy.resnr == argtline.departement) &  (Reslin_queasy.reslinnr == curr_zikatnr) &  (Reslin_queasy.curr_date >= Reslin_queasy.date1) &  (Reslin_queasy.curr_date <= Reslin_queasy.date2)).first()

                if reslin_queasy:
                    argt_betrag = reslin_queasy.deci1 * qty

                    if argt_betrag == 0:
                        add_it = False

                    return generate_inner_output()
            argt_betrag = argt_line.betrag

            arrangement = db_session.query(Arrangement).filter(
                    (Arrangement.argtnr == argt_line.argtnr)).first()

            waehrung = db_session.query(Waehrung).filter(
                    (Waehrungsnr == arrangement.betriebsnr)).first()

            if res_line.betriebsnr != arrangement.betriebsnr:
                argt_betrag = argt_betrag * (waehrung.ankauf / waehrung.einheit) / frate
            argt_betrag = argt_betrag * qty

            if argt_betrag == 0:
                add_it = False


        return generate_inner_output()

    def get_genstat_argtline_rate(contcode:str, argt_recid:int):

        nonlocal output_list_list, curr_date, datum, todate, zikatnr, tot_nr, tot_zipreis, tot_amount, tot_night, tot_lodging, tot_bfast, tot_adroom, tot_exbed, gr_zipreis, gr_amount, gr_night, gr_lodging, gr_bfast, gr_adroom, gr_exbed, ct, take_it, contcode, f_betrag, argt_betrag, qty, bfast_art, lunch_art, dinner_art, lundin_art, fb_dept, exchg_rate, frate, argt_rate, add_it, delta, start_date, actflag1, actflag2, serv2, vat2, vat3, vat4, fact2, a, bill, guest, htparam, artikel, res_line, waehrung, zimkateg, genstat, guest_pr, arrangement, argt_line, fixleist, reslin_queasy
        nonlocal t_output, tbill, rguest, argtline


        nonlocal output_list, t_output, tbill, rguest, argtline
        nonlocal output_list_list

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
                argt_betrag = reslin_queasy.deci1 * qty

                if argt_betrag == 0:
                    add_it = False

                return generate_inner_output()

            if contcode != "":

                reslin_queasy = db_session.query(Reslin_queasy).filter(
                        (func.lower(Reslin_queasy.key) == "argt_line") &  (func.lower(Reslin_queasy.char1) == (contcode).lower()) &  (Reslin_queasy.number1 == res_line.reserve_int) &  (Reslin_queasy.number2 == arrangement.argtnr) &  (Reslin_queasy.number3 == argtline.argt_artnr) &  (Reslin_queasy.resnr == argtline.departement) &  (Reslin_queasy.reslinnr == curr_zikatnr) &  (Reslin_queasy.curr_date >= Reslin_queasy.date1) &  (Reslin_queasy.curr_date <= Reslin_queasy.date2)).first()

                if reslin_queasy:
                    argt_betrag = reslin_queasy.deci1 * qty

                    if argt_betrag == 0:
                        add_it = False

                    return generate_inner_output()
            argt_betrag = argt_line.betrag

            arrangement = db_session.query(Arrangement).filter(
                    (Arrangement.argtnr == argt_line.argtnr)).first()

            waehrung = db_session.query(Waehrung).filter(
                    (Waehrungsnr == arrangement.betriebsnr)).first()

            if res_line.betriebsnr != arrangement.betriebsnr:
                argt_betrag = argt_betrag * (waehrung.ankauf / waehrung.einheit) / frate
            argt_betrag = argt_betrag * qty

            if argt_betrag == 0:
                add_it = False


        return generate_inner_output()

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 125)).first()
    bfast_art = finteger

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 126)).first()
    fb_dept = finteger

    artikel = db_session.query(Artikel).filter(
            (Artikel.zwkum == bfast_art) &  (Artikel.departement == fb_dept)).first()

    if not artikel and bfast_art != 0:

        return generate_output()

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 227)).first()
    lunch_art = finteger

    artikel = db_session.query(Artikel).filter(
            (Artikel.zwkum == lunch_art) &  (Artikel.departement == fb_dept)).first()

    if not artikel and lunch_art != 0:

        return generate_output()

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 228)).first()
    dinner_art = finteger

    artikel = db_session.query(Artikel).filter(
            (Artikel.zwkum == dinner_art) &  (Artikel.departement == fb_dept)).first()

    if not artikel and dinner_art != 0:

        return generate_output()

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 229)).first()
    lundin_art = finteger

    artikel = db_session.query(Artikel).filter(
            (Artikel.zwkum == lundin_art) &  (Artikel.departement == fb_dept)).first()

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
                    (Res_line.gastnr == curr_gastnr) &  (Res_line.active_flag >= actflag1) &  (Res_line.active_flag <= actflag2) &  (Res_line.resstatus != 9) &  (Res_line.resstatus != 10) &  (Res_line.resstatus != 12) &  (Res_line.ankunft <= fr_date) &  (Res_line.abreise >= to_date)).all():

                waehrung = db_session.query(Waehrung).filter(
                        (Waehrungsnr == res_line.betriebsnr)).first()
                exchg_rate = waehrung.ankauf / waehrung.einheit

                if res_line.reserve_dec != 0:
                    frate = reserve_dec
                else:
                    frate = exchg_rate

                if res_line.zikatnr != zikatnr and zikatnr != 0:
                    output_list = Output_list()
                    output_list_list.append(output_list)

                    output_list.ankunft = None
                    output_list.abreise = None
                    output_list.zinr = " "
                    output_list.gname = "T O T a L"
                    output_list.resnr = 0
                    output_list.night = tot_night
                    output_list.zipreis = tot_zipreis
                    output_list.amount = tot_amount
                    output_list.lodging = tot_lodging
                    output_list.bfast = tot_bfast
                    output_list.add_room = tot_adroom
                    output_list.ex_bed = tot_exbed
                    output_list.regno = 0
                    output_list.nr = tot_nr
                    tot_zipreis = 0
                    tot_night = 0
                    tot_amount = 0
                    output_list.bill_no = 0


                    output_list = Output_list()
                    output_list_list.append(output_list)

                    output_list.ankunft = None
                    output_list.abreise = None
                    output_list.zinr = " "
                    output_list.gname = " "
                    output_list.resnr = 0
                    output_list.night = 0
                    output_list.zipreis = 0
                    output_list.amount = 0
                    output_list.lodging = 0
                    output_list.bfast = 0
                    output_list.add_room = 0
                    output_list.ex_bed = 0
                    output_list.amount = 0
                    output_list.regno = 0
                    output_list.bill_no = 0


                output_list = Output_list()
                output_list_list.append(output_list)

                output_list.ankunft = res_line.ankunft
                output_list.abreise = res_line.abreise
                output_list.zinr = res_line.zinr
                output_list.gname = res_line.name
                output_list.resnr = res_line.resnr
                output_list.nr = tot_nr

                if res_line.abreise == res_line.ankunft:
                    output_list.night = 1
                else:
                    output_list.night = res_line.abreise - res_line.ankunft

                zimkateg = db_session.query(Zimkateg).filter(
                        (Zimkateg.zikatnr == res_line.zikatnr)).first()

                if zimkateg:
                    output_list.rmcat = zimkateg.kurzbez

                if res_line.ankunft >= curr_date:
                    output_list.zipreis = res_line.zipreis
                    output_list.amount = res_line.zipreis * res_line.zimmeranz * (res_line.abreise - res_line.ankunft)
                else:

                    for genstat in db_session.query(Genstat).filter(
                            (Genstat.datum == res_line.ankunft) &  (Genstat.resnr == res_line.resnr)).all():
                        output_list.zipreis = genstat.zipreis
                        output_list.amount = genstat.zipreis * res_line.zimmeranz * (res_line.abreise - res_line.ankunft)

                    if output_list.zipreis == 0 and res_line.gratis == 0:
                        output_list.zipreis = res_line.zipreis
                        output_list.amount = res_line.zipreis * res_line.zimmeranz * (res_line.abreise - res_line.ankunft)

                if output_list.zipreis != 0:
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

                    arrangement = db_session.query(Arrangement).filter(
                            (Arrangement == res_line.arrangement)).first()

                    for argt_line in db_session.query(Argt_line).filter(
                            (Argt_line.argtnr == arrangement.argtnr) &  (not Argt_line.kind2)).all():

                        artikel = db_session.query(Artikel).filter(
                                (Artikel.artnr == argt_line.argt_artnr) &  (Artikel.departement == argt_line.departement)).first()

                        if not artikel:
                            take_it = False
                        else:
                            take_it, argt_betrag, qty = get_argtline_rate(contcode, argt_line._recid)

                        if artikel.zwkum == bfast_art and (artikel.umsatzart == 3 or artikel.umsatzart >= 5):
                            output_list.bfast = output_list.bfast + argt_betrag
                            output_list.lodging = output_list.zipreis - argt_betrag

                        elif artikel.zwkum == lunch_art and (artikel.umsatzart == 3 or artikel.umsatzart >= 5):
                            output_list.lunch = output_list.lunch + argt_betrag
                            output_list.lodging = output_list.zipreis - argt_betrag

                        elif artikel.zwkum == dinner_art and (artikel.umsatzart == 3 or artikel.umsatzart >= 5):
                            output_list.dinner = output_list.dinner + argt_betrag
                            output_list.lodging = output_list.zipreis - argt_betrag
                        else:
                            output_list.lodging = output_list.zipreis - argt_betrag
                        output_list.lodging = output_list.zipreis - output_list.bfast - output_list.lunch - output_list.dinner

                for fixleist in db_session.query(Fixleist).filter(
                        (Fixleist.resnr == res_line.resnr) &  (Fixleist.reslinnr == res_line.reslinnr)).all():

                    if fixleist:
                        add_it = False
                        argt_rate = 0

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
                            start_date = res_line.ankunft + delta

                            if (res_line.abreise - start_date) < fixleist.dekade:
                                start_date = res_line.ankunft

                            if datum <= (start_date + (fixleist.dekade - 1)):
                                add_it = True

                            if datum < start_date:
                                add_it = False

                        if add_it:

                            artikel = db_session.query(Artikel).filter(
                                    (Artikel.artnr == fixleist.artnr) &  (Artikel.departement == fixleist.departement)).first()
                            argt_rate = fixleist.betrag * fixleist.number

                            if artikel and artikel.artnr == 110 and argt_rate != 0:
                                output_list.ex_bed = argt_rate

                            elif artikel and artikel.artnr == 112 and argt_rate != 0:
                                output_list.add_room = argt_rate

                bill = db_session.query(Bill).filter(
                        (Bill.resnr == res_line.resnr) &  (Bill.reslinnr == res_line.reslinnr)).first()

                if bill:
                    output_list.regno = bill.rechnr2
                    output_list.bill_no = bill.rechnr

                tbill = db_session.query(Tbill).filter(
                        (Tbill.resnr == output_list.resnr) &  (Tbill.reslinnr == 0)).first()

                if tbill:
                    output_list.verstat = tbill.rechnr
                zikatnr = res_line.zikatnr
                tot_nr = tot_nr + 1
                tot_zipreis = tot_zipreis + output_list.zipreis
                tot_amount = tot_amount + output_list.amount
                tot_night = tot_night + output_list.night
                tot_lodging = tot_lodging + output_list.lodging
                tot_bfast = tot_bfast + output_list.bfast
                tot_adroom = tot_adroom + output_list.add_room
                tot_exbed = tot_exbed + output_list.ex_bed


        else:

            genstat_obj_list = []
            for genstat, res_line, guest in db_session.query(Genstat, Res_line, Guest).join(Res_line,(Res_line.resnr == Genstat.resnr) &  (Res_line.reslinnr == Genstat.res_int[0]) &  (Res_line.l_zuordnung[2] == 0)).join(Guest,(Guest.gastnr == Genstat.gastnrmember)).filter(
                    (Genstat.datum >= fr_date) &  (Genstat.datum <= to_date) &  (Genstat.gastnr == curr_gastnr)).all():
                if genstat._recid in genstat_obj_list:
                    continue
                else:
                    genstat_obj_list.append(genstat._recid)

                if genstat.zikatnr != zikatnr and zikatnr != 0:
                    output_list = Output_list()
                    output_list_list.append(output_list)

                    output_list.ankunft = None
                    output_list.abreise = None
                    output_list.zinr = " "
                    output_list.gname = "T O T a L"
                    output_list.resnr = 0
                    output_list.night = tot_night
                    output_list.zipreis = tot_zipreis
                    output_list.amount = tot_amount
                    output_list.lodging = tot_lodging
                    output_list.bfast = tot_bfast
                    output_list.add_room = tot_adroom
                    output_list.ex_bed = tot_exbed
                    output_list.regno = 0
                    output_list.nr = tot_nr
                    tot_zipreis = 0
                    tot_night = 0
                    tot_amount = 0
                    output_list.bill_no = 0


                    output_list = Output_list()
                    output_list_list.append(output_list)

                    output_list.ankunft = None
                    output_list.abreise = None
                    output_list.zinr = " "
                    output_list.gname = " "
                    output_list.resnr = 0
                    output_list.night = 0
                    output_list.zipreis = 0
                    output_list.amount = 0
                    output_list.lodging = 0
                    output_list.bfast = 0
                    output_list.add_room = 0
                    output_list.ex_bed = 0
                    output_list.amount = 0
                    output_list.regno = 0
                    output_list.bill_no = 0


                output_list = Output_list()
                output_list_list.append(output_list)

                output_list.ankunft = genstat.res_date[0]
                output_list.abreise = genstat.res_date[1]
                output_list.zinr = genstat.zinr
                output_list.gname = guest.name
                output_list.resnr = genstat.resnr
                output_list.night = genstat.res_date[1] - genstat.res_date[0]
                output_list.nr = tot_nr

                if genstat.res_date[1] == genstat.res_date[0]:
                    output_list.night = 1
                else:
                    output_list.night = genstat.res_date[1] - genstat.res_date[0]

                zimkateg = db_session.query(Zimkateg).filter(
                        (Zimkateg.zikatnr == genstat.zikatnr)).first()

                if zimkateg:
                    output_list.rmcat = zimkateg.kurzbez

                if res_line.ankunft >= curr_date:
                    output_list.zipreis = res_line.zipreis
                else:
                    output_list.zipreis = genstat.zipreis

                if output_list.zipreis == 0 and genstat.gratis == 0:
                    output_list.zipreis = genstat.zipreis

                reslin_queasy = db_session.query(Reslin_queasy).filter(
                        (func.lower(Reslin_queasy.key) == "arrangement") &  (Reslin_queasy.resnr == res_line.resnr) &  (Reslin_queasy.reslinnr == res_line.reslinnr)).first()

                if reslin_queasy:

                    if res_line.ankunft == res_line.abreise:
                        todate = res_line.abreise
                    else:
                        todate = res_line.abreise - 1
                    for datum in range(res_line.ankunft,todate  + 1) :

                        reslin_queasy = db_session.query(Reslin_queasy).filter(
                                (func.lower(Reslin_queasy.key) == "arrangement") &  (Reslin_queasy.resnr == res_line.resnr) &  (Reslin_queasy.reslinnr == res_line.reslinnr) &  ((Reslin_queasy.date1 == datum) |  (Reslin_queasy.date2 == datum))).first()

                        if reslin_queasy:
                            output_list.amount = output_list.amount + reslin_queasy.deci1
                    output_list.amount = output_list.amount * res_line.zimmeranz

                elif not reslin_queasy:
                    output_list.amount = res_line.zipreis * res_line.zimmeranz * (res_line.abreise - res_line.ankunft)

                bill = db_session.query(Bill).filter(
                        (Bill.resnr == genstat.resnr) &  (Bill.reslinnr == genstat.res_int[0])).first()

                if bill:
                    output_list.regno = bill.rechnr2
                    output_list.bill_no = bill.rechnr

                tbill = db_session.query(Tbill).filter(
                        (Tbill.resnr == output_list.resnr) &  (Tbill.reslinnr == 0)).first()

                if tbill:
                    output_list.verstat = tbill.rechnr

                arrangement = db_session.query(Arrangement).filter(
                        (Arrangement == genstat.argt)).first()

                if output_list.zipreis != 0:

                    argt_line_obj_list = []
                    for argt_line, artikel in db_session.query(Argt_line, Artikel).join(Artikel,(Artikel.artnr == Argt_line.argt_artnr) &  (Artikel.departement == Argt_line.departement)).filter(
                            (Argt_line.argtnr == arrangement.argtnr) &  (not Argt_line.kind2) &  (Argt_line.kind1)).all():
                        if argt_line._recid in argt_line_obj_list:
                            continue
                        else:
                            argt_line_obj_list.append(argt_line._recid)


                        take_it, f_betrag, argt_betrag, qty = get_genstat_argtline_rate(contcode, argt_line._recid)

                        if artikel.zwkum == bfast_art and (artikel.umsatzart == 3 or artikel.umsatzart >= 5):
                            output_list.bfast = output_list.bfast + argt_betrag

                        elif artikel.zwkum == lunch_art and (artikel.umsatzart == 3 or artikel.umsatzart >= 5):
                            output_list.lunch = output_list.lunch + argt_betrag

                        elif artikel.zwkum == dinner_art and (artikel.umsatzart == 3 or artikel.umsatzart >= 5):
                            output_list.dinner = output_list.dinner + argt_betrag

                        elif artikel.zwkum == lundin_art and (artikel.umsatzart == 3 or artikel.umsatzart >= 5):
                            output_list.dinner = output_list.dinner + argt_betrag

                for fixleist in db_session.query(Fixleist).filter(
                        (Fixleist.resnr == res_line.resnr) &  (Fixleist.reslinnr == res_line.reslinnr)).all():

                    if fixleist:
                        add_it = False
                        argt_rate = 0

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
                            start_date = res_line.ankunft + delta

                            if (res_line.abreise - start_date) < fixleist.dekade:
                                start_date = res_line.ankunft

                            if datum <= (start_date + (fixleist.dekade - 1)):
                                add_it = True

                            if datum < start_date:
                                add_it = False

                        if add_it:

                            artikel = db_session.query(Artikel).filter(
                                    (Artikel.artnr == fixleist.artnr) &  (Artikel.departement == fixleist.departement)).first()
                            argt_rate = fixleist.betrag * fixleist.number

                            if artikel and artikel.artnr == 110 and argt_rate != 0:
                                output_list.ex_bed = argt_rate

                            elif artikel and artikel.artnr == 112 and argt_rate != 0:
                                output_list.add_room = argt_rate
                output_list.lodging = output_list.lodging + genstat.logis
                zikatnr = res_line.zikatnr
                tot_nr = tot_nr + 1
                tot_zipreis = tot_zipreis + output_list.zipreis
                tot_amount = tot_amount + output_list.amount
                tot_night = tot_night + output_list.night
                tot_lodging = tot_lodging + output_list.lodging
                tot_bfast = tot_bfast + output_list.bfast
                tot_adroom = tot_adroom + output_list.add_room
                tot_exbed = tot_exbed + output_list.ex_bed


        output_list = Output_list()
        output_list_list.append(output_list)

        output_list.ankunft = None
        output_list.abreise = None
        output_list.zinr = " "
        output_list.gname = "T O T a L"
        output_list.resnr = 0
        output_list.night = tot_night
        output_list.zipreis = tot_zipreis
        output_list.amount = tot_amount
        output_list.lodging = tot_lodging
        output_list.bfast = tot_bfast
        output_list.add_room = tot_adroom
        output_list.ex_bed = tot_exbed
        output_list.regno = 0
        output_list.nr = tot_nr
        output_list.bill_no = 0

        for output_list in query(output_list_list):

            if output_list.gname.lower()  == "T O T a L":
                gr_zipreis = gr_zipreis + output_list.zipreis
                gr_amount = gr_amount + output_list.amount
                gr_night = gr_night + output_list.night
                gr_lodging = gr_lodging + output_list.lodging
                gr_bfast = gr_bfast + output_list.bfast
                gr_adroom = gr_adroom + output_list.add_room
                gr_exbed = gr_exbed + output_list.ex_bed


        output_list = Output_list()
        output_list_list.append(output_list)

        output_list.ankunft = None
        output_list.abreise = None
        output_list.zinr = " "
        output_list.gname = "GRAND TOTAL"
        output_list.resnr = 0
        output_list.night = gr_night
        output_list.zipreis = gr_zipreis
        output_list.amount = gr_amount
        output_list.lodging = gr_lodging
        output_list.bfast = gr_bfast
        output_list.add_room = gr_adroom
        output_list.ex_bed = gr_exbed
        output_list.regno = 0
        output_list.nr = tot_nr + 1
        output_list.bill_no = 0


    else:

        if fr_date >= curr_date:

            for res_line in db_session.query(Res_line).filter(
                    (Res_line.gastnr == curr_gastnr) &  (Res_line.active_flag >= actflag1) &  (Res_line.active_flag <= actflag2) &  (Res_line.resstatus != 9) &  (Res_line.resstatus != 10) &  (Res_line.resstatus != 12) &  (Res_line.ankunft <= fr_date) &  (Res_line.abreise >= to_date)).all():

                if res_line.active_flag >= 1:

                    bill = db_session.query(Bill).filter(
                            (Bill.resnr == res_line.resnr) &  (Bill.reslinnr == res_line.reslinnr)).first()
                output_list = Output_list()
                output_list_list.append(output_list)

                output_list.ankunft = res_line.ankunft
                output_list.abreise = res_line.abreise
                output_list.zinr = res_line.zinr
                output_list.gname = res_line.name
                output_list.resnr = res_line.resnr
                output_list.night = res_line.abreise - res_line.ankunft

                if res_line.abreise == res_line.ankunft:
                    output_list.night = 1
                else:
                    output_list.night = res_line.abreise - res_line.ankunft

                zimkateg = db_session.query(Zimkateg).filter(
                        (Zimkateg.zikatnr == res_line.zikatnr)).first()

                if zimkateg:
                    output_list.rmcat = zimkateg.kurzbez

                if res_line.ankunft >= curr_date:
                    output_list.zipreis = res_line.zipreis
                    output_list.amount = res_line.zipreis * res_line.zimmeranz * (res_line.abreise - res_line.ankunft)
                else:

                    for genstat in db_session.query(Genstat).filter(
                            (Genstat.datum == res_line.ankunft) &  (res_line.resnr == Genstat.resnr)).all():
                        output_list.zipreis = genstat.zipreis
                        output_list.amount = genstat.zipreis * res_line.zimmeranz * (res_line.abreise - res_line.ankunft)

                    if output_list.zipreis == 0 and res_line.gratis == 0:
                        output_list.zipreis = res_line.zipreis
                        output_list.amount = res_line.zipreis * res_line.zimmeranz * (res_line.abreise - res_line.ankunft)

                if output_list.zipreis != 0:
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

                    arrangement = db_session.query(Arrangement).filter(
                            (Arrangement == res_line.arrangement)).first()

                    for argt_line in db_session.query(Argt_line).filter(
                            (Argt_line.argtnr == arrangement.argtnr) &  (not Argt_line.kind2)).all():

                        artikel = db_session.query(Artikel).filter(
                                (Artikel.artnr == argt_line.argt_artnr) &  (Artikel.departement == argt_line.departement)).first()

                        if not artikel:
                            take_it = False
                        else:
                            take_it, argt_betrag, qty = get_argtline_rate(contcode, argt_line._recid)

                        if artikel.zwkum == bfast_art and (artikel.umsatzart == 3 or artikel.umsatzart >= 5):
                            output_list.bfast = output_list.bfast + argt_betrag
                            output_list.lodging = output_list.zipreis - argt_betrag

                        elif artikel.zwkum == lunch_art and (artikel.umsatzart == 3 or artikel.umsatzart >= 5):
                            output_list.lunch = output_list.lunch + argt_betrag
                            output_list.lodging = output_list.zipreis - argt_betrag

                        elif artikel.zwkum == dinner_art and (artikel.umsatzart == 3 or artikel.umsatzart >= 5):
                            output_list.dinner = output_list.dinner + argt_betrag
                            output_list.lodging = output_list.zipreis - argt_betrag
                        else:
                            output_list.lodging = output_list.zipreis - argt_betrag
                        output_list.lodging = output_list.zipreis - output_list.bfast - output_list.lunch - output_list.dinner

                for fixleist in db_session.query(Fixleist).filter(
                        (Fixleist.resnr == res_line.resnr) &  (Fixleist.reslinnr == res_line.reslinnr)).all():

                    if fixleist:
                        add_it = False
                        argt_rate = 0

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
                            start_date = res_line.ankunft + delta

                            if (res_line.abreise - start_date) < fixleist.dekade:
                                start_date = res_line.ankunft

                            if datum <= (start_date + (fixleist.dekade - 1)):
                                add_it = True

                            if datum < start_date:
                                add_it = False

                        if add_it:

                            artikel = db_session.query(Artikel).filter(
                                    (Artikel.artnr == fixleist.artnr) &  (Artikel.departement == fixleist.departement)).first()
                            argt_rate = fixleist.betrag * fixleist.number

                            if artikel and artikel.artnr == 110 and argt_rate != 0:
                                output_list.ex_bed = argt_rate

                            elif artikel and artikel.artnr == 112 and argt_rate != 0:
                                output_list.add_room = argt_rate

                bill = db_session.query(Bill).filter(
                        (Bill.resnr == res_line.resnr) &  (Bill.reslinnr == res_line.reslinnr)).first()

                if bill:
                    output_list.regno = bill.rechnr2
                    output_list.bill_no = bill.rechnr

                tbill = db_session.query(Tbill).filter(
                        (Tbill.resnr == output_list.resnr) &  (Tbill.reslinnr == 0)).first()

                if tbill:
                    output_list.verstat = tbill.rechnr
                zikatnr = res_line.zikatnr
                tot_nr = tot_nr + 1
                tot_zipreis = tot_zipreis + output_list.zipreis
                tot_amount = tot_amount + output_list.amount
                tot_night = tot_night + output_list.night
                tot_lodging = tot_lodging + output_list.lodging
                tot_bfast = tot_bfast + output_list.bfast
                tot_adroom = tot_adroom + output_list.add_room
                tot_exbed = tot_exbed + output_list.ex_bed


        else:

            genstat_obj_list = []
            for genstat, res_line, guest in db_session.query(Genstat, Res_line, Guest).join(Res_line,(Res_line.resnr == Genstat.resnr) &  (Res_line.reslinnr == Genstat.res_int[0]) &  (Res_line.l_zuordnung[2] == 0)).join(Guest,(Guest.gastnr == Genstat.gastnrmember)).filter(
                    (Genstat.datum >= fr_date) &  (Genstat.datum <= to_date) &  (Genstat.gastnr == curr_gastnr)).all():
                if genstat._recid in genstat_obj_list:
                    continue
                else:
                    genstat_obj_list.append(genstat._recid)


                output_list = Output_list()
                output_list_list.append(output_list)

                output_list.ankunft = genstat.res_date[0]
                output_list.abreise = genstat.res_date[1]
                output_list.zinr = genstat.zinr
                output_list.gname = guest.name
                output_list.resnr = genstat.resnr
                output_list.night = genstat.res_date[1] - genstat.res_date[0]

                if genstat.res_date[1] == genstat.res_date[0]:
                    output_list.night = 1
                else:
                    output_list.night = genstat.res_date[1] - genstat.res_date[0]

                zimkateg = db_session.query(Zimkateg).filter(
                        (Zimkateg.zikatnr == genstat.zikatnr)).first()

                if zimkateg:
                    output_list.rmcat = zimkateg.kurzbez

                if res_line.ankunft >= curr_date:
                    output_list.zipreis = res_line.zipreis
                else:
                    output_list.zipreis = genstat.zipreis

                if output_list.zipreis == 0 and genstat.gratis == 0:
                    output_list.zipreis = genstat.zipreis

                reslin_queasy = db_session.query(Reslin_queasy).filter(
                        (func.lower(Reslin_queasy.key) == "arrangement") &  (Reslin_queasy.resnr == res_line.resnr) &  (Reslin_queasy.reslinnr == res_line.reslinnr)).first()

                if reslin_queasy:

                    if res_line.ankunft == res_line.abreise:
                        todate = res_line.abreise
                    else:
                        todate = res_line.abreise - 1
                    for datum in range(res_line.ankunft,todate  + 1) :

                        reslin_queasy = db_session.query(Reslin_queasy).filter(
                                (func.lower(Reslin_queasy.key) == "arrangement") &  (Reslin_queasy.resnr == res_line.resnr) &  (Reslin_queasy.reslinnr == res_line.reslinnr) &  ((Reslin_queasy.date1 == datum) |  (Reslin_queasy.date2 == datum))).first()

                        if reslin_queasy:
                            output_list.amount = output_list.amount + reslin_queasy.deci1
                    output_list.amount = output_list.amount * res_line.zimmeranz

                elif not reslin_queasy:
                    output_list.amount = res_line.zipreis * res_line.zimmeranz * (res_line.abreise - res_line.ankunft)

                bill = db_session.query(Bill).filter(
                        (Bill.resnr == genstat.resnr) &  (Bill.reslinnr == genstat.res_int[0])).first()

                if bill:
                    output_list.regno = bill.rechnr2
                    output_list.bill_no = bill.rechnr

                tbill = db_session.query(Tbill).filter(
                        (Tbill.resnr == output_list.resnr) &  (Tbill.reslinnr == 0)).first()

                if tbill:
                    output_list.verstat = tbill.rechnr

                arrangement = db_session.query(Arrangement).filter(
                        (Arrangement == genstat.argt)).first()

                if output_list.zipreis != 0:

                    argt_line_obj_list = []
                    for argt_line, artikel in db_session.query(Argt_line, Artikel).join(Artikel,(Artikel.artnr == Argt_line.argt_artnr) &  (Artikel.departement == Argt_line.departement)).filter(
                            (Argt_line.argtnr == arrangement.argtnr) &  (not Argt_line.kind2) &  (Argt_line.kind1)).all():
                        if argt_line._recid in argt_line_obj_list:
                            continue
                        else:
                            argt_line_obj_list.append(argt_line._recid)


                        take_it, f_betrag, argt_betrag, qty = get_genstat_argtline_rate(contcode, argt_line._recid)
                        serv2, vat3, vat4, fact2 = get_output(calc_servtaxesbl(1, artikel.artnr, artikel.departement, curr_date))
                        vat3 = vat3 + vat4

                        if artikel.zwkum == bfast_art and (artikel.umsatzart == 3 or artikel.umsatzart >= 5):
                            output_list.bfast = genstat.res_deci[1] * (1 + vat3 + serv2)

                        elif artikel.zwkum == lunch_art and (artikel.umsatzart == 3 or artikel.umsatzart >= 5):
                            output_list.lunch = genstat.res_deci[2] * (1 + vat3 + serv2)

                        elif artikel.zwkum == dinner_art and (artikel.umsatzart == 3 or artikel.umsatzart >= 5):
                            output_list.dinner = genstat.res_deci[3] * (1 + vat3 + serv2)

                        elif artikel.zwkum == lundin_art and (artikel.umsatzart == 3 or artikel.umsatzart >= 5):
                            output_list.lunch = genstat.res_deci[2] * (1 + vat3 + serv2)


                        else:
                            a = a + argt_betrag

                for fixleist in db_session.query(Fixleist).filter(
                        (Fixleist.resnr == genstat.resnr) &  (Fixleist.reslinnr == genstat.res_int[0])).all():

                    if fixleist:
                        add_it = False
                        argt_rate = 0

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
                            start_date = genstat.res_date[0] + delta

                            if (genstat.res_date[1] - start_date) < fixleist.dekade:
                                start_date = genstat.res_date[0]

                            if datum <= (start_date + (fixleist.dekade - 1)):
                                add_it = True

                            if datum < start_date:
                                add_it = False

                        if add_it:

                            artikel = db_session.query(Artikel).filter(
                                    (Artikel.artnr == fixleist.artnr) &  (Artikel.departement == fixleist.departement)).first()
                            argt_rate = fixleist.betrag * fixleist.number

                            if artikel and artikel.artnr == 110 and argt_rate != 0:
                                output_list.ex_bed = argt_rate

                            elif artikel and artikel.artnr == 112 and argt_rate != 0:
                                output_list.add_room = argt_rate
                output_list.lodging = output_list.lodging + genstat.logis
                zikatnr = res_line.zikatnr
                tot_nr = tot_nr + 1
                tot_zipreis = tot_zipreis + output_list.zipreis
                tot_amount = tot_amount + output_list.amount
                tot_night = tot_night + output_list.night
                tot_lodging = tot_lodging + output_list.lodging
                tot_bfast = tot_bfast + output_list.bfast
                tot_adroom = tot_adroom + output_list.add_room
                tot_exbed = tot_exbed + output_list.ex_bed


        output_list = Output_list()
        output_list_list.append(output_list)

        output_list.ankunft = None
        output_list.abreise = None
        output_list.zinr = " "
        output_list.gname = "T O T a L"
        output_list.resnr = 0
        output_list.night = tot_night
        output_list.zipreis = tot_zipreis
        output_list.amount = tot_amount
        output_list.lodging = tot_lodging
        output_list.bfast = tot_bfast
        output_list.add_room = tot_adroom
        output_list.ex_bed = tot_exbed
        output_list.regno = 0
        output_list.nr = tot_nr
        output_list.bill_no = 0

        for output_list in query(output_list_list):

            if output_list.gname.lower()  == "T O T a L":
                gr_zipreis = gr_zipreis + output_list.zipreis
                gr_amount = gr_amount + output_list.amount
                gr_night = gr_night + output_list.night
                gr_lodging = gr_lodging + output_list.lodging
                gr_bfast = gr_bfast + output_list.bfast
                gr_adroom = gr_adroom + output_list.add_room
                gr_exbed = gr_exbed + output_list.ex_bed


        output_list = Output_list()
        output_list_list.append(output_list)

        output_list.ankunft = None
        output_list.abreise = None
        output_list.zinr = " "
        output_list.gname = "GRAND TOTAL"
        output_list.resnr = 0
        output_list.night = gr_night
        output_list.zipreis = gr_zipreis
        output_list.amount = gr_amount
        output_list.lodging = gr_lodging
        output_list.bfast = gr_bfast
        output_list.add_room = gr_adroom
        output_list.ex_bed = gr_exbed
        output_list.regno = 0
        output_list.nr = tot_nr + 1
        output_list.bill_no = 0

    for output_list in query(output_list_list):
        output_list.amount = output_list.zipreis * output_list.night

    return generate_output()