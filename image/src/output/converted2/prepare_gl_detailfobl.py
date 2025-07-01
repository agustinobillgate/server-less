#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from functions.calc_servtaxesbl import calc_servtaxesbl
from models import Gl_acct, Artikel, Umsatz, Billjournal, Htparam, Bill, Billhis, Reservation

def prepare_gl_detailfobl(pvilanguage:int, fibu:string, bemerk:string, from_date:date):

    prepare_cache ([Artikel, Umsatz, Billjournal, Htparam, Bill, Billhis, Reservation])

    t_gl_acct_list = []
    s_list_list = []
    artnr:int = 0
    dept:int = 0
    lvcarea:string = "gl-detailFO"
    gl_acct = artikel = umsatz = billjournal = htparam = bill = billhis = reservation = None

    s_list = t_gl_acct = None

    s_list_list, S_list = create_model("S_list", {"datum":date, "departement":int, "artnr":int, "artart":int, "bezeich":string, "betrag":Decimal, "service":Decimal, "vat":Decimal, "nett":Decimal})
    t_gl_acct_list, T_gl_acct = create_model_like(Gl_acct)

    db_session = local_storage.db_session

    def generate_output():
        nonlocal t_gl_acct_list, s_list_list, artnr, dept, lvcarea, gl_acct, artikel, umsatz, billjournal, htparam, bill, billhis, reservation
        nonlocal pvilanguage, fibu, bemerk, from_date


        nonlocal s_list, t_gl_acct
        nonlocal s_list_list, t_gl_acct_list

        return {"t-gl-acct": t_gl_acct_list, "s-list": s_list_list}

    def disp_it():

        nonlocal t_gl_acct_list, s_list_list, artnr, dept, lvcarea, gl_acct, artikel, umsatz, billjournal, htparam, bill, billhis, reservation
        nonlocal pvilanguage, fibu, bemerk, from_date


        nonlocal s_list, t_gl_acct
        nonlocal s_list_list, t_gl_acct_list

        serv:Decimal = to_decimal("0.0")
        vat:Decimal = to_decimal("0.0")
        vat2:Decimal = to_decimal("0.0")
        wert:Decimal = to_decimal("0.0")
        fact:Decimal = to_decimal("0.0")
        serv_vat:bool = False
        price_decimal:int = 0
        dept = to_int(entry(2, bemerk, ";"))
        artnr = to_int(entry(3, bemerk, ";"))

        artikel = get_cache (Artikel, {"artnr": [(eq, artnr)],"departement": [(eq, dept)]})

        if not artikel:

            return

        umsatz = get_cache (Umsatz, {"artnr": [(eq, artikel.artnr)],"departement": [(eq, artikel.departement)],"datum": [(eq, from_date)]})

        if not umsatz:

            return

        if artikel.artart == 5:

            billjournal = get_cache (Billjournal, {"artnr": [(eq, artnr)],"departement": [(eq, dept)],"bill_datum": [(eq, from_date)],"anzahl": [(ne, 0)]})

            if not billjournal:
                return
            disp_deposit()

            return

        htparam = get_cache (Htparam, {"paramnr": [(eq, 491)]})
        price_decimal = htparam.finteger

        htparam = get_cache (Htparam, {"paramnr": [(eq, 479)]})
        serv_vat = htparam.flogical
        serv, vat, vat2, fact = get_output(calc_servtaxesbl(1, artikel.artnr, artikel.departement, umsatz.datum))
        vat =  to_decimal(vat) + to_decimal(vat2)


        wert =  to_decimal(umsatz.betrag) / to_decimal(fact)
        s_list = S_list()
        s_list_list.append(s_list)

        s_list.artnr = artikel.artnr
        s_list.departement = artikel.departement
        s_list.artart = artikel.artart
        s_list.bezeich = artikel.bezeich
        s_list.datum = umsatz.datum
        s_list.betrag =  to_decimal(umsatz.betrag)
        s_list.service = to_decimal(round(wert * serv , price_decimal))
        s_list.vat = to_decimal(round(wert * vat , price_decimal))
        s_list.nett =  to_decimal(umsatz.betrag) - to_decimal(s_list.service) - to_decimal(s_list.vat)


    def disp_deposit():

        nonlocal t_gl_acct_list, s_list_list, artnr, dept, lvcarea, gl_acct, artikel, umsatz, billjournal, htparam, bill, billhis, reservation
        nonlocal pvilanguage, fibu, bemerk, from_date


        nonlocal s_list, t_gl_acct
        nonlocal s_list_list, t_gl_acct_list

        serv:Decimal = to_decimal("0.0")
        vat:Decimal = to_decimal("0.0")
        vat2:Decimal = to_decimal("0.0")
        wert:Decimal = to_decimal("0.0")
        fact:Decimal = 1
        serv_vat:bool = False
        price_decimal:int = 0
        n:int = 0
        m:int = 0
        resnr:int = 0
        s:string = ""

        htparam = get_cache (Htparam, {"paramnr": [(eq, 491)]})
        price_decimal = htparam.finteger

        htparam = get_cache (Htparam, {"paramnr": [(eq, 479)]})
        serv_vat = htparam.flogical

        for billjournal in db_session.query(Billjournal).filter(
                 (Billjournal.artnr == artnr) & (Billjournal.departement == dept) & (Billjournal.bill_datum == from_date) & (Billjournal.anzahl != 0)).order_by(Billjournal.zeit).all():
            wert =  to_decimal(billjournal.betrag) / to_decimal(fact)
            s_list = S_list()
            s_list_list.append(s_list)

            s_list.artnr = artikel.artnr
            s_list.departement = artikel.departement
            s_list.artart = artikel.artart
            s_list.bezeich = billjournal.bezeich
            s_list.datum = billjournal.bill_datum
            s_list.betrag =  to_decimal(billjournal.betrag)
            s_list.service = to_decimal(round(wert * serv , price_decimal))
            s_list.vat = to_decimal(round(wert * vat , price_decimal))
            s_list.nett =  to_decimal(billjournal.betrag) - to_decimal(s_list.service) - to_decimal(s_list.vat)

            if billjournal.rechnr != 0:
                s_list.bezeich = s_list.bezeich + "; " + translateExtended ("BillNo", lvcarea, "") + " " + to_string(billjournal.rechnr)

                bill = get_cache (Bill, {"rechnr": [(eq, billjournal.rechnr)]})

                if bill:
                    s_list.bezeich = s_list.bezeich + "; " + bill.name
                else:

                    billhis = get_cache (Billhis, {"rechnr": [(eq, billjournal.rechnr)]})

                    if billhis:
                        s_list.bezeich = s_list.bezeich + "; " + billhis.name

            elif matches(billjournal.bezeich,r"*#*"):
                s = billjournal.bezeich
                m = 0
                for n in range(1,length(s)  + 1) :

                    if substring(s, n - 1, 1) == ("#").lower() :
                        m = n
                        s = substring(s, m - 1)
                        break

                if m > 0:
                    resnr = to_int(substring(entry(0, s, " ") , 1))

                if resnr > 0:

                    reservation = get_cache (Reservation, {"resnr": [(eq, resnr)]})

                    if reservation:
                        s_list.bezeich = s_list.bezeich + "; " + reservation.name

    gl_acct = get_cache (Gl_acct, {"fibukonto": [(eq, fibu)]})
    t_gl_acct = T_gl_acct()
    t_gl_acct_list.append(t_gl_acct)

    buffer_copy(gl_acct, t_gl_acct)
    disp_it()

    return generate_output()