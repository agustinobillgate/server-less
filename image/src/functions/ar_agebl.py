from functions.additional_functions import *
import decimal
from datetime import date
from models import Htparam, Debitor, Artikel, Guest, Waehrung

def ar_agebl(pvilanguage:int, from_art:int, to_art:int, to_date:date, from_name:str, to_name:str, disptype:int):
    outlist = ""
    output_list_list = []
    lvcarea:str = "ar_age"
    default_fcurr:str = ""
    day1:int = 30
    day2:int = 30
    day3:int = 30
    price_decimal:int = 0
    long_digit:bool = False
    htparam = debitor = artikel = guest = waehrung = None

    ledger = age_list = output_list = debt = None

    ledger_list, Ledger = create_model("Ledger", {"artnr":int, "bezeich":str, "debt0":decimal, "debt1":decimal, "debt2":decimal, "debt3":decimal, "tot_debt":decimal})
    age_list_list, Age_list = create_model("Age_list", {"artnr":int, "rechnr":int, "counter":int, "gastnr":int, "creditlimit":decimal, "rgdatum":date, "gastname":str, "saldo":decimal, "debt0":decimal, "debt1":decimal, "debt2":decimal, "debt3":decimal, "tot_debt":decimal, "fcurr":str})
    output_list_list, Output_list = create_model("Output_list", {"curr":str, "gastnr":int, "age1":str, "age2":str, "age3":str, "age4":str, "creditlimit":decimal, "str":str})

    Debt = Debitor

    db_session = local_storage.db_session

    def generate_output():
        nonlocal outlist, output_list_list, lvcarea, default_fcurr, day1, day2, day3, price_decimal, long_digit, htparam, debitor, artikel, guest, waehrung
        nonlocal debt


        nonlocal ledger, age_list, output_list, debt
        nonlocal ledger_list, age_list_list, output_list_list
        return {"outlist": outlist, "output-list": output_list_list}

    def age_list():

        nonlocal outlist, output_list_list, lvcarea, default_fcurr, day1, day2, day3, price_decimal, long_digit, htparam, debitor, artikel, guest, waehrung
        nonlocal debt


        nonlocal ledger, age_list, output_list, debt
        nonlocal ledger_list, age_list_list, output_list_list

        curr_art:int = 0
        billdate:date = None
        ct:int = 0
        t_debet:decimal = 0
        t_credit:decimal = 0
        t_comm:decimal = 0
        t_adjust:decimal = 0
        t_saldo:decimal = 0
        t_debt0:decimal = 0
        t_debt1:decimal = 0
        t_debt2:decimal = 0
        t_debt3:decimal = 0
        tmp_saldo:decimal = 0
        curr_name:str = ""
        curr_gastnr:int = 0
        creditlimit:decimal = 0
        gastname:str = ""
        debt0:decimal = 0
        debt1:decimal = 0
        debt2:decimal = 0
        debt3:decimal = 0
        tot_debt:decimal = 0
        ar_saldo:decimal = 0
        fcurr:int = 0
        curr_fcurr:str = ""
        balance:decimal = 0
        Debt = Debitor
        ledger_list.clear()
        age_list_list.clear()
        output_list_list.clear()

        for artikel in db_session.query(Artikel).filter(
                ((Artikel.artart == 2) |  (Artikel.artart == 7)) &  (Artikel.artnr >= from_art) &  (Artikel.artnr <= to_art) &  (Artikel.departement == 0)).all():
            ledger = Ledger()
            ledger_list.append(ledger)

            ledger.artnr = artikel.artnr
            ledger.bezeich = to_string(artikel.artnr) + "  -  " + artikel.bezeich
        curr_art = 0

        for debitor in db_session.query(Debitor).filter(
                (Debitor.artnr >= from_art) &  (Debitor.artnr <= to_art) &  (Debitor.rgdatum <= to_date) &  (Debitor.opart == 0)).all():

            if debitor.name.lower()  >= (from_name).lower()  and debitor.name.lower()  <= (to_name).lower() :

                if curr_art != debitor.artnr:
                    curr_art = debitor.artnr

                    artikel = db_session.query(Artikel).filter(
                            (Artikel.artnr == curr_art) &  (Artikel.departement == 0)).first()

                if disptype == 0:
                    ar_saldo = debitor.saldo
                else:
                    ar_saldo = debitor.vesrdep

                if debitor.counter != 0:

                    if disptype == 0:

                        for debt in db_session.query(Debt).filter(
                                (Debt.rechnr == debitor.rechnr) &  (Debt.counter == debitor.counter) &  (Debt.opart == 1) &  (Debt.zahlkonto != 0) &  (Debt.rgdatum <= to_date)).all():
                            ar_saldo = ar_saldo + debt.saldo

                    else:

                        for debt in db_session.query(Debt).filter(
                                (Debt.rechnr == debitor.rechnr) &  (Debt.counter == debitor.counter) &  (Debt.opart == 1) &  (Debt.zahlkonto != 0) &  (Debt.debitor.betrieb_gastmem == debitor.betrieb_gastmem) &  (Debt.rgdatum <= to_date)).all():
                            ar_saldo = ar_saldo + debt.vesrdep


                guest = db_session.query(Guest).filter(
                        (Guest.gastnr == debitor.gastnr)).first()
                age_list = Age_list()
                age_list_list.append(age_list)

                age_list.artnr = debitor.artnr
                age_list.rechnr = debitor.rechnr
                age_list.rgdatum = debitor.rgdatum
                age_list.counter = debitor.counter
                age_list.gastnr = debitor.gastnr
                age_list.creditlimit = guest.kreditlimit
                age_list.tot_debt = ar_saldo

                if debitor.betrieb_gastmem == 0:
                    age_list.fcurr = default_fcurr
                else:

                    waehrung = db_session.query(Waehrung).filter(
                            (Waehrungsnr == debitor.betrieb_gastmem)).first()

                    if waehrung:
                        age_list.fcurr = waehrung.wabkurz

                if artikel.artart == 2:
                    age_list.gastname = guest.name + ", " + guest.vorname1 + guest.anredefirma + " " + guest.anrede1
                    age_list.creditlimit = guest.kreditlimit
                else:
                    age_list.creditlimit = 0

                    htparam = db_session.query(Htparam).filter(
                            (Htparam.paramnr == 867)).first()

                    if debitor.gastnr == htparam.finteger:
                        age_list.gastname = "F&B " + artikel.bezeich
                    else:
                        age_list.gastname = "F/O " + artikel.bezeich

                if to_date - age_list.rgdatum > day3:
                    age_list.debt3 = age_list.debt3 + ar_saldo

                elif to_date - age_list.rgdatum > day2:
                    age_list.debt2 = age_list.debt2 + ar_saldo

                elif to_date - age_list.rgdatum > day1:
                    age_list.debt1 = age_list.debt1 + ar_saldo
                else:
                    age_list.debt0 = age_list.debt0 + ar_saldo
        curr_art = 0

        for debitor in db_session.query(Debitor).filter(
                (Debitor.artnr >= from_art) &  (Debitor.artnr <= to_art) &  (Debitor.rgdatum <= to_date) &  (Debitor.opart == 2) &  (Debitor.zahlkonto == 0)).all():

            debt = db_session.query(Debt).filter(
                    (Debt.rechnr == debitor.rechnr) &  (Debt.counter == debitor.counter) &  (Debt.opart == 2) &  (Debt.zahlkonto != 0) &  (Debt.rgdatum > to_date)).first()

            if debt and debitor.name.lower()  >= (from_name).lower()  and debitor.name.lower()  <= (to_name).lower() :

                if curr_art != debitor.artnr:
                    curr_art = debitor.artnr

                    artikel = db_session.query(Artikel).filter(
                            (Artikel.artnr == curr_art) &  (Artikel.departement == 0)).first()

                if disptype == 0:
                    ar_saldo = debitor.saldo
                else:
                    ar_saldo = debitor.vesrdep

                if disptype == 0:

                    for debt in db_session.query(Debt).filter(
                            (Debt.rechnr == debitor.rechnr) &  (Debt.counter == debitor.counter) &  (Debt.opart == 2) &  (Debt.zahlkonto != 0) &  (Debt.rgdatum <= to_date)).all():
                        ar_saldo = ar_saldo + debt.saldo

                else:

                    for debt in db_session.query(Debt).filter(
                            (Debt.rechnr == debitor.rechnr) &  (Debt.counter == debitor.counter) &  (Debt.opart == 2) &  (Debt.zahlkonto != 0) &  (Debt.rgdatum <= to_date) &  (Debt.debitor.betrieb_gastmem == debitor.betrieb_gastmem)).all():
                        ar_saldo = ar_saldo + debt.vesrdep


                guest = db_session.query(Guest).filter(
                        (Guest.gastnr == debitor.gastnr)).first()
                age_list = Age_list()
                age_list_list.append(age_list)

                age_list.artnr = debitor.artnr
                age_list.rechnr = debitor.rechnr
                age_list.rgdatum = debitor.rgdatum
                age_list.counter = debitor.counter
                age_list.gastnr = debitor.gastnr
                age_list.creditlimit = guest.kreditlimit
                age_list.tot_debt = ar_saldo

                if debitor.betrieb_gastmem == 0:
                    age_list.fcurr = default_fcurr
                else:

                    waehrung = db_session.query(Waehrung).filter(
                            (Waehrungsnr == debitor.betrieb_gastmem)).first()

                    if waehrung:
                        age_list.fcurr = waehrung.wabkurz

                if artikel.artart == 2:
                    age_list.gastname = guest.name + ", " + guest.vorname1 + guest.anredefirma + " " + guest.anrede1
                    age_list.creditlimit = guest.kreditlimit
                else:
                    age_list.creditlimit = 0

                    htparam = db_session.query(Htparam).filter(
                            (Htparam.paramnr == 867)).first()

                    if debitor.gastnr == htparam.finteger:
                        age_list.gastname = "F&B " + artikel.bezeich
                    else:
                        age_list.gastname = "F/O " + artikel.bezeich

                if to_date - age_list.rgdatum > day3:
                    age_list.debt3 = age_list.debt3 + ar_saldo

                elif to_date - age_list.rgdatum > day2:
                    age_list.debt2 = age_list.debt2 + ar_saldo

                elif to_date - age_list.rgdatum > day1:
                    age_list.debt1 = age_list.debt1 + ar_saldo
                else:
                    age_list.debt0 = age_list.debt0 + ar_saldo

        for ledger in query(ledger_list):

            artikel = db_session.query(Artikel).filter(
                    (Artikel.artnr == ledger.artnr) &  (Artikel.departement == 0)).first()
            outlist = "    " + ledger.bezeich.upper()
            fill_in_list(0, "")
            outlist = ""
            fill_in_list(0, "")
            ct = 0
            curr_gastnr = 0
            creditlimit = 0
            curr_fcurr = ""

            for age_list in query(age_list_list, filters=(lambda age_list :age_list.artnr == ledger.artnr and age_list.tot_debt != 0)):
                ledger.tot_debt = ledger.tot_debt + age_list.tot_debt
                ledger.debt0 = ledger.debt0 + age_list.debt0
                ledger.debt1 = ledger.debt1 + age_list.debt1
                ledger.debt2 = ledger.debt2 + age_list.debt2
                ledger.debt3 = ledger.debt3 + age_list.debt3
                t_saldo = t_saldo + age_list.tot_debt
                t_debt0 = t_debt0 + age_list.debt0
                t_debt1 = t_debt1 + age_list.debt1
                t_debt2 = t_debt2 + age_list.debt2
                t_debt3 = t_debt3 + age_list.debt3

                if curr_gastnr == 0:
                    gastname = age_list.gastname
                    creditlimit = age_list.creditlimit
                    tot_debt = age_list.tot_debt
                    debt0 = age_list.debt0
                    debt1 = age_list.debt1
                    debt2 = age_list.debt2
                    debt3 = age_list.debt3
                    ct = ct + 1

                elif curr_name != age_list.gastname:

                    if price_decimal == 0:

                        if not long_digit:
                            outlist = "  " + to_string(ct, ">>>9") + "  " + to_string(gastname, "x(34)") + "  " + to_string(tot_debt, "->>>,>>>,>>9.99") + "  " + to_string(debt0, "->>>,>>>,>>9.99") + "  " + to_string(debt1, "->>>,>>>,>>9.99") + "  " + to_string(debt2, "->>>,>>>,>>9.99") + "  " + to_string(debt3, "->>>,>>>,>>9.99") + "  "
                        else:
                            outlist = "  " + to_string(ct, ">>>9") + "  " + to_string(gastname, "x(34)") + "  " + to_string(tot_debt, "->>>>,>>>,>>>,>>9") + to_string(debt0, "->>>>,>>>,>>>,>>9") + to_string(debt1, "->>>>,>>>,>>>,>>9") + to_string(debt2, "->>>>,>>>,>>>,>>9") + to_string(debt3, "->>>>,>>>,>>>,>>9")
                    else:
                        outlist = "  " + to_string(ct, ">>>9") + "  " + to_string(gastname, "x(34)") + "  " + to_string(tot_debt, "->>>,>>>,>>9.99") + "  " + to_string(debt0, "->>>,>>>,>>9.99") + "  " + to_string(debt1, "->>>,>>>,>>9.99") + "  " + to_string(debt2, "->>>,>>>,>>9.99") + "  " + to_string(debt3, "->>>,>>>,>>9.99") + "  "

                    if artikel.artart == 2:
                        fill_in_list(age_list.gastnr, age_list.fcurr)
                    else:
                        fill_in_list(0, "")
                    output_list.creditlimit = creditlimit
                    creditlimit = age_list.creditlimit
                    gastname = age_list.gastname
                    tot_debt = age_list.tot_debt
                    debt0 = age_list.debt0
                    debt1 = age_list.debt1
                    debt2 = age_list.debt2
                    debt3 = age_list.debt3
                    ct = ct + 1


                else:
                    tot_debt = tot_debt + age_list.tot_debt
                    debt0 = debt0 + age_list.debt0
                    debt1 = debt1 + age_list.debt1
                    debt2 = debt2 + age_list.debt2
                    debt3 = debt3 + age_list.debt3


                curr_gastnr = age_list.gastnr
                curr_name = age_list.gastname
                curr_fcurr = age_list.fcurr
                age_list_list.remove(age_list)

            if ct > 0:

                if price_decimal == 0:

                    if not long_digit:
                        outlist = "  " + to_string(ct, ">>>9") + "  " + to_string(gastname, "x(34)") + "  " + to_string(tot_debt, "->>>,>>>,>>9.99") + "  " + to_string(debt0, "->>>,>>>,>>9.99") + "  " + to_string(debt1, "->>>,>>>,>>9.99") + "  " + to_string(debt2, "->>>,>>>,>>9.99") + "  " + to_string(debt3, "->>>,>>>,>>9.99") + "  "
                    else:
                        outlist = "  " + to_string(ct, ">>>9") + "  " + to_string(gastname, "x(34)") + "  " + to_string(tot_debt, "->>>>,>>>,>>>,>>9") + to_string(debt0, "->>>>,>>>,>>>,>>9") + to_string(debt1, "->>>>,>>>,>>>,>>9") + to_string(debt2, "->>>>,>>>,>>>,>>9") + to_string(debt3, "->>>>,>>>,>>>,>>9")
                else:
                    outlist = "  " + to_string(ct, ">>>9") + "  " + to_string(gastname, "x(34)") + "  " + to_string(tot_debt, "->>>,>>>,>>9.99") + "  " + to_string(debt0, "->>>,>>>,>>9.99") + "  " + to_string(debt1, "->>>,>>>,>>9.99") + "  " + to_string(debt2, "->>>,>>>,>>9.99") + "  " + to_string(debt3, "->>>,>>>,>>9.99") + "  "

                if artikel.artart == 2:
                    fill_in_list(curr_gastnr, curr_fcurr)
                else:
                    fill_in_list(0, "")
                output_list.creditlimit = creditlimit
            tmp_saldo = ledger.tot_debt

            if tmp_saldo == 0:
                tmp_saldo = 1
            outlist = fill("-", 170)
            fill_in_list(0, "----")

            if price_decimal == 0:

                if not long_digit:
                    outlist = "                             T o t a l      " + to_string(ledger.tot_debt, "->>>,>>>,>>9.99") + "  " + to_string(ledger.debt0, "->>>,>>>,>>9.99") + "  " + to_string(ledger.debt1, "->>>,>>>,>>9.99") + "  " + to_string(ledger.debt2, "->>>,>>>,>>9.99") + "  " + to_string(ledger.debt3, "->>>,>>>,>>9.99")
                else:
                    outlist = "                             T o t a l      " + to_string(ledger.tot_debt, "->>>>,>>>,>>>,>>9") + to_string(ledger.debt0, "->>>>,>>>,>>>,>>9") + to_string(ledger.debt1, "->>>>,>>>,>>>,>>9") + to_string(ledger.debt2, "->>>>,>>>,>>>,>>9") + to_string(ledger.debt3, "->>>>,>>>,>>>,>>9")
            else:
                outlist = "                             T o t a l      " + to_string(ledger.tot_debt, "->>>,>>>,>>9.99") + "  " + to_string(ledger.debt0, "->>>,>>>,>>9.99") + "  " + to_string(ledger.debt1, "->>>,>>>,>>9.99") + "  " + to_string(ledger.debt2, "->>>,>>>,>>9.99") + "  " + to_string(ledger.debt3, "->>>,>>>,>>9.99")
            fill_in_list(0, "")

            if not long_digit:
                outlist = to_string(translateExtended ("        Statistic Percentage (%):", lvcarea, "") , "x(34)") + "               " + to_string((ledger.tot_debt / tmp_saldo * 100) , "->>,>>9.99") + "       " + to_string((ledger.debt0 / tmp_saldo * 100) , "->>,>>9.99") + "       " + to_string((ledger.debt1 / tmp_saldo * 100) , "->>,>>9.99") + "       " + to_string((ledger.debt2 / tmp_saldo * 100) , "->>,>>9.99") + "       " + to_string((ledger.debt3 / tmp_saldo * 100) , "->>,>>9.99")
            else:
                outlist = to_string(translateExtended ("        Statistic Percentage (%):", lvcarea, "") , "x(34)") + "                 " + to_string((ledger.tot_debt / tmp_saldo * 100) , "->>,>>9.99") + "       " + to_string((ledger.debt0 / tmp_saldo * 100) , "->>,>>9.99") + "       " + to_string((ledger.debt1 / tmp_saldo * 100) , "->>,>>9.99") + "       " + to_string((ledger.debt2 / tmp_saldo * 100) , "->>,>>9.99") + "       " + to_string((ledger.debt3 / tmp_saldo * 100) , "->>,>>9.99")
            fill_in_list(0, "")
            outlist = ""
            fill_in_list(0, "")
        outlist = "-----------------------------------------------------------------------------------------------------------------------------------------------------------"
        fill_in_list(0, "----")

        if price_decimal == 0:

            if not long_digit:
                outlist = to_string(translateExtended ("           T O T A L  A/R:", lvcarea, "") , "x(26)") + "                  " + to_string(t_saldo, "->>>,>>>,>>9.99") + "  " + to_string(t_debt0, "->>>,>>>,>>9.99") + "  " + to_string(t_debt1, "->>>,>>>,>>9.99") + "  " + to_string(t_debt2, "->>>,>>>,>>9.99") + "  " + to_string(t_debt3, "->>>,>>>,>>9.99")
            else:
                outlist = to_string(translateExtended ("           T O T A L  A/R:", lvcarea, "") , "x(26)") + "                  " + to_string(t_saldo, "->>>>,>>>,>>>,>>9") + to_string(t_debt0, "->>>>,>>>,>>>,>>9") + to_string(t_debt1, "->>>>,>>>,>>>,>>9") + to_string(t_debt2, "->>>>,>>>,>>>,>>9") + to_string(t_debt3, "->>>>,>>>,>>>,>>9")
        else:
            outlist = to_string(translateExtended ("           T O T A L  A/R:", lvcarea, "") , "x(26)") + "                  " + to_string(t_saldo, "->>>,>>>,>>9.99") + "  " + to_string(t_debt0, "->>>,>>>,>>9.99") + "  " + to_string(t_debt1, "->>>,>>>,>>9.99") + "  " + to_string(t_debt2, "->>>,>>>,>>9.99") + "  " + to_string(t_debt3, "->>>,>>>,>>9.99")
        fill_in_list(0, "")
        outlist = ""
        fill_in_list(0, "")

        if not long_digit:
            outlist = to_string(translateExtended ("        Statistic Percentage (%):", lvcarea, "") , "x(34)") + "                " + "100.00" + "       " + to_string((t_debt0 / t_saldo * 100) , "->>,>>9.99") + "       " + to_string((t_debt1 / t_saldo * 100) , "->>,>>9.99") + "       " + to_string((t_debt2 / t_saldo * 100) , "->>,>>9.99") + "       " + to_string((t_debt3 / t_saldo * 100) , "->>,>>9.99")
        else:
            outlist = to_string(translateExtended ("        Statistic Percentage (%):", lvcarea, "") , "x(34)") + "                  " + "100.00" + "       " + to_string((t_debt0 / t_saldo * 100) , "->>,>>9.99") + "       " + to_string((t_debt1 / t_saldo * 100) , "->>,>>9.99") + "       " + to_string((t_debt2 / t_saldo * 100) , "->>,>>9.99") + "       " + to_string((t_debt3 / t_saldo * 100) , "->>,>>9.99")
        fill_in_list(0, "")
        outlist = ""
        fill_in_list(0, "")

    def age_lista():

        nonlocal outlist, output_list_list, lvcarea, default_fcurr, day1, day2, day3, price_decimal, long_digit, htparam, debitor, artikel, guest, waehrung
        nonlocal debt


        nonlocal ledger, age_list, output_list, debt
        nonlocal ledger_list, age_list_list, output_list_list

        curr_art:int = 0
        billdate:date = None
        ct:int = 0
        t_debet:decimal = 0
        t_credit:decimal = 0
        t_comm:decimal = 0
        t_adjust:decimal = 0
        t_saldo:decimal = 0
        t_debt0:decimal = 0
        t_debt1:decimal = 0
        t_debt2:decimal = 0
        t_debt3:decimal = 0
        tmp_saldo:decimal = 0
        curr_name:str = ""
        curr_gastnr:int = 0
        creditlimit:decimal = 0
        gastname:str = ""
        debt0:decimal = 0
        debt1:decimal = 0
        debt2:decimal = 0
        debt3:decimal = 0
        tot_debt:decimal = 0
        fcurr:int = 0
        curr_fcurr:str = ""
        balance:decimal = 0
        ar_saldo:decimal = 0
        Debt = Debitor
        ledger_list.clear()
        age_list_list.clear()
        output_list_list.clear()

        for artikel in db_session.query(Artikel).filter(
                ((Artikel.artart == 2) |  (Artikel.artart == 7)) &  (Artikel.artnr >= from_art) &  (Artikel.artnr <= to_art) &  (Artikel.departement == 0)).all():
            ledger = Ledger()
            ledger_list.append(ledger)

            ledger.artnr = artikel.artnr
            ledger.bezeich = to_string(artikel.artnr) + "  -  " + artikel.bezeich
        curr_art = 0

        for debitor in db_session.query(Debitor).filter(
                (Debitor.artnr >= from_art) &  (Debitor.artnr <= to_art) &  (Debitor.rgdatum <= to_date) &  (Debitor.opart == 0)).all():

            if debitor.name.lower()  >= (from_name).lower() :

                if curr_art != debitor.artnr:
                    curr_art = debitor.artnr

                    artikel = db_session.query(Artikel).filter(
                            (Artikel.artnr == curr_art) &  (Artikel.departement == 0)).first()

                if disptype == 1:
                    ar_saldo = debitor.vesrdep


                else:
                    ar_saldo = debitor.saldo

                if debitor.counter != 0:

                    if disptype == 0:

                        for debt in db_session.query(Debt).filter(
                                (Debt.rechnr == debitor.rechnr) &  (Debt.counter == debitor.counter) &  (Debt.opart == 1) &  (Debt.zahlkonto != 0) &  (Debt.rgdatum <= to_date)).all():

                            if disptype == 0:
                                ar_saldo = ar_saldo + debt.saldo
                            else:
                                ar_saldo = ar_saldo + debt.vesrdep

                    else:

                        for debt in db_session.query(Debt).filter(
                                (Debt.rechnr == debitor.rechnr) &  (Debt.counter == debitor.counter) &  (Debt.opart == 1) &  (Debt.zahlkonto != 0) &  (Debt.debitor.betrieb_gastmem == debitor.betrieb_gastmem) &  (Debt.rgdatum <= to_date)).all():
                            ar_saldo = ar_saldo + debt.vesrdep


                guest = db_session.query(Guest).filter(
                        (Guest.gastnr == debitor.gastnr)).first()
                age_list = Age_list()
                age_list_list.append(age_list)

                age_list.artnr = debitor.artnr
                age_list.rechnr = debitor.rechnr
                age_list.rgdatum = debitor.rgdatum
                age_list.counter = debitor.counter
                age_list.gastnr = debitor.gastnr
                age_list.creditlimit = guest.kreditlimit
                age_list.tot_debt = ar_saldo

                if debitor.betrieb_gastmem == 0:
                    age_list.fcurr = default_fcurr
                else:

                    waehrung = db_session.query(Waehrung).filter(
                            (Waehrungsnr == debitor.betrieb_gastmem)).first()

                    if waehrung:
                        age_list.fcurr = waehrung.wabkurz

                if artikel.artart == 2:
                    age_list.gastname = guest.name + ", " + guest.vorname1 + guest.anredefirma + " " + guest.anrede1
                    age_list.creditlimit = guest.kreditlimit
                else:
                    age_list.creditlimit = 0

                    htparam = db_session.query(Htparam).filter(
                            (Htparam.paramnr == 867)).first()

                    if debitor.gastnr == htparam.finteger:
                        age_list.gastname = "F&B " + artikel.bezeich
                    else:
                        age_list.gastname = "F/O " + artikel.bezeich

                if to_date - age_list.rgdatum > day3:
                    age_list.debt3 = age_list.debt3 + ar_saldo

                elif to_date - age_list.rgdatum > day2:
                    age_list.debt2 = age_list.debt2 + ar_saldo

                elif to_date - age_list.rgdatum > day1:
                    age_list.debt1 = age_list.debt1 + ar_saldo
                else:
                    age_list.debt0 = age_list.debt0 + ar_saldo
        curr_art = 0

        for debitor in db_session.query(Debitor).filter(
                (Debitor.artnr >= from_art) &  (Debitor.artnr <= to_art) &  (Debitor.rgdatum <= to_date) &  (Debitor.opart == 2) &  (Debitor.zahlkonto == 0)).all():

            debt = db_session.query(Debt).filter(
                    (Debt.rechnr == debitor.rechnr) &  (Debt.counter == debitor.counter) &  (Debt.opart == 2) &  (Debt.zahlkonto != 0) &  (Debt.rgdatum > to_date)).first()

            if debt and debitor.name.lower()  >= (from_name).lower() :

                if curr_art != debitor.artnr:
                    curr_art = debitor.artnr

                    artikel = db_session.query(Artikel).filter(
                            (Artikel.artnr == curr_art) &  (Artikel.departement == 0)).first()

                if disptype == 0:
                    ar_saldo = debitor.saldo
                else:
                    ar_saldo = debitor.vesrdep

                if disptype == 0:

                    for debt in db_session.query(Debt).filter(
                            (Debt.rechnr == debitor.rechnr) &  (Debt.counter == debitor.counter) &  (Debt.opart == 2) &  (Debt.zahlkonto != 0) &  (Debt.rgdatum <= to_date)).all():
                        ar_saldo = ar_saldo + debt.saldo

                else:

                    for debt in db_session.query(Debt).filter(
                            (Debt.rechnr == debitor.rechnr) &  (Debt.counter == debitor.counter) &  (Debt.opart == 2) &  (Debt.zahlkonto != 0) &  (Debt.rgdatum <= to_date) &  (Debt.debitor.betrieb_gastmem == debitor.betrieb_gastmem)).all():
                        ar_saldo = ar_saldo + debt.vesrdep


                guest = db_session.query(Guest).filter(
                        (Guest.gastnr == debitor.gastnr)).first()
                age_list = Age_list()
                age_list_list.append(age_list)

                age_list.artnr = debitor.artnr
                age_list.rechnr = debitor.rechnr
                age_list.rgdatum = debitor.rgdatum
                age_list.counter = debitor.counter
                age_list.gastnr = debitor.gastnr
                age_list.creditlimit = guest.kreditlimit
                age_list.tot_debt = ar_saldo

                if debitor.betrieb_gastmem == 0:
                    age_list.fcurr = default_fcurr
                else:

                    waehrung = db_session.query(Waehrung).filter(
                            (Waehrungsnr == debitor.betrieb_gastmem)).first()

                    if waehrung:
                        age_list.fcurr = waehrung.wabkurz

                if artikel.artart == 2:
                    age_list.gastname = guest.name + ", " + guest.vorname1 + guest.anredefirma + " " + guest.anrede1
                    age_list.creditlimit = guest.kreditlimit
                else:
                    age_list.creditlimit = 0

                    htparam = db_session.query(Htparam).filter(
                            (Htparam.paramnr == 867)).first()

                    if debitor.gastnr == htparam.finteger:
                        age_list.gastname = "F&B " + artikel.bezeich
                    else:
                        age_list.gastname = "F/O " + artikel.bezeich

                if to_date - age_list.rgdatum > day3:
                    age_list.debt3 = age_list.debt3 + ar_saldo

                elif to_date - age_list.rgdatum > day2:
                    age_list.debt2 = age_list.debt2 + ar_saldo

                elif to_date - age_list.rgdatum > day1:
                    age_list.debt1 = age_list.debt1 + ar_saldo
                else:
                    age_list.debt0 = age_list.debt0 + ar_saldo

        for ledger in query(ledger_list):
            outlist = "   " + ledger.bezeich.upper()
            fill_in_list(0, "")
            outlist = ""
            fill_in_list(0, "")
            ct = 0
            curr_gastnr = 0
            creditlimit = 0

            for age_list in query(age_list_list, filters=(lambda age_list :age_list.artnr == ledger.artnr and age_list.tot_debt != 0)):
                ledger.tot_debt = ledger.tot_debt + age_list.tot_debt
                ledger.debt0 = ledger.debt0 + age_list.debt0
                ledger.debt1 = ledger.debt1 + age_list.debt1
                ledger.debt2 = ledger.debt2 + age_list.debt2
                ledger.debt3 = ledger.debt3 + age_list.debt3
                t_saldo = t_saldo + age_list.tot_debt
                t_debt0 = t_debt0 + age_list.debt0
                t_debt1 = t_debt1 + age_list.debt1
                t_debt2 = t_debt2 + age_list.debt2
                t_debt3 = t_debt3 + age_list.debt3

                if curr_gastnr == 0:
                    gastname = age_list.gastname
                    creditlimit = age_list.creditlimit
                    tot_debt = age_list.tot_debt
                    debt0 = age_list.debt0
                    debt1 = age_list.debt1
                    debt2 = age_list.debt2
                    debt3 = age_list.debt3
                    ct = ct + 1

                elif curr_name != age_list.gastname:

                    if price_decimal == 0:

                        if not long_digit:
                            outlist = "  " + to_string(ct, ">>>9") + "  " + to_string(gastname, "x(34)") + "  " + to_string(tot_debt, "->>>,>>>,>>9.99") + "  " + to_string(debt0, "->>>,>>>,>>9.99") + "  " + to_string(debt1, "->>>,>>>,>>9.99") + "  " + to_string(debt2, "->>>,>>>,>>9.99") + "  " + to_string(debt3, "->>>,>>>,>>9.99") + "  "
                        else:
                            outlist = "  " + to_string(ct, ">>>9") + "  " + to_string(gastname, "x(34)") + "  " + to_string(tot_debt, "->>>>,>>>,>>>,>>9") + to_string(debt0, "->>>>,>>>,>>>,>>9") + to_string(debt1, "->>>>,>>>,>>>,>>9") + to_string(debt2, "->>>>,>>>,>>>,>>9") + to_string(debt3, "->>>>,>>>,>>>,>>9")
                    else:
                        outlist = "  " + to_string(ct, ">>>9") + "  " + to_string(gastname, "x(34)") + "  " + to_string(tot_debt, "->>>,>>>,>>9.99") + "  " + to_string(debt0, "->>>,>>>,>>9.99") + "  " + to_string(debt1, "->>>,>>>,>>9.99") + "  " + to_string(debt2, "->>>,>>>,>>9.99") + "  " + to_string(debt3, "->>>,>>>,>>9.99") + "  "
                    fill_in_list(age_list.gastnr, age_list.fcurr)
                    output_list.creditlimit = creditlimit

                    if output_list.creditlimit != 0:
                        balance = output_list.creditlimit - tot_debt
                    else:
                        balance = 0
                    creditlimit = age_list.creditlimit
                    gastname = age_list.gastname
                    tot_debt = age_list.tot_debt
                    debt0 = age_list.debt0
                    debt1 = age_list.debt1
                    debt2 = age_list.debt2
                    debt3 = age_list.debt3
                    ct = ct + 1
                else:
                    tot_debt = tot_debt + age_list.tot_debt
                    debt0 = debt0 + age_list.debt0
                    debt1 = debt1 + age_list.debt1
                    debt2 = debt2 + age_list.debt2
                    debt3 = debt3 + age_list.debt3
                curr_gastnr = age_list.gastnr
                curr_name = age_list.gastname
                curr_fcurr = age_list.fcurr
                age_list_list.remove(age_list)

            if ct > 0:

                if price_decimal == 0:

                    if not long_digit:
                        outlist = "  " + to_string(ct, ">>>9") + "  " + to_string(gastname, "x(34)") + "  " + to_string(tot_debt, "->>>,>>>,>>9.99") + "  " + to_string(debt0, "->>>,>>>,>>9.99") + "  " + to_string(debt1, "->>>,>>>,>>9.99") + "  " + to_string(debt2, "->>>,>>>,>>9.99") + "  " + to_string(debt3, "->>>,>>>,>>9.99") + "  "
                    else:
                        outlist = "  " + to_string(ct, ">>>9") + "  " + to_string(gastname, "x(34)") + "  " + to_string(tot_debt, "->>>>,>>>,>>>,>>9") + to_string(debt0, "->>>>,>>>,>>>,>>9") + to_string(debt1, "->>>>,>>>,>>>,>>9") + to_string(debt2, "->>>>,>>>,>>>,>>9") + to_string(debt3, "->>>>,>>>,>>>,>>9")
                else:
                    outlist = "  " + to_string(ct, ">>>9") + "  " + to_string(gastname, "x(34)") + "  " + to_string(tot_debt, "->>>,>>>,>>9.99") + "  " + to_string(debt0, "->>>,>>>,>>9.99") + "  " + to_string(debt1, "->>>,>>>,>>9.99") + "  " + to_string(debt2, "->>>,>>>,>>9.99") + "  " + to_string(debt3, "->>>,>>>,>>9.99") + "  "
                fill_in_list(curr_gastnr, curr_fcurr)
                output_list.creditlimit = creditlimit

                if output_list.creditlimit != 0:
                    balance = output_list.creditlimit - tot_debt
                else:
                    balance = 0
            tmp_saldo = ledger.tot_debt

            if tmp_saldo == 0:
                tmp_saldo = 1
            outlist = "-----------------------------------------------------------------------------------------------------------------------------------------------------------"
            fill_in_list(0, "----")

            if price_decimal == 0:

                if not long_digit:
                    outlist = "                             T o t a l      " + to_string(ledger.tot_debt, "->>>,>>>,>>9.99") + "  " + to_string(ledger.debt0, "->>>,>>>,>>9.99") + "  " + to_string(ledger.debt1, "->>>,>>>,>>9.99") + "  " + to_string(ledger.debt2, "->>>,>>>,>>9.99") + "  " + to_string(ledger.debt3, "->>>,>>>,>>9.99")
                else:
                    outlist = "                             T o t a l      " + to_string(ledger.tot_debt, "->>>>,>>>,>>>,>>9") + to_string(ledger.debt0, "->>>>,>>>,>>>,>>9") + to_string(ledger.debt1, "->>>>,>>>,>>>,>>9") + to_string(ledger.debt2, "->>>>,>>>,>>>,>>9") + to_string(ledger.debt3, "->>>>,>>>,>>>,>>9")
            else:
                outlist = "                             T o t a l      " + to_string(ledger.tot_debt, "->>>,>>>,>>9.99") + "  " + to_string(ledger.debt0, "->>>,>>>,>>9.99") + "  " + to_string(ledger.debt1, "->>>,>>>,>>9.99") + "  " + to_string(ledger.debt2, "->>>,>>>,>>9.99") + "  " + to_string(ledger.debt3, "->>>,>>>,>>9.99")
            fill_in_list(0, "")

            if not long_digit:
                outlist = to_string(translateExtended ("        Statistic Percentage (%):", lvcarea, "") , "x(34)") + "               " + to_string((ledger.tot_debt / tmp_saldo * 100) , "->>,>>9.99") + "       " + to_string((ledger.debt0 / tmp_saldo * 100) , "->>,>>9.99") + "       " + to_string((ledger.debt1 / tmp_saldo * 100) , "->>,>>9.99") + "       " + to_string((ledger.debt2 / tmp_saldo * 100) , "->>,>>9.99") + "       " + to_string((ledger.debt3 / tmp_saldo * 100) , "->>,>>9.99")
            else:
                outlist = to_string(translateExtended ("        Statistic Percentage (%):", lvcarea, "") , "x(34)") + "                 " + to_string((ledger.tot_debt / tmp_saldo * 100) , "->>,>>9.99") + "       " + to_string((ledger.debt0 / tmp_saldo * 100) , "->>,>>9.99") + "       " + to_string((ledger.debt1 / tmp_saldo * 100) , "->>,>>9.99") + "       " + to_string((ledger.debt2 / tmp_saldo * 100) , "->>,>>9.99") + "       " + to_string((ledger.debt3 / tmp_saldo * 100) , "->>,>>9.99")
            fill_in_list(0, "")
            outlist = ""
            fill_in_list(0, "")
        outlist = "-----------------------------------------------------------------------------------------------------------------------------------------------------------"
        fill_in_list(0, "----")

        if price_decimal == 0:

            if not long_digit:
                outlist = to_string(translateExtended ("           T O T A L  A/R:", lvcarea, "") , "x(26)") + "                  " + to_string(t_saldo, "->>>,>>>,>>9.99") + "  " + to_string(t_debt0, "->>>,>>>,>>9.99") + "  " + to_string(t_debt1, "->>>,>>>,>>9.99") + "  " + to_string(t_debt2, "->>>,>>>,>>9.99") + "  " + to_string(t_debt3, "->>>,>>>,>>9.99")
            else:
                outlist = to_string(translateExtended ("           T O T A L  A/R:", lvcarea, "") , "x(26)") + "                  " + to_string(t_saldo, "->>>>,>>>,>>>,>>9") + to_string(t_debt0, "->>>>,>>>,>>>,>>9") + to_string(t_debt1, "->>>>,>>>,>>>,>>9") + to_string(t_debt2, "->>>>,>>>,>>>,>>9") + to_string(t_debt3, "->>>>,>>>,>>>,>>9")
        else:
            outlist = to_string(translateExtended ("           T O T A L  A/R:", lvcarea, "") , "x(26)") + "                  " + to_string(t_saldo, "->>>,>>>,>>9.99") + "  " + to_string(t_debt0, "->>>,>>>,>>9.99") + "  " + to_string(t_debt1, "->>>,>>>,>>9.99") + "  " + to_string(t_debt2, "->>>,>>>,>>9.99") + "  " + to_string(t_debt3, "->>>,>>>,>>9.99")
        fill_in_list(0, "")
        outlist = ""
        fill_in_list(0, "")

        if not long_digit:
            outlist = to_string(translateExtended ("        Statistic Percentage (%):", lvcarea, "") , "x(34)") + "                   " + "100.00" + "       " + to_string((t_debt0 / t_saldo * 100) , "->>,>>9.99") + "       " + to_string((t_debt1 / t_saldo * 100) , "->>,>>9.99") + "       " + to_string((t_debt2 / t_saldo * 100) , "->>,>>9.99") + "       " + to_string((t_debt3 / t_saldo * 100) , "->>,>>9.99")
        else:
            outlist = to_string(translateExtended ("        Statistic Percentage (%):", lvcarea, "") , "x(34)") + "                  " + "100.00" + "       " + to_string((t_debt0 / t_saldo * 100) , "->>,>>9.99") + "       " + to_string((t_debt1 / t_saldo * 100) , "->>,>>9.99") + "       " + to_string((t_debt2 / t_saldo * 100) , "->>,>>9.99") + "       " + to_string((t_debt3 / t_saldo * 100) , "->>,>>9.99")
        fill_in_list(0, "")
        outlist = ""
        fill_in_list(0, "")

    def fill_in_list(inp_gastnr:int, currency:str):

        nonlocal outlist, output_list_list, lvcarea, default_fcurr, day1, day2, day3, price_decimal, long_digit, htparam, debitor, artikel, guest, waehrung
        nonlocal debt


        nonlocal ledger, age_list, output_list, debt
        nonlocal ledger_list, age_list_list, output_list_list


        output_list = Output_list()
        output_list_list.append(output_list)

        output_list.str = outlist
        output_list.gastnr = inp_gastnr

        if not long_digit:
            output_list.age1 = substring(STR, 59, 17)
            output_list.age2 = substring(STR, 76, 17)
            output_list.age3 = substring(STR, 93, 17)
            output_list.age4 = substring(STR, 110, 17)
            output_list.curr = currency
        else:
            output_list.age1 = substring(STR, 61, 17)
            output_list.age2 = substring(STR, 78, 17)
            output_list.age3 = substring(STR, 95, 17)
            output_list.age4 = substring(STR, 112, 17)
            output_list.curr = currency

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 144)).first()
    default_fcurr = htparam.fchar

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 330)).first()

    if htparam.finteger != 0:
        day1 = htparam.finteger

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 331)).first()

    if htparam.finteger != 0:
        day2 = htparam.finteger

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 332)).first()

    if htparam.finteger != 0:
        day3 = htparam.finteger
    day2 = day2 + day1
    day3 = day3 + day2

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 491)).first()
    price_decimal = htparam.finteger

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 246)).first()
    long_digit = htparam.flogical

    if substring(to_name, 0, 2) == "zz":
        age_lista()
    else:
        age_list()

    return generate_output()