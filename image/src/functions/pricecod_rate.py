from functions.additional_functions import *
import decimal
from datetime import date
import re
from sqlalchemy import func
from models import Res_line, Queasy, Pricecod, Htparam, Arrangement, Waehrung, Argt_line, Reslin_queasy

def pricecod_rate(resnr:int, reslinnr:int, prcode:str, datum:date, ankunft:date, abreise:date, marknr:int, argtno:int, rmcatno:int, adult:int, child1:int, child2:int, reserve_dec:decimal, wahrno:int):
    rmrate = 0
    rate_found = False
    exrate1:decimal = 1
    ex2:decimal = 1
    do_it:bool = False
    add_it:bool = False
    ebdisc_found:bool = False
    kbdisc_found:bool = False
    argt_defined:bool = False
    qty:int = 0
    niteno:int = 0
    ci_date:date = None
    fdatum:date = None
    tdatum:date = None
    n:int = 0
    ct:str = ""
    rmocc:decimal = -1
    res_line = queasy = pricecod = htparam = arrangement = waehrung = argt_line = reslin_queasy = None

    early_discount = kickback_discount = stay_pay = kbuff = ebuff = None

    early_discount_list, Early_discount = create_model("Early_discount", {"disc_rate":decimal, "min_days":int, "min_stay":int, "max_occ":int})
    kickback_discount_list, Kickback_discount = create_model("Kickback_discount", {"disc_rate":decimal, "max_days":int, "min_stay":int, "max_occ":int})
    stay_pay_list, Stay_pay = create_model("Stay_pay", {"f_date":date, "t_date":date, "stay":int, "pay":int})

    Kbuff = Kickback_discount
    kbuff_list = kickback_discount_list

    Ebuff = Early_discount
    ebuff_list = early_discount_list


    db_session = local_storage.db_session

    def generate_output():
        nonlocal rmrate, rate_found, exrate1, ex2, do_it, add_it, ebdisc_found, kbdisc_found, argt_defined, qty, niteno, ci_date, fdatum, tdatum, n, ct, rmocc, res_line, queasy, pricecod, htparam, arrangement, waehrung, argt_line, reslin_queasy
        nonlocal kbuff, ebuff


        nonlocal early_discount, kickback_discount, stay_pay, kbuff, ebuff
        nonlocal early_discount_list, kickback_discount_list, stay_pay_list
        return {"rmrate": rmrate, "rate_found": rate_found}

    res_line = db_session.query(Res_line).filter(
            (Res_line.resnr == resnr) &  (Res_line.reslinnr == reslinnr)).first()

    if res_line:
        rmrate = res_line.zipreis

        if substring(prcode, 0, 1) == "!":
            prcode = substring(prcode, 1)
        else:
            ct = res_line.zimmer_wunsch

            if re.match(".*\$CODE\$.*",ct):
                ct = substring(ct,0 + get_index(ct, "$CODE$") + 6)
                prcode = substring(ct, 0,1 + get_index(ct, ";") - 1)

    queasy = db_session.query(Queasy).filter(
            (Queasy.key == 18) &  (Queasy.number1 == marknr)).first()

    if queasy and queasy.logi3:
        datum = ankunft

    pricecod = db_session.query(Pricecod).filter(
            (func.lower(Pricecod.code) == (prcode).lower()) &  (Pricecod.marknr == marknr) &  (Pricecod.argtnr == argtno) &  (Pricecod.zikatnr == rmcatno) &  (Pricecod.startperiode <= datum) &  (Pricecod.endperiode >= datum)).first()

    if not pricecod:

        return generate_output()
    rate_found = True
    rmrate = pricecod.perspreis[adult - 1] + pricecod.kindpreis[0] * child1 + pricecod.kindpreis[1] * child2

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 87)).first()
    ci_date = htparam.fdate

    arrangement = db_session.query(Arrangement).filter(
            (Arrangement.argtnr == argtno)).first()

    waehrung = db_session.query(Waehrung).filter(
            (Waehrungsnr == arrangement.betriebsnr)).first()

    if waehrung:
        exrate1 = waehrung.ankauf / waehrung.einheit

    if reserve_dec != 0:
        ex2 = ex2 / reserve_dec
    else:

        waehrung = db_session.query(Waehrung).filter(
                (Waehrungsnr == wahrno)).first()

        if waehrung:
            ex2 = (waehrung.ankauf / waehrung.einheit)

    for argt_line in db_session.query(Argt_line).filter(
            (Argt_line.argtnr == arrangement.argtnr) &  (not Argt_line.kind1) &  (not Argt_line.kind2)).all():
        add_it = False

        if argt_line.vt_percnt == 0:

            if argt_line.betriebsnr == 0:
                qty = adult
            else:
                qty = argt_line.betriebsnr

        elif argt_line.vt_percnt == 1:
            qty = child1

        elif argt_line.vt_percnt == 2:
            qty = child2

        if qty > 0:

            if argt_line.fakt_modus == 1:
                add_it = True

            elif argt_line.fakt_modus == 2:

                if ankunft >= ci_date:
                    add_it = True

            elif argt_line.fakt_modus == 3:

                if (ankunft + 1) >= ci_date:
                    add_it = True

            elif argt_line.fakt_modus == 4 and get_day(datum) == 1:
                add_it = True

            elif argt_line.fakt_modus == 5 and get_day(datum + 1) == 1:
                add_it = True

            elif argt_line.fakt_modus == 6:

                if (ankunft + (argt_line.intervall - 1)) >= ci_date:
                    add_it = True

            if add_it:
                argt_defined = False

                reslin_queasy = db_session.query(Reslin_queasy).filter(
                        (func.lower(Reslin_queasy.key) == "fargt_line") &  (Reslin_queasy.char1 == "") &  (Reslin_queasy.char1 == "") &  (Reslin_queasy.number1 == argt_line.departement) &  (Reslin_queasy.number2 == argt_line.argtnr) &  (Reslin_queasy.resnr == resnr) &  (Reslin_queasy.reslinnr == reslinnr) &  (Reslin_queasy.number3 == argt_line.argt_artnr) &  (Reslin_queasy.date1 <= datum) &  (Reslin_queasy.date2 >= datum)).first()

                if reslin_queasy:
                    argt_defined = True

                    if argt_line.vt_percnt == 0:
                        rmrate = rmrate + reslin_queasy.deci1 * qty

                    elif argt_line.vt_percnt == 1:
                        rmrate = rmrate + reslin_queasy.deci2 * qty

                    elif argt_line.vt_percnt == 2:
                        rmrate = rmrate + reslin_queasy.deci3 * qty

                if not argt_defined:

                    reslin_queasy = db_session.query(Reslin_queasy).filter(
                            (func.lower(Reslin_queasy.key) == "argt_line") &  (func.lower(Reslin_queasy.char1) == (prcode).lower()) &  (Reslin_queasy.number1 == marknr) &  (Reslin_queasy.number2 == argtno) &  (Reslin_queasy.reslinnr == rmcatno) &  (Reslin_queasy.number3 == argt_line.argt_artnr) &  (Reslin_queasy.resnr == argt_line.departement) &  (Reslin_queasy.date1 <= datum) &  (Reslin_queasy.date2 >= datum)).first()

                    if reslin_queasy:

                        if argt_line.vt_percnt == 0:
                            rmrate = rmrate + reslin_queasy.deci1 * qty

                        elif argt_line.vt_percnt == 1:
                            rmrate = rmrate + reslin_queasy.deci2 * qty

                        elif argt_line.vt_percnt == 2:
                            rmrate = rmrate + reslin_queasy.deci3 * qty
                    else:
                        rmrate = rmrate + (argt_line.betrag * qty) * exrate1 / ex2

    return generate_output()