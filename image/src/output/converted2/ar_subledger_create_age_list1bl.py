#using conversion tools version: 1.0.0.112

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Guest, Artikel, Debitor, Bill, Reservation, Res_line, H_bill, Waehrung, Bediener

def ar_subledger_create_age_list1bl(incl:bool, t_artnr:int, t_dept:int, from_name:string, to_name:string, fr_date:date, to_date:date, bdate:date):

    prepare_cache ([Guest, Artikel, Bill, Reservation, Res_line, H_bill, Waehrung, Bediener])

    tot_debt = to_decimal("0.0")
    tot_paid = to_decimal("0.0")
    t_age_list_list = []
    curr_rechnr:int = 0
    opart:int = 0
    opart1:int = 1
    opart2:int = 1
    rechnr:int = 0
    nr:int = 0
    curr_saldo:Decimal = to_decimal("0.0")
    ankunft:date = None
    abreise:date = None
    voucherno:string = ""
    gname:string = ""
    do_it:bool = False
    t_resnr:int = 0
    t_name:string = ""
    guest = artikel = debitor = bill = reservation = res_line = h_bill = waehrung = bediener = None

    ar_list = age_list = t_age_list = guest1 = artikel1 = debt = gast = None

    ar_list_list, Ar_list = create_model("Ar_list", {"arrecid":int})
    age_list_list, Age_list = create_model("Age_list", {"nr":int, "paint_it":bool, "rechnr":int, "refno":int, "rechnr2":int, "opart":int, "zahlkonto":int, "counter":int, "gastnr":int, "company":string, "billname":string, "gastnrmember":int, "zinr":string, "datum":date, "rgdatum":date, "paydatum":date, "user_init":string, "bezeich":string, "wabkurz":string, "debt":Decimal, "credit":Decimal, "fdebt":Decimal, "t_debt":Decimal, "tot_debt":Decimal, "rid":int, "dept":int, "gname":string, "voucher":string, "ankunft":date, "abreise":date, "stay":int, "remarks":string, "ttl":Decimal, "resname":string, "comp_name":string, "comp_add":string, "comp_fax":string, "comp_phone":string})
    t_age_list_list, T_age_list = create_model_like(Age_list)

    Guest1 = create_buffer("Guest1",Guest)
    Artikel1 = create_buffer("Artikel1",Artikel)
    Debt = create_buffer("Debt",Debitor)
    Gast = create_buffer("Gast",Guest)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal tot_debt, tot_paid, t_age_list_list, curr_rechnr, opart, opart1, opart2, rechnr, nr, curr_saldo, ankunft, abreise, voucherno, gname, do_it, t_resnr, t_name, guest, artikel, debitor, bill, reservation, res_line, h_bill, waehrung, bediener
        nonlocal incl, t_artnr, t_dept, from_name, to_name, fr_date, to_date, bdate
        nonlocal guest1, artikel1, debt, gast


        nonlocal ar_list, age_list, t_age_list, guest1, artikel1, debt, gast
        nonlocal ar_list_list, age_list_list, t_age_list_list

        return {"tot_debt": tot_debt, "tot_paid": tot_paid, "t-age-list": t_age_list_list}


    age_list_list.clear()
    ar_list_list.clear()
    curr_rechnr = 0

    if incl:
        opart = 2
        opart2 = 2


    tot_debt =  to_decimal("0")
    tot_paid =  to_decimal("0")
    nr = 0

    artikel = get_cache (Artikel, {"artnr": [(eq, t_artnr)],"departement": [(eq, t_dept)]})

    for debitor in db_session.query(Debitor).filter(
             (Debitor.artnr == artikel.artnr) & (Debitor.name >= (from_name).lower()) & (Debitor.name <= (to_name).lower()) & (Debitor.opart <= opart) & (Debitor.rgdatum >= fr_date) & (Debitor.rgdatum <= to_date) & (Debitor.zahlkonto == 0)).order_by(Debitor._recid).all():
        do_it = True

        if debitor.opart == 2 and bdate != None and debitor.rgdatum < bdate:

            debt = db_session.query(Debt).filter(
                     (Debt.rechnr == debitor.rechnr) & (Debt.counter == debitor.counter) & (Debt.artnr == debitor.artnr) & (Debt.zahlkonto > 0) & (Debt.rgdatum >= bdate)).first()
            do_it = None != debt

        if do_it:
            ar_list = Ar_list()
            ar_list_list.append(ar_list)

            ar_list.arrecid = debitor._recid

    for debitor in db_session.query(Debitor).filter(
             (Debitor.artnr == artikel.artnr) & (Debitor.name >= (from_name).lower()) & (Debitor.name <= (to_name).lower()) & (Debitor.opart >= opart) & (Debitor.opart <= opart2) & (Debitor.rgdatum >= fr_date) & (Debitor.rgdatum <= to_date) & (Debitor.zahlkonto > 0)).order_by(Debitor._recid).all():
        do_it = True

        if debitor.opart == 2 and debitor.rgdatum < bdate:

            debt = db_session.query(Debt).filter(
                     (Debt.rechnr == debitor.rechnr) & (Debt.counter == debitor.counter) & (Debt.artnr == debitor.artnr) & (Debt.zahlkonto > 0) & (Debt.rgdatum >= bdate)).first()
            do_it = None != debt

        if do_it:

            debt = db_session.query(Debt).filter(
                     (Debt.rechnr == debitor.rechnr) & (Debt.counter == debitor.counter) & (Debt.artnr == debitor.artnr) & (Debt.zahlkonto == 0)).first()

            if debt:

                ar_list = query(ar_list_list, filters=(lambda ar_list: ar_list.arrecid == to_int(debt._recid)), first=True)

                if not ar_list:
                    ar_list = Ar_list()
                    ar_list_list.append(ar_list)

                    ar_list.arrecid = debt._recid

    debitor_obj_list = {}
    for debitor, gast in db_session.query(Debitor, Gast).join(Gast,(Gast.gastnr == Debitor.gastnr)).filter(
             ((to_int(Debitor._recid).in_(list(set([ar_list.arrecid for ar_list in ar_list_list])))))).order_by(Gast.name, Debitor.gastnr, Debitor.debref, Debitor.rgdatum, Debitor.rechnr).all():
        if debitor_obj_list.get(debitor._recid):
            continue
        else:
            debitor_obj_list[debitor._recid] = True


        gname = ""
        ankunft = None
        abreise = None

        if debitor.betriebsnr == 0:

            if debitor.rechnr != 0:

                bill = get_cache (Bill, {"rechnr": [(eq, debitor.rechnr)]})

                if bill:

                    reservation = get_cache (Reservation, {"resnr": [(eq, bill.resnr)]})

                if bill and reservation:

                    for res_line in db_session.query(Res_line).filter(
                             (Res_line.resnr == bill.resnr) & (Res_line.reslinnr == bill.parent_nr) & (Res_line.zipreis > 0)).order_by(Res_line.reslinnr).yield_per(100):
                        gname = res_line.name
                        ankunft = res_line.ankunft
                        abreise = res_line.abreise
                        break


                if reservation:
                    voucherno = reservation.vesrdepot
            else:

                if matches(debitor.vesrcod,r"*resno:*"):

                    if num_entries(debitor.vesrcod, ";") == 1:
                        t_resnr = to_int(substring(debitor.vesrcod, 25, length(debitor.vesrcod) - 1))
                    else:
                        t_name = trim(entry(0, debitor.vesrcod, ";"))
                        t_resnr = to_int(substring(t_name, 25, length(t_name) - 1))

                    reservation = get_cache (Reservation, {"resnr": [(eq, t_resnr)]})

                    res_line = get_cache (Res_line, {"resnr": [(eq, t_resnr)]})

                    if res_line:

                        guest = get_cache (Guest, {"gastnr": [(eq, res_line.gastnrmember)]})
                        gname = guest.name + ", " + guest.vorname1 + guest.anredefirma + " " + guest.anrede1

                    if reservation:
                        voucherno = reservation.vesrdepot
        else:

            h_bill = get_cache (H_bill, {"rechnr": [(eq, debitor.rechnr)],"departement": [(eq, debitor.betriebsnr)]})

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
        age_list.stay = (abreise - ankunft).days
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

            waehrung = get_cache (Waehrung, {"waehrungsnr": [(eq, debitor.betrieb_gastmem)]})

            if waehrung:
                age_list.wabkurz = waehrung.wabkurz

        bediener = get_cache (Bediener, {"nr": [(eq, debitor.bediener_nr)]})

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

                artikel1 = get_cache (Artikel, {"artnr": [(eq, debt.zahlkonto)],"departement": [(eq, 0)]})

                if artikel1:
                    age_list.bezeich = artikel1.bezeich

                bediener = get_cache (Bediener, {"nr": [(eq, debt.bediener_nr)]})

                if bediener:
                    age_list.user_init = bediener.userinit
                curr_saldo =  to_decimal(curr_saldo) + to_decimal(debt.saldo)
                age_list.tot_debt =  to_decimal(curr_saldo)

                if debt.betrieb_gastmem != 0:

                    waehrung = get_cache (Waehrung, {"waehrungsnr": [(eq, debt.betrieb_gastmem)]})

                    if waehrung:
                        age_list.wabkurz = waehrung.wabkurz


    guest1_obj_list = {}
    for guest1 in db_session.query(Guest1).filter(
             ((Guest1.gastnr.in_(list(set([age_list.gastnrmember for age_list in age_list_list])))))).order_by(age_list.company, age_list.datum, age_list.counter, age_list.billname.desc()).all():
        if guest1_obj_list.get(guest1._recid):
            continue
        else:
            guest1_obj_list[guest1._recid] = True

        age_list = query(age_list_list, (lambda age_list: (guest1.gastnr == age_list.gastnrmember)), first=True)

        guest = get_cache (Guest, {"gastnr": [(eq, age_list.gastnr)]})
        t_age_list = T_age_list()
        t_age_list_list.append(t_age_list)

        buffer_copy(age_list, t_age_list)
        t_age_list.resname = guest.name + ", " + guest.vorname1 + guest.anredefirma + " " + guest.anrede1 + chr_unicode(10) + guest.adresse1 + chr_unicode(10) + guest.wohnort + " " + guest.plz + chr_unicode(10) + guest.land
        t_age_list.comp_name = guest.name + ", " + guest.vorname1 + guest.anredefirma + " " + guest.anrede1
        t_age_list.comp_add = guest.adresse1 + " " + guest.wohnort + " " + guest.plz + " " + guest.land
        t_age_list.comp_fax = guest.fax
        t_age_list.comp_phone = guest.telefon

    return generate_output()