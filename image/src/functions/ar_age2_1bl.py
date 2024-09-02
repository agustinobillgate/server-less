from functions.additional_functions import *
import decimal
from datetime import date
from functions.htpchar import htpchar
from functions.htpint import htpint
from models import Debitor, Artikel, Guest, Waehrung, Bill

def ar_age2_1bl(pvilanguage:int, curr_gastnr:int, from_art:int, disptype:int, to_date:date, show_inv:bool):
    msg_str = ""
    output_list_list = []
    day1:int = 30
    day2:int = 30
    day3:int = 30
    price_decimal:int = 0
    default_fcurr:str = ""
    outlist:str = ""
    fremdwbetrag:decimal = 0
    lvcarea:str = "ar_age2"
    debitor = artikel = guest = waehrung = bill = None

    age_list = ledger = output_list = debt = None

    age_list_list, Age_list = create_model("Age_list", {"artnr":int, "rechnr":int, "inv_no":int, "counter":int, "gastnr":int, "creditlimit":decimal, "rgdatum":date, "gastname":str, "fbetrag":decimal, "saldo":decimal, "debt0":decimal, "debt1":decimal, "debt2":decimal, "debt3":decimal, "tot_debt":decimal, "curr":str, "inv_soa":int})
    ledger_list, Ledger = create_model("Ledger", {"artnr":int, "bezeich":str, "debt0":decimal, "debt1":decimal, "debt2":decimal, "debt3":decimal, "tot_debt":decimal})
    output_list_list, Output_list = create_model("Output_list", {"inv_no":str, "fbetrag":str, "creditlimit":decimal, "curr":str, "str":str, "inv_soa":str})

    Debt = Debitor

    db_session = local_storage.db_session

    def generate_output():
        nonlocal msg_str, output_list_list, day1, day2, day3, price_decimal, default_fcurr, outlist, fremdwbetrag, lvcarea, debitor, artikel, guest, waehrung, bill
        nonlocal debt


        nonlocal age_list, ledger, output_list, debt
        nonlocal age_list_list, ledger_list, output_list_list
        return {"msg_str": msg_str, "output-list": output_list_list}

    def age_list():

        nonlocal msg_str, output_list_list, day1, day2, day3, price_decimal, default_fcurr, outlist, fremdwbetrag, lvcarea, debitor, artikel, guest, waehrung, bill
        nonlocal debt


        nonlocal age_list, ledger, output_list, debt
        nonlocal age_list_list, ledger_list, output_list_list

        curr_art:int = 0
        billdate:date = None
        ct:int = 0
        gastname:str = ""
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
        creditlimit:decimal = 0
        debt0:decimal = 0
        debt1:decimal = 0
        debt2:decimal = 0
        debt3:decimal = 0
        tot_debt:decimal = 0
        t_fdebt:decimal = 0
        ar_saldo:decimal = 0
        Debt = Debitor

        artikel = db_session.query(Artikel).filter(
                (Artikel.artnr == from_art) &  (Artikel.departement == 0)).first()

        if not artikel:

            return

        guest = db_session.query(Guest).filter(
                (Guest.gastnr == curr_gastnr)).first()
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
                (Debitor.artnr == from_art) &  (Debitor.rgdatum <= to_date) &  (Debitor.opart == 0) &  (Debitor.gastnr == curr_gastnr)).all():

            if curr_art != debitor.artnr:
                curr_art = debitor.artnr

                artikel = db_session.query(Artikel).filter(
                            (Artikel.artnr == curr_art) &  (Artikel.departement == 0)).first()

            if disptype == 0:
                ar_saldo = debitor.saldo
            else:
                ar_saldo = debitor.vesrdep

            if debitor.counter != 0:

                for debt in db_session.query(Debt).filter(
                            (Debt.rechnr == debitor.rechnr) &  (Debt.counter == debitor.counter) &  (Debt.opart == 1) &  (Debt.zahlkonto != 0) &  (Debt.rgdatum <= to_date)).all():

                    if disptype == 0:
                        ar_saldo = ar_saldo + debt.saldo
                    else:
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
            age_list.gastname = debitor.vesrcod
            age_list.creditlimit = guest.kreditlimit
            age_list.fbetrag = age_list.fbetrag + debitor.vesrdep
            age_list.inv_soa = debitor.debref

            waehrung = db_session.query(Waehrung).filter(
                        (Waehrungsnr == debitor.betrieb_gastmem)).first()

            if waehrung:
                age_list.curr = waehrung.wabkurz
            else:
                age_list.curr = default_fcurr

            if to_date - age_list.rgdatum > day3:
                age_list.debt3 = age_list.debt3 + ar_saldo

            elif to_date - age_list.rgdatum > day2:
                age_list.debt2 = age_list.debt2 + ar_saldo

            elif to_date - age_list.rgdatum > day1:
                age_list.debt1 = age_list.debt1 + ar_saldo
            else:
                age_list.debt0 = age_list.debt0 + ar_saldo

            if show_inv:

                bill = db_session.query(Bill).filter(
                            (Bill.rechnr == debitor.rechnr)).first()

                if not bill:
                    msg_str = msg_str + translateExtended ("Bill", lvcarea, "") + " " + translateExtended ("not found.", lvcarea, "") + chr(2)
                else:
                    age_list.inv_no = bill.rechnr2
        curr_art = 0

        for debitor in db_session.query(Debitor).filter(
                (Debitor.artnr == from_art) &  (Debitor.rgdatum <= to_date) &  (Debitor.opart == 2) &  (Debitor.zahlkonto == 0) &  (Debitor.gastnr == curr_gastnr)).all():

            debt = db_session.query(Debt).filter(
                    (Debt.rechnr == debitor.rechnr) &  (Debt.counter == debitor.counter) &  (Debt.opart == 2) &  (Debt.zahlkonto != 0) &  (Debt.rgdatum > to_date)).first()

            if debt and debitor.gastnr == curr_gastnr:

                if curr_art != debitor.artnr:
                    curr_art = debitor.artnr

                    artikel = db_session.query(Artikel).filter(
                            (Artikel.artnr == curr_art) &  (Artikel.departement == 0)).first()

                if disptype == 0:
                    ar_saldo = debitor.saldo
                else:
                    ar_saldo = debitor.vesrdep

                for debt in db_session.query(Debt).filter(
                        (Debt.rechnr == debitor.rechnr) &  (Debt.counter == debitor.counter) &  (Debt.opart == 2) &  (Debt.zahlkonto != 0) &  (Debt.rgdatum <= to_date)).all():

                    if disptype == 0:
                        ar_saldo = ar_saldo + debt.saldo
                    else:
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
                age_list.gastname = debitor.vesrcod
                age_list.creditlimit = guest.kreditlimit
                age_list.fbetrag = age_list.fbetrag + debitor.vesrdep
                age_list.inv_soa = debitor.debref

                waehrung = db_session.query(Waehrung).filter(
                        (Waehrungsnr == debitor.betrieb_gastmem)).first()

                if waehrung:
                    age_list.curr = waehrung.wabkurz
                else:
                    age_list.curr = default_fcurr

                if to_date - age_list.rgdatum > day3:
                    age_list.debt3 = age_list.debt3 + ar_saldo

                elif to_date - age_list.rgdatum > day2:
                    age_list.debt2 = age_list.debt2 + ar_saldo

                elif to_date - age_list.rgdatum > day1:
                    age_list.debt1 = age_list.debt1 + ar_saldo
                else:
                    age_list.debt0 = age_list.debt0 + ar_saldo

                if show_inv:

                    bill = db_session.query(Bill).filter(
                            (Bill.rechnr == debitor.rechnr)).first()

                    if not bill:
                        msg_str = msg_str + translateExtended ("Bill", lvcarea, "") + " " + translateExtended ("not found.", lvcarea, "") + chr(2)
                    else:
                        age_list.inv_no = bill.rechnr2

        for age_list in query(age_list_list, filters=(lambda age_list :age_list.tot_debt != 0)):
            t_saldo = t_saldo + age_list.tot_debt
            t_debt0 = t_debt0 + age_list.debt0
            t_debt1 = t_debt1 + age_list.debt1
            t_debt2 = t_debt2 + age_list.debt2
            t_debt3 = t_debt3 + age_list.debt3

            if price_decimal == 0:
                outlist = to_string(age_list.rechnr, ">>>>>>>>9") + to_string(age_list.gastname, "x(39)") + to_string(age_list.tot_debt, "->>>>,>>>,>>>,>>9") + to_string(to_date - age_list.rgdatum, ">>9") + to_string(age_list.debt0, "->>>>,>>>,>>>,>>9") + to_string(age_list.debt1, "->>>>,>>>,>>>,>>9") + to_string(age_list.debt2, "->>>>,>>>,>>>,>>9") + to_string(age_list.debt3, "->>>>,>>>,>>>,>>9")
            else:
                outlist = to_string(age_list.rechnr, ">>>>>>>>9") + to_string(age_list.gastname, "x(39)") + to_string(age_list.tot_debt, "->,>>>,>>>,>>9.99") + to_string(to_date - age_list.rgdatum, ">>9") + to_string(age_list.debt0, "->,>>>,>>>,>>9.99") + to_string(age_list.debt1, "->,>>>,>>>,>>9.99") + to_string(age_list.debt2, "->,>>>,>>>,>>9.99") + to_string(age_list.debt3, "->,>>>,>>>,>>9.99")
            fremdwbetrag = age_list.fbetrag
            t_fdebt = t_fdebt + fremdwbetrag
            fill_in_list()
            output_list.curr = age_list.curr
            output_list.inv_no = to_string(age_list.inv_no, ">>>>>>>>>")
            output_list.inv_soa = "INV" + to_string(age_list.inv_soa, "999999999")
        fremdwbetrag = 0
        fremdwbetrag = t_fdebt
        outlist = "-----------------------------------------------------------------------------------------------------------------------------------------------------------"
        fill_in_list()
        output_list.curr = "----"
        output_list.inv_no = "---------"

        if price_decimal == 0:
            outlist = to_string(translateExtended ("         T O T A L  A/R:", lvcarea, "") , "x(48)") + to_string(t_saldo, "->>>>,>>>,>>>,>>9") + "   " + to_string(t_debt0, "->>>>,>>>,>>>,>>9") + to_string(t_debt1, "->>>>,>>>,>>>,>>9") + to_string(t_debt2, "->>>>,>>>,>>>,>>9") + to_string(t_debt3, "->>>>,>>>,>>>,>>9")
        else:
            outlist = to_string(translateExtended ("         T O T A L  A/R:", lvcarea, "") , "x(48)") + to_string(t_saldo, "->,>>>,>>>,>>9.99") + "   " + to_string(t_debt0, "->,>>>,>>>,>>9.99") + to_string(t_debt1, "->,>>>,>>>,>>9.99") + to_string(t_debt2, "->,>>>,>>>,>>9.99") + to_string(t_debt3, "->,>>>,>>>,>>9.99")
        fill_in_list()
        outlist = ""
        fill_in_list()
        outlist = ""
        fill_in_list()

    def fill_in_list():

        nonlocal msg_str, output_list_list, day1, day2, day3, price_decimal, default_fcurr, outlist, fremdwbetrag, lvcarea, debitor, artikel, guest, waehrung, bill
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