from functions.additional_functions import *
import decimal
from datetime import date
from sqlalchemy import func
from models import L_orderhdr, Bediener, L_order, L_artikel, L_lieferant

def pr_list_ins_list_1bl(s_list:[S_list], docu_nr:str):
    l_orderhdr = bediener = l_order = l_artikel = l_lieferant = None

    s_list = usr = None

    s_list_list, S_list = create_model("S_list", {"selected":bool, "flag":bool, "loeschflag":int, "approved":bool, "rejected":bool, "s_recid":int, "docu_nr":str, "po_nr":str, "deptnr":int, "str0":str, "bestelldatum":str, "lieferdatum":str, "pos":int, "artnr":int, "bezeich":str, "qty":decimal, "str3":str, "dunit":str, "lief_einheit":decimal, "str4":str, "userinit":str, "pchase_nr":str, "pchase_date":date, "app_rej":str, "rej_reason":str, "cid":str, "cdate":date, "instruct":str, "konto":str, "supno":int, "currno":int, "duprice":decimal, "du_price1":decimal, "du_price2":decimal, "du_price3":decimal, "anzahl":int, "txtnr":int, "suppn1":str, "supp1":int, "suppn2":str, "supp2":int, "suppn3":str, "supp3":int, "supps":str, "einzelpreis":decimal, "amount":decimal, "stornogrund":str, "besteller":str, "lief_fax2":str, "last_pdate":date, "last_pprice":decimal, "zeit":int, "min_bestand":decimal, "max_bestand":decimal, "del_reason":str, "desc_coa":str, "lief_fax3":str, "masseinheit":str, "lief_fax_2":str, "ek_letzter":decimal, "supplier":str, "vk_preis":decimal, "a_firma":str, "last_pbook":decimal}, {"pos": 999999})

    Usr = Bediener

    db_session = local_storage.db_session

    def generate_output():
        nonlocal l_orderhdr, bediener, l_order, l_artikel, l_lieferant
        nonlocal usr


        nonlocal s_list, usr
        nonlocal s_list_list
        return {}

    def ins_list():

        nonlocal l_orderhdr, bediener, l_order, l_artikel, l_lieferant
        nonlocal usr


        nonlocal s_list, usr
        nonlocal s_list_list

        nr:int = 0
        Usr = Bediener

        for l_order in db_session.query(L_order).filter(
                (func.lower(L_order.(docu_nr).lower()) == (docu_nr).lower()) &  (L_order.lief_nr == 0) &  (L_order.pos > 0)).all():
            nr = l_order._recid

            s_list = query(s_list_list, filters=(lambda s_list :s_list.s_recid == nr), first=True)

            if not s_list:

                l_artikel = db_session.query(L_artikel).filter(
                        (L_artikel.artnr == l_order.artnr)).first()

                usr = db_session.query(Usr).filter(
                        (Usr.username == l_order.lief_fax[0])).first()
                s_list = S_list()
                s_list_list.append(s_list)

                s_list.s_recid = l_order._recid
                s_list.docu_nr = l_order.docu_nr
                s_list.pos = l_order.pos
                s_list.artnr = l_artikel.artnr
                s_list.bezeich = l_artikel.bezeich
                s_list.qty = l_order.anzahl
                s_list.dunit = l_artikel.traubensort
                s_list.lief_einheit = l_artikel.lief_einheit
                s_list.pchase_date = l_order.bestelldatum
                s_list.konto = l_order.stornogrund
                s_list.userinit = usr.userinit
                s_list.instruct = l_order.besteller
                s_list.supNo = l_order.angebot_lief[1]
                s_list.currNo = l_order.angebot_lief[2]
                s_list.duprice = l_order.einzelpreis
                s_list.anzahl = l_order.anzahl
                s_list.txtnr = l_order.txtnr
                s_list.einzelpreis = l_order.einzelpreis
                s_list.zeit = l_order.zeit
                s_list.masseinheit = l_artikel.masseinheit
                s_list.lief_fax_2 = l_order.lief_fax[1]
                s_list.vk_preis = l_artikel.vk_preis

                if l_order.bestellart != "":
                    s_list.du_price1 = to_int(entry(1, entry(0, l_order.bestellart , "-") , ";")) / 100
                    s_list.du_price2 = to_int(entry(1, entry(1, l_order.bestellart , "-") , ";")) / 100
                    s_list.du_price3 = to_int(entry(1, entry(2, l_order.bestellart , "-") , ";")) / 100
                    s_list.supp1 = to_int(entry(0, entry(0, l_order.bestellart , "-") , ";"))
                    s_list.supp2 = to_int(entry(0, entry(1, l_order.bestellart , "-") , ";"))
                    s_list.supp3 = to_int(entry(0, entry(2, l_order.bestellart , "-") , ";"))

                l_lieferant = db_session.query(L_lieferant).filter(
                        (L_lieferant.lief_nr == s_list.supp1)).first()

                if l_lieferant:
                    s_list.suppn1 = l_lieferant.firma

                l_lieferant = db_session.query(L_lieferant).filter(
                        (L_lieferant.lief_nr == s_list.supp2)).first()

                if l_lieferant:
                    s_list.suppn2 = l_lieferant.firma

                l_lieferant = db_session.query(L_lieferant).filter(
                        (L_lieferant.lief_nr == s_list.supp3)).first()

                if l_lieferant:
                    s_list.suppn3 = l_lieferant.firma

                l_lieferant = db_session.query(L_lieferant).filter(
                        (L_lieferant.lief_nr == s_list.supNo)).first()

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

        l_orderhdr = db_session.query(L_orderhdr).filter(
                (L_orderhdr.docu_nr == s_list.docu_nr)).first()

        if l_orderhdr:
            s_list.lief_fax2 = l_orderhdr.lief_fax[1]
            s_list.lief_fax3 = l_orderhdr.lief_fax[2]

    return generate_output()