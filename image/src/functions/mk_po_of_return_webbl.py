from functions.additional_functions import *
import decimal
from models import L_order, L_artikel

def mk_po_of_return_webbl(t_amount:decimal, t_l_order:[T_l_order], disc_list:[Disc_list]):
    t_l_order_quality = ""
    t_l_order_einzelpreis = 0
    t_l_order_warenwert = 0
    disc_list_brutto = 0
    amt:decimal = 0
    l_order = l_artikel = None

    disc_list = t_l_order = l_art1 = None

    disc_list_list, Disc_list = create_model("Disc_list", {"l_recid":int, "price0":decimal, "brutto":decimal, "disc":decimal, "disc2":decimal, "vat":decimal, "disc_val":decimal, "disc2_val":decimal, "vat_val":decimal})
    t_l_order_list, T_l_order = create_model_like(L_order, {"rec_id":int, "a_bezeich":str, "lief_einheit":str})

    L_art1 = L_artikel

    db_session = local_storage.db_session

    def generate_output():
        nonlocal t_l_order_quality, t_l_order_einzelpreis, t_l_order_warenwert, disc_list_brutto, amt, l_order, l_artikel
        nonlocal l_art1


        nonlocal disc_list, t_l_order, l_art1
        nonlocal disc_list_list, t_l_order_list
        return {"t_l_order_quality": t_l_order_quality, "t_l_order_einzelpreis": t_l_order_einzelpreis, "t_l_order_warenwert": t_l_order_warenwert, "disc_list_brutto": disc_list_brutto}


    l_order = db_session.query(L_order).filter(
            (L_order._recid == t_L_order.rec_id)).first()

    l_order = db_session.query(L_order).first()
    l_order.quality = to_string(disc_list.disc, "99.99 ") + to_string(disc_list.vat, "99.99") + to_string(disc_list.disc2, " 99.99") + to_string(disc_list.disc_val, " >,>>>,>>>,>>9.999") + to_string(disc_list.disc2_val, " >,>>>,>>>,>>9.999") + to_string(disc_list.vat_val, " >,>>>,>>>,>>9.999")
    amt = l_order.warenwert

    l_art1 = db_session.query(L_art1).filter(
                (L_art1.artnr == l_order.artnr)).first()
    disc_list_brutto = disc_list.price0 * t_l_order.anzahl
    l_order.warenwert = (disc_list_brutto - disc_list.disc_val - disc_list.disc2_val + disc_list.vat_val)
    l_order.einzelpreis = l_order.warenwert / l_order.anzahl

    if not l_order.flag:
        l_order.warenwert = l_order.warenwert * l_art1.lief_einheit
    t_amount = t_amount - amt + l_order.warenwert
    t_l_order_quality = l_order.quality
    t_l_order_einzelpreis = l_order.einzelpreis
    t_l_order_warenwert = l_order.warenwert

    l_order = db_session.query(L_order).first()


    return generate_output()