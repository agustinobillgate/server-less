#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import Artikel, Debitor, Bediener, Guest

def ar_closepaybl(case_type:int, bill_name:string, bill_nr:int, bill_artnr:int, counter:int, balance:Decimal):

    prepare_cache ([Artikel, Debitor, Bediener, Guest])

    b2_list_list = []
    b3_list_list = []
    artikel2_list = []
    artikel = debitor = bediener = guest = None

    b2_list = b3_list = artikel2 = artikel0 = artikel1 = debitor3 = bediener1 = None

    b2_list_list, B2_list = create_model("B2_list", {"name":string, "vorname1":string, "anrede1":string, "anredefirma":string, "rechnr":int, "artnr":int, "bezeich":string, "rgdatum":date, "saldo":Decimal, "counter":int, "b_resname":string, "b_comments":string})
    b3_list_list, B3_list = create_model("B3_list", {"rgdatum":date, "zahlkonto":int, "bezeich":string, "saldo":Decimal, "vesrdep":Decimal, "userinit":string})
    artikel2_list, Artikel2 = create_model("Artikel2", {"artnr":int, "bezeich":string})

    Artikel0 = create_buffer("Artikel0",Artikel)
    Artikel1 = create_buffer("Artikel1",Artikel)
    Debitor3 = create_buffer("Debitor3",Debitor)
    Bediener1 = create_buffer("Bediener1",Bediener)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal b2_list_list, b3_list_list, artikel2_list, artikel, debitor, bediener, guest
        nonlocal case_type, bill_name, bill_nr, bill_artnr, counter, balance
        nonlocal artikel0, artikel1, debitor3, bediener1


        nonlocal b2_list, b3_list, artikel2, artikel0, artikel1, debitor3, bediener1
        nonlocal b2_list_list, b3_list_list, artikel2_list

        return {"balance": balance, "b2-list": b2_list_list, "b3-list": b3_list_list, "artikel2": artikel2_list}

    def open_q2():

        nonlocal b2_list_list, b3_list_list, artikel2_list, artikel, debitor, bediener, guest
        nonlocal case_type, bill_name, bill_nr, bill_artnr, counter, balance
        nonlocal artikel0, artikel1, debitor3, bediener1


        nonlocal b2_list, b3_list, artikel2, artikel0, artikel1, debitor3, bediener1
        nonlocal b2_list_list, b3_list_list, artikel2_list

        artikel1 = None
        curr_rechnr:int = 0
        curr_saldo:Decimal = to_decimal("0.0")
        opart:int = 1
        to_name:string = ""
        Artikel1 =  create_buffer("Artikel1",Artikel)
        curr_rechnr = 0
        to_name = chr_unicode(asc(substring(bill_name, 0, 1)) + 1)

        if bill_nr > 0:

            debitor_obj_list = {}
            debitor = Debitor()
            guest = Guest()
            artikel0 = Artikel()
            for debitor.rechnr, debitor.artnr, debitor.rgdatum, debitor.saldo, debitor.counter, debitor._recid, debitor.zahlkonto, debitor.vesrdep, guest.name, guest.vorname1, guest.anrede1, guest.anredefirma, guest.bemerkung, guest._recid, artikel0.artnr, artikel0.bezeich, artikel0._recid in db_session.query(Debitor.rechnr, Debitor.artnr, Debitor.rgdatum, Debitor.saldo, Debitor.counter, Debitor._recid, Debitor.zahlkonto, Debitor.vesrdep, Guest.name, Guest.vorname1, Guest.anrede1, Guest.anredefirma, Guest.bemerkung, Guest._recid, Artikel0.artnr, Artikel0.bezeich, Artikel0._recid).join(Guest,(Guest.gastnr == Debitor.gastnr)).join(Artikel0,(Artikel0.artnr == Debitor.artnr) & (Artikel0.departement == 0)).filter(
                     (Debitor.artnr == bill_artnr) & (Debitor.opart == 2) & (Debitor.rechnr == bill_nr) & (Debitor.zahlkonto == 0)).order_by(Guest.name, Debitor.rgdatum).all():
                if debitor_obj_list.get(debitor._recid):
                    continue
                else:
                    debitor_obj_list[debitor._recid] = True


                create_b2_list()

        else:

            debitor_obj_list = {}
            debitor = Debitor()
            guest = Guest()
            artikel0 = Artikel()
            for debitor.rechnr, debitor.artnr, debitor.rgdatum, debitor.saldo, debitor.counter, debitor._recid, debitor.zahlkonto, debitor.vesrdep, guest.name, guest.vorname1, guest.anrede1, guest.anredefirma, guest.bemerkung, guest._recid, artikel0.artnr, artikel0.bezeich, artikel0._recid in db_session.query(Debitor.rechnr, Debitor.artnr, Debitor.rgdatum, Debitor.saldo, Debitor.counter, Debitor._recid, Debitor.zahlkonto, Debitor.vesrdep, Guest.name, Guest.vorname1, Guest.anrede1, Guest.anredefirma, Guest.bemerkung, Guest._recid, Artikel0.artnr, Artikel0.bezeich, Artikel0._recid).join(Guest,(Guest.gastnr == Debitor.gastnr)).join(Artikel0,(Artikel0.artnr == Debitor.artnr) & (Artikel0.departement == 0)).filter(
                     (Debitor.artnr == bill_artnr) & (Debitor.opart == 2) & (Debitor.name >= (bill_name).lower()) & (Debitor.name <= (to_name).lower()) & (Debitor.zahlkonto == 0)).order_by(Guest.name, Debitor.rechnr).all():
                if debitor_obj_list.get(debitor._recid):
                    continue
                else:
                    debitor_obj_list[debitor._recid] = True


                create_b2_list()

    def open_q3():

        nonlocal b2_list_list, b3_list_list, artikel2_list, artikel, debitor, bediener, guest
        nonlocal case_type, bill_name, bill_nr, bill_artnr, counter, balance
        nonlocal artikel0, artikel1, debitor3, bediener1


        nonlocal b2_list, b3_list, artikel2, artikel0, artikel1, debitor3, bediener1
        nonlocal b2_list_list, b3_list_list, artikel2_list

        debitor1 = None
        Debitor1 =  create_buffer("Debitor1",Debitor)

        debitor3_obj_list = {}
        debitor3 = Debitor()
        artikel1 = Artikel()
        bediener1 = Bediener()
        for debitor3.rechnr, debitor3.artnr, debitor3.rgdatum, debitor3.saldo, debitor3.counter, debitor3._recid, debitor3.zahlkonto, debitor3.vesrdep, artikel1.artnr, artikel1.bezeich, artikel1._recid, bediener1.userinit, bediener1._recid in db_session.query(Debitor3.rechnr, Debitor3.artnr, Debitor3.rgdatum, Debitor3.saldo, Debitor3.counter, Debitor3._recid, Debitor3.zahlkonto, Debitor3.vesrdep, Artikel1.artnr, Artikel1.bezeich, Artikel1._recid, Bediener1.userinit, Bediener1._recid).join(Artikel1,(Artikel1.departement == 0) & (Artikel1.artnr == Debitor3.zahlkonto)).join(Bediener1,(Bediener1.nr == Debitor3.bediener_nr)).filter(
                 (Debitor3.counter == counter) & (Debitor3.zahlkonto > 0)).order_by(Debitor3.rgdatum, Debitor3.zahlkonto).all():
            if debitor3_obj_list.get(debitor3._recid):
                continue
            else:
                debitor3_obj_list[debitor3._recid] = True


            create_b3_list()

        for artikel in db_session.query(Artikel).filter(
                 (Artikel.departement == 0) & ((Artikel.artart == 4) | (Artikel.artart == 6)) & (Artikel.activeflag)).order_by(Artikel._recid).all():
            artikel2 = Artikel2()
            artikel2_list.append(artikel2)

            artikel2.artnr = artikel.artnr
            artikel2.bezeich = artikel.bezeich

        for debitor1 in db_session.query(Debitor1).filter(
                 (Debitor1.counter == counter) & (Debitor1.opart == 2) & (Debitor1.zahlkonto > 0)).order_by(Debitor1._recid).all():
            balance =  to_decimal(balance) + to_decimal(debitor1.saldo)


    def create_b3_list():

        nonlocal b2_list_list, b3_list_list, artikel2_list, artikel, debitor, bediener, guest
        nonlocal case_type, bill_name, bill_nr, bill_artnr, counter, balance
        nonlocal artikel0, artikel1, debitor3, bediener1


        nonlocal b2_list, b3_list, artikel2, artikel0, artikel1, debitor3, bediener1
        nonlocal b2_list_list, b3_list_list, artikel2_list


        b3_list = B3_list()
        b3_list_list.append(b3_list)

        b3_list.rgdatum = debitor3.rgdatum
        b3_list.zahlkonto = debitor3.zahlkonto
        b3_list.bezeich = artikel1.bezeich
        b3_list.saldo =  to_decimal(debitor3.saldo)
        b3_list.vesrdep =  to_decimal(debitor3.vesrdep)
        b3_list.userinit = bediener1.userinit


    def create_b2_list():

        nonlocal b2_list_list, b3_list_list, artikel2_list, artikel, debitor, bediener, guest
        nonlocal case_type, bill_name, bill_nr, bill_artnr, counter, balance
        nonlocal artikel0, artikel1, debitor3, bediener1


        nonlocal b2_list, b3_list, artikel2, artikel0, artikel1, debitor3, bediener1
        nonlocal b2_list_list, b3_list_list, artikel2_list


        b2_list = B2_list()
        b2_list_list.append(b2_list)

        b2_list.name = guest.name
        b2_list.vorname1 = guest.vorname1
        b2_list.anrede1 = guest.anrede1
        b2_list.anredefirma = guest.anredefirma
        b2_list.rechnr = debitor.rechnr
        b2_list.artnr = debitor.artnr
        b2_list.bezeich = artikel0.bezeich
        b2_list.rgdatum = debitor.rgdatum
        b2_list.saldo =  to_decimal(debitor.saldo)
        b2_list.counter = debitor.counter

        if debitor:
            disp_guest_debt()


    def disp_guest_debt():

        nonlocal b2_list_list, b3_list_list, artikel2_list, artikel, debitor, bediener, guest
        nonlocal case_type, bill_name, bill_nr, bill_artnr, counter, balance
        nonlocal artikel0, artikel1, debitor3, bediener1


        nonlocal b2_list, b3_list, artikel2, artikel0, artikel1, debitor3, bediener1
        nonlocal b2_list_list, b3_list_list, artikel2_list

        if debitor:
            b2_list.b_resname = guest.name + " " + guest.vorname1 + ", " + guest.anrede1 + guest.anredefirma +\
                    chr_unicode(10) + guest.adresse1 +\
                    chr_unicode(10) + guest.wohnort + " " + guest.plz
            b2_list.b_comments = guest.bemerkung


    if case_type == 2:
        open_q2()

    elif case_type == 3:
        open_q3()

    return generate_output()