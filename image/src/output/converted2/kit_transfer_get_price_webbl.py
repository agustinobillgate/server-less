#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from functions.htplogic import htplogic
from datetime import date
from functions.htpdec import htpdec
from models import H_artikel, Paramtext, Artikel

def kit_transfer_get_price_webbl(billart:int, curr_dept:int, qty:int, double_currency:bool, exchg_rate:Decimal, price_decimal:int, price:Decimal):

    prepare_cache ([H_artikel, Paramtext])

    amount = to_decimal("0.0")
    amount_foreign = to_decimal("0.0")
    p_253 = False
    i:int = 0
    n:int = 0
    h_artikel = paramtext = artikel = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal amount, amount_foreign, p_253, i, n, h_artikel, paramtext, artikel
        nonlocal billart, curr_dept, qty, double_currency, exchg_rate, price_decimal, price

        return {"price": price, "amount": amount, "amount_foreign": amount_foreign, "p_253": p_253}

    def calculate_amount():

        nonlocal amount, amount_foreign, p_253, i, n, h_artikel, paramtext, artikel
        nonlocal billart, curr_dept, qty, double_currency, exchg_rate, price_decimal, price

        if double_currency:
            amount_foreign =  to_decimal(price) * to_decimal(qty)
            amount =  to_decimal(price) * to_decimal(exchg_rate) * to_decimal(qty)
            amount =  to_decimal(round (amount , price_decimal))
        else:

            if h_artikel.artart == 0:

                artikel = get_cache (Artikel, {"artnr": [(eq, h_artikel.artnrfront)],"departement": [(eq, h_artikel.departement)]})

                if artikel and artikel.pricetab:
                    amount_foreign =  to_decimal(price) * to_decimal(qty)
                    price =  to_decimal(price) * to_decimal(exchg_rate)
                    amount =  to_decimal(price) * to_decimal(qty)
                    amount =  to_decimal(round (amount , price_decimal))
                else:
                    amount =  to_decimal(price) * to_decimal(qty)
                    amount = to_decimal(round(amount , price_decimal))
            else:
                amount =  to_decimal(price) * to_decimal(qty)
                amount =  to_decimal(round (amount , price_decimal))


    def update_bill(h_artart:int, h_artnrfront:int):

        nonlocal amount, amount_foreign, p_253, i, n, h_artikel, paramtext, artikel
        nonlocal billart, curr_dept, qty, double_currency, exchg_rate, price_decimal, price

        fr_art = None
        h_mwst:Decimal = to_decimal("0.0")
        h_service:Decimal = to_decimal("0.0")
        h_mwst_foreign:Decimal = to_decimal("0.0")
        h_service_foreign:Decimal = to_decimal("0.0")
        closed:bool = False
        p_135:bool = False
        p_134:bool = False
        p_479:bool = False
        unit_price:Decimal = to_decimal("0.0")
        tax:Decimal = to_decimal("0.0")
        serv:Decimal = to_decimal("0.0")
        sysdate:date = None
        zeit:int = 0
        f_dec:Decimal = to_decimal("0.0")
        Fr_art =  create_buffer("Fr_art",Artikel)
        h_service =  to_decimal("0")
        h_mwst =  to_decimal("0")
        h_service_foreign =  to_decimal("0")
        h_mwst_foreign =  to_decimal("0")
        unit_price =  to_decimal(price)


        p_135 = get_output(htplogic(135))
        p_134 = get_output(htplogic(134))
        p_479 = get_output(htplogic(479))

        if not p_135 and h_artart == 0 and h_artikel.service_code != 0:
            f_dec = get_output(htpdec(h_artikel.service_code))

            if f_dec != 0:
                serv =  to_decimal(f_dec) / to_decimal("100")
                h_service =  to_decimal(unit_price) * to_decimal(f_dec) / to_decimal("100")
                h_service_foreign =  to_decimal(round (h_service , 2))

                if double_currency:
                    h_service =  to_decimal(round (h_service) * to_decimal(exchg_rate , 2))
                else:
                    h_service =  to_decimal(round (h_service , 2))

            if not p_134 and h_artart == 0 and h_artikel.mwst_code != 0:
                f_dec = get_output(htpdec(h_artikel.mwst_code))

                if f_dec != 0:
                    tax =  to_decimal(f_dec) / to_decimal("100")
                    h_mwst =  to_decimal(f_dec)

                    if p_479:
                        tax =  to_decimal(tax) * to_decimal((1) + to_decimal(serv))
                        h_mwst =  to_decimal(unit_price) * to_decimal(tax)
                    else:
                        h_mwst =  to_decimal(h_mwst) * to_decimal(unit_price) / to_decimal("100")
                    h_mwst_foreign =  to_decimal(round (h_mwst , 2))

                    if double_currency:
                        h_mwst =  to_decimal(tax) * to_decimal(unit_price) * to_decimal(exchg_rate)
                        h_mwst =  to_decimal(round (h_mwst , 2))
                    else:
                        h_mwst =  to_decimal(round (h_mwst , 2))
        amount =  to_decimal(amount) + to_decimal((h_service) + to_decimal(h_mwst)) * to_decimal(qty)
        amount =  to_decimal(round (amount , price_decimal))
        amount_foreign =  to_decimal(amount_foreign) + to_decimal((h_service_foreign) + to_decimal(h_mwst_foreign)) * to_decimal(qty)


    p_253 = get_output(htplogic(253))

    h_artikel = db_session.query(H_artikel).filter(
             (H_artikel.artnr == billart) & (H_artikel.departement == curr_dept) & (H_artikel.activeflag) & (H_artikel.artart == 0)).first()

    if h_artikel and not p_253:

        if price == h_artikel.epreis1:
            price =  to_decimal(h_artikel.epreis1)

            paramtext = get_cache (Paramtext, {"txtnr": [(eq, (10000 + curr_dept))]})

            if paramtext:
                i = round((get_current_time_in_seconds() / 3600 - 0.5) , 0)

                if i <= 0:
                    i = 24
                n = to_int(substring(paramtext.ptexte, i - 1, 1))

                if n == 2:
                    price =  to_decimal(h_artikel.epreis2)

        if price != 0 and h_artikel.prozent != 0:
            calculate_amount()
            update_bill(h_artikel.artart, h_artikel.artnrfront)

    return generate_output()