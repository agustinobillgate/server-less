#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import L_order, Htparam, L_lieferant, L_orderhdr

def outstand_polist_btn_gobl(from_date:date, to_date:date):

    prepare_cache ([L_order, Htparam, L_lieferant, L_orderhdr])

    exp_polist_data = []
    billdate:date = None
    l_order = htparam = l_lieferant = l_orderhdr = None

    exp_polist = l_order1 = l_order2 = None

    exp_polist_data, Exp_polist = create_model("Exp_polist", {"bestelldatum":date, "firma":string, "docu_nr":string, "lieferdatum":date, "anzahl":Decimal, "warenwert":Decimal, "geliefert":Decimal, "rechnungswert":Decimal, "hlief_fax":[string,3], "bestellart":string, "gedruckt":date, "besteller":string, "lief_fax":[string,3], "lieferdatum1":date, "lieferdatum_eff":date})

    L_order1 = create_buffer("L_order1",L_order)
    L_order2 = create_buffer("L_order2",L_order)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal exp_polist_data, billdate, l_order, htparam, l_lieferant, l_orderhdr
        nonlocal from_date, to_date
        nonlocal l_order1, l_order2


        nonlocal exp_polist, l_order1, l_order2
        nonlocal exp_polist_data

        return {"exp-polist": exp_polist_data}

    htparam = get_cache (Htparam, {"paramnr": [(eq, 110)]})
    billdate = htparam.fdate

    l_orderhdr_obj_list = {}
    l_orderhdr = L_orderhdr()
    l_lieferant = L_lieferant()
    l_order1 = L_order()
    l_order2 = L_order()
    for l_orderhdr.bestelldatum, l_orderhdr.docu_nr, l_orderhdr.lieferdatum, l_orderhdr.lief_fax, l_orderhdr.bestellart, l_orderhdr.gedruckt, l_orderhdr.besteller, l_orderhdr._recid, l_lieferant.firma, l_lieferant._recid, l_order1.rechnungswert, l_order1.lief_fax, l_order1.lieferdatum, l_order1.lieferdatum_eff, l_order1._recid, l_order1.anzahl, l_order1.warenwert, l_order1.geliefert, l_order2.rechnungswert, l_order2.lief_fax, l_order2.lieferdatum, l_order2.lieferdatum_eff, l_order2._recid, l_order2.anzahl, l_order2.warenwert, l_order2.geliefert in db_session.query(L_orderhdr.bestelldatum, L_orderhdr.docu_nr, L_orderhdr.lieferdatum, L_orderhdr.lief_fax, L_orderhdr.bestellart, L_orderhdr.gedruckt, L_orderhdr.besteller, L_orderhdr._recid, L_lieferant.firma, L_lieferant._recid, L_order1.rechnungswert, L_order1.lief_fax, L_order1.lieferdatum, L_order1.lieferdatum_eff, L_order1._recid, L_order1.anzahl, L_order1.warenwert, L_order1.geliefert, L_order2.rechnungswert, L_order2.lief_fax, L_order2.lieferdatum, L_order2.lieferdatum_eff, L_order2._recid, L_order2.anzahl, L_order2.warenwert, L_order2.geliefert).join(L_lieferant,(L_lieferant.lief_nr == L_orderhdr.lief_nr)).join(L_order1,(L_order1.docu_nr == L_orderhdr.docu_nr) & (L_order1.loeschflag == 0) & (L_order1.pos == 0)).join(L_order2,(L_order2.docu_nr == L_orderhdr.docu_nr) & (L_order2.loeschflag == 0) & (L_order2.pos > 0) & (L_order2.geliefert < L_order2.anzahl)).filter(
             (L_orderhdr.bestelldatum >= from_date) & (L_orderhdr.bestelldatum <= to_date) & (L_orderhdr.lieferdatum >= billdate) & (L_orderhdr.betriebsnr <= 1)).order_by(L_orderhdr.bestelldatum, L_lieferant.firma, L_orderhdr.docu_nr).all():
        if l_orderhdr_obj_list.get(l_orderhdr._recid):
            continue
        else:
            l_orderhdr_obj_list[l_orderhdr._recid] = True


        exp_polist = Exp_polist()
        exp_polist_data.append(exp_polist)

        exp_polist.bestelldatum = l_orderhdr.bestelldatum
        exp_polist.firma = l_lieferant.firma
        exp_polist.docu_nr = l_orderhdr.docu_nr
        exp_polist.lieferdatum = l_orderhdr.lieferdatum
        exp_polist.anzahl =  to_decimal(l_order2.anzahl)
        exp_polist.warenwert =  to_decimal(l_order2.warenwert)
        exp_polist.geliefert =  to_decimal(l_order2.geliefert)
        exp_polist.rechnungswert =  to_decimal(l_order1.rechnungswert)
        exp_polist.hlief_fax[2] = l_orderhdr.lief_fax[2]
        exp_polist.bestellart = l_orderhdr.bestellart
        exp_polist.gedruckt = l_orderhdr.gedruckt
        exp_polist.besteller = l_orderhdr.besteller
        exp_polist.lief_fax[1] = l_order1.lief_fax[1]
        exp_polist.lieferdatum1 = l_order1.lieferdatum
        exp_polist.lief_fax[2] = l_order1.lief_fax[2]
        exp_polist.lieferdatum_eff = l_order1.lieferdatum_eff

    return generate_output()