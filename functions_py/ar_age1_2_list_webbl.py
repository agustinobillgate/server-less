# using conversion tools version: 1.0.0.117
"""_yusufwijasena_10/12/2025

        remark: - fixed spacing on longstring
                - added substring to gastname & billname to 30 character  
"""
from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Debitor, Htparam, Artikel, Guest, Waehrung, H_bill, Bill, Res_line

from functions import log_program


def ar_age1_2_list_webbl(pvilanguage: int, case_type: int, mtd_flag: bool, to_date: date, fdate: date, tdate: date, from_art: int, to_art: int, from_name: string, to_name: string, disptype: int, mi_bill: bool, day1: int, day2: int, day3: int, detailed: bool, cvt_flag: bool, dollar_rate: Decimal):

    prepare_cache([Debitor, Htparam, Artikel, Guest, Waehrung, Bill, Res_line])

    arage_balance_list_data = []
    curr_art: int = 0
    counter: int = 0
    t_saldo: Decimal = to_decimal("0.0")
    t_prev: Decimal = to_decimal("0.0")
    t_debit: Decimal = to_decimal("0.0")
    t_credit: Decimal = to_decimal("0.0")
    t_debt0: Decimal = to_decimal("0.0")
    t_debt1: Decimal = to_decimal("0.0")
    t_debt2: Decimal = to_decimal("0.0")
    t_debt3: Decimal = to_decimal("0.0")
    tmp_saldo: Decimal = to_decimal("0.0")
    curr_name: string = ""
    curr_gastnr: int = 0
    gastname: string = ""
    billname: string = ""
    p_bal: Decimal = to_decimal("0.0")
    debit: Decimal = to_decimal("0.0")
    credit: Decimal = to_decimal("0.0")
    debt0: Decimal = to_decimal("0.0")
    debt1: Decimal = to_decimal("0.0")
    debt2: Decimal = to_decimal("0.0")
    debt3: Decimal = to_decimal("0.0")
    credit_limit: Decimal = to_decimal("0.0")
    curr_counter: int = 0
    curr_fcurr: string = ""
    i: int = 0
    tot_debt: Decimal = to_decimal("0.0")
    from_date: date = None
    default_fcurr: string = ""
    outlist: string = ""
    long_digit: bool = False
    curr_rgdatum: date = None
    bill_number: int = 0
    inp_gastnr: int = 0
    inp_artnr: int = 0
    tot_debtall: Decimal = to_decimal("0.0")
    tot_debt0: Decimal = to_decimal("0.0")
    tot_debt1: Decimal = to_decimal("0.0")
    tot_debt2: Decimal = to_decimal("0.0")
    tot_debt3: Decimal = to_decimal("0.0")
    curr_time: int = 0
    ar_ledger: int = 0
    lvcarea: string = "ar-age1"
    bill_name: string = ""
    debitor = htparam = artikel = guest = waehrung = h_bill = bill = res_line = None

    arage_balance_list = arage_list = age_list = tage_list = ledger = debtrec = debt = None

    arage_balance_list_data, Arage_balance_list = create_model(
        "Arage_balance_list",
        {
            "strdate": string,
            "curr": string,
            "gastnr": int,
            "artnr": int,
            "age1": string,
            "age2": string,
            "age3": string,
            "age4": string,
            "rechnr": string,
            "num": string,
            "cust_nm": string,
            "bill_nm": string,
            "p_bal": string,
            "debit": string,
            "credit": string,
            "end_bal": string,
            "creditlimit_str": string
        })
    arage_list_data, Arage_list = create_model(
        "Arage_list",
        {
            "strdate": string,
            "curr": string,
            "gastnr": int,
            "artnr": int,
            "age1": string,
            "age2": string,
            "age3": string,
            "age4": string,
            "rechnr": string,
            "str": string
        })
    age_list_data, Age_list = create_model(
        "Age_list",
        {
            "fcurr": string,
            "artnr": int,
            "rechnr": int,
            "counter": int,
            "gastnr": int,
            "rgdatum": date,
            "gastname": string,
            "billname": string,
            "p_bal": Decimal,
            "debit": Decimal,
            "credit": Decimal,
            "saldo": Decimal,
            "debt0": Decimal,
            "debt1": Decimal,
            "debt2": Decimal,
            "debt3": Decimal,
            "tot_debt": Decimal,
            "opart": int,
            "credit_limit": Decimal
        })
    tage_list_data, Tage_list = create_model_like(Age_list)
    ledger_data, Ledger = create_model(
        "Ledger",
        {
            "artnr": int,
            "bezeich": string,
            "p_bal": Decimal,
            "debit": Decimal,
            "credit": Decimal,
            "debt0": Decimal,
            "debt1": Decimal,
            "debt2": Decimal,
            "debt3": Decimal,
            "tot_debt": Decimal
        })

    Debtrec = create_buffer("Debtrec", Debitor)
    Debt = create_buffer("Debt", Debitor)

    set_cache(
        Artikel, ((Artikel.artart == 2) | (Artikel.artart == 7)) & (Artikel.artnr >= from_art) & (Artikel.artnr <= to_art) & (Artikel.departement == 0), [["artnr", "departement"]], True, [], ["artnr"])
    set_cache(
        Debitor, (Debitor.rechnr > 0) & (Debitor.rgdatum <= to_date) & (((Debitor.artnr >= from_art) & (Debitor.artnr <= to_art) & (Debitor.opart <= 1)) | (Debitor.artnr.in_(get_cache_value_list(Artikel, "artnr")) & ((Debitor.opart == 2) & (Debitor.zahlkonto == 0)))), [], True, [], ["rechnr"])
    set_cache(
        H_bill, (H_bill.rechnr.in_(get_cache_value_list(Debitor, "rechnr"))), [["rechnr"]], True, [], [])
    set_cache(
        Bill, (Bill.rechnr.in_(get_cache_value_list(Debitor, "rechnr"))), [["rechnr"]], True, [], ["resnr"])
    set_cache(
        Res_line, (Res_line.resnr.in_(get_cache_value_list(Bill, "resnr"))), [["resnr"]], True, [], [])

    db_session = local_storage.db_session

    def generate_output():
        nonlocal arage_balance_list_data, curr_art, counter, t_saldo, t_prev, t_debit, t_credit, t_debt0, t_debt1, t_debt2, t_debt3, tmp_saldo, curr_name, curr_gastnr, gastname, billname, p_bal, debit, credit, debt0, debt1, debt2, debt3, credit_limit, curr_counter, curr_fcurr, i, tot_debt, from_date, default_fcurr, outlist, long_digit, curr_rgdatum, bill_number, inp_gastnr, inp_artnr, tot_debtall, tot_debt0, tot_debt1, tot_debt2, tot_debt3, curr_time, ar_ledger, lvcarea, bill_name, debitor, htparam, artikel, guest, waehrung, h_bill, bill, res_line
        nonlocal pvilanguage, case_type, mtd_flag, to_date, fdate, tdate, from_art, to_art, from_name, to_name, disptype, mi_bill, day1, day2, day3, detailed, cvt_flag, dollar_rate
        nonlocal debtrec, debt
        nonlocal arage_balance_list, arage_list, age_list, tage_list, ledger, debtrec, debt
        nonlocal arage_balance_list_data, arage_list_data, age_list_data, tage_list_data, ledger_data

        return {
            "arage-balance-list": arage_balance_list_data
        }

    def create_output():
        nonlocal arage_balance_list_data, curr_art, counter, t_saldo, t_prev, t_debit, t_credit, t_debt0, t_debt1, t_debt2, t_debt3, tmp_saldo, curr_name, curr_gastnr, gastname, billname, p_bal, debit, credit, debt0, debt1, debt2, debt3, credit_limit, curr_counter, curr_fcurr, i, tot_debt, from_date, default_fcurr, outlist, long_digit, curr_rgdatum, bill_number, inp_gastnr, inp_artnr, tot_debtall, tot_debt0, tot_debt1, tot_debt2, tot_debt3, curr_time, ar_ledger, lvcarea, bill_name, debitor, htparam, artikel, guest, waehrung, h_bill, bill, res_line
        nonlocal pvilanguage, case_type, mtd_flag, to_date, fdate, tdate, from_art, to_art, from_name, to_name, disptype, mi_bill, day1, day2, day3, detailed, cvt_flag, dollar_rate
        nonlocal debtrec, debt
        nonlocal arage_balance_list, arage_list, age_list, tage_list, ledger, debtrec, debt
        nonlocal arage_balance_list_data, arage_list_data, age_list_data, tage_list_data, ledger_data

        num_day: int = 0
        num_day = (to_date - age_list.rgdatum).days

        if num_day > day3:
            age_list.debt3 = to_decimal(age_list.tot_debt)

        elif num_day > day2:
            age_list.debt2 = to_decimal(age_list.tot_debt)

        elif num_day > day1:
            age_list.debt1 = to_decimal(age_list.tot_debt)
        else:
            age_list.debt0 = to_decimal(age_list.tot_debt)

        ledger.tot_debt = to_decimal(
            ledger.tot_debt) + to_decimal(age_list.tot_debt)
        ledger.p_bal = to_decimal(ledger.p_bal) + to_decimal(age_list.p_bal)
        ledger.debit = to_decimal(ledger.debit) + to_decimal(age_list.debit)
        ledger.credit = to_decimal(ledger.credit) + to_decimal(age_list.credit)
        ledger.debt0 = to_decimal(ledger.debt0) + to_decimal(age_list.debt0)
        ledger.debt1 = to_decimal(ledger.debt1) + to_decimal(age_list.debt1)
        ledger.debt2 = to_decimal(ledger.debt2) + to_decimal(age_list.debt2)
        ledger.debt3 = to_decimal(ledger.debt3) + to_decimal(age_list.debt3)
        t_saldo = to_decimal(t_saldo) + to_decimal(age_list.tot_debt)
        t_prev = to_decimal(t_prev) + to_decimal(age_list.p_bal)
        t_debit = to_decimal(t_debit) + to_decimal(age_list.debit)
        t_credit = to_decimal(t_credit) + to_decimal(age_list.credit)
        t_debt0 = to_decimal(t_debt0) + to_decimal(age_list.debt0)
        t_debt1 = to_decimal(t_debt1) + to_decimal(age_list.debt1)
        t_debt2 = to_decimal(t_debt2) + to_decimal(age_list.debt2)
        t_debt3 = to_decimal(t_debt3) + to_decimal(age_list.debt3)

        if curr_gastnr == 0:
            curr_rgdatum = age_list.rgdatum
            bill_number = age_list.rechnr
            inp_gastnr = age_list.gastnr
            inp_artnr = age_list.artnr
            gastname = substring(age_list.gastname, 0, 30)
            billname = substring(age_list.billname, 0, 30)
            tot_debt = to_decimal(age_list.tot_debt)
            p_bal = to_decimal(age_list.p_bal)
            debit = to_decimal(age_list.debit)
            credit = to_decimal(age_list.credit)
            debt0 = to_decimal(age_list.debt0)
            debt1 = to_decimal(age_list.debt1)
            debt2 = to_decimal(age_list.debt2)
            debt3 = to_decimal(age_list.debt3)
            counter = counter + 1
            credit_limit = to_decimal(age_list.credit_limit)

        elif curr_name != age_list.gastname:
            if p_bal != 0 or debit != 0 or credit != 0:
                if not long_digit:
                    outlist = "  " + to_string(counter, ">>>9 ") + \
                        to_string(gastname, "x(30)") + \
                        to_string(billname, "x(30)") + \
                        to_string(tot_debt, "->>,>>>,>>>,>>9.99") + \
                        to_string(p_bal, "->>,>>>,>>>,>>9.99") + \
                        to_string(debit, "->>,>>>,>>>,>>9.99") + \
                        to_string(credit, "->>,>>>,>>>,>>9.99") + \
                        to_string(debt0, "->>,>>>,>>>,>>9.99") + \
                        to_string(debt1, "->>,>>>,>>>,>>9.99") + \
                        to_string(debt2, "->>,>>>,>>>,>>9.99") + \
                        to_string(debt3, "->>,>>>,>>>,>>9.99") + \
                        to_string(credit_limit, "->>,>>>,>>>,>>9.99")
                else:
                    outlist = "  " + to_string(counter, ">>>9 ") + \
                        to_string(gastname, "x(30)") + \
                        to_string(billname, "x(30)") + \
                        to_string(tot_debt, "->,>>>,>>>,>>>,>>9") + \
                        to_string(p_bal, "->,>>>,>>>,>>>,>>9") + \
                        to_string(debit, "->,>>>,>>>,>>>,>>9") + \
                        to_string(credit, "->,>>>,>>>,>>>,>>9") + \
                        to_string(debt0, "->,>>>,>>>,>>>,>>9") + \
                        to_string(debt1, "->,>>>,>>>,>>>,>>9") + \
                        to_string(debt2, "->,>>>,>>>,>>>,>>9") + \
                        to_string(debt3, "->,>>>,>>>,>>>,>>9") + \
                        to_string(credit_limit, "->,>>>,>>>,>>>,>>9")

                fill_in_list(True, age_list.fcurr, curr_rgdatum)
            else:
                counter = counter - 1
            curr_rgdatum = age_list.rgdatum
            bill_number = age_list.rechnr
            inp_gastnr = age_list.gastnr
            inp_artnr = age_list.artnr
            gastname = substring(age_list.gastname, 0, 30)
            billname = substring(age_list.billname, 0, 30)
            tot_debt = to_decimal(age_list.tot_debt)
            p_bal = to_decimal(age_list.p_bal)
            debit = to_decimal(age_list.debit)
            credit = to_decimal(age_list.credit)
            debt0 = to_decimal(age_list.debt0)
            debt1 = to_decimal(age_list.debt1)
            debt2 = to_decimal(age_list.debt2)
            debt3 = to_decimal(age_list.debt3)
            credit_limit = to_decimal(age_list.credit_limit)
            counter = counter + 1
        else:
            tot_debt = to_decimal(tot_debt) + to_decimal(age_list.tot_debt)
            p_bal = to_decimal(p_bal) + to_decimal(age_list.p_bal)
            debit = to_decimal(debit) + to_decimal(age_list.debit)
            credit = to_decimal(credit) + to_decimal(age_list.credit)
            debt0 = to_decimal(debt0) + to_decimal(age_list.debt0)
            debt1 = to_decimal(debt1) + to_decimal(age_list.debt1)
            debt2 = to_decimal(debt2) + to_decimal(age_list.debt2)
            debt3 = to_decimal(debt3) + to_decimal(age_list.debt3)

        curr_gastnr = age_list.gastnr
        curr_fcurr = age_list.fcurr

        if not detailed:
            curr_name = age_list.gastname
        age_list_data.remove(age_list)

    def fill_in_list(fill_billno: bool, currency: string, curr_rgdatum: date):
        nonlocal arage_balance_list_data, curr_art, counter, t_saldo, t_prev, t_debit, t_credit, t_debt0, t_debt1, t_debt2, t_debt3, tmp_saldo, curr_name, curr_gastnr, gastname, billname, p_bal, debit, credit, debt0, debt1, debt2, debt3, credit_limit, curr_counter, curr_fcurr, i, tot_debt, from_date, default_fcurr, outlist, long_digit, bill_number, inp_gastnr, inp_artnr, tot_debtall, tot_debt0, tot_debt1, tot_debt2, tot_debt3, curr_time, ar_ledger, lvcarea, bill_name, debitor, htparam, artikel, guest, waehrung, h_bill, bill, res_line
        nonlocal pvilanguage, case_type, mtd_flag, to_date, fdate, tdate, from_art, to_art, from_name, to_name, disptype, mi_bill, day1, day2, day3, detailed, cvt_flag, dollar_rate
        nonlocal debtrec, debt
        nonlocal arage_balance_list, arage_list, age_list, tage_list, ledger, debtrec, debt
        nonlocal arage_balance_list_data, arage_list_data, age_list_data, tage_list_data, ledger_data

        arage_list = Arage_list()
        arage_list_data.append(arage_list)

        if fill_billno:
            arage_list.rechnr = to_string(bill_number, ">>>>>>>>>")
            arage_list.gastnr = inp_gastnr
            arage_list.artnr = inp_artnr

            if curr_rgdatum != None:
                arage_list.strdate = to_string(curr_rgdatum, "99/99/99")
        arage_list.str = outlist

        if substring(outlist, 0, 5) == ("-----"):
            arage_list.rechnr = "---------"
            arage_list.strdate = "--------"

        arage_list.age1 = substring(arage_list.str, 139, 18)
        arage_list.age2 = substring(arage_list.str, 156, 18)
        arage_list.age3 = substring(arage_list.str, 171, 18)
        arage_list.age4 = substring(arage_list.str, 187, 18)
        arage_list.curr = currency

    def age_list1():
        nonlocal arage_balance_list_data, curr_art, counter, t_saldo, t_prev, t_debit, t_credit, t_debt0, t_debt1, t_debt2, t_debt3, tmp_saldo, curr_name, curr_gastnr, gastname, billname, p_bal, debit, credit, debt0, debt1, debt2, debt3, credit_limit, curr_counter, curr_fcurr, i, tot_debt, from_date, default_fcurr, outlist, long_digit, curr_rgdatum, bill_number, inp_gastnr, inp_artnr, tot_debtall, tot_debt0, tot_debt1, tot_debt2, tot_debt3, curr_time, ar_ledger, lvcarea, bill_name, debitor, htparam, artikel, guest, waehrung, h_bill, bill, res_line
        nonlocal pvilanguage, case_type, mtd_flag, to_date, fdate, tdate, from_art, to_art, from_name, to_name, disptype, mi_bill, day1, day2, day3, detailed, cvt_flag, dollar_rate
        nonlocal debtrec, debt
        nonlocal arage_balance_list, arage_list, age_list, tage_list, ledger, debtrec, debt
        nonlocal arage_balance_list_data, arage_list_data, age_list_data, tage_list_data, ledger_data

        curr_art = 0
        counter = 0
        t_saldo = to_decimal("0")
        t_prev = to_decimal("0")
        t_debit = to_decimal("0")
        t_credit = to_decimal("0")
        t_debt0 = to_decimal("0")
        t_debt1 = to_decimal("0")
        t_debt2 = to_decimal("0")
        t_debt3 = to_decimal("0")
        tmp_saldo = to_decimal("0")
        curr_name = ""
        curr_gastnr = 0
        gastname = ""
        billname = ""
        p_bal = to_decimal("0")
        debit = to_decimal("0")
        credit = to_decimal("0")
        debt0 = to_decimal("0")
        debt1 = to_decimal("0")
        debt2 = to_decimal("0")
        debt3 = to_decimal("0")
        tot_debt = to_decimal("0")
        i = 0
        curr_counter = 0
        curr_fcurr = ""

        from_date = date_mdy(get_month(to_date), 1, get_year(to_date))

        for artikel in db_session.query(Artikel).filter(
                ((Artikel.artart == 2) | (Artikel.artart == 7) | (Artikel.artart == 14)) & (Artikel.artnr >= from_art) & (Artikel.artnr <= to_art) & (Artikel.departement == 0)).order_by(Artikel.artart, Artikel.artnr).all():
            ledger = Ledger()
            ledger_data.append(ledger)

            ledger.artnr = artikel.artnr
            ledger.bezeich = to_string(
                artikel.artnr) + "  -  " + artikel.bezeich
        curr_art = 0

        for debitor in db_session.query(Debitor).filter(
                (Debitor.rgdatum <= to_date) & (Debitor.artnr >= from_art) & (Debitor.artnr <= to_art) & (Debitor.opart <= 1)).order_by(Debitor.artnr, Debitor.zahlkonto).all():

            if debitor.name.lower() >= (from_name).lower():
                if curr_art != debitor.artnr:
                    curr_art = debitor.artnr

                    artikel = get_cache(
                        Artikel, {"artnr": [(eq, curr_art)], "departement": [(eq, 0)]})

                if debitor.counter > 0:
                    age_list = query(age_list_data, filters=(
                        lambda age_list: age_list.counter == debitor.counter), first=True)

                if (debitor.counter == 0) or (not age_list):
                    guest = get_cache(
                        Guest, {"gastnr": [(eq, debitor.gastnr)]})
                    age_list = Age_list()
                    age_list_data.append(age_list)

                    age_list.artnr = debitor.artnr
                    age_list.rechnr = debitor.rechnr
                    age_list.rgdatum = debitor.rgdatum
                    age_list.counter = debitor.counter
                    age_list.gastnr = debitor.gastnr
                    age_list.tot_debt = to_decimal("0")
                    age_list.opart = debitor.opart

                    if guest:
                        age_list.credit_limit = to_decimal(guest.kreditlimit)

                    if debitor.betrieb_gastmem == 0:
                        age_list.fcurr = default_fcurr
                    else:
                        waehrung = get_cache(
                            Waehrung, {"waehrungsnr": [(eq, debitor.betrieb_gastmem)]})

                        if waehrung:
                            age_list.fcurr = waehrung.wabkurz

                    if artikel.artart == 2:
                        get_bill_receiver_and_bill_name(debitor.rechnr)
                    else:
                        get_bill_receiver_and_bill_name(debitor.rechnr)

                if disptype == 0:
                    age_list.tot_debt = to_decimal(
                        age_list.tot_debt) + to_decimal(debitor.saldo)
                else:
                    if not cvt_flag:
                        age_list.tot_debt = to_decimal(
                            age_list.tot_debt) + to_decimal(debitor.vesrdep)
                    else:
                        if age_list.fcurr.lower() == (default_fcurr).lower():
                            if debitor.vesrdep != 0:
                                age_list.tot_debt = to_decimal(
                                    age_list.tot_debt) + to_decimal(debitor.vesrdep)

                            else:
                                age_list.tot_debt = to_decimal(
                                    age_list.tot_debt) + to_decimal((debitor.saldo) / to_decimal(dollar_rate))
                        else:
                            age_list.tot_debt = to_decimal(
                                age_list.tot_debt) + to_decimal((debitor.saldo) / to_decimal(dollar_rate))

                if debitor.rgdatum < from_date and debitor.zahlkonto == 0:
                    if disptype == 0:
                        age_list.p_bal = to_decimal(
                            age_list.p_bal) + to_decimal(debitor.saldo)
                    else:
                        if not cvt_flag:
                            age_list.p_bal = to_decimal(
                                age_list.p_bal) + to_decimal(debitor.vesrdep)
                        else:
                            if age_list.fcurr.lower() == (default_fcurr).lower():
                                if debitor.vesrdep != 0:
                                    age_list.p_bal = to_decimal(
                                        age_list.p_bal) + to_decimal(debitor.vesrdep)

                                else:
                                    age_list.p_bal = to_decimal(
                                        age_list.p_bal) + to_decimal((debitor.saldo) / to_decimal(dollar_rate))
                            else:
                                age_list.p_bal = to_decimal(
                                    age_list.p_bal) + to_decimal((debitor.saldo) / to_decimal(dollar_rate))

                if debitor.rgdatum >= from_date and debitor.zahlkonto == 0:
                    if disptype == 0:
                        age_list.debit = to_decimal(
                            age_list.debit) + to_decimal(debitor.saldo)
                    else:
                        if not cvt_flag:
                            age_list.debit = to_decimal(
                                age_list.debit) + to_decimal(debitor.vesrdep)
                        else:
                            if age_list.fcurr.lower() == (default_fcurr).lower():

                                if debitor.vesrdep != 0:
                                    age_list.debit = to_decimal(
                                        age_list.debit) + to_decimal(debitor.vesrdep)

                                else:
                                    age_list.debit = to_decimal(
                                        age_list.debit) + to_decimal((debitor.saldo) / to_decimal(dollar_rate))
                            else:
                                age_list.debit = to_decimal(
                                    age_list.debit) + to_decimal((debitor.saldo) / to_decimal(dollar_rate))

                if debitor.rgdatum < from_date and debitor.zahlkonto != 0:

                    if disptype == 0:
                        age_list.p_bal = to_decimal(
                            age_list.p_bal) + to_decimal(debitor.saldo)
                    else:

                        if not cvt_flag:
                            age_list.p_bal = to_decimal(
                                age_list.p_bal) + to_decimal(debitor.vesrdep)
                        else:

                            if age_list.fcurr.lower() == (default_fcurr).lower():

                                if debitor.vesrdep != 0:
                                    age_list.p_bal = to_decimal(
                                        age_list.p_bal) + to_decimal(debitor.vesrdep)

                                else:
                                    age_list.p_bal = to_decimal(
                                        age_list.p_bal) + to_decimal((debitor.saldo) / to_decimal(dollar_rate))
                            else:
                                age_list.p_bal = to_decimal(
                                    age_list.p_bal) + to_decimal((debitor.saldo) / to_decimal(dollar_rate))
                else:

                    if debitor.rgdatum >= from_date and debitor.zahlkonto != 0:

                        if disptype == 0:
                            age_list.credit = to_decimal(
                                age_list.credit) - to_decimal(debitor.saldo)
                        else:

                            if not cvt_flag:
                                age_list.credit = to_decimal(
                                    age_list.credit) - to_decimal(debitor.vesrdep)
                            else:

                                if age_list.fcurr.lower() == (default_fcurr).lower():

                                    if debitor.vesrdep != 0:
                                        age_list.credit = to_decimal(
                                            age_list.credit) - to_decimal(debitor.vesrdep)

                                    else:
                                        age_list.credit = to_decimal(
                                            age_list.credit) - to_decimal((debitor.saldo) / to_decimal(dollar_rate))
                                else:
                                    age_list.credit = to_decimal(
                                        age_list.credit) - to_decimal((debitor.saldo) / to_decimal(dollar_rate))

        debitor_obj_list = {}
        debitor = Debitor()
        artikel = Artikel()
        for debitor.artnr, debitor.counter, debitor.gastnr, debitor.rechnr, debitor.rgdatum, debitor.opart, debitor.betrieb_gastmem, debitor.saldo, debitor.vesrdep, debitor.zahlkonto, debitor.gastnrmember, debitor.name, debitor._recid, artikel.artnr, artikel.bezeich, artikel.artart, artikel._recid in db_session.query(Debitor.artnr, Debitor.counter, Debitor.gastnr, Debitor.rechnr, Debitor.rgdatum, Debitor.opart, Debitor.betrieb_gastmem, Debitor.saldo, Debitor.vesrdep, Debitor.zahlkonto, Debitor.gastnrmember, Debitor.name, Debitor._recid, Artikel.artnr, Artikel.bezeich, Artikel.artart, Artikel._recid).join(Artikel, ((Artikel.artart == 2) | (Artikel.artart == 7)) & (Artikel.artnr == Debitor.artnr) & (Artikel.departement == 0)).filter(
                (Debitor.artnr >= from_art) & (Debitor.artnr <= to_art) & (Debitor.rgdatum <= to_date) & (Debitor.opart == 2)).order_by(Debitor.rechnr, Debitor.counter, Debitor._recid).all():

            if debitor_obj_list.get(debitor._recid):
                continue
            else:
                debitor_obj_list[debitor._recid] = True

            if debitor.zahlkonto == 0:

                if debitor.name.lower() >= (from_name).lower():

                    guest = get_cache(
                        Guest, {"gastnr": [(eq, debitor.gastnr)]})

                    age_list = query(age_list_data, filters=(lambda age_list: age_list.rechnr ==
                                     debitor.rechnr and age_list.counter == debitor.counter), first=True)

                    if not age_list:
                        age_list = Age_list()
                        age_list_data.append(age_list)

                        age_list.artnr = debitor.artnr
                        age_list.rechnr = debitor.rechnr
                        age_list.rgdatum = debitor.rgdatum
                        age_list.counter = debitor.counter
                        age_list.gastnr = debitor.gastnr
                        age_list.tot_debt = to_decimal(debitor.saldo)
                        age_list.opart = debitor.opart

                        if guest:
                            age_list.credit_limit = to_decimal(
                                guest.kreditlimit)

                        if debitor.betrieb_gastmem == 0:
                            age_list.fcurr = default_fcurr
                        else:

                            waehrung = get_cache(
                                Waehrung, {"waehrungsnr": [(eq, debitor.betrieb_gastmem)]})

                            if waehrung:
                                age_list.fcurr = waehrung.wabkurz

                        if artikel.artart == 2:
                            get_bill_receiver_and_bill_name(debitor.rechnr)
                        else:
                            get_bill_receiver_and_bill_name(debitor.rechnr)

                    if debitor.rgdatum < from_date:

                        if disptype == 0:
                            age_list.p_bal = to_decimal(
                                age_list.p_bal) + to_decimal(debitor.saldo)
                        else:

                            if not cvt_flag:
                                age_list.p_bal = to_decimal(
                                    age_list.p_bal) + to_decimal(debitor.vesrdep)
                            else:

                                if age_list.fcurr.lower() == (default_fcurr).lower():

                                    if debitor.vesrdep != 0:
                                        age_list.p_bal = to_decimal(
                                            age_list.p_bal) + to_decimal(debitor.vesrdep)

                                    else:
                                        age_list.p_bal = to_decimal(
                                            age_list.p_bal) + to_decimal((debitor.saldo) / to_decimal(dollar_rate))
                                else:
                                    age_list.p_bal = to_decimal(
                                        age_list.p_bal) + to_decimal((debitor.saldo) / to_decimal(dollar_rate))

                    elif debitor.rgdatum >= from_date:

                        if disptype == 0:
                            age_list.debit = to_decimal(
                                age_list.debit) + to_decimal(debitor.saldo)
                        else:

                            if not cvt_flag:
                                age_list.debit = to_decimal(
                                    age_list.debit) + to_decimal(debitor.vesrdep)
                            else:

                                if age_list.fcurr.lower() == (default_fcurr).lower():

                                    if debitor.vesrdep != 0:
                                        age_list.debit = to_decimal(
                                            age_list.debit) + to_decimal(debitor.vesrdep)

                                    else:
                                        age_list.debit = to_decimal(
                                            age_list.debit) + to_decimal((debitor.saldo) / to_decimal(dollar_rate))
                                else:
                                    age_list.debit = to_decimal(
                                        age_list.debit) + to_decimal((debitor.saldo) / to_decimal(dollar_rate))

            if debitor.zahlkonto > 0 and debitor.rgdatum <= to_date:
                age_list.tot_debt = to_decimal(
                    age_list.tot_debt) + to_decimal(debitor.saldo)

                if debitor.rgdatum < from_date:

                    if disptype == 0:
                        age_list.p_bal = to_decimal(
                            age_list.p_bal) + to_decimal(debitor.saldo)
                    else:

                        if not cvt_flag:
                            age_list.p_bal = to_decimal(
                                age_list.p_bal) + to_decimal(debitor.vesrdep)
                        else:

                            if age_list.fcurr.lower() == (default_fcurr).lower():
                                age_list.p_bal = to_decimal(
                                    age_list.p_bal) + to_decimal(debitor.vesrdep)
                            else:
                                age_list.p_bal = to_decimal(
                                    age_list.p_bal) + to_decimal((debitor.saldo) / to_decimal(dollar_rate))

                elif debitor.rgdatum >= from_date:

                    if disptype == 0:
                        age_list.credit = to_decimal(
                            age_list.credit) - to_decimal(debitor.saldo)
                    else:

                        if not cvt_flag:
                            age_list.credit = to_decimal(
                                age_list.credit) - to_decimal(debitor.vesrdep)
                        else:

                            if age_list.fcurr.lower() == (default_fcurr).lower():
                                if debitor.vesrdep != 0:
                                    age_list.credit = to_decimal(
                                        age_list.credit) - to_decimal(debitor.vesrdep)

                                else:
                                    age_list.credit = to_decimal(
                                        age_list.credit) - to_decimal((debitor.saldo) / to_decimal(dollar_rate))
                            else:
                                age_list.credit = to_decimal(
                                    age_list.credit) - to_decimal((debitor.saldo) / to_decimal(dollar_rate))

        for age_list in query(age_list_data):

            if age_list.p_bal >= - 1 and age_list.p_bal <= 1 and age_list.debit == 0 and age_list.credit == 0:
                age_list_data.remove(age_list)

        if ar_ledger != 0:

            for age_list in query(age_list_data, filters=(lambda age_list: age_list.artnr == ar_ledger)):

                tage_list = query(tage_list_data, filters=(
                    lambda tage_list: tage_list.rechnr == age_list.rechnr), first=True)

                if not tage_list:
                    tage_list = Tage_list()
                    tage_list_data.append(tage_list)

                    buffer_copy(age_list, tage_list)
                else:
                    tage_list.p_bal = to_decimal(
                        tage_list.p_bal) + to_decimal(age_list.p_bal)
                    tage_list.debit = to_decimal(
                        tage_list.debit) + to_decimal(age_list.debit)
                    tage_list.credit = to_decimal(
                        tage_list.credit) + to_decimal(age_list.credit)
                    tage_list.saldo = to_decimal(
                        tage_list.saldo) + to_decimal(age_list.saldo)
                    tage_list.debt0 = to_decimal(
                        tage_list.debt0) + to_decimal(age_list.debt0)
                    tage_list.debt1 = to_decimal(
                        tage_list.debt1) + to_decimal(age_list.debt1)
                    tage_list.debt2 = to_decimal(
                        tage_list.debt2) + to_decimal(age_list.debt2)
                    tage_list.debt3 = to_decimal(
                        tage_list.debt3) + to_decimal(age_list.debt3)
                    tage_list.tot_debt = to_decimal(
                        tage_list.tot_debt) + to_decimal(age_list.tot_debt)

                age_list_data.remove(age_list)

            for tage_list in query(tage_list_data):
                age_list = Age_list()
                age_list_data.append(age_list)

                buffer_copy(tage_list, age_list)
                tage_list_data.remove(tage_list)

        for ledger in query(ledger_data, sort_by=[("artnr", False)]):

            age_list = query(age_list_data, filters=(
                lambda age_list: age_list.artnr == ledger.artnr), first=True)

            if not age_list:
                continue
            outlist = "      " + ledger.bezeich.upper()
            # print(f"[LOG] ledger.bezeich: {outlist}")
            fill_in_list(False, "", None)
            outlist = ""
            fill_in_list(False, "", None)
            counter = 0
            curr_gastnr = 0

            if mi_bill:

                for age_list in query(age_list_data, filters=(lambda age_list: age_list.artnr == ledger.artnr), sort_by=[("rgdatum", False), ("gastname", False), ("rechnr", False)]):
                    create_output()

            else:

                for age_list in query(age_list_data, filters=(lambda age_list: age_list.artnr == ledger.artnr), sort_by=[("gastname", False), ("rechnr", False)]):
                    create_output()

            if counter > 0 and (p_bal != 0 or debit != 0 or credit != 0):

                if not long_digit:
                    outlist = "  " + to_string(counter, ">>>9 ") + \
                        to_string(gastname, "x(30)") + \
                        to_string(billname, "x(30)") + \
                        to_string(tot_debt, "->>,>>>,>>>,>>9.99") + \
                        to_string(p_bal, "->>,>>>,>>>,>>9.99") + \
                        to_string(debit, "->>,>>>,>>>,>>9.99") + \
                        to_string(credit, "->>,>>>,>>>,>>9.99") + \
                        to_string(debt0, "->>,>>>,>>>,>>9.99") + \
                        to_string(debt1, "->>,>>>,>>>,>>9.99") + \
                        to_string(debt2, "->>,>>>,>>>,>>9.99") + \
                        to_string(debt3, "->>,>>>,>>>,>>9.99") + \
                        to_string(credit_limit, "->>,>>>,>>>,>>9.99")
                else:
                    outlist = "  " + to_string(counter, ">>>9 ") + \
                        to_string(gastname, "x(30)") + \
                        to_string(billname, "x(30)") + \
                        to_string(tot_debt, "->,>>>,>>>,>>>,>>9") + \
                        to_string(p_bal, "->,>>>,>>>,>>>,>>9") + \
                        to_string(debit, "->,>>>,>>>,>>>,>>9") + \
                        to_string(credit, "->,>>>,>>>,>>>,>>9") + \
                        to_string(debt0, "->,>>>,>>>,>>>,>>9") + \
                        to_string(debt1, "->,>>>,>>>,>>>,>>9") + \
                        to_string(debt2, "->,>>>,>>>,>>>,>>9") + \
                        to_string(debt3, "->,>>>,>>>,>>>,>>9") + \
                        to_string(credit_limit, "->,>>>,>>>,>>>,>>9")
                fill_in_list(True, curr_fcurr, curr_rgdatum)
            else:
                counter = counter - 1
            tmp_saldo = to_decimal(ledger.tot_debt)

            if tmp_saldo == 0:
                tmp_saldo = to_decimal("1")
            outlist = "-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------"
            fill_in_list(False, "----", None)

            if not long_digit:
                outlist = "       " + \
                    to_string(translateExtended("T o t a l", lvcarea, ""), "x(30)") + \
                    to_string(translateExtended("T o t a l", lvcarea, ""), "x(30)") +\
                    to_string(ledger.tot_debt, "->>,>>>,>>>,>>9.99") + \
                    to_string(ledger.p_bal, "->>,>>>,>>>,>>9.99") + \
                    to_string(ledger.debit, "->>,>>>,>>>,>>9.99") + \
                    to_string(ledger.credit, "->>,>>>,>>>,>>9.99") + \
                    to_string(ledger.debt0, "->>,>>>,>>>,>>9.99") + \
                    to_string(ledger.debt1, "->>,>>>,>>>,>>9.99") + \
                    to_string(ledger.debt2, "->>,>>>,>>>,>>9.99") + \
                    to_string(ledger.debt3, "->>,>>>,>>>,>>9.99")
            else:
                outlist = "       " + \
                    to_string(translateExtended("T o t a l", lvcarea, ""), "x(30)") + \
                    to_string(translateExtended("T o t a l", lvcarea, ""), "x(30)") + \
                    to_string(ledger.tot_debt, "->,>>>,>>>,>>>,>>9") + \
                    to_string(ledger.p_bal, "->,>>>,>>>,>>>,>>9") + \
                    to_string(ledger.debit, "->,>>>,>>>,>>>,>>9") + \
                    to_string(ledger.credit, "->,>>>,>>>,>>>,>>9") + \
                    to_string(ledger.debt0, "->,>>>,>>>,>>>,>>9") + \
                    to_string(ledger.debt1, "->,>>>,>>>,>>>,>>9") + \
                    to_string(ledger.debt2, "->,>>>,>>>,>>>,>>9") + \
                    to_string(ledger.debt3, "->,>>>,>>>,>>>,>>9")
            fill_in_list(False, "", None)
            outlist = "       " + \
                to_string(translateExtended("Statistic Percentage (%) :", lvcarea, ""), "x(30)") + \
                to_string(translateExtended("Statistic Percentage (%) :", lvcarea, ""), "x(30)") + \
                "            100.00"
            for i in range(1, 55):
                outlist = outlist + "       "
            tot_debt0 = (to_decimal(ledger.debt0) /
                         to_decimal(tmp_saldo) * to_decimal("100"))
            tot_debt1 = (to_decimal(ledger.debt1) /
                         to_decimal(tmp_saldo) * to_decimal("100"))
            tot_debt2 = (to_decimal(ledger.debt2) /
                         to_decimal(tmp_saldo) * to_decimal("100"))
            tot_debt3 = (to_decimal(ledger.debt3) /
                         to_decimal(tmp_saldo) * to_decimal("100"))

            if tot_debt0 == None:
                tot_debt0 = to_decimal("0")

            if tot_debt1 == None:
                tot_debt1 = to_decimal("0")

            if tot_debt2 == None:
                tot_debt2 = to_decimal("0")

            if tot_debt3 == None:
                tot_debt3 = to_decimal("0")
            outlist = outlist + \
                to_string(tot_debt0, "         ->,>>9.99") + \
                to_string(tot_debt1, "         ->,>>9.99") + \
                to_string(tot_debt2, "         ->,>>9.99") + \
                to_string(tot_debt3, "         ->,>>9.99")
            fill_in_list(False, "", None)
            outlist = ""
            fill_in_list(False, "", None)
        outlist = "-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------"
        fill_in_list(False, "----", None)

        if not long_digit:
            outlist = "       " + \
                to_string(translateExtended("T O T A L A/R:", lvcarea, ""), "x(30)") + \
                to_string(translateExtended("T O T A L A/R:", lvcarea, ""), "x(30)") + \
                to_string(t_saldo, "->>,>>>,>>>,>>9.99") + \
                to_string(t_prev, "->>,>>>,>>>,>>9.99") + \
                to_string(t_debit, "->>,>>>,>>>,>>9.99") + \
                to_string(t_credit, "->>,>>>,>>>,>>9.99") + \
                to_string(t_debt0, "->>,>>>,>>>,>>9.99") + \
                to_string(t_debt1, "->>,>>>,>>>,>>9.99") + \
                to_string(t_debt2, "->>,>>>,>>>,>>9.99") + \
                to_string(t_debt3, "->>,>>>,>>>,>>9.99")
        else:
            outlist = "       " + \
                to_string(translateExtended("T O T A L A/R:", lvcarea, ""), "x(30)") + \
                to_string(translateExtended("T O T A L A/R:", lvcarea, ""), "x(30)") + \
                to_string(t_saldo, "->,>>>,>>>,>>>,>>9") + \
                to_string(t_prev, "->,>>>,>>>,>>>,>>9") + \
                to_string(t_debit, "->,>>>,>>>,>>>,>>9") + \
                to_string(t_credit, "->,>>>,>>>,>>>,>>9") + \
                to_string(t_debt0, "->,>>>,>>>,>>>,>>9") + \
                to_string(t_debt1, "->,>>>,>>>,>>>,>>9") + \
                to_string(t_debt2, "->,>>>,>>>,>>>,>>9") + \
                to_string(t_debt3, "->,>>>,>>>,>>>,>>9")
        fill_in_list(False, "", None)
        outlist = "       " + \
            to_string(translateExtended("Statistic Percentage (%) :", lvcarea, ""), "x(30)") + \
            to_string(translateExtended("Statistic Percentage (%) :", lvcarea, ""), "x(30)") + \
            "            100.00"
        for i in range(1, 55):
            outlist = outlist + "       "
        tot_debt0 = (to_decimal(t_debt0) /
                     to_decimal(t_saldo) * to_decimal("100"))
        tot_debt1 = (to_decimal(t_debt1) /
                     to_decimal(t_saldo) * to_decimal("100"))
        tot_debt2 = (to_decimal(t_debt2) /
                     to_decimal(t_saldo) * to_decimal("100"))
        tot_debt3 = (to_decimal(t_debt3) /
                     to_decimal(t_saldo) * to_decimal("100"))

        if tot_debt0 == None:
            tot_debt0 = to_decimal("0")

        if tot_debt1 == None:
            tot_debt1 = to_decimal("0")

        if tot_debt2 == None:
            tot_debt2 = to_decimal("0")

        if tot_debt3 == None:
            tot_debt3 = to_decimal("0")
        outlist = outlist + \
            to_string(tot_debt0, "           ->>9.99") + \
            to_string(tot_debt1, "           ->>9.99") + \
            to_string(tot_debt2, "           ->>9.99") + \
            to_string(tot_debt3, "           ->>9.99")
        fill_in_list(False, "", None)
        outlist = ""
        fill_in_list(False, "", None)

    def age_list2():
        nonlocal arage_balance_list_data, curr_art, counter, t_saldo, t_prev, t_debit, t_credit, t_debt0, t_debt1, t_debt2, t_debt3, tmp_saldo, curr_name, curr_gastnr, gastname, billname, p_bal, debit, credit, debt0, debt1, debt2, debt3, credit_limit, curr_counter, curr_fcurr, i, tot_debt, from_date, default_fcurr, outlist, long_digit, curr_rgdatum, bill_number, inp_gastnr, inp_artnr, tot_debtall, tot_debt0, tot_debt1, tot_debt2, tot_debt3, curr_time, ar_ledger, lvcarea, debitor, htparam, artikel, guest, waehrung, h_bill, bill, res_line
        nonlocal pvilanguage, case_type, mtd_flag, to_date, fdate, tdate, from_art, to_art, from_name, to_name, disptype, mi_bill, day1, day2, day3, detailed, cvt_flag, dollar_rate
        nonlocal debtrec, debt
        nonlocal arage_balance_list, arage_list, age_list, tage_list, ledger, debtrec, debt
        nonlocal arage_balance_list_data, arage_list_data, age_list_data, tage_list_data, ledger_data

        bill_name: string = ""
        curr_art = 0
        counter = 0
        t_saldo = to_decimal("0")
        t_prev = to_decimal("0")
        t_debit = to_decimal("0")
        t_credit = to_decimal("0")
        t_debt0 = to_decimal("0")
        t_debt1 = to_decimal("0")
        t_debt2 = to_decimal("0")
        t_debt3 = to_decimal("0")
        tmp_saldo = to_decimal("0")
        curr_name = ""
        curr_gastnr = 0
        gastname = ""
        billname = ""
        p_bal = to_decimal("0")
        debit = to_decimal("0")
        credit = to_decimal("0")
        debt0 = to_decimal("0")
        debt1 = to_decimal("0")
        debt2 = to_decimal("0")
        debt3 = to_decimal("0")
        tot_debt = to_decimal("0")
        i = 0
        curr_counter = 0
        curr_fcurr = ""

        from_date = date_mdy(get_month(to_date), 1, get_year(to_date))

        for artikel in db_session.query(Artikel).filter(
                ((Artikel.artart == 2) | (Artikel.artart == 7) | (Artikel.artart == 14)) & (Artikel.artnr >= from_art) & (Artikel.artnr <= to_art) & (Artikel.departement == 0)).order_by(Artikel.artart, Artikel.artnr).all():
            ledger = Ledger()
            ledger_data.append(ledger)

            ledger.artnr = artikel.artnr
            ledger.bezeich = to_string(
                artikel.artnr) + "  -  " + artikel.bezeich
        curr_art = 0

        for debitor in db_session.query(Debitor).filter(
                (Debitor.rgdatum <= to_date) & (Debitor.artnr >= from_art) & (Debitor.artnr <= to_art) & (Debitor.opart <= 1)).order_by(Debitor.artnr, Debitor.zahlkonto).all():

            guest = get_cache(Guest, {"gastnr": [(eq, debitor.gastnrmember)]})

            if guest:
                bill_name = guest.name + ", " + guest.vorname1 + \
                    guest.anredefirma + " " + guest.anrede1
            else:
                bill_name = ""

            if matches(bill_name, r"*" + from_name + r"*"):

                if curr_art != debitor.artnr:
                    curr_art = debitor.artnr

                    artikel = get_cache(
                        Artikel, {"artnr": [(eq, curr_art)], "departement": [(eq, 0)]})

                if debitor.counter > 0:

                    age_list = query(age_list_data, filters=(
                        lambda age_list: age_list.counter == debitor.counter), first=True)

                if (debitor.counter == 0) or (not age_list):

                    guest = get_cache(
                        Guest, {"gastnr": [(eq, debitor.gastnr)]})
                    age_list = Age_list()
                    age_list_data.append(age_list)

                    age_list.artnr = debitor.artnr
                    age_list.rechnr = debitor.rechnr
                    age_list.rgdatum = debitor.rgdatum
                    age_list.counter = debitor.counter
                    age_list.gastnr = debitor.gastnr
                    age_list.tot_debt = to_decimal("0")
                    age_list.opart = debitor.opart

                    if guest:
                        age_list.credit_limit = to_decimal(guest.kreditlimit)

                    if debitor.betrieb_gastmem == 0:
                        age_list.fcurr = default_fcurr
                    else:
                        waehrung = get_cache(
                            Waehrung, {"waehrungsnr": [(eq, debitor.betrieb_gastmem)]})

                        if waehrung:
                            age_list.fcurr = waehrung.wabkurz

                    if artikel.artart == 2:
                        get_bill_receiver_and_bill_name(debitor.rechnr)
                    else:
                        get_bill_receiver_and_bill_name(debitor.rechnr)

                if disptype == 0:
                    age_list.tot_debt = to_decimal(
                        age_list.tot_debt) + to_decimal(debitor.saldo)
                else:

                    if not cvt_flag:
                        age_list.tot_debt = to_decimal(
                            age_list.tot_debt) + to_decimal(debitor.vesrdep)
                    else:

                        if age_list.fcurr.lower() == (default_fcurr).lower():

                            if debitor.vesrdep != 0:
                                age_list.tot_debt = to_decimal(
                                    age_list.tot_debt) + to_decimal(debitor.vesrdep)

                            else:
                                age_list.tot_debt = to_decimal(
                                    age_list.tot_debt) + to_decimal((debitor.saldo) / to_decimal(dollar_rate))
                        else:
                            age_list.tot_debt = to_decimal(
                                age_list.tot_debt) + to_decimal((debitor.saldo) / to_decimal(dollar_rate))

                if debitor.rgdatum < from_date and debitor.zahlkonto == 0:

                    if disptype == 0:
                        age_list.p_bal = to_decimal(
                            age_list.p_bal) + to_decimal(debitor.saldo)
                    else:

                        if not cvt_flag:
                            age_list.p_bal = to_decimal(
                                age_list.p_bal) + to_decimal(debitor.vesrdep)
                        else:

                            if age_list.fcurr.lower() == (default_fcurr).lower():

                                if debitor.vesrdep != 0:
                                    age_list.p_bal = to_decimal(
                                        age_list.p_bal) + to_decimal(debitor.vesrdep)

                                else:
                                    age_list.p_bal = to_decimal(
                                        age_list.p_bal) + to_decimal((debitor.saldo) / to_decimal(dollar_rate))
                            else:
                                age_list.p_bal = to_decimal(
                                    age_list.p_bal) + to_decimal((debitor.saldo) / to_decimal(dollar_rate))

                if debitor.rgdatum >= from_date and debitor.zahlkonto == 0:

                    if disptype == 0:
                        age_list.debit = to_decimal(
                            age_list.debit) + to_decimal(debitor.saldo)
                    else:

                        if not cvt_flag:
                            age_list.debit = to_decimal(
                                age_list.debit) + to_decimal(debitor.vesrdep)
                        else:

                            if age_list.fcurr.lower() == (default_fcurr).lower():

                                if debitor.vesrdep != 0:
                                    age_list.debit = to_decimal(
                                        age_list.debit) + to_decimal(debitor.vesrdep)

                                else:
                                    age_list.debit = to_decimal(
                                        age_list.debit) + to_decimal((debitor.saldo) / to_decimal(dollar_rate))
                            else:
                                age_list.debit = to_decimal(
                                    age_list.debit) + to_decimal((debitor.saldo) / to_decimal(dollar_rate))

                if debitor.rgdatum < from_date and debitor.zahlkonto != 0:

                    if disptype == 0:
                        age_list.p_bal = to_decimal(
                            age_list.p_bal) + to_decimal(debitor.saldo)
                    else:

                        if not cvt_flag:
                            age_list.p_bal = to_decimal(
                                age_list.p_bal) + to_decimal(debitor.vesrdep)
                        else:

                            if age_list.fcurr.lower() == (default_fcurr).lower():

                                if debitor.vesrdep != 0:
                                    age_list.p_bal = to_decimal(
                                        age_list.p_bal) + to_decimal(debitor.vesrdep)

                                else:
                                    age_list.p_bal = to_decimal(
                                        age_list.p_bal) + to_decimal((debitor.saldo) / to_decimal(dollar_rate))
                            else:
                                age_list.p_bal = to_decimal(
                                    age_list.p_bal) + to_decimal((debitor.saldo) / to_decimal(dollar_rate))
                else:

                    if debitor.rgdatum >= from_date and debitor.zahlkonto != 0:

                        if disptype == 0:
                            age_list.credit = to_decimal(
                                age_list.credit) - to_decimal(debitor.saldo)
                        else:

                            if not cvt_flag:
                                age_list.credit = to_decimal(
                                    age_list.credit) - to_decimal(debitor.vesrdep)
                            else:

                                if age_list.fcurr.lower() == (default_fcurr).lower():

                                    if debitor.vesrdep != 0:
                                        age_list.credit = to_decimal(
                                            age_list.credit) - to_decimal(debitor.vesrdep)

                                    else:
                                        age_list.credit = to_decimal(
                                            age_list.credit) - to_decimal((debitor.saldo) / to_decimal(dollar_rate))
                                else:
                                    age_list.credit = to_decimal(
                                        age_list.credit) - to_decimal((debitor.saldo) / to_decimal(dollar_rate))

        for artikel in db_session.query(Artikel).filter(
                ((Artikel.artart == 2) | (Artikel.artart == 7) | (Artikel.artart == 14)) & (Artikel.artnr >= from_art) & (Artikel.artnr <= to_art) & (Artikel.departement == 0)).order_by(Artikel.artnr).all():
            curr_counter = 0

            for debitor in db_session.query(Debitor).filter(
                    (Debitor.artnr == artikel.artnr) & (Debitor.rgdatum <= to_date) & (Debitor.opart == 2) & (Debitor.zahlkonto == 0)).order_by(Debitor._recid).all():

                guest = get_cache(
                    Guest, {"gastnr": [(eq, debitor.gastnrmember)]})

                if guest:
                    bill_name = guest.name + ", " + guest.vorname1 + \
                        guest.anredefirma + " " + guest.anrede1
                else:
                    bill_name = ""

                if matches(bill_name, r"*" + from_name + r"*"):

                    guest = get_cache(
                        Guest, {"gastnr": [(eq, debitor.gastnr)]})
                    age_list = Age_list()
                    age_list_data.append(age_list)

                    age_list.artnr = debitor.artnr
                    age_list.rechnr = debitor.rechnr
                    age_list.rgdatum = debitor.rgdatum
                    age_list.counter = debitor.counter
                    age_list.gastnr = debitor.gastnr
                    age_list.tot_debt = to_decimal(debitor.saldo)
                    age_list.opart = debitor.opart

                    if guest:
                        age_list.credit_limit = to_decimal(guest.kreditlimit)

                    if debitor.betrieb_gastmem == 0:
                        age_list.fcurr = default_fcurr
                    else:

                        waehrung = get_cache(
                            Waehrung, {"waehrungsnr": [(eq, debitor.betrieb_gastmem)]})

                        if waehrung:
                            age_list.fcurr = waehrung.wabkurz

                    if artikel.artart == 2:
                        get_bill_receiver_and_bill_name(debitor.rechnr)
                    else:
                        get_bill_receiver_and_bill_name(debitor.rechnr)

                    if debitor.rgdatum < from_date:

                        if disptype == 0:
                            age_list.p_bal = to_decimal(
                                age_list.p_bal) + to_decimal(debitor.saldo)
                        else:

                            if not cvt_flag:
                                age_list.p_bal = to_decimal(
                                    age_list.p_bal) + to_decimal(debitor.vesrdep)
                            else:

                                if age_list.fcurr.lower() == (default_fcurr).lower():

                                    if debitor.vesrdep != 0:
                                        age_list.p_bal = to_decimal(
                                            age_list.p_bal) + to_decimal(debitor.vesrdep)

                                    else:
                                        age_list.p_bal = to_decimal(
                                            age_list.p_bal) + to_decimal((debitor.saldo) / to_decimal(dollar_rate))
                                else:
                                    age_list.p_bal = to_decimal(
                                        age_list.p_bal) + to_decimal((debitor.saldo) / to_decimal(dollar_rate))

                    elif debitor.rgdatum >= from_date:

                        if disptype == 0:
                            age_list.debit = to_decimal(
                                age_list.debit) + to_decimal(debitor.saldo)
                        else:

                            if not cvt_flag:
                                age_list.debit = to_decimal(
                                    age_list.debit) + to_decimal(debitor.vesrdep)
                            else:

                                if age_list.fcurr.lower() == (default_fcurr).lower():

                                    if debitor.vesrdep != 0:
                                        age_list.debit = to_decimal(
                                            age_list.debit) + to_decimal(debitor.vesrdep)

                                    else:
                                        age_list.debit = to_decimal(
                                            age_list.debit) + to_decimal((debitor.saldo) / to_decimal(dollar_rate))
                                else:
                                    age_list.debit = to_decimal(
                                        age_list.debit) + to_decimal((debitor.saldo) / to_decimal(dollar_rate))

                    for debtrec in db_session.query(Debtrec).filter(
                            (Debtrec.counter == debitor.counter) & (Debtrec.rechnr == debitor.rechnr) & (Debtrec.zahlkonto > 0) & (Debtrec.rgdatum <= to_date)).order_by(Debtrec._recid).all():
                        age_list.tot_debt = to_decimal(
                            age_list.tot_debt) + to_decimal(debtrec.saldo)

                        if debtrec.rgdatum < from_date:

                            if disptype == 0:
                                age_list.p_bal = to_decimal(
                                    age_list.p_bal) + to_decimal(debtrec.saldo)
                            else:

                                if not cvt_flag:
                                    age_list.p_bal = to_decimal(
                                        age_list.p_bal) + to_decimal(debtrec.vesrdep)
                                else:

                                    if age_list.fcurr.lower() == (default_fcurr).lower():

                                        if debitor.vesrdep != 0:
                                            age_list.p_bal = to_decimal(
                                                age_list.p_bal) + to_decimal(debitor.vesrdep)

                                        else:
                                            age_list.p_bal = to_decimal(
                                                age_list.p_bal) + to_decimal((debitor.saldo) / to_decimal(dollar_rate))
                                    else:
                                        age_list.p_bal = to_decimal(
                                            age_list.p_bal) + to_decimal((debtrec.saldo) / to_decimal(dollar_rate))

                        elif debtrec.rgdatum >= from_date:
                            if disptype == 0:
                                age_list.credit = to_decimal(
                                    age_list.credit) - to_decimal(debtrec.saldo)
                            else:
                                if not cvt_flag:
                                    age_list.credit = to_decimal(
                                        age_list.credit) - to_decimal(debtrec.vesrdep)
                                else:
                                    if age_list.fcurr.lower() == (default_fcurr).lower():

                                        if debitor.vesrdep != 0:
                                            age_list.credit = to_decimal(
                                                age_list.credit) - to_decimal(debitor.vesrdep)

                                        else:
                                            age_list.credit = to_decimal(
                                                age_list.credit) - to_decimal((debitor.saldo) / to_decimal(dollar_rate))
                                    else:
                                        age_list.credit = to_decimal(
                                            age_list.credit) - to_decimal((debtrec.saldo) / to_decimal(dollar_rate))

        for age_list in query(age_list_data):
            if age_list.p_bal >= - 1 and age_list.p_bal <= 1 and age_list.debit == 0 and age_list.credit == 0:
                age_list_data.remove(age_list)

        if ar_ledger != 0:
            for age_list in query(age_list_data, filters=(lambda age_list: age_list.artnr == ar_ledger)):

                tage_list = query(tage_list_data, filters=(
                    lambda tage_list: tage_list.rechnr == age_list.rechnr), first=True)

                if not tage_list:
                    tage_list = Tage_list()
                    tage_list_data.append(tage_list)

                    buffer_copy(age_list, tage_list)
                else:
                    tage_list.p_bal = to_decimal(
                        tage_list.p_bal) + to_decimal(age_list.p_bal)
                    tage_list.debit = to_decimal(
                        tage_list.debit) + to_decimal(age_list.debit)
                    tage_list.credit = to_decimal(
                        tage_list.credit) + to_decimal(age_list.credit)
                    tage_list.saldo = to_decimal(
                        tage_list.saldo) + to_decimal(age_list.saldo)
                    tage_list.debt0 = to_decimal(
                        tage_list.debt0) + to_decimal(age_list.debt0)
                    tage_list.debt1 = to_decimal(
                        tage_list.debt1) + to_decimal(age_list.debt1)
                    tage_list.debt2 = to_decimal(
                        tage_list.debt2) + to_decimal(age_list.debt2)
                    tage_list.debt3 = to_decimal(
                        tage_list.debt3) + to_decimal(age_list.debt3)
                    tage_list.tot_debt = to_decimal(
                        tage_list.tot_debt) + to_decimal(age_list.tot_debt)

                age_list_data.remove(age_list)

            for tage_list in query(tage_list_data):
                age_list = Age_list()
                age_list_data.append(age_list)

                buffer_copy(tage_list, age_list)
                tage_list_data.remove(tage_list)

        for ledger in query(ledger_data, sort_by=[("artnr", False)]):

            age_list = query(age_list_data, filters=(
                lambda age_list: age_list.artnr == ledger.artnr), first=True)

            if not age_list:
                continue
            outlist = "    " + ledger.bezeich.upper()
            fill_in_list(False, "", None)
            outlist = ""
            fill_in_list(False, "", None)
            counter = 0
            curr_gastnr = 0

            if mi_bill:

                for age_list in query(age_list_data, filters=(lambda age_list: age_list.artnr == ledger.artnr), sort_by=[("rgdatum", False), ("gastname", False)]):
                    create_output()

            else:

                for age_list in query(age_list_data, filters=(lambda age_list: age_list.artnr == ledger.artnr), sort_by=[("gastname", False), ("rechnr", False)]):
                    create_output()

            if counter > 0 and (p_bal != 0 or debit != 0 or credit != 0):

                if not long_digit:
                    outlist = "  " + to_string(counter, ">>>9 ") + \
                        to_string(gastname, "x(30)") + \
                        to_string(billname, "x(30)") + \
                        to_string(tot_debt, "->>,>>>,>>>,>>9.99") + \
                        to_string(p_bal, "->>,>>>,>>>,>>9.99") + \
                        to_string(debit, "->>,>>>,>>>,>>9.99") + \
                        to_string(credit, "->>,>>>,>>>,>>9.99") + \
                        to_string(debt0, "->>,>>>,>>>,>>9.99") + \
                        to_string(debt1, "->>,>>>,>>>,>>9.99") + \
                        to_string(debt2, "->>,>>>,>>>,>>9.99") + \
                        to_string(debt3, "->>,>>>,>>>,>>9.99") + \
                        to_string(credit_limit, "->>,>>>,>>>,>>9.99")
                else:
                    outlist = "  " + to_string(counter, ">>>9 ") + \
                        to_string(gastname, "x(30)") + \
                        to_string(billname, "x(30)") + \
                        to_string(tot_debt, "->,>>>,>>>,>>>,>>9") + \
                        to_string(p_bal, "->,>>>,>>>,>>>,>>9") + \
                        to_string(debit, "->,>>>,>>>,>>>,>>9") + \
                        to_string(credit, "->,>>>,>>>,>>>,>>9") + \
                        to_string(debt0, "->,>>>,>>>,>>>,>>9") + \
                        to_string(debt1, "->,>>>,>>>,>>>,>>9") + \
                        to_string(debt2, "->,>>>,>>>,>>>,>>9") + \
                        to_string(debt3, "->,>>>,>>>,>>>,>>9") + \
                        to_string(credit_limit, "->,>>>,>>>,>>>,>>9")
                fill_in_list(True, curr_fcurr, curr_rgdatum)
            else:
                counter = counter - 1
            tmp_saldo = to_decimal(ledger.tot_debt)

            if tmp_saldo == 0:
                tmp_saldo = to_decimal("1")
            outlist = "-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------"
            fill_in_list(False, "----", None)

            if not long_digit:
                outlist = "       " + \
                    to_string(translateExtended("T o t a l", lvcarea, ""), "x(30)") + \
                    to_string(translateExtended("T o t a l", lvcarea, ""), "x(30)") + \
                    to_string(ledger.tot_debt, "->>,>>>,>>>,>>9.99") + \
                    to_string(ledger.p_bal, "->>,>>>,>>>,>>9.99") + \
                    to_string(ledger.debit, "->>,>>>,>>>,>>9.99") + \
                    to_string(ledger.credit, "->>,>>>,>>>,>>9.99") + \
                    to_string(ledger.debt0, "->>,>>>,>>>,>>9.99") + \
                    to_string(ledger.debt1, "->>,>>>,>>>,>>9.99") + \
                    to_string(ledger.debt2, "->>,>>>,>>>,>>9.99") + \
                    to_string(ledger.debt3, "->>,>>>,>>>,>>9.99")
            else:
                outlist = "       " + \
                    to_string(translateExtended("T o t a l", lvcarea, ""), "x(30)") + \
                    to_string(translateExtended("T o t a l", lvcarea, ""), "x(30)") + \
                    to_string(ledger.tot_debt, "->,>>>,>>>,>>>,>>9") + \
                    to_string(ledger.p_bal, "->,>>>,>>>,>>>,>>9") + \
                    to_string(ledger.debit, "->,>>>,>>>,>>>,>>9") + \
                    to_string(ledger.credit, "->,>>>,>>>,>>>,>>9") + \
                    to_string(ledger.debt0, "->,>>>,>>>,>>>,>>9") + \
                    to_string(ledger.debt1, "->,>>>,>>>,>>>,>>9") + \
                    to_string(ledger.debt2, "->,>>>,>>>,>>>,>>9") + \
                    to_string(ledger.debt3, "->,>>>,>>>,>>>,>>9")
            fill_in_list(False, "", None)
            outlist = "       " + \
                to_string(translateExtended("Statistic Percentage (%) :", lvcarea, ""), "x(30)") + \
                to_string(translateExtended("Statistic Percentage (%) :", lvcarea, ""), "x(30)") + \
                "            100.00"
            for i in range(1, 55):
                outlist = outlist + "       "
            tot_debt0 = (to_decimal(ledger.debt0) /
                         to_decimal(tmp_saldo) * to_decimal("100"))
            tot_debt1 = (to_decimal(ledger.debt1) /
                         to_decimal(tmp_saldo) * to_decimal("100"))
            tot_debt2 = (to_decimal(ledger.debt2) /
                         to_decimal(tmp_saldo) * to_decimal("100"))
            tot_debt3 = (to_decimal(ledger.debt3) /
                         to_decimal(tmp_saldo) * to_decimal("100"))

            if tot_debt0 == None:
                tot_debt0 = to_decimal("0")

            if tot_debt1 == None:
                tot_debt1 = to_decimal("0")

            if tot_debt2 == None:
                tot_debt2 = to_decimal("0")

            if tot_debt3 == None:
                tot_debt3 = to_decimal("0")
            outlist = outlist + \
                to_string(tot_debt0, "           ->>9.99") + \
                to_string(tot_debt1, "           ->>9.99") + \
                to_string(tot_debt2, "           ->>9.99") + \
                to_string(tot_debt3, "           ->>9.99")
            fill_in_list(False, "", None)
            outlist = ""
            fill_in_list(False, "", None)
        outlist = "-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------"
        fill_in_list(False, "----", None)

        if not long_digit:
            outlist = "       " + \
                to_string(translateExtended("T O T A L A/R:", lvcarea, ""), "x(30)") + \
                to_string(translateExtended("T O T A L A/R:", lvcarea, ""), "x(30)") + \
                to_string(t_saldo, "->>,>>>,>>>,>>9.99") + \
                to_string(t_prev, "->>,>>>,>>>,>>9.99") + \
                to_string(t_debit, "->>,>>>,>>>,>>9.99") + \
                to_string(t_credit, "->>,>>>,>>>,>>9.99") + \
                to_string(t_debt0, "->>,>>>,>>>,>>9.99") + \
                to_string(t_debt1, "->>,>>>,>>>,>>9.99") + \
                to_string(t_debt2, "->>,>>>,>>>,>>9.99") + \
                to_string(t_debt3, "->>,>>>,>>>,>>9.99")
        else:
            outlist = "       " + \
                to_string(translateExtended("T O T A L A/R:", lvcarea, ""), "x(30)") + \
                to_string(translateExtended("T O T A L A/R:", lvcarea, ""), "x(30)") + \
                to_string(t_saldo, "->,>>>,>>>,>>>,>>9") + \
                to_string(t_prev, "->,>>>,>>>,>>>,>>9") + \
                to_string(t_debit, "->,>>>,>>>,>>>,>>9") + \
                to_string(t_credit, "->,>>>,>>>,>>>,>>9") + \
                to_string(t_debt0, "->,>>>,>>>,>>>,>>9") + \
                to_string(t_debt1, "->,>>>,>>>,>>>,>>9") + \
                to_string(t_debt2, "->,>>>,>>>,>>>,>>9") + \
                to_string(t_debt3, "->,>>>,>>>,>>>,>>9")
        fill_in_list(False, "", None)
        outlist = "       " + \
            to_string(translateExtended("Statistic Percentage (%) :", lvcarea, ""), "x(30)") + \
            to_string(translateExtended("Statistic Percentage (%) :", lvcarea, ""), "x(30)") + \
            "            100.00"
        for i in range(1, 55):
            outlist = outlist + "       "
        tot_debt0 = (to_decimal(t_debt0) /
                     to_decimal(t_saldo) * to_decimal("100"))
        tot_debt1 = (to_decimal(t_debt1) /
                     to_decimal(t_saldo) * to_decimal("100"))
        tot_debt2 = (to_decimal(t_debt2) /
                     to_decimal(t_saldo) * to_decimal("100"))
        tot_debt3 = (to_decimal(t_debt3) /
                     to_decimal(t_saldo) * to_decimal("100"))

        if tot_debt0 == None:
            tot_debt0 = to_decimal("0")

        if tot_debt1 == None:
            tot_debt1 = to_decimal("0")

        if tot_debt2 == None:
            tot_debt2 = to_decimal("0")

        if tot_debt3 == None:
            tot_debt3 = to_decimal("0")
        outlist = outlist + \
            to_string(tot_debt0, "           ->>9.99") + \
            to_string(tot_debt1, "           ->>9.99") + \
            to_string(tot_debt2, "           ->>9.99") + \
            to_string(tot_debt3, "           ->>9.99")
        fill_in_list(False, "", None)
        outlist = ""
        fill_in_list(False, "", None)

    def age_list1a():
        nonlocal arage_balance_list_data, curr_art, counter, t_saldo, t_prev, t_debit, t_credit, t_debt0, t_debt1, t_debt2, t_debt3, tmp_saldo, curr_name, curr_gastnr, gastname, billname, p_bal, debit, credit, debt0, debt1, debt2, debt3, credit_limit, curr_counter, curr_fcurr, i, tot_debt, from_date, default_fcurr, outlist, long_digit, curr_rgdatum, bill_number, inp_gastnr, inp_artnr, tot_debtall, tot_debt0, tot_debt1, tot_debt2, tot_debt3, curr_time, ar_ledger, lvcarea, bill_name, debitor, htparam, artikel, guest, waehrung, h_bill, bill, res_line
        nonlocal pvilanguage, case_type, mtd_flag, to_date, fdate, tdate, from_art, to_art, from_name, to_name, disptype, mi_bill, day1, day2, day3, detailed, cvt_flag, dollar_rate
        nonlocal debtrec, debt
        nonlocal arage_balance_list, arage_list, age_list, tage_list, ledger, debtrec, debt
        nonlocal arage_balance_list_data, arage_list_data, age_list_data, tage_list_data, ledger_data

        curr_art = 0
        counter = 0
        t_saldo = to_decimal("0")
        t_prev = to_decimal("0")
        t_debit = to_decimal("0")
        t_credit = to_decimal("0")
        t_debt0 = to_decimal("0")
        t_debt1 = to_decimal("0")
        t_debt2 = to_decimal("0")
        t_debt3 = to_decimal("0")
        tmp_saldo = to_decimal("0")
        curr_name = ""
        curr_gastnr = 0
        gastname = ""
        billname = ""
        p_bal = to_decimal("0")
        debit = to_decimal("0")
        credit = to_decimal("0")
        debt0 = to_decimal("0")
        debt1 = to_decimal("0")
        debt2 = to_decimal("0")
        debt3 = to_decimal("0")
        tot_debt = to_decimal("0")
        i = 0
        curr_counter = 0
        curr_fcurr = ""

        from_date = fdate

        for artikel in db_session.query(Artikel).filter(
                ((Artikel.artart == 2) | (Artikel.artart == 7) | (Artikel.artart == 14)) & (Artikel.artnr >= from_art) & (Artikel.artnr <= to_art) & (Artikel.departement == 0)).order_by(Artikel.artart, Artikel.artnr).all():
            ledger = Ledger()
            ledger_data.append(ledger)

            ledger.artnr = artikel.artnr
            ledger.bezeich = to_string(
                artikel.artnr) + "  -  " + artikel.bezeich
        curr_art = 0

        for debitor in db_session.query(Debitor).filter(
                (Debitor.rgdatum <= tdate) & (Debitor.artnr >= from_art) & (Debitor.artnr <= to_art) & (Debitor.opart <= 1)).order_by(Debitor.artnr, Debitor.zahlkonto).all():

            if debitor.name.lower() >= (from_name).lower():

                if curr_art != debitor.artnr:
                    curr_art = debitor.artnr

                    artikel = get_cache(
                        Artikel, {"artnr": [(eq, curr_art)], "departement": [(eq, 0)]})

                if debitor.counter > 0:

                    age_list = query(age_list_data, filters=(
                        lambda age_list: age_list.counter == debitor.counter), first=True)

                if (debitor.counter == 0) or (not age_list):

                    guest = get_cache(
                        Guest, {"gastnr": [(eq, debitor.gastnr)]})
                    age_list = Age_list()
                    age_list_data.append(age_list)

                    age_list.artnr = debitor.artnr
                    age_list.rechnr = debitor.rechnr
                    age_list.rgdatum = debitor.rgdatum
                    age_list.counter = debitor.counter
                    age_list.gastnr = debitor.gastnr
                    age_list.tot_debt = to_decimal("0")
                    age_list.opart = debitor.opart

                    if guest:
                        age_list.credit_limit = to_decimal(guest.kreditlimit)

                    if debitor.betrieb_gastmem == 0:
                        age_list.fcurr = default_fcurr
                    else:

                        waehrung = get_cache(
                            Waehrung, {"waehrungsnr": [(eq, debitor.betrieb_gastmem)]})

                        if waehrung:
                            age_list.fcurr = waehrung.wabkurz

                    if artikel.artart == 2:
                        get_bill_receiver_and_bill_name(debitor.rechnr)
                    else:
                        get_bill_receiver_and_bill_name(debitor.rechnr)

                if disptype == 0:
                    age_list.tot_debt = to_decimal(
                        age_list.tot_debt) + to_decimal(debitor.saldo)
                else:

                    if not cvt_flag:
                        age_list.tot_debt = to_decimal(
                            age_list.tot_debt) + to_decimal(debitor.vesrdep)
                    else:

                        if age_list.fcurr.lower() == (default_fcurr).lower():

                            if debitor.vesrdep != 0:
                                age_list.tot_debt = to_decimal(
                                    age_list.tot_debt) + to_decimal(debitor.vesrdep)

                            else:
                                age_list.tot_debt = to_decimal(
                                    age_list.tot_debt) + to_decimal((debitor.saldo) / to_decimal(dollar_rate))
                        else:
                            age_list.tot_debt = to_decimal(
                                age_list.tot_debt) + to_decimal((debitor.saldo) / to_decimal(dollar_rate))

                if debitor.rgdatum < from_date and debitor.zahlkonto == 0:

                    if disptype == 0:
                        age_list.p_bal = to_decimal(
                            age_list.p_bal) + to_decimal(debitor.saldo)
                    else:

                        if not cvt_flag:
                            age_list.p_bal = to_decimal(
                                age_list.p_bal) + to_decimal(debitor.vesrdep)
                        else:

                            if age_list.fcurr.lower() == (default_fcurr).lower():

                                if debitor.vesrdep != 0:
                                    age_list.p_bal = to_decimal(
                                        age_list.p_bal) + to_decimal(debitor.vesrdep)

                                else:
                                    age_list.p_bal = to_decimal(
                                        age_list.p_bal) + to_decimal((debitor.saldo) / to_decimal(dollar_rate))
                            else:
                                age_list.p_bal = to_decimal(
                                    age_list.p_bal) + to_decimal((debitor.saldo) / to_decimal(dollar_rate))

                if debitor.rgdatum >= from_date and debitor.zahlkonto == 0:

                    if disptype == 0:
                        age_list.debit = to_decimal(
                            age_list.debit) + to_decimal(debitor.saldo)
                    else:

                        if not cvt_flag:
                            age_list.debit = to_decimal(
                                age_list.debit) + to_decimal(debitor.vesrdep)
                        else:

                            if age_list.fcurr.lower() == (default_fcurr).lower():

                                if debitor.vesrdep != 0:
                                    age_list.debit = to_decimal(
                                        age_list.debit) + to_decimal(debitor.vesrdep)

                                else:
                                    age_list.debit = to_decimal(
                                        age_list.debit) + to_decimal((debitor.saldo) / to_decimal(dollar_rate))
                            else:
                                age_list.debit = to_decimal(
                                    age_list.debit) + to_decimal((debitor.saldo) / to_decimal(dollar_rate))

                if debitor.rgdatum < from_date and debitor.zahlkonto != 0:

                    if disptype == 0:
                        age_list.p_bal = to_decimal(
                            age_list.p_bal) + to_decimal(debitor.saldo)
                    else:

                        if not cvt_flag:
                            age_list.p_bal = to_decimal(
                                age_list.p_bal) + to_decimal(debitor.vesrdep)
                        else:

                            if age_list.fcurr.lower() == (default_fcurr).lower():

                                if debitor.vesrdep != 0:
                                    age_list.p_bal = to_decimal(
                                        age_list.p_bal) + to_decimal(debitor.vesrdep)

                                else:
                                    age_list.p_bal = to_decimal(
                                        age_list.p_bal) + to_decimal((debitor.saldo) / to_decimal(dollar_rate))
                            else:
                                age_list.p_bal = to_decimal(
                                    age_list.p_bal) + to_decimal((debitor.saldo) / to_decimal(dollar_rate))
                else:

                    if debitor.rgdatum >= from_date and debitor.zahlkonto != 0:

                        if disptype == 0:
                            age_list.credit = to_decimal(
                                age_list.credit) - to_decimal(debitor.saldo)
                        else:

                            if not cvt_flag:
                                age_list.credit = to_decimal(
                                    age_list.credit) - to_decimal(debitor.vesrdep)
                            else:

                                if age_list.fcurr.lower() == (default_fcurr).lower():

                                    if debitor.vesrdep != 0:
                                        age_list.credit = to_decimal(
                                            age_list.credit) - to_decimal(debitor.vesrdep)

                                    else:
                                        age_list.credit = to_decimal(
                                            age_list.credit) - to_decimal((debitor.saldo) / to_decimal(dollar_rate))
                                else:
                                    age_list.credit = to_decimal(
                                        age_list.credit) - to_decimal((debitor.saldo) / to_decimal(dollar_rate))

        for artikel in db_session.query(Artikel).filter(
                ((Artikel.artart == 2) | (Artikel.artart == 7) | (Artikel.artart == 14)) & (Artikel.artnr >= from_art) & (Artikel.artnr <= to_art) & (Artikel.departement == 0)).order_by(Artikel.artnr).all():
            curr_counter = 0

            for debitor in db_session.query(Debitor).filter(
                    (Debitor.artnr == artikel.artnr) & (Debitor.rgdatum <= to_date) & (Debitor.opart == 2) & (Debitor.zahlkonto == 0)).order_by(Debitor._recid).all():

                if debitor.name.lower() >= (from_name).lower():

                    guest = get_cache(
                        Guest, {"gastnr": [(eq, debitor.gastnr)]})
                    age_list = Age_list()
                    age_list_data.append(age_list)

                    age_list.artnr = debitor.artnr
                    age_list.rechnr = debitor.rechnr
                    age_list.rgdatum = debitor.rgdatum
                    age_list.counter = debitor.counter
                    age_list.gastnr = debitor.gastnr
                    age_list.tot_debt = to_decimal(debitor.saldo)
                    age_list.opart = debitor.opart

                    if guest:
                        age_list.credit_limit = to_decimal(guest.kreditlimit)

                    if debitor.betrieb_gastmem == 0:
                        age_list.fcurr = default_fcurr
                    else:

                        waehrung = get_cache(
                            Waehrung, {"waehrungsnr": [(eq, debitor.betrieb_gastmem)]})

                        if waehrung:
                            age_list.fcurr = waehrung.wabkurz

                    if artikel.artart == 2:
                        get_bill_receiver_and_bill_name(debitor.rechnr)
                    else:
                        get_bill_receiver_and_bill_name(debitor.rechnr)

                    if debitor.rgdatum < from_date:

                        if disptype == 0:
                            age_list.p_bal = to_decimal(
                                age_list.p_bal) + to_decimal(debitor.saldo)
                        else:

                            if not cvt_flag:
                                age_list.p_bal = to_decimal(
                                    age_list.p_bal) + to_decimal(debitor.vesrdep)
                            else:

                                if age_list.fcurr.lower() == (default_fcurr).lower():

                                    if debitor.vesrdep != 0:
                                        age_list.p_bal = to_decimal(
                                            age_list.p_bal) + to_decimal(debitor.vesrdep)

                                    else:
                                        age_list.p_bal = to_decimal(
                                            age_list.p_bal) + to_decimal((debitor.saldo) / to_decimal(dollar_rate))
                                else:
                                    age_list.p_bal = to_decimal(
                                        age_list.p_bal) + to_decimal((debitor.saldo) / to_decimal(dollar_rate))

                    elif debitor.rgdatum >= from_date:

                        if disptype == 0:
                            age_list.debit = to_decimal(
                                age_list.debit) + to_decimal(debitor.saldo)
                        else:

                            if not cvt_flag:
                                age_list.debit = to_decimal(
                                    age_list.debit) + to_decimal(debitor.vesrdep)
                            else:

                                if age_list.fcurr.lower() == (default_fcurr).lower():

                                    if debitor.vesrdep != 0:
                                        age_list.debit = to_decimal(
                                            age_list.debit) + to_decimal(debitor.vesrdep)

                                    else:
                                        age_list.debit = to_decimal(
                                            age_list.debit) + to_decimal((debitor.saldo) / to_decimal(dollar_rate))
                                else:
                                    age_list.debit = to_decimal(
                                        age_list.debit) + to_decimal((debitor.saldo) / to_decimal(dollar_rate))

                    for debtrec in db_session.query(Debtrec).filter(
                            (Debtrec.counter == debitor.counter) & (Debtrec.rechnr == debitor.rechnr) & (Debtrec.zahlkonto > 0) & (Debtrec.rgdatum <= to_date)).order_by(Debtrec._recid).all():
                        age_list.tot_debt = to_decimal(
                            age_list.tot_debt) + to_decimal(debtrec.saldo)

                        if debtrec.rgdatum < from_date:

                            if disptype == 0:
                                age_list.p_bal = to_decimal(
                                    age_list.p_bal) + to_decimal(debtrec.saldo)
                            else:

                                if not cvt_flag:
                                    age_list.p_bal = to_decimal(
                                        age_list.p_bal) + to_decimal(debtrec.vesrdep)
                                else:

                                    if age_list.fcurr.lower() == (default_fcurr).lower():

                                        if debitor.vesrdep != 0:
                                            age_list.p_bal = to_decimal(
                                                age_list.p_bal) + to_decimal(debitor.vesrdep)

                                        else:
                                            age_list.p_bal = to_decimal(
                                                age_list.p_bal) + to_decimal((debitor.saldo) / to_decimal(dollar_rate))
                                    else:
                                        age_list.p_bal = to_decimal(
                                            age_list.p_bal) + to_decimal((debtrec.saldo) / to_decimal(dollar_rate))

                        elif debtrec.rgdatum >= from_date:

                            if disptype == 0:
                                age_list.credit = to_decimal(
                                    age_list.credit) - to_decimal(debtrec.saldo)
                            else:

                                if not cvt_flag:
                                    age_list.credit = to_decimal(
                                        age_list.credit) - to_decimal(debtrec.vesrdep)
                                else:

                                    if age_list.fcurr.lower() == (default_fcurr).lower():

                                        if debitor.vesrdep != 0:
                                            age_list.credit = to_decimal(
                                                age_list.credit) - to_decimal(debitor.vesrdep)

                                        else:
                                            age_list.credit = to_decimal(
                                                age_list.credit) - to_decimal((debitor.saldo) / to_decimal(dollar_rate))
                                    else:
                                        age_list.credit = to_decimal(
                                            age_list.credit) - to_decimal((debtrec.saldo) / to_decimal(dollar_rate))

        for age_list in query(age_list_data):

            if age_list.p_bal >= - 1 and age_list.p_bal <= 1 and age_list.debit == 0 and age_list.credit == 0:
                age_list_data.remove(age_list)

        if ar_ledger != 0:

            for age_list in query(age_list_data, filters=(lambda age_list: age_list.artnr == ar_ledger)):

                tage_list = query(tage_list_data, filters=(
                    lambda tage_list: tage_list.rechnr == age_list.rechnr), first=True)

                if not tage_list:
                    tage_list = Tage_list()
                    tage_list_data.append(tage_list)

                    buffer_copy(age_list, tage_list)
                else:
                    tage_list.p_bal = to_decimal(
                        tage_list.p_bal) + to_decimal(age_list.p_bal)
                    tage_list.debit = to_decimal(
                        tage_list.debit) + to_decimal(age_list.debit)
                    tage_list.credit = to_decimal(
                        tage_list.credit) + to_decimal(age_list.credit)
                    tage_list.saldo = to_decimal(
                        tage_list.saldo) + to_decimal(age_list.saldo)
                    tage_list.debt0 = to_decimal(
                        tage_list.debt0) + to_decimal(age_list.debt0)
                    tage_list.debt1 = to_decimal(
                        tage_list.debt1) + to_decimal(age_list.debt1)
                    tage_list.debt2 = to_decimal(
                        tage_list.debt2) + to_decimal(age_list.debt2)
                    tage_list.debt3 = to_decimal(
                        tage_list.debt3) + to_decimal(age_list.debt3)
                    tage_list.tot_debt = to_decimal(
                        tage_list.tot_debt) + to_decimal(age_list.tot_debt)

                age_list_data.remove(age_list)

            for tage_list in query(tage_list_data):
                age_list = Age_list()
                age_list_data.append(age_list)

                buffer_copy(tage_list, age_list)
                tage_list_data.remove(tage_list)

        for ledger in query(ledger_data, sort_by=[("artnr", False)]):

            age_list = query(age_list_data, filters=(
                lambda age_list: age_list.artnr == ledger.artnr), first=True)

            if not age_list:
                continue
            outlist = "    " + ledger.bezeich.upper()
            fill_in_list(False, "", None)
            outlist = ""
            fill_in_list(False, "", None)
            counter = 0
            curr_gastnr = 0

            if mi_bill:

                for age_list in query(age_list_data, filters=(lambda age_list: age_list.artnr == ledger.artnr), sort_by=[("rgdatum", False), ("gastname", False), ("rechnr", False)]):
                    create_output()

            else:

                for age_list in query(age_list_data, filters=(lambda age_list: age_list.artnr == ledger.artnr), sort_by=[("gastname", False), ("rechnr", False)]):
                    create_output()

            if counter > 0 and (p_bal != 0 or debit != 0 or credit != 0):

                if not long_digit:
                    outlist = "  " + \
                        to_string(counter, ">>>9 ") + \
                        to_string(gastname, "x(30)") + \
                        to_string(billname, "x(30)") + \
                        to_string(tot_debt, "->>,>>>,>>>,>>9.99") + \
                        to_string(p_bal, "->>,>>>,>>>,>>9.99") + \
                        to_string(debit, "->>,>>>,>>>,>>9.99") + \
                        to_string(credit, "->>,>>>,>>>,>>9.99") + \
                        to_string(debt0, "->>,>>>,>>>,>>9.99") + \
                        to_string(debt1, "->>,>>>,>>>,>>9.99") + \
                        to_string(debt2, "->>,>>>,>>>,>>9.99") + \
                        to_string(debt3, "->>,>>>,>>>,>>9.99") + \
                        to_string(credit_limit, "->>,>>>,>>>,>>9.99")
                else:
                    outlist = "  " + \
                        to_string(counter, ">>>9 ") + \
                        to_string(gastname, "x(30)") + \
                        to_string(billname, "x(30)") + \
                        to_string(tot_debt, "->,>>>,>>>,>>>,>>9") + \
                        to_string(p_bal, "->,>>>,>>>,>>>,>>9") + \
                        to_string(debit, "->,>>>,>>>,>>>,>>9") + \
                        to_string(credit, "->,>>>,>>>,>>>,>>9") + \
                        to_string(debt0, "->,>>>,>>>,>>>,>>9") + \
                        to_string(debt1, "->,>>>,>>>,>>>,>>9") + \
                        to_string(debt2, "->,>>>,>>>,>>>,>>9") + \
                        to_string(debt3, "->,>>>,>>>,>>>,>>9") + \
                        to_string(credit_limit, "->,>>>,>>>,>>>,>>9")
                fill_in_list(True, curr_fcurr, curr_rgdatum)
            else:
                counter = counter - 1
            tmp_saldo = to_decimal(ledger.tot_debt)

            if tmp_saldo == 0:
                tmp_saldo = to_decimal("1")
            outlist = "-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------"
            fill_in_list(False, "----", None)

            if not long_digit:
                outlist = "       " + \
                    to_string(translateExtended("T o t a l", lvcarea, ""), "x(30)") + \
                    to_string(translateExtended("T o t a l", lvcarea, ""), "x(30)") + \
                    to_string(ledger.tot_debt, "->>,>>>,>>>,>>9.99") + \
                    to_string(ledger.p_bal, "->>,>>>,>>>,>>9.99") + \
                    to_string(ledger.debit, "->>,>>>,>>>,>>9.99") + \
                    to_string(ledger.credit, "->>,>>>,>>>,>>9.99") + \
                    to_string(ledger.debt0, "->>,>>>,>>>,>>9.99") + \
                    to_string(ledger.debt1, "->>,>>>,>>>,>>9.99") + \
                    to_string(ledger.debt2, "->>,>>>,>>>,>>9.99") + \
                    to_string(ledger.debt3, "->>,>>>,>>>,>>9.99")
            else:
                outlist = "       " + \
                    to_string(translateExtended("T o t a l", lvcarea, ""), "x(30)") + \
                    to_string(translateExtended("T o t a l", lvcarea, ""), "x(30)") + \
                    to_string(ledger.tot_debt, "->,>>>,>>>,>>>,>>9") + \
                    to_string(ledger.p_bal, "->,>>>,>>>,>>>,>>9") + \
                    to_string(ledger.debit, "->,>>>,>>>,>>>,>>9") + \
                    to_string(ledger.credit, "->,>>>,>>>,>>>,>>9") + \
                    to_string(ledger.debt0, "->,>>>,>>>,>>>,>>9") + \
                    to_string(ledger.debt1, "->,>>>,>>>,>>>,>>9") + \
                    to_string(ledger.debt2, "->,>>>,>>>,>>>,>>9") + \
                    to_string(ledger.debt3, "->,>>>,>>>,>>>,>>9")
            fill_in_list(False, "", None)
            outlist = "       " + \
                to_string(translateExtended("Statistic Percentage (%) :", lvcarea, ""), "x(30)") + \
                to_string(translateExtended("Statistic Percentage (%) :", lvcarea, ""), "x(30)") + \
                "            100.00"
            for i in range(1, 55):
                outlist = outlist + "       "
            tot_debt0 = (to_decimal(ledger.debt0) /
                         to_decimal(tmp_saldo) * to_decimal("100"))
            tot_debt1 = (to_decimal(ledger.debt1) /
                         to_decimal(tmp_saldo) * to_decimal("100"))
            tot_debt2 = (to_decimal(ledger.debt2) /
                         to_decimal(tmp_saldo) * to_decimal("100"))
            tot_debt3 = (to_decimal(ledger.debt3) /
                         to_decimal(tmp_saldo) * to_decimal("100"))

            if tot_debt0 == None:
                tot_debt0 = to_decimal("0")

            if tot_debt1 == None:
                tot_debt1 = to_decimal("0")

            if tot_debt2 == None:
                tot_debt2 = to_decimal("0")

            if tot_debt3 == None:
                tot_debt3 = to_decimal("0")
            outlist = outlist + \
                to_string(tot_debt0, "           ->>9.99") + \
                to_string(tot_debt1, "           ->>9.99") + \
                to_string(tot_debt2, "           ->>9.99") + \
                to_string(tot_debt3, "           ->>9.99")
            fill_in_list(False, "", None)
            outlist = ""
            fill_in_list(False, "", None)
        outlist = "-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------"
        fill_in_list(False, "----", None)

        if not long_digit:
            outlist = "       " + \
                to_string(translateExtended("T O T A L A/R:", lvcarea, ""), "x(30)") + \
                to_string(translateExtended("T O T A L A/R:", lvcarea, ""), "x(30)") + \
                to_string(t_saldo, "->>,>>>,>>>,>>9.99") + to_string(t_prev, "->>,>>>,>>>,>>9.99") +\
                to_string(t_debit, "->>,>>>,>>>,>>9.99") + \
                to_string(t_credit, "->>,>>>,>>>,>>9.99") + \
                to_string(t_debt0, "->>,>>>,>>>,>>9.99") + \
                to_string(t_debt1, "->>,>>>,>>>,>>9.99") + \
                to_string(t_debt2, "->>,>>>,>>>,>>9.99") + \
                to_string(t_debt3, "->>,>>>,>>>,>>9.99")
        else:
            outlist = "       " + \
                to_string(translateExtended("T O T A L A/R:", lvcarea, ""), "x(30)") + \
                to_string(translateExtended("T O T A L A/R:", lvcarea, ""), "x(30)") + \
                to_string(t_saldo, "->,>>>,>>>,>>>,>>9") + \
                to_string(t_prev, "->,>>>,>>>,>>>,>>9") + \
                to_string(t_debit, "->,>>>,>>>,>>>,>>9") + \
                to_string(t_credit, "->,>>>,>>>,>>>,>>9") + \
                to_string(t_debt0, "->,>>>,>>>,>>>,>>9") + \
                to_string(t_debt1, "->,>>>,>>>,>>>,>>9") + \
                to_string(t_debt2, "->,>>>,>>>,>>>,>>9") + \
                to_string(t_debt3, "->,>>>,>>>,>>>,>>9")
        fill_in_list(False, "", None)
        outlist = "       " + \
            to_string(translateExtended("Statistic Percentage (%) :", lvcarea, ""), "x(30)") + \
            to_string(translateExtended("Statistic Percentage (%) :", lvcarea, ""), "x(30)") + \
            "            100.00"
        for i in range(1, 55):
            outlist = outlist + "       "
        tot_debt0 = (to_decimal(t_debt0) /
                     to_decimal(t_saldo) * to_decimal("100"))
        tot_debt1 = (to_decimal(t_debt1) /
                     to_decimal(t_saldo) * to_decimal("100"))
        tot_debt2 = (to_decimal(t_debt2) /
                     to_decimal(t_saldo) * to_decimal("100"))
        tot_debt3 = (to_decimal(t_debt3) /
                     to_decimal(t_saldo) * to_decimal("100"))

        if tot_debt0 == None:
            tot_debt0 = to_decimal("0")

        if tot_debt1 == None:
            tot_debt1 = to_decimal("0")

        if tot_debt2 == None:
            tot_debt2 = to_decimal("0")

        if tot_debt3 == None:
            tot_debt3 = to_decimal("0")
        outlist = outlist + \
            to_string(tot_debt0, "           ->>9.99") + \
            to_string(tot_debt1, "           ->>9.99") + \
            to_string(tot_debt2, "           ->>9.99") + \
            to_string(tot_debt3, "           ->>9.99")
        fill_in_list(False, "", None)
        outlist = ""
        fill_in_list(False, "", None)

    def age_list2a():
        nonlocal arage_balance_list_data, curr_art, counter, t_saldo, t_prev, t_debit, t_credit, t_debt0, t_debt1, t_debt2, t_debt3, tmp_saldo, curr_name, curr_gastnr, gastname, billname, p_bal, debit, credit, debt0, debt1, debt2, debt3, credit_limit, curr_counter, curr_fcurr, i, tot_debt, from_date, default_fcurr, outlist, long_digit, curr_rgdatum, bill_number, inp_gastnr, inp_artnr, tot_debtall, tot_debt0, tot_debt1, tot_debt2, tot_debt3, curr_time, ar_ledger, lvcarea, debitor, htparam, artikel, guest, waehrung, h_bill, bill, res_line
        nonlocal pvilanguage, case_type, mtd_flag, to_date, fdate, tdate, from_art, to_art, from_name, to_name, disptype, mi_bill, day1, day2, day3, detailed, cvt_flag, dollar_rate
        nonlocal debtrec, debt
        nonlocal arage_balance_list, arage_list, age_list, tage_list, ledger, debtrec, debt
        nonlocal arage_balance_list_data, arage_list_data, age_list_data, tage_list_data, ledger_data

        bill_name: string = ""
        curr_art = 0
        counter = 0
        t_saldo = to_decimal("0")
        t_prev = to_decimal("0")
        t_debit = to_decimal("0")
        t_credit = to_decimal("0")
        t_debt0 = to_decimal("0")
        t_debt1 = to_decimal("0")
        t_debt2 = to_decimal("0")
        t_debt3 = to_decimal("0")
        tmp_saldo = to_decimal("0")
        curr_name = ""
        curr_gastnr = 0
        gastname = ""
        billname = ""
        p_bal = to_decimal("0")
        debit = to_decimal("0")
        credit = to_decimal("0")
        debt0 = to_decimal("0")
        debt1 = to_decimal("0")
        debt2 = to_decimal("0")
        debt3 = to_decimal("0")
        tot_debt = to_decimal("0")
        i = 0
        curr_counter = 0
        curr_fcurr = ""

        from_date = fdate

        for artikel in db_session.query(Artikel).filter(
                ((Artikel.artart == 2) | (Artikel.artart == 7) | (Artikel.artart == 14)) & (Artikel.artnr >= from_art) & (Artikel.artnr <= to_art) & (Artikel.departement == 0)).order_by(Artikel.artart, Artikel.artnr).all():
            ledger = Ledger()
            ledger_data.append(ledger)

            ledger.artnr = artikel.artnr
            ledger.bezeich = to_string(artikel.artnr) + "  -  " + artikel.bezeich
        curr_art = 0

        for debitor in db_session.query(Debitor).filter(
                (Debitor.rgdatum <= tdate) & (Debitor.artnr >= from_art) & (Debitor.artnr <= to_art) & (Debitor.opart <= 1)).order_by(Debitor.artnr, Debitor.zahlkonto).all():

            guest = get_cache(Guest, {"gastnr": [(eq, debitor.gastnrmember)]})

            if guest:
                bill_name = guest.name + ", " + guest.vorname1 + \
                    guest.anredefirma + " " + guest.anrede1
            else:
                bill_name = ""

            if matches(bill_name, r"*" + from_name + r"*"):

                if curr_art != debitor.artnr:
                    curr_art = debitor.artnr

                    artikel = get_cache(
                        Artikel, {"artnr": [(eq, curr_art)], "departement": [(eq, 0)]})

                if debitor.counter > 0:

                    age_list = query(age_list_data, filters=(
                        lambda age_list: age_list.counter == debitor.counter), first=True)

                if (debitor.counter == 0) or (not age_list):

                    guest = get_cache(
                        Guest, {"gastnr": [(eq, debitor.gastnr)]})
                    age_list = Age_list()
                    age_list_data.append(age_list)

                    age_list.artnr = debitor.artnr
                    age_list.rechnr = debitor.rechnr
                    age_list.rgdatum = debitor.rgdatum
                    age_list.counter = debitor.counter
                    age_list.gastnr = debitor.gastnr
                    age_list.tot_debt = to_decimal("0")
                    age_list.opart = debitor.opart

                    if guest:
                        age_list.credit_limit = to_decimal(guest.kreditlimit)

                    if debitor.betrieb_gastmem == 0:
                        age_list.fcurr = default_fcurr
                    else:

                        waehrung = get_cache(
                            Waehrung, {"waehrungsnr": [(eq, debitor.betrieb_gastmem)]})

                        if waehrung:
                            age_list.fcurr = waehrung.wabkurz

                    if artikel.artart == 2:
                        get_bill_receiver_and_bill_name(debitor.rechnr)
                    else:
                        get_bill_receiver_and_bill_name(debitor.rechnr)

                if disptype == 0:
                    age_list.tot_debt = to_decimal(
                        age_list.tot_debt) + to_decimal(debitor.saldo)
                else:

                    if not cvt_flag:
                        age_list.tot_debt = to_decimal(
                            age_list.tot_debt) + to_decimal(debitor.vesrdep)
                    else:

                        if age_list.fcurr.lower() == (default_fcurr).lower():

                            if debitor.vesrdep != 0:
                                age_list.tot_debt = to_decimal(
                                    age_list.tot_debt) + to_decimal(debitor.vesrdep)

                            else:
                                age_list.tot_debt = to_decimal(
                                    age_list.tot_debt) + to_decimal((debitor.saldo) / to_decimal(dollar_rate))
                        else:
                            age_list.tot_debt = to_decimal(
                                age_list.tot_debt) + to_decimal((debitor.saldo) / to_decimal(dollar_rate))

                if debitor.rgdatum < from_date and debitor.zahlkonto == 0:

                    if disptype == 0:
                        age_list.p_bal = to_decimal(
                            age_list.p_bal) + to_decimal(debitor.saldo)
                    else:

                        if not cvt_flag:
                            age_list.p_bal = to_decimal(
                                age_list.p_bal) + to_decimal(debitor.vesrdep)
                        else:

                            if age_list.fcurr.lower() == (default_fcurr).lower():

                                if debitor.vesrdep != 0:
                                    age_list.p_bal = to_decimal(
                                        age_list.p_bal) + to_decimal(debitor.vesrdep)

                                else:
                                    age_list.p_bal = to_decimal(
                                        age_list.p_bal) + to_decimal((debitor.saldo) / to_decimal(dollar_rate))
                            else:
                                age_list.p_bal = to_decimal(
                                    age_list.p_bal) + to_decimal((debitor.saldo) / to_decimal(dollar_rate))

                if debitor.rgdatum >= from_date and debitor.zahlkonto == 0:

                    if disptype == 0:
                        age_list.debit = to_decimal(
                            age_list.debit) + to_decimal(debitor.saldo)
                    else:

                        if not cvt_flag:
                            age_list.debit = to_decimal(
                                age_list.debit) + to_decimal(debitor.vesrdep)
                        else:

                            if age_list.fcurr.lower() == (default_fcurr).lower():

                                if debitor.vesrdep != 0:
                                    age_list.debit = to_decimal(
                                        age_list.debit) + to_decimal(debitor.vesrdep)

                                else:
                                    age_list.debit = to_decimal(
                                        age_list.debit) + to_decimal((debitor.saldo) / to_decimal(dollar_rate))
                            else:
                                age_list.debit = to_decimal(
                                    age_list.debit) + to_decimal((debitor.saldo) / to_decimal(dollar_rate))

            if debitor.rgdatum < from_date and debitor.zahlkonto != 0:

                if disptype == 0:
                    age_list.p_bal = to_decimal(
                        age_list.p_bal) + to_decimal(debitor.saldo)
                else:

                    if not cvt_flag:
                        age_list.p_bal = to_decimal(
                            age_list.p_bal) + to_decimal(debitor.vesrdep)
                    else:

                        if age_list.fcurr.lower() == (default_fcurr).lower():

                            if debitor.vesrdep != 0:
                                age_list.p_bal = to_decimal(
                                    age_list.p_bal) + to_decimal(debitor.vesrdep)

                            else:
                                age_list.p_bal = to_decimal(
                                    age_list.p_bal) + to_decimal((debitor.saldo) / to_decimal(dollar_rate))
                        else:
                            age_list.p_bal = to_decimal(
                                age_list.p_bal) + to_decimal((debitor.saldo) / to_decimal(dollar_rate))
            else:

                if debitor.rgdatum >= from_date and debitor.zahlkonto != 0:

                    if disptype == 0:
                        age_list.credit = to_decimal(
                            age_list.credit) - to_decimal(debitor.saldo)
                    else:

                        if not cvt_flag:
                            age_list.credit = to_decimal(
                                age_list.credit) - to_decimal(debitor.vesrdep)
                        else:

                            if age_list.fcurr.lower() == (default_fcurr).lower():

                                if debitor.vesrdep != 0:
                                    age_list.credit = to_decimal(
                                        age_list.credit) - to_decimal(debitor.vesrdep)

                                else:
                                    age_list.credit = to_decimal(
                                        age_list.credit) - to_decimal((debitor.saldo) / to_decimal(dollar_rate))
                            else:
                                age_list.credit = to_decimal(
                                    age_list.credit) - to_decimal((debitor.saldo) / to_decimal(dollar_rate))

        for artikel in db_session.query(Artikel).filter(
                ((Artikel.artart == 2) | (Artikel.artart == 7) | (Artikel.artart == 14)) & (Artikel.artnr >= from_art) & (Artikel.artnr <= to_art) & (Artikel.departement == 0)).order_by(Artikel.artnr).all():

            curr_counter = 0

            for debitor in db_session.query(Debitor).filter(
                    (Debitor.artnr == artikel.artnr) & (Debitor.rgdatum <= to_date) & (Debitor.opart == 2) & (Debitor.zahlkonto == 0)).order_by(Debitor._recid).all():

                guest = get_cache(
                    Guest, {"gastnr": [(eq, debitor.gastnrmember)]})

                if guest:
                    bill_name = guest.name + ", " + guest.vorname1 + \
                        guest.anredefirma + " " + guest.anrede1
                else:
                    bill_name = ""

                if matches(bill_name, r"*" + from_name + r"*"):

                    guest = get_cache(
                        Guest, {"gastnr": [(eq, debitor.gastnr)]})
                    age_list = Age_list()
                    age_list_data.append(age_list)

                    age_list.artnr = debitor.artnr
                    age_list.rechnr = debitor.rechnr
                    age_list.rgdatum = debitor.rgdatum
                    age_list.counter = debitor.counter
                    age_list.gastnr = debitor.gastnr
                    age_list.tot_debt = to_decimal(debitor.saldo)
                    age_list.opart = debitor.opart

                    if guest:
                        age_list.credit_limit = to_decimal(guest.kreditlimit)

                    if debitor.betrieb_gastmem == 0:
                        age_list.fcurr = default_fcurr
                    else:

                        waehrung = get_cache(
                            Waehrung, {"waehrungsnr": [(eq, debitor.betrieb_gastmem)]})

                        if waehrung:
                            age_list.fcurr = waehrung.wabkurz

                    if artikel.artart == 2:
                        get_bill_receiver_and_bill_name(debitor.rechnr)
                    else:
                        get_bill_receiver_and_bill_name(debitor.rechnr)

                    if debitor.rgdatum < from_date:

                        if disptype == 0:
                            age_list.p_bal = to_decimal(
                                age_list.p_bal) + to_decimal(debitor.saldo)
                        else:

                            if not cvt_flag:
                                age_list.p_bal = to_decimal(
                                    age_list.p_bal) + to_decimal(debitor.vesrdep)
                            else:

                                if age_list.fcurr.lower() == (default_fcurr).lower():
                                    if debitor.vesrdep != 0:
                                        age_list.p_bal = to_decimal(
                                            age_list.p_bal) + to_decimal(debitor.vesrdep)

                                    else:
                                        age_list.p_bal = to_decimal(
                                            age_list.p_bal) + to_decimal((debitor.saldo) / to_decimal(dollar_rate))
                                else:
                                    age_list.p_bal = to_decimal(
                                        age_list.p_bal) + to_decimal((debitor.saldo) / to_decimal(dollar_rate))

                    elif debitor.rgdatum >= from_date:

                        if disptype == 0:
                            age_list.debit = to_decimal(
                                age_list.debit) + to_decimal(debitor.saldo)
                        else:

                            if not cvt_flag:
                                age_list.debit = to_decimal(
                                    age_list.debit) + to_decimal(debitor.vesrdep)
                            else:

                                if age_list.fcurr.lower() == (default_fcurr).lower():
                                    if debitor.vesrdep != 0:
                                        age_list.debit = to_decimal(
                                            age_list.debit) + to_decimal(debitor.vesrdep)

                                    else:
                                        age_list.debit = to_decimal(
                                            age_list.debit) + to_decimal((debitor.saldo) / to_decimal(dollar_rate))
                                else:
                                    age_list.debit = to_decimal(
                                        age_list.debit) + to_decimal((debitor.saldo) / to_decimal(dollar_rate))

                    for debtrec in db_session.query(Debtrec).filter(
                            (Debtrec.counter == debitor.counter) & (Debtrec.rechnr == debitor.rechnr) & (Debtrec.zahlkonto > 0) & (Debtrec.rgdatum <= to_date)).order_by(Debtrec._recid).all():
                        age_list.tot_debt = to_decimal(
                            age_list.tot_debt) + to_decimal(debtrec.saldo)

                        if debtrec.rgdatum < from_date:

                            if disptype == 0:
                                age_list.p_bal = to_decimal(
                                    age_list.p_bal) + to_decimal(debtrec.saldo)
                            else:

                                if not cvt_flag:
                                    age_list.p_bal = to_decimal(
                                        age_list.p_bal) + to_decimal(debtrec.vesrdep)
                                else:

                                    if age_list.fcurr.lower() == (default_fcurr).lower():

                                        if debitor.vesrdep != 0:
                                            age_list.p_bal = to_decimal(
                                                age_list.p_bal) + to_decimal(debitor.vesrdep)

                                        else:
                                            age_list.p_bal = to_decimal(
                                                age_list.p_bal) + to_decimal((debitor.saldo) / to_decimal(dollar_rate))
                                    else:
                                        age_list.p_bal = to_decimal(
                                            age_list.p_bal) + to_decimal((debtrec.saldo) / to_decimal(dollar_rate))

                        elif debtrec.rgdatum >= from_date:

                            if disptype == 0:
                                age_list.credit = to_decimal(
                                    age_list.credit) - to_decimal(debtrec.saldo)
                            else:

                                if not cvt_flag:
                                    age_list.credit = to_decimal(
                                        age_list.credit) - to_decimal(debtrec.vesrdep)
                                else:

                                    if age_list.fcurr.lower() == (default_fcurr).lower():

                                        if debitor.vesrdep != 0:
                                            age_list.credit = to_decimal(
                                                age_list.credit) - to_decimal(debitor.vesrdep)

                                        else:
                                            age_list.credit = to_decimal(
                                                age_list.credit) - to_decimal((debitor.saldo) / to_decimal(dollar_rate))
                                    else:
                                        age_list.credit = to_decimal(
                                            age_list.credit) - to_decimal((debtrec.saldo) / to_decimal(dollar_rate))

        for age_list in query(age_list_data):

            if age_list.p_bal >= - 1 and age_list.p_bal <= 1 and age_list.debit == 0 and age_list.credit == 0:
                age_list_data.remove(age_list)

        if ar_ledger != 0:

            for age_list in query(age_list_data, filters=(lambda age_list: age_list.artnr == ar_ledger)):

                tage_list = query(tage_list_data, filters=(
                    lambda tage_list: tage_list.rechnr == age_list.rechnr), first=True)

                if not tage_list:
                    tage_list = Tage_list()
                    tage_list_data.append(tage_list)

                    buffer_copy(age_list, tage_list)
                else:
                    tage_list.p_bal = to_decimal(
                        tage_list.p_bal) + to_decimal(age_list.p_bal)
                    tage_list.debit = to_decimal(
                        tage_list.debit) + to_decimal(age_list.debit)
                    tage_list.credit = to_decimal(
                        tage_list.credit) + to_decimal(age_list.credit)
                    tage_list.saldo = to_decimal(
                        tage_list.saldo) + to_decimal(age_list.saldo)
                    tage_list.debt0 = to_decimal(
                        tage_list.debt0) + to_decimal(age_list.debt0)
                    tage_list.debt1 = to_decimal(
                        tage_list.debt1) + to_decimal(age_list.debt1)
                    tage_list.debt2 = to_decimal(
                        tage_list.debt2) + to_decimal(age_list.debt2)
                    tage_list.debt3 = to_decimal(
                        tage_list.debt3) + to_decimal(age_list.debt3)
                    tage_list.tot_debt = to_decimal(
                        tage_list.tot_debt) + to_decimal(age_list.tot_debt)

                age_list_data.remove(age_list)

            for tage_list in query(tage_list_data):
                age_list = Age_list()
                age_list_data.append(age_list)

                buffer_copy(tage_list, age_list)
                tage_list_data.remove(tage_list)

        for ledger in query(ledger_data, sort_by=[("artnr", False)]):

            age_list = query(age_list_data, filters=(
                lambda age_list: age_list.artnr == ledger.artnr), first=True)

            if not age_list:
                continue
            outlist = "    " + ledger.bezeich.upper()

            if not mtd_flag and case_type != 1:
                fill_in_list(False, "", None)
            outlist = ""

            if not mtd_flag and case_type != 1:
                fill_in_list(False, "", None)
            counter = 0
            curr_gastnr = 0

            if mi_bill:

                for age_list in query(age_list_data, filters=(lambda age_list: age_list.artnr == ledger.artnr), sort_by=[("rgdatum", False), ("gastname", False)]):
                    create_output()

            else:

                for age_list in query(age_list_data, filters=(lambda age_list: age_list.artnr == ledger.artnr), sort_by=[("gastname", False), ("rechnr", False)]):
                    create_output()

            if counter > 0 and (p_bal != 0 or debit != 0 or credit != 0):

                if not long_digit:
                    outlist = "  " + to_string(counter, ">>>9 ") + \
                        to_string(gastname, "x(30)") + \
                        to_string(billname, "x(30)") + \
                        to_string(tot_debt, "->>,>>>,>>>,>>9.99") + \
                        to_string(p_bal, "->>,>>>,>>>,>>9.99") + \
                        to_string(debit, "->>,>>>,>>>,>>9.99") + \
                        to_string(credit, "->>,>>>,>>>,>>9.99") + \
                        to_string(debt0, "->>,>>>,>>>,>>9.99") + \
                        to_string(debt1, "->>,>>>,>>>,>>9.99") + \
                        to_string(debt2, "->>,>>>,>>>,>>9.99") + \
                        to_string(debt3, "->>,>>>,>>>,>>9.99") + \
                        to_string(credit_limit, "->>,>>>,>>>,>>9.99")
                else:
                    outlist = "  " + to_string(counter, ">>>9 ") + \
                        to_string(gastname, "x(30)") + \
                        to_string(billname, "x(30)") + \
                        to_string(tot_debt, "->,>>>,>>>,>>>,>>9") + \
                        to_string(p_bal, "->,>>>,>>>,>>>,>>9") + \
                        to_string(debit, "->,>>>,>>>,>>>,>>9") + \
                        to_string(credit, "->,>>>,>>>,>>>,>>9") + \
                        to_string(debt0, "->,>>>,>>>,>>>,>>9") + \
                        to_string(debt1, "->,>>>,>>>,>>>,>>9") + \
                        to_string(debt2, "->,>>>,>>>,>>>,>>9") + \
                        to_string(debt3, "->,>>>,>>>,>>>,>>9") + \
                        to_string(credit_limit, "->,>>>,>>>,>>>,>>9")

                if not mtd_flag and case_type != 1:
                    fill_in_list(True, curr_fcurr, curr_rgdatum)
            else:
                counter = counter - 1
            tmp_saldo = to_decimal(ledger.tot_debt)

            if tmp_saldo == 0:
                tmp_saldo = to_decimal("1")
            outlist = "-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------"

            if not mtd_flag and case_type != 1:
                fill_in_list(False, "----", None)

            if not long_digit:
                outlist = "       " + \
                    to_string(translateExtended("T o t a l", lvcarea, ""), "x(30)") + \
                    to_string(translateExtended("T o t a l", lvcarea, ""), "x(30)") + \
                    to_string(ledger.tot_debt, "->>,>>>,>>>,>>9.99") + \
                    to_string(ledger.p_bal, "->>,>>>,>>>,>>9.99") + \
                    to_string(ledger.debit, "->>,>>>,>>>,>>9.99") + \
                    to_string(ledger.credit, "->>,>>>,>>>,>>9.99") + \
                    to_string(ledger.debt0, "->>,>>>,>>>,>>9.99") + \
                    to_string(ledger.debt1, "->>,>>>,>>>,>>9.99") + \
                    to_string(ledger.debt2, "->>,>>>,>>>,>>9.99") + \
                    to_string(ledger.debt3, "->>,>>>,>>>,>>9.99")
            else:
                outlist = "       " + \
                    to_string(translateExtended("T o t a l", lvcarea, ""), "x(30)") + \
                    to_string(translateExtended("T o t a l", lvcarea, ""), "x(30)") + \
                    to_string(ledger.tot_debt, "->,>>>,>>>,>>>,>>9") + \
                    to_string(ledger.p_bal, "->,>>>,>>>,>>>,>>9") + \
                    to_string(ledger.debit, "->,>>>,>>>,>>>,>>9") + \
                    to_string(ledger.credit, "->,>>>,>>>,>>>,>>9") + \
                    to_string(ledger.debt0, "->,>>>,>>>,>>>,>>9") + \
                    to_string(ledger.debt1, "->,>>>,>>>,>>>,>>9") + \
                    to_string(ledger.debt2, "->,>>>,>>>,>>>,>>9") + \
                    to_string(ledger.debt3, "->,>>>,>>>,>>>,>>9")

            if not mtd_flag and case_type != 1:
                fill_in_list(False, "", None)
            outlist = "       " + \
                to_string(translateExtended("Statistic Percentage (%) :", lvcarea, ""), "x(30)") + \
                to_string(translateExtended("Statistic Percentage (%) :", lvcarea, ""), "x(30)") + \
                " 100.00"
            for i in range(1, 55):
                outlist = outlist + "       "
            tot_debt0 = (to_decimal(ledger.debt0) /
                         to_decimal(tmp_saldo) * to_decimal("100"))
            tot_debt1 = (to_decimal(ledger.debt1) /
                         to_decimal(tmp_saldo) * to_decimal("100"))
            tot_debt2 = (to_decimal(ledger.debt2) /
                         to_decimal(tmp_saldo) * to_decimal("100"))
            tot_debt3 = (to_decimal(ledger.debt3) /
                         to_decimal(tmp_saldo) * to_decimal("100"))

            if tot_debt0 == None:
                tot_debt0 = to_decimal("0")

            if tot_debt1 == None:
                tot_debt1 = to_decimal("0")

            if tot_debt2 == None:
                tot_debt2 = to_decimal("0")

            if tot_debt3 == None:
                tot_debt3 = to_decimal("0")
            outlist = outlist + \
                to_string(tot_debt0, "         ->,>>9.99") + \
                to_string(tot_debt1, "         ->,>>9.99") + \
                to_string(tot_debt2, "         ->,>>9.99") + \
                to_string(tot_debt3, "         ->,>>9.99")

            if not mtd_flag and case_type != 1:
                fill_in_list(False, "", None)
            outlist = ""

            if not mtd_flag and case_type != 1:
                fill_in_list(False, "", None)
        outlist = "-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------"

        if not mtd_flag and case_type != 1:
            fill_in_list(False, "----", None)

        if not long_digit:
            outlist = "       " + \
                to_string(translateExtended("T O T A L A/R:", lvcarea, ""), "x(30)") + \
                to_string(translateExtended("T O T A L A/R:", lvcarea, ""), "x(30)") + \
                to_string(t_saldo, "->>,>>>,>>>,>>9.99") + to_string(t_prev, "->>,>>>,>>>,>>9.99") +\
                to_string(t_debit, "->>,>>>,>>>,>>9.99") + \
                to_string(t_credit, "->>,>>>,>>>,>>9.99") + \
                to_string(t_debt0, "->>,>>>,>>>,>>9.99") + \
                to_string(t_debt1, "->>,>>>,>>>,>>9.99") + \
                to_string(t_debt2, "->>,>>>,>>>,>>9.99") + \
                to_string(t_debt3, "->>,>>>,>>>,>>9.99")
        else:
            outlist = "       " + \
                to_string(translateExtended("T O T A L A/R:", lvcarea, ""), "x(30)") + \
                to_string(translateExtended("T O T A L A/R:", lvcarea, ""), "x(30)") + \
                to_string(t_saldo, "->,>>>,>>>,>>>,>>9") + \
                to_string(t_prev, "->,>>>,>>>,>>>,>>9") + \
                to_string(t_debit, "->,>>>,>>>,>>>,>>9") + \
                to_string(t_credit, "->,>>>,>>>,>>>,>>9") + \
                to_string(t_debt0, "->,>>>,>>>,>>>,>>9") + \
                to_string(t_debt1, "->,>>>,>>>,>>>,>>9") + \
                to_string(t_debt2, "->,>>>,>>>,>>>,>>9") + \
                to_string(t_debt3, "->,>>>,>>>,>>>,>>9")

        if not mtd_flag and case_type != 1:
            fill_in_list(False, "", None)
        outlist = "       " + \
            to_string(translateExtended("Statistic Percentage (%) :", lvcarea, ""), "x(30)") + \
            to_string(translateExtended("Statistic Percentage (%) :", lvcarea, ""), "x(30)") + \
            "            100.00"
        for i in range(1, 55):
            outlist = outlist + "       "
        tot_debt0 = (to_decimal(t_debt0) /
                     to_decimal(t_saldo) * to_decimal("100"))
        tot_debt1 = (to_decimal(t_debt1) /
                     to_decimal(t_saldo) * to_decimal("100"))
        tot_debt2 = (to_decimal(t_debt2) /
                     to_decimal(t_saldo) * to_decimal("100"))
        tot_debt3 = (to_decimal(t_debt3) /
                     to_decimal(t_saldo) * to_decimal("100"))

        if tot_debt0 == None:
            tot_debt0 = to_decimal("0")

        if tot_debt1 == None:
            tot_debt1 = to_decimal("0")

        if tot_debt2 == None:
            tot_debt2 = to_decimal("0")

        if tot_debt3 == None:
            tot_debt3 = to_decimal("0")
        outlist = outlist + \
            to_string(tot_debt0, "           ->>9.99") + \
            to_string(tot_debt1, "           ->>9.99") + \
            to_string(tot_debt2, "           ->>9.99") + \
            to_string(tot_debt3, "           ->>9.99")

        if not mtd_flag and case_type != 1:
            fill_in_list(False, "", None)
        outlist = ""

        if not mtd_flag and case_type != 1:
            fill_in_list(False, "", None)

    def get_bill_receiver_and_bill_name(p_rechnr: int):
        nonlocal arage_balance_list_data, curr_art, counter, t_saldo, t_prev, t_debit, t_credit, t_debt0, t_debt1, t_debt2, t_debt3, tmp_saldo, curr_name, curr_gastnr, gastname, billname, p_bal, debit, credit, debt0, debt1, debt2, debt3, credit_limit, curr_counter, curr_fcurr, i, tot_debt, from_date, default_fcurr, outlist, long_digit, curr_rgdatum, bill_number, inp_gastnr, inp_artnr, tot_debtall, tot_debt0, tot_debt1, tot_debt2, tot_debt3, curr_time, lvcarea, debitor, htparam, artikel, guest, waehrung, h_bill, bill, res_line
        nonlocal pvilanguage, case_type, mtd_flag, to_date, fdate, tdate, from_art, to_art, from_name, to_name, disptype, mi_bill, day1, day2, day3, detailed, cvt_flag, dollar_rate
        nonlocal debtrec, debt
        nonlocal arage_balance_list, arage_list, age_list, ledger, debtrec, debt
        nonlocal arage_balance_list_data, arage_list_data, age_list_data, ledger_data

        guestname: string = ""
        guestvorname1: string = ""
        guestandrefirma: string = ""
        guestanrede1: string = ""
        guestname = guest.name
        guestvorname1 = guest.vorname1
        guestandrefirma = guest.anredefirma
        guestanrede1 = guest.anrede1

        if guestname == None:
            guestname = ""

        if guestvorname1 == None:
            guestvorname1 = ""

        if guestandrefirma == None:
            guestandrefirma = ""

        if guestanrede1 == None:
            guestanrede1 = ""

        if p_rechnr == 0:
            age_list.gastname = substring(f"{guestname}, {guestvorname1}{guestandrefirma} {guestanrede1}", 0, 30)

            guest = get_cache(Guest, {"gastnr": [(eq, debitor.gastnrmember)]})

            if guest:
                age_list.billname = substring(f"{guestname}, {guestvorname1}{guestandrefirma} {guestanrede1}", 0 , 30)
            else:
                age_list.billname = ""
        else:
            age_list.gastname = substring(f"{guestname}, {guestvorname1}{guestandrefirma} {guestanrede1}", 0, 30)

            h_bill = get_cache(H_bill, {"rechnr": [(eq, p_rechnr)]})

            if not h_bill:

                bill = get_cache(Bill, {"rechnr": [(eq, p_rechnr)]})

                if bill:

                    res_line = get_cache(
                        Res_line, {"resnr": [(eq, bill.resnr)]})

                    if res_line:
                        age_list.billname = res_line.name
                else:
                    age_list.billname = ""
            else:
                age_list.billname = ""

    htparam = get_cache(Htparam, {"paramnr": [(eq, 144)]})
    default_fcurr = htparam.fchar

    htparam = get_cache(Htparam, {"paramnr": [(eq, 1051)]})

    if htparam:
        ar_ledger = htparam.finteger

    if mtd_flag:
        if case_type == 1:
            age_list1()
        else:
            age_list2()
    else:
        if case_type == 1:
            age_list1a()
        else:
            age_list2a()
    arage_balance_list_data.clear()

    for arage_list in query(arage_list_data):
        if substring(arage_list.str, 0, 7) != ("-------"):
            arage_balance_list = Arage_balance_list()
            arage_balance_list_data.append(arage_balance_list)

            arage_balance_list.strdate = arage_list.strdate
            arage_balance_list.curr = arage_list.curr
            arage_balance_list.gastnr = arage_list.gastnr
            arage_balance_list.artnr = arage_list.artnr
            arage_balance_list.age1 = arage_list.age1
            arage_balance_list.age2 = arage_list.age2
            arage_balance_list.age3 = arage_list.age3
            arage_balance_list.age4 = arage_list.age4
            arage_balance_list.rechnr = arage_list.rechnr
            
            # log_program.write_log("LOG", f"arange_list.str: {arage_list.str}")
            arage_balance_list.num = substring(arage_list.str, 0, 6)
            arage_balance_list.cust_nm = substring(arage_list.str, 6, 30)
            arage_balance_list.bill_nm = substring(arage_list.str, 56, 30)
            arage_balance_list.p_bal = substring(arage_list.str, 85, 18)
            arage_balance_list.debit = substring(arage_list.str, 105, 18)
            arage_balance_list.credit = substring(arage_list.str, 123, 18)
            arage_balance_list.end_bal = substring(arage_list.str, 67, 18)
            arage_balance_list.creditlimit_str = substring(arage_list.str, 203, 18)            

    arage_balance_list = query(arage_balance_list_data, first=True)

    if arage_balance_list:

        return generate_output()
    else:

        return generate_output()

    return generate_output()
