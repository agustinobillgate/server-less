#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import L_orderhdr, Bediener, L_order, L_artikel, L_lieferant

s_list_list, S_list = create_model("S_list", {"selected":bool, "flag":bool, "loeschflag":int, "approved":bool, "rejected":bool, "s_recid":int, "docu_nr":string, "po_nr":string, "deptnr":int, "str0":string, "bestelldatum":string, "lieferdatum":string, "pos":int, "artnr":int, "bezeich":string, "qty":Decimal, "str3":string, "dunit":string, "lief_einheit":Decimal, "str4":string, "userinit":string, "pchase_nr":string, "pchase_date":date, "app_rej":string, "rej_reason":string, "cid":string, "cdate":date, "instruct":string, "konto":string, "supno":int, "currno":int, "duprice":Decimal, "du_price1":Decimal, "du_price2":Decimal, "du_price3":Decimal, "anzahl":int, "txtnr":int, "suppn1":string, "supp1":int, "suppn2":string, "supp2":int, "suppn3":string, "supp3":int, "supps":string, "einzelpreis":Decimal, "amount":Decimal, "stornogrund":string, "besteller":string, "lief_fax2":string, "last_pdate":date, "last_pprice":Decimal, "zeit":int, "min_bestand":Decimal, "max_bestand":Decimal, "del_reason":string, "desc_coa":string, "lief_fax3":string, "masseinheit":string, "lief_fax_2":string, "ek_letzter":Decimal, "supplier":string, "vk_preis":Decimal, "a_firma":string, "last_pbook":Decimal}, {"pos": 999999})

def pr_list_ins_list_1bl(s_list_list:[S_list], docu_nr:string):

    prepare_cache ([L_orderhdr, Bediener, L_order, L_artikel, L_lieferant])

    l_orderhdr = bediener = l_order = l_artikel = l_lieferant = None

    s_list = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal l_orderhdr, bediener, l_order, l_artikel, l_lieferant
        nonlocal docu_nr


        nonlocal s_list

        return {"s-list": s_list_list}

    def ins_list():

        nonlocal l_orderhdr, bediener, l_order, l_artikel, l_lieferant
        nonlocal docu_nr


        nonlocal s_list

        nr:int = 0
        usr = None
        Usr =  create_buffer("Usr",Bediener)

        for l_order in db_session.query(L_order).filter(
                 (L_order.docu_nr == (docu_nr).lower()) & (L_order.lief_nr == 0) & (L_order.pos > 0)).order_by(L_order._recid).all():
            nr = l_order._recid

            s_list = query(s_list_list, filters=(lambda s_list: s_list.s_recid == nr), first=True)

            if not s_list:

                l_artikel = get_cache (L_artikel, {"artnr": [(eq, l_order.artnr)]})

                usr = get_cache (Bediener, {"username": [(eq, l_order.lief_fax[0])]})
                s_list = S_list()
                s_list_list.append(s_list)

                s_list.s_recid = l_order._recid
                s_list.docu_nr = l_order.docu_nr
                s_list.pos = l_order.pos
                s_list.artnr = l_artikel.artnr
                s_list.bezeich = l_artikel.bezeich
                s_list.qty =  to_decimal(l_order.anzahl)
                s_list.dunit = l_artikel.traubensorte
                s_list.lief_einheit =  to_decimal(l_artikel.lief_einheit)
                s_list.pchase_date = l_order.bestelldatum
                s_list.konto = l_order.stornogrund
                s_list.userinit = usr.userinit
                s_list.instruct = l_order.besteller
                s_list.supno = l_order.angebot_lief[1]
                s_list.currno = l_order.angebot_lief[2]
                s_list.duprice =  to_decimal(l_order.einzelpreis)
                s_list.anzahl = l_order.anzahl
                s_list.txtnr = l_order.txtnr
                s_list.einzelpreis =  to_decimal(l_order.einzelpreis)
                s_list.zeit = l_order.zeit
                s_list.masseinheit = l_artikel.masseinheit
                s_list.lief_fax_2 = l_order.lief_fax[1]
                s_list.vk_preis =  to_decimal(l_artikel.vk_preis)

                if l_order.bestellart != "":
                    s_list.du_price1 =  to_decimal(to_int(entry(1 , entry(0 , l_order.bestellart , "-") , ";"))) / to_decimal("100")
                    s_list.du_price2 =  to_decimal(to_int(entry(1 , entry(1 , l_order.bestellart , "-") , ";"))) / to_decimal("100")
                    s_list.du_price3 =  to_decimal(to_int(entry(1 , entry(2 , l_order.bestellart , "-") , ";"))) / to_decimal("100")
                    s_list.supp1 = to_int(entry(0, entry(0, l_order.bestellart , "-") , ";"))
                    s_list.supp2 = to_int(entry(0, entry(1, l_order.bestellart , "-") , ";"))
                    s_list.supp3 = to_int(entry(0, entry(2, l_order.bestellart , "-") , ";"))

                l_lieferant = get_cache (L_lieferant, {"lief_nr": [(eq, s_list.supp1)]})

                if l_lieferant:
                    s_list.suppn1 = l_lieferant.firma

                l_lieferant = get_cache (L_lieferant, {"lief_nr": [(eq, s_list.supp2)]})

                if l_lieferant:
                    s_list.suppn2 = l_lieferant.firma

                l_lieferant = get_cache (L_lieferant, {"lief_nr": [(eq, s_list.supp3)]})

                if l_lieferant:
                    s_list.suppn3 = l_lieferant.firma

                l_lieferant = get_cache (L_lieferant, {"lief_nr": [(eq, s_list.supno)]})

                if l_lieferant:
                    s_list.supps = l_lieferant.firma

                if l_order.anzahl != 0:
                    s_list.str3 = to_string(l_order.anzahl, ">>>,>>9.99")

                if l_artikel.lief_einheit != 0:
                    s_list.str4 = to_string(l_artikel.lief_einheit, ">>,>>9")

                if l_order.lieferdatum != None:
                    s_list.lieferdatum = to_string(l_order.lieferdatum)

    ins_list()

    for s_list in query(s_list_list):

        l_orderhdr = get_cache (L_orderhdr, {"docu_nr": [(eq, s_list.docu_nr)]})

        if l_orderhdr:
            s_list.lief_fax2 = l_orderhdr.lief_fax[1]
            s_list.lief_fax3 = l_orderhdr.lief_fax[2]

    return generate_output()