#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import L_order, L_artikel, L_orderhdr, Htparam

def mk_po_create_l_orderbl(pos:int, rec_id_l_orderhdr:int, rec_id_l_artikel:int, s_artnr:int, lief_nr:int, docu_nr:string, pr:string, remark:string, price0:Decimal, price1:Decimal, price:Decimal, curr_disc:Decimal, curr_disc2:Decimal, curr_vat:Decimal, qty:Decimal, potype:int, cost_acct:string, new_bez:string, dunit_price:bool, bediener_username:string, t_amount:Decimal):

    prepare_cache ([L_order, L_artikel, L_orderhdr, Htparam])

    put_disc = False
    amount = to_decimal("0.0")
    fl_code = 0
    p_222 = False
    t_l_order_data = []
    disc_list_data = []
    bemerkung:string = ""
    globaldisc:Decimal = to_decimal("0.0")
    disc_value1:Decimal = to_decimal("0.0")
    disc_value2:Decimal = to_decimal("0.0")
    disc_vat:Decimal = to_decimal("0.0")
    l_order = l_artikel = l_orderhdr = htparam = None

    t_l_order = disc_list = None

    t_l_order_data, T_l_order = create_model_like(L_order, {"rec_id":int, "a_bezeich":string, "lief_einheit":Decimal})
    disc_list_data, Disc_list = create_model("Disc_list", {"l_recid":int, "price0":Decimal, "brutto":Decimal, "disc":Decimal, "disc2":Decimal, "vat":Decimal, "disc_val":Decimal, "disc2_val":Decimal, "vat_val":Decimal})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal put_disc, amount, fl_code, p_222, t_l_order_data, disc_list_data, bemerkung, globaldisc, disc_value1, disc_value2, disc_vat, l_order, l_artikel, l_orderhdr, htparam
        nonlocal pos, rec_id_l_orderhdr, rec_id_l_artikel, s_artnr, lief_nr, docu_nr, pr, remark, price0, price1, price, curr_disc, curr_disc2, curr_vat, qty, potype, cost_acct, new_bez, dunit_price, bediener_username, t_amount


        nonlocal t_l_order, disc_list
        nonlocal t_l_order_data, disc_list_data

        return {"pos": pos, "t_amount": t_amount, "put_disc": put_disc, "amount": amount, "fl_code": fl_code, "p_222": p_222, "t-l-order": t_l_order_data, "disc-list": disc_list_data}

    def create_l_order():

        nonlocal put_disc, amount, fl_code, p_222, t_l_order_data, disc_list_data, bemerkung, globaldisc, disc_value1, disc_value2, disc_vat, l_order, l_artikel, l_orderhdr, htparam
        nonlocal pos, rec_id_l_orderhdr, rec_id_l_artikel, s_artnr, lief_nr, docu_nr, pr, remark, price0, price1, price, curr_disc, curr_disc2, curr_vat, qty, potype, cost_acct, new_bez, dunit_price, bediener_username, t_amount


        nonlocal t_l_order, disc_list
        nonlocal t_l_order_data, disc_list_data

        l_od = None
        bruto:Decimal = to_decimal("0.0")
        L_od =  create_buffer("L_od",L_order)

        if pos == 0:
            l_od = L_order()
            db_session.add(l_od)

            l_od.docu_nr = docu_nr
            l_od.pos = 0
            l_od.bestelldatum = l_orderhdr.bestelldatum
            l_od.lief_nr = lief_nr
            l_od.op_art = 2
            l_od.lief_fax[0] = pr
            l_od.betriebsnr = 2

            htparam = get_cache (Htparam, {"paramnr": [(eq, 222)]})
            p_222 = htparam.flogical
            fl_code = 1
        pos = pos + 1
        l_order = L_order()
        db_session.add(l_order)

        l_order.docu_nr = docu_nr
        l_order.artnr = s_artnr
        l_order.pos = pos
        l_order.bestelldatum = l_orderhdr.bestelldatum
        l_order.besteller = bemerkung
        l_order.lief_nr = lief_nr
        l_order.op_art = 2
        l_order.lief_fax[0] = bediener_username
        l_order.lief_fax[2] = l_artikel.traubensorte
        l_order.betriebsnr = 2


        disc_list = Disc_list()
        disc_list_data.append(disc_list)

        disc_list.l_recid = l_order._recid
        disc_list.price0 =  to_decimal(price0)
        disc_list.disc =  to_decimal(curr_disc)
        disc_list.disc2 =  to_decimal(curr_disc2)
        disc_list.vat =  to_decimal(curr_vat)


        l_order.anzahl =  to_decimal(qty)
        l_order.einzelpreis =  to_decimal(price)

        if potype == 2:
            l_order.stornogrund = to_string(cost_acct, "x(12)")
        else:
            l_order.stornogrund = to_string(" ", "x(12)")
        l_order.stornogrund = l_order.stornogrund + new_bez

        if l_artikel.lief_einheit != 0:

            if dunit_price:
                l_order.warenwert =  to_decimal(qty) * to_decimal(price)
                disc_list.brutto =  to_decimal(disc_list.price0) * to_decimal(qty)
                bruto =  to_decimal(price1) * to_decimal(qty)
            else:
                l_order.warenwert =  to_decimal(qty) * to_decimal(price) * to_decimal(l_artikel.lief_einheit)
                disc_list.brutto =  to_decimal(disc_list.price0) * to_decimal(qty) * to_decimal(l_artikel.lief_einheit)
                bruto =  to_decimal(price1) * to_decimal(qty) * to_decimal(l_artikel.lief_einheit)
            l_order.txtnr = l_artikel.lief_einheit
        else:
            l_order.warenwert =  to_decimal(qty) * to_decimal(price)
            l_order.txtnr = 1
            disc_list.brutto =  to_decimal(disc_list.price0) * to_decimal(l_order.anzahl)
            bruto =  to_decimal(price1) * to_decimal(l_order.anzahl)
        l_order.flag = dunit_price
        l_order.quality = to_string(curr_disc, "99.99 ") + to_string(curr_vat, "99.99") + to_string(curr_disc2, " 99.99") + to_string(disc_value1, " >,>>>,>>>,>>9.999") + to_string(disc_value2, " >,>>>,>>>,>>9.999") + to_string(disc_vat, " >,>>>,>>>,>>9.999")
        l_order.quality = l_order.quality
        put_disc = False
        amount =  to_decimal(l_order.warenwert)
        t_amount =  to_decimal(t_amount) + to_decimal(l_order.warenwert)
        disc_list.disc_val = ( to_decimal(curr_disc) / to_decimal(100)) * to_decimal(disc_list.brutto)
        disc_list.disc2_val = ( to_decimal(curr_disc2) / to_decimal(100)) * to_decimal(bruto)
        disc_list.vat_val = ( to_decimal(curr_vat) / to_decimal(100)) * to_decimal(amount)
        pass

        l_od = get_cache (L_order, {"docu_nr": [(eq, docu_nr)],"pos": [(eq, 0)],"lief_nr": [(eq, lief_nr)],"op_art": [(eq, 2)]})
        l_od.warenwert =  to_decimal(globaldisc)


        pass


    bemerkung = entry(0, remark, chr_unicode(2))

    if num_entries(remark, chr_unicode(2)) > 1:
        globaldisc =  to_decimal(to_decimal(entry(1 , remark , chr_unicode(2)))) / to_decimal("100")
        disc_value1 =  to_decimal(to_decimal(entry(2 , remark , chr_unicode(2))) )
        disc_value2 =  to_decimal(to_decimal(entry(3 , remark , chr_unicode(2))) )
        disc_vat =  to_decimal(to_decimal(entry(4 , remark , chr_unicode(2))) )

    l_artikel = get_cache (L_artikel, {"artnr": [(eq, s_artnr)]})

    if not l_artikel:

        return generate_output()

    l_orderhdr = get_cache (L_orderhdr, {"_recid": [(eq, rec_id_l_orderhdr)]})

    l_artikel = get_cache (L_artikel, {"_recid": [(eq, rec_id_l_artikel)]})
    create_l_order()

    for l_order in db_session.query(L_order).filter(
             (L_order.docu_nr == (docu_nr).lower()) & (L_order.pos > 0)).order_by(L_order._recid).all():
        t_l_order = T_l_order()
        t_l_order_data.append(t_l_order)

        buffer_copy(l_order, t_l_order)
        t_l_order.rec_id = l_order._recid

        l_artikel = get_cache (L_artikel, {"artnr": [(eq, l_order.artnr)]})
        t_l_order.a_bezeich = l_artikel.bezeich
        t_l_order.lief_einheit =  to_decimal(l_artikel.lief_einheit)

    return generate_output()