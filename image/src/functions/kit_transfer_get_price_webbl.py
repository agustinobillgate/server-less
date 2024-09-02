from functions.additional_functions import *
import decimal
from functions.htplogic import htplogic
from datetime import date
from functions.htpdec import htpdec
from models import H_artikel, Paramtext, Artikel

def kit_transfer_get_price_webbl(billart:int, curr_dept:int, qty:int, double_currency:bool, exchg_rate:decimal, price_decimal:int, price:decimal):
    amount = 0
    amount_foreign = 0
    p_253 = False
    i:int = 0
    n:int = 0
    h_artikel = paramtext = artikel = None

    fr_art = None

    Fr_art = Artikel

    db_session = local_storage.db_session

    def generate_output():
        nonlocal amount, amount_foreign, p_253, i, n, h_artikel, paramtext, artikel
        nonlocal fr_art


        nonlocal fr_art
        return {"amount": amount, "amount_foreign": amount_foreign, "p_253": p_253}

    def calculate_amount():

        nonlocal amount, amount_foreign, p_253, i, n, h_artikel, paramtext, artikel
        nonlocal fr_art


        nonlocal fr_art

        if double_currency:
            amount_foreign = price * qty
            amount = price * exchg_rate * qty
            amount = round (amount, price_decimal)
        else:

            if h_artikel.artart == 0:

                artikel = db_session.query(Artikel).filter(
                        (Artikel.artnr == h_Artikel.artnrfront) &  (Artikel.departement == h_Artikel.departement)).first()

                if artikel and artikel.pricetab:
                    amount_foreign = price * qty
                    price = price * exchg_rate
                    amount = price * qty
                    amount = round (amount, price_decimal)
                else:
                    amount = price * qty
                    amount = round(amount, price_decimal)
            else:
                amount = price * qty
                amount = round (amount, price_decimal)

    def update_bill(h_artart:int, h_artnrfront:int):

        nonlocal amount, amount_foreign, p_253, i, n, h_artikel, paramtext, artikel
        nonlocal fr_art


        nonlocal fr_art

        h_mwst:decimal = 0
        h_service:decimal = 0
        h_mwst_foreign:decimal = 0
        h_service_foreign:decimal = 0
        closed:bool = False
        p_135:bool = False
        p_134:bool = False
        p_479:bool = False
        unit_price:decimal = 0
        tax:decimal = 0
        serv:decimal = 0
        sysdate:date = None
        zeit:int = 0
        f_dec:decimal = 0
        Fr_art = Artikel
        h_service = 0
        h_mwst = 0
        h_service_foreign = 0
        h_mwst_foreign = 0
        unit_price = price


        p_135 = get_output(htplogic(135))
        p_134 = get_output(htplogic(134))
        p_479 = get_output(htplogic(479))

        if not p_135 and h_artart == 0 and h_artikel.service_code != 0:
            f_dec = get_output(htpdec(h_artikel.service_code))

            if f_dec != 0:
                serv = f_dec / 100
                h_service = unit_price * f_dec / 100
                h_service_foreign = round (h_service, 2)

                if double_currency:
                    h_service = round (h_service * exchg_rate, 2)
                else:
                    h_service = round (h_service, 2)

            if not p_134 and h_artart == 0 and h_artikel.mwst_code != 0:
                f_dec = get_output(htpdec(h_artikel.mwst_code))

                if f_dec != 0:
                    tax = f_dec / 100
                    h_mwst = f_dec

                    if p_479:
                        tax = tax * (1 + serv)
                        h_mwst = unit_price * tax
                    else:
                        h_mwst = h_mwst * unit_price / 100
                    h_mwst_foreign = round (h_mwst, 2)

                    if double_currency:
                        h_mwst = tax * unit_price * exchg_rate
                        h_mwst = round (h_mwst, 2)
                    else:
                        h_mwst = round (h_mwst, 2)
        amount = amount + (h_service + h_mwst) * qty
        amount = round (amount, price_decimal)
        amount_foreign = amount_foreign + (h_service_foreign + h_mwst_foreign) * qty

    p_253 = get_output(htplogic(253))

    h_artikel = db_session.query(H_artikel).filter(
            (H_artikel.artnr == billart) &  (H_artikel.departement == curr_dept) &  (H_artikel.activeflag) &  (H_artikel.artart == 0)).first()

    if h_artikel and not p_253:

        if price == h_artikel.epreis1:
            price = h_artikel.epreis1

            paramtext = db_session.query(Paramtext).filter(
                    (Paramtext.txtnr == (10000 + curr_dept))).first()

            if paramtext:
                i = round((get_current_time_in_seconds() / 3600 - 0.5) , 0)

                if i <= 0:
                    i = 24
                n = to_int(substring(paramtext.ptexte, i - 1, 1))

                if n == 2:
                    price = h_artikel.epreis2

        if price != 0 and h_artikel.prozent != 0:
            calculate_amount()
            update_bill(h_artikel.artart, h_artikel.artnrfront)

    return generate_output()