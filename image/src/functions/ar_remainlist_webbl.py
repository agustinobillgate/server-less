from functions.additional_functions import *
import decimal
from models import Htparam, Debitor, Artikel, Guest, Res_line, Akt_kont

def ar_remainlist_webbl(from_art:int, to_art:int):
    ar_remainderlist_list = []
    day1:int = 0
    day2:int = 0
    day3:int = 0
    letter1:int = 0
    letter2:int = 0
    letter3:int = 0
    price_decimal:int = 0
    htparam = debitor = artikel = guest = res_line = akt_kont = None

    ar_remainderlist = debtpay = None

    ar_remainderlist_list, Ar_remainderlist = create_model("Ar_remainderlist", {"debtrecid":int, "debt_day":int, "descrip":str, "bill_date":str, "bill_no":str, "bill_receive":str, "debt_amount":str, "paid_amount":str, "oustanding":str, "days":str, "last_print":str, "level":str, "address1":str, "address2":str, "address3":str, "contact":str, "periode_stay":str})

    Debtpay = Debitor

    db_session = local_storage.db_session

    def generate_output():
        nonlocal ar_remainderlist_list, day1, day2, day3, letter1, letter2, letter3, price_decimal, htparam, debitor, artikel, guest, res_line, akt_kont
        nonlocal debtpay


        nonlocal ar_remainderlist, debtpay
        nonlocal ar_remainderlist_list
        return {"ar-remainderlist": ar_remainderlist_list}

    def create_list():

        nonlocal ar_remainderlist_list, day1, day2, day3, letter1, letter2, letter3, price_decimal, htparam, debitor, artikel, guest, res_line, akt_kont
        nonlocal debtpay


        nonlocal ar_remainderlist, debtpay
        nonlocal ar_remainderlist_list

        artnr:int = 0
        t_debit:decimal = 0
        tot_debit:decimal = 0
        i:int = 0
        receiver:str = ""
        address1:str = ""
        address2:str = ""
        address3:str = ""
        contact:str = ""
        debt_pay:decimal = 0
        outstand:decimal = 0
        debt_day:int = 0
        maildate:str = ""
        periode__stay:str = ""
        Debtpay = Debitor
        ar_remainderlist_list.clear()

        debitor_obj_list = []
        for debitor, artikel, guest in db_session.query(Debitor, Artikel, Guest).join(Artikel,(Artikel.artnr == Debitor.artnr) &  (Artikel.artart == 2) &  (Artikel.departement == 0)).join(Guest,(Guest.gastnr == Debitor.gastnr)).filter(
                (Debitor.zahlkonto == 0) &  (Debitor.opart == 0) &  (Debitor.artnr >= from_art) &  (Debitor.artnr <= to_art)).all():
            if debitor._recid in debitor_obj_list:
                continue
            else:
                debitor_obj_list.append(debitor._recid)

            res_line = db_session.query(Res_line).filter(
                    (Res_line.gastnr == debitor.gastnr)).first()

            if res_line:
                periode__stay = to_string(res_line.ankunft) + " - " + to_string(res_line.abreise)

            akt_kont = db_session.query(Akt_kont).filter(
                    (akt_kont.gastnr == guest.gastnr)).first()

            if akt_kont:
                contact = akt_kont.name
            address1 = guest.adresse1
            address2 = guest.adresse2
            address3 = guest.adresse3
            debt_day = get_current_date() - debitor.rgdatum

            if debt_day > day1:
                receiver = guest.name + ", " + guest.vorname1 + " " + guest.anredefirma + guest.anrede1
                debt_pay = 0

                for debtpay in db_session.query(Debtpay).filter(
                        (Debtpay.rechnr == debitor.rechnr) &  (Debtpay.opart == 1) &  (Debtpay.counter == debitor.counter)).all():
                    debt_pay = debt_pay + debtpay.saldo
                outstand = debitor.saldo + debt_pay
                maildate = ""

                if debitor.versanddat != None:
                    maildate = to_string(debitor.versanddat)
                ar_remainderlist = Ar_remainderlist()
                ar_remainderlist_list.append(ar_remainderlist)

                ar_remainderlist.debtrecid = debitor._recid
                ar_remainderlist.debt_day = debt_day

                if price_decimal == 2:
                    ar_remainderlist.descrip = artikel.bezeich
                    ar_remainderlist.bill_date = to_string(debitor.rgdatum, "99/99/99")
                    ar_remainderlist.bill_no = to_string(debitor.rechnr, ">>>>>>>>9")
                    ar_remainderlist.bill_receive = receiver
                    ar_remainderlist.debt_amount = to_string(debitor.saldo, "->>,>>>,>>>,>>>,>>9.99")
                    ar_remainderlist.paid_amount = to_string(debt_pay, "->>,>>>,>>>,>>>,>>9.99")
                    ar_remainderlist.oustanding = to_string(outstand, "->>,>>>,>>>,>>>,>>9.99")
                    ar_remainderlist.days = to_string(debt_day, ">>>>9")
                    ar_remainderlist.last_print = to_string(maildate, "99/99/99")
                    ar_remainderlist.level = to_string(debitor.mahnstufe, ">>9")
                    ar_remainderlist.address1 = address1
                    ar_remainderlist.address2 = address2
                    ar_remainderlist.address3 = address3
                    ar_remainderlist.contact = contact
                    ar_remainderlist.periode_stay = periode__stay


                else:
                    ar_remainderlist.descrip = artikel.bezeich
                    ar_remainderlist.bill_date = to_string(debitor.rgdatum, "99/99/99")
                    ar_remainderlist.bill_no = to_string(debitor.rechnr, ">>>>>>>>9")
                    ar_remainderlist.bill_receive = receiver
                    ar_remainderlist.debt_amount = to_string(debitor.saldo, "->,>>>,>>>,>>>,>>>,>>9")
                    ar_remainderlist.paid_amount = to_string(debt_pay, "->,>>>,>>>,>>>,>>>,>>9")
                    ar_remainderlist.oustanding = to_string(outstand, "->,>>>,>>>,>>>,>>>,>>9")
                    ar_remainderlist.days = to_string(debt_day, ">>>>9")
                    ar_remainderlist.last_print = to_string(maildate, "99/99/99")
                    ar_remainderlist.level = to_string(debitor.mahnstufe, ">>9")
                    ar_remainderlist.address1 = address1
                    ar_remainderlist.address2 = address2
                    ar_remainderlist.address3 = address3
                    ar_remainderlist.contact = contact
                    ar_remainderlist.periode_stay = periode__stay

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 330)).first()
    day1 = htparam.finteger

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 331)).first()
    day2 = htparam.finteger + day1

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 332)).first()
    day3 = htparam.finteger + day2

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 670)).first()
    letter1 = htparam.finteger

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 671)).first()
    letter2 = htparam.finteger

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 388)).first()
    letter3 = htparam.finteger

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 491)).first()
    price_decimal = htparam.finteger
    create_list()

    return generate_output()