from functions.additional_functions import *
import decimal
from datetime import date
from sqlalchemy import func
import re
from functions.ratecode_rate import ratecode_rate
from models import Htparam, Waehrung, Res_line, Zimkateg, Genstat, Arrangement, Reslin_queasy, Queasy, Katpreis, Argt_line, Artikel, Fixleist

def mk_resline_view_staycostbl(pvilanguage:int, ankunft:date, abreise:date, contcode:str, currency:str, curr_rmcat:str, curr_argt:str, rate_zikat:str, zimmer_wunsch:str, inp_gastnr:int, inp_resnr:int, inp_reslinnr:int, marketnr:int, zimmeranz:int, pax:int, kind1:int, inp_rmrate:decimal):
    output_list_list = []
    new_contrate:bool = False
    wd_array:[int] = [0, 0, 0, 0, 0, 0, 0, 0, 0]
    bonus_array:[bool] = [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None]
    ci_date:date = None
    lvcarea:str = "view_staycost"
    htparam = waehrung = res_line = zimkateg = genstat = arrangement = reslin_queasy = queasy = katpreis = argt_line = artikel = fixleist = None

    output_list = w1 = None

    output_list_list, Output_list = create_model("Output_list", {"flag":int, "str":str, "str1":str})

    W1 = Waehrung

    db_session = local_storage.db_session

    def generate_output():
        nonlocal output_list_list, new_contrate, wd_array, bonus_array, ci_date, lvcarea, htparam, waehrung, res_line, zimkateg, genstat, arrangement, reslin_queasy, queasy, katpreis, argt_line, artikel, fixleist
        nonlocal w1


        nonlocal output_list, w1
        nonlocal output_list_list
        return {"output-list": output_list_list}

    def get_rackrate(erwachs:int, kind1:int, kind2:int):

        nonlocal output_list_list, new_contrate, wd_array, bonus_array, ci_date, lvcarea, htparam, waehrung, res_line, zimkateg, genstat, arrangement, reslin_queasy, queasy, katpreis, argt_line, artikel, fixleist
        nonlocal w1


        nonlocal output_list, w1
        nonlocal output_list_list

        rate:decimal = 0

        if erwachs >= 1 and erwachs <= 4:
            rate = rate + katpreis.perspreis[erwachs - 1]
        rate = rate + kind1 * katpreis.kindpreis[0] + kind2 * katpreis.kindpreis[1]
        return rate

    def cal_revenue():

        nonlocal output_list_list, new_contrate, wd_array, bonus_array, ci_date, lvcarea, htparam, waehrung, res_line, zimkateg, genstat, arrangement, reslin_queasy, queasy, katpreis, argt_line, artikel, fixleist
        nonlocal w1


        nonlocal output_list, w1
        nonlocal output_list_list

        datum:date = None
        co_date:date = None
        argt_rate:decimal = 0
        rm_rate:decimal = 0
        daily_rate:decimal = 0
        tot_rate:decimal = 0
        add_it:bool = False
        c:str = ""
        fixed_rate:bool = False
        argt_defined:bool = False
        delta:int = 0
        start_date:date = None
        qty:int = 0
        it_exist:bool = False
        exrate1:decimal = 1
        ex2:decimal = 1
        pax:int = 0
        child1:int = 0
        n:int = 0
        created_date:date = None
        bill_date:date = None
        curr_zikatnr:int = 0
        curr_i:int = 0
        w_day:int = 0
        rack_rate:bool = False
        ebdisc_flag:bool = False
        kbdisc_flag:bool = False
        rate_found:bool = False
        early_flag:bool = False
        kback_flag:bool = False
        fix_exrate:decimal = 0
        W1 = Waehrung

        res_line = db_session.query(Res_line).filter(
                (Res_line.resnr == inp_resnr) &  (Res_line.reslinnr == inp_reslinnr)).first()

        if res_line:
            fix_exrate = res_line.reserve_dec
        n = 0

        if re.match(".*DATE,.*",zimmer_wunsch):
            n = 1 + get_index(zimmer_wunsch, "Date,")

        if n > 0:
            c = substring(zimmer_wunsch, n + 5 - 1, 8)
            created_date = date_mdy(to_int(substring(c, 4, 2)) , to_int(substring(c, 6, 2)) , to_int(substring(c, 0, 4)))

        if created_date == None:
            created_date = ci_date
        ebdisc_flag = re.match(".*ebdisc.*",zimmer_wunsch)
        kbdisc_flag = re.match(".*kbdisc.*",zimmer_wunsch)

        if rate_zikat != "":

            zimkateg = db_session.query(Zimkateg).filter(
                    (func.lower(Zimkateg.kurzbez) == (rate_zikat).lower())).first()
            curr_zikatnr = zimkateg.zikatnr
        else:

            zimkateg = db_session.query(Zimkateg).filter(
                    (func.lower(Zimkateg.kurzbez) == (curr_rmcat).lower())).first()
            curr_zikatnr = zimkateg.zikatnr
        co_date = abreise

        if abreise > ankunft:
            co_date = co_date - 1
        for datum in range(ankunft,co_date + 1) :
            curr_i = curr_i + 1
            bill_date = datum
            argt_rate = 0
            daily_rate = 0
            fixed_rate = False

            if datum < ci_date:
                rm_rate = None

                genstat = db_session.query(Genstat).filter(
                        (Genstat.datum == datum) &  (Genstat.resnr == inp_resnr) &  (Genstat.res_int[0] == inp_reslinnr)).first()

                if genstat:
                    rm_rate = genstat.zipreis

                    arrangement = db_session.query(Arrangement).filter(
                            (Arrangement == genstat.argt)).first()

            if datum >= ci_date or not arrangement:

                arrangement = db_session.query(Arrangement).filter(
                        (func.lower(Arrangement) == (curr_argt).lower())).first()

            if (datum >= ci_date) or rm_rate == None:

                reslin_queasy = db_session.query(Reslin_queasy).filter(
                        (func.lower(Reslin_queasy.key) == "arrangement") &  (Reslin_queasy.resnr == inp_resnr) &  (Reslin_queasy.reslinnr == inp_reslinnr) &  (Reslin_queasy.datum >= Reslin_queasy.date1) &  (Reslin_queasy.datum <= Reslin_queasy.date2)).first()

                if reslin_queasy:
                    fixed_rate = True
                    rm_rate = reslin_queasy.deci1

                    if reslin_queasy.number3 != 0:
                        pax = reslin_queasy.number3

                    if reslin_queasy.char1 != "":

                        arrangement = db_session.query(Arrangement).filter(
                                (Arrangement == reslin_queasy.char1)).first()

                if not fixed_rate:

                    if contcode != "":

                        queasy = db_session.query(Queasy).filter(
                                (Queasy.key == 18) &  (Queasy.number1 == marketnr)).first()

                        if queasy and queasy.logi3:
                            bill_date = ankunft
                        rate_found, rm_rate, early_flag, kback_flag = get_output(ratecode_rate(ebdisc_flag, kbdisc_flag, inp_resnr, inp_reslinnr, contcode, None, bill_date, ankunft, abreise, marketnr, arrangement.argtnr, curr_zikatnr, pax, kind1, 0, fix_exrate, waehrungsnr))

                    if not rate_found:
                        w_day = wd_array[get_weekday(bill_date) - 1]

                        if (bill_date == ci_date) or (bill_date == ankunft):
                            rm_rate = inp_rmrate

                            katpreis = db_session.query(Katpreis).filter(
                                    (Katpreis.zikat == curr_zikatnr) &  (Katpreis.argtnr == arrangement.argtnr) &  (Katpreis.startperiode <= bill_date) &  (Katpreis.endperiode >= bill_date) &  (Katpreis.betriebsnr == w_day)).first()

                            if not katpreis:

                                katpreis = db_session.query(Katpreis).filter(
                                        (Katpreis.zikat == curr_zikatnr) &  (Katpreis.argtnr == arrangement.argtnr) &  (Katpreis.startperiode <= bill_date) &  (Katpreis.endperiode >= bill_date) &  (Katpreis.betriebsnr == 0)).first()

                            if katpreis and get_rackrate (pax, kind1, 0) == rm_rate:
                                rack_rate = True

                        elif rack_rate:

                            katpreis = db_session.query(Katpreis).filter(
                                    (Katpreis.zikat == curr_zikatnr) &  (Katpreis.argtnr == arrangement.argtnr) &  (Katpreis.startperiode <= bill_date) &  (Katpreis.endperiode >= bill_date) &  (Katpreis.betriebsnr == w_day)).first()

                            if not katpreis:

                                katpreis = db_session.query(Katpreis).filter(
                                        (Katpreis.zikat == curr_zikatnr) &  (Katpreis.argtnr == arrangement.argtnr) &  (Katpreis.startperiode <= bill_date) &  (Katpreis.endperiode >= bill_date) &  (Katpreis.betriebsnr == 0)).first()

                            if katpreis and get_rackrate (pax, kind1, 0) > 0:
                                rm_rate = get_rackrate (pax, kind1, 0)

                        if bonus_array[curr_i - 1] :
                            rm_rate = 0
            output_list = Output_list()
            output_list_list.append(output_list)

            STR = to_string(datum) + "   " + translateExtended ("Roomrate", lvcarea, "") + "    ==  " + trim(to_string(rm_rate, "->>>,>>>,>>9.99"))
            tot_rate = tot_rate + rm_rate
            daily_rate = rm_rate

            if rm_rate != 0:

                for argt_line in db_session.query(Argt_line).filter(
                        (Argt_line.argtnr == arrangement.argtnr) &  (not Argt_line.kind2)).all():
                    add_it = False

                    if argt_line.vt_percnt == 0:

                        if argt_line.betriebsnr == 0:
                            qty = pax
                        else:
                            qty = argt_line.betriebsnr

                    elif argt_line.vt_percnt == 1:
                        qty = kind1

                    elif argt_line.vt_percnt == 2:
                        qty = 0

                    if qty > 0:

                        if argt_line.fakt_modus == 1:
                            add_it = True

                        elif argt_line.fakt_modus == 2:

                            if ankunft == datum:
                                add_it = True

                        elif argt_line.fakt_modus == 3:

                            if (ankunft + 1) == datum:
                                add_it = True

                        elif argt_line.fakt_modus == 4 and get_day(datum) == 1:
                            add_it = True

                        elif argt_line.fakt_modus == 5 and get_day(datum + 1) == 1:
                            add_it = True

                        elif argt_line.fakt_modus == 6:

                            if (ankunft + (argt_line.intervall - 1)) >= datum:
                                add_it = True

                    if add_it:

                        artikel = db_session.query(Artikel).filter(
                                (Artikel.artnr == argt_line.argt_artnr) &  (Artikel.departement == argt_line.departement)).first()
                        argt_rate = argt_line.betrag
                        argt_defined = False

                        reslin_queasy = db_session.query(Reslin_queasy).filter(
                                (func.lower(Reslin_queasy.key) == "fargt_line") &  (Reslin_queasy.char1 == "") &  (Reslin_queasy.number1 == argt_line.departement) &  (Reslin_queasy.number2 == argt_line.argtnr) &  (Reslin_queasy.resnr == inp_resnr) &  (Reslin_queasy.reslinnr == inp_reslinnr) &  (Reslin_queasy.number3 == argt_line.argt_artnr) &  (Reslin_queasy.bill_date >= Reslin_queasy.date1) &  (Reslin_queasy.bill_date <= Reslin_queasy.date2)).first()

                        if reslin_queasy:
                            argt_defined = True

                            if argt_line.vt_percnt == 0:
                                argt_rate = reslin_queasy.deci1

                            elif argt_line.vt_percnt == 1:
                                argt_rate = reslin_queasy.deci2

                            elif argt_line.vt_percnt == 2:
                                argt_rate = reslin_queasy.deci3

                        if guest_pr and not argt_defined:

                            reslin_queasy = db_session.query(Reslin_queasy).filter(
                                    (func.lower(Reslin_queasy.key) == "argt_line") &  (func.lower(Reslin_queasy.char1) == (contcode).lower()) &  (Reslin_queasy.number1 == marketnr) &  (Reslin_queasy.number2 == arrangement.argtnr) &  (Reslin_queasy.reslinnr == curr_zikatnr) &  (Reslin_queasy.number3 == argt_line.argt_artnr) &  (Reslin_queasy.resnr == argt_line.departement) &  (Reslin_queasy.bill_date >= Reslin_queasy.date1) &  (Reslin_queasy.bill_date <= Reslin_queasy.date2)).first()

                            if reslin_queasy:

                                if argt_line.vt_percnt == 0:
                                    argt_rate = reslin_queasy.deci1

                                elif argt_line.vt_percnt == 1:
                                    argt_rate = reslin_queasy.deci2

                                elif argt_line.vt_percnt == 2:
                                    argt_rate = reslin_queasy.deci3
                        argt_rate = argt_rate * qty
                        output_list = Output_list()
                        output_list_list.append(output_list)

                        output_list.flag = 1
                        c = to_string(qty) + " " + artikel.bezeich
                        STR = to_string(translateExtended ("     Incl.", lvcarea, "") , "x(10)") + " " + to_string(c, "x(16)") + "  ==  " + trim(to_string(argt_rate, "->>>,>>>,>>9.99"))


            for fixleist in db_session.query(Fixleist).filter(
                    (Fixleist.resnr == inp_resnr) &  (Fixleist.reslinnr == inp_reslinnr)).all():
                add_it = False
                argt_rate = 0

                if fixleist.sequenz == 1:
                    add_it = True

                elif fixleist.sequenz == 2 or fixleist.sequenz == 3:

                    if ankunft == datum:
                        add_it = True

                elif fixleist.sequenz == 4 and get_day(datum) == 1:
                    add_it = True

                elif fixleist.sequenz == 5 and get_day(datum + 1) == 1:
                    add_it = True

                elif fixleist.sequenz == 6:

                    if fixleist.lfakt == None:
                        delta = 0
                    else:
                        delta = fixleist.lfakt - ankunft

                        if delta < 0:
                            delta = 0
                    start_date = ankunft + delta

                    if (abreise - start_date) < fixleist.dekade:
                        start_date = ankunft

                    if datum <= (start_date + (fixleist.dekade - 1)):
                        add_it = True

                    if datum < start_date:
                        add_it = False

                if add_it:

                    artikel = db_session.query(Artikel).filter(
                            (Artikel.artnr == fixleist.artnr) &  (Artikel.departement == fixleist.departement)).first()
                    argt_rate = fixleist.betrag * fixleist.number

                if argt_rate != 0:
                    output_list = Output_list()
                    output_list_list.append(output_list)

                    STR = to_string("", "x(8)") + "   " + to_string(artikel.bezeich, "x(16)") + "  ==  " + trim(to_string(argt_rate, "->>>,>>>,>>9.99"))
                    tot_rate = tot_rate + argt_rate
                    daily_rate = daily_rate + argt_rate
            STR = STR + "  Total  ==  " + trim(to_string(daily_rate, "->>>,>>>,>>9.99"))
        output_list = Output_list()
        output_list_list.append(output_list)

        STR = "  " + translateExtended ("Expected total revenue     == ", lvcarea, "") +\
                " " + trim(to_string(tot_rate, "->,>>>,>>>,>>9.99"))
        str1 = "expected"

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 87)).first()
    ci_date = htparam.fdate

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 550)).first()

    if htparam.feldtyp == 4:
        new_contrate = htparam.flogical

    waehrung = db_session.query(Waehrung).filter(
            (func.lower(Waehrung.wabkurz) == (currency).lower())).first()

    if not waehrung:

        waehrung = db_session.query(Waehrung).filter(
                (func.lower(Waehrung.wabkurz) == "1")).first()
    cal_revenue()

    return generate_output()