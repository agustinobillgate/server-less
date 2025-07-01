#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import L_order, L_artikel, Htparam, L_lieferant, L_orderhdr

def expired_polist_btn_go_webbl(from_date:date, to_date:date):

    prepare_cache ([L_order, L_artikel, Htparam, L_lieferant, L_orderhdr])

    exp_polist_list = []
    exp_polist_items_list = []
    billdate:date = None
    l_order = l_artikel = htparam = l_lieferant = l_orderhdr = None

    exp_polist = exp_polist_items = l_order1 = l_art = None

    exp_polist_list, Exp_polist = create_model("Exp_polist", {"bestelldatum":date, "firma":string, "docu_nr":string, "lieferdatum":date, "anzahl":Decimal, "warenwert":Decimal, "geliefert":Decimal, "rechnungswert":Decimal, "hlief_fax":[string,3], "bestellart":string, "gedruckt":date, "besteller":string, "lief_fax":[string,3], "lieferdatum1":date, "lieferdatum_eff":date})
    exp_polist_items_list, Exp_polist_items = create_model("Exp_polist_items", {"artnr":int, "bezeich":string, "anzahl":Decimal, "einzelpreis":Decimal, "warenwert":Decimal, "docu_nr":string, "lief_fax":[string,3], "geliefert":Decimal, "rechnungspreis":Decimal, "txtnr":int, "lieferdatum_eff":date, "angebot_lief":[int,3], "masseinheit":string, "jahrgang":int, "quality":string, "pos":int, "remark":string})

    L_order1 = create_buffer("L_order1",L_order)
    L_art = create_buffer("L_art",L_artikel)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal exp_polist_list, exp_polist_items_list, billdate, l_order, l_artikel, htparam, l_lieferant, l_orderhdr
        nonlocal from_date, to_date
        nonlocal l_order1, l_art


        nonlocal exp_polist, exp_polist_items, l_order1, l_art
        nonlocal exp_polist_list, exp_polist_items_list

        return {"exp-polist": exp_polist_list, "exp-polist-items": exp_polist_items_list}


    htparam = get_cache (Htparam, {"paramnr": [(eq, 110)]})
    billdate = htparam.fdate

    l_orderhdr_obj_list = {}
    l_orderhdr = L_orderhdr()
    l_lieferant = L_lieferant()
    l_order1 = L_order()
    for l_orderhdr.bestelldatum, l_orderhdr.docu_nr, l_orderhdr.lieferdatum, l_orderhdr.lief_fax, l_orderhdr.bestellart, l_orderhdr.gedruckt, l_orderhdr.besteller, l_orderhdr._recid, l_lieferant.firma, l_lieferant._recid, l_order1.docu_nr, l_order1.artnr, l_order1.anzahl, l_order1.einzelpreis, l_order1.warenwert, l_order1.lief_fax, l_order1.geliefert, l_order1.rechnungspreis, l_order1.txtnr, l_order1.lieferdatum_eff, l_order1.angebot_lief, l_order1.quality, l_order1.pos, l_order1.besteller, l_order1._recid, l_order1.rechnungswert, l_order1.lieferdatum in db_session.query(L_orderhdr.bestelldatum, L_orderhdr.docu_nr, L_orderhdr.lieferdatum, L_orderhdr.lief_fax, L_orderhdr.bestellart, L_orderhdr.gedruckt, L_orderhdr.besteller, L_orderhdr._recid, L_lieferant.firma, L_lieferant._recid, L_order1.docu_nr, L_order1.artnr, L_order1.anzahl, L_order1.einzelpreis, L_order1.warenwert, L_order1.lief_fax, L_order1.geliefert, L_order1.rechnungspreis, L_order1.txtnr, L_order1.lieferdatum_eff, L_order1.angebot_lief, L_order1.quality, L_order1.pos, L_order1.besteller, L_order1._recid, L_order1.rechnungswert, L_order1.lieferdatum).join(L_lieferant,(L_lieferant.lief_nr == L_orderhdr.lief_nr)).join(L_order1,(L_order1.docu_nr == L_orderhdr.docu_nr) & (L_order1.loeschflag == 0) & (L_order1.pos >= 0) & (L_order1.geliefert < L_order1.anzahl)).filter(
             (L_orderhdr.bestelldatum >= from_date) & (L_orderhdr.bestelldatum <= to_date) & (L_orderhdr.lieferdatum < billdate) & (L_orderhdr.betriebsnr <= 1)).order_by(L_orderhdr.bestelldatum, L_lieferant.firma, L_orderhdr.docu_nr).all():
        if l_orderhdr_obj_list.get(l_orderhdr._recid):
            continue
        else:
            l_orderhdr_obj_list[l_orderhdr._recid] = True


        exp_polist = Exp_polist()
        exp_polist_list.append(exp_polist)

        exp_polist.bestelldatum = l_orderhdr.bestelldatum
        exp_polist.firma = l_lieferant.firma
        exp_polist.docu_nr = l_orderhdr.docu_nr
        exp_polist.lieferdatum = l_orderhdr.lieferdatum
        exp_polist.anzahl =  to_decimal(l_order1.anzahl)
        exp_polist.warenwert =  to_decimal(l_order1.warenwert)
        exp_polist.geliefert =  to_decimal(l_order1.geliefert)
        exp_polist.rechnungswert =  to_decimal(l_order1.rechnungswert)
        exp_polist.hlief_fax[2] = l_orderhdr.lief_fax[2]
        exp_polist.bestellart = l_orderhdr.bestellart
        exp_polist.gedruckt = l_orderhdr.gedruckt
        exp_polist.besteller = l_orderhdr.besteller
        exp_polist.lief_fax[1] = l_order1.lief_fax[1]
        exp_polist.lieferdatum1 = l_order1.lieferdatum
        exp_polist.lief_fax[2] = l_order1.lief_fax[2]
        exp_polist.lieferdatum_eff = l_order1.lieferdatum_eff

        l_order_obj_list = {}
        l_order = L_order()
        l_art = L_artikel()
        for l_order.docu_nr, l_order.artnr, l_order.anzahl, l_order.einzelpreis, l_order.warenwert, l_order.lief_fax, l_order.geliefert, l_order.rechnungspreis, l_order.txtnr, l_order.lieferdatum_eff, l_order.angebot_lief, l_order.quality, l_order.pos, l_order.besteller, l_order._recid, l_order.rechnungswert, l_order.lieferdatum, l_art.bezeich, l_art.masseinheit, l_art.jahrgang, l_art._recid in db_session.query(L_order.docu_nr, L_order.artnr, L_order.anzahl, L_order.einzelpreis, L_order.warenwert, L_order.lief_fax, L_order.geliefert, L_order.rechnungspreis, L_order.txtnr, L_order.lieferdatum_eff, L_order.angebot_lief, L_order.quality, L_order.pos, L_order.besteller, L_order._recid, L_order.rechnungswert, L_order.lieferdatum, L_art.bezeich, L_art.masseinheit, L_art.jahrgang, L_art._recid).join(L_art,(L_art.artnr == L_order.artnr)).filter(
                 (L_order.docu_nr == l_orderhdr.docu_nr)).order_by(L_order._recid).all():
            if l_order_obj_list.get(l_order._recid):
                continue
            else:
                l_order_obj_list[l_order._recid] = True


            exp_polist_items = Exp_polist_items()
            exp_polist_items_list.append(exp_polist_items)

            exp_polist_items.docu_nr = l_order.docu_nr
            exp_polist_items.artnr = l_order.artnr
            exp_polist_items.bezeich = l_art.bezeich
            exp_polist_items.anzahl =  to_decimal(l_order.anzahl)
            exp_polist_items.einzelpreis =  to_decimal(l_order.einzelpreis)
            exp_polist_items.warenwert =  to_decimal(l_order.warenwert)
            exp_polist_items.lief_fax = l_order.lief_fax
            exp_polist_items.geliefert =  to_decimal(l_order.geliefert)
            exp_polist_items.rechnungspreis =  to_decimal(l_order.rechnungspreis)
            exp_polist_items.txtnr = l_order.txtnr
            exp_polist_items.lieferdatum_eff = l_order.lieferdatum_eff
            exp_polist_items.angebot_lief = l_order.angebot_lief
            exp_polist_items.masseinheit = l_art.masseinheit
            exp_polist_items.jahrgang = l_art.jahrgang
            exp_polist_items.quality = l_order.quality
            exp_polist_items.pos = l_order.pos
            exp_polist_items.remark = l_order.besteller

    return generate_output()