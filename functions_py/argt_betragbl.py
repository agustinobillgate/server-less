#using conversion tools version: 1.0.0.117

# =======================================
# Rulita, 24-10-2025
# Issue :
# - New Compile program
# =======================================

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Waehrung, Htparam, Res_line, Argt_line, Reservation, Arrangement, Reslin_queasy, Guest_pr, Queasy

def argt_betragbl(resno:int, reslinno:int, argt_recid:int):

    prepare_cache ([Waehrung, Htparam, Res_line, Argt_line, Reservation, Arrangement, Reslin_queasy, Guest_pr, Queasy])

    betrag = to_decimal("0.0")
    ex_rate = 1
    add_it:bool = False
    marknr:int = 0
    bill_date:date = None
    argt_defined:bool = False
    qty:int = 0
    foreign_rate:bool = False
    exrate1:Decimal = 1
    ex2:Decimal = 1
    ct:string = ""
    contcode:string = ""
    waehrung = htparam = res_line = argt_line = reservation = arrangement = reslin_queasy = guest_pr = queasy = None

    w1 = None

    W1 = create_buffer("W1",Waehrung)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal betrag, ex_rate, add_it, marknr, bill_date, argt_defined, qty, foreign_rate, exrate1, ex2, ct, contcode, waehrung, htparam, res_line, argt_line, reservation, arrangement, reslin_queasy, guest_pr, queasy
        nonlocal resno, reslinno, argt_recid
        nonlocal w1


        nonlocal w1

        return {"betrag": betrag, "ex_rate": ex_rate}

    def get_exrate1():

        nonlocal betrag, ex_rate, add_it, marknr, bill_date, argt_defined, qty, foreign_rate, exrate1, ex2, ct, contcode, waehrung, htparam, res_line, argt_line, reservation, arrangement, reslin_queasy, guest_pr, queasy
        nonlocal resno, reslinno, argt_recid
        nonlocal w1


        nonlocal w1

        if reservation.insurance and res_line.reserve_dec != 0:
            ex_rate =  to_decimal(res_line.reserve_dec)

        elif res_line.betriebsnr != 0:

            waehrung = get_cache (Waehrung, {"waehrungsnr": [(eq, res_line.betriebsnr)]})

            if waehrung:
                ex_rate =  to_decimal(waehrung.ankauf) / to_decimal(waehrung.einheit)

        elif res_line.adrflag or not foreign_rate:

            htparam = get_cache (Htparam, {"paramnr": [(eq, 152)]})

            waehrung = get_cache (Waehrung, {"wabkurz": [(eq, htparam.fchar)]})

            if waehrung:
                ex_rate =  to_decimal(waehrung.ankauf) / to_decimal(waehrung.einheit)
        else:

            htparam = get_cache (Htparam, {"paramnr": [(eq, 144)]})

            waehrung = get_cache (Waehrung, {"wabkurz": [(eq, htparam.fchar)]})

            if waehrung:
                ex_rate =  to_decimal(waehrung.ankauf) / to_decimal(waehrung.einheit)


    def get_exrate2():

        nonlocal betrag, ex_rate, add_it, marknr, bill_date, argt_defined, qty, foreign_rate, exrate1, ex2, ct, contcode, waehrung, htparam, res_line, argt_line, reservation, arrangement, reslin_queasy, guest_pr, queasy
        nonlocal resno, reslinno, argt_recid
        nonlocal w1


        nonlocal w1

        if reservation.insurance and res_line.reserve_dec != 0:
            ex_rate =  to_decimal(res_line.reserve_dec)

            return

        queasy = get_cache (Queasy, {"key": [(eq, 18)],"number1": [(eq, marknr)]})

        if not queasy or (queasy and queasy.char3 == ""):

            queasy = get_cache (Queasy, {"key": [(eq, 2)],"char1": [(eq, contcode)]})

        if queasy.key == 18:

            waehrung = get_cache (Waehrung, {"wabkurz": [(eq, queasy.char3)]})
        else:

            if queasy.number1 != 0:

                waehrung = get_cache (Waehrung, {"waehrungsnr": [(eq, queasy.number1)]})

            elif queasy.logi1 or not foreign_rate:

                htparam = get_cache (Htparam, {"paramnr": [(eq, 152)]})

                waehrung = get_cache (Waehrung, {"wabkurz": [(eq, htparam.fchar)]})
            else:

                htparam = get_cache (Htparam, {"paramnr": [(eq, 144)]})

                waehrung = get_cache (Waehrung, {"wabkurz": [(eq, htparam.fchar)]})

        if waehrung:
            ex_rate =  to_decimal(waehrung.ankauf) / to_decimal(waehrung.einheit)


    def get_exrate3():

        nonlocal betrag, ex_rate, add_it, marknr, bill_date, argt_defined, qty, foreign_rate, exrate1, ex2, ct, contcode, waehrung, htparam, res_line, argt_line, reservation, arrangement, reslin_queasy, guest_pr, queasy
        nonlocal resno, reslinno, argt_recid
        nonlocal w1


        nonlocal w1

        local_nr:int = 0
        foreign_nr:int = 0

        if arrangement.betriebsnr != 0:

            waehrung = get_cache (Waehrung, {"waehrungsnr": [(eq, arrangement.betriebsnr)]})

            if waehrung:
                ex_rate =  to_decimal(waehrung.ankauf) / to_decimal(waehrung.einheit)

                return

        if foreign_rate:

            htparam = get_cache (Htparam, {"paramnr": [(eq, 144)]})

            waehrung = get_cache (Waehrung, {"wabkurz": [(eq, htparam.fchar)]})

            if waehrung:
                ex_rate =  to_decimal(waehrung.ankauf) / to_decimal(waehrung.einheit)
        else:

            htparam = get_cache (Htparam, {"paramnr": [(eq, 152)]})

            waehrung = get_cache (Waehrung, {"wabkurz": [(eq, htparam.fchar)]})

            if waehrung:
                ex_rate =  to_decimal(waehrung.ankauf) / to_decimal(waehrung.einheit)

    htparam = get_cache (Htparam, {"paramnr": [(eq, 110)]})
    bill_date = htparam.fdate

    htparam = get_cache (Htparam, {"paramnr": [(eq, 143)]})
    foreign_rate = htparam.flogical

    res_line = get_cache (Res_line, {"resnr": [(eq, resno)],"reslinnr": [(eq, reslinno)]})

    argt_line = get_cache (Argt_line, {"_recid": [(eq, argt_recid)]})

    reservation = get_cache (Reservation, {"resnr": [(eq, res_line.resnr)]})

    arrangement = get_cache (Arrangement, {"argtnr": [(eq, argt_line.argtnr)]})

    if argt_line.vt_percnt == 0:

        if argt_line.betriebsnr == 0:
            qty = res_line.erwachs
        else:
            qty = argt_line.betriebsnr

    elif argt_line.vt_percnt == 1:
        qty = res_line.kind1

    elif argt_line.vt_percnt == 2:
        qty = res_line.kind2

    if qty == 0:

        return generate_output()

    if argt_line.fakt_modus == 1:
        add_it = True

    elif argt_line.fakt_modus == 2:

        if res_line.ankunft == bill_date:
            add_it = True

    elif argt_line.fakt_modus == 3:

        if (res_line.ankunft + 1) == bill_date:
            add_it = True

    elif argt_line.fakt_modus == 4 and get_day(bill_date) == 1:
        add_it = True

    elif argt_line.fakt_modus == 5 and get_day(bill_date + 1) == 1:
        add_it = True

    elif argt_line.fakt_modus == 6:

        if (res_line.ankunft + (argt_line.intervall - 1)) >= bill_date:
            add_it = True

    if not add_it:

        return generate_output()
    marknr = res_line.reserve_int

    reslin_queasy = get_cache (Reslin_queasy, {"key": [(eq, "fargt-line")],"char1": [(eq, "")],"resnr": [(eq, res_line.resnr)],"reslinnr": [(eq, res_line.reslinnr)],"number1": [(eq, argt_line.departement)],"number2": [(eq, argt_line.argtnr)],"number3": [(eq, argt_line.argt_artnr)],"date1": [(le, bill_date)],"date2": [(ge, bill_date)]})

    if reslin_queasy:
        argt_defined = True

        if reslin_queasy.char2.lower()  != "" and reslin_queasy.char2.lower()  != ("0").lower() :
            betrag = ( to_decimal(res_line.zipreis) * to_decimal(to_int(reslin_queasy.char2)) / to_decimal(100)) * to_decimal(qty)
        else:
            betrag =  to_decimal(reslin_queasy.deci1) * to_decimal(qty)
        get_exrate1()

        return generate_output()

    guest_pr = get_cache (Guest_pr, {"gastnr": [(eq, res_line.gastnr)]})

    if guest_pr:
        contcode = guest_pr.code
        ct = res_line.zimmer_wunsch

        if matches(ct,r"*$CODE$*"):
            ct = substring(ct, get_index(ct, "$CODE$") + 6 - 1)
            contcode = substring(ct, 0, get_index(ct, ";") - 1)

    if guest_pr and marknr != 0 and not argt_defined:

        reslin_queasy = get_cache (Reslin_queasy, {"key": [(eq, "argt-line")],"char1": [(eq, contcode)],"number1": [(eq, marknr)],"number2": [(eq, argt_line.argtnr)],"reslinnr": [(eq, res_line.zikatnr)],"number3": [(eq, argt_line.argt_artnr)],"resnr": [(eq, argt_line.departement)],"date1": [(le, bill_date)],"date2": [(ge, bill_date)]})

        if reslin_queasy:
            betrag =  to_decimal(reslin_queasy.deci1) * to_decimal(qty)
            get_exrate2()

            return generate_output()

    if argt_line.betrag > 0:
        betrag =  to_decimal(argt_line.betrag) * to_decimal(qty)
    else:
        betrag = ( to_decimal(res_line.zipreis) * to_decimal(- to_decimal(argt_line.betrag) / to_decimal(100))) * to_decimal(qty)
    get_exrate3()

    return generate_output()