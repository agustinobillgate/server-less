#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import L_order

def insert_po_create_l_orderbl(pos:int, t_amount:Decimal, docu_nr:string, s_artnr:int, dunit_price:bool, price:Decimal, curr_disc:Decimal, curr_disc2:Decimal, curr_vat:Decimal, qty:Decimal, potype:int, cost_acct:string, new_bez:string, t_l_artikel_lief_einheit:Decimal, bemerkung:string, lief_nr:int, t_l_artikel_traubensort:string, l_orderhdr_bestelldatum:date, billdate:date, bediener_username:string):
    amount = to_decimal("0.0")
    disc_list_list = []
    t_l_order_list = []
    l_order = None

    disc_list = t_l_order = None

    disc_list_list, Disc_list = create_model("Disc_list", {"l_recid":int, "price0":Decimal, "brutto":Decimal, "disc":Decimal, "disc2":Decimal, "vat":Decimal, "new_created":bool})
    t_l_order_list, T_l_order = create_model_like(L_order, {"rec_id":int})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal amount, disc_list_list, t_l_order_list, l_order
        nonlocal pos, t_amount, docu_nr, s_artnr, dunit_price, price, curr_disc, curr_disc2, curr_vat, qty, potype, cost_acct, new_bez, t_l_artikel_lief_einheit, bemerkung, lief_nr, t_l_artikel_traubensort, l_orderhdr_bestelldatum, billdate, bediener_username


        nonlocal disc_list, t_l_order
        nonlocal disc_list_list, t_l_order_list

        return {"pos": pos, "t_amount": t_amount, "amount": amount, "disc-list": disc_list_list, "t-l-order": t_l_order_list}

    def create_l_order():

        nonlocal amount, disc_list_list, t_l_order_list, l_order
        nonlocal pos, t_amount, docu_nr, s_artnr, dunit_price, price, curr_disc, curr_disc2, curr_vat, qty, potype, cost_acct, new_bez, t_l_artikel_lief_einheit, bemerkung, lief_nr, t_l_artikel_traubensort, l_orderhdr_bestelldatum, billdate, bediener_username


        nonlocal disc_list, t_l_order
        nonlocal disc_list_list, t_l_order_list

        price0:Decimal = to_decimal("0.0")
        price0 =  to_decimal(price)
        price =  to_decimal(price) * to_decimal((1) - to_decimal(curr_disc) / to_decimal(100))
        price =  to_decimal(price) * to_decimal((1) - to_decimal(curr_disc2) / to_decimal(100))
        price =  to_decimal(price) * to_decimal((1) + to_decimal(curr_vat) / to_decimal(100))
        pos = pos + 1
        l_order = L_order()
        db_session.add(l_order)

        l_order.docu_nr = docu_nr
        l_order.artnr = s_artnr
        l_order.anzahl =  to_decimal(qty)
        l_order.einzelpreis =  to_decimal(price)

        if potype == 2:
            l_order.stornogrund = to_string(cost_acct, "x(12)")
        else:
            l_order.stornogrund = to_string(" ", "x(12)")
        l_order.stornogrund = l_order.stornogrund + new_bez

        if t_l_artikel_lief_einheit != 0:

            if dunit_price:
                l_order.warenwert =  to_decimal(qty) * to_decimal(price)
            else:
                l_order.warenwert =  to_decimal(qty) * to_decimal(price) * to_decimal(t_l_artikel_lief_einheit)
            l_order.txtnr = t_l_artikel_lief_einheit
        else:
            l_order.warenwert =  to_decimal(qty) * to_decimal(price)
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
        disc_list.disc =  to_decimal(curr_disc)
        disc_list.disc2 =  to_decimal(curr_disc2)
        disc_list.vat =  to_decimal(curr_vat)
        disc_list.price0 =  to_decimal(l_order.einzelpreis) / to_decimal((1) - to_decimal(disc_list.disc) * to_decimal(0.01)) /\
                (1 - to_decimal(disc_list.disc2) * to_decimal(0.01)) / to_decimal((1) + to_decimal(disc_list.vat) * to_decimal(0.01) )


        disc_list.brutto =  to_decimal(disc_list.price0) * to_decimal(l_order.anzahl)
        amount =  to_decimal(l_order.warenwert)
        t_amount =  to_decimal(t_amount) + to_decimal(l_order.warenwert)
        pass

        for l_order in db_session.query(L_order).filter(
                 (L_order.docu_nr == (docu_nr).lower()) & (L_order.pos > 0) & (L_order.loeschflag == 0)).order_by(L_order._recid).all():
            t_l_order = T_l_order()
            t_l_order_list.append(t_l_order)

            buffer_copy(l_order, t_l_order)
            t_l_order.rec_id = l_order._recid


    create_l_order()

    return generate_output()