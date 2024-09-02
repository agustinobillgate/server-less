from functions.additional_functions import *
import decimal
from models import Htparam, Debitor, Artikel, Guest, Res_line, Akt_kont

def ar_remainlistbl(from_art:int, to_art:int):
    output_list_list = []
    day1:int = 0
    day2:int = 0
    day3:int = 0
    letter1:int = 0
    letter2:int = 0
    letter3:int = 0
    price_decimal:int = 0
    htparam = debitor = artikel = guest = res_line = akt_kont = None

    output_list = debtpay = None

    output_list_list, Output_list = create_model("Output_list", {"debtrecid":int, "debt_day":int, "str":str})

    Debtpay = Debitor

    db_session = local_storage.db_session

    def generate_output():
        nonlocal output_list_list, day1, day2, day3, letter1, letter2, letter3, price_decimal, htparam, debitor, artikel, guest, res_line, akt_kont
        nonlocal debtpay


        nonlocal output_list, debtpay
        nonlocal output_list_list
        return {"output-list": output_list_list}

    def create_list():

        nonlocal output_list_list, day1, day2, day3, letter1, letter2, letter3, price_decimal, htparam, debitor, artikel, guest, res_line, akt_kont
        nonlocal debtpay


        nonlocal output_list, debtpay
        nonlocal output_list_list

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
        output_list_list.clear()

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
                output_list = Output_list()
                output_list_list.append(output_list)

                output_list.debtrecid = debitor._recid
                output_list.debt_day = debt_day

                if price_decimal == 2:
                    STR = to_string(artikel.bezeich, "x(16)") + to_string(debitor.rgdatum) + to_string(debitor.rechnr, ">>>>>>>>9") + to_string(receiver, "x(24)") + to_string(debitor.saldo, "->>,>>>,>>9.99") + to_string(debt_pay, "->>,>>>,>>9.99") + to_string(outstand, "->>,>>>,>>9.99") + to_string(debt_day, ">>>9") + to_string(maildate, "x(8)") + to_string(debitor.mahnstufe, ">9") + to_string(address1, "x(32)") + to_string(address2, "x(32)") + to_string(address3, "x(32)") + to_string(contact, "x(32)") + to_string(periode__stay, "x(20)")
                else:
                    STR = to_string(artikel.bezeich, "x(16)") + to_string(debitor.rgdatum) + to_string(debitor.rechnr, ">>>>>>>>9") + to_string(receiver, "x(24)") + to_string(debitor.saldo, "->,>>>,>>>,>>9") + to_string(debt_pay, "->,>>>,>>>,>>9") + to_string(outstand, "->,>>>,>>>,>>9") + to_string(debt_day, ">>>9") + to_string(maildate, "x(8)") + to_string(debitor.mahnstufe, ">9") + to_string(address1, "x(32)") + to_string(address2, "x(32)") + to_string(address3, "x(32)") + to_string(contact, "x(32)") + to_string(periode__stay, "x(20)")

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