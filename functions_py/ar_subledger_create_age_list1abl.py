#using conversion tools version: 1.0.0.117
#-------------------------------------------
# Rd 28/7/2025
# gitlab: 272
# abreise & ankunft -> None, 
#-------------------------------------------
from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Artikel, Debitor, Guest, Bill, Reservation, Res_line, H_bill, Waehrung, Bediener

def ar_subledger_create_age_list1abl(incl:bool, t_artnr:int, t_dept:int, from_name:string, to_name:string, fr_date:date, to_date:date, bdate:date):

    prepare_cache ([Artikel, Guest, Bill, Reservation, Res_line, H_bill, Waehrung, Bediener])

    tot_debt = to_decimal("0.0")
    tot_paid = to_decimal("0.0")
    age_list_data = []
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
    artikel = debitor = guest = bill = reservation = res_line = h_bill = waehrung = bediener = None

    ar_list = age_list = artikel1 = debt = gast = None

    ar_list_data, Ar_list = create_model("Ar_list", {"arrecid":int})
    age_list_data, Age_list = create_model("Age_list", {"nr":int, "paint_it":bool, "rechnr":int, "refno":int, "rechnr2":int, "opart":int, "zahlkonto":int, "counter":int, "gastnr":int, "company":string, "billname":string, "gastnrmember":int, "zinr":string, "datum":date, "rgdatum":date, "paydatum":date, "user_init":string, "bezeich":string, "wabkurz":string, "debt":Decimal, "credit":Decimal, "fdebt":Decimal, "t_debt":Decimal, "tot_debt":Decimal, "rid":int, "dept":int, "gname":string, "voucher":string, "ankunft":date, "abreise":date, "stay":int, "remarks":string, "ttl":Decimal, "resname":string, "comp_name":string, "comp_add":string, "comp_fax":string, "comp_phone":string})

    Artikel1 = create_buffer("Artikel1",Artikel)
    Debt = create_buffer("Debt",Debitor)
    Gast = create_buffer("Gast",Guest)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal tot_debt, tot_paid, age_list_data, curr_rechnr, opart, opart1, opart2, rechnr, nr, curr_saldo, ankunft, abreise, voucherno, gname, do_it, t_resnr, t_name, artikel, debitor, guest, bill, reservation, res_line, h_bill, waehrung, bediener
        nonlocal incl, t_artnr, t_dept, from_name, to_name, fr_date, to_date, bdate
        nonlocal artikel1, debt, gast


        nonlocal ar_list, age_list, artikel1, debt, gast
        nonlocal ar_list_data, age_list_data

        return {"tot_debt": tot_debt, "tot_paid": tot_paid, "age-list": age_list_data}

    age_list_data.clear()
    ar_list_data.clear()
    curr_rechnr = 0

    if incl:
        opart = 2
        opart2 = 2


    tot_debt =  to_decimal("0")
    tot_paid =  to_decimal("0")
    nr = 0

    artikel = get_cache (Artikel, {"artnr": [(eq, t_artnr)],"departement": [(eq, t_dept)]})

    for debitor in db_session.query(Debitor).filter(
             (Debitor.artnr == artikel.artnr) & (Debitor.name >= (from_name).lower()) & (Debitor.opart <= opart) & (Debitor.rgdatum >= fr_date) & (Debitor.rgdatum <= to_date) & (Debitor.zahlkonto == 0)).order_by(Debitor._recid).all():
        do_it = True

        if debitor.opart == 2 and bdate != None and debitor.rgdatum < bdate:

            debt = db_session.query(Debt).filter(
                     (Debt.rechnr == debitor.rechnr) & (Debt.counter == debitor.counter) & (Debt.artnr == debitor.artnr) & (Debt.zahlkonto > 0) & (Debt.rgdatum >= bdate)).first()
            do_it = None != debt

        if do_it:
            ar_list = Ar_list()
            ar_list_data.append(ar_list)

            ar_list.arrecid = debitor._recid

    for debitor in db_session.query(Debitor).filter(
             (Debitor.artnr == artikel.artnr) & (Debitor.name >= (from_name).lower()) & (Debitor.opart >= opart1) & (Debitor.opart <= opart2) & (Debitor.rgdatum >= fr_date) & (Debitor.rgdatum <= to_date) & (Debitor.zahlkonto > 0)).order_by(Debitor._recid).all():
        do_it = True

        if debitor.opart == 2 and debitor.rgdatum < bdate:

            debt = db_session.query(Debt).filter(
                     (Debt.rechnr == debitor.rechnr) & (Debt.counter == debitor.counter) & (Debt.artnr == debitor.artnr) & (Debt.zahlkonto > 0) & (Debt.rgdatum >= bdate)).first()
            do_it = None != debt

        if do_it:

            debt = db_session.query(Debt).filter(
                     (Debt.rechnr == debitor.rechnr) & (Debt.counter == debitor.counter) & (Debt.artnr == debitor.artnr) & (Debt.zahlkonto == 0)).first()

            if debt:

                ar_list = query(ar_list_data, filters=(lambda ar_list: ar_list.arrecid == to_int(debt._recid)), first=True)

                if not ar_list:
                    ar_list = Ar_list()
                    ar_list_data.append(ar_list)

                    ar_list.arrecid = debt._recid

    debitor_obj_list = {}

    # Rd 28/7/2025
    # simpler for each find first
    # for debitor, gast in db_session.query(Debitor, Gast).join(Gast,(Gast.gastnr == Debitor.gastnr)).filter(
    #          ((to_int(Debitor._recid).in_(list(set([ar_list.arrecid for ar_list in ar_list_data])))))).order_by(Gast.name, Debitor.gastnr, Debitor.debref, Debitor.rgdatum, Debitor.rechnr).all():

    recid_list = [
        int(ar.arrecid) for ar in ar_list_data
        if ar.arrecid is not None and str(ar.arrecid).isdigit()
    ]

    # Step 2: Query debitor and gast using INNER JOIN, filtered by recid_list
    results = (
        db_session.query(Debitor, Gast)
        .join(Gast, Gast.gastnr == Debitor.gastnr)
        .filter(Debitor._recid.in_(recid_list))
        .order_by(Gast.name, Debitor.gastnr, Debitor.debref, Debitor.rgdatum, Debitor.rechnr)
        .all()
    )

    # Step 3: Iterate over valid pairs (mimicking DO block)
    for debitor, gast in results:
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
        age_list_data.append(age_list)

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

        if ankunft is not None:
            age_list.ankunft = ankunft

        if abreise is not None:
            age_list.abreise = abreise

        age_list.ttl =  to_decimal(debitor.vesrdep)

        # Rd, 28/7/2025
        # tambah nama table
        # age_list.stay = (abreise - ankunft).days
        if abreise is not None and ankunft is not None:
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
                age_list_data.append(age_list)

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


    for age_list in query(age_list_data):

        guest = get_cache (Guest, {"gastnr": [(eq, age_list.gastnr)]})
        age_list.resname = guest.name + ", " + guest.vorname1 + guest.anredefirma + " " + guest.anrede1 + chr_unicode(10) + guest.adresse1 + chr_unicode(10) + guest.wohnort + " " + guest.plz + chr_unicode(10) + guest.land
        age_list.comp_name = guest.name + ", " + guest.vorname1 + guest.anredefirma + " " + guest.anrede1
        age_list.comp_add = guest.adresse1 + " " + guest.wohnort + " " + guest.plz + " " + guest.land
        age_list.comp_fax = guest.fax
        age_list.comp_phone = guest.telefon

    return generate_output()