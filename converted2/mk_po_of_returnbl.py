from functions.additional_functions import *
import decimal
from models import L_artikel, L_order

def mk_po_of_returnbl(t_amount:decimal, anzahl:decimal, disc_list_disc:decimal, disc_list_disc2:decimal, disc_list_vat:decimal, disc_list_price0:decimal, disc_list_disc_val:decimal, disc_list_disc2_val:decimal, disc_list_vat_val:decimal, rec_id:int):
    t_l_order_quality = ""
    t_l_order_einzelpreis = to_decimal("0.0")
    t_l_order_warenwert = to_decimal("0.0")
    disc_list_brutto = to_decimal("0.0")
    amt:decimal = to_decimal("0.0")
    l_artikel = l_order = None

    l_art1 = None

    L_art1 = create_buffer("L_art1",L_artikel)

    db_session = local_storage.db_session

    def generate_output():
        nonlocal t_l_order_quality, t_l_order_einzelpreis, t_l_order_warenwert, disc_list_brutto, amt, l_artikel, l_order
        nonlocal t_amount, anzahl, disc_list_disc, disc_list_disc2, disc_list_vat, disc_list_price0, disc_list_disc_val, disc_list_disc2_val, disc_list_vat_val, rec_id
        nonlocal l_art1


        nonlocal l_art1
        return {"t_amount": t_amount, "t_l_order_quality": t_l_order_quality, "t_l_order_einzelpreis": t_l_order_einzelpreis, "t_l_order_warenwert": t_l_order_warenwert, "disc_list_brutto": disc_list_brutto}


    l_order = db_session.query(L_order).filter(
             (L_order._recid == rec_id)).first()
    l_order.quality = to_string(disc_list_disc, "99.99 ") + to_string(disc_list_vat, "99.99") + to_string(disc_list_disc2, " 99.99") + to_string(disc_list_disc_val, " >,>>>,>>>,>>9.999") + to_string(disc_list_disc2_val, " >,>>>,>>>,>>9.999") + to_string(disc_list_vat_val, " >,>>>,>>>,>>9.999")
    amt =  to_decimal(l_order.warenwert)

    l_art1 = db_session.query(L_art1).filter(
                 (L_art1.artnr == l_order.artnr)).first()
    disc_list_brutto =  to_decimal(disc_list_price0) * to_decimal(anzahl)
    l_order.warenwert = ( to_decimal(disc_list_brutto) - to_decimal(disc_list_disc_val) - to_decimal(disc_list_disc2_val) + to_decimal(disc_list_vat_val))
    l_order.einzelpreis =  to_decimal(l_order.warenwert) / to_decimal(l_order.anzahl)

    if not l_order.flag:
        l_order.warenwert =  to_decimal(l_order.warenwert) * to_decimal(l_art1.lief_einheit)
    t_amount =  to_decimal(t_amount) - to_decimal(amt) + to_decimal(l_order.warenwert)
    t_l_order_quality = l_order.quality
    t_l_order_einzelpreis =  to_decimal(l_order.einzelpreis)
    t_l_order_warenwert =  to_decimal(l_order.warenwert)


    return generate_output()