from functions.additional_functions import *
import decimal
from datetime import date
from sqlalchemy import func
from functions.calc_servtaxesbl import calc_servtaxesbl
import re
from models import Gl_acct, Artikel, Umsatz, Billjournal, Htparam, Bill, Billhis, Reservation

def prepare_gl_detailfobl(pvilanguage:int, fibu:str, bemerk:str, from_date:date):
    t_gl_acct_list = []
    s_list_list = []
    artnr:int = 0
    dept:int = 0
    lvcarea:str = "gl_detailFO"
    gl_acct = artikel = umsatz = billjournal = htparam = bill = billhis = reservation = None

    s_list = t_gl_acct = None

    s_list_list, S_list = create_model("S_list", {"datum":date, "departement":int, "artnr":int, "artart":int, "bezeich":str, "betrag":decimal, "service":decimal, "vat":decimal, "nett":decimal})
    t_gl_acct_list, T_gl_acct = create_model_like(Gl_acct)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal t_gl_acct_list, s_list_list, artnr, dept, lvcarea, gl_acct, artikel, umsatz, billjournal, htparam, bill, billhis, reservation


        nonlocal s_list, t_gl_acct
        nonlocal s_list_list, t_gl_acct_list
        return {"t-gl-acct": t_gl_acct_list, "s-list": s_list_list}

    def disp_it():

        nonlocal t_gl_acct_list, s_list_list, artnr, dept, lvcarea, gl_acct, artikel, umsatz, billjournal, htparam, bill, billhis, reservation


        nonlocal s_list, t_gl_acct
        nonlocal s_list_list, t_gl_acct_list

        serv:decimal = 0
        vat:decimal = 0
        vat2:decimal = 0
        wert:decimal = 0
        fact:decimal = 0
        serv_vat:bool = False
        price_decimal:int = 0
        dept = to_int(entry(2, bemerk, ";"))
        artnr = to_int(entry(3, bemerk, ";"))

        artikel = db_session.query(Artikel).filter(
                (Artikel.artnr == artnr) &  (Artikel.departement == dept)).first()

        if not artikel:

            return

        umsatz = db_session.query(Umsatz).filter(
                (Umsatz.artnr == artikel.artnr) &  (Umsatz.departement == artikel.departement) &  (Umsatz.datum == from_date)).first()

        if not umsatz:

            return

        if artikel.artart == 5:

            billjournal = db_session.query(Billjournal).filter(
                    (Billjournal.artnr == artnr) &  (Billjournal.departement == dept) &  (Billjournal.bill_datum == from_date) &  (Billjournal.anzahl != 0)).first()

            if not billjournal:
                return
            disp_deposit()

            return

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 491)).first()
        price_decimal = htparam.finteger

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 479)).first()
        serv_vat = htparam.flogical
        serv, vat, vat2, fact = get_output(calc_servtaxesbl(1, artikel.artnr, artikel.departement, umsatz.datum))
        vat = vat + vat2


        wert = umsatz.betrag / fact
        s_list = S_list()
        s_list_list.append(s_list)

        s_list.artnr = artikel.artnr
        s_list.departement = artikel.departement
        s_list.artart = artikel.artart
        s_list.bezeich = artikel.bezeich
        s_list.datum = umsatz.datum
        s_list.betrag = umsatz.betrag
        s_list.service = round(wert * serv, price_decimal)
        s_list.vat = round(wert * vat, price_decimal)
        s_list.nett = umsatz.betrag - s_list.service - s_list.vat

    def disp_deposit():

        nonlocal t_gl_acct_list, s_list_list, artnr, dept, lvcarea, gl_acct, artikel, umsatz, billjournal, htparam, bill, billhis, reservation


        nonlocal s_list, t_gl_acct
        nonlocal s_list_list, t_gl_acct_list

        serv:decimal = 0
        vat:decimal = 0
        vat2:decimal = 0
        wert:decimal = 0
        fact:decimal = 1
        serv_vat:bool = False
        price_decimal:int = 0
        n:int = 0
        m:int = 0
        resnr:int = 0
        s:str = ""

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 491)).first()
        price_decimal = htparam.finteger

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 479)).first()
        serv_vat = htparam.flogical

        for billjournal in db_session.query(Billjournal).filter(
                (Billjournal.artnr == artnr) &  (Billjournal.departement == dept) &  (Billjournal.bill_datum == from_date) &  (Billjournal.anzahl != 0)).all():
            wert = billjournal.betrag / fact
            s_list = S_list()
            s_list_list.append(s_list)

            s_list.artnr = artikel.artnr
            s_list.departement = artikel.departement
            s_list.artart = artikel.artart
            s_list.bezeich = billjournal.bezeich
            s_list.datum = billjournal.bill_datum
            s_list.betrag = billjournal.betrag
            s_list.service = round(wert * serv, price_decimal)
            s_list.vat = round(wert * vat, price_decimal)
            s_list.nett = billjournal.betrag - s_list.service - s_list.vat

            if billjournal.rechnr != 0:
                s_list.bezeich = s_list.bezeich + "; " + translateExtended ("BillNo", lvcarea, "") + " " + to_string(billjournal.rechnr)

                bill = db_session.query(Bill).filter(
                        (Bill.rechnr == billjournal.rechnr)).first()

                if bill:
                    s_list.bezeich = s_list.bezeich + "; " + bill.name
                else:

                    billhis = db_session.query(Billhis).filter(
                            (Billhis.rechnr == billjournal.rechnr)).first()

                    if billhis:
                        s_list.bezeich = s_list.bezeich + "; " + billhis.name

            elif re.match(".*#.*",billjournal.bezeich):
                s = billjournal.bezeich
                m = 0
                for n in range(1,len(s)  + 1) :

                    if substring(s, n - 1, 1) == "#":
                        m = n
                        s = substring(s, m - 1)
                        break

                if m > 0:
                    resnr = to_int(substring(entry(0, s, " ") , 1))

                if resnr > 0:

                    reservation = db_session.query(Reservation).filter(
                            (Reservation.resnr == resnr)).first()

                    if reservation:
                        s_list.bezeich = s_list.bezeich + "; " + reservation.name


    gl_acct = db_session.query(Gl_acct).filter(
            (func.lower(Gl_acct.fibukonto) == (fibu).lower())).first()
    t_gl_acct = T_gl_acct()
    t_gl_acct_list.append(t_gl_acct)

    buffer_copy(gl_acct, t_gl_acct)
    disp_it()

    return generate_output()