from functions.additional_functions import *
import decimal
from datetime import date
from models import Guest, Artikel, Debitor, Bill, Reservation, Res_line, H_bill, Waehrung, Bediener

def ar_subledger_create_age_list1_webbl(incl:bool, t_artnr:int, t_dept:int, from_name:str, to_name:str, fr_date:date, to_date:date, bdate:date, gastnr:int):
    tot_debt = to_decimal("0.0")
    tot_paid = to_decimal("0.0")
    t_age_list_list = []
    curr_rechnr:int = 0
    opart:int = 0
    opart1:int = 1
    opart2:int = 1
    rechnr:int = 0
    nr:int = 0
    curr_saldo:decimal = to_decimal("0.0")
    ankunft:date = None
    abreise:date = None
    voucherno:str = ""
    gname:str = ""
    do_it:bool = False
    t_resnr:int = 0
    t_name:str = ""
    guest = artikel = debitor = bill = reservation = res_line = h_bill = waehrung = bediener = None

    ar_list = age_list = t_age_list = guest1 = artikel1 = debt = gast = None

    ar_list_list, Ar_list = create_model("Ar_list", {"arrecid":int})
    age_list_list, Age_list = create_model("Age_list", {"nr":int, "paint_it":bool, "rechnr":int, "refno":int, "rechnr2":int, "opart":int, "zahlkonto":int, "counter":int, "gastnr":int, "company":str, "billname":str, "gastnrmember":int, "zinr":str, "datum":date, "rgdatum":date, "paydatum":date, "user_init":str, "bezeich":str, "wabkurz":str, "debt":decimal, "credit":decimal, "fdebt":decimal, "t_debt":decimal, "tot_debt":decimal, "rid":int, "dept":int, "gname":str, "voucher":str, "ankunft":date, "abreise":date, "stay":int, "remarks":str, "ttl":decimal, "resname":str, "comp_name":str, "comp_add":str, "comp_fax":str, "comp_phone":str})
    t_age_list_list, T_age_list = create_model_like(Age_list)

    Guest1 = create_buffer("Guest1",Guest)
    Artikel1 = create_buffer("Artikel1",Artikel)
    Debt = create_buffer("Debt",Debitor)
    Gast = create_buffer("Gast",Guest)

    db_session = local_storage.db_session

    def generate_output():
        nonlocal tot_debt, tot_paid, t_age_list_list, curr_rechnr, opart, opart1, opart2, rechnr, nr, curr_saldo, ankunft, abreise, voucherno, gname, do_it, t_resnr, t_name, guest, artikel, debitor, bill, reservation, res_line, h_bill, waehrung, bediener
        nonlocal incl, t_artnr, t_dept, from_name, to_name, fr_date, to_date, bdate, gastnr
        nonlocal guest1, artikel1, debt, gast


        nonlocal ar_list, age_list, t_age_list, guest1, artikel1, debt, gast
        nonlocal ar_list_list, age_list_list, t_age_list_list
        return {"tot_debt": tot_debt, "tot_paid": tot_paid, "t-age-list": t_age_list_list}


    age_list_list.clear()
    ar_list_list.clear()
    curr_rechnr = 0

    if incl:
        opart2 = 2


    else:
        opart2 = 0


    tot_debt =  to_decimal("0")
    tot_paid =  to_decimal("0")
    nr = 0

    artikel = db_session.query(Artikel).filter(
             (Artikel.artnr == t_artnr) & (Artikel.departement == t_dept)).first()

    debitor_obj_list = []
    for debitor, gast in db_session.query(Debitor, Gast).join(Gast,(Gast.gastnr == Debitor.gastnr)).filter(
             (Debitor.artnr == artikel.artnr) & (Debitor.gastnr == gastnr) & (Debitor.opart >= opart) & (Debitor.opart <= opart2) & (Debitor.rgdatum >= fr_date) & (Debitor.rgdatum <= to_date) & (Debitor.zahlkonto == 0)).order_by(Gast.name, Debitor.gastnr, Debitor.debref, Debitor.rgdatum, Debitor.rechnr).all():
        if debitor._recid in debitor_obj_list:
            continue
        else:
            debitor_obj_list.append(debitor._recid)


        do_it = True

        if debitor.opart == 2 and bdate != None and debitor.rgdatum < bdate:

            debt = db_session.query(Debt).filter(
                     (Debt.rechnr == debitor.rechnr) & (Debt.counter == debitor.counter) & (Debt.artnr == debitor.artnr) & (Debt.zahlkonto > 0) & (Debt.rgdatum >= bdate)).first()
            do_it = None ! == debt

        if do_it:
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

                        if reservation:
                            voucherno = reservation.vesrdepot

                        res_line = db_session.query(Res_line).filter(
                                 (Res_line.resnr == bill.resnr) & (Res_line.reslinnr == bill.parent_nr) & (Res_line.zipreis > 0)).first()

                        if res_line:
                            gname = res_line.name
                            ankunft = res_line.ankunft
                            abreise = res_line.abreise


                else:

                    if re.match(r".*resno:.*",debitor.vesrcod, re.IGNORECASE):

                        if num_entries(debitor.vesrcod, ";") == 1:
                            t_resnr = to_int(substring(debitor.vesrcod, 25, len(debitor.vesrcod) - 1))
                        else:
                            t_name = trim(entry(0, debitor.vesrcod, ";"))
                            t_resnr = to_int(substring(t_name, 25, len(t_name) - 1))

                        reservation = db_session.query(Reservation).filter(
                                 (Reservation.resnr == t_resnr)).first()

                        if reservation:
                            voucherno = reservation.vesrdepot

                        res_line = db_session.query(Res_line).filter(
                                 (Res_line.resnr == t_resnr)).first()

                        if res_line:

                            guest = db_session.query(Guest).filter(
                                     (Guest.gastnr == res_line.gastnrmember)).first()
                            gname = guest.name + ", " + guest.vorname1 + guest.anredefirma + " " + guest.anrede1
            else:

                h_bill = db_session.query(H_bill).filter(
                         (H_bill.rechnr == debitor.rechnr) & (H_bill.departement == debitor.betriebsnr)).first()

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
            age_list.tot_debt =  to_decimal(debitor.saldo)
            age_list.dept = debitor.betriebsnr
            age_list.rid = debitor._recid
            age_list.gname = gname
            age_list.ankunft = ankunft
            age_list.abreise = abreise
            age_list.ttl =  to_decimal(debitor.vesrdep)
            age_list.stay = abreise - ankunft
            age_list.voucher = voucherno
            age_list.remarks = debitor.vesrcod
            age_list.company = gast.name + ", " + gast.vorname1 +\
                    gast.anredefirma + " " + gast.anrede1
            age_list.billname = age_list.company
            age_list.datum = debitor.rgdatum
            age_list.rgdatum = debitor.rgdatum
            age_list.debt =  to_decimal(debitor.saldo)
            age_list.fdebt =  to_decimal(debitor.vesrdep)

            if bill:
                age_list.rechnr2 = bill.rechnr2

            if debitor.betrieb_gastmem != 0:

                waehrung = db_session.query(Waehrung).filter(
                         (Waehrung.waehrungsnr == debitor.betrieb_gastmem)).first()

                if waehrung:
                    age_list.wabkurz = waehrung.wabkurz

            bediener = db_session.query(Bediener).filter(
                     (Bediener.nr == debitor.bediener_nr)).first()

            if bediener:
                age_list.user_init = bediener.userinit
            curr_saldo =  to_decimal(debitor.saldo)
            tot_debt =  to_decimal(tot_debt) + to_decimal(debitor.saldo)

            if debitor.counter > 0:

                for debt in db_session.query(Debt).filter(
                         (Debt.rechnr == debitor.rechnr) & (Debt.counter == debitor.counter) & (Debt.artnr == debitor.artnr) & (Debt.zahlkonto > 0) & (Debt.rgdatum <= to_date)).order_by(Debt.rgdatum).all():
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
                    age_list.credit =  - to_decimal(debt.saldo)
                    age_list.dept = debitor.betriebsnr
                    age_list.fdebt =  - to_decimal(debt.vesrdep)
                    age_list.rid = debitor._recid
                    age_list.company = gast.name + ", " + gast.vorname1 +\
                            gast.anredefirma + " " + gast.anrede1


                    tot_paid =  to_decimal(tot_paid) - to_decimal(debt.saldo)

                    artikel1 = db_session.query(Artikel1).filter(
                             (Artikel1.artnr == debt.zahlkonto) & (Artikel1.departement == 0)).first()

                    if artikel1:
                        age_list.bezeich = artikel1.bezeich

                    bediener = db_session.query(Bediener).filter(
                             (Bediener.nr == debt.bediener_nr)).first()

                    if bediener:
                        age_list.user_init = bediener.userinit
                    curr_saldo =  to_decimal(curr_saldo) + to_decimal(debt.saldo)
                    age_list.tot_debt =  to_decimal(curr_saldo)

                    if debt.betrieb_gastmem != 0:

                        waehrung = db_session.query(Waehrung).filter(
                                 (Waehrung.waehrungsnr == debt.betrieb_gastmem)).first()

                        if waehrung:
                            age_list.wabkurz = waehrung.wabkurz


    guest1_obj_list = []
    for guest1 in db_session.query(Guest1).filter(
             ((Guest1.gastnr.in_(list(set([age_list.gastnrmember for age_list in age_list_list)]))))).order_by(age_list.company, age_list.datum, age_list.counter, age_list.billname.desc()).all():
        if guest1._recid in guest1_obj_list:
            continue
        else:
            guest1_obj_list.append(guest1._recid)

        guest = db_session.query(Guest).filter(
                 (Guest.gastnr == age_list.gastnr)).first()
        t_age_list = T_age_list()
        t_age_list_list.append(t_age_list)

        buffer_copy(age_list, t_age_list)
        t_age_list.resname = guest.name + ", " + guest.vorname1 + guest.anredefirma + " " + guest.anrede1 + chr (10) + guest.adresse1 + chr (10) + guest.wohnort + " " + guest.plz + chr (10) + guest.land
        t_age_list.comp_name = guest.name + ", " + guest.vorname1 + guest.anredefirma + " " + guest.anrede1
        t_age_list.comp_add = guest.adresse1 + " " + guest.wohnort + " " + guest.plz + " " + guest.land
        t_age_list.comp_fax = guest.fax
        t_age_list.comp_phone = guest.telefon

    return generate_output()