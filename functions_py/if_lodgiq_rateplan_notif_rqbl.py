# using conversion tools version: 1.0.0.119
"""_yusufwijasena_13/11/2025

    Ticket ID: 62BADE
        _remark_:   - fix python indentation
                    - add import from function_py
"""
from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from sqlalchemy import func
# from functions.update_child_rates_by_parent import update_child_rates_by_parent
# from functions.calc_servvat import calc_servvat
from functions_py.update_child_rates_by_parent import update_child_rates_by_parent
from functions_py.calc_servvat import calc_servvat
from models import Ratecode, Queasy, Bediener, Htparam, Zimkateg, Res_history, Arrangement, Artikel, Waehrung

drcode_list_data, Drcode_list = create_model(
    "Drcode_list",
    {
        "rcode": str,
        "startdate": date,
        "enddate": date,
        "adult": str,
        "child": str,
        "rmtype": str,
        "rmrate": str,
        "currency": str
    })


def if_lodgiq_rateplan_notif_rqbl(user_init: str, drcode_list_data: list[Drcode_list]):

    prepare_cache([Ratecode, Queasy, Bediener, Htparam, Zimkateg, Res_history, Arrangement, Artikel, Waehrung])

    done = False
    error_flag = 1
    error_rtype = ""
    rcode = ""
    rmtype = ""
    argtno: int = 0
    marktno: int = 0
    rc_bezeich = ""
    j: int = 0
    adlt: int = 0
    bef_start: date = None
    bef_end: date = None
    bef_pax: int = 0
    bef_rate: Decimal = to_decimal("0.0")
    tax_included: bool = False
    iftask = ""
    mestoken = ""
    mesvalue = ""
    tokcounter: int = 0
    cat_flag: bool = False
    ratecode = queasy = bediener = htparam = zimkateg = res_history = arrangement = artikel = waehrung = None

    rcode_list = drcode_list = rcbuff = qsy = rbuff = q_curr = tb3_buff = None

    rcode_list_data, Rcode_list = create_model(
        "Rcode_list",
        {
            "rcode": str,
            "startdate": date,
            "enddate": date,
            "adult": int,
            "child": int,
            "rmtype": str,
            "rmrate": Decimal,
            "currency": str
        })

    Rcbuff = create_buffer("Rcbuff", Ratecode)
    Qsy = create_buffer("Qsy", Queasy)
    Rbuff = create_buffer("Rbuff", Ratecode)
    Q_curr = create_buffer("Q_curr", Queasy)
    Tb3_buff = create_buffer("Tb3_buff", Ratecode)

    db_session = local_storage.db_session

    def generate_output():
        nonlocal done, error_flag, error_rtype, rcode, rmtype, argtno, marktno, rc_bezeich, j, adlt, bef_start, bef_end, bef_pax, bef_rate, tax_included, iftask, mestoken, mesvalue, tokcounter, cat_flag, ratecode, queasy, bediener, htparam, zimkateg, res_history, arrangement, artikel, waehrung
        nonlocal user_init
        nonlocal rcbuff, qsy, rbuff, q_curr, tb3_buff
        nonlocal rcode_list, drcode_list, rcbuff, qsy, rbuff, q_curr, tb3_buff
        nonlocal rcode_list_data

        return {
            "done": done,
            "error_flag": error_flag,
            "error_rtype": error_rtype
        }

    def update_bookengine_config():
        nonlocal done, error_flag, error_rtype, rcode, rmtype, argtno, marktno, rc_bezeich, j, adlt, bef_start, bef_end, bef_pax, bef_rate, tax_included, iftask, mestoken, mesvalue, tokcounter, cat_flag, ratecode, queasy, bediener, htparam, zimkateg, res_history, arrangement, artikel, waehrung
        nonlocal user_init
        nonlocal rcbuff, qsy, rbuff, q_curr, tb3_buff
        nonlocal rcode_list, drcode_list, rcbuff, qsy, rbuff, q_curr, tb3_buff
        nonlocal rcode_list_data

        bqueasy = None
        zbuff = None
        datum: date = None
        cm_gastno: int = 0
        roomnr: int = 0
        dyna = ""
        loopi: int = 0
        currency = ""
        serv: Decimal = to_decimal("0.0")
        vat: Decimal = to_decimal("0.0")
        str = ""
        tqueasy = None
        Bqueasy = create_buffer("Bqueasy", Queasy)
        Zbuff = create_buffer("Zbuff", Zimkateg)
        Tqueasy = create_buffer("Tqueasy", Queasy)

        zbuff = get_cache(Zimkateg, {"kurzbez": [(eq, rcode_list.rmtype)]})

        if cat_flag:
            roomnr = zbuff.typ
            queasy = get_cache(
                Queasy, {"key": [(eq, 152)], "number1": [(eq, roomnr)]})

            if queasy:
                str = queasy.char1
            else:
                roomnr = zbuff.zikatnr
                str = zbuff.kurzbez

        for qsy in db_session.query(Qsy).filter(
                (Qsy.key == 2) & (Qsy.logi2)).order_by(Qsy._recid).all():
            for ratecode in db_session.query(Ratecode).filter(
                    (Ratecode.code == qsy.char1)).order_by(Ratecode._recid).all():
                iftask = ratecode.char1[4]
                for tokcounter in range(1, num_entries(iftask, ";") - 1 + 1):
                    mestoken = substring(
                        entry(tokcounter - 1, iftask, ";"), 0, 2)
                    mesvalue = substring(entry(tokcounter - 1, iftask, ";"), 2)

                    if mestoken == "RC":
                        if mesvalue == rcode_list.rcode:
                            dyna = dyna + qsy.char1 + ";"

        if dyna != "":
            for tokcounter in range(1, num_entries(dyna, ";") + 1):
                mesvalue = trim(entry(tokcounter - 1, dyna, ";"))

                if mesvalue != "":
                    if rcode_list.startdate is not None and rcode_list.enddate is not None:
                        for datum in date_range(rcode_list.startdate, rcode_list.enddate):
                            queasy = get_cache(
                                Queasy, {"key": [(eq, 170)], "date1": [(eq, datum)], "number1": [(eq, roomnr)], "char1": [(eq, mesvalue)], "number2": [(eq, rcode_list.adult)], "number3": [(eq, rcode_list.child)]})

                            if queasy:
                                qsy = get_cache(
                                    Queasy, {"key": [(eq, 170)], "date1": [(eq, datum)], "number1": [(eq, roomnr)], "char1": [(eq, mesvalue)], "number2": [(eq, rcode_list.adult)], "number3": [(eq, rcode_list.child)]})

                                if qsy and qsy.deci1 != rcode_list.rmrate and qsy.logi1 == False and qsy.logi2 == False:
                                    bqueasy = get_cache(
                                        Queasy, {"_recid": [(eq, qsy._recid)]})

                                    if bqueasy:
                                        bqueasy.logi2 = True

                            elif not queasy:
                                queasy = db_session.query(Queasy).filter(
                                    (Queasy.key == 161) & (entry(0, Queasy.char1, ";") == mesvalue) & (entry(2, Queasy.char1, ";") == (str).lower())).first()
                                while queasy is not None:
                                    queasy = Queasy()
                                    db_session.add(queasy)

                                    queasy.key = 170
                                    queasy.date1 = datum
                                    queasy.char1 = mesvalue
                                    queasy.number1 = roomnr
                                    queasy.number2 = rcode_list.adult
                                    queasy.number3 = rcode_list.child
                                    queasy.logi2 = True
                                    queasy.char2 = rcode_list.rcode

                                    arrangement = get_cache(
                                        Arrangement, {"argtnr": [(eq, argtno)]})

                                    if arrangement:
                                        artikel = get_cache(
                                            Artikel, {"artnr": [(eq, arrangement.argt_artikelnr)]})

                                        if artikel:
                                            serv, vat = get_output(calc_servvat(
                                                artikel.departement, artikel.artnr, datum, artikel.service_code, artikel.mwst_code))

                                    if tax_included:
                                        queasy.deci1 = to_decimal(
                                            rcode_list.rmrate)
                                    else:
                                        queasy.deci1 = to_decimal(
                                            round(to_decimal(rcode_list.rmrate * (1 + serv + vat)), 0))

                                    bqueasy = get_cache(
                                        Queasy, {"key": [(eq, 18)], "number1": [(eq, marktno)]})

                                    if bqueasy:
                                        waehrung = get_cache(
                                            Waehrung, {"wabkurz": [(eq, bqueasy.char3)]})

                                    if waehrung:
                                        q_curr = get_cache(
                                            Queasy, {"char1": [(eq, waehrung.wabkurz)], "key": [(eq, 164)], "char2": [(ne, "")]})

                                        if q_curr:
                                            currency = q_curr.char2
                                        else:
                                            currency = "IDR"
                                    else:
                                        currency = "IDR"
                                    queasy.char3 = currency

                                    curr_recid = queasy._recid
                                    queasy = db_session.query(Queasy).filter(
                                        (Queasy.key == 161) & (entry(0, Queasy.char1, ";") == mesvalue) & (entry(2, Queasy.char1, ";") == (str).lower()) & (Queasy._recid > curr_recid)).first()
            else:
                if rcode_list.startdate is not None and rcode_list.enddate is not None:
                    for datum in date_range(rcode_list.startdate, rcode_list.enddate):
                        queasy = get_cache(
                            Queasy, {"key": [(eq, 170)], "date1": [(eq, datum)], "number1": [(eq, roomnr)], "char1": [(eq, rcode_list.rcode)], "number2": [(eq, rcode_list.adult)], "number3": [(eq, rcode_list.child)]})

                        if queasy:
                            qsy = get_cache(
                                Queasy, {"key": [(eq, 170)], "date1": [(eq, datum)], "number1": [(eq, roomnr)], "char1": [(eq, rcode_list.rcode)], "number2": [(eq, rcode_list.adult)], "number3": [(eq, rcode_list.child)]})

                            if qsy and qsy.deci1 != rcode_list.rmrate and qsy.logi1 == False and qsy.logi2 == False:
                                bqueasy = get_cache(
                                    Queasy, {"_recid": [(eq, qsy._recid)]})

                                if bqueasy:
                                    bqueasy.logi2 = True

                        elif not queasy:
                            queasy = db_session.query(Queasy).filter(
                                (Queasy.key == 161) & (entry(0, Queasy.char1, ";") == rcode_list.rcode) & (entry(2, Queasy.char1, ";") == (str).lower())).first()
                            while queasy is not None:
                                queasy = Queasy()
                                db_session.add(queasy)

                                queasy.key = 170
                                queasy.date1 = datum
                                queasy.char1 = rcode_list.rcode
                                queasy.number1 = roomnr
                                queasy.number2 = rcode_list.adult
                                queasy.number3 = rcode_list.child
                                queasy.logi2 = True

                                arrangement = get_cache(
                                    Arrangement, {"argtnr": [(eq, argtno)]})

                                if arrangement:
                                    artikel = get_cache(
                                        Artikel, {"artnr": [(eq, arrangement.argt_artikelnr)]})

                                    if artikel:
                                        serv, vat = get_output(calc_servvat(
                                            artikel.departement, artikel.artnr, datum, artikel.service_code, artikel.mwst_code))

                                if tax_included:
                                    queasy.deci1 = to_decimal(
                                        rcode_list.rmrate)
                                else:
                                    queasy.deci1 = to_decimal(
                                        round(to_decimal(rcode_list.rmrate * (1 + serv + vat)), 0))

                                bqueasy = get_cache(
                                    Queasy, {"key": [(eq, 18)], "number1": [(eq, marktno)]})

                                if bqueasy:
                                    waehrung = get_cache(
                                        Waehrung, {"wabkurz": [(eq, bqueasy.char3)]})

                                if waehrung:
                                    q_curr = get_cache(
                                        Queasy, {"char1": [(eq, waehrung.wabkurz)], "key": [(eq, 164)], "char2": [(ne, "")]})

                                    if q_curr:
                                        currency = q_curr.char2
                                    else:
                                        currency = "IDR"
                                else:
                                    currency = "IDR"
                                queasy.char3 = currency

                                curr_recid = queasy._recid
                                queasy = db_session.query(Queasy).filter(
                                    (Queasy.key == 161) & (entry(0, Queasy.char1, ";") == mesvalue) & (entry(2, Queasy.char1, ";") == (str).lower()) & (Queasy._recid > curr_recid)).first()

    done = False
    bediener = db_session.query(Bediener).filter(
        (matches(Bediener.username, "*LODGIQ*"))).first()

    if bediener:
        user_init = bediener.userinit

    queasy = get_cache(Queasy, {"key": [(eq, 152)]})

    if queasy:
        cat_flag = True

    htparam = get_cache(Htparam, {"paramnr": [(eq, 127)]})

    if htparam:
        tax_included = htparam.flogical

    for drcode_list in query(drcode_list_data):
        for j in range(1, num_entries(drcode_list.adult, "-") + 1):
            adlt = to_int(entry(j - 1, drcode_list.adult, "-"))

            if adlt == 1 or adlt == 2:
                rcode_list = Rcode_list()
                rcode_list_data.append(rcode_list)

                rcode_list.rcode = drcode_list.rcode
                rcode_list.startdate = drcode_list.startdate
                rcode_list.enddate = drcode_list.enddate
                rcode_list.adult = adlt
                rcode_list.child = to_int(drcode_list.child)
                rcode_list.rmtype = drcode_list.rmtype
                rcode_list.rmrate = to_decimal(to_decimal(
                    entry(j) - to_decimal(1, drcode_list.rmrate, "-")))
                rcode_list.currency = drcode_list.currency

            elif adlt == 3:
                rcode_list = Rcode_list()
                rcode_list_data.append(rcode_list)

                rcode_list.rcode = drcode_list.rcode
                rcode_list.startdate = drcode_list.startdate
                rcode_list.enddate = drcode_list.enddate
                rcode_list.adult = adlt
                rcode_list.child = to_int(drcode_list.child)
                rcode_list.rmtype = drcode_list.rmtype
                rcode_list.rmrate = to_decimal(to_decimal(entry(j) - to_decimal("1") - to_decimal(
                    "1"), drcode_list.rmrate, "-")) + to_decimal(to_decimal(entry(j), drcode_list.rmrate, "-") - to_decimal("1"))
                rcode_list.currency = drcode_list.currency

            elif adlt == 4:
                rcode_list = Rcode_list()
                rcode_list_data.append(rcode_list)

                rcode_list.rcode = drcode_list.rcode
                rcode_list.startdate = drcode_list.startdate
                rcode_list.enddate = drcode_list.enddate
                rcode_list.adult = 2
                rcode_list.child = 1
                rcode_list.rmtype = drcode_list.rmtype
                rcode_list.rmrate = to_decimal(to_decimal(entry(j) - to_decimal("2") - to_decimal(
                    1, drcode_list.rmrate, "-"))) + to_decimal(to_decimal(entry(j), drcode_list.rmrate, "-") - to_decimal("1"))
                rcode_list.currency = drcode_list.currency

    rcode_list = query(rcode_list_data, first=True)

    ratecode = get_cache(Ratecode, {"code": [(eq, rcode_list.rcode)]})

    if ratecode:
        argtno = ratecode.argtnr
        marktno = ratecode.marknr
        rc_bezeich = ratecode.bezeichnung
        rcode = ratecode.code

    else:
        done = False
        error_flag = 1

        return generate_output()

    for rcode_list in query(rcode_list_data):
        zimkateg = get_cache(Zimkateg, {"kurzbez": [(eq, rcode_list.rmtype)]})

        if zimkateg:
            ratecode = get_cache(
                Ratecode, {"startperiode": [(le, rcode_list.startdate)], "endperiode": [(ge, rcode_list.enddate)], "zikatnr": [(eq, zimkateg.zikatnr)], "erwachs": [(eq, rcode_list.adult)], "kind1": [(eq, rcode_list.child)], "code": [(eq, rcode_list.rcode)]})

            if not ratecode:
                ratecode = Ratecode()
                db_session.add(ratecode)

                ratecode.code = rcode_list.rcode
                ratecode.bezeichnung = rc_bezeich
                ratecode.startperiode = rcode_list.startdate
                ratecode.endperiode = rcode_list.enddate
                ratecode.erwachs = rcode_list.adult
                ratecode.kind1 = rcode_list.child
                ratecode.zikatnr = zimkateg.zikatnr
                ratecode.argtnr = argtno
                ratecode.marknr = marktno
                ratecode.zipreis = to_decimal(rcode_list.rmrate)
                ratecode.wday = 0

                bediener = get_cache(Bediener, {"userinit": [(eq, user_init)]})

                if bediener:
                    res_history = Res_history()
                    db_session.add(res_history)

                    res_history.nr = bediener.nr
                    res_history.datum = get_current_date()
                    res_history.zeit = get_current_time_in_seconds()
                    res_history.action = "RateCode"
                    # res_history.aenderung = "Create Rate, Code: " + rcode_list.rcode + " Room: " + zimkateg.kurzbez +\
                    #     " start:" + to_string(rcode_list.startdate) + "|end:" + to_string(rcode_list.enddate) +\
                    #     "|adult:" + to_string(rcode_list.adult) + "|rate:" + to_string(rcode_list.rmrate)
                    res_history.aenderung = f"Create Rate, Code: {rcode_list.rcode} Room: {zimkateg.kurzbez} start:{to_string(rcode_list.startdate)}|end:{to_string(rcode_list.enddate)}|adult:{to_string(rcode_list.adult)}|rate:{to_string(rcode_list.rmrate)}"

            elif ratecode and ratecode.startperiode == ratecode.endperiode and ratecode.zipreis != rcode_list.rmrate:
                bef_start = ratecode.startperiode
                bef_end = ratecode.endperiode
                bef_pax = ratecode.erwachs
                bef_rate = to_decimal(ratecode.zipreis)

                ratecode.zipreis = to_decimal(rcode_list.rmrate)
                bediener = get_cache(Bediener, {"userinit": [(eq, user_init)]})

                if bediener:
                    res_history = Res_history()
                    db_session.add(res_history)

                    res_history.nr = bediener.nr
                    res_history.datum = get_current_date()
                    res_history.zeit = get_current_time_in_seconds()
                    # res_history.aenderung = "Modify Rate, Code: " + rcode_list.rcode + " Room: " + zimkateg.kurzbez +\
                    #     ", FR: start:" + to_string(bef_start) + "|end:" + to_string(bef_end) + "|pax:" + to_string(bef_pax) + "|rate:" + to_string(bef_rate) +\
                    #     ", TO: start:" + to_string(rcode_list.startdate) + "|end:" + to_string(rcode_list.enddate) + "|pax:" + to_string(rcode_list.adult) + "|rate:" + to_string(rcode_list.rmrate)
                    res_history.aenderung = f"Modify Rate, Code: {rcode_list.rcode} Room: {zimkateg.kurzbez}, FR: start:{to_string(bef_start)}|end:{to_string(bef_end)}|pax:{to_string(bef_pax)}|rate:{to_string(bef_rate)}, TO: start:{to_string(rcode_list.startdate)}|end:{to_string(rcode_list.enddate)}|rate:{to_string(rcode_list.rmrate)}"
                    res_history.action = "RateCode"

            elif ratecode and ratecode.startperiode < ratecode.endperiode:
                bef_start = ratecode.startperiode
                bef_end = ratecode.endperiode
                bef_pax = ratecode.erwachs
                bef_rate = to_decimal(ratecode.zipreis)

                if ratecode.startperiode == rcode_list.startdate:
                    rcbuff = Ratecode()
                    db_session.add(rcbuff)

                    buffer_copy(ratecode, rcbuff, except_fields=[
                                "startperiode", "endperiode"])
                    rcbuff.startperiode = rcode_list.startdate
                    rcbuff.endperiode = rcode_list.enddate
                    rcbuff.zipreis = to_decimal(rcode_list.rmrate)

                    ratecode.startperiode = ratecode.startperiode + \
                        timedelta(days=1)

                elif ratecode.endperiode == rcode_list.enddate:
                    rcbuff = Ratecode()
                    db_session.add(rcbuff)

                    buffer_copy(ratecode, rcbuff, except_fields=[
                                "startperiode", "endperiode"])
                    rcbuff.startperiode = rcode_list.startdate
                    rcbuff.endperiode = rcode_list.enddate
                    rcbuff.zipreis = to_decimal(rcode_list.rmrate)

                    ratecode.endperiode = ratecode.endperiode - \
                        timedelta(days=1)

                else:
                    rcbuff = Ratecode()
                    db_session.add(rcbuff)

                    buffer_copy(ratecode, rcbuff, except_fields=[
                                "startperiode", "endperiode"])
                    rcbuff.startperiode = rcode_list.startdate
                    rcbuff.endperiode = rcode_list.enddate
                    rcbuff.zipreis = to_decimal(rcode_list.rmrate)

                    rcbuff = Ratecode()
                    db_session.add(rcbuff)

                    buffer_copy(ratecode, rcbuff,
                                except_fields=["startperiode"])
                    rcbuff.startperiode = rcode_list.startdate + \
                        timedelta(days=1)

                    ratecode.endperiode = rcode_list.enddate - \
                        timedelta(days=1)

                bediener = get_cache(Bediener, {"userinit": [(eq, user_init)]})

                if bediener:
                    res_history = Res_history()
                    db_session.add(res_history)

                    res_history.nr = bediener.nr
                    res_history.datum = get_current_date()
                    res_history.zeit = get_current_time_in_seconds()
                    res_history.aenderung = "Modify Rate, Code: " + rcode_list.rcode + " RT: " + zimkateg.kurzbez +\
                        ", FR: start:" + to_string(bef_start) + "|end:" + to_string(bef_end) + "|pax:" + to_string(bef_pax) + "|rate:" + to_string(bef_rate) +\
                        ", TO: start:" + to_string(rcode_list.startdate) + "|end:" + to_string(rcode_list.enddate) + "|pax:" + to_string(rcode_list.adult) + "|rate:" + to_string(rcode_list.rmrate)

                    res_history.action = "RateCode"
            update_bookengine_config()
            error_flag = 0

        else:
            done = False
            error_flag = 2
            error_rtype = rcode_list.rmtype

            return generate_output()
    get_output(update_child_rates_by_parent(rcode))

    if error_flag == 0:
        done = True

    return generate_output()
