# using conversion tools version: 1.0.0.117
"""_yusufwijasena_05/01/2026

        remark: - added validation when t_saldo is zero to avoid division by zero error
"""
from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Htparam, Debitor, Artikel, Guest, Waehrung


def ar_age_2_webbl(pvilanguage: int, from_art: int, to_art: int, to_date: date, from_name: string, to_name: string, disptype: int, cvt_flag: bool, dollar_rate: Decimal):

    prepare_cache([Htparam, Debitor, Artikel, Guest, Waehrung])

    outlist = ""
    arage_list_data = []
    tmpdays: int = 0
    lvcarea: string = "ar-age"
    default_fcurr: string = ""
    day1: int = 30
    day2: int = 30
    day3: int = 30
    price_decimal: int = 0
    long_digit: bool = False
    htparam = debitor = artikel = guest = waehrung = None

    ledger = age_list = arage_list = None

    ledger_data, Ledger = create_model(
        "Ledger",
        {
            "artnr": int,
            "bezeich": string,
            "debt0": Decimal,
            "debt1": Decimal,
            "debt2": Decimal,
            "debt3": Decimal,
            "tot_debt": Decimal
        })
    age_list_data, Age_list = create_model(
        "Age_list",
        {
            "artnr": int,
            "rechnr": int,
            "counter": int,
            "gastnr": int,
            "creditlimit": Decimal,
            "rgdatum": date,
            "gastname": string,
            "saldo": Decimal,
            "debt0": Decimal,
            "debt1": Decimal,
            "debt2": Decimal,
            "debt3": Decimal,
            "tot_debt": Decimal,
            "fcurr": string
        })
    arage_list_data, Arage_list = create_model(
        "Arage_list",
        {
            "curr": string,
            "gastnr": int,
            "number_str": string,
            "customer_name": string,
            "outstanding": string,
            "age1": string,
            "age2": string,
            "age3": string,
            "age4": string,
            "creditlimit": Decimal,
            "balance": Decimal,
            "creditlimit_str": string,
            "balance_str": string
        })

    db_session = local_storage.db_session

    def generate_output():
        nonlocal outlist, arage_list_data, tmpdays, lvcarea, default_fcurr, day1, day2, day3, price_decimal, long_digit, htparam, debitor, artikel, guest, waehrung
        nonlocal pvilanguage, from_art, to_art, to_date, from_name, to_name, disptype, cvt_flag, dollar_rate
        nonlocal ledger, age_list, arage_list
        nonlocal ledger_data, age_list_data, arage_list_data

        return {
            "outlist": outlist,
            "arage-list": arage_list_data
        }

    def age_list():
        nonlocal outlist, arage_list_data, tmpdays, lvcarea, default_fcurr, day1, day2, day3, price_decimal, long_digit, htparam, debitor, artikel, guest, waehrung
        nonlocal pvilanguage, from_art, to_art, to_date, from_name, to_name, disptype, cvt_flag, dollar_rate
        nonlocal ledger, age_list, arage_list
        nonlocal ledger_data, age_list_data, arage_list_data

        curr_art: int = 0
        billdate: date = None
        ct: int = 0
        t_debet: Decimal = to_decimal("0.0")
        t_credit: Decimal = to_decimal("0.0")
        t_comm: Decimal = to_decimal("0.0")
        t_adjust: Decimal = to_decimal("0.0")
        t_saldo: Decimal = to_decimal("0.0")
        t_debt0: Decimal = to_decimal("0.0")
        t_debt1: Decimal = to_decimal("0.0")
        t_debt2: Decimal = to_decimal("0.0")
        t_debt3: Decimal = to_decimal("0.0")
        tmp_saldo: Decimal = to_decimal("0.0")
        curr_name: string = ""
        curr_gastnr: int = 0
        creditlimit: Decimal = to_decimal("0.0")
        gastname: string = ""
        debt0: Decimal = to_decimal("0.0")
        debt1: Decimal = to_decimal("0.0")
        debt2: Decimal = to_decimal("0.0")
        debt3: Decimal = to_decimal("0.0")
        tot_debt: Decimal = to_decimal("0.0")
        ar_saldo: Decimal = to_decimal("0.0")
        fcurr: int = 0
        curr_fcurr: string = ""
        debt = None
        Debt = create_buffer("Debt", Debitor)
        ledger_data.clear()
        age_list_data.clear()
        arage_list_data.clear()

        for artikel in db_session.query(Artikel).filter(
                ((Artikel.artart == 2) | (Artikel.artart == 7)) &
                (Artikel.artnr >= from_art) &
                (Artikel.artnr <= to_art) &
                (Artikel.departement == 0)).order_by((to_string(Artikel.artart) + to_string(Artikel.artnr, "9999"))).all():
            ledger = Ledger()
            ledger_data.append(ledger)

            ledger.artnr = artikel.artnr
            ledger.bezeich = to_string(artikel.artnr) + " - " + artikel.bezeich
        curr_art = 0

        for debitor in db_session.query(Debitor).filter(
                (Debitor.artnr >= from_art) &
                (Debitor.artnr <= to_art) &
                (Debitor.rgdatum <= to_date) &
                (Debitor.opart == 0)).order_by(Debitor.artnr).all():

            if debitor.name.lower() >= (from_name).lower() and debitor.name.lower() <= (to_name).lower():

                if curr_art != debitor.artnr:
                    curr_art = debitor.artnr

                    artikel = get_cache(
                        Artikel, {"artnr": [(eq, curr_art)], "departement": [(eq, 0)]})

                if disptype == 0:
                    ar_saldo = to_decimal(debitor.saldo)
                else:

                    if not cvt_flag:
                        ar_saldo = to_decimal(debitor.vesrdep)
                    else:
                        ar_saldo = to_decimal(
                            debitor.saldo) / to_decimal(dollar_rate)

                if debitor.counter != 0:

                    if disptype == 0:

                        for debt in db_session.query(Debt).filter(
                                (Debt.rechnr == debitor.rechnr) &
                                (Debt.counter == debitor.counter) &
                                (Debt.opart == 1) &
                                (Debt.zahlkonto != 0) &
                                (Debt.rgdatum <= to_date)).order_by(Debt._recid).all():
                            ar_saldo = to_decimal(
                                ar_saldo) + to_decimal(debt.saldo)

                    else:

                        for debt in db_session.query(Debt).filter(
                                (Debt.rechnr == debitor.rechnr) & 
                                (Debt.counter == debitor.counter) &
                                (Debt.opart == 1) &
                                (Debt.zahlkonto != 0) & 
                                (Debt.betrieb_gastmem == debitor.betrieb_gastmem) &
                                (Debt.rgdatum <= to_date)).order_by(Debt._recid).all():

                            if not cvt_flag:
                                ar_saldo = to_decimal(
                                    ar_saldo) + to_decimal(debitor.vesrdep)
                            else:
                                ar_saldo = to_decimal(
                                    ar_saldo) + to_decimal((debitor.saldo) / to_decimal(dollar_rate))

                guest = get_cache(Guest, {"gastnr": [(eq, debitor.gastnr)]})
                age_list = Age_list()
                age_list_data.append(age_list)

                age_list.artnr = debitor.artnr
                age_list.rechnr = debitor.rechnr
                age_list.rgdatum = debitor.rgdatum
                age_list.counter = debitor.counter
                age_list.gastnr = debitor.gastnr
                age_list.creditlimit = to_decimal(guest.kreditlimit)
                age_list.tot_debt = to_decimal(ar_saldo)

                if debitor.betrieb_gastmem == 0:
                    age_list.fcurr = default_fcurr
                else:

                    waehrung = get_cache(
                        Waehrung, {"waehrungsnr": [(eq, debitor.betrieb_gastmem)]})

                    if waehrung:
                        age_list.fcurr = waehrung.wabkurz

                if artikel.artart == 2:
                    age_list.gastname = guest.name + ", " + guest.vorname1 + \
                        guest.anredefirma + " " + guest.anrede1
                    age_list.creditlimit = to_decimal(guest.kreditlimit)
                else:
                    age_list.creditlimit = to_decimal("0")

                    htparam = get_cache(Htparam, {"paramnr": [(eq, 867)]})

                    if debitor.gastnr == htparam.finteger:
                        age_list.gastname = "F&B " + artikel.bezeich
                    else:
                        age_list.gastname = "F/O " + artikel.bezeich
                tmpdays = (to_date - age_list.rgdatum).days

                if tmpdays > day3:
                    age_list.debt3 = to_decimal(
                        age_list.debt3) + to_decimal(ar_saldo)

                elif tmpdays > day2:
                    age_list.debt2 = to_decimal(
                        age_list.debt2) + to_decimal(ar_saldo)

                elif tmpdays > day1:
                    age_list.debt1 = to_decimal(
                        age_list.debt1) + to_decimal(ar_saldo)
                else:
                    age_list.debt0 = to_decimal(
                        age_list.debt0) + to_decimal(ar_saldo)
        curr_art = 0

        for debitor in db_session.query(Debitor).filter(
                (Debitor.artnr >= from_art) &
                (Debitor.artnr <= to_art) &
                (Debitor.rgdatum <= to_date) &
                (Debitor.opart == 2) &
                (Debitor.zahlkonto == 0)).order_by(Debitor.artnr).all():

            debt = get_cache(Debitor, {"rechnr": [(eq, debitor.rechnr)], "counter": [
                             (eq, debitor.counter)], "opart": [(eq, 2)], "zahlkonto": [(ne, 0)], "rgdatum": [(gt, to_date)]})

            if debt and debitor.name.lower() >= (from_name).lower() and debitor.name.lower() <= (to_name).lower():

                if curr_art != debitor.artnr:
                    curr_art = debitor.artnr

                    artikel = get_cache(
                        Artikel, {"artnr": [(eq, curr_art)], "departement": [(eq, 0)]})

                if disptype == 0:
                    ar_saldo = to_decimal(debitor.saldo)
                else:

                    if not cvt_flag:
                        ar_saldo = to_decimal(debitor.vesrdep)
                    else:
                        ar_saldo = to_decimal(
                            debitor.saldo) / to_decimal(dollar_rate)

                if disptype == 0:

                    for debt in db_session.query(Debt).filter(
                            (Debt.rechnr == debitor.rechnr) &
                            (Debt.counter == debitor.counter) &
                            (Debt.opart == 2) &
                            (Debt.zahlkonto != 0) & 
                            (Debt.rgdatum <= to_date)).order_by(Debt._recid).all():
                        ar_saldo = to_decimal(
                            ar_saldo) + to_decimal(debt.saldo)

                else:

                    for debt in db_session.query(Debt).filter(
                            (Debt.rechnr == debitor.rechnr) & 
                            (Debt.counter == debitor.counter) &
                            (Debt.opart == 2) &
                            (Debt.zahlkonto != 0) & 
                            (Debt.rgdatum <= to_date) & 
                            (Debt.betrieb_gastmem == debitor.betrieb_gastmem)).order_by(Debt._recid).all():

                        if not cvt_flag:
                            ar_saldo = to_decimal(
                                ar_saldo) + to_decimal(debt.vesrdep)
                        else:
                            ar_saldo = to_decimal(
                                ar_saldo) + to_decimal((debt.saldo) / to_decimal(dollar_rate))

                guest = get_cache(Guest, {"gastnr": [(eq, debitor.gastnr)]})
                age_list = Age_list()
                age_list_data.append(age_list)

                age_list.artnr = debitor.artnr
                age_list.rechnr = debitor.rechnr
                age_list.rgdatum = debitor.rgdatum
                age_list.counter = debitor.counter
                age_list.gastnr = debitor.gastnr
                age_list.creditlimit = to_decimal(guest.kreditlimit)
                age_list.tot_debt = to_decimal(ar_saldo)

                if debitor.betrieb_gastmem == 0:
                    age_list.fcurr = default_fcurr
                else:

                    waehrung = get_cache(
                        Waehrung, {"waehrungsnr": [(eq, debitor.betrieb_gastmem)]})

                    if waehrung:
                        age_list.fcurr = waehrung.wabkurz

                if artikel.artart == 2:
                    age_list.gastname = guest.name + ", " + guest.vorname1 + \
                        guest.anredefirma + " " + guest.anrede1
                    age_list.creditlimit = to_decimal(guest.kreditlimit)
                else:
                    age_list.creditlimit = to_decimal("0")

                    htparam = get_cache(Htparam, {"paramnr": [(eq, 867)]})

                    if debitor.gastnr == htparam.finteger:
                        age_list.gastname = "F&B " + artikel.bezeich
                    else:
                        age_list.gastname = "F/O " + artikel.bezeich
                tmpdays = (to_date - age_list.rgdatum).days

                if tmpdays > day3:
                    age_list.debt3 = to_decimal(
                        age_list.debt3) + to_decimal(ar_saldo)

                elif tmpdays > day2:
                    age_list.debt2 = to_decimal(
                        age_list.debt2) + to_decimal(ar_saldo)

                elif tmpdays > day1:
                    age_list.debt1 = to_decimal(
                        age_list.debt1) + to_decimal(ar_saldo)
                else:
                    age_list.debt0 = to_decimal(
                        age_list.debt0) + to_decimal(ar_saldo)

        for ledger in query(ledger_data, sort_by=[("artnr", False)]):

            artikel = get_cache(
                Artikel, {"artnr": [(eq, ledger.artnr)], "departement": [(eq, 0)]})

            age_list = query(age_list_data, filters=(
                lambda age_list: age_list.artnr == ledger.artnr), first=True)

            if not age_list:
                continue
            arage_list = Arage_list()
            arage_list_data.append(arage_list)

            arage_list.number_str = to_string(ledger.artnr) + " -"
            arage_list.customer_name = entry(1, ledger.bezeich, "-").upper()
            arage_list = Arage_list()
            arage_list_data.append(arage_list)

            ct = 0
            curr_gastnr = 0
            creditlimit = to_decimal("0")
            curr_fcurr = ""

            for age_list in query(age_list_data, filters=(lambda age_list: age_list.artnr == ledger.artnr and age_list.tot_debt != 0), sort_by=[("gastname", False)]):
                ledger.tot_debt = to_decimal(
                    ledger.tot_debt) + to_decimal(age_list.tot_debt)
                ledger.debt0 = to_decimal(
                    ledger.debt0) + to_decimal(age_list.debt0)
                ledger.debt1 = to_decimal(
                    ledger.debt1) + to_decimal(age_list.debt1)
                ledger.debt2 = to_decimal(
                    ledger.debt2) + to_decimal(age_list.debt2)
                ledger.debt3 = to_decimal(
                    ledger.debt3) + to_decimal(age_list.debt3)
                t_saldo = to_decimal(t_saldo) + to_decimal(age_list.tot_debt)
                t_debt0 = to_decimal(t_debt0) + to_decimal(age_list.debt0)
                t_debt1 = to_decimal(t_debt1) + to_decimal(age_list.debt1)
                t_debt2 = to_decimal(t_debt2) + to_decimal(age_list.debt2)
                t_debt3 = to_decimal(t_debt3) + to_decimal(age_list.debt3)

                if curr_gastnr == 0:
                    gastname = age_list.gastname
                    creditlimit = to_decimal(age_list.creditlimit)
                    tot_debt = to_decimal(age_list.tot_debt)
                    debt0 = to_decimal(age_list.debt0)
                    debt1 = to_decimal(age_list.debt1)
                    debt2 = to_decimal(age_list.debt2)
                    debt3 = to_decimal(age_list.debt3)
                    ct = ct + 1

                elif curr_name != age_list.gastname:

                    if price_decimal == 0:

                        if not long_digit:
                            arage_list = Arage_list()
                            arage_list_data.append(arage_list)

                            arage_list.number_str = to_string(ct, ">>>9")
                            arage_list.customer_name = gastname
                            arage_list.outstanding = to_string(
                                tot_debt, "->>,>>>,>>>,>>9.99")
                            arage_list.age1 = to_string(
                                debt0, "->>,>>>,>>>,>>9.99")
                            arage_list.age2 = to_string(
                                debt1, "->>,>>>,>>>,>>9.99")
                            arage_list.age3 = to_string(
                                debt2, "->>,>>>,>>>,>>9.99")
                            arage_list.age4 = to_string(
                                debt3, "->>,>>>,>>>,>>9.99")

                            if artikel.artart == 2:
                                arage_list.curr = age_list.fcurr
                                arage_list.gastnr = age_list.gastnr

                        else:
                            arage_list = Arage_list()
                            arage_list_data.append(arage_list)

                            arage_list.number_str = to_string(ct, ">>>9")
                            arage_list.customer_name = gastname
                            arage_list.outstanding = to_string(
                                tot_debt, "->>,>>>,>>>,>>>,>>9.99")
                            arage_list.age1 = to_string(
                                debt0, "->>,>>>,>>>,>>>,>>9.99")
                            arage_list.age2 = to_string(
                                debt1, "->>,>>>,>>>,>>>,>>9.99")
                            arage_list.age3 = to_string(
                                debt2, "->>,>>>,>>>,>>>,>>9.99")
                            arage_list.age4 = to_string(
                                debt3, "->>,>>>,>>>,>>>,>>9.99")

                            if artikel.artart == 2:
                                arage_list.curr = age_list.fcurr
                                arage_list.gastnr = age_list.gastnr

                    else:
                        arage_list = Arage_list()
                        arage_list_data.append(arage_list)

                        arage_list.number_str = to_string(ct, ">>>9")
                        arage_list.customer_name = gastname
                        arage_list.outstanding = to_string(
                            tot_debt, "->>,>>>,>>>,>>>,>>9.99")
                        arage_list.age1 = to_string(
                            debt0, "->>,>>>,>>>,>>>,>>9.99")
                        arage_list.age2 = to_string(
                            debt1, "->>,>>>,>>>,>>>,>>9.99")
                        arage_list.age3 = to_string(
                            debt2, "->>,>>>,>>>,>>>,>>9.99")
                        arage_list.age4 = to_string(
                            debt3, "->>,>>>,>>>,>>>,>>9.99")

                        if artikel.artart == 2:
                            arage_list.curr = age_list.fcurr
                            arage_list.gastnr = age_list.gastnr

                    creditlimit = to_decimal(age_list.creditlimit)
                    gastname = age_list.gastname
                    tot_debt = to_decimal(age_list.tot_debt)
                    debt0 = to_decimal(age_list.debt0)
                    debt1 = to_decimal(age_list.debt1)
                    debt2 = to_decimal(age_list.debt2)
                    debt3 = to_decimal(age_list.debt3)
                    ct = ct + 1

                    arage_list.creditlimit = to_decimal(creditlimit)

                    if arage_list.creditlimit != 0:
                        arage_list.balance = to_decimal(
                            arage_list.creditlimit) - to_decimal(tot_debt)
                    else:
                        arage_list.balance = to_decimal("0")
                    arage_list.creditlimit_str = to_string(
                        arage_list.creditlimit, "->>,>>>,>>>,>>>,>>9.99")
                    arage_list.balance_str = to_string(
                        arage_list.balance, "->>,>>>,>>>,>>>,>>9.99")
                else:
                    tot_debt = to_decimal(tot_debt) + \
                        to_decimal(age_list.tot_debt)
                    debt0 = to_decimal(debt0) + to_decimal(age_list.debt0)
                    debt1 = to_decimal(debt1) + to_decimal(age_list.debt1)
                    debt2 = to_decimal(debt2) + to_decimal(age_list.debt2)
                    debt3 = to_decimal(debt3) + to_decimal(age_list.debt3)

                curr_gastnr = age_list.gastnr
                curr_name = age_list.gastname
                curr_fcurr = age_list.fcurr
                age_list_data.remove(age_list)

            if ct > 0:

                if price_decimal == 0:

                    if not long_digit:
                        arage_list = Arage_list()
                        arage_list_data.append(arage_list)

                        arage_list.number_str = to_string(ct, ">>>9")
                        arage_list.customer_name = gastname
                        arage_list.outstanding = to_string(
                            tot_debt, "->>,>>>,>>>,>>9.99")
                        arage_list.age1 = to_string(
                            debt0, "->>,>>>,>>>,>>9.99")
                        arage_list.age2 = to_string(
                            debt1, "->>,>>>,>>>,>>9.99")
                        arage_list.age3 = to_string(
                            debt2, "->>,>>>,>>>,>>9.99")
                        arage_list.age4 = to_string(
                            debt3, "->>,>>>,>>>,>>9.99")

                        if artikel.artart == 2:
                            arage_list.curr = curr_fcurr
                            arage_list.gastnr = curr_gastnr

                    else:
                        arage_list = Arage_list()
                        arage_list_data.append(arage_list)

                        arage_list.number_str = to_string(ct, ">>>9")
                        arage_list.customer_name = gastname
                        arage_list.outstanding = to_string(
                            tot_debt, "->>,>>>,>>>,>>>,>>9.99")
                        arage_list.age1 = to_string(
                            debt0, "->>,>>>,>>>,>>>,>>9.99")
                        arage_list.age2 = to_string(
                            debt1, "->>,>>>,>>>,>>>,>>9.99")
                        arage_list.age3 = to_string(
                            debt2, "->>,>>>,>>>,>>>,>>9.99")
                        arage_list.age4 = to_string(
                            debt3, "->>,>>>,>>>,>>>,>>9.99")
                        arage_list.curr = age_list.fcurr
                        arage_list.gastnr = age_list.gastnr

                        if artikel.artart == 2:
                            arage_list.curr = curr_fcurr
                            arage_list.gastnr = curr_gastnr

                else:
                    arage_list = Arage_list()
                    arage_list_data.append(arage_list)

                    arage_list.number_str = to_string(ct, ">>>9")
                    arage_list.customer_name = gastname
                    arage_list.outstanding = to_string(
                        tot_debt, "->>,>>>,>>>,>>>,>>9.99")
                    arage_list.age1 = to_string(
                        debt0, "->>,>>>,>>>,>>>,>>9.99")
                    arage_list.age2 = to_string(
                        debt1, "->>,>>>,>>>,>>>,>>9.99")
                    arage_list.age3 = to_string(
                        debt2, "->>,>>>,>>>,>>>,>>9.99")
                    arage_list.age4 = to_string(
                        debt3, "->>,>>>,>>>,>>>,>>9.99")

                    if artikel.artart == 2:
                        arage_list.curr = curr_fcurr
                        arage_list.gastnr = curr_gastnr

                arage_list.creditlimit = to_decimal(creditlimit)

                if arage_list.creditlimit != 0:
                    arage_list.balance = to_decimal(
                        arage_list.creditlimit) - to_decimal(tot_debt)
                else:
                    arage_list.balance = to_decimal("0")
                arage_list.creditlimit_str = to_string(
                    arage_list.creditlimit, "->>,>>>,>>>,>>>,>>9.99")
                arage_list.balance_str = to_string(
                    arage_list.balance, "->>,>>>,>>>,>>>,>>9.99")
            tmp_saldo = to_decimal(ledger.tot_debt)

            if tmp_saldo == 0:
                tmp_saldo = to_decimal("1")

            if price_decimal == 0:

                if not long_digit:
                    arage_list = Arage_list()
                    arage_list_data.append(arage_list)

                    arage_list.customer_name = "T o t a l"
                    arage_list.outstanding = to_string(
                        ledger.tot_debt, "->>,>>>,>>>,>>9.99")
                    arage_list.age1 = to_string(
                        ledger.debt0, "->>,>>>,>>>,>>9.99")
                    arage_list.age2 = to_string(
                        ledger.debt1, "->>,>>>,>>>,>>9.99")
                    arage_list.age3 = to_string(
                        ledger.debt2, "->>,>>>,>>>,>>9.99")
                    arage_list.age4 = to_string(
                        ledger.debt3, "->>,>>>,>>>,>>9.99")

                else:
                    arage_list = Arage_list()
                    arage_list_data.append(arage_list)

                    arage_list.customer_name = "T o t a l"
                    arage_list.outstanding = to_string(
                        ledger.tot_debt, "->>,>>>,>>>,>>>,>>9.99")
                    arage_list.age1 = to_string(
                        ledger.debt0, "->>,>>>,>>>,>>>,>>9.99")
                    arage_list.age2 = to_string(
                        ledger.debt1, "->>,>>>,>>>,>>>,>>9.99")
                    arage_list.age3 = to_string(
                        ledger.debt2, "->>,>>>,>>>,>>>,>>9.99")
                    arage_list.age4 = to_string(
                        ledger.debt3, "->>,>>>,>>>,>>>,>>9.99")

            else:
                arage_list = Arage_list()
                arage_list_data.append(arage_list)

                arage_list.customer_name = "T o t a l"
                arage_list.outstanding = to_string(
                    ledger.tot_debt, "->>,>>>,>>>,>>>,>>9.99")
                arage_list.age1 = to_string(
                    ledger.debt0, "->>,>>>,>>>,>>>,>>9.99")
                arage_list.age2 = to_string(
                    ledger.debt1, "->>,>>>,>>>,>>>,>>9.99")
                arage_list.age3 = to_string(
                    ledger.debt2, "->>,>>>,>>>,>>>,>>9.99")
                arage_list.age4 = to_string(
                    ledger.debt3, "->>,>>>,>>>,>>>,>>9.99")

            if not long_digit:
                arage_list = Arage_list()
                arage_list_data.append(arage_list)

                arage_list.customer_name = "Statistic Percentage (%):"
                arage_list.outstanding = to_string(
                    (ledger.tot_debt / tmp_saldo * 100), "->>,>>9.99")
                arage_list.age1 = to_string(
                    (ledger.debt0 / tmp_saldo * 100), "->>,>>9.99")
                arage_list.age2 = to_string(
                    (ledger.debt1 / tmp_saldo * 100), "->>,>>9.99")
                arage_list.age3 = to_string(
                    (ledger.debt2 / tmp_saldo * 100), "->>,>>9.99")
                arage_list.age4 = to_string(
                    (ledger.debt3 / tmp_saldo * 100), "->>,>>9.99")

            else:
                arage_list = Arage_list()
                arage_list_data.append(arage_list)

                arage_list.customer_name = "Statistic Percentage (%):"
                arage_list.outstanding = to_string(
                    (ledger.tot_debt / tmp_saldo * 100), "->>,>>9.99")
                arage_list.age1 = to_string(
                    (ledger.debt0 / tmp_saldo * 100), "->>,>>9.99")
                arage_list.age2 = to_string(
                    (ledger.debt1 / tmp_saldo * 100), "->>,>>9.99")
                arage_list.age3 = to_string(
                    (ledger.debt2 / tmp_saldo * 100), "->>,>>9.99")
                arage_list.age4 = to_string(
                    (ledger.debt3 / tmp_saldo * 100), "->>,>>9.99")

            arage_list = Arage_list()
            arage_list_data.append(arage_list)

        arage_list = Arage_list()
        arage_list_data.append(arage_list)

        if price_decimal == 0:

            if not long_digit:
                arage_list = Arage_list()
                arage_list_data.append(arage_list)

                arage_list.customer_name = "T O T A L A/R:"
                arage_list.outstanding = to_string(
                    t_saldo, "->>,>>>,>>>,>>9.99")
                arage_list.age1 = to_string(t_debt0, "->>,>>>,>>>,>>9.99")
                arage_list.age2 = to_string(t_debt1, "->>,>>>,>>>,>>9.99")
                arage_list.age3 = to_string(t_debt2, "->>,>>>,>>>,>>9.99")
                arage_list.age4 = to_string(t_debt3, "->>,>>>,>>>,>>9.99")

            else:
                arage_list = Arage_list()
                arage_list_data.append(arage_list)

                arage_list.customer_name = "T O T A L A/R:"
                arage_list.outstanding = to_string(
                    t_saldo, "->>,>>>,>>>,>>>,>>9.99")
                arage_list.age1 = to_string(t_debt0, "->>,>>>,>>>,>>>,>>9.99")
                arage_list.age2 = to_string(t_debt1, "->>,>>>,>>>,>>>,>>9.99")
                arage_list.age3 = to_string(t_debt2, "->>,>>>,>>>,>>>,>>9.99")
                arage_list.age4 = to_string(t_debt3, "->>,>>>,>>>,>>>,>>9.99")

        else:
            arage_list = Arage_list()
            arage_list_data.append(arage_list)

            arage_list.customer_name = "T O T A L A/R:"
            arage_list.outstanding = to_string(
                t_saldo, "->>,>>>,>>>,>>>,>>9.99")
            arage_list.age1 = to_string(t_debt0, "->>,>>>,>>>,>>>,>>9.99")
            arage_list.age2 = to_string(t_debt1, "->>,>>>,>>>,>>>,>>9.99")
            arage_list.age3 = to_string(t_debt2, "->>,>>>,>>>,>>>,>>9.99")
            arage_list.age4 = to_string(t_debt3, "->>,>>>,>>>,>>>,>>9.99")

        arage_list = Arage_list()
        arage_list_data.append(arage_list)

        if not long_digit:
            arage_list = Arage_list()
            arage_list_data.append(arage_list)

            arage_list.customer_name = "Statistic Percentage (%):"
            arage_list.outstanding = "100.00"
            if t_saldo != 0:
                arage_list.age1 = to_string(
                    (t_debt0 / t_saldo * 100), "->>,>>9.99")
                arage_list.age2 = to_string(
                    (t_debt1 / t_saldo * 100), "->>,>>9.99")
                arage_list.age3 = to_string(
                    (t_debt2 / t_saldo * 100), "->>,>>9.99")
                arage_list.age4 = to_string(
                    (t_debt3 / t_saldo * 100), "->>,>>9.99")
            else:
                arage_list.age1 = to_string(to_decimal("0.0"), "->>,>>9.99")
                arage_list.age2 = to_string(to_decimal("0.0"), "->>,>>9.99")
                arage_list.age3 = to_string(to_decimal("0.0"), "->>,>>9.99")
                arage_list.age4 = to_string(to_decimal("0.0"), "->>,>>9.99")

        else:
            arage_list = Arage_list()
            arage_list_data.append(arage_list)

            arage_list.customer_name = "Statistic Percentage (%):"
            arage_list.outstanding = "100.00"
            if t_saldo != 0:
                arage_list.age1 = to_string(
                    (t_debt0 / t_saldo * 100), "->>,>>9.99")
                arage_list.age2 = to_string(
                    (t_debt1 / t_saldo * 100), "->>,>>9.99")
                arage_list.age3 = to_string(
                    (t_debt2 / t_saldo * 100), "->>,>>9.99")
                arage_list.age4 = to_string(
                    (t_debt3 / t_saldo * 100), "->>,>>9.99")
            else:
                arage_list.age1 = to_string(to_decimal("0.0"), "->>,>>9.99")
                arage_list.age2 = to_string(to_decimal("0.0"), "->>,>>9.99")
                arage_list.age3 = to_string(to_decimal("0.0"), "->>,>>9.99")
                arage_list.age4 = to_string(to_decimal("0.0"), "->>,>>9.99")

        arage_list = Arage_list()
        arage_list_data.append(arage_list)

    def age_lista():
        nonlocal outlist, arage_list_data, tmpdays, lvcarea, default_fcurr, day1, day2, day3, price_decimal, long_digit, htparam, debitor, artikel, guest, waehrung
        nonlocal pvilanguage, from_art, to_art, to_date, from_name, to_name, disptype, cvt_flag, dollar_rate
        nonlocal ledger, age_list, arage_list
        nonlocal ledger_data, age_list_data, arage_list_data

        curr_art: int = 0
        billdate: date = None
        ct: int = 0
        t_debet: Decimal = to_decimal("0.0")
        t_credit: Decimal = to_decimal("0.0")
        t_comm: Decimal = to_decimal("0.0")
        t_adjust: Decimal = to_decimal("0.0")
        t_saldo: Decimal = to_decimal("0.0")
        t_debt0: Decimal = to_decimal("0.0")
        t_debt1: Decimal = to_decimal("0.0")
        t_debt2: Decimal = to_decimal("0.0")
        t_debt3: Decimal = to_decimal("0.0")
        tmp_saldo: Decimal = to_decimal("0.0")
        curr_name: string = ""
        curr_gastnr: int = 0
        creditlimit: Decimal = to_decimal("0.0")
        gastname: string = ""
        debt0: Decimal = to_decimal("0.0")
        debt1: Decimal = to_decimal("0.0")
        debt2: Decimal = to_decimal("0.0")
        debt3: Decimal = to_decimal("0.0")
        tot_debt: Decimal = to_decimal("0.0")
        fcurr: int = 0
        curr_fcurr: string = ""
        balance: Decimal = to_decimal("0.0")
        debt = None
        ar_saldo: Decimal = to_decimal("0.0")
        Debt = create_buffer("Debt", Debitor)
        ledger_data.clear()
        age_list_data.clear()
        arage_list_data.clear()

        for artikel in db_session.query(Artikel).filter(
                ((Artikel.artart == 2) | (Artikel.artart == 7)) &
                (Artikel.artnr >= from_art) & 
                (Artikel.artnr <= to_art) &
                (Artikel.departement == 0)).order_by((to_string(Artikel.artart) + to_string(Artikel.artnr, "9999"))).all():
            ledger = Ledger()
            ledger_data.append(ledger)

            ledger.artnr = artikel.artnr
            ledger.bezeich = to_string(artikel.artnr) + " - " + artikel.bezeich
        curr_art = 0

        for debitor in db_session.query(Debitor).filter(
                (Debitor.artnr >= from_art) & 
                (Debitor.artnr <= to_art) &
                (Debitor.rgdatum <= to_date) &
                (Debitor.opart == 0)).order_by(Debitor.artnr).all():

            if debitor.name.lower() >= (from_name).lower():

                if curr_art != debitor.artnr:
                    curr_art = debitor.artnr

                    artikel = get_cache(
                        Artikel, {"artnr": [(eq, curr_art)], "departement": [(eq, 0)]})

                if disptype == 1:

                    if not cvt_flag:
                        ar_saldo = to_decimal(debitor.vesrdep)
                    else:
                        ar_saldo = to_decimal(
                            debitor.saldo) / to_decimal(dollar_rate)

                else:
                    ar_saldo = to_decimal(debitor.saldo)

                if debitor.counter != 0:

                    if disptype == 0:

                        for debt in db_session.query(Debt).filter(
                                (Debt.rechnr == debitor.rechnr) & 
                                (Debt.counter == debitor.counter) &
                                (Debt.opart == 1) &
                                (Debt.zahlkonto != 0) &
                                (Debt.rgdatum <= to_date)).order_by(Debt._recid).all():

                            if disptype == 0:
                                ar_saldo = to_decimal(
                                    ar_saldo) + to_decimal(debt.saldo)
                            else:

                                if not cvt_flag:
                                    ar_saldo = to_decimal(
                                        ar_saldo) + to_decimal(debt.vesrdep)
                                else:
                                    ar_saldo = to_decimal(
                                        ar_saldo) + to_decimal((debt.saldo) / to_decimal(dollar_rate))

                    else:

                        for debt in db_session.query(Debt).filter(
                                (Debt.rechnr == debitor.rechnr) &
                                (Debt.counter == debitor.counter) &
                                (Debt.opart == 1) & 
                                (Debt.zahlkonto != 0) & 
                                (Debt.betrieb_gastmem == debitor.betrieb_gastmem) &
                                (Debt.rgdatum <= to_date)).order_by(Debt._recid).all():

                            if not cvt_flag:
                                ar_saldo = to_decimal(
                                    ar_saldo) + to_decimal(debt.vesrdep)
                            else:
                                ar_saldo = to_decimal(
                                    ar_saldo) + to_decimal((debt.saldo) / to_decimal(dollar_rate))

                guest = get_cache(Guest, {"gastnr": [(eq, debitor.gastnr)]})
                age_list = Age_list()
                age_list_data.append(age_list)

                age_list.artnr = debitor.artnr
                age_list.rechnr = debitor.rechnr
                age_list.rgdatum = debitor.rgdatum
                age_list.counter = debitor.counter
                age_list.gastnr = debitor.gastnr
                age_list.creditlimit = to_decimal(guest.kreditlimit)
                age_list.tot_debt = to_decimal(ar_saldo)

                if debitor.betrieb_gastmem == 0:
                    age_list.fcurr = default_fcurr
                else:

                    waehrung = get_cache(
                        Waehrung, {"waehrungsnr": [(eq, debitor.betrieb_gastmem)]})

                    if waehrung:
                        age_list.fcurr = waehrung.wabkurz

                if artikel.artart == 2:
                    age_list.gastname = guest.name + ", " + guest.vorname1 + \
                        guest.anredefirma + " " + guest.anrede1
                    age_list.creditlimit = to_decimal(guest.kreditlimit)
                else:
                    age_list.creditlimit = to_decimal("0")

                    htparam = get_cache(Htparam, {"paramnr": [(eq, 867)]})

                    if debitor.gastnr == htparam.finteger:
                        age_list.gastname = "F&B " + artikel.bezeich
                    else:
                        age_list.gastname = "F/O " + artikel.bezeich
                tmpdays = (to_date - age_list.rgdatum).days

                if tmpdays > day3:
                    age_list.debt3 = to_decimal(
                        age_list.debt3) + to_decimal(ar_saldo)

                elif tmpdays > day2:
                    age_list.debt2 = to_decimal(
                        age_list.debt2) + to_decimal(ar_saldo)

                elif tmpdays > day1:
                    age_list.debt1 = to_decimal(
                        age_list.debt1) + to_decimal(ar_saldo)
                else:
                    age_list.debt0 = to_decimal(
                        age_list.debt0) + to_decimal(ar_saldo)
        curr_art = 0

        for debitor in db_session.query(Debitor).filter(
                (Debitor.artnr >= from_art) &
                (Debitor.artnr <= to_art) &
                (Debitor.rgdatum <= to_date) &
                (Debitor.opart == 2) &
                (Debitor.zahlkonto == 0)).order_by(Debitor.artnr).all():

            debt = get_cache(Debitor, {"rechnr": [(eq, debitor.rechnr)], "counter": [
                             (eq, debitor.counter)], "opart": [(eq, 2)], "zahlkonto": [(ne, 0)], "rgdatum": [(gt, to_date)]})

            if debt and debitor.name.lower() >= (from_name).lower():

                if curr_art != debitor.artnr:
                    curr_art = debitor.artnr

                    artikel = get_cache(
                        Artikel, {"artnr": [(eq, curr_art)], "departement": [(eq, 0)]})

                if disptype == 0:
                    ar_saldo = to_decimal(debitor.saldo)
                else:

                    if not cvt_flag:
                        ar_saldo = to_decimal(debitor.vesrdep)
                    else:
                        ar_saldo = to_decimal(
                            debitor.saldo) / to_decimal(dollar_rate)

                if disptype == 0:

                    for debt in db_session.query(Debt).filter(
                            (Debt.rechnr == debitor.rechnr) & 
                            (Debt.counter == debitor.counter) &
                            (Debt.opart == 2) &
                            (Debt.zahlkonto != 0) &
                            (Debt.rgdatum <= to_date)).order_by(Debt._recid).all():
                        ar_saldo = to_decimal(
                            ar_saldo) + to_decimal(debt.saldo)

                else:

                    for debt in db_session.query(Debt).filter(
                            (Debt.rechnr == debitor.rechnr) &
                            (Debt.counter == debitor.counter) &
                            (Debt.opart == 2) &
                            (Debt.zahlkonto != 0) & 
                            (Debt.rgdatum <= to_date) & 
                            (Debt.betrieb_gastmem == debitor.betrieb_gastmem)).order_by(Debt._recid).all():

                        if not cvt_flag:
                            ar_saldo = to_decimal(
                                ar_saldo) + to_decimal(debt.vesrdep)
                        else:
                            ar_saldo = to_decimal(
                                ar_saldo) + to_decimal((debt.saldo) / to_decimal(dollar_rate))

                guest = get_cache(Guest, {"gastnr": [(eq, debitor.gastnr)]})
                age_list = Age_list()
                age_list_data.append(age_list)

                age_list.artnr = debitor.artnr
                age_list.rechnr = debitor.rechnr
                age_list.rgdatum = debitor.rgdatum
                age_list.counter = debitor.counter
                age_list.gastnr = debitor.gastnr
                age_list.creditlimit = to_decimal(guest.kreditlimit)
                age_list.tot_debt = to_decimal(ar_saldo)

                if debitor.betrieb_gastmem == 0:
                    age_list.fcurr = default_fcurr
                else:

                    waehrung = get_cache(
                        Waehrung, {"waehrungsnr": [(eq, debitor.betrieb_gastmem)]})

                    if waehrung:
                        age_list.fcurr = waehrung.wabkurz

                if artikel.artart == 2:
                    age_list.gastname = guest.name + ", " + guest.vorname1 + \
                        guest.anredefirma + " " + guest.anrede1
                    age_list.creditlimit = to_decimal(guest.kreditlimit)
                else:
                    age_list.creditlimit = to_decimal("0")

                    htparam = get_cache(Htparam, {"paramnr": [(eq, 867)]})

                    if debitor.gastnr == htparam.finteger:
                        age_list.gastname = "F&B " + artikel.bezeich
                    else:
                        age_list.gastname = "F/O " + artikel.bezeich
                tmpdays = (to_date - age_list.rgdatum).days

                if tmpdays > day3:
                    age_list.debt3 = to_decimal(
                        age_list.debt3) + to_decimal(ar_saldo)

                elif tmpdays > day2:
                    age_list.debt2 = to_decimal(
                        age_list.debt2) + to_decimal(ar_saldo)

                elif tmpdays > day1:
                    age_list.debt1 = to_decimal(
                        age_list.debt1) + to_decimal(ar_saldo)
                else:
                    age_list.debt0 = to_decimal(
                        age_list.debt0) + to_decimal(ar_saldo)

        for ledger in query(ledger_data, sort_by=[("artnr", False)]):

            age_list = query(age_list_data, filters=(
                lambda age_list: age_list.artnr == ledger.artnr), first=True)

            if not age_list:
                continue
            arage_list = Arage_list()
            arage_list_data.append(arage_list)

            arage_list.number_str = to_string(ledger.artnr) + " -"
            arage_list.customer_name = entry(1, ledger.bezeich, "-").upper()
            arage_list = Arage_list()
            arage_list_data.append(arage_list)

            ct = 0
            curr_gastnr = 0
            creditlimit = to_decimal("0")

            for age_list in query(age_list_data, filters=(lambda age_list: age_list.artnr == ledger.artnr and age_list.tot_debt != 0), sort_by=[("gastname", False)]):
                ledger.tot_debt = to_decimal(
                    ledger.tot_debt) + to_decimal(age_list.tot_debt)
                ledger.debt0 = to_decimal(
                    ledger.debt0) + to_decimal(age_list.debt0)
                ledger.debt1 = to_decimal(
                    ledger.debt1) + to_decimal(age_list.debt1)
                ledger.debt2 = to_decimal(
                    ledger.debt2) + to_decimal(age_list.debt2)
                ledger.debt3 = to_decimal(
                    ledger.debt3) + to_decimal(age_list.debt3)
                t_saldo = to_decimal(t_saldo) + to_decimal(age_list.tot_debt)
                t_debt0 = to_decimal(t_debt0) + to_decimal(age_list.debt0)
                t_debt1 = to_decimal(t_debt1) + to_decimal(age_list.debt1)
                t_debt2 = to_decimal(t_debt2) + to_decimal(age_list.debt2)
                t_debt3 = to_decimal(t_debt3) + to_decimal(age_list.debt3)

                if curr_gastnr == 0:
                    gastname = age_list.gastname
                    creditlimit = to_decimal(age_list.creditlimit)
                    tot_debt = to_decimal(age_list.tot_debt)
                    debt0 = to_decimal(age_list.debt0)
                    debt1 = to_decimal(age_list.debt1)
                    debt2 = to_decimal(age_list.debt2)
                    debt3 = to_decimal(age_list.debt3)
                    ct = ct + 1

                elif curr_name != age_list.gastname:

                    if price_decimal == 0:

                        if not long_digit:
                            arage_list = Arage_list()
                            arage_list_data.append(arage_list)

                            arage_list.number_str = to_string(ct, ">>>9")
                            arage_list.customer_name = gastname
                            arage_list.outstanding = to_string(
                                tot_debt, "->>,>>>,>>>,>>9.99")
                            arage_list.age1 = to_string(
                                debt0, "->>,>>>,>>>,>>9.99")
                            arage_list.age2 = to_string(
                                debt1, "->>,>>>,>>>,>>9.99")
                            arage_list.age3 = to_string(
                                debt2, "->>,>>>,>>>,>>9.99")
                            arage_list.age4 = to_string(
                                debt3, "->>,>>>,>>>,>>9.99")
                            arage_list.curr = age_list.fcurr
                            arage_list.gastnr = age_list.gastnr

                        else:
                            arage_list = Arage_list()
                            arage_list_data.append(arage_list)

                            arage_list.number_str = to_string(ct, ">>>9")
                            arage_list.customer_name = gastname
                            arage_list.outstanding = to_string(
                                tot_debt, "->>,>>>,>>>,>>>,>>9.99")
                            arage_list.age1 = to_string(
                                debt0, "->>,>>>,>>>,>>>,>>9.99")
                            arage_list.age2 = to_string(
                                debt1, "->>,>>>,>>>,>>>,>>9.99")
                            arage_list.age3 = to_string(
                                debt2, "->>,>>>,>>>,>>>,>>9.99")
                            arage_list.age4 = to_string(
                                debt3, "->>,>>>,>>>,>>>,>>9.99")
                            arage_list.curr = age_list.fcurr
                            arage_list.gastnr = age_list.gastnr

                    else:
                        arage_list = Arage_list()
                        arage_list_data.append(arage_list)

                        arage_list.number_str = to_string(ct, ">>>9")
                        arage_list.customer_name = gastname
                        arage_list.outstanding = to_string(
                            tot_debt, "->>,>>>,>>>,>>>,>>9.99")
                        arage_list.age1 = to_string(
                            debt0, "->>,>>>,>>>,>>>,>>9.99")
                        arage_list.age2 = to_string(
                            debt1, "->>,>>>,>>>,>>>,>>9.99")
                        arage_list.age3 = to_string(
                            debt2, "->>,>>>,>>>,>>>,>>9.99")
                        arage_list.age4 = to_string(
                            debt3, "->>,>>>,>>>,>>>,>>9.99")
                        arage_list.curr = age_list.fcurr
                        arage_list.gastnr = age_list.gastnr

                    arage_list.creditlimit = to_decimal(creditlimit)

                    if arage_list.creditlimit != 0:
                        arage_list.balance = to_decimal(
                            arage_list.creditlimit) - to_decimal(tot_debt)
                    else:
                        arage_list.balance = to_decimal("0")
                    arage_list.creditlimit_str = to_string(
                        arage_list.creditlimit, "->>,>>>,>>>,>>>,>>9.99")
                    arage_list.balance_str = to_string(
                        arage_list.balance, "->>,>>>,>>>,>>>,>>9.99")
                    creditlimit = to_decimal(age_list.creditlimit)
                    gastname = age_list.gastname
                    tot_debt = to_decimal(age_list.tot_debt)
                    debt0 = to_decimal(age_list.debt0)
                    debt1 = to_decimal(age_list.debt1)
                    debt2 = to_decimal(age_list.debt2)
                    debt3 = to_decimal(age_list.debt3)
                    ct = ct + 1
                else:
                    tot_debt = to_decimal(tot_debt) + \
                        to_decimal(age_list.tot_debt)
                    debt0 = to_decimal(debt0) + to_decimal(age_list.debt0)
                    debt1 = to_decimal(debt1) + to_decimal(age_list.debt1)
                    debt2 = to_decimal(debt2) + to_decimal(age_list.debt2)
                    debt3 = to_decimal(debt3) + to_decimal(age_list.debt3)
                curr_gastnr = age_list.gastnr
                curr_name = age_list.gastname
                curr_fcurr = age_list.fcurr
                age_list_data.remove(age_list)

            if ct > 0:

                if price_decimal == 0:

                    if not long_digit:
                        arage_list = Arage_list()
                        arage_list_data.append(arage_list)

                        arage_list.number_str = to_string(ct, ">>>9")
                        arage_list.customer_name = gastname
                        arage_list.outstanding = to_string(
                            tot_debt, "->>,>>>,>>>,>>9.99")
                        arage_list.age1 = to_string(
                            debt0, "->>,>>>,>>>,>>9.99")
                        arage_list.age2 = to_string(
                            debt1, "->>,>>>,>>>,>>9.99")
                        arage_list.age3 = to_string(
                            debt2, "->>,>>>,>>>,>>9.99")
                        arage_list.age4 = to_string(
                            debt3, "->>,>>>,>>>,>>9.99")
                        arage_list.curr = curr_fcurr
                        arage_list.gastnr = curr_gastnr

                    else:
                        arage_list = Arage_list()
                        arage_list_data.append(arage_list)

                        arage_list.number_str = to_string(ct, ">>>9")
                        arage_list.customer_name = gastname
                        arage_list.outstanding = to_string(
                            tot_debt, "->>,>>>,>>>,>>>,>>9.99")
                        arage_list.age1 = to_string(
                            debt0, "->>,>>>,>>>,>>>,>>9.99")
                        arage_list.age2 = to_string(
                            debt1, "->>,>>>,>>>,>>>,>>9.99")
                        arage_list.age3 = to_string(
                            debt2, "->>,>>>,>>>,>>>,>>9.99")
                        arage_list.age4 = to_string(
                            debt3, "->>,>>>,>>>,>>>,>>9.99")
                        arage_list.curr = curr_fcurr
                        arage_list.gastnr = curr_gastnr

                else:
                    arage_list = Arage_list()
                    arage_list_data.append(arage_list)

                    arage_list.number_str = to_string(ct, ">>>9")
                    arage_list.customer_name = gastname
                    arage_list.outstanding = to_string(
                        tot_debt, "->>,>>>,>>>,>>>,>>9.99")
                    arage_list.age1 = to_string(
                        debt0, "->>,>>>,>>>,>>>,>>9.99")
                    arage_list.age2 = to_string(
                        debt1, "->>,>>>,>>>,>>>,>>9.99")
                    arage_list.age3 = to_string(
                        debt2, "->>,>>>,>>>,>>>,>>9.99")
                    arage_list.age4 = to_string(
                        debt3, "->>,>>>,>>>,>>>,>>9.99")
                    arage_list.curr = curr_fcurr
                    arage_list.gastnr = curr_gastnr

                arage_list.creditlimit = to_decimal(creditlimit)

                if arage_list.creditlimit != 0:
                    arage_list.balance = to_decimal(
                        arage_list.creditlimit) - to_decimal(tot_debt)
                else:
                    arage_list.balance = to_decimal("0")
                arage_list.creditlimit_str = to_string(
                    arage_list.creditlimit, "->>,>>>,>>>,>>>,>>9.99")
                arage_list.balance_str = to_string(
                    arage_list.balance, "->>,>>>,>>>,>>>,>>9.99")
            tmp_saldo = to_decimal(ledger.tot_debt)

            if tmp_saldo == 0:
                tmp_saldo = to_decimal("1")

            if price_decimal == 0:

                if not long_digit:
                    arage_list = Arage_list()
                    arage_list_data.append(arage_list)

                    arage_list.customer_name = "T o t a l"
                    arage_list.outstanding = to_string(
                        ledger.tot_debt, "->>,>>>,>>>,>>9.99")
                    arage_list.age1 = to_string(
                        ledger.debt0, "->>,>>>,>>>,>>9.99")
                    arage_list.age2 = to_string(
                        ledger.debt1, "->>,>>>,>>>,>>9.99")
                    arage_list.age3 = to_string(
                        ledger.debt2, "->>,>>>,>>>,>>9.99")
                    arage_list.age4 = to_string(
                        ledger.debt3, "->>,>>>,>>>,>>9.99")

                else:
                    arage_list = Arage_list()
                    arage_list_data.append(arage_list)

                    arage_list.customer_name = "T o t a l"
                    arage_list.outstanding = to_string(
                        ledger.tot_debt, "->>,>>>,>>>,>>>,>>9.99")
                    arage_list.age1 = to_string(
                        ledger.debt0, "->>,>>>,>>>,>>>,>>9.99")
                    arage_list.age2 = to_string(
                        ledger.debt1, "->>,>>>,>>>,>>>,>>9.99")
                    arage_list.age3 = to_string(
                        ledger.debt2, "->>,>>>,>>>,>>>,>>9.99")
                    arage_list.age4 = to_string(
                        ledger.debt3, "->>,>>>,>>>,>>>,>>9.99")

            else:
                arage_list = Arage_list()
                arage_list_data.append(arage_list)

                arage_list.customer_name = "T o t a l"
                arage_list.outstanding = to_string(
                    ledger.tot_debt, "->>,>>>,>>>,>>>,>>9.99")
                arage_list.age1 = to_string(
                    ledger.debt0, "->>,>>>,>>>,>>>,>>9.99")
                arage_list.age2 = to_string(
                    ledger.debt1, "->>,>>>,>>>,>>>,>>9.99")
                arage_list.age3 = to_string(
                    ledger.debt2, "->>,>>>,>>>,>>>,>>9.99")
                arage_list.age4 = to_string(
                    ledger.debt3, "->>,>>>,>>>,>>>,>>9.99")

            if not long_digit:
                arage_list = Arage_list()
                arage_list_data.append(arage_list)

                arage_list.customer_name = "Statistic Percentage (%):"
                if tmp_saldo != 0:
                    arage_list.outstanding = to_string(
                        (ledger.tot_debt / tmp_saldo * 100), "->>,>>9.99")
                    arage_list.age1 = to_string(
                        (ledger.debt0 / tmp_saldo * 100), "->>,>>9.99")
                    arage_list.age2 = to_string(
                        (ledger.debt1 / tmp_saldo * 100), "->>,>>9.99")
                    arage_list.age3 = to_string(
                        (ledger.debt2 / tmp_saldo * 100), "->>,>>9.99")
                    arage_list.age4 = to_string(
                        (ledger.debt3 / tmp_saldo * 100), "->>,>>9.99")
                else:
                    arage_list.outstanding = to_string(
                        to_decimal("0"), "->>,>>9.99")
                    arage_list.age1 = to_string(to_decimal("0"), "->>,>>9.99")
                    arage_list.age2 = to_string(to_decimal("0"), "->>,>>9.99")
                    arage_list.age3 = to_string(to_decimal("0"), "->>,>>9.99")
                    arage_list.age4 = to_string(to_decimal("0"), "->>,>>9.99")

            else:
                arage_list = Arage_list()
                arage_list_data.append(arage_list)

                arage_list.customer_name = "Statistic Percentage (%):"
                if tmp_saldo != 0:
                    arage_list.outstanding = to_string(
                        (ledger.tot_debt / tmp_saldo * 100), "->>,>>9.99")
                    arage_list.age1 = to_string(
                        (ledger.debt0 / tmp_saldo * 100), "->>,>>9.99")
                    arage_list.age2 = to_string(
                        (ledger.debt1 / tmp_saldo * 100), "->>,>>9.99")
                    arage_list.age3 = to_string(
                        (ledger.debt2 / tmp_saldo * 100), "->>,>>9.99")
                    arage_list.age4 = to_string(
                        (ledger.debt3 / tmp_saldo * 100), "->>,>>9.99")
                else:
                    arage_list.outstanding = to_string(
                        to_decimal("0"), "->>,>>9.99")
                    arage_list.age1 = to_string(to_decimal("0"), "->>,>>9.99")
                    arage_list.age2 = to_string(to_decimal("0"), "->>,>>9.99")
                    arage_list.age3 = to_string(to_decimal("0"), "->>,>>9.99")
                    arage_list.age4 = to_string(to_decimal("0"), "->>,>>9.99")

            arage_list = Arage_list()
            arage_list_data.append(arage_list)

        arage_list = Arage_list()
        arage_list_data.append(arage_list)

        if price_decimal == 0:

            if not long_digit:
                arage_list = Arage_list()
                arage_list_data.append(arage_list)

                arage_list.customer_name = "T O T A L A/R:"
                arage_list.outstanding = to_string(
                    t_saldo, "->>,>>>,>>>,>>9.99")
                arage_list.age1 = to_string(t_debt0, "->>,>>>,>>>,>>9.99")
                arage_list.age2 = to_string(t_debt1, "->>,>>>,>>>,>>9.99")
                arage_list.age3 = to_string(t_debt2, "->>,>>>,>>>,>>9.99")
                arage_list.age4 = to_string(t_debt3, "->>,>>>,>>>,>>9.99")

            else:
                arage_list = Arage_list()
                arage_list_data.append(arage_list)

                arage_list.customer_name = "T O T A L A/R:"
                arage_list.outstanding = to_string(
                    t_saldo, "->>,>>>,>>>,>>>,>>9.99")
                arage_list.age1 = to_string(t_debt0, "->>,>>>,>>>,>>>,>>9.99")
                arage_list.age2 = to_string(t_debt1, "->>,>>>,>>>,>>>,>>9.99")
                arage_list.age3 = to_string(t_debt2, "->>,>>>,>>>,>>>,>>9.99")
                arage_list.age4 = to_string(t_debt3, "->>,>>>,>>>,>>>,>>9.99")

        else:
            arage_list = Arage_list()
            arage_list_data.append(arage_list)

            arage_list.customer_name = "T O T A L A/R:"
            arage_list.outstanding = to_string(
                t_saldo, "->>,>>>,>>>,>>>,>>9.99")
            arage_list.age1 = to_string(t_debt0, "->>,>>>,>>>,>>>,>>9.99")
            arage_list.age2 = to_string(t_debt1, "->>,>>>,>>>,>>>,>>9.99")
            arage_list.age3 = to_string(t_debt2, "->>,>>>,>>>,>>>,>>9.99")
            arage_list.age4 = to_string(t_debt3, "->>,>>>,>>>,>>>,>>9.99")

        arage_list = Arage_list()
        arage_list_data.append(arage_list)

        if not long_digit:
            arage_list = Arage_list()
            arage_list_data.append(arage_list)

            arage_list.customer_name = "Statistic Percentage (%):"
            arage_list.outstanding = "100.00"
            if t_saldo != 0:
                arage_list.age1 = to_string(
                    (t_debt0 / t_saldo * 100), "->>,>>9.99")
                arage_list.age2 = to_string(
                    (t_debt1 / t_saldo * 100), "->>,>>9.99")
                arage_list.age3 = to_string(
                    (t_debt2 / t_saldo * 100), "->>,>>9.99")
                arage_list.age4 = to_string(
                    (t_debt3 / t_saldo * 100), "->>,>>9.99")
            else:
                arage_list.age1 = to_string(to_decimal("0"), "->>,>>9.99")
                arage_list.age2 = to_string(to_decimal("0"), "->>,>>9.99")
                arage_list.age3 = to_string(to_decimal("0"), "->>,>>9.99")
                arage_list.age4 = to_string(to_decimal("0"), "->>,>>9.99")

        else:
            arage_list = Arage_list()
            arage_list_data.append(arage_list)

            arage_list.customer_name = "Statistic Percentage (%):"
            arage_list.outstanding = "100.00"
            if t_saldo != 0:
                arage_list.age1 = to_string(
                    (t_debt0 / t_saldo * 100), "->>,>>9.99")
                arage_list.age2 = to_string(
                    (t_debt1 / t_saldo * 100), "->>,>>9.99")
                arage_list.age3 = to_string(
                    (t_debt2 / t_saldo * 100), "->>,>>9.99")
                arage_list.age4 = to_string(
                    (t_debt3 / t_saldo * 100), "->>,>>9.99")
            else:
                arage_list.age1 = to_string(to_decimal("0"), "->>,>>9.99")
                arage_list.age2 = to_string(to_decimal("0"), "->>,>>9.99")
                arage_list.age3 = to_string(to_decimal("0"), "->>,>>9.99")
                arage_list.age4 = to_string(to_decimal("0"), "->>,>>9.99")

        arage_list = Arage_list()
        arage_list_data.append(arage_list)

    htparam = get_cache(Htparam, {"paramnr": [(eq, 144)]})
    default_fcurr = htparam.fchar

    htparam = get_cache(Htparam, {"paramnr": [(eq, 330)]})

    if htparam.finteger != 0:
        day1 = htparam.finteger

    htparam = get_cache(Htparam, {"paramnr": [(eq, 331)]})

    if htparam.finteger != 0:
        day2 = htparam.finteger

    htparam = get_cache(Htparam, {"paramnr": [(eq, 332)]})

    if htparam.finteger != 0:
        day3 = htparam.finteger
    day2 = day2 + day1
    day3 = day3 + day2

    htparam = get_cache(Htparam, {"paramnr": [(eq, 491)]})
    price_decimal = htparam.finteger

    htparam = get_cache(Htparam, {"paramnr": [(eq, 246)]})
    long_digit = htparam.flogical

    if substring(to_name, 0, 2) == "zz":
        age_lista()
    else:
        age_list()

    return generate_output()
