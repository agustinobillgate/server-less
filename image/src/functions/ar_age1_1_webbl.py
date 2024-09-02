from functions.additional_functions import *
import decimal
from datetime import date
from models import Debitor, Htparam, Artikel, Guest, Waehrung

def ar_age1_1_webbl(pvilanguage:int, case_type:int, mtd_flag:bool, to_date:date, fdate:date, tdate:date, from_art:int, to_art:int, from_name:str, to_name:str, disptype:int, mi_bill:bool, day1:int, day2:int, day3:int, detailed:bool):
    arage_balance_list_list = []
    curr_art:int = 0
    counter:int = 0
    t_saldo:decimal = 0
    t_prev:decimal = 0
    t_debit:decimal = 0
    t_credit:decimal = 0
    t_debt0:decimal = 0
    t_debt1:decimal = 0
    t_debt2:decimal = 0
    t_debt3:decimal = 0
    tmp_saldo:decimal = 0
    curr_name:str = ""
    curr_gastnr:int = 0
    gastname:str = ""
    p_bal:decimal = 0
    debit:decimal = 0
    credit:decimal = 0
    debt0:decimal = 0
    debt1:decimal = 0
    debt2:decimal = 0
    debt3:decimal = 0
    curr_counter:int = 0
    curr_fcurr:str = ""
    i:int = 0
    tot_debt:decimal = 0
    from_date:date = None
    default_fcurr:str = ""
    outlist:str = ""
    long_digit:bool = False
    curr_rgdatum:date = None
    bill_number:int = 0
    inp_gastnr:int = 0
    inp_artnr:int = 0
    tot_debtall:decimal = 0
    tot_debt0:decimal = 0
    tot_debt1:decimal = 0
    tot_debt2:decimal = 0
    tot_debt3:decimal = 0
    lvcarea:str = "ar_age1"
    debitor = htparam = artikel = guest = waehrung = None

    arage_balance_list = arage_list = age_list = ledger = debtrec = debt = None

    arage_balance_list_list, Arage_balance_list = create_model("Arage_balance_list", {"strdate":str, "curr":str, "gastnr":int, "artnr":int, "age1":str, "age2":str, "age3":str, "age4":str, "rechnr":str, "num":str, "cust_nm":str, "p_bal":str, "debit":str, "credit":str, "end_bal":str})
    arage_list_list, Arage_list = create_model("Arage_list", {"strdate":str, "curr":str, "gastnr":int, "artnr":int, "age1":str, "age2":str, "age3":str, "age4":str, "rechnr":str, "str":str})
    age_list_list, Age_list = create_model("Age_list", {"fcurr":str, "artnr":int, "rechnr":int, "counter":int, "gastnr":int, "rgdatum":date, "gastname":str, "p_bal":decimal, "debit":decimal, "credit":decimal, "saldo":decimal, "debt0":decimal, "debt1":decimal, "debt2":decimal, "debt3":decimal, "tot_debt":decimal})
    ledger_list, Ledger = create_model("Ledger", {"artnr":int, "bezeich":str, "p_bal":decimal, "debit":decimal, "credit":decimal, "debt0":decimal, "debt1":decimal, "debt2":decimal, "debt3":decimal, "tot_debt":decimal})

    Debtrec = Debitor
    Debt = Debitor

    db_session = local_storage.db_session

    def generate_output():
        nonlocal arage_balance_list_list, curr_art, counter, t_saldo, t_prev, t_debit, t_credit, t_debt0, t_debt1, t_debt2, t_debt3, tmp_saldo, curr_name, curr_gastnr, gastname, p_bal, debit, credit, debt0, debt1, debt2, debt3, curr_counter, curr_fcurr, i, tot_debt, from_date, default_fcurr, outlist, long_digit, curr_rgdatum, bill_number, inp_gastnr, inp_artnr, tot_debtall, tot_debt0, tot_debt1, tot_debt2, tot_debt3, lvcarea, debitor, htparam, artikel, guest, waehrung
        nonlocal debtrec, debt


        nonlocal arage_balance_list, arage_list, age_list, ledger, debtrec, debt
        nonlocal arage_balance_list_list, arage_list_list, age_list_list, ledger_list
        return {"arage-balance-list": arage_balance_list_list}

    def age_list1():

        nonlocal arage_balance_list_list, curr_art, counter, t_saldo, t_prev, t_debit, t_credit, t_debt0, t_debt1, t_debt2, t_debt3, tmp_saldo, curr_name, curr_gastnr, gastname, p_bal, debit, credit, debt0, debt1, debt2, debt3, curr_counter, curr_fcurr, i, tot_debt, from_date, default_fcurr, outlist, long_digit, curr_rgdatum, bill_number, inp_gastnr, inp_artnr, tot_debtall, tot_debt0, tot_debt1, tot_debt2, tot_debt3, lvcarea, debitor, htparam, artikel, guest, waehrung
        nonlocal debtrec, debt


        nonlocal arage_balance_list, arage_list, age_list, ledger, debtrec, debt
        nonlocal arage_balance_list_list, arage_list_list, age_list_list, ledger_list


        curr_art = 0
        counter = 0
        t_saldo = 0
        t_prev = 0
        t_debit = 0
        t_credit = 0
        t_debt0 = 0
        t_debt1 = 0
        t_debt2 = 0
        t_debt3 = 0
        tmp_saldo = 0
        curr_name = ""
        curr_gastnr = 0
        gastname = ""
        p_bal = 0
        debit = 0
        credit = 0
        debt0 = 0
        debt1 = 0
        debt2 = 0
        debt3 = 0
        tot_debt = 0
        i = 0
        curr_counter = 0
        curr_fcurr = ""


        from_date = date_mdy(get_month(to_date) , 1, get_year(to_date))

        for artikel in db_session.query(Artikel).filter(
                ((Artikel.artart == 2) |  (Artikel.artart == 7)) &  (Artikel.artnr >= from_art) &  (Artikel.artnr <= to_art) &  (Artikel.departement == 0)).all():
            ledger = Ledger()
            ledger_list.append(ledger)

            ledger.artnr = artikel.artnr
            ledger.bezeich = to_string(artikel.artnr) + "  -  " + artikel.bezeich
        curr_art = 0

        for debitor in db_session.query(Debitor).filter(
                (Debitor.rgdatum <= to_date) &  (Debitor.artnr >= from_art) &  (Debitor.artnr <= to_art) &  (Debitor.opart <= 1)).all():

            if debitor.name.lower()  >= (from_name).lower() :

                if curr_art != debitor.artnr:
                    curr_art = debitor.artnr

                    artikel = db_session.query(Artikel).filter(
                            (Artikel.artnr == curr_art) &  (Artikel.departement == 0)).first()

                if debitor.counter > 0:

                    age_list = query(age_list_list, filters=(lambda age_list :age_list.counter == debitor.counter), first=True)

                if (debitor.counter == 0) or (not age_list):

                    guest = db_session.query(Guest).filter(
                            (Guest.gastnr == debitor.gastnr)).first()
                    age_list = Age_list()
                    age_list_list.append(age_list)

                    age_list.artnr = debitor.artnr
                    age_list.rechnr = debitor.rechnr
                    age_list.rgdatum = debitor.rgdatum
                    age_list.counter = debitor.counter
                    age_list.gastnr = debitor.gastnr
                    age_list.tot_debt = 0

                    if debitor.betrieb_gastmem == 0:
                        age_list.fcurr = default_fcurr
                    else:

                        waehrung = db_session.query(Waehrung).filter(
                                (Waehrungsnr == debitor.betrieb_gastmem)).first()

                        if waehrung:
                            age_list.fcurr = waehrung.wabkurz

                    if artikel.artart == 2:
                        age_list.gastname = guest.name + ", " + guest.vorname1 + guest.anredefirma + " " + guest.anrede1
                    else:

                        htparam = db_session.query(Htparam).filter(
                                (Htparam.paramnr == 867)).first()

                        if debitor.gastnr == htparam.finteger:
                            age_list.gastname = "F&B " + artikel.bezeich
                        else:
                            age_list.gastname = "F/O " + artikel.bezeich

                if disptype == 0:
                    age_list.tot_debt = age_list.tot_debt + debitor.saldo
                else:
                    age_list.tot_debt = age_list.tot_debt + debitor.vesrdep

                if debitor.rgdatum < from_date and debitor.zahlkonto == 0:

                    if disptype == 0:
                        age_list.p_bal = age_list.p_bal + debitor.saldo
                    else:
                        age_list.p_bal = age_list.p_bal + debitor.vesrdep

                if debitor.rgdatum >= from_date and debitor.zahlkonto == 0:

                    if disptype == 0:
                        age_list.debit = age_list.debit + debitor.saldo
                    else:
                        age_list.debit = age_list.debit + debitor.vesrdep

                if debitor.rgdatum < from_date and debitor.zahlkonto != 0:

                    if disptype == 0:
                        age_list.p_bal = age_list.p_bal + debitor.saldo
                    else:
                        age_list.p_bal = age_list.p_bal + debitor.vesrdep
                else:

                    if debitor.rgdatum >= from_date and debitor.zahlkonto != 0:

                        if disptype == 0:
                            age_list.credit = age_list.credit - debitor.saldo
                        else:
                            age_list.credit = age_list.credit - debitor.vesrdep

        for artikel in db_session.query(Artikel).filter(
                ((Artikel.artart == 2) |  (Artikel.artart == 7)) &  (Artikel.artnr >= from_art) &  (Artikel.artnr <= to_art) &  (Artikel.departement == 0)).all():
            curr_counter = 0

            for debitor in db_session.query(Debitor).filter(
                    (Debitor.artnr == artikel.artnr) &  (Debitor.rgdatum <= to_date) &  (Debitor.opart == 2) &  (Debitor.zahlkonto == 0)).all():

                if debitor.name.lower()  >= (from_name).lower() :

                    guest = db_session.query(Guest).filter(
                            (Guest.gastnr == debitor.gastnr)).first()
                    age_list = Age_list()
                    age_list_list.append(age_list)

                    age_list.artnr = debitor.artnr
                    age_list.rechnr = debitor.rechnr
                    age_list.rgdatum = debitor.rgdatum
                    age_list.counter = debitor.counter
                    age_list.gastnr = debitor.gastnr
                    age_list.tot_debt = debitor.saldo

                    if debitor.betrieb_gastmem == 0:
                        age_list.fcurr = default_fcurr
                    else:

                        waehrung = db_session.query(Waehrung).filter(
                                (Waehrungsnr == debitor.betrieb_gastmem)).first()

                        if waehrung:
                            age_list.fcurr = waehrung.wabkurz

                    if artikel.artart == 2:
                        age_list.gastname = guest.name + ", " + guest.vorname1 + guest.anredefirma + " " + guest.anrede1
                    else:

                        htparam = db_session.query(Htparam).filter(
                                (Htparam.paramnr == 867)).first()

                        if debitor.gastnr == htparam.finteger:
                            age_list.gastname = "F&B " + artikel.bezeich
                        else:
                            age_list.gastname = "F/O " + artikel.bezeich

                    if debitor.rgdatum < from_date:

                        if disptype == 0:
                            age_list.p_bal = age_list.p_bal + debitor.saldo
                        else:
                            age_list.p_bal = age_list.p_bal + debitor.vesrdep

                    elif debitor.rgdatum >= from_date:

                        if disptype == 0:
                            age_list.debit = age_list.debit + debitor.saldo
                        else:
                            age_list.debit = age_list.debit + debitor.vesrdep

                    for debtrec in db_session.query(Debtrec).filter(
                            (Debtrec.counter == debitor.counter) &  (Debtrec.rechnr == debitor.rechnr) &  (Debtrec.zahlkonto > 0) &  (Debtrec.rgdatum <= to_date)).all():
                        age_list.tot_debt = age_list.tot_debt + debtrec.saldo

                        if debtrec.rgdatum < from_date:

                            if disptype == 0:
                                age_list.p_bal = age_list.p_bal + debtrec.saldo
                            else:
                                age_list.p_bal = age_list.p_bal + debtrec.vesrdep

                        elif debtrec.rgdatum >= from_date:

                            if disptype == 0:
                                age_list.credit = age_list.credit - debtrec.saldo
                            else:
                                age_list.credit = age_list.credit - debtrec.vesrdep

        for age_list in query(age_list_list):

            if age_list.p_bal >= - 0.01 and age_list.p_bal <= 0.01 and age_list.debit == 0 and age_list.credit == 0:
                age_list_list.remove(age_list)

        for ledger in query(ledger_list):
            outlist = "    " + ledger.bezeich.upper()
            fill_in_list(False, "", None)
            outlist = ""
            fill_in_list(False, "", None)
            counter = 0
            curr_gastnr = 0

            if mi_bill:

                for age_list in query(age_list_list, filters=(lambda age_list :age_list.artnr == ledger.artnr)):
                    create_output()

            else:

                for age_list in query(age_list_list, filters=(lambda age_list :age_list.artnr == ledger.artnr)):
                    create_output()


            if counter > 0 and (p_bal != 0 or debit != 0 or credit != 0):

                if not long_digit:
                    outlist = "  " + to_string(counter, ">>>9 ") + to_string(gastname, "x(30)") + to_string(tot_debt, "->>,>>>,>>>,>>9.99") + to_string(p_bal, "->>,>>>,>>>,>>9.99") + to_string(debit, "->>,>>>,>>>,>>9.99") + to_string(credit, "->>,>>>,>>>,>>9.99") + to_string(debt0, "->>,>>>,>>>,>>9.99") + to_string(debt1, "->>,>>>,>>>,>>9.99") + to_string(debt2, "->>,>>>,>>>,>>9.99") + to_string(debt3, "->>,>>>,>>>,>>9.99")
                else:
                    outlist = "  " + to_string(counter, ">>>9 ") + to_string(gastname, "x(30)") + to_string(tot_debt, "->,>>>,>>>,>>>,>>9") + to_string(p_bal, "->,>>>,>>>,>>>,>>9") + to_string(debit, "->,>>>,>>>,>>>,>>9") + to_string(credit, "->,>>>,>>>,>>>,>>9") + to_string(debt0, "->,>>>,>>>,>>>,>>9") + to_string(debt1, "->,>>>,>>>,>>>,>>9") + to_string(debt2, "->,>>>,>>>,>>>,>>9") + to_string(debt3, "->,>>>,>>>,>>>,>>9")
                fill_in_list(True, curr_fcurr, curr_rgdatum)
            else:
                counter = counter - 1
            tmp_saldo = ledger.tot_debt

            if tmp_saldo == 0:
                tmp_saldo = 1
            outlist = "-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------"
            fill_in_list(False, "----", None)

            if not long_digit:
                outlist = "       " + to_string(translateExtended ("T o t a l", lvcarea, "") , "x(30)") + to_string(ledger.tot_debt, "->>,>>>,>>>,>>9.99") + to_string(ledger.p_bal, "->>,>>>,>>>,>>9.99") + to_string(ledger.debit, "->>,>>>,>>>,>>9.99") + to_string(ledger.credit, "->>,>>>,>>>,>>9.99") + to_string(ledger.debt0, "->>,>>>,>>>,>>9.99") + to_string(ledger.debt1, "->>,>>>,>>>,>>9.99") + to_string(ledger.debt2, "->>,>>>,>>>,>>9.99") + to_string(ledger.debt3, "->>,>>>,>>>,>>9.99")
            else:
                outlist = "       " + to_string(translateExtended ("T o t a l", lvcarea, "") , "x(30)") + to_string(ledger.tot_debt, "->,>>>,>>>,>>>,>>9") + to_string(ledger.p_bal, "->,>>>,>>>,>>>,>>9") + to_string(ledger.debit, "->,>>>,>>>,>>>,>>9") + to_string(ledger.credit, "->,>>>,>>>,>>>,>>9") + to_string(ledger.debt0, "->,>>>,>>>,>>>,>>9") + to_string(ledger.debt1, "->,>>>,>>>,>>>,>>9") + to_string(ledger.debt2, "->,>>>,>>>,>>>,>>9") + to_string(ledger.debt3, "->,>>>,>>>,>>>,>>9")
            fill_in_list(False, "", None)
            outlist = "       " + to_string(translateExtended ("Statistic Percentage (%) :", lvcarea, "") , "x(30)") + "            100.00"
            for i in range(1,54 + 1) :
                outlist = outlist + " "
            tot_debt0 = (ledger.debt0 / tmp_saldo * 100)
            tot_debt1 = (ledger.debt1 / tmp_saldo * 100)
            tot_debt2 = (ledger.debt2 / tmp_saldo * 100)
            tot_debt3 = (ledger.debt3 / tmp_saldo * 100)

            if tot_debt0 == None:
                tot_debt0 = 0

            if tot_debt1 == None:
                tot_debt1 = 0

            if tot_debt2 == None:
                tot_debt2 = 0

            if tot_debt3 == None:
                tot_debt3 = 0
            outlist = outlist + to_string(tot_debt0, "         ->,>>9.99") + to_string(tot_debt1, "         ->,>>9.99") + to_string(tot_debt2, "         ->,>>9.99") + to_string(tot_debt3, "         ->,>>9.99")
            fill_in_list(False, "", None)
            outlist = ""
            fill_in_list(False, "", None)
        outlist = "-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------"
        fill_in_list(False, "----", None)

        if not long_digit:
            outlist = "       " + to_string(translateExtended ("T O T A L  A/R:", lvcarea, "") , "x(30)") + to_string(t_saldo, "->>,>>>,>>>,>>9.99") + to_string(t_prev, "->>,>>>,>>>,>>9.99") + to_string(t_debit, "->>,>>>,>>>,>>9.99") + to_string(t_credit, "->>,>>>,>>>,>>9.99") + to_string(t_debt0, "->>,>>>,>>>,>>9.99") + to_string(t_debt1, "->>,>>>,>>>,>>9.99") + to_string(t_debt2, "->>,>>>,>>>,>>9.99") + to_string(t_debt3, "->>,>>>,>>>,>>9.99")
        else:
            outlist = "       " + to_string(translateExtended ("T O T A L  A/R:", lvcarea, "") , "x(30)") + to_string(t_saldo, "->,>>>,>>>,>>>,>>9") + to_string(t_prev, "->,>>>,>>>,>>>,>>9") + to_string(t_debit, "->,>>>,>>>,>>>,>>9") + to_string(t_credit, "->,>>>,>>>,>>>,>>9") + to_string(t_debt0, "->,>>>,>>>,>>>,>>9") + to_string(t_debt1, "->,>>>,>>>,>>>,>>9") + to_string(t_debt2, "->,>>>,>>>,>>>,>>9") + to_string(t_debt3, "->,>>>,>>>,>>>,>>9")
        fill_in_list(False, "", None)
        outlist = "       " + to_string(translateExtended ("Statistic Percentage (%) :", lvcarea, "") , "x(30)") + "            100.00"
        for i in range(1,54 + 1) :
            outlist = outlist + " "
        tot_debt0 = (t_debt0 / t_saldo * 100)
        tot_debt1 = (t_debt1 / t_saldo * 100)
        tot_debt2 = (t_debt2 / t_saldo * 100)
        tot_debt3 = (t_debt3 / t_saldo * 100)

        if tot_debt0 == None:
            tot_debt0 = 0

        if tot_debt1 == None:
            tot_debt1 = 0

        if tot_debt2 == None:
            tot_debt2 = 0

        if tot_debt3 == None:
            tot_debt3 = 0
        outlist = outlist + to_string(tot_debt0, "           ->>9.99") + to_string(tot_debt1, "           ->>9.99") + to_string(tot_debt2, "           ->>9.99") + to_string(tot_debt3, "           ->>9.99")
        fill_in_list(False, "", None)
        outlist = ""
        fill_in_list(False, "", None)

    def age_list2():

        nonlocal arage_balance_list_list, curr_art, counter, t_saldo, t_prev, t_debit, t_credit, t_debt0, t_debt1, t_debt2, t_debt3, tmp_saldo, curr_name, curr_gastnr, gastname, p_bal, debit, credit, debt0, debt1, debt2, debt3, curr_counter, curr_fcurr, i, tot_debt, from_date, default_fcurr, outlist, long_digit, curr_rgdatum, bill_number, inp_gastnr, inp_artnr, tot_debtall, tot_debt0, tot_debt1, tot_debt2, tot_debt3, lvcarea, debitor, htparam, artikel, guest, waehrung
        nonlocal debtrec, debt


        nonlocal arage_balance_list, arage_list, age_list, ledger, debtrec, debt
        nonlocal arage_balance_list_list, arage_list_list, age_list_list, ledger_list


        curr_art = 0
        counter = 0
        t_saldo = 0
        t_prev = 0
        t_debit = 0
        t_credit = 0
        t_debt0 = 0
        t_debt1 = 0
        t_debt2 = 0
        t_debt3 = 0
        tmp_saldo = 0
        curr_name = ""
        curr_gastnr = 0
        gastname = ""
        p_bal = 0
        debit = 0
        credit = 0
        debt0 = 0
        debt1 = 0
        debt2 = 0
        debt3 = 0
        tot_debt = 0
        i = 0
        curr_counter = 0
        curr_fcurr = ""


        from_date = date_mdy(get_month(to_date) , 1, get_year(to_date))

        for artikel in db_session.query(Artikel).filter(
                ((Artikel.artart == 2) |  (Artikel.artart == 7)) &  (Artikel.artnr >= from_art) &  (Artikel.artnr <= to_art) &  (Artikel.departement == 0)).all():
            ledger = Ledger()
            ledger_list.append(ledger)

            ledger.artnr = artikel.artnr
            ledger.bezeich = to_string(artikel.artnr) + "  -  " + artikel.bezeich
        curr_art = 0

        for debitor in db_session.query(Debitor).filter(
                (Debitor.rgdatum <= to_date) &  (Debitor.artnr >= from_art) &  (Debitor.artnr <= to_art) &  (Debitor.opart <= 1)).all():

            if debitor.name.lower()  >= (from_name).lower()  and debitor.name.lower()  <= (to_name).lower() :

                if curr_art != debitor.artnr:
                    curr_art = debitor.artnr

                    artikel = db_session.query(Artikel).filter(
                            (Artikel.artnr == curr_art) &  (Artikel.departement == 0)).first()

                if debitor.counter > 0:

                    age_list = query(age_list_list, filters=(lambda age_list :age_list.counter == debitor.counter), first=True)

                if (debitor.counter == 0) or (not age_list):

                    guest = db_session.query(Guest).filter(
                            (Guest.gastnr == debitor.gastnr)).first()
                    age_list = Age_list()
                    age_list_list.append(age_list)

                    age_list.artnr = debitor.artnr
                    age_list.rechnr = debitor.rechnr
                    age_list.rgdatum = debitor.rgdatum
                    age_list.counter = debitor.counter
                    age_list.gastnr = debitor.gastnr
                    age_list.tot_debt = 0

                    if debitor.betrieb_gastmem == 0:
                        age_list.fcurr = default_fcurr
                    else:

                        waehrung = db_session.query(Waehrung).filter(
                                (Waehrungsnr == debitor.betrieb_gastmem)).first()

                        if waehrung:
                            age_list.fcurr = waehrung.wabkurz

                    if artikel.artart == 2:
                        age_list.gastname = guest.name + ", " + guest.vorname1 + guest.anredefirma + " " + guest.anrede1
                    else:

                        htparam = db_session.query(Htparam).filter(
                                (Htparam.paramnr == 867)).first()

                        if debitor.gastnr == htparam.finteger:
                            age_list.gastname = "F&B " + artikel.bezeich
                        else:
                            age_list.gastname = "F/O " + artikel.bezeich

                if disptype == 0:
                    age_list.tot_debt = age_list.tot_debt + debitor.saldo
                else:
                    age_list.tot_debt = age_list.tot_debt + debitor.vesrdep

                if debitor.rgdatum < from_date and debitor.zahlkonto == 0:

                    if disptype == 0:
                        age_list.p_bal = age_list.p_bal + debitor.saldo
                    else:
                        age_list.p_bal = age_list.p_bal + debitor.vesrdep

                if debitor.rgdatum >= from_date and debitor.zahlkonto == 0:

                    if disptype == 0:
                        age_list.debit = age_list.debit + debitor.saldo
                    else:
                        age_list.debit = age_list.debit + debitor.vesrdep

                if debitor.rgdatum < from_date and debitor.zahlkonto != 0:
                    age_list.p_bal = age_list.p_bal + debitor.saldo
                else:

                    if debitor.rgdatum >= from_date and debitor.zahlkonto != 0:

                        if disptype == 0:
                            age_list.credit = age_list.credit - debitor.saldo
                        else:
                            age_list.credit = age_list.credit - debitor.vesrdep

        for artikel in db_session.query(Artikel).filter(
                ((Artikel.artart == 2) |  (Artikel.artart == 7)) &  (Artikel.artnr >= from_art) &  (Artikel.artnr <= to_art) &  (Artikel.departement == 0)).all():
            curr_counter = 0

            for debitor in db_session.query(Debitor).filter(
                    (Debitor.artnr == artikel.artnr) &  (Debitor.rgdatum <= to_date) &  (Debitor.opart == 2) &  (Debitor.zahlkonto == 0)).all():

                if debitor.name.lower()  >= (from_name).lower()  and debitor.name.lower()  <= (to_name).lower() :

                    guest = db_session.query(Guest).filter(
                            (Guest.gastnr == debitor.gastnr)).first()
                    age_list = Age_list()
                    age_list_list.append(age_list)

                    age_list.artnr = debitor.artnr
                    age_list.rechnr = debitor.rechnr
                    age_list.rgdatum = debitor.rgdatum
                    age_list.counter = debitor.counter
                    age_list.gastnr = debitor.gastnr
                    age_list.tot_debt = debitor.saldo

                    if debitor.betrieb_gastmem == 0:
                        age_list.fcurr = default_fcurr
                    else:

                        waehrung = db_session.query(Waehrung).filter(
                                (Waehrungsnr == debitor.betrieb_gastmem)).first()

                        if waehrung:
                            age_list.fcurr = waehrung.wabkurz

                    if artikel.artart == 2:
                        age_list.gastname = guest.name + ", " + guest.vorname1 + guest.anredefirma + " " + guest.anrede1
                    else:

                        htparam = db_session.query(Htparam).filter(
                                (Htparam.paramnr == 867)).first()

                        if debitor.gastnr == htparam.finteger:
                            age_list.gastname = "F&B " + artikel.bezeich
                        else:
                            age_list.gastname = "F/O " + artikel.bezeich

                    if debitor.rgdatum < from_date:

                        if disptype == 0:
                            age_list.p_bal = age_list.p_bal + debitor.saldo
                        else:
                            age_list.p_bal = age_list.p_bal + debitor.vesrdep

                    elif debitor.rgdatum >= from_date:

                        if disptype == 0:
                            age_list.debit = age_list.debit + debitor.saldo
                        else:
                            age_list.debit = age_list.debit + debitor.vesrdep

                    for debtrec in db_session.query(Debtrec).filter(
                            (Debtrec.counter == debitor.counter) &  (Debtrec.rechnr == debitor.rechnr) &  (Debtrec.zahlkonto > 0) &  (Debtrec.rgdatum <= to_date)).all():
                        age_list.tot_debt = age_list.tot_debt + debtrec.saldo

                        if debtrec.rgdatum < from_date:

                            if disptype == 0:
                                age_list.p_bal = age_list.p_bal + debtrec.saldo
                            else:
                                age_list.p_bal = age_list.p_bal + debtrec.vesrdep

                        elif debtrec.rgdatum >= from_date:

                            if disptype == 0:
                                age_list.credit = age_list.credit - debtrec.saldo
                            else:
                                age_list.credit = age_list.credit - debtrec.vesrdep

        for age_list in query(age_list_list):

            if age_list.p_bal >= - 0.01 and age_list.p_bal <= 0.01 and age_list.debit == 0 and age_list.credit == 0:
                age_list_list.remove(age_list)

        for ledger in query(ledger_list):
            outlist = "    " + ledger.bezeich.upper()
            fill_in_list(False, "", None)
            outlist = ""
            fill_in_list(False, "", None)
            counter = 0
            curr_gastnr = 0

            if mi_bill:

                for age_list in query(age_list_list, filters=(lambda age_list :age_list.artnr == ledger.artnr)):
                    create_output()

            else:

                for age_list in query(age_list_list, filters=(lambda age_list :age_list.artnr == ledger.artnr)):
                    create_output()


            if counter > 0 and (p_bal != 0 or debit != 0 or credit != 0):

                if not long_digit:
                    outlist = "  " + to_string(counter, ">>>9 ") + to_string(gastname, "x(30)") + to_string(tot_debt, "->>,>>>,>>>,>>9.99") + to_string(p_bal, "->>,>>>,>>>,>>9.99") + to_string(debit, "->>,>>>,>>>,>>9.99") + to_string(credit, "->>,>>>,>>>,>>9.99") + to_string(debt0, "->>,>>>,>>>,>>9.99") + to_string(debt1, "->>,>>>,>>>,>>9.99") + to_string(debt2, "->>,>>>,>>>,>>9.99") + to_string(debt3, "->>,>>>,>>>,>>9.99")
                else:
                    outlist = "  " + to_string(counter, ">>>9 ") + to_string(gastname, "x(30)") + to_string(tot_debt, "->,>>>,>>>,>>>,>>9") + to_string(p_bal, "->,>>>,>>>,>>>,>>9") + to_string(debit, "->,>>>,>>>,>>>,>>9") + to_string(credit, "->,>>>,>>>,>>>,>>9") + to_string(debt0, "->,>>>,>>>,>>>,>>9") + to_string(debt1, "->,>>>,>>>,>>>,>>9") + to_string(debt2, "->,>>>,>>>,>>>,>>9") + to_string(debt3, "->,>>>,>>>,>>>,>>9")
                fill_in_list(True, curr_fcurr, curr_rgdatum)
            else:
                counter = counter - 1
            tmp_saldo = ledger.tot_debt

            if tmp_saldo == 0:
                tmp_saldo = 1
            outlist = "-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------"
            fill_in_list(False, "----", None)

            if not long_digit:
                outlist = "       " + to_string(translateExtended ("T o t a l", lvcarea, "") , "x(30)") + to_string(ledger.tot_debt, "->>,>>>,>>>,>>9.99") + to_string(ledger.p_bal, "->>,>>>,>>>,>>9.99") + to_string(ledger.debit, "->>,>>>,>>>,>>9.99") + to_string(ledger.credit, "->>,>>>,>>>,>>9.99") + to_string(ledger.debt0, "->>,>>>,>>>,>>9.99") + to_string(ledger.debt1, "->>,>>>,>>>,>>9.99") + to_string(ledger.debt2, "->>,>>>,>>>,>>9.99") + to_string(ledger.debt3, "->>,>>>,>>>,>>9.99")
            else:
                outlist = "       " + to_string(translateExtended ("T o t a l", lvcarea, "") , "x(30)") + to_string(ledger.tot_debt, "->,>>>,>>>,>>>,>>9") + to_string(ledger.p_bal, "->,>>>,>>>,>>>,>>9") + to_string(ledger.debit, "->,>>>,>>>,>>>,>>9") + to_string(ledger.credit, "->,>>>,>>>,>>>,>>9") + to_string(ledger.debt0, "->,>>>,>>>,>>>,>>9") + to_string(ledger.debt1, "->,>>>,>>>,>>>,>>9") + to_string(ledger.debt2, "->,>>>,>>>,>>>,>>9") + to_string(ledger.debt3, "->,>>>,>>>,>>>,>>9")
            fill_in_list(False, "", None)
            outlist = "       " + to_string(translateExtended ("Statistic Percentage (%) :", lvcarea, "") , "x(30)") + "            100.00"
            for i in range(1,54 + 1) :
                outlist = outlist + " "
            tot_debt0 = (ledger.debt0 / tmp_saldo * 100)
            tot_debt1 = (ledger.debt1 / tmp_saldo * 100)
            tot_debt2 = (ledger.debt2 / tmp_saldo * 100)
            tot_debt3 = (ledger.debt3 / tmp_saldo * 100)

            if tot_debt0 == None:
                tot_debt0 = 0

            if tot_debt1 == None:
                tot_debt1 = 0

            if tot_debt2 == None:
                tot_debt2 = 0

            if tot_debt3 == None:
                tot_debt3 = 0
            outlist = outlist + to_string(tot_debt0, "           ->>9.99") + to_string(tot_debt1, "           ->>9.99") + to_string(tot_debt2, "           ->>9.99") + to_string(tot_debt3, "           ->>9.99")
            fill_in_list(False, "", None)
            outlist = ""
            fill_in_list(False, "", None)
        outlist = "-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------"
        fill_in_list(False, "----", None)

        if not long_digit:
            outlist = "       " + to_string(translateExtended ("T O T A L  A/R:", lvcarea, "") , "x(30)") + to_string(t_saldo, "->>,>>>,>>>,>>9.99") + to_string(t_prev, "->>,>>>,>>>,>>9.99") + to_string(t_debit, "->>,>>>,>>>,>>9.99") + to_string(t_credit, "->>,>>>,>>>,>>9.99") + to_string(t_debt0, "->>,>>>,>>>,>>9.99") + to_string(t_debt1, "->>,>>>,>>>,>>9.99") + to_string(t_debt2, "->>,>>>,>>>,>>9.99") + to_string(t_debt3, "->>,>>>,>>>,>>9.99")
        else:
            outlist = "       " + to_string(translateExtended ("T O T A L  A/R:", lvcarea, "") , "x(30)") + to_string(t_saldo, "->,>>>,>>>,>>>,>>9") + to_string(t_prev, "->,>>>,>>>,>>>,>>9") + to_string(t_debit, "->,>>>,>>>,>>>,>>9") + to_string(t_credit, "->,>>>,>>>,>>>,>>9") + to_string(t_debt0, "->,>>>,>>>,>>>,>>9") + to_string(t_debt1, "->,>>>,>>>,>>>,>>9") + to_string(t_debt2, "->,>>>,>>>,>>>,>>9") + to_string(t_debt3, "->,>>>,>>>,>>>,>>9")
        fill_in_list(False, "", None)
        outlist = "       " + to_string(translateExtended ("Statistic Percentage (%) :", lvcarea, "") , "x(30)") + "            100.00"
        for i in range(1,54 + 1) :
            outlist = outlist + " "
        tot_debt0 = (t_debt0 / t_saldo * 100)
        tot_debt1 = (t_debt1 / t_saldo * 100)
        tot_debt2 = (t_debt2 / t_saldo * 100)
        tot_debt3 = (t_debt3 / t_saldo * 100)

        if tot_debt0 == None:
            tot_debt0 = 0

        if tot_debt1 == None:
            tot_debt1 = 0

        if tot_debt2 == None:
            tot_debt2 = 0

        if tot_debt3 == None:
            tot_debt3 = 0
        outlist = outlist + to_string(tot_debt0, "           ->>9.99") + to_string(tot_debt1, "           ->>9.99") + to_string(tot_debt2, "           ->>9.99") + to_string(tot_debt3, "           ->>9.99")
        fill_in_list(False, "", None)
        outlist = ""
        fill_in_list(False, "", None)

    def age_list1a():

        nonlocal arage_balance_list_list, curr_art, counter, t_saldo, t_prev, t_debit, t_credit, t_debt0, t_debt1, t_debt2, t_debt3, tmp_saldo, curr_name, curr_gastnr, gastname, p_bal, debit, credit, debt0, debt1, debt2, debt3, curr_counter, curr_fcurr, i, tot_debt, from_date, default_fcurr, outlist, long_digit, curr_rgdatum, bill_number, inp_gastnr, inp_artnr, tot_debtall, tot_debt0, tot_debt1, tot_debt2, tot_debt3, lvcarea, debitor, htparam, artikel, guest, waehrung
        nonlocal debtrec, debt


        nonlocal arage_balance_list, arage_list, age_list, ledger, debtrec, debt
        nonlocal arage_balance_list_list, arage_list_list, age_list_list, ledger_list


        curr_art = 0
        counter = 0
        t_saldo = 0
        t_prev = 0
        t_debit = 0
        t_credit = 0
        t_debt0 = 0
        t_debt1 = 0
        t_debt2 = 0
        t_debt3 = 0
        tmp_saldo = 0
        curr_name = ""
        curr_gastnr = 0
        gastname = ""
        p_bal = 0
        debit = 0
        credit = 0
        debt0 = 0
        debt1 = 0
        debt2 = 0
        debt3 = 0
        tot_debt = 0
        i = 0
        curr_counter = 0
        curr_fcurr = ""


        from_date = fdate

        for artikel in db_session.query(Artikel).filter(
                ((Artikel.artart == 2) |  (Artikel.artart == 7)) &  (Artikel.artnr >= from_art) &  (Artikel.artnr <= to_art) &  (Artikel.departement == 0)).all():
            ledger = Ledger()
            ledger_list.append(ledger)

            ledger.artnr = artikel.artnr
            ledger.bezeich = to_string(artikel.artnr) + "  -  " + artikel.bezeich
        curr_art = 0

        for debitor in db_session.query(Debitor).filter(
                (Debitor.rgdatum <= tdate) &  (Debitor.artnr >= from_art) &  (Debitor.artnr <= to_art) &  (Debitor.opart <= 1)).all():

            if debitor.name.lower()  >= (from_name).lower() :

                if curr_art != debitor.artnr:
                    curr_art = debitor.artnr

                    artikel = db_session.query(Artikel).filter(
                            (Artikel.artnr == curr_art) &  (Artikel.departement == 0)).first()

                if debitor.counter > 0:

                    age_list = query(age_list_list, filters=(lambda age_list :age_list.counter == debitor.counter), first=True)

                if (debitor.counter == 0) or (not age_list):

                    guest = db_session.query(Guest).filter(
                            (Guest.gastnr == debitor.gastnr)).first()
                    age_list = Age_list()
                    age_list_list.append(age_list)

                    age_list.artnr = debitor.artnr
                    age_list.rechnr = debitor.rechnr
                    age_list.rgdatum = debitor.rgdatum
                    age_list.counter = debitor.counter
                    age_list.gastnr = debitor.gastnr
                    age_list.tot_debt = 0

                    if debitor.betrieb_gastmem == 0:
                        age_list.fcurr = default_fcurr
                    else:

                        waehrung = db_session.query(Waehrung).filter(
                                (Waehrungsnr == debitor.betrieb_gastmem)).first()

                        if waehrung:
                            age_list.fcurr = waehrung.wabkurz

                    if artikel.artart == 2:
                        age_list.gastname = guest.name + ", " + guest.vorname1 + guest.anredefirma + " " + guest.anrede1
                    else:

                        htparam = db_session.query(Htparam).filter(
                                (Htparam.paramnr == 867)).first()

                        if debitor.gastnr == htparam.finteger:
                            age_list.gastname = "F&B " + artikel.bezeich
                        else:
                            age_list.gastname = "F/O " + artikel.bezeich

                if disptype == 0:
                    age_list.tot_debt = age_list.tot_debt + debitor.saldo
                else:
                    age_list.tot_debt = age_list.tot_debt + debitor.vesrdep

                if debitor.rgdatum < from_date and debitor.zahlkonto == 0:

                    if disptype == 0:
                        age_list.p_bal = age_list.p_bal + debitor.saldo
                    else:
                        age_list.p_bal = age_list.p_bal + debitor.vesrdep

                if debitor.rgdatum >= from_date and debitor.zahlkonto == 0:

                    if disptype == 0:
                        age_list.debit = age_list.debit + debitor.saldo
                    else:
                        age_list.debit = age_list.debit + debitor.vesrdep

                if debitor.rgdatum < from_date and debitor.zahlkonto != 0:

                    if disptype == 0:
                        age_list.p_bal = age_list.p_bal + debitor.saldo
                    else:
                        age_list.p_bal = age_list.p_bal + debitor.vesrdep
                else:

                    if debitor.rgdatum >= from_date and debitor.zahlkonto != 0:

                        if disptype == 0:
                            age_list.credit = age_list.credit - debitor.saldo
                        else:
                            age_list.credit = age_list.credit - debitor.vesrdep

        for artikel in db_session.query(Artikel).filter(
                ((Artikel.artart == 2) |  (Artikel.artart == 7)) &  (Artikel.artnr >= from_art) &  (Artikel.artnr <= to_art) &  (Artikel.departement == 0)).all():
            curr_counter = 0

            for debitor in db_session.query(Debitor).filter(
                    (Debitor.artnr == artikel.artnr) &  (Debitor.rgdatum <= to_date) &  (Debitor.opart == 2) &  (Debitor.zahlkonto == 0)).all():

                if debitor.name.lower()  >= (from_name).lower() :

                    guest = db_session.query(Guest).filter(
                            (Guest.gastnr == debitor.gastnr)).first()
                    age_list = Age_list()
                    age_list_list.append(age_list)

                    age_list.artnr = debitor.artnr
                    age_list.rechnr = debitor.rechnr
                    age_list.rgdatum = debitor.rgdatum
                    age_list.counter = debitor.counter
                    age_list.gastnr = debitor.gastnr
                    age_list.tot_debt = debitor.saldo

                    if debitor.betrieb_gastmem == 0:
                        age_list.fcurr = default_fcurr
                    else:

                        waehrung = db_session.query(Waehrung).filter(
                                (Waehrungsnr == debitor.betrieb_gastmem)).first()

                        if waehrung:
                            age_list.fcurr = waehrung.wabkurz

                    if artikel.artart == 2:
                        age_list.gastname = guest.name + ", " + guest.vorname1 + guest.anredefirma + " " + guest.anrede1
                    else:

                        htparam = db_session.query(Htparam).filter(
                                (Htparam.paramnr == 867)).first()

                        if debitor.gastnr == htparam.finteger:
                            age_list.gastname = "F&B " + artikel.bezeich
                        else:
                            age_list.gastname = "F/O " + artikel.bezeich

                    if debitor.rgdatum < from_date:

                        if disptype == 0:
                            age_list.p_bal = age_list.p_bal + debitor.saldo
                        else:
                            age_list.p_bal = age_list.p_bal + debitor.vesrdep

                    elif debitor.rgdatum >= from_date:

                        if disptype == 0:
                            age_list.debit = age_list.debit + debitor.saldo
                        else:
                            age_list.debit = age_list.debit + debitor.vesrdep

                    for debtrec in db_session.query(Debtrec).filter(
                            (Debtrec.counter == debitor.counter) &  (Debtrec.rechnr == debitor.rechnr) &  (Debtrec.zahlkonto > 0) &  (Debtrec.rgdatum <= to_date)).all():
                        age_list.tot_debt = age_list.tot_debt + debtrec.saldo

                        if debtrec.rgdatum < from_date:

                            if disptype == 0:
                                age_list.p_bal = age_list.p_bal + debtrec.saldo
                            else:
                                age_list.p_bal = age_list.p_bal + debtrec.vesrdep

                        elif debtrec.rgdatum >= from_date:

                            if disptype == 0:
                                age_list.credit = age_list.credit - debtrec.saldo
                            else:
                                age_list.credit = age_list.credit - debtrec.vesrdep

        for age_list in query(age_list_list):

            if age_list.p_bal >= - 0.01 and age_list.p_bal <= 0.01 and age_list.debit == 0 and age_list.credit == 0:
                age_list_list.remove(age_list)

        for ledger in query(ledger_list):
            outlist = "    " + ledger.bezeich.upper()
            fill_in_list(False, "", None)
            outlist = ""
            fill_in_list(False, "", None)
            counter = 0
            curr_gastnr = 0

            if mi_bill:

                for age_list in query(age_list_list, filters=(lambda age_list :age_list.artnr == ledger.artnr)):
                    create_output()

            else:

                for age_list in query(age_list_list, filters=(lambda age_list :age_list.artnr == ledger.artnr)):
                    create_output()


            if counter > 0 and (p_bal != 0 or debit != 0 or credit != 0):

                if not long_digit:
                    outlist = "  " + to_string(counter, ">>>9 ") + to_string(gastname, "x(30)") + to_string(tot_debt, "->>,>>>,>>>,>>9.99") + to_string(p_bal, "->>,>>>,>>>,>>9.99") + to_string(debit, "->>,>>>,>>>,>>9.99") + to_string(credit, "->>,>>>,>>>,>>9.99") + to_string(debt0, "->>,>>>,>>>,>>9.99") + to_string(debt1, "->>,>>>,>>>,>>9.99") + to_string(debt2, "->>,>>>,>>>,>>9.99") + to_string(debt3, "->>,>>>,>>>,>>9.99")
                else:
                    outlist = "  " + to_string(counter, ">>>9 ") + to_string(gastname, "x(30)") + to_string(tot_debt, "->,>>>,>>>,>>>,>>9") + to_string(p_bal, "->,>>>,>>>,>>>,>>9") + to_string(debit, "->,>>>,>>>,>>>,>>9") + to_string(credit, "->,>>>,>>>,>>>,>>9") + to_string(debt0, "->,>>>,>>>,>>>,>>9") + to_string(debt1, "->,>>>,>>>,>>>,>>9") + to_string(debt2, "->,>>>,>>>,>>>,>>9") + to_string(debt3, "->,>>>,>>>,>>>,>>9")
                fill_in_list(True, curr_fcurr, curr_rgdatum)
            else:
                counter = counter - 1
            tmp_saldo = ledger.tot_debt

            if tmp_saldo == 0:
                tmp_saldo = 1
            outlist = "-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------"
            fill_in_list(False, "----", None)

            if not long_digit:
                outlist = "       " + to_string(translateExtended ("T o t a l", lvcarea, "") , "x(30)") + to_string(ledger.tot_debt, "->>,>>>,>>>,>>9.99") + to_string(ledger.p_bal, "->>,>>>,>>>,>>9.99") + to_string(ledger.debit, "->>,>>>,>>>,>>9.99") + to_string(ledger.credit, "->>,>>>,>>>,>>9.99") + to_string(ledger.debt0, "->>,>>>,>>>,>>9.99") + to_string(ledger.debt1, "->>,>>>,>>>,>>9.99") + to_string(ledger.debt2, "->>,>>>,>>>,>>9.99") + to_string(ledger.debt3, "->>,>>>,>>>,>>9.99")
            else:
                outlist = "       " + to_string(translateExtended ("T o t a l", lvcarea, "") , "x(30)") + to_string(ledger.tot_debt, "->,>>>,>>>,>>>,>>9") + to_string(ledger.p_bal, "->,>>>,>>>,>>>,>>9") + to_string(ledger.debit, "->,>>>,>>>,>>>,>>9") + to_string(ledger.credit, "->,>>>,>>>,>>>,>>9") + to_string(ledger.debt0, "->,>>>,>>>,>>>,>>9") + to_string(ledger.debt1, "->,>>>,>>>,>>>,>>9") + to_string(ledger.debt2, "->,>>>,>>>,>>>,>>9") + to_string(ledger.debt3, "->,>>>,>>>,>>>,>>9")
            fill_in_list(False, "", None)
            outlist = "       " + to_string(translateExtended ("Statistic Percentage (%) :", lvcarea, "") , "x(30)") + "            100.00"
            for i in range(1,54 + 1) :
                outlist = outlist + " "
            tot_debt0 = (ledger.debt0 / tmp_saldo * 100)
            tot_debt1 = (ledger.debt1 / tmp_saldo * 100)
            tot_debt2 = (ledger.debt2 / tmp_saldo * 100)
            tot_debt3 = (ledger.debt3 / tmp_saldo * 100)

            if tot_debt0 == None:
                tot_debt0 = 0

            if tot_debt1 == None:
                tot_debt1 = 0

            if tot_debt2 == None:
                tot_debt2 = 0

            if tot_debt3 == None:
                tot_debt3 = 0
            outlist = outlist + to_string(tot_debt0, "           ->>9.99") + to_string(tot_debt1, "           ->>9.99") + to_string(tot_debt2, "           ->>9.99") + to_string(tot_debt3, "           ->>9.99")
            fill_in_list(False, "", None)
            outlist = ""
            fill_in_list(False, "", None)
        outlist = "-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------"
        fill_in_list(False, "----", None)

        if not long_digit:
            outlist = "       " + to_string(translateExtended ("T O T A L  A/R:", lvcarea, "") , "x(30)") + to_string(t_saldo, "->>,>>>,>>>,>>9.99") + to_string(t_prev, "->>,>>>,>>>,>>9.99") + to_string(t_debit, "->>,>>>,>>>,>>9.99") + to_string(t_credit, "->>,>>>,>>>,>>9.99") + to_string(t_debt0, "->>,>>>,>>>,>>9.99") + to_string(t_debt1, "->>,>>>,>>>,>>9.99") + to_string(t_debt2, "->>,>>>,>>>,>>9.99") + to_string(t_debt3, "->>,>>>,>>>,>>9.99")
        else:
            outlist = "       " + to_string(translateExtended ("T O T A L  A/R:", lvcarea, "") , "x(30)") + to_string(t_saldo, "->,>>>,>>>,>>>,>>9") + to_string(t_prev, "->,>>>,>>>,>>>,>>9") + to_string(t_debit, "->,>>>,>>>,>>>,>>9") + to_string(t_credit, "->,>>>,>>>,>>>,>>9") + to_string(t_debt0, "->,>>>,>>>,>>>,>>9") + to_string(t_debt1, "->,>>>,>>>,>>>,>>9") + to_string(t_debt2, "->,>>>,>>>,>>>,>>9") + to_string(t_debt3, "->,>>>,>>>,>>>,>>9")
        fill_in_list(False, "", None)
        outlist = "       " + to_string(translateExtended ("Statistic Percentage (%) :", lvcarea, "") , "x(30)") + "            100.00"
        for i in range(1,54 + 1) :
            outlist = outlist + " "
        tot_debt0 = (t_debt0 / t_saldo * 100)
        tot_debt1 = (t_debt1 / t_saldo * 100)
        tot_debt2 = (t_debt2 / t_saldo * 100)
        tot_debt3 = (t_debt3 / t_saldo * 100)

        if tot_debt0 == None:
            tot_debt0 = 0

        if tot_debt1 == None:
            tot_debt1 = 0

        if tot_debt2 == None:
            tot_debt2 = 0

        if tot_debt3 == None:
            tot_debt3 = 0
        outlist = outlist + to_string(tot_debt0, "           ->>9.99") + to_string(tot_debt1, "           ->>9.99") + to_string(tot_debt2, "           ->>9.99") + to_string(tot_debt3, "           ->>9.99")
        fill_in_list(False, "", None)
        outlist = ""
        fill_in_list(False, "", None)

    def age_list2a():

        nonlocal arage_balance_list_list, curr_art, counter, t_saldo, t_prev, t_debit, t_credit, t_debt0, t_debt1, t_debt2, t_debt3, tmp_saldo, curr_name, curr_gastnr, gastname, p_bal, debit, credit, debt0, debt1, debt2, debt3, curr_counter, curr_fcurr, i, tot_debt, from_date, default_fcurr, outlist, long_digit, curr_rgdatum, bill_number, inp_gastnr, inp_artnr, tot_debtall, tot_debt0, tot_debt1, tot_debt2, tot_debt3, lvcarea, debitor, htparam, artikel, guest, waehrung
        nonlocal debtrec, debt


        nonlocal arage_balance_list, arage_list, age_list, ledger, debtrec, debt
        nonlocal arage_balance_list_list, arage_list_list, age_list_list, ledger_list


        curr_art = 0
        counter = 0
        t_saldo = 0
        t_prev = 0
        t_debit = 0
        t_credit = 0
        t_debt0 = 0
        t_debt1 = 0
        t_debt2 = 0
        t_debt3 = 0
        tmp_saldo = 0
        curr_name = ""
        curr_gastnr = 0
        gastname = ""
        p_bal = 0
        debit = 0
        credit = 0
        debt0 = 0
        debt1 = 0
        debt2 = 0
        debt3 = 0
        tot_debt = 0
        i = 0
        curr_counter = 0
        curr_fcurr = ""


        from_date = fdate

        for artikel in db_session.query(Artikel).filter(
                ((Artikel.artart == 2) |  (Artikel.artart == 7)) &  (Artikel.artnr >= from_art) &  (Artikel.artnr <= to_art) &  (Artikel.departement == 0)).all():
            ledger = Ledger()
            ledger_list.append(ledger)

            ledger.artnr = artikel.artnr
            ledger.bezeich = to_string(artikel.artnr) + "  -  " + artikel.bezeich
        curr_art = 0

        for debitor in db_session.query(Debitor).filter(
                (Debitor.rgdatum <= tdate) &  (Debitor.artnr >= from_art) &  (Debitor.artnr <= to_art) &  (Debitor.opart <= 1)).all():

            if debitor.name.lower()  >= (from_name).lower()  and debitor.name.lower()  <= (to_name).lower() :

                if curr_art != debitor.artnr:
                    curr_art = debitor.artnr

                    artikel = db_session.query(Artikel).filter(
                            (Artikel.artnr == curr_art) &  (Artikel.departement == 0)).first()

                if debitor.counter > 0:

                    age_list = query(age_list_list, filters=(lambda age_list :age_list.counter == debitor.counter), first=True)

                if (debitor.counter == 0) or (not age_list):

                    guest = db_session.query(Guest).filter(
                            (Guest.gastnr == debitor.gastnr)).first()
                    age_list = Age_list()
                    age_list_list.append(age_list)

                    age_list.artnr = debitor.artnr
                    age_list.rechnr = debitor.rechnr
                    age_list.rgdatum = debitor.rgdatum
                    age_list.counter = debitor.counter
                    age_list.gastnr = debitor.gastnr
                    age_list.tot_debt = 0

                    if debitor.betrieb_gastmem == 0:
                        age_list.fcurr = default_fcurr
                    else:

                        waehrung = db_session.query(Waehrung).filter(
                                (Waehrungsnr == debitor.betrieb_gastmem)).first()

                        if waehrung:
                            age_list.fcurr = waehrung.wabkurz

                    if artikel.artart == 2:
                        age_list.gastname = guest.name + ", " + guest.vorname1 + guest.anredefirma + " " + guest.anrede1
                    else:

                        htparam = db_session.query(Htparam).filter(
                                (Htparam.paramnr == 867)).first()

                        if debitor.gastnr == htparam.finteger:
                            age_list.gastname = "F&B " + artikel.bezeich
                        else:
                            age_list.gastname = "F/O " + artikel.bezeich

                if disptype == 0:
                    age_list.tot_debt = age_list.tot_debt + debitor.saldo
                else:
                    age_list.tot_debt = age_list.tot_debt + debitor.vesrdep

                if debitor.rgdatum < from_date and debitor.zahlkonto == 0:

                    if disptype == 0:
                        age_list.p_bal = age_list.p_bal + debitor.saldo
                    else:
                        age_list.p_bal = age_list.p_bal + debitor.vesrdep

                if debitor.rgdatum >= from_date and debitor.zahlkonto == 0:

                    if disptype == 0:
                        age_list.debit = age_list.debit + debitor.saldo
                    else:
                        age_list.debit = age_list.debit + debitor.vesrdep

                if debitor.rgdatum < from_date and debitor.zahlkonto != 0:
                    age_list.p_bal = age_list.p_bal + debitor.saldo
                else:

                    if debitor.rgdatum >= from_date and debitor.zahlkonto != 0:

                        if disptype == 0:
                            age_list.credit = age_list.credit - debitor.saldo
                        else:
                            age_list.credit = age_list.credit - debitor.vesrdep

        for artikel in db_session.query(Artikel).filter(
                ((Artikel.artart == 2) |  (Artikel.artart == 7)) &  (Artikel.artnr >= from_art) &  (Artikel.artnr <= to_art) &  (Artikel.departement == 0)).all():
            curr_counter = 0

            for debitor in db_session.query(Debitor).filter(
                    (Debitor.artnr == artikel.artnr) &  (Debitor.rgdatum <= to_date) &  (Debitor.opart == 2) &  (Debitor.zahlkonto == 0)).all():

                if debitor.name.lower()  >= (from_name).lower()  and debitor.name.lower()  <= (to_name).lower() :

                    guest = db_session.query(Guest).filter(
                            (Guest.gastnr == debitor.gastnr)).first()
                    age_list = Age_list()
                    age_list_list.append(age_list)

                    age_list.artnr = debitor.artnr
                    age_list.rechnr = debitor.rechnr
                    age_list.rgdatum = debitor.rgdatum
                    age_list.counter = debitor.counter
                    age_list.gastnr = debitor.gastnr
                    age_list.tot_debt = debitor.saldo

                    if debitor.betrieb_gastmem == 0:
                        age_list.fcurr = default_fcurr
                    else:

                        waehrung = db_session.query(Waehrung).filter(
                                (Waehrungsnr == debitor.betrieb_gastmem)).first()

                        if waehrung:
                            age_list.fcurr = waehrung.wabkurz

                    if artikel.artart == 2:
                        age_list.gastname = guest.name + ", " + guest.vorname1 + guest.anredefirma + " " + guest.anrede1
                    else:

                        htparam = db_session.query(Htparam).filter(
                                (Htparam.paramnr == 867)).first()

                        if debitor.gastnr == htparam.finteger:
                            age_list.gastname = "F&B " + artikel.bezeich
                        else:
                            age_list.gastname = "F/O " + artikel.bezeich

                    if debitor.rgdatum < from_date:

                        if disptype == 0:
                            age_list.p_bal = age_list.p_bal + debitor.saldo
                        else:
                            age_list.p_bal = age_list.p_bal + debitor.vesrdep

                    elif debitor.rgdatum >= from_date:

                        if disptype == 0:
                            age_list.debit = age_list.debit + debitor.saldo
                        else:
                            age_list.debit = age_list.debit + debitor.vesrdep

                    for debtrec in db_session.query(Debtrec).filter(
                            (Debtrec.counter == debitor.counter) &  (Debtrec.rechnr == debitor.rechnr) &  (Debtrec.zahlkonto > 0) &  (Debtrec.rgdatum <= to_date)).all():
                        age_list.tot_debt = age_list.tot_debt + debtrec.saldo

                        if debtrec.rgdatum < from_date:

                            if disptype == 0:
                                age_list.p_bal = age_list.p_bal + debtrec.saldo
                            else:
                                age_list.p_bal = age_list.p_bal + debtrec.vesrdep

                        elif debtrec.rgdatum >= from_date:

                            if disptype == 0:
                                age_list.credit = age_list.credit - debtrec.saldo
                            else:
                                age_list.credit = age_list.credit - debtrec.vesrdep

        for age_list in query(age_list_list):

            if age_list.p_bal >= - 0.01 and age_list.p_bal <= 0.01 and age_list.debit == 0 and age_list.credit == 0:
                age_list_list.remove(age_list)

        for ledger in query(ledger_list):
            outlist = "    " + ledger.bezeich.upper()
            fill_in_list(False, "", None)
            outlist = ""
            fill_in_list(False, "", None)
            counter = 0
            curr_gastnr = 0

            if mi_bill:

                for age_list in query(age_list_list, filters=(lambda age_list :age_list.artnr == ledger.artnr)):
                    create_output()

            else:

                for age_list in query(age_list_list, filters=(lambda age_list :age_list.artnr == ledger.artnr)):
                    create_output()


            if counter > 0 and (p_bal != 0 or debit != 0 or credit != 0):

                if not long_digit:
                    outlist = "  " + to_string(counter, ">>>9 ") + to_string(gastname, "x(30)") + to_string(tot_debt, "->>,>>>,>>>,>>9.99") + to_string(p_bal, "->>,>>>,>>>,>>9.99") + to_string(debit, "->>,>>>,>>>,>>9.99") + to_string(credit, "->>,>>>,>>>,>>9.99") + to_string(debt0, "->>,>>>,>>>,>>9.99") + to_string(debt1, "->>,>>>,>>>,>>9.99") + to_string(debt2, "->>,>>>,>>>,>>9.99") + to_string(debt3, "->>,>>>,>>>,>>9.99")
                else:
                    outlist = "  " + to_string(counter, ">>>9 ") + to_string(gastname, "x(30)") + to_string(tot_debt, "->,>>>,>>>,>>>,>>9") + to_string(p_bal, "->,>>>,>>>,>>>,>>9") + to_string(debit, "->,>>>,>>>,>>>,>>9") + to_string(credit, "->,>>>,>>>,>>>,>>9") + to_string(debt0, "->,>>>,>>>,>>>,>>9") + to_string(debt1, "->,>>>,>>>,>>>,>>9") + to_string(debt2, "->,>>>,>>>,>>>,>>9") + to_string(debt3, "->,>>>,>>>,>>>,>>9")
                fill_in_list(True, curr_fcurr, curr_rgdatum)
            else:
                counter = counter - 1
            tmp_saldo = ledger.tot_debt

            if tmp_saldo == 0:
                tmp_saldo = 1
            outlist = "-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------"
            fill_in_list(False, "----", None)

            if not long_digit:
                outlist = "       " + to_string(translateExtended ("T o t a l", lvcarea, "") , "x(30)") + to_string(ledger.tot_debt, "->>,>>>,>>>,>>9.99") + to_string(ledger.p_bal, "->>,>>>,>>>,>>9.99") + to_string(ledger.debit, "->>,>>>,>>>,>>9.99") + to_string(ledger.credit, "->>,>>>,>>>,>>9.99") + to_string(ledger.debt0, "->>,>>>,>>>,>>9.99") + to_string(ledger.debt1, "->>,>>>,>>>,>>9.99") + to_string(ledger.debt2, "->>,>>>,>>>,>>9.99") + to_string(ledger.debt3, "->>,>>>,>>>,>>9.99")
            else:
                outlist = "       " + to_string(translateExtended ("T o t a l", lvcarea, "") , "x(30)") + to_string(ledger.tot_debt, "->,>>>,>>>,>>>,>>9") + to_string(ledger.p_bal, "->,>>>,>>>,>>>,>>9") + to_string(ledger.debit, "->,>>>,>>>,>>>,>>9") + to_string(ledger.credit, "->,>>>,>>>,>>>,>>9") + to_string(ledger.debt0, "->,>>>,>>>,>>>,>>9") + to_string(ledger.debt1, "->,>>>,>>>,>>>,>>9") + to_string(ledger.debt2, "->,>>>,>>>,>>>,>>9") + to_string(ledger.debt3, "->,>>>,>>>,>>>,>>9")
            fill_in_list(False, "", None)
            outlist = "       " + to_string(translateExtended ("Statistic Percentage (%) :", lvcarea, "") , "x(30)") + "            100.00"
            for i in range(1,54 + 1) :
                outlist = outlist + " "
            tot_debt0 = (ledger.debt0 / tmp_saldo * 100)
            tot_debt1 = (ledger.debt1 / tmp_saldo * 100)
            tot_debt2 = (ledger.debt2 / tmp_saldo * 100)
            tot_debt3 = (ledger.debt3 / tmp_saldo * 100)

            if tot_debt0 == None:
                tot_debt0 = 0

            if tot_debt1 == None:
                tot_debt1 = 0

            if tot_debt2 == None:
                tot_debt2 = 0

            if tot_debt3 == None:
                tot_debt3 = 0
            outlist = outlist + to_string(tot_debt0, "           ->>9.99") + to_string(tot_debt1, "           ->>9.99") + to_string(tot_debt2, "           ->>9.99") + to_string(tot_debt3, "           ->>9.99")
            fill_in_list(False, "", None)
            outlist = ""
            fill_in_list(False, "", None)
        outlist = "-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------"
        fill_in_list(False, "----", None)

        if not long_digit:
            outlist = "       " + to_string(translateExtended ("T O T A L  A/R:", lvcarea, "") , "x(30)") + to_string(t_saldo, "->>,>>>,>>>,>>9.99") + to_string(t_prev, "->>,>>>,>>>,>>9.99") + to_string(t_debit, "->>,>>>,>>>,>>9.99") + to_string(t_credit, "->>,>>>,>>>,>>9.99") + to_string(t_debt0, "->>,>>>,>>>,>>9.99") + to_string(t_debt1, "->>,>>>,>>>,>>9.99") + to_string(t_debt2, "->>,>>>,>>>,>>9.99") + to_string(t_debt3, "->>,>>>,>>>,>>9.99")
        else:
            outlist = "       " + to_string(translateExtended ("T O T A L  A/R:", lvcarea, "") , "x(30)") + to_string(t_saldo, "->,>>>,>>>,>>>,>>9") + to_string(t_prev, "->,>>>,>>>,>>>,>>9") + to_string(t_debit, "->,>>>,>>>,>>>,>>9") + to_string(t_credit, "->,>>>,>>>,>>>,>>9") + to_string(t_debt0, "->,>>>,>>>,>>>,>>9") + to_string(t_debt1, "->,>>>,>>>,>>>,>>9") + to_string(t_debt2, "->,>>>,>>>,>>>,>>9") + to_string(t_debt3, "->,>>>,>>>,>>>,>>9")
        fill_in_list(False, "", None)
        outlist = "       " + to_string(translateExtended ("Statistic Percentage (%) :", lvcarea, "") , "x(30)") + "            100.00"
        for i in range(1,54 + 1) :
            outlist = outlist + " "
        tot_debt0 = (t_debt0 / t_saldo * 100)
        tot_debt1 = (t_debt1 / t_saldo * 100)
        tot_debt2 = (t_debt2 / t_saldo * 100)
        tot_debt3 = (t_debt3 / t_saldo * 100)

        if tot_debt0 == None:
            tot_debt0 = 0

        if tot_debt1 == None:
            tot_debt1 = 0

        if tot_debt2 == None:
            tot_debt2 = 0

        if tot_debt3 == None:
            tot_debt3 = 0
        outlist = outlist + to_string(tot_debt0, "           ->>9.99") + to_string(tot_debt1, "           ->>9.99") + to_string(tot_debt2, "           ->>9.99") + to_string(tot_debt3, "           ->>9.99")
        fill_in_list(False, "", None)
        outlist = ""
        fill_in_list(False, "", None)

    def create_output():

        nonlocal arage_balance_list_list, curr_art, counter, t_saldo, t_prev, t_debit, t_credit, t_debt0, t_debt1, t_debt2, t_debt3, tmp_saldo, curr_name, curr_gastnr, gastname, p_bal, debit, credit, debt0, debt1, debt2, debt3, curr_counter, curr_fcurr, i, tot_debt, from_date, default_fcurr, outlist, long_digit, curr_rgdatum, bill_number, inp_gastnr, inp_artnr, tot_debtall, tot_debt0, tot_debt1, tot_debt2, tot_debt3, lvcarea, debitor, htparam, artikel, guest, waehrung
        nonlocal debtrec, debt


        nonlocal arage_balance_list, arage_list, age_list, ledger, debtrec, debt
        nonlocal arage_balance_list_list, arage_list_list, age_list_list, ledger_list

        if to_date - age_list.rgdatum > day3:
            age_list.debt3 = age_list.tot_debt

        elif to_date - age_list.rgdatum > day2:
            age_list.debt2 = age_list.tot_debt

        elif to_date - age_list.rgdatum > day1:
            age_list.debt1 = age_list.tot_debt
        else:
            age_list.debt0 = age_list.tot_debt
        ledger.tot_debt = ledger.tot_debt + age_list.tot_debt
        ledger.p_bal = ledger.p_bal + age_list.p_bal
        ledger.debit = ledger.debit + age_list.debit
        ledger.credit = ledger.credit + age_list.credit
        ledger.debt0 = ledger.debt0 + age_list.debt0
        ledger.debt1 = ledger.debt1 + age_list.debt1
        ledger.debt2 = ledger.debt2 + age_list.debt2
        ledger.debt3 = ledger.debt3 + age_list.debt3
        t_saldo = t_saldo + age_list.tot_debt
        t_prev = t_prev + age_list.p_bal
        t_debit = t_debit + age_list.debit
        t_credit = t_credit + age_list.credit
        t_debt0 = t_debt0 + age_list.debt0
        t_debt1 = t_debt1 + age_list.debt1
        t_debt2 = t_debt2 + age_list.debt2
        t_debt3 = t_debt3 + age_list.debt3

        if curr_gastnr == 0:
            curr_rgdatum = age_list.rgdatum
            bill_number = age_list.rechnr
            inp_gastnr = age_list.gastnr
            inp_artnr = age_list.artnr
            gastname = age_list.gastname
            tot_debt = age_list.tot_debt
            p_bal = age_list.p_bal
            debit = age_list.debit
            credit = age_list.credit
            debt0 = age_list.debt0
            debt1 = age_list.debt1
            debt2 = age_list.debt2
            debt3 = age_list.debt3
            counter = counter + 1

        elif curr_name != age_list.gastname:

            if p_bal != 0 or debit != 0 or credit != 0:

                if not long_digit:
                    outlist = "  " + to_string(counter, ">>>9 ") + to_string(gastname, "x(30)") + to_string(tot_debt, "->>,>>>,>>>,>>9.99") + to_string(p_bal, "->>,>>>,>>>,>>9.99") + to_string(debit, "->>,>>>,>>>,>>9.99") + to_string(credit, "->>,>>>,>>>,>>9.99") + to_string(debt0, "->>,>>>,>>>,>>9.99") + to_string(debt1, "->>,>>>,>>>,>>9.99") + to_string(debt2, "->>,>>>,>>>,>>9.99") + to_string(debt3, "->>,>>>,>>>,>>9.99")
                else:
                    outlist = "  " + to_string(counter, ">>>9 ") + to_string(gastname, "x(30)") + to_string(tot_debt, "->,>>>,>>>,>>>,>>9") + to_string(p_bal, "->,>>>,>>>,>>>,>>9") + to_string(debit, "->,>>>,>>>,>>>,>>9") + to_string(credit, "->,>>>,>>>,>>>,>>9") + to_string(debt0, "->,>>>,>>>,>>>,>>9") + to_string(debt1, "->,>>>,>>>,>>>,>>9") + to_string(debt2, "->,>>>,>>>,>>>,>>9") + to_string(debt3, "->,>>>,>>>,>>>,>>9")
                fill_in_list(True, age_list.fcurr, curr_rgdatum)
            else:
                counter = counter - 1
            curr_rgdatum = age_list.rgdatum
            bill_number = age_list.rechnr
            inp_gastnr = age_list.gastnr
            inp_artnr = age_list.artnr
            gastname = age_list.gastname
            tot_debt = age_list.tot_debt
            p_bal = age_list.p_bal
            debit = age_list.debit
            credit = age_list.credit
            debt0 = age_list.debt0
            debt1 = age_list.debt1
            debt2 = age_list.debt2
            debt3 = age_list.debt3
            counter = counter + 1
        else:
            tot_debt = tot_debt + age_list.tot_debt
            p_bal = p_bal + age_list.p_bal
            debit = debit + age_list.debit
            credit = credit + age_list.credit
            debt0 = debt0 + age_list.debt0
            debt1 = debt1 + age_list.debt1
            debt2 = debt2 + age_list.debt2
            debt3 = debt3 + age_list.debt3
        curr_gastnr = age_list.gastnr
        curr_fcurr = age_list.fcurr

        if not detailed:
            curr_name = age_list.gastname
        age_list_list.remove(age_list)

    def fill_in_list(fill_billno:bool, currency:str, curr_rgdatum:date):

        nonlocal arage_balance_list_list, curr_art, counter, t_saldo, t_prev, t_debit, t_credit, t_debt0, t_debt1, t_debt2, t_debt3, tmp_saldo, curr_name, curr_gastnr, gastname, p_bal, debit, credit, debt0, debt1, debt2, debt3, curr_counter, curr_fcurr, i, tot_debt, from_date, default_fcurr, outlist, long_digit, bill_number, inp_gastnr, inp_artnr, tot_debtall, tot_debt0, tot_debt1, tot_debt2, tot_debt3, lvcarea, debitor, htparam, artikel, guest, waehrung
        nonlocal debtrec, debt


        nonlocal arage_balance_list, arage_list, age_list, ledger, debtrec, debt
        nonlocal arage_balance_list_list, arage_list_list, age_list_list, ledger_list


        arage_list = Arage_list()
        arage_list_list.append(arage_list)


        if fill_billno:
            arage_list.rechnr = to_string(bill_number, ">>>>>>>>>")
            arage_list.gastnr = inp_gastnr
            arage_list.artnr = inp_artnr

            if curr_rgdatum != None:
                arage_list.strdate = to_string(curr_rgdatum, "99/99/99")
        arage_list.str = outlist

        if substring(outlist, 0, 5) == "-----":
            arage_list.rechnr = "---------"
            arage_list.strdate = "--------"


        arage_list.age1 = substring(STR, 109, 18)
        arage_list.age2 = substring(STR, 127, 18)
        arage_list.age3 = substring(STR, 145, 18)
        arage_list.age4 = substring(STR, 163, 18)
        arage_list.curr = currency


    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 144)).first()
    default_fcurr = htparam.fchar

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
    arage_balance_list_list.clear()

    for arage_list in query(arage_list_list, filters=(lambda arage_list :substring(arage_list.STR, 0, 7) != "-------")):
        arage_balance_list = Arage_balance_list()
        arage_balance_list_list.append(arage_balance_list)

        arage_balance_list.strdate = arage_list.strdate
        arage_balance_list.curr = arage_list.curr
        arage_balance_list.gastnr = arage_list.gastnr
        arage_balance_list.artnr = arage_list.artnr
        arage_balance_list.age1 = arage_list.age1
        arage_balance_list.age2 = arage_list.age2
        arage_balance_list.age3 = arage_list.age3
        arage_balance_list.age4 = arage_list.age4
        arage_balance_list.rechnr = arage_list.rechnr
        arage_balance_list.num = substring(arage_list.STR, 0, 7)
        arage_balance_list.cust_nm = substring(arage_list.STR, 7, 30)
        arage_balance_list.p_bal = substring(arage_list.STR, 55, 18)
        arage_balance_list.debit = substring(arage_list.STR, 73, 18)
        arage_balance_list.credit = substring(arage_list.STR, 91, 18)
        arage_balance_list.end_bal = substring(arage_list.STR, 37, 18)

    return generate_output()