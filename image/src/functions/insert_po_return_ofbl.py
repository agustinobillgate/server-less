from functions.additional_functions import *
import decimal
from models import L_artikel, L_order

def insert_po_return_ofbl(rec_id:int, l_order_anzahl:decimal, l_order_einzelpreis:decimal, disc_list_disc:str, disc_list_disc2:str, disc_list_vat:decimal, t_amount:decimal):
    amt = 0
    l_order_warenwert = 0
    l_order_quality = ""
    l_artikel = l_order = None

    l_art1 = None

    L_art1 = L_artikel

    db_session = local_storage.db_session

    def generate_output():
        nonlocal amt, l_order_warenwert, l_order_quality, l_artikel, l_order
        nonlocal l_art1


        nonlocal l_art1
        return {"amt": amt, "l_order_warenwert": l_order_warenwert, "l_order_quality": l_order_quality}


    l_order = db_session.query(L_order).filter(
            (L_order._recid == rec_id)).first()

    l_order = db_session.query(L_order).first()
    l_order.anzahl = l_order_anzahl

    if l_order.flag:
        amt = l_order.warenwert
        l_order.warenwert = decimal.Decimal(l_order_anzahl) * decimal.Decimal(l_order_einzelpreis) * (1 - decimal.Decimal(disc_list_disc) / 100) * (1 - decimal.Decimal(disc_list_disc2) / 100) * (1 + decimal.Decimal(disc_list_vat) / 100)
        l_order.quality = to_string(decimal.Decimal(disc_list_disc) , "99.99 ") + to_string(decimal.Decimal(disc_list_vat) , "99.99") + to_string(decimal.Decimal(disc_list_disc) , " 99.99")
        t_amount = t_amount - amt + l_order.warenwert
        l_order_warenwert = l_order.warenwert
        l_order_quality = l_order.quality
    else:
        amt = l_order.warenwert

        l_art1 = db_session.query(L_art1).filter(
                    (L_art1.artnr == l_order.artnr)).first()
        l_order.warenwert = decimal.Decimal(l_order_anzahl) * decimal.Decimal(l_order_einzelpreis) * (1 - decimal.Decimal(disc_list_disc) / 100) * (1 - decimal.Decimal(disc_list_disc2) / 100) * (1 + decimal.Decimal(disc_list_vat) / 100) * l_art1.lief_einheit
        l_order.quality = to_string(decimal.Decimal(disc_list_disc) , "99.99 ") + to_string(decimal.Decimal(disc_list_vat) , "99.99") + to_string(decimal.Decimal(disc_list_disc) , " 99.99")
        t_amount = t_amount - amt + l_order.warenwert
        l_order_warenwert = l_order.warenwert
        l_order_quality = l_order.quality

    l_order = db_session.query(L_order).first()


    return generate_output()