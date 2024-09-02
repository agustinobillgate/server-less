from functions.additional_functions import *
import decimal
from sqlalchemy import func
from models import Artikel, Debitor, Bediener, Guest

def ar_closepaybl(case_type:int, bill_name:str, bill_nr:int, bill_artnr:int, counter:int, balance:decimal):
    b2_list_list = []
    b3_list_list = []
    artikel2_list = []
    artikel = debitor = bediener = guest = None

    b2_list = b3_list = artikel2 = artikel0 = artikel1 = debitor3 = bediener1 = debitor1 = None

    b2_list_list, B2_list = create_model("B2_list", {"name":str, "vorname1":str, "anrede1":str, "anredefirma":str, "rechnr":int, "artnr":int, "bezeich":str, "rgdatum":date, "saldo":decimal, "counter":int, "b_resname":str, "b_comments":str})
    b3_list_list, B3_list = create_model("B3_list", {"rgdatum":date, "zahlkonto":int, "bezeich":str, "saldo":decimal, "vesrdep":decimal, "userinit":str})
    artikel2_list, Artikel2 = create_model("Artikel2", {"artnr":int, "bezeich":str})

    Artikel0 = Artikel
    Artikel1 = Artikel
    Debitor3 = Debitor
    Bediener1 = Bediener
    Debitor1 = Debitor

    db_session = local_storage.db_session

    def generate_output():
        nonlocal b2_list_list, b3_list_list, artikel2_list, artikel, debitor, bediener, guest
        nonlocal artikel0, artikel1, debitor3, bediener1, debitor1


        nonlocal b2_list, b3_list, artikel2, artikel0, artikel1, debitor3, bediener1, debitor1
        nonlocal b2_list_list, b3_list_list, artikel2_list
        return {"b2-list": b2_list_list, "b3-list": b3_list_list, "artikel2": artikel2_list}

    def open_q2():

        nonlocal b2_list_list, b3_list_list, artikel2_list, artikel, debitor, bediener, guest
        nonlocal artikel0, artikel1, debitor3, bediener1, debitor1


        nonlocal b2_list, b3_list, artikel2, artikel0, artikel1, debitor3, bediener1, debitor1
        nonlocal b2_list_list, b3_list_list, artikel2_list

        curr_rechnr:int = 0
        curr_saldo:decimal = 0
        opart:int = 1
        to_name:str = ""
        Artikel1 = Artikel
        curr_rechnr = 0
        to_name = chr (ord(substring(bill_name, 0, 1)) + 1)

        if bill_nr > 0:

            debitor_obj_list = []
            for debitor, guest, artikel0 in db_session.query(Debitor, Guest, Artikel0).join(Guest,(Guest.gastnr == Debitor.gastnr)).join(Artikel0,(Artikel0.artnr == Debitor.artnr) &  (Artikel0.departement == 0)).filter(
                    (Debitor.artnr == bill_artnr) &  (Debitor.opart == 2) &  (Debitor.rechnr == bill_nr) &  (Debitor.zahlkonto == 0)).all():
                if debitor._recid in debitor_obj_list:
                    continue
                else:
                    debitor_obj_list.append(debitor._recid)


                create_b2_list()

        else:

            debitor_obj_list = []
            for debitor, guest, artikel0 in db_session.query(Debitor, Guest, Artikel0).join(Guest,(Guest.gastnr == Debitor.gastnr)).join(Artikel0,(Artikel0.artnr == Debitor.artnr) &  (Artikel0.departement == 0)).filter(
                    (Debitor.artnr == bill_artnr) &  (Debitor.opart == 2) &  (func.lower(Debitor.name) >= (bill_name).lower()) &  (func.lower(Debitor.name) <= (to_name).lower()) &  (Debitor.zahlkonto == 0)).all():
                if debitor._recid in debitor_obj_list:
                    continue
                else:
                    debitor_obj_list.append(debitor._recid)


                create_b2_list()


    def open_q3():

        nonlocal b2_list_list, b3_list_list, artikel2_list, artikel, debitor, bediener, guest
        nonlocal artikel0, artikel1, debitor3, bediener1, debitor1


        nonlocal b2_list, b3_list, artikel2, artikel0, artikel1, debitor3, bediener1, debitor1
        nonlocal b2_list_list, b3_list_list, artikel2_list


        Debitor1 = Debitor

        debitor3_obj_list = []
        for debitor3, artikel1, bediener1 in db_session.query(Debitor3, Artikel1, Bediener1).join(Artikel1,(Artikel1.departement == 0) &  (Artikel1.artnr == Debitor3.zahlkonto)).join(Bediener1,(Bediener1.nr == Debitor3.bediener_nr)).filter(
                (Debitor3.counter == counter) &  (Debitor3.zahlkonto > 0)).all():
            if debitor3._recid in debitor3_obj_list:
                continue
            else:
                debitor3_obj_list.append(debitor3._recid)


            create_b3_list()

        for artikel in db_session.query(Artikel).filter(
                (Artikel.departement == 0) &  ((Artikel.artart == 4) |  (Artikel.artart == 6)) &  (Artikel.activeflag)).all():
            artikel2 = Artikel2()
            artikel2_list.append(artikel2)

            artikel2.artnr = artikel.artnr
            artikel2.bezeich = artikel.bezeich

        for debitor1 in db_session.query(Debitor1).filter(
                (Debitor1.counter == counter) &  (Debitor1.opart == 2) &  (Debitor1.zahlkonto > 0)).all():
            balance = balance + debitor1.saldo

    def create_b3_list():

        nonlocal b2_list_list, b3_list_list, artikel2_list, artikel, debitor, bediener, guest
        nonlocal artikel0, artikel1, debitor3, bediener1, debitor1


        nonlocal b2_list, b3_list, artikel2, artikel0, artikel1, debitor3, bediener1, debitor1
        nonlocal b2_list_list, b3_list_list, artikel2_list


        b3_list = B3_list()
        b3_list_list.append(b3_list)

        b3_list.rgdatum = debitor3.rgdatum
        b3_list.zahlkonto = debitor3.zahlkonto
        b3_list.bezeich = artikel1.bezeich
        b3_list.saldo = debitor3.saldo
        b3_list.vesrdep = debitor3.vesrdep
        b3_list.userinit = bediener1.userinit

    def create_b2_list():

        nonlocal b2_list_list, b3_list_list, artikel2_list, artikel, debitor, bediener, guest
        nonlocal artikel0, artikel1, debitor3, bediener1, debitor1


        nonlocal b2_list, b3_list, artikel2, artikel0, artikel1, debitor3, bediener1, debitor1
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
        b2_list.saldo = debitor.saldo
        b2_list.counter = debitor.counter

        if debitor:
            disp_guest_debt()

    def disp_guest_debt():

        nonlocal b2_list_list, b3_list_list, artikel2_list, artikel, debitor, bediener, guest
        nonlocal artikel0, artikel1, debitor3, bediener1, debitor1


        nonlocal b2_list, b3_list, artikel2, artikel0, artikel1, debitor3, bediener1, debitor1
        nonlocal b2_list_list, b3_list_list, artikel2_list

        if debitor:
            b2_list.b_resname = guest.name + " " + guest.vorname1 + ", " + guest.anrede1 + guest.anredefirma +\
                    chr (10) + guest.adresse1 +\
                    chr (10) + guest.wohnort + " " + guest.plz
            b2_list.b_comments = guest.bemerk

    if case_type == 2:
        open_q2()

    elif case_type == 3:
        open_q3()

    return generate_output()