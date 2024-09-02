from functions.additional_functions import *
import decimal
from datetime import date
from sqlalchemy import func
import re
from models import Debitor, Artikel, Guest, Bill_line, Bediener, Waehrung, Reservation, Res_line

def ar_debtpaybl(artnr:int, userinit:str, bill_nr:int, temp_art2:int, bill_date:date, bill_name:str, to_name:str, bill_saldo:decimal, art_selected:int, foutstand:decimal, outstand:decimal):
    curr_art = 0
    age_list_list = []
    t_debt_list = []
    t_resnr:int = 0
    t_name:str = ""
    debitor = artikel = guest = bill_line = bediener = waehrung = reservation = res_line = None

    t_debt = age_list = abuff = debthis = artikel1 = age_list1 = None

    t_debt_list, T_debt = create_model("T_debt", {"t_debt_recid":int, "rgdatum":date})
    age_list_list, Age_list = create_model("Age_list", {"selected":bool, "ar_recid":int, "rechnr":int, "refno":int, "counter":int, "gastnr":int, "billname":str, "gastnrmember":int, "gastname":str, "zinr":str, "rgdatum":date, "user_init":str, "debthis":decimal, "debt_foreign":decimal, "currency":str, "credit":decimal, "tot_debt":decimal, "vouc_nr":str, "prevdate":date, "remarks":str, "b_resname":str, "ci_date":date, "co_date":date})

    Abuff = Age_list
    abuff_list = age_list_list

    Debt = Debitor
    Artikel1 = Artikel
    Age_list1 = Age_list
    age_list1_list = age_list_list


    db_session = local_storage.db_session

    def generate_output():
        nonlocal curr_art, age_list_list, t_debt_list, t_resnr, t_name, debitor, artikel, guest, bill_line, bediener, waehrung, reservation, res_line
        nonlocal abuff, debthis, artikel1, age_list1


        nonlocal t_debt, age_list, abuff, debthis, artikel1, age_list1
        nonlocal t_debt_list, age_list_list
        return {"curr_art": curr_art, "age-list": age_list_list, "t-debthis": t_debt_list}

    def create_age_list():

        nonlocal curr_art, age_list_list, t_debt_list, t_resnr, t_name, debitor, artikel, guest, bill_line, bediener, waehrung, reservation, res_line
        nonlocal abuff, debthis, artikel1, age_list1


        nonlocal t_debt, age_list, abuff, debthis, artikel1, age_list1
        nonlocal t_debt_list, age_list_list

        curr_rechnr:int = 0
        curr_saldo:decimal = 0
        opart:int = 1
        i:int = 0
        Artikel1 = Artikel
        curr_art = artnr
        age_list_list.clear()
        curr_rechnr = 0
        outstand = 0
        foutstand = 0

        if bill_nr != 0:

            for debitor in db_session.query(Debitor).filter(
                        (Debitor.artnr == temp_art2) &  (Debitor.rechnr == bill_nr) &  (Debitor.rgdatum <= bill_date) &  (Debitor.opart < 2)).all():

                if debitor.counter != 0:

                    age_list = query(age_list_list, filters=(lambda age_list :age_list.counter == debitor.counter), first=True)

                if not age_list or debitor.counter == 0:
                    age_list = Age_list()
                    age_list_list.append(age_list)

                    age_list.ar_recid = debitor._recid
                    age_list.rgdatum = debitor.rgdatum
                    age_list.counter = debitor.counter
                    age_list.rechnr = debitor.rechnr
                    age_list.refno = debitor.debref
                    age_list.gastnr = debitor.gastnr
                    age_list.gastnrmember = debitor.gastnrmember
                    age_list.zinr = debitor.zinr
                    disp_guest_debt()

                    guest = db_session.query(Guest).filter(
                                (Guest.gastnr == debitor.gastnr)).first()
                    age_list.billname = guest.name + ", " + guest.vorname1 + guest.anredefirma + " " + guest.anrede1

                    guest = db_session.query(Guest).filter(
                                (Guest.gastnr == debitor.gastnrmember)).first()

                    if guest:
                        age_list.gastname = guest.name + ", " + guest.vorname1 + guest.anredefirma + " " + guest.anrede1

                    bill_line = db_session.query(Bill_line).filter(
                                (Bill_line.rechnr == debitor.rechnr) &  (Bill_line.betrag == (- debitor.saldo)) &  ((Bill_line.zeit >= (debitor.transzeit - 2)) &  ((Bill_line.zeit <= debitor.TRANSzeit + 2)))).first()

                if debitor.zahlkonto == 0:

                    bediener = db_session.query(Bediener).filter(
                                (Bediener.nr == debitor.bediener_nr)).first()

                    if bediener:
                        age_list.user_init = bediener.userinit
                    age_list.rgdatum = debitor.rgdatum
                    age_list.debthis = age_list.debthis + debitor.saldo
                    age_list.debt_foreign = age_list.debt_foreign + debitor.vesrdep

                    if debitor.betrieb_gastmem != 0:

                        waehrung = db_session.query(Waehrung).filter(
                                    (Waehrungsnr == debitor.betrieb_gastmem)).first()

                        if waehrung:
                            age_list.currency = waehrung.wabkurz
                else:
                    age_list.credit = age_list.credit - debitor.saldo
                age_list.tot_debt = age_list.tot_debt + debitor.saldo

        elif (bill_name != "") and (substring(bill_name, 0, 1) != "*"):

            for debitor in db_session.query(Debitor).filter(
                        (Debitor.artnr == temp_art2) &  ((func.lower(Debitor.name).op("~")(".*" + bill_name + ".*")) &  (func.lower(Debitor.name) <= to_name)) &  (Debitor.rgdatum <= bill_date) &  (Debitor.opart < 2)).all():

                if debitor.counter != 0:

                    age_list = query(age_list_list, filters=(lambda age_list :age_list.counter == debitor.counter), first=True)

                if not age_list or debitor.counter == 0:
                    age_list = Age_list()
                    age_list_list.append(age_list)

                    age_list.ar_recid = debitor._recid
                    age_list.rgdatum = debitor.rgdatum
                    age_list.counter = debitor.counter
                    age_list.rechnr = debitor.rechnr
                    age_list.refno = debitor.debref
                    age_list.gastnr = debitor.gastnr
                    age_list.gastnrmember = debitor.gastnrmember
                    age_list.zinr = debitor.zinr
                    disp_guest_debt()

                    guest = db_session.query(Guest).filter(
                                (Guest.gastnr == debitor.gastnr)).first()
                    age_list.billname = guest.name + ", " + guest.vorname1 + guest.anredefirma + " " + guest.anrede1

                    guest = db_session.query(Guest).filter(
                                (Guest.gastnr == debitor.gastnrmember)).first()

                    if guest:
                        age_list.gastname = guest.name + ", " + guest.vorname1 + guest.anredefirma + " " + guest.anrede1

                    bill_line = db_session.query(Bill_line).filter(
                                (Bill_line.rechnr == debitor.rechnr) &  (Bill_line.betrag == (- debitor.saldo)) &  ((Bill_line.zeit >= (debitor.transzeit - 2)) &  ((Bill_line.zeit <= debitor.TRANSzeit + 2)))).first()

                    if re.match(".*resno:.*",debitor.vesrcod):

                        if num_entries(debitor.vesrcod, ";") == 1:
                            t_resnr = to_int(trim(entry(1, entry(0, debitor.vesrcod, ";") , ":")))


                        else:
                            t_name = trim(entry(0, debitor.vesrcod, ";"))
                            t_resnr = to_int(trim(entry(1, t_name, ":")))

                        reservation = db_session.query(Reservation).filter(
                                    (Reservation.resnr == t_resnr)).first()

                        res_line = db_session.query(Res_line).filter(
                                    (Res_line.resnr == t_resnr)).first()

                        if res_line:

                            guest = db_session.query(Guest).filter(
                                        (Guest.gastnr == res_line.gastnrmember)).first()
                            age_list.gastname = guest.name + ", " + guest.vorname1 + guest.anredefirma + " " + guest.anrede1

                    if (re.match(".*;.*",debitor.vesrcod)):
                        age_list.vouc_nr = trim(entry(1, debitor.vesrcod, ";"))
                        age_list.remarks = trim(entry(0, debitor.vesrcod, ";"))


                    else:
                        age_list.remarks = debitor.vesrcod

                        bill_line = db_session.query(Bill_line).filter(
                                    (Bill_line.rechnr == debitor.rechnr) &  (Bill_line.betrag == (- debitor.saldo)) &  ((Bill_line.zeit >= (debitor.transzeit - 2)) &  ((Bill_line.zeit <= debitor.TRANSzeit + 2)))).first()

                        if bill_line:
                            for i in range(1,(len(bill_line.bezeich))  + 1) :

                                if substring(bill_line.bezeich, i - 1, 1) == "/":
                                    age_list.vouc_nr = substring(bill_line.bezeich, (i + 1) - 1, (len(bill_line.bezeich) - i))
                                    i = len(bill_line.bezeich)

                if debitor.zahlkonto == 0:

                    bediener = db_session.query(Bediener).filter(
                                (Bediener.nr == debitor.bediener_nr)).first()

                    if bediener:
                        age_list.user_init = bediener.userinit
                    age_list.rgdatum = debitor.rgdatum
                    age_list.debthis = age_list.debthis + debitor.saldo
                    age_list.debt_foreign = age_list.debt_foreign + debitor.vesrdep

                    if debitor.betrieb_gastmem != 0:

                        waehrung = db_session.query(Waehrung).filter(
                                    (Waehrungsnr == debitor.betrieb_gastmem)).first()

                        if waehrung:
                            age_list.currency = waehrung.wabkurz
                else:
                    age_list.credit = age_list.credit - debitor.saldo
                age_list.tot_debt = age_list.tot_debt + debitor.saldo

        elif (bill_name != "") and (substring(bill_name, 0, 1) == "*"):

            for debitor in db_session.query(Debitor).filter(
                        (Debitor.artnr == temp_art2) &  (Debitor.name.op("~")(bill_name)) &  (Debitor.rgdatum <= bill_date) &  (Debitor.opart < 2)).all():

                if debitor.counter != 0:

                    age_list = query(age_list_list, filters=(lambda age_list :age_list.counter == debitor.counter), first=True)

                if not age_list or debitor.counter == 0:
                    age_list = Age_list()
                    age_list_list.append(age_list)

                    age_list.ar_recid = debitor._recid
                    age_list.rgdatum = debitor.rgdatum
                    age_list.counter = debitor.counter
                    age_list.rechnr = debitor.rechnr
                    age_list.refno = debitor.debref
                    age_list.gastnr = debitor.gastnr
                    age_list.gastnrmember = debitor.gastnrmember
                    age_list.zinr = debitor.zinr
                    disp_guest_debt()

                    guest = db_session.query(Guest).filter(
                                (Guest.gastnr == debitor.gastnr)).first()
                    age_list.billname = guest.name + ", " + guest.vorname1 + guest.anredefirma + " " + guest.anrede1

                    guest = db_session.query(Guest).filter(
                                (Guest.gastnr == debitor.gastnrmember)).first()

                    if guest:
                        age_list.gastname = guest.name + ", " + guest.vorname1 + guest.anredefirma + " " + guest.anrede1

                    bill_line = db_session.query(Bill_line).filter(
                                (Bill_line.rechnr == debitor.rechnr) &  (Bill_line.betrag == (- debitor.saldo)) &  ((Bill_line.zeit >= (debitor.transzeit - 2)) &  ((Bill_line.zeit <= debitor.transzeit + 2)))).first()

                    if re.match(".*resno:.*",debitor.vesrcod):

                        if num_entries(debitor.vesrcod, ";") == 1:
                            t_resnr = to_int(trim(entry(1, entry(0, debitor.vesrcod, ";") , ":")))


                        else:
                            t_name = trim(entry(0, debitor.vesrcod, ";"))
                            t_resnr = to_int(trim(entry(1, t_name, ":")))

                        reservation = db_session.query(Reservation).filter(
                                    (Reservation.resnr == t_resnr)).first()

                        res_line = db_session.query(Res_line).filter(
                                    (Res_line.resnr == t_resnr)).first()

                        if res_line:

                            guest = db_session.query(Guest).filter(
                                        (Guest.gastnr == res_line.gastnrmember)).first()
                            age_list.gastname = guest.name + ", " + guest.vorname1 + guest.anredefirma + " " + guest.anrede1

                    if (re.match(".*;.*",debitor.vesrcod)):
                        age_list.vouc_nr = trim(entry(1, debitor.vesrcod, ";"))
                        age_list.remarks = trim(entry(0, debitor.vesrcod, ";"))


                    else:
                        age_list.remarks = debitor.vesrcod

                        bill_line = db_session.query(Bill_line).filter(
                                    (Bill_line.rechnr == debitor.rechnr) &  (Bill_line.betrag == (- debitor.saldo)) &  ((Bill_line.zeit >= (debitor.transzeit - 2)) &  ((Bill_line.zeit <= debitor.transzeit + 2)))).first()

                        if bill_line:
                            for i in range(1,(len(bill_line.bezeich))  + 1) :

                                if substring(bill_line.bezeich, i - 1, 1) == "/":
                                    age_list.vouc_nr = substring(bill_line.bezeich, (i + 1) - 1, (len(bill_line.bezeich) - i))
                                    i = len(bill_line.bezeich)

                if debitor.zahlkonto == 0:

                    bediener = db_session.query(Bediener).filter(
                                (Bediener.nr == debitor.bediener_nr)).first()

                    if bediener:
                        age_list.user_init = bediener.userinit
                    age_list.rgdatum = debitor.rgdatum
                    age_list.debthis = age_list.debthis + debitor.saldo
                    age_list.debt_foreign = age_list.debt_foreign + debitor.vesrdep

                    if debitor.betrieb_gastmem != 0:

                        waehrung = db_session.query(Waehrung).filter(
                                    (Waehrungsnr == debitor.betrieb_gastmem)).first()

                        if waehrung:
                            age_list.currency = waehrung.wabkurz
                else:
                    age_list.credit = age_list.credit - debitor.saldo
                age_list.tot_debt = age_list.tot_debt + debitor.saldo

        elif bill_name == "":

            for debitor in db_session.query(Debitor).filter(
                        (Debitor.artnr == temp_art2) &  (Debitor.rgdatum <= bill_date) &  (Debitor.opart < 2)).all():

                if debitor.counter != 0:

                    age_list = query(age_list_list, filters=(lambda age_list :age_list.counter == debitor.counter), first=True)

                if not age_list or debitor.counter == 0:
                    age_list = Age_list()
                    age_list_list.append(age_list)

                    age_list.ar_recid = debitor._recid
                    age_list.rgdatum = debitor.rgdatum
                    age_list.counter = debitor.counter
                    age_list.rechnr = debitor.rechnr
                    age_list.refno = debitor.debref
                    age_list.gastnr = debitor.gastnr
                    age_list.gastnrmember = debitor.gastnrmember
                    age_list.zinr = debitor.zinr

                    guest = db_session.query(Guest).filter(
                                (Guest.gastnr == debitor.gastnr)).first()
                    age_list.billname = guest.name + ", " + guest.vorname1 + guest.anredefirma + " " + guest.anrede1

                    guest = db_session.query(Guest).filter(
                                (Guest.gastnr == debitor.gastnrmember)).first()

                    if guest:
                        age_list.gastname = guest.name + ", " + guest.vorname1 + guest.anredefirma + " " + guest.anrede1

                    bill_line = db_session.query(Bill_line).filter(
                                (Bill_line.rechnr == debitor.rechnr) &  (Bill_line.betrag == (- debitor.saldo)) &  ((Bill_line.zeit >= (debitor.transzeit - 2)) &  ((Bill_line.zeit <= debitor.transzeit + 2)))).first()

                    if re.match(".*resno:.*",debitor.vesrcod):

                        if num_entries(debitor.vesrcod, ";") == 1:
                            t_resnr = to_int(trim(entry(1, entry(0, debitor.vesrcod, ";") , ":")))


                        else:
                            t_name = trim(entry(0, debitor.vesrcod, ";"))
                            t_resnr = to_int(trim(entry(1, t_name, ":")))

                        reservation = db_session.query(Reservation).filter(
                                    (Reservation.resnr == t_resnr)).first()

                        res_line = db_session.query(Res_line).filter(
                                    (Res_line.resnr == t_resnr)).first()

                        if res_line:

                            guest = db_session.query(Guest).filter(
                                        (Guest.gastnr == res_line.gastnrmember)).first()
                            age_list.gastname = guest.name + ", " + guest.vorname1 + guest.anredefirma + " " + guest.anrede1

                    if (re.match(".*;.*",debitor.vesrcod)):
                        age_list.vouc_nr = trim(entry(1, debitor.vesrcod, ";"))
                        age_list.remarks = trim(entry(0, debitor.vesrcod, ";"))


                    else:
                        age_list.remarks = debitor.vesrcod

                        bill_line = db_session.query(Bill_line).filter(
                                    (Bill_line.rechnr == debitor.rechnr) &  (Bill_line.betrag == (- debitor.saldo)) &  ((Bill_line.zeit >= (debitor.transzeit - 2)) &  ((Bill_line.zeit <= debitor.transzeit + 2)))).first()

                        if bill_line:
                            for i in range(1,(len(bill_line.bezeich))  + 1) :

                                if substring(bill_line.bezeich, i - 1, 1) == "/":
                                    age_list.vouc_nr = substring(bill_line.bezeich, (i + 1) - 1, (len(bill_line.bezeich) - i))
                                    i = len(bill_line.bezeich)

                if debitor.zahlkonto == 0:

                    bediener = db_session.query(Bediener).filter(
                                (Bediener.nr == debitor.bediener_nr)).first()

                    if bediener:
                        age_list.user_init = bediener.userinit
                    age_list.rgdatum = debitor.rgdatum
                    age_list.debthis = age_list.debthis + debitor.saldo
                    age_list.debt_foreign = age_list.debt_foreign + debitor.vesrdep
                    disp_guest_debt()

                    if debitor.betrieb_gastmem != 0:

                        waehrung = db_session.query(Waehrung).filter(
                                    (Waehrungsnr == debitor.betrieb_gastmem)).first()

                        if waehrung:
                            age_list.currency = waehrung.wabkurz
                else:
                    age_list.credit = age_list.credit - debitor.saldo
                age_list.tot_debt = age_list.tot_debt + debitor.saldo
        art_selected = 1

        if bill_saldo != 0:

            for age_list in query(age_list_list, filters=(lambda age_list :age_list.tot_debt != bill_saldo)):
                age_list_list.remove(age_list)

    def disp_guest_debt():

        nonlocal curr_art, age_list_list, t_debt_list, t_resnr, t_name, debitor, artikel, guest, bill_line, bediener, waehrung, reservation, res_line
        nonlocal abuff, debthis, artikel1, age_list1


        nonlocal t_debt, age_list, abuff, debthis, artikel1, age_list1
        nonlocal t_debt_list, age_list_list

        gastnr:int = 0
        Age_list1 = Age_list
        Debt = Debitor
        age_list.b_resname = "Previous Payment Remark:"

        if debitor.counter != 0:
            age_list.b_resname = "Payment Remark:"

            for debthis in db_session.query(Debt).filter(
                    (Debt.counter == debitor.counter) &  (Debt.opart == 1)).all():

                if debthis.vesrcod != "":
                    age_list.b_resname = age_list.b_resname + chr (10) + to_string(debthis.rgdatum) + " " + trim(to_string(debthis.saldo, "->>>,>>>,>>9.99")) + ": " + debthis.vesrcod

        if age_list.b_resname.lower()  == "Payment Remark:":
            age_list.b_resname = ""
        else:
            age_list.b_resname = age_list.b_resname + chr (10) + chr (10)

        guest = db_session.query(Guest).filter(
                (Guest.gastnr == debitor.gastnr)).first()
        age_list.b_resname = age_list.b_resname + guest.name + ", " + guest.vorname1 + guest.anredefirma + " " + guest.anrede1 + chr (10) + guest.adresse1 + chr (10) + guest.wohnort + " " + guest.plz

    create_age_list()

    for abuff in query(abuff_list):
        debthis = db_session.query(Debt).filter((Debt._recid == abuff.ar_recid)).first()
        if not debthis:
            continue

        t_debt = T_debt()
        t_debt_list.append(t_debt)

        t_debt.t_debt_recid = debthis._recid
        t_debt.rgdatum = debthis.rgdatum

    return generate_output()