from functions.additional_functions import *
import decimal
from sqlalchemy import func
from models import L_order, L_artikel, L_orderhdr, Htparam

def mk_po_create_l_orderbl(pos:int, rec_id_l_orderhdr:int, rec_id_l_artikel:int, s_artnr:int, lief_nr:int, docu_nr:str, pr:str, remark:str, price0:decimal, price1:decimal, price:decimal, curr_disc:decimal, curr_disc2:decimal, curr_vat:decimal, qty:decimal, potype:int, cost_acct:str, new_bez:str, dunit_price:bool, bediener_username:str, t_amount:decimal):
    put_disc = False
    amount = 0
    fl_code = 0
    p_222 = False
    t_l_order_list = []
    disc_list_list = []
    bemerkung:str = ""
    globaldisc:decimal = 0
    disc_value1:decimal = 0
    disc_value2:decimal = 0
    disc_vat:decimal = 0
    l_order = l_artikel = l_orderhdr = htparam = None

    t_l_order = disc_list = l_od = None

    t_l_order_list, T_l_order = create_model_like(L_order, {"rec_id":int, "a_bezeich":str, "lief_einheit":decimal})
    disc_list_list, Disc_list = create_model("Disc_list", {"l_recid":int, "price0":decimal, "brutto":decimal, "disc":decimal, "disc2":decimal, "vat":decimal, "disc_val":decimal, "disc2_val":decimal, "vat_val":decimal})

    L_od = L_order

    db_session = local_storage.db_session

    def generate_output():
        nonlocal put_disc, amount, fl_code, p_222, t_l_order_list, disc_list_list, bemerkung, globaldisc, disc_value1, disc_value2, disc_vat, l_order, l_artikel, l_orderhdr, htparam
        nonlocal l_od


        nonlocal t_l_order, disc_list, l_od
        nonlocal t_l_order_list, disc_list_list
        return {"put_disc": put_disc, "amount": amount, "fl_code": fl_code, "p_222": p_222, "t-l-order": t_l_order_list, "disc-list": disc_list_list}

    def create_l_order():

        nonlocal put_disc, amount, fl_code, p_222, t_l_order_list, disc_list_list, bemerkung, globaldisc, disc_value1, disc_value2, disc_vat, l_order, l_artikel, l_orderhdr, htparam
        nonlocal l_od


        nonlocal t_l_order, disc_list, l_od
        nonlocal t_l_order_list, disc_list_list

        bruto:decimal = 0
        L_od = L_order

        if pos == 0:
            l_od = L_od()
            db_session.add(l_od)

            l_od.docu_nr = docu_nr
            l_od.pos = 0
            l_od.bestelldatum = l_orderhdr.bestelldatum
            l_od.lief_nr = lief_nr
            l_od.op_art = 2
            l_od.lief_fax[0] = pr
            l_od.betriebsnr = 2

            htparam = db_session.query(Htparam).filter(
                    (Htparam.paramnr == 222)).first()
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
        l_order.lief_fax[2] = l_artikel.traubensort
        l_order.betriebsnr = 2


        disc_list = Disc_list()
        disc_list_list.append(disc_list)

        disc_list.l_recid = l_order._recid
        disc_list.price0 = price0
        disc_list.disc = curr_disc
        disc_list.disc2 = curr_disc2
        disc_list.vat = curr_vat


        l_order.anzahl = qty
        l_order.einzelpreis = price

        if potype == 2:
            l_order.stornogrund = to_string(cost_acct, "x(12)")
        else:
            l_order.stornogrund = to_string(" ", "x(12)")
        l_order.stornogrund = l_order.stornogrund + new_bez

        if l_artikel.lief_einheit != 0:

            if dunit_price:
                l_order.warenwert = qty * price
                disc_list.brutto = disc_list.price0 * qty
                bruto = price1 * qty
            else:
                l_order.warenwert = qty * price * l_artikel.lief_einheit
                disc_list.brutto = disc_list.price0 * qty * l_artikel.lief_einheit
                bruto = price1 * qty * l_artikel.lief_einheit
            l_order.txtnr = l_artikel.lief_einheit
        else:
            l_order.warenwert = qty * price
            l_order.txtnr = 1
            disc_list.brutto = disc_list.price0 * l_order.anzahl
            bruto = price1 * l_order.anzahl
        l_order.flag = dunit_price
        l_order.quality = to_string(curr_disc, "99.99 ") + to_string(curr_vat, "99.99") + to_string(curr_disc2, " 99.99") + to_string(disc_value1, " >,>>>,>>>,>>9.999") + to_string(disc_value2, " >,>>>,>>>,>>9.999") + to_string(disc_vat, " >,>>>,>>>,>>9.999")
        l_order.quality = l_order.quality
        put_disc = False
        amount = l_order.warenwert
        t_amount = t_amount + l_order.warenwert
        disc_list.disc_val = (curr_disc / 100) * disc_list.brutto
        disc_list.disc2_val = (curr_disc2 / 100) * bruto
        disc_list.vat_val = (curr_vat / 100) * amount


        l_od = db_session.query(L_od).filter(
                (func.lower(L_od.(docu_nr).lower()) == (docu_nr).lower()) &  (L_od.pos == 0) &  (L_od.lief_nr == lief_nr) &  (L_od.op_art == 2)).first()
        l_od.warenwert = globaldisc

        l_od = db_session.query(L_od).first()

    bemerkung = entry(0, remark, chr(2))

    if num_entries(remark, chr(2)) > 1:
        globaldisc = decimal.Decimal(entry(1, remark, chr(2))) / 100
        disc_value1 = decimal.Decimal(entry(2, remark, chr(2)))
        disc_value2 = decimal.Decimal(entry(3, remark, chr(2)))
        disc_vat = decimal.Decimal(entry(4, remark, chr(2)))

    l_artikel = db_session.query(L_artikel).filter(
            (L_artikel.artnr == s_artnr)).first()

    if not l_artikel:

        return generate_output()

    l_orderhdr = db_session.query(L_orderhdr).filter(
            (L_orderhdr._recid == rec_id_l_orderhdr)).first()

    l_artikel = db_session.query(L_artikel).filter(
            (L_artikel._recid == rec_id_l_artikel)).first()
    create_l_order()

    for l_order in db_session.query(L_order).filter(
            (func.lower(L_order.(docu_nr).lower()) == (docu_nr).lower()) &  (L_order.pos > 0)).all():
        t_l_order = T_l_order()
        t_l_order_list.append(t_l_order)

        buffer_copy(l_order, t_l_order)
        t_l_order.rec_id = l_order._recid

        l_artikel = db_session.query(L_artikel).filter(
                (L_artikel.artnr == l_order.artnr)).first()
        t_l_order.a_bezeich = l_artikel.bezeich
        t_l_order.lief_einheit = l_artikel.lief_einheit

    return generate_output()