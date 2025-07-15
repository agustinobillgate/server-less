#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import Htparam, Debitor, Artikel, Guest, Res_line, Akt_kont

def ar_remainlistbl(from_art:int, to_art:int):

    prepare_cache ([Htparam, Debitor, Artikel, Guest, Res_line, Akt_kont])

    output_list_data = []
    day1:int = 0
    day2:int = 0
    day3:int = 0
    letter1:int = 0
    letter2:int = 0
    letter3:int = 0
    price_decimal:int = 0
    htparam = debitor = artikel = guest = res_line = akt_kont = None

    output_list = None

    output_list_data, Output_list = create_model("Output_list", {"debtrecid":int, "debt_day":int, "str":string})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal output_list_data, day1, day2, day3, letter1, letter2, letter3, price_decimal, htparam, debitor, artikel, guest, res_line, akt_kont
        nonlocal from_art, to_art


        nonlocal output_list
        nonlocal output_list_data

        return {"output-list": output_list_data}

    def create_list():

        nonlocal output_list_data, day1, day2, day3, letter1, letter2, letter3, price_decimal, htparam, debitor, artikel, guest, res_line, akt_kont
        nonlocal from_art, to_art


        nonlocal output_list
        nonlocal output_list_data

        artnr:int = 0
        t_debit:Decimal = to_decimal("0.0")
        tot_debit:Decimal = to_decimal("0.0")
        i:int = 0
        receiver:string = ""
        address1:string = ""
        address2:string = ""
        address3:string = ""
        contact:string = ""
        debtpay = None
        debt_pay:Decimal = to_decimal("0.0")
        outstand:Decimal = to_decimal("0.0")
        debt_day:int = 0
        maildate:string = ""
        periode__stay:string = ""
        Debtpay =  create_buffer("Debtpay",Debitor)
        output_list_data.clear()

        debitor_obj_list = {}
        debitor = Debitor()
        artikel = Artikel()
        guest = Guest()
        for debitor.gastnr, debitor.rgdatum, debitor.rechnr, debitor.counter, debitor.saldo, debitor.versanddat, debitor._recid, debitor.mahnstufe, artikel.bezeich, artikel._recid, guest.gastnr, guest.adresse1, guest.adresse2, guest.adresse3, guest.name, guest.vorname1, guest.anredefirma, guest.anrede1, guest._recid in db_session.query(Debitor.gastnr, Debitor.rgdatum, Debitor.rechnr, Debitor.counter, Debitor.saldo, Debitor.versanddat, Debitor._recid, Debitor.mahnstufe, Artikel.bezeich, Artikel._recid, Guest.gastnr, Guest.adresse1, Guest.adresse2, Guest.adresse3, Guest.name, Guest.vorname1, Guest.anredefirma, Guest.anrede1, Guest._recid).join(Artikel,(Artikel.artnr == Debitor.artnr) & (Artikel.artart == 2) & (Artikel.departement == 0)).join(Guest,(Guest.gastnr == Debitor.gastnr)).filter(
                 (Debitor.zahlkonto == 0) & (Debitor.opart == 0) & (Debitor.artnr >= from_art) & (Debitor.artnr <= to_art)).order_by(Artikel.artnr, Debitor.rgdatum, Debitor.name).all():
            if debitor_obj_list.get(debitor._recid):
                continue
            else:
                debitor_obj_list[debitor._recid] = True

            res_line = get_cache (Res_line, {"gastnr": [(eq, debitor.gastnr)]})

            if res_line:
                periode__stay = to_string(res_line.ankunft) + " - " + to_string(res_line.abreise)

            akt_kont = get_cache (Akt_kont, {"gastnr": [(eq, guest.gastnr)]})

            if akt_kont:
                contact = akt_kont.name
            address1 = guest.adresse1
            address2 = guest.adresse2
            address3 = guest.adresse3
            debt_day = (get_current_date() - debitor.rgdatum).days

            if debt_day > day1:
                receiver = guest.name + ", " + guest.vorname1 + " " + guest.anredefirma + guest.anrede1
                debt_pay =  to_decimal("0")

                for debtpay in db_session.query(Debtpay).filter(
                         (Debtpay.rechnr == debitor.rechnr) & (Debtpay.opart == 1) & (Debtpay.counter == debitor.counter)).order_by(Debtpay._recid).all():
                    debt_pay =  to_decimal(debt_pay) + to_decimal(debtpay.saldo)
                outstand =  to_decimal(debitor.saldo) + to_decimal(debt_pay)
                maildate = ""

                if debitor.versanddat != None:
                    maildate = to_string(debitor.versanddat)
                output_list = Output_list()
                output_list_data.append(output_list)

                output_list.debtrecid = debitor._recid
                output_list.debt_day = debt_day

                if price_decimal == 2:
                    str = to_string(artikel.bezeich, "x(16)") + to_string(debitor.rgdatum) + to_string(debitor.rechnr, ">>>>>>>>9") + to_string(receiver, "x(24)") + to_string(debitor.saldo, "->>,>>>,>>9.99") + to_string(debt_pay, "->>,>>>,>>9.99") + to_string(outstand, "->>,>>>,>>9.99") + to_string(debt_day, ">>>9") + to_string(maildate, "x(8)") + to_string(debitor.mahnstufe, ">9") + to_string(address1, "x(32)") + to_string(address2, "x(32)") + to_string(address3, "x(32)") + to_string(contact, "x(32)") + to_string(periode__stay, "x(20)")
                else:
                    str = to_string(artikel.bezeich, "x(16)") + to_string(debitor.rgdatum) + to_string(debitor.rechnr, ">>>>>>>>9") + to_string(receiver, "x(24)") + to_string(debitor.saldo, "->,>>>,>>>,>>9") + to_string(debt_pay, "->,>>>,>>>,>>9") + to_string(outstand, "->,>>>,>>>,>>9") + to_string(debt_day, ">>>9") + to_string(maildate, "x(8)") + to_string(debitor.mahnstufe, ">9") + to_string(address1, "x(32)") + to_string(address2, "x(32)") + to_string(address3, "x(32)") + to_string(contact, "x(32)") + to_string(periode__stay, "x(20)")


    htparam = get_cache (Htparam, {"paramnr": [(eq, 330)]})
    day1 = htparam.finteger

    htparam = get_cache (Htparam, {"paramnr": [(eq, 331)]})
    day2 = htparam.finteger + day1

    htparam = get_cache (Htparam, {"paramnr": [(eq, 332)]})
    day3 = htparam.finteger + day2

    htparam = get_cache (Htparam, {"paramnr": [(eq, 670)]})
    letter1 = htparam.finteger

    htparam = get_cache (Htparam, {"paramnr": [(eq, 671)]})
    letter2 = htparam.finteger

    htparam = get_cache (Htparam, {"paramnr": [(eq, 388)]})
    letter3 = htparam.finteger

    htparam = get_cache (Htparam, {"paramnr": [(eq, 491)]})
    price_decimal = htparam.finteger
    create_list()

    return generate_output()