#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Debitor, Artikel, Guest, Htparam

def remote_dispar_btn_gobl(guestno:int, from_art:int, to_art:int, from_name:string, to_name:string, to_date:date, day1:int, day2:int, day3:int, detailed:bool):

    prepare_cache ([Debitor, Artikel, Guest, Htparam])

    output_list1_data = []
    from_date:date = None
    curr_bezeich:string = ""
    guest_name:string = ""
    outlist:string = ""
    billname:string = ""
    bill_number:int = 0
    long_digit:bool = False
    debitor = artikel = guest = htparam = None

    age_list = ledger = output_list = output_list1 = None

    age_list_data, Age_list = create_model("Age_list", {"artnr":int, "rechnr":int, "counter":int, "gastnr":int, "rgdatum":date, "gastname":string, "p_bal":Decimal, "debit":Decimal, "credit":Decimal, "saldo":Decimal, "debt0":Decimal, "debt1":Decimal, "debt2":Decimal, "debt3":Decimal, "tot_debt":Decimal})
    ledger_data, Ledger = create_model("Ledger", {"artnr":int, "bezeich":string, "p_bal":Decimal, "debit":Decimal, "credit":Decimal, "debt0":Decimal, "debt1":Decimal, "debt2":Decimal, "debt3":Decimal, "tot_debt":Decimal})
    output_list_data, Output_list = create_model("Output_list", {"age1":string, "age2":string, "age3":string, "age4":string, "rechnr":string, "str":string})
    output_list1_data, Output_list1 = create_model("Output_list1", {"str_counter":string, "cust_name":string, "prev_balance":Decimal, "debit":Decimal, "credit":Decimal, "end_balance":Decimal, "age1":Decimal, "age2":Decimal, "age3":Decimal, "age4":Decimal, "rechnr":int, "str_pbalance":string, "str_debit":string, "str_credit":string, "str_ebalance":string, "str_age1":string, "str_age2":string, "str_age3":string, "str_age4":string, "str_rechnr":string})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal output_list1_data, from_date, curr_bezeich, guest_name, outlist, billname, bill_number, long_digit, debitor, artikel, guest, htparam
        nonlocal guestno, from_art, to_art, from_name, to_name, to_date, day1, day2, day3, detailed


        nonlocal age_list, ledger, output_list, output_list1
        nonlocal age_list_data, ledger_data, output_list_data, output_list1_data

        return {"output-list1": output_list1_data}

    def age_list():

        nonlocal output_list1_data, from_date, curr_bezeich, guest_name, outlist, billname, bill_number, long_digit, debitor, artikel, guest, htparam
        nonlocal guestno, from_art, to_art, from_name, to_name, to_date, day1, day2, day3, detailed


        nonlocal age_list, ledger, output_list, output_list1
        nonlocal age_list_data, ledger_data, output_list_data, output_list1_data

        curr_art:int = 0
        billdate:date = None
        counter:int = 0
        t_comm:Decimal = to_decimal("0.0")
        t_adjust:Decimal = to_decimal("0.0")
        t_saldo:Decimal = to_decimal("0.0")
        t_prev:Decimal = to_decimal("0.0")
        t_debit:Decimal = to_decimal("0.0")
        t_credit:Decimal = to_decimal("0.0")
        t_debt0:Decimal = to_decimal("0.0")
        t_debt1:Decimal = to_decimal("0.0")
        t_debt2:Decimal = to_decimal("0.0")
        t_debt3:Decimal = to_decimal("0.0")
        tmp_saldo:Decimal = to_decimal("0.0")
        curr_name:string = ""
        curr_gastnr:int = 0
        gastname:string = ""
        p_bal:Decimal = to_decimal("0.0")
        debit:Decimal = to_decimal("0.0")
        credit:Decimal = to_decimal("0.0")
        debt0:Decimal = to_decimal("0.0")
        debt1:Decimal = to_decimal("0.0")
        debt2:Decimal = to_decimal("0.0")
        debt3:Decimal = to_decimal("0.0")
        tot_debt:Decimal = to_decimal("0.0")
        i:int = 0
        debtrec = None
        debt = None
        curr_counter:int = 0
        Debtrec =  create_buffer("Debtrec",Debitor)
        Debt =  create_buffer("Debt",Debitor)

        for ledger in query(ledger_data):
            ledger_data.remove(ledger)

        for age_list in query(age_list_data):
            age_list_data.remove(age_list)

        for output_list in query(output_list_data):
            output_list_data.remove(output_list)
        from_date = date (get_month(to_date) , 1, get_year(to_date))

        for artikel in db_session.query(Artikel).filter(
                 ((Artikel.artart == 2) | (Artikel.artart == 7)) & (Artikel.artnr >= from_art) & (Artikel.artnr <= to_art) & (Artikel.departement == 0)).order_by(Artikel._recid).all():
            curr_bezeich = to_string(artikel.artnr, ">>>9") + " - " + artikel.bezeich
            ledger = Ledger()
            ledger_data.append(ledger)

            ledger.artnr = artikel.artnr
            ledger.bezeich = to_string(artikel.artnr) + " - " + artikel.bezeich
        curr_art = 0

        for debitor in db_session.query(Debitor).filter(
                 (Debitor.rgdatum <= to_date) & (Debitor.artnr >= from_art) & (Debitor.artnr <= to_art) & (Debitor.opart <= 1) & (Debitor.gastnr == guestno)).order_by(Debitor._recid).all():

            if debitor.name >= from_name and debitor.name <= to_name:

                if curr_art != debitor.artnr:
                    curr_art = debitor.artnr

                    artikel = get_cache (Artikel, {"artnr": [(eq, curr_art)],"departement": [(eq, 0)]})

                if debitor.counter > 0:

                    age_list = query(age_list_data, filters=(lambda age_list: age_list.counter == debitor.counter), first=True)

                if (debitor.counter == 0) or (not age_list):

                    guest = get_cache (Guest, {"gastnr": [(eq, debitor.gastnr)]})
                    age_list = Age_list()
                    age_list_data.append(age_list)

                    age_list.artnr = debitor.artnr
                    age_list.rechnr = debitor.rechnr
                    age_list.rgdatum = debitor.rgdatum
                    age_list.counter = debitor.counter
                    age_list.gastnr = debitor.gastnr
                    age_list.tot_debt =  to_decimal("0")

                    if artikel.artart == 2:
                        age_list.gastname = guest.name + ", " + guest.vorname1 + guest.anredefirma + " " + guest.anrede1
                    else:

                        htparam = get_cache (Htparam, {"paramnr": [(eq, 867)]})

                        if debitor.gastnr == htparam.finteger:
                            age_list.gastname = "F&B " + artikel.bezeich
                        else:
                            age_list.gastname = "F/O " + artikel.bezeich
                    guest_name = guest.name + ", " + guest.vorname1 + guest.anredefirma + " " + guest.anrede1
                age_list.tot_debt =  to_decimal(age_list.tot_debt) + to_decimal(debitor.saldo)

                if debitor.rgdatum < from_date and debitor.zahlkonto == 0:
                    age_list.p_bal =  to_decimal(age_list.p_bal) + to_decimal(debitor.saldo)

                if debitor.rgdatum >= from_date and debitor.zahlkonto == 0:
                    age_list.debit =  to_decimal(age_list.debit) + to_decimal(debitor.saldo)

                if debitor.rgdatum < from_date and debitor.zahlkonto != 0:
                    age_list.p_bal =  to_decimal(age_list.p_bal) + to_decimal(debitor.saldo)
                else:

                    if debitor.rgdatum >= from_date and debitor.zahlkonto != 0:
                        age_list.credit =  to_decimal(age_list.credit) - to_decimal(debitor.saldo)

        for artikel in db_session.query(Artikel).filter(
                 ((Artikel.artart == 2) | (Artikel.artart == 7)) & (Artikel.artnr >= from_art) & (Artikel.artnr <= to_art) & (Artikel.departement == 0)).order_by(Artikel._recid).all():
            curr_bezeich = to_string(artikel.artnr, ">>>9") + " - " + artikel.bezeich
            curr_counter = 0

            for debitor in db_session.query(Debitor).filter(
                     (Debitor.artnr == artikel.artnr) & (Debitor.rgdatum <= to_date) & (Debitor.opart == 2) & (Debitor.zahlkonto == 0) & (Debitor.gastnr == guestno)).order_by(Debitor._recid).all():

                if debitor.name >= from_name and debitor.name <= to_name:

                    guest = get_cache (Guest, {"gastnr": [(eq, debitor.gastnr)]})
                    age_list = Age_list()
                    age_list_data.append(age_list)

                    age_list.artnr = debitor.artnr
                    age_list.rechnr = debitor.rechnr
                    age_list.rgdatum = debitor.rgdatum
                    age_list.counter = debitor.counter
                    age_list.gastnr = debitor.gastnr
                    age_list.tot_debt =  to_decimal(debitor.saldo)

                    if artikel.artart == 2:
                        age_list.gastname = guest.name + ", " + guest.vorname1 + guest.anredefirma + " " + guest.anrede1
                    else:

                        htparam = get_cache (Htparam, {"paramnr": [(eq, 867)]})

                        if debitor.gastnr == htparam.finteger:
                            age_list.gastname = "F&B " + artikel.bezeich
                        else:
                            age_list.gastname = "F/O " + artikel.bezeich
                    guest_name = guest.name + ", " + guest.vorname1 + guest.anredefirma + " " + guest.anrede1

                    if debitor.rgdatum < from_date:
                        age_list.p_bal =  to_decimal(age_list.p_bal) + to_decimal(debitor.saldo)

                    elif debitor.rgdatum >= from_date:
                        age_list.debit =  to_decimal(age_list.debit) + to_decimal(debitor.saldo)

                    for debtrec in db_session.query(Debtrec).filter(
                             (Debtrec.counter == debitor.counter) & (Debtrec.rechnr == debitor.rechnr) & (Debtrec.zahlkonto > 0) & (Debtrec.rgdatum <= to_date)).order_by(Debtrec._recid).all():
                        age_list.tot_debt =  to_decimal(age_list.tot_debt) + to_decimal(debtrec.saldo)

                        if debtrec.rgdatum < from_date:
                            age_list.p_bal =  to_decimal(age_list.p_bal) + to_decimal(debtrec.saldo)

                        elif debtrec.rgdatum >= from_date:
                            age_list.credit =  to_decimal(age_list.credit) - to_decimal(debtrec.saldo)

        for ledger in query(ledger_data):

            age_list = query(age_list_data, filters=(lambda age_list: age_list.artnr == ledger.artnr), first=True)

            if not age_list:
                continue
            output_list1 = Output_list1()
            output_list1_data.append(output_list1)

            output_list1.str_counter = " "
            output_list1.cust_name = ledger.bezeich.upper()


            counter = 0
            curr_gastnr = 0

            for age_list in query(age_list_data, filters=(lambda age_list: age_list.artnr == ledger.artnr)):

                if to_date - age_list.rgdatum > day3:
                    age_list.debt3 =  to_decimal(age_list.tot_debt)

                elif to_date - age_list.rgdatum > day2:
                    age_list.debt2 =  to_decimal(age_list.tot_debt)

                elif to_date - age_list.rgdatum > day1:
                    age_list.debt1 =  to_decimal(age_list.tot_debt)
                else:
                    age_list.debt0 =  to_decimal(age_list.tot_debt)
                ledger.tot_debt =  to_decimal(ledger.tot_debt) + to_decimal(age_list.tot_debt)
                ledger.p_bal =  to_decimal(ledger.p_bal) + to_decimal(age_list.p_bal)
                ledger.debit =  to_decimal(ledger.debit) + to_decimal(age_list.debit)
                ledger.credit =  to_decimal(ledger.credit) + to_decimal(age_list.credit)
                ledger.debt0 =  to_decimal(ledger.debt0) + to_decimal(age_list.debt0)
                ledger.debt1 =  to_decimal(ledger.debt1) + to_decimal(age_list.debt1)
                ledger.debt2 =  to_decimal(ledger.debt2) + to_decimal(age_list.debt2)
                ledger.debt3 =  to_decimal(ledger.debt3) + to_decimal(age_list.debt3)
                t_saldo =  to_decimal(t_saldo) + to_decimal(age_list.tot_debt)
                t_prev =  to_decimal(t_prev) + to_decimal(age_list.p_bal)
                t_debit =  to_decimal(t_debit) + to_decimal(age_list.debit)
                t_credit =  to_decimal(t_credit) + to_decimal(age_list.credit)
                t_debt0 =  to_decimal(t_debt0) + to_decimal(age_list.debt0)
                t_debt1 =  to_decimal(t_debt1) + to_decimal(age_list.debt1)
                t_debt2 =  to_decimal(t_debt2) + to_decimal(age_list.debt2)
                t_debt3 =  to_decimal(t_debt3) + to_decimal(age_list.debt3)

                if curr_gastnr == 0:
                    bill_number = age_list.rechnr
                    gastname = age_list.gastname
                    tot_debt =  to_decimal(age_list.tot_debt)
                    p_bal =  to_decimal(age_list.p_bal)
                    debit =  to_decimal(age_list.debit)
                    credit =  to_decimal(age_list.credit)
                    debt0 =  to_decimal(age_list.debt0)
                    debt1 =  to_decimal(age_list.debt1)
                    debt2 =  to_decimal(age_list.debt2)
                    debt3 =  to_decimal(age_list.debt3)
                    counter = counter + 1

                elif curr_name != age_list.gastname:

                    if p_bal != 0 or debit != 0 or credit != 0:
                        output_list1 = Output_list1()
                        output_list1_data.append(output_list1)

                        output_list1.str_counter = to_string(counter, ">>>>>>9")
                        output_list1.cust_name = gastname
                        output_list1.prev_balance =  to_decimal(p_bal)
                        output_list1.debit =  to_decimal(debit)
                        output_list1.credit =  to_decimal(credit)
                        output_list1.end_balance =  to_decimal(tot_debt)
                        output_list1.age1 =  to_decimal(debt0)
                        output_list1.age2 =  to_decimal(debt1)
                        output_list1.age3 =  to_decimal(debt2)
                        output_list1.age4 =  to_decimal(debt3)
                        output_list1.rechnr = age_list.rechnr
                        output_list1.str_pbalance = to_string(p_bal, "->>,>>>,>>>,>>9.99")
                        output_list1.str_debit = to_string(debit, "->>,>>>,>>>,>>9.99")
                        output_list1.str_credit = to_string(credit, "->>,>>>,>>>,>>9.99")
                        output_list1.str_ebalance = to_string(tot_debt, "->>,>>>,>>>,>>9.99")
                        output_list1.str_age1 = to_string(debt0, "->>,>>>,>>>,>>9.99")
                        output_list1.str_age2 = to_string(debt1, "->>,>>>,>>>,>>9.99")
                        output_list1.str_age3 = to_string(debt2, "->>,>>>,>>>,>>9.99")
                        output_list1.str_age4 = to_string(debt3, "->>,>>>,>>>,>>9.99")
                        output_list1.str_rechnr = to_string(age_list.rechnr, ">>>>>>9")


                    else:
                        counter = counter - 1
                    bill_number = age_list.rechnr
                    gastname = age_list.gastname
                    tot_debt =  to_decimal(age_list.tot_debt)
                    p_bal =  to_decimal(age_list.p_bal)
                    debit =  to_decimal(age_list.debit)
                    credit =  to_decimal(age_list.credit)
                    debt0 =  to_decimal(age_list.debt0)
                    debt1 =  to_decimal(age_list.debt1)
                    debt2 =  to_decimal(age_list.debt2)
                    debt3 =  to_decimal(age_list.debt3)
                    counter = counter + 1
                else:
                    tot_debt =  to_decimal(tot_debt) + to_decimal(age_list.tot_debt)
                    p_bal =  to_decimal(p_bal) + to_decimal(age_list.p_bal)
                    debit =  to_decimal(debit) + to_decimal(age_list.debit)
                    credit =  to_decimal(credit) + to_decimal(age_list.credit)
                    debt0 =  to_decimal(debt0) + to_decimal(age_list.debt0)
                    debt1 =  to_decimal(debt1) + to_decimal(age_list.debt1)
                    debt2 =  to_decimal(debt2) + to_decimal(age_list.debt2)
                    debt3 =  to_decimal(debt3) + to_decimal(age_list.debt3)
                curr_gastnr = age_list.gastnr

                if not detailed:
                    curr_name = age_list.gastname
                age_list_data.remove(age_list)

            if counter > 0 and (p_bal != 0 or debit != 0 or credit != 0):
                output_list1 = Output_list1()
                output_list1_data.append(output_list1)

                output_list1.str_counter = to_string(counter, ">>>>>>9")
                output_list1.cust_name = gastname
                output_list1.prev_balance =  to_decimal(p_bal)
                output_list1.debit =  to_decimal(debit)
                output_list1.credit =  to_decimal(credit)
                output_list1.end_balance =  to_decimal(tot_debt)
                output_list1.age1 =  to_decimal(debt0)
                output_list1.age2 =  to_decimal(debt1)
                output_list1.age3 =  to_decimal(debt2)
                output_list1.age4 =  to_decimal(debt3)
                output_list1.rechnr = bill_number
                output_list1.str_pbalance = to_string(p_bal, "->>,>>>,>>>,>>9.99")
                output_list1.str_debit = to_string(debit, "->>,>>>,>>>,>>9.99")
                output_list1.str_credit = to_string(credit, "->>,>>>,>>>,>>9.99")
                output_list1.str_ebalance = to_string(tot_debt, "->>,>>>,>>>,>>9.99")
                output_list1.str_age1 = to_string(debt0, "->>,>>>,>>>,>>9.99")
                output_list1.str_age2 = to_string(debt1, "->>,>>>,>>>,>>9.99")
                output_list1.str_age3 = to_string(debt2, "->>,>>>,>>>,>>9.99")
                output_list1.str_age4 = to_string(debt3, "->>,>>>,>>>,>>9.99")
                output_list1.str_rechnr = to_string(bill_number, ">>>>>>9")


            else:
                counter = counter - 1
            tmp_saldo =  to_decimal(ledger.tot_debt)

            if tmp_saldo == 0:
                tmp_saldo =  to_decimal("1")
            output_list1 = Output_list1()
            output_list1_data.append(output_list1)

            output_list1.str_counter = fill("-", 7)
            output_list1.cust_name = fill("-", 30)
            output_list1.str_pbalance = fill("-", 18)
            output_list1.str_debit = fill("-", 18)
            output_list1.str_credit = fill("-", 18)
            output_list1.str_ebalance = fill("-", 18)
            output_list1.str_age1 = fill("-", 18)
            output_list1.str_age2 = fill("-", 18)
            output_list1.str_age3 = fill("-", 18)
            output_list1.str_age4 = fill("-", 18)
            output_list1.str_rechnr = fill("-", 7)


            output_list1 = Output_list1()
            output_list1_data.append(output_list1)

            output_list1.str_counter = " "
            output_list1.cust_name = "T o t a l"
            output_list1.prev_balance =  to_decimal(ledger.p_bal)
            output_list1.debit =  to_decimal(ledger.debit)
            output_list1.credit =  to_decimal(ledger.credit)
            output_list1.end_balance =  to_decimal(ledger.tot_debt)
            output_list1.age1 =  to_decimal(ledger.debt0)
            output_list1.age2 =  to_decimal(ledger.debt1)
            output_list1.age3 =  to_decimal(ledger.debt2)
            output_list1.age4 =  to_decimal(ledger.debt3)
            output_list1.rechnr = 0
            output_list1.str_pbalance = to_string(ledger.p_bal, "->>,>>>,>>>,>>9.99")
            output_list1.str_debit = to_string(ledger.debit, "->>,>>>,>>>,>>9.99")
            output_list1.str_credit = to_string(ledger.credit, "->>,>>>,>>>,>>9.99")
            output_list1.str_ebalance = to_string(ledger.tot_debt, "->>,>>>,>>>,>>9.99")
            output_list1.str_age1 = to_string(ledger.debt0, "->>,>>>,>>>,>>9.99")
            output_list1.str_age2 = to_string(ledger.debt1, "->>,>>>,>>>,>>9.99")
            output_list1.str_age3 = to_string(ledger.debt2, "->>,>>>,>>>,>>9.99")
            output_list1.str_age4 = to_string(ledger.debt3, "->>,>>>,>>>,>>9.99")
            output_list1.str_rechnr = " "


            output_list1 = Output_list1()
            output_list1_data.append(output_list1)

            output_list1.str_counter = " "
            output_list1.cust_name = "Statistic Percentage (%) :"
            output_list1.prev_balance =  to_decimal("0")
            output_list1.debit =  to_decimal("0")
            output_list1.credit =  to_decimal("0")
            output_list1.end_balance =  to_decimal(100.00)
            output_list1.age1 = ( to_decimal(ledger.debt0) / to_decimal(tmp_saldo) * to_decimal("100") )
            output_list1.age2 = ( to_decimal(ledger.debt1) / to_decimal(tmp_saldo) * to_decimal("100") )
            output_list1.age3 = ( to_decimal(ledger.debt2) / to_decimal(tmp_saldo) * to_decimal("100") )
            output_list1.age4 = ( to_decimal(ledger.debt3) / to_decimal(tmp_saldo) * to_decimal("100") )
            output_list1.rechnr = 0
            output_list1.str_pbalance = " "
            output_list1.str_debit = " "
            output_list1.str_credit = " "
            output_list1.str_ebalance = to_string(100.00, "->>,>>>,>>>,>>9.99")
            output_list1.str_age1 = to_string((ledger.debt0 / tmp_saldo * 100) , "->>,>>>,>>>,>>9.99")
            output_list1.str_age2 = to_string((ledger.debt1 / tmp_saldo * 100) , "->>,>>>,>>>,>>9.99")
            output_list1.str_age3 = to_string((ledger.debt2 / tmp_saldo * 100) , "->>,>>>,>>>,>>9.99")
            output_list1.str_age4 = to_string((ledger.debt3 / tmp_saldo * 100) , "->>,>>>,>>>,>>9.99")
            output_list1.str_rechnr = " "


    def fill_in_list(fill_billno:bool):

        nonlocal output_list1_data, from_date, curr_bezeich, guest_name, outlist, billname, bill_number, long_digit, debitor, artikel, guest, htparam
        nonlocal guestno, from_art, to_art, from_name, to_name, to_date, day1, day2, day3, detailed


        nonlocal age_list, ledger, output_list, output_list1
        nonlocal age_list_data, ledger_data, output_list_data, output_list1_data


        output_list = Output_list()
        output_list_data.append(output_list)


        if fill_billno:
            output_list.rechnr = to_string(bill_number, ">>>>>>>>>")
        output_list.str = outlist

        if substring(outlist, 0, 5) == ("-----").lower() :
            output_list.rechnr = "---------"
        output_list.age1 = substring (str, 109, 18)
        output_list.age2 = substring (str, 127, 18)
        output_list.age3 = substring (str, 145, 18)
        output_list.age4 = substring (str, 163, 18)


    age_list()

    return generate_output()