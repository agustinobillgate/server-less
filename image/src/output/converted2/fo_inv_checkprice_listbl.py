from functions.additional_functions import *
import decimal
from functions.fo_invoice_check_pricebl import fo_invoice_check_pricebl
from models import Artikel

def fo_inv_checkprice_listbl(pvilanguage:int, double_currency:bool, price:decimal, p_1086:decimal, billart:int, curr_department:int, balance:decimal, balance_foreign:decimal, price_decimal:int, exchg_rate:decimal):
    do_it = True
    msgint = 0
    l_price = to_decimal("0.0")
    lvcarea:str = "fo-inv-check-price"
    answer:bool = False
    max_price:decimal = to_decimal("0.0")
    artikel = None

    t_artikel = None

    T_artikel = create_buffer("T_artikel",Artikel)

    db_session = local_storage.db_session

    def generate_output():
        nonlocal do_it, msgint, l_price, lvcarea, answer, max_price, artikel
        nonlocal pvilanguage, double_currency, price, p_1086, billart, curr_department, balance, balance_foreign, price_decimal, exchg_rate
        nonlocal t_artikel


        nonlocal t_artikel
        return {"do_it": do_it, "msgint": msgint, "l_price": l_price}


    t_artikel = db_session.query(T_artikel).filter(
             (T_artikel.artnr == billart) & (T_artikel.departement == curr_department)).first()

    if t_artikel:
        max_price =  to_decimal(p_1086)

        if price == 0:
            do_it = False

            return generate_output()

        if double_currency and ((price >= 100) or (price <= - 100)) and t_artikel.pricetab:

            if (t_artikel.artart == 2 or t_artikel.artart == 6 or t_artikel.artart == 7) and balance_foreign != 0:
                l_price = to_decimal(round(price * balance / balance_foreign , price_decimal))


            else:
                l_price = to_decimal(round(price * exchg_rate , price_decimal))


            msgint = 1

        if not double_currency and max_price != 0:

            if price > 0:
                l_price =  to_decimal(price)
            else:
                l_price =  - to_decimal(price)

            if t_artikel.pricetab:
                l_price = get_output(fo_invoice_check_pricebl(l_price, t_artikel.artnr, t_artikel.departement))

            if l_price >= max_price:
                msgint = 2
                do_it = False

    return generate_output()