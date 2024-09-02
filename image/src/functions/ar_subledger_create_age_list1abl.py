from functions.additional_functions import *
import decimal
from datetime import date
from sqlalchemy import func
import re
from models import Artikel, Debitor, Guest, Bill, Reservation, Res_line, H_bill, Waehrung, Bediener

def ar_subledger_create_age_list1abl(incl:bool, t_artnr:int, t_dept:int, from_name:str, to_name:str, fr_date:date, to_date:date, bdate:date):
    tot_debt = 0
    tot_paid = 0
    age_list_list = []
    curr_rechnr:int = 0
    opart:int = 0
    opart1:int = 1
    opart2:int = 1
    rechnr:int = 0
    nr:int = 0
    curr_saldo:decimal = 0
    ankunft:date = None
    abreise:date = None
    voucherno:str = ""
    gname:str = ""
    do_it:bool = False
    t_resnr:int = 0
    t_name:str = ""
    artikel = debitor = guest = bill = reservation = res_line = h_bill = waehrung = bediener = None

    ar_list = age_list = artikel1 = debt = gast = None

    ar_list_list, Ar_list = create_model("Ar_list", {"arrecid":int})
    age_list_list, Age_list = create_model("Age_list", {"nr":int, "paint_it":bool, "rechnr":int, "refno":int, "rechnr2":int, "opart":int, "zahlkonto":int, "counter":int, "gastnr":int, "company":str, "billname":str, "gastnrmember":int, "zinr":str, "datum":date, "rgdatum":date, "paydatum":date, "user_init":str, "bezeich":str, "wabkurz":str, "debt":decimal, "credit":decimal, "fdebt":decimal, "t_debt":decimal, "tot_debt":decimal, "rid":int, "dept":int, "gname":str, "voucher":str, "ankunft":date, "abreise":date, "stay":int, "remarks":str, "ttl":decimal, "resname":str, "comp_name":str, "comp_add":str, "comp_fax":str, "comp_phone":str})

    Artikel1 = Artikel
    Debt = Debitor
    Gast = Guest

    db_session = local_storage.db_session

    def generate_output():
        nonlocal tot_debt, tot_paid, age_list_list, curr_rechnr, opart, opart1, opart2, rechnr, nr, curr_saldo, ankunft, abreise, voucherno, gname, do_it, t_resnr, t_name, artikel, debitor, guest, bill, reservation, res_line, h_bill, waehrung, bediener
        nonlocal artikel1, debt, gast


        nonlocal ar_list, age_list, artikel1, debt, gast
        nonlocal ar_list_list, age_list_list
        return {"tot_debt": tot_debt, "tot_paid": tot_paid, "age-list": age_list_list}

    age_list_list.clear()
    ar_list_list.clear()
    curr_rechnr = 0

    if incl:
        opart = 2
        opart2 = 2


    tot_debt = 0
    tot_paid = 0
    nr = 0

    artikel = db_session.query(Artikel).filter(
            (Artikel.artnr == t_artnr) &  (Artikel.departement == t_dept)).first()

    for debitor in db_session.query(Debitor).filter(
            (Debitor.artnr == artikel.artnr) &  (func.lower(Debitor.name) >= (from_name).lower()) &  (Debitor.opart <= opart) &  (Debitor.rgdatum >= fr_date) &  (Debitor.rgdatum <= to_date) &  (Debitor.zahlkonto == 0)).all():
        do_it = True

        if debitor.opart == 2 and bdate != None and debitor.rgdatum < bdate:

            debt = db_session.query(Debt).filter(
                    (Debt.rechnr == debitor.rechnr) &  (Debt.counter == debitor.counter) &  (Debt.artnr == debitor.artnr) &  (Debt.zahlkonto > 0) &  (Debt.rgdatum >= bdate)).first()
            do_it = None != debt

        if do_it:
            ar_list = Ar_list()
            ar_list_list.append(ar_list)

            ar_list.arRecid = debitor._recid

    for debitor in db_session.query(Debitor).filter(
            (Debitor.artnr == artikel.artnr) &  (func.lower(Debitor.name) >= (from_name).lower()) &  (Debitor.opart >= opart1) &  (Debitor.opart <= opart2) &  (Debitor.rgdatum >= fr_date) &  (Debitor.rgdatum <= to_date) &  (Debitor.zahlkonto > 0)).all():
        do_it = True

        if debitor.opart == 2 and debitor.rgdatum < bdate:

            debt = db_session.query(Debt).filter(
                    (Debt.rechnr == debitor.rechnr) &  (Debt.counter == debitor.counter) &  (Debt.artnr == debitor.artnr) &  (Debt.zahlkonto > 0) &  (Debt.rgdatum >= bdate)).first()
            do_it = None != debt

        if do_it:

            debt = db_session.query(Debt).filter(
                    (Debt.rechnr == debitor.rechnr) &  (Debt.counter == debitor.counter) &  (Debt.artnr == debitor.artnr) &  (Debt.zahlkonto == 0)).first()

            if debt:

                ar_list = query(ar_list_list, filters=(lambda ar_list :ar_list.arRecid == to_int(debt._recid)), first=True)

                if not ar_list:
                    ar_list = Ar_list()
                    ar_list_list.append(ar_list)

                    ar_list.arRecid = debt._recid

    for ar_list in query(ar_list_list):
        debitor = db_session.query(Debitor).filter((to_int(Debitor._recid) == ar_list.arRecid)).first()
        if not debitor:
            continue

        gast = db_session.query(Gast).filter((Gast.gastnr == debitor.gastnr)).first()
        if not gast:
            continue

        gname = ""
        ankunft = None
        abreise = None

        if debitor.betriebsnr == 0:

            if debitor.rechnr != 0:

                bill = db_session.query(Bill).filter(
                        (Bill.rechnr == debitor.rechnr)).first()

                if bill:

                    reservation = db_session.query(Reservation).filter(
                            (Reservation.resnr == bill.resnr)).first()

                if bill and reservation:

                    for res_line in db_session.query(Res_line).filter(
                            (Res_line.resnr == bill.resnr) &  (Res_line.reslinnr == bill.parent_nr) &  (Res_line.zipreis > 0)).all():
                        gname = res_line.name
                        ankunft = res_line.ankunft
                        abreise = res_line.abreise
                        break


                if reservation:
                    voucherno = reservation.vesrdepot
            else:

                if re.match(".*resno:.*",debitor.vesrcod):

                    if num_entries(debitor.vesrcod, ";") == 1:
                        t_resnr = to_int(substring(debitor.vesrcod, 25, len(debitor.vesrcod) - 1))
                    else:
                        t_name = trim(entry(0, debitor.vesrcod, ";"))
                        t_resnr = to_int(substring(t_name, 25, len(t_name) - 1))

                    reservation = db_session.query(Reservation).filter(
                            (Reservation.resnr == t_resnr)).first()

                    res_line = db_session.query(Res_line).filter(
                            (Res_line.resnr == t_resnr)).first()

                    if res_line:

                        guest = db_session.query(Guest).filter(
                                (Guest.gastnr == res_line.gastnrmember)).first()
                        gname = guest.name + ", " + guest.vorname1 + guest.anredefirma + " " + guest.anrede1

                    if reservation:
                        voucherno = reservation.vesrdepot
        else:

            h_bill = db_session.query(H_bill).filter(
                    (H_bill.rechnr == debitor.rechnr) &  (H_bill.departement == debitor.betriebsnr)).first()

            if h_bill and h_bill.bilname != "":
                gname = h_bill.bilname

            elif debitor.name != "":
                gname = debitor.name
        nr = nr + 1
        age_list = Age_list()
        age_list_list.append(age_list)

        age_list.nr = nr
        age_list.rechnr = debitor.rechnr
        age_list.refno = debitor.debref
        age_list.opart = debitor.opart
        age_list.counter = debitor.counter
        age_list.gastnr = debitor.gastnr
        age_list.gastnrmember = debitor.gastnrmember
        age_list.zinr = debitor.zinr
        age_list.tot_debt = debitor.saldo
        age_list.dept = debitor.betriebsnr
        age_list.rid = debitor._recid
        age_list.gname = gname
        age_list.ankunft = ankunft
        age_list.abreise = abreise
        age_list.ttl = debitor.vesrdep
        age_list.stay = abreise - ankunft
        age_list.voucher = voucherno
        age_list.remarks = debitor.vesrcod
        age_list.company = gast.name + ", " + gast.vorname1 +\
                gast.anredefirma + " " + gast.anrede1
        age_list.billname = age_list.company
        age_list.datum = debitor.rgdatum
        age_list.rgdatum = debitor.rgdatum
        age_list.debt = debitor.saldo
        age_list.fdebt = debitor.vesrdep

        if bill:
            age_list.rechnr2 = bill.rechnr2

        if debitor.betrieb_gastmem != 0:

            waehrung = db_session.query(Waehrung).filter(
                    (Waehrungsnr == debitor.betrieb_gastmem)).first()

            if waehrung:
                age_list.wabkurz = waehrung.wabkurz

        bediener = db_session.query(Bediener).filter(
                (Bediener.nr == debitor.bediener_nr)).first()

        if bediener:
            age_list.user_init = bediener.userinit
        curr_saldo = debitor.saldo
        tot_debt = tot_debt + debitor.saldo

        if debitor.counter > 0:

            for debt in db_session.query(Debt).filter(
                    (Debt.rechnr == debitor.rechnr) &  (Debt.counter == debitor.counter) &  (Debt.artnr == debitor.artnr) &  (Debt.zahlkonto > 0) &  (Debt.rgdatum <= to_date)).all():
                nr = nr + 1
                age_list = Age_list()
                age_list_list.append(age_list)

                age_list.nr = nr
                age_list.rechnr = debt.rechnr
                age_list.opart = debt.opart
                age_list.counter = debt.counter
                age_list.zahlkonto = debt.zahlkonto
                age_list.gastnr = debt.gastnr
                age_list.gastnrmember = debt.gastnrmember
                age_list.datum = debitor.rgdatum
                age_list.rgdatum = debt.rgdatum
                age_list.paydatum = debt.rgdatum
                age_list.credit = - debt.saldo
                age_list.dept = debitor.betriebsnr
                age_list.fdebt = - debt.vesrdep
                age_list.rid = debitor._recid
                age_list.company = gast.name + ", " + gast.vorname1 +\
                        gast.anredefirma + " " + gast.anrede1


                tot_paid = tot_paid - debt.saldo

                artikel1 = db_session.query(Artikel1).filter(
                        (Artikel1.artnr == debt.zahlkonto) &  (Artikel1.departement == 0)).first()

                if artikel1:
                    age_list.bezeich = artikel1.bezeich

                bediener = db_session.query(Bediener).filter(
                        (Bediener.nr == debt.bediener_nr)).first()

                if bediener:
                    age_list.user_init = bediener.userinit
                curr_saldo = curr_saldo + debt.saldo
                age_list.tot_debt = curr_saldo

                if debt.betrieb_gastmem != 0:

                    waehrung = db_session.query(Waehrung).filter(
                            (Waehrungsnr == debt.betrieb_gastmem)).first()

                    if waehrung:
                        age_list.wabkurz = waehrung.wabkurz


    for age_list in query(age_list_list):

        guest = db_session.query(Guest).filter(
                (Guest.gastnr == age_list.gastnr)).first()
        age_list.resname = guest.name + ", " + guest.vorname1 + guest.anredefirma + " " + guest.anrede1 + chr (10) + guest.adresse1 + chr (10) + guest.wohnort + " " + guest.plz + chr (10) + guest.land
        age_list.comp_name = guest.name + ", " + guest.vorname1 + guest.anredefirma + " " + guest.anrede1
        age_list.comp_add = guest.adresse1 + " " + guest.wohnort + " " + guest.plz + " " + guest.land
        age_list.comp_fax = guest.fax
        age_list.comp_phone = guest.telefon

    return generate_output()