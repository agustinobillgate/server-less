from functions.additional_functions import *
import decimal
from datetime import date
from sqlalchemy import func
from functions.calc_servtaxesbl import calc_servtaxesbl
from models import Mc_types, Htparam, Res_line, Reservation, Akt_kont, Guest, Mc_guest, Genstat, Arrangement, Artikel, Mc_aclub

def nt_theone():
    billdate:date = None
    curr_date:date = None
    price_decimal:int = 0
    point:int = 0
    lrate:decimal = to_decimal("0.0")
    amount:decimal = to_decimal("0.0")
    proz:decimal = to_decimal("0.0")
    exchgrate:decimal = to_decimal("0.0")
    fact:decimal = to_decimal("0.0")
    sv_amt:decimal = to_decimal("0.0")
    vat_amt:decimal = to_decimal("0.0")
    vat2:decimal = to_decimal("0.0")
    sv_incl:bool = False
    vat_incl:bool = False
    sv_vat:bool = False
    do_it:bool = False
    mc_types = htparam = res_line = reservation = akt_kont = guest = mc_guest = genstat = arrangement = artikel = mc_aclub = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal billdate, curr_date, price_decimal, point, lrate, amount, proz, exchgrate, fact, sv_amt, vat_amt, vat2, sv_incl, vat_incl, sv_vat, do_it, mc_types, htparam, res_line, reservation, akt_kont, guest, mc_guest, genstat, arrangement, artikel, mc_aclub

        return {}


    mc_types = db_session.query(Mc_types).filter(
             (func.lower(Mc_types.bezeich) == ("The One").lower())).first()

    if not mc_types:

        return generate_output()
    proz =  to_decimal(0.05)

    htparam = db_session.query(Htparam).filter(
             (Htparam.paramnr == 127)).first()
    vat_incl = htparam.flogical

    htparam = db_session.query(Htparam).filter(
             (Htparam.paramnr == 128)).first()
    sv_incl = htparam.flogical

    htparam = db_session.query(Htparam).filter(
             (Htparam.paramnr == 479)).first()
    sv_vat = htparam.flogical

    htparam = db_session.query(Htparam).filter(
             (Htparam.paramnr == 491)).first()
    price_decimal = htparam.finteger

    htparam = db_session.query(Htparam).filter(
             (Htparam.paramnr == 110)).first()
    billdate = htparam.fdate

    for res_line in db_session.query(Res_line).filter(
             (Res_line.resstatus == 8) & (Res_line.abreise == billdate) & (Res_line.l_zuordnung[inc_value(2)] == 0)).order_by(Res_line._recid).all():

        reservation = db_session.query(Reservation).filter(
                 (Reservation.resnr == res_line.resnr)).first()
        do_it = reservation.kontakt_nr != 0

        if do_it:

            akt_kont = db_session.query(Akt_kont).filter(
                     (Akt_kont.gastnr == reservation.gastnr) & (Akt_kont.kontakt_nr == reservation.kontakt_nr)).first()
            do_it = None != akt_kont and akt_kont.betrieb_gast != 0

            if do_it:

                guest = db_session.query(Guest).filter(
                         (Guest.gastnr == akt_kont.betrieb_gast)).first()
                do_it = None != guest

        if do_it:

            mc_guest = db_session.query(Mc_guest).filter(
                     (Mc_guest.gastnr == guest.gastnr) & (Mc_guest.nr == mc_types.nr) & (Mc_guest.activeflag)).first()
            do_it = None != mc_guest

        if do_it:
            point = 0
            amount =  to_decimal("0")


            for curr_date in date_range(res_line.ankunft,res_line.abreise) :

                genstat = db_session.query(Genstat).filter(
                         (Genstat.datum == curr_date) & (Genstat.gastnrmember == res_line.gastnrmember) & (Genstat.resnr == res_line.resnr) & (Genstat.res_int[inc_value(0)] == res_line.reslinnr)).first()

                if genstat and genstat.zipreis != 0:
                    lrate =  to_decimal(genstat.rateLocal)

                    if not sv_incl and not vat_incl:
                        amount =  to_decimal(amount) + to_decimal(lrate)


                    else:

                        arrangement = db_session.query(Arrangement).filter(
                                 (Arrangement.arrangement == genstat.argt)).first()

                        artikel = db_session.query(Artikel).filter(
                                 (Artikel.artnr == arrangement.argt_artikelnr) & (Artikel.departement == 0)).first()
                        sv_amt, vat_amt, vat2, fact = get_output(calc_servtaxesbl(1, artikel.artnr, artikel.departement, billdate))
                        amount = to_decimal(amount + round(lrate / fact , price_decimal))

            if amount > 0:
                mc_aclub = Mc_aclub()
                db_session.add(mc_aclub)

                mc_aclub.key = mc_type.nr
                mc_aclub.cardnum = mc_guest.cardnum
                mc_aclub.zeit = get_current_time_in_seconds()
                mc_aclub.billdatum = billdate
                mc_aclub.betrag =  to_decimal(amount)
                mc_aclub.nettobetrag = to_decimal(round(amount * proz , 0))
                mc_aclub.resnr = res_line.resnr
                mc_aclub.reslinnr = res_line.reslinnr
                mc_aclub.bemerk = "Points from ROOM CHARGES"
                mc_aclub.incl_flag = 1
                mc_aclub.date1 = res_line.ankunft
                mc_aclub.date2 = res_line.abreise
                mc_aclub.deci1 =  to_decimal(genstat.rateLocal)
                mc_aclub.num1 = res_line.betriebsnr
                mc_aclub.num2 = res_line.zikatnr
                mc_aclub.num3 = res_line.gastnrmember
                mc_aclub.logi1 = False
                mc_aclub.char1 = res_line.arrangement
                mc_aclub.char2 = "$$"

                mc_aclub = db_session.query(Mc_aclub).filter(
                         (Mc_aclub.key == res_line.gastnr) & (Mc_aclub.incl_flag == 0) & (Mc_aclub.cardnum == mc_guest.cardnum)).first()

                if not mc_aclub:
                    mc_aclub = Mc_aclub()
                    db_session.add(mc_aclub)

                    mc_aclub.key = mc_types.nr
                    mc_aclub.cardnum = mc_guest.cardnum
                    mc_aclub.incl_flag = 0
                    mc_aclub.zeit = get_current_time_in_seconds()
                    mc_aclub.bemerk = "Points Balance"
                    mc_aclub.num3 = res_line.gastnr
                    mc_aclub.num4 = mc_guest.gastnr
                    mc_aclub.logi1 = False
                    mc_aclub.char2 = "$$"


                mc_aclub.betrag =  to_decimal(mc_aclub.betrag) + to_decimal(amount)
                mc_aclub.nettobetrag = to_decimal(mc_aclub.nettobetrag + round(amount * proz , 0))

    return generate_output()