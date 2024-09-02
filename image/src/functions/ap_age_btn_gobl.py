from functions.additional_functions import *
import decimal
from datetime import date
from functions.htpint import htpint
from sqlalchemy import func
from models import L_kredit, L_lieferant, Queasy

def ap_age_btn_gobl(pvilanguage:int, to_date:date, from_name:str, to_name:str, day1:int, day2:int, day3:int, curr_disp:int):
    output_list_list = []
    outlist:str = ""
    price_decimal:int = 0
    lvcarea:str = "ap_age"
    l_kredit = l_lieferant = queasy = None

    age_list = output_list = debt = None

    age_list_list, Age_list = create_model("Age_list", {"name":str, "counter":int, "lief_nr":int, "rgdatum":date, "supplier":str, "saldo":decimal, "debt0":decimal, "debt1":decimal, "debt2":decimal, "debt3":decimal, "tot_debt":decimal, "adresse1":str, "telefon":str})
    output_list_list, Output_list = create_model("Output_list", {"str":str})

    Debt = L_kredit

    db_session = local_storage.db_session

    def generate_output():
        nonlocal output_list_list, outlist, price_decimal, lvcarea, l_kredit, l_lieferant, queasy
        nonlocal debt


        nonlocal age_list, output_list, debt
        nonlocal age_list_list, output_list_list
        return {"output-list": output_list_list}

    def age_list():

        nonlocal output_list_list, outlist, price_decimal, lvcarea, l_kredit, l_lieferant, queasy
        nonlocal debt


        nonlocal age_list, output_list, debt
        nonlocal age_list_list, output_list_list

        billdate:date = None
        counter:int = 0
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
        curr_liefnr:int = 0
        supplier:str = ""
        debt0:decimal = 0
        debt1:decimal = 0
        debt2:decimal = 0
        debt3:decimal = 0
        tot_debt:decimal = 0
        ap_saldo:decimal = 0
        do_it:bool = False
        Debt = L_kredit
        age_list_list.clear()
        output_list_list.clear()

        l_kredit_obj_list = []
        for l_kredit, l_lieferant in db_session.query(L_kredit, L_lieferant).join(L_lieferant,(L_lieferant.lief_nr == L_kredit.lief_nr) &  (func.lower(L_lieferant.firma) >= (from_name).lower()) &  (func.lower(L_lieferant.firma) <= (to_name).lower())).filter(
                (L_kredit.rgdatum <= to_date) &  (L_kredit.opart == 0)).all():
            if l_kredit._recid in l_kredit_obj_list:
                continue
            else:
                l_kredit_obj_list.append(l_kredit._recid)


            do_it = True

            if l_lieferant.segment1 != 0 and l_lieferant.segment1 != l_lieferant.segment1:
                do_it = False

            if do_it:
                ap_saldo = l_kredit.netto

                if l_kredit.counter != 0:

                    for debt in db_session.query(Debt).filter(
                            (Debt.opart == 1) &  (Debt.counter == l_kredit.counter) &  (Debt.zahlkonto != 0) &  (Debt.rgdatum <= to_date)).all():
                        ap_saldo = ap_saldo + debt.saldo
                age_list = Age_list()
                age_list_list.append(age_list)

                age_list.name = l_kredit.name
                age_list.rgdatum = l_kredit.rgdatum
                age_list.counter = l_kredit.counter
                age_list.lief_nr = l_kredit.lief_nr
                age_list.tot_debt = ap_saldo
                age_list.supplier = trim(l_lieferant.firma + ", " + l_lieferant.anredefirma)
                age_list.adresse1 = l_lieferant.adresse1
                age_list.telefon = l_lieferant.adresse1

        l_kredit_obj_list = []
        for l_kredit, l_lieferant in db_session.query(L_kredit, L_lieferant).join(L_lieferant,(L_lieferant.lief_nr == L_kredit.lief_nr) &  (func.lower(L_lieferant.firma) >= (from_name).lower()) &  (func.lower(L_lieferant.firma) <= (to_name).lower())).filter(
                (L_kredit.rgdatum <= to_date) &  (L_kredit.opart == 2) &  (L_kredit.zahlkonto == 0)).all():
            if l_kredit._recid in l_kredit_obj_list:
                continue
            else:
                l_kredit_obj_list.append(l_kredit._recid)


            do_it = True

            if l_lieferant.segment1 != 0 and l_lieferant.segment1 != l_lieferant.segment1:
                do_it = False

            if do_it:
                ap_saldo = l_kredit.netto

                for debt in db_session.query(Debt).filter(
                        (Debt.counter == l_kredit.counter) &  (Debt.opart == 2) &  (Debt.zahlkonto != 0) &  (Debt.rgdatum <= to_date)).all():
                    ap_saldo = ap_saldo + debt.saldo
                age_list = Age_list()
                age_list_list.append(age_list)

                age_list.name = l_kredit.name
                age_list.rgdatum = l_kredit.rgdatum
                age_list.counter = l_kredit.counter
                age_list.lief_nr = l_kredit.lief_nr
                age_list.tot_debt = ap_saldo
                age_list.supplier = l_lieferant.firma + ", " + l_lieferant.anredefirma
                age_list.adresse1 = l_lieferant.adresse1
                age_list.telefon = l_lieferant.adresse1
        curr_liefnr = 0
        counter = 0

        for age_list in query(age_list_list, filters=(lambda age_list :age_list.tot_debt != 0)):

            if to_date - age_list.rgdatum > day3:
                age_list.debt3 = age_list.tot_debt

            elif to_date - age_list.rgdatum > day2:
                age_list.debt2 = age_list.tot_debt

            elif to_date - age_list.rgdatum > day1:
                age_list.debt1 = age_list.tot_debt
            else:
                age_list.debt0 = age_list.tot_debt
            t_saldo = t_saldo + round(age_list.tot_debt, 0)
            t_debt0 = t_debt0 + round(age_list.debt0, 0)
            t_debt1 = t_debt1 + round(age_list.debt1, 0)
            t_debt2 = t_debt2 + round(age_list.debt2, 0)
            t_debt3 = t_debt3 + round(age_list.debt3, 0)

            if curr_liefnr == 0:
                supplier = age_list.supplier
                tot_debt = round(age_list.tot_debt, 0)
                debt0 = round(age_list.debt0, 0)
                debt1 = round(age_list.debt1, 0)
                debt2 = round(age_list.debt2, 0)
                debt3 = round(age_list.debt3, 0)
                counter = counter + 1

            elif curr_name != age_list.supplier:

                if tot_debt != 0:

                    if price_decimal == 0:
                        outlist = "  " + to_string(counter, ">>>9") + "  " + to_string(supplier, "x(34)") + "  " + to_string(tot_debt, "->,>>>,>>>,>>>,>>9") + "  " + to_string(debt0, "->,>>>,>>>,>>>,>>9") + "  " + to_string(debt1, "->,>>>,>>>,>>>,>>9") + "  " + to_string(debt2, "->,>>>,>>>,>>>,>>9") + "  " + to_string(debt3, "->,>>>,>>>,>>>,>>9") + "  "
                    else:
                        outlist = "  " + to_string(counter, ">>>9") + "  " + to_string(supplier, "x(34)") + "  " + to_string(tot_debt, "->>,>>>,>>>,>>9.99") + "  " + to_string(debt0, "->>,>>>,>>>,>>9.99") + "  " + to_string(debt1, "->>,>>>,>>>,>>9.99") + "  " + to_string(debt2, "->>,>>>,>>>,>>9.99") + "  " + to_string(debt3, "->>,>>>,>>>,>>9.99") + "  "
                    fill_in_list()
                else:
                    counter = counter - 1
                supplier = age_list.supplier
                tot_debt = round(age_list.tot_debt, 0)
                debt0 = round(age_list.debt0, 0)
                debt1 = round(age_list.debt1, 0)
                debt2 = round(age_list.debt2, 0)
                debt3 = round(age_list.debt3, 0)
                counter = counter + 1
            else:
                tot_debt = tot_debt + round(age_list.tot_debt, 0)
                debt0 = debt0 + round(age_list.debt0, 0)
                debt1 = debt1 + round(age_list.debt1, 0)
                debt2 = debt2 + round(age_list.debt2, 0)
                debt3 = debt3 + round(age_list.debt3, 0)
            curr_liefnr = age_list.lief_nr
            curr_name = age_list.supplier
            age_list_list.remove(age_list)

        if counter > 0 and tot_debt != 0:

            if price_decimal == 0:
                outlist = "  " + to_string(counter, ">>>9") + "  " + to_string(supplier, "x(34)") + "  " + to_string(tot_debt, "->,>>>,>>>,>>>,>>9") + "  " + to_string(debt0, "->,>>>,>>>,>>>,>>9") + "  " + to_string(debt1, "->,>>>,>>>,>>>,>>9") + "  " + to_string(debt2, "->,>>>,>>>,>>>,>>9") + "  " + to_string(debt3, "->,>>>,>>>,>>>,>>9") + "  "
            else:
                outlist = "  " + to_string(counter, ">>>9") + "  " + to_string(supplier, "x(34)") + "  " + to_string(tot_debt, "->>,>>>,>>>,>>9.99") + "  " + to_string(debt0, "->>,>>>,>>>,>>9.99") + "  " + to_string(debt1, "->>,>>>,>>>,>>9.99") + "  " + to_string(debt2, "->>,>>>,>>>,>>9.99") + "  " + to_string(debt3, "->>,>>>,>>>,>>9.99") + "  "
            fill_in_list()
        outlist = "-------------------------------------------------------------------------------------------------------------------------------------------------"
        fill_in_list()

        if price_decimal == 0:
            outlist = to_string(translateExtended ("           T O T A L  A/P:", lvcarea, "") , "x(26)") + "                  " + to_string(t_saldo, "->,>>>,>>>,>>>,>>9") + "  " + to_string(t_debt0, "->,>>>,>>>,>>>,>>9") + "  " + to_string(t_debt1, "->,>>>,>>>,>>>,>>9") + "  " + to_string(t_debt2, "->,>>>,>>>,>>>,>>9") + "  " + to_string(t_debt3, "->,>>>,>>>,>>>,>>9")
        else:
            outlist = to_string(translateExtended ("           T O T A L  A/P:", lvcarea, "") , "x(26)") + "                  " + to_string(t_saldo, "->>,>>>,>>>,>>9.99") + "  " + to_string(t_debt0, "->>,>>>,>>>,>>9.99") + "  " + to_string(t_debt1, "->>,>>>,>>>,>>9.99") + "  " + to_string(t_debt2, "->>,>>>,>>>,>>9.99") + "  " + to_string(t_debt3, "->>,>>>,>>>,>>9.99")
        fill_in_list()
        outlist = ""
        fill_in_list()
        outlist = to_string(translateExtended ("        Statistic Percentage (%) :", lvcarea, "") , "x(33)") + "                      " + "100.00" + "             " + to_string((t_debt0 / t_saldo * 100) , "->>9.99") + "             " + to_string((t_debt1 / t_saldo * 100) , "->>9.99") + "             " + to_string((t_debt2 / t_saldo * 100) , "->>9.99") + "             " + to_string((t_debt3 / t_saldo * 100) , "->>9.99")
        fill_in_list()
        outlist = ""
        fill_in_list()

    def age_list1():

        nonlocal output_list_list, outlist, price_decimal, lvcarea, l_kredit, l_lieferant, queasy
        nonlocal debt


        nonlocal age_list, output_list, debt
        nonlocal age_list_list, output_list_list

        billdate:date = None
        counter:int = 0
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
        curr_liefnr:int = 0
        supplier:str = ""
        debt0:decimal = 0
        debt1:decimal = 0
        debt2:decimal = 0
        debt3:decimal = 0
        tot_debt:decimal = 0
        ap_saldo:decimal = 0
        do_it:bool = False
        Debt = L_kredit
        age_list_list.clear()
        output_list_list.clear()

        l_kredit_obj_list = []
        for l_kredit, l_lieferant in db_session.query(L_kredit, L_lieferant).join(L_lieferant,(L_lieferant.lief_nr == L_kredit.lief_nr) &  (func.lower(L_lieferant.firma) >= (from_name).lower()) &  (func.lower(L_lieferant.firma) <= (to_name).lower()) &  (L_kredit.steuercode == 1)).filter(
                (L_kredit.rgdatum <= to_date) &  (L_kredit.opart == 0)).all():
            if l_kredit._recid in l_kredit_obj_list:
                continue
            else:
                l_kredit_obj_list.append(l_kredit._recid)


            do_it = True

            if l_lieferant.segment1 != 0 and l_lieferant.segment1 != l_lieferant.segment1:
                do_it = False

            if do_it:
                ap_saldo = l_kredit.netto

                if l_kredit.counter != 0:

                    for debt in db_session.query(Debt).filter(
                            (Debt.opart == 1) &  (Debt.counter == l_kredit.counter) &  (Debt.zahlkonto != 0) &  (Debt.rgdatum <= to_date)).all():
                        ap_saldo = ap_saldo + debt.saldo
                age_list = Age_list()
                age_list_list.append(age_list)

                age_list.name = l_kredit.name
                age_list.rgdatum = l_kredit.rgdatum
                age_list.counter = l_kredit.counter
                age_list.lief_nr = l_kredit.lief_nr
                age_list.tot_debt = ap_saldo
                age_list.supplier = trim(l_lieferant.firma + ", " + l_lieferant.anredefirma)
                age_list.adresse1 = l_lieferant.adresse1
                age_list.telefon = l_lieferant.adresse1

        l_kredit_obj_list = []
        for l_kredit, l_lieferant in db_session.query(L_kredit, L_lieferant).join(L_lieferant,(L_lieferant.lief_nr == L_kredit.lief_nr) &  (func.lower(L_lieferant.firma) >= (from_name).lower()) &  (func.lower(L_lieferant.firma) <= (to_name).lower()) &  (L_kredit.steuercode == 1)).filter(
                (L_kredit.rgdatum <= to_date) &  (L_kredit.opart == 2) &  (L_kredit.zahlkonto == 0)).all():
            if l_kredit._recid in l_kredit_obj_list:
                continue
            else:
                l_kredit_obj_list.append(l_kredit._recid)


            do_it = True

            if l_lieferant.segment1 != 0 and l_lieferant.segment1 != l_lieferant.segment1:
                do_it = False

            if do_it:
                ap_saldo = l_kredit.netto

                for debt in db_session.query(Debt).filter(
                        (Debt.counter == l_kredit.counter) &  (Debt.opart == 2) &  (Debt.zahlkonto != 0) &  (Debt.rgdatum <= to_date)).all():
                    ap_saldo = ap_saldo + debt.saldo
                age_list = Age_list()
                age_list_list.append(age_list)

                age_list.name = l_kredit.name
                age_list.rgdatum = l_kredit.rgdatum
                age_list.counter = l_kredit.counter
                age_list.lief_nr = l_kredit.lief_nr
                age_list.tot_debt = ap_saldo
                age_list.supplier = l_lieferant.firma + ", " + l_lieferant.anredefirma
                age_list.adresse1 = l_lieferant.adresse1
                age_list.telefon = l_lieferant.adresse1
        curr_liefnr = 0
        counter = 0

        for age_list in query(age_list_list, filters=(lambda age_list :age_list.tot_debt != 0)):

            if to_date - age_list.rgdatum > day3:
                age_list.debt3 = age_list.tot_debt

            elif to_date - age_list.rgdatum > day2:
                age_list.debt2 = age_list.tot_debt

            elif to_date - age_list.rgdatum > day1:
                age_list.debt1 = age_list.tot_debt
            else:
                age_list.debt0 = age_list.tot_debt
            t_saldo = t_saldo + round(age_list.tot_debt, 0)
            t_debt0 = t_debt0 + round(age_list.debt0, 0)
            t_debt1 = t_debt1 + round(age_list.debt1, 0)
            t_debt2 = t_debt2 + round(age_list.debt2, 0)
            t_debt3 = t_debt3 + round(age_list.debt3, 0)

            if curr_liefnr == 0:
                supplier = age_list.supplier
                tot_debt = round(age_list.tot_debt, 0)
                debt0 = round(age_list.debt0, 0)
                debt1 = round(age_list.debt1, 0)
                debt2 = round(age_list.debt2, 0)
                debt3 = round(age_list.debt3, 0)
                counter = counter + 1

            elif curr_name != age_list.supplier:

                if tot_debt != 0:

                    if price_decimal == 0:
                        outlist = "  " + to_string(counter, ">>>9") + "  " + to_string(supplier, "x(34)") + "  " + to_string(tot_debt, "->,>>>,>>>,>>>,>>9") + "  " + to_string(debt0, "->,>>>,>>>,>>>,>>9") + "  " + to_string(debt1, "->,>>>,>>>,>>>,>>9") + "  " + to_string(debt2, "->,>>>,>>>,>>>,>>9") + "  " + to_string(debt3, "->,>>>,>>>,>>>,>>9") + "  "
                    else:
                        outlist = "  " + to_string(counter, ">>>9") + "  " + to_string(supplier, "x(34)") + "  " + to_string(tot_debt, "->>,>>>,>>>,>>9.99") + "  " + to_string(debt0, "->>,>>>,>>>,>>9.99") + "  " + to_string(debt1, "->>,>>>,>>>,>>9.99") + "  " + to_string(debt2, "->>,>>>,>>>,>>9.99") + "  " + to_string(debt3, "->>,>>>,>>>,>>9.99") + "  "
                    fill_in_list()
                else:
                    counter = counter - 1
                supplier = age_list.supplier
                tot_debt = round(age_list.tot_debt, 0)
                debt0 = round(age_list.debt0, 0)
                debt1 = round(age_list.debt1, 0)
                debt2 = round(age_list.debt2, 0)
                debt3 = round(age_list.debt3, 0)
                counter = counter + 1
            else:
                tot_debt = tot_debt + round(age_list.tot_debt, 0)
                debt0 = debt0 + round(age_list.debt0, 0)
                debt1 = debt1 + round(age_list.debt1, 0)
                debt2 = debt2 + round(age_list.debt2, 0)
                debt3 = debt3 + round(age_list.debt3, 0)
            curr_liefnr = age_list.lief_nr
            curr_name = age_list.supplier
            age_list_list.remove(age_list)

        if counter > 0 and tot_debt != 0:

            if price_decimal == 0:
                outlist = "  " + to_string(counter, ">>>9") + "  " + to_string(supplier, "x(34)") + "  " + to_string(tot_debt, "->,>>>,>>>,>>>,>>9") + "  " + to_string(debt0, "->,>>>,>>>,>>>,>>9") + "  " + to_string(debt1, "->,>>>,>>>,>>>,>>9") + "  " + to_string(debt2, "->,>>>,>>>,>>>,>>9") + "  " + to_string(debt3, "->,>>>,>>>,>>>,>>9") + "  "
            else:
                outlist = "  " + to_string(counter, ">>>9") + "  " + to_string(supplier, "x(34)") + "  " + to_string(tot_debt, "->>,>>>,>>>,>>9.99") + "  " + to_string(debt0, "->>,>>>,>>>,>>9.99") + "  " + to_string(debt1, "->>,>>>,>>>,>>9.99") + "  " + to_string(debt2, "->>,>>>,>>>,>>9.99") + "  " + to_string(debt3, "->>,>>>,>>>,>>9.99") + "  "
            fill_in_list()
        outlist = "-------------------------------------------------------------------------------------------------------------------------------------------------"
        fill_in_list()

        if price_decimal == 0:
            outlist = to_string(translateExtended ("           T O T A L  A/P:", lvcarea, "") , "x(26)") + "                  " + to_string(t_saldo, "->,>>>,>>>,>>>,>>9") + "  " + to_string(t_debt0, "->,>>>,>>>,>>>,>>9") + "  " + to_string(t_debt1, "->,>>>,>>>,>>>,>>9") + "  " + to_string(t_debt2, "->,>>>,>>>,>>>,>>9") + "  " + to_string(t_debt3, "->,>>>,>>>,>>>,>>9")
        else:
            outlist = to_string(translateExtended ("           T O T A L  A/P:", lvcarea, "") , "x(26)") + "                  " + to_string(t_saldo, "->>,>>>,>>>,>>9.99") + "  " + to_string(t_debt0, "->>,>>>,>>>,>>9.99") + "  " + to_string(t_debt1, "->>,>>>,>>>,>>9.99") + "  " + to_string(t_debt2, "->>,>>>,>>>,>>9.99") + "  " + to_string(t_debt3, "->>,>>>,>>>,>>9.99")
        fill_in_list()
        outlist = ""
        fill_in_list()
        outlist = to_string(translateExtended ("        Statistic Percentage (%) :", lvcarea, "") , "x(33)") + "                      " + "100.00" + "             " + to_string((t_debt0 / t_saldo * 100) , "->>9.99") + "             " + to_string((t_debt1 / t_saldo * 100) , "->>9.99") + "             " + to_string((t_debt2 / t_saldo * 100) , "->>9.99") + "             " + to_string((t_debt3 / t_saldo * 100) , "->>9.99")
        fill_in_list()
        outlist = ""
        fill_in_list()

    def age_list2():

        nonlocal output_list_list, outlist, price_decimal, lvcarea, l_kredit, l_lieferant, queasy
        nonlocal debt


        nonlocal age_list, output_list, debt
        nonlocal age_list_list, output_list_list

        billdate:date = None
        counter:int = 0
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
        curr_liefnr:int = 0
        supplier:str = ""
        debt0:decimal = 0
        debt1:decimal = 0
        debt2:decimal = 0
        debt3:decimal = 0
        tot_debt:decimal = 0
        ap_saldo:decimal = 0
        do_it:bool = False
        Debt = L_kredit
        age_list_list.clear()
        output_list_list.clear()

        l_kredit_obj_list = []
        for l_kredit, l_lieferant in db_session.query(L_kredit, L_lieferant).join(L_lieferant,(L_lieferant.lief_nr == L_kredit.lief_nr) &  (func.lower(L_lieferant.firma) >= (from_name).lower()) &  (func.lower(L_lieferant.firma) <= (to_name).lower()) &  (L_kredit.steuercode == 0)).filter(
                (L_kredit.rgdatum <= to_date) &  (L_kredit.opart == 0)).all():
            if l_kredit._recid in l_kredit_obj_list:
                continue
            else:
                l_kredit_obj_list.append(l_kredit._recid)


            do_it = True

            if l_lieferant.segment1 != 0 and l_lieferant.segment1 != l_lieferant.segment1:
                do_it = False

            if do_it:
                ap_saldo = l_kredit.netto

                if l_kredit.counter != 0:

                    for debt in db_session.query(Debt).filter(
                            (Debt.opart == 1) &  (Debt.counter == l_kredit.counter) &  (Debt.zahlkonto != 0) &  (Debt.rgdatum <= to_date)).all():
                        ap_saldo = ap_saldo + debt.saldo
                age_list = Age_list()
                age_list_list.append(age_list)

                age_list.name = l_kredit.name
                age_list.rgdatum = l_kredit.rgdatum
                age_list.counter = l_kredit.counter
                age_list.lief_nr = l_kredit.lief_nr
                age_list.tot_debt = ap_saldo
                age_list.supplier = trim(l_lieferant.firma + ", " + l_lieferant.anredefirma)
                age_list.adresse1 = l_lieferant.adresse1
                age_list.telefon = l_lieferant.adresse1

        l_kredit_obj_list = []
        for l_kredit, l_lieferant in db_session.query(L_kredit, L_lieferant).join(L_lieferant,(L_lieferant.lief_nr == L_kredit.lief_nr) &  (func.lower(L_lieferant.firma) >= (from_name).lower()) &  (func.lower(L_lieferant.firma) <= (to_name).lower()) &  (L_kredit.steuercode == 0)).filter(
                (L_kredit.rgdatum <= to_date) &  (L_kredit.opart == 2) &  (L_kredit.zahlkonto == 0)).all():
            if l_kredit._recid in l_kredit_obj_list:
                continue
            else:
                l_kredit_obj_list.append(l_kredit._recid)


            do_it = True

            if l_lieferant.segment1 != 0 and l_lieferant.segment1 != l_lieferant.segment1:
                do_it = False

            if do_it:
                ap_saldo = l_kredit.netto

                for debt in db_session.query(Debt).filter(
                        (Debt.counter == l_kredit.counter) &  (Debt.opart == 2) &  (Debt.zahlkonto != 0) &  (Debt.rgdatum <= to_date)).all():
                    ap_saldo = ap_saldo + debt.saldo
                age_list = Age_list()
                age_list_list.append(age_list)

                age_list.name = l_kredit.name
                age_list.rgdatum = l_kredit.rgdatum
                age_list.counter = l_kredit.counter
                age_list.lief_nr = l_kredit.lief_nr
                age_list.tot_debt = ap_saldo
                age_list.supplier = l_lieferant.firma + ", " + l_lieferant.anredefirma
                age_list.adresse1 = l_lieferant.adresse1
                age_list.telefon = l_lieferant.adresse1
        curr_liefnr = 0
        counter = 0

        for age_list in query(age_list_list, filters=(lambda age_list :age_list.tot_debt != 0)):

            if to_date - age_list.rgdatum > day3:
                age_list.debt3 = age_list.tot_debt

            elif to_date - age_list.rgdatum > day2:
                age_list.debt2 = age_list.tot_debt

            elif to_date - age_list.rgdatum > day1:
                age_list.debt1 = age_list.tot_debt
            else:
                age_list.debt0 = age_list.tot_debt
            t_saldo = t_saldo + round(age_list.tot_debt, 0)
            t_debt0 = t_debt0 + round(age_list.debt0, 0)
            t_debt1 = t_debt1 + round(age_list.debt1, 0)
            t_debt2 = t_debt2 + round(age_list.debt2, 0)
            t_debt3 = t_debt3 + round(age_list.debt3, 0)

            if curr_liefnr == 0:
                supplier = age_list.supplier
                tot_debt = round(age_list.tot_debt, 0)
                debt0 = round(age_list.debt0, 0)
                debt1 = round(age_list.debt1, 0)
                debt2 = round(age_list.debt2, 0)
                debt3 = round(age_list.debt3, 0)
                counter = counter + 1

            elif curr_name != age_list.supplier:

                if tot_debt != 0:

                    if price_decimal == 0:
                        outlist = "  " + to_string(counter, ">>>9") + "  " + to_string(supplier, "x(34)") + "  " + to_string(tot_debt, "->,>>>,>>>,>>>,>>9") + "  " + to_string(debt0, "->,>>>,>>>,>>>,>>9") + "  " + to_string(debt1, "->,>>>,>>>,>>>,>>9") + "  " + to_string(debt2, "->,>>>,>>>,>>>,>>9") + "  " + to_string(debt3, "->,>>>,>>>,>>>,>>9") + "  "
                    else:
                        outlist = "  " + to_string(counter, ">>>9") + "  " + to_string(supplier, "x(34)") + "  " + to_string(tot_debt, "->>,>>>,>>>,>>9.99") + "  " + to_string(debt0, "->>,>>>,>>>,>>9.99") + "  " + to_string(debt1, "->>,>>>,>>>,>>9.99") + "  " + to_string(debt2, "->>,>>>,>>>,>>9.99") + "  " + to_string(debt3, "->>,>>>,>>>,>>9.99") + "  "
                    fill_in_list()
                else:
                    counter = counter - 1
                supplier = age_list.supplier
                tot_debt = round(age_list.tot_debt, 0)
                debt0 = round(age_list.debt0, 0)
                debt1 = round(age_list.debt1, 0)
                debt2 = round(age_list.debt2, 0)
                debt3 = round(age_list.debt3, 0)
                counter = counter + 1
            else:
                tot_debt = tot_debt + round(age_list.tot_debt, 0)
                debt0 = debt0 + round(age_list.debt0, 0)
                debt1 = debt1 + round(age_list.debt1, 0)
                debt2 = debt2 + round(age_list.debt2, 0)
                debt3 = debt3 + round(age_list.debt3, 0)
            curr_liefnr = age_list.lief_nr
            curr_name = age_list.supplier
            age_list_list.remove(age_list)

        if counter > 0 and tot_debt != 0:

            if price_decimal == 0:
                outlist = "  " + to_string(counter, ">>>9") + "  " + to_string(supplier, "x(34)") + "  " + to_string(tot_debt, "->,>>>,>>>,>>>,>>9") + "  " + to_string(debt0, "->,>>>,>>>,>>>,>>9") + "  " + to_string(debt1, "->,>>>,>>>,>>>,>>9") + "  " + to_string(debt2, "->,>>>,>>>,>>>,>>9") + "  " + to_string(debt3, "->,>>>,>>>,>>>,>>9") + "  "
            else:
                outlist = "  " + to_string(counter, ">>>9") + "  " + to_string(supplier, "x(34)") + "  " + to_string(tot_debt, "->>,>>>,>>>,>>9.99") + "  " + to_string(debt0, "->>,>>>,>>>,>>9.99") + "  " + to_string(debt1, "->>,>>>,>>>,>>9.99") + "  " + to_string(debt2, "->>,>>>,>>>,>>9.99") + "  " + to_string(debt3, "->>,>>>,>>>,>>9.99") + "  "
            fill_in_list()
        outlist = "-------------------------------------------------------------------------------------------------------------------------------------------------"
        fill_in_list()

        if price_decimal == 0:
            outlist = to_string(translateExtended ("           T O T A L  A/P:", lvcarea, "") , "x(26)") + "                  " + to_string(t_saldo, "->,>>>,>>>,>>>,>>9") + "  " + to_string(t_debt0, "->,>>>,>>>,>>>,>>9") + "  " + to_string(t_debt1, "->,>>>,>>>,>>>,>>9") + "  " + to_string(t_debt2, "->,>>>,>>>,>>>,>>9") + "  " + to_string(t_debt3, "->,>>>,>>>,>>>,>>9")
        else:
            outlist = to_string(translateExtended ("           T O T A L  A/P:", lvcarea, "") , "x(26)") + "                  " + to_string(t_saldo, "->>,>>>,>>>,>>9.99") + "  " + to_string(t_debt0, "->>,>>>,>>>,>>9.99") + "  " + to_string(t_debt1, "->>,>>>,>>>,>>9.99") + "  " + to_string(t_debt2, "->>,>>>,>>>,>>9.99") + "  " + to_string(t_debt3, "->>,>>>,>>>,>>9.99")
        fill_in_list()
        outlist = ""
        fill_in_list()
        outlist = to_string(translateExtended ("        Statistic Percentage (%) :", lvcarea, "") , "x(33)") + "                      " + "100.00" + "             " + to_string((t_debt0 / t_saldo * 100) , "->>9.99") + "             " + to_string((t_debt1 / t_saldo * 100) , "->>9.99") + "             " + to_string((t_debt2 / t_saldo * 100) , "->>9.99") + "             " + to_string((t_debt3 / t_saldo * 100) , "->>9.99")
        fill_in_list()
        outlist = ""
        fill_in_list()

    def age_list3():

        nonlocal output_list_list, outlist, price_decimal, lvcarea, l_kredit, l_lieferant, queasy
        nonlocal debt


        nonlocal age_list, output_list, debt
        nonlocal age_list_list, output_list_list

        billdate:date = None
        counter:int = 0
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
        curr_liefnr:int = 0
        supplier:str = ""
        debt0:decimal = 0
        debt1:decimal = 0
        debt2:decimal = 0
        debt3:decimal = 0
        tot_debt:decimal = 0
        t_date:date = None
        ap_saldo:decimal = 0
        do_it:bool = False
        Debt = L_kredit
        age_list_list.clear()
        output_list_list.clear()

        l_kredit_obj_list = []
        for l_kredit, l_lieferant in db_session.query(L_kredit, L_lieferant).join(L_lieferant,(L_lieferant.lief_nr == L_kredit.lief_nr) &  (func.lower(L_lieferant.firma) >= (from_name).lower()) &  (func.lower(L_lieferant.firma) <= (to_name).lower())).filter(
                (L_kredit.rgdatum <= to_date) &  (L_kredit.opart == 0)).all():
            if l_kredit._recid in l_kredit_obj_list:
                continue
            else:
                l_kredit_obj_list.append(l_kredit._recid)


            do_it = True

            if l_lieferant.segment1 != 0 and l_lieferant.segment1 != l_lieferant.segment1:
                do_it = False

            if do_it:

                queasy = db_session.query(Queasy).filter(
                        (Queasy.key == 221) &  (Queasy.number1 == l_kredit.lief_nr) &  (Queasy.char1 == l_kredit.name)).first()

                if queasy:
                    ap_saldo = l_kredit.netto

                    if l_kredit.counter != 0:

                        for debt in db_session.query(Debt).filter(
                                (Debt.opart == 1) &  (Debt.counter == l_kredit.counter) &  (Debt.zahlkonto != 0) &  (Debt.rgdatum <= to_date)).all():
                            ap_saldo = ap_saldo + debt.saldo
                    age_list = Age_list()
                    age_list_list.append(age_list)

                    age_list.name = l_kredit.name
                    age_list.rgdatum = queasy.date1
                    age_list.counter = l_kredit.counter
                    age_list.lief_nr = l_kredit.lief_nr
                    age_list.tot_debt = ap_saldo
                    age_list.supplier = trim(l_lieferant.firma + ", " + l_lieferant.anredefirma)
                    age_list.adresse1 = l_lieferant.adresse1
                    age_list.telefon = l_lieferant.adresse1

        l_kredit_obj_list = []
        for l_kredit, l_lieferant in db_session.query(L_kredit, L_lieferant).join(L_lieferant,(L_lieferant.lief_nr == L_kredit.lief_nr) &  (func.lower(L_lieferant.firma) >= (from_name).lower()) &  (func.lower(L_lieferant.firma) <= (to_name).lower())).filter(
                (L_kredit.rgdatum <= to_date) &  (L_kredit.opart == 2) &  (L_kredit.zahlkonto == 0)).all():
            if l_kredit._recid in l_kredit_obj_list:
                continue
            else:
                l_kredit_obj_list.append(l_kredit._recid)


            do_it = True

            if l_lieferant.segment1 != 0 and l_lieferant.segment1 != l_lieferant.segment1:
                do_it = False

            if do_it:

                queasy = db_session.query(Queasy).filter(
                        (Queasy.key == 221) &  (Queasy.number1 == l_kredit.lief_nr) &  (Queasy.char1 == l_kredit.name)).first()

                if queasy:
                    ap_saldo = l_kredit.netto

                    for debt in db_session.query(Debt).filter(
                            (Debt.counter == l_kredit.counter) &  (Debt.opart == 2) &  (Debt.zahlkonto != 0) &  (Debt.rgdatum <= to_date)).all():
                        ap_saldo = ap_saldo + debt.saldo
                    age_list = Age_list()
                    age_list_list.append(age_list)

                    age_list.name = l_kredit.name
                    age_list.rgdatum = queasy.date1
                    age_list.counter = l_kredit.counter
                    age_list.lief_nr = l_kredit.lief_nr
                    age_list.tot_debt = ap_saldo
                    age_list.supplier = l_lieferant.firma + ", " + l_lieferant.anredefirma
                    age_list.adresse1 = l_lieferant.adresse1
                    age_list.telefon = l_lieferant.adresse1
        curr_liefnr = 0
        counter = 0

        for age_list in query(age_list_list, filters=(lambda age_list :age_list.tot_debt != 0)):

            if to_date - age_list.rgdatum > day3:
                age_list.debt3 = age_list.tot_debt

            elif to_date - age_list.rgdatum > day2:
                age_list.debt2 = age_list.tot_debt

            elif to_date - age_list.rgdatum > day1:
                age_list.debt1 = age_list.tot_debt
            else:
                age_list.debt0 = age_list.tot_debt
            t_saldo = t_saldo + round(age_list.tot_debt, 0)
            t_debt0 = t_debt0 + round(age_list.debt0, 0)
            t_debt1 = t_debt1 + round(age_list.debt1, 0)
            t_debt2 = t_debt2 + round(age_list.debt2, 0)
            t_debt3 = t_debt3 + round(age_list.debt3, 0)

            if curr_liefnr == 0:
                supplier = age_list.supplier
                tot_debt = round(age_list.tot_debt, 0)
                debt0 = round(age_list.debt0, 0)
                debt1 = round(age_list.debt1, 0)
                debt2 = round(age_list.debt2, 0)
                debt3 = round(age_list.debt3, 0)
                counter = counter + 1

            elif curr_name != age_list.supplier:

                if tot_debt != 0:

                    if price_decimal == 0:
                        outlist = "  " + to_string(counter, ">>>9") + "  " + to_string(supplier, "x(34)") + "  " + to_string(tot_debt, "->,>>>,>>>,>>>,>>9") + "  " + to_string(debt0, "->,>>>,>>>,>>>,>>9") + "  " + to_string(debt1, "->,>>>,>>>,>>>,>>9") + "  " + to_string(debt2, "->,>>>,>>>,>>>,>>9") + "  " + to_string(debt3, "->,>>>,>>>,>>>,>>9") + "  "
                    else:
                        outlist = "  " + to_string(counter, ">>>9") + "  " + to_string(supplier, "x(34)") + "  " + to_string(tot_debt, "->>,>>>,>>>,>>9.99") + "  " + to_string(debt0, "->>,>>>,>>>,>>9.99") + "  " + to_string(debt1, "->>,>>>,>>>,>>9.99") + "  " + to_string(debt2, "->>,>>>,>>>,>>9.99") + "  " + to_string(debt3, "->>,>>>,>>>,>>9.99") + "  "
                    fill_in_list()
                else:
                    counter = counter - 1
                supplier = age_list.supplier
                tot_debt = round(age_list.tot_debt, 0)
                debt0 = round(age_list.debt0, 0)
                debt1 = round(age_list.debt1, 0)
                debt2 = round(age_list.debt2, 0)
                debt3 = round(age_list.debt3, 0)
                counter = counter + 1
            else:
                tot_debt = tot_debt + round(age_list.tot_debt, 0)
                debt0 = debt0 + round(age_list.debt0, 0)
                debt1 = debt1 + round(age_list.debt1, 0)
                debt2 = debt2 + round(age_list.debt2, 0)
                debt3 = debt3 + round(age_list.debt3, 0)
            curr_liefnr = age_list.lief_nr
            curr_name = age_list.supplier
            age_list_list.remove(age_list)

        if counter > 0 and tot_debt != 0:

            if price_decimal == 0:
                outlist = "  " + to_string(counter, ">>>9") + "  " + to_string(supplier, "x(34)") + "  " + to_string(tot_debt, "->,>>>,>>>,>>>,>>9") + "  " + to_string(debt0, "->,>>>,>>>,>>>,>>9") + "  " + to_string(debt1, "->,>>>,>>>,>>>,>>9") + "  " + to_string(debt2, "->,>>>,>>>,>>>,>>9") + "  " + to_string(debt3, "->,>>>,>>>,>>>,>>9") + "  "
            else:
                outlist = "  " + to_string(counter, ">>>9") + "  " + to_string(supplier, "x(34)") + "  " + to_string(tot_debt, "->>,>>>,>>>,>>9.99") + "  " + to_string(debt0, "->>,>>>,>>>,>>9.99") + "  " + to_string(debt1, "->>,>>>,>>>,>>9.99") + "  " + to_string(debt2, "->>,>>>,>>>,>>9.99") + "  " + to_string(debt3, "->>,>>>,>>>,>>9.99") + "  "
            fill_in_list()
        outlist = "-------------------------------------------------------------------------------------------------------------------------------------------------"
        fill_in_list()

        if price_decimal == 0:
            outlist = to_string(translateExtended ("           T O T A L  A/P:", lvcarea, "") , "x(26)") + "                  " + to_string(t_saldo, "->,>>>,>>>,>>>,>>9") + "  " + to_string(t_debt0, "->,>>>,>>>,>>>,>>9") + "  " + to_string(t_debt1, "->,>>>,>>>,>>>,>>9") + "  " + to_string(t_debt2, "->,>>>,>>>,>>>,>>9") + "  " + to_string(t_debt3, "->,>>>,>>>,>>>,>>9")
        else:
            outlist = to_string(translateExtended ("           T O T A L  A/P:", lvcarea, "") , "x(26)") + "                  " + to_string(t_saldo, "->>,>>>,>>>,>>9.99") + "  " + to_string(t_debt0, "->>,>>>,>>>,>>9.99") + "  " + to_string(t_debt1, "->>,>>>,>>>,>>9.99") + "  " + to_string(t_debt2, "->>,>>>,>>>,>>9.99") + "  " + to_string(t_debt3, "->>,>>>,>>>,>>9.99")
        fill_in_list()
        outlist = ""
        fill_in_list()
        outlist = to_string(translateExtended ("        Statistic Percentage (%) :", lvcarea, "") , "x(33)") + "                      " + "100.00" + "             " + to_string((t_debt0 / t_saldo * 100) , "->>9.99") + "             " + to_string((t_debt1 / t_saldo * 100) , "->>9.99") + "             " + to_string((t_debt2 / t_saldo * 100) , "->>9.99") + "             " + to_string((t_debt3 / t_saldo * 100) , "->>9.99")
        fill_in_list()
        outlist = ""
        fill_in_list()

    def fill_in_list():

        nonlocal output_list_list, outlist, price_decimal, lvcarea, l_kredit, l_lieferant, queasy
        nonlocal debt


        nonlocal age_list, output_list, debt
        nonlocal age_list_list, output_list_list


        output_list = Output_list()
        output_list_list.append(output_list)

        output_list.str = outlist

    price_decimal = get_output(htpint(491))

    if curr_disp == 1:
        age_list()

    elif curr_disp == 2:
        age_list1()

    elif curr_disp == 3:
        age_list2()

    elif curr_disp == 4:
        age_list3()

    return generate_output()