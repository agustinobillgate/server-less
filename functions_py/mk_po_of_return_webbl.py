#using conversion tools version: 1.0.0.117
#-------------------------------------------------------
# Rd, 01/12/2025, with_for_update added
#-------------------------------------------------------
from functions.additional_functions import *
from decimal import Decimal
from models import L_order, L_artikel

t_l_order_data, T_l_order = create_model_like(L_order, {"rec_id":int, "a_bezeich":string, "lief_einheit":string})
disc_list_data, Disc_list = create_model("Disc_list", {"l_recid":int, "price0":Decimal, "brutto":Decimal, "disc":Decimal, "disc2":Decimal, "vat":Decimal, "disc_val":Decimal, "disc2_val":Decimal, "vat_val":Decimal})

def mk_po_of_return_webbl(t_amount:Decimal, t_l_order_data:[T_l_order], disc_list_data:[Disc_list]):

    prepare_cache ([L_order, L_artikel])

    t_l_order_quality = ""
    t_l_order_einzelpreis = to_decimal("0.0")
    t_l_order_warenwert = to_decimal("0.0")
    disc_list_brutto = to_decimal("0.0")
    amt:Decimal = to_decimal("0.0")
    l_order = l_artikel = None

    disc_list = t_l_order = l_art1 = None

    L_art1 = create_buffer("L_art1",L_artikel)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal t_l_order_quality, t_l_order_einzelpreis, t_l_order_warenwert, disc_list_brutto, amt, l_order, l_artikel
        nonlocal t_amount
        nonlocal l_art1
        nonlocal disc_list, t_l_order, l_art1

        return {"t_amount": t_amount, "t_l_order_quality": t_l_order_quality, "t_l_order_einzelpreis": t_l_order_einzelpreis, "t_l_order_warenwert": t_l_order_warenwert, "disc_list_brutto": disc_list_brutto}


    # l_order = get_cache (L_order, {"_recid": [(eq, t_l_order.rec_id)]})
    l_order = db_session.query(L_order).filter(
                 (L_order._recid == t_l_order.rec_id)).with_for_update().first()
    
    l_order.quality = to_string(disc_list.disc, "99.99 ") + to_string(disc_list.vat, "99.99") + to_string(disc_list.disc2, " 99.99") + to_string(disc_list.disc_val, " >,>>>,>>>,>>9.999") + to_string(disc_list.disc2_val, " >,>>>,>>>,>>9.999") + to_string(disc_list.vat_val, " >,>>>,>>>,>>9.999")
    amt =  to_decimal(l_order.warenwert)

    l_art1 = get_cache (L_artikel, {"artnr": [(eq, l_order.artnr)]})
    disc_list_brutto =  to_decimal(disc_list.price0) * to_decimal(t_l_order.anzahl)
    l_order.warenwert = ( to_decimal(disc_list_brutto) - to_decimal(disc_list.disc_val) - to_decimal(disc_list.disc2_val) + to_decimal(disc_list.vat_val))
    l_order.einzelpreis =  to_decimal(l_order.warenwert) / to_decimal(l_order.anzahl)

    if not l_order.flag:
        l_order.warenwert =  to_decimal(l_order.warenwert) * to_decimal(l_art1.lief_einheit)
    t_amount =  to_decimal(t_amount) - to_decimal(amt) + to_decimal(l_order.warenwert)
    t_l_order_quality = l_order.quality
    t_l_order_einzelpreis =  to_decimal(l_order.einzelpreis)
    t_l_order_warenwert =  to_decimal(l_order.warenwert)
    pass

    return generate_output()