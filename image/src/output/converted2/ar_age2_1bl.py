#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from functions.htpchar import htpchar
from functions.htpint import htpint
from models import Debitor, Artikel, Guest, Waehrung, Bill

def ar_age2_1bl(pvilanguage:int, curr_gastnr:int, from_art:int, disptype:int, to_date:date, show_inv:bool):

    prepare_cache ([Debitor, Artikel, Guest, Waehrung, Bill])

    msg_str = ""
    output_list_list = []
    day1:int = 30
    day2:int = 30
    day3:int = 30
    price_decimal:int = 0
    default_fcurr:string = ""
    outlist:string = ""
    fremdwbetrag:Decimal = to_decimal("0.0")
    lvcarea:string = "ar-age2"
    debitor = artikel = guest = waehrung = bill = None

    age_list = ledger = output_list = debt = None

    age_list_list, Age_list = create_model("Age_list", {"artnr":int, "rechnr":int, "inv_no":int, "counter":int, "gastnr":int, "creditlimit":Decimal, "rgdatum":date, "gastname":string, "fbetrag":Decimal, "saldo":Decimal, "debt0":Decimal, "debt1":Decimal, "debt2":Decimal, "debt3":Decimal, "tot_debt":Decimal, "curr":string, "inv_soa":int})
    ledger_list, Ledger = create_model("Ledger", {"artnr":int, "bezeich":string, "debt0":Decimal, "debt1":Decimal, "debt2":Decimal, "debt3":Decimal, "tot_debt":Decimal})
    output_list_list, Output_list = create_model("Output_list", {"inv_no":string, "fbetrag":string, "creditlimit":Decimal, "curr":string, "str":string, "inv_soa":string})

    Debt = create_buffer("Debt",Debitor)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal msg_str, output_list_list, day1, day2, day3, price_decimal, default_fcurr, outlist, fremdwbetrag, lvcarea, debitor, artikel, guest, waehrung, bill
        nonlocal pvilanguage, curr_gastnr, from_art, disptype, to_date, show_inv
        nonlocal debt


        nonlocal age_list, ledger, output_list, debt
        nonlocal age_list_list, ledger_list, output_list_list

        return {"msg_str": msg_str, "output-list": output_list_list}

    def age_list():

        nonlocal msg_str, output_list_list, day1, day2, day3, price_decimal, default_fcurr, outlist, fremdwbetrag, lvcarea, debitor, artikel, guest, waehrung, bill
        nonlocal pvilanguage, curr_gastnr, from_art, disptype, to_date, show_inv
        nonlocal debt


        nonlocal age_list, ledger, output_list, debt
        nonlocal age_list_list, ledger_list, output_list_list

        curr_art:int = 0
        billdate:date = None
        ct:int = 0
        gastname:string = ""
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
        creditlimit:Decimal = to_decimal("0.0")
        debt0:Decimal = to_decimal("0.0")
        debt1:Decimal = to_decimal("0.0")
        debt2:Decimal = to_decimal("0.0")
        debt3:Decimal = to_decimal("0.0")
        tot_debt:Decimal = to_decimal("0.0")
        t_fdebt:Decimal = to_decimal("0.0")
        ar_saldo:Decimal = to_decimal("0.0")
        debt = None
        Debt =  create_buffer("Debt",Debitor)

        artikel = get_cache (Artikel, {"artnr": [(eq, from_art)],"departement": [(eq, 0)]})

        if not artikel:

            return

        guest = get_cache (Guest, {"gastnr": [(eq, curr_gastnr)]})
        gastname = guest.name + ", " + guest.vorname1 + " " + guest.anrede1 + guest.anredefirma
        outlist = ""
        fill_in_list()
        outlist = to_string(artikel.artnr, ">>>>>9") + " - " + to_string(artikel.bezeich, "x(30)")
        fill_in_list()
        outlist = ""
        fill_in_list()
        outlist = "(" + trim(to_string(gastname, "x(30)")) + ")"
        fill_in_list()
        curr_art = 0

        for debitor in db_session.query(Debitor).filter(
                 (Debitor.artnr == from_art) & (Debitor.rgdatum <= to_date) & (Debitor.opart == 0) & (Debitor.gastnr == curr_gastnr)).order_by(Debitor.rgdatum).all():

            if curr_art != debitor.artnr:
                curr_art = debitor.artnr

                artikel = get_cache (Artikel, {"artnr": [(eq, curr_art)],"departement": [(eq, 0)]})

            if disptype == 0:
                ar_saldo =  to_decimal(debitor.saldo)
            else:
                ar_saldo =  to_decimal(debitor.vesrdep)

            if debitor.counter != 0:

                for debt in db_session.query(Debt).filter(
                             (Debt.rechnr == debitor.rechnr) & (Debt.counter == debitor.counter) & (Debt.opart == 1) & (Debt.zahlkonto != 0) & (Debt.rgdatum <= to_date)).order_by(Debt._recid).all():

                    if disptype == 0:
                        ar_saldo =  to_decimal(ar_saldo) + to_decimal(debt.saldo)
                    else:
                        ar_saldo =  to_decimal(ar_saldo) + to_decimal(debt.vesrdep)

            guest = get_cache (Guest, {"gastnr": [(eq, debitor.gastnr)]})
            age_list = Age_list()
            age_list_list.append(age_list)

            age_list.artnr = debitor.artnr
            age_list.rechnr = debitor.rechnr
            age_list.rgdatum = debitor.rgdatum
            age_list.counter = debitor.counter
            age_list.gastnr = debitor.gastnr
            age_list.creditlimit =  to_decimal(guest.kreditlimit)
            age_list.tot_debt =  to_decimal(ar_saldo)
            age_list.gastname = debitor.vesrcod
            age_list.creditlimit =  to_decimal(guest.kreditlimit)
            age_list.fbetrag =  to_decimal(age_list.fbetrag) + to_decimal(debitor.vesrdep)
            age_list.inv_soa = debitor.debref

            waehrung = get_cache (Waehrung, {"waehrungsnr": [(eq, debitor.betrieb_gastmem)]})

            if waehrung:
                age_list.curr = waehrung.wabkurz
            else:
                age_list.curr = default_fcurr

            if to_date - age_list.rgdatum > day3:
                age_list.debt3 =  to_decimal(age_list.debt3) + to_decimal(ar_saldo)

            elif to_date - age_list.rgdatum > day2:
                age_list.debt2 =  to_decimal(age_list.debt2) + to_decimal(ar_saldo)

            elif to_date - age_list.rgdatum > day1:
                age_list.debt1 =  to_decimal(age_list.debt1) + to_decimal(ar_saldo)
            else:
                age_list.debt0 =  to_decimal(age_list.debt0) + to_decimal(ar_saldo)

            if show_inv:

                bill = get_cache (Bill, {"rechnr": [(eq, debitor.rechnr)]})

                if not bill:
                    msg_str = msg_str + translateExtended ("Bill", lvcarea, "") + " " + translateExtended ("not found.", lvcarea, "") + chr_unicode(2)
                else:
                    age_list.inv_no = bill.rechnr2
        curr_art = 0

        for debitor in db_session.query(Debitor).filter(
                 (Debitor.artnr == from_art) & (Debitor.rgdatum <= to_date) & (Debitor.opart == 2) & (Debitor.zahlkonto == 0) & (Debitor.gastnr == curr_gastnr)).order_by(Debitor.rgdatum).all():

            debt = get_cache (Debitor, {"rechnr": [(eq, debitor.rechnr)],"counter": [(eq, debitor.counter)],"opart": [(eq, 2)],"zahlkonto": [(ne, 0)],"rgdatum": [(gt, to_date)]})

            if debt and debitor.gastnr == curr_gastnr:

                if curr_art != debitor.artnr:
                    curr_art = debitor.artnr

                    artikel = get_cache (Artikel, {"artnr": [(eq, curr_art)],"departement": [(eq, 0)]})

                if disptype == 0:
                    ar_saldo =  to_decimal(debitor.saldo)
                else:
                    ar_saldo =  to_decimal(debitor.vesrdep)

                for debt in db_session.query(Debt).filter(
                         (Debt.rechnr == debitor.rechnr) & (Debt.counter == debitor.counter) & (Debt.opart == 2) & (Debt.zahlkonto != 0) & (Debt.rgdatum <= to_date)).order_by(Debt._recid).all():

                    if disptype == 0:
                        ar_saldo =  to_decimal(ar_saldo) + to_decimal(debt.saldo)
                    else:
                        ar_saldo =  to_decimal(ar_saldo) + to_decimal(debt.vesrdep)

                guest = get_cache (Guest, {"gastnr": [(eq, debitor.gastnr)]})
                age_list = Age_list()
                age_list_list.append(age_list)

                age_list.artnr = debitor.artnr
                age_list.rechnr = debitor.rechnr
                age_list.rgdatum = debitor.rgdatum
                age_list.counter = debitor.counter
                age_list.gastnr = debitor.gastnr
                age_list.creditlimit =  to_decimal(guest.kreditlimit)
                age_list.tot_debt =  to_decimal(ar_saldo)
                age_list.gastname = debitor.vesrcod
                age_list.creditlimit =  to_decimal(guest.kreditlimit)
                age_list.fbetrag =  to_decimal(age_list.fbetrag) + to_decimal(debitor.vesrdep)
                age_list.inv_soa = debitor.debref

                waehrung = get_cache (Waehrung, {"waehrungsnr": [(eq, debitor.betrieb_gastmem)]})

                if waehrung:
                    age_list.curr = waehrung.wabkurz
                else:
                    age_list.curr = default_fcurr

                if to_date - age_list.rgdatum > day3:
                    age_list.debt3 =  to_decimal(age_list.debt3) + to_decimal(ar_saldo)

                elif to_date - age_list.rgdatum > day2:
                    age_list.debt2 =  to_decimal(age_list.debt2) + to_decimal(ar_saldo)

                elif to_date - age_list.rgdatum > day1:
                    age_list.debt1 =  to_decimal(age_list.debt1) + to_decimal(ar_saldo)
                else:
                    age_list.debt0 =  to_decimal(age_list.debt0) + to_decimal(ar_saldo)

                if show_inv:

                    bill = get_cache (Bill, {"rechnr": [(eq, debitor.rechnr)]})

                    if not bill:
                        msg_str = msg_str + translateExtended ("Bill", lvcarea, "") + " " + translateExtended ("not found.", lvcarea, "") + chr_unicode(2)
                    else:
                        age_list.inv_no = bill.rechnr2

        for age_list in query(age_list_list, filters=(lambda age_list: age_list.tot_debt != 0)):
            t_saldo =  to_decimal(t_saldo) + to_decimal(age_list.tot_debt)
            t_debt0 =  to_decimal(t_debt0) + to_decimal(age_list.debt0)
            t_debt1 =  to_decimal(t_debt1) + to_decimal(age_list.debt1)
            t_debt2 =  to_decimal(t_debt2) + to_decimal(age_list.debt2)
            t_debt3 =  to_decimal(t_debt3) + to_decimal(age_list.debt3)

            if price_decimal == 0:
                outlist = to_string(age_list.rechnr, ">>>>>>>>9") + to_string(age_list.gastname, "x(39)") + to_string(age_list.tot_debt, "->>>>,>>>,>>>,>>9") + to_string(to_date - age_list.rgdatum, ">>9") + to_string(age_list.debt0, "->>>>,>>>,>>>,>>9") + to_string(age_list.debt1, "->>>>,>>>,>>>,>>9") + to_string(age_list.debt2, "->>>>,>>>,>>>,>>9") + to_string(age_list.debt3, "->>>>,>>>,>>>,>>9")
            else:
                outlist = to_string(age_list.rechnr, ">>>>>>>>9") + to_string(age_list.gastname, "x(39)") + to_string(age_list.tot_debt, "->,>>>,>>>,>>9.99") + to_string(to_date - age_list.rgdatum, ">>9") + to_string(age_list.debt0, "->,>>>,>>>,>>9.99") + to_string(age_list.debt1, "->,>>>,>>>,>>9.99") + to_string(age_list.debt2, "->,>>>,>>>,>>9.99") + to_string(age_list.debt3, "->,>>>,>>>,>>9.99")
            fremdwbetrag =  to_decimal(age_list.fbetrag)
            t_fdebt =  to_decimal(t_fdebt) + to_decimal(fremdwbetrag)
            fill_in_list()
            output_list.curr = age_list.curr
            output_list.inv_no = to_string(age_list.inv_no, ">>>>>>>>>")
            output_list.inv_soa = "INV" + to_string(age_list.inv_soa, "999999999")
        fremdwbetrag =  to_decimal("0")
        fremdwbetrag =  to_decimal(t_fdebt)
        outlist = "-----------------------------------------------------------------------------------------------------------------------------------------------------------"
        fill_in_list()
        output_list.curr = "----"
        output_list.inv_no = "---------"

        if price_decimal == 0:
            outlist = to_string(translateExtended (" T O T A L A/R:", lvcarea, "") , "x(48)") + to_string(t_saldo, "->>>>,>>>,>>>,>>9") + " " + to_string(t_debt0, "->>>>,>>>,>>>,>>9") + to_string(t_debt1, "->>>>,>>>,>>>,>>9") + to_string(t_debt2, "->>>>,>>>,>>>,>>9") + to_string(t_debt3, "->>>>,>>>,>>>,>>9")
        else:
            outlist = to_string(translateExtended (" T O T A L A/R:", lvcarea, "") , "x(48)") + to_string(t_saldo, "->,>>>,>>>,>>9.99") + " " + to_string(t_debt0, "->,>>>,>>>,>>9.99") + to_string(t_debt1, "->,>>>,>>>,>>9.99") + to_string(t_debt2, "->,>>>,>>>,>>9.99") + to_string(t_debt3, "->,>>>,>>>,>>9.99")
        fill_in_list()
        outlist = ""
        fill_in_list()
        outlist = ""
        fill_in_list()


    def fill_in_list():

        nonlocal msg_str, output_list_list, day1, day2, day3, price_decimal, default_fcurr, outlist, fremdwbetrag, lvcarea, debitor, artikel, guest, waehrung, bill
        nonlocal pvilanguage, curr_gastnr, from_art, disptype, to_date, show_inv
        nonlocal debt


        nonlocal age_list, ledger, output_list, debt
        nonlocal age_list_list, ledger_list, output_list_list


        output_list = Output_list()
        output_list_list.append(output_list)

        output_list.str = outlist

        if fremdwbetrag != 0:
            output_list.fbetrag = to_string(fremdwbetrag, "->>>,>>>,>>9.99")

    default_fcurr = get_output(htpchar(143))
    price_decimal = get_output(htpint(491))
    day1 = get_output(htpint(330))
    day2 = get_output(htpint(331))
    day3 = get_output(htpint(332))
    day2 = day2 + day1
    day3 = day3 + day2
    age_list()

    return generate_output()