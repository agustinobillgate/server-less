from functions.additional_functions import *
import decimal
from datetime import date
from sqlalchemy import func
from models import Htparam, Res_line, Argt_line, Reservation, Reslin_queasy, Guest_pr, Waehrung, Queasy, Arrangement

def ntargt_betrag(res_recid:int, argt_recid:int):
    lvcarea:str = "NTargt-betrag"
    betrag = to_decimal("0.0")
    ex_rate = 1
    curr_zikatnr:int = 0
    add_it:bool = False
    marknr:int = 0
    bill_date:date = None
    argt_defined:bool = False
    qty:int = 0
    foreign_rate:bool = False
    ct:str = ""
    contcode:str = ""
    htparam = res_line = argt_line = reservation = reslin_queasy = guest_pr = waehrung = queasy = arrangement = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal lvcarea, betrag, ex_rate, curr_zikatnr, add_it, marknr, bill_date, argt_defined, qty, foreign_rate, ct, contcode, htparam, res_line, argt_line, reservation, reslin_queasy, guest_pr, waehrung, queasy, arrangement
        nonlocal res_recid, argt_recid

        return {"betrag": betrag, "ex_rate": ex_rate}

    def get_exrate1():

        nonlocal lvcarea, betrag, ex_rate, curr_zikatnr, add_it, marknr, bill_date, argt_defined, qty, foreign_rate, ct, contcode, htparam, res_line, argt_line, reservation, reslin_queasy, guest_pr, waehrung, queasy, arrangement
        nonlocal res_recid, argt_recid

        if reservation.insurance and res_line.reserve_dec != 0:
            ex_rate =  to_decimal(res_line.reserve_dec)

        elif res_line.betriebsnr != 0:

            waehrung = db_session.query(Waehrung).filter(
                     (Waehrung.waehrungsnr == res_line.betriebsnr)).first()

            if waehrung:
                ex_rate =  to_decimal(waehrung.ankauf) / to_decimal(waehrung.einheit)

        elif res_line.adrflag or not foreign_rate:

            htparam = db_session.query(Htparam).filter(
                     (Htparam.paramnr == 152)).first()

            waehrung = db_session.query(Waehrung).filter(
                     (Waehrung.wabkurz == htparam.fchar)).first()

            if waehrung:
                ex_rate =  to_decimal(waehrung.ankauf) / to_decimal(waehrung.einheit)
        else:

            htparam = db_session.query(Htparam).filter(
                     (Htparam.paramnr == 144)).first()

            waehrung = db_session.query(Waehrung).filter(
                     (Waehrung.wabkurz == htparam.fchar)).first()

            if waehrung:
                ex_rate =  to_decimal(waehrung.ankauf) / to_decimal(waehrung.einheit)


    def get_exrate2():

        nonlocal lvcarea, betrag, ex_rate, curr_zikatnr, add_it, marknr, bill_date, argt_defined, qty, foreign_rate, ct, contcode, htparam, res_line, argt_line, reservation, reslin_queasy, guest_pr, waehrung, queasy, arrangement
        nonlocal res_recid, argt_recid

        if reservation.insurance and res_line.reserve_dec != 0:
            ex_rate =  to_decimal(res_line.reserve_dec)

            return

        queasy = db_session.query(Queasy).filter(
                 (Queasy.key == 2) & (func.lower(Queasy.char1) == (contcode).lower())).first()

        if queasy.number1 != 0:

            waehrung = db_session.query(Waehrung).filter(
                     (Waehrung.waehrungsnr == queasy.number1)).first()

            if waehrung:
                ex_rate =  to_decimal(waehrung.ankauf) / to_decimal(waehrung.einheit)

        elif queasy.logi1 or not foreign_rate:

            htparam = db_session.query(Htparam).filter(
                     (Htparam.paramnr == 152)).first()

            waehrung = db_session.query(Waehrung).filter(
                     (Waehrung.wabkurz == htparam.fchar)).first()

            if waehrung:
                ex_rate =  to_decimal(waehrung.ankauf) / to_decimal(waehrung.einheit)
        else:

            htparam = db_session.query(Htparam).filter(
                     (Htparam.paramnr == 144)).first()

            waehrung = db_session.query(Waehrung).filter(
                     (Waehrung.wabkurz == htparam.fchar)).first()

            if waehrung:
                ex_rate =  to_decimal(waehrung.ankauf) / to_decimal(waehrung.einheit)


    def get_exrate3():

        nonlocal lvcarea, betrag, ex_rate, curr_zikatnr, add_it, marknr, bill_date, argt_defined, qty, foreign_rate, ct, contcode, htparam, res_line, argt_line, reservation, reslin_queasy, guest_pr, waehrung, queasy, arrangement
        nonlocal res_recid, argt_recid

        local_nr:int = 0
        foreign_nr:int = 0

        arrangement = db_session.query(Arrangement).filter(
                 (Arrangement.argtnr == argt_line.argtnr)).first()

        if arrangement.betriebsnr != 0:

            waehrung = db_session.query(Waehrung).filter(
                     (Waehrung.waehrungsnr == arrangement.betriebsnr)).first()

            if waehrung:
                ex_rate =  to_decimal(waehrung.ankauf) / to_decimal(waehrung.einheit)

                return

        if foreign_rate:

            htparam = db_session.query(Htparam).filter(
                     (Htparam.paramnr == 144)).first()

            waehrung = db_session.query(Waehrung).filter(
                     (Waehrung.wabkurz == htparam.fchar)).first()

            if waehrung:
                ex_rate =  to_decimal(waehrung.ankauf) / to_decimal(waehrung.einheit)
        else:

            htparam = db_session.query(Htparam).filter(
                     (Htparam.paramnr == 152)).first()

            waehrung = db_session.query(Waehrung).filter(
                     (Waehrung.wabkurz == htparam.fchar)).first()

            if waehrung:
                ex_rate =  to_decimal(waehrung.ankauf) / to_decimal(waehrung.einheit)

    htparam = db_session.query(Htparam).filter(
             (Htparam.paramnr == 110)).first()
    bill_date = htparam.fdate

    htparam = db_session.query(Htparam).filter(
             (Htparam.paramnr == 143)).first()
    foreign_rate = htparam.flogical

    res_line = db_session.query(Res_line).filter(
             (Res_line._recid == res_recid)).first()

    argt_line = db_session.query(Argt_line).filter(
             (Argt_line._recid == argt_recid)).first()

    reservation = db_session.query(Reservation).filter(
             (Reservation.resnr == res_line.resnr)).first()

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

    if argt_line.vt_percnt == 0:

        if argt_line.betriebsnr == 0:
            qty = res_line.erwachs
        else:
            qty = argt_line.betriebsnr

    elif argt_line.vt_percnt == 1:
        qty = res_line.kind1

    elif argt_line.vt_percnt == 2:
        qty = res_line.kind2
    marknr = res_line.reserve_int

    reslin_queasy = db_session.query(Reslin_queasy).filter(
             (func.lower(Reslin_queasy.key) == ("fargt-line").lower()) & (Reslin_queasy.char1 == "") & (Reslin_queasy.resnr == res_line.resnr) & (Reslin_queasy.reslinnr == res_line.reslinnr) & (Reslin_queasy.number1 == argt_line.departement) & (Reslin_queasy.number2 == argt_line.argtnr) & (Reslin_queasy.number3 == argt_line.argt_artnr) & (Reslin_queasy.bill_date >= Reslin_queasy.date1) & (Reslin_queasy.bill_date <= Reslin_queasy.date2)).first()

    if reslin_queasy:
        argt_defined = True
        betrag =  to_decimal(reslin_queasy.deci1) * to_decimal(qty)
        get_exrate1()

        return generate_output()

    if res_line.l_zuordnung[0] != 0:
        curr_zikatnr = res_line.l_zuordnung[0]
    else:
        curr_zikatnr = res_line.zikatnr

    guest_pr = db_session.query(Guest_pr).filter(
             (Guest_pr.gastnr == res_line.gastnr)).first()

    if guest_pr:
        contcode = guest_pr.code
        ct = res_line.zimmer_wunsch

        if re.match(r".*\$CODE\$.*",ct, re.IGNORECASE):
            ct = substring(ct, 0 + get_index(ct, "$CODE$") + 6)
            contcode = substring(ct, 0, 1 + get_index(ct, ";") - 1)

    if guest_pr and marknr != 0 and not argt_defined:

        reslin_queasy = db_session.query(Reslin_queasy).filter(
                 (func.lower(Reslin_queasy.key) == ("argt-line").lower()) & (func.lower(Reslin_queasy.char1) == (contcode).lower()) & (Reslin_queasy.number1 == marknr) & (Reslin_queasy.number2 == argt_line.argtnr) & (Reslin_queasy.reslinnr == curr_zikatnr) & (Reslin_queasy.number3 == argt_line.argt_artnr) & (Reslin_queasy.resnr == argt_line.departement) & (Reslin_queasy.fdate >= Reslin_queasy.date1) & (Reslin_queasy.fdate <= Reslin_queasy.date2)).first()

        if reslin_queasy:
            betrag =  to_decimal(reslin_queasy.deci1) * to_decimal(qty)
            get_exrate2()

            return generate_output()
    betrag =  to_decimal(argt_line.betrag) * to_decimal(qty)
    get_exrate3()

    return generate_output()