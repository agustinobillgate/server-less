#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from functions.htpint import htpint
from models import L_kredit, L_lieferant, Queasy

def ap_age_btn_gobl(pvilanguage:int, to_date:date, from_name:string, to_name:string, day1:int, day2:int, day3:int, curr_disp:int):

    prepare_cache ([L_kredit, L_lieferant, Queasy])

    output_list_list = []
    outlist:string = ""
    price_decimal:int = 0
    lvcarea:string = "ap-age"
    l_kredit = l_lieferant = queasy = None

    age_list = output_list = None

    age_list_list, Age_list = create_model("Age_list", {"name":string, "counter":int, "lief_nr":int, "rgdatum":date, "supplier":string, "saldo":Decimal, "debt0":Decimal, "debt1":Decimal, "debt2":Decimal, "debt3":Decimal, "tot_debt":Decimal, "adresse1":string, "telefon":string})
    output_list_list, Output_list = create_model("Output_list", {"str":string})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal output_list_list, outlist, price_decimal, lvcarea, l_kredit, l_lieferant, queasy
        nonlocal pvilanguage, to_date, from_name, to_name, day1, day2, day3, curr_disp


        nonlocal age_list, output_list
        nonlocal age_list_list, output_list_list

        return {"output-list": output_list_list}

    def age_list():

        nonlocal output_list_list, outlist, price_decimal, lvcarea, l_kredit, l_lieferant, queasy
        nonlocal pvilanguage, to_date, from_name, to_name, day1, day2, day3, curr_disp


        nonlocal age_list, output_list
        nonlocal age_list_list, output_list_list

        billdate:date = None
        counter:int = 0
        t_debet:Decimal = to_decimal("0.0")
        t_credit:Decimal = to_decimal("0.0")
        t_comm:Decimal = to_decimal("0.0")
        t_adjust:Decimal = to_decimal("0.0")
        t_saldo:Decimal = to_decimal("0.0")
        t_debt0:Decimal = to_decimal("0.0")
        t_debt1:Decimal = to_decimal("0.0")
        t_debt2:Decimal = to_decimal("0.0")
        t_debt3:Decimal = to_decimal("0.0")
        tmp_saldo:Decimal = to_decimal("0.0")
        curr_name:string = ""
        curr_liefnr:int = 0
        supplier:string = ""
        debt0:Decimal = to_decimal("0.0")
        debt1:Decimal = to_decimal("0.0")
        debt2:Decimal = to_decimal("0.0")
        debt3:Decimal = to_decimal("0.0")
        tot_debt:Decimal = to_decimal("0.0")
        ap_saldo:Decimal = to_decimal("0.0")
        do_it:bool = False
        debt = None
        Debt =  create_buffer("Debt",L_kredit)
        age_list_list.clear()
        output_list_list.clear()

        l_kredit_obj_list = {}
        l_kredit = L_kredit()
        l_lieferant = L_lieferant()
        for l_kredit.netto, l_kredit.counter, l_kredit.name, l_kredit.rgdatum, l_kredit.lief_nr, l_kredit._recid, l_lieferant.segment1, l_lieferant.firma, l_lieferant.anredefirma, l_lieferant.adresse1, l_lieferant._recid in db_session.query(L_kredit.netto, L_kredit.counter, L_kredit.name, L_kredit.rgdatum, L_kredit.lief_nr, L_kredit._recid, L_lieferant.segment1, L_lieferant.firma, L_lieferant.anredefirma, L_lieferant.adresse1, L_lieferant._recid).join(L_lieferant,(L_lieferant.lief_nr == L_kredit.lief_nr) & (L_lieferant.firma >= (from_name).lower()) & (L_lieferant.firma <= (to_name).lower())).filter(
                 (L_kredit.rgdatum <= to_date) & (L_kredit.opart == 0)).order_by(L_lieferant.firma).all():
            if l_kredit_obj_list.get(l_kredit._recid):
                continue
            else:
                l_kredit_obj_list[l_kredit._recid] = True


            do_it = True

            if l_lieferant.segment1 != 0 and l_lieferant.segment1 != l_lieferant.segment1:
                do_it = False

            if do_it:
                ap_saldo =  to_decimal(l_kredit.netto)

                if l_kredit.counter != 0:

                    for debt in db_session.query(Debt).filter(
                             (Debt.opart == 1) & (Debt.counter == l_kredit.counter) & (Debt.zahlkonto != 0) & (Debt.rgdatum <= to_date)).order_by(Debt._recid).all():
                        ap_saldo =  to_decimal(ap_saldo) + to_decimal(debt.saldo)
                age_list = Age_list()
                age_list_list.append(age_list)

                age_list.name = l_kredit.name
                age_list.rgdatum = l_kredit.rgdatum
                age_list.counter = l_kredit.counter
                age_list.lief_nr = l_kredit.lief_nr
                age_list.tot_debt =  to_decimal(ap_saldo)
                age_list.supplier = trim(l_lieferant.firma + ", " + l_lieferant.anredefirma)
                age_list.adresse1 = l_lieferant.adresse1
                age_list.telefon = l_lieferant.adresse1

        l_kredit_obj_list = {}
        l_kredit = L_kredit()
        l_lieferant = L_lieferant()
        for l_kredit.netto, l_kredit.counter, l_kredit.name, l_kredit.rgdatum, l_kredit.lief_nr, l_kredit._recid, l_lieferant.segment1, l_lieferant.firma, l_lieferant.anredefirma, l_lieferant.adresse1, l_lieferant._recid in db_session.query(L_kredit.netto, L_kredit.counter, L_kredit.name, L_kredit.rgdatum, L_kredit.lief_nr, L_kredit._recid, L_lieferant.segment1, L_lieferant.firma, L_lieferant.anredefirma, L_lieferant.adresse1, L_lieferant._recid).join(L_lieferant,(L_lieferant.lief_nr == L_kredit.lief_nr) & (L_lieferant.firma >= (from_name).lower()) & (L_lieferant.firma <= (to_name).lower())).filter(
                 (L_kredit.rgdatum <= to_date) & (L_kredit.opart == 2) & (L_kredit.zahlkonto == 0)).order_by(L_kredit.counter).all():
            if l_kredit_obj_list.get(l_kredit._recid):
                continue
            else:
                l_kredit_obj_list[l_kredit._recid] = True


            do_it = True

            if l_lieferant.segment1 != 0 and l_lieferant.segment1 != l_lieferant.segment1:
                do_it = False

            if do_it:
                ap_saldo =  to_decimal(l_kredit.netto)

                for debt in db_session.query(Debt).filter(
                         (Debt.counter == l_kredit.counter) & (Debt.opart == 2) & (Debt.zahlkonto != 0) & (Debt.rgdatum <= to_date)).order_by(Debt._recid).all():
                    ap_saldo =  to_decimal(ap_saldo) + to_decimal(debt.saldo)
                age_list = Age_list()
                age_list_list.append(age_list)

                age_list.name = l_kredit.name
                age_list.rgdatum = l_kredit.rgdatum
                age_list.counter = l_kredit.counter
                age_list.lief_nr = l_kredit.lief_nr
                age_list.tot_debt =  to_decimal(ap_saldo)
                age_list.supplier = l_lieferant.firma + ", " + l_lieferant.anredefirma
                age_list.adresse1 = l_lieferant.adresse1
                age_list.telefon = l_lieferant.adresse1
        curr_liefnr = 0
        counter = 0

        for age_list in query(age_list_list, filters=(lambda age_list: age_list.tot_debt != 0), sort_by=[("supplier",False)]):

            if to_date - age_list.rgdatum > day3:
                age_list.debt3 =  to_decimal(age_list.tot_debt)

            elif to_date - age_list.rgdatum > day2:
                age_list.debt2 =  to_decimal(age_list.tot_debt)

            elif to_date - age_list.rgdatum > day1:
                age_list.debt1 =  to_decimal(age_list.tot_debt)
            else:
                age_list.debt0 =  to_decimal(age_list.tot_debt)
            t_saldo = to_decimal(t_saldo + round(age_list.tot_debt , 0))
            t_debt0 = to_decimal(t_debt0 + round(age_list.debt0 , 0))
            t_debt1 = to_decimal(t_debt1 + round(age_list.debt1 , 0))
            t_debt2 = to_decimal(t_debt2 + round(age_list.debt2 , 0))
            t_debt3 = to_decimal(t_debt3 + round(age_list.debt3 , 0))

            if curr_liefnr == 0:
                supplier = age_list.supplier
                tot_debt = to_decimal(round(age_list.tot_debt , 0))
                debt0 = to_decimal(round(age_list.debt0 , 0))
                debt1 = to_decimal(round(age_list.debt1 , 0))
                debt2 = to_decimal(round(age_list.debt2 , 0))
                debt3 = to_decimal(round(age_list.debt3 , 0))
                counter = counter + 1

            elif curr_name != age_list.supplier:

                if tot_debt != 0:

                    if price_decimal == 0:
                        outlist = " " + to_string(counter, ">>>9") + " " + to_string(supplier, "x(34)") + " " + to_string(tot_debt, "->,>>>,>>>,>>>,>>9") + " " + to_string(debt0, "->,>>>,>>>,>>>,>>9") + " " + to_string(debt1, "->,>>>,>>>,>>>,>>9") + " " + to_string(debt2, "->,>>>,>>>,>>>,>>9") + " " + to_string(debt3, "->,>>>,>>>,>>>,>>9") + " "
                    else:
                        outlist = " " + to_string(counter, ">>>9") + " " + to_string(supplier, "x(34)") + " " + to_string(tot_debt, "->>,>>>,>>>,>>9.99") + " " + to_string(debt0, "->>,>>>,>>>,>>9.99") + " " + to_string(debt1, "->>,>>>,>>>,>>9.99") + " " + to_string(debt2, "->>,>>>,>>>,>>9.99") + " " + to_string(debt3, "->>,>>>,>>>,>>9.99") + " "
                    fill_in_list()
                else:
                    counter = counter - 1
                supplier = age_list.supplier
                tot_debt = to_decimal(round(age_list.tot_debt , 0))
                debt0 = to_decimal(round(age_list.debt0 , 0))
                debt1 = to_decimal(round(age_list.debt1 , 0))
                debt2 = to_decimal(round(age_list.debt2 , 0))
                debt3 = to_decimal(round(age_list.debt3 , 0))
                counter = counter + 1
            else:
                tot_debt = to_decimal(tot_debt + round(age_list.tot_debt , 0))
                debt0 = to_decimal(debt0 + round(age_list.debt0 , 0))
                debt1 = to_decimal(debt1 + round(age_list.debt1 , 0))
                debt2 = to_decimal(debt2 + round(age_list.debt2 , 0))
                debt3 = to_decimal(debt3 + round(age_list.debt3 , 0))
            curr_liefnr = age_list.lief_nr
            curr_name = age_list.supplier
            age_list_list.remove(age_list)

        if counter > 0 and tot_debt != 0:

            if price_decimal == 0:
                outlist = " " + to_string(counter, ">>>9") + " " + to_string(supplier, "x(34)") + " " + to_string(tot_debt, "->,>>>,>>>,>>>,>>9") + " " + to_string(debt0, "->,>>>,>>>,>>>,>>9") + " " + to_string(debt1, "->,>>>,>>>,>>>,>>9") + " " + to_string(debt2, "->,>>>,>>>,>>>,>>9") + " " + to_string(debt3, "->,>>>,>>>,>>>,>>9") + " "
            else:
                outlist = " " + to_string(counter, ">>>9") + " " + to_string(supplier, "x(34)") + " " + to_string(tot_debt, "->>,>>>,>>>,>>9.99") + " " + to_string(debt0, "->>,>>>,>>>,>>9.99") + " " + to_string(debt1, "->>,>>>,>>>,>>9.99") + " " + to_string(debt2, "->>,>>>,>>>,>>9.99") + " " + to_string(debt3, "->>,>>>,>>>,>>9.99") + " "
            fill_in_list()
        outlist = "-------------------------------------------------------------------------------------------------------------------------------------------------"
        fill_in_list()

        if price_decimal == 0:
            outlist = to_string(translateExtended (" T O T A L A/P:", lvcarea, "") , "x(26)") + " " + to_string(t_saldo, "->,>>>,>>>,>>>,>>9") + " " + to_string(t_debt0, "->,>>>,>>>,>>>,>>9") + " " + to_string(t_debt1, "->,>>>,>>>,>>>,>>9") + " " + to_string(t_debt2, "->,>>>,>>>,>>>,>>9") + " " + to_string(t_debt3, "->,>>>,>>>,>>>,>>9")
        else:
            outlist = to_string(translateExtended (" T O T A L A/P:", lvcarea, "") , "x(26)") + " " + to_string(t_saldo, "->>,>>>,>>>,>>9.99") + " " + to_string(t_debt0, "->>,>>>,>>>,>>9.99") + " " + to_string(t_debt1, "->>,>>>,>>>,>>9.99") + " " + to_string(t_debt2, "->>,>>>,>>>,>>9.99") + " " + to_string(t_debt3, "->>,>>>,>>>,>>9.99")
        fill_in_list()
        outlist = ""
        fill_in_list()
        outlist = to_string(translateExtended (" Statistic Percentage (%) :", lvcarea, "") , "x(33)") + " " + "100.00" + " " + to_string((t_debt0 / t_saldo * 100) , "->>9.99") + " " + to_string((t_debt1 / t_saldo * 100) , "->>9.99") + " " + to_string((t_debt2 / t_saldo * 100) , "->>9.99") + " " + to_string((t_debt3 / t_saldo * 100) , "->>9.99")
        fill_in_list()
        outlist = ""
        fill_in_list()


    def age_list1():

        nonlocal output_list_list, outlist, price_decimal, lvcarea, l_kredit, l_lieferant, queasy
        nonlocal pvilanguage, to_date, from_name, to_name, day1, day2, day3, curr_disp


        nonlocal age_list, output_list
        nonlocal age_list_list, output_list_list

        billdate:date = None
        counter:int = 0
        t_debet:Decimal = to_decimal("0.0")
        t_credit:Decimal = to_decimal("0.0")
        t_comm:Decimal = to_decimal("0.0")
        t_adjust:Decimal = to_decimal("0.0")
        t_saldo:Decimal = to_decimal("0.0")
        t_debt0:Decimal = to_decimal("0.0")
        t_debt1:Decimal = to_decimal("0.0")
        t_debt2:Decimal = to_decimal("0.0")
        t_debt3:Decimal = to_decimal("0.0")
        tmp_saldo:Decimal = to_decimal("0.0")
        curr_name:string = ""
        curr_liefnr:int = 0
        supplier:string = ""
        debt0:Decimal = to_decimal("0.0")
        debt1:Decimal = to_decimal("0.0")
        debt2:Decimal = to_decimal("0.0")
        debt3:Decimal = to_decimal("0.0")
        tot_debt:Decimal = to_decimal("0.0")
        ap_saldo:Decimal = to_decimal("0.0")
        do_it:bool = False
        debt = None
        Debt =  create_buffer("Debt",L_kredit)
        age_list_list.clear()
        output_list_list.clear()

        l_kredit_obj_list = {}
        l_kredit = L_kredit()
        l_lieferant = L_lieferant()
        for l_kredit.netto, l_kredit.counter, l_kredit.name, l_kredit.rgdatum, l_kredit.lief_nr, l_kredit._recid, l_lieferant.segment1, l_lieferant.firma, l_lieferant.anredefirma, l_lieferant.adresse1, l_lieferant._recid in db_session.query(L_kredit.netto, L_kredit.counter, L_kredit.name, L_kredit.rgdatum, L_kredit.lief_nr, L_kredit._recid, L_lieferant.segment1, L_lieferant.firma, L_lieferant.anredefirma, L_lieferant.adresse1, L_lieferant._recid).join(L_lieferant,(L_lieferant.lief_nr == L_kredit.lief_nr) & (L_lieferant.firma >= (from_name).lower()) & (L_lieferant.firma <= (to_name).lower()) & (L_kredit.steuercode == 1)).filter(
                 (L_kredit.rgdatum <= to_date) & (L_kredit.opart == 0)).order_by(L_lieferant.firma).all():
            if l_kredit_obj_list.get(l_kredit._recid):
                continue
            else:
                l_kredit_obj_list[l_kredit._recid] = True


            do_it = True

            if l_lieferant.segment1 != 0 and l_lieferant.segment1 != l_lieferant.segment1:
                do_it = False

            if do_it:
                ap_saldo =  to_decimal(l_kredit.netto)

                if l_kredit.counter != 0:

                    for debt in db_session.query(Debt).filter(
                             (Debt.opart == 1) & (Debt.counter == l_kredit.counter) & (Debt.zahlkonto != 0) & (Debt.rgdatum <= to_date)).order_by(Debt._recid).all():
                        ap_saldo =  to_decimal(ap_saldo) + to_decimal(debt.saldo)
                age_list = Age_list()
                age_list_list.append(age_list)

                age_list.name = l_kredit.name
                age_list.rgdatum = l_kredit.rgdatum
                age_list.counter = l_kredit.counter
                age_list.lief_nr = l_kredit.lief_nr
                age_list.tot_debt =  to_decimal(ap_saldo)
                age_list.supplier = trim(l_lieferant.firma + ", " + l_lieferant.anredefirma)
                age_list.adresse1 = l_lieferant.adresse1
                age_list.telefon = l_lieferant.adresse1

        l_kredit_obj_list = {}
        l_kredit = L_kredit()
        l_lieferant = L_lieferant()
        for l_kredit.netto, l_kredit.counter, l_kredit.name, l_kredit.rgdatum, l_kredit.lief_nr, l_kredit._recid, l_lieferant.segment1, l_lieferant.firma, l_lieferant.anredefirma, l_lieferant.adresse1, l_lieferant._recid in db_session.query(L_kredit.netto, L_kredit.counter, L_kredit.name, L_kredit.rgdatum, L_kredit.lief_nr, L_kredit._recid, L_lieferant.segment1, L_lieferant.firma, L_lieferant.anredefirma, L_lieferant.adresse1, L_lieferant._recid).join(L_lieferant,(L_lieferant.lief_nr == L_kredit.lief_nr) & (L_lieferant.firma >= (from_name).lower()) & (L_lieferant.firma <= (to_name).lower()) & (L_kredit.steuercode == 1)).filter(
                 (L_kredit.rgdatum <= to_date) & (L_kredit.opart == 2) & (L_kredit.zahlkonto == 0)).order_by(L_kredit.counter).all():
            if l_kredit_obj_list.get(l_kredit._recid):
                continue
            else:
                l_kredit_obj_list[l_kredit._recid] = True


            do_it = True

            if l_lieferant.segment1 != 0 and l_lieferant.segment1 != l_lieferant.segment1:
                do_it = False

            if do_it:
                ap_saldo =  to_decimal(l_kredit.netto)

                for debt in db_session.query(Debt).filter(
                         (Debt.counter == l_kredit.counter) & (Debt.opart == 2) & (Debt.zahlkonto != 0) & (Debt.rgdatum <= to_date)).order_by(Debt._recid).all():
                    ap_saldo =  to_decimal(ap_saldo) + to_decimal(debt.saldo)
                age_list = Age_list()
                age_list_list.append(age_list)

                age_list.name = l_kredit.name
                age_list.rgdatum = l_kredit.rgdatum
                age_list.counter = l_kredit.counter
                age_list.lief_nr = l_kredit.lief_nr
                age_list.tot_debt =  to_decimal(ap_saldo)
                age_list.supplier = l_lieferant.firma + ", " + l_lieferant.anredefirma
                age_list.adresse1 = l_lieferant.adresse1
                age_list.telefon = l_lieferant.adresse1
        curr_liefnr = 0
        counter = 0

        for age_list in query(age_list_list, filters=(lambda age_list: age_list.tot_debt != 0), sort_by=[("supplier",False)]):

            if to_date - age_list.rgdatum > day3:
                age_list.debt3 =  to_decimal(age_list.tot_debt)

            elif to_date - age_list.rgdatum > day2:
                age_list.debt2 =  to_decimal(age_list.tot_debt)

            elif to_date - age_list.rgdatum > day1:
                age_list.debt1 =  to_decimal(age_list.tot_debt)
            else:
                age_list.debt0 =  to_decimal(age_list.tot_debt)
            t_saldo = to_decimal(t_saldo + round(age_list.tot_debt , 0))
            t_debt0 = to_decimal(t_debt0 + round(age_list.debt0 , 0))
            t_debt1 = to_decimal(t_debt1 + round(age_list.debt1 , 0))
            t_debt2 = to_decimal(t_debt2 + round(age_list.debt2 , 0))
            t_debt3 = to_decimal(t_debt3 + round(age_list.debt3 , 0))

            if curr_liefnr == 0:
                supplier = age_list.supplier
                tot_debt = to_decimal(round(age_list.tot_debt , 0))
                debt0 = to_decimal(round(age_list.debt0 , 0))
                debt1 = to_decimal(round(age_list.debt1 , 0))
                debt2 = to_decimal(round(age_list.debt2 , 0))
                debt3 = to_decimal(round(age_list.debt3 , 0))
                counter = counter + 1

            elif curr_name != age_list.supplier:

                if tot_debt != 0:

                    if price_decimal == 0:
                        outlist = " " + to_string(counter, ">>>9") + " " + to_string(supplier, "x(34)") + " " + to_string(tot_debt, "->,>>>,>>>,>>>,>>9") + " " + to_string(debt0, "->,>>>,>>>,>>>,>>9") + " " + to_string(debt1, "->,>>>,>>>,>>>,>>9") + " " + to_string(debt2, "->,>>>,>>>,>>>,>>9") + " " + to_string(debt3, "->,>>>,>>>,>>>,>>9") + " "
                    else:
                        outlist = " " + to_string(counter, ">>>9") + " " + to_string(supplier, "x(34)") + " " + to_string(tot_debt, "->>,>>>,>>>,>>9.99") + " " + to_string(debt0, "->>,>>>,>>>,>>9.99") + " " + to_string(debt1, "->>,>>>,>>>,>>9.99") + " " + to_string(debt2, "->>,>>>,>>>,>>9.99") + " " + to_string(debt3, "->>,>>>,>>>,>>9.99") + " "
                    fill_in_list()
                else:
                    counter = counter - 1
                supplier = age_list.supplier
                tot_debt = to_decimal(round(age_list.tot_debt , 0))
                debt0 = to_decimal(round(age_list.debt0 , 0))
                debt1 = to_decimal(round(age_list.debt1 , 0))
                debt2 = to_decimal(round(age_list.debt2 , 0))
                debt3 = to_decimal(round(age_list.debt3 , 0))
                counter = counter + 1
            else:
                tot_debt = to_decimal(tot_debt + round(age_list.tot_debt , 0))
                debt0 = to_decimal(debt0 + round(age_list.debt0 , 0))
                debt1 = to_decimal(debt1 + round(age_list.debt1 , 0))
                debt2 = to_decimal(debt2 + round(age_list.debt2 , 0))
                debt3 = to_decimal(debt3 + round(age_list.debt3 , 0))
            curr_liefnr = age_list.lief_nr
            curr_name = age_list.supplier
            age_list_list.remove(age_list)

        if counter > 0 and tot_debt != 0:

            if price_decimal == 0:
                outlist = " " + to_string(counter, ">>>9") + " " + to_string(supplier, "x(34)") + " " + to_string(tot_debt, "->,>>>,>>>,>>>,>>9") + " " + to_string(debt0, "->,>>>,>>>,>>>,>>9") + " " + to_string(debt1, "->,>>>,>>>,>>>,>>9") + " " + to_string(debt2, "->,>>>,>>>,>>>,>>9") + " " + to_string(debt3, "->,>>>,>>>,>>>,>>9") + " "
            else:
                outlist = " " + to_string(counter, ">>>9") + " " + to_string(supplier, "x(34)") + " " + to_string(tot_debt, "->>,>>>,>>>,>>9.99") + " " + to_string(debt0, "->>,>>>,>>>,>>9.99") + " " + to_string(debt1, "->>,>>>,>>>,>>9.99") + " " + to_string(debt2, "->>,>>>,>>>,>>9.99") + " " + to_string(debt3, "->>,>>>,>>>,>>9.99") + " "
            fill_in_list()
        outlist = "-------------------------------------------------------------------------------------------------------------------------------------------------"
        fill_in_list()

        if price_decimal == 0:
            outlist = to_string(translateExtended (" T O T A L A/P:", lvcarea, "") , "x(26)") + " " + to_string(t_saldo, "->,>>>,>>>,>>>,>>9") + " " + to_string(t_debt0, "->,>>>,>>>,>>>,>>9") + " " + to_string(t_debt1, "->,>>>,>>>,>>>,>>9") + " " + to_string(t_debt2, "->,>>>,>>>,>>>,>>9") + " " + to_string(t_debt3, "->,>>>,>>>,>>>,>>9")
        else:
            outlist = to_string(translateExtended (" T O T A L A/P:", lvcarea, "") , "x(26)") + " " + to_string(t_saldo, "->>,>>>,>>>,>>9.99") + " " + to_string(t_debt0, "->>,>>>,>>>,>>9.99") + " " + to_string(t_debt1, "->>,>>>,>>>,>>9.99") + " " + to_string(t_debt2, "->>,>>>,>>>,>>9.99") + " " + to_string(t_debt3, "->>,>>>,>>>,>>9.99")
        fill_in_list()
        outlist = ""
        fill_in_list()
        outlist = to_string(translateExtended (" Statistic Percentage (%) :", lvcarea, "") , "x(33)") + " " + "100.00" + " " + to_string((t_debt0 / t_saldo * 100) , "->>9.99") + " " + to_string((t_debt1 / t_saldo * 100) , "->>9.99") + " " + to_string((t_debt2 / t_saldo * 100) , "->>9.99") + " " + to_string((t_debt3 / t_saldo * 100) , "->>9.99")
        fill_in_list()
        outlist = ""
        fill_in_list()


    def age_list2():

        nonlocal output_list_list, outlist, price_decimal, lvcarea, l_kredit, l_lieferant, queasy
        nonlocal pvilanguage, to_date, from_name, to_name, day1, day2, day3, curr_disp


        nonlocal age_list, output_list
        nonlocal age_list_list, output_list_list

        billdate:date = None
        counter:int = 0
        t_debet:Decimal = to_decimal("0.0")
        t_credit:Decimal = to_decimal("0.0")
        t_comm:Decimal = to_decimal("0.0")
        t_adjust:Decimal = to_decimal("0.0")
        t_saldo:Decimal = to_decimal("0.0")
        t_debt0:Decimal = to_decimal("0.0")
        t_debt1:Decimal = to_decimal("0.0")
        t_debt2:Decimal = to_decimal("0.0")
        t_debt3:Decimal = to_decimal("0.0")
        tmp_saldo:Decimal = to_decimal("0.0")
        curr_name:string = ""
        curr_liefnr:int = 0
        supplier:string = ""
        debt0:Decimal = to_decimal("0.0")
        debt1:Decimal = to_decimal("0.0")
        debt2:Decimal = to_decimal("0.0")
        debt3:Decimal = to_decimal("0.0")
        tot_debt:Decimal = to_decimal("0.0")
        ap_saldo:Decimal = to_decimal("0.0")
        do_it:bool = False
        debt = None
        Debt =  create_buffer("Debt",L_kredit)
        age_list_list.clear()
        output_list_list.clear()

        l_kredit_obj_list = {}
        l_kredit = L_kredit()
        l_lieferant = L_lieferant()
        for l_kredit.netto, l_kredit.counter, l_kredit.name, l_kredit.rgdatum, l_kredit.lief_nr, l_kredit._recid, l_lieferant.segment1, l_lieferant.firma, l_lieferant.anredefirma, l_lieferant.adresse1, l_lieferant._recid in db_session.query(L_kredit.netto, L_kredit.counter, L_kredit.name, L_kredit.rgdatum, L_kredit.lief_nr, L_kredit._recid, L_lieferant.segment1, L_lieferant.firma, L_lieferant.anredefirma, L_lieferant.adresse1, L_lieferant._recid).join(L_lieferant,(L_lieferant.lief_nr == L_kredit.lief_nr) & (L_lieferant.firma >= (from_name).lower()) & (L_lieferant.firma <= (to_name).lower()) & (L_kredit.steuercode == 0)).filter(
                 (L_kredit.rgdatum <= to_date) & (L_kredit.opart == 0)).order_by(L_lieferant.firma).all():
            if l_kredit_obj_list.get(l_kredit._recid):
                continue
            else:
                l_kredit_obj_list[l_kredit._recid] = True


            do_it = True

            if l_lieferant.segment1 != 0 and l_lieferant.segment1 != l_lieferant.segment1:
                do_it = False

            if do_it:
                ap_saldo =  to_decimal(l_kredit.netto)

                if l_kredit.counter != 0:

                    for debt in db_session.query(Debt).filter(
                             (Debt.opart == 1) & (Debt.counter == l_kredit.counter) & (Debt.zahlkonto != 0) & (Debt.rgdatum <= to_date)).order_by(Debt._recid).all():
                        ap_saldo =  to_decimal(ap_saldo) + to_decimal(debt.saldo)
                age_list = Age_list()
                age_list_list.append(age_list)

                age_list.name = l_kredit.name
                age_list.rgdatum = l_kredit.rgdatum
                age_list.counter = l_kredit.counter
                age_list.lief_nr = l_kredit.lief_nr
                age_list.tot_debt =  to_decimal(ap_saldo)
                age_list.supplier = trim(l_lieferant.firma + ", " + l_lieferant.anredefirma)
                age_list.adresse1 = l_lieferant.adresse1
                age_list.telefon = l_lieferant.adresse1

        l_kredit_obj_list = {}
        l_kredit = L_kredit()
        l_lieferant = L_lieferant()
        for l_kredit.netto, l_kredit.counter, l_kredit.name, l_kredit.rgdatum, l_kredit.lief_nr, l_kredit._recid, l_lieferant.segment1, l_lieferant.firma, l_lieferant.anredefirma, l_lieferant.adresse1, l_lieferant._recid in db_session.query(L_kredit.netto, L_kredit.counter, L_kredit.name, L_kredit.rgdatum, L_kredit.lief_nr, L_kredit._recid, L_lieferant.segment1, L_lieferant.firma, L_lieferant.anredefirma, L_lieferant.adresse1, L_lieferant._recid).join(L_lieferant,(L_lieferant.lief_nr == L_kredit.lief_nr) & (L_lieferant.firma >= (from_name).lower()) & (L_lieferant.firma <= (to_name).lower()) & (L_kredit.steuercode == 0)).filter(
                 (L_kredit.rgdatum <= to_date) & (L_kredit.opart == 2) & (L_kredit.zahlkonto == 0)).order_by(L_kredit.counter).all():
            if l_kredit_obj_list.get(l_kredit._recid):
                continue
            else:
                l_kredit_obj_list[l_kredit._recid] = True


            do_it = True

            if l_lieferant.segment1 != 0 and l_lieferant.segment1 != l_lieferant.segment1:
                do_it = False

            if do_it:
                ap_saldo =  to_decimal(l_kredit.netto)

                for debt in db_session.query(Debt).filter(
                         (Debt.counter == l_kredit.counter) & (Debt.opart == 2) & (Debt.zahlkonto != 0) & (Debt.rgdatum <= to_date)).order_by(Debt._recid).all():
                    ap_saldo =  to_decimal(ap_saldo) + to_decimal(debt.saldo)
                age_list = Age_list()
                age_list_list.append(age_list)

                age_list.name = l_kredit.name
                age_list.rgdatum = l_kredit.rgdatum
                age_list.counter = l_kredit.counter
                age_list.lief_nr = l_kredit.lief_nr
                age_list.tot_debt =  to_decimal(ap_saldo)
                age_list.supplier = l_lieferant.firma + ", " + l_lieferant.anredefirma
                age_list.adresse1 = l_lieferant.adresse1
                age_list.telefon = l_lieferant.adresse1
        curr_liefnr = 0
        counter = 0

        for age_list in query(age_list_list, filters=(lambda age_list: age_list.tot_debt != 0), sort_by=[("supplier",False)]):

            if to_date - age_list.rgdatum > day3:
                age_list.debt3 =  to_decimal(age_list.tot_debt)

            elif to_date - age_list.rgdatum > day2:
                age_list.debt2 =  to_decimal(age_list.tot_debt)

            elif to_date - age_list.rgdatum > day1:
                age_list.debt1 =  to_decimal(age_list.tot_debt)
            else:
                age_list.debt0 =  to_decimal(age_list.tot_debt)
            t_saldo = to_decimal(t_saldo + round(age_list.tot_debt , 0))
            t_debt0 = to_decimal(t_debt0 + round(age_list.debt0 , 0))
            t_debt1 = to_decimal(t_debt1 + round(age_list.debt1 , 0))
            t_debt2 = to_decimal(t_debt2 + round(age_list.debt2 , 0))
            t_debt3 = to_decimal(t_debt3 + round(age_list.debt3 , 0))

            if curr_liefnr == 0:
                supplier = age_list.supplier
                tot_debt = to_decimal(round(age_list.tot_debt , 0))
                debt0 = to_decimal(round(age_list.debt0 , 0))
                debt1 = to_decimal(round(age_list.debt1 , 0))
                debt2 = to_decimal(round(age_list.debt2 , 0))
                debt3 = to_decimal(round(age_list.debt3 , 0))
                counter = counter + 1

            elif curr_name != age_list.supplier:

                if tot_debt != 0:

                    if price_decimal == 0:
                        outlist = " " + to_string(counter, ">>>9") + " " + to_string(supplier, "x(34)") + " " + to_string(tot_debt, "->,>>>,>>>,>>>,>>9") + " " + to_string(debt0, "->,>>>,>>>,>>>,>>9") + " " + to_string(debt1, "->,>>>,>>>,>>>,>>9") + " " + to_string(debt2, "->,>>>,>>>,>>>,>>9") + " " + to_string(debt3, "->,>>>,>>>,>>>,>>9") + " "
                    else:
                        outlist = " " + to_string(counter, ">>>9") + " " + to_string(supplier, "x(34)") + " " + to_string(tot_debt, "->>,>>>,>>>,>>9.99") + " " + to_string(debt0, "->>,>>>,>>>,>>9.99") + " " + to_string(debt1, "->>,>>>,>>>,>>9.99") + " " + to_string(debt2, "->>,>>>,>>>,>>9.99") + " " + to_string(debt3, "->>,>>>,>>>,>>9.99") + " "
                    fill_in_list()
                else:
                    counter = counter - 1
                supplier = age_list.supplier
                tot_debt = to_decimal(round(age_list.tot_debt , 0))
                debt0 = to_decimal(round(age_list.debt0 , 0))
                debt1 = to_decimal(round(age_list.debt1 , 0))
                debt2 = to_decimal(round(age_list.debt2 , 0))
                debt3 = to_decimal(round(age_list.debt3 , 0))
                counter = counter + 1
            else:
                tot_debt = to_decimal(tot_debt + round(age_list.tot_debt , 0))
                debt0 = to_decimal(debt0 + round(age_list.debt0 , 0))
                debt1 = to_decimal(debt1 + round(age_list.debt1 , 0))
                debt2 = to_decimal(debt2 + round(age_list.debt2 , 0))
                debt3 = to_decimal(debt3 + round(age_list.debt3 , 0))
            curr_liefnr = age_list.lief_nr
            curr_name = age_list.supplier
            age_list_list.remove(age_list)

        if counter > 0 and tot_debt != 0:

            if price_decimal == 0:
                outlist = " " + to_string(counter, ">>>9") + " " + to_string(supplier, "x(34)") + " " + to_string(tot_debt, "->,>>>,>>>,>>>,>>9") + " " + to_string(debt0, "->,>>>,>>>,>>>,>>9") + " " + to_string(debt1, "->,>>>,>>>,>>>,>>9") + " " + to_string(debt2, "->,>>>,>>>,>>>,>>9") + " " + to_string(debt3, "->,>>>,>>>,>>>,>>9") + " "
            else:
                outlist = " " + to_string(counter, ">>>9") + " " + to_string(supplier, "x(34)") + " " + to_string(tot_debt, "->>,>>>,>>>,>>9.99") + " " + to_string(debt0, "->>,>>>,>>>,>>9.99") + " " + to_string(debt1, "->>,>>>,>>>,>>9.99") + " " + to_string(debt2, "->>,>>>,>>>,>>9.99") + " " + to_string(debt3, "->>,>>>,>>>,>>9.99") + " "
            fill_in_list()
        outlist = "-------------------------------------------------------------------------------------------------------------------------------------------------"
        fill_in_list()

        if price_decimal == 0:
            outlist = to_string(translateExtended (" T O T A L A/P:", lvcarea, "") , "x(26)") + " " + to_string(t_saldo, "->,>>>,>>>,>>>,>>9") + " " + to_string(t_debt0, "->,>>>,>>>,>>>,>>9") + " " + to_string(t_debt1, "->,>>>,>>>,>>>,>>9") + " " + to_string(t_debt2, "->,>>>,>>>,>>>,>>9") + " " + to_string(t_debt3, "->,>>>,>>>,>>>,>>9")
        else:
            outlist = to_string(translateExtended (" T O T A L A/P:", lvcarea, "") , "x(26)") + " " + to_string(t_saldo, "->>,>>>,>>>,>>9.99") + " " + to_string(t_debt0, "->>,>>>,>>>,>>9.99") + " " + to_string(t_debt1, "->>,>>>,>>>,>>9.99") + " " + to_string(t_debt2, "->>,>>>,>>>,>>9.99") + " " + to_string(t_debt3, "->>,>>>,>>>,>>9.99")
        fill_in_list()
        outlist = ""
        fill_in_list()
        outlist = to_string(translateExtended (" Statistic Percentage (%) :", lvcarea, "") , "x(33)") + " " + "100.00" + " " + to_string((t_debt0 / t_saldo * 100) , "->>9.99") + " " + to_string((t_debt1 / t_saldo * 100) , "->>9.99") + " " + to_string((t_debt2 / t_saldo * 100) , "->>9.99") + " " + to_string((t_debt3 / t_saldo * 100) , "->>9.99")
        fill_in_list()
        outlist = ""
        fill_in_list()


    def age_list3():

        nonlocal output_list_list, outlist, price_decimal, lvcarea, l_kredit, l_lieferant, queasy
        nonlocal pvilanguage, to_date, from_name, to_name, day1, day2, day3, curr_disp


        nonlocal age_list, output_list
        nonlocal age_list_list, output_list_list

        billdate:date = None
        counter:int = 0
        t_debet:Decimal = to_decimal("0.0")
        t_credit:Decimal = to_decimal("0.0")
        t_comm:Decimal = to_decimal("0.0")
        t_adjust:Decimal = to_decimal("0.0")
        t_saldo:Decimal = to_decimal("0.0")
        t_debt0:Decimal = to_decimal("0.0")
        t_debt1:Decimal = to_decimal("0.0")
        t_debt2:Decimal = to_decimal("0.0")
        t_debt3:Decimal = to_decimal("0.0")
        tmp_saldo:Decimal = to_decimal("0.0")
        curr_name:string = ""
        curr_liefnr:int = 0
        supplier:string = ""
        debt0:Decimal = to_decimal("0.0")
        debt1:Decimal = to_decimal("0.0")
        debt2:Decimal = to_decimal("0.0")
        debt3:Decimal = to_decimal("0.0")
        tot_debt:Decimal = to_decimal("0.0")
        t_date:date = None
        ap_saldo:Decimal = to_decimal("0.0")
        do_it:bool = False
        debt = None
        Debt =  create_buffer("Debt",L_kredit)
        age_list_list.clear()
        output_list_list.clear()

        l_kredit_obj_list = {}
        l_kredit = L_kredit()
        l_lieferant = L_lieferant()
        for l_kredit.netto, l_kredit.counter, l_kredit.name, l_kredit.rgdatum, l_kredit.lief_nr, l_kredit._recid, l_lieferant.segment1, l_lieferant.firma, l_lieferant.anredefirma, l_lieferant.adresse1, l_lieferant._recid in db_session.query(L_kredit.netto, L_kredit.counter, L_kredit.name, L_kredit.rgdatum, L_kredit.lief_nr, L_kredit._recid, L_lieferant.segment1, L_lieferant.firma, L_lieferant.anredefirma, L_lieferant.adresse1, L_lieferant._recid).join(L_lieferant,(L_lieferant.lief_nr == L_kredit.lief_nr) & (L_lieferant.firma >= (from_name).lower()) & (L_lieferant.firma <= (to_name).lower())).filter(
                 (L_kredit.rgdatum <= to_date) & (L_kredit.opart == 0)).order_by(L_lieferant.firma).all():
            if l_kredit_obj_list.get(l_kredit._recid):
                continue
            else:
                l_kredit_obj_list[l_kredit._recid] = True


            do_it = True

            if l_lieferant.segment1 != 0 and l_lieferant.segment1 != l_lieferant.segment1:
                do_it = False

            if do_it:

                queasy = get_cache (Queasy, {"key": [(eq, 221)],"number1": [(eq, l_kredit.lief_nr)],"char1": [(eq, l_kredit.name)]})

                if queasy:
                    ap_saldo =  to_decimal(l_kredit.netto)

                    if l_kredit.counter != 0:

                        for debt in db_session.query(Debt).filter(
                                 (Debt.opart == 1) & (Debt.counter == l_kredit.counter) & (Debt.zahlkonto != 0) & (Debt.rgdatum <= to_date)).order_by(Debt._recid).all():
                            ap_saldo =  to_decimal(ap_saldo) + to_decimal(debt.saldo)
                    age_list = Age_list()
                    age_list_list.append(age_list)

                    age_list.name = l_kredit.name
                    age_list.rgdatum = queasy.date1
                    age_list.counter = l_kredit.counter
                    age_list.lief_nr = l_kredit.lief_nr
                    age_list.tot_debt =  to_decimal(ap_saldo)
                    age_list.supplier = trim(l_lieferant.firma + ", " + l_lieferant.anredefirma)
                    age_list.adresse1 = l_lieferant.adresse1
                    age_list.telefon = l_lieferant.adresse1

        l_kredit_obj_list = {}
        l_kredit = L_kredit()
        l_lieferant = L_lieferant()
        for l_kredit.netto, l_kredit.counter, l_kredit.name, l_kredit.rgdatum, l_kredit.lief_nr, l_kredit._recid, l_lieferant.segment1, l_lieferant.firma, l_lieferant.anredefirma, l_lieferant.adresse1, l_lieferant._recid in db_session.query(L_kredit.netto, L_kredit.counter, L_kredit.name, L_kredit.rgdatum, L_kredit.lief_nr, L_kredit._recid, L_lieferant.segment1, L_lieferant.firma, L_lieferant.anredefirma, L_lieferant.adresse1, L_lieferant._recid).join(L_lieferant,(L_lieferant.lief_nr == L_kredit.lief_nr) & (L_lieferant.firma >= (from_name).lower()) & (L_lieferant.firma <= (to_name).lower())).filter(
                 (L_kredit.rgdatum <= to_date) & (L_kredit.opart == 2) & (L_kredit.zahlkonto == 0)).order_by(L_kredit.counter).all():
            if l_kredit_obj_list.get(l_kredit._recid):
                continue
            else:
                l_kredit_obj_list[l_kredit._recid] = True


            do_it = True

            if l_lieferant.segment1 != 0 and l_lieferant.segment1 != l_lieferant.segment1:
                do_it = False

            if do_it:

                queasy = get_cache (Queasy, {"key": [(eq, 221)],"number1": [(eq, l_kredit.lief_nr)],"char1": [(eq, l_kredit.name)]})

                if queasy:
                    ap_saldo =  to_decimal(l_kredit.netto)

                    for debt in db_session.query(Debt).filter(
                             (Debt.counter == l_kredit.counter) & (Debt.opart == 2) & (Debt.zahlkonto != 0) & (Debt.rgdatum <= to_date)).order_by(Debt._recid).all():
                        ap_saldo =  to_decimal(ap_saldo) + to_decimal(debt.saldo)
                    age_list = Age_list()
                    age_list_list.append(age_list)

                    age_list.name = l_kredit.name
                    age_list.rgdatum = queasy.date1
                    age_list.counter = l_kredit.counter
                    age_list.lief_nr = l_kredit.lief_nr
                    age_list.tot_debt =  to_decimal(ap_saldo)
                    age_list.supplier = l_lieferant.firma + ", " + l_lieferant.anredefirma
                    age_list.adresse1 = l_lieferant.adresse1
                    age_list.telefon = l_lieferant.adresse1
        curr_liefnr = 0
        counter = 0

        for age_list in query(age_list_list, filters=(lambda age_list: age_list.tot_debt != 0), sort_by=[("supplier",False)]):

            if to_date - age_list.rgdatum > day3:
                age_list.debt3 =  to_decimal(age_list.tot_debt)

            elif to_date - age_list.rgdatum > day2:
                age_list.debt2 =  to_decimal(age_list.tot_debt)

            elif to_date - age_list.rgdatum > day1:
                age_list.debt1 =  to_decimal(age_list.tot_debt)
            else:
                age_list.debt0 =  to_decimal(age_list.tot_debt)
            t_saldo = to_decimal(t_saldo + round(age_list.tot_debt , 0))
            t_debt0 = to_decimal(t_debt0 + round(age_list.debt0 , 0))
            t_debt1 = to_decimal(t_debt1 + round(age_list.debt1 , 0))
            t_debt2 = to_decimal(t_debt2 + round(age_list.debt2 , 0))
            t_debt3 = to_decimal(t_debt3 + round(age_list.debt3 , 0))

            if curr_liefnr == 0:
                supplier = age_list.supplier
                tot_debt = to_decimal(round(age_list.tot_debt , 0))
                debt0 = to_decimal(round(age_list.debt0 , 0))
                debt1 = to_decimal(round(age_list.debt1 , 0))
                debt2 = to_decimal(round(age_list.debt2 , 0))
                debt3 = to_decimal(round(age_list.debt3 , 0))
                counter = counter + 1

            elif curr_name != age_list.supplier:

                if tot_debt != 0:

                    if price_decimal == 0:
                        outlist = " " + to_string(counter, ">>>9") + " " + to_string(supplier, "x(34)") + " " + to_string(tot_debt, "->,>>>,>>>,>>>,>>9") + " " + to_string(debt0, "->,>>>,>>>,>>>,>>9") + " " + to_string(debt1, "->,>>>,>>>,>>>,>>9") + " " + to_string(debt2, "->,>>>,>>>,>>>,>>9") + " " + to_string(debt3, "->,>>>,>>>,>>>,>>9") + " "
                    else:
                        outlist = " " + to_string(counter, ">>>9") + " " + to_string(supplier, "x(34)") + " " + to_string(tot_debt, "->>,>>>,>>>,>>9.99") + " " + to_string(debt0, "->>,>>>,>>>,>>9.99") + " " + to_string(debt1, "->>,>>>,>>>,>>9.99") + " " + to_string(debt2, "->>,>>>,>>>,>>9.99") + " " + to_string(debt3, "->>,>>>,>>>,>>9.99") + " "
                    fill_in_list()
                else:
                    counter = counter - 1
                supplier = age_list.supplier
                tot_debt = to_decimal(round(age_list.tot_debt , 0))
                debt0 = to_decimal(round(age_list.debt0 , 0))
                debt1 = to_decimal(round(age_list.debt1 , 0))
                debt2 = to_decimal(round(age_list.debt2 , 0))
                debt3 = to_decimal(round(age_list.debt3 , 0))
                counter = counter + 1
            else:
                tot_debt = to_decimal(tot_debt + round(age_list.tot_debt , 0))
                debt0 = to_decimal(debt0 + round(age_list.debt0 , 0))
                debt1 = to_decimal(debt1 + round(age_list.debt1 , 0))
                debt2 = to_decimal(debt2 + round(age_list.debt2 , 0))
                debt3 = to_decimal(debt3 + round(age_list.debt3 , 0))
            curr_liefnr = age_list.lief_nr
            curr_name = age_list.supplier
            age_list_list.remove(age_list)

        if counter > 0 and tot_debt != 0:

            if price_decimal == 0:
                outlist = " " + to_string(counter, ">>>9") + " " + to_string(supplier, "x(34)") + " " + to_string(tot_debt, "->,>>>,>>>,>>>,>>9") + " " + to_string(debt0, "->,>>>,>>>,>>>,>>9") + " " + to_string(debt1, "->,>>>,>>>,>>>,>>9") + " " + to_string(debt2, "->,>>>,>>>,>>>,>>9") + " " + to_string(debt3, "->,>>>,>>>,>>>,>>9") + " "
            else:
                outlist = " " + to_string(counter, ">>>9") + " " + to_string(supplier, "x(34)") + " " + to_string(tot_debt, "->>,>>>,>>>,>>9.99") + " " + to_string(debt0, "->>,>>>,>>>,>>9.99") + " " + to_string(debt1, "->>,>>>,>>>,>>9.99") + " " + to_string(debt2, "->>,>>>,>>>,>>9.99") + " " + to_string(debt3, "->>,>>>,>>>,>>9.99") + " "
            fill_in_list()
        outlist = "-------------------------------------------------------------------------------------------------------------------------------------------------"
        fill_in_list()

        if price_decimal == 0:
            outlist = to_string(translateExtended (" T O T A L A/P:", lvcarea, "") , "x(26)") + " " + to_string(t_saldo, "->,>>>,>>>,>>>,>>9") + " " + to_string(t_debt0, "->,>>>,>>>,>>>,>>9") + " " + to_string(t_debt1, "->,>>>,>>>,>>>,>>9") + " " + to_string(t_debt2, "->,>>>,>>>,>>>,>>9") + " " + to_string(t_debt3, "->,>>>,>>>,>>>,>>9")
        else:
            outlist = to_string(translateExtended (" T O T A L A/P:", lvcarea, "") , "x(26)") + " " + to_string(t_saldo, "->>,>>>,>>>,>>9.99") + " " + to_string(t_debt0, "->>,>>>,>>>,>>9.99") + " " + to_string(t_debt1, "->>,>>>,>>>,>>9.99") + " " + to_string(t_debt2, "->>,>>>,>>>,>>9.99") + " " + to_string(t_debt3, "->>,>>>,>>>,>>9.99")
        fill_in_list()
        outlist = ""
        fill_in_list()
        outlist = to_string(translateExtended (" Statistic Percentage (%) :", lvcarea, "") , "x(33)") + " " + "100.00" + " " + to_string((t_debt0 / t_saldo * 100) , "->>9.99") + " " + to_string((t_debt1 / t_saldo * 100) , "->>9.99") + " " + to_string((t_debt2 / t_saldo * 100) , "->>9.99") + " " + to_string((t_debt3 / t_saldo * 100) , "->>9.99")
        fill_in_list()
        outlist = ""
        fill_in_list()


    def fill_in_list():

        nonlocal output_list_list, outlist, price_decimal, lvcarea, l_kredit, l_lieferant, queasy
        nonlocal pvilanguage, to_date, from_name, to_name, day1, day2, day3, curr_disp


        nonlocal age_list, output_list
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