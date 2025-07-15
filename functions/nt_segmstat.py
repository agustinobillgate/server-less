from functions.additional_functions import *
import decimal
from datetime import date
from functions.calc_servtaxesbl import calc_servtaxesbl
from functions.argt_betrag import argt_betrag
from sqlalchemy import func
from models import Htparam, Prmarket, Waehrung, Zimmer, Res_line, History, Reservation, Arrangement, Artikel, Argt_line, Guest_queasy

def nt_segmstat():
    do_it:bool = False
    bill_date:date = None
    lodg_betrag:decimal = to_decimal("0.0")
    exchg_rate:decimal = 1
    ex_rate:decimal = to_decimal("0.0")
    frate:decimal = to_decimal("0.0")
    s:decimal = to_decimal("0.0")
    s1:decimal = to_decimal("0.0")
    s2:decimal = to_decimal("0.0")
    price_decimal:int = 0
    rm_serv:bool = False
    rm_vat:bool = False
    service:decimal = to_decimal("0.0")
    vat:decimal = to_decimal("0.0")
    vat2:decimal = to_decimal("0.0")
    fact:decimal = to_decimal("0.0")
    anz:int = 0
    dayuse:bool = False
    argt_betrag:decimal = to_decimal("0.0")
    foreign_rate:bool = False
    msegm:int = 0
    def_msegm:int = 0
    htparam = prmarket = waehrung = zimmer = res_line = history = reservation = arrangement = artikel = argt_line = guest_queasy = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal do_it, bill_date, lodg_betrag, exchg_rate, ex_rate, frate, s, s1, s2, price_decimal, rm_serv, rm_vat, service, vat, vat2, fact, anz, dayuse, argt_betrag, foreign_rate, msegm, def_msegm, htparam, prmarket, waehrung, zimmer, res_line, history, reservation, arrangement, artikel, argt_line, guest_queasy

        return {}

    def get_marketsegm():

        nonlocal do_it, bill_date, lodg_betrag, exchg_rate, ex_rate, frate, s, s1, s2, price_decimal, rm_serv, rm_vat, service, vat, vat2, fact, anz, dayuse, argt_betrag, foreign_rate, msegm, def_msegm, htparam, prmarket, waehrung, zimmer, res_line, history, reservation, arrangement, artikel, argt_line, guest_queasy


        msegm = def_msegm

        if res_line.reserve_int != 0:
            msegm = res_line.reserve_int

    htparam = db_session.query(Htparam).filter(
             (Htparam.paramnr == 110)).first()
    bill_date = htparam.fdate

    htparam = db_session.query(Htparam).filter(
             (Htparam.paramnr == 255)).first()

    if htparam.finteger != 0:

        prmarket = db_session.query(Prmarket).filter(
                 (Prmarket.nr == htparam.finteger)).first()

        if not prmarket:
            pass
        else:
            def_msegm = htparam.finteger

    htparam = db_session.query(Htparam).filter(
             (Htparam.paramnr == 491)).first()
    price_decimal = htparam.finteger

    htparam = db_session.query(Htparam).filter(
             (Htparam.paramnr == 143)).first()
    foreign_rate = htparam.flogical

    if foreign_rate:

        htparam = db_session.query(Htparam).filter(
                 (Htparam.paramnr == 144)).first()

        waehrung = db_session.query(Waehrung).filter(
                 (Waehrung.wabkurz == htparam.fchar)).first()

        if waehrung:
            exchg_rate =  to_decimal(waehrung.ankauf) / to_decimal(waehrung.einheit)

    htparam = db_session.query(Htparam).filter(
             (Htparam.paramnr == 127)).first()
    rm_vat = not htparam.flogical

    htparam = db_session.query(Htparam).filter(
             (Htparam.paramnr == 128)).first()
    rm_serv = not htparam.flogical

    res_line_obj_list = []
    for res_line, zimmer in db_session.query(Res_line, Zimmer).join(Zimmer,(Zimmer.zinr == Res_line.zinr) & (Zimmer.sleeping)).filter(
             (res_line.ankunft <= bill_date) & (abreise >= bill_date) & ((Res_line.resstatus == 6) | (Res_line.resstatus == 13) | (Res_line.resstatus == 8)) & (Res_line.zipreis > 0)).order_by(Res_line.resnr, Res_line.gastnr, Res_line.reserve_int).all():
        if res_line._recid in res_line_obj_list:
            continue
        else:
            res_line_obj_list.append(res_line._recid)


        dayuse = False
        do_it = False

        if res_line.active_flag == 2 and (res_line.ankunft == abreise):

            history = db_session.query(History).filter(
                     (History.resnr == res_line.resnr) & (History.reslinnr == res_line.reslinnr)).first()

            if history and history.argtumsatz > 0:
                do_it = True
                dayuse = True

        if res_line.active_flag == 1:
            do_it = True

        if do_it:

            reservation = db_session.query(Reservation).filter(
                     (Reservation.resnr == res_line.resnr)).first()

            if res_line.reserve_dec != 0:
                frate =  to_decimal(res_line.reserve_dec)
            else:

                waehrung = db_session.query(Waehrung).filter(
                         (Waehrung.waehrungsnr == res_line.betriebsnr)).first()
                frate =  to_decimal(waehrung.ankauf) / to_decimal(waehrung.einheit)

            arrangement = db_session.query(Arrangement).filter(
                     (Arrangement.arrangement == res_line.arrangement)).first()

            artikel = db_session.query(Artikel).filter(
                     (Artikel.artnr == arrangement.argt_artikelnr) & (Artikel.departement == 0)).first()
            service, vat, vat2, fact = get_output(calc_servtaxesbl(1, artikel.artnr, artikel.departement, bill_date))
            lodg_betrag =  to_decimal(res_line.zipreis) * to_decimal(frate)

            for argt_line in db_session.query(Argt_line).filter(
                     (Argt_line.argtnr == arrangement.argtnr) & (not Argt_line.kind2)).order_by(Argt_line._recid).all():

                artikel = db_session.query(Artikel).filter(
                         (Artikel.artnr == argt_line.argt_artnr) & (Artikel.departement == argt_line.departement)).first()
                argt_betrag, ex_rate = get_output(argt_betrag(res_line._recid, argt_line._recid))
                lodg_betrag =  to_decimal(lodg_betrag) - to_decimal(argt_betrag) * to_decimal(ex_rate)
            lodg_betrag =  to_decimal(round (lodg_betrag , price_decimal))

            if not rm_serv:
                lodg_betrag =  to_decimal(lodg_betrag) / to_decimal(fact)
            get_marketsegm()

            if msegm != 0:

                guest_queasy = db_session.query(Guest_queasy).filter(
                         (func.lower(Guest_queasy.key) == ("msegm").lower()) & (Guest_queasy.gastnr == res_line.gastnr) & (Guest_queasy.number1 == msegm) & (Guest_queasy.date1 == bill_date)).first()

                if not guest_queasy:
                    guest_queasy = Guest_queasy()
                    db_session.add(guest_queasy)

                    guest_queasy.key = "msegm"
                    guest_queasy.gastnr = res_line.gastnr
                    guest_queasy.number1 = msegm
                    guest_queasy.date1 = bill_date

                if res_line.resstatus != 13:
                    guest_queasy.number2 = guest_queasy.number2 + 1
                guest_queasy.number3 = guest_queasy.number3 + res_line.erwachs + res_line.kind1 + res_line.kind2
                guest_queasy.deci1 =  to_decimal(guest_queasy.deci1) + to_decimal(lodg_betrag)

    return generate_output()