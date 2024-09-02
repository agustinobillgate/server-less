from functions.additional_functions import *
import decimal
from datetime import date
from models import L_order, Htparam, L_lieferant, L_orderhdr

def expired_polist_btn_gobl(from_date:date, to_date:date):
    exp_polist_list = []
    billdate:date = None
    l_order = htparam = l_lieferant = l_orderhdr = None

    exp_polist = l_order1 = l_order2 = None

    exp_polist_list, Exp_polist = create_model("Exp_polist", {"bestelldatum":date, "firma":str, "docu_nr":str, "lieferdatum":date, "anzahl":decimal, "warenwert":decimal, "geliefert":decimal, "rechnungswert":decimal, "hlief_fax":[str], "bestellart":str, "gedruckt":date, "besteller":str, "lief_fax":[str, 3], "lieferdatum1":date, "lieferdatum_eff":date})

    L_order1 = L_order
    L_order2 = L_order

    db_session = local_storage.db_session

    def generate_output():
        nonlocal exp_polist_list, billdate, l_order, htparam, l_lieferant, l_orderhdr
        nonlocal l_order1, l_order2


        nonlocal exp_polist, l_order1, l_order2
        nonlocal exp_polist_list
        return {"exp-polist": exp_polist_list}

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 110)).first()
    billdate = htparam.fdate

    l_orderhdr_obj_list = []
    for l_orderhdr, l_lieferant, l_order1, l_order2 in db_session.query(L_orderhdr, L_lieferant, L_order1, L_order2).join(L_lieferant,(L_lieferant.lief_nr == L_orderhdr.lief_nr)).join(L_order1,(L_order1.docu_nr == L_orderhdr.docu_nr) &  (L_order1.loeschflag == 0) &  (L_order1.pos == 0)).join(L_order2,(L_order2.docu_nr == L_orderhdr.docu_nr) &  (L_order2.loeschflag == 0) &  (L_order2.pos > 0) &  (L_order2.geliefert < L_order2.anzahl)).filter(
            (L_orderhdr.bestelldatum >= from_date) &  (L_orderhdr.bestelldatum <= to_date) &  (L_orderhdr.lieferdatum < billdate) &  (L_orderhdr.betriebsnr <= 1)).all():
        if l_orderhdr._recid in l_orderhdr_obj_list:
            continue
        else:
            l_orderhdr_obj_list.append(l_orderhdr._recid)


        exp_polist = Exp_polist()
        exp_polist_list.append(exp_polist)

        exp_polist.bestelldatum = l_orderhdr.bestelldatum
        exp_polist.firma = l_lieferant.firma
        exp_polist.docu_nr = l_orderhdr.docu_nr
        exp_polist.lieferdatum = l_orderhdr.lieferdatum
        exp_polist.anzahl = l_order2.anzahl
        exp_polist.warenwert = l_order2.warenwert
        exp_polist.geliefert = l_order2.geliefert
        exp_polist.rechnungswert = l_order1.rechnungswert
        exp_polist.hlief_fax[2] = l_orderhdr.lief_fax[2]
        exp_polist.bestellart = l_orderhdr.bestellart
        exp_polist.gedruckt = l_orderhdr.gedruckt
        exp_polist.besteller = l_orderhdr.besteller
        exp_polist.lief_fax[1] = l_order1.lief_fax[1]
        exp_polist.lieferdatum1 = l_order1.lieferdatum
        exp_polist.lief_fax[2] = l_order1.lief_fax[2]
        exp_polist.lieferdatum_eff = l_order1.lieferdatum_eff

    return generate_output()