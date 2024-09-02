from functions.additional_functions import *
import decimal
from datetime import date
import re
from sqlalchemy import func
from functions.ratecode_compli import ratecode_compli
from models import Htparam, Res_line, Reservation, Queasy, Ratecode, Arrangement, Waehrung, Argt_line, Reslin_queasy, Zimmer, Kontline

def ratecode_rate(ebdisc_flag:bool, kbdisc_flag:bool, resnr:int, reslinnr:int, prcode:str, crdate:date, datum:date, ankunft:date, abreise:date, marknr:int, argtno:int, rmcatno:int, adult:int, child1:int, child2:int, res_exrate:decimal, wahrno:int):
    rate_found = False
    rmrate = 0
    early_flag = False
    kback_flag = False
    occ_type:int = 0
    restricted_disc:bool = False
    exrate1:decimal = 1
    ex2:decimal = 1
    do_it:bool = False
    add_it:bool = False
    ebdisc_found:bool = False
    kbdisc_found:bool = False
    argt_defined:bool = False
    qty:int = 0
    compno:int = 0
    niteno:int = 0
    book_date:date = None
    ci_date:date = None
    fdatum:date = None
    tdatum:date = None
    ct:str = ""
    orig_prcode:str = ""
    rmocc:decimal = -1
    avrgrate_option:bool = False
    stay_nites:int = 0
    bonus_nites:int = 0
    bonus:bool = False
    n:int = 0
    w_day:int = 0
    wd_array:[int] = [0, 0, 0, 0, 0, 0, 0, 0, 0]
    htparam = res_line = reservation = queasy = ratecode = arrangement = waehrung = argt_line = reslin_queasy = zimmer = kontline = None

    early_discount = kickback_discount = stay_pay = kbuff = ebuff = None

    early_discount_list, Early_discount = create_model("Early_discount", {"disc_rate":decimal, "min_days":int, "min_stay":int, "max_occ":int, "from_date":date, "to_date":date, "flag":bool}, {"from_date": None, "to_date": None})
    kickback_discount_list, Kickback_discount = create_model("Kickback_discount", {"disc_rate":decimal, "max_days":int, "min_stay":int, "max_occ":int, "flag":bool})
    stay_pay_list, Stay_pay = create_model("Stay_pay", {"f_date":date, "t_date":date, "stay":int, "pay":int})

    Kbuff = Kickback_discount
    kbuff_list = kickback_discount_list

    Ebuff = Early_discount
    ebuff_list = early_discount_list


    db_session = local_storage.db_session

    def generate_output():
        nonlocal rate_found, rmrate, early_flag, kback_flag, occ_type, restricted_disc, exrate1, ex2, do_it, add_it, ebdisc_found, kbdisc_found, argt_defined, qty, compno, niteno, book_date, ci_date, fdatum, tdatum, ct, orig_prcode, rmocc, avrgrate_option, stay_nites, bonus_nites, bonus, n, w_day, wd_array, htparam, res_line, reservation, queasy, ratecode, arrangement, waehrung, argt_line, reslin_queasy, zimmer, kontline
        nonlocal kbuff, ebuff


        nonlocal early_discount, kickback_discount, stay_pay, kbuff, ebuff
        nonlocal early_discount_list, kickback_discount_list, stay_pay_list
        return {"rate_found": rate_found, "rmrate": rmrate, "early_flag": early_flag, "kback_flag": kback_flag}

    def calc_occupancy():

        nonlocal rate_found, rmrate, early_flag, kback_flag, occ_type, restricted_disc, exrate1, ex2, do_it, add_it, ebdisc_found, kbdisc_found, argt_defined, qty, compno, niteno, book_date, ci_date, fdatum, tdatum, ct, orig_prcode, rmocc, avrgrate_option, stay_nites, bonus_nites, bonus, n, w_day, wd_array, htparam, res_line, reservation, queasy, ratecode, arrangement, waehrung, argt_line, reslin_queasy, zimmer, kontline
        nonlocal kbuff, ebuff


        nonlocal early_discount, kickback_discount, stay_pay, kbuff, ebuff
        nonlocal early_discount_list, kickback_discount_list, stay_pay_list

        zim100:int = 0
        curr_date:date = None
        from_date:date = None
        to_date:date = None
        totocc:decimal = 0
        minocc:decimal = 1000
        maxocc:decimal = 0

        if rmocc >= 0:

            return

        if ankunft == abreise:
            rmocc = 100

            return

        if occ_type == 1:
            from_date = datum
            to_date = datum
        else:
            from_date = ankunft
            to_date = abreise - 1

        for zimmer in db_session.query(Zimmer).filter(
                (Zimmer.sleeping)).all():
            zim100 = zim100 + 1
        for curr_date in range(from_date,to_date + 1) :
            rmocc = 0

            for res_line in db_session.query(Res_line).filter(
                    (Res_line.active_flag <= 1) &  (Res_line.resstatus <= 6) &  (Res_line.resstatus != 3) &  (Res_line.resstatus != 4) &  (not (Res_line.ankunft > curr_date)) &  (not (Res_line.abreise <= curr_date)) &  (Res_line.gastnr > 0) &  (Res_line.kontignr >= 0)).all():

                if res_line.resnr != resnr or res_line.reslinnr != reslinnr:

                    if res_line.zinr != "":

                        zimmer = db_session.query(Zimmer).filter(
                                (Zimmer.zinr == res_line.zinr)).first()

                        if zimmer.sleeping:
                            rmocc = rmocc + res_line.zimmeranz
                    else:
                        rmocc = rmocc + res_line.zimmeranz

            for kontline in db_session.query(Kontline).filter(
                    (Kontline.betriebsnr == 1) &  (Kontline.ankunft <= curr_date) &  (Kontline.abreise >= curr_date) &  (Kontline.kontstat == 1)).all():
                rmocc = rmocc + kontline.zimmeranz

            if minocc > rmocc:
                minocc = rmocc

            if maxocc < rmocc:
                maxocc = rmocc
            totocc = totocc + rmocc

        if occ_type == 0:
            rmocc = totocc / (1 + to_date - from_date) / zim100 * 100

        elif occ_type == 1:
            rmocc = rmocc / zim100 * 100

        elif occ_type == 2:
            rmocc = minocc / zim100 * 100

        elif occ_type == 3:
            rmocc = maxocc / zim100 * 100

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 933)).first()

    if htparam.feldtyp == 4:
        avrgrate_option = htparam.flogical


    if resnr > 0:

        res_line = db_session.query(Res_line).filter(
                (Res_line.resnr == resnr) &  (Res_line.reslinnr == reslinnr)).first()
    orig_prcode = prcode

    if substring(prcode, 0, 1) == "!":
        prcode = substring(prcode, 1)

    if res_line:
        rmrate = res_line.zipreis

        if substring(orig_prcode, 0, 1) != "!":
            ct = res_line.zimmer_wunsch

            if re.match(".*\$CODE\$.*",ct):
                ct = substring(ct,0 + get_index(ct, "$CODE$") + 6)
                prcode = substring(ct, 0,1 + get_index(ct, ";") - 1)

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 549)).first()
    occ_type = htparam.finteger

    if crdate == None and res_line:
        n = 0

        if re.match(".*DATE,.*",res_line.zimmer_wunsch):
            n = 1 + get_index(res_line.zimmer_wunsch, "Date,")

        if n > 0:
            ct = substring(res_line.zimmer_wunsch, n + 5 - 1, 8)
            crdate = date_mdy(to_int(substring(ct, 4, 2)) , to_int(substring(ct, 6, 2)) , to_int(substring(ct, 0, 4)))
        else:

            reservation = db_session.query(Reservation).filter(
                    (Reservation.resnr == resnr)).first()
            crdate = reservation.resdat

    queasy = db_session.query(Queasy).filter(
            (Queasy.key == 18) &  (Queasy.number1 == marknr)).first()

    if queasy and queasy.logi3:
        datum = ankunft
    w_day = wd_array[get_weekday(datum) - 1]

    if argtno != 0:

        ratecode = db_session.query(Ratecode).filter(
                (func.lower(Ratecode.code) == (prcode).lower()) &  (Ratecode.marknr == marknr) &  (Ratecode.argtnr == argtno) &  (Ratecode.zikatnr == rmcatno) &  (Ratecode.startperiode <= datum) &  (Ratecode.endperiode >= datum) &  (Ratecode.wday == w_day) &  (Ratecode.erwachs == adult) &  (Ratecode.kind1 == child1) &  (Ratecode.kind2 == child2)).first()

        if not ratecode:

            ratecode = db_session.query(Ratecode).filter(
                    (func.lower(Ratecode.code) == (prcode).lower()) &  (Ratecode.marknr == marknr) &  (Ratecode.argtnr == argtno) &  (Ratecode.zikatnr == rmcatno) &  (Ratecode.startperiode <= datum) &  (Ratecode.endperiode >= datum) &  (Ratecode.wday == 0) &  (Ratecode.erwachs == adult) &  (Ratecode.kind1 == child1) &  (Ratecode.kind2 == child2)).first()

        if not ratecode:

            ratecode = db_session.query(Ratecode).filter(
                    (func.lower(Ratecode.code) == (prcode).lower()) &  (Ratecode.marknr == marknr) &  (Ratecode.argtnr == argtno) &  (Ratecode.zikatnr == rmcatno) &  (Ratecode.startperiode <= datum) &  (Ratecode.endperiode >= datum) &  (Ratecode.wday == w_day) &  (Ratecode.erwachs == adult)).first()

        if not ratecode:

            ratecode = db_session.query(Ratecode).filter(
                    (func.lower(Ratecode.code) == (prcode).lower()) &  (Ratecode.marknr == marknr) &  (Ratecode.argtnr == argtno) &  (Ratecode.zikatnr == rmcatno) &  (Ratecode.startperiode <= datum) &  (Ratecode.endperiode >= datum) &  (Ratecode.wday == 0) &  (Ratecode.erwachs == adult)).first()

        if not ratecode:

            return generate_output()
        rate_found = True
    else:

        ratecode = db_session.query(Ratecode).filter(
                (func.lower(Ratecode.code) == (prcode).lower()) &  (Ratecode.marknr == marknr) &  (Ratecode.zikatnr == rmcatno) &  (Ratecode.startperiode <= datum) &  (Ratecode.endperiode >= datum) &  (Ratecode.wday == w_day) &  (Ratecode.erwachs == adult) &  (Ratecode.kind1 == child1) &  (Ratecode.kind2 == child2)).first()

        if not ratecode:

            ratecode = db_session.query(Ratecode).filter(
                    (func.lower(Ratecode.code) == (prcode).lower()) &  (Ratecode.marknr == marknr) &  (Ratecode.zikatnr == rmcatno) &  (Ratecode.startperiode <= datum) &  (Ratecode.endperiode >= datum) &  (Ratecode.wday == 0) &  (Ratecode.erwachs == adult) &  (Ratecode.kind1 == child1) &  (Ratecode.kind2 == child2)).first()

        if not ratecode:

            ratecode = db_session.query(Ratecode).filter(
                    (func.lower(Ratecode.code) == (prcode).lower()) &  (Ratecode.marknr == marknr) &  (Ratecode.zikatnr == rmcatno) &  (Ratecode.startperiode <= datum) &  (Ratecode.endperiode >= datum) &  (Ratecode.wday == w_day) &  (Ratecode.erwachs == adult)).first()

        if not ratecode:

            ratecode = db_session.query(Ratecode).filter(
                    (func.lower(Ratecode.code) == (prcode).lower()) &  (Ratecode.marknr == marknr) &  (Ratecode.zikatnr == rmcatno) &  (Ratecode.startperiode <= datum) &  (Ratecode.endperiode >= datum) &  (Ratecode.wday == 0) &  (Ratecode.erwachs == adult)).first()

        if not ratecode:

            return generate_output()
        rate_found = True

    if (num_entries(ratecode.char1[2], ";") >= 2):

        if not avrgrate_option and res_line:
            bonus = get_output(ratecode_compli(resnr, reslinnr, prcode, rmcatno, datum))

            if bonus:
                rmrate = 0

                return generate_output()
    rmrate = ratecode.zipreis + child1 * ratecode.ch1preis + child2 * ch2preis

    if rmrate <= 0.1:
        rmrate = 0

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 87)).first()
    ci_date = htparam.fdate
    book_date = crdate

    arrangement = db_session.query(Arrangement).filter(
            (Arrangement.argtnr == argtno)).first()

    waehrung = db_session.query(Waehrung).filter(
            (Waehrungsnr == arrangement.betriebsnr)).first()

    if waehrung:
        exrate1 = waehrung.ankauf / waehrung.einheit

    if res_exrate != 0:
        ex2 = ex2 / res_exrate
    else:

        waehrung = db_session.query(Waehrung).filter(
                (Waehrungsnr == wahrno)).first()

        if waehrung:
            ex2 = (waehrung.ankauf / waehrung.einheit)

    if arrangement:

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

    kbdisc_found = False

    if num_entries(ratecode.char1[1], ";") >= 2 and kbdisc_flag:
        for n in range(1,num_entries(ratecode.char1[1], ";") - 1 + 1) :
            ct = entry(n - 1, ratecode.char1[1], ";")
            kbuff = Kbuff()
            kbuff_list.append(kbuff)

            kbuff.disc_rate = to_int(entry(0, ct, ",")) / 100
            kbuff.max_days = to_int(entry(1, ct, ","))
            kbuff.min_stay = to_int(entry(2, ct, ","))
            kbuff.max_occ = to_int(entry(3, ct, ","))

        for kbuff in query(kbuff_list):
            add_it = True

            if kbuff.max_days > 0:
                add_it = (ankunft - crdate) <= kbuff.max_days

            if add_it and kbuff.min_stay > 0:
                add_it = (abreise - ankunft) >= kbuff.min_stay

            if add_it and kbuff.max_occ > 0:
                calc_occupancy()
                add_it = rmocc <= kbuff.max_occ

            if add_it:
                kbdisc_found = True
                kbuff.flag = True

                if not restricted_disc:
                    restricted_disc = (kbuff.max_days > 0) or (kbuff.min_stay > 0) or (kbuff.max_occ > 0)
                break
    ebdisc_found = False

    if num_entries(ratecode.char1[0], ";") >= 2 and ebdisc_flag:
        for n in range(1,num_entries(ratecode.char1[0], ";") - 1 + 1) :
            ct = entry(n - 1, ratecode.char1[0], ";")
            ebuff = Ebuff()
            ebuff_list.append(ebuff)

            ebuff.disc_rate = to_int(entry(0, ct, ",")) / 100
            ebuff.min_days = to_int(entry(1, ct, ","))
            ebuff.min_stay = to_int(entry(2, ct, ","))
            ebuff.max_occ = to_int(entry(3, ct, ","))

            if num_entries(ct, ",") >= 5 and trim(entry(4, ct, ",")) != "":
                ebuff.from_date = date_mdy(to_int(substring(entry(4, ct, ",") , 4, 2)) , to_int(substring(entry(4, ct, ",") , 6, 2)) , to_int(substring(entry(4, ct, ",") , 0, 4)))

            if num_entries(ct, ",") >= 6 and trim(entry(5, ct, ",")) != "":
                ebuff.to_date = date_mdy(to_int(substring(entry(5, ct, ",") , 4, 2)) , to_int(substring(entry(5, ct, ",") , 6, 2)) , to_int(substring(entry(5, ct, ",") , 0, 4)))

        for ebuff in query(ebuff_list):
            add_it = True

            if ebuff.from_date != None:
                add_it = book_date >= ebuff.from_date and book_date <= ebuff.to_date

            if add_it and ebuff.min_days > 0:
                add_it = (ankunft - crdate) >= ebuff.min_days

            if add_it and ebuff.min_stay > 0:
                add_it = (abreise - ankunft) >= ebuff.min_stay

            if add_it and ebuff.max_occ > 0:
                calc_occupancy()
                add_it = rmocc <= ebuff.max_occ

            if add_it:
                ebdisc_found = True
                ebuff.flag = True

                if not restricted_disc:
                    restricted_disc = (ebuff.min_days > 0) or (ebuff.max_occ > 0)
                break

    if kbdisc_found:

        kbuff = query(kbuff_list, filters=(lambda kbuff :kbuff.flag), first=True)
        rmrate = rmrate * (1 - kbuff.disc_rate / 100)
        kback_flag = True

    if ebdisc_found:

        ebuff = query(ebuff_list, filters=(lambda ebuff :ebuff.flag), first=True)
        rmrate = rmrate * (1 - ebuff.disc_rate / 100)
        early_flag = True
    early_flag = restricted_disc

    if kbdisc_found or ebdisc_found:

        if rmrate >= 10000:
            rmrate = round(rmrate + 0.49, 0)
        else:
            rmrate = round(rmrate + 0.0049, 2)

    if not avrgrate_option:

        return generate_output()

    stay_pay = query(stay_pay_list, first=True)

    if not stay_pay:

        return generate_output()
    stay_nites = abreise - ankunft

    for stay_pay in query(stay_pay_list, filters=(lambda stay_pay :stay_nites >= stay_pay.stay)):
        bonus_nites = stay_pay.stay - stay_pay.pay
        rmrate = rmrate * (stay_nites - bonus_nites) / stay_nites

        return generate_output()