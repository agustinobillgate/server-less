#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from functions.ratecode_compli import ratecode_compli
from models import Htparam, Res_line, Reservation, Queasy, Ratecode, Arrangement, Waehrung, Argt_line, Reslin_queasy, Zimmer, Kontline

def ratecode_rate(ebdisc_flag:bool, kbdisc_flag:bool, resnr:int, reslinnr:int, prcode:string, crdate:date, datum:date, ankunft:date, abreise:date, marknr:int, argtno:int, rmcatno:int, adult:int, child1:int, child2:int, res_exrate:Decimal, wahrno:int):

    prepare_cache ([Htparam, Res_line, Reservation, Ratecode, Arrangement, Waehrung, Argt_line, Reslin_queasy, Kontline])

    rate_found = False
    rmrate = to_decimal("0.0")
    early_flag = False
    kback_flag = False
    occ_type:int = 0
    restricted_disc:bool = False
    exrate1:Decimal = 1
    ex2:Decimal = 1
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
    ct:string = ""
    orig_prcode:string = ""
    rmocc:Decimal = -1
    avrgrate_option:bool = False
    stay_nites:int = 0
    bonus_nites:int = 0
    bonus:bool = False
    n:int = 0
    w_day:int = 0
    wd_array:List[int] = [7, 1, 2, 3, 4, 5, 6, 7]
    htparam = res_line = reservation = queasy = ratecode = arrangement = waehrung = argt_line = reslin_queasy = zimmer = kontline = None

    early_discount = kickback_discount = stay_pay = kbuff = ebuff = None

    early_discount_data, Early_discount = create_model("Early_discount", {"disc_rate":Decimal, "min_days":int, "min_stay":int, "max_occ":int, "from_date":date, "to_date":date, "flag":bool}, {"from_date": None, "to_date": None})
    kickback_discount_data, Kickback_discount = create_model("Kickback_discount", {"disc_rate":Decimal, "max_days":int, "min_stay":int, "max_occ":int, "flag":bool})
    stay_pay_data, Stay_pay = create_model("Stay_pay", {"f_date":date, "t_date":date, "stay":int, "pay":int})

    Kbuff = Kickback_discount
    kbuff_data = kickback_discount_data

    Ebuff = Early_discount
    ebuff_data = early_discount_data

    db_session = local_storage.db_session

    def generate_output():
        nonlocal rate_found, rmrate, early_flag, kback_flag, occ_type, restricted_disc, exrate1, ex2, do_it, add_it, ebdisc_found, kbdisc_found, argt_defined, qty, compno, niteno, book_date, ci_date, fdatum, tdatum, ct, orig_prcode, rmocc, avrgrate_option, stay_nites, bonus_nites, bonus, n, w_day, wd_array, htparam, res_line, reservation, queasy, ratecode, arrangement, waehrung, argt_line, reslin_queasy, zimmer, kontline
        nonlocal ebdisc_flag, kbdisc_flag, resnr, reslinnr, prcode, crdate, datum, ankunft, abreise, marknr, argtno, rmcatno, adult, child1, child2, res_exrate, wahrno
        nonlocal kbuff, ebuff


        nonlocal early_discount, kickback_discount, stay_pay, kbuff, ebuff
        nonlocal early_discount_data, kickback_discount_data, stay_pay_data

        return {"rate_found": rate_found, "rmrate": rmrate, "early_flag": early_flag, "kback_flag": kback_flag}

    def calc_occupancy():

        nonlocal rate_found, rmrate, early_flag, kback_flag, occ_type, restricted_disc, exrate1, ex2, do_it, add_it, ebdisc_found, kbdisc_found, argt_defined, qty, compno, niteno, book_date, ci_date, fdatum, tdatum, ct, orig_prcode, rmocc, avrgrate_option, stay_nites, bonus_nites, bonus, n, w_day, wd_array, htparam, res_line, reservation, queasy, ratecode, arrangement, waehrung, argt_line, reslin_queasy, zimmer, kontline
        nonlocal ebdisc_flag, kbdisc_flag, resnr, reslinnr, prcode, crdate, datum, ankunft, abreise, marknr, argtno, rmcatno, adult, child1, child2, res_exrate, wahrno
        nonlocal kbuff, ebuff


        nonlocal early_discount, kickback_discount, stay_pay, kbuff, ebuff
        nonlocal early_discount_data, kickback_discount_data, stay_pay_data

        zim100:int = 0
        curr_date:date = None
        from_date:date = None
        to_date:date = None
        totocc:Decimal = to_decimal("0.0")
        minocc:Decimal = 1000
        maxocc:Decimal = to_decimal("0.0")

        if rmocc >= 0:

            return

        if ankunft == abreise:
            rmocc =  to_decimal("100")

            return

        if occ_type == 1:
            from_date = datum
            to_date = datum
        else:
            from_date = ankunft
            to_date = abreise - timedelta(days=1)

        for zimmer in db_session.query(Zimmer).filter(
                 (Zimmer.sleeping)).order_by(Zimmer._recid).all():
            zim100 = zim100 + 1
        for curr_date in date_range(from_date,to_date) :
            rmocc =  to_decimal("0")

            for res_line in db_session.query(Res_line).filter(
                     (Res_line.active_flag <= 1) & (Res_line.resstatus <= 6) & (Res_line.resstatus != 3) & (Res_line.resstatus != 4) & (not_ (Res_line.ankunft > curr_date)) & (not_ (Res_line.abreise <= curr_date)) & (Res_line.gastnr > 0) & (Res_line.kontignr >= 0)).order_by(Res_line._recid).all():

                if res_line.resnr != resnr or res_line.reslinnr != reslinnr:

                    if res_line.zinr != "":

                        zimmer = get_cache (Zimmer, {"zinr": [(eq, res_line.zinr)]})

                        if zimmer.sleeping:
                            rmocc =  to_decimal(rmocc) + to_decimal(res_line.zimmeranz)
                    else:
                        rmocc =  to_decimal(rmocc) + to_decimal(res_line.zimmeranz)

            for kontline in db_session.query(Kontline).filter(
                     (Kontline.betriebsnr == 1) & (Kontline.ankunft <= curr_date) & (Kontline.abreise >= curr_date) & (Kontline.kontstatus == 1)).order_by(Kontline._recid).all():
                rmocc =  to_decimal(rmocc) + to_decimal(kontline.zimmeranz)

            if minocc > rmocc:
                minocc =  to_decimal(rmocc)

            if maxocc < rmocc:
                maxocc =  to_decimal(rmocc)
            totocc =  to_decimal(totocc) + to_decimal(rmocc)

        if occ_type == 0:
            rmocc =  to_decimal(totocc) / to_decimal((1) + to_decimal(to_date) - to_decimal(from_date)) / to_decimal(zim100) * to_decimal("100")

        elif occ_type == 1:
            rmocc =  to_decimal(rmocc) / to_decimal(zim100) * to_decimal("100")

        elif occ_type == 2:
            rmocc =  to_decimal(minocc) / to_decimal(zim100) * to_decimal("100")

        elif occ_type == 3:
            rmocc =  to_decimal(maxocc) / to_decimal(zim100) * to_decimal("100")


    htparam = get_cache (Htparam, {"paramnr": [(eq, 933)]})

    if htparam.feldtyp == 4:
        avrgrate_option = htparam.flogical
    pass

    if resnr > 0:

        res_line = get_cache (Res_line, {"resnr": [(eq, resnr)],"reslinnr": [(eq, reslinnr)]})
    orig_prcode = prcode

    if substring(prcode, 0, 1) == ("!").lower() :
        prcode = substring(prcode, 1)

    if res_line:
        rmrate =  to_decimal(res_line.zipreis)

        if substring(orig_prcode, 0, 1) != ("!").lower() :
            ct = res_line.zimmer_wunsch

            if matches(ct,r"*$CODE$*"):
                ct = substring(ct, get_index(ct, "$CODE$") + 6 - 1)
                prcode = substring(ct, 0, get_index(ct, ";") - 1)

    htparam = get_cache (Htparam, {"paramnr": [(eq, 549)]})
    occ_type = htparam.finteger

    if crdate == None and res_line:
        n = 0

        if matches(res_line.zimmer_wunsch,r"*DATE,*"):
            n = get_index(res_line.zimmer_wunsch, "Date,")

        if n > 0:
            ct = substring(res_line.zimmer_wunsch, n + 5 - 1, 8)
            crdate = date_mdy(to_int(substring(ct, 4, 2)) , to_int(substring(ct, 6, 2)) , to_int(substring(ct, 0, 4)))
        else:

            reservation = get_cache (Reservation, {"resnr": [(eq, resnr)]})
            crdate = reservation.resdat

    queasy = get_cache (Queasy, {"key": [(eq, 18)],"number1": [(eq, marknr)]})

    if queasy and queasy.logi3:
        datum = ankunft
    w_day = wd_array[get_weekday(datum) - 1]

    if argtno != 0:

        ratecode = get_cache (Ratecode, {"code": [(eq, prcode)],"marknr": [(eq, marknr)],"argtnr": [(eq, argtno)],"zikatnr": [(eq, rmcatno)],"startperiode": [(le, datum)],"endperiode": [(ge, datum)],"wday": [(eq, w_day)],"erwachs": [(eq, adult)],"kind1": [(eq, child1)],"kind2": [(eq, child2)]})

        if not ratecode:

            ratecode = get_cache (Ratecode, {"code": [(eq, prcode)],"marknr": [(eq, marknr)],"argtnr": [(eq, argtno)],"zikatnr": [(eq, rmcatno)],"startperiode": [(le, datum)],"endperiode": [(ge, datum)],"wday": [(eq, 0)],"erwachs": [(eq, adult)],"kind1": [(eq, child1)],"kind2": [(eq, child2)]})

        if not ratecode:

            ratecode = get_cache (Ratecode, {"code": [(eq, prcode)],"marknr": [(eq, marknr)],"argtnr": [(eq, argtno)],"zikatnr": [(eq, rmcatno)],"startperiode": [(le, datum)],"endperiode": [(ge, datum)],"wday": [(eq, w_day)],"erwachs": [(eq, adult)]})

        if not ratecode:

            ratecode = get_cache (Ratecode, {"code": [(eq, prcode)],"marknr": [(eq, marknr)],"argtnr": [(eq, argtno)],"zikatnr": [(eq, rmcatno)],"startperiode": [(le, datum)],"endperiode": [(ge, datum)],"wday": [(eq, 0)],"erwachs": [(eq, adult)]})

        if not ratecode:

            return generate_output()
        rate_found = True
    else:

        ratecode = get_cache (Ratecode, {"code": [(eq, prcode)],"marknr": [(eq, marknr)],"zikatnr": [(eq, rmcatno)],"startperiode": [(le, datum)],"endperiode": [(ge, datum)],"wday": [(eq, w_day)],"erwachs": [(eq, adult)],"kind1": [(eq, child1)],"kind2": [(eq, child2)]})

        if not ratecode:

            ratecode = get_cache (Ratecode, {"code": [(eq, prcode)],"marknr": [(eq, marknr)],"zikatnr": [(eq, rmcatno)],"startperiode": [(le, datum)],"endperiode": [(ge, datum)],"wday": [(eq, 0)],"erwachs": [(eq, adult)],"kind1": [(eq, child1)],"kind2": [(eq, child2)]})

        if not ratecode:

            ratecode = get_cache (Ratecode, {"code": [(eq, prcode)],"marknr": [(eq, marknr)],"zikatnr": [(eq, rmcatno)],"startperiode": [(le, datum)],"endperiode": [(ge, datum)],"wday": [(eq, w_day)],"erwachs": [(eq, adult)]})

        if not ratecode:

            ratecode = get_cache (Ratecode, {"code": [(eq, prcode)],"marknr": [(eq, marknr)],"zikatnr": [(eq, rmcatno)],"startperiode": [(le, datum)],"endperiode": [(ge, datum)],"wday": [(eq, 0)],"erwachs": [(eq, adult)]})

        if not ratecode:

            return generate_output()
        rate_found = True

    if (num_entries(ratecode.char1[2], ";") >= 2):

        if not avrgrate_option and res_line:
            bonus = get_output(ratecode_compli(resnr, reslinnr, prcode, rmcatno, datum))

            if bonus:
                rmrate =  to_decimal("0")

                return generate_output()
    rmrate =  to_decimal(ratecode.zipreis) + to_decimal(child1) * to_decimal(ratecode.ch1preis) + to_decimal(child2) * to_decimal(ratecode.ch2preis)

    if rmrate <= 0.1:
        rmrate =  to_decimal("0")

    htparam = get_cache (Htparam, {"paramnr": [(eq, 87)]})
    ci_date = htparam.fdate
    book_date = crdate

    arrangement = get_cache (Arrangement, {"argtnr": [(eq, argtno)]})

    waehrung = get_cache (Waehrung, {"waehrungsnr": [(eq, arrangement.betriebsnr)]})

    if waehrung:
        exrate1 =  to_decimal(waehrung.ankauf) / to_decimal(waehrung.einheit)

    if res_exrate != 0:
        ex2 =  to_decimal(ex2) / to_decimal(res_exrate)
    else:

        waehrung = get_cache (Waehrung, {"waehrungsnr": [(eq, wahrno)]})

        if waehrung:
            ex2 = ( to_decimal(waehrung.ankauf) / to_decimal(waehrung.einheit))

    if arrangement:

        for argt_line in db_session.query(Argt_line).filter(
                 (Argt_line.argtnr == arrangement.argtnr) & not_ (Argt_line.kind1) & not_ (Argt_line.kind2)).order_by(Argt_line._recid).all():
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

                    reslin_queasy = get_cache (Reslin_queasy, {"key": [(eq, "fargt-line")],"char1": [(eq, ""),(eq, "")],"number1": [(eq, argt_line.departement)],"number2": [(eq, argt_line.argtnr)],"resnr": [(eq, resnr)],"reslinnr": [(eq, reslinnr)],"number3": [(eq, argt_line.argt_artnr)],"date1": [(le, datum)],"date2": [(ge, datum)]})

                    if reslin_queasy:
                        argt_defined = True

                        if argt_line.vt_percnt == 0:
                            rmrate =  to_decimal(rmrate) + to_decimal(reslin_queasy.deci1) * to_decimal(qty)

                        elif argt_line.vt_percnt == 1:
                            rmrate =  to_decimal(rmrate) + to_decimal(reslin_queasy.deci2) * to_decimal(qty)

                        elif argt_line.vt_percnt == 2:
                            rmrate =  to_decimal(rmrate) + to_decimal(reslin_queasy.deci3) * to_decimal(qty)

                    if not argt_defined:

                        reslin_queasy = get_cache (Reslin_queasy, {"key": [(eq, "argt-line")],"char1": [(eq, prcode)],"number1": [(eq, marknr)],"number2": [(eq, argtno)],"reslinnr": [(eq, rmcatno)],"number3": [(eq, argt_line.argt_artnr)],"resnr": [(eq, argt_line.departement)],"date1": [(le, datum)],"date2": [(ge, datum)]})

                        if reslin_queasy:

                            if argt_line.vt_percnt == 0:
                                rmrate =  to_decimal(rmrate) + to_decimal(reslin_queasy.deci1) * to_decimal(qty)

                            elif argt_line.vt_percnt == 1:
                                rmrate =  to_decimal(rmrate) + to_decimal(reslin_queasy.deci2) * to_decimal(qty)

                            elif argt_line.vt_percnt == 2:
                                rmrate =  to_decimal(rmrate) + to_decimal(reslin_queasy.deci3) * to_decimal(qty)
                        else:
                            rmrate =  to_decimal(rmrate) + to_decimal((argt_line.betrag) * to_decimal(qty)) * to_decimal(exrate1) / to_decimal(ex2)

    kbdisc_found = False

    if num_entries(ratecode.char1[1], ";") >= 2 and kbdisc_flag:
        for n in range(1,num_entries(ratecode.char1[1], ";") - 1 + 1) :
            ct = entry(n - 1, ratecode.char1[1], ";")
            kbuff = Kbuff()
            kbuff_data.append(kbuff)

            kbuff.disc_rate =  to_decimal(to_int(entry(0 , ct , ","))) / to_decimal("100")
            kbuff.max_days = to_int(entry(1, ct, ","))
            kbuff.min_stay = to_int(entry(2, ct, ","))
            kbuff.max_occ = to_int(entry(3, ct, ","))

        for kbuff in query(kbuff_data, sort_by=[("max_occ",False)]):
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
            ebuff_data.append(ebuff)

            ebuff.disc_rate =  to_decimal(to_int(entry(0 , ct , ","))) / to_decimal("100")
            ebuff.min_days = to_int(entry(1, ct, ","))
            ebuff.min_stay = to_int(entry(2, ct, ","))
            ebuff.max_occ = to_int(entry(3, ct, ","))

            if num_entries(ct, ",") >= 5 and trim(entry(4, ct, ",")) != "":
                ebuff.from_date = date_mdy(to_int(substring(entry(4, ct, ",") , 4, 2)) , to_int(substring(entry(4, ct, ",") , 6, 2)) , to_int(substring(entry(4, ct, ",") , 0, 4)))

            if num_entries(ct, ",") >= 6 and trim(entry(5, ct, ",")) != "":
                ebuff.to_date = date_mdy(to_int(substring(entry(5, ct, ",") , 4, 2)) , to_int(substring(entry(5, ct, ",") , 6, 2)) , to_int(substring(entry(5, ct, ",") , 0, 4)))

        for ebuff in query(ebuff_data, sort_by=[("from_date",False),("to_date",False),("max_occ",False)]):
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

        kbuff = query(kbuff_data, filters=(lambda kbuff: kbuff.flag), first=True)
        rmrate =  to_decimal(rmrate) * to_decimal((1) - to_decimal(kbuff.disc_rate) / to_decimal(100))
        kback_flag = True

    if ebdisc_found:

        ebuff = query(ebuff_data, filters=(lambda ebuff: ebuff.flag), first=True)
        rmrate =  to_decimal(rmrate) * to_decimal((1) - to_decimal(ebuff.disc_rate) / to_decimal(100))
        early_flag = True
    early_flag = restricted_disc

    if kbdisc_found or ebdisc_found:

        if rmrate >= 10000:
            rmrate = to_decimal(round(rmrate + 0.49 , 0))
        else:
            rmrate = to_decimal(round(rmrate + 0.0049 , 2))

    if not avrgrate_option:

        return generate_output()

    stay_pay = query(stay_pay_data, first=True)

    if not stay_pay:

        return generate_output()
    stay_nites = (abreise - ankunft).days

    for stay_pay in query(stay_pay_data, filters=(lambda stay_pay: stay_pay.stay_nites >= stay_pay.stay), sort_by=[("stay",True)]):
        bonus_nites = stay_pay.stay - stay_pay.pay
        rmrate =  to_decimal(rmrate) * to_decimal((stay_nites) - to_decimal(bonus_nites)) / to_decimal(stay_nites)

        return generate_output()

    return generate_output()