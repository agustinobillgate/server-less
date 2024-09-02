from functions.additional_functions import *
import decimal
from datetime import date
from sqlalchemy import func
from models import L_order

def insert_po_create_l_orderbl(pos:int, t_amount:decimal, docu_nr:str, s_artnr:int, dunit_price:bool, price:decimal, curr_disc:decimal, curr_disc2:decimal, curr_vat:decimal, qty:decimal, potype:int, cost_acct:str, new_bez:str, t_l_artikel_lief_einheit:decimal, bemerkung:str, lief_nr:int, t_l_artikel_traubensort:str, l_orderhdr_bestelldatum:date, billdate:date, bediener_username:str):
    amount = 0
    disc_list_list = []
    t_l_order_list = []
    l_order = None

    disc_list = t_l_order = None

    disc_list_list, Disc_list = create_model("Disc_list", {"l_recid":int, "price0":decimal, "brutto":decimal, "disc":decimal, "disc2":decimal, "vat":decimal, "new_created":bool})
    t_l_order_list, T_l_order = create_model_like(L_order, {"rec_id":int})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal amount, disc_list_list, t_l_order_list, l_order


        nonlocal disc_list, t_l_order
        nonlocal disc_list_list, t_l_order_list
        return {"amount": amount, "disc-list": disc_list_list, "t-l-order": t_l_order_list}

    def create_l_order():

        nonlocal amount, disc_list_list, t_l_order_list, l_order


        nonlocal disc_list, t_l_order
        nonlocal disc_list_list, t_l_order_list

        price0:decimal = 0
        price0 = price
        price = price * (1 - curr_disc / 100)
        price = price * (1 - curr_disc2 / 100)
        price = price * (1 + curr_vat / 100)
        pos = pos + 1
        l_order = L_order()
        db_session.add(l_order)

        l_order.docu_nr = docu_nr
        l_order.artnr = s_artnr
        l_order.anzahl = qty
        l_order.einzelpreis = price

        if potype == 2:
            l_order.stornogrund = to_string(cost_acct, "x(12)")
        else:
            l_order.stornogrund = to_string(" ", "x(12)")
        l_order.stornogrund = l_order.stornogrund + new_bez

        if t_l_artikel_lief_einheit != 0:

            if dunit_price:
                l_order.warenwert = qty * price
            else:
                l_order.warenwert = qty * price * t_l_artikel_lief_einheit
            l_order.txtnr = t_l_artikel_lief_einheit
        else:
            l_order.warenwert = qty * price
            l_order.txtnr = 1
        l_order.pos = pos
        l_order.bestelldatum = l_orderhdr_bestelldatum
        l_order.besteller = bemerkung
        l_order.lief_nr = lief_nr
        l_order.op_art = 2
        l_order.flag = dunit_price
        l_order.lief_fax[2] = t_l_artikel_traubensort
        l_order.bestelldatum = billdate
        l_order.lief_fax[0] = bediener_username


        l_order.quality = to_string(curr_disc, "99.99 ") + to_string(curr_vat, "99.99") + to_string(curr_disc, " 99.99")
        disc_list = Disc_list()
        disc_list_list.append(disc_list)

        disc_list.new_created = True
        disc_list.l_recid = l_order._recid
        disc_list.disc = curr_disc
        disc_list.disc2 = curr_disc2
        disc_list.vat = curr_vat
        disc_list.price0 = l_order.einzelpreis / (1 - disc_list.disc * 0.01) /\
                (1 - disc_list.disc2 * 0.01) / (1 + disc_list.vat * 0.01)


        disc_list.brutto = disc_list.price0 * l_order.anzahl
        amount = l_order.warenwert
        t_amount = t_amount + l_order.warenwert


        for l_order in db_session.query(L_order).filter(
                (func.lower(L_order.(docu_nr).lower()) == (docu_nr).lower()) &  (L_order.pos > 0) &  (L_order.loeschflag == 0)).all():
            t_l_order = T_l_order()
            t_l_order_list.append(t_l_order)

            buffer_copy(l_order, t_l_order)
            t_l_order.rec_id = l_order._recid

    create_l_order()

    return generate_output()