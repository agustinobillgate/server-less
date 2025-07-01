#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import L_artikel, L_order

def insert_po_return_ofbl(rec_id:int, l_order_anzahl:Decimal, l_order_einzelpreis:Decimal, disc_list_disc:string, disc_list_disc2:string, disc_list_vat:Decimal, t_amount:Decimal):

    prepare_cache ([L_artikel, L_order])

    amt = to_decimal("0.0")
    l_order_warenwert = to_decimal("0.0")
    l_order_quality = ""
    l_artikel = l_order = None

    l_art1 = None

    L_art1 = create_buffer("L_art1",L_artikel)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal amt, l_order_warenwert, l_order_quality, l_artikel, l_order
        nonlocal rec_id, l_order_anzahl, l_order_einzelpreis, disc_list_disc, disc_list_disc2, disc_list_vat, t_amount
        nonlocal l_art1


        nonlocal l_art1

        return {"t_amount": t_amount, "amt": amt, "l_order_warenwert": l_order_warenwert, "l_order_quality": l_order_quality}


    l_order = get_cache (L_order, {"_recid": [(eq, rec_id)]})
    pass
    l_order.anzahl =  to_decimal(l_order_anzahl)

    if l_order.flag:
        amt =  to_decimal(l_order.warenwert)
        l_order.warenwert =  to_decimal(to_decimal(l_order_anzahl)) * to_decimal(to_decimal(l_order_einzelpreis)) * to_decimal((1) - to_decimal(to_decimal(disc_list_disc)) / to_decimal(100)) * to_decimal((1) - to_decimal(to_decimal(disc_list_disc2)) / to_decimal(100)) * to_decimal((1) + to_decimal(to_decimal(disc_list_vat)) / to_decimal(100))
        l_order.quality = to_string(to_decimal(disc_list_disc) , "99.99 ") + to_string(to_decimal(disc_list_vat) , "99.99") + to_string(to_decimal(disc_list_disc) , " 99.99")
        t_amount =  to_decimal(t_amount) - to_decimal(amt) + to_decimal(l_order.warenwert)
        l_order_warenwert =  to_decimal(l_order.warenwert)
        l_order_quality = l_order.quality
    else:
        amt =  to_decimal(l_order.warenwert)

        l_art1 = get_cache (L_artikel, {"artnr": [(eq, l_order.artnr)]})
        l_order.warenwert =  to_decimal(to_decimal(l_order_anzahl)) * to_decimal(to_decimal(l_order_einzelpreis)) * to_decimal((1) - to_decimal(to_decimal(disc_list_disc)) / to_decimal(100)) * to_decimal((1) - to_decimal(to_decimal(disc_list_disc2)) / to_decimal(100)) * to_decimal((1) + to_decimal(to_decimal(disc_list_vat)) / to_decimal(100)) * to_decimal(l_art1.lief_einheit)
        l_order.quality = to_string(to_decimal(disc_list_disc) , "99.99 ") + to_string(to_decimal(disc_list_vat) , "99.99") + to_string(to_decimal(disc_list_disc) , " 99.99")
        t_amount =  to_decimal(t_amount) - to_decimal(amt) + to_decimal(l_order.warenwert)
        l_order_warenwert =  to_decimal(l_order.warenwert)
        l_order_quality = l_order.quality
    pass

    return generate_output()